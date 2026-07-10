import streamlit as st
import pandas as pd
from theme import apply_theme


st.set_page_config(
    page_title="About",
    layout="wide"
)



st.title("ℹ️ À propos")

st.write(
    "Cette application permet de prédire le risque de décrochage universitaire "
    "à l'aide d'un modèle de Machine Learning et de visualiser les résultats "
    "à travers un tableau de bord interactif."
)

st.divider()

st.subheader("🎯 Objectif de l'application")

st.write("""
         Cette application a été développée afin de prédire le risque de décrochage Universitaire à partir des informations académiques et personnelles des étudiants. 
         Grâce à un modèle de Machine Learning, elle estime la probabilité qu'un étudiant abandonne ou réussisse son parcours universitaire. 
         En complément de la prédiction, l'application fournit une explication des résultats, un historique des prédictions réalisées 
         ainsi qu'un tableau de bord interactif permettant de suivre les principales statistiques d'utilisation.""")


st.divider()

st.subheader("⚙️ Fonctionnalités")

st.markdown("#### 🔮 Prediction")
st.write("""
         Permet de saisir les informations d'un étudiant afin de prédire son risque de décrochage. 
         L'application affiche la classe prédite, la probabilité associée ainsi qu'une explication des principaux facteurs ayant influencé la décision du modèle grâce à SHAP.
         """)
         
st.markdown("#### 📊 Dashboard")
st.write("""
         Présente des statistiques descriptives du jeu de données ainsi que des indicateurs dynamiques issus de l'historique des prédictions, 
         notamment les distributions, les tendances temporelles et les dernières prédictions enregistrées.
         """)

st.markdown("#### 📜 History")

st.write("""Regroupe l'ensemble des prédictions réalisées par les utilisateurs. Cette page permet de consulter les résultats précédents, 
         triés par date, et d'exporter l'historique au format CSV.
         """)


st.divider()

st.subheader("🤖 Modèle de Machine Learning")

st.write("""
         Le modèle de Machine Learning a été entraîné à partir d'un jeu de données d'étudiants de l'enseignement supérieur. 
         Après le prétraitement des données, le modèle est utilisé pour estimer le risque de décrochage universitaire à partir des informations académiques, démographiques et socio-économiques des étudiants. 
         Les prédictions sont accompagnées d'une explication basée sur SHAP afin d'améliorer leur interprétabilité.
         """)

st.divider()

st.subheader("🛠️ Technologies utilisées")
tech = pd.DataFrame(
    {
        "Technologie": [
            "Python",
            "Streamlit",
            "Scikit-learn",
            "Pandas",
            "Plotly",
            "SQLite",
            "SHAP"
        ],
        "Utilisation": [
            "Développement",
            "Interface utilisateur",
            "Machine Learning",
            "Manipulation des données",
            "Visualisation",
            "Historique des prédictions",
            "Explication des prédictions"
        ]
    }
)

st.dataframe(
    tech,
    width="stretch",
    hide_index=True
)


st.divider()

st.subheader("👨‍💻 Auteur")

st.write("""Nom : Bakary Dembele

Formation : Ingénierie Science des Données et Intelligence Artificielle (ISDIA)

Projet : Student Dropout Prediction

Année : 2025-2026
         
         """)


st.caption("Version 1.0 • Juillet 2026")