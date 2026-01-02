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
import cv2
import numpy as np

from colors_72 import COLORS_72
from colors_72_catalog import COLORS_72_CATALOG
from colors_144_catalog import COLORS_144_CATALOG
from colors_24_portrait import COLORS_24_PORTRAIT
try:
    from colors_72_2017 import COLORS_72_2017
except ImportError:
    COLORS_72_2017 = []
try:
    from colors_my_72 import COLORS_MY_72
except ImportError:
    COLORS_MY_72 = []

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
        504: "Żółć cytrynowa",
        555: "Pomarańcz papajowy",
        556: "Pomarańcz bursztynowy",
        557: "Pomarańcz mandarynkowy",
        558: "Pomarańcz ognisty",
        559: "Pomarańcz portlandzki",
        560: "Pomarańcz łososiowy ciemny",
        357: "Pomarańcz morelowy",
        600: "Czerwień szkarłatna jasna",
        601: "Czerwień szkarłatna",
        602: "Czerwień porzeczkowa",
        603: "Czerwień winna",
        604: "Czerwień koralowa",
        605: "Czerwień burgundzka",
        606: "Czerwień cynobrowa ciemna",
        607: "Róż ponczowy",
        608: "Róż francuski jasny",
        609: "Róż antyczny",
        610: "Czerwień karminowa jasna",
        132: "Czerwień karminowa",
        170: "Czerwień pirolowa",
        13: "Fiolet lawendowy",
        178: "Fiolet czerwonawy",
        179: "Fiolet niebieskawy",
        181: "Fiolet windsorski",
        182: "Fiolet ciemny",
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
        # Białe / neutralne - znormalizowane względem białego
        1: (187, 174, 104),      # White - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        
        # Żółcie - poprawione wartości RGB dla lepszej wierności kolorów
        2: (255, 250, 100),      # Lemon Yellow
        3: (187, 181, 122),      # Chrome Yellow - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        4: (220, 180, 40),       # Dark Yellow
        41: (190, 179, 81),      # Banana Yellow - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        43: (255, 245, 200),     # Naples Yellow Light
        44: (186, 149, 114),     # Naples Yellow - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        
        # Pomarańcze - poprawione wartości RGB
        5: (191, 145, 83),        # Reddish Orange - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        9: (255, 200, 150),      # Apricot Orange
        42: (183, 135, 76),       # Chromium Orange - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        45: (184, 144, 104),      # Light Orange - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        46: (255, 130, 70),      # Cadmium Orange
        67: (255, 210, 130),     # Yellowish Orange
        357: (176, 108, 141),    # Apricot Orange - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        
        # Czerwienie / róże - poprawione wartości RGB
        6: (186, 112, 86),        # Vermillion Red - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        7: (200, 20, 50),        # Carmine Red
        8: (137, 110, 138),       # Bordeaux Red - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        10: (255, 180, 200),     # Persian Pink
        47: (255, 36, 0),        # Scarlet Red - szkarłatny
        48: (180, 20, 30),       # Scarlet Red Dark
        76: (220, 20, 60),       # Pyrrole Red - intensywny czerwony
        
        # Fiolety - poprawione wartości RGB
        11: (230, 230, 250),     # Light Violet - lawendowy
        12: (186, 85, 211),      # Reddish Violet - czerwonawy fiolet
        13: (230, 230, 250),     # Lavender Violet - lawendowy
        14: (138, 43, 226),      # Bluish Violet - niebieskawy fiolet
        49: (120, 80, 150),      # Permanent Violet
        50: (138, 43, 226),      # Windsor Violet - windsorski fiolet
        51: (138, 43, 226),      # Dark Violet - ciemny fiolet
        
        # Błękity - poprawione wartości RGB
        15: (176, 224, 230),     # Ice Blue - lodowy
        16: (0, 123, 167),        # Cerulean Blue - ceruleum
        17: (0, 71, 171),         # Cobalt Blue - kobaltowy
        18: (173, 216, 230),      # Light Blue - jasny niebieski
        19: (8, 37, 103),         # Sapphire Blue - szafirowy
        20: (0, 49, 83),          # Prussian Blue - pruski
        52: (0, 123, 167),        # Dark Ice Blue - ciemny lodowy
        53: (0, 15, 137),         # Phthalo Blue - ftalowy
        54: (0, 51, 153),         # Cobalt Blue Dark - ciemny kobaltowy
        55: (25, 25, 112),        # Permanent Blue - trwały niebieski
        56: (75, 0, 130),         # Indigo Blue - indygo
        57: (70, 130, 180),       # Mountain Blue - górski
        
        # Zieleń - poprawione wartości RGB
        21: (0, 206, 209),        # Bluish Green - niebieskawa zieleń
        22: (154, 205, 50),       # Yellowish Green - żółtawa zieleń
        23: (0, 255, 127),        # Spring Green - wiosenna
        24: (152, 251, 152),      # Pea Green - groszkowa
        25: (50, 205, 50),        # Meadow Green - łąkowa
        26: (0, 100, 0),          # Dark Green - ciemna zieleń
        27: (85, 107, 47),        # Olive Green Dark - ciemna oliwkowa
        58: (144, 238, 144),     # Light Green - jasna zieleń
        59: (124, 252, 0),        # Grass Green - trawiasta
        60: (0, 201, 87),         # Emerald Green - szmaragdowa
        61: (80, 125, 42),        # Sap Green - sokowa zieleń
        62: (141, 182, 0),        # Apple Green - jabłkowa
        63: (107, 142, 35),       # Light Olive Green - jasna oliwkowa
        
        # Brązy / ochry - poprawione wartości RGB
        28: (184, 134, 76),       # Gold Ochre - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        29: (210, 180, 140),      # Light Ochre - jasna ochra
        30: (139, 69, 19),        # Reddish Brown - czerwonawy brąz
        31: (160, 82, 45),        # Light Brown - jasny brąz
        32: (160, 82, 45),        # Natural Sienna - naturalna sienna
        33: (101, 67, 33),        # Dark Brown - ciemny brąz
        64: (160, 82, 45),        # Burnt Ochre - palona ochra
        65: (205, 133, 63),       # Medium Terracotta - średnia terra cotta
        66: (101, 67, 33),        # Raw Umber - surowa umbra
        68: (101, 67, 33),        # Burnt Umber - palona umbra
        
        # Szarości / czernie / metaliczne - poprawione wartości RGB
        34: (176, 196, 222),      # Bluish Grey Light - jasna niebieskawa
        35: (200, 200, 200),      # Platine Grey
        36: (0, 0, 0),            # Ivory Black - czarny
        38: (140, 150, 160),      # Cold Grey
        39: (192, 192, 192),      # Standard Silver - srebro
        40: (255, 215, 0),        # Standard Gold - złoto
        69: (200, 200, 200),      # Light Grey
        70: (100, 100, 100),     # Dark Grey
        71: (128, 128, 128),      # Medium Grey - średnia
        72: (112, 128, 144),      # Slate Grey - łupkowa
        
        # Zestaw Portrait (dodatkowe kolory)
        350: (255, 220, 200),    # Portrait Peach
        351: (255, 230, 230),    # Light Portrait Pink
        352: (255, 200, 220),    # Blush Pink
        353: (240, 180, 200),    # Amaranth Pink
        354: (255, 180, 160),    # Salmon Pink
        355: (255, 200, 170),    # Peach Orange
        
        # Dodatkowe kolory z katalogu 144 - żółcie/beże
        500: (255, 250, 240),    # Ivory Bone
        504: (190, 186, 106),    # Lemon Yellow - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        550: (255, 245, 220),    # Fair Portrait Gold
        501: (255, 248, 200),    # Pollen Yellow
        801: (187, 153, 78),     # Yellow Ochre - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        
        # Dodatkowe pomarańcze - poprawione wartości RGB
        555: (255, 200, 140),    # Papaya Orange
        556: (255, 180, 100),    # Amber Orange
        557: (255, 160, 80),      # Tangerine Orange
        558: (185, 155, 100),      # Fire Orange - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        126: (184, 122, 76),     # Persian Orange - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        559: (255, 150, 100),     # Portland Orange
        560: (220, 120, 100),     # Dark Salmon Orange
        
        # Dodatkowe czerwienie/róże - poprawione wartości RGB
        600: (255, 100, 80),     # Light Scarlet Red
        601: (165, 105, 103),    # Scarlet Red - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        606: (200, 40, 30),      # Dark Vermilion Red
        602: (180, 30, 50),      # Currant Red
        603: (166, 85, 96),      # Wine Red - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        605: (100, 10, 30),      # Burgundy Red
        653: (255, 50, 150),     # Mexican Pink
        131: (137, 77, 97),       # French Pink - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        132: (172, 90, 87),       # Carmine Red - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        170: (184, 104, 101),    # Pyrrole Red - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        609: (220, 150, 160),    # Antique Rose
        604: (255, 120, 100),    # Coral Red
        610: (240, 100, 120),    # Light Carmine Red
        607: (255, 130, 160),    # Punch Pink
        608: (255, 200, 210),    # Light French Pink
        
        # Dodatkowe fiolety - poprawione wartości RGB
        651: (230, 180, 240),    # Orchid Purple
        654: (140, 60, 120),     # Dark Reddish Violet
        655: (120, 40, 100),     # Byzantium Purple
        177: (146, 110, 145),    # Lilac Violet - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        650: (80, 30, 60),       # Fig Purple
        180: (115, 97, 128),     # Dark Lavender Violet - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        13: (230, 230, 250),     # Lavender Violet - lawendowy
        178: (147, 97, 131),     # Reddish Violet - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        179: (138, 43, 226),     # Bluish Violet - niebieskawy fiolet
        181: (138, 43, 226),     # Windsor Violet - windsorski fiolet
        182: (113, 93, 113),      # Dark Violet - OpenCV mediana z środkowej części (245x65 = 15,925 pikseli, bez krawędzi i linii)
        
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
        
        # Dodatkowe brązy/ochry - poprawione wartości RGB
        802: (184, 134, 11),     # Dark Yellow Ochre - ciemna ochra żółta
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
        
        # Dodatkowe szarości - poprawione wartości RGB
        408: (47, 79, 79),       # Cool Grey 8 - chłodna 8
        406: (105, 105, 105),    # Cool Grey 6 - chłodna 6
        405: (120, 120, 130),    # Cool Grey 5
        403: (169, 169, 169),    # Cool Grey 3 - chłodna 3
        401: (211, 211, 211),    # Cool Grey 1 - chłodna 1
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


