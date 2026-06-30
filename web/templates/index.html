<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Verificador Vehicular Peru</title>
  <style>
    :root{
      --azul:#1a365d;--azul2:#2b6cb0;--azul3:#ebf8ff;
      --verde:#276749;--verde2:#c6f6d5;
      --rojo:#c53030;--rojo2:#fed7d7;
      --amarillo:#744210;--amarillo2:#fefcbf;
      --gris:#4a5568;--gris2:#718096;--gris3:#e2e8f0;
      --blanco:#ffffff;
    }
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#f7fafc;color:#2d3748}
    .hero{background:linear-gradient(135deg,var(--azul) 0%,var(--azul2) 100%);padding:60px 20px 80px;text-align:center;color:white}
    .hero-icon{font-size:64px;display:block;margin-bottom:16px}
    .hero h1{font-size:clamp(24px,5vw,42px);font-weight:900;letter-spacing:-0.5px;margin-bottom:12px}
    .hero p{font-size:clamp(14px,2.5vw,18px);opacity:.9;max-width:640px;margin:0 auto 36px;line-height:1.6}
    .form-card{background:white;border-radius:20px;padding:32px 28px;max-width:520px;margin:0 auto;box-shadow:0 20px 60px rgba(0,0,0,0.15)}
    .form-label{display:block;font-size:13px;font-weight:700;color:var(--azul);text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
    .form-input-wrap{display:flex;gap:10px;margin-bottom:8px}
    .form-input{flex:1;padding:14px 18px;border:2px solid var(--gris3);border-radius:12px;font-size:17px;font-weight:700;letter-spacing:2px;text-transform:uppercase;outline:none;transition:border-color .2s}
    .form-input:focus{border-color:var(--azul2)}
    .btn-verificar{padding:14px 22px;background:linear-gradient(135deg,var(--azul),var(--azul2));color:white;border:none;border-radius:12px;font-size:15px;font-weight:800;cursor:pointer;white-space:nowrap;transition:opacity .2s}
    .btn-verificar:hover{opacity:.9}
    .form-hint{font-size:11px;color:var(--gris2);text-align:center;margin-top:4px}
    .error-msg{background:var(--rojo2);color:var(--rojo);border:1px solid #fc8181;border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:14px;font-weight:600}

    /* ── TABS ── */
    .tabs{display:flex;gap:0;margin-bottom:20px;border-radius:10px;overflow:hidden;border:2px solid var(--gris3)}
    .tab{flex:1;padding:11px 10px;text-align:center;font-size:13px;font-weight:700;cursor:pointer;background:var(--gris3);color:var(--gris);border:none;transition:all .2s}
    .tab.activo{background:var(--azul2);color:white}
    .panel{display:none}
    .panel.activo{display:block}

    /* ── Zona de carga masiva ── */
    .drop-zone{border:2px dashed rgba(43,108,176,0.4);border-radius:12px;padding:30px 20px;text-align:center;cursor:pointer;transition:all .2s;margin-bottom:14px;background:var(--azul3)}
    .drop-zone:hover,.drop-zone.drag-over{border-color:var(--azul2);background:#dbeafe}
    .drop-icon{font-size:36px;display:block;margin-bottom:8px}
    .drop-label{font-size:14px;font-weight:600;color:var(--azul);margin-bottom:4px}
    .drop-hint{font-size:11px;color:var(--gris2)}
    #inputArchivo{display:none}
    .placas-detectadas{display:none;margin-top:14px}
    .placas-titulo{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--gris2);margin-bottom:8px}
    .placas-grid{display:flex;flex-wrap:wrap;gap:7px;max-height:160px;overflow-y:auto;margin-bottom:14px}
    .placa-tag{background:var(--azul3);color:var(--azul2);border:1px solid #bee3f8;border-radius:6px;padding:4px 10px;font-size:13px;font-weight:700;letter-spacing:1.5px;display:flex;align-items:center;gap:5px}
    .placa-tag .remove{cursor:pointer;color:#a0aec0;font-size:15px;line-height:1}
    .placa-tag .remove:hover{color:var(--rojo)}
    .btn-iniciar{width:100%;padding:13px;background:linear-gradient(135deg,var(--azul),var(--azul2));color:white;border:none;border-radius:10px;font-size:15px;font-weight:800;cursor:pointer;transition:opacity .2s}
    .btn-iniciar:hover{opacity:.9}
    .btn-iniciar:disabled{opacity:.5;cursor:not-allowed}
    .cargando-msg{font-size:12px;color:var(--gris2);text-align:center;margin-top:8px;min-height:16px}
    .limite-msg{font-size:11px;color:var(--gris2);margin-top:6px;text-align:right}

    /* Resto de la pagina */
    .fuentes{padding:60px 20px;max-width:960px;margin:0 auto}
    .fuentes h2{font-size:24px;font-weight:800;color:var(--azul);text-align:center;margin-bottom:8px}
    .fuentes-sub{text-align:center;color:var(--gris2);font-size:14px;margin-bottom:36px}
    .fuentes-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
    .fuente-card{background:white;border-radius:14px;padding:20px;border:1px solid var(--gris3);transition:box-shadow .2s}
    .fuente-card:hover{box-shadow:0 4px 20px rgba(0,0,0,0.08)}
    .fuente-icon{font-size:28px;margin-bottom:10px}
    .fuente-nombre{font-size:13px;font-weight:700;color:var(--azul);margin-bottom:4px}
    .fuente-desc{font-size:12px;color:var(--gris2);line-height:1.5}
    .como{background:var(--azul);color:white;padding:60px 20px;text-align:center}
    .como h2{font-size:24px;font-weight:800;margin-bottom:40px}
    .pasos{display:flex;gap:24px;justify-content:center;flex-wrap:wrap;max-width:800px;margin:0 auto}
    .paso{background:rgba(255,255,255,0.1);border-radius:16px;padding:24px;width:200px}
    .paso-num{font-size:36px;font-weight:900;color:rgba(255,255,255,0.3);margin-bottom:8px}
    .paso-titulo{font-size:14px;font-weight:700;margin-bottom:6px}
    .paso-desc{font-size:12px;opacity:.8;line-height:1.5}
    footer{background:var(--azul);color:rgba(255,255,255,0.7);text-align:center;padding:24px 20px;font-size:12px;margin-top:1px}
  </style>
</head>
<body>

<section class="hero">
  <span class="hero-icon">&#x1F697;</span>
  <h1>Verificador Vehicular Peru</h1>
  <p>Consulta 20 fuentes oficiales antes de comprar un auto usado. Documentacion, deudas, papeletas e inspeccion tecnica en un solo reporte.</p>

  <div class="form-card">
    {% if error %}
    <div class="error-msg">&#x26A0;&#xFE0F; {{ error }}</div>
    {% endif %}

    <!-- Pestanas -->
    <div class="tabs">
      <button class="tab activo" onclick="cambiarTab('individual',this)">&#x1F50D; Consulta Individual</button>
      <button class="tab" onclick="cambiarTab('masivo',this)">&#x1F4CB; Carga Masiva</button>
    </div>

    <!-- Panel individual -->
    <div class="panel activo" id="panel-individual">
      <label class="form-label">Ingresa la placa del vehiculo</label>
      <form method="POST" action="/consultar">
        <div class="form-input-wrap">
          <input class="form-input" type="text" name="placa"
                 placeholder="Ej: B1N553"
                 maxlength="8" autocomplete="off" autofocus
                 pattern="[A-Za-z0-9\-\s]{5,8}" required/>
          <button class="btn-verificar" type="submit">
            &#x1F50D; Verificar
          </button>
        </div>
        <p class="form-hint">Formatos validos: B1N553 &middot; ABC123 &middot; A8R-215</p>
      </form>
    </div>

    <!-- Panel masivo -->
    <div class="panel" id="panel-masivo">
      <label class="form-label">Sube tu archivo con las placas</label>
      <div class="drop-zone" id="dropZone" onclick="document.getElementById('inputArchivo').click()">
        <span class="drop-icon">&#x1F4C2;</span>
        <div class="drop-label">Arrastra tu archivo o haz clic para seleccionar</div>
        <div class="drop-hint">Excel (.xlsx) &middot; Word (.docx) &middot; PDF (.pdf) &middot; Max. 100 placas</div>
      </div>
      <input type="file" id="inputArchivo" accept=".xlsx,.xls,.docx,.doc,.pdf,.txt,.csv"/>
      <div id="msgCargando" class="cargando-msg"></div>

      <div class="placas-detectadas" id="placasDetectadas">
        <div class="placas-titulo">Placas detectadas &mdash; <span id="totalDetectadas">0</span></div>
        <div class="placas-grid" id="gridPlacas"></div>
        <p class="limite-msg">Se procesaran en orden, una a la vez.</p>
        <button class="btn-iniciar" id="btnIniciar" onclick="iniciarMasivo()">
          &#x1F680; Iniciar Verificacion Masiva
        </button>
      </div>
    </div>

  </div>
</section>

<section class="fuentes">
  <h2>&#x1F4CB; 20 Fuentes Oficiales Consultadas</h2>
  <p class="fuentes-sub">Revisamos todos los registros que importan antes de la compra.</p>
  <div class="fuentes-grid">
    <div class="fuente-card"><div class="fuente-icon">&#x1F3E6;</div><div class="fuente-nombre">SUNARP Vehicular</div><div class="fuente-desc">Titularidad, gravamenes, bloqueos registrales y estado legal del vehiculo.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F6E1;&#xFE0F;</div><div class="fuente-nombre">SOAT APESEG</div><div class="fuente-desc">Vigencia del Seguro Obligatorio de Accidentes de Transito.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F527;</div><div class="fuente-nombre">MTC Inspeccion Tecnica</div><div class="fuente-desc">Historial de revisiones tecnicas vehiculares.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F4DC;</div><div class="fuente-nombre">SUNARP SPRL</div><div class="fuente-desc">Historial completo de propietarios anteriores.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F9FE;</div><div class="fuente-nombre">SUNARP Siguelo+</div><div class="fuente-desc">Estado de cargas y gravamenes actuales sobre el titulo.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F6A6;</div><div class="fuente-nombre">SUTRAN</div><div class="fuente-desc">Infracciones de transporte y sanciones a nivel nacional.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F68C;</div><div class="fuente-nombre">ATU Lima</div><div class="fuente-desc">Multas de transporte urbano en la capital.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F3E5;</div><div class="fuente-nombre">SBS Accidentes SOAT</div><div class="fuente-desc">Siniestros registrados en el sistema de seguros.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F6DF;</div><div class="fuente-nombre">Callao &amp; GNV/FISE</div><div class="fuente-desc">Papeletas del Callao y deuda de conversion GNV.</div></div>
    <div class="fuente-card"><div class="fuente-icon">&#x1F4CD;</div><div class="fuente-nombre">10 Municipalidades Regionales</div><div class="fuente-desc">Trujillo, Piura, Chiclayo, Arequipa, Tacna, Ica, Cajamarca, Huancayo, Chachapoyas y Tarapoto.</div></div>
  </div>
</section>

<section class="como">
  <h2>Como funciona</h2>
  <div class="pasos">
    <div class="paso"><div class="paso-num">1</div><div class="paso-titulo">Ingresa la placa</div><div class="paso-desc">Escribe la placa del vehiculo que deseas verificar.</div></div>
    <div class="paso"><div class="paso-num">2</div><div class="paso-titulo">Consulta automatica</div><div class="paso-desc">Consultamos 20 fuentes oficiales en tiempo real.</div></div>
    <div class="paso"><div class="paso-num">3</div><div class="paso-titulo">Inspeccion visual</div><div class="paso-desc">Completa el checklist de 45 puntos de inspeccion.</div></div>
    <div class="paso"><div class="paso-num">4</div><div class="paso-titulo">Veredicto final</div><div class="paso-desc">Obtenes un reporte completo y recomendaciones de compra.</div></div>
  </div>
</section>

<footer>
  <p>Verificador Vehicular Peru &mdash; Herramienta de apoyo para la compra informada de vehiculos usados.</p>
  <p style="margin-top:6px">Los datos provienen de fuentes oficiales pero pueden no estar actualizados al momento de la consulta.</p>
</footer>

<script>
// Tabs
function cambiarTab(id, btn) {
  document.querySelectorAll(".tab").forEach(function(t){ t.classList.remove("activo"); });
  document.querySelectorAll(".panel").forEach(function(p){ p.classList.remove("activo"); });
  btn.classList.add("activo");
  document.getElementById("panel-" + id).classList.add("activo");
}

// Drag & drop
var dz = document.getElementById("dropZone");
dz.addEventListener("dragover", function(e){ e.preventDefault(); dz.classList.add("drag-over"); });
dz.addEventListener("dragleave", function(){ dz.classList.remove("drag-over"); });
dz.addEventListener("drop", function(e){
  e.preventDefault();
  dz.classList.remove("drag-over");
  var f = e.dataTransfer.files[0];
  if (f) procesarArchivo(f);
});
document.getElementById("inputArchivo").addEventListener("change", function(e){
  if (e.target.files[0]) procesarArchivo(e.target.files[0]);
});

var placasActuales = [];

function procesarArchivo(archivo) {
  var msg = document.getElementById("msgCargando");
  msg.textContent = "Analizando archivo...";
  document.getElementById("placasDetectadas").style.display = "none";
  placasActuales = [];

  var fd = new FormData();
  fd.append("archivo", archivo);

  fetch("/masivo/cargar", { method: "POST", body: fd })
    .then(function(res){ return res.json(); })
    .then(function(data){
      if (data.error) {
        msg.innerHTML = '<span style="color:#c53030">&#x26A0; ' + data.error + '</span>';
        return;
      }
      placasActuales = data.placas;
      msg.textContent = "";
      renderPlacas(placasActuales);
    })
    .catch(function(){
      msg.innerHTML = '<span style="color:#c53030">&#x26A0; Error al procesar el archivo.</span>';
    });
}

function renderPlacas(placas) {
  var grid = document.getElementById("gridPlacas");
  grid.innerHTML = "";
  document.getElementById("totalDetectadas").textContent = placas.length;
  placas.forEach(function(p){
    var tag = document.createElement("div");
    tag.className = "placa-tag";
    tag.id = "tag-" + p;
    tag.innerHTML = p + '<span class="remove" onclick="quitarPlaca(\'' + p + '\')">&times;</span>';
    grid.appendChild(tag);
  });
  document.getElementById("placasDetectadas").style.display = "block";
  document.getElementById("btnIniciar").disabled = placas.length === 0;
}

function quitarPlaca(p) {
  placasActuales = placasActuales.filter(function(x){ return x !== p; });
  var tag = document.getElementById("tag-" + p);
  if (tag) tag.remove();
  document.getElementById("totalDetectadas").textContent = placasActuales.length;
  document.getElementById("btnIniciar").disabled = placasActuales.length === 0;
}

function iniciarMasivo() {
  if (!placasActuales.length) return;
  var btn = document.getElementById("btnIniciar");
  btn.disabled = true;
  btn.textContent = "Iniciando...";

  fetch("/masivo/iniciar", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({placas: placasActuales})
  })
  .then(function(res){ return res.json(); })
  .then(function(data){
    if (data.error) {
      document.getElementById("msgCargando").innerHTML =
        '<span style="color:#c53030">&#x26A0; ' + data.error + '</span>';
      btn.disabled = false;
      btn.textContent = "Iniciar Verificacion Masiva";
      return;
    }
    window.location.href = "/masivo/" + data.bid;
  })
  .catch(function(){
    document.getElementById("msgCargando").innerHTML =
      '<span style="color:#c53030">&#x26A0; Error al iniciar. Intenta de nuevo.</span>';
    btn.disabled = false;
    btn.textContent = "Iniciar Verificacion Masiva";
  });
}
</script>
</body>
</html>
