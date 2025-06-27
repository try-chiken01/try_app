# File: app.py

import streamlit as st
from utils.auth import login_user, register_user, get_current_user
from utils.db_handler import init_db
from models.user import Mahasiswa, Joki
from models.tugas import Tugas
from models.penawaran import Penawaran
import pandas as pd

# Inisialisasi database
init_db()

# Session state untuk login
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Routing utama
menu = ["Login", "Register"] if not st.session_state['user'] else ["Dashboard", "Tugas", "Statistik", "Logout"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    login_user()

elif choice == "Register":
    register_user()

elif choice == "Logout":
    st.session_state['user'] = None
    st.rerun()

elif choice == "Dashboard":
    user = get_current_user()
    st.title(f"Selamat datang, {user.username} ({user.role})")
    if user.role == "mahasiswa":
        st.subheader("Tugas Anda")
        user.show_own_tasks()
        st.subheader("Buat Tugas Baru")
        user.create_task_form()
    elif user.role == "joki":
        st.subheader("Daftar Tugas Tersedia")
        user.list_available_tasks()

elif choice == "Tugas":
    user = get_current_user()
    if user.role == "mahasiswa":
        user.manage_offers()
    elif user.role == "joki":
        user.manage_submissions()

elif choice == "Statistik":
    st.title("Statistik Aplikasi")
    df_tugas = pd.read_sql_query("SELECT * FROM tugas", init_db())
    df_penawaran = pd.read_sql_query("SELECT * FROM penawaran", init_db())
    st.metric("Total Tugas", len(df_tugas))
    if len(df_penawaran) > 0:
        rata2 = df_penawaran.groupby('joki_id')['harga'].mean()
        st.write("Rata-rata Penawaran per Joki:")
        st.dataframe(rata2)

# Catatan:
# - Fungsi seperti user.show_own_tasks(), user.create_task_form(), dsb. akan didefinisikan di masing-masing kelas
# - File lainnya seperti models/user.py, tugas.py, utils/auth.py akan berisi definisi fungsi dan integrasi
# - Dummy data bisa ditambahkan saat init_db() dijalankan pertama kali
