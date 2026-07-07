import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import shap
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[2]  
sys.path.insert(0, str(root))

 

from src.prediction import predict_student
from src.validation import validation
from src.shap_utils import explain_student,shap_summary
from src.options import(
    GENDER_OPTIONS,
    MARITAL_STATUS_OPTIONS,
    COURSE_OPTIONS,
    APPLICATION_MODE_OPTIONS,
    MOTHERS_QUALIFICATION_OPTIONS,
    FATHERS_QUALIFICATION_OPTIONS,
    MOTHERS_OCCUPATION_OPTIONS,
    FATHERS_OCCUPATION_OPTIONS,
    PREVIOUS_QUALIFICATION_OPTIONS,
    DAYTIME_OPTIONS,
    DISPLACED_OPTIONS,
    YES_NO_OPTIONS
)

st.set_page_config(page_title="Prediction",
                   page_icon="🎓",
                   layout="wide")

st.title("🎓 Prédiction du décrochage étudiant")

st.write("""
Remplissez les informations de l'étudiant, puis cliquez sur Prédire
pour estimer le risque de décrochage.
""")

st.divider()




with st.expander("👤 Informations personnelles", expanded=True):
    col1,col2=st.columns(2)

    with col1:
        genre=st.radio("Genre",GENDER_OPTIONS,horizontal=True)
        situation_matrimoniale=st.selectbox("Situation matrimoniale",MARITAL_STATUS_OPTIONS)
        deplace=st.radio("Etudiant déplacé",DISPLACED_OPTIONS,horizontal=True)

    with col2:
        age=st.number_input(label="Âge à l'inscription",min_value=17,max_value=70,step=1)
        international=st.radio("Etudiant international",YES_NO_OPTIONS,horizontal=True)
        besoins_particuliers=st.radio("Bésoins particuliers educatifs",YES_NO_OPTIONS,horizontal=True)

user_inputs={"Gender":genre,
             "Marital_status_grouped":situation_matrimoniale,
             "Displaced":deplace,
             "Age at enrollment":age,
             "International":international,
             "Educational special needs":besoins_particuliers}




with st.expander("🎓 Parcours académique", expanded=False):
    col1,col2=st.columns(2)

    with col1:
        formation=st.selectbox("Formation",COURSE_OPTIONS)
        ordre_preference=st.slider("Ordre de préférence",min_value=0,max_value=9,step=1)
        mode_candidature=st.selectbox("Mode de candidature",APPLICATION_MODE_OPTIONS)
        enseignement=st.radio("Enseignement",DAYTIME_OPTIONS,horizontal=True)
    
    with col2:
        qualification_precedente=st.selectbox("Qualification précedente",PREVIOUS_QUALIFICATION_OPTIONS)
        qualification_precedente_note=st.number_input("Note de la qualification précedente",min_value=0.0,max_value=200.0,step=0.1)
        note_admission=st.number_input("Note d'admission",min_value=0.0,max_value=200.0,step=0.1)


user_inputs.update({
    "Course":formation,
    "Application order":ordre_preference,
    "Application_mode_grouped":mode_candidature,
    "Daytime/evening attendance":enseignement,
    "Previous_qualification_grouped":qualification_precedente,
    "Previous qualification (grade)":qualification_precedente_note,
    "Admission grade":note_admission
})


with st.expander("👨‍👩‍👧 Informations familiales"):
    col1,col2=st.columns(2)

    with col1:
        qualification_mere=st.selectbox("Qualification de la mère",MOTHERS_QUALIFICATION_OPTIONS)
        profession_mere=st.selectbox("Profession de la mère",MOTHERS_OCCUPATION_OPTIONS)
    with col2:
        qualification_pere=st.selectbox("Qualification du père",FATHERS_QUALIFICATION_OPTIONS)
        profession_pere=st.selectbox("Profession du père",FATHERS_OCCUPATION_OPTIONS)


user_inputs.update({
    "Mother's_qualification_grouped":qualification_mere,
    "Mother's_occupation_grouped":profession_mere,
    "Father's_qualification_grouped":qualification_pere,
    "Father's_occupation_grouped":profession_pere
})

with st.expander("💰 Situation financière", expanded=False):
    col1,col2=st.columns(2)
    with col1:
        debiteur=st.radio("Debiteur",YES_NO_OPTIONS,horizontal=True)
        boursier=st.radio("Boursier",YES_NO_OPTIONS,horizontal=True)
    with col2:
        frais_a_jour=st.radio("Frais de scolarité a jour",YES_NO_OPTIONS,horizontal=True)

