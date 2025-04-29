import streamlit as st
from utils.overlays import OverlayManager
from typing import List, Tuple, Optional

def show_overlays_ui() -> List[Tuple[str, float, float, Optional[float]]]:
    """
    Muestra la interfaz de usuario para seleccionar overlays.
    
    Returns:
        Lista de tuplas (nombre_overlay, opacidad, tiempo_inicio, duración)
    """
    st.header("🎨 Overlays de Video")
    
    # Inicializar el gestor de overlays
    overlay_manager = OverlayManager()
    available_overlays = overlay_manager.get_available_overlays()
    
    if not available_overlays:
        st.warning("No se encontraron overlays en la carpeta 'overlays'. Por favor, añade algunos archivos de video.")
        return []
    
    # Selección de overlays
    selected_overlays = st.multiselect(
        "Selecciona los overlays a aplicar",
        options=available_overlays,
        default=[],
        help="Puedes seleccionar múltiples overlays que se aplicarán en secuencia"
    )
    
    # Opacidad global para todos los overlays
    opacity = st.slider(
        "Opacidad de los overlays",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1
    )
    
    # Crear secuencia con la misma opacidad para todos los overlays
    overlay_sequence = [(name, opacity, 0, None) for name in selected_overlays]
    
    return overlay_sequence 