#!/usr/bin/env python3

import csv #module permettant de traiter les fichier csv
import requests #module permettant de lancer une requête HTTP vers une URL et de récupérer la réponse
import json  #module permettant de manipuler des données au format JSON
import urllib.parse #module permettant d'analyser les URL

def generer_graphique_juxtapose():
    # Fonction principale qui récupère les données, les traite
    # et génère un graphique comparatif
    url_csv = "https://www.data.gouv.fr/api/1/datasets/r/5e662e9b-f033-44fa-9e9a-a5b40fec2cd3" 
    #l'url du csv à traiter
    response = requests.get(url_csv) 
    # pour accéder au texte de la page web
    response.raise_for_status()

    reader = csv.DictReader(response.text.splitlines(), delimiter=';')
    #permet de convertir le fichier csv  en dictionnaire

    villes_cibles = ["PARIS", "LILLE", "LYON", "NANTES", "VERSAILLES"] 
    #liste des académies à étudier

    stats = {v: {"presents": 0, "admis": 0, "refuses": 0} for v in villes_cibles}
    #création du dictionnaire contenant les statistique
    #les clés : les villes à étudier
    #les valeurs : un dictionnaire contenant le nombre de participants présents, admis et refusés

    for row in reader:
        # Parcours de chaque ligne du fichier CSV

        ville = row.get("Académie", "").strip().upper()
        # Récupération du nom de l’académie
        # strip() enlève les espaces
        # upper() met en majuscules pour éviter les erreurs de comparaison

        if ville in villes_cibles:
            # Traitement des villes sélectionnées

            try:
                presents = int(row.get("Nombre de présents") or 0)
                # Conversion du nombre de présents en entier

                admis = int(row.get("Nombre d'admis totaux") or 0)
                # Conversion du nombre d’admis en entier

                stats[ville]["presents"] += presents
                # Ajout du nombre de présents à la ville correspondante

                stats[ville]["admis"] += admis
                # Ajout du nombre d’admis

                stats[ville]["refuses"] += max(0, presents - admis)
                # Calcul du nombre de refusés
                # max(0, ...) évite les valeurs négatives

            except ValueError:
                # Ignore les lignes contenant des valeurs non numériques
                pass

    labels = list(stats.keys())
    # Liste des villes (utilisée pour l’axe des abscisses)

    taux_admis = [
        round(stats[v]["admis"] / stats[v]["presents"] * 100, 2)
        if stats[v]["presents"] else 0
        for v in labels
    ]
    # Calcul du taux d’admission (%) pour chaque académies
    # Arrondi à 2 décimales
    # Si aucun présent, le taux est 0

    taux_echec = [
        round(stats[v]["refuses"] / stats[v]["presents"] * 100, 2)
        if stats[v]["presents"] else 0
        for v in labels
    ]
    # Calcul du taux d’échec (%) pour chaque ville

    configuration = {
        "type": "bar",
        # Type de graphique : diagramme en barres

        "data": {
            "labels": labels,
            # Noms des villes sur l’axe X

            "datasets": [
                {
                    "label": "Taux d'Admis (%)",
                    "data": taux_admis,
                    # Données du taux d’admission
                    "backgroundColor": "pattern.draw('diagonal', '#FFD700')"
                    # Couleur dorée avec motif diagonal
                },
                {
                    "label": "Taux de refus (%)",
                    "data": taux_echec,
                    # Données du taux d’échec
                    "backgroundColor": "pattern.draw('diagonal-right-left', '#B22222')"
                    # Couleur rouge foncé avec motif
                }
            ]
        },

        "options": {
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "beginAtZero": True,
                        "max": 100
                    }
                }]
            },
            # Axe vertical de 0 à 100 %

            "title": {
                "display": True,
                "text": "Comparaison des taux d'admission et d'échec (%)"
            }
            # Titre du graphique
        }
    }

    chart_json = json.dumps(configuration)
    # Conversion de la configuration en JSON

    chart_url = "https://quickchart.io/chart?c=" + urllib.parse.quote(chart_json) + "&plugin=patterns"
    # Génération de l’URL du graphique via QuickChart

    print("\n📊 Lien du graphique :")
    print(chart_url)
    # Affichage du lien du graphique

if __name__ == "__main__":
    # Point d’entrée du programme
    generer_graphique_juxtapose()
