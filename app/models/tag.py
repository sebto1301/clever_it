import re
from app.models.task import tag_task
from app import db

class Tag(db.Model):
    """Tag to be stored"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __init__(self, name):
        regex_not_allowed_chars = r"[\x00-\x08\x0E-\x1F\s.,]"
        name = name.strip().lower()

        if re.search(regex_not_allowed_chars, name):
            raise ValueError(f"{name} is not allowed as a tag.")

        self.name = name

    def clean_unused(self):
        """Delete tag if is not in any task"""
        conn = db.engine.connect()
        query = tag_task.select().where(tag_task.c.tag_id == self.id)
        result = conn.execute(query)
        conn.close()

        if not result.all():
            db.session.delete(self)

