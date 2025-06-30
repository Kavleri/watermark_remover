import cv2
import numpy as np

drawing = False
mask = None
original_image = None
display_image = None
scaling_factor = 1.0
brush_size = 20 

def resize_to_fit(image, max_width=1280, max_height=720):
    """Mengubah ukuran gambar dengan menjaga aspek rasio."""
    global scaling_factor
    h, w = image.shape[:2]
    
    if h > max_height or w > max_width:
        scaling_factor = min(max_height / h, max_width / w)
        new_w = int(w * scaling_factor)
        new_h = int(h * scaling_factor)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    else:
        scaling_factor = 1.0
        return image

def draw_mask(event, x, y, flags, param):
    """Menggambar pada mask dengan koordinat yang sudah disesuaikan."""
    global drawing, mask, brush_size, scaling_factor

    original_x = int(x / scaling_factor)
    original_y = int(y / scaling_factor)
    scaled_brush_size = int(brush_size / scaling_factor)

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(mask, (original_x, original_y), scaled_brush_size, (255, 255, 255), -1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(mask, (original_x, original_y), scaled_brush_size, (255, 255, 255), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(mask, (original_x, original_y), scaled_brush_size, (255, 255, 255), -1)

def main():
    global mask, original_image, display_image

    file_gambar = input("Masukkan nama file gambar (contoh: 'kucing.jpg'): ")
    try:
        original_image = cv2.imread(file_gambar)
        if original_image is None:
            print(f"Error: File '{file_gambar}' tidak ditemukan atau format tidak didukung.")
            return
    except Exception as e:
        print(f"Terjadi error saat membaca gambar: {e}")
        return

    display_image = resize_to_fit(original_image)
    
    mask = np.zeros(original_image.shape[:2], dtype="uint8")

    cv2.namedWindow("Tandai Area Watermark")
    cv2.setMouseCallback("Tandai Area Watermark", draw_mask)

    print("\n--- INSTRUKSI ---")
    print(f"Ukuran Kuas: {brush_size} (bisa diubah di dalam kode)")
    print("1. Tahan dan gerakkan mouse untuk menandai area yang akan dihapus.")
    print("2. Tekan 's' untuk MENYIMPAN dan MEMPROSES.")
    print("3. Tekan 'r' untuk MERESET tanda.")
    print("4. Tekan 'q' untuk KELUAR.")
    print("-----------------\n")

    while True:
        mask_resized_for_display = cv2.resize(mask, (display_image.shape[1], display_image.shape[0]))
        overlay_color = cv2.cvtColor(mask_resized_for_display, cv2.COLOR_GRAY2BGR)
        overlay_color[np.where((overlay_color == [255, 255, 255]).all(axis=2))] = [0, 0, 255]

        combined_display = cv2.addWeighted(display_image, 0.6, overlay_color, 0.4, 0)

        cv2.imshow("Tandai Area Watermark", combined_display)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("r"):
            mask = np.zeros(original_image.shape[:2], dtype="uint8") 
            print("Tanda telah direset.")
        elif key == ord("s"):
            print("Memproses...")
            result = cv2.inpaint(original_image, mask, 3, cv2.INPAINT_NS)

            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            
            h = 400
            original_resized = resize_to_fit(original_image, max_height=h)
            mask_resized = resize_to_fit(mask_bgr, max_height=h)
            result_resized = resize_to_fit(result, max_height=h)

            cv2.putText(original_resized, 'Asli', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(mask_resized, 'Masker', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(result_resized, 'Hasil', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            final_comparison = np.hstack((original_resized, mask_resized, result_resized))

            cv2.imshow("Perbandingan Hasil", final_comparison)
            
            nama_hasil = "hasil_" + file_gambar
            cv2.imwrite(nama_hasil, result)
            print(f"Proses selesai! Hasil resolusi penuh disimpan sebagai '{nama_hasil}'")
            print("Tekan tombol 'q' di jendela manapun untuk keluar.")
            
            while True:
                if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Perbandingan Hasil", cv2.WND_PROP_VISIBLE) < 1:
                    break
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()