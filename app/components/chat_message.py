from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from utils.image_utils import extract_image_references

class ChatMessage(QWidget):
    """Widget pour afficher un message dans le chat"""
    def __init__(self, message, is_user=True, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.message, self.image_paths = extract_image_references(message)
        self.is_user = is_user
        self.message_frame = None
        self.message_label = None
        self.image_labels = []
        
        self.init_ui(self.message, is_user)
    
    def init_ui(self, message, is_user):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Créer une frame pour contenir le message
        self.message_frame = QFrame()
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        
        # Créer le label du message
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignTop)
        self.message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Permet de sélectionner le texte ( surtout pour débugger)
        self.message_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        
        # Ajoute le label dans la frame
        frame_layout.addWidget(self.message_label)
        self.message_frame.setLayout(frame_layout)
        
        if self.image_paths:
            for img_path in self.image_paths:
                # Créer un QLabel pour l'image
                image_label = QLabel()
                image_label.setAlignment(Qt.AlignCenter)
                                
                # Charger l'image
                pixmap = QPixmap(img_path)

                # Gestion des erreurs d'affichage de l'image
                if pixmap.isNull():
                    print(f"Failed to load image: {img_path}")
                    image_label.setText(f"❌ Image not found:Failed to load image: {img_path}")
                    image_label.setStyleSheet("""
                        QLabel {
                            background-color: #ffeeee;
                            color: #990000;
                            border: 1px solid #ffcccc;
                            border-radius: 5px;
                            padding: 10px;
                        }
                    """)
                else:
                    # Ajuste la taille des images trop grandes (TO CHANGE)
                    if pixmap.width() > 300 or pixmap.height() > 300:
                        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    image_label.setPixmap(pixmap)
                    
                    image_label.setStyleSheet("""
                        QLabel {
                            background-color: white;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                            padding: 5px;
                        }
                    """)
                
                # Add the image to the vertical layout
                frame_layout.addWidget(image_label)
                self.image_labels.append(image_label)  # Store reference
        
        self.update_style()
        
        if is_user:
            layout.addStretch(1)  # Espace à gauche
            layout.addWidget(self.message_frame, 4)  
        else:
            layout.addWidget(self.message_frame, 4)  
            layout.addStretch(1)  # Espace à Droite
        
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        
        

    def update_style(self):
        if self.main_window and self.message_frame and self.message_label:
            window_width = self.main_window.width()
            max_width = int(window_width * 0.8)  # 80% maximum
            min_width = int(window_width * 0.3)  # 30% minimum
            
            # Gérer la taille
            self.message_frame.setMaximumWidth(max_width)
            self.message_frame.setMinimumWidth(min_width)
            
            # Créer la "bulle" de dialogue
            self.message_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {'#007ACC' if self.is_user else '#CCEBD3'};
                    border-radius: 15px;
                    padding: 2px;
                }}
            """)
            
            # Style pour le texte
            self.message_label.setStyleSheet(f"""
                QLabel {{
                    background-color: transparent;
                    color: {'white' if self.is_user else 'black'};
                    padding: 12px 15px;
                    font-size: 20px;
                    line-height: 1.4;
                    border: none;
                }}
            """)