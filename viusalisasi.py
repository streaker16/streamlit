import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set konfigurasi halaman Streamlit
st.set_page_config(page_title="DPMPTSP Dashboard", layout="wide")

# Header
t1, t2 = st.columns((0.07, 1))

# Pastikan untuk menyesuaikan path logo jika diperlukan
#t1.image('images/dpmptsp_logo2.jpeg', width=100)
t2.title('Dashboard Tipologi DPMPTSP Jakarta')
t2.markdown("**tel :** 1500164 / (021)1500164 **| website :** https://pelayanan.jakarta.go.id/ **")

with st.spinner('Updating Report ....'):
    # Membaca data dari Excel
    file_path = 'D:\Penyimpanan Utama\Documents\Skilvul\Python Dasar\Data Izin DPMPTSP.xlsx'
    
    # Membaca service point
    sp_izin_df = pd.read_excel(file_path, sheet_name='Data Izin All')
    
    # Mengambil daftar service point unik
    service_points = sp_izin_df['service_point'].unique()
    sp = st.selectbox('Choose Service Point', service_points, help='Filter report to show only one service point of penanaman modal')

    # label logic: menentukan level
    if sp.startswith('Kantor Camat'):
        level = 'kecamatan'
    elif sp.startswith('Kantor Lurah'):
        level = 'kelurahan'
    else:
        level = 'kota / kabupaten'

    # Data total izin berdasarkan status
    total_izin = sp_izin_df[sp_izin_df['service_point'] == sp]['total_diajukan'].sum()
    average_izin = sp_izin_df[sp_izin_df['service_point'] == sp]['total_diajukan'].mean()
    selesai_diproses = sp_izin_df[sp_izin_df['service_point'] == sp]['total_selesai'].sum()
    ditolak_dibatalkan = (sp_izin_df[sp_izin_df['service_point'] == sp]['total_di_tolak'].sum() +
                          sp_izin_df[sp_izin_df['service_point'] == sp]['total_dibatalkan'].sum())
    masih_diproses = sp_izin_df[sp_izin_df['service_point'] == sp]['total_proses'].sum()

    # Persentase
    selesai_perc = (selesai_diproses / total_izin * 100) if total_izin else 0
    ditolak_perc = (ditolak_dibatalkan / total_izin * 100) if total_izin else 0
    masih_perc = (masih_diproses / total_izin * 100) if total_izin else 0

    # Data untuk pie chart berdasarkan 'Bidang_Recode'
    pcdf = sp_izin_df[sp_izin_df['service_point'] == sp]

    # Membuat layout subplot untuk menampilkan metrik dan pie chart
    fig = make_subplots(
        rows=2, cols=4,  # 4 kolom untuk metrik dan 1 baris tambahan untuk pie chart
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
               [{"colspan": 4, "type": "domain"}, None, None, None]],  # Pie chart akan mengambil seluruh kolom (4)
        subplot_titles=["", "", "", "", "Distribusi Bidang Recode"]
    )

    # Menambahkan indikator ke dalam subplot
    fig.add_trace(go.Indicator(
        mode="number",
        value=total_izin,
        title={"text": "Total Izin yang Diajukan"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="number",
        value=average_izin,
        title={"text": f"Rata-rata Izin per {level.capitalize()}"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=2)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=selesai_diproses,
        delta={'reference': total_izin, 'relative': True},
        title={"text": "Selesai Diproses"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=3)

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=ditolak_dibatalkan,
        delta={'reference': total_izin, 'relative': True},
        title={"text": "Ditolak & Dibatalkan"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ), row=1, col=4)

    # Menambahkan pie chart di bawah indikator
    fig.add_trace(go.Pie(
        labels=pcdf['Bidang_Recode'], 
        values=pcdf['total_diajukan'], 
        hole=.3
    ), row=2, col=1)  # Pie chart ada di baris kedua dan kolom pertama

    # Memperbarui layout keseluruhan
    fig.update_layout(
        title_text="Statistik Izin DPMPTSP Jakarta",
        height=600,
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    # Menampilkan grafik di Streamlit
    st.plotly_chart(fig, use_container_width=True)
