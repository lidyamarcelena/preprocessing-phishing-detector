import streamlit as st
import joblib
import pandas as pd
from feature_extractor import extract_features

# load model
model = joblib.load("best_prediction_model.pkl")

st.title("Phishing Website Detection")
st.write("Masukkan URL untuk mendeteksi apakah phishing atau legitimate")

url = st.text_input("Input URL")

if st.button("Deteksi"):

    feats = extract_features(url)

    if feats is None:
        st.error("Halaman tidak bisa diakses atau bukan HTML")
    else:

        feature_values = []
        for col in model.feature_names_in_:
            feature_values.append(feats[col])

        X = pd.DataFrame([feature_values], columns=model.feature_names_in_)

        prob = model.predict_proba(X)[0]
        classes = list(model.classes_)

        prob_phish = prob[classes.index("phishing")]
        prob_legit = prob[classes.index("legitimate")]

        if prob_phish > prob_legit:
            status = "PHISHING"
            confidence = prob_phish * 100
        else:
            status = "LEGITIMATE"
            confidence = prob_legit * 100

        st.subheader("Hasil Deteksi")
        st.write("Status :", status)
        st.write("Confidence :", f"{confidence:.2f}%")
        st.write("Prob phishing :", prob_phish)
        st.write("Prob legit :", prob_legit)