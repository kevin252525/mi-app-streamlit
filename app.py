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

# --- Configuración de la página ---
st.set_page_config(page_title="Cuestionario - Apuestas Deportivas", layout="centered")
st.title("🎲 Cuestionario Diagnóstico - Apuestas Deportivas")

# --- Estado de la sesión ---
ss = st.session_state
if "nombre" not in ss:
    ss.nombre = ""
if "edad" not in ss:
    ss.edad = 0
if "jugar" not in ss:
    ss.jugar = False
if "intentos" not in ss:
    ss.intentos = 0
if "mejor_nota" not in ss:
    ss.mejor_nota = 0
if "mostrar_form" not in ss:
    ss.mostrar_form = False
if "mostrar_resultado" not in ss:
    ss.mostrar_resultado = False

# --- Paso 1: ingreso de datos ---
if not ss.jugar and ss.intentos < 3:
    st.subheader("👤 Ingresa tus datos para comenzar")
    ss.nombre = st.text_input("Nombre", value=ss.nombre)
    ss.edad = st.number_input("Edad", min_value=1, max_value=120, step=1, value=ss.edad)
    if st.button("Iniciar juego"):
        if ss.nombre.strip() == "":
            st.warning("❗ Por favor ingresa tu nombre.")
        elif ss.edad < 18:
            st.error("🚫 Debes tener al menos 18 años para participar.")
        else:
            ss.jugar = True
            ss.mostrar_form = True
            ss.mostrar_resultado = False
            st.experimental_rerun()

# --- Definición de preguntas ---
preguntas = [
    {"pregunta": "¿Qué es una apuesta deportiva?",
     "opciones": ["Predicción sin dinero","Juego de azar con dinero","Inversión garantizada","Actividad ilegal"],
     "respuesta": "Juego de azar con dinero"},
    {"pregunta": "¿Qué significa 'cuota' en apuestas?",
     "opciones": ["Dinero apostado","Probabilidad de ganar","Pago potencial","Tipo de apuesta"],
     "respuesta": "Pago potencial"},
    {"pregunta": "¿Qué representa el 'stake'?",
     "opciones": ["Tipo de apuesta","Cantidad apostada","Probabilidad de ganar","Pago potencial"],
     "respuesta": "Cantidad apostada"},
    {"pregunta": "¿Qué tipo de apuesta es '1X2'?",
     "opciones": ["Ganar, empatar o perder","Solo ganar o perder","Empate sí o no","Dobles oportunidades"],
     "respuesta": "Ganar, empatar o perder"},
    {"pregunta": "¿Qué es una cuota decimal?",
     "opciones": ["Formato europeo","Formato americano","Tipo de apuesta","Valor fijo"],
     "respuesta": "Formato europeo"},
    {"pregunta": "¿Qué es una cuota fraccionaria?",
     "opciones": ["Formato europeo","Formato británico","Tipo de apuesta","Pago fijo"],
     "respuesta": "Formato británico"},
    {"pregunta": "¿Qué indica una cuota americana?",
     "opciones": ["Prob. de empate","Pago potencial","Equipo favorito o no","Tipo de deporte"],
     "respuesta": "Equipo favorito o no"},
    {"pregunta": "¿Qué es el valor esperado (EV)?",
     "opciones": ["Ganancia segura","Probabilidad media","Beneficio promedio a largo plazo","Apuesta mínima"],
     "respuesta": "Beneficio promedio a largo plazo"},
    {"pregunta": "¿Qué es bankroll?",
     "opciones": ["Total de apuestas","Dinero disponible para apostar","Tipo de apuesta","Cuota mínima"],
     "respuesta": "Dinero disponible para apostar"},
    {"pregunta": "¿Qué significa 'doble oportunidad'?",
     "opciones": ["Dos eventos distintos","Dos resultados en el mismo partido","Doble cantidad","Ganador del torneo"],
     "respuesta": "Dos resultados en el mismo partido"},
    {"pregunta": "¿Qué es 'Draw No Bet' (DNB)?",
     "opciones": ["Gana con empate","Anula si hay empate","Ganador claro","Empate"],
     "respuesta": "Anula si hay empate"},
    {"pregunta": "¿Qué significa 'mercado' en apuestas?",
     "opciones": ["Lugar físico","Opciones disponibles","Mínimo a apostar","Cuota mínima"],
     "respuesta": "Opciones disponibles"},
    {"pregunta": "¿Por qué es importante la gestión del bankroll?",
     "opciones": ["Para apostar sin límites","Para no perder todo el dinero","Para ganar siempre","Para varios deportes"],
     "respuesta": "Para no perder todo el dinero"},
    {"pregunta": "¿Qué es 'tilt' en apuestas?",
     "opciones": ["Estrategia","Error emocional","Apuesta segura","Tipo de cuota"],
     "respuesta": "Error emocional"},
    {"pregunta": "¿Qué significa apostar responsablemente?",
     "opciones": ["Sin control","Conocer límites y riesgos","Solo en casa","Siempre al máximo"],
     "respuesta": "Conocer límites y riesgos"},
    {"pregunta": "¿Qué es una apuesta combinada?",
     "opciones": ["Múltiple con varios eventos","Ganar o empatar","Doble oportunidad","Sin cuota"],
     "respuesta": "Múltiple con varios eventos"},
    {"pregunta": "¿Qué es la cuota implícita?",
     "opciones": ["Probabilidad desde la cuota","Cuota más baja","Apuesta mínima","Pago seguro"],
     "respuesta": "Probabilidad desde la cuota"},
    {"pregunta": "¿Qué es un mercado de apuestas?",
     "opciones": ["Lugar de apuestas","Conjunto de opciones","Cantidad apostada","Pago recibido"],
     "respuesta": "Conjunto de opciones"},
    {"pregunta": "¿Qué es la cuota más alta?",
     "opciones": ["Paga menos","Paga más","Cuota mínima","Cuota media"],
     "respuesta": "Paga más"},
    {"pregunta": "¿Por qué comparar cuotas?",
     "opciones": ["Menos partidos","Maximizar ganancias","Menos dinero","Sin riesgo"],
     "respuesta": "Maximizar ganancias"}
]

