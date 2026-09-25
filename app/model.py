"""
Chargement du modele de scoring credit.

Le modele a été entrainé et enregistré avec MLflow lors du projet précédent (algo LightGBM, cf. notebooks). On utilise le flavor natif mlflow.lightgbm
pour avoir accès a predict_proba, necessaire pour récuperer une vraie probabilité continue.
"""
import mlflow.lightgbm


MODEL_PATH = "models/credit_scoring_lightgbm"


def load_model():
    """Charge le modele depuis le disque. Appelé une seule fois au demarrage."""
    model = mlflow.lightgbm.load_model(MODEL_PATH)
    return model


def predict(model, features: dict) -> float:
    """
    Calcule la probabilite de defaut pour un client. Quel est le risque que le client ne paye pas?
    `features` est un dictionnaire {nom_feature: valeur}. Il n'est pas necessaire de fournir les 839 features du modele : les colonnes
    manquantes sont completées automatiquement avec NaN.
    """
    import json

    import numpy as np
    import pandas as pd

    with open("models/feature_names.json") as f:
        feature_names = json.load(f)                                             # charge la liste des 839 features

    row = {name: features.get(name, np.nan) for name in feature_names}           # conserve les valeurs envoyées et complete les manquantes par NaN
    df = pd.DataFrame([row], columns=feature_names)

    proba = model.predict_proba(df)                                              # calcul et renvoie la proba de défaut de paiment
    return float(proba[0, 1])