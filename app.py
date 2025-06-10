
import streamlit as st
import pandas as pd
import pickle

# Load model
with open("421282fa-a0f7-41d1-9c3c-7a7819f2b93b.pkl", "rb") as f:
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
