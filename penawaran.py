# File: models/penawaran.py

class Penawaran:
    def __init__(self, id, tugas_id, joki_id, harga, status="Menunggu"):
        self.id = id
        self.tugas_id = tugas_id
        self.joki_id = joki_id
        self.harga = harga
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "tugas_id": self.tugas_id,
            "joki_id": self.joki_id,
            "harga": self.harga,
            "status": self.status
        }
