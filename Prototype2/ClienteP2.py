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
    def login(email, password):
        try:
            response = requests.post('http://localhost:5000/login', json={"email": email, "password": password})
            if response.status_code == 200:
                return response.json()
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

class NenDAO:
    @staticmethod
    def get_child_by_name(child_name):
        try:
            response = requests.get(f'http://localhost:5000/children/{child_name}')
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
        except ValueError as e:
            print(f"Error: La respuesta no es un JSON válido. Detalles: {e}")
            print(f"Respuesta del servidor: {response.text}")
            return None

class ViewConsole:
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
    def show_menu():
        print("\n--- Menú Principal ---")
        print("1. Login")
        print("2. Registro")
        print("3. Ver información del niño")
        print("4. Salir")
        return ViewConsole.get_input("Seleccione una opción: ")

if __name__ == "__main__":
    while True:
        opcion = ViewConsole.show_menu()
        if opcion == "1":  # Login
            email, password = ViewConsole.get_input_login()
            usuario = UsuarioDAO.login(email, password)
            if usuario:
                print(f"Bienvenido, {usuario.get('nombre', 'Usuario')}!")
            else:
                print("Login fallido. Verifique sus credenciales.")
        elif opcion == "2":  # Registro
            nombre, apellido, email, password = ViewConsole.get_input_registro()
            usuario = UsuarioDAO.registrar(nombre, apellido, email, password)
            if usuario:
                print(f"Usuario registrado: {usuario.get('nombre', 'Usuario')}")
            else:
                print("Error en el registro.")
        elif opcion == "3":  # Ver información del niño
            ViewConsole.show_child_info()
        elif opcion == "4":  # Salir
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

