from flask import request, abort

def parametr_int(nazwa, minimum, maksimum):
    if nazwa not in request.args:
        abort(400, description=f"Brak parametru {nazwa}")
    
    surowa_wartosc = request.args.get(nazwa)
    
    try:
        wartosc = int(surowa_wartosc)
    except (TypeError, ValueError):
        abort(400, description=f"Parametr {nazwa} musi być liczbą")
        
    if not (minimum <= wartosc <= maksimum):
        abort(422, description=f"Parametr {nazwa} poza zakresem {minimum}-{maksimum}")
        
    return wartosc