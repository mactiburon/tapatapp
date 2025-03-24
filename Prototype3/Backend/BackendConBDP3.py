from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
)
from functools import wraps
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date, time

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Cambia esto en un entorno de producción
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hora de expiración para el token de acceso
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # 1 día de expiración para el token de refresco
jwt = JWTManager(app)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        conexion = mysql.connector.connect(
            user='root',
            password='',
            host='127.0.0.1',
            database='tapatapp_bd',
            port='3306'
        )
        return conexion
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Decorador para verificar roles
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            conexion = get_db_connection()
            if conexion is None:
                return jsonify({"error": "Database connection failed"}), 500

            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT role_id FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            conexion.close()

            if user and user['role_id'] == role:
                return f(*args, **kwargs)
            return jsonify({"error": "Access forbidden: insufficient permissions"}), 403
        return decorated_function
    return decorator

# Endpoint de Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conexion.close()

    if user:
        access_token = create_access_token(identity=user['id'])
        refresh_token = create_refresh_token(identity=user['id'])
        return jsonify(access_token=access_token, refresh_token=refresh_token, user=user), 200

    return jsonify({"error": "Credenciales inválidas"}), 401

# Endpoint para obtener usuarios
@app.route('/users', methods=['GET'])
def get_users():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(users), 200

# Endpoint para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email') or not data.get('role_id'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)"
    values = (data['username'], data['password'], data['email'], data['role_id'])
    cursor.execute(query, values)
    conexion.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_user = {
        "id": user_id,
        "username": data['username'],
        "password": data['password'],
        "email": data['email'],
        "role_id": data['role_id']
    }
    return jsonify(new_user), 201

# Endpoint para obtener un usuario por nombre de usuario
@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conexion.close()

    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# Endpoint para obtener niños
@app.route('/children', methods=['GET'])
def get_children():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM children")
    children = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(children), 200

