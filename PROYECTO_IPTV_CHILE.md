# Proyecto IPTV Chile

Playlist M3U de canales chilenos y latinoamericanos.

## Link de la playlist (GitHub)
```
https://raw.githubusercontent.com/proyectosiahebe-bit/iptv-chile/main/todos_tus_canales_live.m3u
```

## Fuentes de canales

### 1. iptv.wtf (principal)
- **URL base:** `http://iptv.wtf:25461/get.php?username=gxdcxnbf&password=1eZr21rf1D&type=m3u&output=ts`
- **Tipo:** Xtream API / M3U
- **Canales:** ~5,590 totales, ~74 chilenos
- **Formato:** `.ts` (transport stream)
- **Requiere:** Suscripcion

### 2. jumangis.cloud (secundaria para canales que faltan)
- **URL base:** `http://jumangis.cloud:2082/get.php?username=Margarito&password=tXBU2WnnL8&type=m3u`
- **Tipo:** Xtream API / M3U
- **Canales:** ~84,500 (incluye VOD y en vivo)
- **Fuente de:** Mega 2, MTV/VH1 latino
- **Nota:** demora en cargar (redirecciona por CDN multiple)

### 3. pirostv.lat (revision)
- **URL base:** `http://pirostv.lat:8080/live/Nestrive/Polopolo321$/`
- **Tipo:** Xtream
- **Nota:** Meganoticias quedo protegida (401), no usable

### 4. iptv-org / m3u.cl (complementarias)
- iptv-org: `https://iptv-org.github.io/iptv/countries/cl.m3u`
- m3u.cl: `https://m3u.cl/lista/CL.m3u`
- Usadas para: CHV Noticias (rudo.video), TVN3 (mdstrm), Zona Latina

## Canales por categoria (92 total)

### NACIONALES (29)
24 Horas, CHV Noticias, CL: NTV, TVN3, CL: TV+, CL: UCV, T13, Zona Latina, T13 En Vivo, TV+ (rudo), TV Chile, NTV (mdstrm), TVN 24 Horas, Mega (dps), CHV (rudo), Canal 13 (dps), T13 (rudo), T13 Radio, CNN Chile
- **Duplicados diferenciados (para elegir):** Bio Bio TV (rudo)/(tlink), La Red (circa)/(tlink), Mega 2 (jumangis)/(org), TVN (intersur)/(org), Meganoticias (mdstrm) y Meganoticias Ahora (tlink)

### SERIES / ENTRETENIMIENTO (10)
AXN, Comedy Central, E!, Space, TNT, TNT Series, Warner Channel, 13 Realities, 13 Teleseries, E! (org)

### PELICULAS (6)
AMC, Cinemax, Golden Edge, Studio Universal, Cinecanal Pacific, Telemundo Internacional

### INFANTILES (5)
Cartoonito, Discovery Kids, 13 Kids, Disney Channel Panregional, Nick Jr

### DOCUMENTALES / ESTILO DE VIDA (11)
A&E, Animal Planet, Discovery Home and Health, Discovery Science, Discovery TLC, Discovery Turbo, Food Network, H2, Investigation Discovery, Love Nature, 13C

### MUSICA (8)
MTV 80s, MTV Live (MX), VH1 Classic (MX), 13 Festival, FM Plus TV, Retro Plus TV Senal 1, Retro Plus TV Senal 2, Retro Plus TV Senal 3 (cdnz)

### DEPORTES (8)
ESPN 2 Peru, ESPN 3 Peru, TNT Sports 3, TNT Sports HD ARG, TNT Sports Premium, CHV Deportes, CDO (iptv.wtf)/(tlink)

### INTERNACIONALES (5)
AR: Telefe, Arirang, Arirang HD, ES: Antena 3, Europa Europa (iptv.wtf)

### TELETRAK + RADIO BIO BIO + TV SENADO (10)
- CL: TV Senado, CL: Teletrak (iptv.wtf)
- Radio Bio Bio: Concepcion, Los Angeles, Osorno, Puerto Montt, Santiago, Temuco, Valdivia, Valparaiso (iptv.wtf)

