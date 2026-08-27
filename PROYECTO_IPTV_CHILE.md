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

## Canales por categoria (80 total)

### NACIONALES (47)
| Canal | Fuente | URL |
|-------|--------|-----|
| 24 Horas | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/2109.ts |
| CL: CHV | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/9049.ts |
| CHV Noticias | rudo.video | https://redirector.rudo.video/hls-video/339f69c6122f6d8f4574732c235f09b7683e31a5/chvn/chvn.smil/playlist.m3u8 |
| CL: Canal 13 | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/9752.ts |
| CL: Mega | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/7469.ts |
| Mega 2 | jumangis | http://jumangis.cloud:2082/Mmt5YzNXVTlNclVRbEQ0K3pBakV6TEt5SkFaYVhieWRWRFNsa3FJZVprdz0 |
| CL: NTV | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/10501.ts |
| CL: TV + | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/14874.ts |
| TVN3 | mdstrm | https://mdstrm.com/live-stream-playlist/5653641561b4eba30a7e4929.m3u8 |
| CL: UCV | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/14893.ts |
| T13 | iptv.wtf | http://iptv.wtf:80/live/gxdcxnbf/1eZr21rf1D/2111.ts |
| Zona Latina | iptv-org | http://45.162.193.35/ZONALATINA/index.m3u8 |

### DEPORTES (30)
- CDO, CDO 2, CDO HD (iptv.wtf)
- CL: ESPN, ESPN 2, ESPN 3, ESPN Extra (iptv.wtf)
- ESPN, ESPN 2, ESPN 3 (general) + variantes Argentina/Peru/Sur (iptv.wtf)
- ESPN Deportes, ESPN News, ESPN Premium ARG, ESPN Sur (iptv.wtf)
- Fox Sports HD, Fox Sports 2 HD, Fox Sports 3 HD (iptv.wtf)
- TNT Sports, TNT Sports 3, TNT Sports HD ARG, TNT Sports Premium, TyC Sports (iptv.wtf)

### PELICULAS (16)
- AMC, Cinecanal HD, Cinemax, Golden Edge, Studio Universal (iptv.wtf)
- HBO, HBO 2, HBO Family, HBO Mundi, HBO Plus, HBO Pop, HBO Signature, HBO Xtreme (iptv.wtf)

### SERIES / ENTRETENIMIENTO (13)
- AXN, Comedy Central, E!, Space, TNT, TNT Series, Warner Channel (iptv.wtf)

### INFANTILES (13)
- Cartoonito, Discovery Kids (iptv.wtf)
- Disney Channel, Disney Channel HD, Disney Jr HD (iptv.wtf)

### DOCUMENTALES / ESTILO DE VIDA (12)
- A&E, Animal Planet, Discovery Home and Health, Discovery Science, Discovery TLC, Discovery Turbo, Food Network, H2, Investigation Discovery, Love Nature (iptv.wtf)

### MUSICA (12)
- MTV 80s (iptv.wtf)
- MTV Latino, MTV FHD (MX), MTV Live (MX), MTV Hits (MX), VH1 Classic (MX) (jumangis)

### INTERNACIONALES (5)
- AR: Telefe, Arirang, Arirang HD, ES: Antena 3, Europa Europa (iptv.wtf)

### TELETRAK + RADIO BIO BIO + TV SENADO (al final, 10)
- CL: TV Senado, CL: Teletrak (iptv.wtf)
- Radio Bio Bio: Concepcion, Los Angeles, Osorno, Puerto Montt, Santiago, Temuco, Valdivia, Valparaiso (iptv.wtf)

## Canales agregados desde m3u.cl (20, 2026-08-27)
Casi todos con señal real (solo Meganoticias queda 401 por token):
- **NACIONALES:** Bio Bio TV (rudo), La Red (circa), TV+ (rudo), TV Chile (mdstrm), TVN (intersurtv), NTV (mdstrm), TVN 24 Horas (mdstrm), Mega (dps), Meganoticias (401), CHV (rudo), Canal 13 (dps), 13 Internacional, 13 popup, T13 (rudo), T13 Radio, CNN Chile
- **DEPORTES:** CHV Deportes (rudo)
- **MUSICA:** Retro Plus TV, Retro Plus TV Senal 2, Retro Plus TV Senal 3 (cdnz)
- Ya estaban (mismo URL): TVN3, CHV Noticias, 13 go

## Canales agregados desde iptv-org (42, 2026-08-27)
Pedidos por el usuario. Incluidos en la playlist aunque muchos NO tienen seÃ±al (se agregaron todos por pedido explicito):
- **Con seÃ±al real (funcionan):** 13C, 13 Entretencion, 13 Festival, 13 Humor, 13 Kids, 13 Prime, 13 Realities, 13 Teleseries (dpsgo), Cinecanal Pacific, Disney Channel Panregional, Disney Jr HD, Nick Jr, TV Chile (mdstrm)
- **Sin seÃ±al (tlink muerto / 403 / stub):** 13Rec, 24 Horas(org), AXN(org), Bio Bio TV, Canal 13(org), CHV Noticias(org), CDO, ChileVision, Comedy Central(org), Disney Channel(org), E!(org), ETC TV, FM Plus TV, La Red, Mega(org), Mega 2, Mega Ficcion, Meganoticias Ahora, Megatiempo, MTV Latin America, Nickelodeon(org), Telemundo Internacional, TVN, TVN3(org), TVR, UCV TV(org), Via X, Disney Jr(org)
- **Cert SSL (probar en app):** T13 En Vivo, TV+ (org)

## Canales sin seÃ±al (resumen)
- Meganoticias/Megatiempo/13Rec solo en CDN tlink muerto o HTTP 401/403 (protegidos). Se incluyeron de todas formas por pedido del usuario.

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
| 2026-08-27 | 80 | Eliminados 78 por pedido: CL CHV/Canal13/Mega, Bio Bio, La Red, Mega 2, HBO, ESPN (solo quedan Peru), CDO, Fox, TNT Sports, todos (org) excepto E!, etc. |
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
