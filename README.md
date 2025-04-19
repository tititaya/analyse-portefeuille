![CI/CD](https://github.com/tititaya/analyse-portefeuille/actions/workflows/main.yml/badge.svg)

# 📊 Analyse de portefeuilles boursiers

Cette application Streamlit interactive permet de :
- Visualiser les données historiques des actions
- Simuler des portefeuilles optimaux (rendement, risque, Sharpe)
- Comparer plusieurs portefeuilles (internes ou chargés)
- Suivre en temps réel la performance du portefeuille optimal avec alertes

---

## 🚀 Fonctionnalités

### 1. Simulation de portefeuille
- Téléchargement automatique des données via `yfinance`
- Calculs de rendements, corrélations, et ratios de Sharpe
- Génération de milliers de portefeuilles simulés
- Affichage graphique interactif (rendement vs risque)

### 2. Comparateur de portefeuilles
- Sélection de portefeuilles à comparer
- Chargement de portefeuilles personnalisés (CSV)
- Comparaison des performances (rendement, risque, Sharpe)
- Graphiques d’allocation et comparaison de rendements

### 3. Suivi temps réel & alertes
- Suivi automatique du portefeuille optimal
- Alerte visuelle et sonore si le rendement cumulé chute sous un seuil défini
- Actualisation automatique toutes les 60 secondes

---

## 📁 Structure du projet

```
.
├── app.py                     # Point d'entrée principal
├── requirements.txt          # Dépendances Python
├── Dockerfile                # Image Docker de l'app
├── docker-compose.yml        # Lancement simplifié avec Docker Compose
├── .streamlit/
│   └── config.toml           # Configuration du thème Streamlit
├── data/
│   ├── tickers.csv
│   ├── tickers_par_secteur.json
│   ├── raw_prices.csv
│   └── alerte.mp3
├── modules/
│   ├── analyse.py
│   ├── simulation.py
│   ├── visualisations.py
│   ├── telechargement.py
│   ├── suivi.py
│   └── comparateur.py
├── services/
│   ├── export.py
│   └── utils.py
└── .github/workflows/
    └── docker.yml            # Workflow CI/CD GitHub Actions
```

---

## 🛠️ Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/<utilisateur>/analyse-portefeuille.git
cd analyse-portefeuille

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate       # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

---

## 🐳 Utilisation avec Docker

### Docker CLI

```bash
docker build -t analyse-portefeuille .
docker run -p 8501:8501 analyse-portefeuille
```

### Docker Compose

```bash
docker-compose up --build
```

---

## 🔁 Déploiement CI/CD (GitHub Actions)

Un workflow CI/CD est inclus pour :
- Construire l'image Docker
- La pousser automatiquement sur Docker Hub

### Secrets GitHub à définir :

| Clé               | Description                       |
|-------------------|-----------------------------------|
| `DOCKER_USERNAME` | Identifiant Docker Hub            |
| `DOCKER_TOKEN`    | Token d’accès personnel Docker    |

---

## 📄 Format CSV attendu pour import

```csv
Ticker,Poids
AAPL,0.25
MSFT,0.25
GOOGL,0.25
TSLA,0.25
```

---

## 📌 À venir

- Déploiement sur Render, Railway, ou HuggingFace Spaces
- Analyse fondamentale (ratios financiers)
- Gestion multi-utilisateur

---

## 📃 Licence

Ce projet est distribué sous licence [MIT](https://opensource.org/licenses/MIT).

---

## 🤝 Contribuer

Toute contribution est la bienvenue !  
N'hésitez pas à :
- Ouvrir une *issue*
- Proposer une *pull request*

---

## 🚀 Déploiement

L'application est hébergée en ligne sur [Railway](https://railway.app/).

[![Déploiement Railway](https://img.shields.io/badge/Railway-app-green?logo=railway&style=flat-square)](https://analyse-portefeuille.up.railway.app)

👉 Accédez à l'application : [https://analyse-portefeuille.up.railway.app](https://analyse-portefeuille.up.railway.app)


## 👨‍💻 Auteur

Projet développé par **[@tititaya](https://github.com/tititaya)**
