# File: utils/db_handler.py

import sqlite3
import os

DB_PATH = os.path.join("data", "database.db")

# Koneksi ke database

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Agar bisa akses dengan nama kolom
    return conn

# Inisialisasi database: membuat tabel jika belum ada
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT CHECK(role IN ('mahasiswa', 'joki')) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT,
            deskripsi TEXT,
            deadline TEXT,
            budget INTEGER,
            mahasiswa_id INTEGER,
            joki_id INTEGER,
            status TEXT,
            FOREIGN KEY(mahasiswa_id) REFERENCES users(id),
            FOREIGN KEY(joki_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penawaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tugas_id INTEGER,
            joki_id INTEGER,
            harga INTEGER,
            status TEXT,
            FOREIGN KEY(tugas_id) REFERENCES tugas(id),
            FOREIGN KEY(joki_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

    return get_db_connection()  # agar bisa langsung dipakai di app.py

