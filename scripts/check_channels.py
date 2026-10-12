#!/usr/bin/env python3
"""Prueba los canales de la grilla (1-119) de todos_tus_canales_live.m3u y
reemplaza las URLs caidas por un respaldo funcional de la misma lista
(bloques replica 120-357 y secciones M3U.CL / FUENTES).

Seguridad: si se detectan como caidos mas de MAX_DEAD_RATIO de la grilla se
aborta sin tocar nada (probable bloqueo de red del runner de CI).
"""
import concurrent.futures
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
M3U = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "todos_tus_canales_live.m3u")
UA = (
    "Mozilla/5.0 (Linux; Android 11; SM-A125M) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
)
TIMEOUT = 12
WORKERS = 16
MAX_DEAD_RATIO = 0.6


def norm(name: str) -> str:
    s = name.upper()
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)
    s = re.sub(r"\b(HD|FHD|SD|UHD|4K|1080P|720P|576P)\b", " ", s)
    s = re.sub(r"\bALT\b", " ", s)
    s = re.sub(r"^\s*\d+\s+", "", s)
    s = re.sub(r"[^A-Z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def alive(url, timeout=12):
    if not url or not url.lower().startswith(("http://", "https://")):
        return False
    for _ in range(2):
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
            entries.append(
                {"num": num, "name": name, "url": url, "url_line": j}
            )
            i = j + 1
        else:
            i += 1
    return entries


def main():
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "todos_tus_canales_live.m3u",
    )
    lines = open(path, encoding="utf-8").read().splitlines()
    entries = parse(lines)

    grilla = [e for e in entries if e["num"] and 1 <= e["num"] <= 119]
    pool = {}
    for e in entries:
        if e["num"] and 1 <= e["num"] <= 119:
            continue
        pool.setdefault(norm(e["name"]), []).append(e)

    print("grilla: %d canales | pool de respaldos: %d nombres" % (len(grilla), len(pool)))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        state = list(ex.map(lambda e: alive(e["url"]), grilla))

    dead = [e for e, ok in zip(grilla, state) if not ok]
    print("caidos: %d de %d" % (len(dead), len(grilla)))

    if len(dead) > int(len(grilla) * 0.6):
        print(
            "ABORTADO: demasiados caidos (%d/%d), posible bloqueo de red en CI."
            % (len(dead), len(grilla))
        )
        return 1

    # Candidatos por nombre normalizado.
    cands = {}
    for e in dead:
        cands[e["url_line"]] = pool.get(norm(e["name"]), [])
    all_cand_urls = {c["url"] for lst in cands.values() for c in lst}
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex:
        ok_urls = set(
            u for u, ok in zip(all_cand_urls, ex.map(alive, list(all_cand_urls))) if ok
        )

    changes = 0
    for e in dead:
        replacement = None
        for c in cands[e["url_line"]]:
            if c["url"] in ok_urls and c["url"] != e["url"]:
                replacement = c["url"]
                break
        if replacement:
            print("  %d %s -> reemplazado" % (e["num"], e["name"]))
            lines[e["url_line"]] = replacement
            changes += 1
        else:
            print("  %d %s -> SIN respaldo funcional" % (e["num"], e["name"]))

    if changes:
        open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
        print("cambios aplicados: %d" % changes)
    else:
        print("sin cambios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
