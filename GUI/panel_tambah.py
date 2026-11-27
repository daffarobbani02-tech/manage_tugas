from tkinter import messagebox

import customtkinter

from models import TugasKuliah, TugasKelompok, TugasPribadi
from utils.validasi import parse_tanggal
from .helper import baca_angka, WARNA_SUKSES

TEKS_BELUM_ADA = "(belum ada mata kuliah)"


class PanelTambah(customtkinter.CTkFrame):

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.matkul_map = {}  
        self.grid_columnconfigure((0, 1), weight=1, uniform="kolom")
        self.grid_rowconfigure(0, weight=1)

        self.buat_form_tugas()
        self.buat_form_matkul()
        self.ganti_jenis("Kuliah")

    def buat_form_tugas(self):
        frame = customtkinter.CTkFrame(self)
        frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        judul_form = customtkinter.CTkLabel(
            frame, text="Tambah tugas", anchor="w",
            font=customtkinter.CTkFont(size=15, weight="bold"))
        judul_form.grid(row=0, column=0, padx=15, pady=(12, 4), sticky="ew")

        customtkinter.CTkLabel(frame, text="Jenis tugas", anchor="w").grid(
            row=1, column=0, padx=15, sticky="ew")
        self.menu_jenis = customtkinter.CTkOptionMenu(
            frame, values=["Kuliah", "Kelompok", "Pribadi"],
            command=self.ganti_jenis)
        self.menu_jenis.grid(row=2, column=0, padx=15, pady=(0, 6), sticky="ew")

        customtkinter.CTkLabel(frame, text="Judul", anchor="w").grid(
            row=3, column=0, padx=15, sticky="ew")
        self.entry_judul = customtkinter.CTkEntry(frame)
        self.entry_judul.grid(row=4, column=0, padx=15, pady=(0, 6), sticky="ew")

        customtkinter.CTkLabel(frame, text="Deadline (DD-MM-YYYY)", anchor="w").grid(
            row=5, column=0, padx=15, sticky="ew")
        self.entry_deadline = customtkinter.CTkEntry(
            frame, placeholder_text="contoh: 25-12-2026")
        self.entry_deadline.grid(row=6, column=0, padx=15, pady=(0, 6), sticky="ew")

        customtkinter.CTkLabel(frame, text="Estimasi pengerjaan (jam)", anchor="w").grid(
            row=7, column=0, padx=15, sticky="ew")
        self.entry_estimasi = customtkinter.CTkEntry(frame, placeholder_text="contoh: 6")
        self.entry_estimasi.grid(row=8, column=0, padx=15, pady=(0, 6), sticky="ew")

        self.frame_kuliah = customtkinter.CTkFrame(frame, fg_color="transparent")
        self.frame_kuliah.grid_columnconfigure(0, weight=1)
        customtkinter.CTkLabel(self.frame_kuliah, text="Mata kuliah", anchor="w").grid(
            row=0, column=0, sticky="ew")
        self.menu_matkul = customtkinter.CTkOptionMenu(
            self.frame_kuliah, values=[TEKS_BELUM_ADA])
        self.menu_matkul.grid(row=1, column=0, pady=(0, 6), sticky="ew")
        customtkinter.CTkLabel(self.frame_kuliah, text="Bobot nilai (%)", anchor="w").grid(
            row=2, column=0, sticky="ew")
        self.entry_bobot = customtkinter.CTkEntry(
            self.frame_kuliah, placeholder_text="contoh: 20")
        self.entry_bobot.grid(row=3, column=0, sticky="ew")

        self.frame_kelompok = customtkinter.CTkFrame(frame, fg_color="transparent")
        self.frame_kelompok.grid_columnconfigure(0, weight=1)
        customtkinter.CTkLabel(self.frame_kelompok, text="Jumlah anggota", anchor="w").grid(
            row=0, column=0, sticky="ew")
        self.entry_anggota = customtkinter.CTkEntry(
            self.frame_kelompok, placeholder_text="contoh: 3")
        self.entry_anggota.grid(row=1, column=0, sticky="ew")

        self.tombol_tugas = customtkinter.CTkButton(
            frame, text="Simpan tugas", command=self.simpan_tugas)
        self.tombol_tugas.grid(row=10, column=0, padx=15, pady=(12, 4), sticky="ew")
        self.status_tugas = customtkinter.CTkLabel(frame, text="", anchor="w")
        self.status_tugas.grid(row=11, column=0, padx=15, pady=(0, 10), sticky="ew")

    def buat_form_matkul(self):
        frame = customtkinter.CTkFrame(self)
        frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        judul_form = customtkinter.CTkLabel(
            frame, text="Tambah mata kuliah", anchor="w",
            font=customtkinter.CTkFont(size=15, weight="bold"))
        judul_form.grid(row=0, column=0, padx=15, pady=(12, 4), sticky="ew")

        customtkinter.CTkLabel(frame, text="Kode mata kuliah", anchor="w").grid(
            row=1, column=0, padx=15, sticky="ew")
        self.entry_kode_mk = customtkinter.CTkEntry(frame, placeholder_text="contoh: IF204")
        self.entry_kode_mk.grid(row=2, column=0, padx=15, pady=(0, 6), sticky="ew")

        customtkinter.CTkLabel(frame, text="Nama mata kuliah", anchor="w").grid(
            row=3, column=0, padx=15, sticky="ew")
        self.entry_nama_mk = customtkinter.CTkEntry(frame)
        self.entry_nama_mk.grid(row=4, column=0, padx=15, pady=(0, 6), sticky="ew")

        customtkinter.CTkLabel(frame, text="SKS (1 sampai 6)", anchor="w").grid(
            row=5, column=0, padx=15, sticky="ew")
        self.entry_sks = customtkinter.CTkEntry(frame, placeholder_text="contoh: 3")
        self.entry_sks.grid(row=6, column=0, padx=15, pady=(0, 6), sticky="ew")

        self.tombol_matkul = customtkinter.CTkButton(
            frame, text="Simpan mata kuliah", command=self.simpan_matkul)
        self.tombol_matkul.grid(row=7, column=0, padx=15, pady=(12, 4), sticky="ew")
        self.status_matkul = customtkinter.CTkLabel(frame, text="", anchor="w")
        self.status_matkul.grid(row=8, column=0, padx=15, pady=(0, 10), sticky="ew")

    def ganti_jenis(self, pilihan):
        """Tampilkan isian tambahan sesuai jenis tugas yang dipilih."""
        self.frame_kuliah.grid_forget()
        self.frame_kelompok.grid_forget()
        if pilihan == "Kuliah":
            self.frame_kuliah.grid(row=9, column=0, padx=15, sticky="ew")
        elif pilihan == "Kelompok":
            self.frame_kelompok.grid(row=9, column=0, padx=15, sticky="ew")

    def buat_kode(self):
        """Kode otomatis TGS001, TGS002, ... dan dipastikan belum dipakai."""
        daftar = self.app.service.daftar_tugas
        nomor = len(daftar) + 1
        while f"TGS{nomor:03d}" in daftar:
            nomor += 1
        return f"TGS{nomor:03d}"

    def simpan_tugas(self):
        service = self.app.service
        try:
            judul = self.entry_judul.get().strip()
            deadline = parse_tanggal(self.entry_deadline.get())
            estimasi = baca_angka(self.entry_estimasi.get(), "Estimasi")
            kode = self.buat_kode()
            pilihan = self.menu_jenis.get()

            if pilihan == "Kuliah":
                kode_mk = self.matkul_map.get(self.menu_matkul.get())
                if kode_mk is None:
                    raise ValueError("Pilih mata kuliah dulu. Tambahkan di panel "
                                     "sebelah kanan jika belum ada.")
                bobot = baca_angka(self.entry_bobot.get(), "Bobot")
                tugas = TugasKuliah(kode, judul, deadline, estimasi,
                                    service.daftar_matkul[kode_mk], bobot)
            elif pilihan == "Kelompok":
                anggota = baca_angka(self.entry_anggota.get(), "Jumlah anggota")
                tugas = TugasKelompok(kode, judul, deadline, estimasi, anggota)
            else:
                tugas = TugasPribadi(kode, judul, deadline, estimasi)

            service.tambah_tugas(tugas)
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))
            return

        for entry in (self.entry_judul, self.entry_deadline, self.entry_estimasi,
                      self.entry_bobot, self.entry_anggota):
            entry.delete(0, "end")
        self.status_tugas.configure(text=f"Tugas {kode} ditambahkan.",
                                    text_color=WARNA_SUKSES)
        self.app.segarkan_semua()

    def simpan_matkul(self):
        try:
            kode = self.entry_kode_mk.get().strip().upper()
            nama = self.entry_nama_mk.get().strip()
            sks = baca_angka(self.entry_sks.get(), "SKS")
            self.app.service.tambah_matkul(kode, nama, sks)
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))
            return

        for entry in (self.entry_kode_mk, self.entry_nama_mk, self.entry_sks):
            entry.delete(0, "end")
        self.status_matkul.configure(text=f"Mata kuliah {kode} ditambahkan.",
                                     text_color=WARNA_SUKSES)
        self.app.segarkan_semua()

    def segarkan(self):
        """Perbarui pilihan mata kuliah (data bisa berubah karena muat data)."""
        sebelumnya = self.menu_matkul.get()
        self.matkul_map = {f"{m.kode} - {m.nama}": m.kode
                           for m in self.app.service.daftar_matkul.values()}
        pilihan = list(self.matkul_map) or [TEKS_BELUM_ADA]
        self.menu_matkul.configure(values=pilihan)
        self.menu_matkul.set(sebelumnya if sebelumnya in pilihan else pilihan[0])