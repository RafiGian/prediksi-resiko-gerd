
import streamlit as st
import pandas as pd
import pickle

# Load model
with open("import streamlit as st
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
    st.write(f"Risiko GERD Anda: **{'Tinggi' if pred == 1 else 'Rendah'}**")
    st.metric(label="Probabilitas GERD", value=f"{int(proba * 100)}%")

    if pred == 1:
        st.warning("Saran: Hindari makanan pedas, berlemak, dan jangan tidur setelah makan.")
    else:
        st.success("Pola makan Anda cukup baik. Pertahankan!")

    # Pie chart
    st.progress(proba)
", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="GERD Predictor", layout="centered")

# Halaman navigasi
if "page" not in st.session_state:
    st.session_state.page = "home"

# Halaman 1 - Welcome
if st.session_state.page == "home":
    st.title("GERD Predictor")
    if st.button("Mulai"):
        st.session_state.page = "login"

# Halaman 2 - Login
elif st.session_state.page == "login":
    st.markdown("### L0gin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Masuk"):
        st.session_state.page = "input"
    st.markdown("Tidak mempunyai akun? [Daftar](#)")

# Halaman 3 - Input
elif st.session_state.page == "input":
    st.markdown("### Input Pola Makan")

    input_makanan = st.selectbox("Input makanan", ["Makanan berat", "Snack", "Minuman manis"])
    frekuensi_makan = st.selectbox("Frekuensi makan per minggu", ["<3", "3-5", ">5"])
    makanan_pedas = st.selectbox("Jenis makanan pedas/tidak", ["Ya", "Tidak"])

    if st.button("Prediksi"):
        # Preprocessing dummy sederhana
        df = pd.DataFrame({
            "input_makanan": [input_makanan],
            "frekuensi_makan": [frekuensi_makan],
            "makanan_pedas": [makanan_pedas]
        })

        # Pastikan encodingnya sesuai dengan training model Anda
        prob = model.predict_proba(df)[0][1]
        risk_percent = int(prob * 100)
        st.session_state.risk = risk_percent
        st.session_state.page = "hasil"

# Halaman 4 - Hasil
elif st.session_state.page == "hasil":
    risk = st.session_state.get("risk", 0)
    st.markdown("## Hasil Prediksi")
    st.markdown("### Risiko GERD Anda")

    if risk > 70:
        risiko = "Tinggi"
        saran = "Hindari makanan pedas"
    elif risk > 40:
        risiko = "Sedang"
        saran = "Kurangi makanan berminyak"
    else:
        risiko = "Rendah"
        saran = "Jaga pola makan tetap sehat"

    st.markdown(f"**{risiko}**")
    st.progress(risk)
    st.markdown(f"**{risk}%**")
    st.markdown(f"**Saran:** {saran}")
