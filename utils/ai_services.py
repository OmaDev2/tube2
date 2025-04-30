import os
import requests
import google.generativeai as genai

class AIServices:
    def __init__(self):
        # Inicialización de servicios de IA
        pass
    
    def generate_content(self, prompt):
        # Lógica para generar contenido usando IA
        pass 

def list_gemini_models(api_key=None):
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return []
    try:
        genai.configure(api_key=api_key)
        modelos = genai.list_models()
        return [(m.name, m.supported_generation_methods) for m in modelos]
    except Exception as e:
        return [(f"[ERROR] {e}", [])]

def generate_gemini_script(system_prompt, user_prompt, model="models/gemini-pro", api_key=None):
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return "[ERROR] No se ha configurado la clave de API de Gemini."
    try:
        genai.configure(api_key=api_key)
        modelo = genai.GenerativeModel(model)
        # Concatenar ambos prompts en uno solo, rol 'user'
        contenido = [
            {"role": "user", "parts": [{"text": f"{system_prompt}\n\n{user_prompt}"}]}
        ]
        response = modelo.generate_content(contenido)
        return response.text
    except Exception as e:
        return f"[ERROR] Error al llamar a Gemini: {e}" 