# --- Paso 2: Mostrar formulario de preguntas ---
if ss.jugar and ss.intentos < 3 and ss.mostrar_form:
    with st.form("form_cuestionario"):
        puntaje = 0
        respuestas = []
        for idx, p in enumerate(preguntas):
            st.markdown(f"**{idx+1}. {p['pregunta']}**")
            r = st.radio("", p["opciones"], key=f"p{idx}")
            respuestas.append(r)
        enviar = st.form_submit_button("Enviar respuestas")
        if enviar:
            for idx, p in enumerate(preguntas):
                if respuestas[idx] == p["respuesta"]:
                    puntaje += 1
            nota = round((puntaje / len(preguntas)) * 10, 2)
            st.session_state.intentos += 1
            if nota > ss.mejor_nota:
                ss.mejor_nota = nota
            ss.mostrar_form = False
            ss.mostrar_resultado = True
            st.success(f"✅ Intento {ss.intentos}: obtuviste {puntaje}/{len(preguntas)} respuestas correctas. Nota: {nota}/10")
            if ss.intentos < 3:
                st.info("¿Quieres realizar otro intento?")
                if st.button("🔄 Quiero realizar otro intento"):
                    ss.mostrar_form = True
                    ss.mostrar_resultado = False
                    st.experimental_rerun()

# --- Paso 3: Resultado final y reinicio ---
if ss.intentos >= 3 and ss.mostrar_resultado:
    st.warning("📛 Ya usaste los 3 intentos.")
    st.info(f"🎯 Tu mejor nota fue: **{ss.mejor_nota}/10**")
    if st.button("🔁 Reiniciar juego completamente"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.experimental_rerun()
