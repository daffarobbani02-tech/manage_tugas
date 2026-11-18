import unittest
from datetime import date, timedelta

from models import (MataKuliah, Tugas, TugasKuliah, TugasKelompok,
                    TugasPribadi)

HARI_INI = date(2026, 11, 18)


def deadline(n):
    return HARI_INI + timedelta(days=n)


class TestTugas(unittest.TestCase):
    def setUp(self):
        self.matkul = MataKuliah("IF201", "PBO", 3)

    def test_tugas_abstract_tidak_bisa_dibuat(self):
        with self.assertRaises(TypeError):
            Tugas("T1", "x", deadline(1), 1)

    def test_sisa_hari(self):
        self.assertEqual(TugasPribadi("T1", "x", deadline(5), 1).sisa_hari(HARI_INI), 5)
        self.assertEqual(TugasPribadi("T1", "x", deadline(-2), 1).sisa_hari(HARI_INI), -2)

    def test_skor_urgensi_batas(self):
        harapan = {-1: 100, 0: 80, 1: 80, 2: 60, 3: 60, 4: 40, 7: 40, 8: 20, 30: 20}
        for sisa, skor in harapan.items():
            tugas = TugasPribadi("T1", "x", deadline(sisa), 1)
            self.assertEqual(tugas.skor_urgensi(HARI_INI), skor, f"sisa {sisa} hari")

    def test_prioritas_kuliah(self):
        tugas = TugasKuliah("T1", "x", deadline(2), 5, self.matkul, 30)
        self.assertAlmostEqual(tugas.hitung_prioritas(HARI_INI), 75)

    def test_prioritas_kelompok(self):
        tugas = TugasKelompok("T2", "x", deadline(2), 5, 3)
        self.assertAlmostEqual(tugas.hitung_prioritas(HARI_INI), 70)

    def test_prioritas_pribadi(self):
        tugas = TugasPribadi("T3", "x", deadline(2), 5)
        self.assertAlmostEqual(tugas.hitung_prioritas(HARI_INI), 42)

    def test_tandai_selesai(self):
        tugas = TugasPribadi("T1", "x", deadline(2), 5)
        self.assertFalse(tugas.selesai)
        tugas.tandai_selesai()
        self.assertTrue(tugas.selesai)
        with self.assertRaises(ValueError):
            tugas.tandai_selesai()


if __name__ == "__main__":
    unittest.main()