import logging
import time
from datetime import date
from flask import Flask, g
from .config import KONFIGURACJE
from .converters import RegionConverter
from .errors import zarejestruj_obsluge_bledow
from .filters import zarejestruj_filtry
from .services import dostepne_regiony

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)
    zarejestruj_filtry(app)

    @app.context_processor
    def dane_wspolne():
        return {
            "regiony": dostepne_regiony(app.config["SCIEZKA_DANYCH"]),
            "rok_biezacy": date.today().year,
        }

    app.url_map.converters["region"] = RegionConverter

    from .routes_api import api_bp
    from .routes_panel import panel_bp

    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")

    @app.before_request
    def przed_zapytaniem():
        g.start = time.perf_counter()

    @app.after_request
    def po_zapytaniu(response):
        if hasattr(g, "start"):
            czas_ms = (time.perf_counter() - g.start) * 1000
            response.headers["X-Czas-Ms"] = f"{czas_ms:.2f}"
        return response

    zarejestruj_obsluge_bledow(app)

    return app