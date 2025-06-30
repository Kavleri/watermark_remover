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

Ketika sudah menginstall semua dependensi, masukkan token HuggingFace (Optional)
```bash
huggingface-cli login

Terminal akan menampilkan Token: (Masukkan Token anda, Tempel (paste) token yang sudah Anda salin tadi, misal : hf_xxxxxxxxxxxxxxxxxxxxxxxxSJ, lalu tekan enter)

<i>Catatan: Saat Anda menempelkan token, teksnya mungkin tidak akan terlihat di layar. Ini adalah fitur keamanan standar di terminal.</i>

Setelah berhasil, akan terlihat pesan seperti (Token is valid. Login successful)

Pilihan lain, anda bisa menjalankan langsung alat <b>hapus_watermark.py</b> (Untuk gambar tanpa AI)
dengan perintah
``bash
python hapus_watermark.py

Kalau sudah memasukkan Token, bisa langsung pakai alat <b>video_foto_watermark.py</b>
dengan perintah
``bash
python video_foto_watermark.py
