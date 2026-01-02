#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt do ekstrakcji wartości RGB z rzeczywistych próbek kredek na zdjęciu
"""

from PIL import Image
import json

def extract_rgb_from_swatch(img, swatch_x, swatch_y, swatch_width, swatch_height):
    """
    Wyciąga wartość RGB z prostokątnej próbki koloru.
    Używa mediany z najciemniejszych/najbardziej nasyconych pikseli,
    aby uniknąć wpływu przeświecającego papieru.
    """
    pixels = []
    white_threshold = 230  # Piksele jaśniejsze niż to są uważane za białe tło
    black_threshold = 40   # Piksele ciemniejsze niż to są uważane za czarne obramowanie
    
    for y in range(swatch_y, swatch_y + swatch_height):
        for x in range(swatch_x, swatch_x + swatch_width):
            if 0 <= x < img.width and 0 <= y < img.height:
                pixel = img.getpixel((x, y))
                if isinstance(pixel, int):
                    # Grayscale
                    r = g = b = pixel
                else:
                    r, g, b = pixel[:3]
                
                # Ignoruj białe tło i czarne obramowanie
                if not (r > white_threshold and g > white_threshold and b > white_threshold):
                    if not (r < black_threshold and g < black_threshold and b < black_threshold):
                        pixels.append((r, g, b))
    
    if not pixels:
        return None
    
    # Sortuj piksele według nasycenia (różnica między max a min wartością RGB)
    # i weź medianę z 30% najbardziej nasyconych pikseli
    pixels_with_saturation = []
    for r, g, b in pixels:
        saturation = max(r, g, b) - min(r, g, b)
        pixels_with_saturation.append((saturation, r, g, b))
    
    # Sortuj według nasycenia (malejąco)
    pixels_with_saturation.sort(reverse=True)
    
    # Weź 30% najbardziej nasyconych pikseli
    top_pixels = pixels_with_saturation[:max(1, len(pixels_with_saturation) // 3)]
    
    # Oblicz średnią z najbardziej nasyconych pikseli
    avg_r = sum(p[1] for p in top_pixels) // len(top_pixels)
    avg_g = sum(p[2] for p in top_pixels) // len(top_pixels)
    avg_b = sum(p[3] for p in top_pixels) // len(top_pixels)
    
    return (avg_r, avg_g, avg_b)


def extract_colors_from_photo(image_path):
    """
    Ekstrahuje wartości RGB z kolumny "PRÓBKA KREDKAMI" na zdjęciu.
    """
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    print(f"Rozmiar obrazka: {width}x{height}")
    
    # Numery kredek w kolejności od góry do dołu (zgodnie z opisem)
    pencil_numbers = [1, 41, 504, 3, 801, 28, 45, 44, 42, 558, 126, 5, 6, 170, 601, 132, 603, 131, 357, 178, 177, 8, 182, 180]
    
    # Szacunkowe pozycje - będziemy musieli dostosować na podstawie rzeczywistego obrazka
    # Zakładam, że próbki są w prawej kolumnie, zaczynają się poniżej nagłówków
    
    # Najpierw znajdźmy obszar z próbkami - szukamy kolumny z kolorami (nie białej)
    # Próbki są w prawej kolumnie, około 60-70% szerokości obrazka
    
    # Szacunkowe wartości - będziemy musieli je dostosować
    # Zakładam strukturę: [NUMERY] [WYDRUK] [PRÓBKA KREDKAMI]
    # Próbka kredek jest w prawej kolumnie
    
    # Znajdź początek próbek (poniżej nagłówków)
    header_height = int(height * 0.08)  # Około 8% wysokości na nagłówki
    
    # Szerokość kolumny z próbkami
    # Zakładam, że obrazek ma 3 kolumny, każda zajmuje ~30% szerokości
    swatch_column_start = int(width * 0.60)  # Prawa kolumna zaczyna się około 60% szerokości
    swatch_column_width = int(width * 0.30)    # Kolumna ma około 30% szerokości
    
    # Wysokość każdej próbki
    num_rows = 24
    available_height = height - header_height
    swatch_height = int(available_height / num_rows)
    
    color_map = {}
    
    print("\nEkstrakcja kolorów z próbek kredek:")
    print("=" * 80)
    
    for i, pencil_num in enumerate(pencil_numbers):
        # Pozycja próbki
        swatch_y = header_height + i * swatch_height + int(swatch_height * 0.1)  # 10% marginesu od góry próbki
        swatch_x = swatch_column_start + int(swatch_column_width * 0.1)  # 10% marginesu od lewej
        swatch_w = int(swatch_column_width * 0.8)  # 80% szerokości kolumny
        swatch_h = int(swatch_height * 0.8)  # 80% wysokości próbki
        
        # Wyciągnij kolor
        rgb = extract_rgb_from_swatch(img, swatch_x, swatch_y, swatch_w, swatch_h)
        
        if rgb:
            color_map[pencil_num] = rgb
            print(f"  3800/{pencil_num:03d}: RGB{rgb}")
        else:
            print(f"  3800/{pencil_num:03d}: NIE ZNALEZIONO")
    
    return color_map


if __name__ == "__main__":
    image_path = "probki-kredek-na-papierze.jpg"
    
    print("Ekstrakcja wartości RGB z rzeczywistych próbek kredek...")
    print(f"Obrazek: {image_path}")
    print()
    
    color_map = extract_colors_from_photo(image_path)
    
    print()
    print("=" * 80)
    print(f"Wyekstrahowano {len(color_map)} kolorów")
    
    # Zapisz do pliku JSON
    with open("extracted_rgb_from_photo.json", "w") as f:
        json.dump(color_map, f, indent=2)
    print(f"✓ Zapisano do extracted_rgb_from_photo.json")
    
    # Wyświetl porównanie ze starymi wartościami
    print()
    print("PORÓWNANIE Z OBECNYMI WARTOŚCIAMI:")
    print("=" * 80)
    
    # Wczytaj obecne wartości z generate_swatches.py
    import sys
    sys.path.insert(0, '.')
    from generate_swatches import get_color_for_pencil
    
    for pencil_num in sorted(color_map.keys()):
        new_rgb = color_map[pencil_num]
        old_rgb = get_color_for_pencil(pencil_num, "")
        if old_rgb != new_rgb:
            print(f"  3800/{pencil_num:03d}:")
            print(f"    Stare: RGB{old_rgb}")
            print(f"    Nowe:  RGB{new_rgb}")
            print()

