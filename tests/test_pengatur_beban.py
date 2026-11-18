import unittest
from datetime import date

from models import MataKuliah, TugasKuliah, TugasKelompok, TugasPribadi
from services import PengaturBeban

HARI_INI = date(2026, 11, 18)


class TestPengaturBeban(unittest.TestCase):
    def setUp(self):
        self.service = PengaturBeban()
        self.pbo = self.service.tambah_matkul("IF201", "PBO", 3)

    def isi_data(self):
        s = self.service
        s.tambah_tugas(TugasKuliah("T1", "Laporan", date(2026, 11, 20), 6, self.pbo, 30))
        s.tambah_tugas(TugasKelompok("T2", "Proyek", date(2026, 11, 20), 15, 3))
        s.tambah_tugas(TugasPribadi("T3", "Belajar", date(2026, 11, 20), 4))
        s.tambah_tugas(TugasPribadi("T4", "Telat", date(2026, 11, 10), 2))

    def test_tambah_matkul(self):
        self.assertIn("IF201", self.service.daftar_matkul)
        with self.assertRaises(ValueError):
            self.service.tambah_matkul("IF201", "Duplikat", 3)
        with self.assertRaises(ValueError):
            self.service.tambah_matkul("IF202", "", 3)
        with self.assertRaises(ValueError):
            self.service.tambah_matkul("IF202", "X", 9)

    def test_tambah_tugas_valid(self):
        self.isi_data()
        self.assertEqual(len(self.service.daftar_tugas), 4)

    def test_tambah_tugas_ditolak(self):
        self.isi_data()
        s = self.service
        salah = [
            TugasPribadi("T1", "kode kembar", date(2026, 11, 20), 3),
            TugasPribadi("T9", "", date(2026, 11, 20), 3),
            TugasPribadi("T9", "x", date(2026, 11, 20), 0),
            TugasPribadi("T9", "x", "20-11-2026", 3),
            TugasKuliah("T9", "x", date(2026, 11, 20), 3, self.pbo, 150),
            TugasKuliah("T9", "x", date(2026, 11, 20), 3, MataKuliah("ZZ", "Z", 2), 50),
            TugasKelompok("T9", "x", date(2026, 11, 20), 3, 1),
        ]
        for tugas in salah:
            with self.assertRaises(ValueError, msg=tugas.judul):
                s.tambah_tugas(tugas)
        self.assertEqual(len(s.daftar_tugas), 4)
        with self.assertRaises(ValueError):
            s.tambah_tugas("bukan tugas")

    def test_urut_prioritas_dan_tie_break(self):
        self.isi_data()
        urutan = [t.kode for t in self.service.daftar_urut_prioritas(HARI_INI)]
        # T1=75, T4=70 (deadline lebih dekat), T2=70, T3=42
        self.assertEqual(urutan, ["T1", "T4", "T2", "T3"])

    def test_tugas_selesai_tidak_ikut_daftar(self):
        self.isi_data()
        self.service.tandai_selesai("T1")
        urutan = [t.kode for t in self.service.daftar_urut_prioritas(HARI_INI)]
        self.assertNotIn("T1", urutan)

    def test_tandai_selesai_error(self):
        self.isi_data()
        self.service.tandai_selesai("T1")
        with self.assertRaises(ValueError):
            self.service.tandai_selesai("T1")
        with self.assertRaises(ValueError):
            self.service.tandai_selesai("XXX")

    def test_minggu_kritis_mengabaikan_tugas_lewat(self):
        self.isi_data()
        hasil = self.service.cek_minggu_kritis(HARI_INI)
        self.assertEqual(len(hasil), 1)
        kode = sorted(t.kode for t in hasil[0]["tugas"])
        self.assertEqual(kode, ["T1", "T2", "T3"])  # T4 sudah lewat, tidak dihitung
        self.assertEqual(hasil[0]["total_jam"], 25)

    def test_buat_saran(self):
        self.isi_data()
        saran = self.service.buat_saran(HARI_INI)
        self.assertEqual([s[0].kode for s in saran], ["T1", "T4", "T2", "T3"])
        tugas, mulai, hari, lewat = saran[2]  # T2: 15 jam, 2 jam per hari
        self.assertEqual((tugas.kode, hari, mulai, lewat),
                         ("T2", 8, date(2026, 11, 12), True))


if __name__ == "__main__":
    unittest.main()