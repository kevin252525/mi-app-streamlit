import streamlit as st

# --- Configuración inicial ---
st.set_page_config(page_title="Juego de Apuestas Deportivas", layout="centered")

st.title("🎲 Juego de Apuestas Deportivas")

# --- Inicializar estados ---
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
    st.session_state.mejor_nota = 0
    st.session_state.nombre = ""
    st.session_state.edad = ""
    st.session_state.jugando = False

# --- Formulario de inicio ---
if not st.session_state.jugando:
    with st.form("datos_usuario"):
        st.subheader("👤 Ingresa tus datos para comenzar")
        nombre = st.text_input("Nombre")
        edad = st.number_input("Edad", min_value=12, max_value=120, step=1)
        iniciar = st.form_submit_button("Iniciar juego")

        if iniciar and nombre.strip() != "":
            st.session_state.nombre = nombre
            st.session_state.edad = edad
            st.session_state.jugando = True
            st.experimental_rerun()
        elif iniciar:
            st.warning("Por favor ingresa tu nombre.")

# --- Preguntas (opción múltiple) ---
preguntas = [
    {
        "pregunta": "¿Qué es el bankroll?",
        "opciones": ["Tu equipo favorito", "Dinero reservado para apostar", "Tipo de apuesta", "Nombre de una casa de apuestas"],
        "respuesta": "Dinero reservado para apostar"
    },
    {
        "pregunta": "¿Qué representa una cuota 2.00?",
        "opciones": ["Que ganarás el doble", "Que es poco probable", "Que solo se puede apostar 2$", "Ninguna es correcta"],
        "respuesta": "Que ganarás el doble"
    },
    {
        "pregunta": "¿Qué es una apuesta en vivo?",
        "opciones": ["Una apuesta que haces mientras el evento ocurre", "Una apuesta al día siguiente", "Una apuesta cancelada", "Una apuesta sobre música en vivo"],
        "respuesta": "Una apuesta que haces mientras el evento ocurre"
    },
    {
        "pregunta": "¿Cuál es el riesgo de apostar todo tu bankroll?",
        "opciones": ["Duplicar siempre", "No hay riesgo", "Perder todo tu dinero", "Recibir bonos"],
        "respuesta": "Perder todo tu dinero"
    }
]

# --- Juego principal ---
if st.session_state.jugando and st.session_state.intentos < 3:
    with st.form("juego"):
        st.subheader(f"Jugador: {st.session_state.nombre} | Edad: {st.session_state.edad}")
        st.info(f"Intento actual: {st.session_state.intentos + 1}/3")

        respuestas_usuario = []
        puntaje = 0

        for i, p in enumerate(preguntas):
            st.write(f"**Pregunta {i+1}: {p['pregunta']}**")
            respuesta = st.radio("Selecciona una opción:", p["opciones"], key=f"preg_{i}")
            respuestas_usuario.append(respuesta)

        enviado = st.form_submit_button("Enviar respuestas")

        if enviado:
            for i, p in enumerate(preguntas):
                if respuestas_usuario[i] == p["respuesta"]:
                    puntaje += 1

            nota = round((puntaje / len(preguntas)) * 10, 2)
            st.success(f"Obtuviste {puntaje} de {len(preguntas)} respuestas correctas. Nota: {nota}/10")

            if nota > st.session_state.mejor_nota:
                st.session_state.mejor_nota = nota

            st.session_state.intentos += 1
            st.experimental_rerun()

# --- Final del juego ---
if st.session_state.jugando and st.session_state.intentos >= 3:
    st.warning("🔁 Ya usaste los 3 intentos.")
    st.info(f"🎯 Tu mejor nota fue: **{st.session_state.mejor_nota}/10**")

    if st.button("Volver a jugar"):
        st.session_state.intentos = 0
        st.session_state.mejor_nota = 0
        st.session_state.jugando = False
        st.experimental_rerun()

