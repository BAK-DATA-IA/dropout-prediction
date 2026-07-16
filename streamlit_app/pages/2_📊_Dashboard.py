import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px

APP_ROOT = Path(__file__).resolve().parents[1]   # streamlit_app/
PROJECT_ROOT = APP_ROOT.parent                    # racine du projet
for p in (APP_ROOT, PROJECT_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from assets.styles.theme import apply_theme
from assets.styles.color import Colors
from assets.styles.components import (
    render_sidebar,
    render_sidebar_footer,
    page_header,
    style_chart,
    render_data_table,
    kpi_card,
    section_title,
    chart_title,
    resolve_status_colors,
)

from src.Dashboard import *
from src.Database.database import *

st.set_page_config(page_title="Dashboard", page_icon="🎓", layout="wide")

apply_theme()
render_sidebar()

page_header(
    title="📊 Tableau de bord",
    eyebrow="Analytics",
    subtitle="Analyse descriptive du jeu de données et suivi des prédictions.",
)

# ------------------------------------------------------------------
# Statistiques du jeu de données (cartes KPI à badges, comme Home)
# ------------------------------------------------------------------
stats = get_statistics()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("👨‍🎓", stats["n_students"], "Étudiants", "Total dans la base", badge="blue")

with col2:
    kpi_card("📉", f"{stats['dropout_rate']} %", "Taux de décrochage", "Sur l'ensemble des étudiants", badge="rose")

with col3:
    kpi_card("🎓", f"{stats['graduate_rate']} %", "Taux de diplômés", "Sur l'ensemble des étudiants", badge="green")

with col4:
    kpi_card("📋", stats["n_feature"], "Variables", "Caractéristiques", badge="purple")

st.write("")

# ------------------------------------------------------------------
# Vue d'ensemble du jeu de données (une seule carte, 4 mini-graphiques)
# ------------------------------------------------------------------
with st.container(border=True):
    section_title("📊", "Vue d'ensemble du jeu de données", tag="Données fixes", tag_kind="neutral")

    col1, col2 = st.columns(2)

    with col1:
        chart_title("Répartition des étudiants")
        target_distribution = get_target_distribution()
        fig = px.pie(
            target_distribution,
            names="classe",
            values="nombre",
            hole=0.55,
            color="classe",
            color_discrete_map=resolve_status_colors(target_distribution["classe"]),
        )
        fig.update_traces(textinfo="percent+label")
        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        chart_title("Répartition par sexe")
        gender_distribution = get_gender_distribution()
        fig = px.bar(gender_distribution, x="Genre", y="Nombre")
        fig.update_traces(marker_color=Colors.PRIMARY)
        fig = style_chart(fig, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        chart_title("Distribution de l'âge")
        age_distribution = get_age_distribution()
        fig = px.histogram(age_distribution, x="Age at enrollment")
        fig.update_traces(marker_color=Colors.PRIMARY)
        fig = style_chart(fig, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        chart_title("Répartition des parcours")
        course_distribution = get_course_distribution()
        fig = px.bar(course_distribution, x="Nombre", y="Parcours", orientation="h")
        fig.update_traces(marker_color=Colors.PRIMARY)
        fig = style_chart(fig, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        chart_title("Répartition des boursiers")
        scholarship_holder_distribution = get_scholarship_holder_distribution()
        fig = px.bar(scholarship_holder_distribution, x="Boursier", y="Nombre")
        fig.update_traces(marker_color=Colors.PRIMARY)
        fig = style_chart(fig, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        chart_title("Régularité des frais de scolarité")
        Tuition_fees_up_to_date = get_Tuition_fees_distribution()
        fig = px.bar(Tuition_fees_up_to_date, x="Frais de scolarité a jour", y="Nombre")
        fig.update_traces(marker_color=Colors.PRIMARY)
        fig = style_chart(fig, show_legend=False)
        st.plotly_chart(fig, use_container_width=True)

st.write("")

# ------------------------------------------------------------------
# Suivi des prédictions (cartes KPI + une carte "vue d'ensemble" prédictions)
# ------------------------------------------------------------------
statistics = get_prediction_statistics()

total_predictions = statistics["total_predictions"] or 0
dropout_predictions = statistics["dropout_predictions"] or 0
graduate_predictions = statistics["graduate_predictions"] or 0
avg_probability = statistics["average_probability"]
avg_probability_display = (
    f"{round(avg_probability * 100, 2)} %" if avg_probability is not None else "—"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("📈", total_predictions, "Prédictions totales", "Depuis le lancement", badge="blue")

with col2:
    kpi_card("⚠️", dropout_predictions, "Abandons prédits", "Nombre de prédictions", badge="rose")

with col3:
    kpi_card("✅", graduate_predictions, "Succès prédits", "Nombre de prédictions", badge="green")

with col4:
    kpi_card(
        "🎯",
        avg_probability_display,
        "Probabilité moyenne",
        "Toutes prédictions confondues",
        badge="sky",
    )

st.write("")

with st.container(border=True):
    section_title("📈", "Suivi des prédictions", tag="Temps réel", tag_kind="success")

    col1, col2 = st.columns(2)

    with col1:
        chart_title("Répartition des prédictions")
        prediction_distribution = get_prediction_distribution()
        fig = px.pie(
            prediction_distribution,
            names="prediction",
            values="effectif",
            hole=0.55,
            color="prediction",
            color_discrete_map=resolve_status_colors(prediction_distribution["prediction"]),
        )
        fig.update_traces(textinfo="percent+label")
        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        chart_title("Répartition des prédictions par parcours")
        course_prediction_distribution = get_course_prediction_distribution()
        fig = px.bar(
            course_prediction_distribution,
            x="course",
            y="effectif",
            color="prediction",
            barmode="group",
            color_discrete_map=resolve_status_colors(course_prediction_distribution["prediction"]),
        )
        # Légende en haut : les noms de parcours sont longs et pivotés en bas,
        # une légende en bas les chevaucherait.
        fig = style_chart(fig, legend_position="top")
        st.plotly_chart(fig, use_container_width=True)

    st.write("")
    chart_title("Prédictions par jour")
    prediction_timeline = get_prediction_timeline()
    if len(prediction_timeline) > 1:
        fig = px.line(prediction_timeline, x="date", y="effectif")
        fig.update_traces(line_color=Colors.PRIMARY)
        fig = style_chart(fig, show_legend=False, height=280)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "Le graphique concernant l'evolution des predictions en fonctions "
            "du temps sera disponible après plusieurs jours d'utilisation."
        )

    st.write("")
    chart_title("Dernières prédictions")
    last_predictions = get_last_predictions()

    # Mise en forme façon maquette : dates lisibles, probabilité en %,
    # colonnes renommées en français.
    display_df = last_predictions.copy()
    display_df["prediction_date"] = pd.to_datetime(display_df["prediction_date"]).dt.strftime("%d/%m/%Y %H:%M")
    display_df["probability"] = (display_df["probability"] * 100).round(2).astype(str) + " %"
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

render_sidebar_footer()
