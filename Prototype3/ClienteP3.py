import requests

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

class UsuarioDAO:
    @staticmethod
    def logout():
        import json
        localStorage = {}  # Simulación de localStorage en Python
        if 'access_token' in localStorage:
            del localStorage['access_token']
        if 'user' in localStorage:
            del localStorage['user']
        print("Sesión cerrada. Token y usuario eliminados.")

    @staticmethod
    def login(email, password):
        try:
            response = requests.post('http://localhost:5000/login', json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                # Guardar el token y la información del usuario en localStorage
                if 'access_token' in data and 'user' in data:
                    import json
                    localStorage = {}  # Simulación de localStorage en Python
                    localStorage['access_token'] = data['access_token']
                    localStorage['user'] = json.dumps(data['user'])
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
    @staticmethod
    def get_child_by_name(child_name):
        try:
            # Obtener el token de localStorage
            import json
            localStorage = {}  # Simulación de localStorage en Python
            token = localStorage.get('access_token', None)
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
    @staticmethod
    def get_all_users():
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
    def create_user(nombre, apellido, email, password, role_id):
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
    @staticmethod
    def get_cuidadores():
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

class ViewConsole:
    @staticmethod
    def show_user_info():
        import json
        localStorage = {}  # Simulación de localStorage en Python
        user_data = localStorage.get('user', None)
        if user_data:
            user = json.loads(user_data)
            print(f"Usuario logueado: {user['username']} ({user['email']})")
        else:
            print("No hay usuario logueado.")

    @staticmethod
    def get_input(prompt):
        user_input = input(prompt).strip()
        while not user_input:
            print("Error: El campo no puede estar vacío.")
            user_input = input(prompt).strip()
        return user_input

    @staticmethod
    def show_child_info():
        child_name = ViewConsole.get_input("Ingrese el nombre del niño: ")
        child = NenDAO.get_child_by_name(child_name)
        if child:
            print(f"Información del niño: {child}")
        else:
            print(f"No se encontró un niño con el nombre '{child_name}'.")

    @staticmethod
    def get_input_login():
        email = ViewConsole.get_input("Ingrese su email: ")
        password = ViewConsole.get_input("Ingrese su contraseña: ")
        return email, password

    @staticmethod
    def get_input_registro():
        nombre = ViewConsole.get_input("Ingrese su nombre: ")
        apellido = ViewConsole.get_input("Ingrese su apellido: ")
        email = ViewConsole.get_input("Ingrese su email: ")
        password = ViewConsole.get_input("Ingrese su contraseña: ")
        return nombre, apellido, email, password

    @staticmethod
    def recuperar_contrasena():
        email = ViewConsole.get_input("Ingrese su email: ")
        response = UsuarioDAO.recuperar_contrasena(email)
        if response:
            print(response.get("message", "Correo enviado con éxito."))

    @staticmethod
    def show_all_children():
        children = NenDAO.get_all_children()
        if children:
            print("\nLista de niños:")
            for child in children:
                print(f"ID: {child['id']}, Nombre: {child['child_name']}")
        else:
            print("No se encontraron niños.")

    @staticmethod
    def show_child_historial():
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
        users = AdminDAO.get_all_users()
        if users:
            print("\nLista de usuarios:")
            for user in users:
                print(f"ID: {user['id']}, Nombre: {user['username']}, Email: {user['email']}, Rol: {user['role_id']}")
        else:
            print("No se encontraron usuarios.")

    @staticmethod
    def delete_user():
        user_id = ViewConsole.get_input("Ingrese el ID del usuario a eliminar: ")
        response = AdminDAO.delete_user(user_id)
        if response:
            print(response.get("message", "Usuario eliminado correctamente."))

    @staticmethod
    def create_user():
        nombre = ViewConsole.get_input("Ingrese el nombre del usuario: ")
        email = ViewConsole.get_input("Ingrese el email del usuario: ")
        password = ViewConsole.get_input("Ingrese la contraseña del usuario: ")
        role_id = ViewConsole.get_input("Ingrese el ID del rol del usuario: ")
        response = AdminDAO.create_user(nombre, "", email, password, role_id)
        if response:
            print(f"Usuario creado: {response.get('username', 'Usuario')}")

    @staticmethod
    def update_user_admin():
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
        username = ViewConsole.get_input("Ingrese el nombre de usuario del cuidador: ")
        password = ViewConsole.get_input("Ingrese la contraseña del cuidador: ")
        email = ViewConsole.get_input("Ingrese el email del cuidador: ")
        response = AdminDAO.create_cuidador(username, password, email)
        if response:
            print(f"Cuidador creado: {response.get('username', 'Cuidador')}")

    @staticmethod
    def show_cuidadores_medico():
        cuidadores = MedicoDAO.get_cuidadores()
        if cuidadores:
            print("\nLista de cuidadores:")
            for cuidador in cuidadores:
                print(f"ID: {cuidador['id']}, Nombre: {cuidador['username']}, Email: {cuidador['email']}")
        else:
            print("No se encontraron cuidadores.")

    @staticmethod
    def add_cuidador_medico():
        username = ViewConsole.get_input("Ingrese el nombre de usuario del cuidador: ")
        password = ViewConsole.get_input("Ingrese la contraseña del cuidador: ")
        email = ViewConsole.get_input("Ingrese el email del cuidador: ")
        response = MedicoDAO.add_cuidador(username, password, email)
        if response:
            print(f"Cuidador añadido: {response.get('username', 'Cuidador')}")

    @staticmethod
    def delete_cuidador_medico():
        user_id = ViewConsole.get_input("Ingrese el ID del cuidador a eliminar: ")
        response = MedicoDAO.delete_cuidador(user_id)
        if response:
            print(response.get("message", "Cuidador eliminado correctamente."))

@staticmethod
def show_menu():
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
    print("17. Salir")
    return ViewConsole.get_input("Seleccione una opción: ")

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
        elif opcion == "17":  # Salir
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")