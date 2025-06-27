# File: utils/auth.py

import streamlit as st
from utils.db_handler import get_db_connection
from models.user import Mahasiswa, Joki
import sqlite3

def login_user():
    st.header("Login Pengguna")
    with st.form("form_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                if user['role'] == 'mahasiswa':
                    st.session_state['user'] = Mahasiswa(user['id'], user['username'])
                elif user['role'] == 'joki':
                    st.session_state['user'] = Joki(user['id'], user['username'])
                st.success(f"Berhasil login sebagai {user['role']}")
                st.rerun()
            else:
                st.error("Username atau password salah")

def register_user():
    st.header("Registrasi Pengguna Baru")
    with st.form("form_register"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Daftar sebagai", ["mahasiswa", "joki"])
        submitted = st.form_submit_button("Daftar")

        if submitted:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (username, password, role))
                conn.commit()
                conn.close()
                st.success("Registrasi berhasil! Silakan login.")
            except sqlite3.IntegrityError:
                st.error("Username sudah digunakan. Coba yang lain.")

def get_current_user():
    return st.session_state.get('user')
