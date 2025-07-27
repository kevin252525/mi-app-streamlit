import streamlit as st

# Configuración inicial
st.set_page_config(page_title="Cuestionario Apuestas Deportivas", layout="centered")

# Colores y estilos
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; }
        .stButton>button {
            background-color: #0099ff;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #007acc;
        }
    </style>
""", unsafe_allow_html=True)

# Título del juego
st.title("🎲 Juego de Apuestas Deportivas")

# Estado inicial
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
if "mejor_nota" not in st.session_state:
    st.session_state.mejor_nota = 0
if "jugar" not in st.session_state:
    st.session_state.jugar = False

# Datos del usuario
if not st.session_state.jugar:
    st.subheader("👤 Ingresa tus datos para comenzar")
    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", min_value=0, max_value=100, step=1)

    if st.button("Iniciar juego"):
        if not nombre:
            st.warning("Por favor, ingresa tu nombre.")
        elif edad < 18:
            st.error("🚫 Debes tener al menos 18 años para jugar.")
        else:
            st.session_state.jugar = True
            st.session_state.nombre = nombre
            st.session_state.edad = edad
            st.experimental_rerun()

# Preguntas
if st.session_state.jugar and st.session_state.intentos < 3:
    preguntas = [
        {
            "pregunta": "¿Qué es una apuesta deportiva?",
            "opciones": ["Una predicción sin dinero", "Un juego de azar con dinero", "Una inversión garantizada", "Una actividad ilegal"],
            "respuesta": "Un juego de azar con dinero"
        },
        {
            "pregunta": "¿Qué significa 'cuota' en apuestas?",
            "opciones": ["El dinero apostado", "La probabilidad de ganar", "El pago potencial", "El tipo de apuesta"],
            "respuesta": "El pago potencial"
        },
        {
            "pregunta": "¿Qué representa el 'stake'?",
            "opciones": ["El tipo de apuesta", "La cantidad apostada", "La probabilidad de ganar", "El pago potencial"],
            "respuesta": "La cantidad apostada"
        },
        {
            "pregunta": "¿Qué tipo de apuesta es '1X2'?",
            "opciones": ["Ganar, empatar o perder", "Sólo ganar o perder", "Empate sí o no", "Dobles oportunidades"],
            "respuesta": "Ganar, empatar o perder"
        }
    ]

    st.markdown(f"#### Intento N° {st.session_state.intentos + 1}")
    puntaje = 0

    respuestas_usuario = []

    for i, p in enumerate(preguntas):
        st.write(f"**{p['pregunta']}**")
        seleccion = st.radio("Selecciona una opción:", p["opciones"], key=f"q_{i}")
        respuestas_usuario.append(seleccion)
        if seleccion == p["respuesta"]:
            puntaje += 1

    if st.button("Enviar respuestas"):
        nota = round((puntaje / len(preguntas)) * 10, 2)
        st.success(f"✅ Obtuviste {puntaje} de {len(preguntas)} respuestas correctas. Nota: {nota}/10")
