from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    get_jwt_identity, create_refresh_token
)
from functools import wraps
import mysql.connector
from mysql.connector import Error, pooling
from datetime import datetime
import bcrypt
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import re

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key-change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400))  # 1 day
app.config['DB_POOL_SIZE'] = int(os.getenv('DB_POOL_SIZE', 5))
app.config['DB_POOL_NAME'] = 'mysql_pool'

# Initialize JWT
jwt = JWTManager(app)

# Database connection pool
db_pool = None

def initialize_db_pool():
    """Initialize database connection pool"""
    global db_pool
    try:
        db_pool = pooling.MySQLConnectionPool(
            pool_name=app.config['DB_POOL_NAME'],
            pool_size=app.config['DB_POOL_SIZE'],
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'tapatapp_bd'),
            port=int(os.getenv('DB_PORT', '3306'))
        )
        app.logger.info("Database connection pool initialized successfully")
    except Error as e:
        app.logger.error(f"Error initializing database pool: {e}")
        raise

# Configure logging
def configure_logging():
    """Configure application logging"""
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    
    # File handler with rotation
    file_handler = RotatingFileHandler('tapatapp.log', maxBytes=1024 * 1024, backupCount=10)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    
    # Add handlers to the app
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)

# Helper functions
def get_db_connection():
    """Get a connection from the pool"""
    try:
        return db_pool.get_connection()
    except Error as e:
        app.logger.error(f"Error getting database connection: {e}")
        return None

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(stored_hash, provided_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False
    return True

def role_required(roles):
    """Decorator to verify user has required role(s)"""
    if isinstance(roles, int):
        roles = [roles]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            conn = get_db_connection()
            if conn is None:
                return jsonify({"error": "Database connection failed"}), 500

            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT role_id FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                
                if not user or user['role_id'] not in roles:
                    return jsonify({"error": "Access forbidden: insufficient permissions"}), 403
                
                return f(*args, **kwargs)
            except Error as e:
                app.logger.error(f"Database error in role_required: {e}")
                return jsonify({"error": "Database error"}), 500
            finally:
                if conn:
                    conn.close()
        return decorated_function
    return decorator

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized", "message": str(error)}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden", "message": str(error)}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "message": str(error)}), 500

# API Endpoints

## Authentication Endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate user and return JWT tokens"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user or not verify_password(user['password'], password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Remove sensitive data before returning
        user.pop('password', None)
        
        access_token = create_access_token(identity=user['id'])
        refresh_token = create_refresh_token(identity=user['id'])
        
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user
        }), 200
    except Error as e:
        app.logger.error(f"Database error in login: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token using refresh token"""
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token), 200

