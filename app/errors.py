from flask import request, jsonify
from werkzeug.exceptions import HTTPException

def zarejestruj_obsluge_bledow(app):
    @app.errorhandler(HTTPException)
    def obsluz_blad(blad):
        if request.path.startswith("/api"):
            return jsonify(blad=blad.description, kod=blad.code), blad.code
        return f"<h1>{blad.code}</h1><p>Żądanie nie mogło zostać zrealizowane</p>", blad.code