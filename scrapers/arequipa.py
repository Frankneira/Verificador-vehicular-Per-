"""
arequipa.py — Papeletas Municipalidad de Arequipa.
URL: https://www.muniarequipa.gob.pe/oficina-virtual/c0nInfrPermisos/faltas/papeletas.php
"""
from playwright.async_api import Page
from config import URLS
from scrapers.papeleta_base import consultar_papeleta

async def consultar(page: Page, placa: str):
    return await consultar_papeleta(
        page=page, url=URLS["arequipa"], ciudad="Arequipa", placa=placa,
        selector_placa=(
            "input[id*='plac' i], input[name*='plac' i], "
            "input[placeholder*='plac' i], input[type='text']"
        ),
        espera_extra=2.5,
    )
