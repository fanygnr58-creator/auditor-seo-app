import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Auditor SEO PRO Muebles", layout="wide")
st.title("🚀 Auditor SEO PRO Muebles (Nivel Empresa)")

file = st.file_uploader("Sube tu archivo", type=["xlsx", "csv"])
MIN_IMAGES = 4

# 🧠 CATEGORIZACIÓN COMPLETA MUEBLES
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
    elif "banco" in t or "banca" in t:
        return "banca"
    elif "archivero" in t:
        return "archivero"
    elif "librero" in t or "estante" in t:
        return "librero"
    elif "closet" in t or "ropero" in t:
        return "closet"
    elif "cama" in t:
        return "cama"
    elif "buró" in t or "buro" in t:
        return "buro"
    elif "tocador" in t:
        return "tocador"
    
    return "general"

# 🧠 DETECTAR MATERIALES
def detectar_materiales(title):
    t = title.lower()
    mats = []

    if "madera" in t or "melamina" in t:
        mats.append("estructura en madera/melamina")
    if "metal" in t or "acero" in t:
        mats.append("estructura metálica resistente")
    if "plastico" in t or "plástico" in t:
        mats.append("material plástico duradero")
    if "tela" in t:
        mats.append("tapizado en tela")
    if "piel" in t or "vinil" in t:
        mats.append("acabado tipo piel")

    return mats

# 🧠 BULLETS DINÁMICOS
def generar_bullets(cat, materiales):
    base = []

    if cat == "silla":
        base = ["Diseño ergonómico", "Comodidad prolongada", "Ideal para oficina"]
    elif cat == "comedor":
        base = ["Ideal para reuniones", "Diseño moderno", "Ahorro de espacio"]
    elif cat == "sofa":
        base = ["Máximo confort", "Diseño elegante", "Ideal para sala"]
    elif cat == "escritorio":
        base = ["Espacio funcional", "Ideal para trabajo", "Diseño moderno"]
    else:
        base = ["Alta calidad", "Diseño funcional", "Uso versátil"]

    return base + materiales

# 🧠 SEO POR MARKETPLACE
def optimizar_titulo(title, market, cat):
    m = market.lower()

    if "amazon" in m:
        return f"{title} {cat} moderno resistente hogar oficina"[:120]

    if "mercado" in m:
        return f"{title} nuevo envío gratis garantía"[:120]

    if "walmart" in m:
        return f"{title} mueble hogar calidad precio"[:120]

    if "liverpool" in m:
        return f"{title} diseño premium hogar moderno"[:120]

    if "coppel" in m:
        return f"{title} práctico económico hogar"[:120]

    if "elektra" in m:
        return f"{title} oferta especial mueble hogar"[:120]

    if "shopify" in m:
        return f"{title} tienda oficial diseño exclusivo"[:120]

    return title[:120]

# 🧠 DESCRIPCIONES PRO
def generar_desc(title, market, cat, materiales, bullets):
    m = market.lower()

    bullets_txt = "\n".join([f"✔️ {b}" for b in bullets])

    if "amazon" in m:
        return f"""🔹 {title}

Producto diseñado para ofrecer funcionalidad y estilo en cualquier espacio.

{bullets_txt}

Perfecto para hogar u oficina."""

    if "mercado" in m:
        return f"""🔹 {title}

Producto nuevo listo para envío inmediato 🚀

{bullets_txt}

📦 Envío rápido\n🔒 Garantía incluida"""

    if "walmart" in m:
        return f"""🔹 {title}

Renueva tu espacio con este mueble funcional.

{bullets_txt}

Gran opción para tu hogar."""

    if "liverpool" in m:
        return f"""🔹 {title}

Diseño elegante que complementa cualquier ambiente.

{bullets_txt}

Ideal para espacios modernos."""

    return f"""🔹 {title}

{bullets_txt}"""

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
        market = str(row.get("marketplace", ""))

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
            bullets = generar_bullets(cat, materiales)

            nuevo_titulo = optimizar_titulo(title, market, cat)
            nueva_desc = generar_desc(nuevo_titulo, market, cat, materiales, bullets)

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
