from dataclasses import dataclass
import json
import math
import re

from models import Tugas, TugasKuliah, TugasKelompok
from .layanan_ai import LayananAI, LayananAIError


@dataclass
class HasilEstimasi:
    """Data class untuk membungkus hasil estimasi waktu dari AI."""
    estimasi_jam: int
    estimasi_hari: int
    alasan: str


class AsistenAI:
    """Mengelola 3 fitur AI: panduan tugas, estimasi waktu, dan saran cicilan."""

    def __init__(self, layanan: LayananAI):
        if not isinstance(layanan, LayananAI):
            raise ValueError("Objek layanan harus turunan dari LayananAI.")
        self._layanan = layanan

    # ---------- helper internal ----------
    def _deskripsi_tugas(self, tugas: Tugas) -> str:
        """Ubah objek Tugas menjadi teks ringkas sebagai konteks untuk AI."""
        info = [
            f"Judul: {tugas.judul}",
            f"Jenis: {type(tugas).__name__}",
            f"Deadline: {tugas.deadline.strftime('%d-%m-%Y')}",
            f"Estimasi saat ini: {tugas.estimasi_jam} jam",
        ]
        if isinstance(tugas, TugasKuliah):
            info.append(
                f"Mata Kuliah: {tugas.matkul.nama} ({tugas.matkul.sks} SKS, bobot {tugas.bobot}%)"
            )
        elif isinstance(tugas, TugasKelompok):
            info.append(f"Jumlah Anggota: {tugas.jumlah_anggota} orang")
        return " | ".join(info)

    def _ekstrak_json(self, teks: str) -> dict:
        """Ambil blok JSON dari jawaban AI meski dibungkus markdown ```json."""
        cocok = re.search(r"\{.*\}", teks.strip(), re.DOTALL)
        if not cocok:
            raise ValueError("Format JSON tidak ditemukan pada respons AI.")
        return json.loads(cocok.group(0))

    # ---------- Fitur 1: Memandu Tugas ----------
    def pandu_tugas(self, tugas: Tugas, pertanyaan: str = "") -> str:
        """Menjelaskan ulang materi/konsep tugas dan memberi langkah pengerjaan."""
        if not isinstance(tugas, Tugas):
            raise ValueError("Parameter harus berupa objek Tugas.")

        tambahan = f"\nPertanyaan spesifik mahasiswa: {pertanyaan}" if pertanyaan.strip() else ""
        prompt = (
            "Kamu adalah asisten belajar mahasiswa yang menjelaskan dengan bahasa Indonesia "
            "yang santai, jelas, dan mudah dipahami.\n\n"
            f"Data tugas:\n{self._deskripsi_tugas(tugas)}{tambahan}\n\n"
            "Berikan panduan singkat berisi:\n"
            "1. Penjelasan inti materi/konsep tugas ini dengan bahasa sederhana.\n"
            "2. Langkah konkret pengerjaan dari awal sampai selesai (3-5 langkah).\n"
            "3. Tips agar tidak terjebak kesalahan umum."
        )
        return self._layanan.kirim_prompt(prompt)

    # ---------- Fitur 2: Estimasi Selesainya Tugas ----------
    def estimasi_selesai(
        self,
        judul: str,
        jenis_tugas: str,
        detail: str = "",
        jam_per_hari: int = 2,
    ) -> HasilEstimasi:
        """Meminta AI mengestimasi total jam dan hari pengerjaan tugas."""
        if not judul or not judul.strip():
            raise ValueError("Judul tugas tidak boleh kosong.")
        if jam_per_hari <= 0:
            raise ValueError("jam_per_hari harus positif.")

        prompt = (
            "Kamu adalah asisten manajemen waktu mahasiswa. Estimasi waktu pengerjaan "
            "tugas berikut secara realistis untuk mahasiswa S1.\n"
            f"Judul tugas: {judul}\n"
            f"Jenis tugas: {jenis_tugas}\n"
            f"Detail tambahan: {detail if detail else '-'}\n"
            f"Kapasitas belajar mahasiswa: {jam_per_hari} jam per hari.\n\n"
            "Balas HANYA dengan JSON valid tanpa teks lain dengan format persis seperti ini:\n"
            '{"estimasi_jam": 4, "estimasi_hari": 2, "alasan": "Penjelasan singkat 1-2 kalimat"}'
        )

        try:
            teks = self._layanan.kirim_prompt(prompt)
            data = self._ekstrak_json(teks)
            jam = max(1, int(data["estimasi_jam"]))
            hari = max(1, int(data.get("estimasi_hari", math.ceil(jam / jam_per_hari))))
            alasan = str(data.get("alasan", "Estimasi berdasarkan kompleksitas tugas."))
            return HasilEstimasi(estimasi_jam=jam, estimasi_hari=hari, alasan=alasan)
        except (LayananAIError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            jam_default = 4
            return HasilEstimasi(
                estimasi_jam=jam_default,
                estimasi_hari=math.ceil(jam_default / jam_per_hari),
                alasan="Menggunakan estimasi cadangan karena AI sedang offline atau respons tidak valid.",
            )

    # ---------- Fitur 3: Saran Cicilan Saat Minggu Padat ----------
    def saran_cicil_minggu_padat(
        self,
        daftar_minggu_kritis: list,
        hari_ini,
        jam_per_hari: int = 2,
    ) -> str:
        """Membuat strategi penyicilan harian dari hasil PengaturBeban.cek_minggu_kritis()."""
        if not daftar_minggu_kritis:
            return "Tidak ada minggu kritis saat ini. Kamu bisa mengerjakan tugas sesuai urutan prioritas normal."

        bagian_minggu = []
        for idx, minggu in enumerate(daftar_minggu_kritis, start=1):
            mulai = minggu["mulai"].strftime("%d-%m-%Y")
            selesai = minggu["selesai"].strftime("%d-%m-%Y")
            tugas_terurut = sorted(
                minggu["tugas"],
                key=lambda t: (-t.hitung_prioritas(hari_ini), t.deadline, t.kode),
            )
            rincian_tugas = "\n".join(
                f"  - [{t.kode}] {t.judul} ({type(t).__name__}) | "
                f"Deadline: {t.deadline.strftime('%d-%m-%Y')} | "
                f"Estimasi: {t.estimasi_jam} jam | "
                f"Skor Prioritas: {t.hitung_prioritas(hari_ini):.0f}"
                for t in tugas_terurut
            )
            bagian_minggu.append(
                f"Minggu Kritis #{idx} ({mulai} s.d. {selesai}) - "
                f"{minggu['jumlah']} tugas, total {minggu['total_jam']} jam:\n{rincian_tugas}"
            )

        ringkasan = "\n\n".join(bagian_minggu)
        prompt = (
            "Kamu adalah mentor manajemen waktu mahasiswa.\n"
            f"Tanggal hari ini: {hari_ini.strftime('%d-%m-%Y')}.\n"
            f"Kapasitas kerja mahasiswa: {jam_per_hari} jam/hari.\n\n"
            f"Berikut daftar minggu padat beserta tugas yang sudah diurutkan dari skor prioritas tertinggi:\n"
            f"{ringkasan}\n\n"
            "Buatkan strategi penyicilan yang realistis dalam bahasa Indonesia:\n"
            "1. Tentukan tugas mana yang WAJIB dicicil duluan dan alasannya.\n"
            "2. Pecah menjadi jadwal cicilan per hari sesuai kapasitas jam/hari.\n"
            "3. Berikan saran singkat jika total jam melebihi kapasitas mingguan."
        )
        return self._layanan.kirim_prompt(prompt)