import streamlit as st

def cargar_css():
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
    .pregunta-card h3 { margin: 0; }

    /* Inputs amarillo pastel */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input {
      background-color: #fff9c4;
      color: #0a0a0a;
      border: 1px solid #fdd835;
      border-radius: 5px;
      padding: 0.5em;
      font-weight: bold;
    }
    .stTextInput>div>div>input::placeholder {
      color: #666;
      font-weight: bold;
    }

    /* Radios verde pastel */
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

    /* Forzar texto oscuro en móvil */
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

def inicializar_estado():
    defaults = {
        "nombre": "",
        "edad": 18,
        "jugando": False,
        "intentos": 0,
        "mejor_nota": 0.0,
        "nota_actual": 0.0,
        "mostrar_preguntas": False,
        "mostrar_decision": False,
        "finalizado": False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def mostrar_encabezado():
    st.markdown(
        "<h1 style='text-align:center;'>Encuesta Diagnóstica: Apuestas Deportivas</h1>",
        unsafe_allow_html=True
    )

def formulario_ingreso():
    ss = st.session_state
    if not ss.jugando and not ss.finalizado and ss.intentos < 3:
        with st.form("login_form"):
            st.subheader("👤 Por favor, ingrese sus datos personales (18 años o más)")
            nombre = st.text_input("Nombre completo", ss.nombre,
                                   placeholder="Ingrese su nombre completo")
            edad = st.number_input("Edad", min_value=1, max_value=120,
                                   value=ss.edad, step=1)
            enviar = st.form_submit_button("🟢 Comenzar evaluación diagnóstica")
        if enviar:
            if not nombre.strip():
                st.warning("❗ Debe ingresar su nombre completo.")
            elif edad < 18:
                st.error("🚫 Debe tener al menos 18 años.")
            else:
                ss.nombre = nombre
                ss.edad = edad
                ss.jugando = True
                ss.mostrar_preguntas = True
                st.rerun()

def obtener_preguntas():
    return [
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

def formulario_cuestionario():
    ss = st.session_state
    preguntas = obtener_preguntas()
    if ss.jugando and ss.mostrar_preguntas and ss.intentos < 3:
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
                opts = ["-- Seleccione una opción --"] + p["opciones"]
                sel = st.radio("", opts, index=0, key=f"q{i}")
                respuestas.append(sel)
            enviar = st.form_submit_button("💥 Enviar respuestas")
        if enviar:
            if any(r == "-- Seleccione una opción --" for r in respuestas):
                st.error("❗ Por favor responda todas las preguntas.")
            else:
                aciertos = sum(
                    1 for idx, p in enumerate(preguntas)
                    if respuestas[idx] == p["respuesta"]
                )
                nota = round((aciertos / len(preguntas)) * 10, 2)
                ss.nota_actual = nota
                ss.mejor_nota = max(ss.mejor_nota, nota)
                ss.intentos += 1
                ss.mostrar_preguntas = False
                ss.mostrar_decision = True
                if ss.intentos >= 3:
                    ss.finalizado = True
                st.rerun()

def mostrar_resultado():
    ss = st.session_state
    if ss.mostrar_decision:
        st.info(f"🎯 Nota del intento: **{ss.nota_actual}/10**")
        st.success(f"⭐ Mejor nota: **{ss.mejor_nota}/10**")
        if ss.finalizado:
            if st.button("🏠 Pantalla principal"):
                reiniciar()
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 Sí, otro intento"):
                    limpiar_respuestas(len(obtener_preguntas()))
                    ss.mostrar_preguntas = True
                    ss.mostrar_decision = False
                    st.rerun()
            with c2:
                if st.button("❌ No, no deseo otro intento"):
                    ss.finalizado = True
                    st.rerun()

def limpiar_respuestas(n):
    for i in range(n):
        key = f"q{i}"
        if key in st.session_state:
            del st.session_state[key]

def reiniciar():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

def main():
    cargar_css()
    inicializar_estado()
    mostrar_encabezado()
    formulario_ingreso()
    formulario_cuestionario()
    mostrar_resultado()

if __name__ == "__main__":
    main()
