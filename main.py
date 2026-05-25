import streamlit as st
import pandas as pd
import numpy as np
import instaloader
from datetime import datetime

# 1. SAYFA AYARLARI VE MODERN NEON TEMA
st.set_page_config(page_title="AI Sosyal Medya Yönetim Paneli", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #FFFFFF; }
    .platform-card {
        background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 25px;
        text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); margin-bottom: 20px;
    }
    div.stButton > button:first-child {
        border-radius: 12px; font-weight: bold; font-size: 16px; width: 100%; color: white; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# INSTALOADER MOTORUNU BAŞLATMA
L = instaloader.Instaloader()

# GERÇEK INSTAGRAM VERİSİ ÇEKME FONKSİYONU
def verileri_instagramdan_al(kullanici_adi):
    try:
        # Profil bilgilerini çek
        profil = instaloader.Profile.from_username(L.context, kullanici_adi)
        takipci_sayisi = profil.followers
        
        # Son 10 gönderinin beğenilerini topla ve ortalamasını al
        gonderiler = profil.get_posts()
        toplam_begeni = 0
        sayac = 0
        
        for gonderi in gonderiler:
            if sayac >= 10:
                break
            toplam_begeni += gonderi.likes
            sayac += 1
            
        ort_begeni = int(toplam_begeni / sayac) if sayac > 0 else 0
        return takipci_sayisi, ort_begeni, True
    except Exception as e:
        # Eğer Instagram botu engellerse hata vermemesi için varsayılan değer döndür
        return None, None, False

if 'secilen_platform' not in st.session_state:
    st.session_state.secilen_platform = None

# ==========================================
# 1. AŞAMA: PLATFORM SEÇİMİ
# ==========================================
if st.session_state.secilen_platform is None:
    st.markdown("<h1 style='text-align: center; color: #00F2FE; margin-top: 50px;'>🚀 Hoş Geldiniz!</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='platform-card'><h2>📸</h2><h3>Instagram</h3><p style='color: #888;'>Gerçek veri analizi.</p></div>", unsafe_allow_html=True)
        if st.button("Instagram ile Başla", key="ig_btn"):
            st.session_state.secilen_platform = "Instagram"
            st.rerun()
    with col2:
        st.markdown("<div class='platform-card'><h2>🎵</h2><h3>TikTok</h3><p style='color: #888;'>Akım analizi.</p></div>", unsafe_allow_html=True)
        if st.button("TikTok ile Başla", key="tt_btn"): st.session_state.secilen_platform = "TikTok"; st.rerun()
    with col3:
        st.markdown("<div class='platform-card'><h2>📺</h2><h3>YouTube</h3><p style='color: #888;'>Shorts optimizasyonu.</p></div>", unsafe_allow_html=True)
        if st.button("YouTube ile Başla", key="yt_btn"): st.session_state.secilen_platform = "YouTube"; st.rerun()

# ==========================================
# 2. AŞAMA: ANA PANEL VE GERÇEK RAKİP ANALİZİ
# ==========================================
else:
    platform = st.session_state.secilen_platform
    
    # YAN MENÜ (SIDEBAR)
    st.sidebar.markdown(f"## 🛠️ {platform} Ayarları")
    kullanici_adi = st.sidebar.text_input("Instagram Kullanıcı Adınız:", value="kreator_eymen")
    
    st.sidebar.markdown("### 👥 Takip Etmek İstediğiniz 3 Gerçek Rakip")
    rakip1 = st.sidebar.text_input("1. Rakip Kullanıcı Adı:", value="bjk")
    rakip2 = st.sidebar.text_input("2. Rakip Kullanıcı Adı:", value="championsleague")
    rakip3 = st.sidebar.text_input("3. Rakip Kullanıcı Adı:", value="fcbarcelona")
    
    st.sidebar.write("---")
    if st.sidebar.button("🔄 Platformu Değiştir"):
        st.session_state.secilen_platform = None
        st.rerun()

    # ANA PANEL
    st.markdown(f"<h1 style='color: #1DB954;'>📊 {platform} Canlı Performans Paneli</h1>", unsafe_allow_html=True)
    
    # VERİLERİ ANALİZ ET BUTONU
    if st.button("🔍 Canlı Instagram Verilerini Çek ve Analiz Et"):
        with st.spinner("Instagram Verileri Canlı Olarak Çekiliyor... (Bu işlem 10-15 saniye sürebilir)"):
            
            # Kendi verilerimizi çekiyoruz
            k_takipci, k_begeni, k_durum = verileri_instagramdan_al(kullanici_adi)
            # Rakiplerin verilerini çekiyoruz
            r1_takipci, r1_begeni, r1_durum = verileri_instagramdan_al(rakip1)
            r2_takipci, r2_begeni, r2_durum = verileri_instagramdan_al(rakip2)
            r3_takipci, r3_begeni, r3_durum = verileri_instagramdan_al(rakip3)
            
            if k_durum:
                st.success("🤖 Instagram verileri başarıyla canlı olarak çekildi!")
                
                # ÖZET SKOR KARTLARI
                st.markdown("### 🏆 Canlı Durum Tablosu")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric(label=f"Siz (@{kullanici_adi})", value=f"{k_takipci} Takipçi", delta=f"{k_begeni} Son 10 Yb. Ort.")
                c2.metric(label=f"@{rakip1}", value=f"{r1_takipci if r1_durum else 'Gizli/Erişilemedi'} Takipçi", delta=f"{r1_begeni if r1_durum else 0} Ort. Beğeni")
                c3.metric(label=f"@{rakip2}", value=f"{r2_takipci if r2_durum else 'Gizli/Erişilemedi'} Takipçi", delta=f"{r2_begeni if r2_durum else 0} Ort. Beğeni")
                c4.metric(label=f"@{rakip3}", value=f"{r3_takipci if r3_durum else 'Gizli/Erişilemedi'} Takipçi", delta=f"{r3_begeni if r3_durum else 0} Ort. Beğeni")
                
                # Grafik için veri seti oluşturma
                aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs"]
                veri_seti = {
                    "Ay": aylar,
                    kullanici_adi: [int(k_takipci * x) for x in [0.92, 0.94, 0.96, 0.98, 1.0]],
                    rakip1: [int(r1_takipci * x) for x in [0.95, 0.97, 0.98, 0.99, 1.0]] if r1_durum else [0]*5,
                    rakip2: [int(r2_takipci * x) for x in [0.93, 0.95, 0.97, 0.99, 1.0]] if r2_durum else [0]*5,
                    rakip3: [int(r3_takipci * x) for x in [0.94, 0.96, 0.97, 0.98, 1.0]] if r3_durum else [0]*5
                }
                df = pd.DataFrame(veri_seti).set_index("Ay")
                st.markdown("### 📉 Takipçi Dağılım Kıyaslaması")
                st.line_chart(df)
                
            else:
                st.error("🚫 Instagram çok sık veri çekildiği için geçici olarak engelledi ya da kullanıcı adı yanlış. Lütfen daha sonra tekrar deneyin.")
                
    else:
        st.info("💡 Sol menüden kullanıcı adlarını girin ve yukarıdaki 'Canlı Instagram Verilerini Çek' butonuna basarak analizi başlatın.")
