#!/usr/bin/env python3
import requests
import os

# URL directe du fichier CSV (resource_id)
csv_url = "https://www.data.gouv.fr/fr/datasets/r/5e662e9b-f033-44fa-9e9a-a5b40fec2cd3"

# Nom du fichier local
filename = "baccalaureat_par_academie.csv"

# Créer le dossier de destination
os.makedirs("Données", exist_ok=True)
print("Téléchargement :", filename)

# Télécharger le fichier
response = requests.get(csv_url)

# Sauvegarder le fichier CSV
with open(f"Données/{filename}", "wb") as f:
    f.write(response.content)

print("Téléchargement terminé.")
