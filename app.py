# app.py
import streamlit as st
import time
import os
from PIL import Image
import numpy as np
import tempfile
import uuid
import base64
from pathlib import Path
from pages import batch_generator
from pages import settings
from pages import history

# Importaciones simuladas de tus módulos de utilidades
# En una implementación real, crearías estos archivos
#from utils.ai_services import generate_script, generate_image_prompts, generate_images
#from utils.audio_services import generate_voice, transcribe_audio
#from utils.video_services import create_video, add_transitions
#from utils.storage import save_project, load_project, get_all_projects

# Configuración de la página (debe ser la primera llamada a Streamlit)
st.set_page_config(
    page_title="Video Generator",
    page_icon="🎥",
    layout="wide"
)

# Inicializar estado de sesión si no existe
if "projects" not in st.session_state:
    st.session_state.projects = {}
if "current_project_id" not in st.session_state:
    st.session_state.current_project_id = None
if "generation_step" not in st.session_state:
    st.session_state.generation_step = 0
if "script_content" not in st.session_state:
    st.session_state.script_content = ""

# Función para crear un nuevo proyecto
def create_new_project():
    project_id = str(uuid.uuid4())
    st.session_state.current_project_id = project_id
    st.session_state.projects[project_id] = {
        "id": project_id,
        "title": "",
        "context": "",
        "script": "",
        "audio_path": None,
        "transcription": [],
        "prompts": [],
        "images": [],
        "video_path": None,
        "metadata": {},
        "created_at": time.time(),
        "status": "new"
    }
    st.session_state.generation_step = 0
    st.session_state.script_content = ""
    return project_id

# Sidebar para navegación y proyectos
with st.sidebar:
    st.title("🎬 VideoGen AI")
    
    # Botones de navegación
    st.button("➕ Nuevo Proyecto", on_click=create_new_project)
    
    # Lista de proyectos existentes
    st.subheader("Proyectos")
    if st.session_state.projects:
        project_titles = {pid: f"{p.get('title', 'Sin título')} ({pid[:6]})" 
                         for pid, p in st.session_state.projects.items()}
        selected_project = st.selectbox(
            "Seleccionar proyecto", 
            options=list(project_titles.keys()),
            format_func=lambda x: project_titles[x],
            index=0 if st.session_state.current_project_id in project_titles else 0
        )
        if selected_project != st.session_state.current_project_id:
            st.session_state.current_project_id = selected_project
            st.session_state.generation_step = 0
    else:
        st.info("No hay proyectos. Crea uno nuevo.")
        if st.button("Crear primer proyecto"):
            create_new_project()

    # Configuración general
    st.subheader("Configuración")
    ai_model = st.selectbox(
        "Modelo para guiones", 
        ["gpt-3.5-turbo", "gpt-4", "gemini-pro", "claude-instant", "llama3 (local)"]
    )
    
    image_model = st.selectbox(
        "Modelo para imágenes",
        ["stability-ai/sdxl", "stability-ai/stable-diffusion", "midjourney"]
    )
    
    voice_model = st.selectbox(
        "Voz",
        ["es-ES-ElviraNeural", "es-ES-AlvaroNeural", "es-MX-JorgeNeural", "en-US-JennyNeural"]
    )
    
    video_type = st.radio("Tipo de video", ["Short", "Video largo"])
    
    # Procesamiento por lotes
    st.subheader("Procesamiento por lotes")
    if st.button("Ir a generador por lotes"):
        st.switch_page("pages/batch_generator.py")

# Contenido principal
if not st.session_state.current_project_id:
    st.title("Bienvenido a VideoGen AI")
    st.write("Crea un nuevo proyecto o selecciona uno existente para comenzar.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Crear nuevo proyecto", on_click=create_new_project, use_container_width=True)
