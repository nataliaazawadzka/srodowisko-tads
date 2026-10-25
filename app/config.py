import os
from pathlib import Path

KATALOG = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    SCIEZKA_DANYCH = str(KATALOG / "dane" / "zamowienia.csv")
    DEBUG = False


class RozwojowaConfig(Config):
    DEBUG = True


KONFIGURACJE = {"rozwojowa": RozwojowaConfig, "produkcyjna": Config}