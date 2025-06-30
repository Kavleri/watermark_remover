import cv2
import numpy as np
import torch
from PIL import Image
from diffusers import AutoPipelineForInpainting
import os # Ditambahkan untuk manajemen file

# --- Variabel Global & Fungsi Bantuan (Sebagian besar sama) ---
drawing = False
mask = None
original_image = None # Untuk gambar, ini adalah gambar. Untuk video, ini adalah frame pertama.
display_image = None
scaling_factor = 1.0
brush_size = 30 # Ukuran kuas bisa diubah di sini

def resize_to_fit(image, max_width=1280, max_height=720):
    global scaling_factor
    h, w = image.shape[:2]
    # Hanya hitung ulang scaling_factor jika belum di-set
    if scaling_factor == 1.0 or (h > max_height or w > max_width):
        scaling_factor = min(max_height / h, max_width / w)
        if scaling_factor >= 1.0:
            scaling_factor = 1.0
            return image
        return cv2.resize(image, (int(w * scaling_factor), int(h * scaling_factor)))
    else: # Gunakan scaling factor yang sudah ada
        return cv2.resize(image, (int(w * scaling_factor), int(h * scaling_factor)))

def draw_mask(event, x, y, flags, param):
    global drawing, mask, brush_size, scaling_factor
    # Pastikan mask tidak None
    if mask is None:
        return
        
    original_x, original_y = int(x / scaling_factor), int(y / scaling_factor)
    
    # Brush size dihitung ulang relatif terhadap resolusi asli
    # Ini membuat ukuran kuas konsisten terlepas dari seberapa besar gambar di-resize
    scaled_brush_size = int(brush_size / scaling_factor)

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(mask, (original_x, original_y), scaled_brush_size, 255, -1)
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.circle(mask, (original_x, original_y), scaled_brush_size, 255, -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(mask, (original_x, original_y), scaled_brush_size, 255, -1)

# --- Fungsi Pemrosesan Inti ---

def get_user_mask(frame_to_mask):
    """Fungsi untuk menampilkan UI dan mendapatkan mask dari pengguna."""
    global mask, display_image
    
    # Inisialisasi mask berdasarkan resolusi frame asli
    mask = np.zeros(frame_to_mask.shape[:2], dtype="uint8")
    
    # Tampilkan UI untuk menggambar mask
    window_name = "Tandai Area yang Akan Dihapus (Tekan 's' untuk Lanjut, 'q' untuk Batal)"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_mask)
    
    print("\nSilakan gambar pada area yang ingin Anda hapus/ubah.")
    print("Gunakan mouse untuk menggambar. Tekan 's' jika sudah selesai, atau 'q' untuk keluar.")
    
    while True:
        display_image = resize_to_fit(frame_to_mask)
        mask_resized = cv2.resize(mask, (display_image.shape[1], display_image.shape[0]))
        
        # Buat overlay merah transparan
        overlay_color = cv2.cvtColor(mask_resized, cv2.COLOR_GRAY2BGR)
        overlay_color[np.where((overlay_color == [255, 255, 255]).all(axis=2))] = [0, 0, 255] # Merah
        combined_display = cv2.addWeighted(display_image, 0.7, overlay_color, 0.3, 0)
        
        cv2.imshow(window_name, combined_display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            return None # Batal
        elif key == ord('s'):
            cv2.destroyAllWindows()
            # Cek jika mask kosong
            if np.all(mask == 0):
                print("Peringatan: Anda tidak menandai area apapun. Proses dibatalkan.")
                return None
            return mask # Selesai

def process_image(pipe, device):
    """Logika untuk memproses file gambar tunggal."""
    global original_image
    file_gambar = input("Masukkan nama file gambar: ")
    original_image = cv2.imread(file_gambar)
    if original_image is None:
        print(f"Error: File '{file_gambar}' tidak ditemukan.")
        return

    # Dapatkan mask dari pengguna
    user_mask = get_user_mask(original_image)
    if user_mask is None:
        return

    prompt = input("Masukkan PROMPT (deskripsi gambar, cth: 'a photo of a clear blue sky'): ")
    print("\nMemproses dengan AI... Harap tunggu.")

    # Konversi ke format yang dibutuhkan pipeline
    pil_image = Image.fromarray(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    pil_mask = Image.fromarray(user_mask)

    generator = torch.Generator(device=device).manual_seed(0)
    result_image_pil = pipe(
        prompt=prompt,
        image=pil_image,
        mask_image=pil_mask,
        generator=generator,
        num_inference_steps=25, # sedikit lebih tinggi untuk kualitas
        strength=0.99,
    ).images[0]
    
    result_image_cv = cv2.cvtColor(np.array(result_image_pil), cv2.COLOR_RGB2BGR)
    print("Proses AI selesai!")

    # Simpan dan tampilkan hasil
    nama_hasil = "hasil_ai_" + os.path.basename(file_gambar)
    cv2.imwrite(nama_hasil, result_image_cv)
    print(f"Hasil resolusi penuh disimpan sebagai '{nama_hasil}'")
    
    original_resized = resize_to_fit(original_image, max_height=512)
    result_resized = resize_to_fit(result_image_cv, max_height=512)
    final_comparison = np.hstack((original_resized, result_resized))
    cv2.imshow("Perbandingan (Asli vs Hasil AI) - Tekan tombol apapun untuk keluar", final_comparison)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_video(pipe, device):
    """Logika untuk memproses file video."""
    file_video = input("Masukkan nama file video: ")
    cap = cv2.VideoCapture(file_video)
    if not cap.isOpened():
        print(f"Error: Gagal membuka file video '{file_video}'.")
        return

    # Baca frame pertama untuk mendapatkan mask dari pengguna
    ret, first_frame = cap.read()
    if not ret:
        print("Error: Tidak bisa membaca frame dari video.")
        cap.release()
        return

    # Dapatkan mask dari pengguna menggunakan frame pertama
    user_mask = get_user_mask(first_frame)
    if user_mask is None:
        cap.release()
        return
        
    prompt = input("Masukkan PROMPT (deskripsi untuk area yang dihapus, cth: 'a clean wall'): ")

    # Siapkan video output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Codec
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    nama_hasil = "hasil_ai_" + os.path.basename(file_video)
    out = cv2.VideoWriter(nama_hasil, fourcc, fps, (width, height))
    
    # Reset video capture untuk mulai dari awal
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    print(f"\nMemulai pemrosesan video ({total_frames} frames)... Ini akan memakan waktu SANGAT LAMA.")
    print("PERINGATAN: Jangan menutup jendela program sampai proses selesai.")
    
    # Konversi mask ke PIL Image sekali saja
    pil_mask = Image.fromarray(user_mask)
    generator = torch.Generator(device=device).manual_seed(0)

    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        print(f"Memproses frame {i+1}/{total_frames}...")

        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        result_image_pil = pipe(
            prompt=prompt,
            image=pil_image,
            mask_image=pil_mask,
            generator=generator,
            num_inference_steps=20, # Turunkan sedikit untuk kecepatan
            strength=0.99,
        ).images[0]
        
        result_frame_cv = cv2.cvtColor(np.array(result_image_pil), cv2.COLOR_RGB2BGR)
        out.write(result_frame_cv)
        
    print("\nProses video selesai!")
    print(f"Video hasil disimpan sebagai '{nama_hasil}'")

    # Cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    """Fungsi utama untuk menjalankan program."""
    print("="*50)
    print("   AI Inpainting Tool untuk Gambar dan Video   ")
    print("="*50)
    
    print("Mengecek ketersediaan hardware...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32
    print(f"Menggunakan device: {device.upper()}")
    if device == "cpu":
        print("PERINGATAN: Tidak ada GPU yang terdeteksi. Proses akan SANGAT LAMBAT.")

    try:
        print("Memuat model AI Inpainting... (Ini bisa memakan waktu lama saat pertama kali)")
        pipe = AutoPipelineForInpainting.from_pretrained(
            "diffusers/stable-diffusion-xl-1.0-inpainting-0.1",
            torch_dtype=torch_dtype,
            variant="fp16" if device == "cuda" else None # Tidak pakai fp16 di CPU
        ).to(device)
        print("Model AI berhasil dimuat.")
    except Exception as e:
        print(f"Gagal memuat model AI: {e}")
        print("Pastikan instalasi PyTorch, diffusers, dll sudah benar dan koneksi internet stabil.")
        return

    while True:
        print("\n" + "-"*20)
        mode = input("Pilih mode (1: Gambar, 2: Video, q: Keluar): ")
        if mode == '1':
            process_image(pipe, device)
        elif mode == '2':
            process_video(pipe, device)
        elif mode.lower() == 'q':
            print("Terima kasih telah menggunakan program ini.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    main()