import re
import os
import sys

def extract_image_references(message):
    """
    Extract image references from message and convert them to absolute file paths.
    
    Args:
        message (str): The message containing image references
        
    Returns:
        tuple: (clean_message, absolute_image_paths)
    """
    # Recherche la citation de l'image à afficher par l'assistant
    image_pattern = r'\{([^{}]+\.(png|jpg|jpeg|gif))\}'
    
    # Cherche toutes les occurences
    matches = re.findall(image_pattern, message, re.IGNORECASE)
    
    # Détermine le chemin de base du projet
    # Gestion différente selon qu'on est dans un bundle PyInstaller ou en développement
    if getattr(sys, 'frozen', False):
        # Si on est dans un bundle PyInstaller
        project_root = sys._MEIPASS
    else:
        # Si on est en développement
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    assets_folder = os.path.join(project_root, "assets", "images")
    
    # Récupère le chemin absolu complet de l'image
    image_paths = []
    for match in matches:
        filename = match[0]
        image_path = os.path.join(assets_folder, filename)
        image_paths.append(image_path)
    
    # Enlève la référence pour que le message soit propre
    clean_message = re.sub(image_pattern, '', message)
    clean_message = clean_message.strip()
    
    return clean_message, image_paths