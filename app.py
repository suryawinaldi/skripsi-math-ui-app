
import streamlit as st
import sqlite3
import pandas as pd

# Koneksi ke database
conn = sqlite3.connect("Mini Project FIX.db", check_same_thread=False)

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d1b2a, #1b263b);
        background-attachment: fixed;
        color: #ffffff;
    }

    h1 {
        text-align: center;
        color: #ffffff;
    }

    label, .stSelectbox label, .stTextInput label {
        color: #e0e0e0 !important;
    }

    .stButton>button {
        background-color: #3a86ff;
        color: white;
        border-radius: 8px;
    }

    .stDataFrame {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>📚 Sistem Pencarian Data Skripsi Mahasiswa Departemen Matematika FMIPA UI</h1>", unsafe_allow_html=True)

# Dropdown options
peminatan_list = ["Semua"] + [row[0] for row in conn.execute("SELECT DISTINCT PEMINATAN FROM Skripsi").fetchall()]
dosen_list = ["Semua"] + [row[0] for row in conn.execute("SELECT DISTINCT NAMA_DOSEN FROM Dosen").fetchall()]
tahun_list = ["Semua"] + sorted([str(row[0]) for row in conn.execute("SELECT DISTINCT TAHUN FROM Skripsi").fetchall() if row[0]])

# Input
keyword = st.text_input("🔍 Kata kunci dalam judul skripsi:")
peminatan = st.selectbox("📌 Filter Peminatan:", peminatan_list)
dosen = st.selectbox("👨‍🏫 Nama Dosen Pembimbing:", dosen_list)
tahun = st.selectbox("📅 Tahun:", tahun_list)

# Search button
if st.button("Cari Data Skripsi"):
    query = """
    SELECT Skripsi.JUDUL_SKRIPSI, Skripsi.PEMINATAN, Skripsi.TAHUN,
           Mahasiswa.NAMA_MAHASISWA, Dosen.NAMA_DOSEN, Bimbingan.PERAN
    FROM Skripsi
    LEFT JOIN Mahasiswa ON Skripsi.NPM = Mahasiswa.NPM
    LEFT JOIN Bimbingan ON Skripsi.KODE_SKRIPSI = Bimbingan.KODE_SKRIPSI
    LEFT JOIN Dosen ON Bimbingan.NUP_PEMBIMBING = Dosen.NUP
    WHERE 1=1
    """
    params = []

    if keyword:
        query += " AND Skripsi.JUDUL_SKRIPSI LIKE ?"
        params.append(f"%{keyword}%")
    if peminatan != "Semua":
        query += " AND Skripsi.PEMINATAN = ?"
        params.append(peminatan)
    if dosen != "Semua":
        query += " AND Dosen.NAMA_DOSEN = ?"
        params.append(dosen)
    if tahun != "Semua":
        query += " AND Skripsi.TAHUN = ?"
        params.append(tahun)

    df = pd.read_sql_query(query, conn, params=params)
    if not df.empty:
        st.success(f"Ditemukan {len(df)} hasil.")
        st.dataframe(df)
    else:
        st.warning("Tidak ada data yang sesuai.")

# Tampilkan semua data
with st.expander("📖 Tampilkan semua data skripsi"):
    df_all = pd.read_sql_query(
        """
        SELECT Skripsi.JUDUL_SKRIPSI, Skripsi.PEMINATAN, Skripsi.TAHUN,
               Mahasiswa.NAMA_MAHASISWA, Dosen.NAMA_DOSEN, Bimbingan.PERAN
        FROM Skripsi
        LEFT JOIN Mahasiswa ON Skripsi.NPM = Mahasiswa.NPM
        LEFT JOIN Bimbingan ON Skripsi.KODE_SKRIPSI = Bimbingan.KODE_SKRIPSI
        LEFT JOIN Dosen ON Bimbingan.NUP_PEMBIMBING = Dosen.NUP
        """, conn
    )
    st.dataframe(df_all)
