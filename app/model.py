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
    Calcule la probabilite de défaut de paiment pour un client.

    `features` est un dictionnaire {nom_feature: valeur}. On le transforme en DataFrame (format attendu par le modele), puis on recupere la probabilité
    de la classe 1 (défaut de paiement / quel est le risque que le client ne paye pas ?).
    """
    import pandas as pd

    df = pd.DataFrame([features])
    proba = model.predict_proba(df)
    return float(proba[0, 1])