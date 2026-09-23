"""
Extrait un petit echantillon du dataset d'entrainement complet, pour servir de donnees de reference au monitoring du data drift.

On ne charge pas tout le fichier en memoire (car lourd/1.4 Go) : on ne lit que les 1000 premieres lignes.
"""
import pandas as pd

# Chemin
SOURCE_PATH = "C:/Users/yavas/credit_scoring/donnees/traitees/dataset_final_train.csv"
OUTPUT_PATH = "data/reference_sample.csv"

df = pd.read_csv(SOURCE_PATH, nrows=1000)

# On ne garde que les features (pas la cible)
if "TARGET" in df.columns:
    df = df.drop(columns=["TARGET"])

df.to_csv(OUTPUT_PATH, index=False)
print(f"Echantillon sauvegarde : {df.shape[0]} lignes, {df.shape[1]} colonnes.")