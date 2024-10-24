import streamlit as st
import pandas as pd

# Baca data dari file Excel
file_path = '/Users/macbookair/Desktop/Virtual Pyhton/Data Izin DPMPTSP.xlsx'
sheet_name = 'Data Izin All'
df = pd.read_excel(file_path, sheet_name=sheet_name)


# Jika 'total_revisi' ada, konversi tipe datanya
if 'total_revisi' in df.columns:
    df['total_revisi'] = pd.to_numeric(df['total_revisi'], errors='coerce').fillna(0).astype(int)



st.title("Dashboard Perizinan Investasi di Indonesia")
st.write("Data Perizinan Investasi Berdasarkan Wilayah")

# Tampilkan dataframe di Streamlit untuk verifikasi
st.dataframe(df)

# Agregasi data
total_izin = df['total_diajukan'].sum()  # Kolom total_diajukan
average_izin = df['total_diajukan'].mean()
selesai_diproses = df['total_selesai'].sum()  # Kolom total_selesai
ditolak_dibatalkan = df['total_di_tolak'].sum() + df['total_dibatalkan'].sum()  # Kolom total_di_tolak + total_dibatalkan
masih_diproses = df['total_proses'].sum()  # Kolom total_proses

# Buat box untuk menampilkan data agregat
st.metric("Total Izin", total_izin)
st.metric("Rata-rata Izin", average_izin)
st.metric("Selesai Diproses", selesai_diproses)
st.metric("Ditolak/Dibatalkan", ditolak_dibatalkan)
st.metric("Masih Diproses", masih_diproses)

# Dropdown untuk filter berdasarkan wilayah (kota/kecamatan)
wilayah = st.selectbox('Pilih Wilayah', df['Kec'].unique())  # Kolom Kec

# Filter data berdasarkan wilayah yang dipilih
filtered_df = df[df['Kec'] == wilayah]

# Tampilkan data yang terfilter
st.write(f"Data untuk {wilayah}")
st.dataframe(filtered_df)

st.markdown("---")

import plotly.express as px

# Buat pie chart untuk kategori izin per bidang
pie_chart = px.pie(filtered_df, names='Bidang_Recode', title='Distribusi Kategori Izin Per Bidang')  # Kolom Bidang_Recode
st.plotly_chart(pie_chart)

# List bidang per kecamatan
list_bidang = filtered_df['Bidang_Recode'].unique()  # Kolom Bidang_Recode
st.write(f"Daftar Bidang di {wilayah}:")
st.write(list_bidang)
