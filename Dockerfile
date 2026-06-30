# ── Verificador Vehicular Peru ── Dockerfile ──────────────────────────────────
# Compatible con: Render.com (Docker), Railway, Fly.io, VPS Ubuntu/Debian
# NO compatible con: Vercel, AWS Lambda, Google Cloud Functions (serverless)
# porque requiere Playwright (Chromium) y conexiones SSE de larga duracion.

FROM python:3.11-slim

# ── Dependencias del sistema para Chromium / Playwright ──────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Chromium core
    libnss3 libnspr4 \
    libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libasound2 \
    libpango-1.0-0 libpangocairo-1.0-0 \
    libcairo2 libxshmfence1 \
    # Fuentes
    fonts-liberation fonts-noto-color-emoji \
    # Utilidades
    ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# ── Directorio de trabajo ─────────────────────────────────────────────────────
WORKDIR /app

# ── Instalar dependencias Python ──────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Instalar Chromium via Playwright ─────────────────────────────────────────
RUN playwright install chromium

# ── Copiar codigo fuente ──────────────────────────────────────────────────────
COPY . .

# ── Crear carpeta de reportes ─────────────────────────────────────────────────
RUN mkdir -p reportes

# ── Variables de entorno por defecto (sobreescribir en la plataforma) ─────────
ENV HEADLESS=true
ENV TIMEOUT=30
ENV PORT=8000

# ── Puerto expuesto ───────────────────────────────────────────────────────────
EXPOSE 8000

# ── Servidor de produccion ────────────────────────────────────────────────────
CMD gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 4 \
    --timeout 300 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile -
