import streamlit as st

# --- CSS para botones coloreados ---
st.markdown("""
<style>
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5em 1em;
    border-radius: 0.5em;
    font-size: 1em;
    margin: 0.2em 0;
}
div.stButton > button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Cuestionario - Apuestas Deportivas", layout="centered")
st.title("🎲 Cuestionario Diagnóstico - Apuestas Deportivas")

ss = st.session_state

# --- Inicializar session state ---
for var, default in [
    ("nombre",""), ("edad",18),
    ("jugar",False), ("intentos",0),
    ("mejor_nota",0),
    ("mostrar_form",False), ("mostrar_resultado",False),
    ("nota_actual", 0)
]:
    if var not in ss:
        ss[var] = default

# --- Paso 1: ingreso de datos ---
if not ss.jugar and ss.intentos < 3 and not ss.mostrar_resultado:
    st.subheader("👤 Ingresa tus datos (≥18 años)")
    ss.nombre = st.text_input("Nombre", value=ss.nombre)
    ss.edad   = st.number_input("Edad", min_value=1, max_value=120, value=ss.edad, step=1)
    if st.button("Iniciar juego"):
        if ss.nombre.strip()=="":
            st.warning("❗ Por favor ingresa tu nombre.")
        elif ss.edad<18:
            st.error("🚫 Debes tener al menos 18 años.")
        else:
            ss.jugar = True
            ss.mostrar_form = True

# --- Definir preguntas (rellena con tus 20 preguntas) ---
preguntas = [
    {"pregunta":"¿Qué es una apuesta deportiva?",
     "opciones":["Predicción sin dinero","Juego de azar con dinero",
                 "Inversión garantizada","Actividad ilegal"],
     "respuesta":"Juego de azar con dinero"},
    {"pregunta":"¿Qué significa 'cuota' en apuestas?",
     "opciones":["Dinero apostado","Probabilidad de ganar",
                 "Pago potencial","Tipo de apuesta"],
     "respuesta":"Pago potencial"},
    # ... añade aquí las demás preguntas ...
]

# --- Paso 2: formulario de preguntas ---
if ss.jugar and ss.intentos < 3 and ss.mostrar_form:
    with st.form("form_cuestionario"):
        st.subheader(f"🏆 Intento {ss.intentos+1} de 3 — {ss.nombre}")
        respuestas = []
        for idx, p in enumerate(preguntas):
            st.markdown(f"**{idx+1}. {p['pregunta']}**")
            opciones = ["-- Selecciona una opción --"] + p["opciones"]
            sel = st.radio("", opciones, index=0, key=f"q{idx}")
            respuestas.append(sel)
        enviado = st.form_submit_button("Enviar respuestas")

    if enviado:
        if any(r=="-- Selecciona una opción --" for r in respuestas):
            st.error("❗ Debes responder todas las preguntas.")
        else:
            # Calcular nota
            correctas = sum(1 for i,p in enumerate(preguntas) if respuestas[i]==p["respuesta"])
            nota = round((correctas/len(preguntas))*10,2)
            ss.nota_actual = nota
            ss.intentos += 1
            ss.mejor_nota = max(ss.mejor_nota, nota)
            ss.mostrar_form = False
            ss.mostrar_resultado = True

# --- Paso 3: mostrar nota y decisión ---
if ss.mostrar_resultado:
    st.info(f"🎯 Nota del intento: **{ss.nota_actual}/10**")
    st.success(f"⭐ Mejor nota hasta ahora: **{ss.mejor_nota}/10**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Sí, otro intento"):
            # Limpiar respuestas previas
            for idx in range(len(preguntas)):
                key = f"q{idx}"
                if key in ss: del ss[key]
            ss.mostrar_form = True
            ss.mostrar_resultado = False
            st.rerun()
    with col2:
        if st.button("❌ No, no quiero otro intento"):
            # Mostrar nota final y botón principal
            ss.mostrar_form = False
            ss.jugar = False

# --- Paso 4: pantalla principal tras "No" ---
if not ss.jugar and ss.mostrar_resultado:
    st.info(f"🏁 Tu nota final es: **{ss.mejor_nota}/10**")
    if st.button("🏠 Pantalla principal"):
        for k in list(ss.keys()):
            del ss[k]
        st.rerun()

# --- Paso 5: si agotó intentos ---
if ss.intentos >= 3 and ss.mostrar_form==False and ss.mostrar_resultado==False:
    ss.mostrar_resultado = True
    st.warning("📛 Has usado los 3 intentos.")
    st.experimental_rerun()
