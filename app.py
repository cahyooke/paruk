import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os

# Set konfigurasi halaman
st.set_page_config(page_title="Prediksi Kebutuhan Energi Bangunan", layout="wide")

# Cek file di direktori
st.sidebar.write("📁 File yang tersedia:")
st.sidebar.write(os.listdir())

# Coba load model
try:
    model = joblib.load("model_energy_efficiency.pkl")  # pastikan nama file .pkl benar
except Exception as e:
    st.error("❌ Gagal memuat model. Pastikan file 'model_energy_efficiency.pkl' tersedia.")
    st.exception(e)
    st.stop()

# Judul aplikasi
st.title("🏢 Prediksi Kebutuhan Energi Bangunan")
st.markdown("Masukkan nilai-nilai fitur bangunan di bawah ini:")

# Buat dua kolom
col1, col2 = st.columns([2, 1])

# --- Kolom input (kiri)
with col1:
    X1 = st.slider("Relative Compactness (X1)", 0.5, 1.0, 0.75)
    X2 = st.slider("Surface Area (X2)", 500.0, 900.0, 750.0)
    X3 = st.slider("Wall Area (X3)", 250.0, 420.0, 300.0)
    X4 = st.slider("Roof Area (X4)", 100.0, 390.0, 150.0)
    X5 = st.slider("Overall Height (X5)", 3.5, 7.0, 5.25)
    X6 = st.selectbox("Orientation (X6)", [2, 3, 4, 5])
    X7 = st.selectbox("Glazing Area (X7)", [0.0, 0.1, 0.25, 0.4])
    X8 = st.selectbox("Glazing Area Distribution (X8)", [0, 1, 2, 3, 4, 5])
    predict_button = st.button("🔍 Prediksi Kebutuhan Energi")

# --- Kolom output (kanan)
with col2:
    st.subheader("Hasil Prediksi")

    if predict_button:
        try:
            input_data = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
            prediction = float(model.predict(input_data)[0])  # pastikan tipe numerik

            # Kategorisasi nilai energi
            if prediction < 15:
                label = "Rendah"
            elif prediction < 30:
                label = "Sedang"
            else:
                label = "Tinggi"

            st.metric(label="Nilai Prediksi", value=f"{prediction:.2f}")
            st.success(f"Kategori Energi: **{label}**")

        except Exception as e:
            st.error("❌ Gagal menjalankan prediksi.")
            st.exception(e)
