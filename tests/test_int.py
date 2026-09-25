"""
Tests d'integration de l'API de scoring credit.

On utilise TestClient (fourni par FastAPI), qui simule des appels HTTP directement en memoire, sans lancer de vrai serveur uvicorn.
on teste toute la chaine :  route HTTP + validation Pydantic + appel au modele + reponse.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_predict_champ_features_absent():
    """
    Teste des entrées avec des données manquantes pour des champs obligatoires. 
    'features' est obligatoire dans PredictionRequest : une requete qui l'omet doit etre rejetée par Pydantic.
    renvoi 422 = code pour une requete qui ne respecte pas le schema.
    """
    payload = {"sk_id_curr": 100002}                      # pas de "features" du tout ici
    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_predict_type_incorrect_dans_features():
    """
    Teste des types de donnees incorrects (ex: du texte la où un chiffre est attendu)". 
    Le schema declare features: Dict[str, float] : une valeur textuelle doit etre rejetee.
    """
    payload = {"features": {"AMT_INCOME_TOTAL": "beaucoup"}}
    response = client.post("/predict", json=payload)

    assert response.status_code == 422