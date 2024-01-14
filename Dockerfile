# Utilise une image Python officielle
FROM python:3.12

# Définit le répertoire de travail
WORKDIR /app

# Copie le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers de l'application dans le conteneur
COPY . .

# Commande pour lancer l'application
CMD ["python", "app.py"]

