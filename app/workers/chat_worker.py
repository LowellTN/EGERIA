from PySide6.QtCore import QObject, Signal

class ChatWorker(QObject):
    """Worker thread pour les appels API non-bloquants"""
    finished = Signal(str)
    error = Signal(str)
    
    def __init__(self, chatbot, message):
        super().__init__()
        self.chatbot = chatbot
        self.message = message
    
    def run(self):
        try:
            response = self.chatbot.send_message(self.message)
            self.finished.emit(response)
        except Exception as e:
            self.error.emit(str(e))