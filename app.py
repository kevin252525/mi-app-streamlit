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

/* Tarjeta de pregunta y encabezado de intento */
.pregunta-card {
  background-color: #fff3e0;
  border: 2px solid #ff7043;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.pregunta-card h3 {
  margin: 0;
}

/* Campos de entrada en amarillo pastel */
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
  background-color: #fff9c4;
  color: #0a0a0a;
  border: 1px solid #fdd835;
  border-radius: 5px;
  padding: 0.5em;
  font-weight: bold;
}

/* Placeholder en negrita */
.stTextInput>div>div>input::placeholder {
  color: #666;
  font-weight: bold;
}

/* Radios en verde pastel */
.stRadio > div > label {
  font-weight: bold;
  color: #0a0a0a;
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

/* Botones en verde pastel */
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

/* Encabezados en naranja pastel */
h1, h2, h3 {
  color: #ffb74d;
  font-weight: bold;
}

/* Forzar texto oscuro en móviles */
@media (max-width: 600px) {
  .pregunta-card,
  .pregunta-card strong,
  .stRadio > div > label,
  .stRadio > div > label > input[type="radio"] + span,
  .stTextInput>div>div>input,
  .stNumberInput>div>div>input {
    color: #0a0a0a !important;
  }
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎲 Cuestionario de Apuestas Deportivas", layout="centered")

# === Títulos ===
st.markdown("<h1 style='text-align:center;'>🎲 Cuestionario Diagnóstico de Apuestas Deportivas</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>Compruebe sus conocimientos</h2>", unsafe_allow_html=True)

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

# === 1) Formulario de datos ===
if not ss.jugando and not ss.final and ss.intentos < 3:
    with st.form("login_form"):
        st.subheader("👤 Por favor, ingrese sus datos (≥18 años)")
        nombre = st.text_input("Nombre completo", ss.nombre, placeholder="Ingrese su nombre")
        edad   = st.number_input("Edad", min_value=1, max_value=120, value=ss.edad, step=1)
        iniciar = st.form_submit_button("🟢 Iniciar cuestionario")
    if iniciar:
        if not nombre.strip():
            st.warning("❗ Por favor, ingrese su nombre.")
        elif edad < 18:
            st.error("🚫 Debe tener al menos 18 años para continuar.")
        else:
            ss.nombre = nombre
            ss.edad   = edad
            ss.jugando = True
            ss.show_q  = True
            st.rerun()

# === Listado de preguntas (complete hasta 20) ===
preguntas = [
    {"pregunta":"¿Qué es una apuesta deportiva?",
     "opciones":["Predicción sin dinero","Juego de azar con dinero",
                 "Inversión garantizada","Actividad ilegal"],
     "respuesta":"Juego de azar con dinero"},
    {"pregunta":"¿Qué significa 'cuota' en apuestas?",
     "opciones":["Dinero apostado","Probabilidad de ganar",
                 "Pago potencial","Tipo de apuesta"],
     "respuesta":"Pago potencial"},
    # … agregue aquí las restantes …
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
            opciones = ["-- Seleccione una opción --"] + p["opciones"]
            sel = st.radio("", opciones, index=0, key=f"q{i}")
            respuestas.append(sel)
        enviar = st.form_submit_button("💥 Enviar respuestas")
    if enviar:
        if any(r == "-- Seleccione una opción --" for r in respuestas):
            st.error("❗ Por favor, responda todas las preguntas antes de continuar.")
        else:
            aciertos = sum(1 for idx, p in enumerate(preguntas) if respuestas[idx] == p["respuesta"])
            nota = round((aciertos / len(preguntas)) * 10, 2)
            ss.nota_actual = nota
            ss.mejor_nota  = max(ss.mejor_nota, nota)
            ss.intentos   += 1
            ss.show_q      = False
            ss.show_decision = True
            if ss.intentos >= 3:
                ss.final = True
            st.rerun()

# === 3) Mostrar nota y decisión ===
if ss.show_decision:
    st.info(f"🎯 Nota de este intento: **{ss.nota_actual}/10**")
    st.success(f"⭐ Mejor nota obtenida: **{ss.mejor_nota}/10**")
    if ss.final:
        if st.button("🏠 Volver al inicio"):
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
                ss.show_q       = True
                ss.show_decision = False
                st.rerun()
        with col2:
            if st.button("❌ No, deseo finalizar"):
                ss.final = True
                st.rerun()

# === 4) Pantalla final ===
if ss.final and not ss.show_q and not ss.show_decision:
    st.info(f"🏁 Nota final: **{ss.mejor_nota}/10**")
    if st.button("🏠 Volver al inicio"):
        for k in list(ss.keys()):
            del ss[k]
        st.rerun()
