#!/usr/bin/env python3
"""Prueba los canales de la grilla (1-119) de todos_tus_canales_live.m3u y
reemplaza las URLs caidas por un respaldo funcional de la misma lista
(bloques replica 120-357 y secciones M3U.CL / FUENTES).

Ademas genera `channel_status.json` con el estado (vivo/caido) de todos los
canales numerados, para que la app muestre un punto verde/rojo en la grilla.

Seguridad: si se detectan como caidos mas de MAX_DEAD_RATIO de la grilla se
aborta sin tocar nada (probable bloqueo de red del runner de CI).
"""
import concurrent.futures
import datetime
import json
import os
import re
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
TIMEOUT = 12
WORKERS = 20
MAX_DEAD_RATIO = 0.6


def norm(name: str) -> str:
    s = name.upper()
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)
    s = re.sub(r"\b(HD|FHD|SD|UHD|4K|1080P|720P|576P)\b", " ", s)
    s = re.sub(r"\bALT\b", " ", s)
    s = re.sub(r"^\s*\d+\s+", "", s)
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def alive(url, timeout=TIMEOUT, attempts=2):
    if not url or not url.lower().startswith(("http://", "https://")):
        return False
    for _ in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.getcode() in (200, 206):
                    r.read(1024)
                    return True
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404, 410):
                return False
        except Exception:
            pass
    return False


def parse(lines):
    """Devuelve lista de entradas {num, name, url, url_line}."""
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
            entries.append({"num": num, "name": name, "url": url, "url_line": j})
            i = j + 1
        else:
            i += 1
    return entries


def replace_dead(entries):
    """Reemplaza en `lines` las URLs caidas de la grilla por respaldos."""
    grilla = [e for e in entries if e["num"] is not None and 1 <= e["num"] <= 119]
    others = [e for e in entries if not (e["num"] is not None and 1 <= e["num"] <= 119)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        dead_flags = list(ex.map(lambda e: not alive(e["url"]), grilla))
    dead = [e for e, is_dead in zip(grilla, dead_flags) if is_dead]

    if len(dead) > MAX_DEAD_RATIO * len(grilla):
        print(
            "ABORTADO: demasiados caidos (%d/%d), posible bloqueo de red en CI."
            % (len(dead), len(grilla))
        )
        return None

    pool = {}
    for e in others:
        key = norm(e["name"])
        if key:
            pool.setdefault(key, []).append(e)

    cands = {}
    for e in dead:
        cands[e["url_line"]] = pool.get(norm(e["name"]), [])
    cand_urls = sorted({c["url"] for lst in cands.values() for c in lst})
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        ok_flags = list(ex.map(alive, cand_urls))
    ok_urls = {u for u, ok in zip(cand_urls, ok_flags) if ok}

    replacements = {}
    for e in dead:
        for c in cands[e["url_line"]]:
            if c["url"] in ok_urls and c["url"] != e["url"]:
                replacements[e["url_line"]] = c["url"]
                print("  %d %s -> respaldo" % (e["num"], e["name"]))
                break
        else:
            print("  %d %s -> SIN respaldo funcional" % (e["num"], e["name"]))
    return replacements


def write_status(entries):
    """Prueba todos los canales numerados y escribe channel_status.json."""
    numbered = [e for e in entries if e["num"] is not None]
    if not numbered:
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        results = list(
            ex.map(lambda e: alive(e["url"], timeout=8, attempts=1), numbered)
        )
    status = {}
    for e, ok in zip(numbered, results):
        num = e["num"]
        # Un canal repetido se marca vivo si cualquiera de sus senales responde.
        status[num] = bool(status.get(num, False) or ok)
    payload = {
        "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "count": len(status),
        "status": {str(k): v for k, v in sorted(status.items())},
    }
    with open(STATUS, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    print("estado escrito: %d canales (%d vivos)" % (len(status), sum(status.values()))) 


def main():
    lines = open(M3U, encoding="utf-8").read().splitlines()
    entries = parse(lines)

    replacements = replace_dead(entries)
    if replacements is None:
        return 1

    changes = 0
    for line_no, url in replacements.items():
        lines[line_no] = url
        changes += 1

    if changes:
        with open(M3U, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print("cambios aplicados: %d" % changes)
    else:
        print("sin cambios en la grilla")

    # Estado para los puntos verde/rojo de la app (sobre la lista ya corregida).
    write_status(parse(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
