import streamlit as st

# === CSS personalizado ===
st.markdown("""
<style>
/* Fondo suave */
section.main {
  background: #f0f4f8;
  color: #0a0a0a;
  font-weight: bold;
}

/* Tarjeta de pregunta */
.pregunta-card {
  background-color: #ffffff;
  border: 2px solid #4caf50;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Inputs amarillo pastel */
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
  background-color: #fff9c4;
  color: #333;
  border: 1px solid #fdd835;
  border-radius: 5px;
  padding: 0.5em;
  font-weight: bold;
}

/* Placeholder negrita */
.stTextInput>div>div>input::placeholder {
  color: #666;
  font-weight: bold;
}

/* Radios verde pastel */
.stRadio > div > label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.stRadio > div > label > input[type="radio"] + span:before {
  border: 2px solid #66bb6a;
  background-color: #e8f5e9;
}
.stRadio > div > label > input[type="radio"]:checked + span:after {
  background-color: #66bb6a;
  border-color: #66bb6a;
}

/* Botones verde pastel */
div.stButton > button {
  background-color: #a5d6a7;
  color: #1b5e20;
  border: 2px solid #66bb6a;
  padding: 0.6em 1.2em;
  border-radius: 0.5em;
  font-weight: bold;
  font-size: 1em;
  margin: 0.3em 0;
  width: 100%;
}
div.stButton > button:hover {
  background-color: #81c784;
  border-color: #4caf50;
}

/* Encabezados naranja pastel */
h1, h2, h3 {
  color: #ffb74d;
  font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎲 Apuestas Deportivas", layout="centered")

# --- Títulos sin banner de imagen ---
st.markdown("<h1 style='text-align:center;'>🎲 Cuestionario Diagnóstico</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>Apuestas Deportivas</h2>", unsafe_allow_html=True)

# --- Session State ---
ss = st.session_state
for key, default in [
    ("nombre",""),
    ("edad",18),
    ("jugando",False),
    ("intentos",0),
    ("mejor_nota",0.0),
    ("nota_actual",0.0),
    ("show_q",False),
    ("show_decision",False),
    ("final",False),
]:
    if key not in ss:
        ss[key] = default

# --- 1) Formulario de Login ---
if not ss.jugando and not ss.final and ss.intentos < 3:
    with st.form("login_form"):
        st.subheader("👤 Ingresa tus datos (≥18 años)")
        nombre = st.text_input("Nombre", ss.nombre, placeholder="Tu nombre aquí")
        edad   = st.number_input("Edad", min_value=1, max_value=120, value=ss.edad, step=1)
        iniciar = st.form_submit_button("🟢 Iniciar juego")
    if iniciar:
        if nombre.strip() == "":
            st.warning("❗ Debes ingresar tu nombre.")
        elif edad < 18:
            st.error("🚫 Debes tener al menos 18 años.")
        else:
            ss.nombre = nombre
            ss.edad   = edad
            ss.jugando = True
            ss.show_q  = True
            st.rerun()

# --- Ejemplo de preguntas (extiende hasta 20) ---
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


# --- 2) Cuestionario ---
if ss.jugando and ss.show_q and ss.intentos < 3:
    with st.form("quiz_form"):
        st.markdown(
            f"<div class='pregunta-card'><h3>🏅 Intento {ss.intentos+1} de 3 — {ss.nombre}</h3></div>",
            unsafe_allow_html=True
        )
        respuestas = []
        for i, p in enumerate(preguntas):
            st.markdown(
                f"<div class='pregunta-card'>🎯 <strong>{i+1}. {p['pregunta']}</strong></div>",
                unsafe_allow_html=True
            )
            opts = ["-- Selecciona una opción --"] + p["opciones"]
            sel = st.radio("", opts, index=0, key=f"q{i}")
            respuestas.append(sel)
        enviar = st.form_submit_button("💥 Enviar respuestas")
    if enviar:
        if any(r == "-- Selecciona una opción --" for r in respuestas):
            st.error("❗ Debes responder todas las preguntas.")
        else:
            aciertos = sum(
                1 for idx, p in enumerate(preguntas)
                if respuestas[idx] == p["respuesta"]
            )
            nota = round((aciertos / len(preguntas)) * 10, 2)
            ss.nota_actual = nota
            ss.mejor_nota  = max(ss.mejor_nota, nota)
            ss.intentos   += 1
            ss.show_q      = False
            ss.show_decision = True
            if ss.intentos >= 3:
                ss.final = True
            st.rerun()

# --- 3) Nota y decisión ---
if ss.show_decision:
    st.info(f"🎯 Nota del intento: **{ss.nota_actual}/10**")
    st.success(f"⭐ Mejor nota hasta ahora: **{ss.mejor_nota}/10**")
    if ss.final:
        if st.button("🏠 Pantalla principal"):
            for k in list(ss.keys()):
                del ss[k]
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Sí, otro intento"):
                for idx in range(len(preguntas)):
                    key = f"q{idx}"
                    if key in ss:
                        del ss[key]
                ss.show_q      = True
                ss.show_decision = False
                st.rerun()
        with col2:
            if st.button("❌ No, no quiero otro intento"):
                ss.final = True
                st.rerun()

# --- 4) Pantalla final ---
if ss.final and not ss.show_q and not ss.show_decision:
    st.info(f"🏁 Tu nota final es: **{ss.mejor_nota}/10**")
    if st.button("🏠 Pantalla principal"):
        for k in list(ss.keys()):
            del ss[k]
        st.rerun()
