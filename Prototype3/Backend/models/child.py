from datetime import datetime

class Child:
    def __init__(self, id, child_name, sleep_average, treatment_id, time, informacioMedica, created_at=None):
        self.id = id
        self.child_name = child_name
        self.sleep_average = sleep_average
        self.treatment_id = treatment_id
        self.time = time
        self.informacioMedica = informacioMedica
        self.created_at = created_at if created_at else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "child_name": self.child_name,
            "sleep_average": self.sleep_average,
            "treatment_id": self.treatment_id,
            "time": self.time,
            "informacioMedica": self.informacioMedica,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }