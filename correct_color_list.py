#!/usr/bin/env python3
"""
Skrypt do automatycznego poprawiania listy kolorów z błędami.
Dopasowuje nazwy do wzorca z katalogu 144 (źródło prawdy).
"""

import re
from colors_144_catalog import COLORS_144_CATALOG


def correct_color_list(user_list_text):
    """
    Przyjmuje listę z możliwymi błędami i poprawia ją do wzorca z katalogu 144.
    
    Args:
        user_list_text: Tekst z listą w formacie "1 x Nazwa Koloru Numer,"
    
    Returns:
        Lista krotek (numer, poprawiona_nazwa)
    """
    # Utwórz mapę numer -> nazwa z katalogu 144
    catalog_map = {}
    for num, name in COLORS_144_CATALOG:
        if num not in catalog_map:
            catalog_map[num] = name
    
    # Parsuj wklejoną listę
    lines = user_list_text.strip().split('\n')
    parsed_list = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Parsuj format: "1 x White 1," lub "1 x White 1" lub "1 x White 1."
        # Szukaj numeru na końcu linii
        match = re.search(r'(\d+)\s*[,.]?\s*$', line)
        if match:
            num = int(match.group(1))
            # Wyciągnij nazwę (wszystko między "x" a numerem)
            name_match = re.search(r'x\s+(.+?)\s+\d+\s*[,.]?\s*$', line)
            if name_match:
                name = name_match.group(1).strip()
                parsed_list.append((num, name))
    
    # Popraw listę
    corrected_list = []
    corrections = []
    
    for num, user_name in parsed_list:
        if num in catalog_map:
            # Użyj nazwy z katalogu (źródło prawdy)
            catalog_name = catalog_map[num]
            corrected_list.append((num, catalog_name))
            # Sprawdź czy była różnica
            if user_name.lower().strip() != catalog_name.lower().strip():
                corrections.append((num, user_name, catalog_name))
        else:
            # Użyj nazwy z wklejonej listy (spoza katalogu)
            corrected_list.append((num, user_name))
    
    return corrected_list, corrections, catalog_map


if __name__ == '__main__':
    # Test z przykładową listą
    user_list = """1 x White 1,
1 x Lemon Yellow 2,
1 x Chrome Yellow 3,
1 x Dark Yellow 4,
1 x Reddish Orange 5,
1 x Vermillion Red 6,
1 x Carmine Red 7,
1 x Bordeaux Red 8,
1 x Apricot Orange 9,
1 x Persian Pink 10,
1 x Light Violet 11,
1 x Reddish Violet 12,
1 x Medium Violet 13,
1 x Bluish Violet 14,
1 x Ice Blue 15,
1 x Cerulean Blue 16,
1 x Cobalt Blue 17,
1 x Light Blue 18,
1 x Sapphire Blue 19,
1 x Prussian Blue 20,
1 x Bluish Green 21,
1 x Yellowish Green 22,
1 x Spring Green 23,
1 x Pea Green 24,
1 x Meadow Green 25,
1 x Dark Green 26,
1 x Olive Green Dark 27,
1 x Gold Ochre 28,
1 x Light Ochre 29,
1 x Reddish Brown 30,
1 x Light Brown 31,
1 x Natural Sienna 32,
1 x Dark Brown 33,
1 x Bluish Grey Light 34,
1 x Platine Grey 35,
1 x Ivory Black 36,
1 x Cold Grey 38,
1 x Standard Silver 39,
1 x Standard Gold 40,
1 x Banana Yellow 41,
1 x Chromium Orange 42,
1 x Naples Yellow Light 43,
1 x Naples Yellow 44,
1 x Light Orange 45,
1 x Cadmium Orange 46,
1 x Scarlet Red 47,
1 x Scarlet Red Dark 48,
1 x Permanent Violet 49
1 x Windsor Violet 50,
1 x Dark Violet 51,
1 x Azure Blue 52,
1 x Phthalo Blue 53,
1 x Cobalt Blue Dark 54,
1 x Permanent Blue 55,
1 x Indigo Blue 56,
1 x Mountain Blue 57,
1 x Light Green 58,
1 x Grass Green 59,
1 x Emerald Green 60,
1 x Sap Green 61,
1 x Apple Green 62,
1 x Olive Green Light 63,
1 x Burnt Ochre 64,
1 x Medium Terracotta 65,
1 x Raw Umber 66,
1 x Yellowish Orange 67,
1 x Burnt Umber 68,
1 x Light Grey 69,
1 x Dark Grey 70,
1 x Medium Grey 71,
1 x Slate Grey 72,
1 x Pyrrole Red 76."""
    
    corrected, corrections, catalog_map = correct_color_list(user_list)
    
    print('POPRAWIONA LISTA (zgodna z katalogiem 144):')
    print('=' * 70)
    print()
    
    for num, name in corrected:
        source = 'katalog' if num in catalog_map else 'wklejona lista'
        print(f'{num:3d}: {name:35s} ({source})')
    
    print()
    if corrections:
        print('ROZBIEŻNOŚCI (co zostało poprawione):')
        print('-' * 70)
        for num, user_name, catalog_name in corrections:
            print(f'  {num:3d}: "{user_name}" -> "{catalog_name}"')
    else:
        print('✓ Wszystkie nazwy były poprawne!')

