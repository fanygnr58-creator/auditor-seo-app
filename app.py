import io
import re
import pandas as pd
import streamlit as st

# =========================
# ⚙️ CONFIG APP
# =========================
st.set_page_config(page_title="Auditoría Inteligente PRO (Web)", layout="wide")
st.title("🧠 Auditoría Inteligente de Listings (IA GRATIS - Web)")

st.caption("Audita, optimiza y exporta listings para Amazon, Mercado Libre y Walmart — sin API.")

# =========================
# 🔧 CONFIG GLOBAL
# =========================
KEYWORDS_DEFAULT = ["original", "nuevo", "oficial", "garantía", "envío gratis", "premium"]
MIN_IMAGES = 4
MIN_DESC_LENGTH = 120

# =========================
# 🧠 REGLAS POR MARKETPLACE
# =========================
def reglas_marketplace(marketplace: str):
    m = str(marketplace).lower()
    if "amazon" in m:
        return {"min_title": 80, "keywords": ["ergonómico", "oficina", "resistente", "ajustable"]}
    elif "mercado" in m:
        return {"min_title": 60, "keywords": ["nuevo", "garantía", "envío gratis"]}
    elif "walmart" in m:
        return {"min_title": 50, "keywords": ["calidad", "hogar", "oferta"]}
    else:
        return {"min_title": 40, "keywords": KEYWORDS_DEFAULT}

# =========================
# 🧹 UTILIDADES
# =========================
def limpiar_texto(t: str):
    t = str(t).replace("\n", " ").strip()
    t = re.sub(r"\s+", " ", t)
    return t

# =========================
# 🧠 DETECCIÓN DE CATEGORÍA (MEJORADA)
# =========================
def detectar_categoria(title: str):
    t = title.lower()
    reglas = {
        "silla": ["silla", "butaca", "banco"],
        "escritorio": ["escritorio", "desk", "mesa de trabajo"],
        "mesa": ["mesa", "comedor", "table"],
        "sofa": ["sofá", "sofa", "sillón"],
        "archivero": ["archivero", "cajonera", "archivo"],
    }
    for cat, kws in reglas.items():
        if any(k in t for k in kws):
            return cat
    return "general"

# =========================
# ✏️ OPTIMIZADOR DE TÍTULO
# =========================
def optimizar_titulo_inteligente(title: str, keywords: list):
    base = limpiar_texto(title)
    cat = detectar_categoria(base)

    # agrega keywords faltantes
    for kw in keywords:
        if kw not in base.lower():
            base += f" {kw}"

    # ajustes por categoría
    if cat == "silla" and "ergonómica" not in base.lower():
        base += " ergonómica cómoda oficina"
    if cat == "escritorio":
        base += " moderno funcional amplio"
    if cat == "mesa":
        base += " resistente hogar comedor"
    if cat == "sofa":
        base += " cómodo elegante sala"
    if cat == "archivero":
        base += " organizador resistente oficina"

    # limpieza final + límite típico
    base = limpiar_texto(base)
    return base[:120]

# =========================
# 📝 DESCRIPCIÓN INTELIGENTE
# =========================
def generar_descripcion_inteligente(title: str):
    cat = detectar_categoria(title)

    if cat == "silla":
        return f"""🔹 {title}

🪑 Silla ergonómica diseñada para máxima comodidad
🛠️ Estructura resistente y duradera
📏 Ideal para oficina o home office

✔️ Ajuste de altura
✔️ Soporte cómodo
✔️ Diseño moderno

🚚 Envío rápido y seguro
"""
    if cat == "escritorio":
        return f"""🔹 {title}

🖥️ Escritorio funcional para trabajo o estudio
🛠️ Material resistente de alta calidad
📏 Superficie amplia y organizada

✔️ Fácil armado
✔️ Estabilidad superior
✔️ Diseño moderno

🚚 Envío seguro
"""
    if cat == "mesa":
        return f"""🔹 {title}

🍽️ Mesa ideal para comedor o uso diario
🛠️ Material duradero
📏 Tamaño práctico para tu espacio

✔️ Fácil limpieza
✔️ Estructura firme
✔️ Estilo moderno

🚚 Entrega segura
"""
    if cat == "sofa":
        return f"""🔹 {title}

🛋️ Sofá cómodo para sala
🛠️ Estructura sólida y acolchado confortable
✨ Diseño elegante

✔️ Ideal para descanso
✔️ Material resistente
✔️ Estilo moderno

🚚 Envío seguro
"""
    if cat == "archivero":
        return f"""🔹 {title}

🗂️ Archivero para organización de documentos
🛠️ Estructura resistente
📏 Compacto y funcional

✔️ Cajones amplios
✔️ Fácil uso
✔️ Ideal para oficina

🚚 Envío rápido
"""
    return f"""🔹 {title}

✔️ Producto de alta calidad
✔️ Diseño funcional
✔️ Material resistente

🚚 Envío rápido
"""

# =========================
# 🖼️ SUGERENCIAS DE IMÁGENES
# =========================
def sugerir_imagenes(cantidad_actual: int):
    faltantes = max(0, MIN_IMAGES - int(cantidad_actual))
    ideas = [
        "Foto principal fondo blanco",
        "Foto en uso",
        "Detalle / close-up",
        "Empaque",
        "Medidas / dimensiones",
        "Lifestyle"
    ]
    return ideas[:faltantes]

# =========================
# 🚀 AUTO OPTIMIZACIÓN
# =========================
def auto_optimizar_row(row):
    title = str(row.get("title", ""))
    marketplace = str(row.get("marketplace", ""))

    rules = reglas_marketplace(marketplace)
    keywords = rules["keywords"]

    nuevo_titulo = optimizar_titulo_inteligente(title, keywords)
    nueva_desc = generar_descripcion_inteligente(nuevo_titulo)

    return pd.Series({
        "Título Optimizado": nuevo_titulo,
        "Descripción Optimizada": nueva_desc
    })

