import tkinter as tk
from tkinter import ttk, messagebox
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
    def __init__(self, id, nombre, apellido, email, password, role_id):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password
        self.role_id = role_id  # 1: Admin, 2: Médico, 3: Usuario

    def __str__(self):
        return f"Nombre: {self.nombre} {self.apellido}, Email: {self.email}, Rol: {self.role_id}"


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
        try:
            response = requests.post('http://localhost:5000/login', json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and 'refresh_token' in data and 'user' in data:
                    LocalStorage.set_item('access_token', data['access_token'])
                    LocalStorage.set_item('refresh_token', data['refresh_token'])
                    LocalStorage.set_item('user', json.dumps(data['user']))
                    messagebox.showinfo("Login Exitoso", "Token y usuario guardados.")
                    return data['user']
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
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
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def get_all_children():
        try:
            response = requests.get('http://localhost:5000/medico/niños')
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def add_child(child_name, edad, fecha_nacimiento, informacioMedica):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                messagebox.showerror("Error", "No hay token de acceso. Inicie sesión primero.")
                return None

            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post('http://localhost:5000/children', json={
                "child_name": child_name,
                "edad": edad,
                "fecha_nacimiento": fecha_nacimiento,
                "informacioMedica": informacioMedica
            }, headers=headers)
            if response.status_code == 201:
                return response.json()
            else:
                messagebox.showerror("Error", f"{response.status_code} - {response.json().get('error', 'Error desconocido')}")
                return None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", str(e))
            return None

    @staticmethod
    def update_child(child_id, child_name, edad, fecha_nacimiento, informacioMedica):
        try:
            token = LocalStorage.get_item('access_token')
            if not token:
                messagebox.showerror("Error", "No hay token de acceso. Inicie sesión primero.")
                return None

            headers = {"Authorization": f"Bearer {token}"}
            response = requests.put(f'http://localhost:5000/children/{child_id}', json={
                "child_name": child_name,
                "edad": edad,
                "fecha_nacimiento": fecha_nacimiento,
                "informacioMedica": informacioMedica
            }, headers=headers)
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
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Usar un tema moderno

        self.show_login_window()

    def clear_window(self):
        """Limpia la ventana actual."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_window(self):
        """Muestra la ventana de login."""
        self.clear_window()

        ttk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.root, text="Email:").pack()
        self.email_entry = ttk.Entry(self.root)
        self.email_entry.pack(pady=5)

        ttk.Label(self.root, text="Contraseña:").pack()
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self.root, text="Iniciar Sesión", command=self.login).pack(pady=10)
        ttk.Button(self.root, text="Registrarse", command=self.show_registro_window).pack(pady=5)
        ttk.Button(self.root, text="Recuperar Contraseña", command=self.show_recuperar_contrasena_window).pack(pady=5)

    def show_registro_window(self):
        """Muestra la ventana de registro."""
        self.clear_window()

        ttk.Label(self.root, text="Registro", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.root, text="Nombre:").pack()
        self.nombre_entry = ttk.Entry(self.root)
        self.nombre_entry.pack(pady=5)

        ttk.Label(self.root, text="Apellido:").pack()
        self.apellido_entry = ttk.Entry(self.root)
        self.apellido_entry.pack(pady=5)

        ttk.Label(self.root, text="Email:").pack()
        self.email_registro_entry = ttk.Entry(self.root)
        self.email_registro_entry.pack(pady=5)

        ttk.Label(self.root, text="Contraseña:").pack()
        self.password_registro_entry = ttk.Entry(self.root, show="*")
        self.password_registro_entry.pack(pady=5)

        ttk.Button(self.root, text="Registrar", command=self.registrar).pack(pady=10)
        ttk.Button(self.root, text="Volver", command=self.show_login_window).pack(pady=5)

    def show_recuperar_contrasena_window(self):
        """Muestra la ventana para recuperar contraseña."""
        self.clear_window()

        ttk.Label(self.root, text="Recuperar Contraseña", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.root, text="Email:").pack()
        self.email_recuperar_entry = ttk.Entry(self.root)
        self.email_recuperar_entry.pack(pady=5)

        ttk.Button(self.root, text="Recuperar", command=self.recuperar_contrasena).pack(pady=10)
        ttk.Button(self.root, text="Volver", command=self.show_login_window).pack(pady=5)

    def login(self):
        """Maneja el proceso de login."""
        email = self.email_entry.get()
        password = self.password_entry.get()

        usuario = UsuarioDAO.login(email, password)
        if usuario:
            role_id = usuario.get('role_id', 3)  # Por defecto, asumimos que es un usuario normal
            if role_id == 1:
                self.show_admin_window()
            elif role_id == 2:
                self.show_medico_window()
            else:
                self.show_user_window()
        else:
            messagebox.showerror("Error", "Login fallido. Verifique sus credenciales.")

    def registrar(self):
        """Maneja el proceso de registro."""
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        email = self.email_registro_entry.get()
        password = self.password_registro_entry.get()

        usuario = UsuarioDAO.registrar(nombre, apellido, email, password)
        if usuario:
            messagebox.showinfo("Registro Exitoso", f"Usuario registrado: {usuario.get('username', 'Usuario')}")
            self.show_login_window()
        else:
            messagebox.showerror("Error", "Error en el registro.")

    def recuperar_contrasena(self):
        """Maneja el proceso de recuperación de contraseña."""
        email = self.email_recuperar_entry.get()
        response = UsuarioDAO.recuperar_contrasena(email)
        if response:
            messagebox.showinfo("Éxito", response.get("message", "Correo enviado con éxito."))
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo.")

    def show_admin_window(self):
        """Muestra la ventana de administrador."""
        self.clear_window()

        ttk.Label(self.root, text="Panel de Administrador", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.root, text="Ver Usuarios", command=self.show_all_users).pack(pady=5)
        ttk.Button(self.root, text="Crear Usuario", command=self.show_create_user_window).pack(pady=5)
        ttk.Button(self.root, text="Cerrar Sesión", command=self.logout).pack(pady=5)

    def show_medico_window(self):
        """Muestra la ventana de médico."""
        self.clear_window()

        ttk.Label(self.root, text="Panel de Médico", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.root, text="Ver Niños", command=self.show_all_children).pack(pady=5)
        ttk.Button(self.root, text="Añadir Niño", command=self.show_add_child_window).pack(pady=5)
        ttk.Button(self.root, text="Cerrar Sesión", command=self.logout).pack(pady=5)

    def show_user_window(self):
        """Muestra la ventana de usuario."""
        self.clear_window()

        ttk.Label(self.root, text="Panel de Usuario", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.root, text="Ver Información del Niño", command=self.show_child_info_window).pack(pady=5)
        ttk.Button(self.root, text="Cerrar Sesión", command=self.logout).pack(pady=5)

    def logout(self):
        """Cierra la sesión y vuelve a la ventana de login."""
        UsuarioDAO.logout()
        self.show_login_window()

    def show_all_users(self):
        """Muestra la lista de usuarios."""
        self.clear_window()

        ttk.Label(self.root, text="Lista de Usuarios", font=("Arial", 16)).pack(pady=10)

        users = AdminDAO.get_all_users()
        if users:
            for user in users:
                ttk.Label(self.root, text=f"ID: {user['id']}, Nombre: {user['username']}, Email: {user['email']}, Rol: {user['role_id']}").pack()
        else:
            ttk.Label(self.root, text="No se encontraron usuarios.").pack()

        ttk.Button(self.root, text="Volver", command=self.show_admin_window).pack(pady=10)

    def show_create_user_window(self):
        """Muestra la ventana para crear un usuario."""
        self.clear_window()

        ttk.Label(self.root, text="Crear Usuario", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.root, text="Nombre:").pack()
        self.nombre_create_entry = ttk.Entry(self.root)
        self.nombre_create_entry.pack(pady=5)

        ttk.Label(self.root, text="Email:").pack()
        self.email_create_entry = ttk.Entry(self.root)
        self.email_create_entry.pack(pady=5)

        ttk.Label(self.root, text="Contraseña:").pack()
        self.password_create_entry = ttk.Entry(self.root, show="*")
        self.password_create_entry.pack(pady=5)

        ttk.Label(self.root, text="ID del Rol:").pack()
        self.role_id_entry = ttk.Entry(self.root)
        self.role_id_entry.pack(pady=5)

        ttk.Button(self.root, text="Crear", command=self.create_user).pack(pady=10)
        ttk.Button(self.root, text="Volver", command=self.show_admin_window).pack(pady=5)

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

    def show_all_children(self):
        """Muestra la lista de niños."""
        self.clear_window()

        ttk.Label(self.root, text="Lista de Niños", font=("Arial", 16)).pack(pady=10)

        children = NenDAO.get_all_children()
        if children:
            for child in children:
                ttk.Label(self.root, text=f"ID: {child['id']}, Nombre: {child['child_name']}").pack()
        else:
            ttk.Label(self.root, text="No se encontraron niños.").pack()

        ttk.Button(self.root, text="Volver", command=self.show_medico_window).pack(pady=10)

    def show_add_child_window(self):
        """Muestra la ventana para añadir un niño."""
        self.clear_window()

        ttk.Label(self.root, text="Añadir Niño", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.root, text="Nombre del niño:").pack()
        self.child_name_entry = ttk.Entry(self.root)
        self.child_name_entry.pack(pady=5)

        ttk.Label(self.root, text="Edad:").pack()
        self.edad_entry = ttk.Entry(self.root)
        self.edad_entry.pack(pady=5)

        ttk.Label(self.root, text="Fecha de Nacimiento (YYYY-MM-DD):").pack()
        self.fecha_nacimiento_entry = ttk.Entry(self.root)
        self.fecha_nacimiento_entry.pack(pady=5)

        ttk.Label(self.root, text="Información Médica:").pack()
        self.informacioMedica_entry = ttk.Entry(self.root)
        self.informacioMedica_entry.pack(pady=5)

        ttk.Button(self.root, text="Añadir", command=self.add_child).pack(pady=10)
        ttk.Button(self.root, text="Volver", command=self.show_medico_window).pack(pady=5)

    def add_child(self):
        """Maneja el proceso de añadir un niño."""
        child_name = self.child_name_entry.get()
        edad = self.edad_entry.get()
        fecha_nacimiento = self.fecha_nacimiento_entry.get()
        informacioMedica = self.informacioMedica_entry.get()

        response = NenDAO.add_child(child_name, edad, fecha_nacimiento, informacioMedica)
        if response:
            messagebox.showinfo("Éxito", f"Niño añadido: {response.get('child_name', 'Niño')}")
        else:
            messagebox.showerror("Error", "No se pudo añadir el niño.")

    def show_child_info_window(self):
        """Muestra la ventana para ver la información de un niño."""
        self.clear_window()

        ttk.Label(self.root, text="Información del Niño", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.root, text="Nombre del niño:").pack()
        self.child_name_info_entry = ttk.Entry(self.root)
        self.child_name_info_entry.pack(pady=5)

        ttk.Button(self.root, text="Buscar", command=self.show_child_info).pack(pady=10)
        ttk.Button(self.root, text="Volver", command=self.show_user_window).pack(pady=5)

    def show_child_info(self):
        """Muestra la información del niño."""
        child_name = self.child_name_info_entry.get()
        child = NenDAO.get_child_by_name(child_name)
        if child:
            messagebox.showinfo("Información del Niño", str(child))
        else:
            messagebox.showerror("Error", f"No se encontró un niño con el nombre '{child_name}'.")


# Ejecución del programa
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()