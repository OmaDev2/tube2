import streamlit as st
import os
from utils.video_services import VideoServices
from pages.efectos_ui import show_effects_ui
from moviepy.editor import AudioFileClip
from utils.transitions import TransitionEffect

def show_batch_generator():
    st.title("🎥 Generador de Videos")
    
    # Inicializar el servicio de video
    video_service = VideoServices()
    
    # Sección 1: Cargar imágenes
    st.header("1. Cargar Imágenes")
    uploaded_images = st.file_uploader(
        "Selecciona las imágenes para el video",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    
    if not uploaded_images:
        st.warning("Por favor, carga al menos una imagen.")
        return
    
    # Sección 2: Configuración del video
    st.header("2. Configuración del Video")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        duration_per_image = st.slider(
            "Duración por imagen (segundos)",
            min_value=1.0,
            max_value=10.0,
            value=3.0,
            step=0.5
        )
    
    with col2:
        transition_duration = st.slider(
            "Duración de la transición (segundos)",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1
        )
    
    with col3:
        transition_type = st.selectbox(
            "Tipo de transición",
            options=TransitionEffect.get_available_transitions(),
            format_func=lambda x: "Sin transición" if x == "none" else "Disolución" if x == "dissolve" else x
        )
    
    # Sección 3: Efectos
    st.header("3. Efectos")
    effects_sequence = show_effects_ui()
    
    # Sección 4: Audio
    st.header("4. Audio (Opcional)")
    background_music = st.file_uploader(
        "Música de fondo",
        type=["mp3", "wav"],
        accept_multiple_files=False
    )
    
    # Sección 5: Texto
    st.header("5. Texto (Opcional)")
    text = st.text_area("Texto a mostrar en el video")
    if text:
        col1, col2, col3 = st.columns(3)
        with col1:
            text_position = st.selectbox(
                "Posición del texto",
                ["top", "center", "bottom"]
            )
        with col2:
            text_color = st.color_picker("Color del texto", "#FFFFFF")
        with col3:
            text_size = st.slider(
                "Tamaño del texto",
                min_value=10,
                max_value=100,
                value=30
            )
    
    # Botón para generar el video
    if st.button("Generar Video"):
        with st.spinner("Generando video..."):
            # Guardar imágenes temporalmente
            temp_images = []
            for uploaded_file in uploaded_images:
                temp_path = os.path.join("temp", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                temp_images.append(temp_path)
            
            # Procesar música de fondo si se proporciona
            background_music_clip = None
            if background_music:
                temp_audio = os.path.join("temp", background_music.name)
                with open(temp_audio, "wb") as f:
                    f.write(background_music.getbuffer())
                background_music_clip = AudioFileClip(temp_audio)
            
            # Crear el video
            output_path = video_service.create_video_from_images(
                images=temp_images,
                duration_per_image=duration_per_image,
                transition_duration=transition_duration,
                transition_type=transition_type,
                background_music=background_music_clip,
                text=text if text else None,
                text_position=text_position if text else 'bottom',
                text_color=text_color if text else 'white',
                text_size=text_size if text else 30,
                effects_sequence=effects_sequence
            )
            
            # Limpiar archivos temporales
            for temp_file in temp_images:
                os.remove(temp_file)
            if background_music:
                os.remove(temp_audio)
            
            # Mostrar el video generado
            st.video(output_path)
            
            # Proporcionar enlace de descarga
            with open(output_path, "rb") as f:
                st.download_button(
                    "Descargar Video",
                    f,
                    file_name=os.path.basename(output_path),
                    mime="video/mp4"
                ) 