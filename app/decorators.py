from functools import wraps
from flask import abort, request

def wymagany_parametr(nazwa):
    def dekorator(f):
        @wraps(f)  
        def owinieta(*args, **kwargs):
            if nazwa not in request.args:
                abort(400, description=f"Brak parametru {nazwa}")
            return f(*args, **kwargs)
        return owinieta
    return dekorator