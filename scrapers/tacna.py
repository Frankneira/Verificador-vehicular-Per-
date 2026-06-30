"""
tacna.py — Papeletas Municipalidad de Tacna.
URL: https://www.munitacna.gob.pe/pagina/sf/servicios/papeletas
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["tacna"], ciudad="Tacna", placa=placa,
        selector_tipo="select[id*='tipo' i], select[name*='tipo' i]",
        valor_tipo="PLACA",
        espera_extra=2.5,
    )
