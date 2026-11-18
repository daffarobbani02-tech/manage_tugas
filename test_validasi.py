import unittest
from datetime import date

from utils.validasi import (valid_teks, valid_estimasi, valid_bobot,
                            valid_anggota, parse_tanggal)


class TestValidasi(unittest.TestCase):
    def test_valid_teks(self):
        self.assertTrue(valid_teks("abc"))
        for salah in ["", "   ", None, 123]:
            self.assertFalse(valid_teks(salah))

    def test_valid_estimasi(self):
        self.assertTrue(valid_estimasi(1))
        for salah in [0, -1, 2.5, "3", True]:
            self.assertFalse(valid_estimasi(salah))

    def test_valid_bobot(self):
        self.assertTrue(valid_bobot(1))
        self.assertTrue(valid_bobot(100))
        for salah in [0, 101, 12.5, "20"]:
            self.assertFalse(valid_bobot(salah))

    def test_valid_anggota(self):
        self.assertTrue(valid_anggota(2))
        for salah in [1, 0, "3"]:
            self.assertFalse(valid_anggota(salah))

    def test_parse_tanggal_valid(self):
        self.assertEqual(parse_tanggal("20-11-2026"), date(2026, 11, 20))
        self.assertEqual(parse_tanggal(" 01-01-2027 "), date(2027, 1, 1))

    def test_parse_tanggal_salah(self):
        for salah in ["2026-11-20", "31-02-2026", "abc", "", None]:
            with self.assertRaises(ValueError):
                parse_tanggal(salah)


if __name__ == "__main__":
    unittest.main()