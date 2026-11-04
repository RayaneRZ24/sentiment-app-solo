"""Interface Streamlit (TP5) : elle appelle l'API, jamais le modèle.

Lancer, API déjà démarrée dans un autre terminal : streamlit run ui/app.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # pour importer ui.client

import pandas as pd
import streamlit as st

from ui import client, graphiques

st.set_page_config(page_title="Analyse de sentiment")
st.set_option("client.toolbarMode", "minimal")
st.set_option("client.showErrorDetails", False)
st.title("Analyse de sentiment des avis")
st.caption("Classez vos avis en positifs, négatifs ou à vérifier.")

session = client.creer_session()
etat = client.sante(session)
if etat.ok:
    st.caption("Service d’analyse disponible.")
else:
    st.error(etat.message)

onglet_avis, onglet_lot = st.tabs(["Un avis", "Un fichier d'avis"])

with onglet_avis:
    texte = st.text_area("Avis client")
    if st.button("Analyser"):
        reponse = client.predire(session, texte)
        if reponse.ok and reponse.label is not None and reponse.score is not None:
            st.metric(client.VERDICTS[reponse.label], f"{reponse.score:.0%}")
            if reponse.label == "INDETERMINE":
                st.info("La confiance est sous le seuil d'abstention : un humain doit trancher.")
        elif reponse.message == client.REFUS:
            st.warning(reponse.message)
        else:
            st.error(reponse.message)

with onglet_lot:
    fichier = st.file_uploader("Fichier CSV avec une colonne text", type="csv")
    if fichier is not None:
        try:
            avis = pd.read_csv(fichier)
        except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError):
            st.warning("Fichier illisible : utilisez un CSV UTF-8 avec une colonne text.")
            st.stop()
        if "text" not in avis.columns:
            st.error("Colonne text absente du fichier.")
        else:
            reponses = client.predire_lot(session, avis["text"].astype(str).tolist())
            avis["verdict"] = [client.VERDICTS[r.label] if r.ok and r.label else r.message for r in reponses]
            avis["confiance"] = [r.score for r in reponses]
            st.dataframe(avis, use_container_width=True)
            compte = graphiques.repartition(reponses)["avis"]
            st.caption(f"{compte['positif']} positifs · {compte['négatif']} négatifs · "
                       f"{compte['à vérifier']} à vérifier · {compte['refus ou erreur']} refus ou erreurs")
            colonne_verdicts, colonne_confiances = st.columns(2)
            colonne_verdicts.caption("Répartition des verdicts")
            colonne_verdicts.bar_chart(graphiques.repartition(reponses))
            colonne_confiances.caption("Confiance du modèle, par tranche")
            colonne_confiances.bar_chart(graphiques.histogramme_confiances(reponses))
            st.download_button("Télécharger les résultats", avis.to_csv(index=False),
                               file_name="resultats.csv", mime="text/csv")
