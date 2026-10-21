#!/usr/bin/env python3
"""Prueba los canales de todos_tus_canales_live.m3u, repara los caidos y
sustituye los SATURADOS por un alias vivo del mismo panel.

Tres estados (el tercero es el que faltaba):
  ALIVE     -> respondio y entrega playlist/TS  -> punto VERDE
  SATURADO  -> respondio 401/429/456/458         -> punto NARANJA
               (la linea existe pero su cupo de conexiones esta lleno;
                NO es un link roto, asi que NO se marca rojo)
  BLOCKED   -> fallo de red no concluyente      -> sin punto
  DEAD      -> fallo concluyente (404/410)       -> punto ROJO

Ademas rota alias: cuando un canal da SATURADO se prueban
  (a) los alias del mismo panel (mismo path en otro host/puerto) y
  (b) el `backup-url` declarado y otros canales con el mismo nombre,
y si alguno responde ALIVE se usa como URL principal (quedando el anterior
como backup). Eso es la "multiconexion" real: varias lineas independientes.

Genera `channel_status.json` con el estado de todos los canales numerados,
para que la app muestre un punto verde/naranja/rojo en la grilla.

Anti-"falsos rojos": el runner de GitHub corre en EE.UU. y varios CDN
chilenos (p. ej. mdstrm) DESCARTAN conexiones de fuera de Chile -> timeouts /
resets. Ese fallo es de RED, no concluyente, asi que NO se pinta rojo. Solo
se marca rojo cuando el problema es concluyente: HTTP 404/410, DNS
inexistente, pagina HTML de bloqueo/error.

Uso:
  python scripts/check_channels.py            # aplica cambios y escribe
  python scripts/check_channels.py --dry-run  # solo informa, no escribe nada

Seguridad: si mas de MAX_DEAD_RATIO de la grilla sale caida concluyente se
aborta sin tocar nada (probable bloqueo de red del runner de CI).
"""
import concurrent.futures
import datetime
import json
import os
import re
import socket
import sys
import threading
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
M3U = os.path.join(REPO, "todos_tus_canales_live.m3u")
STATUS = os.path.join(REPO, "channel_status.json")
ALIAS_MAP = os.path.join(HERE, "alias_map.json")

