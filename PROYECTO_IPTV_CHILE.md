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

## Canales por categoria (96 total)

### NACIONALES (12)
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

### PELICULAS (13)
- AMC, Cinecanal HD, Cinemax, Golden Edge, Studio Universal (iptv.wtf)
- HBO, HBO 2, HBO Family, HBO Mundi, HBO Plus, HBO Pop, HBO Signature, HBO Xtreme (iptv.wtf)

### SERIES / ENTRETENIMIENTO (7)
- AXN, Comedy Central, E!, Space, TNT, TNT Series, Warner Channel (iptv.wtf)

### INFANTILES (5)
- Cartoonito, Discovery Kids (iptv.wtf)
- Disney Channel, Disney Channel HD, Disney Jr HD (iptv.wtf)

### DOCUMENTALES / ESTILO DE VIDA (10)
- A&E, Animal Planet, Discovery Home and Health, Discovery Science, Discovery TLC, Discovery Turbo, Food Network, H2, Investigation Discovery, Love Nature (iptv.wtf)

### MUSICA (6)
- MTV 80s (iptv.wtf)
- MTV Latino, MTV FHD (MX), MTV Live (MX), MTV Hits (MX), VH1 Classic (MX) (jumangis)

### INTERNACIONALES (5)
- AR: Telefe, Arirang, Arirang HD, ES: Antena 3, Europa Europa (iptv.wtf)

### TELETRAK + RADIO BIO BIO + TV SENADO (al final, 10)
- CL: TV Senado, CL: Teletrak (iptv.wtf)
- Radio Bio Bio: Concepcion, Los Angeles, Osorno, Puerto Montt, Santiago, Temuco, Valdivia, Valparaiso (iptv.wtf)

## Canales NO disponibles (sin señal)
- Meganoticias, Megatiempo, 13Rec/Rec13: no existen con señal jugable en ninguna fuente (tlink/dps muertos, pirostv Meganoticias protegida 401, no estan en iptv.wtf ni jumangis). Solo en YouTube en vivo (no jugable directo en M3U).

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
| 2026-08-27 | 96 | Agregados Mega, Canal 13, Mega 2, ESPN/FOX/CDO/TNT, HBO/Cinecanal, Disney, MTV/VH1; TV Senado al final |
| 2026-08-27 | 52 | Seleccion inversa conservando 52 canales |
| 2026-08-27 | 66 | Seleccion de 66 canales |
| 2026-08-26 | 109 | Eliminados Mega 2/13Rec/Meganoticias/Megatiempo (URLs rotas), corregidos TVN3 y CHV Noticias |
| 2026-08-26 | 113 | Eliminados USA/CA/BR, agregados TVN3/Mega2/CHV Noticias/13Rec/Meganoticias/Megatiempo/Zona Latina |
| 2026-08-26 | 157 | Reorganizado por categorias, agregado CHV |
| 2026-08-26 | 186 | Eliminadas variantes duplicadas (HD/Full HD) |
| 2026-08-26 | 290 | Playlist inicial con todos los canales de iptv.wtf |