else:
    # Obtener proyecto actual
    current_project = st.session_state.projects[st.session_state.current_project_id]
    
    # Título del proyecto
    if current_project.get("title"):
        st.title(current_project["title"])
    else:
        st.title("Nuevo proyecto")
    
    # Pestañas principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ Guion", "2️⃣ Voz y transcripción", 
        "3️⃣ Imágenes", "4️⃣ Video", "5️⃣ Metadata"
    ])
    
    # ----- TAB 1: GUION -----
    with tab1:
        st.header("Generación de guion")
        
        # Sección de entrada
        col1, col2 = st.columns([2, 1])
        with col1:
            # Título y contexto
            title = st.text_input("Título del video", value=current_project.get("title", ""))
            if title != current_project.get("title"):
                current_project["title"] = title
            
            context = st.text_area(
                "Contexto o tema del video", 
                value=current_project.get("context", ""),
                height=100
            )
            if context != current_project.get("context"):
                current_project["context"] = context
        
        with col2:
            # Opciones de generación
            st.subheader("Opciones")
            tone = st.select_slider(
                "Tono", 
                options=["Formal", "Informativo", "Casual", "Entusiasta", "Humorístico"]
            )
            length = st.select_slider(
                "Longitud", 
                options=["Corto", "Medio", "Largo"]
            )
            st.caption(f"Usando modelo: {ai_model}")
        
        # Botones de acción para guion
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Generar guion", use_container_width=True):
                if not title or not context:
                    st.error("Debes proporcionar un título y contexto.")
                else:
                    with st.spinner("Generando guion..."):
                        # Aquí conectarías con tu servicio de IA
                        # Por ahora, simularemos un retraso
                        time.sleep(2)
                        generated_script = f"Este es un guion de ejemplo para '{title}' sobre '{context}' con tono {tone} y longitud {length}.\n\nAquí iría el contenido generado por la IA basado en el contexto proporcionado. El modelo {ai_model} analizaría el tema y generaría un guion coherente y estructurado para tu video.\n\nIncluiría una introducción atractiva, desarrollo de ideas principales, y una conclusión que invite a la acción."
                        current_project["script"] = generated_script
                        st.session_state.script_content = generated_script
                        current_project["status"] = "script_generated"
                        st.session_state.generation_step = 1
        
        with col2:
            if st.button("Cargar guion desde archivo", use_container_width=True):
                # En una app real, aquí permitirías cargar un archivo
                st.info("Funcionalidad de carga simulada")
                
        # Mostrar o editar guion
        st.subheader("Contenido del guion")
        script_content = st.text_area(
            "Editar guion (o genera uno nuevo)",
            value=current_project.get("script", st.session_state.script_content),
            height=300
        )
        if script_content != current_project.get("script"):
            current_project["script"] = script_content
            current_project["status"] = "script_edited"
            
        # Botón para avanzar
        if current_project.get("script"):
            if st.button("Continuar a generación de voz ▶️", use_container_width=True):
                st.session_state.generation_step = 1
                st.experimental_rerun()
    
    # ----- TAB 2: VOZ Y TRANSCRIPCIÓN -----
    with tab2:
        st.header("Generación de voz y transcripción")
        
        # Verificar si tenemos guion
        if not current_project.get("script"):
            st.warning("Primero debes crear un guion en la pestaña anterior.")
        else:
            # Opciones de voz
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("Guion a convertir")
                st.text_area("Guion", value=current_project.get("script", ""), height=150, disabled=True)
            
            with col2:
                st.subheader("Configuración de voz")
                voice = st.selectbox(
                    "Seleccionar voz",
                    [voice_model, "es-ES-AlvaroNeural", "es-MX-JorgeNeural"]
                )
                speed = st.slider("Velocidad", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
                pitch = st.slider("Tono", min_value=-10, max_value=10, value=0)
            
            # Generar audio
            if st.button("Generar audio", use_container_width=True):
                with st.spinner("Generando audio con Edge TTS..."):
                    # Simular generación de audio
                    time.sleep(3)
                    current_project["audio_path"] = "simulated_audio.mp3"
                    current_project["voice_config"] = {
                        "voice": voice,
                        "speed": speed,
                        "pitch": pitch
                    }
                    current_project["status"] = "audio_generated"
                    st.session_state.generation_step = 2
                    
            # Mostrar reproductor de audio si existe
            if current_project.get("audio_path"):
                st.subheader("Previsualización de audio")
                st.audio("https://samplelib.com/lib/preview/mp3/sample-3s.mp3")  # Audio simulado
                
                # Transcripción
                st.subheader("Transcripción")
                with st.spinner("Generando transcripción..."):
                    # Simular transcripción con timestamps
                    if not current_project.get("transcription"):
                        time.sleep(2)
                        # Crear transcripción simulada con timestamps
                        lines = current_project.get("script", "").split("\n\n")
                        transcription = []
                        start_time = 0
                        
                        for i, line in enumerate(lines):
                            if line.strip():
                                duration = len(line.split()) * 0.3  # ~0.3s por palabra
                                end_time = start_time + duration
                                transcription.append({
                                    "text": line.strip(),
                                    "start": start_time,
                                    "end": end_time,
                                    "segment_id": i
                                })
                                start_time = end_time + 0.5  # Pausa entre segmentos
                        
                        current_project["transcription"] = transcription
                        current_project["status"] = "transcription_complete"
                
                # Mostrar transcripción con timestamps
                if current_project.get("transcription"):
                    for segment in current_project["transcription"]:
                        st.text(f"[{segment['start']:.2f}s - {segment['end']:.2f}s]: {segment['text']}")
                    
                    # Botón para continuar
                    if st.button("Continuar a generación de imágenes ▶️", use_container_width=True):
                        st.session_state.generation_step = 3
                        st.experimental_rerun()
    
    # ----- TAB 3: IMÁGENES -----
    with tab3:
        st.header("Generación de imágenes")
        
        # Verificar que tengamos transcripción
        if not current_project.get("transcription"):
            st.warning("Primero debes generar el audio y la transcripción en la pestaña anterior.")
        else:
            # Opciones de generación de imágenes
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Configuración de imágenes")
                prompt_style = st.selectbox(
                    "Estilo de prompts",
                    ["Descriptivo", "Artístico", "Realista", "Abstracto", "Minimalista"]
                )
                
                image_per_segment = st.number_input(
                    "Imágenes por segmento", 
                    min_value=1,
                    max_value=3,
                    value=1
                )
                
                st.caption(f"Usando modelo: {image_model}")
                
            with col2:
                st.subheader("Estilo visual")
                aspect_ratio = st.radio(
                    "Relación de aspecto",
                    ["16:9 (Horizontal)", "9:16 (Vertical/Short)", "1:1 (Cuadrado)"]
                )
                
                style_modifiers = st.multiselect(
                    "Modificadores de estilo",
                    ["Cinematográfico", "Alta definición", "Ilustración", "Fotorrealista", "3D"],
                    default=["Cinematográfico", "Alta definición"]
                )
            
            # Botón para generar prompts e imágenes
            if st.button("Generar prompts e imágenes", use_container_width=True):
                # Mostrar segmentos y generar prompts
                st.subheader("Segmentos y prompts")
                
                # Simular generación de prompts
                with st.spinner("Generando prompts para imágenes..."):
                    time.sleep(2)
                    
                    if not current_project.get("prompts"):
                        prompts = []
                        for i, segment in enumerate(current_project["transcription"]):
                            prompt = {
                                "segment_id": segment["segment_id"],
                                "text": segment["text"],
                                "prompt": f"Imagen {prompt_style.lower()} que represente: {segment['text'][:50]}... {', '.join(style_modifiers).lower()}, {aspect_ratio}",
                                "images": []
                            }
                            prompts.append(prompt)
                        
                        current_project["prompts"] = prompts
                        current_project["status"] = "prompts_generated"
                
                # Mostrar y permitir editar prompts
                if current_project.get("prompts"):
                    for i, prompt_data in enumerate(current_project["prompts"]):
                        with st.expander(f"Segmento {i+1}: {prompt_data['text'][:50]}..."):
                            # Texto original
                            st.text(prompt_data["text"])
                            
                            # Editar prompt
                            edited_prompt = st.text_area(
                                "Prompt para imagen", 
                                value=prompt_data["prompt"],
                                key=f"prompt_{i}"
                            )
                            
                            if edited_prompt != prompt_data["prompt"]:
                                current_project["prompts"][i]["prompt"] = edited_prompt
                                current_project["prompts"][i]["images"] = []  # Limpiar imágenes si se edita el prompt
                            
                            # Generar imágenes para este segmento
                            if st.button(f"Generar imagen para segmento {i+1}", key=f"gen_img_{i}"):
                                with st.spinner(f"Generando imagen para segmento {i+1}..."):
                                    # Simular generación de imagen
                                    time.sleep(3)
                                    image_urls = [f"https://picsum.photos/800/450?random={uuid.uuid4()}"]
                                    current_project["prompts"][i]["images"] = image_urls
                                    st.experimental_rerun()
                            
                            # Mostrar imágenes generadas
                            if prompt_data.get("images"):
                                for img_url in prompt_data["images"]:
                                    st.image(img_url, caption=f"Imagen generada - Segmento {i+1}")
                    
                    # Botón para generar todas las imágenes
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Generar todas las imágenes faltantes", use_container_width=True):
                            with st.spinner("Generando todas las imágenes faltantes..."):
                                # Simular generación de imágenes para todos los segmentos
                                for i, prompt_data in enumerate(current_project["prompts"]):
                                    if not prompt_data.get("images"):
                                        time.sleep(1)  # Simular tiempo de generación
                                        image_urls = [f"https://picsum.photos/800/450?random={uuid.uuid4()}"]
                                        current_project["prompts"][i]["images"] = image_urls
                                
                                current_project["status"] = "images_generated"
                                st.experimental_rerun()
                    
                    with col2:
                        # Botón para continuar
                        if all(p.get("images") for p in current_project.get("prompts", [])):
                            if st.button("Continuar a composición de video ▶️", use_container_width=True):
                                st.session_state.generation_step = 4
                                st.experimental_rerun()
                        else:
                            st.warning("Genera imágenes para todos los segmentos antes de continuar")
    
    # ----- TAB 4: VIDEO -----
    with tab4:
        st.header("Composición de video")
        
        # Verificar que tengamos imágenes
        if not current_project.get("prompts") or not all(p.get("images") for p in current_project.get("prompts", [])):
            st.warning("Primero debes generar imágenes para todos los segmentos.")
        else:
            # Opciones de composición
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Transiciones")
                transition_type = st.selectbox(
                    "Tipo de transición",
                    ["Dissolve", "Fade", "Cut", "Wipe"]
                )
                transition_duration = st.slider(
                    "Duración de transición (segundos)",
                    min_value=0.1,
                    max_value=2.0,
                    value=0.7,
                    step=0.1
                )
            
            with col2:
                st.subheader("Música de fondo")
                use_bg_music = st.checkbox("Añadir música de fondo", value=True)
                if use_bg_music:
                    bg_music_type = st.selectbox(
                        "Tipo de música",
                        ["Inspiradora", "Energética", "Relajante", "Corporativa", "Sin música"]
                    )
                    bg_music_volume = st.slider("Volumen", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
            
            # Mostrar timeline simulado
            st.subheader("Timeline")
            timeline_col = st.columns(len(current_project.get("prompts", [])))
            
            for i, (col, segment) in enumerate(zip(timeline_col, current_project.get("prompts", []))):
                with col:
                    if segment.get("images"):
                        st.image(segment["images"][0], caption=f"Seg. {i+1}", width=100)
            
            # Opciones de formato
            st.subheader("Formato de salida")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                resolution = st.selectbox(
                    "Resolución",
                    ["1080p (1920x1080)", "720p (1280x720)", "Vertical (1080x1920)"]
                )
            
            with col2:
                format_type = st.selectbox(
                    "Formato",
                    ["MP4", "MOV", "WebM"]
                )
            
            with col3:
                quality = st.select_slider(
                    "Calidad",
                    options=["Baja", "Media", "Alta", "Ultra"]
                )
            
            # Botón para generar video
            if st.button("Generar video", use_container_width=True):
                with st.spinner("Componiendo video... Esto puede tomar unos minutos"):
                    # Simular barra de progreso
                    progress_bar = st.progress(0)
                    for i in range(101):
                        time.sleep(0.05)  # Simular trabajo
                        progress_bar.progress(i)
                    
                    # Simular video generado
                    current_project["video_path"] = "simulated_video.mp4"
                    current_project["video_config"] = {
                        "transition": transition_type,
                        "transition_duration": transition_duration,
                        "bg_music": bg_music_type if use_bg_music else None,
                        "bg_music_volume": bg_music_volume if use_bg_music else 0,
                        "resolution": resolution,
                        "format": format_type,
                        "quality": quality
                    }
                    current_project["status"] = "video_generated"
                    st.session_state.generation_step = 5
                    st.success("¡Video generado con éxito!")
            
            # Mostrar video si existe
            if current_project.get("video_path"):
                st.subheader("Video generado")
                # Usar un video de ejemplo para demostración
                st.video("https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4")
                
                # Botones de acción
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.download_button(
                        "Descargar video",
                        data=b"video_simulado",  # Aquí irían los bytes del video real
                        file_name=f"{current_project['title']}.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("Continuar a metadata ▶️", use_container_width=True):
                        st.session_state.generation_step = 5
                        st.experimental_rerun()
    
    # ----- TAB 5: METADATA -----
    with tab5:
        st.header("Metadata para YouTube")
        
        # Verificar que tengamos video
        if not current_project.get("video_path"):
            st.warning("Primero debes generar el video en la pestaña anterior.")
        else:
            # Generar metadata
            if not current_project.get("metadata"):
                with st.spinner("Generando metadata optimizada para YouTube..."):
                    time.sleep(2)
                    # Simular generación de metadata
                    current_project["metadata"] = {
                        "title": f"{current_project.get('title')} - {['Tutorial', 'Guía', 'Explicación'][np.random.randint(0,3)]} Completa",
                        "description": f"En este video exploramos {current_project.get('context')}.\n\nDescubre más sobre este tema y cómo puede beneficiarte.\n\n#VideoAI #Contenido #{current_project.get('title').replace(' ', '')}",
                        "tags": [
                            current_project.get('title'),
                            "tutorial",
                            "guía",
                            "aprendizaje",
                            "VideoAI"
                        ],
                        "category": "Education",
                        "visibility": "Public",
                        "thumbnail_text": f"{current_project.get('title').upper()}"
                    }
                    
                    current_project["status"] = "metadata_generated"
            
            # Mostrar y permitir editar metadata
            if current_project.get("metadata"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("Metadata para YouTube")
                    
                    yt_title = st.text_input(
                        "Título optimizado", 
                        value=current_project["metadata"]["title"]
                    )
                    if yt_title != current_project["metadata"]["title"]:
                        current_project["metadata"]["title"] = yt_title
                    
                    yt_desc = st.text_area(
                        "Descripción", 
                        value=current_project["metadata"]["description"],
                        height=150
                    )
                    if yt_desc != current_project["metadata"]["description"]:
                        current_project["metadata"]["description"] = yt_desc
                    
                    yt_tags = st.text_area(
                        "Tags (uno por línea)", 
                        value="\n".join(current_project["metadata"]["tags"]),
                        height=100
                    )
                    current_project["metadata"]["tags"] = [tag.strip() for tag in yt_tags.split("\n") if tag.strip()]
                    
                    yt_category = st.selectbox(
                        "Categoría",
                        ["Education", "Entertainment", "Science & Technology", "Howto & Style"],
                        index=["Education", "Entertainment", "Science & Technology", "Howto & Style"].index(current_project["metadata"]["category"])
                    )
                    if yt_category != current_project["metadata"]["category"]:
                        current_project["metadata"]["category"] = yt_category
                
                with col2:
                    st.subheader("Miniatura")
                    thumbnail_text = st.text_input(
                        "Texto para miniatura", 
                        value=current_project["metadata"]["thumbnail_text"]
                    )
                    if thumbnail_text != current_project["metadata"]["thumbnail_text"]:
                        current_project["metadata"]["thumbnail_text"] = thumbnail_text
                    
                    st.image(
                        f"https://picsum.photos/800/450?random={current_project['id']}",
                        caption="Miniatura generada (simulada)"
                    )
                    
                    if st.button("Regenerar miniatura"):
                        st.warning("Funcionalidad simulada")
                
                # Opciones de exportación
                st.subheader("Exportación")
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.download_button(
                        "Descargar metadata",
                        data=str(current_project["metadata"]),
                        file_name=f"{current_project['title']}_metadata.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("Simular subida a YouTube", use_container_width=True):
                        with st.spinner("Subiendo a YouTube..."):
                            time.sleep(3)
                            st.success("¡Video subido a YouTube con éxito! (Simulado)")
                            current_project["status"] = "uploaded"

# Barra de estado en el pie de página
st.divider()
st.caption(f"VideoGen AI - Proyecto: {st.session_state.current_project_id[:8] if st.session_state.current_project_id else 'Ninguno'}")

# Guardar estado del proyecto actual
if st.session_state.current_project_id:
    # En una aplicación real, aquí guardarías los datos en Firebase o localmente
    pass

def main():
    # Sidebar navigation
    st.sidebar.title("Navegación")
    page = st.sidebar.radio(
        "Selecciona una página",
        ["Generador de Videos", "Configuración", "Historial"]
    )
    
    if page == "Generador de Videos":
        batch_generator.show_batch_generator()
    elif page == "Configuración":
        settings.show_settings()
    elif page == "Historial":
        history.show_history()

if __name__ == "__main__":
    main()