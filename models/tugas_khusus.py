from .tugas import Tugas
from .matakuliah import MataKuliah


class TugasKuliah(Tugas):
    """Tugas dari mata kuliah. Bobot nilai besar menaikkan prioritas."""

    def __init__(self, kode, judul, deadline, estimasi_jam, matkul: MataKuliah, bobot):
        super().__init__(kode, judul, deadline, estimasi_jam)
        self.matkul = matkul
        self.bobot = bobot  # persen terhadap nilai akhir, contoh 20

    def hitung_prioritas(self, hari_ini):
        return self.skor_urgensi(hari_ini) + self.bobot * 0.5

    def __str__(self):
        return f"{super().__str__()} | Kuliah: {self.matkul.nama} (bobot {self.bobot}%)"


class TugasKelompok(Tugas):
    """Tugas kelompok. Butuh koordinasi, jadi prioritas ditambah tetap."""

    def __init__(self, kode, judul, deadline, estimasi_jam, jumlah_anggota):
        super().__init__(kode, judul, deadline, estimasi_jam)
        self.jumlah_anggota = jumlah_anggota

    def hitung_prioritas(self, hari_ini):
        return self.skor_urgensi(hari_ini) + 10

    def __str__(self):
        return f"{super().__str__()} | Kelompok: {self.jumlah_anggota} anggota"


class TugasPribadi(Tugas):
    """Tugas pribadi. Paling fleksibel, jadi skornya diturunkan."""

    def hitung_prioritas(self, hari_ini):
        return self.skor_urgensi(hari_ini) * 0.7

    def __str__(self):
        return f"{super().__str__()} | Pribadi"