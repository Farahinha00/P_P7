# Utilise une image Python officielle
FROM python:3.9

# Définit le répertoire de travail dans le conteneur
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copie les fichiers de l'application dans le conteneur
COPY . ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
