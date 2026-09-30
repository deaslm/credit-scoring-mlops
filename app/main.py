"""
API FastAPI de credit scoring.

Le modele est chargé un seule fois au démarrage de l'API (variable `model`), puis réutilisé pour toutes les requetes.
"""
import time

from fastapi import FastAPI, HTTPException

from app.model import load_model, load_feature_names, predict
from app.schemas import PredictionRequest, PredictionResponse
from app.logging_utilities import log_prediction

app = FastAPI(title="API FastAPI de credit scoring")

# Chargement du modèle et liste des features au démarrage du serveur (pas à chaque requete)
model = load_model()
feature_names = load_feature_names()


@app.get("/health")
def health_check():
    """
    Endpoint de santé : verifie que l'API tourne et que le modele est bien chargé.
    """
    return {
        "status": "ok",
        "model_loaded": model is not None,
    }


@app.post("/predict", response_model=PredictionResponse)                 # FastAPI valide la sortie
def predict_endpoint(request: PredictionRequest):                        # FastAPI valide l'entrée et éxecute la fonction
    """Endpoint de prédiction : calcule un score à partir des données d'un client"""

    debut = time.perf_counter()                                          # marque le début, pour mesurer la latence
    erreur_survenue = None                                               # valeur initiale. Sera remplacée si une erreur est survenue dans le try

    try:
        proba = predict(model, feature_names, request.features)          # renvoi une proba selon la feature recue lors de la requete
        decision = "refuse" if proba >= 0.5 else "accorde"               # traduit la proba en décision metier, selon le seuil optimal (0.5).
    except Exception as e:
        erreur_survenue = str(e)                                         # message d'erreur lisible, pour le log
        proba = None
        decision = None

    latence_ms = (time.perf_counter() - debut) * 1000                    # temps ecoulé en millisecondes, erreur ou pas

    log_prediction(
        sk_id_curr=request.sk_id_curr,
        features_recues=request.features,
        probability=proba,
        decision=decision,
        latency_ms=latence_ms,
        error=erreur_survenue,
    )

    if erreur_survenue:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul du score.")

    return PredictionResponse(                                           # retourne la réponse au format valide
        sk_id_curr=request.sk_id_curr,                                   # on renvoie le meme identifiant recu en entrée
        probability_default=proba,                                       # la proba de défaut de paiment calculée
        decision=decision,                                               # la décision finale
    )