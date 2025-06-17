# EGERIA
EGERIA est un projet d'application utilisant un agent conversationnel dans le cadre de l'accompagnement des personnes agées en EHPAD.


## Setup Instructions:

1. Clone the repository
2. Create a virtual environment: `python -m venv env`
3. Activate it: `source env/bin/activate` (Linux/Mac) or `env\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your OpenAI API key (see below)
6. Run: `python app/main.py`

## Environment Setup:

Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your_api_key_here
```

## How to build:

```bash
cd /home/lowell/projets/EGERIA/
pyinstaller --onefile \
            --windowed \
            --name "EGERIA" \
            --paths="./app" \
            --hidden-import="windows.main_window" \
            --hidden-import="components.chat_message" \
            --hidden-import="workers.chat_worker" \
            --hidden-import="controllers.chat" \
            app/main.py
```