@app.route('/api/auth/password-recovery', methods=['POST'])
def password_recovery():
    """Initiate password recovery process"""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            # In a real application, you would generate a token and send an email
            return jsonify({
                "message": "If an account with this email exists, a recovery link has been sent",
                "token": "simulated-recovery-token"  # In production, generate a real token
            }), 200
        else:
            # Don't reveal if email exists or not for security
            return jsonify({
                "message": "If an account with this email exists, a recovery link has been sent"
            }), 200
    except Error as e:
        app.logger.error(f"Database error in password_recovery: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

## User Management Endpoints
@app.route('/api/users', methods=['GET'])
@jwt_required()
@role_required([1])  # Only admin
def get_users():
    """Get all users (admin only)"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, role_id, created_at FROM users")
        users = cursor.fetchall()
        
        # Get role names for each user
        for user in users:
            cursor.execute("SELECT type_rol FROM roles WHERE id = %s", (user['role_id'],))
            role = cursor.fetchone()
            user['role_name'] = role['type_rol'] if role else 'Unknown'
        
        return jsonify(users), 200
    except Error as e:
        app.logger.error(f"Database error in get_users: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user details"""
    current_user_id = get_jwt_identity()
    
    # Users can only view their own profile unless they're admin
    if user_id != current_user_id:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
            current_user = cursor.fetchone()
            
            if not current_user or current_user['role_id'] != 1:  # Not admin
                return jsonify({"error": "Unauthorized"}), 403
        except Error as e:
            app.logger.error(f"Database error in get_user permission check: {e}")
            return jsonify({"error": "Database error"}), 500
        finally:
            if conn:
                conn.close()

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.role_id, r.type_rol as role_name, u.created_at
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.id = %s
        """, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify(user), 200
    except Error as e:
        app.logger.error(f"Database error in get_user: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/users', methods=['POST'])
@jwt_required()
@role_required([1])  # Only admin
def create_user():
    """Create a new user (admin only)"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password', 'role_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not validate_email(data['email']):
        return jsonify({"error": "Invalid email format"}), 400

    if not validate_password(data['password']):
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Check if email already exists
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({"error": "Email already in use"}), 400

        # Hash password
        hashed_password = hash_password(data['password'])

        # Insert new user
        cursor.execute("""
            INSERT INTO users (username, email, password, role_id)
            VALUES (%s, %s, %s, %s)
        """, (data['username'], data['email'], hashed_password, data['role_id']))
        
        conn.commit()
        user_id = cursor.lastrowid

        # Get the created user
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.role_id, r.type_rol as role_name, u.created_at
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.id = %s
        """, (user_id,))
        new_user = cursor.fetchone()

        return jsonify(new_user), 201
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in create_user: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user information"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Users can only update their own profile unless they're admin
    if user_id != current_user_id:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
            current_user = cursor.fetchone()
            
            if not current_user or current_user['role_id'] != 1:  # Not admin
                return jsonify({"error": "Unauthorized"}), 403
        except Error as e:
            app.logger.error(f"Database error in update_user permission check: {e}")
            return jsonify({"error": "Database error"}), 500
        finally:
            if conn:
                conn.close()

    # Validate input
    if 'email' in data and not validate_email(data['email']):
        return jsonify({"error": "Invalid email format"}), 400

    if 'password' in data and not validate_password(data['password']):
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        # Check if new email is already in use
        if 'email' in data:
            cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (data['email'], user_id))
            if cursor.fetchone():
                return jsonify({"error": "Email already in use"}), 400

        # Build update query
        update_fields = []
        values = []
        
        if 'username' in data:
            update_fields.append("username = %s")
            values.append(data['username'])
        
        if 'email' in data:
            update_fields.append("email = %s")
            values.append(data['email'])
        
        if 'password' in data:
            update_fields.append("password = %s")
            values.append(hash_password(data['password']))
        
        if 'role_id' in data and user_id != current_user_id:  # Only admin can change roles, and can't change their own
            update_fields.append("role_id = %s")
            values.append(data['role_id'])
        
        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(user_id)
        
        update_query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(update_query, values)
        conn.commit()

        # Get the updated user
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.role_id, r.type_rol as role_name, u.created_at
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.id = %s
        """, (user_id,))
        updated_user = cursor.fetchone()

        return jsonify(updated_user), 200
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in update_user: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required([1])  # Only admin
def delete_user(user_id):
    """Delete a user (admin only)"""
    current_user_id = get_jwt_identity()
    
    # Prevent admin from deleting themselves
    if user_id == current_user_id:
        return jsonify({"error": "Cannot delete your own account"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        # Delete user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in delete_user: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

## Child Management Endpoints
@app.route('/api/children', methods=['GET'])
@jwt_required()
def get_children():
    """Get list of children"""
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check user role to determine which children to show
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        if user['role_id'] == 3:  # Tutor
            cursor.execute("""
                SELECT c.*, t.username as tutor_name, cu.username as cuidador_name
                FROM children c
                LEFT JOIN users t ON c.tutor_id = t.id
                LEFT JOIN users cu ON c.cuidador_id = cu.id
                WHERE c.tutor_id = %s
            """, (current_user_id,))
        elif user['role_id'] == 4:  # Cuidador
            cursor.execute("""
                SELECT c.*, t.username as tutor_name, cu.username as cuidador_name
                FROM children c
                LEFT JOIN users t ON c.tutor_id = t.id
                LEFT JOIN users cu ON c.cuidador_id = cu.id
                WHERE c.cuidador_id = %s
            """, (current_user_id,))
        else:  # Admin or Médico
            cursor.execute("""
                SELECT c.*, t.username as tutor_name, cu.username as cuidador_name
                FROM children c
                LEFT JOIN users t ON c.tutor_id = t.id
                LEFT JOIN users cu ON c.cuidador_id = cu.id
            """)
        
        children = cursor.fetchall()
        return jsonify(children), 200
    except Error as e:
        app.logger.error(f"Database error in get_children: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/children/<int:child_id>', methods=['GET'])
@jwt_required()
def get_child(child_id):
    """Get child details"""
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # First get the child
        cursor.execute("""
            SELECT c.*, t.username as tutor_name, cu.username as cuidador_name
            FROM children c
            LEFT JOIN users t ON c.tutor_id = t.id
            LEFT JOIN users cu ON c.cuidador_id = cu.id
            WHERE c.id = %s
        """, (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({"error": "Child not found"}), 404
            
        # Check permissions
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        if user['role_id'] == 3 and child['tutor_id'] != current_user_id:  # Tutor but not this child's tutor
            return jsonify({"error": "Unauthorized"}), 403
            
        if user['role_id'] == 4 and child['cuidador_id'] != current_user_id:  # Cuidador but not this child's cuidador
            return jsonify({"error": "Unauthorized"}), 403
            
        return jsonify(child), 200
    except Error as e:
        app.logger.error(f"Database error in get_child: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/children', methods=['POST'])
@jwt_required()
@role_required([1, 2])  # Admin or Médico
def create_child():
    """Create a new child"""
    data = request.get_json()
    
    required_fields = ['child_name', 'edad', 'informacioMedica']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        
        # Insert new child
        cursor.execute("""
            INSERT INTO children (child_name, edad, informacioMedica, tutor_id, cuidador_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['child_name'],
            data['edad'],
            data['informacioMedica'],
            data.get('tutor_id'),
            data.get('cuidador_id')
        ))
        
        conn.commit()
        child_id = cursor.lastrowid

        # Get the created child
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, t.username as tutor_name, cu.username as cuidador_name
            FROM children c
            LEFT JOIN users t ON c.tutor_id = t.id
            LEFT JOIN users cu ON c.cuidador_id = cu.id
            WHERE c.id = %s
        """, (child_id,))
        new_child = cursor.fetchone()

        return jsonify(new_child), 201
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in create_child: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/children/<int:child_id>', methods=['PUT'])
@jwt_required()
@role_required([1, 2])  # Admin or Médico
def update_child(child_id):
    """Update child information"""
    data = request.get_json()
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Check if child exists
        cursor.execute("SELECT id FROM children WHERE id = %s", (child_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Child not found"}), 404

        # Build update query
        update_fields = []
        values = []
        
        if 'child_name' in data:
            update_fields.append("child_name = %s")
            values.append(data['child_name'])
        
        if 'edad' in data:
            update_fields.append("edad = %s")
            values.append(data['edad'])
        
        if 'informacioMedica' in data:
            update_fields.append("informacioMedica = %s")
            values.append(data['informacioMedica'])
        
        if 'tutor_id' in data:
            update_fields.append("tutor_id = %s")
            values.append(data['tutor_id'])
        
        if 'cuidador_id' in data:
            update_fields.append("cuidador_id = %s")
            values.append(data['cuidador_id'])
        
        if not update_fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(child_id)
        
        update_query = f"UPDATE children SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(update_query, values)
        conn.commit()

        # Get the updated child
        cursor.execute("""
            SELECT c.*, t.username as tutor_name, cu.username as cuidador_name
            FROM children c
            LEFT JOIN users t ON c.tutor_id = t.id
            LEFT JOIN users cu ON c.cuidador_id = cu.id
            WHERE c.id = %s
        """, (child_id,))
        updated_child = cursor.fetchone()

        return jsonify(updated_child), 200
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in update_child: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/children/<int:child_id>', methods=['DELETE'])
@jwt_required()
@role_required([1, 2])  # Admin or Médico
def delete_child(child_id):
    """Delete a child"""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        
        # Check if child exists
        cursor.execute("SELECT id FROM children WHERE id = %s", (child_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Child not found"}), 404

        # Delete child
        cursor.execute("DELETE FROM children WHERE id = %s", (child_id,))
        conn.commit()

        return jsonify({"message": "Child deleted successfully"}), 200
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in delete_child: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

## Sleep History Endpoints
@app.route('/api/children/<int:child_id>/history', methods=['GET'])
@jwt_required()
def get_child_history(child_id):
    """Get sleep history for a child"""
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # First check permissions
        cursor.execute("""
            SELECT c.id, c.tutor_id, c.cuidador_id
            FROM children c
            WHERE c.id = %s
        """, (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({"error": "Child not found"}), 404
            
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Check if user has access to this child's history
        if user['role_id'] == 3 and child['tutor_id'] != current_user_id:  # Tutor but not this child's tutor
            return jsonify({"error": "Unauthorized"}), 403
            
        if user['role_id'] == 4 and child['cuidador_id'] != current_user_id:  # Cuidador but not this child's cuidador
            return jsonify({"error": "Unauthorized"}), 403
        
        # Get history
        cursor.execute("""
            SELECT h.*, u.username as recorded_by
            FROM historial_tapat h
            LEFT JOIN users u ON h.user_id = u.id
            WHERE h.child_id = %s
            ORDER BY h.data DESC, h.hora DESC
        """, (child_id,))
        history = cursor.fetchall()
        
        return jsonify(history), 200
    except Error as e:
        app.logger.error(f"Database error in get_child_history: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/children/<int:child_id>/history', methods=['POST'])
@jwt_required()
def add_child_history(child_id):
    """Add sleep history record for a child"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['data', 'hora', 'estat', 'totalHores']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # First check permissions
        cursor.execute("""
            SELECT c.id, c.tutor_id, c.cuidador_id
            FROM children c
            WHERE c.id = %s
        """, (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({"error": "Child not found"}), 404
            
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Check if user can add history for this child
        if user['role_id'] == 3 and child['tutor_id'] != current_user_id:  # Tutor but not this child's tutor
            return jsonify({"error": "Unauthorized"}), 403
            
        if user['role_id'] == 4 and child['cuidador_id'] != current_user_id:  # Cuidador but not this child's cuidador
            return jsonify({"error": "Unauthorized"}), 403
        
        # Add history record
        cursor.execute("""
            INSERT INTO historial_tapat (child_id, user_id, data, hora, estat, totalHores)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            child_id,
            current_user_id,
            data['data'],
            data['hora'],
            data['estat'],
            data['totalHores']
        ))
        
        conn.commit()
        history_id = cursor.lastrowid

        # Get the created history record
        cursor.execute("""
            SELECT h.*, u.username as recorded_by
            FROM historial_tapat h
            LEFT JOIN users u ON h.user_id = u.id
            WHERE h.id = %s
        """, (history_id,))
        new_history = cursor.fetchone()

        return jsonify(new_history), 201
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in add_child_history: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

## Comment Endpoints
@app.route('/api/children/<int:child_id>/comments', methods=['GET'])
@jwt_required()
def get_child_comments(child_id):
    """Get comments for a child"""
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # First check permissions
        cursor.execute("""
            SELECT c.id, c.tutor_id, c.cuidador_id
            FROM children c
            WHERE c.id = %s
        """, (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({"error": "Child not found"}), 404
            
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Check if user has access to this child's comments
        if user['role_id'] == 3 and child['tutor_id'] != current_user_id:  # Tutor but not this child's tutor
            return jsonify({"error": "Unauthorized"}), 403
            
        if user['role_id'] == 4 and child['cuidador_id'] != current_user_id:  # Cuidador but not this child's cuidador
            return jsonify({"error": "Unauthorized"}), 403
        
        # Get comments
        cursor.execute("""
            SELECT c.*, u.username as author
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.child_id = %s
            ORDER BY c.timestamp DESC
        """, (child_id,))
        comments = cursor.fetchall()
        
        return jsonify(comments), 200
    except Error as e:
        app.logger.error(f"Database error in get_child_comments: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/children/<int:child_id>/comments', methods=['POST'])
@jwt_required()
def add_child_comment(child_id):
    """Add comment for a child"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('text'):
        return jsonify({"error": "Comment text is required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # First check permissions
        cursor.execute("""
            SELECT c.id, c.tutor_id, c.cuidador_id
            FROM children c
            WHERE c.id = %s
        """, (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({"error": "Child not found"}), 404
            
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Check if user can add comments for this child
        if user['role_id'] == 3 and child['tutor_id'] != current_user_id:  # Tutor but not this child's tutor
            return jsonify({"error": "Unauthorized"}), 403
            
        if user['role_id'] == 4 and child['cuidador_id'] != current_user_id:  # Cuidador but not this child's cuidador
            return jsonify({"error": "Unauthorized"}), 403
        
        # Add comment
        cursor.execute("""
            INSERT INTO comments (child_id, user_id, text, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (
            child_id,
            current_user_id,
            data['text'],
            datetime.now()
        ))
        
        conn.commit()
        comment_id = cursor.lastrowid

        # Get the created comment
        cursor.execute("""
            SELECT c.*, u.username as author
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """, (comment_id,))
        new_comment = cursor.fetchone()

        return jsonify(new_comment), 201
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in add_child_comment: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Delete a comment"""
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get the comment
        cursor.execute("""
            SELECT c.*, u.role_id as author_role
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """, (comment_id,))
        comment = cursor.fetchone()
        
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
            
        # Check permissions
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        current_user = cursor.fetchone()
        
        if not current_user:
            return jsonify({"error": "User not found"}), 404
            
        # Only allow deletion if:
        # 1. User is admin (role_id 1)
        # 2. User is the author of the comment
        # 3. User is médico (role_id 2) and the comment is about their child
        if (current_user['role_id'] != 1 and 
            comment['user_id'] != current_user_id and 
            not (current_user['role_id'] == 2 and comment['author_role'] in [3, 4])):
            return jsonify({"error": "Unauthorized"}), 403
        
        # Delete comment
        cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        conn.commit()

        return jsonify({"message": "Comment deleted successfully"}), 200
    except Error as e:
        conn.rollback()
        app.logger.error(f"Database error in delete_comment: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

## Stats and Reports Endpoints
@app.route('/api/children/<int:child_id>/stats', methods=['GET'])
@jwt_required()
def get_child_stats(child_id):
    """Get sleep statistics for a child"""
    current_user_id = get_jwt_identity()
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        
        # First check permissions
        cursor.execute("""
            SELECT c.id, c.tutor_id, c.cuidador_id
            FROM children c
            WHERE c.id = %s
        """, (child_id,))
        child = cursor.fetchone()
        
        if not child:
            return jsonify({"error": "Child not found"}), 404
            
        cursor.execute("SELECT role_id FROM users WHERE id = %s", (current_user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Check if user has access to this child's stats
        if user['role_id'] == 3 and child['tutor_id'] != current_user_id:  # Tutor but not this child's tutor
            return jsonify({"error": "Unauthorized"}), 403
            
        if user['role_id'] == 4 and child['cuidador_id'] != current_user_id:  # Cuidador but not this child's cuidador
            return jsonify({"error": "Unauthorized"}), 403
        
        # Get basic stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                AVG(totalHores) as avg_sleep_hours,
                MIN(totalHores) as min_sleep_hours,
                MAX(totalHores) as max_sleep_hours,
                SUM(CASE WHEN estat = 'Dormido' THEN 1 ELSE 0 END) as times_slept,
                SUM(CASE WHEN estat = 'Despierto' THEN 1 ELSE 0 END) as times_awake,
                SUM(CASE WHEN estat = 'Inquieto' THEN 1 ELSE 0 END) as times_restless
            FROM historial_tapat
            WHERE child_id = %s
        """, (child_id,))
        stats = cursor.fetchone()
        
        # Get sleep trends by day of week
        cursor.execute("""
            SELECT 
                DAYOFWEEK(data) as day_of_week,
                AVG(totalHores) as avg_sleep_hours
            FROM historial_tapat
            WHERE child_id = %s
            GROUP BY DAYOFWEEK(data)
            ORDER BY day_of_week
        """, (child_id,))
        day_stats = cursor.fetchall()
        
        # Get sleep trends by hour
        cursor.execute("""
            SELECT 
                HOUR(hora) as hour_of_day,
                AVG(totalHores) as avg_sleep_hours
            FROM historial_tapat
            WHERE child_id = %s
            GROUP BY HOUR(hora)
            ORDER BY hour_of_day
        """, (child_id,))
        hour_stats = cursor.fetchall()
        
        return jsonify({
            "basic_stats": stats,
            "day_of_week_stats": day_stats,
            "hour_of_day_stats": hour_stats
        }), 200
    except Error as e:
        app.logger.error(f"Database error in get_child_stats: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()

# Application startup
if __name__ == '__main__':
    configure_logging()
    initialize_db_pool()
    app.run(host='0.0.0.0', port=5000, debug=True)