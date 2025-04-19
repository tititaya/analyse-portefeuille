import numpy as np
import pandas as pd

def simuler_portefeuilles(rendements, nb_portefeuilles=5000, taux_sans_risque=0.01):
    """
    Simule un ensemble de portefeuilles aléatoires en répartissant des poids
    sur les actifs donnés. Calcule le rendement, la volatilité et le Sharpe ratio
    pour chacun d'eux.

    Paramètres :
    - rendements : DataFrame des rendements quotidiens des actifs
    - nb_portefeuilles : nombre de simulations à effectuer
    - taux_sans_risque : utilisé pour le calcul du Sharpe ratio (par défaut 1%)

    Retour :
    - DataFrame contenant les performances et pondérations de chaque portefeuille simulé
    """

    np.random.seed(42)  # pour reproductibilité

    nb_actifs = len(rendements.columns)
    poids_portefeuilles = []
    rendements_attendus = []
    volatilites = []
    ratios_sharpe = []

    moyennes = rendements.mean()
    cov = rendements.cov()

    for _ in range(nb_portefeuilles):
        poids = np.random.random(nb_actifs)
        poids /= np.sum(poids)

        rendement = np.dot(poids, moyennes) * 252
        volatilite = np.sqrt(np.dot(poids.T, np.dot(cov * 252, poids)))
        sharpe = (rendement - taux_sans_risque) / volatilite

        poids_portefeuilles.append(poids)
        rendements_attendus.append(rendement)
        volatilites.append(volatilite)
        ratios_sharpe.append(sharpe)

    data = {
        'Rendement': rendements_attendus,
        'Volatilite': volatilites,
        'Sharpe': ratios_sharpe
    }

    for i, nom in enumerate(rendements.columns):
        data[nom] = [poids[i] for poids in poids_portefeuilles]

    df = pd.DataFrame(data)

    # Ajout de la colonne ID pour identification simple
    df["ID"] = df.index

    return df
