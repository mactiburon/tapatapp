import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler = RotatingFileHandler('tapatapp.log', maxBytes=1024*1024, backupCount=10)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)

import re
from datetime import datetime
from flask import jsonify

def validate_email(email):
    """
    Valida el formato de un email
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def validate_password(password):
    """
    Valida que la contraseña tenga al menos:
    - 8 caracteres
    - 1 mayúscula
    - 1 número
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

def format_date(date_str, from_format='%Y-%m-%d', to_format='%d/%m/%Y'):
    """
    Formatea una fecha de un formato a otro
    """
    try:
        date_obj = datetime.strptime(date_str, from_format)
        return date_obj.strftime(to_format)
    except ValueError:
        return None

def api_response(success=True, message="", data=None, status_code=200):
    """
    Formatea una respuesta API consistente
    """
    response = {
        "success": success,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def parse_request_data(request):
    """
    Parsea los datos de la request y devuelve un diccionario
    """
    if request.is_json:
        return request.get_json()
    elif request.form:
        return request.form.to_dict()
    else:
        return {}