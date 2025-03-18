from datetime import date, time, datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
)
from functools import wraps

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Cambia esto en un entorno de producción
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hora de expiración para el token de acceso
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 86400  # 1 día de expiración para el token de refresco
jwt = JWTManager(app)

# Clases y métodos para serialización
class User:
    """
    Clase que representa a un usuario en el sistema.

    Atributos:
        id (int): Identificador único del usuario.
        username (str): Nombre de usuario.
        password (str): Contraseña del usuario.
        email (str): Correo electrónico del usuario.
        role_id (int): Identificador del rol del usuario.
    """

    def __init__(self, id, username, password, email, role_id):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role_id = role_id

    def __str__(self):
        return f"{self.username}:{self.email}"

    def to_dict(self):
        """
        Convierte el objeto User en un diccionario.

        Returns:
            dict: Diccionario con los atributos del usuario.
        """
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role_id": self.role_id
        }

class HistorialTapat:
    """
    Clase que representa un historial de sueño de un niño.

    Atributos:
        data (date): Fecha del historial.
        hora (time): Hora del historial.
        estat (str): Estado del niño.
        totalHores (int): Total de horas de sueño.
    """

    def __init__(self, data: date, hora: time, estat: str, totalHores: int):
        self.data = data
        self.hora = hora
        self.estat = estat
        self.totalHores = totalHores

    def __str__(self):
        return f"Data: {self.data}, Hora: {self.hora}, Estat: {self.estat}, Total hores: {self.totalHores}"

    def to_dict(self):
        """
        Convierte el objeto HistorialTapat en un diccionario.

        Returns:
            dict: Diccionario con los atributos del historial.
        """
        return {
            "data": self.data.isoformat(),
            "hora": self.hora.isoformat(),
            "estat": self.estat,
            "totalHores": self.totalHores
        }

class LlistaHistorial:
    """
    Clase que representa una lista de historiales de sueño.

    Atributos:
        historial (list): Lista de objetos HistorialTapat.
    """

    def __init__(self):
        self.historial = []

    def afegirHistorial(self, historial: HistorialTapat):
        """
        Añade un historial a la lista.

        Args:
            historial (HistorialTapat): Historial a añadir.
        """
        self.historial.append(historial)

    def eliminarHistorial(self, data: date):
        """
        Elimina un historial de la lista por fecha.

        Args:
            data (date): Fecha del historial a eliminar.
        """
        self.historial = [h for h in self.historial if h.data != data]

    def buscarHistorial(self, data: date) -> HistorialTapat:
        """
        Busca un historial por fecha.

        Args:
            data (date): Fecha del historial a buscar.

        Returns:
            HistorialTapat: Historial encontrado o None si no existe.
        """
        for h in self.historial:
            if h.data == data:
                return h
        return None

    def to_dict(self):
        """
        Convierte la lista de historiales en una lista de diccionarios.

        Returns:
            list: Lista de diccionarios con los historiales.
        """
        return [hist.to_dict() for hist in self.historial]

class Nen:
    """
    Clase que representa a un niño en el sistema.

    Atributos:
        id (int): Identificador único del niño.
        child_name (str): Nombre del niño.
        sleep_average (int): Promedio de sueño.
        treatment_id (int): Identificador del tratamiento.
        time (int): Tiempo de tratamiento.
        informacioMedica (str): Información médica del niño.
        historialTapat (LlistaHistorial): Historial de sueño del niño.
    """

    def __init__(self, id, child_name, sleep_average, treatment_id, time, informacioMedica, historialTapat):
        self.id = id
        self.child_name = child_name
        self.sleep_average = sleep_average
        self.treatment_id = treatment_id
        self.time = time
        self.informacioMedica = informacioMedica
        self.historialTapat = historialTapat

    def __str__(self):
        return f"{self.child_name}:{self.sleep_average}:{self.treatment_id}:{self.time}:{self.informacioMedica}"

    def to_dict(self):
        """
        Convierte el objeto Nen en un diccionario.

        Returns:
            dict: Diccionario con los atributos del niño.
        """
        return {
            "id": self.id,
            "child_name": self.child_name,
            "sleep_average": self.sleep_average,
            "treatment_id": self.treatment_id,
            "time": self.time,
            "informacioMedica": self.informacioMedica,
            "historialTapat": self.historialTapat.to_dict()
        }

