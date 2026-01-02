#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ekstrakcja listy 72 kolorów z katalogu PDF z 2017 roku
"""

import pdfplumber
import re

pdf_path = "PolycolorCC.pdf"
colors = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        # Przejdź przez wszystkie strony
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                current_code = None
                current_name = None
                current_catalog_num = None
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Szukaj kodów produktu (10 cyfr + KS)
                    code_match = re.search(r'(\d{10})KS', line)
                    if code_match:
                        current_code = code_match.group(1)
                        # Wyciągnij numer z kodu (ostatnie 3-4 cyfry)
                        # Kod ma format 3800001001KS, gdzie 001 to numer
                        code_num = current_code[-3:] if len(current_code) >= 3 else current_code
                        # Jeśli kod zaczyna się od 3800, wyciągnij część po 3800
                        if current_code.startswith('3800'):
                            # Format może być różny, spróbujmy wyciągnąć numer
                            if len(current_code) == 10:
                                # 3800001001 -> 001
                                code_num = current_code[4:7] if len(current_code) > 7 else current_code[4:]
                    
                    # Szukaj nazw kolorów (duże litery na początku, bez cyfr)
                    name_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', line)
                    if name_match and not re.search(r'\d{10}', line):
                        potential_name = name_match.group(1)
                        # Pomiń jeśli to ocena gwiazdkowa lub inne
                        if '★' not in potential_name and len(potential_name) > 2:
                            current_name = potential_name
                    
                    # Szukaj numerów katalogowych (małe liczby, np. 170, 19, 41)
                    catalog_match = re.search(r'\b(\d{1,3})\b', line)
                    if catalog_match and current_name:
                        num = int(catalog_match.group(1))
                        # Numery katalogowe są zwykle 1-200
                        if 1 <= num <= 200:
                            current_catalog_num = num
                    
                    # Jeśli mamy wszystkie dane, zapisz
                    if current_code and current_name and current_catalog_num:
                        colors.append({
                            'code': current_code,
                            'name': current_name,
                            'catalog_num': current_catalog_num
                        })
                        # Resetuj
                        current_code = None
                        current_name = None
                        current_catalog_num = None
                        if len(colors) >= 72:
                            break
                
                if len(colors) >= 72:
                    break
                    
except Exception as e:
    print(f"Błąd: {e}")
    import traceback
    traceback.print_exc()

print(f"Znaleziono {len(colors)} kolorów\n")
for i, color in enumerate(colors[:20], 1):
    print(f"{i}. {color['code']} - {color['name']} (kat: {color['catalog_num']})")

