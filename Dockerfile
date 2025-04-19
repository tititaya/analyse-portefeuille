# Étape 1 : image de base
FROM python:3.11-slim

# Étape 2 : définir le répertoire de travail
WORKDIR /app

# Étape 3 : copier les fichiers nécessaires dans le conteneur
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Étape 4 : définir le port utilisé par Streamlit
EXPOSE 8501

# Étape 5 : lancer l'application Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
