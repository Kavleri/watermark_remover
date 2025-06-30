# Watermark_Remover

Alat ini menyediakan dua metode untuk menghapus watermark dari gambar dan video. Anda dapat memilih antara metode standar berbasis OpenCV atau metode canggih berbasis AI (Inpainting) yang didukung oleh model dari Hugging Face.

## Fitur 
<li>AI Inpainting: Menghapus objek atau watermark dari gambar dan video secara cerdas.</li>

<li>Metode Standar: Menghapus watermark dari gambar menggunakan teknik pemrosesan gambar konvensional.</li>

<li>Dukungan Video & Gambar: Mampu memproses file gambar dan video (khusus untuk mode AI).</li>

<li>Antarmuka Interaktif: Memungkinkan pengguna untuk menandai area watermark secara manual.</li>

### Instalasi

Pastikan Anda memiliki Python 3.8+ terinstal. Untuk menginstal semua dependensi yang diperlukan, jalankan perintah berikut di terminal Anda:

```bash
pip install opencv-python numpy torch torchvision torchaudio diffusers transformers accelerate pillow
```

### Konfigurasi 

<h4>Token Hugging Face (Wajib untuk Fitur AI)</h4>

Fitur penghapusan watermark berbasis AI memerlukan autentikasi ke Hugging Face Hub untuk mengunduh model. Anda hanya perlu melakukan konfigurasi ini satu kali.
<li>Dapatkan Access Token dari akun Hugging Face Anda di: <a href>huggingface.co/settings/tokens.</a></li>
<li>Jalankan perintah berikut di terminal untuk login terlebih dahulu:</li>

```bash
huggingface-cli login
```

<li>Tempelkan token Anda saat diminta dan tekan Enter.(misal : misal : hf_xxxxxxxxxxxxxxxxxxxxxxxxSJ)</li>

### Cara Penggunaan 

Proyek ini menyediakan dua skrip berbeda sesuai kebutuhan.


<li>Penghapus Watermark Berbasis AI (Gambar & Video)</li>

Skrip ini menggunakan model AI untuk mengisi area watermark secara cerdas. Cocok untuk watermark kompleks pada gambar dan video.

```bash
python video_foto_watermark.py
```

<li>Penghapus Watermark Standar (Hanya Gambar)</li>

Skrip ini menggunakan metode non-AI dan cocok untuk menghapus watermark sederhana pada gambar. Skrip ini tidak memerlukan token Hugging Face.

```bash
python hapus_watermark.py
```

### <i>Catatan Penggunaan

<li><b>Kinerja AI</b> : Fitur AI sangat bergantung pada spesifikasi komputer. Sangat disarankan menggunakan <b>GPU NVIDIA (CUDA)</b> untuk waktu proses yang wajar. Jika hanya menggunakan CPU, prosesnya akan sangat lambat.</li><br>

<li><b>Unduhan Pertama Kali</b> : Saat pertama kali menjalankan skrip AI, program akan mengunduh model dari Hugging Face. Ukuran model ini <b>lebih dari 5 GB</b>, jadi pastikan Anda memiliki koneksi internet yang stabil. Proses ini hanya terjadi sekali.</li><br>

<li><b>Panduan Prompt</b> : Kualitas hasil AI sangat dipengaruhi oleh prompt yang Anda berikan. Jelaskan area yang seharusnya ada di balik watermark, bukan menjelaskan watermark itu sendiri.</li><br>

<li><b>Batasan Pemrosesan Video</b> : Untuk video, mask (area yang Anda tandai) pada frame pertama akan diterapkan ke <b>seluruh durasi video</b>. Fitur ini paling efektif untuk menghapus objek statis seperti logo atau teks yang posisinya tidak berubah.</li><br>

<li><b>Sumber Daya</b> : Proses AI memakan banyak memori (RAM dan VRAM), terutama saat memproses video. Pastikan komputer Anda memiliki sumber daya yang cukup sebelum memproses file berdurasi panjang.</li></i>