class Tap:
    """
    Clase que representa un tap (evento de sueño).

    Atributos:
        id (int): Identificador único del tap.
        child_id (int): Identificador del niño.
        status_id (int): Identificador del estado.
        user_id (int): Identificador del usuario.
        init (str): Hora de inicio.
        end (str): Hora de fin.
    """

    def __init__(self, id, child_id, status_id, user_id, init, end):
        self.id = id
        self.child_id = child_id
        self.status_id = status_id
        self.user_id = user_id
        self.init = init
        self.end = end

    def __str__(self):
        return f"{self.id}:{self.child_id}:{self.status_id}:{self.user_id}:{self.init}:{self.end}"

    def to_dict(self):
        """
        Convierte el objeto Tap en un diccionario.

        Returns:
            dict: Diccionario con los atributos del tap.
        """
        return {
            "id": self.id,
            "child_id": self.child_id,
            "status_id": self.status_id,
            "user_id": self.user_id,
            "init": self.init,
            "end": self.end
        }

class Role:
    """
    Clase que representa un rol en el sistema.

    Atributos:
        id (int): Identificador único del rol.
        type_rol (str): Tipo de rol.
    """

    def __init__(self, id, type_rol):
        self.id = id
        self.type_rol = type_rol

    def __str__(self):
        return f"{self.id}:{self.type_rol}"

    def to_dict(self):
        """
        Convierte el objeto Role en un diccionario.

        Returns:
            dict: Diccionario con los atributos del rol.
        """
        return {
            "id": self.id,
            "type_rol": self.type_rol
        }

class Status:
    """
    Clase que representa un estado en el sistema.

    Atributos:
        id (int): Identificador único del estado.
        name (str): Nombre del estado.
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.id}:{self.name}"

    def to_dict(self):
        """
        Convierte el objeto Status en un diccionario.

        Returns:
            dict: Diccionario con los atributos del estado.
        """
        return {
            "id": self.id,
            "name": self.name
        }

class Treatment:
    """
    Clase que representa un tratamiento en el sistema.

    Atributos:
        id (int): Identificador único del tratamiento.
        name (str): Nombre del tratamiento.
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.id}:{self.name}"

    def to_dict(self):
        """
        Convierte el objeto Treatment en un diccionario.

        Returns:
            dict: Diccionario con los atributos del tratamiento.
        """
        return {
            "id": self.id,
            "name": self.name
        }

comments = []

class Comment:
    """
    Clase que representa un comentario en el sistema.

    Atributos:
        id (int): Identificador único del comentario.
        child_id (int): Identificador del niño.
        user_id (int): Identificador del usuario.
        text (str): Texto del comentario.
        timestamp (datetime): Fecha y hora del comentario.
        parent_id (int): Identificador del comentario padre (opcional).
        important (bool): Indica si el comentario es importante.
    """

    def __init__(self, id, child_id, user_id, text, timestamp, parent_id=None, important=False):
        self.id = id
        self.child_id = child_id
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp
        self.parent_id = parent_id
        self.important = important

    def to_dict(self):
        """
        Convierte el objeto Comment en un diccionario.

        Returns:
            dict: Diccionario con los atributos del comentario.
        """
        return {
            "id": self.id,
            "child_id": self.child_id,
            "user_id": self.user_id,
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
            "parent_id": self.parent_id,
            "important": self.important
        }

def role_required(role):
    """
    Decorador para verificar si el usuario tiene el rol requerido.

    Args:
        role (int): Identificador del rol requerido.

    Returns:
        function: Función decorada.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = next((user for user in users if user.id == user_id), None)
            if user and user.role_id == role:
                return f(*args, **kwargs)
            return jsonify({"error": "Access forbidden: insufficient permissions"}), 403
        return decorated_function
    return decorator

# Endpoints para Comentarios
@app.route('/comentarios', methods=['POST'])
@jwt_required()
def add_comment():
    """
    Añade un nuevo comentario.

    Returns:
        JSON: El comentario añadido.
    """
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('text'):
        return jsonify({"error": "Invalid input"}), 400
    new_comment = Comment(
        id=len(comments) + 1,
        child_id=data['child_id'],
        user_id=get_jwt_identity(),
        text=data['text'],
        timestamp=datetime.now(),
        parent_id=data.get('parent_id'),
        important=data.get('important', False)
    )
    comments.append(new_comment)
    return jsonify(new_comment.to_dict()), 201

@app.route('/comentarios/<int:child_id>', methods=['GET'])
@jwt_required()
def get_comments(child_id):
    """
    Obtiene los comentarios de un niño.

    Args:
        child_id (int): Identificador del niño.

    Returns:
        JSON: Lista de comentarios.
    """
    child_comments = [comment.to_dict() for comment in comments if comment.child_id == child_id]
    return jsonify(child_comments), 200

@app.route('/comentarios/<int:comment_id>', methods=['PUT'])
@jwt_required()
def edit_comment(comment_id):
    """
    Edita un comentario existente.

    Args:
        comment_id (int): Identificador del comentario.

    Returns:
        JSON: El comentario editado.
    """
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"error": "Invalid input"}), 400
    comment = next((comment for comment in comments if comment.id == comment_id), None)
    if comment:
        comment.text = data.get('text', comment.text)
        comment.important = data.get('important', comment.important)
        return jsonify(comment.to_dict()), 200
    return jsonify({"error": "Comment not found"}), 404

@app.route('/comentarios/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """
    Elimina un comentario.

    Args:
        comment_id (int): Identificador del comentario.

    Returns:
        JSON: Mensaje de éxito o error.
    """
    global comments
    comment = next((comment for comment in comments if comment.id == comment_id), None)
    if comment:
        comments = [c for c in comments if c.id != comment_id]
        return jsonify({"message": "Comment deleted successfully"}), 200
    return jsonify({"error": "Comment not found"}), 404

# Datos de ejemplo
users = [
    User(id=1, username="admin", password="admin123", email="admin@example.com", role_id=1),
    User(id=2, username="medico1", password="medico123", email="medico@example.com", role_id=2),
    User(id=3, username="tutor1", password="tutor123", email="tutor@example.com", role_id=3)
]

roles = [
    Role(id=1, type_rol='Admin'),
    Role(id=2, type_rol='Médico'),
    Role(id=3, type_rol='Tutor'),
    Role(id=4, type_rol='Cuidador')
]

# Datos de ejemplo
historialCarolina = LlistaHistorial()
historialCarolina.afegirHistorial(HistorialTapat(data=date(2024, 12, 17), hora=time(19, 30), estat="mimido", totalHores=8))
historialCarolina.afegirHistorial(HistorialTapat(data=date(2024, 12, 18), hora=time(20, 00), estat="despertao", totalHores=2))

historialJacobo = LlistaHistorial()
historialJacobo.afegirHistorial(HistorialTapat(data=date(2024, 12, 17), hora=time(21, 00), estat="mimido", totalHores=10))
historialJacobo.afegirHistorial(HistorialTapat(data=date(2024, 12, 18), hora=time(18, 30), estat="despertao", totalHores=3))

children = [
    Nen(id=1, child_name="Carolina", sleep_average=8, treatment_id=1, time=6, informacioMedica="Al·lèrgia a la llet de vaca", historialTapat=historialCarolina),
    Nen(id=2, child_name="Jacobo", sleep_average=10, treatment_id=2, time=6, informacioMedica="No té cap al·lèrgia", historialTapat=historialJacobo)
]

taps = [
    Tap(id=1, child_id=1, status_id=1, user_id=1, init="2024-12-18T19:42:43", end="2024-12-18T20:42:43"),
    Tap(id=2, child_id=2, status_id=2, user_id=2, init="2024-12-18T21:42:43", end="2024-12-18T22:42:43")
]

statuses = [
    Status(id=1, name="mimido"),
    Status(id=2, name="despertao"),
    Status(id=3, name="tieneElparche"),
    Status(id=4, name="notieneElparche")
]

treatments = [
    Treatment(id=1, name='Horas'),
    Treatment(id=2, name='Porcentage')
]

# Endpoints para Usuarios
@app.route('/users', methods=['GET'])
def get_users():
    """
    Obtiene la lista de usuarios.

    Returns:
        JSON: Lista de usuarios.
    """
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    """
    Obtiene un usuario por su nombre de usuario.

    Args:
        username (str): Nombre de usuario.

    Returns:
        JSON: Información del usuario.
    """
    user = next((user for user in users if user.username == username), None)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """
    Crea un nuevo usuario.

    Returns:
        JSON: Información del usuario creado.
    """
    data = request.get_json()
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'])
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

# Endpoints para Niños
@app.route('/children', methods=['GET'])
def get_children():
    """
    Obtiene la lista de niños.

    Returns:
        JSON: Lista de niños.
    """
    return jsonify([child.to_dict() for child in children]), 200

@app.route('/children/<child_name>', methods=['GET'])
def get_child(child_name):
    """
    Obtiene un niño por su nombre.

    Args:
        child_name (str): Nombre del niño.

    Returns:
        JSON: Información del niño.
    """
    child = next((child for child in children if child.child_name.lower() == child_name.lower()), None)
    if child:
        return jsonify(child.to_dict()), 200
    return jsonify({"error": f"Child with name '{child_name}' not found"}), 404

@app.route('/children', methods=['POST'])
def create_child():
    """
    Crea un nuevo niño.

    Returns:
        JSON: Información del niño creado.
    """
    data = request.get_json()
    new_child = Nen(id=len(children) + 1, child_name=data['child_name'], sleep_average=data['sleep_average'], treatment_id=data['treatment_id'], time=data['time'], informacioMedica=data['informacioMedica'], historialTapat=data['historialTapat'])
    children.append(new_child)
    return jsonify(new_child.to_dict()), 201

# Endpoints para Taps
@app.route('/taps', methods=['GET'])
def get_taps():
    """
    Obtiene la lista de taps.

    Returns:
        JSON: Lista de taps.
    """
    return jsonify([tap.to_dict() for tap in taps]), 200

@app.route('/taps/<int:tap_id>', methods=['GET'])
def get_tap(tap_id):
    """
    Obtiene un tap por su ID.

    Args:
        tap_id (int): Identificador del tap.

    Returns:
        JSON: Información del tap.
    """
    # Buscar el tap por ID
    tap = next((tap for tap in taps if tap.id == tap_id), None)
    if tap:
        return jsonify(tap.to_dict()), 200
    return jsonify({"error": f"Tap with ID {tap_id} not found"}), 404

@app.route('/taps', methods=['POST'])
def create_tap():
    """
    Crea un nuevo tap.

    Returns:
        JSON: Información del tap creado.
    """
    data = request.get_json()
    new_tap = Tap(id=len(taps) + 1, child_id=data['child_id'], status_id=data['status_id'], user_id=data['user_id'], init=data['init'], end=data['end'])
    taps.append(new_tap)
    return jsonify(new_tap.to_dict()), 201

# Endpoints para Roles
@app.route('/roles', methods=['GET'])
def get_roles():
    """
    Obtiene la lista de roles.

    Returns:
        JSON: Lista de roles.
    """
    return jsonify([role.to_dict() for role in roles]), 200

@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    """
    Obtiene un rol por su ID.

    Args:
        role_id (int): Identificador del rol.

    Returns:
        JSON: Información del rol.
    """
    # Buscar el rol por ID
    role = next((role for role in roles if role.id == role_id), None)
    if role:
        return jsonify(role.to_dict()), 200
    return jsonify({"error": f"Role with ID {role_id} not found"}), 404

# Endpoints para Estados
@app.route('/statuses', methods=['GET'])
def get_statuses():
    """
    Obtiene la lista de estados.

    Returns:
        JSON: Lista de estados.
    """
    return jsonify([status.to_dict() for status in statuses]), 200

@app.route('/statuses/<int:status_id>', methods=['GET'])
def get_status(status_id):
    """
    Obtiene un estado por su ID.

    Args:
        status_id (int): Identificador del estado.

    Returns:
        JSON: Información del estado.
    """
    status = next((status for status in statuses if status.id == status_id), None)
    if status:
        return jsonify(status.to_dict()), 200
    return jsonify({"error": "Status not found"}), 404

# Endpoints para Tratamientos
@app.route('/treatments', methods=['GET'])
def get_treatments():
    """
    Obtiene la lista de tratamientos.

    Returns:
        JSON: Lista de tratamientos.
    """
    return jsonify([treatment.to_dict() for treatment in treatments]), 200

@app.route('/treatments/<int:treatment_id>', methods=['GET'])
def get_treatment(treatment_id):
    """
    Obtiene un tratamiento por su ID.

    Args:
        treatment_id (int): Identificador del tratamiento.

    Returns:
        JSON: Información del tratamiento.
    """
    treatment = next((treatment for treatment in treatments if treatment.id == treatment_id), None)
    if treatment:
        return jsonify(treatment.to_dict()), 200
    return jsonify({"error": "Treatment not found"}), 404

# Endpoints para Historial
@app.route('/historial/<child_name>', methods=['GET'])
def get_historial(child_name):
    """
    Obtiene el historial de sueño de un niño.

    Args:
        child_name (str): Nombre del niño.

    Returns:
        JSON: Historial de sueño del niño.
    """
    child = next((child for child in children if child.child_name == child_name), None)
    if child:
        return jsonify(child.historialTapat.to_dict()), 200
    return jsonify({"error": "Child not found"}), 404

@app.route('/historial/<child_name>/<date>', methods=['GET'])
def get_historial_by_date(child_name, date):
    """
    Obtiene el historial de sueño de un niño por fecha.

    Args:
        child_name (str): Nombre del niño.
        date (str): Fecha del historial.

    Returns:
        JSON: Historial de sueño del niño para la fecha especificada.
    """
    child = next((child for child in children if child.child_name == child_name), None)
    if child:
        historial = next((hist for hist in child.historialTapat.historial if str(hist.data) == date), None)
        if historial:
            return jsonify(historial.to_dict()), 200
        return jsonify({"error": "Historial not found for the given date"}), 404
    return jsonify({"error": "Child not found"}), 404

@app.route('/recuperar-contrasena', methods=['POST'])
def recuperar_contrasena():
    """
    Recupera la contraseña de un usuario.

    Returns:
        JSON: Mensaje de éxito o error.
    """
    data = request.get_json()
    email = data.get('email', None)
    user = next((user for user in users if user.email == email), None)
    if user:
        # Simulamos el envío de un correo con la contraseña
        return jsonify({"message": f"Se ha enviado un correo a {email} con instrucciones para recuperar la contraseña."}), 200
    return jsonify({"error": "Email no encontrado"}), 404

# 2. Funcionalidades del Médico
@app.route('/medico/niños', methods=['GET'])
def get_niños_medico():
    """
    Obtiene la lista de niños para el médico.

    Returns:
        JSON: Lista de niños.
    """
    if not children:
        return jsonify({"error": "No children found"}), 404
    return jsonify([child.to_dict() for child in children]), 200

@app.route('/medico/niños/<int:child_id>/historial', methods=['GET'])
def get_historial_medico(child_id):
    """
    Obtiene el historial de sueño de un niño para el médico.

    Args:
        child_id (int): Identificador del niño.

    Returns:
        JSON: Historial de sueño del niño.
    """
    # Buscar el niño por ID
    child = next((child for child in children if child.id == child_id), None)
    if child:
        # Validar si el historial está vacío
        if not child.historialTapat.historial:
            return jsonify({"error": f"No historial found for child with ID {child_id}"}), 404
        return jsonify(child.historialTapat.to_dict()), 200
    return jsonify({"error": f"Child with ID {child_id} not found"}), 404

# 3. Funcionalidades del Administrador
@app.route('/admin/usuarios', methods=['GET'])
@jwt_required()
@role_required(1)  # Only Admin
def get_usuarios_admin():
    """
    Obtiene la lista de usuarios para el administrador.

    Returns:
        JSON: Lista de usuarios.
    """
    if not users:
        return jsonify({"error": "No users found"}), 404
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/admin/usuarios/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(1)  # Only Admin
def delete_usuario_admin(user_id):
    """
    Elimina un usuario para el administrador.

    Args:
        user_id (int): Identificador del usuario.

    Returns:
        JSON: Mensaje de éxito o error.
    """
    global users
    user = next((user for user in users if user.id == user_id), None)
    if user:
        users = [u for u in users if u.id != user_id]
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/admin/usuarios', methods=['POST'])
@jwt_required()
@role_required(1)  # Only Admin
def create_usuario_admin():
    """
    Crea un nuevo usuario para el administrador.

    Returns:
        JSON: Información del usuario creado.
    """
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email') or not data.get('role_id'):
        return jsonify({"error": "Invalid input"}), 400
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'], role_id=data['role_id'])
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

@app.route('/admin/usuarios/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required(1)  # Only Admin
def update_user_admin(user_id):
    """
    Actualiza un usuario para el administrador.

    Args:
        user_id (int): Identificador del usuario.

    Returns:
        JSON: Información del usuario actualizado.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    user = next((user for user in users if user.id == user_id), None)
    if user:
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        user.email = data.get('email', user.email)
        user.role_id = data.get('role_id', user.role_id)
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/admin/usuarios/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required(1)  # Only Admin
def get_usuario_admin(user_id):
    """
    Obtiene un usuario por su ID para el administrador.

    Args:
        user_id (int): Identificador del usuario.

    Returns:
        JSON: Información del usuario.
    """
    # Buscar el usuario por ID
    user = next((user for user in users if user.id == user_id), None)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": f"User with ID {user_id} not found"}), 404

# Endpoint de Login
@app.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión en el sistema.

    Returns:
        JSON: Token de acceso y información del usuario.
    """
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)

    # Validar que los datos requeridos estén presentes
    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    # Buscar el usuario en la lista de usuarios
    user = next((user for user in users if user.email == email and user.password == password), None)
    if user:
        # Crear un token de acceso y un token de refresco
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        if not access_token or not refresh_token:
            app.logger.error("Error: No se pudieron generar los tokens.")
            return jsonify({"error": "Error interno del servidor"}), 500
        return jsonify(access_token=access_token, refresh_token=refresh_token, user=user.to_dict()), 200

    # Si las credenciales no coinciden
    app.logger.warning(f"Intento de inicio de sesión fallido para el email: {email}")
    return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresca el token de acceso.

    Returns:
        JSON: Nuevo token de acceso.
    """
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token), 200

@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    """
    Endpoint protegido que requiere autenticación.

    Returns:
        JSON: Información del usuario autenticado.
    """
    # Obtener el ID del usuario desde el token
    current_user_id = get_jwt_identity()
    user = next((user for user in users if user.id == current_user_id), None)
    if user:
        return jsonify(logged_in_as=user.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# 2. Crear un cuidador (Admin)
@app.route('/admin/cuidadores', methods=['POST'])
def create_cuidador_admin():
    """
    Crea un nuevo cuidador para el administrador.

    Returns:
        JSON: Información del cuidador creado.
    """
    data = request.get_json()
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'], role_id=4)  # Rol 4 = Cuidador
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

# 3. Ver lista de cuidadores (Médico)
@app.route('/medico/cuidadores', methods=['GET'])
@jwt_required()
@role_required(2)  # Only Médico
def get_cuidadores_medico():
    """
    Obtiene la lista de cuidadores para el médico.

    Returns:
        JSON: Lista de cuidadores.
    """
    cuidadores = [user for user in users if user.role_id == 4]  # Rol 4 = Cuidador
    return jsonify([user.to_dict() for user in cuidadores]), 200

# 4. Añadir un cuidador (Médico)
@app.route('/medico/cuidadores', methods=['POST'])
@jwt_required()
@role_required(2)  # Only Médico
def add_cuidador_medico():
    """
    Añade un nuevo cuidador para el médico.

    Returns:
        JSON: Información del cuidador añadido.
    """
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"error": "Invalid input"}), 400
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'], role_id=4)  # Rol 4 = Cuidador
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

