import requests

# Clase User
class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password  # Puede ser None si el backend no la devuelve
        self.email = email
    
    def __str__(self):
        return f"Id: {self.id}, Username: {self.username}, Email: {self.email}"

class UserDAO:
    BASE_URL = 'http://localhost:10050/tapatappV1/'
    
    @staticmethod
    def get_user_by_username(username):
        """Obtiene la información de un usuario por su nombre de usuario."""
        try:
            response = requests.get(f'{UserDAO.BASE_URL}Username?username={username}')
            if response.status_code == 200:
                user_data = response.json()
                return User(user_data['id'], user_data['username'], None, user_data['email'])
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

# Clase Child
class Child:
    def __init__(self, id, child_name, sleep_average, treatment_id, time):
        self.id = id
        self.child_name = child_name
        self.sleep_average = sleep_average
        self.treatment_id = treatment_id
        self.time = time
    
    def __str__(self):
        return f"Id: {self.id}, Name: {self.child_name}, Sleep Avg: {self.sleep_average}, Treatment: {self.treatment_id}, Time: {self.time}"

class ChildDAO:
    BASE_URL = 'http://localhost:10050/tapatappV1/'
    
    @staticmethod
    def get_child_by_name(child_name):
        """Obtiene la información de un niño por su nombre."""
        try:
            response = requests.get(f'{ChildDAO.BASE_URL}Child?name={child_name}')
            if response.status_code == 200:
                child_data = response.json()
                return Child(child_data['id'], child_data['child_name'], child_data['sleep_average'], child_data['treatment_id'], child_data['time'])
            else:
                print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None

# Clase ViewConsole para interactuar con el usuario
class ViewConsole:
    @staticmethod
    def get_input(prompt):
        """Solicita al usuario que ingrese un dato."""
        value = input(prompt).strip()
        while not value:
            print("Error: El valor no puede estar vacío.")
            value = input(prompt).strip()
        return value
    
    @staticmethod
    def show_user_info(username):
        """Muestra la información de un usuario."""
        user = UserDAO.get_user_by_username(username)
        if user:
            print(f"User Info: {user}")
        else:
            print(f"User with username '{username}' not found.")
    
    @staticmethod
    def show_child_info(child_name):
        """Muestra la información de un niño."""
        child = ChildDAO.get_child_by_name(child_name)
        if child:
            print(f"Child Info: {child}")
        else:
            print(f"Child with name '{child_name}' not found.")

if __name__ == "__main__":
    while True:
        print("\n--- MENU ---")
        print("1. Buscar usuario por username")
        print("2. Buscar niño por nombre")
        print("3. Salir")
        choice = input("Seleccione una opción: ")
        
        if choice == "1":
            username = ViewConsole.get_input("Ingrese el username: ")
            ViewConsole.show_user_info(username)
        elif choice == "2":
            child_name = ViewConsole.get_input("Ingrese el nombre del niño: ")
            ViewConsole.show_child_info(child_name)
        elif choice == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

