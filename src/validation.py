
def validation(user_inputs):
    error=[]

    if user_inputs['Marital_status_grouped']=="__Selectionnez le statut matrimoniale__":
        error.append("Veuillez selectionner le statut matrimoniale")

    if user_inputs['Course']=="__Selectionnez le parcours__":
        error.append("Veuillez selectionner le parcours")

    if user_inputs['Application_mode_grouped']=="__Selectionnez le mode de candidature__":
        error.append("Veuillez selectionner le mode de candidature ")

    if user_inputs['Previous_qualification_grouped']=="__Selectionnez l'ancienne qualification__":
        error.append("Veuillez choisir l'ancienne qualification")

    if user_inputs["Mother's_qualification_grouped"]=="__Selectionnez la qualification de la mère__":
        error.append("Veuillez selectionner la qualification de la mère")

    if user_inputs["Father's_qualification_grouped"]=="__Selectionnez la qualification du père__":
        error.append("Veuillez selectionner la qualification du père")

    if user_inputs["Mother's_occupation_grouped"]=="__Selectionnez la profession de la mère__":
        error.append("Veuillez la profession de la mère")
    
    if user_inputs["Father's_occupation_grouped"]=="__Selectionnez la profession du père__":
        error.append("Veuillez selectionner la pofession du père")



    if user_inputs['Curricular units 1st sem (credited)']>user_inputs['Curricular units 1st sem (enrolled)']:
        error.append("en S1 le nombre de matière creditée ne peut pas depasser le nombre matière inscrite ")
    
    if user_inputs['Curricular units 1st sem (approved)']>user_inputs['Curricular units 1st sem (enrolled)']:
        error.append("en S1 le nombre de matière validé ne peut pas depasser le nombre de matière inscrite")

    if user_inputs['Curricular units 1st sem (without evaluations)']>user_inputs['Curricular units 1st sem (enrolled)']:
        error.append("en S1 le nombre de matière validé sans evaluation ne peut pas depasser le nombre de matière inscrite")

    if user_inputs['Curricular units 1st sem (without evaluations)']>user_inputs['Curricular units 1st sem (approved)']:
        error.append("en S1 le nombre de matière validé sans evaluation ne peut pas depasser le nombre de matière inscrite")

    

    if user_inputs['Curricular units 2nd sem (credited)']>user_inputs['Curricular units 2nd sem (enrolled)']:
        error.append("en S2 le nombre de matière creditée ne peut pas depasser le nombre matière inscrite  ")
    
    if user_inputs['Curricular units 2nd sem (approved)']>user_inputs['Curricular units 2nd sem (enrolled)']:
        error.append("en S2 le nombre de matière validé ne peut pas depasser le nombre de matière inscrite")

    if user_inputs['Curricular units 2nd sem (without evaluations)']>user_inputs['Curricular units 2nd sem (enrolled)']:
        error.append("en S2 le nombre de matière validé sans evaluation ne peut pas depasser le nombre de matière inscrite")

    if user_inputs['Curricular units 2nd sem (without evaluations)']>user_inputs['Curricular units 2nd sem (approved)']:
        error.append("en S2 le nombre de matière validé sans evaluation ne peut pas depasser le nombre de matière inscrite")

    

    

    return error