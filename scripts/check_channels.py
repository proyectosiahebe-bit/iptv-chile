#!/usr/bin/env python3
"""Prueba los canales de la grilla (1-119) de todos_tus_canales_live.m3u,
reemplaza las URLs *realmente* caidas por un respaldo funcional de la misma
lista (bloques replica 120-357 y secciones M3U.CL / FUENTES) y ademas inyecta
el atributo `backup-url="..."` en cada canal de la grilla para que la app haga
failover instantaneo si la senal principal falla.

Genera `channel_status.json` con el estado de todos los canales numerados, para
que la app muestre un punto verde/rojo en la grilla.

Anti-"falsos rojos": el runner de GitHub corre en EE.UU. y varios CDN chilenos
(p. ej. mdstrm) DESCARTAN conexiones de fuera de Chile -> timeouts / resets.
Ese fallo es de RED, no concluyente, asi que NO se pinta rojo. Solo se marca
rojo cuando el problema es concluyente: HTTP 404/410, DNS inexistente, pagina
HTML de bloqueo/error, o acceso denegado (401/403/429) persistente.

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
WORKERS = 32
MAX_DEAD_RATIO = 0.6
CANDIDATES_PER_CHANNEL = 5

# Estados de un sondeo.
ALIVE = "alive"      # responde y entrega una playlist valida -> verde
BLOCKED = "blocked"  # fallo de RED no concluyente (geo-bloqueo del runner) -> no rojo
DEAD = "dead"        # fallo concluyente -> rojo

_PLAYLIST_HINTS = (b"#extm3u", b"#extinf", b"#ext-x-")
_HTML_HINTS = (b"<!doctype", b"<html", b"<head", b"<body", b"<script", b"<meta")
_RANK = {ALIVE: 2, BLOCKED: 1, DEAD: 0}

_BACKUP_RE = re.compile(r'backup-url="[^"]*"')
_DUR_RE = re.compile(r"^(#EXTINF:\S+\s)")

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


def _probe_once(url, timeout):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        code = r.getcode()
        body = r.read(4096)
        ctype = (r.headers.get("Content-Type") or "").lower()
        if code in (200, 206):
            if _is_playlist(body, ctype):
                return ALIVE, "http %d" % code
            if _is_html(body):
                return DEAD, "http %d html" % code
            return BLOCKED, "http %d sin playlist" % code
        return DEAD, "http %d" % code


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
            if state == ALIVE:
                break
        except urllib.error.HTTPError as e:
            code = e.code
            if code in (404, 410):
                state, detail = DEAD, "http %d" % code
                break
            # 401/403/429: puede ser bloqueo del runner o acceso real denegado.
            # Si persiste tras los reintentos se considera caido (concluyente).
            state, detail = DEAD, "http %d" % code
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
            entries.append(
                {
                    "num": num,
                    "name": name,
                    "url": url,
                    "extinf_line": i,
                    "url_line": j,
                }
            )
            i = j + 1
        else:
            i += 1
    return entries


def _is_grilla(num):
    return num is not None and 1 <= num <= 119


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


def replace_dead(entries):
    """Devuelve {url_line: nueva_url} reemplazando solo las caidas concluyentes."""
    grilla = [e for e in entries if _is_grilla(e["num"])]
    if not grilla:
        return {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        states = list(ex.map(lambda e: probe(e["url"])[0], grilla))
    dead = [e for e, st in zip(grilla, states) if st == DEAD]

    if len(dead) > MAX_DEAD_RATIO * len(grilla):
        print(
            "ABORTADO: demasiados caidos concluyentes (%d/%d), "
            "posible bloqueo de red en CI." % (len(dead), len(grilla))
        )
        return None

    pool = _pool_by_name([e for e in entries if not _is_grilla(e["num"])])

    cands = {}
    for e in dead:
        cands[e["url_line"]] = [
            c
            for c in pool.get(norm(e["name"]), [])
            if c["url"] and c["url"] != e["url"]
        ][:CANDIDATES_PER_CHANNEL]

    cand_urls = sorted(
        {c["url"] for lst in cands.values() for c in lst}
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        ok_flags = list(ex.map(lambda u: probe(u)[0] == ALIVE, cand_urls))
    ok_urls = {u for u, ok in zip(cand_urls, ok_flags) if ok}

    replacements = {}
    for e in dead:
        for c in cands[e["url_line"]]:
            if c["url"] in ok_urls and c["url"] != e["url"]:
                replacements[e["url_line"]] = c["url"]
                print("  %s %s -> respaldo" % (e["num"], e["name"]))
                break
        else:
            print("  %s %s -> SIN respaldo funcional" % (e["num"], e["name"]))
    return replacements


def _set_backup_url(line, url):
    attr = 'backup-url="%s"' % url
    if _BACKUP_RE.search(line):
        return _BACKUP_RE.sub(lambda _m: attr, line)
    return _DUR_RE.sub(lambda m: m.group(1) + attr + " ", line, count=1)


def add_backups(lines, entries):
    """Inyecta/refresca backup-url en cada canal de la grilla con respaldo vivo.

    Devuelve cuantas lineas cambiaron.
    """
    grilla = [e for e in entries if _is_grilla(e["num"])]
    pool = _pool_by_name([e for e in entries if not _is_grilla(e["num"])])

    todo = []
    for e in grilla:
        line = lines[e["extinf_line"]]
        m = _BACKUP_RE.search(line)
        current = m.group(0)[len('backup-url="'):-1] if m else None
        cands = _unique(
            [
                c["url"]
                for c in pool.get(norm(e["name"]), [])
                if c["url"] and c["url"] != e["url"]
            ]
        )[:CANDIDATES_PER_CHANNEL]
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
        chosen = next((u for u in cands if u in ok_urls), None)
        if chosen is None:
            continue  # no hay respaldo vivo: se deja lo que ya hubiera
        new_line = _set_backup_url(lines[e["extinf_line"]], chosen)
        if new_line != lines[e["extinf_line"]]:
            lines[e["extinf_line"]] = new_line
            if current:
                refreshed += 1
            else:
                added += 1
    print("backup-url: %d agregados, %d actualizados" % (added, refreshed))
    return added + refreshed


def write_status(entries, dry_run=False):
    """Escribe channel_status.json: true = usable, false = caido concluyente."""
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
    blocked = sorted(num for num, st in best.items() if st == BLOCKED)
    payload = {
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "count": len(status),
        "status": {str(k): v for k, v in sorted(status.items())},
        "blocked": blocked,
    }
    if dry_run:
        print(
            "[dry-run] estado: %d canales (%d vivos, %d bloqueados sin verificar)"
            % (len(status), sum(status.values()), len(blocked))
        )
        return
    with open(STATUS, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    print(
        "estado escrito: %d canales (%d vivos, %d bloqueados sin verificar)"
        % (len(status), sum(status.values()), len(blocked))
    )


def main():
    dry = "--dry-run" in sys.argv
    lines = open(M3U, encoding="utf-8").read().splitlines()
    entries = parse(lines)

    replacements = replace_dead(entries)
    if replacements is None:
        return 1

    url_changes = 0
    for line_no, url in replacements.items():
        if lines[line_no] != url:
            lines[line_no] = url
            url_changes += 1

    backup_changes = add_backups(lines, parse(lines))

    if dry:
        print("[dry-run] sin escritura (url=%d, backup=%d)" % (url_changes, backup_changes))
    elif url_changes or backup_changes:
        with open(M3U, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print("m3u escrito: %d URLs, %d backups" % (url_changes, backup_changes))
    else:
        print("sin cambios en la grilla")

    # Estado para los puntos verde/rojo de la app (sobre la lista ya corregida).
    write_status(parse(lines), dry_run=dry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
