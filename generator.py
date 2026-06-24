# 🚗 Verificador Vehicular Perú

Herramienta web para verificar un vehículo usado antes de comprarlo. Consulta **20 fuentes oficiales del Estado peruano** automáticamente usando Playwright, genera un reporte HTML completo, y guía al comprador con un checklist de inspección técnica y un veredicto final inteligente.

---

## ¿Qué verifica?

| Bloque | Fuentes |
|--------|---------|
| **Documentación** | SUNARP Vehicular, SOAT APESEG, MTC Inspección Técnica, SUNARP SPRL (historial propietarios), SUNARP SigueloPlus (monto pagado) |
| **Deudas e Infracciones** | SUTRAN, ATU, SBS Accidentes SOAT, Municipalidad Callao, GNV FISE |
| **Papeletas Regionales** | Trujillo, Piura, Chiclayo, Tarapoto, Cajamarca, Chachapoyas, Huancayo, Ica, Tacna, Arequipa |
| **Inspección Técnica** | Checklist de 45 puntos: exterior, interior, motor, chasis, prueba de manejo |
| **Veredicto Final** | APTO PARA COMPRAR / NEGOCIAR / REVISAR EN TALLER / NO RECOMENDADO |

---

## Estructura del Proyecto

```
vehicle_checker/
├── app.py                      ← Aplicación web Flask (interfaz principal)
├── main.py                     ← CLI (uso por terminal sin web)
├── config.py                   ← Configuración y URLs desde .env
├── requirements.txt
├── .env.example                ← Plantilla de credenciales
├── Procfile                    ← Para Railway / Render
├── render.yaml                 ← Configuración automática Render.com
├── .gitignore
│
├── scrapers/                   ← 20 scrapers oficiales
│   ├── base.py                 ← ResultadoConsulta dataclass
│   ├── papeleta_base.py        ← Motor genérico de papeletas
│   ├── sunarp_vehicular.py
│   ├── soat_apeseg.py
│   ├── mtc_inspeccion.py
│   ├── sunarp_sprl.py
│   ├── sunarp_siguelo.py
│   ├── sutran.py
│   ├── atu.py
│   ├── sbs_accidentes.py
│   ├── callao.py
│   ├── gnv_fise.py
│   └── [trujillo, piura, chiclayo, tarapoto, cajamarca,
│       chachapoyas, huancayo, ica, tacna, arequipa].py
│
├── inspeccion/                 ← Fase 3: Inspección técnica
│   ├── checklist.py            ← 45 ítems en 5 categorías
│   └── recomendaciones.py      ← Motor de veredicto inteligente
│
├── reporter/                   ← Generador de reporte HTML
│   ├── generator.py
│   └── templates/reporte.html
│
├── web/                        ← Plantillas de la app web
│   └── templates/
│       ├── index.html          ← Página principal
│       └── verificando.html    ← Progreso SSE + checklist + veredicto
│
└── reportes/                   ← Reportes HTML generados (gitignored)
```

---

## Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/verificador-vehicular-peru.git
cd verificador-vehicular-peru
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### 3. Configurar credenciales

```bash
cp .env.example .env
```

Editar `.env` con tus datos:

```env
# Credenciales SUNARP SPRL (registro de propietarios)
SUNARP_SPRL_USUARIO=TU_USUARIO_RUC_O_DNI
SUNARP_SPRL_CLAVE=TU_CLAVE

# Credenciales SAT Trujillo (opcional)
TRUJILLO_DNI=12345678
TRUJILLO_CELULAR=999999999
TRUJILLO_CORREO=tu@correo.com

# Configuración
TIMEOUT=30
HEADLESS=false        # false = navegador visible (para resolver CAPTCHAs)
```

### 4. Ejecutar la aplicación web

```bash
python app.py
```

Abrir en el navegador: **http://localhost:5000**

### 5. (Alternativa) Uso por terminal

```bash
python main.py B1N553
# o
python main.py        # pregunta la placa por teclado
```

---

## Uso de la App Web

