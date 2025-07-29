import streamlit as st

def mostrar_cuestionario():
    preguntas = [
        {"pregunta": "¿Qué es una apuesta deportiva?",
         "opciones": ["Una predicción sin dinero", "Un juego de azar con dinero", "Una inversión garantizada", "Una actividad ilegal"],
         "respuesta": "Un juego de azar con dinero"},
        {"pregunta": "¿Qué significa 'cuota' en apuestas?",
         "opciones": ["El dinero apostado", "La probabilidad de ganar", "El pago potencial", "El tipo de apuesta"],
         "respuesta": "El pago potencial"},
        # ... agrega las 20 preguntas aquí como en el ejemplo anterior ...
    ]

    puntaje = 0

    for i, pregunta in enumerate(preguntas, 1):
        st.write(f"**Pregunta {i}:** {pregunta['pregunta']}")
        opciones = pregunta["opciones"]
        respuesta_correcta = pregunta["respuesta"]
        seleccion = st.radio("", opciones, key=f"pregunta_{i}")
        if seleccion == respuesta_correcta:
            puntaje += 1

    st.session_state['puntaje'] = puntaje

def main():
    if "mostrar_resultado" not in st.session_state:
        st.session_state.mostrar_resultado = False
    if "intentos" not in st.session_state:
        st.session_state.intentos = 0
    if "puntaje" not in st.session_state:
        st.session_state.puntaje = 0

    if not st.session_state.mostrar_resultado:
        mostrar_cuestionario()
        if st.button("Enviar respuestas"):
            st.session_state.intentos += 1
            st.session_state.mostrar_resultado = True
    else:
        st.write(f"Tu puntaje es {st.session_state.puntaje} de 20")
        st.write(f"Intento número: {st.session_state.intentos}")

        opcion = st.radio("¿Quieres realizar otro intento?", ("Sí", "No"))

        if opcion == "Sí":
            st.session_state.mostrar_resultado = False
            # Limpiar respuestas previas para nuevo intento
            for i in range(1, 21):
                key = f"pregunta_{i}"
                if key in st.session_state:
                    del st.session_state[key]

        if opcion == "No":
            st.write("Gracias por participar.")
            if st.button("Regresar al menú principal"):
                st.session_state.mostrar_resultado = False
                st.session_state.intentos = 0
                st.session_state.puntaje = 0
                # Aquí puedes añadir la lógica para regresar al menú principal o reiniciar la app

if __name__ == "__main__":
    main()
