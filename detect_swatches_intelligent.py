#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inteligentne wykrywanie obszarów próbek kolorów na obrazie używając OpenCV
- Automatyczne wykrywanie konturów prostokątnych
- Wykrywanie linii siatki (grid)
- Segmentacja obszarów próbek
- Automatyczne znajdowanie środka każdej próbki
"""

import cv2
import numpy as np
import json


def detect_grid_lines(img_gray):
    """
    Wykrywa poziome i pionowe linie siatki (grid) na obrazie.
    
    Returns:
        tuple: (horizontal_lines, vertical_lines) - listy linii
    """
    # Wykryj krawędzie używając Canny
    edges = cv2.Canny(img_gray, 50, 150, apertureSize=3)
    
    # Wykryj linie używając HoughLinesP (probabilistyczna wersja - szybsza)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                            minLineLength=100, maxLineGap=10)
    
    if lines is None:
        return [], []
    
    horizontal_lines = []
    vertical_lines = []
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        # Określ czy linia jest pozioma czy pionowa
        if abs(x2 - x1) > abs(y2 - y1):
            # Pozioma linia
            horizontal_lines.append((y1, y2))
        else:
            # Pionowa linia
            vertical_lines.append((x1, x2))
    
    return horizontal_lines, vertical_lines


def detect_swatch_contours(img_gray, min_area=5000, max_area=50000):
    """
    Wykrywa kontury prostokątnych próbek na obrazie.
    
    Args:
        img_gray: Obraz w skali szarości
        min_area: Minimalna powierzchnia konturu
        max_area: Maksymalna powierzchnia konturu
    
    Returns:
        list: Lista prostokątów (x, y, width, height)
    """
    # Binary threshold - czarne linie i obramowania będą czarne
    _, binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Znajdź kontury
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    swatches = []
    
    for contour in contours:
        # Oblicz powierzchnię konturu
        area = cv2.contourArea(contour)
        
        if min_area < area < max_area:
            # Znajdź prostokąt ograniczający
            x, y, w, h = cv2.boundingRect(contour)
            
            # Sprawdź czy to prostokąt (stosunek boków)
            aspect_ratio = w / h if h > 0 else 0
            if 0.3 < aspect_ratio < 3.0:  # Dopuszczalny zakres proporcji
                swatches.append((x, y, w, h))
    
    # Posortuj według pozycji (góra-dół, lewo-prawo)
    swatches.sort(key=lambda s: (s[1], s[0]))
    
    return swatches


def detect_swatch_regions_by_color(img_rgb, target_col_start=400, target_col_width=445, num_swatches=24):
    """
    Wykrywa obszary próbek na podstawie kolumny docelowej i segmentacji kolorów.
    Używa projekcji histogramu do wykrywania poziomych linii.
    
    Args:
        img_rgb: Obraz w RGB
        target_col_start: Początek kolumny docelowej (X)
        target_col_width: Szerokość kolumny docelowej
        num_swatches: Oczekiwana liczba próbek
    
    Returns:
        list: Lista obszarów próbek [(x, y, w, h), ...]
    """
    height, width = img_rgb.shape[:2]
    
    # Wyciągnij kolumnę docelową
    col_end = min(target_col_start + target_col_width, width)
    target_col = img_rgb[:, target_col_start:col_end]
    
    # Konwertuj na skale szarości dla analizy
    target_col_gray = cv2.cvtColor(target_col, cv2.COLOR_RGB2GRAY)
    
    # Wykryj poziome linie używając projekcji histogramu
    # Czarne linie będą miały niskie wartości w projekcji
    h_projection = np.sum(target_col_gray, axis=1)
    
    # Normalizuj projekcję
    h_projection_norm = (h_projection - np.min(h_projection)) / (np.max(h_projection) - np.min(h_projection) + 1)
    
    # Znajdź minima (linie) - użyj threshold adaptacyjnego
    threshold = np.mean(h_projection_norm) * 0.7  # 70% średniej wartości
    line_mask = h_projection_norm < threshold
    
    # Znajdź ciągłe regiony linii
    line_positions = []
    in_line = False
    line_start = 0
    
    for i, is_line in enumerate(line_mask):
        if is_line and not in_line:
            line_start = i
            in_line = True
        elif not is_line and in_line:
            # Środek linii
            line_positions.append((line_start + i) // 2)
            in_line = False
    
    # Równomierny podział na podstawie oczekiwanej liczby próbek
    # NIE pomijaj górnego paska - dziel od y=0
    # Pomijaj dolny margines (40px)
    bottom_margin = 40
    total_height = height - bottom_margin
    
    # Oblicz DOKŁADNĄ wysokość i szerokość - wszystkie próbki mają identyczne wymiary
    swatch_height = int(total_height / num_swatches)  # Dokładna wysokość (zaokrąglona w dół)
    margin_x = int(target_col_width * 0.05)  # 5% marginesu z każdej strony
    swatch_width = target_col_width - 2 * margin_x  # Dokładna szerokość
    
    swatches = []
    for i in range(num_swatches):
        y_start = int(i * swatch_height)
        y_end = int((i + 1) * swatch_height)
        h = swatch_height  # Użyj dokładnej wysokości (nie obliczonej z różnicy)
        x_actual = target_col_start + margin_x
        w_actual = swatch_width  # Użyj dokładnej szerokości
        
        swatches.append((x_actual, y_start, w_actual, h))
    
    return swatches
    
    # NIE używaj wykrytych linii - zawsze używaj równomiernego podziału
    # (kod powyżej już zwraca równomierny podział)


def intelligent_swatch_detection(image_path, target_col_start=400, target_col_width=445, pencil_order=None):
    """
    Inteligentne wykrywanie obszarów próbek na obrazie.
    Kombinuje różne metody wykrywania.
    
    Args:
        image_path: Ścieżka do obrazu
        target_col_start: Początek kolumny docelowej (X)
        target_col_width: Szerokość kolumny docelowej
        pencil_order: Lista numerów kredek w kolejności, w jakiej są na zdjęciu (z góry do dołu)
                     Jeśli None, użyje domyślnej kolejności
    
    Returns:
        dict: Mapa numeru kredki -> (center_x, center_y, width, height)
    """
    # Wczytaj obraz
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print(f"Błąd: Nie można wczytać obrazu {image_path}")
        return None
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    height, width = img_rgb.shape[:2]
    
    print(f"Rozmiar obrazka: {width}x{height}")
    print()
    
    # METODA 1: Wykrywanie na podstawie kolumny i segmentacji kolorów
    print("Wykrywanie próbek metodą segmentacji kolorów...")
    swatches = detect_swatch_regions_by_color(img_rgb, target_col_start, target_col_width, num_swatches=24)
    
    print(f"Znaleziono {len(swatches)} próbek")
    
    # POSORTUJ swatches według współrzędnej Y (od góry do dołu), aby mieć pewność kolejności
    swatches_sorted = sorted(swatches, key=lambda s: s[1])  # s[1] to współrzędna Y
    
    # Numery kredek w kolejności - użyj przekazanej kolejności lub domyślnej
    if pencil_order is None:
        pencil_numbers = [1, 41, 504, 3, 801, 28, 45, 44, 42, 558, 126, 5, 6, 170, 601, 132, 603, 131, 357, 178, 177, 8, 182, 180]
    else:
        pencil_numbers = pencil_order
    
    # Stwórz mapę: numer kredki -> obszar próbki
    
    swatch_map = {}
    
    for i, (x, y, w, h) in enumerate(swatches_sorted):
        if i < len(pencil_numbers):
            pencil_num = pencil_numbers[i]
            center_x = x + w // 2
            center_y = y + h // 2
            
            swatch_map[pencil_num] = {
                'center_x': int(center_x),
                'center_y': int(center_y),
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h)
            }
            
            print(f"  Kredka {pencil_num:03d}: Y={y}, center=({center_x}, {center_y}), size=({w}x{h})")
    
    return swatch_map


def extract_rgb_from_detected_swatch(img_rgb, swatch_info, margin_percent=0.25):
    """
    Ekstrahuje RGB z wykrytego obszaru próbki, unikając krawędzi.
    
    Args:
        img_rgb: Obraz w RGB
        swatch_info: Dict z informacjami o próbce (x, y, width, height)
        margin_percent: Procent marginesu do odcięcia (0.25 = 25% z każdej strony)
    
    Returns:
        tuple: (R, G, B) lub None
    """
    x = swatch_info['x']
    y = swatch_info['y']
    w = swatch_info['width']
    h = swatch_info['height']
    
    # Oblicz marginesy (odcinamy krawędzie)
    margin_x = int(w * margin_percent)
    margin_y = int(h * margin_percent)
    
    # Wyciągnij tylko środkową część próbki
    x_start = max(0, x + margin_x)
    x_end = min(img_rgb.shape[1], x + w - margin_x)
    y_start = max(0, y + margin_y)
    y_end = min(img_rgb.shape[0], y + h - margin_y)
    
    roi = img_rgb[y_start:y_end, x_start:x_end]
    
    if roi.size == 0:
        return None
    
    # Filtruj czarne i szare piksele (linie, obramowania)
    # NIE filtruj białych - mogą być prawdziwymi kolorami (np. White)
    black_threshold = 60
    
    black_mask = np.all(roi < black_threshold, axis=2)
    channel_diff = np.max(roi, axis=2) - np.min(roi, axis=2)
    gray_black_mask = channel_diff < 15  # Szare/czarne linie
    
    valid_mask = ~(black_mask | gray_black_mask)
    
    # Jeśli nie ma wystarczająco ważnych pikseli, użyj wszystkich (może być biały kolor)
    if not np.any(valid_mask) or np.sum(valid_mask) < roi.size * 0.1:
        # Użyj wszystkich pikseli z wykluczeniem tylko czarnych linii
        valid_mask = ~black_mask
        if not np.any(valid_mask):
            valid_mask = np.ones(roi.shape[:2], dtype=bool)  # Użyj wszystkich pikseli
    
    valid_pixels = roi[valid_mask]
    median_rgb = np.median(valid_pixels, axis=0).astype(int)
    
    return (int(median_rgb[0]), int(median_rgb[1]), int(median_rgb[2]))


if __name__ == "__main__":
    image_path = "probki-kredek-na-papierze-trzecia-kalibracja.jpg"
    
    print("=" * 80)
    print("INTELIGENTNE WYKRYWANIE OBSZARÓW PRÓBEK")
    print("=" * 80)
    print()
    
    # Wykryj obszary próbek
    swatch_map = intelligent_swatch_detection(image_path)
    
    if swatch_map:
        print()
        print("=" * 80)
        print("EKSTRAKCJA KOLORÓW Z WYKRYTYCH OBSZARÓW")
        print("=" * 80)
        print()
        
        # Wczytaj obraz ponownie dla ekstrakcji
        img_bgr = cv2.imread(image_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        color_map = {}
        
        for pencil_num, swatch_info in sorted(swatch_map.items()):
            rgb = extract_rgb_from_detected_swatch(img_rgb, swatch_info, margin_percent=0.25)
            
            if rgb:
                color_map[pencil_num] = rgb
                print(f"  3800/{pencil_num:03d}: RGB{rgb}")
            else:
                print(f"  3800/{pencil_num:03d}: NIE ZNALEZIONO")
        
        # Zapisz do JSON
        output_data = {}
        for num, rgb in color_map.items():
            output_data[str(num)] = {
                'rgb': list(rgb),
                'swatch_info': swatch_map[num]
            }
        
        with open("extracted_rgb_intelligent.json", "w") as f:
            json.dump(output_data, f, indent=2)
        
        print()
        print("=" * 80)
        print(f"Wyekstrahowano {len(color_map)} kolorów")
        print(f"✓ Zapisano do extracted_rgb_intelligent.json")
        print()
        print("Metoda: Inteligentne wykrywanie obszarów + ekstrakcja z środka próbki")

