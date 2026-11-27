from tkinter import messagebox

import customtkinter

from .helper import (WARNA_LABEL, label_status, teks_sisa, format_tanggal,
                     jenis, keterangan)


class PanelDaftar(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.ringkasan = customtkinter.CTkLabel(
            self, text="", anchor="w",
            font=customtkinter.CTkFont(size=14, weight="bold"))
        self.ringkasan.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")

        self.list_frame = customtkinter.CTkScrollableFrame(
            self, label_text="Tugas urut prioritas (tertinggi dulu)")
        self.list_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.list_frame.grid_columnconfigure(1, weight=1)

    def segarkan(self):
        hari_ini = self.app.hari_ini()
        daftar = self.app.service.daftar_urut_prioritas(hari_ini)

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not daftar:
            kosong = customtkinter.CTkLabel(
                self.list_frame, text="Tidak ada tugas yang belum selesai.")
            kosong.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

        jumlah = {"TERLAMBAT": 0, "MENDESAK": 0, "AMAN": 0}
        for baris, tugas in enumerate(daftar):
            status = label_status(tugas, hari_ini)
            jumlah[status] += 1

            badge = customtkinter.CTkLabel(
                self.list_frame, text=status, width=90, corner_radius=6,
                fg_color=WARNA_LABEL[status], text_color="white",
                font=customtkinter.CTkFont(size=12, weight="bold"))
            badge.grid(row=baris, column=0, padx=(5, 10), pady=4)

            detail = " | ".join(bagian for bagian in (
                tugas.kode,
                jenis(tugas),
                f"{format_tanggal(tugas.deadline)} ({teks_sisa(tugas, hari_ini)})",
                f"{tugas.estimasi_jam} jam",
                keterangan(tugas),
            ) if bagian)
            info = customtkinter.CTkLabel(
                self.list_frame, text=f"{tugas.judul}\n{detail}",
                anchor="w", justify="left", wraplength=520)
            info.grid(row=baris, column=1, padx=5, pady=4, sticky="ew")

            skor = customtkinter.CTkLabel(
                self.list_frame, text=f"skor {tugas.hitung_prioritas(hari_ini):.0f}")
            skor.grid(row=baris, column=2, padx=10, pady=4)

            tombol = customtkinter.CTkButton(
                self.list_frame, text="Selesai", width=80,
                command=lambda kode=tugas.kode: self.selesai(kode))
            tombol.grid(row=baris, column=3, padx=(0, 5), pady=4)

        self.ringkasan.configure(
            text=f"{len(daftar)} tugas belum selesai  |  "
                 f"{jumlah['TERLAMBAT']} terlambat  |  "
                 f"{jumlah['MENDESAK']} mendesak  |  {jumlah['AMAN']} aman")

    def selesai(self, kode):
        try:
            self.app.service.tandai_selesai(kode)
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))
        self.app.segarkan_semua()