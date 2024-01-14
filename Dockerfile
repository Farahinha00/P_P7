# Utilise une image Python officielle
FROM python:3.12

# Définit le répertoire de travail dans le conteneur
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copie les fichiers de l'application dans le conteneur
COPY . ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande pour lancer l'application avec Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
