import io
import pandas as pd

def generer_csv(poids_actifs):
    """
    Génère un fichier CSV en mémoire à partir des poids d'actifs.

    Args:
        poids_actifs (pd.Series): Série avec les actifs en index et les poids en valeurs.

    Returns:
        BytesIO: Flux binaire du CSV prêt à être téléchargé.
    """
    df = pd.DataFrame(poids_actifs.rename("Poids"))
    df["Poids"] = df["Poids"].apply(lambda x: round(x, 4))

    buffer = io.BytesIO()
    buffer.write(df.to_csv().encode("utf-8"))
    buffer.seek(0)

    return buffer
