
#!/usr/bin/env python3

import csv
import requests
import json
import urllib.parse

def generer_graphique_juxtapose():
    url_csv = "https://www.data.gouv.fr/api/1/datasets/r/5e662e9b-f033-44fa-9e9a-a5b40fec2cd3"
    response = requests.get(url_csv) # envoi de request http pour récupérer les données depuis internet 
    content = response.content.decode('utf-8') # Décodage du contenu du fichier CSV en UTF-8
    reader = csv.DictReader(content.splitlines(), delimiter=';') # transforme le CSV en lecteur de dictionnaire 

    # le choix des villes 
    villes_cibles = ["PARIS", "LILLE", "LYON", "NANTES", "VERSAILLES"]
    stats = {ville: {"presents": 0, "admis": 0, "refuses": 0} for ville in villes_cibles}

    # Parcour de chaque ligne du fichier cvs afin extraire les statistiques par ville
    for row in reader:
        aca = row.get('Académie', '').strip().upper()
        if aca in villes_cibles: # vérifie si l'académie fait parti des villes séléctionner 
            try:
                #récupération et conversion des valeurs numériques 
                p = int(row.get("Nombre de présents", 0) or 0)
                a = int(row.get("Nombre d'admis totaux", 0) or 0)
                #Calcule et accumulationdes présent, admis et refus 
                stats[aca]["presents"] += p
                stats[aca]["admis"] += a
                stats[aca]["refuses"] += max(0, p - a)
            except: continue
    # Calcule des taux d'admis et d'échec en pourcentage %
    labels = list(stats.keys())
    taux_admis = [round((stats[v]["admis"] / stats[v]["presents"]) * 100, 2) if stats[v]["presents"] > 0 else 0 for v in labels]
    taux_echec = [round((stats[v]["refuses"] / stats[v]["presents"]) * 100, 2) if stats[v]["presents"] > 0 else 0 for v in labels]

    # configuratiion du graphique en barres comparatives
    configuration = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Taux d'Admis (%)",
                    "data": taux_admis,
                    "backgroundColor": "pattern.draw('diagonal', '#1a2a6c')" # JAUNE avec hachures
                },
                {
                    "label": "Taux d'Échec (%)",
                    "data": taux_echec,
                    "backgroundColor": "pattern.draw('diagonal-right-left', '#8B4513')" # ROUGE avec hachures
                }
            ]
        },
        "options": {
            "scales": {
                "xAxes": [{"stacked": False}], # FALSE pour coller les barres côte à côte
                "yAxes": [{"ticks": {"beginAtZero": True, "max": 100}}]
            },
            # le titre du graphique 
            "title": {"display": True, "text": "Comparaison Admis (Jaune) vs Echecs (Rouge) en %"}
        }
    }

    params = urllib.parse.quote(json.dumps(configuration))
    url = f"https://quickchart.io/chart?c={params}&plugin=patterns"
    print(f"\nLien du graphique (Barres collées Jaune/Rouge) :\n{url}")

if __name__ == "__main__":
    generer_graphique_juxtapose()