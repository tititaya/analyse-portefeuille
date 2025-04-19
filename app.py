import streamlit as st
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import json
import os

from modules.telechargement import telecharger_donnees
from modules.analyse import calculer_rendements
from modules.visualisations import afficher_courbe_prix, afficher_matrice_correlation
from modules.simulation import simuler_portefeuilles
from modules.comparateur import comparer_portefeuilles
from services.export import generer_csv
from services.utils import generer_synthese
from modules.suivi import afficher_suivi_temps_reel

st.set_page_config(page_title="Analyse de portefeuille", layout="wide")

# Chargement des tickers
with open("data/tickers_par_secteur.json", "r", encoding="utf-8") as f:
    tickers_par_secteur = json.load(f)
df_tickers = pd.read_csv("data/tickers.csv")

# Interface
st.markdown("<h1 style='text-align: center;'>Analyse de portefeuille boursier</h1>", unsafe_allow_html=True)
st.markdown("Visualisez les actions, simulez des portefeuilles et suivez votre rendement en temps réel.")

with st.sidebar:
    st.header("Paramètres")
    secteur = st.selectbox("Choisissez un secteur", list(tickers_par_secteur.keys()))
    tickers_input = st.text_input("Tickers", ", ".join(tickers_par_secteur[secteur]))
    st.markdown("---")
    mot_cle = st.text_input("Recherche (nom, secteur, ticker)").lower()
    st.dataframe(df_tickers[df_tickers.apply(lambda r: mot_cle in str(r).lower(), axis=1)] if mot_cle else df_tickers)

    date_debut = st.date_input("Date de début", datetime.date(2022, 1, 1))
    date_fin = st.date_input("Date de fin", datetime.date.today())
    nb_portefeuilles = st.slider("Nombre de portefeuilles simulés", 1000, 20000, 5000, step=1000)
    seuil_alerte = st.number_input("Seuil d'alerte (%)", min_value=-100.0, max_value=100.0, value=-1.0, step=0.5) / 100
    suivi_en_temps_reel = st.checkbox("Activer le suivi temps réel du portefeuille optimal")
    analyser = st.button("Analyser")

col1, col2 = st.columns([0.05, 0.95])
with col2:
    if analyser or ("prix" in st.session_state and "tickers" in st.session_state):
        if analyser:
            tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
            prix = telecharger_donnees(tickers, str(date_debut), str(date_fin))
            rendements = calculer_rendements(prix)
            df_simul = simuler_portefeuilles(rendements, nb_portefeuilles)

            st.session_state.update({
                "tickers": tickers,
                "prix": prix,
                "rendements": rendements,
                "df_simul": df_simul
            })

        tickers = st.session_state.tickers
        prix = st.session_state.prix
        rendements = st.session_state.rendements
        df_simul = st.session_state.df_simul

        if prix.empty:
            st.warning("Aucune donnée récupérée.")
        else:
            st.subheader("1. Données de marché")
            st.pyplot(afficher_courbe_prix(prix))

            st.subheader("2. Corrélation entre les actifs")
            st.pyplot(afficher_matrice_correlation(rendements))

            st.subheader("3. Simulation de portefeuilles")
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = ax.scatter(df_simul["Volatilite"], df_simul["Rendement"], c=df_simul["Sharpe"], cmap='viridis', alpha=0.6)
            ax.set_title("Portefeuilles simulés (rendement vs risque)")
            ax.set_xlabel("Volatilité")
            ax.set_ylabel("Rendement attendu")
            plt.colorbar(scatter, ax=ax, label="Sharpe")
            st.pyplot(fig)

            st.subheader("4. Portefeuille optimal")
            pf_opt = df_simul.loc[df_simul["Sharpe"].idxmax()]
            st.markdown(f"- Rendement : {pf_opt['Rendement']:.2%}")
            st.markdown(f"- Volatilité : {pf_opt['Volatilite']:.2%}")
            st.markdown(f"- Sharpe : {pf_opt['Sharpe']:.2f}")
            poids_opt = pf_opt[tickers]
            st.dataframe(poids_opt.rename("Poids").apply(lambda x: f"{x:.2%}"))
            st.info(generer_synthese(pf_opt, poids_opt))
            st.download_button("Télécharger (CSV)", generer_csv(poids_opt), "portefeuille_optimal.csv", "text/csv")

            st.subheader("5. Portefeuille minimum risque")
            pf_min = df_simul.loc[df_simul["Volatilite"].idxmin()]
            st.markdown(f"- Rendement : {pf_min['Rendement']:.2%}")
            st.markdown(f"- Volatilité : {pf_min['Volatilite']:.2%}")
            st.markdown(f"- Sharpe : {pf_min['Sharpe']:.2f}")
            poids_min = pf_min[tickers]
            st.dataframe(poids_min.rename("Poids").apply(lambda x: f"{x:.2%}"))

            st.subheader("6. Comparateur de portefeuilles")
            id1 = st.selectbox("ID portefeuille 1", df_simul["ID"], index=0)
            id2 = st.selectbox("ID portefeuille 2", df_simul["ID"], index=1)

            try:
                pf1 = df_simul[df_simul["ID"] == id1].iloc[0][tickers]
                pf2 = df_simul[df_simul["ID"] == id2].iloc[0][tickers]

                comp = comparer_portefeuilles(pf1, pf2, rendements)

                st.markdown("**Poids comparés par actif :**")
                comp_display = pd.DataFrame({
                    "Poids 1": comp["Poids 1"],
                    "Poids 2": comp["Poids 2"],
                    "Différence": comp["Différence"]
                })
                st.dataframe(comp_display.style.format("{:.2%}"))


                st.markdown("**Résumé des performances :**")
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Rendement portefeuille 1", f"{comp['Rendement_1'].iloc[0]*100:.2f} %")
                    st.metric("Volatilité portefeuille 1", f"{comp['Volatilite_1'].iloc[0]*100:.2f} %")
                    st.metric("Sharpe portefeuille 1", f"{comp['Sharpe_1'].iloc[0]:.2f}")

                with col2:
                    st.metric("Rendement portefeuille 2", f"{comp['Rendement_2'].iloc[0]*100:.2f} %")
                    st.metric("Volatilité portefeuille 2", f"{comp['Volatilite_2'].iloc[0]*100:.2f} %")
                    st.metric("Sharpe portefeuille 2", f"{comp['Sharpe_2'].iloc[0]:.2f}")

            except IndexError:
                st.warning("Impossible de récupérer un des portefeuilles sélectionnés.")

            st.subheader("Charger un portefeuille externe")
            file = st.file_uploader("CSV (Ticker, Poids)", type=["csv"])
            if file:
                try:
                    df_ext = pd.read_csv(file)
                    pf_ext = pd.Series(df_ext.Poids.values, index=df_ext.Ticker.str.upper())
                    for t in tickers:
                        if t not in pf_ext:
                            pf_ext[t] = 0
                    pf_ext = pf_ext[tickers]
                    comp_ext = comparer_portefeuilles(pf_ext, pf_opt[tickers], rendements)
                    st.dataframe(comp_ext)
                except Exception as e:
                    st.error(f"Erreur : {e}")

            if suivi_en_temps_reel:
                st.subheader("7. Suivi temps réel du portefeuille optimal")
                afficher_suivi_temps_reel(pf_opt, rendements, tickers, seuil=seuil_alerte)