# =========================
# 📦 CARGA ARCHIVO (CACHE)
# =========================
@st.cache_data(show_spinner=False)
def cargar_archivo(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)

# =========================
# 🧪 VALIDACIÓN COLUMNAS
# =========================
def validar_columnas(df):
    cols = [c.lower() for c in df.columns]
    mapping = {}
    for c in df.columns:
        cl = c.lower()
        if "title" in cl or "titulo" in cl:
            mapping["title"] = c
        if "desc" in cl:
            mapping["description"] = c
        if "image" in cl:
            mapping["images"] = c
        if "market" in cl:
            mapping["marketplace"] = c

    # fallback
    for k in ["title", "description", "images", "marketplace"]:
        if k not in mapping:
            mapping[k] = k  # asume que ya existe

    return mapping

# =========================
# 🧠 AUDITORÍA
# =========================
def auditar(df, mapping):
    results = []

    for _, row in df.iterrows():
        title = str(row.get(mapping["title"], ""))
        description = str(row.get(mapping["description"], "")).lower()
        images_list = str(row.get(mapping["images"], "")).split(",")
        marketplace = str(row.get(mapping["marketplace"], ""))

        rules = reglas_marketplace(marketplace)
        min_title = rules["min_title"]
        keywords = rules["keywords"]

        issues, recs, extras = [], [], []

        # título
        if len(title) < min_title:
            issues.append("Título corto")
            recs.append(f"Mínimo {min_title} caracteres")

        missing_keywords = [k for k in keywords if k not in title.lower()]
        if missing_keywords:
            issues.append("Faltan keywords")
            recs.append(f"Agregar: {', '.join(missing_keywords[:3])}")

        # imágenes
        if len(images_list) < MIN_IMAGES:
            issues.append("Pocas imágenes")
            extras.append(f"📸 Agregar: {', '.join(sugerir_imagenes(len(images_list)))}")

        if images_list and "http" not in images_list[0]:
            issues.append("Imagen principal inválida")

        # descripción
        if "sin descripcion" in description or len(description) < MIN_DESC_LENGTH:
            issues.append("Descripción pobre")

        # score
        score = 100
        if len(title) < min_title: score -= 25
        if len(images_list) < MIN_IMAGES: score -= 20
        if len(description) < MIN_DESC_LENGTH: score -= 25
        if missing_keywords: score -= 20
        score = max(score, 0)

        if score < 50:
            prioridad = "🔴 Urgente"
        elif score < 80:
            prioridad = "🟠 Mejorar"
        else:
            prioridad = "🟢 Bien"

        results.append({
            "Marketplace": marketplace,
            "Producto": title,
            "Score SEO": score,
            "Prioridad": prioridad,
            "Problemas": ", ".join(issues),
            "Recomendaciones": " | ".join(recs),
            "Sugerencias": "\n".join(extras)
        })

    return pd.DataFrame(results)

# =========================
# 📤 EXPORTAR EXCEL BONITO
# =========================
def exportar_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Auditoria")
        wb  = writer.book
        ws  = writer.sheets["Auditoria"]

        # formatos
        red = wb.add_format({"bg_color": "#FFC7CE"})
        yellow = wb.add_format({"bg_color": "#FFEB9C"})
        green = wb.add_format({"bg_color": "#C6EFCE"})

        # aplica colores por prioridad
        pr_col = list(df.columns).index("Prioridad")
        for i, val in enumerate(df["Prioridad"], start=1):
            fmt = green if "🟢" in val else yellow if "🟠" in val else red
            ws.set_row(i, None, fmt)

        ws.set_column(0, len(df.columns)-1, 28)

    return output.getvalue()

# =========================
# 🧾 UI
# =========================
file = st.file_uploader("Sube tu archivo (.xlsx o .csv)", type=["xlsx", "csv"])

if file:
    df = cargar_archivo(file)
    df.fillna("", inplace=True)

    mapping = validar_columnas(df)

    st.success("Archivo cargado ✅")

    # auditoría
    result_df = auditar(df, mapping)

    # métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", len(result_df))
    c2.metric("🔴 Urgentes", len(result_df[result_df["Prioridad"]=="🔴 Urgente"]))
    c3.metric("🟢 Bien", len(result_df[result_df["Prioridad"]=="🟢 Bien"]))

    # filtro
    filtro = st.selectbox("Filtrar por prioridad", ["Todos", "🔴 Urgente", "🟠 Mejorar", "🟢 Bien"])
    view_df = result_df if filtro == "Todos" else result_df[result_df["Prioridad"] == filtro]

    st.dataframe(view_df, use_container_width=True)

    # descargas
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button("📥 Descargar CSV", view_df.to_csv(index=False), "auditoria.csv", "text/csv")
    with col_dl2:
        st.download_button("📥 Descargar Excel (colores)", exportar_excel(view_df), "auditoria.xlsx")

    st.divider()

    # 🚀 AUTO-OPTIMIZAR
    if st.button("🚀 Arreglar TODO (IA GRATIS)"):
        optimizados = df.apply(auto_optimizar_row, axis=1)
        df_final = pd.concat([df, optimizados], axis=1)

        st.success("Optimización completa 🔥")
        st.dataframe(df_final, use_container_width=True)

        col2_dl1, col2_dl2 = st.columns(2)
        with col2_dl1:
            st.download_button("📥 CSV optimizados", df_final.to_csv(index=False), "listings_optimizados.csv", "text/csv")
        with col2_dl2:
            st.download_button("📥 Excel optimizados", exportar_excel(df_final), "listings_optimizados.xlsx")