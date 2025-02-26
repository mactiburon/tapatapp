import requests

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
        return f"Id: {self.id}, Nombre: {self.child_name}, Promedio de sueño: {self.sleep_average}, ID Tratamiento: {self.treatment_id}, Tiempo: {self.time}, Info médica: {self.informacioMedica}"

class NenDAO:
    @staticmethod
    def get_child_by_name(child_name):
        try:
            response = requests.get(f'http://localhost:5000/children/{child_name}')
            if response.status_code == 200:
                child_data = response.json()
                return Nen(
                    id=child_data['id'],
                    child_name=child_data['child_name'],
                    sleep_average=child_data['sleep_average'],
                    treatment_id=child_data['treatment_id'],
                    time=child_data['time'],
                    informacioMedica=child_data['informacioMedica'],
                    historialTapat=child_data['historialTapat']
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
    def get_input_child_name():
        child_name = input("Ingrese el nombre del niño: ").strip()
        while not child_name:
            print("Error: El nombre del niño no puede estar vacío.")
            child_name = input("Ingrese el nombre del niño: ").strip()
        return child_name

    @staticmethod
    def show_child_info(child_name):
        child = NenDAO.get_child_by_name(child_name)
        if child:
            print(f"Información del niño: {child}")
        else:
            print(f"No se encontró un niño con el nombre '{child_name}'.")

if __name__ == "__main__":
    child_name = ViewConsole.get_input_child_name()
    ViewConsole.show_child_info(child_name)
