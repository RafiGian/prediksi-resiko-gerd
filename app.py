import streamlit as st
import numpy as np
import pickle

# Load model
with open("model_randomforest_gerd.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="GERD Predictor", page_icon="🤖", layout="centered")

# Tampilan Awal
st.title("GERD Predictor")
st.write("Masukkan data pola makan Anda untuk memprediksi risiko GERD.")

# Form input user
st.header("Input Pola Makan")

frekuensi = st.slider("Frekuensi makan per hari", 1, 10, 3)
jumlah_makanan = st.slider("Jumlah makanan per porsi (gram)", 50, 1000, 250)
makanan_pedas = st.selectbox("Apakah Anda makan makanan pedas?", ["Tidak", "Ya"])
makanan_berlemak = st.selectbox("Apakah Anda makan makanan berlemak?", ["Tidak", "Ya"])
waktu_tidur = st.slider("Berapa menit setelah makan Anda tidur?", 0, 180, 60)

# Konversi input ke format numerik
input_data = np.array([[
    frekuensi,
    jumlah_makanan,
    1 if makanan_pedas == "Ya" else 0,
    1 if makanan_berlemak == "Ya" else 0,
    waktu_tidur
]])

# Prediksi
if st.button("Prediksi"):
    pred = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0][1]  # Probabilitas GERD

    st.subheader("Hasil Prediksi")
    st.write(f"Risiko GERD Anda: **{**
