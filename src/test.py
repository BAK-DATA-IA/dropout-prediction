import pandas as pd


data=pd.read_csv("../data/data_preprocessed.csv")

print(data['Tuition fees up to date'].value_counts())