## Canales agregados desde m3u.cl (20, 2026-08-27)
Verificados con señal real (solo Meganoticias quedaba 401 por token):
- **NACIONALES:** Bio Bio TV (rudo), La Red (circa), TV+ (rudo), TV Chile (mdstrm), TVN (intersurtv), NTV (mdstrm), TVN 24 Horas (mdstrm), Mega (dps), Meganoticias, CHV (rudo), Canal 13 (dps), 13 Internacional, 13 popup, T13 (rudo), T13 Radio, CNN Chile
- **DEPORTES:** CHV Deportes (rudo)
- **MUSICA:** Retro Plus TV, Retro Plus TV Senal 2, Retro Plus TV Senal 3 (cdnz)

## Canales agregados desde iptv-org (42, 2026-08-27)
- **Con señal real:** 13C, 13 Entretencion, 13 Festival, 13 Humor, 13 Kids, 13 Prime, 13 Realities, 13 Teleseries (dpsgo), Cinecanal Pacific, Disney Channel Panregional, Disney Jr HD, Nick Jr, TV Chile (mdstrm)
- Resto sin señal (tlink muerto/403) — muchos fueron eliminados en la limpieza a 80.

## Restaurados 2026-08-27 (duplicados con nombre diferenciado)
Bio Bio TV, La Red, Mega 2, TVN, Meganoticias y CDO se restauraron en sus 2 versiones marcando la fuente entre paréntesis para que el usuario elija cuál conservar.

## Cambios 2026-09-09 (119 canales, reordenados por categoría)
- **Eliminados:** VENUS (111) y PLAYBOY (112) — pedido del usuario
- **Los canales de solutionspremium ya no están al final:** fueron movidos e integrados dentro de la sección de su categoría (renumeración global 1-119):
  - **SERIES / REALITY:** TNT NOVELAS (23), SONY (24), UNIVERSAL (25) — SONY y UNIVERSAL movidos a SERIES/REALITY según clasificación del usuario
  - **CINE:** USA NETWORK (49), ADULT SWIM (50) — dentro del bloque CINE
  - **INTERNACIONAL:** TVE INTERNACIONAL (99)
  - **NOTICIAS:** DW ESPANOL (102)
  - **RADIOS:** PUDAHUEL FM (113), CAROLINA TV (114), ROMANTICA (115), INFINITA (116), DUNA (117), LA CLAVE (118), LA METRO (119)

## Cambios 2026-09-06 (121 canales)
- **Canal 33 WARNER CHANNEL** -> version latina (HD Dual Audio) desde solutionspremium (antes en ingles via iptv.wtf)
- **Canal 42 HBO** -> version latina (HD LAT) desde solutionspremium (antes en ingles via jumangis)
- **Eliminado duplicado** HBO XTREME (quedaba un solo canal) y renumerado todo
- **Canales CINE agregados:** SONY (106), UNIVERSAL (107), USA NETWORK (108), ADULT SWIM (109), TNT NOVELAS (110), VENUS (111), PLAYBOY (112)
- **INTERNACIONAL:** TVE INTERNACIONAL (113)
- **NOTICIAS:** DW ESPANOL (114)
- **RADIOS agregadas:** PUDAHUEL FM (115), CAROLINA TV (116), ROMANTICA (117), INFINITA (118), DUNA (119), LA CLAVE (120), LA METRO (121)
- **Eliminados:** TNT SD, RAI 1, RADIOACTIVA TV (pedido del usuario)
- **Venus/Playboy** tomados desde jumangis (Venus Latino, Playboy Latino HD) — vipsclient no era confiable
- **Fuente nueva (solutionspremium):** `http://solutionspremium.net:80/channel/user2620/37428848293/<stream_id>.ts` — usada para Warner/HBO/Sony/Universal/USA/Adult Swim/TNT Novelas/TVE/DW

