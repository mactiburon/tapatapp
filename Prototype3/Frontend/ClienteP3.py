import requests
import json

# Simulación de localStorage en Python
class LocalStorage:
    storage = {}

    @staticmethod
    def set_item(key, value):
        LocalStorage.storage[key] = value

    @staticmethod
    def get_item(key):
        return LocalStorage.storage.get(key, None)

    @staticmethod
    def remove_item(key):
        if key in LocalStorage.storage:
            del LocalStorage.storage[key]

# Clases de dominio
class Usuario:
    """
    Clase que representa a un usuario en el sistema.

    Atributos:
        id (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        apellido (str): Apellido del usuario.
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
    """

    def __init__(self, id, nombre, apellido, email, password):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password

    def __str__(self):
        return f"Nombre: {self.nombre} {self.apellido}, Email: {self.email}"

class Nen:
    """
    Clase que representa a un niño en el sistema.

    Atributos:
        id (int): Identificador único del niño.
        child_name (str): Nombre del niño.
        edad (int): Edad del niño.
        fecha_nacimiento (str): Fecha de nacimiento del niño.
        informacioMedica (str): Información médica del niño.
        historialTapat (list): Historial de sueño del niño.
    """

    def __init__(self, id, child_name, edad=None, fecha_nacimiento=None, informacioMedica=None, historialTapat=None):
        self.id = id
        self.child_name = child_name
        self.edad = edad
        self.fecha_nacimiento = fecha_nacimiento
        self.informacioMedica = informacioMedica
        self.historialTapat = historialTapat

    def __str__(self):
        info = f"Nombre: {self.child_name}"
        if self.edad:
            info += f", Edad: {self.edad}"
        if self.fecha_nacimiento:
            info += f", Fecha de Nacimiento: {self.fecha_nacimiento}"
        if self.informacioMedica:
            info += f", Información Médica: {self.informacioMedica}"
        if self.historialTapat:
            info += "\nHistorial de sueño:"
            for hist in self.historialTapat:
                info += f"\n- Fecha: {hist.get('data')}, Hora: {hist.get('hora')}, Estado: {hist.get('estat')}, Total horas: {hist.get('totalHores')}"
        return info

