import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load model
with open("model_randomforest_gerd.pkl", "rb") as f:
    model = pickle.load(f)

# Title and header
st.set_page_config(page_title="Analisis Risiko GERD", layout="centered")
st.markdown("## 📊 Input Data Pola Makan")

# Input fields
usia = st.number_input("Usia:", min_value=1, max_value=100, step=1)
berat_badan = st.number_input("Berat Badan (kg):", min_value=1.0, max_value=200.0, step=0.1)
tinggi_badan = st.number_input("Tinggi Badan (cm):", min_value=30.0, max_value=250.0, step=0.1)

frekuensi_makan = st.selectbox("Frekuensi Makan per Hari:", options=[1, 2, 3, 4, 5, 6])

waktu_makan_malam = st.selectbox("Waktu Makan Malam:", options=["< 18.00", "18.00 - 20.00", "> 20.00"])

# Jenis makanan
st.markdown("**Jenis Makanan yang Sering Dikonsumsi:**")
makanan_pedas = st.checkbox("Makanan Pedas")
makanan_asam = st.checkbox("Makanan Asam")
kopi_kafein = st.checkbox("Kopi/Kafein")
makanan_berlemak = st.checkbox("Makanan Berlemak")
cokelat = st.checkbox("Cokelat")
minuman_berkafein = st.checkbox("Minuman Bersoda")

# Status merokok
status_merokok = st.selectbox("Status Merokok:", options=["Tidak", "Ya"])

# Konversi input ke bentuk DataFrame sesuai model
def preprocess_input():
    data = {
        "usia": usia,
        "berat_badan": berat_badan,
        "tinggi_badan": tinggi_badan,
        "frekuensi_makan": frekuensi_makan,
        "waktu_makan_malam": 0 if waktu_makan_malam == "< 18.00" else (1 if waktu_makan_malam == "18.00 - 20.00" else 2),
        "makanan_pedas": int(makanan_pedas),
        "makanan_asam": int(makanan_asam),
        "kopi_kafein": int(kopi_kafein),
        "makanan_berlemak": int(makanan_berlemak),
        "cokelat": int(cokelat),
        "minuman_bersoda": int(minuman_berkafein),
        "merokok": 1 if status_merokok == "Ya" else 0
    }
    return pd.DataFrame([data])

# Tombol prediksi
if st.button("🔍 Analisis Risiko GERD"):
    input_df = preprocess_input()
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Risiko GERD **TINGGI** ({probability*100:.2f}%)")
    else:
        st.success(f"✅ Risiko GERD **RENDAH** ({probability*100:.2f}%)")
