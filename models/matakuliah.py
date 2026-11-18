class MataKuliah:
    """Data sebuah mata kuliah."""

    def __init__(self, kode, nama, sks):
        self.kode = kode
        self.nama = nama
        self.sks = sks

    def __str__(self):
        return f"[{self.kode}] {self.nama} ({self.sks} SKS)"