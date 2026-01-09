#!/usr/bin/env python3

import argparse
import requests
import re

parser=argparse.ArgumentParser(description="Affiche les notes du baccalauréat")
#Description du script 

parser.add_argument("url", help="lien")
#L'argument pris en paramètre, dans notre cas c'est un lien


args=parser.parse_args()

r=requests.get(args.url)
#Pour accéder au texte d'une page web
  
r.encoding="utf-8"#encodage de la réponse 

motif=re.compile(r"motif")
#Module re permet la recherche de motif

matches=motif.finditer(r.text)
#Placement de tous les éléments de l'argument dans un raw string

for elt in matches:
    print(elt.group()) #affichage des éléments recherchés

