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
    @staticmethod
    def get_user_by_username(username):
        """Obtiene la información de un usuario por su nombre de usuario."""
        try:
            # Hacer la solicitud al backend con la ruta correcta
            response = requests.get(f'http://localhost:10050/tapatappV1/Username?username={username}')
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                user_data = response.json()
                user = User(user_data['id'], user_data['username'], None, user_data['email'])  # Password como None
                return user
            else:
                # Manejar errores
                print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            # Manejar errores de conexión
            print(f"Error de conexión: {e}")
            return None

class ViewConsole:
    @staticmethod
    def get_input_username():
        """Solicita al usuario que ingrese un nombre de usuario."""
        username = input("Enter username: ").strip()
        while not username:
            print("Error: El nombre de usuario no puede estar vacío.")
            username = input("Enter username: ").strip()
        return username
    
    @staticmethod
    def show_user_info(username):
        """Muestra la información de un usuario."""
        user = UserDAO.get_user_by_username(username)
        if user:
            print(f"User Info: {user}")
        else:
            print(f"User with username '{username}' not found.")

if __name__ == "__main__":
    # Solicitar el nombre de usuario al usuario
    username = ViewConsole.get_input_username()
    
    # Mostrar la información del usuario
    ViewConsole.show_user_info(username)