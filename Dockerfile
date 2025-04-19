# Utiliser une image légère de Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'app
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port que Railway utilisera
EXPOSE 8501

# Lancer l'application Streamlit avec le port fourni par Railway
CMD sh -c "streamlit run app.py --server.port=$PORT --server.enableCORS=false --server.enableXsrfProtection=false"
