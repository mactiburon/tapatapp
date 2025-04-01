class Historial:
    def __init__(self, id, child_id, data, hora, estat, totalHores):
        self.id = id
        self.child_id = child_id
        self.data = data  # Fecha en formato YYYY-MM-DD
        self.hora = hora  # Hora en formato HH:MM:SS
        self.estat = estat  # Estado del sueño
        self.totalHores = totalHores  # Total horas dormidas

    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "data": self.data,
            "hora": self.hora,
            "estat": self.estat,
            "totalHores": self.totalHores
        }