import streamlit as st
import sys
from pathlib import Path
import plotly.express as px
from theme import apply_theme


root = Path(__file__).resolve().parents[2]  
sys.path.insert(0, str(root))

from src.Dashboard import *
from src.Database.database import *
st.set_page_config(page_title="Dashboard",layout="wide")



st.title("📊 Tableau de bord")
st.write("Analyse descriptive du jeu de données et suivi des prédictions.")

st.divider()

st.subheader("📁 Statistiques du jeu de données")
stats = get_statistics()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👨‍🎓 Étudiants",
        value=stats["n_students"],
        border=True
    )

with col2:
    st.metric(
        label="📉 Taux de décrochage",
        value=f"{stats['dropout_rate']} %",
        border=True
    )

with col3:
    st.metric(
        label="🎓 Taux de diplômés",
        value=f"{stats['graduate_rate']} %",
        border=True
    )

with col4:
    st.metric(
        label="📋 Variables",
        value=stats["n_feature"],
        border=True
    )

st.divider()

st.subheader("📊 Distribution des principales variables")



col1,col2=st.columns(2)

with col1:
    target_distribution = get_target_distribution()



    fig = px.pie(
        target_distribution,
        names="classe",
        values="nombre",
        title="Répartition des étudiants"
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    fig.update_layout(
        title_x=0.25
    )
    st.plotly_chart(fig, use_container_width=True)


with col2:
    gender_distribution = get_gender_distribution()

    fig = px.bar(
    gender_distribution,
    x="Genre",
    y="Nombre",
    title="Répartition par sexe"
)
    fig.update_layout(
        title_x=0.3
    )

    st.plotly_chart(fig, use_container_width=True)


col1,col2=st.columns(2)

with col1:
    age_distribution = get_age_distribution()

    fig = px.histogram(
    age_distribution,
    x="Age at enrollment",
    title="Distribution de l'âge"
)
    fig.update_layout(
        title_x=0.3
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:
    course_distribution=get_course_distribution()
    fig = px.bar(
    course_distribution,
    x="Nombre",
    y="Parcours",
    title="Répartition des parcours"
)
    fig.update_layout(
        title_x=0.3
    )

    st.plotly_chart(fig, use_container_width=True)


col1,col2=st.columns(2)

with col1:
    scholarship_holder_distribution=get_scholarship_holder_distribution()
    fig=px.bar(
        scholarship_holder_distribution,
        x="Boursier",
        y="Nombre",
        title="Repartition des Boursiers"
    )
    fig.update_layout(
        title_x=0.3
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    Tuition_fees_up_to_date=get_Tuition_fees_distribution()
    fig=px.bar(
        Tuition_fees_up_to_date,
        x="Frais de scolarité a jour",
        y="Nombre",
        title="Repartition par regularité de frais de scolarité"
    )
    fig.update_layout(
        title_x=0.3
    )
    st.plotly_chart(fig, use_container_width=True)




st.divider()

st.subheader("📈 Suivi des prédictions")


col1, col2, col3, col4 = st.columns(4)
statistics=get_prediction_statistics()
with col1:
    st.metric(label="📈 Nombre total de prédictions",value=statistics["total_predictions"],border=True)

with col2:
    st.metric(label="❌ Nombre d'abandons prédits",value=statistics["dropout_predictions"],border=True)


with col3:
    st.metric(label="✅ Nombre de succès prédits",value=statistics["graduate_predictions"],border=True)

with col4:
    st.metric("📊 Probabilité moyenne",value=f"{round(statistics["average_probability"]*100,2)}%",border=True)



col1,col2=st.columns(2)

with col1:
    prediction_distribution = get_prediction_distribution()
    fig = px.pie(
        prediction_distribution,
        names="prediction",
        values="effectif",
        title="Répartition des prédictions"
    )


    fig.update_traces(
            textinfo="percent+label"
        )

    fig.update_layout(
            title_x=0.22
        )
    st.plotly_chart(fig, width="stretch")

with col2:
    course_prediction_distribution=get_course_prediction_distribution()
    fig=px.bar(
        course_prediction_distribution,
        x="course",
        y="effectif",
        color="prediction",
        title="Répartition des prédictions par parcours",
        barmode="group"
    )

    st.plotly_chart(fig, width="stretch")
st.write("")
st.write("")

col1,col2=st.columns(2)

with col1:
    
    prediction_timeline = get_prediction_timeline()
    if len(prediction_timeline) > 1:
    # afficher la courbe

        fig = px.line(
        prediction_timeline,
        x="date",
        y="effectif",
        title="Évolution des prédictions"
    )
        st.plotly_chart(
        fig,
        width="stretch"
    )

    else:
        st.info("Le graphique concernant l'evolution des predictions en fonctions du temps sera disponible après plusieurs jours d'utilisation.")
    
with col2:
    last_predictions = get_last_predictions()

    st.dataframe(
    last_predictions,
    width="stretch"
    )




