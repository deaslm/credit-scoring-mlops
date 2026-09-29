"""
Trafic de production : envoie plusieurs requetes à l'API /predict en utilisant les clients de dataset_final_test.csv 
(jamais vus par le modele à aucune étape).

Chaque appel génère une ligne dans logs/predictions_log.jsonl, ce qui nous donne un vrai jeu de données à analyser.
"""
import json

import pandas as pd
import requests

SOURCE_PATH = "C:/Users/yavas/credit_scoring/donnees/traitees/dataset_final_test.csv"
API_URL = "http://127.0.0.1:8000/predict"                        # l'API doit déjà tourner en local (uvicorn) avant de lancer ce script
NB_CLIENTS = 200                                                 # nombre de clients (lignes) à envoyer à l'API

feature_names = json.load(open("models/feature_names.json"))     # liste des 839 features

df = pd.read_csv(SOURCE_PATH, nrows=NB_CLIENTS)                  # charge seulement les 200 premières lignes, pas tout le fichier

for _, ligne in df.iterrows():                                    # parcourt chaque client (ligne) un par un
    sk_id_curr = int(ligne["SK_ID_CURR"])                         
    features = ligne[feature_names].to_dict()                     

    payload = {"sk_id_curr": sk_id_curr, "features": features}    # le corps de la requete, au format attendu par l'API
    reponse = requests.post(API_URL, json=payload)                # envoie la requete à /predict

    if reponse.status_code != 200:                                # signale si une requete échoue
        print(f"Erreur pour le client {sk_id_curr} : {reponse.status_code}")

print(f"{NB_CLIENTS} requetes envoyées.")                        # confirmation finale, une fois toutes les requetes traitées