"""Generador de Presentación de Diapositivas NexusNav en PowerPoint (.pptx).

Diseño corporativo y editorial de alto impacto inspirado en el estilo de referencia:
- Header limpio con categoría (kicker), título y separador lineal sutil.
- Esquema de color profesional: Navy / Slate, Blanco / Light Gray, con acentos Teal, Amber, Coral y Blue.
- Estructuras visuales: tarjetas de pilares con badges circulares, split-screen, matrices de cuadrantes y líneas de tiempo.
- Integración de diagramas UML de alta resolución y gráficas de benchmarking.
- Tipografía editorial ampliada y legible para proyecciones y lectura clara.
- Sin menciones a 'guía', 'rúbrica', 'CETO', 'materia' ni nombres repetitivos en cada diapositiva.
"""

from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Directorios de trabajo
ROOT = Path(__file__).resolve().parent
OUTPUT_PPTX = ROOT / "NexusNav_Presentacion_Arquitectura.pptx"
WORKSPACE_PPTX = ROOT.parent / "NexusNav_Presentacion_Arquitectura.pptx"

# Rutas de imágenes
DIAG_DIR = ROOT / "diagramas"
GRAF_DIR = ROOT / "graficas"

IMG_COMPONENTES = DIAG_DIR / "01_componentes.png"
IMG_SECUENCIA = DIAG_DIR / "02_secuencia.png"
IMG_CLASES = DIAG_DIR / "03_clases.png"
IMG_ACTIVIDAD = DIAG_DIR / "04_actividad.png"

IMG_LATENCIA = GRAF_DIR / "fig01_latencia_comparativa.png"
IMG_NODOS = GRAF_DIR / "fig02_nodos_explorados.png"
IMG_THROUGHPUT = GRAF_DIR / "fig03_throughput_escalabilidad.png"
IMG_DESVIO = GRAF_DIR / "fig04_desvio_dinamico_tiempos.png"

# Paleta cromática profesional
C_WHITE = RGBColor(255, 255, 255)
C_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50
C_CARD_BG = RGBColor(255, 255, 255)
C_CARD_ALT = RGBColor(241, 245, 249)      # Slate 100
C_BORDER_LIGHT = RGBColor(226, 232, 240)  # Slate 200
C_LINE = RGBColor(203, 213, 225)          # Slate 300

C_NAVY_DARK = RGBColor(15, 23, 42)        # Slate 900 (Títulos principales)
C_NAVY = RGBColor(30, 41, 59)             # Slate 800 (Texto primario)
C_MUTED = RGBColor(100, 116, 139)         # Slate 500 (Texto secundario)
C_BODY = RGBColor(51, 65, 85)             # Slate 700 (Cuerpo)

# Acentos temáticos
C_TEAL = RGBColor(13, 148, 136)           # Teal 600 (Acento principal)
C_TEAL_LIGHT = RGBColor(204, 251, 241)     # Teal 100
C_AMBER = RGBColor(217, 119, 6)           # Amber 600
C_AMBER_LIGHT = RGBColor(254, 243, 199)    # Amber 100
C_CORAL = RGBColor(225, 29, 72)           # Rose 600
C_CORAL_LIGHT = RGBColor(255, 228, 230)    # Rose 100
C_BLUE = RGBColor(37, 99, 235)            # Blue 600
C_BLUE_LIGHT = RGBColor(219, 234, 254)     # Blue 100
C_INDIGO = RGBColor(79, 70, 229)          # Indigo 600
C_SKY = RGBColor(14, 165, 233)            # Sky 500
C_SLATE_HERO = RGBColor(24, 32, 47)       # Dark container


# ---------------------------------------------------------------------------
# Helpers de Renderizado y Estructura Visual
# ---------------------------------------------------------------------------
def init_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_slide_header(slide, title: str, kicker: str = "ARQUITECTURA DE SOFTWARE · SISTEMA NEXUSNAV", slide_num: int = None):
    """Renderiza la cabecera editorial unificada con título, categoría y línea divisoria."""
    # Kicker (categoría superior)
    kicker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.30), Inches(9.5), Inches(0.28))
    tf_k = kicker_box.text_frame
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker.upper()
    p_k.font.name = "Arial"
    p_k.font.size = Pt(9.5)
    p_k.font.bold = True
    p_k.font.color.rgb = C_TEAL

    # Título principal (tipografía aumentada a 23 pt)
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.54), Inches(10.6), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = "Arial"
    p_t.font.size = Pt(23)
    p_t.font.bold = True
    p_t.font.color.rgb = C_NAVY_DARK

    # Contador de diapositiva (Pill estilizada en la esquina superior derecha)
    if slide_num is not None:
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.6), Inches(0.42), Inches(0.933), Inches(0.38))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_CARD_ALT
        pill.line.color.rgb = C_BORDER_LIGHT
        pill.line.width = Pt(1)
        tf_num = pill.text_frame
        tf_num.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.CENTER
        p_num.text = f"{slide_num:02d} / 16"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = C_MUTED

    # Línea divisoria elegante
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.24), Inches(11.733), Pt(1.2))
    line.fill.solid()
    line.fill.fore_color.rgb = C_LINE
    line.line.fill.background()


def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT, border_width=1.0):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card


def add_circular_badge(slide, left, top, size, text, bg_color=C_TEAL, text_color=C_WHITE, font_size=11):
    badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    badge.fill.solid()
    badge.fill.fore_color.rgb = bg_color
    badge.line.fill.background()
    tf = badge.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.name = "Arial"
    run.font.bold = True
    run.font.size = Pt(font_size)
    run.font.color.rgb = text_color
    return badge


def add_proportional_image(slide, path, left, top, max_width, max_height, border=True):
    path = Path(path)
    if not path.exists():
        return None
    with Image.open(path) as img:
        img_w, img_h = img.size
    aspect = img_w / img_h
    w = max_width
    h = w / aspect
    if h > max_height:
        h = max_height
        w = h * aspect
    off_x = (max_width - w) / 2
    off_y = (max_height - h) / 2

    if border:
        frame = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + off_x - Inches(0.04), top + off_y - Inches(0.04), w + Inches(0.08), h + Inches(0.08))
        frame.fill.solid()
        frame.fill.fore_color.rgb = C_WHITE
        frame.line.color.rgb = C_BORDER_LIGHT
        frame.line.width = Pt(1)

    pic = slide.shapes.add_picture(str(path), left + off_x, top + off_y, width=w, height=h)
    return pic


def set_bullet_point(paragraph, bold_prefix, text, font_size=11, bold_color=C_NAVY_DARK, text_color=C_BODY, space_after=6):
    paragraph.space_after = Pt(space_after)
    paragraph.line_spacing = 1.15
    if bold_prefix:
        r1 = paragraph.add_run()
        r1.text = bold_prefix + " "
        r1.font.name = "Arial"
        r1.font.bold = True
        r1.font.size = Pt(font_size)
        r1.font.color.rgb = bold_color
    r2 = paragraph.add_run()
    r2.text = text
    r2.font.name = "Arial"
    r2.font.bold = False
    r2.font.size = Pt(font_size)
    r2.font.color.rgb = text_color


# ---------------------------------------------------------------------------
# DIAPOSITIVA 1: Portada
# ---------------------------------------------------------------------------
def build_slide_01(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Fondo claro con panel héroe oscuro central
    hero = add_card(slide, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=C_SLATE_HERO, border_color=None)

    # Franja decorativa de acento superior
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.12))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = C_TEAL
    stripe.line.fill.background()

    # Kicker
    k_box = slide.shapes.add_textbox(Inches(1.4), Inches(1.3), Inches(10.5), Inches(0.35))
    p_k = k_box.text_frame.paragraphs[0]
    p_k.text = "ARQUITECTURA DE SOFTWARE · SISTEMAS DISTRIBUIDOS Y NAVEGACIÓN INTELIGENTE"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(10.5)
    p_k.font.bold = True
    p_k.font.color.rgb = C_TEAL

    # Título principal (31 pt)
    t_box = slide.shapes.add_textbox(Inches(1.4), Inches(1.72), Inches(10.5), Inches(1.4))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "NexusNav: Arquitectura de Navegación y Enrutamiento Multimodal Dinámico"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(31)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE

    # Subtítulo explicativo (14.5 pt)
    sub_box = slide.shapes.add_textbox(Inches(1.4), Inches(3.18), Inches(10.5), Inches(0.8))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Estrategias de Optimización, Patrones de Diseño GoF, Poda Topológica Espacial y Telemetría Reactiva para Redes Urbanas de Alta Densidad"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(14.5)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)

    # Badges de atributos y estándares: 2 filas balanceadas dentro de la tarjeta
    badges_row1 = [
        ("PATRONES DE DISEÑO GOF (5)", C_TEAL),
        ("PODA COMPOSITE (-53.79 %)", C_AMBER),
        ("CACHÉ ESPACIAL (4.13x)", C_CORAL),
    ]
    badges_row2 = [
        ("EVALUACIÓN FORMAL ATAM", C_BLUE),
        ("ESTÁNDAR ISO/IEC 25010:2023", C_INDIGO),
        ("TELEMETRÍA REACTIVA O(K)", C_SKY),
    ]

    for b_list, y_pos in [(badges_row1, Inches(4.18)), (badges_row2, Inches(4.70))]:
        cur_x = Inches(1.4)
        for b_text, b_col in b_list:
            b_w = Inches(len(b_text) * 0.088 + 0.5)
            pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cur_x, y_pos, b_w, Inches(0.38))
            pill.fill.solid()
            pill.fill.fore_color.rgb = b_col
            pill.line.fill.background()
            tf_b = pill.text_frame
            tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
            p_b = tf_b.paragraphs[0]
            p_b.alignment = PP_ALIGN.CENTER
            p_b.text = b_text
            p_b.font.name = "Arial"
            p_b.font.size = Pt(9.5)
            p_b.font.bold = True
            p_b.font.color.rgb = C_WHITE
            cur_x += b_w + Inches(0.20)

    # Autores y Equipo
    auth_box = slide.shapes.add_textbox(Inches(1.4), Inches(5.38), Inches(10.5), Inches(0.8))
    tf_a = auth_box.text_frame
    p_a1 = tf_a.paragraphs[0]
    p_a1.text = "Equipo de Proyecto y Arquitectura:"
    p_a1.font.name = "Arial"
    p_a1.font.size = Pt(10)
    p_a1.font.color.rgb = C_MUTED

    p_a2 = tf_a.add_paragraph()
    p_a2.text = "Juan Carlos Benítez Rojas  ·  Juan José Córdoba Eraso"
    p_a2.font.name = "Arial"
    p_a2.font.size = Pt(13.5)
    p_a2.font.bold = True
    p_a2.font.color.rgb = C_WHITE


