from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip, ImageClip,
    concatenate_videoclips, CompositeVideoClip, CompositeAudioClip,
    concatenate_audioclips
)
from moviepy.video.fx import all as vfx
from moviepy.audio.fx import all as afx
from utils.efectos import EfectosVideo
from utils.transitions import TransitionEffect
import os
from typing import List, Union, Optional

class VideoServices:
    def __init__(self):
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_video_from_images(
        self,
        images: List[str],
        duration_per_image: float = 3.0,
        transition_duration: float = 1.0,
        transition_type: str = 'dissolve',
        background_music: Optional[AudioFileClip] = None,
        text: Optional[str] = None,
        text_position: str = 'bottom',
        text_color: str = 'white',
        text_size: int = 30,
        effects_sequence: Optional[List[tuple]] = None
    ) -> str:
        """Crea un video a partir de imágenes con transiciones y efectos."""
        clips = []
        
        for i, image_path in enumerate(images):
            # Crear clip de imagen
            clip = ImageClip(image_path, duration=duration_per_image)
            
            # Aplicar efecto si se proporciona
            if effects_sequence:
                effect_index = i % len(effects_sequence)
                effect_name, effect_params = effects_sequence[effect_index]
                clip = EfectosVideo.apply_effect(clip, effect_name, **effect_params)
            
            # Aplicar texto si se proporciona
            if text:
                txt_clip = TextClip(text, fontsize=text_size, color=text_color)
                txt_clip = txt_clip.set_position(text_position).set_duration(duration_per_image)
                clip = CompositeVideoClip([clip, txt_clip])
            
            clips.append(clip)
        
        # Aplicar transiciones entre clips
        final_clip = TransitionEffect.apply_transition(
            clips, 
            transition_type=transition_type,
            transition_duration=transition_duration
        )
        
        # Añadir música de fondo si se proporciona
        if background_music:
            if final_clip.duration > background_music.duration:
                # Repetir la música si es más corta que el video
                while background_music.duration < final_clip.duration:
                    background_music = concatenate_audioclips([background_music, background_music])
                background_music = background_music.subclip(0, final_clip.duration)
            final_clip = final_clip.set_audio(background_music)
        
        # Generar nombre de archivo único
        output_path = self._get_unique_output_path()
        
        # Guardar el video
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        return output_path
    
    def add_text_to_video(
        self,
        video_path: str,
        text: str,
        position: str = "bottom",
        font_size: int = 24,
        color: str = "white",
        output_name: str = "video_with_text.mp4"
    ) -> str:
        """
        Añade texto a un video existente.
        
        Args:
            video_path: Ruta al video original
            text: Texto a añadir
            position: Posición del texto ('top', 'bottom', 'center')
            font_size: Tamaño de la fuente
            color: Color del texto
            output_name: Nombre del archivo de salida
            
        Returns:
            str: Ruta al video con texto
        """
        video = VideoFileClip(video_path)
        
        # Crear clip de texto
        txt_clip = TextClip(
            text,
            fontsize=font_size,
            color=color,
            bg_color='transparent'
        )
        
        # Posicionar el texto
        if position == "top":
            txt_clip = txt_clip.set_position(('center', 'top'))
        elif position == "bottom":
            txt_clip = txt_clip.set_position(('center', 'bottom'))
        else:
            txt_clip = txt_clip.set_position('center')
        
        # Combinar video y texto
        final_clip = video.set_mask(txt_clip)
        
        # Guardar el resultado
        output_path = os.path.join(self.output_dir, output_name)
        final_clip.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        
        return output_path
    
    def apply_effect(
        self,
        video_path: str,
        effect: str,
        output_name: str = "video_with_effect.mp4"
    ) -> str:
        """
        Aplica un efecto al video.
        
        Args:
            video_path: Ruta al video original
            effect: Nombre del efecto a aplicar
            output_name: Nombre del archivo de salida
            
        Returns:
            str: Ruta al video con el efecto aplicado
        """
        video = VideoFileClip(video_path)
        
        # Aplicar el efecto
        if effect == "fadein":
            video = vfx.fadein(video, duration=1.0)
        elif effect == "fadeout":
            video = vfx.fadeout(video, duration=1.0)
        elif effect == "mirror_x":
            video = vfx.mirror_x(video)
        elif effect == "mirror_y":
            video = vfx.mirror_y(video)
        
        # Guardar el resultado
        output_path = os.path.join(self.output_dir, output_name)
        video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac'
        )
        
        return output_path

    def create_video(self, images, audio, text):
        # Lógica para crear video usando las nuevas características de MoviePy 2.0
        # Mejor manejo de clips y efectos
        pass
    
    def edit_video(self, video_path, edits):
        # Lógica para editar video usando las nuevas características
        # Mejor rendimiento y más opciones de edición
        pass
    
    def add_effects(self, clip, effects):
        # Nuevo sistema de efectos en MoviePy 2.0
        for effect in effects:
            clip = effect(clip)
        return clip

    def _get_unique_output_path(self):
        # Implementa la lógica para obtener un nombre de archivo único
        # Este es un ejemplo básico, puedes mejorarlo según tus necesidades
        return os.path.join(self.output_dir, f"video_{len(os.listdir(self.output_dir))}.mp4") 