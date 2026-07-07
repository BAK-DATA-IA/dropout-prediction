
import joblib
import streamlit as st


@st.cache_resource
def load_pipeline():
    pipeline = joblib.load("../models/pipeline_dropout.pkl")
    return pipeline



def create_features(user_inputs):
    user_inputs['no_academic_activity']=((user_inputs['Curricular units 1st sem (grade)']==0) & 
                                         (user_inputs['Curricular units 1st sem (evaluations)']==0) & 
                                         (user_inputs['Curricular units 1st sem (enrolled)']==0)).astype(int)
    

    user_inputs['no_assessment_taken']=((user_inputs['Curricular units 1st sem (grade)']==0) & 
                                        (user_inputs['Curricular units 1st sem (evaluations)']==0) & 
                                        (user_inputs['Curricular units 1st sem (enrolled)']>0)).astype(int)
    
    user_inputs['low_performance']=((user_inputs['Curricular units 1st sem (grade)']==0) & 
                                    (user_inputs['Curricular units 1st sem (evaluations)']>0) & 
                                    (user_inputs['Curricular units 1st sem (enrolled)']>0)).astype(int)
    

    user_inputs['grade2_echec']=((user_inputs['Curricular units 2nd sem (grade)']==0) & 
                                 
                                 (user_inputs['Curricular units 1st sem (grade)']!=0)).astype(int)
    return user_inputs


def predict_student(user_inputs):

    features=create_features(user_inputs)
    pipeline=load_pipeline()

    prediction=pipeline.predict(features)[0]
    probability=pipeline.predict_proba(features)[0,1]

    
    return {'probability':probability, "prediction":prediction}









