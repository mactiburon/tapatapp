from .auth import auth_bp
from .users import users_bp
from .children import children_bp
from .taps import taps_bp
from .comments import comments_bp
from .historial import historial_bp
from .admin import admin_bp
from .medico import medico_bp
from .tutor import tutor_bp

__all__ = [
    'auth_bp',
    'users_bp',
    'children_bp',
    'taps_bp',
    'comments_bp',
    'historial_bp',
    'admin_bp',
    'medico_bp',
    'tutor_bp'
]