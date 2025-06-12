import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Définir le chemin vers le sous-dossier "données"
filename = "Planning_EHPAD_Mai_Juin_Complet"
fichier = Path(f"data/{filename}.xlsx")

print(fichier)

# Lire le fichier Excel
df = pd.read_excel(fichier, engine="openpyxl")

# Convertir les colonnes datetime en string
for col in df.select_dtypes(include=['datetime64']).columns:
    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

# Créer une nouvelle structure où "Horaires" est la clé principale
planning_restructure = {}

mois_string = filename.replace("Planning_EHPAD_", "").replace("_Complet", "")

# Séparer les deux mois
mois_liste = mois_string.split("_")


# Parcourir chaque ligne du DataFrame
for _, row in df.iterrows():
    horaire = row.get('Horaires')
    
    # Ignorer les lignes où Horaires est NaN
    if pd.isna(horaire):
        continue
    
    liste_mois = ["Juillet", "aout"]
    
    # Créer un dictionnaire pour cette tranche horaire
    planning_restructure[horaire] = {
        mois_liste[0] : {},
        mois_liste[1] : {}
    }
    
    # Ajouter chaque jour comme enfant
    month_ind = -1
    for col in df.columns:
        if col != 'Horaires' and not pd.isna(row.get(col)):
            day, number = col.split()
            if number == "1":
                month_ind += 1
            planning_restructure[horaire][mois_liste[month_ind]][col] = row.get(col)

# Définir le chemin de sortie
output_path = Path("json")
output_file = output_path / f"planning_EHPAD_{mois_string}.json"

# Créer le dossier de sortie s'il n'existe pas
output_path.mkdir(parents=True, exist_ok=True)

# Custom encoder to handle NaN values
class NaNEncoder(json.JSONEncoder):
    def default(self, obj):
        if pd.isna(obj):
            return None
        return super().default(obj)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(planning_restructure, f, ensure_ascii=False, indent=4, cls=NaNEncoder)

print(f"✅ JSON restructuré créé : {output_file}")
