#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator wzorników kolorów Koh-I-Noor Polycolor do wydruku na A4
Układ poziomy: nazwa -> numer 3800/nr -> kwadrat próbki
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white, black, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import math
import os

from colors_72 import COLORS_72
from colors_72_catalog import COLORS_72_CATALOG
from colors_144_catalog import COLORS_144_CATALOG
from colors_24_portrait import COLORS_24_PORTRAIT

# Polskie nazwy kolorów zgodne z nomenklaturą plastyczną
# Źródło prawdy: ZESTAW_72_KOLOROW.txt i ZRODLO_PRAWDY_144_KOLOROW.txt
# Uzupełnione dla wszystkich 72 kolorów i pełnego katalogu 144 kolorów
POLISH_NAMES = {
    1: "Biel tytanowa",
    2: "Żółć cytrynowa",
    3: "Żółć chromowa",
    5: "Pomarańcz czerwonawy",
    6: "Czerwień cynobrowa",
    7: "Czerwień karminowa",
    8: "Czerwień bordowa",
    9: "Pomarańcz morelowy",
    11: "Fiolet lawendowy",
    12: "Fiolet czerwonawy",
    14: "Fiolet niebieskawy",
    15: "Błękit lodowy",
    16: "Błękit ceruleum",
    17: "Błękit kobaltowy",
    18: "Błękit jasny",
    19: "Błękit szafirowy",
    20: "Błękit pruski",
    21: "Zieleń niebieskawa",
    22: "Zieleń żółtawa",
    23: "Zieleń wiosenna",
    24: "Zieleń groszkowa",
    25: "Zieleń łąkowa",
    26: "Zieleń ciemna",
    27: "Zieleń oliwkowa ciemna",
    28: "Ochra złota",
    29: "Ochra jasna",
    30: "Brąz czerwonawy",
    31: "Brąz jasny",
    32: "Siena naturalna",
    33: "Brąz ciemny",
    34: "Szarość niebieskawa jasna",
    36: "Czerń kości słoniowej",
    39: "Srebro standardowe",
    40: "Złoto standardowe",
    41: "Żółć bananowa",
    42: "Pomarańcz chromowy",
    44: "Żółć neapolitańska",
    45: "Pomarańcz jasny",
    47: "Czerwień szkarłatna",
    50: "Fiolet windsorski",
    51: "Fiolet ciemny",
    52: "Błękit lodowy ciemny",
    53: "Błękit ftalowy",
    54: "Błękit kobaltowy ciemny",
    55: "Błękit trwały",
    56: "Błękit indygo",
    57: "Błękit górski",
    58: "Zieleń jasna",
    59: "Zieleń trawiasta",
    60: "Zieleń szmaragdowa",
    61: "Zieleń sokowa",
    62: "Zieleń jabłkowa",
    63: "Zieleń oliwkowa jasna",
    64: "Ochra palona",
    65: "Terra cotta średnia",
    66: "Umbra surowa",
    68: "Umbra palona",
    71: "Szarość średnia",
    72: "Szarość łupkowa",
    75: "Brąz standardowy",
    76: "Czerwień pirolowa",
    126: "Pomarańcz perski",
    131: "Róż francuski",
    177: "Fiolet bzowy",
    180: "Fiolet lawendowy ciemny",
    212: "Caput mortuum",
    214: "Brąz ziemny ciemny",
    350: "Brzoskwinia portretowa",
    351: "Róż portretowy jasny",
    352: "Róż rumiany",
    353: "Róż amarantowy",
    354: "Róż łososiowy",
    355: "Pomarańcz brzoskwiniowy",
    401: "Szarość chłodna 1",
    403: "Szarość chłodna 3",
    405: "Szarość chłodna 5",
    406: "Szarość chłodna 6",
    408: "Szarość chłodna 8",
    409: "Szarość chłodna 9",
    451: "Szarość ciepła 1",
    452: "Szarość ciepła 2",
    453: "Szarość ciepła 3",
    455: "Szarość ciepła 5",
    456: "Szarość ciepła 6",
    458: "Szarość ciepła 8",
    500: "Kość słoniowa",
    501: "Żółć pyłkowa",
    502: "Żółć limonkowa",
    503: "Żółć chartreuse",
    550: "Złoto portretowe jasne",
    551: "Cera portretowa",
    552: "Jasność portretowa",
    553: "Piasek portretowy",
    554: "Miód portretowy",
    555: "Pomarańcz papajowy",
    556: "Pomarańcz bursztynowy",
    557: "Pomarańcz mandarynkowy",
    558: "Pomarańcz ognisty",
    559: "Pomarańcz portlandzki",
    560: "Pomarańcz łososiowy ciemny",
    600: "Czerwień szkarłatna jasna",
    602: "Czerwień porzeczkowa",
    603: "Czerwień winna",
    604: "Czerwień koralowa",
    605: "Czerwień burgundzka",
    606: "Czerwień cynobrowa ciemna",
    607: "Róż ponczowy",
    608: "Róż francuski jasny",
    609: "Róż antyczny",
    610: "Czerwień karminowa jasna",
    650: "Fiolet figowy",
    651: "Fiolet storczykowy",
    653: "Róż meksykański",
    654: "Fiolet czerwonawy ciemny",
    655: "Fiolet bizantyjski",
    700: "Błękit północny",
    701: "Błękit lazurowy ciemny",
    702: "Błękit lazurowy",
    703: "Błękit ceruleum ciemny",
    704: "Błękit morski",
    705: "Błękit morski",
    731: "Błękit morski ciemny",
    732: "Błękit morski",
    750: "Turkus królewski",
    751: "Zieleń morska",
    752: "Turkus średni",
    770: "Zieleń perska",
    771: "Zieleń jadeitowa",
    772: "Zieleń głęboka",
    773: "Zieleń szmaragdowa jasna",
    774: "Zieleń jadeitowa jasna",
    775: "Zieleń awokadowa",
    776: "Zieleń seledynowa",
    800: "Ochra złota ciemna",
    801: "Ochra żółta",
    802: "Ochra żółta ciemna",
    803: "Ochra żółto-brązowa",
    804: "Ochra brązowa",
    820: "Brąz orzechowy",
    821: "Brąz migdałowy",
    822: "Brąz kawowy",
    823: "Brąz piaskowcowy",
    824: "Brąz cynamonowy",
    825: "Siena palona",
}


