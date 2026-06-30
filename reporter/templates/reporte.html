<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Reporte Vehicular — {{ placa }}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f4f8; color: #1a202c; font-size: 14px; line-height: 1.6; }
    a { color: #2b6cb0; }
    :root {
      --ok: #276749; --ok-bg: #f0fff4; --ok-border: #68d391;
      --warn: #744210; --warn-bg: #fffbeb; --warn-border: #f6ad55;
      --error: #742a2a; --error-bg: #fff5f5; --error-border: #fc8181;
      --neutral: #2d3748; --neutral-bg: #edf2f7; --neutral-border: #a0aec0;
      --accent: #2b6cb0;
    }

    /* Header */
    header { background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 100%); color: white; padding: 28px 40px; display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap; }
    header .logo-area h1 { font-size: 24px; font-weight: 700; }
    header .logo-area p { font-size: 12px; opacity: 0.85; margin-top: 4px; }
    .placa-badge { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.4); border-radius: 12px; padding: 10px 24px; text-align: center; }
    .placa-badge .label { font-size: 10px; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px; }
    .placa-badge .placa { font-size: 28px; font-weight: 900; letter-spacing: 4px; margin-top: 2px; }
    header .fecha { font-size: 11px; opacity: 0.75; text-align: right; }

    /* Layout */
    main { max-width: 980px; margin: 28px auto; padding: 0 16px 60px; }

    /* Resumen ejecutivo */
    .resumen { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 28px; }
    .resumen-card { background: white; border-radius: 10px; padding: 16px 12px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.08); border-top: 4px solid var(--accent); }
    .resumen-card .numero { font-size: 32px; font-weight: 800; line-height: 1; }
    .resumen-card .etiqueta { font-size: 10px; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 5px; }
    .resumen-card.ok { border-color: var(--ok-border); } .resumen-card.ok .numero { color: var(--ok); }
    .resumen-card.warn { border-color: var(--warn-border); } .resumen-card.warn .numero { color: var(--warn); }
    .resumen-card.error { border-color: var(--error-border); } .resumen-card.error .numero { color: var(--error); }

    /* Grupos / Secciones */
    section.grupo { margin-bottom: 28px; }
    .grupo-titulo { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #4a5568; border-bottom: 2px solid #e2e8f0; padding-bottom: 7px; margin-bottom: 14px; }

    /* Tarjeta de consulta */
    .consulta-card { background: white; border-radius: 10px; border-left: 5px solid var(--neutral-border); box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 12px; overflow: hidden; }
    .consulta-card.ok          { border-left-color: var(--ok-border); }
    .consulta-card.advertencia { border-left-color: var(--warn-border); }
    .consulta-card.error       { border-left-color: var(--error-border); }
    .consulta-card.sin_datos   { border-left-color: var(--neutral-border); }

    .card-header { display: flex; align-items: center; gap: 10px; padding: 12px 18px; cursor: pointer; user-select: none; }
    .estado-badge { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 3px 9px; border-radius: 20px; white-space: nowrap; }
    .ok .estado-badge          { background: var(--ok-bg);      color: var(--ok);      border: 1px solid var(--ok-border); }
    .advertencia .estado-badge { background: var(--warn-bg);    color: var(--warn);    border: 1px solid var(--warn-border); }
    .error .estado-badge       { background: var(--error-bg);   color: var(--error);   border: 1px solid var(--error-border); }
    .sin_datos .estado-badge   { background: var(--neutral-bg); color: var(--neutral); border: 1px solid var(--neutral-border); }

    .card-header .fuente { font-weight: 600; font-size: 14px; flex: 1; }
    .card-header .url { font-size: 10px; color: #718096; }
    .card-header .toggle { font-size: 16px; color: #a0aec0; }

    .card-body { padding: 0 18px 14px; border-top: 1px solid #edf2f7; }

    /* Tablas de datos */
    .datos-tabla { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .datos-tabla tr:nth-child(even) { background: #f7fafc; }
    .datos-tabla td { padding: 7px 10px; font-size: 13px; border-bottom: 1px solid #edf2f7; }
    .datos-tabla td:first-child { font-weight: 600; color: #4a5568; width: 38%; }

    .infracciones-tabla { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }
    .infracciones-tabla th { background: #2d3748; color: white; padding: 7px 9px; text-align: left; font-weight: 600; }
    .infracciones-tabla td { padding: 6px 9px; border-bottom: 1px solid #edf2f7; }
    .infracciones-tabla tr:nth-child(even) td { background: #fff8f0; }

    /* Alertas */
    .mensaje-alerta { margin-top: 9px; padding: 9px 12px; border-radius: 7px; font-size: 13px; font-weight: 500; }
    .ok .mensaje-alerta          { background: var(--ok-bg);      color: var(--ok); }
    .advertencia .mensaje-alerta { background: var(--warn-bg);    color: var(--warn); }
    .error .mensaje-alerta       { background: var(--error-bg);   color: var(--error); }
    .sin_datos .mensaje-alerta   { background: var(--neutral-bg); color: var(--neutral); }

    /* Grid para papeletas regionales (2 columnas) */
    .grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    @media (max-width: 680px) { .grid-2col { grid-template-columns: 1fr; } }

    /* Botón PDF */
    .btn-pdf { position: fixed; bottom: 24px; right: 24px; background: var(--accent); color: white; border: none; border-radius: 50px; padding: 12px 22px; font-size: 14px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 14px rgba(43,108,176,0.4); }
    .btn-pdf:hover { background: #2c5282; }

    footer { text-align: center; color: #a0aec0; font-size: 11px; padding: 18px; margin-top: 32px; border-top: 1px solid #e2e8f0; }

    @media print {
      body { background: white; }
      .btn-pdf { display: none; }
      header { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
      .consulta-card, .grid-2col > div { break-inside: avoid; }
    }
  </style>
</head>
<body>

<!-- ── HEADER ────────────────────────────────────────────────────────────── -->
<header>
  <div class="logo-area">
    <h1>🚗 Verificador Vehicular — Perú</h1>
    <p>Consulta integral antes de comprar un vehículo usado</p>
  </div>
  <div class="placa-badge">
    <div class="label">Placa consultada</div>
    <div class="placa">{{ placa }}</div>
  </div>
  <div class="fecha">Generado el<br><strong>{{ fecha }}</strong></div>
</header>

<!-- ── MAIN ───────────────────────────────────────────────────────────────── -->
<main>

  <!-- Resumen ejecutivo -->
  <div class="resumen">
    <div class="resumen-card ok">
      <div class="numero">{{ conteo.ok }}</div>
      <div class="etiqueta">✅ Sin problemas</div>
    </div>
    <div class="resumen-card warn">
      <div class="numero">{{ conteo.advertencia }}</div>
      <div class="etiqueta">⚠️ Advertencias</div>
    </div>
    <div class="resumen-card error">
      <div class="numero">{{ conteo.error }}</div>
      <div class="etiqueta">🚨 Errores</div>
    </div>
    <div class="resumen-card">
      <div class="numero" style="color:#718096">{{ conteo.sin_datos }}</div>
      <div class="etiqueta">ℹ️ Sin datos</div>
    </div>
    <div class="resumen-card">
      <div class="numero" style="color:#2b6cb0">{{ conteo.total }}</div>
      <div class="etiqueta">📊 Total consul.</div>
    </div>
  </div>

  <!-- ── Macro para renderizar una tarjeta ─────────────────────────────── -->
  {% macro tarjeta(r) %}
  <div class="consulta-card {{ r.estado }}">
    <div class="card-header" onclick="toggleCard(this)">
      <span class="estado-badge">
        {% if r.estado == 'ok' %}✅ OK
        {% elif r.estado == 'advertencia' %}⚠️ ADVERTENCIA
        {% elif r.estado == 'error' %}🚨 ERROR
        {% else %}ℹ️ SIN DATOS{% endif %}
      </span>
      <span class="fuente">{{ r.fuente }}</span>
      <span class="url"><a href="{{ r.url }}" target="_blank">{{ r.url }}</a></span>
      <span class="toggle">▾</span>
    </div>
    <div class="card-body">
      {% set lista = r.datos.get('infracciones') or r.datos.get('multas') or r.datos.get('papeletas') %}
      {% if lista is not none %}
        {% if lista | length == 0 %}
          <p style="color:var(--ok);font-weight:600;margin-top:10px;">✅ Sin registros.</p>
        {% else %}
          <table class="infracciones-tabla">
            <thead><tr>{% for k in lista[0].keys() %}<th>{{ k }}</th>{% endfor %}</tr></thead>
            <tbody>{% for item in lista %}<tr>{% for v in item.values() %}<td>{{ v }}</td>{% endfor %}</tr>{% endfor %}</tbody>
          </table>
        {% endif %}
      {% elif r.datos %}
        <table class="datos-tabla">
          {% for clave, valor in r.datos.items() %}
          {% if clave not in ['infracciones','multas','papeletas','resumen','total'] %}
          <tr><td>{{ clave }}</td><td>{{ valor }}</td></tr>
          {% endif %}
          {% endfor %}
        </table>
      {% endif %}
      {% if r.mensaje %}<div class="mensaje-alerta">{{ r.mensaje }}</div>{% endif %}
    </div>
  </div>
  {% endmacro %}

  <!-- ── BLOQUE 1: Documentación ──────────────────────────────────────── -->
  <section class="grupo">
    <div class="grupo-titulo">📋 Bloque 1 — Documentación del Vehículo</div>
    {% for r in resultados_doc %}{{ tarjeta(r) }}{% endfor %}
  </section>

  <!-- ── BLOQUE 2: Deudas e Infracciones ──────────────────────────────── -->
  <section class="grupo">
    <div class="grupo-titulo">🚦 Bloque 2 — Deudas e Infracciones</div>
    {% for r in resultados_deudas %}{{ tarjeta(r) }}{% endfor %}
  </section>

  <!-- ── BLOQUE 3: Papeletas Regionales ───────────────────────────────── -->
  {% if resultados_regiones %}
  <section class="grupo">
    <div class="grupo-titulo">📍 Bloque 3 — Papeletas Regionales</div>
    <div class="grid-2col">
      {% for r in resultados_regiones %}{{ tarjeta(r) }}{% endfor %}
    </div>
  </section>
  {% endif %}

</main>

<footer>
  Reporte generado automáticamente | Verificador Vehicular Perú | {{ fecha }}<br>
  Fuentes: SUNARP · APESEG · MTC · SUTRAN · ATU · SBS · FISE · SATs municipales
</footer>

<button class="btn-pdf" onclick="window.print()">🖨️ Exportar PDF</button>

<script>
  function toggleCard(header) {
    const body = header.nextElementSibling;
    const toggle = header.querySelector('.toggle');
    const hidden = body.style.display === 'none';
    body.style.display = hidden ? 'block' : 'none';
    toggle.textContent = hidden ? '▾' : '▸';
  }
</script>
</body>
</html>
