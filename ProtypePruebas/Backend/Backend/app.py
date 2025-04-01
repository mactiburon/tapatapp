from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
import logging
from datetime import timedelta

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importación de blueprints
from routes.auth import auth_bp
from routes.users import users_bp
from routes.children import children_bp
from routes.taps import taps_bp
from routes.comments import comments_bp
from routes.historial import historial_bp
from routes.admin import admin_bp
from routes.medico import medico_bp
from routes.tutor import tutor_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configuración JWT adicional
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Inicializar JWT
    jwt = JWTManager(app)
    
    # Callback para token inválido
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'invalid_token',
            'message': 'Token de acceso no válido'
        }), 401
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(children_bp, url_prefix='/api/children')
    app.register_blueprint(taps_bp, url_prefix='/api/taps')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(historial_bp, url_prefix='/api/historial')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(medico_bp, url_prefix='/api/medico')
    app.register_blueprint(tutor_bp, url_prefix='/api/tutor')
    
    # Ruta de verificación de salud
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Servidor operativo'})
    
    # Manejador de errores global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'Recurso no encontrado'}), 404
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )