import sys
from pathlib import Path

import streamlit as st

APP_ROOT = Path(__file__).resolve().parent  # streamlit_app/
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

PROJECT_ROOT = APP_ROOT.parent                    # racine du projet
for p in (APP_ROOT, PROJECT_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))



from assets.styles.theme import apply_theme
from assets.styles.components import render_sidebar, render_sidebar_footer, page_header, kpi_card
from src.Dashboard import get_statistics


st.set_page_config(
    page_title="Student dropout prediction",
    page_icon="🎓",
    layout="wide",
)

apply_theme()
render_sidebar()

page_header(
    title="🎓 Accueil",
    eyebrow="Machine Learning · Enseignement supérieur",
    subtitle=(
        "Cette application prédit le risque de décrochage d'un étudiant à "
        "partir de ses données académiques, démographiques et socio-économiques, "
        "et explique chaque prédiction."
    ),
)

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    stats = get_statistics()
    kpi_card("👨‍🎓", f"{stats["n_students"]}", "Étudiants", "Total dans la base", badge="blue")

with col2:
    kpi_card("📋", "36", "Variables", "Caractéristiques", badge="purple")

with col3:
    kpi_card("🤖", "Régression logistique", "Modèle", "Modèle utilisé", badge="amber")

with col4:
    kpi_card("🎯", "Dropout / Succès", "Cible", "Classes prédites", badge="sky")

st.divider()

col_left, col_right = st.columns(2, gap="large")

with col_left:
    st.subheader("🚀 Comment utiliser l'application")
    st.markdown(
        """
        1. Ouvrez la page **Prediction**.
        2. Renseignez les informations de l'étudiant.
        3. Cliquez sur **Prédire**.
        4. Consultez la prédiction et son explication (SHAP).
        """
    )

with col_right:
    st.subheader("🎯 Prêt à commencer ?")
    st.write("Estimez le risque de décrochage d'un étudiant en moins d'une minute.")
    with st.container(key="home-cta-prediction"):
        st.page_link(
            "pages/1_🔮_prediction.py",
            label="Faire une prédiction",
            icon="🔮",
            use_container_width=True,
        )

render_sidebar_footer()

