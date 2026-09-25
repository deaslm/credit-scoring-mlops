"""
Test unitaire : verifie la fonction predict() de maniere isolée, sans passer par l'API.
"""
from app.model import load_model, predict


def test_predict_retourne_une_probabilite_valide():
    """
    Une probabilité est toujours un nombre entre 0 et 1 par definition, on verifie que la fonction respecte cette contrainte,
    independamment de l'API qui l'appelle.
    """
    model = load_model()
    proba = predict(model, {"AMT_INCOME_TOTAL": 100000})

    assert isinstance(proba, float)
    assert 0.0 <= proba <= 1.0