import tkinter as tk
from tkinter import messagebox, ttk
import json
import requests

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
    def __init__(self, id, nombre, apellido, email, password):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password

    def __str__(self):
        return f"Nombre: {self.nombre} {self.apellido}, Email: {self.email}"

class Nen:
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
    @staticmethod
    def logout():
        LocalStorage.remove_item('access_token')
        LocalStorage.remove_item('refresh_token')
        LocalStorage.remove_item('user')
        messagebox.showinfo("Logout", "Sesión cerrada. Token y usuario eliminados.")

    @staticmethod
    def login(email, password):
        """
        Inicia sesión en el sistema.

        Args:
            email (str): Correo electrónico del usuario.
            password (str): Contraseña del usuario.

        Returns:
            dict: Información del usuario si el login es exitoso, None en caso contrario.
        """
        try:
            # Validar que los campos no estén vacíos
            if not email or not password:
                messagebox.showerror("Error", "El email y la contraseña son obligatorios.")
                return None

            response = requests.post('http://localhost:5000/login', json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and 'refresh_token' in data and 'user' in data:
                    LocalStorage.set_item('access_token', data['access_token'])
                    LocalStorage.set_item('refresh_token', data['refresh_token'])
                    LocalStorage.set_item('user', json.dumps(data['user']))
                    messagebox.showinfo("Login Exitoso", "Token y usuario guardados.")
                    return data['user']
            elif response.status_code == 401:
                messagebox.showerror("Error", "Credenciales inválidas. Verifique su email y contraseña.")
            elif response.status_code == 400:
                messagebox.showerror("Error", "El email y la contraseña son obligatorios.")
            else:
                messagebox.showerror("Error", f"Error inesperado: {response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def registrar(nombre, apellido, email, password):
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
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def recuperar_contrasena(email):
        try:
            response = requests.post('http://localhost:5000/recuperar-contrasena', json={"email": email})
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

class NenDAO:
    @staticmethod
    def get_child_by_name(child_name):
        """
        Obtiene un niño por su nombre.

        Args:
            child_name (str): Nombre del niño.

        Returns:
            Nen: Objeto con la información del niño o None si no se encuentra.
        """
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                messagebox.showerror("Error", "No hay token de acceso. Inicie sesión primero.")
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
            elif response.status_code == 404:
                messagebox.showerror("Error", f"Niño con nombre '{child_name}' no encontrado.")
            else:
                messagebox.showerror("Error", f"Error inesperado: {response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def get_all_children():
        """
        Obtiene la lista de todos los niños.

        Returns:
            list: Lista de niños o None si ocurre un error.
        """
        try:
            response = requests.get('http://localhost:5000/medico/niños')
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                messagebox.showerror("Error", "No se encontraron niños.")
            else:
                messagebox.showerror("Error", f"Error inesperado: {response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def get_child_historial(child_id):
        """
        Obtiene el historial de sueño de un niño.

        Args:
            child_id (int): Identificador del niño.

        Returns:
            list: Historial del niño o None si ocurre un error.
        """
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                messagebox.showerror("Error", "No hay token de acceso. Inicie sesión primero.")
                return None

            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f'http://localhost:5000/medico/niños/{child_id}/historial', headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                messagebox.showerror("Error", f"No se encontró historial para el niño con ID {child_id}.")
            else:
                messagebox.showerror("Error", f"Error inesperado: {response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

class AdminDAO:
    @staticmethod
    def get_all_users():
        """
        Obtiene la lista de todos los usuarios.

        Returns:
            list: Lista de usuarios o None si ocurre un error.
        """
        try:
            response = requests.get('http://localhost:5000/admin/usuarios')
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                messagebox.showerror("Error", "No se encontraron usuarios.")
            else:
                messagebox.showerror("Error", f"Error inesperado: {response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def delete_user(user_id):
        try:
            response = requests.delete(f'http://localhost:5000/admin/usuarios/{user_id}')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def create_user(nombre, email, password, role_id):
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
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def update_user(user_id, username, password, email, role_id):
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
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def create_cuidador(username, password, email):
        try:
            response = requests.post('http://localhost:5000/admin/cuidadores', json={
                "username": username,
                "password": password,
                "email": email
            })
            if response.status_code == 201:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def get_user_by_id(user_id):
        """
        Obtiene un usuario por su ID.

        Args:
            user_id (int): Identificador del usuario.

        Returns:
            dict: Información del usuario o None si ocurre un error.
        """
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                messagebox.showerror("Error", "No hay token de acceso. Inicie sesión primero.")
                return None

            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f'http://localhost:5000/admin/usuarios/{user_id}', headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                messagebox.showerror("Error", f"Usuario con ID {user_id} no encontrado.")
            else:
                messagebox.showerror("Error", f"Error inesperado: {response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

class MedicoDAO:
    @staticmethod
    def get_cuidadores():
        try:
            response = requests.get('http://localhost:5000/medico/cuidadores')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def add_cuidador(username, password, email):
        try:
            response = requests.post('http://localhost:5000/medico/cuidadores', json={
                "username": username,
                "password": password,
                "email": email
            })
            if response.status_code == 201:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def delete_cuidador(user_id):
        try:
            response = requests.delete(f'http://localhost:5000/medico/cuidadores/{user_id}')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

class SearchDAO:
    @staticmethod
    def search(query):
        try:
            response = requests.get(f'http://localhost:5000/search?query={query}')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

class TapDAO:
    @staticmethod
    def add_tap_tutor(child_id, status_id, init, end):
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
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def add_tap_medico(child_id, status_id, init, end):
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
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

class HistorialDAO:
    @staticmethod
    def add_historial_tutor(child_id, data, hora, estat, totalHores):
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
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def add_historial_medico(child_id, data, hora, estat, totalHores):
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
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

class CommentDAO:
    @staticmethod
    def edit_comment(comment_id, text):
        try:
            response = requests.put(f'http://localhost:5000/comentarios/{comment_id}', json={"text": text})
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def delete_comment(comment_id):
        try:
            response = requests.delete(f'http://localhost:5000/comentarios/{comment_id}')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

# Interfaz Gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Médica")
        self.root.geometry("600x400")

        self.create_main_menu()

    def create_main_menu(self):
        """Crea el menú principal de la aplicación."""
        self.clear_window()

        tk.Label(self.root, text="Menú Principal", font=("Arial", 16)).pack(pady=10)

        buttons = [
            ("Login", self.open_login_window),
            ("Registro", self.open_registro_window),
            ("Ver información del niño", self.open_child_info_window),
            ("Recuperar Contraseña", self.open_recuperar_contrasena_window),
            ("Ver niños (Médico)", self.open_show_all_children_window),
            ("Ver historial de un niño (Médico)", self.open_show_child_historial_window),
            ("Ver usuarios (Admin)", self.open_show_all_users_window),
            ("Eliminar usuario (Admin)", self.open_delete_user_window),
            ("Crear usuario (Admin)", self.open_create_user_window),
            ("Modificar usuario (Admin)", self.open_update_user_window),
            ("Crear cuidador (Admin)", self.open_create_cuidador_window),
            ("Ver cuidadores (Médico)", self.open_show_cuidadores_window),
            ("Añadir cuidador (Médico)", self.open_add_cuidador_window),
            ("Eliminar cuidador (Médico)", self.open_delete_cuidador_window),
            ("Ver información del usuario", self.show_user_info),
            ("Cerrar sesión", UsuarioDAO.logout),
            ("Buscar", self.open_search_window),
            ("Añadir tap (Tutor)", self.open_add_tap_tutor_window),
            ("Añadir tap (Médico)", self.open_add_tap_medico_window),
            ("Añadir historial (Tutor)", self.open_add_historial_tutor_window),
            ("Añadir historial (Médico)", self.open_add_historial_medico_window),
            ("Editar comentario", self.open_edit_comment_window),
            ("Eliminar comentario", self.open_delete_comment_window),
            ("Salir", self.root.quit)
        ]

        for text, command in buttons:
            tk.Button(self.root, text=text, command=command).pack(pady=5)

    def clear_window(self):
        """Limpia la ventana actual."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def open_login_window(self):
        """Abre la ventana de login."""
        self.clear_window()

        tk.Label(self.root, text="Login", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Iniciar Sesión", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def login(self):
        """Maneja el proceso de login."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        usuario = UsuarioDAO.login(email, password)
        if usuario:
            messagebox.showinfo("Login Exitoso", f"Bienvenido, {usuario.get('username', 'Usuario')}!")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Login fallido. Verifique sus credenciales.")

    def open_registro_window(self):
        """Abre la ventana de registro."""
        self.clear_window()

        tk.Label(self.root, text="Registro", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Nombre:").pack()
        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.pack(pady=5)

        tk.Label(self.root, text="Apellido:").pack()
        self.apellido_entry = tk.Entry(self.root)
        self.apellido_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack()
        self.email_registro_entry = tk.Entry(self.root)
        self.email_registro_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack()
        self.password_registro_entry = tk.Entry(self.root, show="*")
        self.password_registro_entry.pack(pady=5)

        tk.Button(self.root, text="Registrar", command=self.registrar).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def registrar(self):
        """Maneja el proceso de registro."""
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        email = self.email_registro_entry.get()
        password = self.password_registro_entry.get()

        usuario = UsuarioDAO.registrar(nombre, apellido, email, password)
        if usuario:
            messagebox.showinfo("Registro Exitoso", f"Usuario registrado: {usuario.get('username', 'Usuario')}")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Error en el registro.")

    def open_child_info_window(self):
        """Abre la ventana para ver la información de un niño."""
        self.clear_window()

        tk.Label(self.root, text="Información del Niño", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Nombre del niño:").pack()
        self.child_name_entry = tk.Entry(self.root)
        self.child_name_entry.pack(pady=5)

        tk.Button(self.root, text="Buscar", command=self.show_child_info).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def show_child_info(self):
        """Muestra la información del niño."""
        child_name = self.child_name_entry.get()
        child = NenDAO.get_child_by_name(child_name)
        if child:
            messagebox.showinfo("Información del Niño", str(child))
        else:
            messagebox.showerror("Error", f"No se encontró un niño con el nombre '{child_name}'.")

    def open_recuperar_contrasena_window(self):
        """Abre la ventana para recuperar contraseña."""
        self.clear_window()

        tk.Label(self.root, text="Recuperar Contraseña", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Email:").pack()
        self.email_recuperar_entry = tk.Entry(self.root)
        self.email_recuperar_entry.pack(pady=5)

        tk.Button(self.root, text="Recuperar", command=self.recuperar_contrasena).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def recuperar_contrasena(self):
        """Maneja el proceso de recuperación de contraseña."""
        email = self.email_recuperar_entry.get()
        response = UsuarioDAO.recuperar_contrasena(email)
        if response:
            messagebox.showinfo("Éxito", response.get("message", "Correo enviado con éxito."))
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo.")

    def open_show_all_children_window(self):
        """Abre la ventana para ver todos los niños."""
        self.clear_window()

        tk.Label(self.root, text="Lista de Niños", font=("Arial", 14)).pack(pady=10)

        children = NenDAO.get_all_children()
        if children:
            for child in children:
                tk.Label(self.root, text=f"ID: {child['id']}, Nombre: {child['child_name']}").pack()
        else:
            tk.Label(self.root, text="No se encontraron niños.").pack()

        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=10)

    def open_show_child_historial_window(self):
        """Abre la ventana para ver el historial de un niño."""
        self.clear_window()

        tk.Label(self.root, text="Historial del Niño", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del niño:").pack()
        self.child_id_entry = tk.Entry(self.root)
        self.child_id_entry.pack(pady=5)

        tk.Button(self.root, text="Buscar", command=self.show_child_historial).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def show_child_historial(self):
        """Muestra el historial de un niño."""
        child_id = self.child_id_entry.get()
        historial = NenDAO.get_child_historial(child_id)
        if historial:
            historial_text = "\n".join([f"Fecha: {h['data']}, Hora: {h['hora']}, Estado: {h['estat']}, Total horas: {h['totalHores']}" for h in historial])
            messagebox.showinfo("Historial del Niño", historial_text)
        else:
            messagebox.showerror("Error", "No se encontró historial para el niño.")

    def open_show_all_users_window(self):
        """Abre la ventana para ver todos los usuarios."""
        self.clear_window()

        tk.Label(self.root, text="Lista de Usuarios", font=("Arial", 14)).pack(pady=10)

        users = AdminDAO.get_all_users()
        if users:
            for user in users:
                tk.Label(self.root, text=f"ID: {user['id']}, Nombre: {user['username']}, Email: {user['email']}, Rol: {user['role_id']}").pack()
        else:
            tk.Label(self.root, text="No se encontraron usuarios.").pack()

        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=10)

    def open_delete_user_window(self):
        """Abre la ventana para eliminar un usuario."""
        self.clear_window()

        tk.Label(self.root, text="Eliminar Usuario", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del usuario:").pack()
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.pack(pady=5)

        tk.Button(self.root, text="Eliminar", command=self.delete_user).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def delete_user(self):
        """Maneja el proceso de eliminar un usuario."""
        user_id = self.user_id_entry.get()
        response = AdminDAO.delete_user(user_id)
        if response:
            messagebox.showinfo("Éxito", response.get("message", "Usuario eliminado correctamente."))
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario.")

    def open_create_user_window(self):
        """Abre la ventana para crear un usuario."""
        self.clear_window()

        tk.Label(self.root, text="Crear Usuario", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Nombre:").pack()
        self.nombre_create_entry = tk.Entry(self.root)
        self.nombre_create_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack()
        self.email_create_entry = tk.Entry(self.root)
        self.email_create_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack()
        self.password_create_entry = tk.Entry(self.root, show="*")
        self.password_create_entry.pack(pady=5)

        tk.Label(self.root, text="ID del Rol:").pack()
        self.role_id_entry = tk.Entry(self.root)
        self.role_id_entry.pack(pady=5)

        tk.Button(self.root, text="Crear", command=self.create_user).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def create_user(self):
        """Maneja el proceso de crear un usuario."""
        nombre = self.nombre_create_entry.get()
        email = self.email_create_entry.get()
        password = self.password_create_entry.get()
        role_id = self.role_id_entry.get()

        response = AdminDAO.create_user(nombre, email, password, role_id)
        if response:
            messagebox.showinfo("Éxito", f"Usuario creado: {response.get('username', 'Usuario')}")
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario.")

    def open_update_user_window(self):
        """Abre la ventana para actualizar un usuario."""
        self.clear_window()

        tk.Label(self.root, text="Actualizar Usuario", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del usuario:").pack()
        self.user_id_update_entry = tk.Entry(self.root)
        self.user_id_update_entry.pack(pady=5)

        tk.Label(self.root, text="Nuevo nombre:").pack()
        self.username_update_entry = tk.Entry(self.root)
        self.username_update_entry.pack(pady=5)

        tk.Label(self.root, text="Nueva contraseña:").pack()
        self.password_update_entry = tk.Entry(self.root, show="*")
        self.password_update_entry.pack(pady=5)

        tk.Label(self.root, text="Nuevo email:").pack()
        self.email_update_entry = tk.Entry(self.root)
        self.email_update_entry.pack(pady=5)

        tk.Label(self.root, text="Nuevo ID del Rol:").pack()
        self.role_id_update_entry = tk.Entry(self.root)
        self.role_id_update_entry.pack(pady=5)

        tk.Button(self.root, text="Actualizar", command=self.update_user).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def update_user(self):
        """Maneja el proceso de actualizar un usuario."""
        user_id = self.user_id_update_entry.get()
        username = self.username_update_entry.get()
        password = self.password_update_entry.get()
        email = self.email_update_entry.get()
        role_id = self.role_id_update_entry.get()

        response = AdminDAO.update_user(user_id, username, password, email, role_id)
        if response:
            messagebox.showinfo("Éxito", f"Usuario actualizado: {response.get('username', 'Usuario')}")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el usuario.")

    def open_create_cuidador_window(self):
        """Abre la ventana para crear un cuidador."""
        self.clear_window()

        tk.Label(self.root, text="Crear Cuidador", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Nombre:").pack()
        self.nombre_cuidador_entry = tk.Entry(self.root)
        self.nombre_cuidador_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack()
        self.email_cuidador_entry = tk.Entry(self.root)
        self.email_cuidador_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack()
        self.password_cuidador_entry = tk.Entry(self.root, show="*")
        self.password_cuidador_entry.pack(pady=5)

        tk.Button(self.root, text="Crear", command=self.create_cuidador).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def create_cuidador(self):
        """Maneja el proceso de crear un cuidador."""
        nombre = self.nombre_cuidador_entry.get()
        email = self.email_cuidador_entry.get()
        password = self.password_cuidador_entry.get()

        response = AdminDAO.create_cuidador(nombre, password, email)
        if response:
            messagebox.showinfo("Éxito", f"Cuidador creado: {response.get('username', 'Cuidador')}")
        else:
            messagebox.showerror("Error", "No se pudo crear el cuidador.")

    def open_show_cuidadores_window(self):
        """Abre la ventana para ver todos los cuidadores."""
        self.clear_window()

        tk.Label(self.root, text="Lista de Cuidadores", font=("Arial", 14)).pack(pady=10)

        cuidadores = MedicoDAO.get_cuidadores()
        if cuidadores:
            for cuidador in cuidadores:
                tk.Label(self.root, text=f"ID: {cuidador['id']}, Nombre: {cuidador['username']}, Email: {cuidador['email']}").pack()
        else:
            tk.Label(self.root, text="No se encontraron cuidadores.").pack()

        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=10)

    def open_add_cuidador_window(self):
        """Abre la ventana para añadir un cuidador."""
        self.clear_window()

        tk.Label(self.root, text="Añadir Cuidador", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Nombre:").pack()
        self.nombre_add_cuidador_entry = tk.Entry(self.root)
        self.nombre_add_cuidador_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack()
        self.email_add_cuidador_entry = tk.Entry(self.root)
        self.email_add_cuidador_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack()
        self.password_add_cuidador_entry = tk.Entry(self.root, show="*")
        self.password_add_cuidador_entry.pack(pady=5)

        tk.Button(self.root, text="Añadir", command=self.add_cuidador).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def add_cuidador(self):
        """Maneja el proceso de añadir un cuidador."""
        nombre = self.nombre_add_cuidador_entry.get()
        email = self.email_add_cuidador_entry.get()
        password = self.password_add_cuidador_entry.get()

        response = MedicoDAO.add_cuidador(nombre, password, email)
        if response:
            messagebox.showinfo("Éxito", f"Cuidador añadido: {response.get('username', 'Cuidador')}")
        else:
            messagebox.showerror("Error", "No se pudo añadir el cuidador.")

    def open_delete_cuidador_window(self):
        """Abre la ventana para eliminar un cuidador."""
        self.clear_window()

        tk.Label(self.root, text="Eliminar Cuidador", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del cuidador:").pack()
        self.cuidador_id_entry = tk.Entry(self.root)
        self.cuidador_id_entry.pack(pady=5)

        tk.Button(self.root, text="Eliminar", command=self.delete_cuidador).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def delete_cuidador(self):
        """Maneja el proceso de eliminar un cuidador."""
        user_id = self.cuidador_id_entry.get()
        response = MedicoDAO.delete_cuidador(user_id)
        if response:
            messagebox.showinfo("Éxito", response.get("message", "Cuidador eliminado correctamente."))
        else:
            messagebox.showerror("Error", "No se pudo eliminar el cuidador.")

    def show_user_info(self):
        """Muestra la información del usuario logueado."""
        user_data = LocalStorage.get_item('user')
        if user_data:
            user = json.loads(user_data)
            messagebox.showinfo("Información del Usuario", f"Usuario logueado: {user['username']} ({user['email']})")
        else:
            messagebox.showerror("Error", "No hay usuario logueado.")

    def open_search_window(self):
        """Abre la ventana de búsqueda."""
        self.clear_window()

        tk.Label(self.root, text="Buscar", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Término de búsqueda:").pack()
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)

        tk.Button(self.root, text="Buscar", command=self.search).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def search(self):
        """Maneja el proceso de búsqueda."""
        query = self.search_entry.get()
        results = SearchDAO.search(query)
        if results:
            results_text = "\n".join([f"{category.capitalize()}: {item}" for category, items in results.items() for item in items])
            messagebox.showinfo("Resultados de la Búsqueda", results_text)
        else:
            messagebox.showerror("Error", "No se encontraron resultados.")

    def open_add_tap_tutor_window(self):
        """Abre la ventana para añadir un tap como tutor."""
        self.clear_window()

        tk.Label(self.root, text="Añadir Tap (Tutor)", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del niño:").pack()
        self.child_id_tap_tutor_entry = tk.Entry(self.root)
        self.child_id_tap_tutor_entry.pack(pady=5)

        tk.Label(self.root, text="ID del estado:").pack()
        self.status_id_tap_tutor_entry = tk.Entry(self.root)
        self.status_id_tap_tutor_entry.pack(pady=5)

        tk.Label(self.root, text="Hora de inicio (YYYY-MM-DDTHH:MM:SS):").pack()
        self.init_tap_tutor_entry = tk.Entry(self.root)
        self.init_tap_tutor_entry.pack(pady=5)

        tk.Label(self.root, text="Hora de fin (YYYY-MM-DDTHH:MM:SS):").pack()
        self.end_tap_tutor_entry = tk.Entry(self.root)
        self.end_tap_tutor_entry.pack(pady=5)

        tk.Button(self.root, text="Añadir", command=self.add_tap_tutor).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def add_tap_tutor(self):
        """Maneja el proceso de añadir un tap como tutor."""
        child_id = self.child_id_tap_tutor_entry.get()
        status_id = self.status_id_tap_tutor_entry.get()
        init = self.init_tap_tutor_entry.get()
        end = self.end_tap_tutor_entry.get()

        response = TapDAO.add_tap_tutor(child_id, status_id, init, end)
        if response:
            messagebox.showinfo("Éxito", f"Tap añadido: {response}")
        else:
            messagebox.showerror("Error", "No se pudo añadir el tap.")

    def open_add_tap_medico_window(self):
        """Abre la ventana para añadir un tap como médico."""
        self.clear_window()

        tk.Label(self.root, text="Añadir Tap (Médico)", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del niño:").pack()
        self.child_id_tap_medico_entry = tk.Entry(self.root)
        self.child_id_tap_medico_entry.pack(pady=5)

        tk.Label(self.root, text="ID del estado:").pack()
        self.status_id_tap_medico_entry = tk.Entry(self.root)
        self.status_id_tap_medico_entry.pack(pady=5)

        tk.Label(self.root, text="Hora de inicio (YYYY-MM-DDTHH:MM:SS):").pack()
        self.init_tap_medico_entry = tk.Entry(self.root)
        self.init_tap_medico_entry.pack(pady=5)

        tk.Label(self.root, text="Hora de fin (YYYY-MM-DDTHH:MM:SS):").pack()
        self.end_tap_medico_entry = tk.Entry(self.root)
        self.end_tap_medico_entry.pack(pady=5)

        tk.Button(self.root, text="Añadir", command=self.add_tap_medico).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def add_tap_medico(self):
        """Maneja el proceso de añadir un tap como médico."""
        child_id = self.child_id_tap_medico_entry.get()
        status_id = self.status_id_tap_medico_entry.get()
        init = self.init_tap_medico_entry.get()
        end = self.end_tap_medico_entry.get()

        response = TapDAO.add_tap_medico(child_id, status_id, init, end)
        if response:
            messagebox.showinfo("Éxito", f"Tap añadido: {response}")
        else:
            messagebox.showerror("Error", "No se pudo añadir el tap.")

    def open_add_historial_tutor_window(self):
        """Abre la ventana para añadir un historial como tutor."""
        self.clear_window()

        tk.Label(self.root, text="Añadir Historial (Tutor)", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del niño:").pack()
        self.child_id_historial_tutor_entry = tk.Entry(self.root)
        self.child_id_historial_tutor_entry.pack(pady=5)

        tk.Label(self.root, text="Fecha (YYYY-MM-DD):").pack()
        self.data_historial_tutor_entry = tk.Entry(self.root)
        self.data_historial_tutor_entry.pack(pady=5)

        tk.Label(self.root, text="Hora (HH:MM:SS):").pack()
        self.hora_historial_tutor_entry = tk.Entry(self.root)
        self.hora_historial_tutor_entry.pack(pady=5)

        tk.Label(self.root, text="Estado:").pack()
        self.estat_historial_tutor_entry = tk.Entry(self.root)
        self.estat_historial_tutor_entry.pack(pady=5)

        tk.Label(self.root, text="Total horas:").pack()
        self.totalHores_historial_tutor_entry = tk.Entry(self.root)
        self.totalHores_historial_tutor_entry.pack(pady=5)

        tk.Button(self.root, text="Añadir", command=self.add_historial_tutor).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def add_historial_tutor(self):
        """Maneja el proceso de añadir un historial como tutor."""
        child_id = self.child_id_historial_tutor_entry.get()
        data = self.data_historial_tutor_entry.get()
        hora = self.hora_historial_tutor_entry.get()
        estat = self.estat_historial_tutor_entry.get()
        totalHores = self.totalHores_historial_tutor_entry.get()

        response = HistorialDAO.add_historial_tutor(child_id, data, hora, estat, totalHores)
        if response:
            messagebox.showinfo("Éxito", f"Historial añadido: {response}")
        else:
            messagebox.showerror("Error", "No se pudo añadir el historial.")

    def open_add_historial_medico_window(self):
        """Abre la ventana para añadir un historial como médico."""
        self.clear_window()

        tk.Label(self.root, text="Añadir Historial (Médico)", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del niño:").pack()
        self.child_id_historial_medico_entry = tk.Entry(self.root)
        self.child_id_historial_medico_entry.pack(pady=5)

        tk.Label(self.root, text="Fecha (YYYY-MM-DD):").pack()
        self.data_historial_medico_entry = tk.Entry(self.root)
        self.data_historial_medico_entry.pack(pady=5)

        tk.Label(self.root, text="Hora (HH:MM:SS):").pack()
        self.hora_historial_medico_entry = tk.Entry(self.root)
        self.hora_historial_medico_entry.pack(pady=5)

        tk.Label(self.root, text="Estado:").pack()
        self.estat_historial_medico_entry = tk.Entry(self.root)
        self.estat_historial_medico_entry.pack(pady=5)

        tk.Label(self.root, text="Total horas:").pack()
        self.totalHores_historial_medico_entry = tk.Entry(self.root)
        self.totalHores_historial_medico_entry.pack(pady=5)

        tk.Button(self.root, text="Añadir", command=self.add_historial_medico).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def add_historial_medico(self):
        """Maneja el proceso de añadir un historial como médico."""
        child_id = self.child_id_historial_medico_entry.get()
        data = self.data_historial_medico_entry.get()
        hora = self.hora_historial_medico_entry.get()
        estat = self.estat_historial_medico_entry.get()
        totalHores = self.totalHores_historial_medico_entry.get()

        response = HistorialDAO.add_historial_medico(child_id, data, hora, estat, totalHores)
        if response:
            messagebox.showinfo("Éxito", f"Historial añadido: {response}")
        else:
            messagebox.showerror("Error", "No se pudo añadir el historial.")

    def open_edit_comment_window(self):
        """Abre la ventana para editar un comentario."""
        self.clear_window()

        tk.Label(self.root, text="Editar Comentario", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del comentario:").pack()
        self.comment_id_entry = tk.Entry(self.root)
        self.comment_id_entry.pack(pady=5)

        tk.Label(self.root, text="Nuevo texto:").pack()
        self.comment_text_entry = tk.Entry(self.root)
        self.comment_text_entry.pack(pady=5)

        tk.Button(self.root, text="Editar", command=self.edit_comment).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def edit_comment(self):
        """Maneja el proceso de editar un comentario."""
        comment_id = self.comment_id_entry.get()
        text = self.comment_text_entry.get()

        response = CommentDAO.edit_comment(comment_id, text)
        if response:
            messagebox.showinfo("Éxito", f"Comentario editado: {response}")
        else:
            messagebox.showerror("Error", "No se pudo editar el comentario.")

    def open_delete_comment_window(self):
        """Abre la ventana para eliminar un comentario."""
        self.clear_window()

        tk.Label(self.root, text="Eliminar Comentario", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="ID del comentario:").pack()
        self.comment_id_delete_entry = tk.Entry(self.root)
        self.comment_id_delete_entry.pack(pady=5)

        tk.Button(self.root, text="Eliminar", command=self.delete_comment).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_main_menu).pack(pady=5)

    def delete_comment(self):
        """Maneja el proceso de eliminar un comentario."""
        comment_id = self.comment_id_delete_entry.get()
        response = CommentDAO.delete_comment(comment_id)
        if response:
            messagebox.showinfo("Éxito", response.get("message", "Comentario eliminado correctamente."))
        else:
            messagebox.showerror("Error", "No se pudo eliminar el comentario.")

# Ejecución del programa
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()