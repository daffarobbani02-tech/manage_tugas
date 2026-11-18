from datetime import date, timedelta

from models import TugasKuliah, TugasKelompok, TugasPribadi
from services import PengaturBeban
from utils.validasi import parse_tanggal


def baca_angka(prompt):
    teks = input(prompt).strip()
    try:
        return int(teks)
    except ValueError:
        raise ValueError(f"'{teks}' bukan angka bulat.")


def buat_kode(service):
    """Kode tugas otomatis: TGS001, TGS002, ..."""
    return f"TGS{len(service.daftar_tugas) + 1:03d}"


def label(tugas, hari_ini):
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


def siapkan_data(service, hari_ini):
    """Data contoh (tanggal relatif terhadap hari ini) supaya demo langsung terisi."""
    pbo = service.tambah_matkul("IF201", "Pemrograman Berbasis Objek", 3)
    basdat = service.tambah_matkul("IF202", "Basis Data", 3)
    etika = service.tambah_matkul("IF203", "Etika Kecerdasan Artifisial", 2)

    def hari(n):
        return hari_ini + timedelta(days=n)

    service.tambah_tugas(TugasKuliah("TGS001", "Laporan praktikum OOP", hari(2), 6, pbo, 20))
    service.tambah_tugas(TugasKelompok("TGS002", "Proyek UAS Basis Data", hari(3), 15, 3))
    service.tambah_tugas(TugasKuliah("TGS003", "Makalah etika AI", hari(3), 5, etika, 10))
    service.tambah_tugas(TugasPribadi("TGS004", "Belajar kalkulus", hari(9), 4))
    service.tambah_tugas(TugasKuliah("TGS005", "Kuis basis data", hari(10), 3, basdat, 15))
    service.tambah_tugas(TugasPribadi("TGS006", "Rapikan catatan", hari(-1), 2))


# ---------- menu ----------
def menu_tambah(service, hari_ini):
    print("\n1. Tugas kuliah\n2. Tugas kelompok\n3. Tugas pribadi\n4. Mata kuliah baru")
    pilihan = input("Pilih: ").strip()

    if pilihan == "4":
        kode = input("Kode mata kuliah: ").strip().upper()
        nama = input("Nama mata kuliah: ").strip()
        sks = baca_angka("SKS: ")
        service.tambah_matkul(kode, nama, sks)
        print("Mata kuliah ditambahkan.")
        return
    if pilihan not in ("1", "2", "3"):
        print("Pilihan tidak dikenal.")
        return

    judul = input("Judul tugas: ").strip()
    deadline = parse_tanggal(input("Deadline (DD-MM-YYYY): "))
    estimasi = baca_angka("Estimasi pengerjaan (jam): ")
    kode = buat_kode(service)

    if pilihan == "1":
        if not service.daftar_matkul:
            raise ValueError("Belum ada mata kuliah. Tambahkan dulu (pilihan 4).")
        for matkul in service.daftar_matkul.values():
            print("  ", matkul)
        kode_mk = input("Kode mata kuliah: ").strip().upper()
        matkul = service.daftar_matkul.get(kode_mk)
        if matkul is None:
            raise ValueError(f"Mata kuliah {kode_mk} tidak ditemukan.")
        bobot = baca_angka("Bobot nilai (%): ")
        tugas = TugasKuliah(kode, judul, deadline, estimasi, matkul, bobot)
    elif pilihan == "2":
        anggota = baca_angka("Jumlah anggota: ")
        tugas = TugasKelompok(kode, judul, deadline, estimasi, anggota)
    else:
        tugas = TugasPribadi(kode, judul, deadline, estimasi)

    service.tambah_tugas(tugas)
    print(f"Tugas ditambahkan dengan kode {kode}.")


def menu_daftar(service, hari_ini):
    daftar = service.daftar_urut_prioritas(hari_ini)
    if not daftar:
        print("Tidak ada tugas yang belum selesai.")
        return
    print("\nTugas urut prioritas (tertinggi dulu):")
    for no, tugas in enumerate(daftar, start=1):
        print(f"{no}. [{label(tugas, hari_ini):<9}] {tugas.kode} {tugas.judul} "
              f"| {jenis(tugas)} | {format_tanggal(tugas.deadline)} "
              f"({teks_sisa(tugas, hari_ini)}) | skor {tugas.hitung_prioritas(hari_ini):.0f}")


def menu_selesai(service, hari_ini):
    menu_daftar(service, hari_ini)
    kode = input("Kode tugas yang selesai: ").strip().upper()
    tugas = service.tandai_selesai(kode)
    print(f"'{tugas.judul}' ditandai selesai.")


def menu_minggu_kritis(service, hari_ini):
    hasil = service.cek_minggu_kritis(hari_ini)
    if not hasil:
        print("Tidak ada minggu kritis. Beban kerja aman.")
        return
    for minggu in hasil:
        print(f"\nMinggu {format_tanggal(minggu['mulai'])} s.d. "
              f"{format_tanggal(minggu['selesai'])}: {minggu['jumlah']} tugas, "
              f"{minggu['total_jam']} jam -> KRITIS")
        for tugas in minggu["tugas"]:
            print(f"   - {tugas.judul} ({tugas.estimasi_jam} jam, "
                  f"deadline {format_tanggal(tugas.deadline)})")


def menu_saran(service, hari_ini):
    saran = service.buat_saran(hari_ini)
    if not saran:
        print("Tidak ada tugas yang belum selesai.")
        return
    print("\nSaran waktu mulai (urut prioritas):")
    for tugas, mulai, hari, lewat in saran:
        catatan = "SUDAH LEWAT, mulai sekarang" if lewat else "masih sempat"
        print(f"- {tugas.judul}: butuh {hari} hari, mulai paling lambat "
              f"{format_tanggal(mulai)} ({catatan})")


MENU = {
    "1": menu_tambah,
    "2": menu_daftar,
    "3": menu_selesai,
    "4": menu_minggu_kritis,
    "5": menu_saran,
}


def main():
    hari_ini = date.today()
    service = PengaturBeban()
    siapkan_data(service, hari_ini)

    while True:
        print(f"\n=== PENGATUR BEBAN SEMESTER ({format_tanggal(hari_ini)}) ===")
        print("1. Tambah tugas / mata kuliah")
        print("2. Lihat tugas urut prioritas")
        print("3. Tandai tugas selesai")
        print("4. Cek minggu kritis")
        print("5. Saran waktu mulai mengerjakan")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "0":
            print("Semangat mengerjakan tugasnya!")
            break
        aksi = MENU.get(pilihan)
        if aksi is None:
            print("Menu tidak dikenal.")
            continue
        try:
            aksi(service, hari_ini)
        except ValueError as e:
            print(f"Gagal: {e}")


if __name__ == "__main__":
    main()