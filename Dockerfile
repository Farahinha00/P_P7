# Utilise une image Python officielle
FROM python:3.9

# Définit le répertoire de travail dans le conteneur
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copie les fichiers de l'application dans le conteneur
COPY . ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port (optionnel pour Azure mais bon pour la pratique)
EXPOSE 8000

# Remplacez la ligne ci-dessous par la commande appropriée pour votre application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
