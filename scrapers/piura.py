"""
piura.py — Papeletas Municipalidad de Piura.
URL: http://www.munipiura.gob.pe/consulta-de-multas-de-transito#buscar-por-placa
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["piura"], ciudad="Piura", placa=placa,
        selector_buscar="button:has-text('Buscar'), input[type='submit'], button[type='submit']",
        espera_extra=2.0,
    )
