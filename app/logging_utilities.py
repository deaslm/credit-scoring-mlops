"""
Enregistrement structure (JSON Lines) de chaque appel à /predict.

Chaque ligne du fichier logs/predictions_log.jsonl est un objet JSON indépendant (+ facile à recharger plus tard en DataFrame)
"""
import json
import os
from datetime import datetime, timezone

LOG_PATH = "logs/predictions_log.jsonl"


def log_prediction(sk_id_curr, features_recues: dict, probability: float,
                    decision: str, latency_ms: float, error: str = None) -> None:                    #rien à récuperer, on l'appelle juste pour créer le fichier
    """Ajoute une ligne JSON au fichier de logs (mode ("a"=append/jamais ecrasé))."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sk_id_curr": sk_id_curr,
        "nb_features_recues": len(features_recues) if features_recues else 0,
        "probability_default": probability,
        "decision": decision,
        "latency_ms": latency_ms,
        "error": error,
    }

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")