"""
Dashboard de monitoring de l'API credit scoring.

Affiche les métriques operationnelles (latence, taux d'erreur, distribution des scores) à  partir des logs de production (logs/predictions_log.jsonl),
et donne accès au rapport de data drift généré par Evidently.
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Monitoring - Credit Scoring", layout="wide")

st.title("Monitoring de l'API Credit Scoring")

# Chargement des logs de production. On affiche un message si le fichier n'existe pas encore.
try:
    logs = pd.read_json("logs/predictions_log.jsonl", lines=True)
except (FileNotFoundError, ValueError):
    st.warning("Aucun log trouvé. Lancez d'abord l'API et le script de simulation de trafic.")
    st.stop()

# Métriques cles, affichées en haut du dashboard
col1, col2, col3 = st.columns(3)

taux_erreur = logs["error"].notna().mean() * 100
latence_moyenne = logs["latency_ms"].mean()
nb_requetes = len(logs)

col1.metric("Nombre de requetes", nb_requetes)
col2.metric("Latence moyenne", f"{latence_moyenne:.1f} ms")
col3.metric("Taux d'erreur", f"{taux_erreur:.2f} %")

st.divider()

# Distribution des scores prédits
st.subheader("Distribution des scores prédits")
st.bar_chart(logs["probability_default"].value_counts(bins=20).sort_index())

# Répartition des décisions
st.subheader("Repartition des décisions")
st.bar_chart(logs["decision"].value_counts())

# Latence dans le temps 
st.subheader("Latence des requetes dans le temps")
st.line_chart(logs.set_index("timestamp")["latency_ms"])

st.divider()

# Lien vers le rapport de data drift
st.subheader("Analyse du data drift")
st.write(
    "Le rapport complet de data drift (Evidently) est disponible dans ""`monitoring/rapport_drift.html`,"
    " generé par le notebook ""`notebooks/analyse_monitoring.ipynb`.") 