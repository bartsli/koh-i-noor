#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt do ekstrakcji kolorów z obrazków katalogowych Koh-I-Noor Polycolor
"""

from PIL import Image
import os
import json

def extract_color_from_grid(img, row, col, rows=6, cols=8, margin_top=80, margin_bottom=150, margin_left=60, margin_right=60):
    """
    Ekstrahuje kolor z siatki próbek na obrazku.
    Próbki kolorów to gradienty - najciemniejszy/najmocniejszy kolor jest na dole każdego kwadratu.
    
    Args:
        img: Obrazek PIL
        row: Numer wiersza (0-based)
        col: Numer kolumny (0-based)
        rows: Liczba wierszy w siatce
        cols: Liczba kolumn w siatce
        margin_*: Marginesy wokół siatki (w pikselach)
    
    Returns:
        Tuple (r, g, b) lub None
    """
    width, height = img.size
    
    # Oblicz rozmiar każdej komórki siatki
    cell_width = (width - margin_left - margin_right) / cols
    cell_height = (height - margin_top - margin_bottom) / rows
    
    # Oblicz pozycję środka próbki koloru - NA DOLE komórki, gdzie kolor jest najmocniejszy
    # Próbka koloru jest w dolnej części komórki, około 75-85% wysokości (dolna część)
    x = margin_left + col * cell_width + cell_width / 2
    y = margin_top + row * cell_height + cell_height * 0.80  # 80% wysokości - dolna część, gdzie kolor jest najmocniejszy
    
    # Pobierz próbkę z małego obszaru na samym dole (środek dolnej części)
    sample_size_x = 10  # poziomy rozmiar próbki
    sample_size_y = 8    # pionowy rozmiar próbki (mały, bo chcemy tylko dół)
    pixels = []
    for dx in range(-sample_size_x, sample_size_x + 1):
        for dy in range(-sample_size_y, 0):  # Tylko w górę od punktu (czyli dolna część)
            px = int(x + dx)
            py = int(y + dy)
            if 0 <= px < width and 0 <= py < height:
                pixel = img.getpixel((px, py))
                # Ignoruj białe piksele (prawdopodobnie tło)
                if pixel != (255, 255, 255):
                    pixels.append(pixel)
    
    if pixels:
        # Oblicz średni kolor (tylko z nie-białych pikseli)
        avg_r = sum(p[0] for p in pixels) // len(pixels)
        avg_g = sum(p[1] for p in pixels) // len(pixels)
        avg_b = sum(p[2] for p in pixels) // len(pixels)
        return (avg_r, avg_g, avg_b)
    
    return None


def build_color_map_from_images():
    """
    Buduje mapę kolorów na podstawie obrazków katalogowych.
    Mapowanie numerów kredek do pozycji w siatce na podstawie opisów obrazków.
    """
    color_map = {}
    
    # Obrazek 1: Białe, żółcie, pomarańcze, czerwienie, róże, brązy/skóry (6x8 = 48 kolorów)
    # Zgodnie z opisem - rzędy od góry do dołu, kolumny od lewej do prawej
    # Mapowanie: pozycja w siatce -> numer kredki w zestawie 72
    img1_mapping = {
        # Row 1 (Whites and Yellows)
        (0, 0): 1,    # Titanium White (3800/01)
        (0, 1): 500,  # Ivory Bone (3800/500) - nie w zestawie 72
        (0, 2): 550,  # Fair Portrait Gold (3800/550) - nie w zestawie 72
        (0, 3): 501,  # Pollen Yellow (3800/501) - nie w zestawie 72
        (0, 4): 41,   # Banana Yellow (3800/41)
        (0, 5): 2,    # Lemon Yellow (3800/504 w obrazku, ale 2 w zestawie 72)
        (0, 6): 3,    # Chrome Yellow (3800/03)
        (0, 7): 801,  # Yellow Ochre (3800/801) - nie w zestawie 72
        
        # Row 2 (Oranges and Yellows)
        (1, 0): 28,   # Gold Ochre (3800/28)
        (1, 1): 555,  # Papaya Orange (3800/555)
        (1, 2): 556,  # Amber Orange (3800/556)
        (1, 3): 557,  # Tangerine Orange (3800/557)
        (1, 4): 45,   # Light Orange (3800/45)
        (1, 5): 44,   # Naples Yellow (3800/44)
        (1, 6): 42,   # Chromium Orange (3800/42)
        (1, 7): 558,  # Fire Orange (3800/558)
        
        # Row 3 (Oranges and Reds)
        (2, 0): 126,  # Persian Orange (3800/126) - nie w zestawie 72
        (2, 1): 5,    # Reddish Orange (3800/05)
        (2, 2): 559,  # Portland Orange (3800/559) - nie w zestawie 72
        (2, 3): 560,  # Dark Salmon Orange (3800/560) - nie w zestawie 72
        (2, 4): 6,    # Vermilion Red (3800/06)
        (2, 5): 600,  # Light Scarlet Red (3800/600) - nie w zestawie 72
        (2, 6): 76,   # Pyrrole Red (3800/170 w obrazku, ale 76 w zestawie 72)
        (2, 7): 606,  # Dark Vermilion Red (3800/606) - nie w zestawie 72
        
        # Row 4 (Reds and Pinks)
        (3, 0): 47,   # Scarlet Red (3800/601 w obrazku, ale 47 w zestawie 72)
        (3, 1): 602,  # Currant Red (3800/602) - nie w zestawie 72
        (3, 2): 7,    # Carmine Red (3800/132 w obrazku, ale 7 w zestawie 72)
        (3, 3): 603,  # Wine Red (3800/603) - nie w zestawie 72
        (3, 4): 605,  # Burgundy Red (3800/605) - nie w zestawie 72
        (3, 5): 653,  # Mexican Pink (3800/653) - nie w zestawie 72
        (3, 6): 131,  # French Pink (3800/131) - nie w zestawie 72
        (3, 7): 609,  # Antique Rose (3800/609) - nie w zestawie 72
        
        # Row 5 (Reds, Pinks, and Oranges)
        (4, 0): 604,  # Coral Red (3800/604) - nie w zestawie 72
        (4, 1): 610,  # Light Carmine Red (3800/610) - nie w zestawie 72
        (4, 2): 607,  # Punch Pink (3800/607) - nie w zestawie 72
        (4, 3): 608,  # Light French Pink (3800/608) - nie w zestawie 72
        (4, 4): 352,  # Blush Pink (3800/352) - tylko w Portrait
        (4, 5): 355,  # Peach Orange (3800/355) - tylko w Portrait
        (4, 6): 354,  # Salmon Pink (3800/354) - tylko w Portrait
        (4, 7): 9,    # Apricot Orange (3800/357 w obrazku, ale 9 w zestawie 72)
        
        # Row 6 (Browns, Skin Tones, and Pinks)
        (5, 0): 821,  # Almond Brown (3800/821)
        (5, 1): 553,  # Portrait Sand (3800/553)
        (5, 2): 350,  # Portrait Peach (3800/350)
        (5, 3): 554,  # Portrait Honey (3800/554)
        (5, 4): 552,  # Portrait Light (3800/552)
        (5, 5): 551,  # Portrait Fair (3800/551)
        (5, 6): 351,  # Light Portrait Pink (3800/351)
        (5, 7): 353,  # Amaranth Pink (3800/353)
    }
    
    # Obrazek 2: Fiolety, błękity, zielenie (6x8 = 48 kolorów)
    img2_mapping = {
        # Row 1 (Purples and Reds)
        (0, 0): 651,  # Orchid Purple (3800/651) - nie w zestawie 72
        (0, 1): 12,   # Reddish Violet (3800/178 w obrazku, ale 12 w zestawie 72)
        (0, 2): 654,  # Dark Reddish Violet (3800/654) - nie w zestawie 72
        (0, 3): 655,  # Byzantium Purple (3800/655) - nie w zestawie 72
        (0, 4): 177,  # Lilac Violet (3800/177) - nie w zestawie 72
        (0, 5): 8,    # Bordeaux Red (3800/08)
        (0, 6): 650,  # Fig Purple (3800/650) - nie w zestawie 72
        (0, 7): 51,   # Dark Violet (3800/182 w obrazku, ale 51 w zestawie 72)
        
        # Row 2 (Violets and Blues)
        (1, 0): 180,  # Dark Lavender Violet (3800/180) - nie w zestawie 72
        (1, 1): 11,   # Lavender Violet (3800/13 w obrazku, ale 11 w zestawie 72)
        (1, 2): 14,   # Bluish Violet (3800/179 w obrazku, ale 14 w zestawie 72)
        (1, 3): 50,   # Windsor Violet (3800/181 w obrazku, ale 50 w zestawie 72)
        (1, 4): 700,  # Midnight Blue (3800/700)
        (1, 5): 17,   # Cobalt Blue (3800/17)
        (1, 6): 56,   # Indigo Blue (3800/56)
        (1, 7): 55,   # Permanent Blue (3800/55)
        
        # Row 3 (Blues)
        (2, 0): 704,  # Navy Blue (3800/704)
        (2, 1): 19,   # Sapphire Blue (3800/19)
        (2, 2): 705,  # Sea Blue (3800/705)
        (2, 3): 54,   # Dark Cobalt Blue (3800/54)
        (2, 4): 701,  # Dark Azure Blue (3800/701)
        (2, 5): 53,   # Phthalo Blue (3800/53)
        (2, 6): 52,   # Dark Ice Blue (3800/52)
        (2, 7): 18,   # Light Blue (3800/18)
        
        # Row 4 (Blues and Teals)
        (3, 0): 20,   # Prussian Blue (3800/20)
        (3, 1): 57,   # Mountain Blue (3800/57)
        (3, 2): 52,   # Azure Blue (3800/702 w obrazku, ale 52 w zestawie 72)
        (3, 3): 16,   # Cerulean Blue (3800/16)
        (3, 4): 703,  # Dark Cerulean Blue (3800/703) - nie w zestawie 72
        (3, 5): 15,   # Ice Blue (3800/15)
        (3, 6): 752,  # Medium Turquoise (3800/752) - nie w zestawie 72
        (3, 7): 751,  # Teal Green (3800/751) - nie w zestawie 72
        
        # Row 5 (Teals and Greens)
        (4, 0): 750,  # Royal Teal (3800/750)
        (4, 1): 732,  # Teal Blue (3800/732)
        (4, 2): 731,  # Dark Teal Blue (3800/731)
        (4, 3): 772,  # Deep Green (3800/772)
        (4, 4): 26,   # Dark Green (3800/26)
        (4, 5): 775,  # Avocado Green (3800/775)
        (4, 6): 61,   # Sap Green (3800/61)
        (4, 7): 59,   # Grass Green (3800/59)
        
        # Row 6 (Greens)
        (5, 0): 60,   # Emerald Green (3800/60)
        (5, 1): 21,   # Bluish Green (3800/21)
        (5, 2): 770,  # Persian Green (3800/770)
        (5, 3): 771,  # Jade Green (3800/771)
        (5, 4): 774,  # Light Jade Green (3800/774)
        (5, 5): 773,  # Light Emerald Green (3800/773)
        (5, 6): 24,   # Pea Green (3800/24)
        (5, 7): 58,   # Light Green (3800/58)
    }
    
    # Obrazek 3: Zielenie, brązy, szarości (8x8 = 64 kolory)
    img3_mapping = {
        # Row 1 (Greens/Yellows)
        (0, 0): 23,   # Spring Green (3800/23)
        (0, 1): 22,   # Yellowish Green (3800/22)
        (0, 2): 502,  # Lime Yellow (3800/502)
        (0, 3): 503,  # Chartreuse Yellow (3800/503)
        (0, 4): 62,   # Apple Green (3800/62)
        (0, 5): 776,  # Celadon Green (3800/776)
        (0, 6): 25,   # Meadow Green (3800/25)
        (0, 7): 63,   # Light Olive Green (3800/63)
        
        # Row 2 (Greens/Browns/Ochres)
        (1, 0): 27,   # Dark Olive Green (3800/27)
        (1, 1): 66,   # Raw Umber (3800/66)
        (1, 2): 802,  # Dark Yellow Ochre (3800/802)
        (1, 3): 29,   # Light Ochre (3800/29)
        (1, 4): 800,  # Dark Gold Ochre (3800/800)
        (1, 5): 803,  # Yellow Brown Ochre (3800/803)
        (1, 6): 804,  # Brown Ochre (3800/804)
        (1, 7): 823,  # Sandstone Brown (3800/823)
        
        # Row 3 (Browns/Terracottas)
        (2, 0): 64,   # Burnt Ochre (3800/64)
        (2, 1): 824,  # Cinnamon Brown (3800/824)
        (2, 2): 825,  # Burnt Sienna (3800/825)
        (2, 3): 30,   # Reddish Brown (3800/30)
        (2, 4): 212,  # Caput Mortuum (3800/212)
        (2, 5): 65,   # Medium Terracotta (3800/65)
        (2, 6): 31,   # Light Brown (3800/31)
        (2, 7): 820,  # Hazelnut Brown (3800/820)
        
        # Row 4 (Browns/Metallics)
        (3, 0): 32,   # Natural Sienna (3800/32)
        (3, 1): 33,   # Dark Brown (3800/33)
        (3, 2): 822,  # Cafe Noir Brown (3800/822)
        (3, 3): 214,  # Dark Earth Brown (3800/214)
        (3, 4): 68,   # Burnt Umber (3800/68)
        (3, 5): 75,   # Standard Bronze (3800/75)
        (3, 6): 40,   # Standard Gold (3800/40)
        (3, 7): 39,   # Standard Silver (3800/39)
        
        # Row 5 (Cool Greys)
        (4, 0): 34,   # Light Bluish Grey (3800/34)
        (4, 1): 72,   # Slate Grey (3800/72)
        (4, 2): 71,   # Medium Grey (3800/71)
        (4, 3): 408,  # Cool Grey 8 (3800/408)
        (4, 4): 406,  # Cool Grey 6 (3800/406)
        (4, 5): 405,  # Cool Grey 5 (3800/405)
        (4, 6): 403,  # Cool Grey 3 (3800/403)
        (4, 7): 401,  # Cool Grey 1 (3800/401)
        
        # Row 6 (Warm Greys/Black)
        (5, 0): 451,  # Warm Grey 1 (3800/451)
        (5, 1): 452,  # Warm Grey 2 (3800/452)
        (5, 2): 453,  # Warm Grey 3 (3800/453)
        (5, 3): 455,  # Warm Grey 5 (3800/455)
        (5, 4): 456,  # Warm Grey 6 (3800/456)
        (5, 5): 458,  # Warm Grey 8 (3800/458)
        (5, 6): 36,   # Ivory Black (3800/36)
        (5, 7): 409,  # Cool Grey 9 (3800/409)
        
        # Row 7 i 8 - mogą być puste lub zawierać dodatkowe kolory
        # Na razie pomijam, bo nie mam pełnego opisu
    }
    
    # Ekstrahuj kolory z obrazka 1
    if os.path.exists("polycolor_3800_1.jpg"):
        img1 = Image.open("polycolor_3800_1.jpg").convert('RGB')
        for (row, col), num in img1_mapping.items():
            color = extract_color_from_grid(img1, row, col, rows=6, cols=8)
            if color:
                color_map[num] = color
    
    # Ekstrahuj kolory z obrazka 2
    if os.path.exists("polycolor_3800_2.jpg"):
        img2 = Image.open("polycolor_3800_2.jpg").convert('RGB')
        for (row, col), num in img2_mapping.items():
            color = extract_color_from_grid(img2, row, col, rows=6, cols=8)
            if color:
                color_map[num] = color
    
    # Ekstrahuj kolory z obrazka 3
    if os.path.exists("polycolor_3800_3.jpg"):
        img3 = Image.open("polycolor_3800_3.jpg").convert('RGB')
        for (row, col), num in img3_mapping.items():
            color = extract_color_from_grid(img3, row, col, rows=8, cols=8)
            if color:
                color_map[num] = color
    
    return color_map


if __name__ == "__main__":
    print("Ekstrakcja kolorów z obrazków katalogowych...")
    color_map = build_color_map_from_images()
    
    print(f"\nWyekstrahowano {len(color_map)} kolorów")
    print("\nPrzykładowe kolory:")
    for num in sorted(color_map.keys())[:10]:
        r, g, b = color_map[num]
        print(f"  {num}: RGB({r}, {g}, {b})")
    
    # Zapisz do pliku JSON
    with open("extracted_colors.json", "w") as f:
        json.dump(color_map, f, indent=2)
    print(f"\n✓ Zapisano do extracted_colors.json")

