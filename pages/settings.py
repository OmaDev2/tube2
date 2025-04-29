import streamlit as st
import os
from dotenv import load_dotenv, set_key

ENV_PATH = ".env"

# Cargar variables de entorno
load_dotenv(ENV_PATH)

def show_settings():
    st.title("🔑 Configuración de APIs")
    st.write("Gestiona aquí tus claves de acceso a los servicios de IA.")

    # Leer claves actuales
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    replicate_api_key = os.getenv("REPLICATE_API_KEY", "")

    # Formulario para editar claves
    with st.form("api_keys_form"):
        openai = st.text_input("OpenAI API Key", value=openai_api_key, type="password")
        gemini = st.text_input("Gemini API Key", value=gemini_api_key, type="password")
        replicate = st.text_input("Replicate API Key", value=replicate_api_key, type="password")
        submitted = st.form_submit_button("Guardar claves")
        if submitted:
            set_key(ENV_PATH, "OPENAI_API_KEY", openai)
            set_key(ENV_PATH, "GEMINI_API_KEY", gemini)
            set_key(ENV_PATH, "REPLICATE_API_KEY", replicate)
            st.success("Claves guardadas correctamente en .env")
            # Recargar variables de entorno
            load_dotenv(ENV_PATH, override=True)

    st.write("Funcionalidad en desarrollo...") 