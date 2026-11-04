from flask import Blueprint, abort, current_app, request, redirect, url_for, render_template
from .services import dostepne_regiony, policz_wskazniki, zapisz_raport, raporty_roku, zestawienie_regionow
from datetime import date

panel_bp = Blueprint("panel", __name__)

ROK_DOMYSLNY = 2026


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
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", wskazniki["region"])

    return render_template(
        "panel.html",
        wskazniki=wskazniki,
        zestawienie=zestawienie_regionow(sciezka),
        dzisiaj=date.today()
    )


@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka)

    if kod not in regiony:
        abort(404, description=f"Nieznany region: {kod}")

    wskazniki = policz_wskazniki(sciezka, kod)

    return render_template(
        "panel.html",
        wskazniki=wskazniki,
        zestawienie=zestawienie_regionow(sciezka),
        dzisiaj=date.today()
    )


@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    n = len(raporty_roku(rok))
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {n}</p>"


@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "POST":
        rok = request.form.get("rok", type=int)
        region = request.form.get("region")
        
        sciezka = current_app.config["SCIEZKA_DANYCH"]
        regiony = dostepne_regiony(sciezka)
        
        if rok is None or not region or region not in regiony:
            abort(400, description="Niepoprawne dane formularza")
        if not (2020 <= rok <= 2030):
            abort(422, description="Rok poza zakresem 2020-2030")
            
        zapisz_raport(rok, region)
        return redirect(url_for("panel.raport", rok=rok), 303)
        
    return "Instrukcja zapisu raportu"


@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)