## Cambios 2026-09-12 (app+lista) — RESTAURAR colores: fuera `mediacodec` y la grilla SD (v1.7.25)
- **Reversión del experimento `mediacodec-copy` (v1.7.21-23).** Usuario en FHD (7, 9, 11, 14, 18): OK ~5 s → "vuelve a cargar" → **color azul** + desfase. Confirmado el origen: el tinte azulado del Allwinner vive en los **frames de salida del MediaCodec** (el bug no era solo la superficie GLES), y el cambio de `hwdec` en reproducción hace reiniciar el decoder a mpv (~5 s). Se vuelve a software puro con colores correctos (límite físico del deco en 1080p por software documentado en 1.7.20).
- **Eliminada la grilla SD** (v1.7.24): se borró `todos_tus_canales_sd.m3u`, el botón "Grilla SD" de la app y la URL alterna. Películas/series intactas en la grilla principal.
- Canales verificados OK al momento: **5 TV+, 6 TV CHILE, 8 NTV, 10 TVN3**. Problemáticos (1080p): **7 TVN, 9 MEGA, 11 CHV, 14 CHV NOTICIAS, 18 ZONA LATINA** (aceptado: desfase leve en software, azul si se fuerza hardware).
- **Verificación final (canal 7, 5 min):** `avsync` 60.6 → 99.6 s en ~75 s (decode ~45-63% del tiempo real con skip=all) → el desfase de 1080p crece linealmente sin límite → límite físico del A53 1 GHz. Se decide dejar así (colores correctos en todo; SD/HD perfectos; los 1080p lentos). Única vía de sincronía en este deco = hardware (azul, rechazado).
- **Versión app:** 1.7.25 (versionCode 36). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-12 (app+lista) — Grilla SD aparte, sin películas/series (v1.7.24) [RETIRADA]
- **Nuevo archivo `todos_tus_canales_sd.m3u`** (repo): grilla SD alternativa (49 canales) para que el deco decodifique por software en tiempo real sin desfases.
- **Chilenos SD verificados con `ffprobe`:** TV+ (1280x720 .ts), UCV (1280x720 .ts), VIA X (720x480 mpeg2), T13 (1280x720 .ts), TVN 24 HORAS (1280x720), RETRO PLUS TV y SEÑAL 2 (1280x720), TV SENADO y TELETRAK (1280x720) + radios.
- **Fuente de Colombia** (http://190.60.37.154:45000/playlist.m3u8, ~72 canales todos SD), **excluidos: nacionales colombianos** (Caracol, RCN, Uno, Institucional, Congreso, City TV, Capital, Señal Colombia, Telemedellín, Telecaribe, Telepacifico, Telecafe, Teleantioquia, Teleislas, TRO, Zoom, WIN+, RCN Novelas, Canal Estrellas, chd, MODULADOR) y **películas/series** (HBO/HBO2/HBO Family/HBO XTREME, TNT/TNT Novelas, Cinecanal, Cinemax, DE PELICULA, STAR CHANNEL, Sony, Space, Studio Universal, Warner, AXN, FX, TELENOVELAS).
- **Canales descartados por ser 1080p** (el objetivo del grid es SD): PUDAHUEL TV (113), LA CLAVE (118).
- **App:** botón **"Grilla SD"** en el inicio (alterna `defaultPlaylistUrl` ↔ `sdPlaylistUrl`, recarga; no toca la grilla principal ni su numeración).
- **Pendiente:** pushear `todos_tus_canales_sd.m3u` al repo (la app baja de `raw.githubusercontent.com/proyectosiahebe-bit/iptv-chile/main/`).
- **Versión app:** 1.7.24 (versionCode 35). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-12 (app) — `video-params/h` era double → enforcement caía (v1.7.23)
- v1.7.22 seguía con `hwdec=no` en 1080p. Verificado binario `libmpv.so` del APK: **`mediacodec-copy` existe** en la build (strings, count=1). El bug era el check `h is int` del muestreador: libmpv devuelve `video-params/h` como **double** → siempre false → nunca se enforceaba.
- **Fix:** normalización `num → int` (mismo patrón de `Settings.applyToPlayer`).
- **Versión app:** 1.7.23 (versionCode 34). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-12 (app) — `mediacodec-copy` no tomaba efecto: enforcement en vivo (v1.7.22)
- **Telemetría 1.7.21:** `hwdec-current=no` con 1920×1080 (avsync 0.28 → 13.8 s en 40 s). Causa: `applyToPlayer` corre al abrir cuando `video-params/h` = 0 → el cambio de hwdec para FHD nunca saltaba.
- **Fix:** el muestreador POLOTV (5 s) ahora **enforcea `hwdec` en vivo** según `video-params/h` real: **≥1080 → `mediacodec-copy`**, **<1080 → `no`**. Autocorrección al cambiar de canal; queda reflejado en la telemetría.
- **Versión app:** 1.7.22 (versionCode 33). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-12 (app) — FHD 7/9/18: hardware con copia (`mediacodec-copy`) (v1.7.21)
- **Investigación seria con datos:** (1) telemetría deco: `avsync` 3.8 → 38.4 s en 95 s con `skiploopfilter=all` → decode 1080p en SW al **~63% del tiempo real** (app 72% de CPU); (2) masters con `curl`: TVN (intersurtv), MEGA (dps) y ZONA LATINA (45.162.193.35) solo expuestos a **1920×1080** (sin variante 720p) → no hay ahorro por software ni señal más liviana disponible.
- **Fix:** en FHD (h≥1080) `hwdec=mediacodec-copy`: MediaCodec decodifica a velocidad real pero COPIA frames a RAM → render por software → colores correctos (evita el tinte del camino superficie-GLES del bug Allwinner). SD/HD intactos en SW puro. La telemetría ahora reporta `hwdec-current` (`mediacodec-copy` esperado en 7/9/18).
- **Pendiente verificación del usuario:** sincronía voz/imagen en 7/9/18 + colores/estética.
- **Versión app:** 1.7.21 (versionCode 32). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-12 (app) — FHD que va lento: decoder no alcanza el tiempo real (v1.7.20)
- **Telemetría v1.7.18 en vivo (datos reales del deco):** 1920×1080 → `avsync` 9.3 → 19.2 s en 40 s (la imagen se atrasa ~25%, `est-fps` reportado 30 porque es el esperado del filtro). 1280×720 → `avsync=0.007` (curioso: la imagen "va más lenta", el audio normal). → en FHD el decode H.264 30p progresivo (no entrelazado) de 1 GHz no alcanza al tiempo real; el desentrelazado NO es aquí el costo.
- **Fix:** escalera de `vd-lavc-skiploopfilter` en 3 niveles según `video-params/h` real del deco: **≥1080 → `all`** (loop filter completo fuera, máximo ahorro), **700–1079 → `nonkey`** (720p validado sincronizado), **<700 → `nonintra`**. Se mantienen deinterlace=yes, threads=4, audio-buffer=0.4, readahead 45s, hls-bitrate=no, ⏱ y telemetría.
- **Verificación pendiente:** avsync≈0 estable en un canal FHD (2/7/18) tras lograr el decode en tiempo real.
- **Versión app:** 1.7.20 (versionCode 31). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-12 (app) — Desfase = HLS por segmentos, no solo HD (v1.7.19)
- **Revisión del usuario por canal** (desfasados 2,3,7,8,9,10,18; síncronos 5,12,13,20) + **sondeo `ffprobe` de la señal real** de cada uno: NTV (8) y TVN3 (10) van a **854×480 HLS y AÚN se desfasaban** → el desfase NO era peso del decode HD: es el **formato**: los 7 desfasados son **HLS por segmentos**; los síncronos son **TS directo** (5 TV+, 12 UCV, 20 VIA X) y CANAL 13 es HLS pero 720p progresivo (ligero, sin micro-corte perceptible).
- **Causa del desfase residual:** en cada cambio de segmento HLS (fetch/TLS/parseo en la CPU débil del Q96) hay un micro-corte → el video se atrasa y comienza el desfase, que persiste porque la voz (estable) no se mueve. Coherente con "el desfase empieza tras un micro-corte".
- **Fix en modo Software:** `demuxer-readahead-secs=45` (el demuxer baja varios segmentos por delante → un fetch lento ya no detiene el video) y `hls-bitrate=no` (no cambia de variante a mitad de emisión → menos discontinuidades). Se mantienen `deinterlace=yes`, skip-loop por resolución, `vd-lavc-threads=4`, `audio-buffer=0.4`, ⏱ manual y la telemetría.
- **Telemetría 1.7.18:** muestreo cada 5 s de `avsync`/`drop-frame-count`/`estimated-vf-fps`/`video-params` con `debugPrint(POLOTV ...)` → captura por logcat; verificación final pendiente en el deco.
- **Versión app:** 1.7.19 (versionCode 30). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — REVERT `framedrop=hard` (v1.7.17)
- **1.7.16 (framedrop=hard) empeoró a desfase grande (~10 s):** con un decoder que va más lento que el tiempo real (A53 1 GHz en HD/FHD), el modo hard descarta los fotogramas atrasados en vez de mostrarlos y la brecha audio-video **crece**. Revertido al default (soft): muestra lo decodificado tarde → mejor estado validado por el usuario.
- Verificado en el deco que el ajuste manual ⏱ no estaba guardado (`audioDelayMs` ausente en SharedPreferences → audio-delay=0): el desfase grande NO vino de la calibración sino del framedrop.
- **Versión app:** 1.7.17 (versionCode 28). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Micro-cortes que dejan desfase en HD/FHD (v1.7.16)
- **Verificación en vivo durante la queja del usuario** (canal HD desfasado): CPU oscilando **45%↔90%** entre muestras → es el "pegado" cada milisegundos; audio **0 underruns** (la voz va estable); eth0 OK; 69 °C. Tras cada pico el video quedaba tarde y mpv compensaba estirando → desfase leve persistente.
- **Fix en modo Software:** **`framedrop=hard`** → ante un fotograma atrasado mpv lo suelta y salta directo a la posición de la voz (sincronía al instante) y, al no decodificar lo que llegaría tarde, baja el propio pico de CPU. Se mantienen `deinterlace=yes`, skip-loop escalonado (SD nonintra / HD nonkey), `vd-lavc-threads=4`, `audio-buffer=0.4` y el ajuste manual ⏱.
- **Versión app:** 1.7.16 (versionCode 27). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Desfase SOLO en HD/FHD: offload escalonado (v1.7.15)
- **Patrón del usuario:** SD perfectos; **todos los HD/FHD con desfase** (la voz no concuerda). Esto descarta el offset fijo del pipeline HDMI (afectaría también al SD): en HD/FHD el VIDEO se atrasa en picos de decode mientras la voz (bitrate bajo, buffer estable, 0 underruns verificado) sigue → desfase. El paso `nonintra` de 1.7.13 ayudó ("se ve mucho mejor"); falta apretar más en HD/FHD.
- **Cambio en `Settings.applyToPlayer`:** el ahorro de decode baja en escalera por resolución (`video-params/h`), manteniendo **`deinterlace=yes` SIEMPRE** (lección de v1.7.11, que quitó el desentrelazado → robot):
  - SD (<700): `vd-lavc-skiploopfilter=nonintra`.
  - HD/FHD (≥700): `vd-lavc-skiploopfilter=nonkey` (solo se afina el keyframe) → mucho menos trabajo por fotograma, el video deja de atrasarse y la voz concuerda; mínima pérdida de nitidez en movimiento (imperceptible en TV en vivo).
- **Versión app:** 1.7.15 (versionCode 26). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Calibración manual de sincronía voz/imagen (v1.7.14)
- **Verificación interna del desfase (todos los canales, HD reproduciendo):** audio sin underruns (partial=0 empty=0), CPU al ~50% de 4 núcleos, refresh 50.000 fps exactos, deco por **Ethernet cableado** (WiFi desconectada), temperatura 68°C (< 85), memoria 178-400 MB PSS sobre 8 GB → el desfase no es falta de recursos: es un **offset fijo de latencia del pipeline HDMI** (no compensation en mpv para estos decos).
- **Solución:** control de calibración en la app. Nuevo botón **⏱ Sincronía** (último de la barra, índice 7, no reordena controles existentes). Con él: **◀ ▶ ajustan la voz ±50 ms en vivo** y OK sale; se persiste globalmente (`audioDelayMs`, `audio-delay` de libmpv) y se aplica a todos los canales en cada `open()`. Grilla y ajustes intactos.
- **Versión app:** 1.7.14 (versionCode 25). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Sincronía voz/imagen en decos de 1 GHz (v1.7.13)
- **Diagnóstico en vivo** (HD reproduciendo, `top` Android): app al **87% CPU** con picos → el video se atrasa y la voz sigue → "voz no concuerda". Memoria OK (178 MB PSS, sin swap, 8 GB totales), temp 58-62°C (tope 85°C); el cuello de botella es el decode puntual, no RAM/calor.
- **Fix quirúrgico:** `Settings.applyToPlayer` mantiene `deinterlace=yes` (inalterable) y añade **`vd-lavc-skiploopfilter=nonintra`** → menor coste de decode por fotograma (~20-30%), menos micro-stalls, el video deja de atrasarse y la voz concuerda. (En 1.7.11 este filtro iba combinado con `deinterlace=no` → por eso dio "robot"; ahora va solo con desentrelazado ON.)
- Se desecha el experimento `video-output-levels=limited` (empeora colores). No se toca la grilla.
- **Versión app:** 1.7.13 (versionCode 24). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Revert reducción HD por resolución + optimización real del deco (v1.7.12)
- **v1.7.11 fue un error:** dividir por `video-params/h` hizo que muchos canales "SD" (que en IPTV vienen en 1080) se clasificaran como HD y perdieran el desentrelazado → se veían "robot"/peines; y los HD (1080i real sin desentrelazar) peor. Lo confirmó el usuario: SD y HD empeoraron.
- **Revert en la app:** `Settings.applyToPlayer` vuelve al modo Software uniforme validado por el usuario — `deinterlace=yes`, `vd-lavc-threads=4`, `audio-buffer=0.4` para TODOS los canales (colores y voz correctos, sin tocar la grilla).
- **La reducción de carga se hace en el DECO (no en la app):**
  - Se midió con `top` reproductor activo: `com.android.vending` consumía **41% de CPU** y `com.google.android.gms` **31%** → le robaban hasta la mitad del hilo al decoder.
  - `pm disable-user --user 0 com.android.vending` (Play Store libre de fondo, reversible con `pm enable`).
  - `cmd appops set com.google.android.gms RUN_IN_BACKGROUND deny` (fondo de Play Services limitado).
  - Governor de CPU: se revierte la recomendación de `performance` → **`interactive`** (performance fijo calienta el H313 y en reproducción sostenida bajaba rendimiento; el foro X96Q confirma throttling del SoC 1.2→0.6 GHz por calor). Comando: `adb shell 'for c in 0 1 2 3; do echo interactive > /sys/devices/system/cpu/cpu$c/cpufreq/scaling_governor; done'`.
  - Tras optimizar: temperatura OK (48°C), app al 22% de CPU, Play fuera de top.
- **Versión app:** 1.7.12 (versionCode 23). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — HD a carga reducida según resolución (v1.7.11) [REVERTIDO]
- Metodología probada y ANULADA en v1.7.12 (ver arriba); se deja el registro histórico.
- Con Skia (1.7.10) el HD se ve bien de color pero aún entrecorta: la CPU de 1 GHz no alcanza para 1080i/p por software (el desentrelazado de 1080i es lo más caro).
- **Cambio original:** en `Settings.applyToPlayer` se lee `video-params/h`: SD (<700 px) inalterado; HD (≥700 px) `deinterlace=no` + `vd-lavc-skiploopfilter=nonintra`.
- **Versión app:** 1.7.11 (versionCode 22).

## Cambios 2026-09-11 (app) — Desactivar Impeller (v1.7.10)
- **Problema:** los canales HD del deco Q96 quedan "robotizados" con la voz desfasada (los SD perfectos con CPU). HD por software supera la CPU de 1 GHz, y el decode por hardware tiñe el video (bug conocido de MediaCodec/mpv en decos; por eso XPlayer usa ExoPlayer nativo, no arreglable aquí).
- **Hipótesis probada:** el renderer **Impeller** de Flutter (default en Android 14) causa micro-congelamientos de video en decos baratos (Mali/Allwinner). Referencias: flutter/flutter#142711, media-kit#1123 (confirma que desactivar Impeller lo arregla).
- **Cambio:** se añadió `io.flutter.embedding.android.EnableImpeller=false` en `android/app/src/main/AndroidManifest.xml` → Flutter usa **Skia**; verificado en el APK final con aapt2. No se tocó el modo Software ni los ajustes.
- **Versión app:** 1.7.10 (versionCode 21). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Fix "robotizado" y desfase voz/imagen (v1.7.9)
- El modo CPU quedaba "robotizado" y con la voz desfasada de los labios. Causas (introducidas en v1.7.8 para acelerar):
  1. `vd-lavc-fast=yes` → salta fotogramas → imagen a tirones y desfase.
  2. `deinterlace=no` → los canales entrelazados se muestran a campo saltado → "robot" y labios no cuadran con la voz.
- **Cambios:** se eliminó `vd-lavc-fast`; se restaura `deinterlace=yes`; se añade `audio-buffer=0.4` (menos cortes de audio con CPU al límite). Se mantienen `vd-lavc-threads=4` y el governor `performance` en el deco (ADB root).
- **Versión app:** 1.7.9 (versionCode 20). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Software por defecto + migración (v1.7.8)
- Confirmado: el **tinte azulado es de TODOS los canales** y proviene del decoder de hardware (MPP) de Allwinner; no se arregla con matriz de color. Solo la decodificación en CPU da color correcto.
- **Cambios:** `DecodeMode.software` vuelve a ser el default; los decos Allwinner/H313 quedan bien de color. Se añade migración (`settingsVersion=2`): en la primera apertura tras la app 1.7.8 se fuerza Software aunque hubiera configurado "hardware/auto" (evita que los decos ya instalados se queden con colores malos). Optimizaciones CPU: `deinterlace=no`, `vd-lavc-threads=4`, `vd-lavc-fast=yes`.
- **Optimización del deco (ADB root):** el Q96 (H313) tiene la CPU fijada a **1.008 GHz** (cap del firmware) y governor `interactive`. Comandos para ponerlo a máximo:
  `adb root`
  `adb shell 'for c in 0 1 2 3; do echo performance > /sys/devices/system/cpu/cpu$c/cpufreq/scaling_governor; done'`
  (4×A53 a 1 GHz, temp 56°C OK; el setting se pierde al reiniciar el deco).
- **Versión app:** 1.7.8 (versionCode 19). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Fix tinte azulado SD en hardware (v1.7.7)
- El usuario identifica el problema de color como **tinte azulado** en un canal SD → causa típica del decoder HW de Allwinner: etiqueta la matriz de color de SD (`bt.601`) como `bt.709`.
- **Solución:** en modo hardware se lee `video-params/h` tras `open()`; si el video es SD (alto ≤ 600 px) se fuerza `colormatrix=bt.601` + `colormatrix-primaries=bt.601` → colores correctos **sin perder la velocidad del hardware**. (En modo CPU el desentrelazado off + 4 hilos reducen el micro-corte pero el box 32-bit sigue al límite: hardware sigue siendo la vía correcta.)
- **Versión app:** 1.7.7 (versionCode 18). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Aceleración del modo CPU (v1.7.6)
- El modo CPU/Software daba colores correctos (como pedía el usuario, mejor que hardware) pero entrecortaba en el Q96. La causa típica: **desentrelazado por defecto** (canales SD entrelazados saturan la CPU 32-bit) + decodificación mono-hilo.
- **Solución:** en modo CPU se aplican además `deinterlace=no` y `vd-lavc-threads=4` (`Settings.applyToPlayer`, lib/settings.dart). Se mantiene el botón 🎨 por canal.
- **Versión app:** 1.7.6 (versionCode 17). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Botón de colores por canal (v1.7.5)
- El intento de corregir el color en modo hardware con `video-output-levels=limited` (v1.7.4) **empeoró** el color y causó **entrecortes** en el Q96 → **descartado**.
- **Solución final:** queda Automática (hardware) como default rápido, y se añade un **botón 🎨 por canal** en la barra de controles del reproductor (índice 3, junto a favorito/grabar): activa decodificación en CPU **solo para ese canal** (colores corregidos; puede ir lento). Estado persistente por nombre de canal en `SharedPreferences` (`setChannelSoftware`/`isChannelSoftware` en `lib/settings.dart`).
- El modo Software global se conserva en Ajustes, pero no recomendado en decos 32-bit por lentitud.
- **Versión app:** 1.7.5 (versionCode 16). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — "Cámara lenta" en decos Allwinner (v1.7.4)
- Con el fix de colores anterior (1.7.3, `hwdec=no` por defecto = Software) el deco Q96 (Allwinner sun8iw7p1, **32-bit**) reproduce a **cámara lenta**: su CPU no da para decodificar en software.
- **Solución (modos de Decodificación):**
  - **Automática** (nuevo default): `hwdec=auto-safe` — rápido (hardware).
  - **Hardware**: `hwdec=auto-safe` + `video-output-levels=limited` — rápido y corrige el **rango de color** (el decoder HW de Allwinner publica rango incorrecto → colores deslavados).
  - **Software**: `hwdec=no` — colores siempre correctos pero lento en este deco (solo para canales puntuales).
- Implementación en `lib/settings.dart` (`Settings.applyToPlayer`), llamado desde `player.dart` y `vod_play_page.dart` tras cada `open()`.
- **Versión app:** 1.7.4 (versionCode 15). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Colores en decos Allwinner
- **Problema:** en un deco Q96 (Allwinner sun8iw7p1, Android 14, salida fija 720p50) un canal que no es FullHD se veía con **colores alterados**.
- **Causa:** libmpv decodificaba por hardware (MediaCodec/Allwinner) y ese decoder descolora flujos SD/MPEG2. El selector "Decodificación" de la app solo cambiaba `vo`, no desactivaba el hardware real.
- **Solución:** la opción ahora mapea a `hwdec` de libmpv: `software` → `no` (CPU, colores correctos, default), `auto/hardware` → `auto-safe` (HW). Se aplica con `setProperty('hwdec', ...)` tras cada `open()` en `player.dart` y `vod_play_page.dart` (media_kit no expone `hwdec` en `PlayerConfiguration`).
- **Nota deco Q96:** salida HDMI fija 720p@50 → la imagen se ve algo suave en TV FullHD (límite del hardware, no de la app). Códecs HW: H.264/HEVC/VP9/MPEG2 (sin AV1).
- **Versión app:** 1.7.3 (versionCode 14). Documentado en `iptv_app/README.md`.

## Cambios 2026-09-11 (app) — Mirrors para decos chinos
- **Problema:** en un deco Android chino, con el usuario `sole` la app mostraba "No se pudieron cargar los usuarios. Verifica tu conexión a internet." aunque el usuario existía en `usuarios.json` y había internet.
- **Causa:** los archivos del repo (`usuarios.json`, `dispositivos.json`, la playlist M3U) se descargaban solo desde `raw.githubusercontent.com`, host que suele estar bloqueado en redes chinas. La validación de usuario fallaba antes de chequear cualquier cuenta.
- **Solución:** nueva `lib/mirrors.dart` en `iptv_app` que prueba en orden: `raw.githubusercontent.com` → `ghproxy.net` → `cdn.jsdelivr.net` → `gh-proxy.com`. Aplicada a auth/devices/m3u (usuarios, dispositivos y playlist).
- **Versión app:** 1.7.2 (versionCode 13), APK en `_releases/polo_tv_1.7.2.apk`. Documentado en `iptv_app/README.md`.
- Detalle: `sole` se validó en GitHub (max_disp=1, activo) y la URL responde 200 desde acá.

## Como actualizar - Scripts de busqueda
```powershell
# Buscar canal en iptv.wtf
$lines = Get-Content "iptv_wtf_real.m3u"
$lines | Where-Object { $_ -match "^#EXTINF" -and $_ -match "NombreCanal" }

# Buscar en jumangis (descargar primero)
Invoke-WebRequest "http://jumangis.cloud:2082/get.php?username=Margarito&password=tXBU2WnnL8&type=m3u" -OutFile "jumangis.m3u"
Get-Content "jumangis.m3u" | Where-Object { $_ -match "^#EXTINF" -and $_ -match "NombreCanal" }
```

## Historial de cambios
| Fecha | Canales | Cambios |
|-------|---------|---------|
| 2026-09-09 | 119 | SONY y UNIVERSAL movidos de CINE a SERIES/REALITY (24 y 25); renumerado 1-119 |
| 2026-09-09 | 119 | Canales solutionspremium movidos dentro de su categoría (CINE 47-50, SERIES/REALITY 23, INTERNACIONAL 99, NOTICIAS 102, RADIOS 113-119); renumerado 1-119; USA Network a CINE |
| 2026-09-06 | 121 | Warner/HBO latino (solutionspremium), sin duplicado HBO XTREME, agregados Sony/Universal/USA network/Adult Swim/TNT Novelas/Venus/Playboy/TVE/DW + 7 radios; eliminados TNT SD, RAI 1, Radioactiva |
| 2026-08-27 | 92 | Restaurados 12 duplicados con nombre diferenciado (Bio Bio, La Red, Mega 2, TVN, Meganoticias, CDO x2) para elegir |
| 2026-08-27 | 158 | Movida categoria DEPORTES despues de SERIES/ENTRETENIMIENTO |
| 2026-08-27 | 158 | Agregados 20 de m3u.cl (Bio Bio, La Red, CHV, CNN, Mega dps, Retro Plus, etc.), casi todos con señal |
| 2026-08-27 | 138 | Agregados 42 canales de iptv-org (13C/13 Festival/13 Kids/DIsney/Nick/Cinecanal Pacific/etc.), pedidos por usuario |
| 2026-08-27 | 96 | Agregados Mega, Canal 13, Mega 2, ESPN/FOX/CDO/TNT, HBO/Cinecanal, Disney, MTV/VH1; TV Senado al final |
| 2026-08-27 | 52 | Seleccion inversa conservando 52 canales |
| 2026-08-27 | 66 | Seleccion de 66 canales |
| 2026-08-26 | 109 | Eliminados Mega 2/13Rec/Meganoticias/Megatiempo (URLs rotas), corregidos TVN3 y CHV Noticias |
| 2026-08-26 | 113 | Eliminados USA/CA/BR, agregados TVN3/Mega2/CHV Noticias/13Rec/Meganoticias/Megatiempo/Zona Latina |
| 2026-08-26 | 157 | Reorganizado por categorias, agregado CHV |
| 2026-08-26 | 186 | Eliminadas variantes duplicadas (HD/Full HD) |
| 2026-08-26 | 290 | Playlist inicial con todos los canales de iptv.wtf |
