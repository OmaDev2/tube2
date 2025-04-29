from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.fx import all as vfx
from typing import List, Tuple, Optional
import os
from PIL import Image
import cv2
import numpy as np

class VideoOverlay:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.clip = None
    
    def load(self):
        if not self.clip:
            self.clip = VideoFileClip(self.path)
        return self.clip
    
    def apply(self, base_clip, opacity: float = 1.0, start_time: float = 0, duration: Optional[float] = None):
        overlay = self.load()
        if duration:
            overlay = overlay.subclip(0, duration)
        
        # Función para redimensionar usando cv2
        def resize_frame(frame):
            return cv2.resize(frame, (base_clip.w, base_clip.h), interpolation=cv2.INTER_LINEAR)
        
        # Aplicar redimensionamiento
        overlay = overlay.fl_image(resize_frame)
        
        # Aplicar opacidad
        if opacity < 1.0:
            overlay = overlay.set_opacity(opacity)
        
        # Posicionar en el tiempo
        overlay = overlay.set_start(start_time)
        
        return CompositeVideoClip([base_clip, overlay])

class OverlayManager:
    def __init__(self, overlays_dir: str = "overlays"):
        self.overlays_dir = overlays_dir
        self.overlays = {}
        self._load_overlays()
    
    def _load_overlays(self):
        if not os.path.exists(self.overlays_dir):
            os.makedirs(self.overlays_dir)
            return
        
        for filename in os.listdir(self.overlays_dir):
            if filename.endswith(('.mp4', '.mov', '.avi')):
                name = os.path.splitext(filename)[0]
                path = os.path.join(self.overlays_dir, filename)
                self.overlays[name] = VideoOverlay(name, path)
    
    def get_available_overlays(self) -> List[str]:
        return list(self.overlays.keys())
    
    def apply_overlays(self, base_clip, overlay_sequence: List[Tuple[str, float, float, Optional[float]]]) -> VideoFileClip:
        """
        Aplica una secuencia de overlays al video base.
        
        Args:
            base_clip: Video base al que aplicar los overlays
            overlay_sequence: Lista de tuplas (nombre_overlay, opacidad, tiempo_inicio, duración)
        
        Returns:
            VideoFileClip con los overlays aplicados
        """
        result = base_clip
        for overlay_name, opacity, start_time, duration in overlay_sequence:
            if overlay_name in self.overlays:
                overlay = self.overlays[overlay_name]
                result = overlay.apply(result, opacity, start_time, duration)
        return result 