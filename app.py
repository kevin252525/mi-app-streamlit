import streamlit as st

# --- Configuración inicial ---
st.set_page_config(page_title="Juego de Apuestas Deportivas", layout="centered")
st.title("🎲 Juego de Apuestas Deportivas")
st.write("Pon a prueba tus conocimientos. Tienes hasta 3 intentos. Se guardará tu mejor puntuación.")

# --- Preguntas del cuestionario ---
preguntas = [
    {
        "tipo": "opcion",
        "pregunta": "¿Qué es el bankroll?",
        "opciones": ["Tu equipo favorito", "Dinero reservado para apostar", "Tipo de apuesta", "Nombre de una casa de apuestas"],
        "respuesta": "Dinero reservado para apostar"
    },
    {
        "tipo": "opcion",
        "pregunta": "¿Qué representa una cuota 2.00?",
        "opciones": ["Que ganarás el doble", "Que es poco probable", "Que solo se puede apostar 2$", "Ninguna es correcta"],
        "respuesta": "Que ganarás el doble"
    },
    {
        "tipo": "completar",
        "pregunta": "Escribe cómo se llama a una apuesta que incluye dos o más selecciones combinadas.",
        "respuesta": "parlay"
    }
]

# --- Intentos y estado ---
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
    st.session_state.mejor_nota = 0

# --- Formulario del intento ---
if st.session_state.intentos < 3:
    with st.form("juego_apuestas"):
        puntaje = 0
        respuestas_usuario = []

        for i, p in enumerate(preguntas):
            st.subheader(f"Pregunta {i + 1}")
            if p["tipo"] == "opcion":
                respuesta = st.radio(p["pregunta"], p["opciones"], key=f"preg_{i}")
            else:
                respuesta = st.text_input(p["pregunta"], key=f"preg_{i}")
            respuestas_usuario.append(respuesta)

        enviado = st.form_submit_button("Enviar respuestas")

        if enviado:
            for i, p in enumerate(preguntas):
                correcta = p["respuesta"].strip().lower()
                respuesta_usuario = respuestas_usuario[i].strip().lower()
                if respuesta_usuario == correcta:
                    puntaje += 1

            nota = round((puntaje / len(preguntas)) * 10, 2)
            st.success(f"✅ Intento #{st.session_state.intentos + 1}: Obtuviste {puntaje}/{len(preguntas)} respuestas correctas. Nota: {nota}/10")

            if nota > st.session_state.mejor_nota:
                st.session_state.mejor_nota = nota

            st.session_state.intentos += 1

else:
    st.warning("Ya usaste los 3 intentos.")
    st.info(f"🎯 Tu mejor nota fue: **{st.session_state.mejor_nota}/10**")