def load_color_from_images(color_num):
    """
    Ładuje kolor z obrazków JPG na podstawie numeru kredki.
    Używa pliku JSON z wyekstrahowanymi kolorami z obrazków katalogowych.
    Zwraca kolor RGB jako tuple (r, g, b) lub None jeśli nie znaleziono.
    """
    json_file = "extracted_colors.json"
    if os.path.exists(json_file):
        try:
            import json
            with open(json_file, "r") as f:
                extracted_colors = json.load(f)
                # Konwertuj klucze na int (JSON zapisuje jako stringi)
                extracted_colors = {int(k): tuple(v) for k, v in extracted_colors.items()}
                if color_num in extracted_colors:
                    color = extracted_colors[color_num]
                    # Sprawdź czy to nie jest biały (prawdopodobnie błąd ekstrakcji)
                    if color != (255, 255, 255):
                        return color
        except Exception as e:
            pass  # Jeśli błąd, zwróć None
    
    return None


def get_color_from_name(color_name):
    """
    Próbuje uzyskać kolor RGB z nazwy koloru używając standardowych mapowań.
    Zwraca tuple (r, g, b) lub None jeśli nie znaleziono.
    """
    if not color_name:
        return None
    
    # Mapowanie specyficznych nazw Koh-I-Noor do standardowych nazw kolorów CSS/X11
    name_mapping = {
        "White": "white",
        "Banana Yellow": "yellow",
        "Lemon Yellow": "yellow",
        "Chrome Yellow": "gold",
        "Naples Yellow": "wheat",
        "Naples Yellow Light": "wheat",
        "Dark Yellow": "goldenrod",
        "Yellowish Orange": "orange",
        "Apricot Orange": "peachpuff",
        "Light Orange": "orange",
        "Reddish Orange": "orangered",
        "Chromium Orange": "darkorange",
        "Cadmium Orange": "orange",
        "Persian Pink": "pink",
        "Vermillion Red": "crimson",
        "Vermilion Red": "crimson",
        "Scarlet Red": "red",
        "Scarlet Red Dark": "darkred",
        "Carmine Red": "crimson",
        "Pyrrole Red": "red",
        "Bordeaux Red": "maroon",
        "Lavender Violet": "lavender",
        "Reddish Violet": "mediumorchid",
        "Light Violet": "lavender",
        "Bluish Violet": "blueviolet",
        "Permanent Violet": "mediumorchid",
        "Windsor Violet": "darkviolet",
        "Dark Violet": "darkviolet",
        "Ice Blue": "lightblue",
        "Cerulean Blue": "skyblue",
        "Cobalt Blue": "blue",
        "Light Blue": "lightblue",
        "Sapphire Blue": "blue",
        "Prussian Blue": "navy",
        "Azure Blue": "deepskyblue",
        "Phthalo Blue": "blue",
        "Cobalt Blue Dark": "darkblue",
        "Permanent Blue": "blue",
        "Indigo Blue": "indigo",
        "Mountain Blue": "steelblue",
        "Bluish Green": "turquoise",
        "Yellowish Green": "yellowgreen",
        "Spring Green": "springgreen",
        "Pea Green": "greenyellow",
        "Meadow Green": "limegreen",
        "Dark Green": "darkgreen",
        "Olive Green Dark": "olive",
        "Light Green": "lightgreen",
        "Grass Green": "green",
        "Emerald Green": "lime",
        "Sap Green": "green",
        "Apple Green": "greenyellow",
        "Olive Green Light": "olive",
        "Gold Ochre": "gold",
        "Light Ochre": "wheat",
        "Reddish Brown": "saddlebrown",
        "Light Brown": "peru",
        "Natural Sienna": "sienna",
        "Dark Brown": "saddlebrown",
        "Burnt Ochre": "darkgoldenrod",
        "Medium Terracotta": "chocolate",
        "Raw Umber": "saddlebrown",
        "Burnt Umber": "saddlebrown",
        "Bluish Grey Light": "lightsteelblue",
        "Platine Grey": "silver",
        "Ivory Black": "black",
        "Cold Grey": "gray",
        "Standard Silver": "silver",
        "Standard Gold": "gold",
        "Light Grey": "lightgray",
        "Dark Grey": "dimgray",
        "Medium Grey": "gray",
        "Slate Grey": "slategray",
        "Portrait Peach": "peachpuff",
        "Light Portrait Pink": "pink",
        "Blush Pink": "pink",
        "Amaranth Pink": "pink",
        "Salmon Pink": "salmon",
        "Peach Orange": "peachpuff",
    }
    
    # Najpierw sprawdź mapowanie specyficzne dla Koh-I-Noor
    standard_name = name_mapping.get(color_name)
    if standard_name:
        try:
            from PIL import ImageColor
            rgb = ImageColor.getrgb(standard_name)
            return rgb
        except:
            pass
    
    # Spróbuj bezpośrednio użyć nazwy jako standardowej nazwy koloru
    try:
        from PIL import ImageColor
        rgb = ImageColor.getrgb(color_name.lower())
        return rgb
    except:
        pass
    
    return None


