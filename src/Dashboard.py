import pandas as pd
import streamlit as st





@st.cache_data
def load_dataFrame():
    data=pd.read_csv("../data/data_preprocessed.csv")
    return data




@st.cache_data
def get_statistics():

    data=load_dataFrame()

    Target_rate=((data['Target'].value_counts()/data.shape[0])*100).round(2)
    statistics={
        "n_students":data.shape[0],
        "dropout_rate":Target_rate[1],
        "graduate_rate":Target_rate[0],
        "n_feature":36
    }

    return statistics

@st.cache_data
def get_target_distribution():
    data=load_dataFrame()
    temp=data['Target'].value_counts()
    target_distribution=pd.DataFrame(
        columns=["classe","nombre"],data=[["Abandon",temp[1]],["Succès",temp[0]]]
    )

    return target_distribution


@st.cache_data
def get_gender_distribution():
    data = load_dataFrame()

    temp = data["Gender"].value_counts()

    gender_distribution = pd.DataFrame(
        columns=["Genre", "Nombre"],
        data=[
            ["Homme", temp[1]],
            ["Femme", temp[0]]
        ]
    )

    return gender_distribution


@st.cache_data
def get_age_distribution():
    data = load_dataFrame()

    age_distribution = data[["Age at enrollment"]]

    return age_distribution

@st.cache_data
def get_course_distribution():
    data = load_dataFrame()

    temp = data["Course"].value_counts()

    course_distribution = pd.DataFrame({
        "Parcours": temp.index,
        "Nombre": temp.values
    })

    return course_distribution


@st.cache_data
def get_scholarship_holder_distribution():
    data=load_dataFrame()
    temp = data["Scholarship holder"].value_counts()

    scholarship_holder_distribution = pd.DataFrame(
        columns=["Boursier", "Nombre"],
        data=[
            ["oui", temp[1]],
            ["non", temp[0]]
        ]
    )

    return scholarship_holder_distribution

@st.cache_data
def get_Tuition_fees_distribution():

    data=load_dataFrame()
    temp = data["Tuition fees up to date"].value_counts()

    Tuition_fees_up_to_date= pd.DataFrame(
        columns=["Frais de scolarité a jour", "Nombre"],
        data=[
            ["oui", temp[0]],
            ["non", temp[1]]
        ]
    )

    return Tuition_fees_up_to_date