def generate_portrait_variant3_black_white(colors, output_filename, title="Koh-I-Noor Polycolor 24 Portrait"):
    """
    Wariant 3: Dokładnie taki sam jak TONALNY, ale z czarnym kwadratem 9x9mm na górze
    (po przeciwległej stronie do próbki koloru)
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
        try:
            c.setFont("UnicodeFont-Bold", 18)
            title_font = "UnicodeFont-Bold"
        except:
            c.setFont("Helvetica-Bold", 18)
            title_font = "Helvetica-Bold"
        branded_title = title.upper()
        if num_pages > 1:
            branded_title += f" - Strona {page_num + 1}/{num_pages}"
        c.drawString(margin_x, page_height - margin_y - 8 * mm, branded_title)
        c.setLineWidth(0.5)
        c.line(margin_x, page_height - margin_y - 11 * mm, page_width - margin_x, page_height - margin_y - 11 * mm)
        
        # Pozycja startowa
        header_height = 20 * mm
        available_height = page_height - 2 * margin_y - header_height
        
        # Wysokości elementów
        name_text_max_height = 25 * mm
        num_text_max_height = 15 * mm
        swatch_size_val = swatch_height
        
        # Całkowita wysokość potrzebna na jeden element
        total_element_height = name_text_max_height + swatch_size_val + num_text_max_height + 8 * mm
        
        # Przesunięcie w dół
        center_y = margin_y + header_height + (available_height * 0.4) - 20 * mm + 60 * mm
        
        # Pozycja kwadratów
        swatch_y = center_y - num_text_max_height - swatch_size_val
        
        start_x = margin_x
        
        for idx, (num, name) in enumerate(page_colors):
            x = start_x + idx * (swatch_width + spacing)
            center_x = x + swatch_width / 2
            global_order_num += 1
            order_num = global_order_num
            
            # 1. Nazwa koloru po angielsku (pionowo, obrócona o 90 stopni, na górze, po lewej)
            c.setFont("Helvetica", 8)
            c.setFillColor(black)
            name_text = str(name)
            
            # Skróć nazwę jeśli za długa
            if len(name_text) > 20:
                name_text = name_text[:18] + "..."
            
            name_text_width = c.stringWidth(name_text, "Helvetica", 8)
            name_text_x = center_x - 1.5 * mm
            name_text_y = swatch_y + swatch_height + 10 * mm + name_text_width / 2
            
            c.saveState()
            c.setFillColor(black)
            c.translate(name_text_x, name_text_y)
            c.rotate(90)
            c.drawString(-name_text_width / 2, 0, name_text)
            c.restoreState()
            
            # 1b. Polska nazwa koloru (pionowo, obrócona o 90 stopni, obok angielskiej, po prawej)
            polish_name = POLISH_NAMES.get(num, "")
            if polish_name:
                try:
                    font_name = "UnicodeFont"
                    c.setFont(font_name, 7)
                except:
                    font_name = "Helvetica"
                    c.setFont(font_name, 7)
                c.setFillColor(black)
                
                polish_text_width = c.stringWidth(polish_name, font_name, 7)
                polish_text_x = center_x + 1.5 * mm
                polish_text_y = swatch_y + swatch_height + 10 * mm + polish_text_width / 2
                
                c.saveState()
                c.setFillColor(black)
                c.translate(polish_text_x, polish_text_y)
                c.rotate(90)
                c.drawString(-polish_text_width / 2, 0, polish_name)
                c.restoreState()
            
            # 3. Kredka próbki (prostokąt jak kredka) - 9mm szerokość, 89mm wysokość
            # Główny prostokąt kredki - pusty, do wypełnienia kredką (dokładnie jak w TONALNY)
            c.setStrokeColor(black)
            c.setLineWidth(1.2)
            c.setFillColor(white)
            corner_radius = 1 * mm
            c.roundRect(x, swatch_y, swatch_width, swatch_height, corner_radius, fill=1, stroke=1)
            
            # Czarny prostokąt 35mm wysokości - na górze
            black_height = 35 * mm  # 35mm wysokości
            black_square_y = swatch_y + swatch_height - black_height  # na górze prostokąta
            c.setFillColor(black)
            c.setStrokeColor(black)
            c.setLineWidth(1.0)
            c.roundRect(x, black_square_y, swatch_width, black_height, corner_radius, fill=1, stroke=1)
            
            # Mały kwadracik 9x9mm z kolorem próbki - na dole prostokąta (dokładnie jak w TONALNY)
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
            num_text = f"3800/{num:02d}"
            
            num_text_width = c.stringWidth(num_text, "Helvetica-Bold", 8)
            num_text_x = center_x
            num_text_y = swatch_y - 8 * mm - num_text_width / 2
            
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


def generate_portrait_with_photo(colors, output_filename, photo_path, title="Koh-I-Noor Polycolor 24 Portrait", pencil_order=None):
    """
    Generuje PDF z próbkami kolorów i dokładnie tymi samymi prostokątami ze zdjęcia,
    z których ekstrahujemy kolory - używając inteligentnego wykrywania obszarów.
    
    Args:
        colors: Lista kolorów w kolejności, w jakiej mają być wyświetlone w PDF
        output_filename: Nazwa pliku wyjściowego
        photo_path: Ścieżka do zdjęcia z próbkami
        title: Tytuł PDF
        pencil_order: Lista numerów kredek w kolejności, w jakiej są na zdjęciu (z góry do dołu)
                     Jeśli None, użyje domyślnej kolejności z detect_swatches_intelligent.py
    """
    import cv2
    import tempfile
    import sys
    import importlib.util
    
    # Zaimportuj funkcje z detect_swatches_intelligent.py
    spec = importlib.util.spec_from_file_location("detect_swatches_intelligent", 
                                                   os.path.join(os.path.dirname(__file__), "detect_swatches_intelligent.py"))
    detect_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(detect_module)
    
    page_width, page_height = landscape(A4)
    
    num_colors = len(colors)
    swatch_width = 9 * mm
    sample_size = 9 * mm
    swatch_height = 80 * mm + sample_size
    spacing = 1 * mm
    
    colors_per_page = 24
    num_pages = (num_colors + colors_per_page - 1) // colors_per_page
    
    c = canvas.Canvas(output_filename, pagesize=landscape(A4))
    
    # Wczytaj zdjęcie
    if not os.path.exists(photo_path):
        print(f"Błąd: Zdjęcie nie znalezione: {photo_path}")
        return
    
    img_bgr = cv2.imread(photo_path)
    if img_bgr is None:
        print(f"Błąd: Nie można wczytać obrazu {photo_path}")
        return
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    height, width = img_rgb.shape[:2]
    
    # INTELIGENTNE WYKRYWANIE OBSZARÓW PRÓBEK
    # Ustal kolumnę do analizy (ta sama, którą chcemy zwizualizować w PDF)
    target_col_start = 400
    # Szerokość kolumny: od x=400 do końca zdjęcia (845) = 445 pikseli
    target_col_width = width - target_col_start  # 845 - 400 = 445

    print("Wykrywanie obszarów próbek...")
    # Przekaż kolejność kredek do funkcji wykrywania (kolejność z góry do dołu na zdjęciu)
    swatch_map = detect_module.intelligent_swatch_detection(
        photo_path,
        target_col_start=target_col_start,
        target_col_width=target_col_width,
        pencil_order=pencil_order,
    )
    
    if not swatch_map:
        print("Błąd: Nie udało się wykryć obszarów próbek")
        return
    
    print(f"Wykryto {len(swatch_map)} obszarów próbek")
    
    # Narysuj zielone ramki bezpośrednio na zdjęciu (przed obrotem)
    print("Rysowanie zielonych ramek na zdjęciu...")
    img_bgr_with_frames = img_bgr.copy()
    
    # Znajdź obszar z najmniejszą współrzędną Y (najwyżej na zdjęciu) - to będzie pierwsza kredka
    first_swatch_y = float('inf')
    first_swatch_num = None
    for num, swatch_info in swatch_map.items():
        y = swatch_info['y']
        if y < first_swatch_y:
            first_swatch_y = y
            first_swatch_num = num
    
    for num, swatch_info in swatch_map.items():
        x = swatch_info['x']
        y = swatch_info['y']
        w = swatch_info['width']
        h = swatch_info['height']
        
        # Użyj tych samych marginesów co przy ekstrakcji kolorów: 5% dla X, 10% dla Y
        margin_x_percent = 0.05  # 5% margines w szerokości
        margin_y_percent = 0.10  # 10% margines w wysokości
        x_start = x + int(w * margin_x_percent)
        x_end = x + w - int(w * margin_x_percent)
        y_start = y + int(h * margin_y_percent)
        y_end = y + h - int(h * margin_y_percent)
        
        # Narysuj zieloną ramkę pokazującą rzeczywisty obszar ekstrakcji (BGR format w OpenCV: (0, 255, 0) = zielony)
        # Użyj grubszej linii (3 piksele) dla lepszej widoczności w PDF
        cv2.rectangle(img_bgr_with_frames, (x_start, y_start), (x_end, y_end), (0, 255, 0), 3)
        # Jeśli to pierwsza kredka (najwyżej na zdjęciu), dodaj etykietę
        if num == first_swatch_num:
            label = f"3800/{num:02d}"
            # umieść etykietę tuż nad ramką - większy rozmiar i lepsza widoczność
            font_scale = 1.2
            thickness = 3
            text_x = x + w // 2  # Wyśrodkuj tekst
            text_y = max(25, y - 15)  # Wyżej nad ramką
            # Pobierz rozmiar tekstu, aby wyśrodkować
            (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
            text_x = text_x - text_width // 2  # Wyśrodkuj
            cv2.putText(
                img_bgr_with_frames,
                label,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (0, 255, 0),
                thickness,
                cv2.LINE_AA,
            )
    
    # Zapisz zmodyfikowane zdjęcie do pliku tymczasowego
    temp_dir = tempfile.mkdtemp()
    temp_photo_path = os.path.join(temp_dir, "photo_with_frames.jpg")
    cv2.imwrite(temp_photo_path, img_bgr_with_frames)
    photo_path = temp_photo_path  # Użyj zmodyfikowanego zdjęcia
    print(f"Zapisano zdjęcie z ramkami: {temp_photo_path}")
    
    # Sprawdź, czy wszystkie kolory mają wykryte obszary
    missing_colors = []
    for num, name in colors:
        if num not in swatch_map:
            missing_colors.append((num, name))
    
    if missing_colors:
        print(f"UWAGA: {len(missing_colors)} kolorów nie ma wykrytych obszarów:")
        for num, name in missing_colors:
            print(f"  - {num:03d}: {name}")
    
    margin_x = 10 * mm
    margin_y = 20 * mm
    
    global_order_num = 0
    
    # Tymczasowy folder na wycięte prostokąty
    temp_dir = tempfile.mkdtemp()
    
    for page_num in range(num_pages):
        if page_num > 0:
            c.showPage()
        
        start_idx = page_num * colors_per_page
        end_idx = min(start_idx + colors_per_page, num_colors)
        page_colors = colors[start_idx:end_idx]
        num_colors_on_page = len(page_colors)
        
        # Tytuł
        try:
            c.setFont("UnicodeFont-Bold", 18)
            title_font = "UnicodeFont-Bold"
        except:
            c.setFont("Helvetica-Bold", 18)
            title_font = "Helvetica-Bold"
        branded_title = title.upper()
        if num_pages > 1:
            branded_title += f" - Strona {page_num + 1}/{num_pages}"
        c.drawString(margin_x, page_height - margin_y - 8 * mm, branded_title)
        c.setLineWidth(0.5)
        c.line(margin_x, page_height - margin_y - 11 * mm, page_width - margin_x, page_height - margin_y - 11 * mm)
        
        # LEWA STRONA - Próbki kolorów
        header_height = 20 * mm
        available_height = page_height - 2 * margin_y - header_height
        
        name_text_max_height = 25 * mm
        num_text_max_height = 15 * mm
        swatch_size_val = swatch_height
        total_element_height = name_text_max_height + swatch_size_val + num_text_max_height + 8 * mm
        
        center_y = margin_y + header_height + (available_height * 0.4) - 20 * mm + 60 * mm
        swatch_y = center_y - num_text_max_height - swatch_size_val
        
        # Oblicz szerokość - zdjęcie jest nakładane NA próbkę, więc szerokość = tylko szerokość próbki
        element_width = swatch_width  # Tylko szerokość próbki (zdjęcie jest na próbce)
        total_width = num_colors_on_page * element_width + (num_colors_on_page - 1) * spacing
        # Wyśrodkuj na stronie
        left_margin = (page_width - total_width) / 2
        start_x = left_margin
        
        for idx, (num, name) in enumerate(page_colors):
            # Pozycja próbki
            element_start_x = start_x + idx * (element_width + spacing)
            x = element_start_x
            center_x_pdf = x + swatch_width / 2
            global_order_num += 1
            order_num = global_order_num
            
            # Nazwa angielska
            c.setFont("Helvetica", 8)
            c.setFillColor(black)
            name_text = str(name)
            if len(name_text) > 20:
                name_text = name_text[:18] + "..."
            
            name_text_width = c.stringWidth(name_text, "Helvetica", 8)
            name_text_x = center_x_pdf - 1.5 * mm
            name_text_y = swatch_y + swatch_height + 10 * mm + name_text_width / 2
            
            c.saveState()
            c.setFillColor(black)
            c.translate(name_text_x, name_text_y)
            c.rotate(90)
            c.drawString(-name_text_width / 2, 0, name_text)
            c.restoreState()
            
            # Polska nazwa
            polish_name = POLISH_NAMES.get(num, "")
            if polish_name:
                try:
                    font_name = "UnicodeFont"
                    c.setFont(font_name, 7)
                except:
                    font_name = "Helvetica"
                    c.setFont(font_name, 7)
                c.setFillColor(black)
                polish_text_width = c.stringWidth(polish_name, font_name, 7)
                polish_text_x = center_x_pdf + 1.5 * mm
                polish_text_y = swatch_y + swatch_height + 10 * mm + polish_text_width / 2
                c.saveState()
                c.setFillColor(black)
                c.translate(polish_text_x, polish_text_y)
                c.rotate(90)
                c.drawString(-polish_text_width / 2, 0, polish_name)
                c.restoreState()
            
            # Numer
            c.setFont("Helvetica-Bold", 9)
            num_text = f"3800/{num:03d}"
            num_text_width = c.stringWidth(num_text, "Helvetica-Bold", 9)
            num_text_x = center_x_pdf - num_text_width / 2
            num_text_y = swatch_y - 5 * mm
            c.drawString(num_text_x, num_text_y, num_text)
            
            # Numer porządkowy
            c.setFont("Helvetica", 8)
            order_text = str(order_num)
            order_text_width = c.stringWidth(order_text, "Helvetica", 8)
            order_text_x = center_x_pdf - order_text_width / 2
            order_text_y = swatch_y - 12 * mm
            c.drawString(order_text_x, order_text_y, order_text)
            
            # NAJPIERW wstaw obraz ze zdjęcia (tło), POTEM próbkę koloru (nakładka półprzezroczysta)
            # Użyj inteligentnie wykrytego obszaru - DLA WSZYSTKICH KOLORÓW
            # Każdy kolor MUSI mieć próbkę ze zdjęcia
            if num in swatch_map:
                swatch_info = swatch_map[num]
                
                # Wyciągnij prostokąt z wykrytego obszaru - INTELIGENTNE wykrywanie granic
                # UŻYJ ODDZIELNYCH ZMIENNYCH dla współrzędnych ze zdjęcia!
                swatch_x = swatch_info['x']  # Współrzędna X ze zdjęcia
                swatch_y_photo = swatch_info['y']  # Współrzędna Y ze zdjęcia
                w = swatch_info['width']
                h = swatch_info['height']
                
                # Użyj różnych marginesów: 5% dla szerokości (X), 10% dla wysokości (Y)
                margin_x_percent = 0.05  # 5% margines w szerokości
                margin_y_percent = 0.10  # 10% margines w wysokości
                
                x_start = swatch_x + int(w * margin_x_percent)
                x_end = swatch_x + w - int(w * margin_x_percent)
                y_start = swatch_y_photo + int(h * margin_y_percent)
                y_end = swatch_y_photo + h - int(h * margin_y_percent)
                
                # Wyciągnij prostokąt ze zdjęcia
                roi = img_rgb[y_start:y_end, x_start:x_end]
                
                if roi.size > 0:
                    # DODATKOWE filtrowanie - usuń wszystkie czarne i ciemne piksele z wyciętego obszaru
                    # SPECJALNA OBSŁUGA dla białego koloru (kredka 1) - nie filtruj szarych pikseli!
                    roi_cleaned = roi.copy()
                    
                    if num == 1:  # White - specjalna obsługa
                        # Dla białego koloru, usuń TYLKO naprawdę czarne piksele (linie)
                        # Nie filtruj szarych - biały na zdjęciu może być szary!
                        roi_gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
                        black_mask = roi_gray < 50  # Tylko naprawdę czarne (linie)
                        
                        if np.any(black_mask):
                            # Zamień tylko naprawdę czarne piksele na biały
                            roi_cleaned[black_mask] = [255, 255, 255]
                    else:
                        # Dla innych kolorów - normalne filtrowanie
                        # Konwertuj na skale szarości do wykrywania czarnych pikseli
                        roi_gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
                        
                        # Wykryj czarne i bardzo ciemne piksele (linie) - bardzo agresywny próg
                        black_threshold = 80  # Wyższy próg - wykryj też ciemne obszary
                        black_mask = roi_gray < black_threshold
                        
                        # Wykryj również piksele o niskiej saturacji (szare linie)
                        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
                        saturation = roi_hsv[:, :, 1]
                        low_saturation_mask = saturation < 30  # Niska saturacja = szare linie
                        
                        # Kombinuj: czarne + niska saturacja = linie do usunięcia
                        lines_mask = black_mask | low_saturation_mask
                        
                        if np.any(lines_mask):
                            # Znajdź nie-liniowe piksele
                            non_lines_mask = ~lines_mask
                            
                            if np.any(non_lines_mask):
                                # Dla każdego kanału RGB, wypełnij linie medianą z nie-liniowych pikseli
                                for channel in range(3):
                                    channel_data = roi[:, :, channel].copy()
                                    median_color = np.median(channel_data[non_lines_mask])
                                    channel_data[lines_mask] = int(median_color)
                                    roi_cleaned[:, :, channel] = channel_data
                            else:
                                # Jeśli wszystkie piksele to linie, użyj białego
                                roi_cleaned[lines_mask] = [255, 255, 255]
                    
                    # Zapisz wycięty prostokąt jako tymczasowy plik
                    roi_pil = Image.fromarray(roi_cleaned)
                    
                    # OBRÓĆ prostokąt o 90 stopni, aby był pionowy (wzdłuż) jak próbka
                    roi_pil_rotated = roi_pil.rotate(90, expand=True)
                    
                    temp_file = os.path.join(temp_dir, f"roi_{num}.png")
                    roi_pil_rotated.save(temp_file)
                    
                    # NAJPIERW narysuj główny prostokąt kredki z czarną ramką (jak w oryginalnej wersji)
                    corner_radius = 1 * mm
                    c.setStrokeColor(black)
                    c.setLineWidth(1.2)
                    c.setFillColor(white)
                    c.roundRect(x, swatch_y, swatch_width, swatch_height, corner_radius, fill=1, stroke=1)
                    
                    # Potem kwadracik 9x9mm z kolorem RGB na dole
                    color_rgb = get_color_for_pencil(num, name)
                    color = HexColor(f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
                    
                    # Kwadracik na dole - 9mm x 9mm (sample_size jest już zdefiniowane w funkcji)
                    sample_y = swatch_y  # na samym dole prostokąta
                    
                    c.setFillColor(color)
                    c.setStrokeColor(black)
                    c.setLineWidth(1.0)
                    c.roundRect(x, sample_y, swatch_width, sample_size, corner_radius,
                               fill=1, stroke=1)
                    
                    # TERAZ nałóż wycięty prostokąt NA próbkę koloru (w tym samym miejscu co próbka PDF)
                    # Użyj współrzędnych PDF, nie ze zdjęcia!
                    photo_x = x  # x to współrzędna PDF próbki (z pętli)
                    photo_y = swatch_y  # swatch_y to współrzędna PDF próbki
                    photo_width = swatch_width  # Ta sama szerokość co próbka
                    photo_height = swatch_height  # Ta sama wysokość co próbka
                    
                    # Oblicz skalę zachowując proporcje (dla obróconego obrazu)
                    roi_width, roi_height = roi_pil_rotated.size
                    if roi_width > 0 and roi_height > 0:
                        # Użyj pełnej szerokości i wysokości próbki (bez skalowania w dół)
                        # Obraz powinien wypełnić całą próbkę
                        try:
                            # Narysuj wycięty prostokąt - użyj pełnej szerokości i wysokości próbki
                            # NIE skalować - użyj dokładnie rozmiaru próbki
                            # Sprawdź czy plik istnieje przed wstawieniem
                            if os.path.exists(temp_file):
                                # Wstaw obraz w oryginalnej skali (zachowując proporcje)
                                # Skaluj tak, aby obraz zmieścił się w próbce, zachowując proporcje
                                scale_w = photo_width / roi_width
                                scale_h = photo_height / roi_height
                                scale = min(scale_w, scale_h)  # Użyj min, aby obraz zmieścił się w próbce
                                
                                scaled_width = roi_width * scale
                                scaled_height = roi_height * scale
                                
                                # Wyśrodkuj w obszarze próbki
                                photo_x_centered = photo_x + (photo_width - scaled_width) / 2
                                photo_y_centered = photo_y + (photo_height - scaled_height) / 2
                                
                                c.drawImage(temp_file, photo_x_centered, photo_y_centered,
                                           width=scaled_width, height=scaled_height, preserveAspectRatio=True)
                                
                                print(f"  ✓ Wstawiono próbkę dla kredki {num:03d} (rozmiar: {scaled_width:.1f}x{scaled_height:.1f}mm)")
                            else:
                                print(f"  ✗ Błąd: Plik {temp_file} nie istnieje dla kredki {num:03d}")
                        except Exception as e:
                            # Jeśli błąd, narysuj prostokąt z komunikatem
                            print(f"  ✗ Błąd wstawiania próbki dla kredki {num:03d}: {str(e)}")
                            c.setFont("Helvetica", 6)
                            c.setFillColor(black)
                            c.drawString(photo_x + 1 * mm, photo_y + photo_height / 2, f"Błąd: {str(e)[:20]}")
                    else:
                        print(f"  ✗ Błąd: Nieprawidłowe wymiary ROI dla kredki {num:03d}: {roi_width}x{roi_height}")
                else:
                    print(f"  ✗ Błąd: Pusty ROI dla kredki {num:03d}")
            else:
                # Jeśli kolor nie ma wykrytego obszaru, wyświetl komunikat
                print(f"UWAGA: Kolor {num:03d} ({name}) nie ma wykrytego obszaru - brak próbki ze zdjęcia")
            
            # NIE rysuj próbki koloru - zostaw tylko obrazy ze zdjęcia, żeby były w pełni widoczne
            # Jeśli chcesz próbki kolorów, odkomentuj poniższy kod:
            # color_rgb = get_color_for_pencil(num, name)
            # color = HexColor(f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
            # c.setFillColor(color)
            # c.setStrokeColor(black)
            # c.setLineWidth(1.2)
            # corner_radius = 1 * mm
            # c.roundRect(x, swatch_y, swatch_width, swatch_height, corner_radius, fill=1, stroke=1)
    
    # Dodaj drugą stronę z całym zdjęciem
    c.showPage()
    
    # Tytuł na stronie ze zdjęciem
    header_height = 20 * mm
    try:
        c.setFont("UnicodeFont-Bold", 18)
        title_font = "UnicodeFont-Bold"
    except:
        c.setFont("Helvetica-Bold", 18)
        title_font = "Helvetica-Bold"
    photo_title = "ZDJĘCIE KALIBRACYJNE - PRÓBKI KREDKAMI"
    c.drawString(margin_x, page_height - margin_y - 8 * mm, photo_title)
    c.setLineWidth(0.5)
    c.line(margin_x, page_height - margin_y - 11 * mm, page_width - margin_x, page_height - margin_y - 11 * mm)
    
    # Oblicz szerokość wszystkich kredek (ta sama szerokość co na pierwszej stronie)
    # To jest szerokość całego rzędu kredek z pierwszej strony
    first_page_colors = min(colors_per_page, num_colors)
    total_swatches_width = first_page_colors * swatch_width + (first_page_colors - 1) * spacing
    left_margin_swatches = (page_width - total_swatches_width) / 2
    
    # Użyj tej samej szerokości dla zdjęcia (obróconego o 90 stopni)
    # Zdjęcie jest pionowe (height > width), więc po obrocie szerokość = wysokość oryginału
    img_pdf_width = total_swatches_width  # Ta sama szerokość co wszystkie kredki
    # Oblicz wysokość zachowując proporcje (po obrocie: wysokość = szerokość oryginału)
    img_pdf_height = (img_pdf_width / height) * width  # Po obrocie: height->width, width->height
    
    # Wyśrodkuj zdjęcie (użyj tego samego marginesu co kredki)
    img_x = left_margin_swatches
    available_height = page_height - 2 * margin_y - header_height
    img_y = margin_y + (available_height - img_pdf_height) / 2
    
    # Skale dla przeliczania współrzędnych
    scale_x = img_pdf_width / height  # Skala dla szerokości (po obrocie: height->width)
    scale_y = img_pdf_height / width  # Skala dla wysokości (po obrocie: width->height)
    
    # Obróć zdjęcie o 90 stopni w lewo (aby było poziome)
    # Ramki są już narysowane bezpośrednio na zdjęciu, więc nie trzeba ich rysować tutaj
    c.saveState()
    c.translate(img_x + img_pdf_width / 2, img_y + img_pdf_height / 2)
    c.rotate(90)
    # Po obrocie, współrzędne są względem środka, więc przesuń o połowę wymiarów
    c.drawImage(photo_path, -img_pdf_height / 2, -img_pdf_width / 2, 
                width=img_pdf_height, height=img_pdf_width, preserveAspectRatio=True)
    c.restoreState()
    
    # Numer strony
    c.setFont("Helvetica", 9)
    c.drawRightString(page_width - margin_x, margin_y - 5 * mm, f"Strona {num_pages + 1}/{num_pages + 1}")
    
    c.save()
    
    # Usuń tymczasowe pliki
    import shutil
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
    
    print(f"✓ Wygenerowano: {output_filename} (z wyciętymi prostokątami ze zdjęcia)")


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
    
    # Generuj wzornik dla zestawu 72 - KATALOG 2017
    if COLORS_72_2017:
        print(f"Zestaw 72 kolorów - KATALOG 2017 ({len(COLORS_72_2017)} kolorów)...")
        generate_portrait_variant1_single_row(
            COLORS_72_2017,
            "Koh-I-Noor_Polycolor_72_2017.pdf",
            "KOH-I-NOOR POLYCOLOR 72 - KATALOG 2017"
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
    
    # Generuj wariant 3: Prostokąty podzielone na pół (białe/czarne tło) - KOLEJNOŚĆ TONALNA
    print(f"Zestaw 24 Portrait - Wariant 3 BIAŁE/CZARNE TŁO (jeden rząd, test krycia)...")
    generate_portrait_variant3_black_white(
        COLORS_24_PORTRAIT,
        "Koh-I-Noor_Polycolor_24_Portrait_BIALE_CZARNE.pdf",
        "KOH-I-NOOR POLYCOLOR 24 PORTRAIT (3824) - TEST KRYCIA NA BIAŁYM I CZARNYM TLE"
    )
    
    # Generuj PDF dla 24 kolorów ZE ZDJĘCIA KALIBRACYJNEGO ze skorygowanymi wartościami RGB
    print()
    print(f"24 kolory ze zdjęcia kalibracyjnego - SKORYGOWANE WARTOŚCI RGB (na próbę)...")
    import json
    from colorsys import rgb_to_hsv
    
    # Wczytaj skorygowane wartości
    try:
        with open('calibrated_colors_second.json', 'r') as f:
            calibrated = json.load(f)
    except FileNotFoundError:
        calibrated = {}
    
    # Numery kredek które były na zdjęciu kalibracyjnym
    calibration_pencils = [1, 41, 504, 3, 801, 28, 45, 44, 42, 558, 126, 5, 6, 170, 601, 132, 603, 131, 357, 178, 177, 8, 182, 180]
    
    # Pobierz nazwy z katalogu
    catalog_map = {num: name for num, name in COLORS_144_CATALOG}
    
    # Stwórz listę kolorów ze skorygowanymi wartościami RGB
    colors_calibrated = []
    for num in calibration_pencils:
        if str(num) in calibrated:
            target_rgb = tuple(calibrated[str(num)]['target_rgb'])
            name = catalog_map.get(num, f"Color {num}")
            colors_calibrated.append((num, name, target_rgb))
    
    # Sortowanie według hue (odcienia) - standardowe podejście
    # Konwertuj RGB na HSV i sortuj według hue rosnąco, potem według value (jasności)
    colors_with_hsv = []
    for num, name, rgb in colors_calibrated:
        r, g, b = rgb
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        h, s, v = rgb_to_hsv(r, g, b)
        colors_with_hsv.append({
            'num': num,
            'name': name,
            'rgb': rgb,
            'h': h,
            's': s,
            'v': v
        })
    
    # Sortuj według hue rosnąco, potem według value (jasności) - od najjaśniejszych do najciemniejszych
    tonal_sorted = sorted(colors_with_hsv, key=lambda c: (c['h'], -c['v']))
    
    # Odwróć kolejność: kredka 28 na pozycji 1, kredka 132 na pozycji 17
    # Znajdź pozycje kredek 28 i 132
    pos_28 = next(i for i, c in enumerate(tonal_sorted) if c['num'] == 28)
    pos_132 = next(i for i, c in enumerate(tonal_sorted) if c['num'] == 132)
    
    # Część 1: Od początku do kredki 28 (odwróć) - pozycje 1-16
    part1 = tonal_sorted[:pos_28+1]
    part1_reversed = part1[::-1]
    
    # Część 2: Od kredki 28 do kredki 132 (odwróć, bez kredki 28) - pozycje 17-24
    part2 = tonal_sorted[pos_28+1:pos_132+1]
    part2_reversed = part2[::-1]
    
    # Część 3: Od kredki 132 do końca (bez kredki 132) - nie ma, bo 132 jest na końcu
    part3 = tonal_sorted[pos_132+1:]
    
    # Nowa kolejność: odwróć od początku do 28, potem odwróć od 28 do 132
    tonal_sorted = part1_reversed + part2_reversed + part3
    
    # Przenieś biały na początek (pozycja 1)
    white_idx = next(i for i, c in enumerate(tonal_sorted) if c['num'] == 1)
    if white_idx > 0:
        white_color = tonal_sorted.pop(white_idx)
        tonal_sorted.insert(0, white_color)
    
    COLORS_CALIBRATED_24 = [(c['num'], c['name']) for c in tonal_sorted]
    
    # Stwórz mapę skorygowanych wartości RGB
    calibrated_rgb_map = {c['num']: c['rgb'] for c in tonal_sorted}
    
    # Tymczasowo nadpisz get_color_for_pencil dla tych kolorów
    original_get_color = globals()['get_color_for_pencil']
    
    def get_color_calibrated(num, color_name=None):
        if num in calibrated_rgb_map:
            return calibrated_rgb_map[num]
        return original_get_color(num, color_name)
    
    # Nadpisz globalną funkcję
    globals()['get_color_for_pencil'] = get_color_calibrated
    
    try:
        generate_portrait_variant1_single_row(
            COLORS_CALIBRATED_24,
            "Koh-I-Noor_Polycolor_24_KALIBROWANE.pdf",
            "KOH-I-NOOR POLYCOLOR 24 KOLORY - SKORYGOWANE WARTOŚCI RGB ZE ZDJĘCIA"
        )
        
        # Generuj PDF ze zdjęciem dla porównania
        photo_path = "probki-kredek-na-papierze-trzecia-kalibracja.jpg"
        if os.path.exists(photo_path):
            print()
            print(f"24 kolory ze zdjęcia kalibracyjnego - PDF ZE ZDJĘCIEM (porównanie)...")
            # Użyj kolejności z zdjęcia (calibration_pencils) dla pierwszej strony
            # Kolejność na zdjęciu (z góry do dołu) musi być taka sama jak na pierwszej stronie PDF
            catalog_map = {num: name for num, name in COLORS_144_CATALOG}
            colors_in_photo_order = [(num, catalog_map.get(num, f"Color {num}")) for num in calibration_pencils]
            
            # Przekaż kolejność kredek do funkcji wykrywania, aby mapowanie było poprawne
            generate_portrait_with_photo(
                colors_in_photo_order,  # Użyj kolejności z zdjęcia!
                "Koh-I-Noor_Polycolor_24_Z_ZDJECIEM.pdf",
                photo_path,
                "KOH-I-NOOR POLYCOLOR 24 KOLORY - PORÓWNANIE Z RZECZYWISTYMI KREDKAMI",
                pencil_order=calibration_pencils  # Przekaż kolejność z zdjęcia
            )
    finally:
        # Przywróć oryginalną funkcję
        globals()['get_color_for_pencil'] = original_get_color
    
    # Generuj PDF dla mojego zestawu 72 kolorów - wariant z czarnym prostokątem
    if COLORS_MY_72:
        print()
        print(f"Mój zestaw 72 kolorów - Wariant BIAŁE/CZARNE TŁO (test krycia)...")
        generate_portrait_variant3_black_white(
            COLORS_MY_72,
            "Koh-I-Noor_Polycolor_MOJ_ZESTAW_72_BIALE_CZARNE.pdf",
            "KOH-I-NOOR POLYCOLOR - MÓJ ZESTAW 72 KOLORÓW - TEST KRYCIA NA BIAŁYM I CZARNYM TLE"
        )
    
    print()
    print("✓ Gotowe! Wszystkie pliki PDF są gotowe do wydruku na A4 (orientacja pozioma).")


if __name__ == "__main__":
    main()

