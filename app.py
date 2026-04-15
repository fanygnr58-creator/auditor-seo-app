import pandas as pd
import streamlit as st
from io import BytesIO
import random

st.set_page_config(page_title="Auditor SEO PRO Muebles", layout="wide")
st.title("🚀 Auditor SEO PRO Muebles (Nivel Humano Real)")

file = st.file_uploader("Sube tu archivo", type=["xlsx", "csv"])
MIN_IMAGES = 4

# 🧠 CATEGORÍAS
def detectar_categoria(title):
    t = title.lower()

    if "comedor" in t or "set" in t:
        return "comedor"
    elif "silla" in t:
        return "silla"
    elif "escritorio" in t:
        return "escritorio"
    elif "mesa" in t:
        return "mesa"
    elif "sofa" in t or "sofá" in t:
        return "sofa"
    elif "sillon" in t or "sillón" in t:
        return "sillon"
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

# 🧠 ATRIBUTOS DINÁMICOS
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

    if "oslo" in t:
        atributos.append("diseño moderno estilo Oslo")

    return atributos

# 🧠 BULLETS
def generar_bullets(cat, materiales, atributos):
    base = []

    if cat == "comedor":
        base = [
            "Ideal para reuniones familiares",
            "Diseño moderno y funcional",
            "Optimiza tu espacio"
        ]
    elif cat == "silla":
        base = [
            "Comodidad durante largas jornadas",
            "Diseño ergonómico",
            "Versátil para hogar u oficina"
        ]
    else:
        base = [
            "Alta calidad",
            "Diseño funcional",
            "Uso versátil"
        ]

    return base + materiales + atributos

# 🧠 VARIACIÓN HUMANA
introducciones = [
    "Transforma tu espacio con este increíble",
    "Dale un toque moderno a tu hogar con este",
    "Renueva tu ambiente con este funcional",
    "Haz de tu espacio un lugar más cómodo con este"
]

cierres = [
    "Perfecto para complementar tu hogar con estilo y funcionalidad.",
    "Una excelente opción para quienes buscan diseño y practicidad.",
    "Ideal para crear espacios cómodos y bien aprovechados.",
    "Diseñado para adaptarse a diferentes necesidades del día a día."
]

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

# 🧠 DESCRIPCIÓN HUMANA PRO
def generar_desc(title, market, cat, materiales):
    atributos = detectar_atributos(title)
    bullets = generar_bullets(cat, materiales, atributos)

    intro_random = random.choice(introducciones)
    cierre_random = random.choice(cierres)

    bullets_txt = "\n".join([f"✔️ {b}" for b in bullets])

    intro = f"{intro_random} {cat} {', '.join(atributos[:2])}." if atributos else f"{intro_random} {cat} ideal para tu espacio."

    parrafo_extra = ""
    if cat == "comedor":
        parrafo_extra = "Este set de comedor está pensado para brindar comodidad y estilo en reuniones familiares o momentos cotidianos, adaptándose fácilmente a diferentes espacios del hogar."
    elif cat == "silla":
        parrafo_extra = "Su diseño está enfocado en brindar confort durante el uso continuo, manteniendo una estética moderna y funcional."
    else:
        parrafo_extra = "Diseñado para ofrecer funcionalidad sin sacrificar el estilo, adaptándose a distintos entornos."

    return f"""🔹 {title}

{intro}

{parrafo_extra}

{bullets_txt}

{cierre_random}"""

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

    resultados = []

    for _, row in df.iterrows():
        title = str(row.get("title", ""))
        desc = str(row.get("description", ""))
        images = str(row.get("images", "")).split(",")

        score = 100

        if len(title) < 50:
            score -= 25
        if len(images) < MIN_IMAGES:
            score -= 20
        if len(desc) < 120:
            score -= 25

        prioridad = "🟢 Bien"
        if score < 80:
            prioridad = "🟠 Mejorar"
        if score < 50:
            prioridad = "🔴 Urgente"

        resultados.append({
            "Producto": title,
            "Score SEO": score,
            "Prioridad": prioridad
        })

    st.dataframe(pd.DataFrame(resultados), use_container_width=True)

    if st.button("🚀 Arreglar TODO PRO"):
        nuevos = []

        for _, row in df.iterrows():
            title = str(row.get("title", ""))
            market = str(row.get("marketplace", ""))

            cat = detectar_categoria(title)
            materiales = detectar_materiales(title)

            nuevo_titulo = optimizar_titulo(title, market, cat)
            nueva_desc = generar_desc(nuevo_titulo, market, cat, materiales)

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
