import streamlit as st

# Inicializar estados
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "edad" not in st.session_state:
    st.session_state.edad = 0
if "jugar" not in st.session_state:
    st.session_state.jugar = False
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
if "mejor_nota" not in st.session_state:
    st.session_state.mejor_nota = 0

st.title("🎲 Juego de Apuestas Deportivas")

# Paso 1: Datos personales
if not st.session_state.jugar:
    st.subheader("👤 Ingresa tus datos para comenzar")
    st.session_state.nombre = st.text_input("Nombre")
    st.session_state.edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
    if st.button("Iniciar juego"):
        if st.session_state.nombre.strip() == "":
            st.warning("Por favor ingresa tu nombre.")
        elif st.session_state.edad < 18:
            st.error("Debes tener al menos 18 años para jugar.")
        elif st.session_state.intentos >= 3:
            st.warning("Ya usaste los 3 intentos.")
        else:
            st.session_state.jugar = True
            st.query_params(jugar="true")  # ✅ sin experimental

# Paso 2: Juego
if st.session_state.jugar:
    st.subheader(f"📋 Preguntas para {st.session_state.nombre}")
    
    preguntas = [
        {
            "pregunta": "¿Qué es una apuesta deportiva?",
            "opciones": ["Un juego de mesa", "Una predicción sobre un evento deportivo", "Una lotería", "Una aplicación de ejercicio"],
            "respuesta": "Una predicción sobre un evento deportivo"
        },
        {
            "pregunta": "¿Qué significa 'cuota' en las apuestas?",
            "opciones": ["El valor que pagas por apostar", "La probabilidad de que ocurra un resultado", "Una multa", "Un impuesto deportivo"],
            "respuesta": "La probabilidad de que ocurra un resultado"
        },
        {
            "pregunta": "¿Qué pasa si apuestas con 'hándicap'?",
            "opciones": ["Juegas con ventaja o desventaja artificial", "No hay reglas", "Solo apuestas en vivo", "Se duplica tu apuesta"],
            "respuesta": "Juegas con ventaja o desventaja artificial"
        },
        {
            "pregunta": "¿Qué es el 'bankroll'?",
            "opciones": ["El tipo de apuesta", "Tu presupuesto disponible para apostar", "La aplicación de apuestas", "La cuenta bancaria del jugador"],
            "respuesta": "Tu presupuesto disponible para apostar"
        }
    ]

    respuestas_usuario = []
    for i, p in enumerate(preguntas):
        st.markdown(f"**{i+1}. {p['pregunta']}**")
        respuesta = st.radio("Selecciona una opción:", p["opciones"], key=i)
        respuestas_usuario.append(respuesta)
        st.write("")

    enviado = st.button("Enviar respuestas")

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

        if st.session_state.intentos >= 3:
            st.warning("📛 Ya usaste los 3 intentos.")
            st.info(f"🎯 Tu mejor nota fue: **{st.session_state.mejor_nota}/10**")
        else:
            if st.button("🔄 Volver a jugar"):
                st.session_state.jugar = False
                st.query_params(jugar="false")  # reset

# Mostrar botón reset si ya acabó todo
if st.session_state.intentos >= 3:
    if st.button("🔁 Reiniciar juego completamente"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
