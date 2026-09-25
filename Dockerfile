# Plus léger, rend le build plus rapide et limage finale plus petite.
FROM python:3.12-slim                                         

# Dossier de travail à l'intérieur du conteneur : toutes les commandes suivantes s'éxécutent depuis ce dossier.
WORKDIR /app              

# Installe la librairie (libgomp), nécessaire à LightGBM. Absente de l'image "slim" par defaut.
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# On copie d'abord requirements.txt et on installe les dépéndances avant de copier le reste pour que Docker mette en cache chaque étape.
COPY requirements.txt .                                       
RUN pip install --no-cache-dir -r requirements.txt

# On copie le reste du code nécessaire a l'éxécution de l'API.
COPY app/ app/                                                
COPY models/ models/

# Documente le port utilisé par l'API.
EXPOSE 8000                                                  

# Commande executée au démarrage du conteneur : lance le serveur uvicorn.
# --host 0.0.0.0 pour que l'API soit accessible depuis l'éxterieur du conteneur et pas seulement depuis l'intérieur de celui-ci.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]     
