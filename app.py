import streamlit as st

# === CSS personalizado con media query para móvil ===
st.markdown("""
<style>
/* Fondo suave y texto oscuro */
section.main, .block-container {
  background: #f0f4f8 !important;
  color: #0a0a0a !important;
  font-weight: bold !important;
}

/* Tarjeta de pregunta: verde pastel por defecto */
.pregunta-card {
  background-color: #ffffff !important;
  border: 2px solid #4caf50 !important;
  border-radius: 10px !important;
  padding: 1rem !important;
  margin-bottom: 1.5rem !important;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}

/* Inputs amarillo pastel */
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
  background-color: #fff9c4 !important;
  color: #0a0a0a !important;
  border: 1px solid #fdd835 !important;
  border-radius: 5px !important;
  padding: 0.5em !important;
  font-weight: bold !important;
}

/* Placeholder negrita y oscuro */
.stTextInput>div>div>input::placeholder {
  color: #666 !important;
  font-weight: bold !important;
}

/* Radios verde pastel */
.stRadio > div > label {
  font-weight: bold !important;
  color: #0a0a0a !important;
  margin-bottom: 0.5rem !important;
}
.stRadio > div > label > input[type="radio"] + span:before {
  border: 2px solid #66bb6a !important;
  background-color: #e8f5e9 !important;
}
.stRadio > div > label > input[type="radio"]:checked + span:after {
  background-color: #66bb6a !important;
  border-color: #66bb6a !important;
}

/* Botones verde pastel */
div.stButton > button {
  background-color: #a5d6a7 !important;
  color: #1b5e20 !important;
  border: 2px solid #66bb6a !important;
  padding: 0.6em 1.2em !important;
  border-radius: 0.5em !important;
  font-weight: bold !important;
  font-size: 1em !important;
  margin: 0.3em 0 !important;
  width: 100% !important;
}
div.stButton > button:hover {
  background-color: #81c784 !important;
  border-color: #4caf50 !important;
}

/* Encabezados naranja pastel */
h1, h2, h3 {
  color: #ffb74d !important;
  font-weight: bold !important;
}

/* SOLO MÓVIL: borde naranja vibrante en las tarjetas */
@media only screen and (max-width: 600px) {
  .pregunta-card {
    background-color: #fff3e0 !important;
    border: 2px solid #ff7043 !important;
  }
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎲 Apuestas Deportivas", layout="centered")

# === Títulos ===
st.markdown("<h1 style='text-align:center;'>🎲 Cuestionario Diagnóstico</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>Apuestas Deportivas</h2>", unsafe_allow_html=True)

# === Session State ===
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

# === 1) Formulario de Login ===
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

# === Preguntas (extiende hasta 20) ===
preguntas = [
    {"pregunta":"¿Qué es una apuesta deportiva?",
     "opciones":["Predicción sin dinero","Juego de azar con dinero","Inversión garantizada","Actividad ilegal"],
     "respuesta":"Juego de azar con dinero"},
    {"pregunta":"¿Qué significa 'cuota' en apuestas?",
     "opciones":["Dinero apostado","Probabilidad de ganar","Pago potencial","Tipo de apuesta"],
     "respuesta":"Pago potencial"},
    # ... añade aquí las 18 preguntas restantes ...
]

# === 2) Cuestionario ===
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

# === 3) Nota y decisión ===
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

# === 4) Pantalla final ===
if ss.final and not ss.show_q and not ss.show_decision:
    st.info(f"🏁 Tu nota final es: **{ss.mejor_nota}/10**")
    if st.button("🏠 Pantalla principal"):
        for k in list(ss.keys()):
            del ss[k]
        st.rerun()
