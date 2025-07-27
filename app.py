import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Juego de Apuestas Deportivas", layout="centered")
st.title("🎲 Juego de Apuestas Deportivas")

# --- Inicialización del estado ---
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
    st.session_state.mejor_nota = 0
    st.session_state.jugar = False
    st.session_state.nombre = ""
    st.session_state.edad = 0

# --- Datos del usuario ---
if not st.session_state.jugar:
    st.subheader("👤 Ingresa tus datos para comenzar")
    with st.form("form_datos"):
        nombre = st.text_input("Nombre", placeholder="Tu nombre")
        edad = st.number_input("Edad", min_value=12, step=1)
        iniciar = st.form_submit_button("Iniciar juego")
        if iniciar and nombre.strip() != "":
            st.session_state.nombre = nombre
            st.session_state.edad = edad
            st.session_state.jugar = True
            st.rerun()

# --- Preguntas ---
preguntas = [
    {
        "pregunta": "¿Qué es el bankroll?",
        "opciones": ["Tu equipo favorito", "Dinero reservado para apostar", "Tipo de apuesta", "Casa de apuestas"],
        "respuesta": "Dinero reservado para apostar"
    },
    {
        "pregunta": "¿Qué representa una cuota 2.00?",
        "opciones": ["Ganarás el doble", "Solo puedes apostar 2$", "Es muy arriesgada", "Ninguna es correcta"],
        "respuesta": "Ganarás el doble"
    },
    {
        "pregunta": "¿Qué significa 'under 2.5 goles'?",
        "opciones": ["Que habrá más de 2 goles", "Que habrá menos de 3 goles", "Que un equipo hará 2 goles", "Ninguna"],
        "respuesta": "Que habrá menos de 3 goles"
    },
    {
        "pregunta": "¿Cuál es un buen consejo para principiantes?",
        "opciones": ["Apostar todo", "Seguir tu instinto", "Gestionar el bankroll", "Copiar a otros"],
        "respuesta": "Gestionar el bankroll"
    }
]

# --- Juego ---
if st.session_state.jugar and st.session_state.intentos < 3:
    with st.form("form_juego"):
        st.subheader(f"🧠 Preguntas para {st.session_state.nombre}, edad {st.session_state.edad}")
        respuestas_usuario = []
        for i, p in enumerate(preguntas):
            r = st.radio(f"{i+1}. {p['pregunta']}", p["opciones"], key=f"q{i}")
            respuestas_usuario.append(r)
        enviado = st.form_submit_button("Enviar respuestas")

        if enviado:
            correctas = 0
            for i, p in enumerate(preguntas):
                if respuestas_usuario[i] == p["respuesta"]:
                    correctas += 1
            nota = round((correctas / len(preguntas)) * 10, 2)
            st.success(f"✅ Obtuviste {correctas} de {len(preguntas)} respuestas correctas. Nota: {nota}/10")

            st.session_state.intentos += 1
            if nota > st.session_state.mejor_nota:
                st.session_state.mejor_nota = nota

            st.query_params(jugar="true")

# --- Resultado final ---
if st.session_state.intentos >= 3:
    st.warning("⚠️ Ya usaste los 3 intentos.")
    st.info(f"🎯 Tu mejor nota fue: **{st.session_state.mejor_nota}/10**")

    if st.button("🔁 Volver a jugar"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
