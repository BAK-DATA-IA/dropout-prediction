import pandas as pd


DATA=pd.read_csv("../data/data_preprocessed.csv")



GENDER_OPTIONS=DATA['Gender'].unique().tolist()
MARITAL_STATUS_OPTIONS=["__Selectionnez le statut matrimoniale__"]+DATA['Marital_status_grouped'].unique().tolist()
COURSE_OPTIONS=["__Selectionnez le parcours__"]+DATA['Course'].unique().tolist()
APPLICATION_MODE_OPTIONS=["__Selectionnez le mode de candidature__"]+DATA['Application_mode_grouped'].unique().tolist()
MOTHERS_QUALIFICATION_OPTIONS=["__Selectionnez la qualification de la mère__"]+DATA["Mother's_qualification_grouped"].unique().tolist()
FATHERS_QUALIFICATION_OPTIONS=["__Selectionnez la qualification du père__"]+DATA["Father's_qualification_grouped"].unique().tolist()
MOTHERS_OCCUPATION_OPTIONS=["__Selectionnez la profession de la mère__"]+DATA["Mother's_occupation_grouped"].unique().tolist()
FATHERS_OCCUPATION_OPTIONS=["__Selectionnez la profession du père__"]+DATA["Father's_occupation_grouped"].unique().tolist()
PREVIOUS_QUALIFICATION_OPTIONS=["__Selectionnez l'ancienne qualification__"]+DATA['Previous_qualification_grouped'].unique().tolist()
APPLICATION_ORDER_OPTIONS=list(range(0,10))
DAYTIME_OPTIONS=DATA['Daytime/evening attendance'].unique().tolist()
DISPLACED_OPTIONS=DATA['Displaced'].unique().tolist()

YES_NO_OPTIONS=["oui","non"]

