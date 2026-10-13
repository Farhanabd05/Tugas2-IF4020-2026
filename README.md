# Cakra Cipher

## Deskripsi

Cakra Cipher merupakan algoritma kriptografi yang dikembangkan dengan memodifikasi struktur Jaringan Feistel melalui 
penambahan operasi rotasi bit dinamis dan penjumlahan modulo 256. Rotasi bit pada fungsi putaran dirancang untuk meningkatkan 
penyebaran bit (*diffusion*), sedangkan penjumlahan modulo 256 menambahkan hubungan non-linear antara kunci utama dan kunci putaran 
dengan biaya komputasi yang relatif ringan. S-box dan P-box dibangkitkan secara independen menggunakan algoritma Fisher–Yates, 
sehingga struktur substitusi dan permutasi yang digunakan tidak diambil langsung dari rancangan cipher yang sudah ada.

Penjelasan lengkap mengenai mekanisme dan rancangan algoritma tersedia dalam dokumen laporan di folder `doc`.

## Tech Stack

- Python

## Dependensi

- Python 3.11.5 atau versi kompatibel yang setara.

## Cara Menjalankan Program
- **Contoh penggunaan API:** Lihat `example.py` untuk mempelajari cara menggunakan fungsi enkripsi dan dekripsi dari program.
- **Aplikasi CLI:** Jalankan `main.py` untuk menggunakan antarmuka command-line dalam mengenkripsi atau mendekripsi file teks (`.txt`).
- **Menjalankan pengujian:** Untuk menghasilkan ulang hasil pengujian, jalankan skrip pengujian yang tersedia di folder `test`.
