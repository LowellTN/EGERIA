import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Définir le chemin vers le sous-dossier "données"
filename = "Planning_Personnalisé_Nathalie_Mai_Juin"
fichier = Path(f"data/{filename}.xlsx")

# Lire le fichier Excel
df = pd.read_excel(fichier, engine="openpyxl")

# Convertir les colonnes datetime en string
for col in df.select_dtypes(include=['datetime64']).columns:
    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

# Créer une nouvelle structure où le jour est la clé principale, puis le mois, puis l'horaire
planning_par_jour = {}

mois_string = filename.replace("Planning_Personnalisé_Nathalie_", "")
print(f"Extracted months: {mois_string}")

# Séparer les deux mois
mois_liste = mois_string.split("_")
print(f"Month list: {mois_liste}")

# D'abord, créer la structure pour les jours et les mois
days_by_month = {}
for col in df.columns:
    if col != 'Horaires':
        try:
            day, number = col.split()
            
            # Déterminer le mois
            month_index = 0 if int(number) <= 31 else 1
            month_name = mois_liste[month_index]
            
            # Initialiser la structure si nécessaire
            if col not in planning_par_jour:
                planning_par_jour[col] = {}
            
        except ValueError:
            print(f"Colonne ignorée: {col}")

# Parcourir chaque ligne du DataFrame pour remplir les activités
for _, row in df.iterrows():
    horaire = row.get('Horaires')
    
    # Ignorer les lignes où Horaires est NaN
    if pd.isna(horaire):
        continue
    
    # Ajouter les activités pour chaque jour
    for col in df.columns:
        if col != 'Horaires':
            try:
                day, number = col.split()
                
                # Déterminer le mois
                month_index = 0 if int(number) <= 31 else 1
                month_name = mois_liste[month_index]
                
                # Récupérer la valeur de la cellule
                cell_value = row.get(col)
                
                # Si la cellule est vide/NaN, mettre "Pas d'activité"
                if pd.isna(cell_value) or cell_value == "":
                    activity = "Pas d'activité"
                else:
                    activity = cell_value
                
                # Initialiser la structure si nécessaire
                if col not in planning_par_jour:
                    planning_par_jour[col] = {}
                
                # Ajouter l'activité
                planning_par_jour[col][horaire] = activity
                
            except ValueError:
                # Si la colonne ne peut pas être splitée (pas un jour), l'ignorer
                pass
            except IndexError:
                # Si month_index dépasse les limites de mois_liste
                print(f"Erreur d'index pour la colonne: {col}")

# Regrouper par mois
planning_final = {
    mois_liste[0]: {},
    mois_liste[1]: {}
}

mois_index = -1
for jour_complet, activites in planning_par_jour.items():
    jour, numero = jour_complet.split()
    if int(numero) != 0:
        if int(numero) == 1:
            mois_index += 1
        mois = mois_liste[mois_index]
        
        # Ajouter à la structure finale
        planning_final[mois][jour_complet] = activites

# Définir le chemin de sortie
output_path = Path("data/json")
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
    json.dump(planning_final, f, ensure_ascii=False, indent=4, cls=NaNEncoder)

print(f"✅ JSON restructuré par jour créé : {output_file}")