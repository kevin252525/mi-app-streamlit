import streamlit as st
from streamlit_extras.stylable_container import stylable_container  # Asegúrate de tener instalado el paquete

st.set_page_config(page_title="Cuestionario Apuestas", layout="centered")

# Estilos CSS para botones
boton_estilo = """
    <style>
    div.stButton > button:first-child {
        background-color: #0072C6;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
    }
    </style>
"""
st.markdown(boton_estilo, unsafe_allow_html=True)

# ---------- Inicializar sesión ----------
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "edad" not in st.session_state:
    st.session_state.edad = 0
if "intentos" not in st.session_state:
    st.session_state.intentos = 0
if "mejor_nota" not in st.session_state:
    st.session_state.mejor_nota = 0

# ---------- Formulario de entrada ----------
st.title("🎯 Cuestionario Diagnóstico - Apuestas Deportivas")
st.subheader("🔑 Ingresa tus datos para comenzar")
nombre = st.text_input("Nombre")
edad = st.number_input("Edad", min_value=0, step=1)

if st.button("Iniciar cuestionario"):
    if edad < 18:
        st.warning("🚫 Debes tener al menos 18 años para participar.")
        st.stop()
    else:
        st.session_state.nombre = nombre
        st.session_state.edad = edad
        st.session_state.intentos += 1
        st.experimental_rerun()

