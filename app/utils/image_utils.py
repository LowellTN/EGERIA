import re
import os
from pathlib import Path

def extract_image_references(message):
    # Recherche la citation de l'image à afficher par l'assistant
    image_pattern = r'\{([^{}]+\.(png|jpg|jpeg|gif))\}'
    
    # Cherche toutes les occurences
    matches = re.findall(image_pattern, message, re.IGNORECASE)
    
    # Récupère le nom de l'image
    image_names = []
    for match in matches:
        filename = match[0]
        print(filename)
        image_names.append(filename)
    
    # Enlève la référence pour que le message soit propre
    clean_message = re.sub(image_pattern, '', message)
    clean_message = clean_message.strip()
    
    return clean_message, image_names