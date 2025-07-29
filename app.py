import streamlit as st

# === CSS personalizado responsivo ===
st.markdown("""
<style>
/* —––––––––––––––––––––––––––––––––– Base styles –––––––––––––––––––––––––––––––––— */

/* Fondo suave y texto en negrita */
section.main {
  background: #f0f4f8;
  color: #0a0a0a;
  font-weight: bold;
}

/* Encabezados naranja pastel */
h1, h2, h3 {
  color: #ffb74d;
  font-weight: bold;
  margin-bottom: 0.5em;
}

/* Tarjetas de pregunta */
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

/* Botones verde pastel sin ancho fijo */
div.stButton > button {
  background-color: #a5d6a7;
  color: #1b5e20;
  border: 2px solid #66bb6a;
  padding: 0.6em 1.2em;
  border-radius: 0.5em;
  font-weight: bold;
  font-size: 1em;
  margin: 0.5em auto;
  display: block;
  max-width: 280px;
  width: auto;
}
div.stButton > button:hover {
  background-color: #81c784;
  border-color: #4caf50;
}

/* Alerts personalizados */
.stAlertInfo    { background:#bbdefb;  color:#0d47a1; border:1px solid #64b5f6; }
.stAlertSuccess { background:#c8e6c9;  color:#1b5e20; border:1px solid #81c784; }
.stAlertWarning { background:#ffe0b2;  color:#e65100; border:1px solid #ffb74d; }
.stAlertError   { background:#ffcdd2;  color:#b71c1c; border:1px solid #e57373; }

/* —––––––––––––––––––––––––––––––––– Responsive para móviles –––––––––––––––––––––––––––––––––— */
@media only screen and (max-width: 600px) {
  /* Tarjetas más compactas */
  .pregunta-card {
    padding: 0.6rem;
    margin-bottom: 1rem;
  }
  /* Encabezados más pequeños */
  h1 { font-size: 1.6rem !important; }
  h2 { font-size: 1.3rem !important; }
  h3 { font-size: 1.1rem !important; }

  /* Inputs más compactos */
  .stTextInput>div>div>input,
  .stNumberInput>div>div>input {
    font-size: 0.9rem;
    padding: 0.4em;
  }

  /* Radios más compactos */
  .stRadio > div > label {
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
  }

  /* Botones fluidos en móvil */
  div.stButton > button {
    font-size: 0.9rem;
    padding: 0.5em 1em;
    max-width: 90%;
  }
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="🎲 Apuestas Deportivas", layout="centered")

# --- Títulos ---
st.markdown("<h1 style='text-align:center;'>🎲 Cuestionario Diagnóstico</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>Apuestas Deportivas</h2>", unsafe_allow_html=True)

# --- Resto de tu lógica (session state, login form, cuestionario, etc.) ---
# ... (mantén todo igual a como lo tenías) ...
