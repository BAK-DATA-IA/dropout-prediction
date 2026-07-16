import streamlit as st
import sys
from pathlib import Path
import pandas as pd

APP_ROOT = Path(__file__).resolve().parents[1]   # streamlit_app/
PROJECT_ROOT = APP_ROOT.parent                    # racine du projet
for p in (APP_ROOT, PROJECT_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from assets.styles.theme import apply_theme
from assets.styles.components import (
    render_sidebar,
    render_sidebar_footer,
    page_header,
    kpi_card,
    section_title,
    render_data_table,
)

from src.Database.database import load_history

st.set_page_config(page_title="History", page_icon="🎓", layout="wide")

apply_theme()
render_sidebar()

page_header(
    title="🕐 Historique des prédictions",
    eyebrow="Journal",
    subtitle="Retrouvez l'ensemble des prédictions réalisées, triées par date.",
)

history = load_history()

if history.empty:
    st.info("Aucune prédiction n'a encore été enregistrée. Rendez-vous sur la page **Prediction** pour commencer.")
else:
    # ------------------------------------------------------------------
    # Cartes KPI de résumé
    # ------------------------------------------------------------------
    total = len(history)
    n_abandon = int((history["prediction"] == "Abandon").sum())
    n_succes = int((history["prediction"] == "Succès").sum())
    avg_probability = history["probability"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card("🕐", total, "Prédictions enregistrées", "Historique complet", badge="blue")

    with col2:
        kpi_card("⚠️", n_abandon, "Abandons prédits", f"{round(n_abandon / total * 100, 1)} % du total", badge="rose")

    with col3:
        kpi_card("✅", n_succes, "Succès prédits", f"{round(n_succes / total * 100, 1)} % du total", badge="green")

    with col4:
        kpi_card("🎯", f"{round(avg_probability * 100, 2)} %", "Probabilité moyenne", "Toutes prédictions", badge="sky")

    st.write("")

    # ------------------------------------------------------------------
    # Filtres
    # ------------------------------------------------------------------
    course_options = ["Toutes"] + sorted(history["course"].dropna().unique().tolist())

    col_filter1, col_filter2 = st.columns([2, 3])
    with col_filter1:
        course_filter = st.selectbox("Filière", course_options)
    with col_filter2:
        prediction_filter = st.radio(
            "Résultat", ["Toutes", "Succès", "Abandon"], horizontal=True
        )

    filtered = history.copy()
    if course_filter != "Toutes":
        filtered = filtered[filtered["course"] == course_filter]
    if prediction_filter != "Toutes":
        filtered = filtered[filtered["prediction"] == prediction_filter]

    st.write("")

    # ------------------------------------------------------------------
    # Carte : tableau détaillé
    # ------------------------------------------------------------------
    with st.container(border=True):
        section_title(
            "📋",
            "Journal des prédictions",
            tag=f"{len(filtered)} résultat(s)",
            tag_kind="neutral",
        )

        if filtered.empty:
            st.info("Aucune prédiction ne correspond à ces filtres.")
        else:
            display_df = filtered.copy()
            display_df["prediction_date"] = pd.to_datetime(
                display_df["prediction_date"]
            ).dt.strftime("%d/%m/%Y %H:%M")
            display_df["probability"] = (
                display_df["probability"] * 100
            ).round(2).astype(str) + " %"
            display_df = display_df.rename(columns={
                "prediction_date": "Date",
                "course": "Filière",
                "prediction": "Prédiction",
                "probability": "Probabilité",
            })

            render_data_table(
                display_df,
                pill_column="Prédiction",
                pill_rules={
                    "abandon": "error",
                    "succès": "success",
                    "succes": "success",
                },
            )

    st.write("")
    st.download_button(
        label="⬇️ Exporter au format CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="historique_predictions.csv",
        mime="text/csv",
    )

render_sidebar_footer()

