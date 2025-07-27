import streamlit as st
from streamlit_extras.colored_header import colored_header

st.set_page_config(page_title="Cuestionario Apuestas", layout="centered")

# TÍTULO
st.markdown("""
    <h1 style='text-align: center; color: #4B0082;'>🎲 Cuestionario Diagnóstico - Apuestas Deportivas</h1>
""", unsafe_allow_html=True)

# DATOS DE USUARIO
with st.form("form_usuario"):
    colored_header("Ingresa tus datos para comenzar", description="", color_name="violet-60")
    nombre = st.text_input("👤 Nombre")
    edad = st.number_input("🎂 Edad", min_value=0, max_value=120, step=1)
    empezar = st.form_submit_button("Iniciar juego")

if "jugar" not in st.session_state:
    st.session_state.jugar = False
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
if "mejor_puntaje" not in st.session_state:
    st.session_state.mejor_puntaje = 0

# VERIFICAR DATOS
if empezar:
    if not nombre:
        st.warning("⚠️ Debes ingresar un nombre.")
    elif edad < 18:
        st.error("🚫 Debes tener al menos 18 años para jugar.")
    else:
        st.session_state.jugar = True
        st.session_state.intentos = 1

if st.session_state.jugar and st.session_state.intentos <= 3:

    preguntas = [
        # (Tu lista de 20 preguntas aquí con sus respuestas y opciones como diccionario)
    ]

    puntaje = 0
    st.subheader(f"Intento {st.session_state.intentos} de 3")

    for i, pregunta in enumerate(preguntas, 1):
        st.markdown(f"**Pregunta {i}:** {pregunta['pregunta']}")
        respuesta = st.radio("", pregunta["opciones"], key=f"pregunta_{i}_{st.session_state.intentos}")
        if respuesta == pregunta["respuesta"]:
            puntaje += 1

    if st.button("Enviar respuestas", key=f"boton_enviar_{st.session_state.intentos}"):
        st.success(f"🎉 Obtuviste {puntaje} de {len(preguntas)} puntos. Nota: {(puntaje/len(preguntas))*10:.1f}/10")
        if puntaje > st.session_state.mejor_puntaje:
            st.session_state.mejor_puntaje = puntaje

        if st.session_state.intentos < 3:
            if st.button("🔁 Realizar otro intento"):
                st.session_state.intentos += 1
                st.rerun()
        else:
            st.warning("😮 Ya usaste los 3 intentos.")
            st.info(f"🏆 Tu mejor nota fue: {st.session_state.mejor_puntaje * 10 / len(preguntas):.1f}/10")

elif st.session_state.intentos > 3:
    st.warning("😮 Ya usaste los 3 intentos.")
    st.info(f"🏆 Tu mejor nota fue: {st.session_state.mejor_puntaje * 10 / len(preguntas):.1f}/10")
