import streamlit as st

# ================================================
# Cambios de redacción y estilo formal aplicados:
# 1. Título: “🎲 Cuestionario Diagnóstico” → “🎲 Cuestionario Diagnóstico de Apuestas Deportivas”
# 2. Subtítulo: “Apuestas Deportivas” → “Compruebe sus conocimientos”
# 3. Formulario de datos:
#    • “Ingresa tus datos” → “Por favor, ingrese sus datos (≥18 años)”
#    • “Nombre” → “Nombre completo” (placeholder: “Ingrese su nombre”)
#    • Botón “Iniciar juego” → “🟢 Iniciar cuestionario”
# 4. Validaciones:
#    • “Debes ingresar tu nombre.” → “Por favor, ingrese su nombre.”
#    • “Debes tener al menos 18 años.” → “Debe tener al menos 18 años para continuar.”
# 5. Placeholder de opciones:
#    • “-- Seleccione una opción --” (uso de “usted”)
# 6. Botones de decisión:
#    • “🔄 Sí, otro intento”
#    • “❌ No, deseo finalizar”
# 7. Resultados:
#    • “Nota del intento” → “Nota de este intento”
#    • “Mejor nota hasta ahora” → “Mejor nota obtenida”
#    • Botón “Volver al inicio”
# ================================================

# --- CSS personalizado ---
st.markdown("""
<style>
/* … (CSS igual que antes) … */
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎲 Cuestionario de Apuestas Deportivas", layout="centered")

# === Títulos con redacción formal ===
st.markdown("<h1 style='text-align:center;'>🎲 Cuestionario Diagnóstico de Apuestas Deportivas</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>Compruebe sus conocimientos</h2>", unsafe_allow_html=True)

# === Session State ===
ss = st.session_state
for key, default in [
    ("nombre",""),
    ("edad",18),
    ("jugando",False),
    ("intentos",0),
    ("mejor_nota",0.0),
    ("nota_actual",0.0),
    ("show_q",False),
    ("show_decision",False),
    ("final",False),
]:
    if key not in ss:
        ss[key] = default

# === 1) Formulario de datos con texto formal ===
if not ss.jugando and not ss.final and ss.intentos < 3:
    with st.form("login_form"):
        st.subheader("👤 Por favor, ingrese sus datos (≥18 años)")
        nombre = st.text_input("Nombre completo", ss.nombre, placeholder="Ingrese su nombre")
        edad   = st.number_input("Edad", min_value=1, max_value=120, value=ss.edad, step=1)
        iniciar = st.form_submit_button("🟢 Iniciar cuestionario")
    if iniciar:
        if not nombre.strip():
            st.warning("❗ Por favor, ingrese su nombre.")
        elif edad < 18:
            st.error("🚫 Debe tener al menos 18 años para continuar.")
        else:
            ss.nombre = nombre
            ss.edad   = edad
            ss.jugando = True
            ss.show_q  = True
            st.rerun()

# === Preguntas (extienda hasta 20) ===
preguntas = [
    {"pregunta":"¿Qué es una apuesta deportiva?",
     "opciones":["Predicción sin dinero","Juego de azar con dinero","Inversión garantizada","Actividad ilegal"],
     "respuesta":"Juego de azar con dinero"},
    {"pregunta":"¿Qué significa 'cuota' en apuestas?",
     "opciones":["Dinero apostado","Probabilidad de ganar","Pago potencial","Tipo de apuesta"],
     "respuesta":"Pago potencial"},
    # … resto de preguntas …
]

# === 2) Cuestionario ===
if ss.jugando and ss.show_q and ss.intentos < 3:
    with st.form("quiz_form"):
        st.markdown(
            f"<div class='pregunta-card'><h3>🏅 Intento {ss.intentos+1} de 3 — {ss.nombre}</h3></div>",
            unsafe_allow_html=True
        )
        respuestas = []
        for i, p in enumerate(preguntas):
            st.markdown(
                f"<div class='pregunta-card'>🎯 <strong>{i+1}. {p['pregunta']}</strong></div>",
                unsafe_allow_html=True
            )
            opciones = ["-- Seleccione una opción --"] + p["opciones"]
            sel = st.radio("", opciones, index=0, key=f"q{i}")
            respuestas.append(sel)
        enviar = st.form_submit_button("💥 Enviar respuestas")
    if enviar:
        if any(r == "-- Seleccione una opción --" for r in respuestas):
            st.error("❗ Por favor, responda todas las preguntas antes de continuar.")
        else:
            aciertos = sum(1 for idx, p in enumerate(preguntas) if respuestas[idx] == p["respuesta"])
            nota = round((aciertos / len(preguntas)) * 10, 2)
            ss.nota_actual = nota
            ss.mejor_nota  = max(ss.mejor_nota, nota)
            ss.intentos   += 1
            ss.show_q      = False
            ss.show_decision = True
            if ss.intentos >= 3:
                ss.final = True
            st.rerun()

# === 3) Mostrar nota y botones formales ===
if ss.show_decision:
    st.info(f"🎯 Nota de este intento: **{ss.nota_actual}/10**")
    st.success(f"⭐ Mejor nota obtenida: **{ss.mejor_nota}/10**")
    if ss.final:
        if st.button("🏠 Volver al inicio"):
            for k in list(ss.keys()):
                del ss[k]
            st.rerun()
    else:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄 Sí, otro intento"):
                for idx in range(len(preguntas)):
                    key = f"q{idx}"
                    if key in ss: del ss[key]
                ss.show_q       = True
                ss.show_decision = False
                st.rerun()
        with c2:
            if st.button("❌ No, deseo finalizar"):
                ss.final = True
                st.rerun()

# === 4) Pantalla final formal ===
if ss.final and not ss.show_q and not ss.show_decision:
    st.info(f"🏁 Nota final: **{ss.mejor_nota}/10**")
    if st.button("🏠 Volver al inicio"):
        for k in list(ss.keys()): del ss[k]
        st.rerun()
