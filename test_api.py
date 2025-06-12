import warnings
import os 
import time
from dotenv import load_dotenv
from openai import OpenAI

# Cacher les warnings de dépréciations : ligne potentiellement à commenter dans le futurs
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Récupération de la clé API
load_dotenv()  # Charge les variables depuis .env

openai_api_key = os.getenv("OPENAI_API_KEY")

# Création du client
client = OpenAI(api_key=openai_api_key)

# Création d'un thread
thread = client.beta.threads.create()

def chat(message_utilisateur):
    # Ajouter le message utilisateur au thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_utilisateur
    )
    
    # Lancement de l'assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_QsDGRra4i0AKvCKgphu7vxHI"  # Your assistant ID
    )
    
    # 3. Attente de l'assitant
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    # 4. Vérification que le run est complété
    if run.status == 'completed':
        # Récupère le message de l'assistant
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        # Renvoi le message de l'assistant
        return messages.data[0].content[0].text.value
    else:
        return f"Error: Run status is {run.status}"



# Test conversation
while True:
    message = input("\nVous : ")
    
    # Conditions pour quitter la conversation
    if message.lower() in ['quit', 'exit', 'bye', 'au revoir', 'stop']:
        print("Assistant : Au revoir ! À bientôt !")
        break
    
    # Si le message est vide, on continue
    if not message.strip():
        continue
    
    try:
        reponse = chat(message)
        print(f"Assistant : {reponse}")
    except Exception as e:
        print(f"Erreur : {e}")
        print("Essayez de nouveau...")