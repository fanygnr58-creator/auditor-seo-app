import pandas as pd
import streamlit as st
from io import BytesIO
import random

st.set_page_config(page_title="Auditor SEO PRO Muebles", layout="wide")
st.title("🚀 Auditor SEO PRO Muebles (Copywriter Automático REAL)")

file = st.file_uploader("Sube tu archivo", type=["xlsx", "csv"])
MIN_IMAGES = 4

# 🧠 MEMORIA GLOBAL (evita repetición)
frases_usadas = set()

def elegir_unico(lista):
    opciones = [x for x in lista if x not in frases_usadas]
    if not opciones:
        frases_usadas.clear()
        opciones = lista
    elegido = random.choice(opciones)
    frases_usadas.add(elegido)
    return elegido

# 🧠 CATEGORÍAS
def detectar_categoria(title):
    t = title.lower()
    if "comedor" in t or "set" in t:
        return "comedor"
    elif "silla" in t:
        return "silla"
    elif "escritorio" in t:
        return "escritorio"
    elif "sofa" in t or "sofá" in t:
        return "sofa"
    return "general"

# 🧠 MATERIALES
def detectar_materiales(title):
    t = title.lower()
    mats = []

    if "madera" in t or "melamina" in t:
        mats.append("estructura en madera resistente")
    if "metal" in t:
        mats.append("base metálica de alta durabilidad")
    if "tela" in t:
        mats.append("tapizado en tela cómoda")
    if "piel" in t or "vinil" in t:
        mats.append("acabado tipo piel elegante")

    return mats

# 🧠 ATRIBUTOS
def detectar_atributos(title):
    t = title.lower()
    atributos = []

    if "4" in t:
        atributos.append("incluye 4 piezas")
    if "6" in t:
        atributos.append("incluye 6 piezas")
    if "rectangular" in t:
        atributos.append("mesa rectangular")
    if "circular" in t:
        atributos.append("mesa circular")
    if "negro" in t:
        atributos.append("acabado en color negro")
    if "blanco" in t:
        atributos.append("acabado en color blanco")

    return atributos

# 🧠 BULLETS
def generar_bullets(cat, materiales, atributos):
    base = {
        "comedor": [
            "Ideal para reuniones familiares",
            "Diseño moderno y funcional",
            "Optimiza tu espacio"
        ],
        "silla": [
            "Comodidad prolongada",
            "Diseño ergonómico",
            "Uso versátil"
        ],
        "general": [
            "Alta calidad",
            "Diseño funcional",
            "Uso versátil"
        ]
    }

    bullets = base.get(cat, base["general"]) + materiales + atributos
    random.shuffle(bullets)
    return bullets[:6]

# 🧠 FRASES HUMANAS
intros = [
    "Transforma tu espacio con este",
    "Dale un toque moderno a tu hogar con este",
    "Renueva tu ambiente con este",
    "Haz de tu espacio un lugar más funcional con este"
]

desarrollos = [
    "Diseñado para adaptarse a diferentes espacios, combinando estética y funcionalidad.",
    "Pensado para brindar comodidad y estilo en el día a día.",
    "Una opción práctica que se integra fácilmente en distintos ambientes.",
    "Ideal para quienes buscan equilibrio entre diseño y utilidad."
]

cierres = [
    "Perfecto para complementar tu hogar.",
    "Una excelente elección para tu espacio.",
    "Ideal para uso diario con estilo.",
    "Gran opción para mejorar tu ambiente."
]

# 🧠 GENERADOR PRO
def generar_desc(title, market, cat, materiales):
    atributos = detectar_atributos(title)
    bullets = generar_bullets(cat, materiales, atributos)

    intro = elegir_unico(intros)
    desarrollo = elegir_unico(desarrollos)
    cierre = elegir_unico(cierres)

    bullets_txt = "\n".join([f"✔️ {b}" for b in bullets])

    estructura = random.choice([1,2,3])

    if estructura == 1:
        return f"""🔹 {title}

{intro} {cat} {', '.join(atributos[:2])}.

{desarrollo}

{bullets_txt}

{cierre}"""

    elif estructura == 2:
        return f"""🔹 {title}

{desarrollo}

{intro} {cat} ideal para tu espacio.

{bullets_txt}

{cierre}"""

    else:
        return f"""🔹 {title}

{intro} {cat} pensado para tu hogar.

{bullets_txt}

{desarrollo}

{cierre}"""

# 🧠 TÍTULO SEO
def optimizar_titulo(title, market, cat):
    m = market.lower()

    if "amazon" in m:
        return f"{title} {cat} moderno resistente hogar oficina"[:120]
    if "mercado" in m:
        return f"{title} nuevo envío gratis garantía"[:120]
    if "walmart" in m:
        return f"{title} mueble hogar calidad precio"[:120]

    return title[:120]

# 🎨 EXPORTAR
def exportar_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# 🚀 PROCESO
if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df.fillna("", inplace=True)

    if st.button("🚀 Arreglar TODO PRO"):
        nuevos = []

        for _, row in df.iterrows():
            title = str(row.get("title", ""))
            market = str(row.get("marketplace", ""))

            cat = detectar_categoria(title)
            materiales = detectar_materiales(title)

            nuevo_titulo = optimizar_titulo(title, market, cat)
            nueva_desc = generar_desc(title, market, cat, materiales)

            nuevos.append({
                "Título Nuevo": nuevo_titulo,
                "Descripción Nueva": nueva_desc
            })

        final_df = pd.concat([df, pd.DataFrame(nuevos)], axis=1)

        st.dataframe(final_df, use_container_width=True)

        st.download_button(
            "📥 Descargar Excel PRO",
            exportar_excel(final_df),
            "auditoria_pro.xlsx"
        )