# DAOs (Data Access Objects)
class UsuarioDAO:
    """
    Clase que maneja las operaciones de acceso a datos para los usuarios.
    """

    @staticmethod
    def logout():
        """
        Cierra la sesión del usuario eliminando el token y la información del usuario del almacenamiento local.
        """
        LocalStorage.remove_item('access_token')
        LocalStorage.remove_item('refresh_token')
        LocalStorage.remove_item('user')
        print("Sesión cerrada. Token y usuario eliminados.")

    @staticmethod
    def login(email, password):
        """
        Inicia sesión en el sistema.

        Args:
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del usuario.

        Returns:
            dict: Información del usuario y tokens.
        """
        try:
            response = requests.post('http://localhost:5000/login', json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and 'refresh_token' in data and 'user' in data:
                    LocalStorage.set_item('access_token', data['access_token'])
                    LocalStorage.set_item('refresh_token', data['refresh_token'])
                    LocalStorage.set_item('user', json.dumps(data['user']))
                    # Verificar si los tokens se guardaron correctamente
                    if not LocalStorage.get_item('access_token') or not LocalStorage.get_item('refresh_token'):
                        print("Error: Los tokens no se guardaron correctamente en LocalStorage.")
                    else:
                        print("Login exitoso. Token y usuario guardados.")
                    return data['user']
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def registrar(nombre, apellido, email, password):
        """
        Registra un nuevo usuario en el sistema.

        Args:
            nombre (str): Nombre del usuario.
            apellido (str): Apellido del usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del usuario.

        Returns:
            dict: Información del usuario registrado.
        """
        try:
            response = requests.post('http://localhost:5000/registro', json={
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "password": password
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def recuperar_contrasena(email):
        """
        Recupera la contraseña de un usuario.

        Args:
            email (str): Correo electrónico del usuario.

        Returns:
            dict: Mensaje de éxito o error.
        """
        try:
            response = requests.post('http://localhost:5000/recuperar-contrasena', json={"email": email})
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

class NenDAO:
    """
    Clase que maneja las operaciones de acceso a datos para los niños.
    """

    @staticmethod
    def get_child_by_name(child_name):
        """
        Obtiene un niño por su nombre.

        Args:
            child_name (str): Nombre del niño.

        Returns:
            Nen: Información del niño.
        """
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                print("Error: No hay token de acceso. Inicie sesión primero.")
                return None

            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f'http://localhost:5000/children/{child_name}', headers=headers)
            if response.status_code == 200:
                child_data = response.json()
                return Nen(
                    id=child_data.get('id'),
                    child_name=child_data.get('child_name'),
                    edad=child_data.get('edad'),
                    fecha_nacimiento=child_data.get('fecha_nacimiento'),
                    informacioMedica=child_data.get('informacioMedica'),
                    historialTapat=child_data.get('historialTapat')
                )
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def get_all_children():
        """
        Obtiene la lista de niños.

        Returns:
            list: Lista de niños.
        """
        try:
            response = requests.get('http://localhost:5000/medico/niños')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def get_child_historial(child_id):
        """
        Obtiene el historial de sueño de un niño.

        Args:
            child_id (int): Identificador del niño.

        Returns:
            list: Historial de sueño del niño.
        """
        try:
            response = requests.get(f'http://localhost:5000/medico/niños/{child_id}/historial')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

class AdminDAO:
    """
    Clase que maneja las operaciones de acceso a datos para el administrador.
    """

    @staticmethod
    def get_all_users():
        """
        Obtiene la lista de usuarios.

        Returns:
            list: Lista de usuarios.
        """
        try:
            response = requests.get('http://localhost:5000/admin/usuarios')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def delete_user(user_id):
        """
        Elimina un usuario.

        Args:
            user_id (int): Identificador del usuario.

        Returns:
            dict: Mensaje de éxito o error.
        """
        try:
            response = requests.delete(f'http://localhost:5000/admin/usuarios/{user_id}')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def create_user(nombre, email, password, role_id):
        """
        Crea un nuevo usuario.

        Args:
            nombre (str): Nombre del usuario.
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del usuario.
            role_id (int): Identificador del rol del usuario.

        Returns:
            dict: Información del usuario creado.
        """
        try:
            response = requests.post('http://localhost:5000/admin/usuarios', json={
                "username": nombre,
                "password": password,
                "email": email,
                "role_id": role_id
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def update_user(user_id, username, password, email, role_id):
        """
        Actualiza un usuario.

        Args:
            user_id (int): Identificador del usuario.
            username (str): Nombre de usuario.
            password (str): Contraseña del usuario.
            email (str): Correo electrónico del usuario.
            role_id (int): Identificador del rol del usuario.

        Returns:
            dict: Información del usuario actualizado.
        """
        try:
            response = requests.put(f'http://localhost:5000/admin/usuarios/{user_id}', json={
                "username": username,
                "password": password,
                "email": email,
                "role_id": role_id
            })
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def create_cuidador(username, password, email):
        """
        Crea un nuevo cuidador.

        Args:
            username (str): Nombre de usuario del cuidador.
            password (str): Contraseña del cuidador.
            email (str): Correo electrónico del cuidador.

        Returns:
            dict: Información del cuidador creado.
        """
        try:
            response = requests.post('http://localhost:5000/admin/cuidadores', json={
                "username": username,
                "password": password,
                "email": email
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

class MedicoDAO:
    """
    Clase que maneja las operaciones de acceso a datos para el médico.
    """

    @staticmethod
    def get_cuidadores():
        """
        Obtiene la lista de cuidadores.

        Returns:
            list: Lista de cuidadores.
        """
        try:
            response = requests.get('http://localhost:5000/medico/cuidadores')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def add_cuidador(username, password, email):
        """
        Añade un nuevo cuidador.

        Args:
            username (str): Nombre de usuario del cuidador.
            password (str): Contraseña del cuidador.
            email (str): Correo electrónico del cuidador.

        Returns:
            dict: Información del cuidador añadido.
        """
        try:
            response = requests.post('http://localhost:5000/medico/cuidadores', json={
                "username": username,
                "password": password,
                "email": email
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def delete_cuidador(user_id):
        """
        Elimina un cuidador.

        Args:
            user_id (int): Identificador del cuidador.

        Returns:
            dict: Mensaje de éxito o error.
        """
        try:
            response = requests.delete(f'http://localhost:5000/medico/cuidadores/{user_id}')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

class SearchDAO:
    """
    Clase que maneja las operaciones de búsqueda en el sistema.
    """

    @staticmethod
    def search(query):
        """
        Realiza una búsqueda en el sistema.

        Args:
            query (str): Término de búsqueda.

        Returns:
            dict: Resultados de la búsqueda.
        """
        try:
            response = requests.get(f'http://localhost:5000/search?query={query}')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

class TapDAO:
    """
    Clase que maneja las operaciones de acceso a datos para los taps.
    """

    @staticmethod
    def add_tap_tutor(child_id, status_id, init, end):
        """
        Añade un nuevo tap como tutor.

        Args:
            child_id (int): Identificador del niño.
            status_id (int): Identificador del estado.
            init (str): Hora de inicio.
            end (str): Hora de fin.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            response = requests.post('http://localhost:5000/tutores/taps', json={
                "child_id": child_id,
                "status_id": status_id,
                "init": init,
                "end": end
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def add_tap_medico(child_id, status_id, init, end):
        """
        Añade un nuevo tap como médico.

        Args:
            child_id (int): Identificador del niño.
            status_id (int): Identificador del estado.
            init (str): Hora de inicio.
            end (str): Hora de fin.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            response = requests.post('http://localhost:5000/medicos/taps', json={
                "child_id": child_id,
                "status_id": status_id,
                "init": init,
                "end": end
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

class HistorialDAO:
    """
    Clase que maneja las operaciones de acceso a datos para los historiales.
    """

    @staticmethod
    def add_historial_tutor(child_id, data, hora, estat, totalHores):
        """
        Añade un nuevo historial como tutor.

        Args:
            child_id (int): Identificador del niño.
            data (str): Fecha del historial.
            hora (str): Hora del historial.
            estat (str): Estado del niño.
            totalHores (int): Total de horas.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            response = requests.post('http://localhost:5000/tutores/historial', json={
                "child_id": child_id,
                "data": data,
                "hora": hora,
                "estat": estat,
                "totalHores": totalHores
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def add_historial_medico(child_id, data, hora, estat, totalHores):
        """
        Añade un nuevo historial como médico.

        Args:
            child_id (int): Identificador del niño.
            data (str): Fecha del historial.
            hora (str): Hora del historial.
            estat (str): Estado del niño.
            totalHores (int): Total de horas.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            response = requests.post('http://localhost:5000/medicos/historial', json={
                "child_id": child_id,
                "data": data,
                "hora": hora,
                "estat": estat,
                "totalHores": totalHores
            })
            if response.status_code == 201:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

class CommentDAO:
    """
    Clase que maneja las operaciones de acceso a datos para los comentarios.
    """

    @staticmethod
    def edit_comment(comment_id, text):
        """
        Edita un comentario existente.

        Args:
            comment_id (int): Identificador del comentario.
            text (str): Nuevo texto del comentario.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            response = requests.put(f'http://localhost:5000/comentarios/{comment_id}', json={"text": text})
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

    @staticmethod
    def delete_comment(comment_id):
        """
        Elimina un comentario.

        Args:
            comment_id (int): Identificador del comentario.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            response = requests.delete(f'http://localhost:5000/comentarios/{comment_id}')
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

# Vista de consola
class ViewConsole:
    """
    Clase que maneja la interacción con el usuario a través de la consola.
    """

    @staticmethod
    def show_user_info():
        """
        Muestra la información del usuario logueado.
        """
        user_data = LocalStorage.get_item('user')
        if user_data:
            user = json.loads(user_data)
            print(f"Usuario logueado: {user['username']} ({user['email']})")
        else:
            print("No hay usuario logueado.")

    @staticmethod
    def get_input(prompt):
        """
        Obtiene la entrada del usuario.

        Args:
            prompt (str): Mensaje para el usuario.

        Returns:
            str: Entrada del usuario.
        """
        user_input = input(prompt).strip()
        while not user_input:
            print("Error: El campo no puede estar vacío.")
            user_input = input(prompt).strip()
        return user_input

    @staticmethod
    def show_child_info():
        """
        Muestra la información de un niño.
        """
        child_name = ViewConsole.get_input("Ingrese el nombre del niño: ")
        child = NenDAO.get_child_by_name(child_name)
        if child:
            print(f"Información del niño: {child}")
        else:
            print(f"No se encontró un niño con el nombre '{child_name}'.")

    @staticmethod
    def get_input_login():
        """
        Obtiene las credenciales de inicio de sesión.

        Returns:
            tuple: Email y contraseña.
        """
        email = ViewConsole.get_input("Ingrese su email: ")
        password = ViewConsole.get_input("Ingrese su contraseña: ")
        return email, password

    @staticmethod
    def get_input_registro():
        """
        Obtiene los datos de registro de un nuevo usuario.

        Returns:
            tuple: Nombre, apellido, email y contraseña.
        """
        nombre = ViewConsole.get_input("Ingrese su nombre: ")
        apellido = ViewConsole.get_input("Ingrese su apellido: ")
        email = ViewConsole.get_input("Ingrese su email: ")
        password = ViewConsole.get_input("Ingrese su contraseña: ")
        return nombre, apellido, email, password

    @staticmethod
    def recuperar_contrasena():
        """
        Recupera la contraseña de un usuario.
        """
        email = ViewConsole.get_input("Ingrese su email: ")
        response = UsuarioDAO.recuperar_contrasena(email)
        if response:
            print(response.get("message", "Correo enviado con éxito."))

    @staticmethod
    def show_all_children():
        """
        Muestra la lista de niños.
        """
        children = NenDAO.get_all_children()
        if children:
            print("\nLista de niños:")
            for child in children:
                print(f"ID: {child['id']}, Nombre: {child['child_name']}")
        else:
            print("No se encontraron niños.")

    @staticmethod
    def show_child_historial():
        """
        Muestra el historial de sueño de un niño.
        """
        child_id = ViewConsole.get_input("Ingrese el ID del niño: ")
        historial = NenDAO.get_child_historial(child_id)
        if historial:
            print("\nHistorial del niño:")
            for hist in historial:
                print(f"Fecha: {hist['data']}, Hora: {hist['hora']}, Estado: {hist['estat']}, Total horas: {hist['totalHores']}")
        else:
            print("No se encontró historial para el niño.")

    @staticmethod
    def show_all_users():
        """
        Muestra la lista de usuarios.
        """
        users = AdminDAO.get_all_users()
        if users:
            print("\nLista de usuarios:")
            for user in users:
                print(f"ID: {user['id']}, Nombre: {user['username']}, Email: {user['email']}, Rol: {user['role_id']}")
        else:
            print("No se encontraron usuarios.")

    @staticmethod
    def delete_user():
        """
        Elimina un usuario.
        """
        user_id = ViewConsole.get_input("Ingrese el ID del usuario a eliminar: ")
        response = AdminDAO.delete_user(user_id)
        if response:
            print(response.get("message", "Usuario eliminado correctamente."))

    @staticmethod
    def create_user():
        """
        Crea un nuevo usuario.
        """
        nombre = ViewConsole.get_input("Ingrese el nombre del usuario: ")
        email = ViewConsole.get_input("Ingrese el email del usuario: ")
        password = ViewConsole.get_input("Ingrese la contraseña del usuario: ")
        role_id = ViewConsole.get_input("Ingrese el ID del rol del usuario: ")
        response = AdminDAO.create_user(nombre, email, password, role_id)
        if response:
            print(f"Usuario creado: {response.get('username', 'Usuario')}")

    @staticmethod
    def update_user_admin():
        """
        Actualiza un usuario.
        """
        user_id = ViewConsole.get_input("Ingrese el ID del usuario a modificar: ")
        username = ViewConsole.get_input("Ingrese el nuevo nombre de usuario: ")
        password = ViewConsole.get_input("Ingrese la nueva contraseña: ")
        email = ViewConsole.get_input("Ingrese el nuevo email: ")
        role_id = ViewConsole.get_input("Ingrese el nuevo ID de rol: ")
        response = AdminDAO.update_user(user_id, username, password, email, role_id)
        if response:
            print(f"Usuario modificado: {response.get('username', 'Usuario')}")

    @staticmethod
    def create_cuidador_admin():
        """
        Crea un nuevo cuidador.
        """
        username = ViewConsole.get_input("Ingrese el nombre de usuario del cuidador: ")
        password = ViewConsole.get_input("Ingrese la contraseña del cuidador: ")
        email = ViewConsole.get_input("Ingrese el email del cuidador: ")
        response = AdminDAO.create_cuidador(username, password, email)
        if response:
            print(f"Cuidador creado: {response.get('username', 'Cuidador')}")

    @staticmethod
    def show_cuidadores_medico():
        """
        Muestra la lista de cuidadores.
        """
        cuidadores = MedicoDAO.get_cuidadores()
        if cuidadores:
            print("\nLista de cuidadores:")
            for cuidador in cuidadores:
                print(f"ID: {cuidador['id']}, Nombre: {cuidador['username']}, Email: {cuidador['email']}")
        else:
            print("No se encontraron cuidadores.")

    @staticmethod
    def add_cuidador_medico():
        """
        Añade un nuevo cuidador.
        """
        username = ViewConsole.get_input("Ingrese el nombre de usuario del cuidador: ")
        password = ViewConsole.get_input("Ingrese la contraseña del cuidador: ")
        email = ViewConsole.get_input("Ingrese el email del cuidador: ")
        response = MedicoDAO.add_cuidador(username, password, email)
        if response:
            print(f"Cuidador añadido: {response.get('username', 'Cuidador')}")

    @staticmethod
    def delete_cuidador_medico():
        """
        Elimina un cuidador.
        """
        user_id = ViewConsole.get_input("Ingrese el ID del cuidador a eliminar: ")
        response = MedicoDAO.delete_cuidador(user_id)
        if response:
            print(response.get("message", "Cuidador eliminado correctamente."))

    @staticmethod
    def show_menu():
        """
        Muestra el menú principal.

        Returns:
            str: Opción seleccionada por el usuario.
        """
        print("\n--- Menú Principal ---")
        print("1. Login")
        print("2. Registro")
        print("3. Ver información del niño")
        print("4. Recuperar Contraseña")
        print("5. Ver niños (Médico)")
        print("6. Ver historial de un niño (Médico)")
        print("7. Ver usuarios (Admin)")
        print("8. Eliminar usuario (Admin)")
        print("9. Crear usuario (Admin)")
        print("10. Modificar usuario (Admin)")
        print("11. Crear cuidador (Admin)")
        print("12. Ver cuidadores (Médico)")
        print("13. Añadir cuidador (Médico)")
        print("14. Eliminar cuidador (Médico)")
        print("15. Ver información del usuario")
        print("16. Cerrar sesión")
        print("17. Buscar")
        print("18. Añadir tap (Tutor)")
        print("19. Añadir tap (Médico)")
        print("20. Añadir historial (Tutor)")
        print("21. Añadir historial (Médico)")
        print("22. Editar comentario")
        print("23. Eliminar comentario")
        print("24. Salir")
        return ViewConsole.get_input("Seleccione una opción: ")

    @staticmethod
    def search():
        """
        Realiza una búsqueda en el sistema.
        """
        query = ViewConsole.get_input("Ingrese el término de búsqueda: ")
        results = SearchDAO.search(query)
        if results:
            print("\nResultados de la búsqueda:")
            for category, items in results.items():
                print(f"\n{category.capitalize()}:")
                for item in items:
                    print(item)
        else:
            print("No se encontraron resultados.")

    @staticmethod
    def add_tap_tutor():
        """
        Añade un nuevo tap como tutor.
        """
        child_id = ViewConsole.get_input("Ingrese el ID del niño: ")
        status_id = ViewConsole.get_input("Ingrese el ID del estado: ")
        init = ViewConsole.get_input("Ingrese la hora de inicio (YYYY-MM-DDTHH:MM:SS): ")
        end = ViewConsole.get_input("Ingrese la hora de fin (YYYY-MM-DDTHH:MM:SS): ")
        response = TapDAO.add_tap_tutor(child_id, status_id, init, end)
        if response:
            print(f"Tap añadido: {response}")

    @staticmethod
    def add_tap_medico():
        """
        Añade un nuevo tap como médico.
        """
        child_id = ViewConsole.get_input("Ingrese el ID del niño: ")
        status_id = ViewConsole.get_input("Ingrese el ID del estado: ")
        init = ViewConsole.get_input("Ingrese la hora de inicio (YYYY-MM-DDTHH:MM:SS): ")
        end = ViewConsole.get_input("Ingrese la hora de fin (YYYY-MM-DDTHH:MM:SS): ")
        response = TapDAO.add_tap_medico(child_id, status_id, init, end)
        if response:
            print(f"Tap añadido: {response}")

    @staticmethod
    def add_historial_tutor():
        """
        Añade un nuevo historial como tutor.
        """
        child_id = ViewConsole.get_input("Ingrese el ID del niño: ")
        data = ViewConsole.get_input("Ingrese la fecha (YYYY-MM-DD): ")
        hora = ViewConsole.get_input("Ingrese la hora (HH:MM:SS): ")
        estat = ViewConsole.get_input("Ingrese el estado: ")
        totalHores = ViewConsole.get_input("Ingrese el total de horas: ")
        response = HistorialDAO.add_historial_tutor(child_id, data, hora, estat, totalHores)
        if response:
            print(f"Historial añadido: {response}")

    @staticmethod
    def add_historial_medico():
        """
        Añade un nuevo historial como médico.
        """
        child_id = ViewConsole.get_input("Ingrese el ID del niño: ")
        data = ViewConsole.get_input("Ingrese la fecha (YYYY-MM-DD): ")
        hora = ViewConsole.get_input("Ingrese la hora (HH:MM:SS): ")
        estat = ViewConsole.get_input("Ingrese el estado: ")
        totalHores = ViewConsole.get_input("Ingrese el total de horas: ")
        response = HistorialDAO.add_historial_medico(child_id, data, hora, estat, totalHores)
        if response:
            print(f"Historial añadido: {response}")

    @staticmethod
    def edit_comment():
        """
        Edita un comentario existente.
        """
        comment_id = ViewConsole.get_input("Ingrese el ID del comentario: ")
        text = ViewConsole.get_input("Ingrese el nuevo texto del comentario: ")
        response = CommentDAO.edit_comment(comment_id, text)
        if response:
            print(f"Comentario editado: {response}")

    @staticmethod
    def delete_comment():
        """
        Elimina un comentario.
        """
        comment_id = ViewConsole.get_input("Ingrese el ID del comentario: ")
        response = CommentDAO.delete_comment(comment_id)
        if response:
            print(response.get("message", "Comentario eliminado correctamente."))

# Ejecución del programa
if __name__ == "__main__":
    while True:
        opcion = ViewConsole.show_menu()
        if opcion == "1":  # Login
            email, password = ViewConsole.get_input_login()
            usuario = UsuarioDAO.login(email, password)
            if usuario:
                print(f"Bienvenido, {usuario.get('username', 'Usuario')}!")
            else:
                print("Login fallido. Verifique sus credenciales.")
        elif opcion == "2":  # Registro
            nombre, apellido, email, password = ViewConsole.get_input_registro()
            usuario = UsuarioDAO.registrar(nombre, apellido, email, password)
            if usuario:
                print(f"Usuario registrado: {usuario.get('username', 'Usuario')}")
            else:
                print("Error en el registro.")
        elif opcion == "3":  # Ver información del niño
            ViewConsole.show_child_info()
        elif opcion == "4":  # Recuperar Contraseña
            ViewConsole.recuperar_contrasena()
        elif opcion == "5":  # Ver niños (Médico)
            ViewConsole.show_all_children()
        elif opcion == "6":  # Ver historial de un niño (Médico)
            ViewConsole.show_child_historial()
        elif opcion == "7":  # Ver usuarios (Admin)
            ViewConsole.show_all_users()
        elif opcion == "8":  # Eliminar usuario (Admin)
            ViewConsole.delete_user()
        elif opcion == "9":  # Crear usuario (Admin)
            ViewConsole.create_user()
        elif opcion == "10":  # Modificar usuario (Admin)
            ViewConsole.update_user_admin()
        elif opcion == "11":  # Crear cuidador (Admin)
            ViewConsole.create_cuidador_admin()
        elif opcion == "12":  # Ver cuidadores (Médico)
            ViewConsole.show_cuidadores_medico()
        elif opcion == "13":  # Añadir cuidador (Médico)
            ViewConsole.add_cuidador_medico()
        elif opcion == "14":  # Eliminar cuidador (Médico)
            ViewConsole.delete_cuidador_medico()
        elif opcion == "15":  # Ver información del usuario
            ViewConsole.show_user_info()
        elif opcion == "16":  # Cerrar sesión
            UsuarioDAO.logout()
        elif opcion == "17":  # Buscar
            ViewConsole.search()
        elif opcion == "18":  # Añadir tap (Tutor)
            ViewConsole.add_tap_tutor()
        elif opcion == "19":  # Añadir tap (Médico)
            ViewConsole.add_tap_medico()
        elif opcion == "20":  # Añadir historial (Tutor)
            ViewConsole.add_historial_tutor()
        elif opcion == "21":  # Añadir historial (Médico)
            ViewConsole.add_historial_medico()
        elif opcion == "22":  # Editar comentario
            ViewConsole.edit_comment()
        elif opcion == "23":  # Eliminar comentario
            ViewConsole.delete_comment()
        elif opcion == "24":  # Salir
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")