"""
base.py — Clase base para todos los scrapers.
Define la interfaz común y manejo de errores.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ResultadoConsulta:
    """Contenedor estandarizado para el resultado de cada consulta."""
    fuente: str                          # Nombre legible del sitio
    url: str                             # URL consultada
    estado: str = "pendiente"            # ok | advertencia | error | sin_datos
    datos: Dict[str, Any] = field(default_factory=dict)
    mensaje: Optional[str] = None        # Mensaje de error o nota adicional

    def marcar_ok(self, datos: Dict[str, Any]):
        self.estado = "ok"
        self.datos = datos

    def marcar_advertencia(self, datos: Dict[str, Any], mensaje: str):
        self.estado = "advertencia"
        self.datos = datos
        self.mensaje = mensaje

    def marcar_error(self, mensaje: str):
        self.estado = "error"
        self.mensaje = mensaje

    def marcar_sin_datos(self, mensaje: str = "Sin información disponible"):
        self.estado = "sin_datos"
        self.mensaje = mensaje
