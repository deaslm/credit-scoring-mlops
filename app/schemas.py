"""
Schemas Pydantic : definissent la forme attendue des donnees echangées avec l'API. FastAPI s'en sert pour valider automatiquement
les requetes et générer la réponse/la documentation Swagger.
"""
from typing import Dict, Optional

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """Requete de scoring d'un client."""

    sk_id_curr: Optional[int] = None                     # ce champs peut etre soit un entier soit vide si on veut juste calculer un score sans id.
    features: Dict[str, float]                           # la clé doit etre du texte(nom feature) et la valeur un nombre


class PredictionResponse(BaseModel):
    """Reponse renvoyee par l'API apres scoring."""

    sk_id_curr: Optional[int]
    probability_default: float
    decision: str