1. **Ingresa la placa** del vehículo en la página principal
2. El sistema consulta automáticamente las 20 fuentes oficiales — verás el progreso en tiempo real
3. Si algún portal tiene **CAPTCHA**, el navegador se abrirá visible para que lo resuelvas
4. Al terminar la consulta, aparece el **Checklist de Inspección Técnica** (45 ítems)
5. Marca cada ítem al revisar físicamente el vehículo
6. Haz clic en **"Generar Veredicto"** para obtener las recomendaciones finales
7. Exporta a PDF con el botón de impresión

---

## Despliegue en la Nube

### Opción A — Render.com (Recomendado, gratuito)

1. Crear cuenta en [render.com](https://render.com)
2. **New → Web Service → Connect to GitHub repository**
3. Render detecta `render.yaml` automáticamente
4. En **Environment Variables**, agregar:
   - `SUNARP_SPRL_USUARIO`
   - `SUNARP_SPRL_CLAVE`
   - `TRUJILLO_DNI`, `TRUJILLO_CELULAR`, `TRUJILLO_CORREO`
   - `HEADLESS=true`
5. Deploy — Render instala Playwright y Chromium automáticamente

> **Importante:** En la nube, `HEADLESS=true` obligatorio. Los CAPTCHAs que requieran intervención manual no podrán resolverse. Se recomienda usar solo para consultas sin CAPTCHA o implementar un servicio de resolución de CAPTCHAs (2captcha, CapMonster).

### Opción B — Railway.app

1. Crear cuenta en [railway.app](https://railway.app)
2. **New Project → Deploy from GitHub repo**
3. Variables de entorno: igual que Render
4. En Settings → Nixpacks, agregar en **Build Command**:
   ```
   pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
   ```
5. **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 300`

### Opción C — VPS / Servidor propio (Ubuntu)

```bash
# Instalar dependencias del sistema
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv

# Clonar y configurar
git clone https://github.com/TU_USUARIO/verificador-vehicular-peru.git
cd verificador-vehicular-peru
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
playwright install-deps chromium

# Configurar .env
cp .env.example .env
nano .env  # editar credenciales, HEADLESS=true

# Ejecutar con Gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 1 --threads 4 --timeout 300 --daemon

# O con systemd (recomendado para producción)
sudo nano /etc/systemd/system/verificador.service
```

Contenido del servicio systemd:
```ini
[Unit]
Description=Verificador Vehicular Peru
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/verificador-vehicular-peru
Environment=PATH=/home/ubuntu/verificador-vehicular-peru/venv/bin
ExecStart=/home/ubuntu/verificador-vehicular-peru/venv/bin/gunicorn app:app --bind 0.0.0.0:5000 --workers 1 --threads 4 --timeout 300
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable verificador
sudo systemctl start verificador
```

---

## Notas Técnicas

### CAPTCHAs
Varios portales del Estado peruano (SUNARP, SUTRAN, etc.) implementan reCAPTCHA. La aplicación:
- En modo `HEADLESS=false`: abre el navegador visible y espera hasta 60 segundos para que el usuario resuelva el CAPTCHA manualmente.
- En modo `HEADLESS=true` (nube): si hay CAPTCHA, el scraper retorna `estado=error` y continúa con los demás portales.

### Seguridad de credenciales
- **NUNCA subir el archivo `.env` al repositorio.** Está incluido en `.gitignore`.
- Las credenciales de SUNARP SPRL son las de tu cuenta registrada en el portal.
- En producción, usar las variables de entorno del proveedor cloud (Render, Railway).

### Limitaciones
- Las consultas son secuenciales (un portal a la vez) para respetar los servidores del Estado.
- El tiempo total de consulta es de 5-15 minutos dependiendo de la velocidad de respuesta de cada portal.
- Algunos portales regionales pueden estar inactivos temporalmente.

---

## Tecnologías

| Componente | Tecnología |
|------------|-----------|
| Scraping | Python + Playwright (Chromium) |
| Web framework | Flask 3.x |
| Progreso en tiempo real | Server-Sent Events (SSE) |
| Templates | Jinja2 |
| Reportes | HTML + CSS (exportable a PDF) |
| Despliegue | Gunicorn + Render / Railway / VPS |

---

## Licencia

MIT — Uso libre con fines informativos. No afiliado al Estado peruano.

Los datos provienen de portales públicos oficiales. El uso de esta herramienta debe respetar los términos de servicio de cada portal consultado.