def get_color_for_pencil(num, color_name=None):
    """
    Zwraca kolor RGB dla danej kredki na podstawie numeru.
    Używa tylko przybliżonych wartości RGB, które lepiej odzwierciedlają rzeczywiste kolory kredek.
    """
    # Użyj tylko przybliżonych wartości (mapowanie z nazw daje nieprawidłowe wyniki)
    # Kompletna mapa kolorów dla wszystkich kredek (przybliżone wartości RGB)
    color_map = {
        # Białe / neutralne
        1: (255, 255, 255),      # White
        
        # Żółcie
        2: (255, 250, 100),      # Lemon Yellow
        3: (255, 220, 50),       # Chrome Yellow
        4: (220, 180, 40),       # Dark Yellow
        41: (255, 237, 100),     # Banana Yellow
        43: (255, 245, 200),     # Naples Yellow Light
        44: (255, 235, 150),     # Naples Yellow
        
        # Pomarańcze
        5: (255, 120, 60),       # Reddish Orange
        9: (255, 200, 150),      # Apricot Orange
        42: (255, 140, 80),      # Chromium Orange
        45: (255, 180, 120),     # Light Orange
        46: (255, 130, 70),      # Cadmium Orange
        67: (255, 210, 130),     # Yellowish Orange
        
        # Czerwienie / róże
        6: (255, 60, 40),        # Vermillion Red
        7: (200, 20, 50),        # Carmine Red
        8: (120, 20, 40),        # Bordeaux Red
        10: (255, 180, 200),     # Persian Pink
        47: (220, 30, 50),       # Scarlet Red
        48: (180, 20, 30),       # Scarlet Red Dark
        76: (220, 40, 60),       # Pyrrole Red
        
        # Fiolety
        11: (220, 180, 240),     # Light Violet
        12: (200, 120, 200),     # Reddish Violet
        13: (150, 80, 180),      # Medium Violet
        14: (120, 100, 200),     # Bluish Violet
        49: (120, 80, 150),      # Permanent Violet
        50: (100, 60, 140),      # Windsor Violet
        51: (80, 40, 100),       # Dark Violet
        
        # Błękity
        15: (200, 240, 255),     # Ice Blue
        16: (100, 180, 220),     # Cerulean Blue
        17: (50, 120, 200),      # Cobalt Blue
        18: (150, 200, 255),     # Light Blue
        19: (30, 80, 150),       # Sapphire Blue
        20: (20, 40, 100),       # Prussian Blue
        52: (80, 160, 240),      # Azure Blue
        53: (30, 100, 180),      # Phthalo Blue
        54: (40, 90, 160),       # Cobalt Blue Dark
        55: (60, 140, 220),      # Permanent Blue
        56: (40, 60, 140),       # Indigo Blue
        57: (100, 180, 240),     # Mountain Blue
        
        # Zieleń
        21: (60, 180, 160),      # Bluish Green
        22: (180, 240, 100),     # Yellowish Green
        23: (120, 240, 180),     # Spring Green
        24: (140, 200, 80),      # Pea Green
        25: (100, 200, 120),     # Meadow Green
        26: (20, 100, 60),       # Dark Green
        27: (100, 120, 60),      # Olive Green Dark
        58: (160, 240, 160),      # Light Green
        59: (80, 200, 100),      # Grass Green
        60: (40, 220, 120),      # Emerald Green
        61: (100, 180, 80),       # Sap Green
        62: (120, 220, 100),      # Apple Green
        63: (180, 200, 140),      # Olive Green Light
        
        # Brązy / ochry
        28: (220, 180, 100),     # Gold Ochre
        29: (220, 200, 140),     # Light Ochre
        30: (150, 80, 60),       # Reddish Brown
        31: (180, 150, 120),     # Light Brown
        32: (180, 140, 100),     # Natural Sienna
        33: (80, 50, 40),        # Dark Brown
        64: (180, 120, 80),      # Burnt Ochre
        65: (180, 100, 80),      # Medium Terracotta
        66: (120, 100, 80),      # Raw Umber
        68: (100, 70, 50),       # Burnt Umber
        
        # Szarości / czernie / metaliczne
        34: (180, 200, 220),     # Bluish Grey Light
        35: (200, 200, 200),     # Platine Grey
        36: (20, 20, 20),        # Ivory Black
        38: (140, 150, 160),     # Cold Grey
        39: (180, 180, 180),     # Standard Silver
        40: (220, 180, 80),      # Standard Gold
        69: (200, 200, 200),     # Light Grey
        70: (100, 100, 100),     # Dark Grey
        71: (150, 150, 150),     # Medium Grey
        72: (120, 120, 130),     # Slate Grey
        
        # Zestaw Portrait (dodatkowe kolory)
        350: (255, 220, 200),    # Portrait Peach
        351: (255, 230, 230),    # Light Portrait Pink
        352: (255, 200, 220),    # Blush Pink
        353: (240, 180, 200),    # Amaranth Pink
        354: (255, 180, 160),    # Salmon Pink
        355: (255, 200, 170),    # Peach Orange
        
        # Dodatkowe kolory z katalogu 144 - żółcie/beże
        500: (255, 250, 240),    # Ivory Bone
        550: (255, 245, 220),    # Fair Portrait Gold
        501: (255, 248, 200),    # Pollen Yellow
        801: (240, 220, 160),    # Yellow Ochre
        
        # Dodatkowe pomarańcze
        555: (255, 200, 140),    # Papaya Orange
        556: (255, 180, 100),    # Amber Orange
        557: (255, 160, 80),     # Tangerine Orange
        558: (255, 100, 40),     # Fire Orange
        126: (255, 140, 90),     # Persian Orange
        559: (255, 150, 100),    # Portland Orange
        560: (220, 120, 100),    # Dark Salmon Orange
        
        # Dodatkowe czerwienie/róże
        600: (255, 100, 80),     # Light Scarlet Red
        606: (200, 40, 30),      # Dark Vermilion Red
        602: (180, 30, 50),      # Currant Red
        603: (140, 20, 40),      # Wine Red
        605: (100, 10, 30),      # Burgundy Red
        653: (255, 50, 150),     # Mexican Pink
        131: (255, 150, 180),    # French Pink
        609: (220, 150, 160),    # Antique Rose
        604: (255, 120, 100),    # Coral Red
        610: (240, 100, 120),    # Light Carmine Red
        607: (255, 130, 160),    # Punch Pink
        608: (255, 200, 210),    # Light French Pink
        
        # Dodatkowe fiolety
        651: (230, 180, 240),    # Orchid Purple
        654: (140, 60, 120),     # Dark Reddish Violet
        655: (120, 40, 100),     # Byzantium Purple
        177: (200, 160, 220),    # Lilac Violet
        650: (80, 30, 60),       # Fig Purple
        180: (150, 100, 160),    # Dark Lavender Violet
        
        # Dodatkowe błękity
        700: (10, 20, 60),       # Midnight Blue
        704: (20, 30, 80),       # Navy Blue
        705: (40, 100, 160),     # Sea Blue
        701: (30, 80, 140),      # Dark Azure Blue
        703: (20, 100, 150),     # Dark Cerulean Blue
        752: (50, 180, 200),     # Medium Turquoise
        751: (30, 140, 160),     # Teal Green
        
        # Dodatkowe zielenie/teale
        750: (20, 120, 140),     # Royal Teal
        732: (40, 160, 180),     # Teal Blue
        731: (20, 100, 120),     # Dark Teal Blue
        772: (10, 80, 60),       # Deep Green
        775: (140, 180, 100),    # Avocado Green
        770: (30, 180, 160),     # Persian Green
        771: (50, 160, 120),     # Jade Green
        774: (120, 200, 160),    # Light Jade Green
        773: (80, 240, 140),     # Light Emerald Green
        
        # Dodatkowe zielenie/żółcie
        502: (200, 255, 100),    # Lime Yellow
        503: (180, 255, 80),     # Chartreuse Yellow
        776: (180, 200, 160),    # Celadon Green
        
        # Dodatkowe brązy/ochry
        802: (200, 160, 100),    # Dark Yellow Ochre
        800: (200, 150, 80),     # Dark Gold Ochre
        803: (180, 140, 100),    # Yellow Brown Ochre
        804: (160, 120, 80),     # Brown Ochre
        823: (180, 140, 120),    # Sandstone Brown
        824: (180, 100, 80),     # Cinnamon Brown
        825: (160, 80, 60),      # Burnt Sienna
        212: (100, 50, 60),      # Caput Mortuum
        820: (140, 100, 80),     # Hazelnut Brown
        822: (60, 40, 30),       # Cafe Noir Brown
        214: (80, 60, 50),       # Dark Earth Brown
        821: (200, 180, 160),    # Almond Brown
        
        # Dodatkowe portretowe/skóry
        553: (240, 220, 200),    # Portrait Sand
        554: (240, 200, 160),    # Portrait Honey
        552: (250, 240, 230),    # Portrait Light
        551: (255, 245, 235),    # Portrait Fair
        
        # Dodatkowe szarości
        408: (60, 60, 70),       # Cool Grey 8
        406: (100, 100, 110),    # Cool Grey 6
        405: (120, 120, 130),    # Cool Grey 5
        403: (180, 180, 190),    # Cool Grey 3
        401: (230, 230, 240),    # Cool Grey 1
        451: (240, 235, 230),    # Warm Grey 1
        452: (220, 215, 210),    # Warm Grey 2
        453: (200, 195, 190),    # Warm Grey 3
        455: (160, 155, 150),    # Warm Grey 5
        456: (140, 135, 130),    # Warm Grey 6
        458: (100, 95, 90),      # Warm Grey 8
        409: (40, 40, 50),       # Cool Grey 9
        
        # Dodatkowe metaliczne
        75: (180, 140, 100),     # Standard Bronze
    }
    
    return color_map.get(num, (255, 255, 255))  # Domyślnie biały


