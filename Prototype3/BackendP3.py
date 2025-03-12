from datetime import date, time
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)

# Clases y métodos para serialización
class User:
    def __init__(self, id, username, password, email, role_id):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role_id = role_id

    def __str__(self):
        return f"{self.username}:{self.email}"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role_id": self.role_id
        }

class HistorialTapat:
    def __init__(self, data: date, hora: time, estat: str, totalHores: int):
        self.data = data
        self.hora = hora
        self.estat = estat
        self.totalHores = totalHores

    def __str__(self):
        return f"Data: {self.data}, Hora: {self.hora}, Estat: {self.estat}, Total hores: {self.totalHores}"

    def to_dict(self):
        return {
            "data": self.data.isoformat(),
            "hora": self.hora.isoformat(),
            "estat": self.estat,
            "totalHores": self.totalHores
        }

class LlistaHistorial:
    def __init__(self):
        self.historial = []

    def afegirHistorial(self, historial: HistorialTapat):
        self.historial.append(historial)

    def eliminarHistorial(self, data: date):
        self.historial = [h for h in self.historial if h.data != data]

    def buscarHistorial(self, data: date) -> HistorialTapat:
        for h in self.historial:
            if h.data == data:
                return h
        return None

    def to_dict(self):
        return [hist.to_dict() for hist in self.historial]

class Nen:
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
        return {
            "id": self.id,
            "child_id": self.child_id,
            "status_id": self.status_id,
            "user_id": self.user_id,
            "init": self.init,
            "end": self.end
        }

class Role:
    def __init__(self, id, type_rol):
        self.id = id
        self.type_rol = type_rol

    def __str__(self):
        return f"{self.id}:{self.type_rol}"

    def to_dict(self):
        return {
            "id": self.id,
            "type_rol": self.type_rol
        }

class Status:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.id}:{self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Treatment:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.id}:{self.name}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

comments = []

class Comment:
    def __init__(self, id, child_id, user_id, text, timestamp):
        self.id = id
        self.child_id = child_id
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "user_id": self.user_id,
            "text": self.text,
            "timestamp": self.timestamp.isoformat()
        }

