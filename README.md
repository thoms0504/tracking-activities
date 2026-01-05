# PNS Activity Tracker 🎯

Aplikasi berbasis web yang dibangun menggunakan **Streamlit** untuk memantau, mencatat, dan menganalisis kegiatan harian Pegawai Negeri Sipil (PNS). Aplikasi ini menyediakan antarmuka yang modern untuk manajemen tugas dan visualisasi produktivitas kerja.

## ✨ Fitur Utama

*   **Dashboard Interaktif**: Ringkasan statistik real-time (Total Kegiatan, Selesai, Dalam Proses, Tertunda).
*   **Manajemen Kegiatan (CRUD)**:
    *   Tambah kegiatan baru dengan detail lengkap (Tanggal, Kategori, Status, Deskripsi).
    *   Edit dan Hapus kegiatan yang sudah ada.
    *   **Bukti Kegiatan**: Dukungan upload foto atau ambil gambar langsung melalui kamera perangkat.
*   **Visualisasi & Analisis Data**:
    *   Grafik Pie distribusi kategori kegiatan.
    *   Grafik Batang tren kegiatan bulanan.
    *   Heatmap intensitas kegiatan.
    *   Grafik garis kumulatif progres kerja.
*   **Export Data**: Unduh rekap laporan kegiatan dalam format CSV berdasarkan rentang tanggal.
*   **Penyimpanan Lokal**: Data tersimpan aman dalam format CSV dan gambar bukti tersimpan di folder lokal.

## 🛠️ Teknologi

*   [Python](https://www.python.org/) (Bahasa Pemrograman Utama)
*   [Streamlit](https://streamlit.io/) (Framework Frontend)
*   [Pandas](https://pandas.pydata.org/) (Manipulasi Data)
*   [Plotly](https://plotly.com/) (Visualisasi Grafik Interaktif)
*   [Pillow (PIL)](https://python-pillow.org/) (Pemrosesan Gambar)

## ⚙️ Prasyarat

Pastikan Python sudah terinstal di komputer Anda.

## 🚀 Cara Instalasi & Menjalankan

1.  **Clone atau Download** repositori/folder proyek ini.

2.  **Instal Library Dependensi**:
    Buka terminal atau command prompt di folder proyek, lalu jalankan perintah berikut:

    ```bash
    pip install streamlit pandas plotly pillow
    ```

3.  **Jalankan Aplikasi**:
    Gunakan perintah berikut untuk memulai aplikasi:

    ```bash
    streamlit run tracking.py
    ```

4.  **Akses Aplikasi**:
    Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

## 📂 Struktur Folder

*   `tracking.py`: Kode utama aplikasi.
*   `kegiatan_pns.csv`: Database lokal (dibuat otomatis saat data disimpan).
*   `bukti_kegiatan/`: Folder penyimpanan gambar bukti (dibuat otomatis).

## 📝 Catatan

Aplikasi ini menggunakan sistem file lokal. Pastikan untuk membackup file `kegiatan_pns.csv` dan folder `bukti_kegiatan` jika Anda memindahkan aplikasi ke komputer lain agar data tidak hilang.

---
