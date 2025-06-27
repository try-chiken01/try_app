# File: models/user.py

import streamlit as st
from utils.db_handler import get_db_connection
from models.tugas import Tugas
from models.penawaran import Penawaran
import pandas as pd
import sqlite3

class User:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    def get_id(self):
        return self.id


class Mahasiswa(User):
    def __init__(self, id, username):
        super().__init__(id, username, "mahasiswa")

    def create_task_form(self):
        with st.form("form_buat_tugas"):
            judul = st.text_input("Judul Tugas")
            deskripsi = st.text_area("Deskripsi")
            deadline = st.date_input("Deadline")
            budget = st.number_input("Budget (Rp)", min_value=0)
            submit = st.form_submit_button("Buat Tugas")

            if submit:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tugas (judul, deskripsi, deadline, budget, mahasiswa_id, status) VALUES (?, ?, ?, ?, ?, ?)",
                               (judul, deskripsi, str(deadline), budget, self.id, "Open"))
                conn.commit()
                conn.close()
                st.success("Tugas berhasil dibuat!")

    def show_own_tasks(self):
        conn = get_db_connection()
        df = pd.read_sql_query(f"SELECT * FROM tugas WHERE mahasiswa_id = {self.id}", conn)
        conn.close()
        st.dataframe(df)

    def manage_offers(self):
        st.subheader("Penawaran Masuk")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, t.judul, u.username as joki, p.harga, p.status
            FROM penawaran p
            JOIN tugas t ON p.tugas_id = t.id
            JOIN users u ON p.joki_id = u.id
            WHERE t.mahasiswa_id = ? AND t.status = 'Open'
        """, (self.id,))
        rows = cursor.fetchall()
        for row in rows:
            st.write(f"Tugas: {row['judul']} | Joki: {row['joki']} | Penawaran: Rp{row['harga']} | Status: {row['status']}")
            if row['status'] == 'Menunggu':
                if st.button(f"Terima Penawaran #{row['id']}"):
                    cursor.execute("UPDATE penawaran SET status = 'Diterima' WHERE id = ?", (row['id'],))
                    cursor.execute("UPDATE tugas SET joki_id = (SELECT joki_id FROM penawaran WHERE id = ?), status = 'Dalam Pengerjaan' WHERE id = (SELECT tugas_id FROM penawaran WHERE id = ?)", (row['id'], row['id']))
                    conn.commit()
                    st.success("Penawaran diterima!")
                    st.rerun()
        conn.close()


class Joki(User):
    def __init__(self, id, username):
        super().__init__(id, username, "joki")

    def list_available_tasks(self):
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM tugas WHERE status = 'Open'", conn)
        conn.close()
        for index, row in df.iterrows():
            st.write(f"**{row['judul']}** - {row['deskripsi']} | Budget: Rp{row['budget']}")
            with st.form(f"form_penawaran_{row['id']}"):
                harga = st.number_input("Tawarkan Harga", min_value=0, key=f"harga_{row['id']}")
                submit = st.form_submit_button("Kirim Penawaran")
                if submit:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO penawaran (tugas_id, joki_id, harga, status) VALUES (?, ?, ?, ?)",
                                   (row['id'], self.id, harga, "Menunggu"))
                    conn.commit()
                    conn.close()
                    st.success("Penawaran dikirim!")

    def manage_submissions(self):
        st.subheader("Tugas Anda")
        conn = get_db_connection()
        df = pd.read_sql_query(f"SELECT * FROM tugas WHERE joki_id = {self.id}", conn)
        conn.close()
        for index, row in df.iterrows():
            st.write(f"**{row['judul']}** - Status: {row['status']}")
            if row['status'] == "Dalam Pengerjaan":
                if st.button(f"Tandai Selesai #{row['id']}"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tugas SET status = 'Selesai' WHERE id = ?", (row['id'],))
                    conn.commit()
                    conn.close()
                    st.success("Status tugas diperbarui menjadi 'Selesai'")
                    st.rerun()