UA = (
    "Mozilla/5.0 (Linux; Android 11; SM-A125M) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
)
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/vnd.apple.mpegurl, application/x-mpegURL, */*",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
}
TIMEOUT = 12
ATTEMPTS = 2
WORKERS = 40
MAX_DEAD_RATIO = 0.6
CANDIDATES_PER_CHANNEL = 5

# Estados de un sondeo.
ALIVE = "alive"        # responde y entrega una playlist valida -> verde
SATURADO = "saturado"  # 401/429/456/458 -> cupo lleno -> NARANJA (no rojo)
BLOCKED = "blocked"    # fallo de RED no concluyente (geo-bloqueo del runner)
DEAD = "dead"          # fallo concluyente -> rojo

_PLAYLIST_HINTS = (b"#extm3u", b"#extinf", b"#ext-x-")
_HTML_HINTS = (b"<!doctype", b"<html", b"<head", b"<body", b"<script", b"<meta")
_RANK = {ALIVE: 3, SATURADO: 2, BLOCKED: 1, DEAD: 0}

_BACKUP_RE = re.compile(r'backup-url="[^"]*"')
_DUR_RE = re.compile(r"^(#EXTINF:\S+\s)")
_URL_RE = re.compile(r"^(?P<scheme>https?)://(?P<host>[^/]+)(?P<path>/.*)$")
# firma del canal DENTRO de un panel: /live/usuario/clave/id.ts
_LIVE_RE = re.compile(r"^/live/([^/]+)/([^/]+)/([^/?#]+)")
# panel con token en el path: /Mmt5Yz...  (base64 del canal)
_TOKEN_RE = re.compile(r"^/([A-Za-z0-9+/=_-]{16,})(/.*)?$")

_cache = {}
_cache_lock = threading.Lock()


def norm(name: str) -> str:
    """Normaliza un nombre para emparejar una senal con su respaldo."""
    s = name.upper()
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)
    s = re.sub(r"\b(HD|FHD|SD|UHD|4K|1080P|720P|576P)\b", " ", s)
    s = re.sub(r"\bALT\b", " ", s)
    s = re.sub(r"^\s*\d+\s+", "", s)
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _is_playlist(body: bytes, ctype: str) -> bool:
    if ctype and ("mpegurl" in ctype or "playlist" in ctype):
        return True
    head = body[:4096].lstrip().lower()
    return any(hint in head for hint in _PLAYLIST_HINTS)


def _is_html(body: bytes) -> bool:
    head = body[:4096].lstrip().lower()
    return any(hint in head for hint in _HTML_HINTS)


def _is_video(body: bytes, ctype: str) -> bool:
    """TS crudo (sync 0x47) o video/mp2t: senal real aunque no sea HLS."""
    if ctype and ctype.startswith("video/"):
        return True
    return body[:1] == b"\x47"


def _classify(code: int, body: bytes, ctype: str):
    """Clasifica un codigo HTTP. Devuelve (estado, detalle)."""
    if code in (200, 206):
        if _is_html(body):
            return DEAD, "http %d html" % code
        if _is_playlist(body, ctype) or _is_video(body, ctype):
            return ALIVE, "http %d" % code
        return BLOCKED, "http %d sin playlist" % code
    # 401/429/456/458: la linea existe pero el cupo de conexiones esta lleno
    # (o la IP fue limitada). NO es un link roto -> no se pinta rojo.
    if code in (401, 429, 456, 458):
        return SATURADO, "http %d saturado" % code
    # 403: puede ser bloqueo por region/IP u otro servicio en ese puerto.
    if code == 403:
        return BLOCKED, "http %d" % code
    if code in (404, 410):
        return DEAD, "http %d" % code
    if code >= 500:
        return BLOCKED, "http %d" % code
    return DEAD, "http %d" % code


def _probe_once(url, timeout):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code = r.getcode()
            body = r.read(4096)
            ctype = (r.headers.get("Content-Type") or "").lower()
            return _classify(code, body, ctype)
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read(4096)
        except Exception:  # noqa: BLE001
            pass
        ctype = ""
        if e.headers is not None:
            ctype = (e.headers.get("Content-Type") or "").lower()
        return _classify(e.code, body, ctype)


def probe(url, timeout=TIMEOUT, attempts=ATTEMPTS):
    """Sondea `url` y devuelve (estado, detalle). Resultado cacheado."""
    if not url or not url.lower().startswith(("http://", "https://")):
        return DEAD, "url invalida"
    with _cache_lock:
        cached = _cache.get(url)
    if cached is not None:
        return cached

    state, detail = DEAD, "sin respuesta"
    for _ in range(attempts):
        try:
            state, detail = _probe_once(url, timeout)
            if state in (ALIVE, SATURADO, DEAD):
                break
        except socket.timeout:
            state, detail = BLOCKED, "timeout"
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.gaierror):
                state, detail = DEAD, "dns"
                break
            state, detail = BLOCKED, "net %s" % e.reason
        except Exception as e:  # noqa: BLE001 - red/conexion inesperada
            state, detail = BLOCKED, type(e).__name__

    with _cache_lock:
        _cache[url] = (state, detail)
    return state, detail


def parse(lines):
    """Devuelve lista de entradas {num, name, url, extinf_line, url_line}."""
    entries = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("#EXTINF"):
            line = lines[i]
            idx = line.rfind('",')
            raw = line[idx + 2:] if idx != -1 else line.split(",", 1)[-1]
            m = re.match(r"\s*(\d+)\s+(\S.*)", raw)
            num = int(m.group(1)) if m else None
            name = m.group(2).strip() if m else raw.strip()
            j = i + 1
            while j < len(lines) and (
                lines[j].strip() == "" or lines[j].lstrip().startswith("#")
            ):
                j += 1
            url = lines[j].strip() if j < len(lines) else ""
            bm = _BACKUP_RE.search(line)
            backup = bm.group(0)[len('backup-url="'):-1] if bm else ""
            entries.append(
                {
                    "num": num,
                    "name": name,
                    "url": url,
                    "backup": backup,
                    "extinf_line": i,
                    "url_line": j,
                }
            )
            i = j + 1
        else:
            i += 1
    return entries


# --------------------------------------------------------------- alias
def _split_url(url):
    m = _URL_RE.match(url or "")
    if not m:
        return None
    return m.group("host"), m.group("path")


def _alias_key(url):
    """Firma del canal dentro de su panel.

    Si dos URLs de paneles distintos comparten firma, son el MISMO canal
    servido por alias distintos: probarlos en el otro host es la via para
    esquivar el cupo de conexiones.
    """
    parts = _split_url(url)
    if not parts:
        return None
    _host, path = parts
    m = _LIVE_RE.match(path)
    if m:
        return "live|%s|%s|%s" % m.groups()
    m = _TOKEN_RE.match(path)
    if m:
        return "tok|%s" % m.group(1)
    return None


def build_alias_groups(entries):
    """{firma: {host, ...}} con los hosts que sirven el mismo canal."""
    groups = {}
    for e in entries:
        key = _alias_key(e["url"])
        if not key:
            continue
        parts = _split_url(e["url"])
        if not parts:
            continue
        groups.setdefault(key, set()).add(parts[0])
    return {k: v for k, v in groups.items() if len(v) > 1}


def load_alias_map():
    """Alias explicitos (panel -> lista de bases alternativas)."""
    if not os.path.exists(ALIAS_MAP):
        return {}
    try:
        with open(ALIAS_MAP, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:  # noqa: BLE001
        return {}
    out = {}
    for base, alts in (data or {}).items():
        if isinstance(alts, list):
            out[base.rstrip("/")] = [a.rstrip("/") for a in alts]
    return out


def alias_candidates(url, groups, alias_map):
    """URLs alternativas del mismo canal: mismo path en otro host/panel."""
    parts = _split_url(url)
    if not parts:
        return []
    host, path = parts
    out = []
    key = _alias_key(url)
    if key:
        for h in sorted(groups.get(key, ())):
            if h == host:
                continue
            out.append("http://%s%s" % (h, path))
            out.append("https://%s%s" % (h, path))
    base = "http://%s" % host
    for alt_base in alias_map.get(base, ()):
        out.append("%s%s" % (alt_base, path))
        out.append("%s%s" % (alt_base.replace("http://", "https://"), path))
    seen = set()
    uniq = []
    for u in out:
        if u != url and u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


# --------------------------------------------------------------- repair
def _pool_by_name(entries):
    pool = {}
    for e in entries:
        key = norm(e["name"])
        if key:
            pool.setdefault(key, []).append(e)
    return pool


def _unique(seq):
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _candidates_for(e, pool, groups, alias_map):
    """Candidatos a reemplazar la URL de un canal, en orden de preferencia."""
    cands = []
    # 1) alias del mismo panel (mismo path, otro host) -> esquivan el cupo
    for u in alias_candidates(e["url"], groups, alias_map):
        cands.append(u)
    # 2) el backup-url declarado en la propia linea
    if e.get("backup"):
        cands.append(e["backup"])
    # 3) otros canales con el mismo nombre (otra linea / otro panel)
    for c in pool.get(norm(e["name"]), []):
        if c["url"] and c["url"] != e["url"]:
            cands.append(c["url"])
        if c.get("backup") and c["backup"] != e["url"]:
            cands.append(c["backup"])
    return _unique(cands)[:CANDIDATES_PER_CHANNEL * 3]


def repair_channels(entries, lines):
    """Reemplaza URLs caidas o saturadas por una alternativa viva.

    Devuelve (reemplazos {url_line: nueva_url}, {url_line: backup_viejo}).
    """
    numbered = [e for e in entries if e["num"] is not None]
    if not numbered:
        return {}, {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        states = list(ex.map(lambda e: probe(e["url"])[0], numbered))
    to_fix = []
    for e, st in zip(numbered, states):
        if st in (DEAD, SATURADO):
            to_fix.append(e)

    dead = [e for e in to_fix]
    if not dead:
        return {}, {}

    # cota de seguridad: demasiados caidos concluyentes = red del runner
    concluyentes = [e for e in dead if probe(e["url"])[0] == DEAD]
    if len(concluyentes) > MAX_DEAD_RATIO * len(numbered):
        print(
            "ABORTADO: demasiados caidos concluyentes (%d/%d), "
            "posible bloqueo de red en CI." % (len(concluyentes), len(numbered))
        )
        return None, None

    pool = _pool_by_name([e for e in entries if e["num"] is None])
    groups = build_alias_groups(entries)
    alias_map = load_alias_map()
    if groups:
        print("grupos de alias detectados: %d" % len(groups))

    cand_map = {}
    all_cands = set()
    for e in dead:
        cs = _candidates_for(e, pool, groups, alias_map)
        cand_map[e["url_line"]] = cs
        all_cands.update(cs)
    all_cands = sorted(all_cands)

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        cand_states = list(ex.map(lambda u: probe(u)[0], all_cands))
    cand_state = dict(zip(all_cands, cand_states))

    replacements = {}
    backups = {}
    for e in dead:
        for c in cand_map[e["url_line"]]:
            if cand_state.get(c) == ALIVE:
                replacements[e["url_line"]] = c
                backups[e["url_line"]] = e["url"]
                etiqueta = ("alias/linea viva" if probe(e["url"])[0] == SATURADO
                            else "respaldo")
                print("  %s %s -> %s" % (e["num"], e["name"], etiqueta))
                break
        else:
            st = probe(e["url"])[0]
            etiqueta = "saturado sin cupo" if st == SATURADO else "SIN respaldo"
            print("  %s %s -> %s" % (e["num"], e["name"], etiqueta))
    return replacements, backups


def _set_backup_url(line, url):
    attr = 'backup-url="%s"' % url
    if _BACKUP_RE.search(line):
        return _BACKUP_RE.sub(lambda _m: attr, line)
    return _DUR_RE.sub(lambda m: m.group(1) + attr + " ", line, count=1)


def add_backups(lines, entries):
    """Inyecta/refresca backup-url en cada canal numerado con respaldo vivo.

    Elige como respaldo una fuente de OTRO host (si existe), porque un
    respaldo del mismo panel comparte el cupo de conexiones y no sirve de
    nada cuando la linea esta saturada.
    """
    numbered = [e for e in entries if e["num"] is not None]
    pool = _pool_by_name([e for e in entries if e["num"] is None])
    groups = build_alias_groups(entries)
    alias_map = load_alias_map()

    todo = []
    for e in numbered:
        line = lines[e["extinf_line"]]
        m = _BACKUP_RE.search(line)
        current = m.group(0)[len('backup-url="'):-1] if m else None
        cands = _unique(
            [
                c["url"]
                for c in pool.get(norm(e["name"]), [])
                if c["url"] and c["url"] != e["url"]
            ]
            + alias_candidates(e["url"], groups, alias_map)
        )[:CANDIDATES_PER_CHANNEL * 2]
        todo.append((e, current, cands))

    urls = set()
    for _e, current, cands in todo:
        urls.update(cands)
        if current:
            urls.add(current)
    urls.discard("")
    urls = sorted(urls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        ok_flags = list(ex.map(lambda u: probe(u)[0] == ALIVE, urls))
    ok_urls = {u for u, ok in zip(urls, ok_flags) if ok}

    added = refreshed = 0
    for e, current, cands in todo:
        if current and current in ok_urls:
            continue  # el respaldo actual sigue vivo
        host = (_split_url(e["url"]) or ("", ""))[0]
        elegido = None
        for u in cands:
            if u in ok_urls:
                h = (_split_url(u) or ("", ""))[0]
                if h != host:
                    elegido = u
                    break
        if elegido is None:
            elegido = next((u for u in cands if u in ok_urls), None)
        if elegido is None:
            continue  # no hay respaldo vivo: se deja lo que ya hubiera
        new_line = _set_backup_url(lines[e["extinf_line"]], elegido)
        if new_line != lines[e["extinf_line"]]:
            lines[e["extinf_line"]] = new_line
            if current:
                refreshed += 1
            else:
                added += 1
    print("backup-url: %d agregados, %d actualizados" % (added, refreshed))
    return added + refreshed


def write_status(entries, dry_run=False):
    """Escribe channel_status.json.

    status: true = usable (vivo o saturado, el link existe)
    saturado: numeros con cupo de conexiones lleno -> punto NARANJA
    blocked: fallo de red no concluyente -> sin punto
    """
    numbered = [e for e in entries if e["num"] is not None]
    if not numbered:
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        results = list(ex.map(lambda e: probe(e["url"])[0], numbered))

    best = {}
    for e, st in zip(numbered, results):
        num = e["num"]
        prev = best.get(num)
        if prev is None or _RANK[st] > _RANK[prev]:
            best[num] = st

    status = {num: (st != DEAD) for num, st in best.items()}
    saturado = sorted(num for num, st in best.items() if st == SATURADO)
    blocked = sorted(num for num, st in best.items() if st == BLOCKED)
    payload = {
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "count": len(status),
        "status": {str(k): v for k, v in sorted(status.items())},
        "saturado": saturado,
        "blocked": blocked,
    }
    if dry_run:
        print(
            "[dry-run] estado: %d canales (%d vivos, %d saturados, %d sin verificar)"
            % (len(status), sum(status.values()), len(saturado), len(blocked))
        )
        return
    with open(STATUS, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    print(
        "estado escrito: %d canales (%d vivos, %d saturados, %d sin verificar)"
        % (len(status), sum(status.values()), len(saturado), len(blocked))
    )


def main():
    dry = "--dry-run" in sys.argv
    lines = open(M3U, encoding="utf-8").read().splitlines()
    entries = parse(lines)

    replacements, backups = repair_channels(entries, lines)
    if replacements is None:
        return 1

    url_changes = 0
    for line_no, url in replacements.items():
        if lines[line_no] != url:
            lines[line_no] = url
            url_changes += 1

    # la URL que era principal pasa a quedar como backup del canal
    for line_no, old in backups.items():
        ent = next((e for e in parse(lines) if e["url_line"] == line_no), None)
        if ent is None:
            continue
        lines[ent["extinf_line"]] = _set_backup_url(lines[ent["extinf_line"]], old)

    backup_changes = add_backups(lines, parse(lines))

    if dry:
        print("[dry-run] sin escritura (url=%d, backup=%d)" % (url_changes, backup_changes))
    elif url_changes or backup_changes:
        with open(M3U, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print("m3u escrito: %d URLs, %d backups" % (url_changes, backup_changes))
    else:
        print("sin cambios en la grilla")

    # Estado para los puntos verde/naranja/rojo de la app (sobre la lista ya
    # corregida).
    write_status(parse(lines), dry_run=dry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
