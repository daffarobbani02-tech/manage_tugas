from datetime import date

from models import Tugas, TugasKuliah, TugasKelompok, MataKuliah
from utils.validasi import (valid_teks, valid_estimasi, valid_bobot,
                            valid_anggota)
from .analisis_beban import AnalisisBeban


class PengaturBeban:
    """Menyimpan data (di memori) dan mengatur alur aplikasi."""

    def __init__(self, analisis=None):
        self.daftar_tugas = {}   # kode -> Tugas
        self.daftar_matkul = {}  # kode -> MataKuliah
        self._analisis = analisis if analisis is not None else AnalisisBeban()

    # ---------- data master ----------
    def tambah_matkul(self, kode, nama, sks):
        if not (valid_teks(kode) and valid_teks(nama)):
            raise ValueError("Kode dan nama mata kuliah tidak boleh kosong.")
        if not (isinstance(sks, int) and 1 <= sks <= 6):
            raise ValueError("SKS harus bilangan bulat 1 sampai 6.")
        if kode in self.daftar_matkul:
            raise ValueError(f"Kode mata kuliah {kode} sudah digunakan.")
        matkul = MataKuliah(kode, nama, sks)
        self.daftar_matkul[kode] = matkul
        return matkul

    def tambah_tugas(self, tugas):
        if not isinstance(tugas, Tugas):
            raise ValueError("Objek yang ditambahkan bukan Tugas.")
        if not (valid_teks(tugas.kode) and valid_teks(tugas.judul)):
            raise ValueError("Kode dan judul tugas tidak boleh kosong.")
        if tugas.kode in self.daftar_tugas:
            raise ValueError(f"Kode tugas {tugas.kode} sudah digunakan.")
        if not isinstance(tugas.deadline, date):
            raise ValueError("Deadline harus berupa tanggal.")
        if not valid_estimasi(tugas.estimasi_jam):
            raise ValueError("Estimasi jam harus bilangan bulat positif.")
        if isinstance(tugas, TugasKuliah):
            if not valid_bobot(tugas.bobot):
                raise ValueError("Bobot harus bilangan bulat 1 sampai 100.")
            if self.daftar_matkul.get(tugas.matkul.kode) is not tugas.matkul:
                raise ValueError("Mata kuliah belum terdaftar.")
        if isinstance(tugas, TugasKelompok) and not valid_anggota(tugas.jumlah_anggota):
            raise ValueError("Tugas kelompok minimal 2 anggota.")
        self.daftar_tugas[tugas.kode] = tugas
        return tugas

    def cari_tugas(self, kode):
        tugas = self.daftar_tugas.get(kode)
        if tugas is None:
            raise ValueError(f"Tugas {kode} tidak ditemukan.")
        return tugas

    def tandai_selesai(self, kode):
        tugas = self.cari_tugas(kode)
        tugas.tandai_selesai()  # ValueError jika sudah selesai
        return tugas

    # ---------- tampilan data ----------
    def daftar_urut_prioritas(self, hari_ini):
        """Tugas belum selesai, skor tertinggi dulu (seri: deadline lebih dekat)."""
        belum = [t for t in self.daftar_tugas.values() if not t.selesai]
        return sorted(
            belum,
            key=lambda t: (-t.hitung_prioritas(hari_ini), t.deadline, t.kode),
        )

    # ---------- analisis (didelegasikan) ----------
    def cek_minggu_kritis(self, hari_ini):
        """Hanya tugas belum selesai yang deadline-nya belum lewat."""
        mendatang = [t for t in self.daftar_tugas.values()
                     if not t.selesai and t.deadline >= hari_ini]
        return self._analisis.minggu_kritis(mendatang)

    def buat_saran(self, hari_ini):
        """List of (tugas, tanggal_mulai, hari_dibutuhkan, sudah_lewat), urut prioritas."""
        saran = []
        for tugas in self.daftar_urut_prioritas(hari_ini):
            mulai, hari, lewat = self._analisis.saran_mulai(tugas, hari_ini)
            saran.append((tugas, mulai, hari, lewat))
        return saran