# 5. Eliminar un cuidador (Médico)
@app.route('/medico/cuidadores/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(2)  # Only Médico
def delete_cuidador_medico(user_id):
    """
    Elimina un cuidador para el médico.

    Args:
        user_id (int): Identificador del cuidador.

    Returns:
        JSON: Mensaje de éxito o error.
    """
    global users
    user = next((user for user in users if user.id == user_id and user.role_id == 4), None)  # Solo cuidadores
    if user:
        users = [u for u in users if u.id != user_id]
        return jsonify({"message": "Cuidador eliminado correctamente"}), 200
    return jsonify({"error": "Cuidador no encontrado"}), 404

# Busqueda avançada
@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    """
    Realiza una búsqueda avanzada en el sistema.

    Returns:
        JSON: Resultados de la búsqueda.
    """
    query = request.args.get('query', '')
    results = {
        'users': [user.to_dict() for user in users if query.lower() in user.username.lower() or query.lower() in user.email.lower()],
        'children': [child.to_dict() for child in children if query.lower() in child.child_name.lower()],
        'taps': [tap.to_dict() for tap in taps if query.lower() in str(tap.id)],
        'roles': [role.to_dict() for role in roles if query.lower() in role.type_rol.lower()],
        'statuses': [status.to_dict() for status in statuses if query.lower() in status.name.lower()],
        'treatments': [treatment.to_dict() for treatment in treatments if query.lower() in treatment.name.lower()]
    }
    return jsonify(results), 200

# Modificar y añadir taps (Medico y Tutor)
@app.route('/tutores/taps', methods=['POST'])
@jwt_required()
@role_required(3)  # Only Tutor
def add_tap_tutor():
    """
    Añade un nuevo tap para el tutor.

    Returns:
        JSON: Información del tap añadido.
    """
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('status_id') or not data.get('init') or not data.get('end'):
        return jsonify({"error": "Invalid input"}), 400
    new_tap = Tap(id=len(taps) + 1, child_id=data['child_id'], status_id=data['status_id'], user_id=get_jwt_identity(), init=data['init'], end=data['end'])
    taps.append(new_tap)
    return jsonify(new_tap.to_dict()), 201

@app.route('/medicos/taps', methods=['POST'])
@jwt_required()
@role_required(2)  # Only Médico
def add_tap_medico():
    """
    Añade un nuevo tap para el médico.

    Returns:
        JSON: Información del tap añadido.
    """
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('status_id') or not data.get('init') or not data.get('end'):
        return jsonify({"error": "Invalid input"}), 400
    new_tap = Tap(id=len(taps) + 1, child_id=data['child_id'], status_id=data['status_id'], user_id=get_jwt_identity(), init=data['init'], end=data['end'])
    taps.append(new_tap)
    return jsonify(new_tap.to_dict()), 201

@app.route('/tutores/historial', methods=['POST'])
@jwt_required()
@role_required(3)  # Only Tutor
def add_historial_tutor():
    """
    Añade un nuevo historial para el tutor.

    Returns:
        JSON: Información del historial añadido.
    """
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('data') or not data.get('hora') or not data.get('estat') or not data.get('totalHores'):
        return jsonify({"error": "Invalid input"}), 400
    child = next((child for child in children if child.id == data['child_id']), None)
    if child:
        new_historial = HistorialTapat(data=data['data'], hora=data['hora'], estat=data['estat'], totalHores=data['totalHores'])
        child.historialTapat.afegirHistorial(new_historial)
        return jsonify(new_historial.to_dict()), 201
    return jsonify({"error": "Child not found"}), 404

@app.route('/medicos/historial', methods=['POST'])
@jwt_required()
@role_required(2)  # Only Médico
def add_historial_medico():
    """
    Añade un nuevo historial para el médico.

    Returns:
        JSON: Información del historial añadido.
    """
    data = request.get_json()
    if not data or not data.get('child_id') or not data.get('data') or not data.get('hora') or not data.get('estat') or not data.get('totalHores'):
        return jsonify({"error": "Invalid input"}), 400
    child = next((child for child in children if child.id == data['child_id']), None)
    if child:
        new_historial = HistorialTapat(data=data['data'], hora=data['hora'], estat=data['estat'], totalHores=data['totalHores'])
        child.historialTapat.afegirHistorial(new_historial)
        return jsonify(new_historial.to_dict()), 201
    return jsonify({"error": "Child not found"}), 404

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)