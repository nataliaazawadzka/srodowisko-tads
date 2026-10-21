from flask import Flask, abort, jsonify, request
from services import dostepne_regiony, policz_wskazniki

app = Flask(__name__)
SCIEZKA_DANYCH = "dane/zamowienia.csv"


@app.get("/")
def index():
    return "Panel wskaźników"


@app.get("/kpi")
def kpi_html():
    region = request.args.get("region")
    regiony = dostepne_regiony(SCIEZKA_DANYCH)

    if region not in regiony:
        abort(404, description=f"Nieznany region: {region}")

    wskazniki = policz_wskazniki(SCIEZKA_DANYCH, region)
    marza = wskazniki["marza"]

    return f"<h1>Wskaźniki: {region}</h1><p>Marża: {marza:.2%}</p>"


@app.get("/api/kpi")
def kpi_api():
    region = request.args.get("region")
    regiony = dostepne_regiony(SCIEZKA_DANYCH)

    if region not in regiony:
        abort(404, description=f"Nieznany region: {region}")

    wskazniki = policz_wskazniki(SCIEZKA_DANYCH, region)
    return jsonify(wskazniki)