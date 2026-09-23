# Credit Scoring MLOps

Mise en production d'un modele de scoring credit pour l'entreprise "Pret à dépenser".

## Contexte

Ce projet fait suite au projet "Initiez-vous au MLOps", dans lequel un modele de scoring (LightGBM) a ete entrainé, evalué et versionné avec MLflow (cf. `notebooks/` et `docs/screenshots/`).

L'objectif ici est de déployer ce modele en production :
- une API de scoring (FastAPI)
- une conteneurisation Docker
- un monitoring du modele en production (dashboard + detection de data drift)
- un pipeline CI/CD

## Structure du projet

- `notebooks/` : notebooks d'analyse et de modélisation (projet de base)
- `models/` : artefacts du modele MLflow (LightGBM)
- `data/` : échantillon de référence pour le monitoring
- `scripts/` : scripts pour generer l'échantillon de référance
- `docs/` : documentation et captures d'ecran