# ---------- Mostrar cuestionario solo si ya ingresó ----------
if st.session_state.nombre and st.session_state.edad >= 18 and st.session_state.intentos <= 3:

    preguntas = [
        {"pregunta": "¿Qué es una apuesta deportiva?", "opciones": ["Una predicción sin dinero", "Un juego de azar con dinero", "Una inversión garantizada", "Una actividad ilegal"], "respuesta": "Un juego de azar con dinero"},
        {"pregunta": "¿Qué significa 'cuota' en apuestas?", "opciones": ["El dinero apostado", "La probabilidad de ganar", "El pago potencial", "El tipo de apuesta"], "respuesta": "El pago potencial"},
        {"pregunta": "¿Qué representa el 'stake'?", "opciones": ["El tipo de apuesta", "La cantidad apostada", "La probabilidad de ganar", "El pago potencial"], "respuesta": "La cantidad apostada"},
        {"pregunta": "¿Qué tipo de apuesta es '1X2'?", "opciones": ["Ganar, empatar o perder", "Sólo ganar o perder", "Empate sí o no", "Dobles oportunidades"], "respuesta": "Ganar, empatar o perder"},
        {"pregunta": "¿Qué es una cuota decimal?", "opciones": ["Un formato europeo", "Un formato americano", "Un tipo de apuesta", "Un valor fijo"], "respuesta": "Un formato europeo"},
        {"pregunta": "¿Qué es una cuota fraccionaria?", "opciones": ["Un formato europeo", "Un formato británico", "Un tipo de apuesta", "Un pago fijo"], "respuesta": "Un formato británico"},
        {"pregunta": "¿Qué indica una cuota americana?", "opciones": ["La probabilidad de empate", "El pago potencial", "El equipo favorito o no", "El tipo de deporte"], "respuesta": "El equipo favorito o no"},
        {"pregunta": "¿Qué es el valor esperado (EV)?", "opciones": ["La ganancia segura", "La probabilidad media", "El beneficio promedio a largo plazo", "La apuesta mínima"], "respuesta": "El beneficio promedio a largo plazo"},
        {"pregunta": "¿Qué es bankroll?", "opciones": ["El total de apuestas hechas", "El dinero disponible para apostar", "El tipo de apuesta", "La cuota mínima"], "respuesta": "El dinero disponible para apostar"},
        {"pregunta": "¿Qué significa 'doble oportunidad'?", "opciones": ["Apostar en dos eventos diferentes", "Apostar a dos resultados en el mismo partido", "Apostar doble cantidad", "Apostar al ganador del torneo"], "respuesta": "Apostar a dos resultados en el mismo partido"},
        {"pregunta": "¿Qué es una apuesta 'Draw No Bet' (DNB)?", "opciones": ["Apuesta que gana con empate", "Apuesta que anula si hay empate", "Apuesta a ganador claro", "Apuesta a empate"], "respuesta": "Apuesta que anula si hay empate"},
        {"pregunta": "¿Qué significa el término 'mercado' en apuestas?", "opciones": ["Lugar físico para apostar", "Tipo de apuesta disponible", "Cantidad mínima para apostar", "Cuota mínima"], "respuesta": "Tipo de apuesta disponible"},
        {"pregunta": "¿Por qué es importante la gestión del bankroll?", "opciones": ["Para apostar sin límites", "Para evitar perder todo el dinero", "Para ganar siempre", "Para apostar en varios deportes"], "respuesta": "Para evitar perder todo el dinero"},
        {"pregunta": "¿Qué es 'tilt' en apuestas?", "opciones": ["Una estrategia", "Un error emocional", "Una apuesta segura", "Un tipo de cuota"], "respuesta": "Un error emocional"},
        {"pregunta": "¿Qué significa apostar responsablemente?", "opciones": ["Apostar sin control", "Conocer límites y riesgos", "Apostar solo en casa", "Apostar siempre lo máximo"], "respuesta": "Conocer límites y riesgos"},
        {"pregunta": "¿Qué es una apuesta combinada?", "opciones": ["Una apuesta múltiple con varios eventos", "Una apuesta a ganador y empate", "Una apuesta a doble oportunidad", "Una apuesta sin cuota"], "respuesta": "Una apuesta múltiple con varios eventos"},
        {"pregunta": "¿Qué es la cuota implícita?", "opciones": ["La probabilidad calculada a partir de la cuota", "La cuota más baja", "La apuesta mínima", "El pago seguro"], "respuesta": "La probabilidad calculada a partir de la cuota"},
        {"pregunta": "¿Qué es un 'mercado de apuestas'?", "opciones": ["El lugar donde se hacen las apuestas", "El conjunto de opciones disponibles para apostar", "La cantidad apostada", "El pago recibido"], "respuesta": "El conjunto de opciones disponibles para apostar"},
        {"pregunta": "¿Qué es la cuota más alta?", "opciones": ["La que paga menos", "La que paga más", "La cuota mínima", "La cuota media"], "respuesta": "La que paga más"},
        {"pregunta": "¿Por qué es importante comparar cuotas?", "opciones": ["Para apostar en menos partidos", "Para maximizar ganancias potenciales", "Para apostar menos dinero", "Para apostar sin riesgo"], "respuesta": "Para maximizar ganancias potenciales"}
    ]

    puntaje = 0
    for i, pregunta in enumerate(preguntas, 1):
        st.write(f"**Pregunta {i}:** {pregunta['pregunta']}")
        seleccion = st.radio("", pregunta['opciones'], key=f"q_{i}")
        if seleccion == pregunta['respuesta']:
            puntaje += 1

    if st.button("Enviar respuestas"):
        nota = round((puntaje / len(preguntas)) * 10, 1)
        st.success(f"✅ Obtuviste {puntaje} de {len(preguntas)} respuestas correctas. Nota: {nota}/10")
        if nota > st.session_state.mejor_nota:
            st.session_state.mejor_nota = nota

        if st.session_state.intentos < 3:
            if st.button("🔁 Realizar otro intento"):
                st.experimental_rerun()
        else:
            st.warning("⚠️ Ya usaste los 3 intentos.")
            st.info(f"Tu mejor nota fue: **{st.session_state.mejor_nota}/10**")

elif st.session_state.intentos >= 3:
    st.warning("⚠️ Ya usaste los 3 intentos permitidos.")
    st.info(f"Tu mejor nota fue: **{st.session_state.mejor_nota}/10**")
