"""
Chargement du modele de scoring credit.

Le modele a été entrainé et enregistré avec MLflow lors du projet précédent (algo LightGBM, cf. notebooks). On utilise le flavor natif mlflow.lightgbm
pour avoir accès a predict_proba, necessaire pour récuperer une vraie probabilité continue.
"""
import json

import mlflow.lightgbm
import numpy as np

MODEL_PATH = "models/credit_scoring_lightgbm"
FEATURE_NAMES_PATH = "models/feature_names.json"


def load_model():
    """Charge le modele depuis le disque. Appelé une seule fois au demarrage."""
    model = mlflow.lightgbm.load_model(MODEL_PATH)
    return model


def load_feature_names():
    """Charge la liste des 839 features, une seule fois au demarrage (évite de relire ce fichier à chaque appel de predict()"""
    with open(FEATURE_NAMES_PATH) as f:
        return json.load(f)


def predict(model, feature_names: list, features: dict) -> float:
    """
    Calcule la probabilite de défaut pour un client. Quel est le risque que le client ne paye pas?
    Optimisation (etape 4) : utilise un array NumPy plutot qu'un DataFrame
    pandas pour construire l'entree du modele -> gain mesure de 84.6% sur
    le temps d'inference (cf. notebooks/optimisation_performance.ipynb).
    """
    valeurs = [features.get(name, np.nan) for name in feature_names]     # conserve les valeurs envoyées, NaN pour celles manquantes
    X = np.array([valeurs])                                              # tableau 2D : 1 ligne, len(feature_names) colonnes

    proba = model.predict_proba(X)                                       # calcul et renvoie la proba de défaut de paiment
    return float(proba[0, 1])