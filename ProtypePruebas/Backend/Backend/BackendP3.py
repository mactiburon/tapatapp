from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from utils.database import get_db_connection
from utils.helpers import configure_logging
from routes import auth, users, children, taps, comments, historial, admin, medico, tutor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key-change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400))  # 1 day

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(children.bp)
app.register_blueprint(taps.bp)
app.register_blueprint(comments.bp)
app.register_blueprint(historial.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(medico.bp)
app.register_blueprint(tutor.bp)

# Application startup
if __name__ == '__main__':
    configure_logging(app)
    app.run(host='0.0.0.0', port=5000, debug=True)