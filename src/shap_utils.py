import shap
import joblib
import streamlit as st
import pandas as pd
import numpy as np

from src.prediction import load_pipeline, create_features
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "X_train.pkl"





@st.cache_data
def load_background_data():
    return joblib.load(DATA_PATH)




@st.cache_resource
def load_explainer():
    pipeline = load_pipeline()
    preprocessor = pipeline.named_steps["preprocessor"]
    classifier = pipeline.named_steps["classifier"]

    X_train=load_background_data()
    X_train_transformed = preprocessor.transform(X_train)
    explainer = shap.LinearExplainer(
    classifier,
    X_train_transformed
)
    return explainer, preprocessor



def explain_student(user_inputs):

    features=create_features(user_inputs)
    explainer, preprocessor = load_explainer()

    feature_names = preprocessor.get_feature_names_out()

    features_transformed = pd.DataFrame(
    preprocessor.transform(features),
    columns=feature_names
)
    clean_feature_names = [
    name.replace("num__", "").replace("cat__", "")
    for name in feature_names
]
    print(clean_feature_names[:5])
    shap_values = explainer(features_transformed)
    shap_values.feature_names = clean_feature_names
    
    return shap_values


def shap_summary(shap_values):
    shap_df = pd.DataFrame({
    "Variable": shap_values.feature_names,
    "Valeur": shap_values.data[0],
    "Contribution SHAP": shap_values.values[0].round(2)
})
    
    shap_df['Effet']=np.where(
        shap_df["Contribution SHAP"]>0,
        "🔴 Augmente le risque",
        "🔵 Réduit le risque"
    )
    
    shap_df["Importance"] = shap_df["Contribution SHAP"].abs()
    shap_df = shap_df.sort_values(
    by="Importance",
    ascending=False
)
    
    return shap_df




