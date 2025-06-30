# watermark_remover
Alat ini menyediakan dua metode untuk menghapus watermark dari gambar dan video. Anda dapat memilih antara metode standar berbasis OpenCV atau metode canggih berbasis AI (Inpainting) yang didukung oleh model dari Hugging Face.

## Fitur ✨
<li>AI Inpainting: Menghapus objek atau watermark dari gambar dan video secara cerdas.</li>

<li>Metode Standar: Menghapus watermark dari gambar menggunakan teknik pemrosesan gambar konvensional.</li>

<li>Dukungan Video & Gambar: Mampu memproses file gambar dan video (khusus untuk mode AI).</li>

<li>Antarmuka Interaktif: Memungkinkan pengguna untuk menandai area watermark secara manual.</li>

### Instalasi ⚙️

Pastikan Anda memiliki Python 3.8+ terinstal. Untuk menginstal semua dependensi yang diperlukan, jalankan perintah berikut di terminal Anda:

```bash
pip install opencv-python numpy torch torchvision torchaudio diffusers transformers accelerate pillow
```
### Konfigurasi 🔑
<h4>Token Hugging Face (Wajib untuk Fitur AI)</h4>
Fitur penghapusan watermark berbasis AI memerlukan autentikasi ke Hugging Face Hub untuk mengunduh model. Anda hanya perlu melakukan konfigurasi ini satu kali.
<li>Dapatkan Access Token dari akun Hugging Face Anda di: <a href>huggingface.co/settings/tokens.</a></li>
<li>Jalankan perintah berikut di terminal untuk login terlebih dahulu:</li>
```bash
huggingface-cli login
```
<li>Tempelkan token Anda saat diminta dan tekan Enter.</li>

### Cara Penggunaan 🚀
Proyek ini menyediakan dua skrip berbeda sesuai kebutuhan.

Terminal akan menampilkan Token: (Masukkan Token anda, Tempel (paste) token yang sudah Anda salin tadi, misal : hf_xxxxxxxxxxxxxxxxxxxxxxxxSJ, lalu tekan enter)

<li>1. Penghapus Watermark Berbasis AI (Gambar & Video)</li>
Skrip ini menggunakan model AI untuk mengisi area watermark secara cerdas. Cocok untuk watermark kompleks pada gambar dan video.
```bash
python video_foto_watermark.py
```

<li>Penghapus Watermark Standar (Hanya Gambar)</li>
Skrip ini menggunakan metode non-AI dan cocok untuk menghapus watermark sederhana pada gambar. Skrip ini tidak memerlukan token Hugging Face.
```bash
python hapus_watermark.py
```
