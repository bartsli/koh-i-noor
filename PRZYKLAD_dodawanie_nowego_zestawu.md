# Jak dodać nowy zestaw kredek

## Krok 1: Utwórz plik z definicją kolorów

Stwórz nowy plik np. `colors_XX.py` (gdzie XX to liczba kolorów lub nazwa zestawu):

```python
# Koh-I-Noor Polycolor XX - kolory w kolejności tonalnej

COLORS_XX = [
    (1, "White"),
    (2, "Lemon Yellow"),
    (3, "Chrome Yellow"),
    # ... dodaj wszystkie kolory
]
```

## Krok 2: Dodaj import w generate_swatches.py

Na początku pliku `generate_swatches.py` dodaj:

```python
from colors_XX import COLORS_XX
```

## Krok 3: Dodaj polskie nazwy (opcjonalnie)

W słowniku `POLISH_NAMES` w `generate_swatches.py` dodaj:

```python
POLISH_NAMES = {
    # ... istniejące nazwy ...
    2: "Żółć cytrynowa",
    3: "Żółć chromowa",
    # ... dodaj nowe
}
```

## Krok 4: Dodaj kolory do get_color_for_pencil() (opcjonalnie)

W funkcji `get_color_for_pencil()` dodaj kolory dla nowego zestawu:

```python
color_map = {
    # ... istniejące kolory ...
    2: (255, 250, 100),  # Lemon Yellow
    3: (255, 220, 50),   # Chrome Yellow
    # ... dodaj nowe
}
```

## Krok 5: Dodaj wywołanie w main()

W funkcji `main()` dodaj:

```python
# Generuj wzornik dla zestawu XX
print(f"Zestaw XX ({len(COLORS_XX)} kolorów)...")
generate_portrait_variant1_single_row(
    COLORS_XX,
    "Koh-I-Noor_Polycolor_XX_TONALNY.pdf",
    "KOH-I-NOOR POLYCOLOR XX - KOLEJNOŚĆ TONALNA"
)

# Jeśli masz kolejność z pudełka:
box_order = [1, 2, 3, ...]  # kolejność z fizycznego pudełka
color_map = {num: (num, name) for num, name in COLORS_XX}
colors_box_order = [color_map[num] for num in box_order if num in color_map]
generate_portrait_variant1_single_row(
    colors_box_order,
    "Koh-I-Noor_Polycolor_XX_Z_PUDELKA.pdf",
    "KOH-I-NOOR POLYCOLOR XX - KOLEJNOŚĆ Z PUDEŁKA"
)
```

## Przykład: Zestaw 12 kolorów

1. Utwórz `colors_12.py`:
```python
COLORS_12 = [
    (1, "White"),
    (41, "Banana Yellow"),
    # ... 12 kolorów
]
```

2. W `generate_swatches.py`:
```python
from colors_12 import COLORS_12

# W main():
generate_portrait_variant1_single_row(
    COLORS_12,
    "Koh-I-Noor_Polycolor_12_TONALNY.pdf",
    "KOH-I-NOOR POLYCOLOR 12 - KOLEJNOŚĆ TONALNA"
)
```

## Uwagi

- Funkcja `generate_portrait_variant1_single_row` działa z dowolną liczbą kolorów
- Automatycznie dostosowuje szerokość i odstępy
- Możesz użyć tej samej funkcji dla różnych zestawów
- Nie musisz kopiować całego skryptu - wystarczy dodać nowy plik z kolorami i wywołanie w main()