# Endpoint para crear un niño
@app.route('/children', methods=['POST'])
def create_child():
    data = request.get_json()
    if not data or not data.get('child_name') or not data.get('sleep_average') or not data.get('treatment_id') or not data.get('time') or not data.get('informacioMedica'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO children (child_name, sleep_average, treatment_id, time, informacioMedica) VALUES (%s, %s, %s, %s, %s)"
    values = (data['child_name'], data['sleep_average'], data['treatment_id'], data['time'], data['informacioMedica'])
    cursor.execute(query, values)
    conexion.commit()
    child_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_child = {
        "id": child_id,
        "child_name": data['child_name'],
        "sleep_average": data['sleep_average'],
        "treatment_id": data['treatment_id'],
        "time": data['time'],
        "informacioMedica": data['informacioMedica']
    }
    return jsonify(new_child), 201

# Endpoint para obtener un niño por nombre
@app.route('/children/<child_name>', methods=['GET'])
def get_child(child_name):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM children WHERE child_name = %s"
    cursor.execute(query, (child_name,))
    child = cursor.fetchone()
    cursor.close()
    conexion.close()

    if child:
        return jsonify(child), 200
    return jsonify({"error": f"Child with name '{child_name}' not found"}), 404

# Endpoint para obtener historial de sueño de un niño
@app.route('/historial/<child_name>', methods=['GET'])
def get_historial(child_name):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT h.* FROM historial_tapat h
        JOIN children c ON h.child_id = c.id
        WHERE c.child_name = %s
    """
    cursor.execute(query, (child_name,))
    historial = cursor.fetchall()
    cursor.close()
    conexion.close()

    if historial:
        return jsonify(historial), 200
    return jsonify({"error": "Historial not found"}), 404

# Endpoint para añadir un comentario
@app.route('/comentarios', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('text'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO comments (child_id, user_id, text, timestamp) VALUES (%s, %s, %s, %s)"
    values = (data['child_id'], get_jwt_identity(), data['text'], datetime.now())
    cursor.execute(query, values)
    conexion.commit()
    comment_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_comment = {
        "id": comment_id,
        "child_id": data['child_id'],
        "user_id": get_jwt_identity(),
        "text": data['text'],
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(new_comment), 201

# Endpoint para obtener comentarios de un niño
@app.route('/comentarios/<int:child_id>', methods=['GET'])
@jwt_required()
def get_comments(child_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM comments WHERE child_id = %s"
    cursor.execute(query, (child_id,))
    comments = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(comments), 200

# Endpoint para editar un comentario
@app.route('/comentarios/<int:comment_id>', methods=['PUT'])
@jwt_required()
def edit_comment(comment_id):
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "UPDATE comments SET text = %s, important = %s WHERE id = %s"
    values = (data['text'], data.get('important', False), comment_id)
    cursor.execute(query, values)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"message": "Comment updated successfully"}), 200

# Endpoint para eliminar un comentario
@app.route('/comentarios/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "DELETE FROM comments WHERE id = %s"
    cursor.execute(query, (comment_id,))
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"message": "Comment deleted successfully"}), 200

# Endpoint para obtener roles
@app.route('/roles', methods=['GET'])
def get_roles():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(roles), 200

# Endpoint para obtener estados
@app.route('/statuses', methods=['GET'])
def get_statuses():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM statuses")
    statuses = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(statuses), 200

# Endpoint para obtener tratamientos
@app.route('/treatments', methods=['GET'])
def get_treatments():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM treatments")
    treatments = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(treatments), 200

# Endpoint para obtener taps
@app.route('/taps', methods=['GET'])
def get_taps():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM taps")
    taps = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(taps), 200

# Endpoint para crear un tap
@app.route('/taps', methods=['POST'])
@jwt_required()
def create_tap():
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('status_id') or not data.get('init') or not data.get('end'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO taps (child_id, status_id, user_id, init, end) VALUES (%s, %s, %s, %s, %s)"
    values = (data['child_id'], data['status_id'], get_jwt_identity(), data['init'], data['end'])
    cursor.execute(query, values)
    conexion.commit()
    tap_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_tap = {
        "id": tap_id,
        "child_id": data['child_id'],
        "status_id": data['status_id'],
        "user_id": get_jwt_identity(),
        "init": data['init'],
        "end": data['end']
    }
    return jsonify(new_tap), 201

# Endpoint para obtener un tap por ID
@app.route('/taps/<int:tap_id>', methods=['GET'])
def get_tap(tap_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM taps WHERE id = %s"
    cursor.execute(query, (tap_id,))
    tap = cursor.fetchone()
    cursor.close()
    conexion.close()

    if tap:
        return jsonify(tap), 200
    return jsonify({"error": f"Tap with ID {tap_id} not found"}), 404

# Endpoint para eliminar un tap
@app.route('/taps/<int:tap_id>', methods=['DELETE'])
@jwt_required()
def delete_tap(tap_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "DELETE FROM taps WHERE id = %s"
    cursor.execute(query, (tap_id,))
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"message": "Tap deleted successfully"}), 200

# Endpoint para obtener historial por fecha
@app.route('/historial/<child_name>/<date>', methods=['GET'])
def get_historial_by_date(child_name, date):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    query = """
        SELECT h.* FROM historial_tapat h
        JOIN children c ON h.child_id = c.id
        WHERE c.child_name = %s AND h.data = %s
    """
    cursor.execute(query, (child_name, date))
    historial = cursor.fetchone()
    cursor.close()
    conexion.close()

    if historial:
        return jsonify(historial), 200
    return jsonify({"error": "Historial not found for the given date"}), 404

# Endpoint para recuperar contraseña
@app.route('/recuperar-contrasena', methods=['POST'])
def recuperar_contrasena():
    data = request.get_json()
    email = data.get('email', None)

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conexion.close()

    if user:
        # Simulamos el envío de un correo con la contraseña
        return jsonify({"message": f"Se ha enviado un correo a {email} con instrucciones para recuperar la contraseña."}), 200
    return jsonify({"error": "Email no encontrado"}), 404

# Endpoint para obtener niños (Médico)
@app.route('/medico/niños', methods=['GET'])
@jwt_required()
@role_required(2)  # Only Médico
def get_niños_medico():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM children")
    children = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not children:
        return jsonify({"error": "No children found"}), 404
    return jsonify(children), 200

# Endpoint para obtener historial de un niño (Médico)
@app.route('/medico/niños/<int:child_id>/historial', methods=['GET'])
@jwt_required()
@role_required(2)  # Only Médico
def get_historial_medico(child_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM historial_tapat WHERE child_id = %s", (child_id,))
    historial = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not historial:
        return jsonify({"error": f"No historial found for child with ID {child_id}"}), 404
    return jsonify(historial), 200

# Endpoint para obtener usuarios (Admin)
@app.route('/admin/usuarios', methods=['GET'])
@jwt_required()
@role_required(1)  # Only Admin
def get_usuarios_admin():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conexion.close()

    if not users:
        return jsonify({"error": "No users found"}), 404
    return jsonify(users), 200

# Endpoint para eliminar un usuario (Admin)
@app.route('/admin/usuarios/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(1)  # Only Admin
def delete_usuario_admin(user_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"message": "Usuario eliminado correctamente"}), 200

# Endpoint para crear un usuario (Admin)
@app.route('/admin/usuarios', methods=['POST'])
@jwt_required()
@role_required(1)  # Only Admin
def create_usuario_admin():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email') or not data.get('role_id'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)"
    values = (data['username'], data['password'], data['email'], data['role_id'])
    cursor.execute(query, values)
    conexion.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_user = {
        "id": user_id,
        "username": data['username'],
        "password": data['password'],
        "email": data['email'],
        "role_id": data['role_id']
    }
    return jsonify(new_user), 201

# Endpoint para actualizar un usuario (Admin)
@app.route('/admin/usuarios/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(1)  # Only Admin
def update_user_admin(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "UPDATE users SET username = %s, password = %s, email = %s, role_id = %s WHERE id = %s"
    values = (data.get('username'), data.get('password'), data.get('email'), data.get('role_id'), user_id)
    cursor.execute(query, values)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"message": "Usuario actualizado correctamente"}), 200

# Endpoint para obtener un usuario (Admin)
@app.route('/admin/usuarios/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required(1)  # Only Admin
def get_usuario_admin(user_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conexion.close()

    if user:
        return jsonify(user), 200
    return jsonify({"error": f"User with ID {user_id} not found"}), 404

# Endpoint para crear un cuidador (Admin)
@app.route('/admin/cuidadores', methods=['POST'])
@jwt_required()
@role_required(1)  # Only Admin
def create_cuidador_admin():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, 4)"  # Rol 4 = Cuidador
    values = (data['username'], data['password'], data['email'])
    cursor.execute(query, values)
    conexion.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_user = {
        "id": user_id,
        "username": data['username'],
        "password": data['password'],
        "email": data['email'],
        "role_id": 4
    }
    return jsonify(new_user), 201

# Endpoint para obtener cuidadores (Médico)
@app.route('/medico/cuidadores', methods=['GET'])
@jwt_required()
@role_required(2)  # Only Médico
def get_cuidadores_medico():
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE role_id = 4")  # Rol 4 = Cuidador
    cuidadores = cursor.fetchall()
    cursor.close()
    conexion.close()

    return jsonify(cuidadores), 200

# Endpoint para añadir un cuidador (Médico)
@app.route('/medico/cuidadores', methods=['POST'])
@jwt_required()
@role_required(2)  # Only Médico
def add_cuidador_medico():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, 4)"  # Rol 4 = Cuidador
    values = (data['username'], data['password'], data['email'])
    cursor.execute(query, values)
    conexion.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_user = {
        "id": user_id,
        "username": data['username'],
        "password": data['password'],
        "email": data['email'],
        "role_id": 4
    }
    return jsonify(new_user), 201

# Endpoint para eliminar un cuidador (Médico)
@app.route('/medico/cuidadores/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(2)  # Only Médico
def delete_cuidador_medico(user_id):
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "DELETE FROM users WHERE id = %s AND role_id = 4"  # Solo cuidadores
    cursor.execute(query, (user_id,))
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"message": "Cuidador eliminado correctamente"}), 200

# Endpoint para búsqueda avanzada
@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('query', '')
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    
    # Buscar en usuarios
    cursor.execute("SELECT * FROM users WHERE username LIKE %s OR email LIKE %s", (f"%{query}%", f"%{query}%"))
    users = cursor.fetchall()
    
    # Buscar en niños
    cursor.execute("SELECT * FROM children WHERE child_name LIKE %s", (f"%{query}%",))
    children = cursor.fetchall()
    
    # Buscar en taps
    cursor.execute("SELECT * FROM taps WHERE id LIKE %s", (f"%{query}%",))
    taps = cursor.fetchall()
    
    # Buscar en roles
    cursor.execute("SELECT * FROM roles WHERE type_rol LIKE %s", (f"%{query}%",))
    roles = cursor.fetchall()
    
    # Buscar en estados
    cursor.execute("SELECT * FROM statuses WHERE name LIKE %s", (f"%{query}%",))
    statuses = cursor.fetchall()
    
    # Buscar en tratamientos
    cursor.execute("SELECT * FROM treatments WHERE name LIKE %s", (f"%{query}%",))
    treatments = cursor.fetchall()
    
    cursor.close()
    conexion.close()

    results = {
        'users': users,
        'children': children,
        'taps': taps,
        'roles': roles,
        'statuses': statuses,
        'treatments': treatments
    }
    return jsonify(results), 200

# Endpoint para añadir un tap (Tutor)
@app.route('/tutores/taps', methods=['POST'])
@jwt_required()
@role_required(3)  # Only Tutor
def add_tap_tutor():
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('status_id') or not data.get('init') or not data.get('end'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO taps (child_id, status_id, user_id, init, end) VALUES (%s, %s, %s, %s, %s)"
    values = (data['child_id'], data['status_id'], get_jwt_identity(), data['init'], data['end'])
    cursor.execute(query, values)
    conexion.commit()
    tap_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_tap = {
        "id": tap_id,
        "child_id": data['child_id'],
        "status_id": data['status_id'],
        "user_id": get_jwt_identity(),
        "init": data['init'],
        "end": data['end']
    }
    return jsonify(new_tap), 201

# Endpoint para añadir un tap (Médico)
@app.route('/medicos/taps', methods=['POST'])
@jwt_required()
@role_required(2)  # Only Médico
def add_tap_medico():
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('status_id') or not data.get('init') or not data.get('end'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO taps (child_id, status_id, user_id, init, end) VALUES (%s, %s, %s, %s, %s)"
    values = (data['child_id'], data['status_id'], get_jwt_identity(), data['init'], data['end'])
    cursor.execute(query, values)
    conexion.commit()
    tap_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_tap = {
        "id": tap_id,
        "child_id": data['child_id'],
        "status_id": data['status_id'],
        "user_id": get_jwt_identity(),
        "init": data['init'],
        "end": data['end']
    }
    return jsonify(new_tap), 201

# Endpoint para añadir historial (Tutor)
@app.route('/tutores/historial', methods=['POST'])
@jwt_required()
@role_required(3)  # Only Tutor
def add_historial_tutor():
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('data') or not data.get('hora') or not data.get('estat') or not data.get('totalHores'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO historial_tapat (child_id, data, hora, estat, totalHores) VALUES (%s, %s, %s, %s, %s)"
    values = (data['child_id'], data['data'], data['hora'], data['estat'], data['totalHores'])
    cursor.execute(query, values)
    conexion.commit()
    historial_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_historial = {
        "id": historial_id,
        "child_id": data['child_id'],
        "data": data['data'],
        "hora": data['hora'],
        "estat": data['estat'],
        "totalHores": data['totalHores']
    }
    return jsonify(new_historial), 201

# Endpoint para añadir historial (Médico)
@app.route('/medicos/historial', methods=['POST'])
@jwt_required()
@role_required(2)  # Only Médico
def add_historial_medico():
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('data') or not data.get('hora') or not data.get('estat') or not data.get('totalHores'):
        return jsonify({"error": "Invalid input"}), 400

    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor()
    query = "INSERT INTO historial_tapat (child_id, data, hora, estat, totalHores) VALUES (%s, %s, %s, %s, %s)"
    values = (data['child_id'], data['data'], data['hora'], data['estat'], data['totalHores'])
    cursor.execute(query, values)
    conexion.commit()
    historial_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    new_historial = {
        "id": historial_id,
        "child_id": data['child_id'],
        "data": data['data'],
        "hora": data['hora'],
        "estat": data['estat'],
        "totalHores": data['totalHores']
    }
    return jsonify(new_historial), 201

# Endpoint protegido
@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    current_user_id = get_jwt_identity()
    conexion = get_db_connection()
    if conexion is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (current_user_id,))
    user = cursor.fetchone()
    cursor.close()
    conexion.close()

    if user:
        return jsonify(logged_in_as=user), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# Endpoint para refrescar token
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