def generate_swatch_pdf(colors, output_filename, title="Koh-I-Noor Polycolor"):
    """
    Generuje PDF z wzornikami kolorów w układzie poziomym (landscape)
    
    Args:
        colors: lista krotek (numer, nazwa)
        output_filename: nazwa pliku PDF
        title: tytuł dokumentu
    """
    # Wymiary A4 w orientacji poziomej
    page_width, page_height = landscape(A4)
    
    # Marginesy
    margin_x = 15 * mm
    margin_y = 20 * mm
    
    # Wymiary kwadratu próbki
    swatch_size = 22 * mm
    
    # Odstępy między elementami
    spacing_x = 6 * mm  # poziomy odstęp między kolumnami
    spacing_y = 4 * mm  # pionowy odstęp między wierszami
    
    # Liczba kolumn (w orientacji poziomej - więcej kolumn)
    cols = 8
    
    # Oblicz szerokość kolumny
    usable_width = page_width - 2 * margin_x
    col_width = (usable_width - (cols - 1) * spacing_x) / cols
    
    # Wysokość jednego elementu (nazwa + numer + kwadrat + odstępy)
    name_height = 4.5 * mm
    num_height = 4 * mm
    element_height = name_height + num_height + swatch_size + spacing_y
    
    # Liczba wierszy na stronę (w orientacji poziomej mamy więcej miejsca na szerokość, mniej na wysokość)
    rows_per_page = int((page_height - 2 * margin_y - 30 * mm) / element_height)
    
    c = canvas.Canvas(output_filename, pagesize=landscape(A4))
    
    page_num = 0
    row = 0
    col = 0
    
    def draw_page_header(page_number):
        """Rysuje nagłówek strony"""
        if page_number == 0:
            # Tytuł tylko na pierwszej stronie - użyj czcionki Unicode - pogrubiony
            try:
                c.setFont("UnicodeFont-Bold", 20)  # Zmniejszony z 22 do 20
            except:
                c.setFont("Helvetica-Bold", 20)  # Zmniejszony z 22 do 20
            c.drawString(margin_x, page_height - margin_y - 8 * mm, title)
            try:
                c.setFont("UnicodeFont", 11)
            except:
                c.setFont("Helvetica", 11)
            c.drawString(margin_x, page_height - margin_y - 14 * mm, f"Zestaw {len(colors)} kolorów - Wzornik do próbek")
            # Linia pod tytułem
            c.setLineWidth(0.5)
            c.line(margin_x, page_height - margin_y - 17 * mm, page_width - margin_x, page_height - margin_y - 17 * mm)
            return page_height - margin_y - 22 * mm
        else:
            # Numer strony na kolejnych stronach
            c.setFont("Helvetica", 9)
            c.drawRightString(page_width - margin_x, page_height - margin_y - 5 * mm, f"Strona {page_number + 1}")
            return page_height - margin_y - 10 * mm
    
    # Rysuj nagłówek pierwszej strony
    start_y = draw_page_header(page_num)
    
    for num, name in colors:
        # Sprawdź czy potrzebna nowa strona
        if row >= rows_per_page:
            c.showPage()
            page_num += 1
            row = 0
            col = 0
            start_y = draw_page_header(page_num)
        
        # Oblicz pozycję (wyśrodkowane w kolumnie)
        col_center_x = margin_x + col * (col_width + spacing_x) + col_width / 2
        y = start_y - row * element_height
        
        # 1. Nazwa koloru angielska (na górze, wyśrodkowana)
        c.setFont("Helvetica", 9)
        c.setFillColor(black)
        # Skróć nazwę jeśli za długa
        name_text = name
        if len(name_text) > 20:
            name_text = name_text[:17] + "..."
        # Wyśrodkuj tekst
        text_width = c.stringWidth(name_text, "Helvetica", 9)
        c.drawString(col_center_x - text_width / 2, y, name_text)
        
        # 1b. Polska nazwa koloru (pod angielską, wyśrodkowana, mniejsza czcionka)
        polish_name = POLISH_NAMES.get(num, "")
        if polish_name:
            try:
                c.setFont("UnicodeFont", 7)
                font_name = "UnicodeFont"
            except:
                c.setFont("Helvetica", 7)
                font_name = "Helvetica"
            c.setFillColor(black)
            # Skróć polską nazwę jeśli za długa
            polish_text = polish_name
            if len(polish_text) > 22:
                polish_text = polish_text[:19] + "..."
            polish_text_width = c.stringWidth(polish_text, font_name, 7)
            c.drawString(col_center_x - polish_text_width / 2, y - 3.5 * mm, polish_text)
        
        # 2. Numer w formacie 3800/nr (pod nazwą, wyśrodkowany)
        c.setFont("Helvetica-Bold", 10)
        num_text = f"3800/{num:02d}"  # Zera wiodące: 3800/01, 3800/02, etc.
        text_width = c.stringWidth(num_text, "Helvetica-Bold", 10)
        # Jeśli jest polska nazwa, przesuń numer niżej
        num_y_offset = 3.5 * mm if polish_name else 0
        c.drawString(col_center_x - text_width / 2, y - num_height - num_y_offset, num_text)
        
        # 3. Kwadrat próbki (na dole, wyśrodkowany)
        swatch_x = col_center_x - swatch_size / 2
        swatch_y = y - num_height - swatch_size - 1 * mm
        
        # Ramka kwadratu (ciemniejsza)
        c.setStrokeColor(black)
        c.setLineWidth(1.2)
        c.setFillColor(white)
        c.rect(swatch_x, swatch_y, swatch_size, swatch_size, fill=1, stroke=1)
        
        # Przejdź do następnej kolumny
        col += 1
        if col >= cols:
            col = 0
            row += 1
    
    # Dodaj numer strony na pierwszej stronie (jeśli była tylko jedna)
    if page_num == 0:
        c.setFont("Helvetica", 9)
        c.drawRightString(page_width - margin_x, margin_y - 5 * mm, "Strona 1")
    
    c.save()
    print(f"✓ Wygenerowano: {output_filename}")


