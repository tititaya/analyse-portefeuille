import yfinance as yf
import pandas as pd

def telecharger_donnees(tickers, date_debut, date_fin, intervalle="1d"):
    tickers = [t.strip().upper() for t in tickers if t.strip() != ""]
    if not tickers:
        print("Aucun ticker valide fourni.")
        return pd.DataFrame()

    try:
        donnees = yf.download(
            tickers=tickers[0] if len(tickers) == 1 else tickers,
            start=date_debut,
            end=date_fin,
            interval=intervalle,
            group_by='ticker',
            auto_adjust=False,
            progress=False
        )

        if donnees.empty:
            print("Aucune donnée reçue de Yahoo Finance.")
            return pd.DataFrame()

        # Cas 1 : plusieurs tickers → MultiIndex
        if isinstance(donnees.columns, pd.MultiIndex):
            try:
                prix = donnees.loc[:, (slice(None), 'Adj Close')]
                prix.columns = prix.columns.get_level_values(0)
                return prix
            except Exception as e:
                print("Erreur extraction 'Adj Close' multi-ticker :", e)
                return pd.DataFrame()

        # Cas 2 : un seul ticker → colonnes simples
        elif 'Adj Close' in donnees.columns:
            return donnees[['Adj Close']].rename(columns={"Adj Close": tickers[0]})
        else:
            print("'Adj Close' introuvable")
            return pd.DataFrame()

    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return pd.DataFrame()
