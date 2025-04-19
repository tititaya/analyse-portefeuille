def generer_synthese(portefeuille, poids_actifs):
    """
    Crée une phrase de synthèse lisible décrivant le portefeuille optimal.

    Args:
        portefeuille (pd.Series): Contient 'Rendement', 'Volatilite'...
        poids_actifs (pd.Series): Poids par actif (ex: AAPL: 0.45)

    Returns:
        str: Phrase synthétique du type "Pour un rendement de X%..."
    """
    synthese = f"Pour un rendement de {portefeuille['Rendement']:.2%} et une volatilité de {portefeuille['Volatilite']:.2%}, "
    synthese += "vous devriez investir "
    parts = [f"{poids:.0%} en {actif}" for actif, poids in poids_actifs.items()]
    synthese += ", ".join(parts) + "."

    return synthese

