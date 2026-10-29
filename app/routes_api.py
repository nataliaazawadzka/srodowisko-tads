from flask import Blueprint, abort, current_app, jsonify, request
from app.validators import parametr_int
from app.decorators import wymagany_parametr
from .services import dostepne_regiony, policz_wskazniki, raporty_roku

api_bp = Blueprint("api", __name__)


@api_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    region = request.args.get("region")
    regiony = dostepne_regiony(sciezka)

    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")

    wskazniki = policz_wskazniki(sciezka, region)
    return jsonify(wskazniki)

@api_bp.get("/raporty")
@wymagany_parametr("rok")
def raporty():
    rok = parametr_int("rok", 2020, 2030)
    return jsonify(rok=rok, raporty=raporty_roku(rok))