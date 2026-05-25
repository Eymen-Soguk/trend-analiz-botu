import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 1. SAYFA AYARLARI VE MODERN NEON TEMA
st.set_page_config(page_title="AI Sosyal Medya Yönetim Paneli", layout="wide")

# Özel Neon Arayüz Tasarımı (CSS)
st.markdown("""
    <style>
    /* Arka Plan */
    .stApp {
        background-color: #0F172A;
        color: #FFFFFF;
    }
    /* Modern Kart Tasarımları */
    .platform-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    /* Özel Platform Buton Renkleri */
    div.stButton > button:first-child {
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 2. OTURUM DURUMU (SESSION STATE) KONTROLÜ
if 'secilen_platform' not in st.session_state:
    st.session_state.secilen_platform = None

# ==========================================
# 1. AŞAMA: İLK KARŞILAMA VE PLATFORM SEÇİMİ
# ==========================================
if st.session_state.secilen_platform is None:
    st.markdown("<h1 style='text-align: center; color: #00F2FE; margin-top: 50px;'>🚀 Hoş Geldiniz!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #CCCCCC;'>Büyümek İstediğiniz Platformu Seçin</h3>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='platform-card'>
            <h2>📸</h2>
            <h3>Instagram</h3>
            <p style='color: #888;'>Fotoğraf, Reels ve Hikaye odaklı analiz.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Instagram ile Başla", key="ig_btn"):
            st.session_state.secilen_platform = "Instagram"
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class='platform-card'>
            <h2>🎵</h2>
            <h3>TikTok</h3>
            <p style='color: #888;'>Kısa video ve viral akım algoritması.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("TikTok ile Başla", key="tt_btn"):
            st.session_state.secilen_platform = "TikTok"
            st.rerun()
            
    with col3:
        st.markdown("""
        <div class='platform-card'>
            <h2>📺</h2>
            <h3>YouTube</h3>
            <p style='color: #888;'>Uzun video ve Shorts arama optimizasyonu.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("YouTube ile Başla", key="yt_btn"):
            st.session_state.secilen_platform = "YouTube"
            st.rerun()

# ==========================================
# 2. AŞAMA: ANA PANEL VE AKILLI RAKİP ANALİZİ
# ==========================================
else:
    platform = st.session_state.secilen_platform
    
    # YAN MENÜ (SIDEBAR) VERİ GİRİŞİ
    st.sidebar.markdown(f"## 🛠️ {platform} Ayarları")
    kullanici_adi = st.sidebar.text_input("Kullanıcı Adınız:", value="Kreatör_Eymen")
    takipci = st.sidebar.number_input("Takipçi Sayınız:", min_value=0, value=5000, step=100)
    begeni = st.sidebar.number_input("Ortalama Beğeni Sayınız:", min_value=0, value=450, step=10)
    
    st.sidebar.write("---")
    if st.sidebar.button("🔄 Platformu Değiştir"):
        st.session_state.secilen_platform = None
        st.rerun()

    # ANA PANEL BAŞLIĞI
    st.markdown(f"<h1 style='color: #1DB954;'>📊 {platform} Performans Paneli</h1>", unsafe_allow_html=True)
    st.write(f"Hoş geldin **{kullanici_adi}**! Sistem şu an senin verilerine benzer içerikler üreten 3 rakip hesabı otomatik olarak eşleştirdi.")
    
    # AKILLI RAKİP BELİRLEME MOTORU VE VERİ SİMÜLASYONU
    # Sabit random veriler için kullanıcı adına bağlı tohum (seed) atıyoruz
    np.random.seed(len(kullanici_adi) + takipci)
    
    aylar = ["Aralık", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs"]
    
    # Rakiplerin performans dalgalanmalarını simüle etme
    veri_seti = {
        "Ay": aylar,
        kullanici_adi: [int(takipci * x) for x in [0.85, 0.90, 0.94, 0.97, 1.0, 1.02]],
        "Rakip Alfa (Benzer İçerik)": [int(takipci * random.uniform(0.82, 1.05)) for _ in range(6)],
        "Rakip Beta (Dengeli Rakip)": [int(takipci * random.uniform(0.84, 1.03)) for _ in range(6)],
        "Rakip Gama (Yükselen Yıldız)": [int(takipci * random.uniform(0.80, 1.06)) for _ in range(6)]
    }
    
    # Kullanıcının güncel ay verisini tam girdiği değer yapalım
    veri_seti[kullanici_adi][-1] = takipci
    
    df = pd.DataFrame(veri_seti)
    df.set_index("Ay", inplace=True)
    
    # 📈 REKABET VE YÜKSELİŞ ÇIZGİ GRAFİĞİ
    st.markdown("### 📉 Son 6 Aylık Rekabet ve Büyüme Yarışı")
    st.line_chart(df)
    
    # ÖZET SKOR KARTLARI
    st.markdown("### 🏆 Güncel Durum Tablosu")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(label=f"Siz ({kullanici_adi})", value=f"{takipci} Takipçi", delta=f"{begeni} Ort. Beğeni")
    c2.metric(label="Rakip Alfa", value=f"{veri_seti['Rakip Alfa (Benzer İçerik)'][-1]} Takipçi", delta="-1.2%")
    c3.metric(label="Rakip Beta", value=f"{veri_seti['Rakip Beta (Dengeli Rakip)'][-1]} Takipçi", delta="+3.4%")
    c4.metric(label="Rakip Gama", value=f"{veri_seti['Rakip Gama (Yükselen Yıldız)'][-1]} Takipçi", delta="+5.1%")

    # 🤖 AI STRATEJİ KARTI
    st.write("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FE2C55, #1DB954); padding: 20px; border-radius: 12px;'>
        <h4 style='margin-top:0; color: white;'>🧠 Yapay Zeka Strateji Raporu</h4>
        <p style='color: white; font-size: 15px;'>
            <b>Analiz Sonucu:</b> Rakiplerinle benzer beğeni oranlarına sahipsin fakat <b>Rakip Gama</b> son iki ayda dikey video geçiş efektlerini kullanarak öne geçmiş durumda.<br>
            <b>Öneri Taktik:</b> Profilini öne geçirmek için önümüzdeki 7 gün boyunca trend olan sesleri ilk 3 saniyede kancayla (hook) birleştirerek paylaşım yapmalısın.
        </p>
    </div>
    """, unsafe_allow_html=True)
