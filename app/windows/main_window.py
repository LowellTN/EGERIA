from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLineEdit, QPushButton, QScrollArea)
from PySide6.QtCore import Qt, QThread, QTimer

from controllers.chat import ChatBot
from components.chat_message import ChatMessage
from workers.chat_worker import ChatWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chatbot = ChatBot()
        self.worker = None
        self.thread = None
        self.init_ui()
    
    def init_ui(self):
        # Configuration de la fenêtre
        self.setWindowTitle("EGERIA - Assistant")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Zone de chat avec scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Widget contenant les messages
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setSpacing(8)
        self.chat_layout.addStretch()
        self.chat_widget.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.chat_widget)
        
        # Zone de saisie
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Tapez votre message ici...")
        self.message_input.returnPressed.connect(self.send_message)
        
        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        
        # Ajouter au layout principal
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(input_layout)
        
        # Message de bienvenue
        self.add_message("Bonjour ! Je suis EGERIA, votre assistant IA. Comment puis-je vous aider ?", False)
    
    def add_message(self, message, is_user=True):
        """Ajouter un message au chat using ChatMessage component"""
        message_widget = ChatMessage(message, is_user, self)
        
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message_widget)

        QTimer.singleShot(10, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """Scroll to bottom of chat"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        """Envoyer un message"""
        message = self.message_input.text().strip()
        if not message:
            return
        
        # Ajouter le message de l'utilisateur
        self.add_message(message, True)
        
        # Vider le champ de saisie
        self.message_input.clear()
        
        # Désactiver le bouton pendant l'envoi
        self.send_button.setEnabled(False)
        self.send_button.setText("Envoi en cours...")
        
        # Créer le thread worker pour l'API
        self.thread = QThread()
        self.worker = ChatWorker(self.chatbot, message)
        self.worker.moveToThread(self.thread)
        
        # Connecter les signaux
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_response_received)
        self.worker.error.connect(self.on_error_received)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        # Démarrer le thread
        self.thread.start()
    
    def on_response_received(self, response):
        """Callback quand la réponse API est reçue"""
        # Ajouter la réponse de l'assistant
        self.add_message(response, False)
        
        # Réactiver le bouton
        self.send_button.setEnabled(True)
        self.send_button.setText("Envoyer")
        
        # Remettre le focus sur l'input
        self.message_input.setFocus()
    
    def on_error_received(self, error_message):
        """Callback en cas d'erreur"""
        self.add_message(f"Erreur: {error_message}", False)
        
        # Réactiver le bouton
        self.send_button.setEnabled(True)
        self.send_button.setText("Envoyer")
        self.message_input.setFocus()
    
    
    ### Fonction de Copilot (A revoir)
    def resizeEvent(self, event):
        """Handle window resize to update message widths"""
        super().resizeEvent(event)
        self.update_all_message_styles()
    
    def update_all_message_styles(self):
        """Update styles for all chat messages""" 
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, ChatMessage):
                    widget.update_style()
