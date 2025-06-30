# watermark_remover

## Persiapan

### Requirements

Untuk menjalankan alat ini, install semua dependensi yang dibutuhkan dengan perintah berikut:

```bash
pip install opencv-python numpy torch torchvision torchaudio diffusers transformers accelerate pillow

### Kebutuhhan

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
