"""
recomendaciones.py -- Motor de recomendaciones finales.
Analiza los resultados de scraping + checklist y genera un veredicto.
"""


NIVELES = {
    "COMPRAR":       {"color": "#276749", "bg": "#f0fff4", "border": "#68d391", "icono": "✅"},
    "NEGOCIAR":      {"color": "#744210", "bg": "#fffbeb", "border": "#f6ad55", "icono": "⚠️"},
    "REVISAR_TALLER":{"color": "#744210", "bg": "#fffbeb", "border": "#f6ad55", "icono": "🔧"},
    "NO_COMPRAR":    {"color": "#742a2a", "bg": "#fff5f5", "border": "#fc8181", "icono": "🚨"},
}


def generar(resultados_scraping, respuestas_checklist=None):
    """
    Genera el reporte de recomendaciones.

    Args:
        resultados_scraping : Lista de ResultadoConsulta de todos los bloques.
        respuestas_checklist: Dict {id_item: "ok" | "falla" | "no_revisado"}
                              Si es None, se omite el analisis del checklist.
    Returns:
        Dict con veredicto, puntuacion, razones y recomendaciones_lista.
    """
    respuestas = respuestas_checklist or {}

    puntos_negativos  = 0
    puntos_positivos  = 0
    razones_rechazo   = []
    razones_atencion  = []
    puntos_favor      = []
    recomendaciones   = []

    # ── Analisis de resultados de scraping ────────────────────────────────────
    for r in resultados_scraping:
        fuente = r.fuente
        datos  = r.datos or {}
        msg    = r.mensaje or ""

        if r.estado == "advertencia":
            puntos_negativos += 2

            # SOAT vencido
            if "soat" in fuente.lower() and "vencido" in msg.lower():
                razones_rechazo.append("El SOAT esta VENCIDO. El vehiculo no puede circular legalmente.")
                recomendaciones.append("Exige al vendedor renovar el SOAT antes de cerrar el trato o descuenta el costo del precio.")

            # Infracciones SUTRAN
            elif "sutran" in fuente.lower():
                total = datos.get("total", "?")
                razones_atencion.append("El vehiculo tiene {} infraccion(es) en SUTRAN.".format(total))
                recomendaciones.append("Verifica con el vendedor quien pagara las papeletas SUTRAN pendientes. Descuenta el monto del precio.")

            # Multas ATU
            elif "atu" in fuente.lower():
                total = datos.get("total", "?")
                razones_atencion.append("{} multa(s) pendiente(s) en ATU.".format(total))
                recomendaciones.append("Solicita al vendedor cancelar las multas ATU antes de la transferencia.")

            # Papeletas regionales
            elif "papeletas" in fuente.lower():
                ciudad = datos.get("Ciudad", fuente.replace("Papeletas --", "").strip())
                total = datos.get("total", "?")
                razones_atencion.append("Papeleta(s) pendiente(s) en {}: {} multa(s).".format(ciudad, total))
                recomendaciones.append("Negocia el descuento del valor de las papeletas de {} en el precio final.".format(ciudad))

            # Accidentes SBS
            elif "sbs" in fuente.lower() or "accidente" in fuente.lower():
                num = datos.get("Accidentes en ultimos 5 anos", datos.get("Accidentes en últimos 5 años", "?"))
                razones_atencion.append("El vehiculo registra {} siniestro(s) SOAT en los ultimos 5 anos.".format(num))
                recomendaciones.append("Solicita el historial tecnico del vehiculo y exige inspeccion en taller de confianza.")

            # SUNARP SPRL -- alerta legal
            elif "sprl" in fuente.lower():
                if "embargo" in msg.lower():
                    razones_rechazo.append("ALERTA: El vehiculo tiene EMBARGO registrado en SUNARP. NO transferible hasta levantar la medida.")
                    puntos_negativos += 5
                elif "prescripcion" in msg.lower():
                    razones_rechazo.append("ALERTA: Se detecta PRESCRIPCION DE DOMINIO en SUNARP. Consulta a un abogado.")
                    puntos_negativos += 5
                else:
                    razones_atencion.append("Hay anotaciones en SUNARP SPRL. Revisa con un abogado antes de firmar.")

            # GNV FISE
            elif "gnv" in fuente.lower() or "fise" in fuente.lower():
                razones_atencion.append("El vehiculo tiene deuda de GNV en FISE.")
                recomendaciones.append("Solicita al vendedor cancelar la deuda GNV antes de la transferencia.")

            # Callao
            elif "callao" in fuente.lower():
                razones_atencion.append("Papeleta(s) pendiente(s) en el Callao.")
                recomendaciones.append("Descuenta el valor de las papeletas del Callao del precio.")

            else:
                razones_atencion.append("Advertencia en {}: {}".format(fuente, msg[:100]))

        elif r.estado == "ok":
            puntos_positivos += 1
            if "soat" in fuente.lower():
                estado_soat = datos.get("Estado", datos.get("estado", "")).lower()
                if "vigente" in estado_soat:
                    puntos_favor.append("SOAT vigente.")
            elif "inspeccion" in fuente.lower() or "itv" in fuente.lower() or "mtc" in fuente.lower():
                puntos_favor.append("Inspeccion Tecnica Vehicular al dia.")
            elif "sutran" in fuente.lower():
                puntos_favor.append("Sin infracciones en SUTRAN.")
            elif "atu" in fuente.lower():
                puntos_favor.append("Sin multas en ATU.")
            elif "sbs" in fuente.lower():
                puntos_favor.append("Sin accidentes SOAT registrados.")

        elif r.estado == "error":
            # Errores de scraping no son fallas del vehiculo -- solo informamos
            pass

    # ── Analisis del checklist ────────────────────────────────────────────────
    if respuestas:
        from inspeccion.checklist import CHECKLIST
        criticos_fallidos = []
        items_fallidos    = []

        for item in CHECKLIST:
            estado_item = respuestas.get(item["id"], "no_revisado")
            if estado_item == "falla":
                if item["critico"]:
                    criticos_fallidos.append(item["item"])
                    puntos_negativos += 3
                else:
                    items_fallidos.append(item["item"])
                    puntos_negativos += 1
            elif estado_item == "ok":
                puntos_positivos += 1

        if criticos_fallidos:
            razones_rechazo.extend(["FALLA CRITICA: " + i for i in criticos_fallidos])
            recomendaciones.append(
                "Los items criticos fallidos son problemas graves. Rechaza el vehiculo o exige reparacion documentada antes de comprar."
            )

        if items_fallidos:
            razones_atencion.extend(items_fallidos)
            if items_fallidos:
                recomendaciones.append(
                    "Cotiza la reparacion de los items con falla y descuenta ese monto del precio negociado."
                )

    # ── Recomendaciones generales siempre presentes ───────────────────────────
    recomendaciones.append("Verifica que la placa y VIN del vehiculo coincidan con la Tarjeta de Propiedad (TIVE).")
    recomendaciones.append("Firma el contrato de compraventa ante notario y realiza la transferencia en SUNARP el mismo dia.")
    recomendaciones.append("Solicita facturas de mantenimiento o historial de servicio del vehiculo.")
    recomendaciones.append("Contrata una revision tecnica en taller independiente antes de cerrar el trato (costo: S/ 100 - S/ 200).")

    # ── Veredicto final ───────────────────────────────────────────────────────
    if razones_rechazo:
        veredicto = "NO_COMPRAR"
    elif puntos_negativos >= 6:
        veredicto = "NO_COMPRAR"
    elif puntos_negativos >= 3:
        veredicto = "REVISAR_TALLER"
    elif puntos_negativos >= 1:
        veredicto = "NEGOCIAR"
    else:
        veredicto = "COMPRAR"

    nivel = NIVELES[veredicto]

    return {
        "veredicto"         : veredicto,
        "etiqueta"          : {
            "COMPRAR"       : "APTO PARA COMPRAR",
            "NEGOCIAR"      : "NEGOCIAR PRECIO",
            "REVISAR_TALLER": "REVISAR EN TALLER",
            "NO_COMPRAR"    : "NO RECOMENDADO",
        }[veredicto],
        "color"             : nivel["color"],
        "bg"                : nivel["bg"],
        "border"            : nivel["border"],
        "icono"             : nivel["icono"],
        "puntos_negativos"  : puntos_negativos,
        "puntos_positivos"  : puntos_positivos,
        "razones_rechazo"   : razones_rechazo,
        "razones_atencion"  : razones_atencion,
        "puntos_favor"      : puntos_favor,
        "recomendaciones"   : list(dict.fromkeys(recomendaciones)),  # deduplicar
    }
