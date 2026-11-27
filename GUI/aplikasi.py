from datetime import date

import customtkinter

from main import siapkan_data 
from services import PengaturBeban
from .helper import format_tanggal
from .panel_analisis import PanelAnalisis
from .panel_daftar import PanelDaftar
from .panel_data import PanelData
from .panel_tambah import PanelTambah

customtkinter.set_appearance_mode("dark")     
customtkinter.set_default_color_theme("green")  


class AplikasiGUI(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.title("Sistem Manage Tugas")
        self.geometry("920x640")
        self.minsize(800, 560)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.service = PengaturBeban()
        siapkan_data(self.service, self.hari_ini())

        self.header = customtkinter.CTkLabel(
            self, text="", anchor="w",
            font=customtkinter.CTkFont(size=18, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")

        self.tabview = customtkinter.CTkTabview(self, command=self.segarkan_semua)
        self.tabview.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.daftar_panel = []
        for nama, kelas in (("Daftar Tugas", PanelDaftar),
                            ("Tambah", PanelTambah),
                            ("Analisis", PanelAnalisis),
                            ("Data", PanelData)):
            tab = self.tabview.add(nama)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
            panel = kelas(tab, self)
            panel.grid(row=0, column=0, sticky="nsew")
            self.daftar_panel.append(panel)

        self.segarkan_semua()

    def hari_ini(self):
        return date.today()

    def segarkan_semua(self):
        self.header.configure(
            text=f"Sistem Manage Tugas |   Hari ini: {format_tanggal(self.hari_ini())}")
        for panel in self.daftar_panel:
            panel.segarkan()