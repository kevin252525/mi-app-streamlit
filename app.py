import streamlit as st

# --- Estilos para botones verdes ---
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

st.set_page_config(page_title="Cuestionario Apuestas Deportivas", layout="centered")
st.title("🎲 Cuestionario Diagnóstico - Apuestas Deportivas")

# --- sesión (session_state) ---
ss = st.session_state

# inicializar claves
for key, default in [
    ("nombre",""),
    ("edad",18),
    ("jugando", False),
    ("intentos", 0),
    ("mejor_nota", 0.0),
    ("nota_actual", 0.0),
    ("show_q", False),
    ("show_decision", False),
    ("final", False)
]:
    if key not in ss:
        ss[key] = default

# --- Paso 1: ingreso datos ---
if not ss.jugando and not ss.final and ss.intentos < 3:
    st.subheader("👤 Ingresa tus datos (≥18 años)")
    ss.nombre = st.text_input("Nombre", value=ss.nombre)
    ss.edad   = st.number_input("Edad", min_value=1, max_value=120, value=ss.edad, step=1)
    if st.button("Iniciar juego"):
        if ss.nombre.strip()=="":
            st.warning("❗ Por favor ingresa tu nombre.")
        elif ss.edad < 18:
            st.error("🚫 Debes tener al menos 18 años.")
        else:
            ss.jugando = True
            ss.show_q = True
            ss.show_decision = False
            st.experimental_rerun()

# --- Tus 20 preguntas (ejemplo con 2, repite hasta 20) ---
preguntas = [
    {"pregunta":"¿Qué es una apuesta deportiva?",
     "opciones":["Predicción sin dinero","Juego de azar con dinero","Inversión garantizada","Actividad ilegal"],
     "respuesta":"Juego de azar con dinero"},
    {"pregunta":"¿Qué significa 'cuota' en apuestas?",
     "opciones":["Dinero apostado","Probabilidad de ganar","Pago potencial","Tipo de apuesta"],
     "respuesta":"Pago potencial"},
    # ... agrega aquí las 18 restantes ...
]

# --- Paso 2: mostrar cuestionario ---
if ss.jugando and ss.show_q and ss.intentos < 3:
    with st.form("quiz_form"):
        st.subheader(f"🏅 Intento {ss.intentos+1} de 3 — {ss.nombre}")
        respuestas = []
        for i, p in enumerate(preguntas):
            st.markdown(f"**{i+1}. {p['pregunta']}**")
            opciones = ["-- Selecciona una opción --"] + p["opciones"]
            sel = st.radio("", opciones, index=0, key=f"q{i}")
            respuestas.append(sel)
        enviar = st.form_submit_button("Enviar respuestas")

    if enviar:
        if any(r == "-- Selecciona una opción --" for r in respuestas):
            st.error("❗ Debes responder todas las preguntas antes de enviar.")
        else:
            # calcular nota
            aciertos = sum(1 for i,p in enumerate(preguntas) if respuestas[i] == p["respuesta"])
            nota = round((aciertos/len(preguntas))*10,2)
            ss.nota_actual = nota
            ss.mejor_nota = max(ss.mejor_nota, nota)
            ss.intentos += 1
            ss.show_q = False
            ss.show_decision = True
            # si se acaba 3º intento, marcaremos final
            if ss.intentos >= 3:
                ss.final = True
            st.experimental_rerun()

# --- Paso 3: mostrar nota y decidir si otro intento ---
if ss.show_decision:
    st.info(f"🎯 Nota del intento: **{ss.nota_actual}/10**")
    st.success(f"⭐ Mejor nota hasta ahora: **{ss.mejor_nota}/10**")

    # Si ya agotó, mostramos directamente pantalla principal
    if ss.final:
        if st.button("🏠 Pantalla principal"):
            for k in list(ss.keys()):
                del ss[k]
            st.experimental_rerun()
    else:
        # Dos botones para decidir
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Sí, otro intento"):
                # limpiar respuestas previas
                for i in range(len(preguntas)):
                    key = f"q{i}"
                    if key in ss: del ss[key]
                ss.show_q = True
                ss.show_decision = False
                st.experimental_rerun()
        with col2:
            if st.button("❌ No, no quiero otro intento"):
                ss.final = True
                st.experimental_rerun()

# --- Paso 4: pantalla final (tras "No" o 3 intentos) ---
if ss.final and not ss.show_q and not ss.show_decision:
    st.info(f"🏁 Tu nota final es: **{ss.mejor_nota}/10**")
    if st.button("🏠 Pantalla principal"):
        for k in list(ss.keys()):
            del ss[k]
        st.experimental_rerun()