# ---------------------------------------------------------------------------
# DIAPOSITIVA 2: Desafíos Arquitectónicos (Problema)
# ---------------------------------------------------------------------------
def build_slide_02(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Desafíos Arquitectónicos en Navegación y Movilidad Urbana", "DELIMITACIÓN DEL PROBLEMA", 2)

    cards_data = [
        ("01", C_CORAL, "COMPLEJIDAD COMPUTACIONAL", "Explosión Combinatoria O(V log V + E)", [
            ("Búsqueda Global Exhaustiva:", "Algoritmos tradicionales sin orientación (Dijkstra) evalúan redes enteras de miles de nodos."),
            ("Degradación de Latencia:", "Tiempos de respuesta > 2 000 ms bajo saturación concurrente en cruces metropolitanos."),
            ("Consumo de CPU Extremo:", "Operaciones de cola de prioridad que saturan los núcleos del servidor de cálculo.")
        ]),
        ("02", C_AMBER, "SATURACIÓN TELEMÁTICA", "Sobrecarga Masiva por Sondeo (Polling)", [
            ("Peticiones Innecesarias:", "Miles de clientes móviles consultan periódicamente (cada 2–5 s) sin cambios viales reales."),
            ("Inanición de Conexiones:", "Agotamiento de sockets HTTP y ancho de banda saturado en horas pico de tránsito."),
            ("Falta de Reactividad:", "Los incidentes no se notifican en el instante de ocurrir, provocando ingresos a trancones.")
        ]),
        ("03", C_NAVY, "RIGIDEZ ESTRUCTURAL", "Acoplamiento y Deuda Técnica (ATD)", [
            ("Monolito Inflexible:", "Acoplamiento estrecho entre la estructura topológica del grafo y los algoritmos de búsqueda."),
            ("Incapacidad de Conmutación:", "Imposible alternar en caliente entre criterios de tiempo, distancia o eficiencia energética."),
            ("Sin Auditoría ni Retorno:", "Inexistencia de bitácora transaccional para reversibilidad de maniobras ('undo').")
        ])
    ]

    card_w = Inches(3.64)
    card_h = Inches(5.7)
    spacing = Inches(0.4)
    base_x = Inches(0.8)
    base_y = Inches(1.42)

    for i, (badge_num, badge_col, kicker, title, bullets) in enumerate(cards_data):
        x = base_x + i * (card_w + spacing)
        add_card(slide, x, base_y, card_w, card_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        # Franja superior
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, base_y, card_w, Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = badge_col
        top_bar.line.fill.background()

        # Circular Badge
        add_circular_badge(slide, x + Inches(0.35), base_y + Inches(0.35), Inches(0.7), badge_num, bg_color=badge_col, font_size=13.5)

        # Kicker
        k_box = slide.shapes.add_textbox(x + Inches(1.2), base_y + Inches(0.38), Inches(2.2), Inches(0.25))
        p_k = k_box.text_frame.paragraphs[0]
        p_k.text = kicker
        p_k.font.name = "Arial"
        p_k.font.size = Pt(9)
        p_k.font.bold = True
        p_k.font.color.rgb = badge_col

        # Card Title
        t_box = slide.shapes.add_textbox(x + Inches(0.35), base_y + Inches(1.2), Inches(2.94), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK

        # Bullets aumentados a 11 pt
        b_box = slide.shapes.add_textbox(x + Inches(0.35), base_y + Inches(2.1), Inches(2.94), Inches(3.4))
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        for j, (p_bold, p_text) in enumerate(bullets):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            set_bullet_point(p, p_bold, p_text, font_size=11, bold_color=C_NAVY_DARK, text_color=C_BODY, space_after=8)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 3: Justificación e Impacto Multidimensional
# ---------------------------------------------------------------------------
def build_slide_03(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Impacto Multidimensional y Relevancia Operativa", "JUSTIFICACIÓN ARQUITECTÓNICA", 3)

    # Panel izquierdo oscuro destacado
    add_card(slide, Inches(0.8), Inches(1.42), Inches(4.5), Inches(5.7), bg_color=C_SLATE_HERO, border_color=None)

    l_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.75), Inches(3.7), Inches(4.8))
    tf_l = l_box.text_frame
    tf_l.word_wrap = True

    p1 = tf_l.paragraphs[0]
    p1.text = "VISIÓN ESTRATÉGICA"
    p1.font.name = "Arial"
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = C_TEAL

    p2 = tf_l.add_paragraph()
    p2.text = "La Navegación como Servicio de Misión Crítica"
    p2.font.name = "Arial"
    p2.font.size = Pt(21)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(8)
    p2.space_after = Pt(14)

    p3 = tf_l.add_paragraph()
    p3.text = "En operaciones de última milla, transporte de emergencia y flotas comerciales, un segundo de retraso en cruces complejos induce vacilación en conductores, demoras acumulativas y penalizaciones por incumplimiento de SLAs."
    p3.font.name = "Arial"
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.space_after = Pt(20)

    # Tarjeta métrica interna
    m_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.8), Inches(3.7), Inches(1.8))
    m_card.fill.solid()
    m_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    m_card.line.color.rgb = C_TEAL
    m_card.line.width = Pt(1)

    tf_mc = m_card.text_frame
    tf_mc.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_mc1 = tf_mc.paragraphs[0]
    p_mc1.alignment = PP_ALIGN.CENTER
    p_mc1.text = "LATENCIA OBJETIVO SUB-MILISEGUNDO"
    p_mc1.font.name = "Arial"
    p_mc1.font.size = Pt(9)
    p_mc1.font.bold = True
    p_mc1.font.color.rgb = C_TEAL

    p_mc2 = tf_mc.add_paragraph()
    p_mc2.alignment = PP_ALIGN.CENTER
    p_mc2.text = "p50 < 0.35 ms  ·  Caché < 0.10 ms"
    p_mc2.font.name = "Arial"
    p_mc2.font.size = Pt(14)
    p_mc2.font.bold = True
    p_mc2.font.color.rgb = C_WHITE

    # Panel derecho con 4 cards
    right_x = Inches(5.7)
    items = [
        ("UX", C_TEAL, "Experiencia de Usuario y Conducción Segura",
         "Despacho progresivo de maniobras sin pausas perceptibles en cruces de alta velocidad, eliminando desorientación."),
        ("CPU", C_AMBER, "Rendimiento y Caudal Transaccional del Servidor",
         "Sustitución de sondeo continuo por observadores selectivos O(K), abatiendo el 90 % del tráfico entrante inútil."),
        ("ECO", C_CORAL, "Eficiencia Energética y Logística de Flota",
         "Ahorro de 5 a 8 minutos de tránsito por recorrido urbano, minimizando consumo de combustible y emisiones de CO2."),
        ("MOD", C_BLUE, "Mantenibilidad y Arquitectura Evolutiva",
         "Adición de nuevos algoritmos heurísticos o bio-inspirados en caliente bajo Clean Architecture e interfaces DIP.")
    ]

    for i, (tag, col, h_title, h_desc) in enumerate(items):
        y = Inches(1.42) + i * Inches(1.4)
        add_card(slide, right_x, y, Inches(6.833), Inches(1.28), bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        add_circular_badge(slide, right_x + Inches(0.25), y + Inches(0.25), Inches(0.7), tag, bg_color=col, font_size=11)

        t_box = slide.shapes.add_textbox(right_x + Inches(1.15), y + Inches(0.18), Inches(5.4), Inches(0.9))
        tf = t_box.text_frame
        tf.word_wrap = True

        pt1 = tf.paragraphs[0]
        pt1.text = h_title
        pt1.font.name = "Arial"
        pt1.font.size = Pt(13)
        pt1.font.bold = True
        pt1.font.color.rgb = C_NAVY_DARK

        pt2 = tf.add_paragraph()
        pt2.text = h_desc
        pt2.font.name = "Arial"
        pt2.font.size = Pt(11)
        pt2.font.color.rgb = C_BODY
        pt2.space_before = Pt(3)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 4: Objetivos y Criterios Arquitectónicos
# ---------------------------------------------------------------------------
def build_slide_04(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Objetivos del Sistema y Requisitos de Calidad", "REQUISITOS Y ATRIBUTOS ISO/IEC 25010:2023", 4)

    objs = [
        ("OBJ 1", C_TEAL, "PODA ESPACIAL", "Poda Topológica Jerárquica",
         "Utilización de Recursos",
         "Particionar la red metropolitana en macro-zonas urbanas (`ZoneCluster`), logrando podar >= 45 % de los nodos evaluados en búsquedas de larga distancia."),
        ("OBJ 2", C_AMBER, "ADAPTABILIDAD", "Conmutación Algorítmica Dinámica",
         "Modificabilidad / Eficiencia",
         "Integrar múltiples estrategias de enrutamiento (A* dinámico, Dijkstra exacto, Pareto multiobjetivo) conmutables en caliente sin detener el motor."),
        ("OBJ 3", C_CORAL, "REACTIVIDAD", "Telemetría Asíncrona O(K)",
         "Fiabilidad / Recuperabilidad",
         "Ingestar eventos de congestión vial vía bus reactivo, notificando únicamente a los vehículos afectados y recalculando desvíos en tiempo sub-milisegundo."),
        ("OBJ 4", C_BLUE, "INTEGRIDAD", "Auditabilidad y Desacoplamiento",
         "Seguridad / Usabilidad",
         "Encapsular comandos transaccionales con capacidad de rollback (`undo`) y exponer maniobras paso a paso desacopladas de la matriz matemática del grafo.")
    ]

    card_w = Inches(2.7)
    card_h = Inches(5.7)
    spacing = Inches(0.31)
    base_x = Inches(0.8)
    base_y = Inches(1.42)

    for i, (badge_txt, col, tag, title, iso_attr, desc) in enumerate(objs):
        x = base_x + i * (card_w + spacing)
        add_card(slide, x, base_y, card_w, card_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        # Franja superior
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, base_y, card_w, Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        # Circular Badge
        add_circular_badge(slide, x + Inches(0.3), base_y + Inches(0.35), Inches(0.7), badge_txt, bg_color=col, font_size=10.5)

        # Tag
        tg_box = slide.shapes.add_textbox(x + Inches(1.15), base_y + Inches(0.4), Inches(1.4), Inches(0.25))
        p_tg = tg_box.text_frame.paragraphs[0]
        p_tg.text = tag
        p_tg.font.name = "Arial"
        p_tg.font.size = Pt(8.5)
        p_tg.font.bold = True
        p_tg.font.color.rgb = col

        # Título
        t_box = slide.shapes.add_textbox(x + Inches(0.3), base_y + Inches(1.2), Inches(2.1), Inches(0.75))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK

        # Badge ISO
        iso_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.3), base_y + Inches(2.05), Inches(2.1), Inches(0.32))
        iso_pill.fill.solid()
        iso_pill.fill.fore_color.rgb = C_CARD_ALT
        iso_pill.line.color.rgb = C_BORDER_LIGHT
        iso_pill.line.width = Pt(0.8)
        tf_iso = iso_pill.text_frame
        tf_iso.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_iso = tf_iso.paragraphs[0]
        p_iso.alignment = PP_ALIGN.CENTER
        p_iso.text = f"ISO 25010: {iso_attr}"
        p_iso.font.name = "Arial"
        p_iso.font.size = Pt(8)
        p_iso.font.bold = True
        p_iso.font.color.rgb = C_MUTED

        # Descripción aumentada a 10.5 pt
        d_box = slide.shapes.add_textbox(x + Inches(0.3), base_y + Inches(2.55), Inches(2.1), Inches(2.9))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_BODY
        p_d.line_spacing = 1.2


# ---------------------------------------------------------------------------
# DIAPOSITIVA 5: Vista de Componentes (UML 1)
# ---------------------------------------------------------------------------
def build_slide_05(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Arquitectura de Software: Vista de Componentes", "ESTRUCTURA MODULAR Y CAPAS", 5)

    # Diagrama de componentes a la izquierda
    add_proportional_image(slide, IMG_COMPONENTES, Inches(0.8), Inches(1.4), Inches(7.2), Inches(5.7))

    # Panel lateral derecho con 4 capas
    layers = [
        ("01", C_TEAL, "Capa de Presentación y Borde",
         "Mobile Vehicle Client, Fleet Dashboard y IoT Sensor Gateway consumen el sistema a través de un API Gateway REST (`/route`) y WebSockets (`/traffic-stream`)."),
        ("02", C_AMBER, "Capa de Coordinación Transaccional",
         "Navigation Session Manager coordina los viajes activos. Command Dispatcher encapsula las peticiones y TrafficEventBus actúa como Sujeto reactivo."),
        ("03", C_CORAL, "Motor de Enrutamiento y Caché",
         "Route Engine Context (Strategy) delega en implementaciones algorítmicas (A*, Dijkstra, Pareto), respaldado por una Caché Espacial reactiva LRU/TTL en memoria."),
        ("04", C_NAVY, "Topología y Travesía Espacial",
         "Topology Manager (Composite) gobierna la jerarquía de macro-zonas y tramos viales, exponiendo la ruta a clientes vía `IRouteIterator` (Iterator).")
    ]

    right_x = Inches(8.3)
    for i, (num, col, l_title, l_desc) in enumerate(layers):
        y = Inches(1.42) + i * Inches(1.4)
        add_card(slide, right_x, y, Inches(4.233), Inches(1.28), bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        add_circular_badge(slide, right_x + Inches(0.2), y + Inches(0.2), Inches(0.55), num, bg_color=col, font_size=10)

        t_box = slide.shapes.add_textbox(right_x + Inches(0.9), y + Inches(0.12), Inches(3.15), Inches(1.05))
        tf = t_box.text_frame
        tf.word_wrap = True

        pt1 = tf.paragraphs[0]
        pt1.text = l_title
        pt1.font.name = "Arial"
        pt1.font.size = Pt(12)
        pt1.font.bold = True
        pt1.font.color.rgb = C_NAVY_DARK

        pt2 = tf.add_paragraph()
        pt2.text = l_desc
        pt2.font.name = "Arial"
        pt2.font.size = Pt(9.5)
        pt2.font.color.rgb = C_BODY
        pt2.line_spacing = 1.15
        pt2.space_before = Pt(2)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 6: Catálogo e Integración de los 5 Patrones GoF
# ---------------------------------------------------------------------------
def build_slide_06(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Articulación y Sinergia de Patrones de Diseño GoF", "PATRONES DE DISEÑO GOF", 6)

    patterns = [
        ("STRATEGY", C_TEAL, "Patrón de Comportamiento",
         "Intercambio Algorítmico Dinámico",
         "Define la familia de algoritmos `IRoutingStrategy` (A*, Dijkstra, Pareto). Permite alternar la heurística en tiempo de ejecución sin alterar el motor ni los clientes.",
         "Modificabilidad & Eficiencia"),
        ("COMPOSITE", C_AMBER, "Patrón Estructural",
         "Jerarquía Vial y Poda Espacial",
         "Modela macro-zonas (`ZoneCluster`) y tramos viales (`RoadSegment`) bajo una misma interfaz `INetworkComponent`. Poda el 53.79% de nodos antes del cómputo.",
         "Utilización de Recursos"),
        ("OBSERVER", C_CORAL, "Patrón de Comportamiento",
         "Telemetría Reactiva de Incidentes",
         "Desacopla la ingestión masiva de sensores IoT. El `TrafficEventBus` notifica selectivamente en O(K) solo a los vehículos con tramos afectados en su ruta activa.",
         "Escalabilidad & Concurrencia"),
        ("COMMAND", C_BLUE, "Patrón de Comportamiento",
         "Acciones Transaccionales y Desvíos",
         "Encapsula peticiones de viaje (`NavigateCommand`) y recálculos (`RecalculateDetourCommand`). Habilita auditoría de trayectorias y soporte de reversibilidad (`undo`).",
         "Recuperabilidad & Integridad"),
        ("ITERATOR", C_INDIGO, "Patrón de Comportamiento",
         "Travesía Desacoplada de Maniobras",
         "Provee acceso secuencial a la lista de maniobras (`ManeuverStep`) sin exponer la matriz matemática del grafo al cliente móvil o a la interfaz de navegación.",
         "Modularidad & Usabilidad")
    ]

    card_w = Inches(11.733)
    card_h = Inches(1.04)
    base_x = Inches(0.8)
    base_y = Inches(1.4)
    spacing = Inches(0.12)

    for i, (name, col, p_type, title, desc, iso) in enumerate(patterns):
        y = base_y + i * (card_h + spacing)
        add_card(slide, base_x, y, card_w, card_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        # Franja lateral de color
        side_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, base_x, y, Inches(0.1), card_h)
        side_bar.fill.solid()
        side_bar.fill.fore_color.rgb = col
        side_bar.line.fill.background()

        # Badge del patrón
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, base_x + Inches(0.3), y + Inches(0.32), Inches(1.5), Inches(0.38))
        pill.fill.solid()
        pill.fill.fore_color.rgb = col
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pill = tf_p.paragraphs[0]
        p_pill.alignment = PP_ALIGN.CENTER
        p_pill.text = name
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(10)
        p_pill.font.bold = True
        p_pill.font.color.rgb = C_WHITE

        # Tipo GoF y Título
        t_box = slide.shapes.add_textbox(base_x + Inches(2.0), y + Inches(0.14), Inches(3.2), Inches(0.75))
        tf_t = t_box.text_frame
        p_t1 = tf_t.paragraphs[0]
        p_t1.text = p_type.upper()
        p_t1.font.name = "Arial"
        p_t1.font.size = Pt(8)
        p_t1.font.bold = True
        p_t1.font.color.rgb = col

        p_t2 = tf_t.add_paragraph()
        p_t2.text = title
        p_t2.font.name = "Arial"
        p_t2.font.size = Pt(12.5)
        p_t2.font.bold = True
        p_t2.font.color.rgb = C_NAVY_DARK

        # Descripción técnica (10 pt)
        d_box = slide.shapes.add_textbox(base_x + Inches(5.3), y + Inches(0.14), Inches(4.5), Inches(0.78))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_BODY
        p_d.line_spacing = 1.15

        # Tag ISO 25010
        iso_box = slide.shapes.add_textbox(base_x + Inches(9.9), y + Inches(0.22), Inches(1.65), Inches(0.55))
        tf_iso = iso_box.text_frame
        tf_iso.word_wrap = True
        p_i1 = tf_iso.paragraphs[0]
        p_i1.text = "ATRIBUTO ISO:"
        p_i1.font.name = "Arial"
        p_i1.font.size = Pt(7.5)
        p_i1.font.bold = True
        p_i1.font.color.rgb = C_MUTED

        p_i2 = tf_iso.add_paragraph()
        p_i2.text = iso
        p_i2.font.name = "Arial"
        p_i2.font.size = Pt(9)
        p_i2.font.bold = True
        p_i2.font.color.rgb = C_NAVY_DARK


# ---------------------------------------------------------------------------
# DIAPOSITIVA 7: Poda Topológica (Composite) e Iterador (Iterator)
# ---------------------------------------------------------------------------
def build_slide_07(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Poda Topológica (Composite) e Iterador de Maniobras", "DESACOPLAMIENTO ALGORÍTMICO Y ESTRUCTURAL", 7)

    col_w = Inches(5.65)
    col_h = Inches(5.7)

    # Columna Izquierda: Composite
    x_l = Inches(0.8)
    add_card(slide, x_l, Inches(1.42), col_w, col_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

    sb_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_l, Inches(1.42), col_w, Inches(0.08))
    sb_l.fill.solid()
    sb_l.fill.fore_color.rgb = C_TEAL
    sb_l.line.fill.background()

    add_circular_badge(slide, x_l + Inches(0.4), Inches(1.75), Inches(0.7), "CMP", bg_color=C_TEAL, font_size=12)

    t_box_l = slide.shapes.add_textbox(x_l + Inches(1.3), Inches(1.75), Inches(4.0), Inches(0.8))
    tf_tl = t_box_l.text_frame
    p_tl1 = tf_tl.paragraphs[0]
    p_tl1.text = "PATRÓN COMPOSITE (ESTRUCTURAL)"
    p_tl1.font.name = "Arial"
    p_tl1.font.size = Pt(9.5)
    p_tl1.font.bold = True
    p_tl1.font.color.rgb = C_TEAL

    p_tl2 = tf_tl.add_paragraph()
    p_tl2.text = "Jerarquización Vial y Poda Espacial"
    p_tl2.font.name = "Arial"
    p_tl2.font.size = Pt(16)
    p_tl2.font.bold = True
    p_tl2.font.color.rgb = C_NAVY_DARK

    bullets_l = [
        ("Interfaz Común INetworkComponent:", "Trata de forma polimórfica a hojas atómicas (`RoadSegment`) y contenedores jerárquicos (`ZoneCluster`)."),
        ("Conexión por Corredores Arteriales:", "Las macro-zonas urbanas se comunican exclusivamente mediante avenidas centrales y vías troncales de alta velocidad."),
        ("Estrategia de Poda del Subgrafo:", "Al calcular una ruta entre zonas distantes, se descartan automáticamente todas las calles capilares intermedias irrelevantes."),
        ("Impacto de Rendimiento Medido:", "Logra una reducción neta del 53.79 % en los nodos explorados (25.0 frente a 54.1 nodos en Dijkstra), eliminando operaciones de cola.")
    ]

    b_box_l = slide.shapes.add_textbox(x_l + Inches(0.4), Inches(2.65), Inches(4.85), Inches(4.2))
    tf_bl = b_box_l.text_frame
    tf_bl.word_wrap = True
    for i, (b_bold, b_txt) in enumerate(bullets_l):
        p = tf_bl.paragraphs[0] if i == 0 else tf_bl.add_paragraph()
        set_bullet_point(p, b_bold, b_txt, font_size=11, space_after=10)

    # Columna Derecha: Iterator
    x_r = Inches(6.88)
    add_card(slide, x_r, Inches(1.42), col_w, col_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

    sb_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_r, Inches(1.42), col_w, Inches(0.08))
    sb_r.fill.solid()
    sb_r.fill.fore_color.rgb = C_NAVY
    sb_r.line.fill.background()

    add_circular_badge(slide, x_r + Inches(0.4), Inches(1.75), Inches(0.7), "ITR", bg_color=C_NAVY, font_size=12)

    t_box_r = slide.shapes.add_textbox(x_r + Inches(1.3), Inches(1.75), Inches(4.0), Inches(0.8))
    tf_tr = t_box_r.text_frame
    p_tr1 = tf_tr.paragraphs[0]
    p_tr1.text = "PATRÓN ITERATOR (COMPORTAMIENTO)"
    p_tr1.font.name = "Arial"
    p_tr1.font.size = Pt(9.5)
    p_tr1.font.bold = True
    p_tr1.font.color.rgb = C_NAVY

    p_tr2 = tf_tr.add_paragraph()
    p_tr2.text = "Travesía Uniforme y Desacoplada"
    p_tr2.font.name = "Arial"
    p_tr2.font.size = Pt(16)
    p_tr2.font.bold = True
    p_tr2.font.color.rgb = C_NAVY_DARK

    bullets_r = [
        ("Desacoplamiento Estricto del Cliente:", "El dispositivo móvil o panel vehicular desconoce la matriz matemática de adyacencia y la estructura interna del grafo."),
        ("Interfaz Estándar IRouteIterator:", "Provee operaciones de cursor `has_next()`, `next()`, `current()` y `reset()` para un consumo progresivo paso a paso."),
        ("Entidad Limpia ManeuverStep:", "Cada elemento expone instrucción textual, distancia en metros, tiempo estimado y dirección de giro para sintetizadores de voz."),
        ("Sincronización en Caliente ante Desvíos:", "El método `update_route_path()` ajusta las maniobras pendientes tras un recálculo dinámico sin reiniciar el viaje del conductor.")
    ]

    b_box_r = slide.shapes.add_textbox(x_r + Inches(0.4), Inches(2.65), Inches(4.85), Inches(4.2))
    tf_br = b_box_r.text_frame
    tf_br.word_wrap = True
    for i, (b_bold, b_txt) in enumerate(bullets_r):
        p = tf_br.paragraphs[0] if i == 0 else tf_br.add_paragraph()
        set_bullet_point(p, b_bold, b_txt, font_size=11, space_after=10)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 8: Flujo de Navegación y Secuencia (UML 2)
# ---------------------------------------------------------------------------
def build_slide_08(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Flujo de Navegación y Recálculo Dinámico (Secuencia UML)", "DINÁMICA TEMPORAL DEL SISTEMA", 8)

    # Imagen del diagrama de secuencia centrada arriba
    add_proportional_image(slide, IMG_SECUENCIA, Inches(0.8), Inches(1.38), Inches(11.733), Inches(3.65))

    # 3 Fases del proceso en la parte inferior
    phases = [
        ("FASE 1", C_TEAL, "Cálculo y Poda Inicial",
         "Petición al API Gateway -> Dispatcher ejecuta `NavigateCommand` -> Consulta en Caché Espacial -> `TopologyManager` podar grafo con Composite -> Cálculo A* -> Suscripción de observador."),
        ("FASE 2", C_AMBER, "Travesía con Iterador",
         "El vehículo inicia su marcha consumiendo maniobras secuenciales vía `ManeuverIterator.next()`. El grafo permanece encapsulado en el servidor sin transmisión pesada."),
        ("FASE 3", C_CORAL, "Re-enrutamiento Proactivo",
         "Sensor IoT detecta incidente en tramo vial -> `TrafficEventBus` notifica en O(K) -> Si delta C > tau (60 s), se dispara `RecalculateDetourCommand` -> Desvío en 0.66 ms.")
    ]

    p_w = Inches(3.64)
    p_h = Inches(1.85)
    base_x = Inches(0.8)
    base_y = Inches(5.2)
    sp = Inches(0.4)

    for i, (fase_tag, col, f_title, f_desc) in enumerate(phases):
        x = base_x + i * (p_w + sp)
        add_card(slide, x, base_y, p_w, p_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        # Franja superior
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, base_y, p_w, Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = col
        top_bar.line.fill.background()

        # Tag
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), base_y + Inches(0.18), Inches(1.0), Inches(0.28))
        pill.fill.solid()
        pill.fill.fore_color.rgb = col
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pill = tf_p.paragraphs[0]
        p_pill.alignment = PP_ALIGN.CENTER
        p_pill.text = fase_tag
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(9)
        p_pill.font.bold = True
        p_pill.font.color.rgb = C_WHITE

        # Titulo
        t_box = slide.shapes.add_textbox(x + Inches(1.3), base_y + Inches(0.15), Inches(2.2), Inches(0.35))
        p_t = t_box.text_frame.paragraphs[0]
        p_t.text = f_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK

        # Descripcion (9.5 pt)
        d_box = slide.shapes.add_textbox(x + Inches(0.2), base_y + Inches(0.55), Inches(3.24), Inches(1.2))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = f_desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_BODY
        p_d.line_spacing = 1.15


# ---------------------------------------------------------------------------
# DIAPOSITIVA 9: Diagrama de Clases (UML 3)
# ---------------------------------------------------------------------------
def build_slide_09(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Modelo de Dominio e Integración de Clases (UML)", "ESTRUCTURA INTERNA Y ACOPLAMIENTO", 9)

    add_proportional_image(slide, IMG_CLASES, Inches(0.8), Inches(1.4), Inches(7.2), Inches(5.7))

    principles = [
        ("DIP", C_TEAL, "Inversión de Dependencias (DIP)",
         "El núcleo `RoutingEngine` interactúa exclusivamente con la abstracción `IRoutingStrategy`, permitiendo incorporar nuevas heurísticas bio-inspiradas sin tocar el motor."),
        ("SRP", C_AMBER, "Responsabilidad Única (SRP)",
         "Separación tajante de funciones: `CommandInvoker` audita transacciones, `TrafficEventBus` gestiona la telemetría pub/sub y `TopologyManager` resuelve la geometría vial."),
        ("OCP", C_BLUE, "Abierto / Cerrado (OCP)",
         "La jerarquía `INetworkComponent` permite agregar nuevos tipos de agrupaciones viales (ej. túneles, peajes) sin alterar la lógica de poda del algoritmo."),
        ("CMD", C_CORAL, "Transaccionalidad y Reversibilidad",
         "Los comandos `NavigateCommand` y `RecalculateDetourCommand` almacenan la ruta anterior en su pila, garantizando el retroceso (`undo`) ante cancelaciones.")
    ]

    right_x = Inches(8.3)
    for i, (tag, col, p_title, p_desc) in enumerate(principles):
        y = Inches(1.42) + i * Inches(1.4)
        add_card(slide, right_x, y, Inches(4.233), Inches(1.28), bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        add_circular_badge(slide, right_x + Inches(0.2), y + Inches(0.2), Inches(0.55), tag, bg_color=col, font_size=10)

        t_box = slide.shapes.add_textbox(right_x + Inches(0.9), y + Inches(0.12), Inches(3.15), Inches(1.05))
        tf = t_box.text_frame
        tf.word_wrap = True

        pt1 = tf.paragraphs[0]
        pt1.text = p_title
        pt1.font.name = "Arial"
        pt1.font.size = Pt(12)
        pt1.font.bold = True
        pt1.font.color.rgb = C_NAVY_DARK

        pt2 = tf.add_paragraph()
        pt2.text = p_desc
        pt2.font.name = "Arial"
        pt2.font.size = Pt(9.5)
        pt2.font.color.rgb = C_BODY
        pt2.line_spacing = 1.15
        pt2.space_before = Pt(2)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 10: Diagrama de Actividad (UML 4)
# ---------------------------------------------------------------------------
def build_slide_10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Lógica de Control y Supervisión Concurrente (Actividad UML)", "FLUJO ALGORÍTMICO Y COMPORTAMIENTO", 10)

    add_proportional_image(slide, IMG_ACTIVIDAD, Inches(0.8), Inches(1.4), Inches(7.2), Inches(5.7))

    gates = [
        ("01", C_TEAL, "Comprobación de Caché Espacial",
         "Acceso en memoria O(1). Si hay acierto (*Cache Hit*), la ruta se entrega en < 0.10 ms sin ejecutar ningún cálculo algorítmico sobre el grafo."),
        ("02", C_AMBER, "Poda Topológica (Composite)",
         "Ante un *Cache Miss*, el sistema extrae el subgrafo específico de las macro-zonas origen/destino y corredores arteriales, reduciendo 53.79 % de nodos."),
        ("03", C_BLUE, "Selección Dinámica (Strategy)",
         "Instanciación en caliente: A* Heurístico con factor de congestión alfa para tráfico dinámico, Dijkstra para exactitud estricta, o Pareto multiobjetivo."),
        ("04", C_CORAL, "Fork Concurrente y Desvío Crítico",
         "Consumo paso a paso vía iterador en paralelo con monitoreo de incidentes. Si delta C > tau (60 s), se emite `RecalculateDetourCommand` sin detener al conductor.")
    ]

    right_x = Inches(8.3)
    for i, (num, col, g_title, g_desc) in enumerate(gates):
        y = Inches(1.42) + i * Inches(1.4)
        add_card(slide, right_x, y, Inches(4.233), Inches(1.28), bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        add_circular_badge(slide, right_x + Inches(0.2), y + Inches(0.2), Inches(0.55), num, bg_color=col, font_size=10)

        t_box = slide.shapes.add_textbox(right_x + Inches(0.9), y + Inches(0.12), Inches(3.15), Inches(1.05))
        tf = t_box.text_frame
        tf.word_wrap = True

        pt1 = tf.paragraphs[0]
        pt1.text = g_title
        pt1.font.name = "Arial"
        pt1.font.size = Pt(12)
        pt1.font.bold = True
        pt1.font.color.rgb = C_NAVY_DARK

        pt2 = tf.add_paragraph()
        pt2.text = g_desc
        pt2.font.name = "Arial"
        pt2.font.size = Pt(9.5)
        pt2.font.color.rgb = C_BODY
        pt2.line_spacing = 1.15
        pt2.space_before = Pt(2)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 11: Prototipo Funcional y Escenario Experimental
# ---------------------------------------------------------------------------
def build_slide_11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Prototipo Funcional y Entorno Experimental", "IMPLEMENTACIÓN Y VERIFICACIÓN EMPÍRICA", 11)

    cards = [
        ("01", C_TEAL, "TOPOLOGÍA SINTÉTICA", "Red Vial Urbana Multizona", [
            ("100 Intersecciones (Nodos):", "Distribuidas uniformemente en 4 macro-zonas (Zona Norte, Oriente, Occidente y Sur)."),
            ("164 Tramos Viales (Aristas):", "Calles locales (40 km/h), avenidas arteriales (60 km/h) y troncales interzonales (80 km/h)."),
            ("Perturbaciones Estocásticas:", "Pesos viales variables modelando tráfico urbano realista.")
        ]),
        ("02", C_AMBER, "ARQUITECTURA MODULAR", "Núcleo Algorítmico en Python 3", [
            ("Paquete nexusnav/:", "Separación modular limpia de patrones (`composite.py`, `strategy.py`, `observer.py`, `command.py`, `iterator.py`)."),
            ("Caché Espacial Reactiva:", "Almacenamiento LRU en memoria con tiempo de vida (TTL) y soporte de invalidación granular."),
            ("Clean Architecture:", "Cero dependencias cruzadas entre el motor de búsqueda y la presentación.")
        ]),
        ("03", C_BLUE, "BANCO DE PRUEBAS", "Suite Automatizada (benchmark.py)", [
            ("100 Consultas Origen-Destino:", "Pares interzonales aleatorios evaluados concurrentemente bajo condiciones homogéneas."),
            ("Métricas Cuantitativas:", "Registro estricto de latencias en percentiles p50, p95 y p99, y recuento de nodos explorados."),
            ("4 Configuraciones Comparadas:", "Dijkstra completo, A* completo, NexusNav (Composite+A*) y NexusNav en Caché.")
        ]),
        ("04", C_CORAL, "INYECCIÓN DE CAOS", "Simulación de Incidentes Dinámicos", [
            ("Incidente Vial Crítico:", "Inyección de evento `INC-991` (retraso 5.0x) sobre el tercer tramo de una ruta activa."),
            ("Despacho Selectivo en Bus:", "Validación del patrón Observer sin sondeo periódico de clientes telemáticos."),
            ("Recálculo y Desvío:", "Emisión de `RecalculateDetourCommand` y sincronización inmediata del iterador en 0.66 ms.")
        ])
    ]

    card_w = Inches(5.65)
    card_h = Inches(2.72)
    base_x = Inches(0.8)
    base_y = Inches(1.42)
    sp_x = Inches(0.43)
    sp_y = Inches(0.24)

    for i, (num, col, kicker, title, bullets) in enumerate(cards):
        col_idx = i % 2
        row_idx = i // 2
        x = base_x + col_idx * (card_w + sp_x)
        y = base_y + row_idx * (card_h + sp_y)

        add_card(slide, x, y, card_w, card_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        # Franja lateral
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.08), card_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        add_circular_badge(slide, x + Inches(0.25), y + Inches(0.25), Inches(0.55), num, bg_color=col, font_size=11)

        # Kicker & Titulo
        t_box = slide.shapes.add_textbox(x + Inches(0.95), y + Inches(0.18), Inches(4.4), Inches(0.65))
        tf = t_box.text_frame
        p1 = tf.paragraphs[0]
        p1.text = kicker
        p1.font.name = "Arial"
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Arial"
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY_DARK

        # Bullets aumentados a 10.5 pt
        b_box = slide.shapes.add_textbox(x + Inches(0.35), y + Inches(0.85), Inches(5.1), Inches(1.75))
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        for j, (p_bold, p_txt) in enumerate(bullets):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            set_bullet_point(p, p_bold, p_txt, font_size=10.5, space_after=5)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 12: Resultados: Latencia y Nodos Explorados
# ---------------------------------------------------------------------------
def build_slide_02_metrics(slide):
    pass


def build_slide_12(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Resultados Experimentales: Latencia y Reducción del Grafo", "BENCHMARKING DE RENDIMIENTO", 12)

    # Dos gráficas a la izquierda
    add_proportional_image(slide, IMG_LATENCIA, Inches(0.8), Inches(1.4), Inches(4.6), Inches(3.6))
    add_proportional_image(slide, IMG_NODOS, Inches(5.6), Inches(1.4), Inches(4.6), Inches(3.6))

    # Panel lateral derecho con KPIs clave
    right_x = Inches(10.4)
    # KPI 1: Poda de nodos
    kpi1 = add_card(slide, right_x, Inches(1.4), Inches(2.133), Inches(2.65), bg_color=C_CARD_BG, border_color=C_TEAL, border_width=1.5)
    tf1 = kpi1.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "PODA DE GRAFO"
    p1.font.name = "Arial"
    p1.font.size = Pt(9)
    p1.font.bold = True
    p1.font.color.rgb = C_TEAL

    p2 = tf1.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "-53.79%"
    p2.font.name = "Arial"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = C_NAVY_DARK

    p3 = tf1.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "De 54.1 nodos evaluados en Dijkstra a solo 25.0 nodos en NexusNav gracias a la poda con Composite."
    p3.font.name = "Arial"
    p3.font.size = Pt(9)
    p3.font.color.rgb = C_BODY
    p3.space_before = Pt(4)

    # KPI 2: Aceleración
    kpi2 = add_card(slide, right_x, Inches(4.3), Inches(2.133), Inches(2.65), bg_color=C_CARD_BG, border_color=C_CORAL, border_width=1.5)
    tf2 = kpi2.text_frame
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf2.word_wrap = True
    p4 = tf2.paragraphs[0]
    p4.alignment = PP_ALIGN.CENTER
    p4.text = "ACELERACIÓN"
    p4.font.name = "Arial"
    p4.font.size = Pt(9)
    p4.font.bold = True
    p4.font.color.rgb = C_CORAL

    p5 = tf2.add_paragraph()
    p5.alignment = PP_ALIGN.CENTER
    p5.text = "4.13x"
    p5.font.name = "Arial"
    p5.font.size = Pt(28)
    p5.font.bold = True
    p5.font.color.rgb = C_NAVY_DARK

    p6 = tf2.add_paragraph()
    p6.alignment = PP_ALIGN.CENTER
    p6.text = "Latencia mediana reducida de 0.33 ms a 0.08 ms sirviendo desde la Caché Espacial reactiva."
    p6.font.name = "Arial"
    p6.font.size = Pt(9)
    p6.font.color.rgb = C_BODY
    p6.space_before = Pt(4)

    # Tabla resumen inferior (9.5 pt)
    t_card = add_card(slide, Inches(0.8), Inches(5.2), Inches(9.4), Inches(1.85), bg_color=C_CARD_ALT, border_color=C_BORDER_LIGHT)
    tf_t = t_card.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "TABLA COMPARATIVA DE RENDIMIENTO (100 CONSULTAS ORIGEN-DESTINO ALEATORIAS)"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(10)
    p_t.font.bold = True
    p_t.font.color.rgb = C_NAVY_DARK

    bullets_t = [
        ("Dijkstra Monolítico:", "p50: 0.33 ms | p95: 0.44 ms | p99: 0.51 ms | Nodos explorados: 54.1 (Línea base)."),
        ("A* Grafo Completo:", "p50: 0.32 ms | p95: 0.48 ms | p99: 0.55 ms | Nodos explorados: 28.5 (Mejora heurística)."),
        ("NexusNav (Composite + A*):", "p50: 0.34 ms | p95: 0.43 ms | p99: 0.47 ms | Nodos explorados: 25.0 (Poda neta 53.79 %)."),
        ("NexusNav (Cache Hit):", "p50: 0.08 ms | p95: 0.10 ms | p99: 0.11 ms | Nodos: 0.0 | Aceleración: 4.13x con cola ultra-estable.")
    ]
    for b_bold, b_txt in bullets_t:
        p = tf_t.add_paragraph()
        set_bullet_point(p, b_bold, b_txt, font_size=9.5, space_after=3)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 13: Resultados: Throughput y Desvío Dinámico
# ---------------------------------------------------------------------------
def build_slide_13(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Resultados: Escalabilidad y Re-enrutamiento Proactivo", "BENCHMARKING DE CONCURRENCIA Y CAOS", 13)

    # Dos gráficas a la izquierda
    add_proportional_image(slide, IMG_THROUGHPUT, Inches(0.8), Inches(1.4), Inches(4.6), Inches(3.6))
    add_proportional_image(slide, IMG_DESVIO, Inches(5.6), Inches(1.4), Inches(4.6), Inches(3.6))

    # Panel lateral derecho con KPIs clave
    right_x = Inches(10.4)
    # KPI 1: Throughput
    kpi1 = add_card(slide, right_x, Inches(1.4), Inches(2.133), Inches(2.65), bg_color=C_CARD_BG, border_color=C_BLUE, border_width=1.5)
    tf1 = kpi1.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "CAUDAL MÁXIMO"
    p1.font.name = "Arial"
    p1.font.size = Pt(9)
    p1.font.bold = True
    p1.font.color.rgb = C_BLUE

    p2 = tf1.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = ">10 500"
    p2.font.name = "Arial"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = C_NAVY_DARK

    p3 = tf1.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "Rutas / segundo con Caché Activa. Modo Activo sostiene hasta 5 400 r/s (frente a 2 200 r/s de Dijkstra)."
    p3.font.name = "Arial"
    p3.font.size = Pt(9)
    p3.font.color.rgb = C_BODY
    p3.space_before = Pt(4)

    # KPI 2: Tiempo de Desvío
    kpi2 = add_card(slide, right_x, Inches(4.3), Inches(2.133), Inches(2.65), bg_color=C_CARD_BG, border_color=C_AMBER, border_width=1.5)
    tf2 = kpi2.text_frame
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf2.word_wrap = True
    p4 = tf2.paragraphs[0]
    p4.alignment = PP_ALIGN.CENTER
    p4.text = "DESVÍO PROACTIVO"
    p4.font.name = "Arial"
    p4.font.size = Pt(9)
    p4.font.bold = True
    p4.font.color.rgb = C_AMBER

    p5 = tf2.add_paragraph()
    p5.alignment = PP_ALIGN.CENTER
    p5.text = "0.66 ms"
    p5.font.name = "Arial"
    p5.font.size = Pt(26)
    p5.font.bold = True
    p5.font.color.rgb = C_NAVY_DARK

    p6 = tf2.add_paragraph()
    p6.alignment = PP_ALIGN.CENTER
    p6.text = "Cómputo algorítmico del desvío alternativo (2.69 ms acumulados con notificación y sincronización)."
    p6.font.name = "Arial"
    p6.font.size = Pt(9)
    p6.font.color.rgb = C_BODY
    p6.space_before = Pt(4)

    # Desglose temporal inferior (9.5 pt)
    t_card = add_card(slide, Inches(0.8), Inches(5.2), Inches(9.4), Inches(1.85), bg_color=C_CARD_ALT, border_color=C_BORDER_LIGHT)
    tf_t = t_card.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "DESGLOSE TEMPORAL DEL CICLO REACTIVO ANTE INCIDENTES VIALES (INC-991)"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(10)
    p_t.font.bold = True
    p_t.font.color.rgb = C_NAVY_DARK

    bullets_t = [
        ("Ingestión y Despacho en Bus (1.20 ms):", "Sensor IoT publica evento -> TrafficEventBus notifica selectivamente a observadores afectados."),
        ("Evaluación de Impacto (0.30 ms):", "RouteMonitorObserver calcula delta C > 60 s y decide disparar el recálculo dinámico."),
        ("Cálculo del Desvío Óptimo (0.66 ms):", "RecalculateDetourCommand invoca el motor A* podando el tramo bloqueado (nueva ruta: 7 512.6 m, 428.59 s)."),
        ("Actualización del Iterador (0.50 ms):", "ManeuverIterator sincroniza en caliente 16 maniobras pendientes sin detener la marcha del vehículo.")
    ]
    for b_bold, b_txt in bullets_t:
        p = tf_t.add_paragraph()
        set_bullet_point(p, b_bold, b_txt, font_size=9.5, space_after=3)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 14: Evaluación Arquitectónica Formal: Método ATAM (SEI)
# ---------------------------------------------------------------------------
def build_slide_14(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Evaluación Arquitectónica Formal: Método ATAM (SEI)", "EVALUACIÓN DE ATRIBUTOS DE CALIDAD", 14)

    quads = [
        ("01", C_TEAL, "ÁRBOL DE UTILIDAD (UTILITY TREE)", "Escenarios de Calidad Priorizados", [
            ("Eficiencia de Desempeño (Alto/Medio):", "Latencia p95 < 2.0 ms bajo 100 consultas concurrentes usando poda Composite y A*."),
            ("Caché en Memoria (Alto/Bajo):", "Consultas repetidas despachadas en < 0.2 ms desde caché espacial."),
            ("Recuperabilidad (Alto/Alto):", "Detección de bloqueo vial y recálculo de desvío resuelto en < 50 ms."),
            ("Mantenibilidad (Medio/Bajo):", "Incorporación de nuevas estrategias de enrutamiento en < 2 días sin alterar clientes.")
        ]),
        ("02", C_AMBER, "PUNTOS DE SENSIBILIDAD", "Parámetros Críticos del Sistema", [
            ("S1 - Umbral de Desvío (tau = 60 s):", "Un umbral muy bajo induce recálculos espurios ('route fluttering'); un umbral alto retarda la evasión."),
            ("S2 - Granularidad de Macro-zonas:", "Zonas muy grandes minimizan la poda espacial; zonas diminutas encarecen la composición de corredores arteriales."),
            ("S3 - Política de Expiración TTL:", "Balancea frescura de las condiciones de congestión vs tasa de aciertos en caché espacial.")
        ]),
        ("03", C_BLUE, "COMPROMISOS (TRADE-OFFS)", "Balances Arquitectónicos Explícitos", [
            ("T1 - Memoria RAM vs Velocidad:", "Almacenar rutas en caché espacial consume RAM en servidores, a cambio de acelerar la respuesta 4.13x."),
            ("T2 - Poda vs Optimalidad Global:", "Descartar calles capilares intermedias podría omitir un atajo marginal (<1.5 % probabilidad), a cambio de reducir 53.79 % de nodos evaluados."),
            ("T3 - Centralización vs Desacoplamiento:", "Coordinación transaccional centralizada frente a travesía autónoma en clientes móviles.")
        ]),
        ("04", C_CORAL, "RIESGOS Y NO-RIESGOS", "Matriz de Mitigación Técnica", [
            ("Riesgo R1 (Inconsistencia de Caché):", "Rutas cacheadas desactualizadas ante incidentes súbitos. Mitigación: Invalidación síncrona en el bus de eventos."),
            ("No-Riesgo NR1 (Extensibilidad):", "La adición de nuevos algoritmos no introduce regresiones gracias al contrato `IRoutingStrategy`."),
            ("No-Riesgo NR2 (Sobrecarga IoT):", "El patrón Observer garantiza que el arribo de telemetría no degrada a los clientes que navegan.")
        ])
    ]

    card_w = Inches(5.65)
    card_h = Inches(2.72)
    base_x = Inches(0.8)
    base_y = Inches(1.42)
    sp_x = Inches(0.43)
    sp_y = Inches(0.24)

    for i, (num, col, kicker, title, bullets) in enumerate(quads):
        col_idx = i % 2
        row_idx = i // 2
        x = base_x + col_idx * (card_w + sp_x)
        y = base_y + row_idx * (card_h + sp_y)

        add_card(slide, x, y, card_w, card_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(0.08), card_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = col
        bar.line.fill.background()

        add_circular_badge(slide, x + Inches(0.25), y + Inches(0.25), Inches(0.55), num, bg_color=col, font_size=11)

        t_box = slide.shapes.add_textbox(x + Inches(0.95), y + Inches(0.18), Inches(4.4), Inches(0.65))
        tf = t_box.text_frame
        p1 = tf.paragraphs[0]
        p1.text = kicker
        p1.font.name = "Arial"
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = col

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Arial"
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = C_NAVY_DARK

        # Bullets aumentados a 10 pt
        b_box = slide.shapes.add_textbox(x + Inches(0.35), y + Inches(0.85), Inches(5.1), Inches(1.75))
        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        for j, (p_bold, p_txt) in enumerate(bullets):
            p = tf_b.paragraphs[0] if j == 0 else tf_b.add_paragraph()
            set_bullet_point(p, p_bold, p_txt, font_size=10, space_after=3)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 15: Conclusiones Arquitectónicas y Trabajo Futuro
# ---------------------------------------------------------------------------
def build_slide_15(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_header(slide, "Conclusiones Técnicas y Líneas de Evolución Futura", "SÍNTESIS Y CONCLUSIONES", 15)

    col_w = Inches(5.65)
    col_h = Inches(5.7)

    # Panel Izquierdo: Conclusiones
    x_l = Inches(0.8)
    add_card(slide, x_l, Inches(1.42), col_w, col_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

    sb_l = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_l, Inches(1.42), col_w, Inches(0.08))
    sb_l.fill.solid()
    sb_l.fill.fore_color.rgb = C_TEAL
    sb_l.line.fill.background()

    add_circular_badge(slide, x_l + Inches(0.4), Inches(1.75), Inches(0.7), "OK", bg_color=C_TEAL, font_size=12)

    t_box_l = slide.shapes.add_textbox(x_l + Inches(1.3), Inches(1.75), Inches(4.0), Inches(0.8))
    tf_tl = t_box_l.text_frame
    p_tl1 = tf_tl.paragraphs[0]
    p_tl1.text = "LECCIONES Y LOGROS ARQUITECTÓNICOS"
    p_tl1.font.name = "Arial"
    p_tl1.font.size = Pt(9.5)
    p_tl1.font.bold = True
    p_tl1.font.color.rgb = C_TEAL

    p_tl2 = tf_tl.add_paragraph()
    p_tl2.text = "Conclusiones de la Arquitectura NexusNav"
    p_tl2.font.name = "Arial"
    p_tl2.font.size = Pt(16)
    p_tl2.font.bold = True
    p_tl2.font.color.rgb = C_NAVY_DARK

    bullets_l = [
        ("Sinergia de Patrones GoF:", "La articulación de Strategy, Composite, Observer, Command e Iterator erradicó la rigidez de los motores monolíticos, aislando cálculo, telemetría y travesía."),
        ("Poda Topológica Efectiva (-53.79 %):", "La estructuración jerárquica con Composite comprobó experimentalmente reducir más de la mitad del espacio de búsqueda sin degradar la precisión."),
        ("Aceleración y Escalabilidad Extrema:", "La combinación de caché reactiva y A* redujo la latencia mediana a 0.08 ms (4.13x) y sostuvo más de 10 500 rutas/s bajo concurrencia."),
        ("Resiliencia en Tiempo Real:", "El ciclo proactivo de detección y desvío resolvió incidentes en 2.69 ms acumulados (0.66 ms de cómputo), garantizando continuidad de viaje.")
    ]

    b_box_l = slide.shapes.add_textbox(x_l + Inches(0.4), Inches(2.65), Inches(4.85), Inches(4.2))
    tf_bl = b_box_l.text_frame
    tf_bl.word_wrap = True
    for i, (b_bold, b_txt) in enumerate(bullets_l):
        p = tf_bl.paragraphs[0] if i == 0 else tf_bl.add_paragraph()
        set_bullet_point(p, b_bold, b_txt, font_size=11, space_after=10)

    # Panel Derecho: Trabajo Futuro
    x_r = Inches(6.88)
    add_card(slide, x_r, Inches(1.42), col_w, col_h, bg_color=C_CARD_BG, border_color=C_BORDER_LIGHT)

    sb_r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x_r, Inches(1.42), col_w, Inches(0.08))
    sb_r.fill.solid()
    sb_r.fill.fore_color.rgb = C_BLUE
    sb_r.line.fill.background()

    add_circular_badge(slide, x_r + Inches(0.4), Inches(1.75), Inches(0.7), "FUT", bg_color=C_BLUE, font_size=12)

    t_box_r = slide.shapes.add_textbox(x_r + Inches(1.3), Inches(1.75), Inches(4.0), Inches(0.8))
    tf_tr = t_box_r.text_frame
    p_tr1 = tf_tr.paragraphs[0]
    p_tr1.text = "EVOLUCIÓN Y ROADMAP TÉCNICO"
    p_tr1.font.name = "Arial"
    p_tr1.font.size = Pt(9.5)
    p_tr1.font.bold = True
    p_tr1.font.color.rgb = C_BLUE

    p_tr2 = tf_tr.add_paragraph()
    p_tr2.text = "Líneas de Evolución Futura"
    p_tr2.font.name = "Arial"
    p_tr2.font.size = Pt(16)
    p_tr2.font.bold = True
    p_tr2.font.color.rgb = C_NAVY_DARK

    bullets_r = [
        ("Factor de Congestión con Machine Learning:", "Implementar modelos ligeros de Reinforcement Learning para calibrar adaptativamente el parámetro alfa según series temporales de tráfico histórico."),
        ("Microservicios Distribuidos en la Nube:", "Contenerizar los componentes en Kubernetes y desacoplar la caché en clústeres de Redis distribuidos con replicación geográfica."),
        ("Ingestión Masiva OpenStreetMap (500k+ Nodos):", "Extender el generador topológico hacia redes viales metropolitanas reales de escala continental con integración de datos GIS y satelitales."),
        ("Enrutamiento Multiobjetivo para Flotas Eléctricas:", "Incorporar modelos de consumo energético dependientes de topografía y puntos de recarga rápida con algoritmos de frontera de Pareto.")
    ]

    b_box_r = slide.shapes.add_textbox(x_r + Inches(0.4), Inches(2.65), Inches(4.85), Inches(4.2))
    tf_br = b_box_r.text_frame
    tf_br.word_wrap = True
    for i, (b_bold, b_txt) in enumerate(bullets_r):
        p = tf_br.paragraphs[0] if i == 0 else tf_br.add_paragraph()
        set_bullet_point(p, b_bold, b_txt, font_size=11, space_after=10)


# ---------------------------------------------------------------------------
# DIAPOSITIVA 16: Cierre y Acceso a Recursos
# ---------------------------------------------------------------------------
def build_slide_16(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Fondo Héroe Oscuro elegante
    add_card(slide, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), bg_color=C_SLATE_HERO, border_color=None)

    # Franja de acento superior
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.12))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = C_TEAL
    stripe.line.fill.background()

    # Kicker
    k_box = slide.shapes.add_textbox(Inches(1.4), Inches(1.3), Inches(10.5), Inches(0.35))
    p_k = k_box.text_frame.paragraphs[0]
    p_k.text = "ARQUITECTURA DE SOFTWARE · REPOSITORIO Y ARTEFACTOS DEL PROYECTO"
    p_k.font.name = "Arial"
    p_k.font.size = Pt(10.5)
    p_k.font.bold = True
    p_k.font.color.rgb = C_TEAL

    # Título
    t_box = slide.shapes.add_textbox(Inches(1.4), Inches(1.7), Inches(10.5), Inches(0.8))
    p_t = t_box.text_frame.paragraphs[0]
    p_t.text = "NexusNav: Recursos y Acceso a la Plataforma"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE

    # 3 Cards horizontales de recursos
    resources = [
        ("GITHUB", C_TEAL, "Código Fuente y Artefactos",
         "https://github.com/Alboguaci/nexusnav-routing-architecture",
         "Repositorio oficial con código de patrones GoF, generador de grafos, suite de benchmarking y modelos UML."),
        ("YOUTUBE", C_CORAL, "Demostración Técnica en Video",
         "https://youtu.be/IqVim9WxDhA (14 min 25 s)",
         "Sustentación oral, recorrido arquitectónico de patrones, demostración en vivo del prototipo ejecutable y análisis de resultados."),
        ("DOCS", C_BLUE, "Documento de Arquitectura Formal",
         "Informe_Actividad6_Navegando_Mareas.pdf (15 págs)",
         "Informe técnico exhaustivo con especificación de requisitos ISO 25010, modelos PlantUML, evaluación formal ATAM y referencias.")
    ]

    card_w = Inches(3.38)
    card_h = Inches(2.65)
    sp = Inches(0.35)
    base_x = Inches(1.4)
    base_y = Inches(2.55)

    for i, (badge_txt, col, r_title, r_link, r_desc) in enumerate(resources):
        x = base_x + i * (card_w + sp)
        add_card(slide, x, base_y, card_w, card_h, bg_color=RGBColor(30, 41, 59), border_color=col, border_width=1.2)

        # Badge
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.25), base_y + Inches(0.22), Inches(1.1), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = col
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pill = tf_p.paragraphs[0]
        p_pill.alignment = PP_ALIGN.CENTER
        p_pill.text = badge_txt
        p_pill.font.name = "Arial"
        p_pill.font.size = Pt(9.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = C_WHITE

        # Titulo
        t_box = slide.shapes.add_textbox(x + Inches(0.25), base_y + Inches(0.65), Inches(2.88), Inches(0.45))
        p_t = t_box.text_frame.paragraphs[0]
        p_t.text = r_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        # Enlace
        l_box = slide.shapes.add_textbox(x + Inches(0.25), base_y + Inches(1.10), Inches(2.88), Inches(0.45))
        tf_l = l_box.text_frame
        tf_l.word_wrap = True
        p_l = tf_l.paragraphs[0]
        p_l.text = r_link
        p_l.font.name = "Arial"
        p_l.font.size = Pt(9)
        p_l.font.bold = True
        p_l.font.color.rgb = col

        # Descripcion (10.5 pt)
        d_box = slide.shapes.add_textbox(x + Inches(0.25), base_y + Inches(1.60), Inches(2.88), Inches(0.95))
        tf_d = d_box.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = r_desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = RGBColor(203, 213, 225)
        p_d.line_spacing = 1.15

    # Pie de autores
    f_box = slide.shapes.add_textbox(Inches(1.4), Inches(5.45), Inches(10.5), Inches(0.5))
    tf_f = f_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Arquitectura de Software  ·  Juan Carlos Benítez Rojas & Juan José Córdoba Eraso  ·  2026"
    p_f.font.name = "Arial"
    p_f.font.size = Pt(11)
    p_f.font.color.rgb = C_MUTED


# ---------------------------------------------------------------------------
# MAIN BUILDER
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("INICIANDO GENERACIÓN DE DIAPOSITIVAS EN POWERPOINT (NEXUSNAV)")
    print("=" * 70)

    prs = init_presentation()

    print("Generando diapositivas con estilo editorial corporativo...")
    build_slide_01(prs)  # 1. Portada
    build_slide_02(prs)  # 2. Desafíos Arquitectónicos (Problema)
    build_slide_03(prs)  # 3. Impacto Multidimensional (Justificación)
    build_slide_04(prs)  # 4. Objetivos y Criterios ISO 25010
    build_slide_05(prs)  # 5. Vista de Componentes (UML 1)
    build_slide_06(prs)  # 6. Catálogo de los 5 Patrones GoF
    build_slide_07(prs)  # 7. Composite e Iterator en Detalle
    build_slide_08(prs)  # 8. Flujo y Secuencia (UML 2)
    build_slide_09(prs)  # 9. Modelo de Clases (UML 3)
    build_slide_10(prs)  # 10. Flujo de Actividad y Decisiones (UML 4)
    build_slide_11(prs)  # 11. Prototipo Funcional y Pruebas
    build_slide_12(prs)  # 12. Métricas: Latencia y Nodos Explorados
    build_slide_13(prs)  # 13. Métricas: Throughput y Desvío Dinámico
    build_slide_14(prs)  # 14. Evaluación Formal ATAM (SEI)
    build_slide_15(prs)  # 15. Conclusiones y Trabajo Futuro
    build_slide_16(prs)  # 16. Cierre y Enlaces a Recursos

    prs.save(OUTPUT_PPTX)
    print(f"-> Presentación guardada en: {OUTPUT_PPTX} ({OUTPUT_PPTX.stat().st_size} bytes)")

    # Copia en la raíz de la carpeta de trabajo
    prs.save(WORKSPACE_PPTX)
    print(f"-> Copia guardada en: {WORKSPACE_PPTX} ({WORKSPACE_PPTX.stat().st_size} bytes)")

    print("=" * 70)
    print("PRESENTACIÓN GENERADA EXITOSAMENTE (16 DIAPOSITIVAS EN FORMATO 16:9).")
    print("=" * 70)


if __name__ == "__main__":
    main()
