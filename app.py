import streamlit as st

# Título del juego
st.title("🔤 Sopa de Letras: Apuestas Deportivas")

# Palabras a buscar
palabras_clave = {"CUOTA", "RIESGO", "APUESTA", "PARLAY", "GANANCIA", "JUGADOR", "BOOKMAKER", "BANCA"}

# Mostrar instrucciones
st.info("Encuentra las palabras ocultas relacionadas con las apuestas deportivas. Escríbelas en el campo de abajo. ¡Tienes 8 intentos!")

# Sopa de letras (manual para mostrar visualmente)
sopa = """
R I E S G O P A R L A Y
U B O O K M A K E R G N
A P U E S T A N B A N C
S R T J U G A D O R M I
C Q W E R T Y U I O P A
"""

st.text_area("🔍 Sopa de letras:", sopa, height=150, disabled=True)

# Inicializar variables
if "encontradas" not in st.session_state:
    st.session_state.encontradas = set()
if "intentos" not in st.session_state:
    st.session_state.intentos = 0

# Entrada del usuario
palabra = st.text_input("✍️ Escribe una palabra que encontraste:")

if st.button("Validar palabra"):
    palabra_mayus = palabra.strip().upper()
    st.session_state.intentos += 1

    if palabra_mayus in palabras_clave and palabra_mayus not in st.session_state.encontradas:
        st.success(f"✅ ¡Correcto! Encontraste: {palabra_mayus}")
        st.session_state.encontradas.add(palabra_mayus)
    elif palabra_mayus in st.session_state.encontradas:
        st.warning("⚠️ Esa palabra ya la encontraste.")
    else:
        st.error("❌ Esa palabra no está en la lista.")

# Mostrar progreso
st.markdown(f"🧠 Palabras encontradas: **{len(st.session_state.encontradas)} / {len(palabras_clave)}**")
st.markdown(f"🕓 Intentos usados: **{st.session_state.intentos} / 8**")

# Mostrar palabras ya encontradas
if st.session_state.encontradas:
    st.write("📌 Palabras encontradas:")
    st.write(", ".join(sorted(st.session_state.encontradas)))

# Fin del juego
if len(st.session_state.encontradas) == len(palabras_clave):
    st.balloons()
    st.success("🎉 ¡Encontraste todas las palabras! ¡Buen trabajo!")

if st.session_state.intentos >= 8 and len(st.session_state.encontradas) < len(palabras_clave):
    st.warning("😢 Se acabaron los intentos.")

# Botón para reiniciar
if st.button("🔁 Reiniciar juego"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

