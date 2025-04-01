from datetime import datetime

class User:
    def __init__(self, id, username, password, email, role_id, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role_id = role_id
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role_id": self.role_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }