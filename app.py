import streamlit as st

# --- CSS personalizado para tema de apuestas ---
st.markdown("""
<style>
/* Fondo general */
section.main {
  background: #1a1a1a;
  color: #f2f2f2;
}
/* Encabezado */
h1, h2, h3 {
  font-family: 'Segoe UI', sans-serif;
  color: #FFD700;  /* Dorado */
}
/* Tarjetas */
.stCard {
  background-color: #2e2e2e;
  border: 2px solid #444;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
}
/* Botones */
div.stButton > button {
  background-color: #00b300;  /* Verde apuestas */
  color: white;
  border: 2px solid #FFD700;
  padding: 0.6em 1.2em;
  border-radius: 0.5em;
  font-weight: bold;
  font-size: 1em;
  margin: 0.3em;
  width: 100%;
}
div.stButton > button:hover {
  background-color: #009900;
  border-color: #FFA500;
}
/* Inputs */
.stTextInput>div>div>input, .stNumberInput>div>div>input {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
}
/* Radios estilo personalizado */
.stRadio > label {
  font-size: 0.95em;
}
.stRadio > div > label > input[type="radio"] + span:before {
  border: 2px solid #FFD700;
  background-color: #1a1a1a;
}
.stRadio > div > label > input[type="radio"]:checked + span:after {
  background-color: #FFD700;
  border-color: #FFD700;
}
/* Infos y warnings */
.stAlertInfo {
  background-color: #004d66;
  color: #e6f7ff;
  border: 1px solid #00aaff;
}
.stAlertSuccess {
  background-color: #004d11;
  color: #ccffcc;
  border: 1px solid #00e600;
}
.stAlertWarning {
  background-color: #663300;
  color: #ffe6cc;
  border: 1px solid #ff9900;
}
.stAlertError {
  background-color: #660000;
  color: #ffcccc;
  border: 1px solid #ff0000;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎲 Apuestas Deportivas", layout="wide")

# --- Banner principal ---
st.markdown(
    "<h1 style='text-align:center;'>🎲 Cuestionario Diagnóstico - Apuestas Deportivas</h1>"
    "<h3 style='text-align:center; color:#FFA500;'>Pon a prueba tus conocimientos y gana puntos</h3>",
    unsafe_allow_html=True
)

ss = st.session_state
# Inicializar estado
for k, v in [
    ("nombre",""),
    ("edad",18),
    ("jugando", False),
    ("intentos", 0),
    ("mejor_nota", 0.0),
    ("nota_actual", 0.0),
    ("show_q", False),
    ("show_decision", False),
    ("final", False),
]:
    if k not in ss:
        ss[k] = v

# --- 1) FORMULARIO DE LOGIN ---
if not ss.jugando and not ss.final and ss.intentos < 3:
    with st.form("login_form", clear_on_submit=False):
        st.subheader("👤 Ingresa tus datos (≥18 años)")
        ss.nombre = st.text_input("Nombre", ss.nombre)
        ss.edad = st.number_input("Edad", min_value=1, max_value=120, value=ss.edad, step=1)
        iniciar = st.form_submit_button("🟢 Iniciar juego")
    if iniciar:
        if ss.nombre.strip() == "":
            st.warning("❗ Debes ingresar tu nombre.")
        elif ss.edad < 18:
            st.error("🚫 Debes tener al menos 18 años.")
        else:
            ss.jugando = True
            ss.show_q = True
            ss.show_decision = False
            st.rerun()

# --- Tus 20 preguntas (ejemplo con 2; extiende) ---
preguntas = [
    {"pregunta": "¿Qué es una apuesta deportiva?",
     "opciones": ["Predicción sin dinero", "Juego de azar con dinero",
                  "Inversión garantizada", "Actividad ilegal"],
     "respuesta": "Juego de azar con dinero"},
    {"pregunta": "¿Qué significa 'cuota' en apuestas?",
     "opciones": ["Dinero apostado", "Probabilidad de ganar",
                  "Pago potencial", "Tipo de apuesta"],
     "respuesta": "Pago potencial"},
    # ... hasta 20 preguntas ...
]

# --- 2) Formulario del cuestionario ---
if ss.jugando and ss.show_q and ss.intentos < 3:
    with st.form("quiz_form"):
        st.markdown(f"<div class='stCard'><h3>🏅 Intento {ss.intentos+1} de 3 — {ss.nombre}</h3></div>", unsafe_allow_html=True)
        respuestas = []
        for i, p in enumerate(preguntas):
            st.markdown(f"**{i+1}. {p['pregunta']}**")
            opts = ["-- Selecciona una opción --"] + p["opciones"]
            sel = st.radio("", opts, index=0, key=f"q{i}")
            respuestas.append(sel)
        enviar = st.form_submit_button("💥 Enviar respuestas")
    if enviar:
        if any(r == "-- Selecciona una opción --" for r in respuestas):
            st.error("❗ Debes responder todas las preguntas.")
        else:
            aciertos = sum(1 for i,p in enumerate(preguntas) if respuestas[i] == p["respuesta"])
            nota = round((aciertos/len(preguntas))*10,2)
            ss.nota_actual = nota
            ss.mejor_nota = max(ss.mejor_nota, nota)
            ss.intentos += 1
            ss.show_q = False
            ss.show_decision = True
            if ss.intentos >= 3:
                ss.final = True
            st.rerun()

# --- 3) Mostrar nota y decisión ---
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
                for i in range(len(preguntas)):
                    key = f"q{i}"
                    if key in ss: del ss[key]
                ss.show_q = True
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
