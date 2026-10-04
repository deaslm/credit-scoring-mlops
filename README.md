# Credit Scoring MLOps

Mise en production d'un modèle de credit scoring pour l'entreprise "Prêt à dépenser".

# test demo

## Contexte

Ce projet fait suite au projet "Initiez-vous au MLOps", dans lequel un modèle de scoring (LightGBM) a été entraîné, évalué et versionné avec MLflow (cf. `notebooks/` et `docs/screenshots/`).

L'objectif ici est de déployer ce modèle en production :
- une API de scoring (FastAPI)
- une conteneurisation Docker
- un pipeline CI/CD (GitHub Actions)
- un monitoring du modèle en production (logs, dashboard, détection de data drift)
- une analyse et optimisation des performances d'inférence

## Structure du dépôt
credit-scoring-mlops/
- app/        # code de l'API (FastAPI)
- main.py     # endpoints /health et /predict
- model.py    # chargement du modèle et fonction de prédiction
- schemas.py  # schémas Pydantic (validation)
- logging_utilities.py       # journalisation des prédictions
- tests/      # tests unitaires et d'intégration (pytest)
- models/     # artefacts du modèle MLflow (LightGBM) + liste des features
- data/       # échantillon de référence pour le monitoring
- scripts/    # scripts (échantillon, simulation de trafic)
- monitoring/         # dashboard Streamlit + rapport de data drift
- notebooks/          # notebooks d'analyse (exploration, modélisation, monitoring, optimisation)
- docs/screenshots/   # captures d'écran (MLflow, stockage de production)
- logs/       # logs de production (générés à l'exécution)
- .github/workflows/         # pipeline CI/CD
- Dockerfile
- requirements.txt

## Installation

```bash
python -m venv venv
source venv/Scripts/activate      
pip install -r requirements.txt
```

Le modèle et la liste des features doivent être présents dans `models/credit_scoring_lightgbm/` et `models/feature_names.json`.

## Lancer l'API

**En local :**
```bash
uvicorn app.main:app --reload
```
L'API est accessible sur `http://127.0.0.1:8000`, avec une documentation interactive Swagger sur `http://127.0.0.1:8000/docs`.

**Avec Docker :**
```bash
docker build -t credit-scoring-api .
docker run -p 8000:8000 credit-scoring-api
```

## Utiliser l'API

**Vérifier que l'API tourne :**
```bash
curl http://127.0.0.1:8000/health
```

**Demander un score :**
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sk_id_curr": 12, "features": {"AMT_CREDIT": 40000, "AMT_INCOME_TOTAL": 200000}}'
```
Réponse :
```json
{"sk_id_curr": 12, "probability_default": 0.8168540317419912, "decision": "refuse"}
```
 Le seuil de décision (0.5) correspond au seuil optimal déterminé lors du projet précédent.

## Tests automatisés

```bash
python -m pytest tests/ -v
```
3 tests : 1 test unitaire (validité de la probabilité renvoyée par `predict()`) et 2 tests d'intégration (données obligatoires manquantes, type de donnée incorrect).

## Pipeline CI/CD

À chaque `push` sur `main` (ou pull request), GitHub Actions exécute automatiquement :
1. les tests (`pytest`)
2. la construction de l'image Docker (uniquement si les tests passent)
3. un déploiement simulé (lancement du conteneur + vérification que `/health` répond)

## Monitoring en production

**Stockage** : chaque appel à `/predict` est journalisé dans `logs/predictions_log.jsonl` (format JSON Lines) — timestamp, identifiant client, nombre de features reçues, probabilité prédite, décision, latence, erreur. Ce fichier n'est pas versionné (données générées à l'exécution, voir `.gitignore`).

**Simuler du trafic** (pour générer des logs à analyser) :
```bash
python scripts/traffic_production.py
```
**Analyser le data drift et les anomalies opérationnelles** : notebook `notebooks/analyse_monitoring.ipynb`, qui compare les données d'entraînement (référence) aux données "production" simulées (`dataset_final_test.csv`, jamais vues par le modèle) via la librairie Evidently, et calcule le taux d'erreur, la latence, et la distribution des scores à partir des logs.

**Dashboard :**
```bash
streamlit run monitoring/dashboard.py
```
Affiche en temps réel : nombre de requêtes, latence moyenne, taux d'erreur, distribution des scores prédits, répartition des décisions, latence dans le temps.

## Interprétation des résultats

- **Data drift** : Evidently signale un drift significatif si plus de 50% des features dérivent statistiquement par rapport à la référence. Un pourcentage plus faible (comme observé ici, ~12%) reste normal .
- **Latence anormale** : une requête est considérée comme anormale si elle dépasse la moyenne + 3 écarts-types observés.
- **Taux d'erreur** : proportion de requêtes ayant levé une exception ; un taux élevé indique un problème à investiguer (entrée invalide non gérée, indisponibilité du modèle...).

Captures d'écran de la solution de stockage : `docs/screenshots/stockage_production/`.

## Optimisation des performances

Un profiling (`cProfile`, voir `notebooks/optimisation_performance.ipynb`) a identifié la construction du DataFrame pandas comme principal goulot d'étranglement de `predict()`. Son remplacement par un tableau NumPy réduit le temps d'inférence de **84,6 %** (11,1 ms → 1,7 ms par prédiction), sans aucune régression sur la précision des prédictions (résultats vérifiés identiques). Cette version optimisée est celle actuellement déployée.

## Limites/pistes d'amélioration

- Stockage des logs en fichier local : à remplacer par une base de données pour un usage à fort volume.
- Le drift est mesuré une fois, ponctuellement : un vrai suivi en production nécessiterait un recalcul régulier et des seuils d'alerte automatisés.
- Conformité RGPD : les logs contiennent un identifiant client (`SK_ID_CURR`) ; une politique de rétention et de contrôle d'accès serait nécessaire en production réelle.
