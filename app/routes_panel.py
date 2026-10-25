from flask import Blueprint, abort, current_app, request
from .services import dostepne_regiony, policz_wskazniki

panel_bp = Blueprint("panel", __name__)


@panel_bp.get("/")
def index():
    return "Panel wskaźników"


@panel_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    regiony = dostepne_regiony(sciezka)

    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")

    wskazniki = policz_wskazniki(sciezka, region)

    # Punkt 6: Zapis w dzienniku na poziomie INFO
    current_app.logger.info(
        "Obliczono wskaźniki dla regionu %s", wskazniki["region"]
    )

    marza = wskazniki["marza"]
    etykieta = region if region is not None else "Wszystkie"
    return f"<h1>Wskaźniki: {etykieta}</h1><p>Marża: {marza:.2%}</p>"