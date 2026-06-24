# Verificador Vehicular Peru

Aplicacion web que consulta **20 fuentes oficiales** antes de comprar un auto usado:
SUNARP, SOAT, MTC, SUTRAN, ATU, SBS, municipalidades de 10 regiones y mas.

---

## Importante: Plataformas compatibles

| Plataforma | Compatible | Motivo |
|---|---|---|
| **Render.com** (Docker) | Si | Soporta Docker + Chromium |
| **Railway.app** | Si | Soporta Docker + Chromium |
| **Fly.io** | Si | Soporta Docker + Chromium |
| **VPS Ubuntu/Debian** | Si | Control total |
| Vercel | NO | Serverless, sin soporte Playwright |
| AWS Lambda | NO | Serverless, sin soporte Playwright |
| Google Cloud Functions | NO | Serverless, sin soporte Playwright |
| Netlify | NO | Serverless, sin soporte Playwright |

> La app usa Playwright (Chromium) para automatizar navegadores reales.
> Las plataformas serverless no pueden ejecutar navegadores.

---

## Despliegue en Render.com (Recomendado)

1. Sube la carpeta `vehicle_checker/` a un repositorio GitHub
2. En Render.com: **New > Web Service**
3. Conecta tu repositorio de GitHub
4. Render detecta el `render.yaml` automaticamente → click **Apply**
5. En **Environment Variables** agrega:
   ```
   SUNARP_SPRL_USUARIO=TU_USUARIO
   SUNARP_SPRL_CLAVE=TU_CLAVE
   TRUJILLO_DNI=45975202
   TRUJILLO_CELULAR=969762557
   TRUJILLO_CORREO=informesautoescuela@gmail.com
   ```
6. Click **Deploy** — el primer build tarda ~5 min (descarga Chromium)

---

## Despliegue en Railway.app

1. Instala Railway CLI: `npm install -g @railway/cli`
2. Desde la carpeta `vehicle_checker/`:
   ```bash
   railway login
   railway init
   railway up
   ```
3. Configura variables de entorno en el dashboard de Railway

---

## Despliegue en VPS Ubuntu

```bash
# 1. Clonar / subir el proyecto
git clone https://github.com/TU_USUARIO/verificador-vehicular.git
cd verificador-vehicular/vehicle_checker

# 2. Instalar Docker
curl -fsSL https://get.docker.com | sh

# 3. Crear .env con tus credenciales
cp .env.example .env
nano .env

# 4. Construir y correr
docker build -t verificador-vehicular .
docker run -d \
  --name verificador \
  --env-file .env \
  -p 80:8000 \
  --restart unless-stopped \
  verificador-vehicular

# La app estara disponible en http://TU_IP
```

---

## Instalacion local (desarrollo)

```bash
# Requisitos: Python 3.10+
cd vehicle_checker

# Instalar dependencias
pip install -r requirements.txt
playwright install chromium

# Configurar credenciales
cp .env.example .env
# Editar .env con tus datos reales

# Iniciar
python app.py
# Abrir: http://localhost:5000
```

---

## Estructura del proyecto

```
vehicle_checker/
├── app.py                  # Aplicacion Flask (rutas, SSE, masivo)
├── config.py               # URLs y configuracion
├── main.py                 # Orquestador CLI (uso sin web)
├── requirements.txt        # Dependencias Python
├── Dockerfile              # Para despliegue Docker
├── render.yaml             # Config Render.com (auto-detectado)
├── railway.toml            # Config Railway.app
├── Procfile                # Para Heroku / Dokku
├── .env.example            # Plantilla de variables de entorno
├── scrapers/               # 20 scrapers (SUNARP, SOAT, MTC, regiones...)
├── reporter/               # Generador de reporte HTML
├── inspeccion/             # Checklist 45 puntos + motor de recomendaciones
├── utils/                  # Extractor de placas (Excel, Word, PDF)
└── web/templates/          # Templates HTML (landing, progreso, masivo)
```

---

## Uso: Consulta Individual

1. Ingresa la placa en la pagina principal
2. Espera mientras se consultan las 20 fuentes (puede tardar 2-5 min)
3. Completa el checklist de inspeccion visual (45 puntos)
4. Obtiene el veredicto: COMPRAR / NEGOCIAR / REVISAR_TALLER / NO_COMPRAR

## Uso: Carga Masiva

1. Selecciona la pestana "Carga Masiva"
2. Sube un archivo Excel, Word o PDF con las placas
3. El sistema detecta las placas automaticamente
4. Click "Iniciar Verificacion Masiva" — se procesan de a una
5. Descarga el reporte CSV al finalizar

---

## Variables de entorno

| Variable | Descripcion | Requerida |
|---|---|---|
| `SUNARP_SPRL_USUARIO` | Usuario SUNARP SPRL | Si |
| `SUNARP_SPRL_CLAVE` | Clave SUNARP SPRL | Si |
| `TRUJILLO_DNI` | DNI para SAT Trujillo | Si |
| `TRUJILLO_CELULAR` | Celular para SAT Trujillo | Si |
| `TRUJILLO_CORREO` | Correo para SAT Trujillo | Si |
| `HEADLESS` | `true` en produccion, `false` en desarrollo | No |
| `TIMEOUT` | Segundos por pagina (default: 30) | No |
| `SECRET_KEY` | Clave secreta Flask | No |
| `PORT` | Puerto del servidor (default: 8000) | No |
