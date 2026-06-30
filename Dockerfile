# ── Verificador Vehicular Peru ── Dockerfile ─────────────────────────────────────────
# Compatible con: Render.com (Docker), Railway, Fly.io, VPS Ubuntu/Debian
# NO compatible con: Vercel, AWS Lambda, Google Cloud Functions (serverless)
# porque requiere Playwright (Chromium) y conexiones SSE de larga duracion.

FROM python:3.11-slim

# Herramientas base minimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Chromium con TODAS sus dependencias del sistema (forma correcta para Docker)
RUN playwright install --with-deps chromium

COPY . .

RUN mkdir -p reportes

ENV HEADLESS=true
ENV TIMEOUT=30
ENV PORT=8000
ENV PYTHONPATH=/app

EXPOSE 8000

CMD gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 4 \
    --timeout 300 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile -
