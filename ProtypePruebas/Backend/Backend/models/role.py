class Role:
    def __init__(self, id, type_rol, description=None):
        self.id = id
        self.type_rol = type_rol
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "type_rol": self.type_rol,
            "description": self.description
        }