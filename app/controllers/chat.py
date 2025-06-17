import warnings
import os 
import time
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import re

# Cacher les warnings de dépréciations
warnings.filterwarnings("ignore", category=DeprecationWarning)

class ChatBot:
    def __init__(self):
        # Récupération de la clé API
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Création du client
        self.client = OpenAI(api_key=openai_api_key)
        
        # Création d'un thread
        self.thread = self.client.beta.threads.create()
        
        # Envoyer l'horodatage initial
        self._send_timestamp()
    
    def _send_timestamp(self):
        debut_session = datetime.now()
        jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        mois = ["janvier", "février", "mars", "avril", "mai", "juin",
                "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        
        jour_nom = jours[debut_session.weekday()]
        jour = debut_session.day
        mois_nom = mois[debut_session.month - 1]
        annee = debut_session.year
        heure = debut_session.strftime("%H:%M")
        
        horodatage = f"Nous sommes le {jour_nom} {jour} {mois_nom} {annee}, à l'heure {heure}."
        
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="assistant",
            content=horodatage
        )
    
    def send_message(self, message_utilisateur):
        try:
            # Ajouter le message utilisateur au thread
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=message_utilisateur
            )
            
            # Lancement de l'assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id="asst_QsDGRra4i0AKvCKgphu7vxHI"
            )
            
            # Attente de l'assistant
            while run.status in ['queued', 'in_progress', 'cancelling']:
                time.sleep(1)
                run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
            
            # Vérification que le run est complété
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                response = messages.data[0].content[0].text.value
                
                # Enlève la citation de l'API
                cleaned_response = self._remove_citations(response)
                return cleaned_response
            else:
                return f"Erreur: {run.status}"
            
        except Exception as e:
            return f"Erreur: {str(e)}"

    def _remove_citations(self, text):
        """Remove citation references like 【5:11†filename.json】"""
        # Recherche la  citations sous ce format : 【number:number†filename】
        citation_pattern = r'【\d+:\d+†[^】]+】'
        cleaned_text = re.sub(citation_pattern, '', text)
        
        # Enlève les espaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        return cleaned_text