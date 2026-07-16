import streamlit as st
import pandas as pd
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]   # streamlit_app/
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from assets.styles.theme import apply_theme
from assets.styles.components import (
    render_sidebar,
    render_sidebar_footer,
    page_header,
    section_title,
    feature_card,
    render_data_table,
    render_author_card,
)

st.set_page_config(page_title="About", page_icon="🎓", layout="wide")

apply_theme()
render_sidebar()

page_header(
    title="ℹ️ À propos",
    eyebrow="Documentation",
    subtitle="Cette application permet de prédire le risque de décrochage universitaire "
             "à l'aide d'un modèle de Machine Learning et de visualiser les résultats "
             "à travers un tableau de bord interactif.",
)

# ------------------------------------------------------------------
# Objectif de l'application
# ------------------------------------------------------------------
with st.container(border=True):
    section_title("🎯", "Objectif de l'application")
    st.write(
        "Cette application a été développée afin de prédire le risque de décrochage "
        "universitaire à partir des informations académiques et personnelles des "
        "étudiants. Grâce à un modèle de Machine Learning, elle estime la probabilité "
        "qu'un étudiant abandonne ou réussisse son parcours universitaire. En "
        "complément de la prédiction, l'application fournit une explication des "
        "résultats, un historique des prédictions réalisées ainsi qu'un tableau de "
        "bord interactif permettant de suivre les principales statistiques d'utilisation."
    )

st.write("")

# ------------------------------------------------------------------
# Fonctionnalités
# ------------------------------------------------------------------
with st.container(border=True):
    section_title("⚙️", "Fonctionnalités")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        feature_card(
            "🔮",
            "Prediction",
            "Permet de saisir les informations d'un étudiant afin de prédire son "
            "risque de décrochage. L'application affiche la classe prédite, la "
            "probabilité associée ainsi qu'une explication des principaux facteurs "
            "ayant influencé la décision du modèle grâce à SHAP.",
            badge="blue",
        )

    with col2:
        feature_card(
            "📊",
            "Dashboard",
            "Présente des statistiques descriptives du jeu de données ainsi que des "
            "indicateurs dynamiques issus de l'historique des prédictions, notamment "
            "les distributions, les tendances temporelles et les dernières "
            "prédictions enregistrées.",
            badge="purple",
        )

    with col3:
        feature_card(
            "🕐",
            "History",
            "Regroupe l'ensemble des prédictions réalisées par les utilisateurs. "
            "Cette page permet de consulter les résultats précédents, triés par "
            "date, filtrés par filière ou résultat, et d'exporter l'historique au "
            "format CSV.",
            badge="sky",
        )

st.write("")

# ------------------------------------------------------------------
# Modèle de Machine Learning
# ------------------------------------------------------------------
with st.container(border=True):
    section_title("🤖", "Modèle de Machine Learning")
    st.write(
        "Le modèle de Machine Learning a été entraîné à partir d'un jeu de données "
        "d'étudiants de l'enseignement supérieur. Après le prétraitement des "
        "données, le modèle est utilisé pour estimer le risque de décrochage "
        "universitaire à partir des informations académiques, démographiques et "
        "socio-économiques des étudiants. Les prédictions sont accompagnées d'une "
        "explication basée sur SHAP afin d'améliorer leur interprétabilité."
    )

st.write("")

# ------------------------------------------------------------------
# Technologies utilisées
# ------------------------------------------------------------------
with st.container(border=True):
    section_title("🛠️", "Technologies utilisées")

    tech = pd.DataFrame({
        "Technologie": ["Python", "Streamlit", "Scikit-learn", "Pandas", "Plotly", "SQLite", "SHAP"],
        "Utilisation": [
            "Développement",
            "Interface utilisateur",
            "Machine Learning",
            "Manipulation des données",
            "Visualisation",
            "Historique des prédictions",
            "Explication des prédictions",
        ],
    })

    render_data_table(tech)

st.write("")

# ------------------------------------------------------------------
# Auteur
# ------------------------------------------------------------------
with st.container(border=True):
    section_title("👨‍💻", "Auteur")
    render_author_card(
        name="Bakary Dembele",
        role="Ingénierie Science des Données et Intelligence Artificielle (ISDIA)",
        details={
            "Projet": "Student Dropout Prediction",
            "Année": "2025-2026",
        },
    )

st.caption("Version 1.0 • Juillet 2026")

render_sidebar_footer()
