"""
generator.py -- Genera el reporte HTML a partir de los resultados.
"""
import os
from datetime import datetime
from pathlib import Path
from typing import List
from jinja2 import Environment, FileSystemLoader
from scrapers.base import ResultadoConsulta

TEMPLATES_DIR = Path(__file__).parent / "templates"


def generar_reporte(
    placa,
    resultados_doc,
    resultados_deudas,
    resultados_regiones=None,
    ruta_salida=None
):
    resultados_regiones = resultados_regiones or []

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("reporte.html")

    todos = resultados_doc + resultados_deudas + resultados_regiones
    conteo = {
        "ok"         : sum(1 for r in todos if r.estado == "ok"),
        "advertencia": sum(1 for r in todos if r.estado == "advertencia"),
        "error"      : sum(1 for r in todos if r.estado == "error"),
        "sin_datos"  : sum(1 for r in todos if r.estado == "sin_datos"),
        "total"      : len(todos),
    }

    html = template.render(
        placa=placa.upper(),
        fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),
        resultados_doc=resultados_doc,
        resultados_deudas=resultados_deudas,
        resultados_regiones=resultados_regiones,
        conteo=conteo,
    )

    if not ruta_salida:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta_salida = os.path.join(
            os.path.dirname(__file__), "..", "reportes",
            "reporte_{}_{}.html".format(placa.upper(), ts)
        )

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html)

    return os.path.abspath(ruta_salida)
