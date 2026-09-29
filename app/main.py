"""
API FastAPI de scoring credit.

Le modele est chargé un seule fois au démarrage de l'API (variable `model`), puis réutilisé pour toutes les requetes : 

"""
from fastapi import FastAPI

from app.model import load_model, predict
from app.schemas import PredictionRequest, PredictionResponse

app = FastAPI(title="API de Scoring Credit")

# Chargement du modèle au démarrage du serveur (pas à chaque requete)
model = load_model()

@app.get("/health")
def health_check():
    """
    Endpoint de santé : verifie que l'API tourne et que le modele est bien chargé.
    """
    return {
        "status": "ok",
        "model_loaded": model is not None,                               # renvoi true si chargé, false sinon
    }

@app.post("/predict", response_model=PredictionResponse)                 # FastAPI valide la sortie
def predict_endpoint(request: PredictionRequest):                        # FastAPI valide l'entrée et éxecute la fonction
    """Endpoint de prédiction : calcule un score à partir des données d'un client""" 
    proba = predict(model, request.features)                             # renvoi une proba selon la feature recue lors de la requete
    decision = "refuse" if proba >= 0.5 else "accorde"                   # traduit la proba en décision metier, selon le seuil optimal (0.5).

    return PredictionResponse(                                           # retourne la réponse au format valide
        sk_id_curr=request.sk_id_curr,                                   # on renvoie le meme identifiant recu en entrée
        probability_default=proba,                                       # la proba de défaut de paiment calculée
        decision=decision,                                               # la décision finale
    )