#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ekstrakcja wartości RGB z rzeczywistych próbek kredek używając OpenCV
- Szybsze przetwarzanie (numpy arrays)
- Mediana zamiast średniej (bardziej odporna na outliers)
- Zaawansowane maskowanie
- Maksymalny obszar ekstrakcji (539x143 pikseli)
"""

import cv2
import numpy as np
import json

def extract_rgb_opencv(img_rgb, center_x, center_y, area_width, area_height):
    """
    Ekstrakcja RGB używając OpenCV - mediana z ważnych pikseli.
    
    Args:
        img_rgb: Obraz w formacie RGB (numpy array)
        center_x, center_y: Środek obszaru ekstrakcji
        area_width, area_height: Rozmiar obszaru
    
    Returns:
        tuple: (R, G, B) lub None
    """
    # Oblicz granice obszaru
    half_w = area_width // 2
    half_h = area_height // 2
    
    x_start = max(0, center_x - half_w)
    x_end = min(img_rgb.shape[1], center_x + half_w)
    y_start = max(0, center_y - half_h)
    y_end = min(img_rgb.shape[0], center_y + half_h)
    
    # Wyciągnij obszar (ROI - Region of Interest)
    roi = img_rgb[y_start:y_end, x_start:x_end]
    
    if roi.size == 0:
        return None
    
    # Stwórz maskę - wyklucz białe, czarne i szare piksele (bardziej agresywne filtrowanie)
    white_threshold = 230  # Niższy próg - wyklucz też bardzo jasne
    black_threshold = 60   # Wyższy próg - wyklucz też ciemne (czarne linie, obramowania)
    
    # Maskowanie białych pikseli (wszystkie kanały > threshold)
    white_mask = np.all(roi > white_threshold, axis=2)
    
    # Maskowanie czarnych pikseli (wszystkie kanały < threshold)
    black_mask = np.all(roi < black_threshold, axis=2)
    
    # Dodatkowo: wyklucz piksele z małą różnicą między kanałami (szare/czarne linie)
    # Czarne linie i obramowania mają niską wartość we wszystkich kanałach
    channel_diff = np.max(roi, axis=2) - np.min(roi, axis=2)
    gray_black_mask = channel_diff < 15  # Bardzo mała różnica = szare/czarne (linie, obramowania)
    
    # Kombinuj maski (wyklucz białe, czarne i szare/czarne)
    valid_mask = ~(white_mask | black_mask | gray_black_mask)
    
    if not np.any(valid_mask):
        return None
    
    # Wyciągnij ważne piksele
    valid_pixels = roi[valid_mask]
    
    # Użyj mediany zamiast średniej - bardziej odporna na outliers
    median_rgb = np.median(valid_pixels, axis=0).astype(int)
    
    # Konwertuj numpy.int64 na zwykły int dla JSON
    return (int(median_rgb[0]), int(median_rgb[1]), int(median_rgb[2]))


def extract_colors_from_photo_opencv(image_path):
    """
    Ekstrahuje wartości RGB z kolumny "PRÓBKA KREDKAMI" używając OpenCV.
    """
    # Wczytaj obraz używając OpenCV
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print(f"Błąd: Nie można wczytać obrazu {image_path}")
        return None
    
    # Konwertuj BGR na RGB (OpenCV używa BGR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    height, width = img_rgb.shape[:2]
    
    print(f"Rozmiar obrazka: {width}x{height}")
    print()
    
    # Numery kredek w kolejności
    pencil_numbers = [1, 41, 504, 3, 801, 28, 45, 44, 42, 558, 126, 5, 6, 170, 601, 132, 603, 131, 357, 178, 177, 8, 182, 180]
    
    # Parametry ekstrakcji - maksymalny obszar
    header_height = int(height * 0.08)
    num_rows = 24
    available_height = height - header_height
    swatch_height = int(available_height / num_rows)
    
    # Kolumna PRÓBKA KREDKAMI - faktyczna szerokość
    real_col_start = 300  # Od X=300
    real_col_width = 545  # Do X=845 (szerokość 545)
    center_x = real_col_start + real_col_width // 2
    
    # OBSZAR EKSTRAKCJI - tylko środkowa część próbki (bez krawędzi, czarnych linii i fragmentów wydruku)
    # Zmniejszony obszar, aby uniknąć:
    # - poziomych linii (kolumna "wydruk" zamiast "kredka")
    # - pionowych linii (wyjeżdżanie poza granice pojedynczej próbki)
    area_width = int(real_col_width * 0.45)  # 45% szerokości - tylko środek (unika pionowych linii)
    area_height = int(swatch_height * 0.45)  # 45% wysokości - tylko środek (unika poziomych linii z wydruku)
    
    print(f"Parametry ekstrakcji:")
    print(f"  Wysokość próbki: {swatch_height} pikseli")
    print(f"  Szerokość kolumny: {real_col_width} pikseli")
    print(f"  Obszar ekstrakcji: {area_width}x{area_height} = {area_width * area_height:,} pikseli")
    print()
    
    color_map = {}
    
    print("Ekstrakcja kolorów używając OpenCV (mediana):")
    print("=" * 80)
    
    for i, pencil_num in enumerate(pencil_numbers):
        # Środek próbki
        swatch_y = header_height + i * swatch_height + swatch_height // 2
        
        # Wyciągnij kolor używając OpenCV
        rgb = extract_rgb_opencv(img_rgb, center_x, swatch_y, area_width, area_height)
        
        if rgb:
            color_map[pencil_num] = rgb
            print(f"  3800/{pencil_num:03d}: RGB{rgb}")
        else:
            print(f"  3800/{pencil_num:03d}: NIE ZNALEZIONO")
    
    return color_map


if __name__ == "__main__":
    image_path = "probki-kredek-na-papierze-trzecia-kalibracja.jpg"
    
    print("Ekstrakcja wartości RGB używając OpenCV...")
    print(f"Obrazek: {image_path}")
    print()
    
    color_map = extract_colors_from_photo_opencv(image_path)
    
    if color_map:
        print()
        print("=" * 80)
        print(f"Wyekstrahowano {len(color_map)} kolorów")
        
        # Zapisz do pliku JSON
        output_data = {}
        for num, rgb in color_map.items():
            output_data[str(num)] = {
                'rgb': list(rgb)
            }
        
        with open("extracted_rgb_opencv.json", "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"✓ Zapisano do extracted_rgb_opencv.json")
        
        print()
        print("Metoda: Mediana z ważnych pikseli (odporna na outliers)")
        print("Obszar: 539x143 = 77,077 pikseli na próbkę")

