import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.write("L'application qui prédit l'accord du crédit")

# Fonction pour collecter les caractéristiques du client
def client_caract_entree():
    Gender = st.sidebar.selectbox('Sexe', ('Male', 'Female'))
    Married = st.sidebar.selectbox('Marié', ('Yes', 'No'))
    Dependents = st.sidebar.selectbox('Enfants', ('0', '1', '2', '3+'))
    Education = st.sidebar.selectbox('Education', ('Graduate', 'Not Graduate'))
    Self_Employed = st.sidebar.selectbox('Salarié ou Entrepreneur', ('Yes', 'No'))
    ApplicantIncome = st.sidebar.slider('Salaire du client', 150, 4000, 200)
    CoapplicantIncome = st.sidebar.slider('Salaire du conjoint', 0, 40000, 2000)
    LoanAmount = st.sidebar.slider('Montant du crédit en dollar', 9.0, 700.0, 201.0)
    Loan_Amount_Term = st.sidebar.selectbox('Durée du crédit', (360.0, 120.0, 240.0, 180.0, 60.0, 300.0, 36.0, 84.0, 12.0))
    Credit_History = st.sidebar.selectbox('Credit_History', ('1', '0'))
    Property_Area = st.sidebar.selectbox('Property_Area', ('Urban', 'Rural', 'Semiurban'))

    data = {
        'Gender': Gender,
        'Married': Married,
        'Dependents': Dependents,
        'Education': Education,
        'Self_Employed': Self_Employed,
        'ApplicantIncome': ApplicantIncome,
        'CoapplicantIncome': CoapplicantIncome,  
        'LoanAmount': LoanAmount,
        'Loan_Amount_Term': Loan_Amount_Term,
        'Credit_History': Credit_History,
        'Property_Area': Property_Area
    }

    profil_client = pd.DataFrame(data, index=[0])
    return profil_client

input_df = client_caract_entree()

# Utiliser des chemins relatifs pour les fichiers
data_path = os.path.join('data', 'dataset', 'train.csv')
model_path = os.path.join('data', 'models', 'prevision_credit.pkl')
columns_path = os.path.join('data', 'models', 'column_names.pkl')


# Importer la base de données pour la concaténation
df = pd.read_csv(data_path)
credit_input = df.drop(columns=['Loan_ID', 'Loan_Status'])  # Exclure Loan_Status ici
donne_entree = pd.concat([input_df, credit_input], axis=0)

# Convertir Credit_History en numérique
donne_entree['Credit_History'] = donne_entree['Credit_History'].astype(float)

# Utiliser get_dummies pour encoder les colonnes catégoriques
var_cat = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
donne_entree = pd.get_dummies(donne_entree, columns=var_cat, drop_first=True)

# Charger les noms des colonnes utilisés lors de l'entraînement
column_names = pickle.load(open(columns_path, 'rb'))

# Aligner les colonnes de l'entrée utilisateur avec celles utilisées pendant l'entraînement
donne_entree = donne_entree.reindex(columns=column_names, fill_value=0)

# Prendre uniquement la première ligne (entrée utilisateur)
donne_entree = donne_entree[:1]

# Afficher les données transformées
st.subheader('Les caractéristiques transformées')
st.write(donne_entree)

# Charger le modèle
load_model = pickle.load(open(model_path, 'rb'))

# Appliquer le modèle sur le profil d'entrée
prevision = load_model.predict(donne_entree)

# Résultat de la prévision avec des icônes et des couleurs
st.subheader('Résultat de la prévision')

if prevision[0] == 1:
    st.success("**Félicitations !** Le client est éligible pour obtenir le crédit. 🎉")
else:
    st.error("**Désolé.** La demande de crédit du client est refusée. ❌")

# Explications sur la décision
st.subheader('Explications sur la décision')

# Afficher certaines caractéristiques importantes
important_features = [
    'ApplicantIncome',
    'CoapplicantIncome',
    'LoanAmount',
    'Credit_History'
]

st.write("Voici quelques caractéristiques clés du profil du client qui ont influencé la décision :")

for feature in important_features:
    st.write(f"**{feature}** : {donne_entree[feature].values[0]}")

# Afficher le profil complet du client
st.subheader('Profil complet du client')
st.write(input_df)
