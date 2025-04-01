from datetime import datetime

class Tap:
    def __init__(self, id, child_id, status_id, user_id, init, end, created_at=None):
        self.id = id
        self.child_id = child_id
        self.status_id = status_id
        self.user_id = user_id
        self.init = init
        self.end = end
        self.created_at = created_at if created_at else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "status_id": self.status_id,
            "user_id": self.user_id,
            "init": self.init,
            "end": self.end,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }