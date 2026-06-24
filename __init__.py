"""
checklist.py -- Checklist de inspeccion visual y tecnica antes de comprar un auto usado.
Basado en fuentes: masmotor.mx, tuauto.com.pe, blog.one.com.pe, autofact.com.pe

Estructura de cada item:
  id       : identificador unico
  categoria: grupo al que pertenece
  item     : descripcion del punto a revisar
  detalle  : que buscar / que significa
  critico  : True si un fallo aqui es motivo de rechazo inmediato
"""

CATEGORIAS = [
    "exterior",
    "interior",
    "motor",
    "chasis",
    "prueba_manejo",
]

CHECKLIST = [
    # ── EXTERIOR ──────────────────────────────────────────────────────────────
    {
        "id": "E01", "categoria": "exterior", "critico": True,
        "item": "Uniformidad de la pintura",
        "detalle": "Bajo luz natural, verificar que el color sea exactamente igual en todas las partes. Diferencias indican repintura por golpe o accidente.",
    },
    {
        "id": "E02", "categoria": "exterior", "critico": True,
        "item": "Alineacion de puertas, capo y maletero",
        "detalle": "Las separaciones entre paneles deben ser uniformes. Espacios irregulares o asimetricos revelan accidentes o reparaciones deficientes.",
    },
    {
        "id": "E03", "categoria": "exterior", "critico": False,
        "item": "Estado de los paneles (abolladuras, ondulaciones)",
        "detalle": "Pasar la mano sobre cada panel. Las ondulaciones ocultas indican masilla o relleno sobre golpes.",
    },
    {
        "id": "E04", "categoria": "exterior", "critico": True,
        "item": "Signos de herrumbre o corrosion",
        "detalle": "Revisar debajo de los marcos de las puertas, paso de ruedas y partes bajas. La corrosion estructural es irreparable de forma economica.",
    },
    {
        "id": "E05", "categoria": "exterior", "critico": False,
        "item": "Estado de vidrios y parabrisas",
        "detalle": "Buscar fisuras, rayones profundos o estrellas. Un parabrisas danado es peligroso y costoso de reemplazar.",
    },
    {
        "id": "E06", "categoria": "exterior", "critico": False,
        "item": "Estado de las gomas y burlete de puertas",
        "detalle": "Las gomas resecas o rotas permiten entrada de agua y ruido. Indicador de falta de mantenimiento.",
    },
    {
        "id": "E07", "categoria": "exterior", "critico": False,
        "item": "Funcionamiento de luces (delanteras, traseras, neblineros)",
        "detalle": "Probar todas las luces: cruce, largas, direccionales, freno, reversa y neblineros. Verificar que los faros no tengan agua interior.",
    },
    {
        "id": "E08", "categoria": "exterior", "critico": True,
        "item": "Estado de neumaticos (4 + repuesto)",
        "detalle": "La banda de rodaje debe ser mayor a 3mm (insertar una moneda de S/1: si se ve el 'sol' completo, estan desgastados). Desgaste irregular indica problemas de alineacion o suspension.",
    },
    {
        "id": "E09", "categoria": "exterior", "critico": False,
        "item": "Estado de los rines",
        "detalle": "Golpes o rayaduras profundas en los rines pueden indicar que el vehiculo ha sufrido impactos o ha circulado con llantas bajas.",
    },
    {
        "id": "E10", "categoria": "exterior", "critico": False,
        "item": "Funcionamiento de cerraduras y manijas",
        "detalle": "Probar todas las puertas desde adentro y afuera. Verificar el cierre centralizado si aplica.",
    },

    # ── INTERIOR ──────────────────────────────────────────────────────────────
    {
        "id": "I01", "categoria": "interior", "critico": False,
        "item": "Estado de tapiceria (asientos, techo, alfombra)",
        "detalle": "Manchas de humedad o moho en el techo o alfombra indican filtraciones de agua. El costo de reparacion puede ser elevado.",
    },
    {
        "id": "I02", "categoria": "interior", "critico": True,
        "item": "Panel de instrumentos sin luces de advertencia",
        "detalle": "Encender el motor y verificar que ningun testigo permanezca encendido (check engine, ABS, airbag, temperatura, presion de aceite).",
    },
    {
        "id": "I03", "categoria": "interior", "critico": True,
        "item": "Sistema de airbags (sin testigos de falla)",
        "detalle": "El testigo del airbag debe encenderse al arrancar y apagarse. Si queda encendido, el sistema esta desactivado o fue activado en un accidente.",
    },
    {
        "id": "I04", "categoria": "interior", "critico": True,
        "item": "Cinturones de seguridad (los 5)",
        "detalle": "Probar que todos los cinturones se enrollen correctamente y que los seguros encajen con click firme. Cinturones que no se retraen deben cambiarse.",
    },
    {
        "id": "I05", "categoria": "interior", "critico": False,
        "item": "Aire acondicionado y calefaccion",
        "detalle": "Encender el A/C y verificar que enfrie en menos de 2 minutos. Un gas insuficiente o compresor danado es costoso de reparar.",
    },
    {
        "id": "I06", "categoria": "interior", "critico": False,
        "item": "Sistema electrico (vidrios electricos, espejos, sunroof)",
        "detalle": "Operar cada control electrico. Los motores de vidrios electricos son caros de reemplazar.",
    },
    {
        "id": "I07", "categoria": "interior", "critico": False,
        "item": "Sistema de audio y pantalla",
        "detalle": "Probar radio, Bluetooth, USB. Si el equipo fue reemplazado puede indicar robo del original.",
    },
    {
        "id": "I08", "categoria": "interior", "critico": False,
        "item": "Kilometraje en el odometro",
        "detalle": "Un auto promedio recorre 15,000-20,000 km/anio. Desconfiar si el kilometraje es inusualmente bajo para el anio o si hay signos de adulteracion.",
    },
    {
        "id": "I09", "categoria": "interior", "critico": False,
        "item": "Estado del volante y palanca de cambios",
        "detalle": "El desgaste del volante y palanca puede revelar el uso real, que puede no coincidir con el odometro.",
    },
    {
        "id": "I10", "categoria": "interior", "critico": False,
        "item": "Pedales (freno, acelerador, embrague)",
        "detalle": "Los pedales desgastados en un vehiculo de bajo kilometraje son una contradiccion que sugiere adulteracion del odometro.",
    },

    # ── MOTOR ─────────────────────────────────────────────────────────────────
    {
        "id": "M01", "categoria": "motor", "critico": True,
        "item": "Sin fugas de aceite (bajo el capo y en el suelo)",
        "detalle": "Manchas de aceite debajo del motor indican fugas. Colocar carton blanco durante 15 minutos para detectarlas.",
    },
    {
        "id": "M02", "categoria": "motor", "critico": True,
        "item": "Color y nivel del aceite de motor",
        "detalle": "El aceite debe ser ambar oscuro a negro. Si es grisaceo o cremoso (emulsionado) puede indicar falla de empaque de culata (agua mezclada con aceite). Extremadamente critico.",
    },
    {
        "id": "M03", "categoria": "motor", "critico": True,
        "item": "Color y nivel del liquido refrigerante",
        "detalle": "Debe ser verde, azul o naranja segun la marca. Si es color chocolate o tiene residuos aceitosos, hay mezcla con aceite. Critico.",
    },
    {
        "id": "M04", "categoria": "motor", "critico": False,
        "item": "Nivel del liquido de frenos",
        "detalle": "Debe estar entre MIN y MAX. Si esta bajo puede indicar pastillas desgastadas o fuga en el circuito hidraulico.",
    },
    {
        "id": "M05", "categoria": "motor", "critico": False,
        "item": "Estado de correas (distribucion, alternador)",
        "detalle": "Las correas no deben tener grietas ni desgastes. La correa de distribucion es critica: su rotura puede destruir el motor.",
    },
    {
        "id": "M06", "categoria": "motor", "critico": False,
        "item": "Estado de mangueras y conexiones",
        "detalle": "Ninguna manguera debe estar reseca, agrietada o con remiendos. Verificar que las abrazaderas esten firmes.",
    },
    {
        "id": "M07", "categoria": "motor", "critico": False,
        "item": "Bateria (estado y fecha de fabricacion)",
        "detalle": "Una bateria tiene vida util de 2-3 anios. Verificar que los terminales no tengan corrosion (polvo blanco/verde).",
    },
    {
        "id": "M08", "categoria": "motor", "critico": False,
        "item": "Ruidos anormales al encender (golpeteos, silbidos)",
        "detalle": "Un motor sano arranca suave. Golpeteos metalicos indican falla de bielas o ciguenal. Silbidos en correas o problema de admision.",
    },
    {
        "id": "M09", "categoria": "motor", "critico": False,
        "item": "Color del humo del escape",
        "detalle": "Humo blanco persistente: agua en motor. Humo azul: aceite quemado. Humo negro: mezcla rica de combustible. Todos son problemas serios.",
    },
    {
        "id": "M10", "categoria": "motor", "critico": False,
        "item": "Temperatura del motor en ralenti",
        "detalle": "Dejar el motor en ralenti 5 minutos. La temperatura debe estabilizarse al centro. Si sube demasiado hay problema de refrigeracion.",
    },

    # ── CHASIS Y PARTE INFERIOR ───────────────────────────────────────────────
    {
        "id": "C01", "categoria": "chasis", "critico": True,
        "item": "Soldaduras o danos estructurales en el chasis",
        "detalle": "Inspeccionar debajo del vehiculo con linterna. Soldaduras recientes o zonas repintadas indican accidente estructural grave.",
    },
    {
        "id": "C02", "categoria": "chasis", "critico": True,
        "item": "Estado de amortiguadores",
        "detalle": "Presionar fuerte cada esquina del vehiculo: debe rebotar 1 vez y detenerse. Si rebota mas, los amortiguadores estan gastados.",
    },
    {
        "id": "C03", "categoria": "chasis", "critico": False,
        "item": "Estado de bujes y rotulas de suspension",
        "detalle": "Con el vehiculo en rampa, mover las ruedas: no deben tener juego ni hacer ruidos. Cambio costoso si hay falla.",
    },
    {
        "id": "C04", "categoria": "chasis", "critico": False,
        "item": "Sistema de frenos (discos y pastillas)",
        "detalle": "Las estraciones en los discos deben ser superficiales. Verificar que no haya fugas en mangueras o cilindros de freno.",
    },
    {
        "id": "C05", "categoria": "chasis", "critico": False,
        "item": "Estado del sistema de escape",
        "detalle": "Sin perforaciones, sin oxido avanzado, bien sujeto. Un escape roto es peligroso por filtracion de gases al habitaculo.",
    },
    {
        "id": "C06", "categoria": "chasis", "critico": False,
        "item": "Fugas en sistema de transmision",
        "detalle": "Buscar manchas de aceite en la caja de cambios, diferencial y transmision. Las fugas indican sellos danados.",
    },
    {
        "id": "C07", "categoria": "chasis", "critico": False,
        "item": "Estado de los semiaxes y juntas homoceticas",
        "detalle": "Verificar que los fuelles de las juntas homoceticas no esten rotos. Un fuelle roto provoca contaminacion y fallo de la junta.",
    },

    # ── PRUEBA DE MANEJO ──────────────────────────────────────────────────────
    {
        "id": "P01", "categoria": "prueba_manejo", "critico": False,
        "item": "Arranque en frio (sin precalentar)",
        "detalle": "El motor debe arrancar a la primera. Un arranque dificultoso indica bateria debil, bujias gastadas o problema en el sistema de combustible.",
    },
    {
        "id": "P02", "categoria": "prueba_manejo", "critico": True,
        "item": "El vehiculo no jala hacia un lado",
        "detalle": "En una recta con manos sueltas del volante, el vehiculo no debe desviarse. Si jala, hay problema de alineacion o frenos.",
    },
    {
        "id": "P03", "categoria": "prueba_manejo", "critico": True,
        "item": "Frenos responden firmes y sin ruidos",
        "detalle": "El pedal debe estar firme (no esponjoso). Frenada recta sin vibrar. Ruidos al frenar indican discos o pastillas en mal estado.",
    },
    {
        "id": "P04", "categoria": "prueba_manejo", "critico": False,
        "item": "Cambios de marcha suaves (caja manual o automatica)",
        "detalle": "Los cambios no deben ser bruscos ni rechinar. La caja automatica no debe demorar o dar tirones al cambiar.",
    },
    {
        "id": "P05", "categoria": "prueba_manejo", "critico": False,
        "item": "Aceleracion progresiva sin tirones",
        "detalle": "El motor debe responder uniformemente. Tirones o 'sacudidas' indican bujias, inyectores o sensores defectuosos.",
    },
    {
        "id": "P06", "categoria": "prueba_manejo", "critico": False,
        "item": "Sin ruidos de suspension en baches o curvas",
        "detalle": "Golpes metalicos sobre baches = rotulas o bujes gastados. Ruidos al girar = juntas homoceticas o cojinetes de rueda danados.",
    },
    {
        "id": "P07", "categoria": "prueba_manejo", "critico": False,
        "item": "Temperatura del motor se estabiliza durante el recorrido",
        "detalle": "Durante la prueba (minimo 15 min), vigilar el indicador de temperatura. No debe pasar del centro.",
    },
    {
        "id": "P08", "categoria": "prueba_manejo", "critico": False,
        "item": "Sin vibraciones en el volante a alta velocidad",
        "detalle": "Vibraciones a mas de 80 km/h indican llantas desbalanceadas o problema de geometria de direccion.",
    },
]


def obtener_por_categoria(categoria):
    """Retorna los items de una categoria especifica."""
    return [i for i in CHECKLIST if i["categoria"] == categoria]


def obtener_criticos():
    """Retorna solo los items criticos."""
    return [i for i in CHECKLIST if i["critico"]]


NOMBRES_CATEGORIA = {
    "exterior"      : "Exterior y Carroceria",
    "interior"      : "Interior y Electronica",
    "motor"         : "Motor y Compartimiento",
    "chasis"        : "Chasis y Parte Inferior",
    "prueba_manejo" : "Prueba de Manejo",
}

ICONOS_CATEGORIA = {
    "exterior"      : "🚗",
    "interior"      : "🪑",
    "motor"         : "🔧",
    "chasis"        : "⚙️",
    "prueba_manejo" : "🏁",
}
