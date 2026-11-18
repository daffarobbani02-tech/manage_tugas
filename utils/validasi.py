from datetime import datetime


def valid_teks(teks):
    """Teks harus string dan tidak kosong."""
    return isinstance(teks, str) and teks.strip() != ""


def valid_estimasi(jam):
    """Estimasi pengerjaan: bilangan bulat positif (jam)."""
    return isinstance(jam, int) and not isinstance(jam, bool) and jam > 0


def valid_bobot(bobot):
    """Bobot nilai tugas kuliah: bilangan bulat 1 sampai 100 (persen)."""
    return isinstance(bobot, int) and not isinstance(bobot, bool) and 1 <= bobot <= 100


def valid_anggota(jumlah):
    """Tugas kelompok minimal 2 anggota."""
    return isinstance(jumlah, int) and not isinstance(jumlah, bool) and jumlah >= 2


def parse_tanggal(teks):
    """Ubah teks DD-MM-YYYY menjadi objek date. ValueError jika tidak valid."""
    try:
        return datetime.strptime(teks.strip(), "%d-%m-%Y").date()
    except (ValueError, AttributeError):
        raise ValueError("Format tanggal harus DD-MM-YYYY, contoh 20-11-2026.")