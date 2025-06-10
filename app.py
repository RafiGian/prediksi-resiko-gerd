import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Risiko GERD",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS Custom untuk styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset dan styling umum */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Question container */
    .question-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .question-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Progress bar custom */
    .progress-container {
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #48bb78, #38a169);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Result styling */
    .result-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .risk-indicator {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin: 0 auto 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #48bb78, #38a169);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ed8936, #dd6b20);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #f56565, #e53e3e);
    }
    
    .result-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #2d3748;
    }
    
    .result-description {
        font-size: 1rem;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    /* Recommendations styling */
    .recommendations {
        background: #f8fafc;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        text-align: left;
        border-left: 4px solid #667eea;
    }
    
    .recommendations h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .recommendations ul {
        list-style: none;
        padding: 0;
    }
    
    .recommendations li {
        padding: 0.5rem 0;
        border-bottom: 1px solid #e2e8f0;
        font-size: 0.9rem;
        color: #4a5568;
    }
    
    .recommendations li:last-child {
        border-bottom: none;
    }
    
    .recommendations li::before {
        content: '✓';
        color: #48bb78;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Radio button styling */
    .stRadio > div {
        background: rgba(255,255,255,0.8);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric styling */
    .metric-container {
        background: rgba(255,255,255,0.9);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk menghitung risiko GERD
def calculate_gerd_risk(answers):
    """
    Menghitung risiko GERD berdasarkan jawaban pengguna
    """
    total_score = sum(answers.values())
    
    # Konversi skor ke persentase (skor min: 8, max: 32)
    risk_percentage = min(round(((total_score - 8) / (32 - 8)) * 100), 100)
    
    if risk_percentage <= 30:
        return {
            'percentage': risk_percentage,
            'level': 'Rendah',
            'class': 'risk-low',
            'title': 'Risiko Rendah',
            'description': 'Berdasarkan evaluasi, Anda memiliki risiko rendah untuk mengalami GERD. Pertahankan gaya hidup sehat Anda.',
            'color': '#48bb78'
        }
    elif risk_percentage <= 60:
        return {
            'percentage': risk_percentage,
            'level': 'Sedang',
            'class': 'risk-medium',
            'title': 'Risiko Sedang',
            'description': 'Anda memiliki risiko sedang untuk mengalami GERD. Disarankan untuk mulai memperhatikan pola makan dan gaya hidup.',
            'color': '#ed8936'
        }
    else:
        return {
            'percentage': risk_percentage,
            'level': 'Tinggi',
            'class': 'risk-high',
            'title': 'Risiko Tinggi',
            'description': 'Anda memiliki risiko tinggi untuk mengalami GERD. Sangat disarankan untuk berkonsultasi dengan dokter.',
            'color': '#f56565'
        }

# Fungsi untuk mendapatkan rekomendasi
def get_recommendations(risk_level, answers):
    """
    Memberikan rekomendasi berdasarkan tingkat risiko dan jawaban
    """
    base_recommendations = [
        "Konsultasikan dengan dokter untuk evaluasi lebih lanjut",
        "Hindari makanan pemicu seperti makanan pedas dan asam",
        "Jaga berat badan ideal",
        "Hindari makan 3 jam sebelum tidur",
        "Tidur dengan posisi kepala lebih tinggi"
    ]
    
    additional_recommendations = []
    
    # Rekomendasi berdasarkan BMI
    if answers.get('bmi', 1) >= 3:
        additional_recommendations.append("Konsultasi dengan ahli gizi untuk program penurunan berat badan")
    
    # Rekomendasi berdasarkan kebiasaan merokok
    if answers.get('smoking', 1) >= 3:
        additional_recommendations.append("Pertimbangkan untuk berhenti merokok atau mengurangi konsumsi")
    
    # Rekomendasi berdasarkan konsumsi alkohol
    if answers.get('alcohol', 1) >= 3:
        additional_recommendations.append("Kurangi konsumsi alkohol")
    
    # Rekomendasi berdasarkan pola makan
    if answers.get('eating_pattern', 1) >= 3:
        additional_recommendations.append("Atur pola makan menjadi lebih teratur dengan porsi yang lebih kecil")
    
    return base_recommendations + additional_recommendations

# Fungsi untuk membuat gauge chart risiko
def create_risk_gauge(risk_percentage, color):
    """
    Membuat gauge chart untuk menampilkan risiko
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Tingkat Risiko GERD", 'font': {'size': 20, 'color': '#2d3748'}},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(72, 187, 120, 0.3)'},
                {'range': [30, 60], 'color': 'rgba(237, 137, 54, 0.3)'},
                {'range': [60, 100], 'color': 'rgba(245, 101, 101, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        font={'color': "#2d3748", 'family': "Inter"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Inisialisasi session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

# Header utama
st.markdown("""
<div class="main-header">
    <h1>🏥 Prediksi Risiko GERD</h1>
    <p>Evaluasi risiko Gastroesophageal Reflux Disease Anda</p>
</div>
""", unsafe_allow_html=True)

# Definisi pertanyaan
questions = {
    1: {
        'title': 'Berapa usia Anda saat ini?',
        'key': 'age',
        'options': [
            'Di bawah 30 tahun',
            '30-45 tahun', 
            '46-60 tahun',
            'Di atas 60 tahun'
        ]
    },
    2: {
        'title': 'Bagaimana kondisi berat badan Anda?',
        'key': 'bmi',
        'options': [
            'Underweight (BMI < 18.5)',
            'Normal (BMI 18.5-24.9)',
            'Overweight (BMI 25-29.9)',
            'Obese (BMI ≥ 30)'
        ]
    },
    3: {
        'title': 'Apakah Anda merokok atau pernah merokok?',
        'key': 'smoking',
        'options': [
            'Tidak pernah merokok',
            'Mantan perokok (berhenti > 1 tahun)',
            'Perokok ringan (< 10 batang/hari)',
            'Perokok berat (≥ 10 batang/hari)'
        ]
    },
    4: {
        'title': 'Seberapa sering Anda mengonsumsi alkohol?',
        'key': 'alcohol',
        'options': [
            'Tidak pernah',
            'Kadang-kadang (1-2x/bulan)',
            'Sering (1-3x/minggu)',
            'Sangat sering (hampir setiap hari)'
        ]
    },
    5: {
        'title': 'Seberapa sering Anda mengonsumsi makanan pedas atau asam?',
        'key': 'spicy_food',
        'options': [
            'Sangat jarang',
            'Kadang-kadang',
            'Sering',
            'Hampir setiap hari'
        ]
    },
    6: {
        'title': 'Bagaimana pola makan Anda?',
        'key': 'eating_pattern',
        'options': [
            'Teratur, 3 kali sehari, tidak terlalu kenyang',
            'Kadang tidak teratur, porsi sedang',
            'Sering tidak teratur, porsi besar',
            'Sangat tidak teratur, sering makan berlebihan'
        ]
    },
    7: {
        'title': 'Apakah Anda sering mengalami gejala seperti heartburn atau regurgitasi?',
        'key': 'symptoms',
        'options': [
            'Tidak pernah',
            'Sangat jarang (< 1x/bulan)',
            'Kadang-kadang (1-2x/minggu)',
            'Sering (3x/minggu atau lebih)'
        ]
    },
    8: {
        'title': 'Apakah ada riwayat keluarga dengan GERD atau masalah pencernaan?',
        'key': 'family_history',
        'options': [
            'Tidak ada riwayat keluarga',
            'Riwayat keluarga jauh',
            'Riwayat keluarga dekat (kakek/nenek)',
            'Riwayat keluarga langsung (orangtua/saudara)'
        ]
    }
}

# Progress bar
progress = (st.session_state.current_question - 1) / len(questions) * 100
st.markdown(f"""
<div class="progress-container">
    <div class="progress-bar" style="width: {progress}%"></div>
</div>
<p style="text-align: center; color: white; font-weight: 500; margin-bottom: 2rem;">
    Pertanyaan {st.session_state.current_question} dari {len(questions)}
</p>
""", unsafe_allow_html=True)

# Tampilkan pertanyaan atau hasil
if not st.session_state.show_result:
    current_q = questions[st.session_state.current_question]
    
    st.markdown(f"""
    <div class="question-container">
        <div class="question-title">{current_q['title']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Radio button untuk pilihan jawaban
    answer = st.radio(
        "Pilih jawaban Anda:",
        options=range(len(current_q['options'])),
        format_func=lambda x: current_q['options'][x],
        key=f"q_{st.session_state.current_question}",
        label_visibility="collapsed"
    )
    
    # Tombol navigasi
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_question > 1:
            if st.button("◀ Kembali", key="prev_btn"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col3:
        if st.session_state.current_question < len(questions):
            if st.button("Selanjutnya ▶", key="next_btn"):
                st.session_state.answers[current_q['key']] = answer + 1
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("Lihat Hasil 🎯", key="result_btn"):
                st.session_state.answers[current_q['key']] = answer + 1
                st.session_state.show_result = True
                st.rerun()

else:
    # Tampilkan hasil
    risk_result = calculate_gerd_risk(st.session_state.answers)
    recommendations = get_recommendations(risk_result['level'], st.session_state.answers)
    
    st.markdown(f"""
    <div class="result-container">
        <div class="risk-indicator {risk_result['class']}">
            {risk_result['percentage']}%
        </div>
        <div class="result-title">{risk_result['title']}</div>
        <div class="result-description">{risk_result['description']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Gauge chart
    fig = create_risk_gauge(risk_result['percentage'], risk_result['color'])
    st.plotly_chart(fig, use_container_width=True)
    
    # Rekomendasi
    st.markdown(f"""
    <div class="recommendations">
        <h3>🎯 Rekomendasi untuk Anda:</h3>
        <ul>
            {''.join([f'<li>{rec}</li>' for rec in recommendations])}
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Tombol untuk mengulang
    if st.button("🔄 Mulai Ulang Assessment", key="restart_btn"):
        st.session_state.current_question = 1
        st.session_state.answers = {}
        st.session_state.show_result = False
        st.rerun()
    
    # Informasi tambahan
    st.markdown("""
    <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin-top: 2rem; border-left: 4px solid #667eea;">
        <h4 style="color: #2d3748; margin-bottom: 1rem;">ℹ️ Informasi Penting</h4>
        <p style="color: #64748b; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0;">
            Hasil prediksi ini hanya untuk referensi dan tidak menggantikan diagnosis medis profesional. 
            Jika Anda mengalami gejala yang mengkhawatirkan, segera konsultasikan dengan dokter.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; color: rgba(255,255,255,0.8); font-size: 0.9rem;">
    <p>© 2024 Aplikasi Prediksi Risiko GERD - Dibuat dengan ❤️ menggunakan Streamlit</p>
</div>
""", unsafe_allow_html=True)
