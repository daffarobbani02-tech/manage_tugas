import unittest
from datetime import date

from models import TugasPribadi
from services import AnalisisBeban

HARI_INI = date(2026, 11, 18)  # Rabu; minggu ini Senin 16 s.d. Minggu 22 Nov


def tugas(kode, tanggal, jam):
    return TugasPribadi(kode, kode, tanggal, jam)


class TestAnalisisBeban(unittest.TestCase):
    def setUp(self):
        self.analisis = AnalisisBeban(jam_per_hari=2, ambang_jam=20)

    def test_kritis_karena_jumlah_tugas(self):
        daftar = [tugas(f"T{i}", date(2026, 11, 20), 1) for i in range(3)]
        hasil = self.analisis.minggu_kritis(daftar)
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["jumlah"], 3)
        self.assertEqual(hasil[0]["mulai"], date(2026, 11, 16))
        self.assertEqual(hasil[0]["selesai"], date(2026, 11, 22))

    def test_kritis_karena_total_jam(self):
        daftar = [tugas("T1", date(2026, 11, 20), 12), tugas("T2", date(2026, 11, 21), 12)]
        hasil = self.analisis.minggu_kritis(daftar)
        self.assertEqual(hasil[0]["total_jam"], 24)

    def test_tidak_kritis(self):
        daftar = [tugas("T1", date(2026, 11, 20), 5), tugas("T2", date(2026, 11, 21), 5)]
        self.assertEqual(self.analisis.minggu_kritis(daftar), [])

    def test_tepat_di_ambang_belum_kritis(self):
        daftar = [tugas("T1", date(2026, 11, 20), 10), tugas("T2", date(2026, 11, 21), 10)]
        self.assertEqual(self.analisis.minggu_kritis(daftar), [])

    def test_tugas_selesai_diabaikan(self):
        daftar = [tugas(f"T{i}", date(2026, 11, 20), 1) for i in range(3)]
        daftar[0].tandai_selesai()
        self.assertEqual(self.analisis.minggu_kritis(daftar), [])

    def test_minggu_berbeda_dipisah(self):
        # Minggu 22 Nov dan Senin 23 Nov berada di minggu yang berbeda
        daftar = [tugas("T1", date(2026, 11, 22), 12), tugas("T2", date(2026, 11, 23), 12)]
        self.assertEqual(self.analisis.minggu_kritis(daftar), [])

    def test_saran_mulai_sudah_lewat(self):
        mulai, hari, lewat = self.analisis.saran_mulai(tugas("T1", date(2026, 11, 20), 15), HARI_INI)
        self.assertEqual(hari, 8)
        self.assertEqual(mulai, date(2026, 11, 12))
        self.assertTrue(lewat)

    def test_saran_mulai_masih_sempat(self):
        mulai, hari, lewat = self.analisis.saran_mulai(tugas("T1", date(2026, 11, 30), 4), HARI_INI)
        self.assertEqual(hari, 2)
        self.assertEqual(mulai, date(2026, 11, 28))
        self.assertFalse(lewat)

    def test_pembulatan_ke_atas(self):
        _, hari, _ = self.analisis.saran_mulai(tugas("T1", date(2026, 11, 30), 5), HARI_INI)
        self.assertEqual(hari, 3)

    def test_parameter_tidak_valid(self):
        with self.assertRaises(ValueError):
            AnalisisBeban(jam_per_hari=0)
        with self.assertRaises(ValueError):
            AnalisisBeban(ambang_jam=-5)


if __name__ == "__main__":
    unittest.main()