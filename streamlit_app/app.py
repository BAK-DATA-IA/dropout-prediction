import streamlit as st

st.set_page_config(
    page_title="Student Dropout Prediction",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Dropout Prediction")

st.write("""
This application predicts the risk of student dropout using a Machine Learning
model trained on academic, demographic, and socio-economic data.

Use the navigation menu on the left to access the different features of
the application.
""")

st.divider()


col1,col2,col3,col4=st.columns([1,1,2,2])

with col1:
    st.metric(label="👨‍🎓 Students",value=4424,border=True)

with col2:
    st.metric(label="📋 Features", value=36,border=True)

with col3:
    st.metric(label="🤖 Model",value="logistic Regression",border=True)

with col4:
    st.metric(label="🎯 Target",value="Dropout/no dropout",border=True)


st.divider()

st.subheader("🚀 How to Use")

st.write("""
1. Go to the Prediction page.
2. Fill in the student's information.
3. Click Predict.
4. View the prediction and explanation.
         """)

st.divider()

st.subheader("💡 Tip")

st.write(""" For the best results, complete all required fields with accurate information.""")