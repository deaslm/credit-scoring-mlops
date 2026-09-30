"""
Test unitaire : verifie la fonction predict() de maniere isolée, sans passer par l'API.
"""
from app.model import load_model,load_feature_names,predict


def test_predict_retourne_une_probabilite_valide():
    """
    Une probabilité est toujours un nombre entre 0 et 1 par definition, on verifie que la fonction respecte cette contrainte,
    independamment de l'API qui l'appelle.
    """
    model = load_model()
    feature_names = load_feature_names()
    proba = predict(model, feature_names, {"AMT_INCOME_TOTAL": 100000.0})

    assert isinstance(proba, float)
    assert 0.0 <= proba <= 1.0