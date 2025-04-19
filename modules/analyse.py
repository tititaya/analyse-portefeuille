import pandas as pd
import numpy as np

def calculer_rendements(prix):
    """
    Calcule les rendements journaliers à partir des prix ajustés.

    Args:
        prix (pd.DataFrame): Données de prix ajustés par actif.

    Returns:
        pd.DataFrame: Rendements journaliers (% de variation).
    """
    rendements = prix.pct_change()
    rendements = rendements.dropna()
    return rendements

def calculer_rendement_annuel(rendements):
    """
    Calcule le rendement annualisé moyen pour chaque actif.

    Args:
        rendements (pd.DataFrame): Rendements quotidiens.

    Returns:
        pd.Series: Rendement annualisé moyen par actif.
    """
    return rendements.mean() * 252

def calculer_statistiques_portefeuille(poids, rendements, taux_sans_risque=0.0):
    """
    Calcule les performances d’un portefeuille :
    - Rendement annualisé
    - Volatilité annualisée
    - Ratio de Sharpe

    Args:
        poids (pd.Series ou np.ndarray): Pondérations des actifs.
        rendements (pd.DataFrame): Rendements quotidiens des actifs.
        taux_sans_risque (float): Taux sans risque annuel (par défaut 0.0)

    Returns:
        dict: {
            "rendement": rendement annuel attendu,
            "volatilite": volatilité annuelle,
            "sharpe": ratio de Sharpe
        }
    """
    moyenne = rendements.mean()
    covariance = rendements.cov()

    rendement_annuel = np.dot(poids, moyenne) * 252
    volatilite_annuelle = np.sqrt(np.dot(poids.T, np.dot(covariance * 252, poids)))
    sharpe = (rendement_annuel - taux_sans_risque) / volatilite_annuelle if volatilite_annuelle != 0 else 0

    return {
        "rendement": rendement_annuel,
        "volatilite": volatilite_annuelle,
        "sharpe": sharpe
    }
