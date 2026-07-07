import pandas as pd
import streamlit as st


@st.cache_data
def load_dataFrame():
    data=pd.read_csv("../data/data_preprocessed.csv")