user_inputs.update({
    "Debtor":debiteur,
    "Scholarship holder":boursier,
    "Tuition fees up to date":frais_a_jour
})



with st.expander("📚 Résultats du 1er semestre", expanded=False):
    col1,col2=st.columns(2)
    with col1:
        credited_s1=st.number_input("Nombre de matiere validé par equivalence",min_value=0,max_value=26,step=1)
        enrolled_s1=st.number_input("Nombre de matière auquel il s'est inscrit en s1",min_value=0,max_value=26,step=1)
        evaluation_s1=st.number_input("Nombre d'evaluation passé en s1",min_value=0,max_value=45,step=1)
        
    with col2:
        approved_s1=st.number_input("Nombre de matière validée en s1",min_value=0,max_value=26,step=1)
        grade_s1=st.number_input("Moyenne obtenu en s1",min_value=0.0,max_value=20.0,step=0.01)
        non_evaluation_s1=st.number_input("Nombre de matière validé sans evaluation",min_value=0,max_value=26,step=1)


user_inputs.update({
    "Curricular units 1st sem (credited)":credited_s1,
    "Curricular units 1st sem (enrolled)":enrolled_s1,
    "Curricular units 1st sem (evaluations)":evaluation_s1,
    "Curricular units 1st sem (approved)":approved_s1,
    "Curricular units 1st sem (grade)":grade_s1,
    "Curricular units 1st sem (without evaluations)":non_evaluation_s1
})




with st.expander("📚 Résultats du 2eme semestre ", expanded=False):
    col1,col2=st.columns(2)
    with col1:
        credited_s2=st.number_input("Nombre de matiere validé par equivalence",min_value=0,max_value=23,step=1)
        enrolled_s2=st.number_input("Nombre de matière auquel il s'est inscrit en s2",min_value=0,max_value=23,step=1)
        evaluation_s2=st.number_input("Nombre d'evaluation passé en s2",min_value=0,max_value=33,step=1)
        
    with col2:
        approved_s2=st.number_input("Nombre de matière validée en s2",min_value=0,max_value=23,step=1)
        grade_s2=st.number_input("Moyenne obtenu en s2",min_value=0.0,max_value=20.0,step=0.01)
        non_evaluation_s2=st.number_input("Nombre de matière validé sans evaluation",min_value=0,max_value=23,step=1)


user_inputs.update({
    "Curricular units 2nd sem (credited)":credited_s2,
    "Curricular units 2nd sem (enrolled)":enrolled_s2,
    "Curricular units 2nd sem (evaluations)":evaluation_s2,
    "Curricular units 2nd sem (approved)":approved_s2,
    "Curricular units 2nd sem (grade)":grade_s2,
    "Curricular units 2nd sem (without evaluations)":non_evaluation_s2
})



with st.expander("📈 Indicateurs économiques", expanded=False):
    col1,col2=st.columns(2)

    with col1:
        taux_chomage=st.number_input("Taux de chomage en pourcentage",min_value=0.0,max_value=100.0,step=0.1)
        taux_inflation=st.number_input("Taux d'inflation",min_value=-20.0,max_value=100.0,value=0.0,step=0.1)

    with col2:
        croissance_pib=st.number_input("Croissance du PIB",min_value=-20.0,max_value=100.0,value=0.0,step=0.01)


user_inputs.update({
    "Unemployment rate": taux_chomage,
    "Inflation rate": taux_inflation,
    "GDP": croissance_pib
})




if st.button("🎯 Prédire le risque de décrochage",use_container_width=True):


    errors=validation(user_inputs)

    if errors:
        for e in errors:
            st.error(e)

    else:

        user_inputs = pd.DataFrame([user_inputs])

        result = predict_student(user_inputs)

        prediction = result["prediction"]
        probability = result["probability"]

        st.divider()
        st.subheader("🎯 Résultat de la prédiction")
        if prediction == 1:
            st.error("Décrochage prédit")
        else:
            st.success("Pas de décrochage prédit")

        st.metric(label="Probabilité de décrochage",value=f"{round(probability*100,2)}%",border=True)



        
        shap_values = explain_student(user_inputs)
        shap.plots.waterfall(shap_values[0], show=False)

        st.pyplot(plt.gcf())

        plt.clf()


        shap_df=shap_summary(shap_values)
        shap_df=shap_df.rename(columns={"Contribution SHAP":"Impact sur la prédiction","Variable":"Facteur"})

        st.dataframe(shap_df[["Facteur","Impact sur la prédiction","Effet"]].head(10),use_container_width=True)
