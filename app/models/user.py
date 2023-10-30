import re
import jwt
from app import db, JWT_KEY


class User(db.Model):
    """User to be stored"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    db.Index('names', 'name')

    def __init__(self, name):
        regex_not_allowed_chars = r"[\d\,]"
        name = name.strip().capitalize()

        if name == "":
            raise ValueError("Empty names not allowed")
        if re.search(regex_not_allowed_chars, name):
            raise ValueError(f"{name} is not allowed as a name.")

        self.name = name

    def calculate_token(self):
        """Returns the token for a user"""
        payload = {
            'sub': self.id,
            'name': self.name
        }
        return jwt.encode(payload, JWT_KEY, algorithm='HS256')
