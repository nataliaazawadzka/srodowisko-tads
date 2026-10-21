import csv
from pathlib import Path


def wczytaj_zamowienia(sciezka):
    """Wczytuje zamowienia z pliku CSV."""
    zamowienia = []
    sciezka_pliku = Path(sciezka)
    if not sciezka_pliku.is_file():
        return zamowienia

    with open(sciezka_pliku, mode="r", encoding="utf-8") as plik:
        czytnik = csv.DictReader(plik)
        for wiersz in czytnik:
            zamowienia.append(
                {
                    "data": wiersz["data"].strip(),
                    "region": wiersz["region"].strip(),
                    "przychod": float(wiersz["przychod"]),
                    "koszt": float(wiersz["koszt"]),
                }
            )
    return zamowienia


def dostepne_regiony(sciezka):
    """Zwraca posortowana liste unikalnych regionow."""
    zamowienia = wczytaj_zamowienia(sciezka)
    regiony = sorted(list({z["region"] for z in zamowienia}))
    return regiony


def policz_wskazniki(sciezka, region=None):
    """Liczy wskazniki dla wybranego regionu lub wszystkich zamowien."""
    zamowienia = wczytaj_zamowienia(sciezka)

    if region is not None:
        zamowienia = [z for z in zamowienia if z["region"] == region]

    liczba_zamowien = len(zamowienia)
    przychod = round(sum(z["przychod"] for z in zamowienia), 2)
    koszt = round(sum(z["koszt"] for z in zamowienia), 2)

    if przychod == 0.0:
        marza = 0.0
    else:
        marza = round((przychod - koszt) / przychod, 4)

    return {
        "region": region,
        "liczba_zamowien": liczba_zamowien,
        "przychod": przychod,
        "koszt": koszt,
        "marza": marza,
    }