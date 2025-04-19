import pandas as pd

def comparer_portefeuilles(pf1, pf2, rendements, taux_sans_risque=0.0):
    """
    Compare deux portefeuilles en termes de :
    - Poids par actif
    - Rendement attendu
    - Volatilité
    - Ratio de Sharpe

    Paramètres :
    - pf1, pf2 : Series pandas avec les poids des actifs
    - rendements : DataFrame des rendements
    - taux_sans_risque : taux d’intérêt sans risque (par défaut 0.0)

    Retour :
    - DataFrame avec :
      * Poids 1, Poids 2, Différence
      * Rendement_1, Rendement_2
      * Volatilite_1, Volatilite_2
      * Sharpe_1, Sharpe_2
    """
    diff = pf1 - pf2

    # Calcul des rendements attendus annuels
    moyenne_rendements = rendements.mean()
    rendement1 = (pf1 * moyenne_rendements).sum() * 252
    rendement2 = (pf2 * moyenne_rendements).sum() * 252

    # Calcul des volatilités annuelles
    cov = rendements.cov() * 252
    volatilite1 = (pf1 @ cov @ pf1) ** 0.5
    volatilite2 = (pf2 @ cov @ pf2) ** 0.5

    # Ratios de Sharpe
    sharpe1 = (rendement1 - taux_sans_risque) / volatilite1 if volatilite1 != 0 else 0
    sharpe2 = (rendement2 - taux_sans_risque) / volatilite2 if volatilite2 != 0 else 0

    # Création du tableau de comparaison
    comparaison = pd.DataFrame({
        "Poids 1": pf1,
        "Poids 2": pf2,
        "Différence": diff
    })

    # Ajout des statistiques en une seule ligne
    comparaison["Rendement_1"] = round(rendement1, 4)
    comparaison["Rendement_2"] = round(rendement2, 4)
    comparaison["Volatilite_1"] = round(volatilite1, 4)
    comparaison["Volatilite_2"] = round(volatilite2, 4)
    comparaison["Sharpe_1"] = round(sharpe1, 4)
    comparaison["Sharpe_2"] = round(sharpe2, 4)

    return comparaison