@app.route('/comentarios', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    new_comment = Comment(
        id=len(comments) + 1,
        child_id=data['child_id'],
        user_id=get_jwt_identity(),
        text=data['text'],
        timestamp=datetime.now()
    )
    comments.append(new_comment)
    return jsonify(new_comment.to_dict()), 201

@app.route('/comentarios/<int:child_id>', methods=['GET'])
@jwt_required()
def get_comments(child_id):
    child_comments = [comment.to_dict() for comment in comments if comment.child_id == child_id]
    return jsonify(child_comments), 200

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

roles = [
    Role(id=1, type_rol='Admin'),
    Role(id=2, type_rol='Tutor Mare Pare'),
    Role(id=3, type_rol='Cuidador'),
    Role(id=4, type_rol='Seguiment')
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
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = next((user for user in users if user.username == username), None)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'])
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

# Endpoints para Niños
@app.route('/children', methods=['GET'])
def get_children():
    return jsonify([child.to_dict() for child in children]), 200

@app.route('/children/<child_name>', methods=['GET'])
def get_child(child_name):
    child = next((child for child in children if child.child_name == child_name), None)
    if child:
        return jsonify(child.to_dict()), 200
    return jsonify({"error": "Child not found"}), 404

@app.route('/children', methods=['POST'])
def create_child():
    data = request.get_json()
    new_child = Nen(id=len(children) + 1, child_name=data['child_name'], sleep_average=data['sleep_average'], treatment_id=data['treatment_id'], time=data['time'], informacioMedica=data['informacioMedica'], historialTapat=data['historialTapat'])
    children.append(new_child)
    return jsonify(new_child.to_dict()), 201

# Endpoints para Taps
@app.route('/taps', methods=['GET'])
def get_taps():
    return jsonify([tap.to_dict() for tap in taps]), 200

@app.route('/taps/<int:tap_id>', methods=['GET'])
def get_tap(tap_id):
    tap = next((tap for tap in taps if tap.id == tap_id), None)
    if tap:
        return jsonify(tap.to_dict()), 200
    return jsonify({"error": "Tap not found"}), 404

@app.route('/taps', methods=['POST'])
def create_tap():
    data = request.get_json()
    new_tap = Tap(id=len(taps) + 1, child_id=data['child_id'], status_id=data['status_id'], user_id=data['user_id'], init=data['init'], end=data['end'])
    taps.append(new_tap)
    return jsonify(new_tap.to_dict()), 201

# Endpoints para Roles
@app.route('/roles', methods=['GET'])
def get_roles():
    return jsonify([role.to_dict() for role in roles]), 200

@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = next((role for role in roles if role.id == role_id), None)
    if role:
        return jsonify(role.to_dict()), 200
    return jsonify({"error": "Role not found"}), 404

# Endpoints para Estados
@app.route('/statuses', methods=['GET'])
def get_statuses():
    return jsonify([status.to_dict() for status in statuses]), 200

@app.route('/statuses/<int:status_id>', methods=['GET'])
def get_status(status_id):
    status = next((status for status in statuses if status.id == status_id), None)
    if status:
        return jsonify(status.to_dict()), 200
    return jsonify({"error": "Status not found"}), 404

# Endpoints para Tratamientos
@app.route('/treatments', methods=['GET'])
def get_treatments():
    return jsonify([treatment.to_dict() for treatment in treatments]), 200

@app.route('/treatments/<int:treatment_id>', methods=['GET'])
def get_treatment(treatment_id):
    treatment = next((treatment for treatment in treatments if treatment.id == treatment_id), None)
    if treatment:
        return jsonify(treatment.to_dict()), 200
    return jsonify({"error": "Treatment not found"}), 404

# Endpoints para Historial
@app.route('/historial/<child_name>', methods=['GET'])
def get_historial(child_name):
    child = next((child for child in children if child.child_name == child_name), None)
    if child:
        return jsonify(child.historialTapat.to_dict()), 200
    return jsonify({"error": "Child not found"}), 404

@app.route('/historial/<child_name>/<date>', methods=['GET'])
def get_historial_by_date(child_name, date):
    child = next((child for child in children if child.child_name == child_name), None)
    if child:
        historial = next((hist for hist in child.historialTapat.historial if str(hist.data) == date), None)
        if historial:
            return jsonify(historial.to_dict()), 200
        return jsonify({"error": "Historial not found for the given date"}), 404
    return jsonify({"error": "Child not found"}), 404

@app.route('/recuperar-contrasena', methods=['POST'])
def recuperar_contrasena():
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
    # Suponemos que el médico tiene acceso a todos los niños
    return jsonify([child.to_dict() for child in children]), 200

@app.route('/medico/niños/<int:child_id>/historial', methods=['GET'])
def get_historial_medico(child_id):
    child = next((child for child in children if child.id == child_id), None)
    if child:
        return jsonify(child.historialTapat.to_dict()), 200
    return jsonify({"error": "Niño no encontrado"}), 404

# 3. Funcionalidades del Administrador
@app.route('/admin/usuarios', methods=['GET'])
def get_usuarios_admin():
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/admin/usuarios/<int:user_id>', methods=['DELETE'])
def delete_usuario_admin(user_id):
    global users
    user = next((user for user in users if user.id == user_id), None)
    if user:
        users = [u for u in users if u.id != user_id]
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/admin/usuarios', methods=['POST'])
def create_usuario_admin():
    data = request.get_json()
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'], role_id=data['role_id'])
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

@app.route('/admin/usuarios/<int:user_id>', methods=['PUT'])
def update_user_admin(user_id):
    data = request.get_json()
    user = next((user for user in users if user.id == user_id), None)
    if user:
        user.username = data.get('username', user.username)
        user.password = data.get('password', user.password)
        user.email = data.get('email', user.email)
        user.role_id = data.get('role_id', user.role_id)
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# Endpoint de Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', None)
    password = data.get('password', None)

    # Buscar el usuario en la lista de usuarios
    user = next((user for user in users if user.email == email and user.password == password), None)
    if user:
        # Crear un token de acceso
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, user=user.to_dict()), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    # Obtener el ID del usuario desde el token
    current_user_id = get_jwt_identity()
    user = next((user for user in users if user.id == current_user_id), None)
    if user:
        return jsonify(logged_in_as=user.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# 2. Crear un cuidador (Admin)
@app.route('/admin/cuidadores', methods=['POST'])
def create_cuidador_admin():
    data = request.get_json()
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'], role_id=4)  # Rol 4 = Cuidador
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

# 3. Ver lista de cuidadores (Médico)
@app.route('/medico/cuidadores', methods=['GET'])
def get_cuidadores_medico():
    cuidadores = [user for user in users if user.role_id == 4]  # Rol 4 = Cuidador
    return jsonify([user.to_dict() for user in cuidadores]), 200

# 4. Añadir un cuidador (Médico)
@app.route('/medico/cuidadores', methods=['POST'])
def add_cuidador_medico():
    data = request.get_json()
    new_user = User(id=len(users) + 1, username=data['username'], password=data['password'], email=data['email'], role_id=4)  # Rol 4 = Cuidador
    users.append(new_user)
    return jsonify(new_user.to_dict()), 201

# 5. Eliminar un cuidador (Médico)
@app.route('/medico/cuidadores/<int:user_id>', methods=['DELETE'])
def delete_cuidador_medico(user_id):
    global users
    user = next((user for user in users if user.id == user_id and user.role_id == 4), None)  # Solo cuidadores
    if user:
        users = [u for u in users if u.id != user_id]
        return jsonify({"message": "Cuidador eliminado correctamente"}), 200
    return jsonify({"error": "Cuidador no encontrado"}), 404

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)