def generate_portrait_variant1_single_row(colors, output_filename, title="Koh-I-Noor Polycolor 24 Portrait"):
    """
    Wariant 1: Jeden rząd kredek z pionowymi napisami (kompaktowy)
    Odwzorowuje układ kredek obok siebie - kredki 9mm, odstęp 1mm
    Obsługuje wiele stron - automatycznie dzieli na strony po 24 kredki
    """
    page_width, page_height = landscape(A4)
    
    num_colors = len(colors)
    swatch_width = 9 * mm  # szerokość jak kredki
    sample_size = 9 * mm  # kwadracik próbki na dole
    swatch_height = 80 * mm + sample_size  # 80mm górna część + 9mm kwadracik = 89mm
    spacing = 1 * mm  # dokładnie 1mm odstęp
    
    # Maksymalna liczba kredek na stronę (24)
    colors_per_page = 24
    
    # Oblicz ile stron potrzeba
    num_pages = (num_colors + colors_per_page - 1) // colors_per_page
    
    c = canvas.Canvas(output_filename, pagesize=landscape(A4))
    
    # Globalny numer porządkowy (kontynuuje przez wszystkie strony)
    global_order_num = 0
    
    for page_num in range(num_pages):
        # Przejdź do nowej strony (oprócz pierwszej)
        if page_num > 0:
            c.showPage()
        
        # Kolory dla tej strony
        start_idx = page_num * colors_per_page
        end_idx = min(start_idx + colors_per_page, num_colors)
        page_colors = colors[start_idx:end_idx]
        num_colors_on_page = len(page_colors)
        
        # Oblicz całkowitą szerokość potrzebną dla tej strony
        total_width = num_colors_on_page * swatch_width + (num_colors_on_page - 1) * spacing
        
        # Wyśrodkuj na stronie
        margin_x = (page_width - total_width) / 2
        margin_y = 20 * mm
        
        # Tytuł - zgodnie z brandingiem KOH-I-NOOR (wersaliki) - pogrubiony
        # Użyj czcionki Unicode jeśli dostępna, w przeciwnym razie Helvetica-Bold
        try:
            c.setFont("UnicodeFont-Bold", 18)  # Zmniejszony z 20 do 18
            title_font = "UnicodeFont-Bold"
        except:
            c.setFont("Helvetica-Bold", 18)  # Zmniejszony z 20 do 18
            title_font = "Helvetica-Bold"
        # Tytuł już jest w wersalikach z main(), ale upewnijmy się
        branded_title = title.upper()
        if num_pages > 1:
            branded_title += f" - Strona {page_num + 1}/{num_pages}"
        c.drawString(margin_x, page_height - margin_y - 8 * mm, branded_title)
        c.setLineWidth(0.5)
        c.line(margin_x, page_height - margin_y - 11 * mm, page_width - margin_x, page_height - margin_y - 11 * mm)
        
        # Pozycja startowa - przesunięta w dół strony
        header_height = 20 * mm
        available_height = page_height - 2 * margin_y - header_height
        
        # Wysokości elementów
        name_text_max_height = 25 * mm  # maksymalna wysokość nazwy (szerokość po obrocie) - więcej miejsca na 2 nazwy
        num_text_max_height = 15 * mm  # maksymalna wysokość numeru (szerokość po obrocie)
        swatch_size_val = swatch_height  # wysokość kredki
        
        # Całkowita wysokość potrzebna na jeden element
        total_element_height = name_text_max_height + swatch_size_val + num_text_max_height + 8 * mm  # odstępy
        
        # Przesunięcie w dół - około 6cm niżej
        center_y = margin_y + header_height + (available_height * 0.4) - 20 * mm + 60 * mm
        
        # Pozycja kwadratów (przesunięte w dół)
        swatch_y = center_y - num_text_max_height - swatch_size_val
        
        start_x = margin_x
        
        for idx, (num, name) in enumerate(page_colors):
            x = start_x + idx * (swatch_width + spacing)
            center_x = x + swatch_width / 2
            global_order_num += 1
            order_num = global_order_num  # numer porządkowy kontynuuje przez wszystkie strony
            
            # 1. Nazwa koloru po angielsku (pionowo, obrócona o 90 stopni, na górze, po lewej)
            c.setFont("Helvetica", 8)
            c.setFillColor(black)
            name_text = str(name)
            
            # Skróć nazwę jeśli za długa
            if len(name_text) > 20:
                name_text = name_text[:18] + "..."
            
            # Pozycja dla obróconego tekstu angielskiego - najwyżej, po lewej stronie (mniejsze przesunięcie)
            name_text_width = c.stringWidth(name_text, "Helvetica", 8)
            name_text_x = center_x - 1.5 * mm  # mniejsze przesunięcie w lewo, żeby nie nachodziło na sąsiednią kredkę
            name_text_y = swatch_y + swatch_height + 10 * mm + name_text_width / 2  # na górze
            
            c.saveState()
            c.setFillColor(black)
            c.translate(name_text_x, name_text_y)
            c.rotate(90)
            c.drawString(-name_text_width / 2, 0, name_text)
            c.restoreState()
            
            # 1b. Polska nazwa koloru (pionowo, obrócona o 90 stopni, obok angielskiej, po prawej)
            polish_name = POLISH_NAMES.get(num, "")
            if polish_name:
                # Użyj czcionki Unicode jeśli dostępna, w przeciwnym razie Helvetica
                try:
                    font_name = "UnicodeFont"
                    c.setFont(font_name, 7)
                except:
                    font_name = "Helvetica"
                    c.setFont(font_name, 7)
                c.setFillColor(black)
                # NIE SKRACAJ polskich nazw - wyświetlaj w całości
                
                polish_text_width = c.stringWidth(polish_name, font_name, 7)
                polish_text_x = center_x + 1.5 * mm  # mniejsze przesunięcie w prawo, żeby nie nachodziło na sąsiednią kredkę
                # Ta sama wysokość co angielska nazwa
                polish_text_y = swatch_y + swatch_height + 10 * mm + polish_text_width / 2  # na tej samej wysokości co angielska
                
                c.saveState()
                c.setFillColor(black)
                c.translate(polish_text_x, polish_text_y)
                c.rotate(90)
                c.drawString(-polish_text_width / 2, 0, polish_name)
                c.restoreState()
            
            # 3. Kredka próbki (prostokąt jak kredka) - 9mm szerokość, 75mm wysokość
            # Główny prostokąt kredki - pusty, do wypełnienia kredką
            c.setStrokeColor(black)
            c.setLineWidth(1.2)
            c.setFillColor(white)
            corner_radius = 1 * mm
            c.roundRect(x, swatch_y, swatch_width, swatch_height, corner_radius, fill=1, stroke=1)
            
            # Mały kwadracik 9x9mm z kolorem próbki - na dole prostokąta
            color_rgb = get_color_for_pencil(num, name)
            color = HexColor(f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
            
            # Kwadracik na dole - 9mm x 9mm
            sample_y = swatch_y  # na samym dole prostokąta
            c.setFillColor(color)
            c.setStrokeColor(black)
            c.setLineWidth(1.0)
            c.roundRect(x, sample_y, swatch_width, sample_size, corner_radius, fill=1, stroke=1)
            
            # 4. Numer porządkowy (poziomy, tuż pod kredką)
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(black)
            order_text = str(order_num)
            order_text_width = c.stringWidth(order_text, "Helvetica-Bold", 9)
            c.drawString(center_x - order_text_width / 2, swatch_y - 4 * mm, order_text)
            
            # 5. Numer 3800/nr (pionowo, obrócona o 90 stopni, na dole)
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(black)
            num_text = f"3800/{num:02d}"  # Zera wiodące: 3800/01, 3800/02, etc.
            
            # Pozycja dla obróconego numeru - na dole, wyśrodkowany
            num_text_width = c.stringWidth(num_text, "Helvetica-Bold", 8)
            num_text_x = center_x
            num_text_y = swatch_y - 8 * mm - num_text_width / 2  # jeszcze niżej, pod numerem porządkowym
            
            c.saveState()
            c.setFillColor(black)
            c.translate(num_text_x, num_text_y)
            c.rotate(90)
            c.drawString(-num_text_width / 2, 0, num_text)
            c.restoreState()
    
    c.save()
    print(f"✓ Wygenerowano: {output_filename} ({num_pages} stron)")


def generate_portrait_variant2_two_rows(colors, output_filename, title="Koh-I-Noor Polycolor 24 Portrait"):
    """
    Wariant 2: Dwa rzędy po 12 kredek (bardziej czytelny)
    """
    page_width, page_height = landscape(A4)
    
    margin_x = 12 * mm
    margin_y = 20 * mm
    
    num_colors = len(colors)
    colors_per_row = num_colors // 2  # 12 kredek w każdym rzędzie
    
    usable_width = page_width - 2 * margin_x
    spacing = 4 * mm
    
    # Oblicz rozmiar kwadratu dla 12 kredek
    swatch_size = (usable_width - (colors_per_row - 1) * spacing) / colors_per_row
    
    # Wysokość elementu
    name_height = 4.5 * mm
    num_height = 4 * mm
    element_height = name_height + num_height + swatch_size + 3 * mm
    
    # Odstęp między rzędami
    row_spacing = 18 * mm
    
    c = canvas.Canvas(output_filename, pagesize=landscape(A4))
    
    # Tytuł - użyj czcionki Unicode - pogrubiony
    try:
        c.setFont("UnicodeFont-Bold", 18)  # Zmniejszony z 20 do 18
    except:
        c.setFont("Helvetica-Bold", 18)  # Zmniejszony z 20 do 18
    c.drawString(margin_x, page_height - margin_y - 8 * mm, title)
    try:
        c.setFont("UnicodeFont", 10)
    except:
        c.setFont("Helvetica", 10)
    c.drawString(margin_x, page_height - margin_y - 14 * mm, "Wariant 2: Dwa rzędy po 12 kredek - czytelny układ")
    c.setLineWidth(0.5)
    c.line(margin_x, page_height - margin_y - 17 * mm, page_width - margin_x, page_height - margin_y - 17 * mm)
    
    # Pozycja startowa - wyśrodkowana
    header_height = 25 * mm
    available_height = page_height - 2 * margin_y - header_height
    total_rows_height = 2 * element_height + row_spacing
    start_y = page_height - margin_y - header_height - (available_height - total_rows_height) / 2
    
    for idx, (num, name) in enumerate(colors):
        row = idx // colors_per_row  # 0 lub 1
        col = idx % colors_per_row   # 0-11
        
        x = margin_x + col * (swatch_size + spacing)
        center_x = x + swatch_size / 2
        y = start_y - row * (element_height + row_spacing)
        
        # 1. Nazwa koloru angielska (na górze, wyśrodkowana)
        c.setFont("Helvetica", 9)
        c.setFillColor(black)
        name_text = name
        if len(name_text) > 22:
            name_text = name_text[:19] + "..."
        text_width = c.stringWidth(name_text, "Helvetica", 9)
        c.drawString(center_x - text_width / 2, y, name_text)
        
        # 1b. Polska nazwa koloru (pod angielską, wyśrodkowana, mniejsza czcionka)
        polish_name = POLISH_NAMES.get(num, "")
        if polish_name:
            try:
                c.setFont("UnicodeFont", 7)
                font_name = "UnicodeFont"
            except:
                c.setFont("Helvetica", 7)
                font_name = "Helvetica"
            c.setFillColor(black)
            polish_text = polish_name
            if len(polish_text) > 24:
                polish_text = polish_text[:21] + "..."
            polish_text_width = c.stringWidth(polish_text, font_name, 7)
            c.drawString(center_x - polish_text_width / 2, y - 3.5 * mm, polish_text)
        
        # 2. Numer 3800/nr (pod nazwą, wyśrodkowany)
        c.setFont("Helvetica-Bold", 10)
        num_text = f"3800/{num:02d}"  # Zera wiodące: 3800/01, 3800/02, etc.
        text_width = c.stringWidth(num_text, "Helvetica-Bold", 10)
        # Jeśli jest polska nazwa, przesuń numer niżej
        num_y_offset = 3.5 * mm if polish_name else 0
        c.drawString(center_x - text_width / 2, y - num_height - num_y_offset, num_text)
        
        # 3. Kwadrat próbki (na dole, wyśrodkowany)
        swatch_x = center_x - swatch_size / 2
        swatch_y = y - num_height - swatch_size - 2 * mm
        
        c.setStrokeColor(black)
        c.setLineWidth(1.2)
        c.setFillColor(white)
        c.rect(swatch_x, swatch_y, swatch_size, swatch_size, fill=1, stroke=1)
    
    # Numer strony
    c.setFont("Helvetica", 9)
    c.drawRightString(page_width - margin_x, margin_y - 5 * mm, "Strona 1")
    
    c.save()
    print(f"✓ Wygenerowano: {output_filename}")


def register_unicode_font():
    """Rejestruje czcionkę TrueType z obsługą polskich znaków"""
    # Próbuj zarejestrować systemową czcionkę obsługującą Unicode
    font_paths = [
        # macOS - Arial (dobra obsługa Unicode)
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        # Windows
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialuni.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('UnicodeFont', font_path))
                pdfmetrics.registerFont(TTFont('UnicodeFont-Bold', font_path))
                print(f"✓ Zarejestrowano czcionkę Unicode: {os.path.basename(font_path)}")
                return True
            except Exception as e:
                print(f"  Próba {font_path}: {e}")
                continue
    
    print("⚠ Nie znaleziono czcionki Unicode - polskie znaki mogą się nie wyświetlać poprawnie")
    return False


def main():
    """Główna funkcja generująca oba wzorniki"""
    
    # Zarejestruj czcionkę Unicode
    has_unicode = register_unicode_font()
    
    print("Generowanie wzorników Koh-I-Noor Polycolor...")
    print()
    
    # Generuj wzornik dla zestawu 72 - KOLEJNOŚĆ TONALNA
    print(f"Zestaw 72 kolorów - TONALNY ({len(COLORS_72)} kolorów)...")
    generate_portrait_variant1_single_row(
        COLORS_72,
        "Koh-I-Noor_Polycolor_72_TONALNY.pdf",
        "KOH-I-NOOR POLYCOLOR 72 - KOLEJNOŚĆ TONALNA"
    )
    
    print()
    
    # Generuj wzornik dla zestawu 72 - KOLEJNOŚĆ KATALOGOWA
    print(f"Zestaw 72 kolorów - KATALOGOWY ({len(COLORS_72_CATALOG)} kolorów)...")
    generate_portrait_variant1_single_row(
        COLORS_72_CATALOG,
        "Koh-I-Noor_Polycolor_72_KATALOGOWY.pdf",
        "KOH-I-NOOR POLYCOLOR 72 - KOLEJNOŚĆ KATALOGOWA"
    )
    
    print()
    
    # Generuj wzornik dla pełnego katalogu 144 kolorów - KOLEJNOŚĆ KATALOGOWA
    print(f"Pełny katalog 144 kolorów - KATALOGOWY ({len(COLORS_144_CATALOG)} kolorów)...")
    generate_portrait_variant1_single_row(
        COLORS_144_CATALOG,
        "Koh-I-Noor_Polycolor_144_KATALOGOWY.pdf",
        "KOH-I-NOOR POLYCOLOR 144 - KOLEJNOŚĆ KATALOGOWA"
    )
    
    print()
    
    # Generuj wariant 1: Jeden rząd 24 kredek - KOLEJNOŚĆ TONALNA
    print(f"Zestaw 24 Portrait - Wariant 1 TONALNY (jeden rząd, pionowe napisy)...")
    generate_portrait_variant1_single_row(
        COLORS_24_PORTRAIT,
        "Koh-I-Noor_Polycolor_24_Portrait_TONALNY.pdf",
        "KOH-I-NOOR POLYCOLOR 24 PORTRAIT (3824) - KOLEJNOŚĆ TONALNA"
    )
    
    # Generuj wariant 1: Jeden rząd 24 kredek - KOLEJNOŚĆ Z PUDEŁKA (z fizycznego pudełka)
    print(f"Zestaw 24 Portrait - Wariant 1 Z PUDEŁKA (jeden rząd, pionowe napisy)...")
    # Kolejność z fizycznego pudełka (od lewej do prawej) - faktyczna kolejność w pudełku
    # Zaktualizowane numery zgodnie ze źródłem prawdy: 43->501, 10->131, 48->7, 49->50
    box_order_from_photo = [1, 41, 501, 44, 29, 9, 131, 353, 351, 355, 354, 352, 350, 30, 7, 64, 65, 31, 68, 33, 50, 16, 63, 66]
    color_map = {num: (num, name) for num, name in COLORS_24_PORTRAIT}
    colors_box_order = [color_map[num] for num in box_order_from_photo if num in color_map]
    generate_portrait_variant1_single_row(
        colors_box_order,
        "Koh-I-Noor_Polycolor_24_Portrait_Z_PUDELKA.pdf",
        "KOH-I-NOOR POLYCOLOR 24 PORTRAIT (3824) - KOLEJNOŚĆ Z PUDEŁKA"
    )
    
    print()
    print("✓ Gotowe! Wszystkie pliki PDF są gotowe do wydruku na A4 (orientacja pozioma).")


if __name__ == "__main__":
    main()

