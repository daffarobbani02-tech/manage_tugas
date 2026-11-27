import os
from tkinter import messagebox

import customtkinter

from services.penyimpanan import (simpan_json, muat_json, simpan_csv,
                                  muat_csv, simpan_txt, muat_txt)
from .helper import WARNA_SUKSES

NAMA_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

FORMAT = {
    "JSON": (simpan_json, muat_json, "data.json"),
    "CSV": (simpan_csv, muat_csv, "data_matkul.csv dan data_tugas.csv"),
    "TXT": (simpan_txt, muat_txt, "data_matkul.txt dan data_tugas.txt"),
}


class PanelData(customtkinter.CTkFrame):

    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)

        frame = customtkinter.CTkFrame(self)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame.grid_columnconfigure((0, 1), weight=1, uniform="tombol")

        customtkinter.CTkLabel(
            frame, text="Simpan dan muat data", anchor="w",
            font=customtkinter.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, columnspan=2, padx=15, pady=(12, 4), sticky="ew")

        customtkinter.CTkLabel(frame, text="Format file", anchor="w").grid(
            row=1, column=0, columnspan=2, padx=15, sticky="ew")
        self.menu_format = customtkinter.CTkOptionMenu(
            frame, values=list(FORMAT), command=self.tampilkan_info)
        self.menu_format.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 6), sticky="ew")

        self.info = customtkinter.CTkLabel(frame, text="", anchor="w")
        self.info.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 8), sticky="ew")

        customtkinter.CTkButton(frame, text="Simpan data", command=self.simpan).grid(
            row=4, column=0, padx=(15, 5), pady=4, sticky="ew")
        customtkinter.CTkButton(frame, text="Muat data", command=self.muat).grid(
            row=4, column=1, padx=(5, 15), pady=4, sticky="ew")

        self.status = customtkinter.CTkLabel(frame, text="", anchor="w")
        self.status.grid(row=5, column=0, columnspan=2, padx=15, pady=(4, 12), sticky="ew")

        tampilan = customtkinter.CTkFrame(self)
        tampilan.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        tampilan.grid_columnconfigure(0, weight=1)
        customtkinter.CTkLabel(tampilan, text="Tampilan", anchor="w",
                               font=customtkinter.CTkFont(size=15, weight="bold")).grid(
            row=0, column=0, padx=15, pady=(12, 4), sticky="ew")
        self.menu_mode = customtkinter.CTkOptionMenu(
            tampilan, values=["system", "light", "dark"],
            command=customtkinter.set_appearance_mode)
        self.menu_mode.grid(row=1, column=0, padx=15, pady=(0, 12), sticky="ew")

        self.tampilkan_info()

    def tampilkan_info(self, *args):
        self.info.configure(text=f"File: {FORMAT[self.menu_format.get()][2]}")

    def simpan(self):
        simpan_fungsi, _, nama_file = FORMAT[self.menu_format.get()]
        try:
            simpan_fungsi(self.app.service, NAMA_DATA)
        except (ValueError, OSError) as e:
            messagebox.showerror("Gagal menyimpan", str(e))
            return
        self.status.configure(text=f"Data disimpan ke {nama_file}.",
                              text_color=WARNA_SUKSES)

    def muat(self):
        _, muat_fungsi, nama_file = FORMAT[self.menu_format.get()]
        if not messagebox.askyesno(
                "Muat data",
                "Data yang sedang tampil akan diganti dengan isi file. Lanjutkan?"):
            return

        service = self.app.service
        cadangan_matkul = dict(service.daftar_matkul)
        cadangan_tugas = dict(service.daftar_tugas)
        try:
            muat_fungsi(service, NAMA_DATA)
        except (ValueError, OSError, KeyError, TypeError) as e:
            service.daftar_matkul.clear()
            service.daftar_matkul.update(cadangan_matkul)
            service.daftar_tugas.clear()
            service.daftar_tugas.update(cadangan_tugas)
            if isinstance(e, (KeyError, TypeError)):
                e = "Isi file tidak sesuai format aplikasi."
            messagebox.showerror("Gagal memuat", str(e))
            return
        self.status.configure(text=f"Data dimuat dari {nama_file}.",
                              text_color=WARNA_SUKSES)
        self.app.segarkan_semua()

    def segarkan(self):
        pass  