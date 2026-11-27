import customtkinter

from .helper import format_tanggal


class PanelAnalisis(customtkinter.CTkFrame):
    
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 3), weight=1)

        judul_font = customtkinter.CTkFont(size=14, weight="bold")
        customtkinter.CTkLabel(self, text="Minggu kritis", anchor="w",
                               font=judul_font).grid(
            row=0, column=0, padx=10, pady=(10, 2), sticky="ew")
        self.kotak_kritis = customtkinter.CTkTextbox(self, wrap="word", height=120)
        self.kotak_kritis.grid(row=1, column=0, padx=10, pady=(0, 6), sticky="nsew")

        customtkinter.CTkLabel(self, text="Saran waktu mulai mengerjakan", anchor="w",
                               font=judul_font).grid(
            row=2, column=0, padx=10, pady=(6, 2), sticky="ew")
        self.kotak_saran = customtkinter.CTkTextbox(self, wrap="word", height=160)
        self.kotak_saran.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")

    @staticmethod
    def isi(kotak, teks):
        kotak.configure(state="normal")
        kotak.delete("1.0", "end")
        kotak.insert("1.0", teks)
        kotak.configure(state="disabled")  

    def segarkan(self):
        hari_ini = self.app.hari_ini()
        service = self.app.service

        hasil = service.cek_minggu_kritis(hari_ini)
        if not hasil:
            teks = "Tidak ada minggu kritis. Beban kerja aman."
        else:
            bagian = []
            for minggu in hasil:
                baris = [f"Minggu {format_tanggal(minggu['mulai'])} s.d. "
                         f"{format_tanggal(minggu['selesai'])}: {minggu['jumlah']} tugas, "
                         f"{minggu['total_jam']} jam -> KRITIS"]
                for tugas in minggu["tugas"]:
                    baris.append(f"   - {tugas.judul} ({tugas.estimasi_jam} jam, "
                                 f"deadline {format_tanggal(tugas.deadline)})")
                bagian.append("\n".join(baris))
            teks = "\n\n".join(bagian)
        self.isi(self.kotak_kritis, teks)

        saran = service.buat_saran(hari_ini)
        if not saran:
            teks = "Tidak ada tugas yang blm selesai."
        else:
            baris = []
            for tugas, mulai, hari, lewat in saran:
                catatan = "Sudah Lewat, segera dikerjakan" if lewat else "masih sempat"
                baris.append(f"- {tugas.judul}: butuh {hari} hari, mulai paling lambat "
                             f"{format_tanggal(mulai)} ({catatan})")
            teks = "\n".join(baris)
        self.isi(self.kotak_saran, teks)