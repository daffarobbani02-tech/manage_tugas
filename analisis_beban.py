import math
from datetime import timedelta


class AnalisisBeban:
    """Menganalisis beban kerja: minggu kritis dan saran waktu mulai."""

    MIN_TUGAS_KRITIS = 3  # 3 tugas atau lebih dalam satu minggu = kritis

    def __init__(self, jam_per_hari=2, ambang_jam=20):
        if jam_per_hari <= 0 or ambang_jam <= 0:
            raise ValueError("jam_per_hari dan ambang_jam harus positif.")
        self.jam_per_hari = jam_per_hari  # kemampuan mengerjakan per hari
        self.ambang_jam = ambang_jam      # total jam per minggu yang dianggap berat

    def minggu_kritis(self, daftar_tugas):
        """Kelompokkan tugas belum selesai per minggu (Senin-Minggu) dari deadline.

        Minggu kritis jika total jam melebihi ambang_jam, atau tugasnya
        berjumlah MIN_TUGAS_KRITIS atau lebih. Hasil: list of dict, urut tanggal.
        """
        per_minggu = {}
        for tugas in daftar_tugas:
            if tugas.selesai:
                continue
            senin = tugas.deadline - timedelta(days=tugas.deadline.weekday())
            per_minggu.setdefault(senin, []).append(tugas)

        hasil = []
        for senin in sorted(per_minggu):
            kelompok = per_minggu[senin]
            total_jam = sum(t.estimasi_jam for t in kelompok)
            if total_jam > self.ambang_jam or len(kelompok) >= self.MIN_TUGAS_KRITIS:
                hasil.append({
                    "mulai": senin,
                    "selesai": senin + timedelta(days=6),
                    "jumlah": len(kelompok),
                    "total_jam": total_jam,
                    "tugas": kelompok,
                })
        return hasil

    def saran_mulai(self, tugas, hari_ini):
        """Kapan paling lambat mulai mengerjakan supaya cukup dicicil.

        Hasil: (tanggal_mulai, hari_dibutuhkan, sudah_lewat).
        """
        hari_dibutuhkan = math.ceil(tugas.estimasi_jam / self.jam_per_hari)
        tanggal_mulai = tugas.deadline - timedelta(days=hari_dibutuhkan)
        return tanggal_mulai, hari_dibutuhkan, tanggal_mulai < hari_ini