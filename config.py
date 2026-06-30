"""
config.py -- Carga centralizada de configuracion y credenciales desde .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Credenciales SUNARP SPRL
SUNARP_SPRL_USUARIO = os.getenv("SUNARP_SPRL_USUARIO", "")
SUNARP_SPRL_CLAVE   = os.getenv("SUNARP_SPRL_CLAVE", "")

# Credenciales SAT Trujillo
TRUJILLO_DNI      = os.getenv("TRUJILLO_DNI", "")
TRUJILLO_CELULAR  = os.getenv("TRUJILLO_CELULAR", "")
TRUJILLO_CORREO   = os.getenv("TRUJILLO_CORREO", "")

# Configuracion del navegador
TIMEOUT  = int(os.getenv("TIMEOUT", "30")) * 1000
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# URLs de consulta
URLS = {
    # --- Fase 1: Documentacion ---
    "sunarp_vehicular" : "https://consultavehicular.sunarp.gob.pe/consulta-vehicular/inicio",
    "soat_apeseg"      : "https://www.apeseg.org.pe/consultas-soat/",
    "mtc_inspeccion"   : "https://rec.mtc.gob.pe/Citv/ArConsultaCitv",
    # --- Fase 1: Infracciones y deudas ---
    "sutran"           : "https://www.sutran.gob.pe/consultas/record-de-infracciones/record-de-infracciones/",
    "atu"              : "https://pasarela.atu.gob.pe/",
    "sbs_accidentes"   : "https://servicios.sbs.gob.pe/reportesoat/ReporteCentralRiesgo",
    # --- Fase 2: SUNARP avanzado ---
    "sunarp_sprl"      : "https://sprl.sunarp.gob.pe/sprl/main/partidas-base-grafica-registral",
    "sunarp_siguelo"   : "https://sigueloplus.sunarp.gob.pe/siguelo/",
    # --- Fase 2: Papeletas Lima/Callao ---
    "callao"           : "https://pagopapeletascallao.pe/",
    # --- Fase 2: Servicios adicionales ---
    "gnv_fise"         : "https://fise.minem.gob.pe:23308/consulta-taller/pages/consultaTaller/inicio",
    # --- Fase 2: Papeletas Norte ---
    "trujillo"         : "https://satt.gob.pe/servicios/record-de-infracciones",
    "piura"            : "http://www.munipiura.gob.pe/consulta-de-multas-de-transito",
    "chiclayo"         : "https://virtualsatch.satch.gob.pe/virtualsatch/record_infracciones/buscar_placa_",
    "tarapoto"         : "https://www.sat-t.gob.pe/",
    "chachapoyas"      : "https://app.munichachapoyas.gob.pe/servicios/consulta_papeletas/app/papeletas.php",
    "cajamarca"        : "https://www.satcajamarca.gob.pe/#/",
    # --- Fase 2: Papeletas Centro ---
    "huancayo"         : "http://sathuancayo.fortiddns.com:888/VentanillaVirtual/ConsultaPIT.aspx",
    "ica"              : "https://m.satica.gob.pe/consultapapeletas.php",
    # --- Fase 2: Papeletas Sur ---
    "tacna"            : "https://www.munitacna.gob.pe/pagina/sf/servicios/papeletas",
    "arequipa"         : "https://www.muniarequipa.gob.pe/oficina-virtual/c0nInfrPermisos/faltas/papeletas.php",
}
