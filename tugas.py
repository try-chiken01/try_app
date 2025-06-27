# File: models/tugas.py

class Tugas:
    def __init__(self, id, judul, deskripsi, deadline, budget, mahasiswa_id, status="Open", joki_id=None):
        self.id = id
        self.judul = judul
        self.deskripsi = deskripsi
        self.deadline = deadline
        self.budget = budget
        self.mahasiswa_id = mahasiswa_id
        self.status = status
        self.joki_id = joki_id

    def to_dict(self):
        return {
            "id": self.id,
            "judul": self.judul,
            "deskripsi": self.deskripsi,
            "deadline": self.deadline,
            "budget": self.budget,
            "mahasiswa_id": self.mahasiswa_id,
            "status": self.status,
            "joki_id": self.joki_id
        }
