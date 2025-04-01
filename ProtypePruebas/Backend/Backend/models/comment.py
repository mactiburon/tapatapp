from datetime import datetime

class Comment:
    def __init__(self, id, child_id, user_id, text, important, timestamp=None):
        self.id = id
        self.child_id = child_id
        self.user_id = user_id
        self.text = text
        self.important = bool(important)
        self.timestamp = timestamp if timestamp else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "child_id": self.child_id,
            "user_id": self.user_id,
            "text": self.text,
            "important": self.important,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }