from flask import Blueprint, abort, current_app, jsonify, request
from .services import dostepne_regiony, policz_wskazniki

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