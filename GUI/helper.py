from models import TugasKuliah, TugasKelompok

WARNA_LABEL = {
    "TERLAMBAT": "#c0392b",  
    "MENDESAK": "#d68910",   
    "AMAN":"#2e8b57",       
}
WARNA_SUKSES = "#2e8b57"


def label_status(tugas, hari_ini):
    sisa = tugas.sisa_hari(hari_ini)
    if sisa < 0:
        return "TERLAMBAT"
    if sisa <= 3:
        return "MENDESAK"
    return "AMAN"


def teks_sisa(tugas, hari_ini):
    sisa = tugas.sisa_hari(hari_ini)
    if sisa < 0:
        return f"lewat {-sisa} hari"
    if sisa == 0:
        return "hari ini"
    return f"{sisa} hari lagi"


def format_tanggal(tanggal):
    return tanggal.strftime("%d-%m-%Y")


def jenis(tugas):
    return type(tugas).__name__.replace("Tugas", "")


def keterangan(tugas):
    if isinstance(tugas, TugasKuliah):
        return f"{tugas.matkul.nama}, bobot {tugas.bobot}%"
    if isinstance(tugas, TugasKelompok):
        return f"{tugas.jumlah_anggota} anggota"
    return ""


def baca_angka(teks, nama_field):
    try:
        return int(teks.strip())
    except ValueError:
        raise ValueError(f"{nama_field} harus berupa angka bulat.")