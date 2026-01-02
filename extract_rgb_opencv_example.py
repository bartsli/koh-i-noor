#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Przykład użycia OpenCV do ekstrakcji kolorów z obrazów
- Szybsze niż PIL dla dużych obszarów
- Zaawansowane maskowanie i filtrowanie
- Możliwość użycia mediany/percentyli zamiast średniej
"""

import cv2
import numpy as np
import json

def extract_rgb_opencv(image_path, center_x, center_y, area_width, area_height):
    """
    Ekstrakcja RGB używając OpenCV - szybsza i bardziej zaawansowana.
    
    Zalety OpenCV:
    - Szybsze przetwarzanie (numpy arrays)
    - Zaawansowane maskowanie
    - Możliwość użycia mediany/percentyli
    - Lepsze filtrowanie
    """
    # Wczytaj obraz
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Konwertuj BGR na RGB (OpenCV używa BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Oblicz granice obszaru
    half_w = area_width // 2
    half_h = area_height // 2
    
    x_start = max(0, center_x - half_w)
    x_end = min(img_rgb.shape[1], center_x + half_w)
    y_start = max(0, center_y - half_h)
    y_end = min(img_rgb.shape[0], center_y + half_h)
    
    # Wyciągnij obszar
    roi = img_rgb[y_start:y_end, x_start:x_end]
    
    if roi.size == 0:
        return None
    
    # Stwórz maskę - wyklucz białe i czarne piksele
    white_threshold = 240
    black_threshold = 50
    
    # Maskowanie białych pikseli
    white_mask = np.all(roi > white_threshold, axis=2)
    
    # Maskowanie czarnych pikseli
    black_mask = np.all(roi < black_threshold, axis=2)
    
    # Kombinuj maski (wyklucz białe i czarne)
    valid_mask = ~(white_mask | black_mask)
    
    if not np.any(valid_mask):
        return None
    
    # Wyciągnij ważne piksele
    valid_pixels = roi[valid_mask]
    
    # OPCJA 1: Średnia (jak obecnie)
    avg_rgb = np.mean(valid_pixels, axis=0).astype(int)
    
    # OPCJA 2: Mediana (bardziej odporna na outliers)
    median_rgb = np.median(valid_pixels, axis=0).astype(int)
    
    # OPCJA 3: Percentyl 75 (bardziej nasycone kolory)
    percentile_75_rgb = np.percentile(valid_pixels, 75, axis=0).astype(int)
    
    return {
        'mean': tuple(avg_rgb),
        'median': tuple(median_rgb),
        'percentile_75': tuple(percentile_75_rgb),
        'num_pixels': len(valid_pixels)
    }


def extract_rgb_opencv_advanced(image_path, center_x, center_y, area_width, area_height):
    """
    Zaawansowana ekstrakcja z OpenCV - używa segmentacji kolorów.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Oblicz granice
    half_w = area_width // 2
    half_h = area_height // 2
    
    x_start = max(0, center_x - half_w)
    x_end = min(img_rgb.shape[1], center_x + half_w)
    y_start = max(0, center_y - half_h)
    y_end = min(img_rgb.shape[0], center_y + half_h)
    
    roi = img_rgb[y_start:y_end, x_start:x_end]
    
    if roi.size == 0:
        return None
    
    # Filtruj białe i czarne
    white_mask = np.all(roi > 240, axis=2)
    black_mask = np.all(roi < 50, axis=2)
    valid_mask = ~(white_mask | black_mask)
    
    if not np.any(valid_mask):
        return None
    
    valid_pixels = roi[valid_mask]
    
    # Użyj K-means clustering do znalezienia dominującego koloru
    # (opcjonalnie - bardziej zaawansowane)
    from sklearn.cluster import KMeans
    
    # Reshape dla K-means
    pixels_reshaped = valid_pixels.reshape(-1, 3)
    
    # K-means z 1 klastrem = dominujący kolor
    kmeans = KMeans(n_clusters=1, random_state=42, n_init=10)
    kmeans.fit(pixels_reshaped)
    
    dominant_color = kmeans.cluster_centers_[0].astype(int)
    
    return {
        'dominant_kmeans': tuple(dominant_color),
        'mean': tuple(np.mean(valid_pixels, axis=0).astype(int)),
        'median': tuple(np.median(valid_pixels, axis=0).astype(int)),
        'num_pixels': len(valid_pixels)
    }


if __name__ == "__main__":
    # Przykład użycia
    image_path = "probki-kredek-na-papierze-trzecia-kalibracja.jpg"
    
    # Parametry dla kredki 5
    center_x = 572  # Środek kolumny
    center_y = 1970  # Środek próbki kredki 5
    area_width = 539
    area_height = 143
    
    print("Ekstrakcja RGB używając OpenCV:")
    print("=" * 80)
    
    result = extract_rgb_opencv(image_path, center_x, center_y, area_width, area_height)
    
    if result:
        print(f"Liczba ważnych pikseli: {result['num_pixels']:,}")
        print()
        print("Metody ekstrakcji:")
        print(f"  Średnia:        RGB{result['mean']}")
        print(f"  Mediana:        RGB{result['median']}")
        print(f"  Percentyl 75:  RGB{result['percentile_75']}")
        print()
        print("Rekomendacja: Użyj mediany - bardziej odporna na outliers")
        print(f"  RGB{result['median']}")


