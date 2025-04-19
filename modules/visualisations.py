import matplotlib.pyplot as plt
import seaborn as sns

def afficher_courbe_prix(prix):
    plt.figure(figsize=(12, 5))
    plt.plot(prix)
    plt.title("Évolution des prix ajustés")
    plt.xlabel("Date")
    plt.ylabel("Prix ($)")
    plt.legend(prix.columns)
    plt.grid(True)
    plt.tight_layout()
    return plt

def afficher_matrice_correlation(rendements):
    corr = rendements.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Corrélation entre les actifs")
    plt.tight_layout()
    return plt
