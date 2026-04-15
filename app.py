import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Auditor SEO PRO", layout="wide")

st.title("🚀 Auditor SEO Inteligente PRO (IA GRATIS)")

file = st.file_uploader("Sube tu archivo", type=["xlsx", "csv"])

MIN_IMAGES = 4

# 🧠 Detectar categoría
def detectar_categoria(title):
    t = title.lower()
    if "silla" in t:
        return "silla"
    elif "escritorio" in t:
        return "escritorio"
    elif "mesa" in t:
        return "mesa"
    return "general"

# 🧠 Reglas marketplace
def reglas(market):
    m = str(market).lower()
    if "amazon" in m:
        return ["ergonómico", "oficina", "ajustable", "resistente"]
    if "mercado" in m:
        return ["nuevo", "garantía", "envío gratis"]
    if "walmart" in m:
        return ["calidad", "oferta", "hogar"]
    return ["premium", "original"]

# ✨ Optimizar título
def optimizar_titulo(title, market):
    cat = detectar_categoria(title)
    kws = reglas(market)

    nuevo = title.strip()

    for kw in kws:
        if kw not in nuevo.lower():
            nuevo += f" {kw}"

    if cat == "silla":
        nuevo += " ergonómica cómoda oficina"
    if cat == "escritorio":
        nuevo += " moderno funcional"

    return nuevo[:120]

# ✨ Descripción inteligente
def generar_desc(title):
    cat = detectar_categoria(title)

    if cat == "silla":
        return f"""🔹 {title}

🪑 Diseño ergonómico para máxima comodidad
🛠️ Material resistente y duradero
📏 Ideal para oficina o home office

✔️ Ajuste de altura
✔️ Soporte lumbar
✔️ Estilo moderno

🚚 Envío rápido y seguro"""

    if cat == "escritorio":
        return f"""🔹 {title}

🖥️ Espacio ideal para trabajar o estudiar
🛠️ Estructura firme y resistente
📏 Diseño moderno y funcional

✔️ Fácil armado
✔️ Excelente estabilidad
✔️ Amplia superficie

🚚 Entrega segura"""

    return f"""🔹 {title}

✔️ Alta calidad
✔️ Diseño funcional
✔️ Uso versátil

🚚 Envío rápido"""

# 🎨 Exportar Excel bonito
def exportar_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)

        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        format_red = workbook.add_format({"bg_color": "#FFC7CE"})
        format_yellow = workbook.add_format({"bg_color": "#FFEB9C"})
        format_green = workbook.add_format({"bg_color": "#C6EFCE"})

        worksheet.conditional_format("C2:C1000", {
            "type": "cell",
            "criteria": "<",
            "value": 50,
            "format": format_red
        })
        worksheet.conditional_format("C2:C1000", {
            "type": "cell",
            "criteria": "between",
            "minimum": 50,
            "maximum": 80,
            "format": format_yellow
        })
        worksheet.conditional_format("C2:C1000", {
            "type": "cell",
            "criteria": ">",
            "value": 80,
            "format": format_green
        })

    return output.getvalue()

# 🚀 PROCESO
if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df.fillna("", inplace=True)

    st.success("Archivo cargado ✅")

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

    view_df = pd.DataFrame(resultados)
    st.dataframe(view_df, use_container_width=True)

    # 🚀 BOTÓN PRO
    if st.button("🚀 Arreglar TODO (IA GRATIS)"):
        nuevos = []

        for _, row in df.iterrows():
            title = str(row.get("title", ""))
            market = str(row.get("marketplace", ""))

            nuevo_titulo = optimizar_titulo(title, market)
            nueva_desc = generar_desc(nuevo_titulo)

            nuevos.append({
                "Título Nuevo": nuevo_titulo,
                "Descripción Nueva": nueva_desc
            })

        nuevos_df = pd.DataFrame(nuevos)
        final_df = pd.concat([df, nuevos_df], axis=1)

        st.success("🔥 Optimización completa")

        st.dataframe(final_df, use_container_width=True)

        st.download_button(
            "📥 Descargar Excel PRO",
            exportar_excel(final_df),
            "auditoria_pro.xlsx"
        )
