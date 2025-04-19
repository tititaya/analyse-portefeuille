import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import datetime

def afficher_suivi_temps_reel(portefeuille_optimal, rendements, tickers, seuil=-0.01):
    """
    Affiche le rendement cumulé du portefeuille optimal avec :
    - un graphique interactif Plotly
    - un résumé textuel clair
    - une alerte sonore si seuil franchi
    - une mise à jour automatique toutes les 60 secondes
    """

    # Rafraîchissement automatique toutes les 60 secondes
    st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)

    poids = portefeuille_optimal[tickers].values
    rendements_recents = rendements.tail(60)

    if rendements_recents.empty or len(rendements_recents) < 2:
        st.warning("Pas assez de données récentes pour le suivi.")
        return

    # Calcul du rendement cumulé
    rendement_portefeuille = rendements_recents @ poids
    rendement_cumule = (1 + rendement_portefeuille).cumprod() - 1
    rendement_df = pd.DataFrame({
        "Rendement cumulé (%)": rendement_cumule.values * 100
    }, index=rendement_cumule.index)

    # Affichage du graphique interactif
    st.subheader("Suivi en temps réel (interactif avec Plotly)")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=rendement_df.index,
        y=rendement_df["Rendement cumulé (%)"],
        mode="lines+markers",
        name="Rendement cumulé",
        line=dict(color="blue"),
        marker=dict(size=6)
    ))

    fig.add_hline(
        y=seuil * 100,
        line=dict(color="red", dash="dash"),
        annotation_text=f"Seuil d'alerte ({seuil:.2%})",
        annotation_position="bottom right"
    )

    fig.update_layout(
        yaxis_title="Rendement cumulé (%)",
        xaxis_title="Date",
        title="Suivi en temps réel du portefeuille optimal",
        hovermode="x unified",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Dernier rendement
    dernier_rendement = rendement_df["Rendement cumulé (%)"].iloc[-1]
    derniere_date = rendement_df.index[-1].strftime("%d/%m/%Y")

    st.markdown(f"**Dernier rendement cumulé : {dernier_rendement:.2f}%**")
    st.markdown(f"**Date du dernier point : {derniere_date}**")

    # Heure actuelle
    st.caption(f"Suivi mis à jour le {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Alerte seuil
    if dernier_rendement / 100 < seuil:
        st.error(f"Alerte : le rendement est passé sous {seuil:.2%}")
        audio_path = "data/alerte.mp3"
        if os.path.exists(audio_path):
            st.audio(audio_path, format="audio/mp3")
