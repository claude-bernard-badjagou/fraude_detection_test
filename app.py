import streamlit as st
import joblib

# Fonction pour charger le modèle avec mise en cache
@st.cache_resource
def load_model():
    return joblib.load("xgboost_model.joblib")

# Charger le modèle XGBoost
xgboost_model = load_model()

# Fonction pour effectuer une prédiction
def predict_fraud(input_data):
    prediction = xgboost_model.predict([input_data])[0]
    return "Fraude détectée" if prediction == 1 else "Pas de fraude"

# Configuration de l'application
st.subheader("Détecter les opérations frauduleuses")
st.markdown("**Application de détection de transactions frauduleuses.**")

# Champs pour les entrées utilisateur
type_transaction = st.selectbox("Choisissez le type de la transaction", ["TRANSFERT", "RETRAIT"])
montant_transaction = st.number_input("Quel est le montant de la transaction", min_value=0.0, step=1500.0)
solde_initial_initiateur = st.number_input("Solde initial de l'initiateur", min_value=0.0, step=1500.0)
solde_final_initiateur = st.number_input("Solde final de l'initiateur", min_value=0.0, step=1500.0)
solde_initial_destinataire = st.number_input("Solde initial du destinataire", min_value=0.0, step=1500.0)
solde_final_destinataire = st.number_input("Solde final du destinataire", min_value=0.0, step=1500.0)

# Utilisation des boutons radio pour des choix à deux valeurs
frequence_destinataire = st.radio("Fréquence du destinataire", [0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")
solde_initiateur_vide = st.radio("Solde initiateur vide ?", [0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")
solde_destinataire_vide = st.radio("Solde destinataire vide ?", [0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")
seuil_depasse = st.radio("Seuil dépassé ?", [0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")

erreur_solde_initiateur = st.number_input("Erreur sur le solde de l'initiateur", min_value=0.0, step=1500.0)
erreur_solde_destinataire = st.number_input("Erreur sur le solde du destinataire", min_value=0.0, step=1500.0)

# Bouton de prédiction
if st.button("Prédire"):
    # Conversion du type de transaction
    type_map = {"TRANSFERT": 0, "RETRAIT": 1}
    type_transaction_encoded = type_map[type_transaction]

    # Préparation des données pour la prédiction
    input_data = [
        type_transaction_encoded, montant_transaction, solde_initial_initiateur,
        solde_final_initiateur, solde_initial_destinataire, solde_final_destinataire,
        solde_initiateur_vide, solde_destinataire_vide, seuil_depasse,
        frequence_destinataire, erreur_solde_initiateur, erreur_solde_destinataire
    ]

    # Prédiction
    result = predict_fraud(input_data)
    st.success(f"Résultat : {result}")

    