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
