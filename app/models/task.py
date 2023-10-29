from datetime import datetime
from app import db
from app.models.tag_task import tag_task


class Task(db.Model):
    """Task table"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pendiente')
    tags = db.relationship(
        'Tag', secondary=tag_task, lazy='subquery', backref=db.backref('tasks', lazy=True))

    db.Index('dates', 'due_date')
    db.Index('title', 'title')
    db.Index('status-date', 'due_date', 'status')

    def __init__(self, title, description, due_date, status):
        self.title = title.strip()
        self.description = description.strip()
        self.due_date = datetime.strptime(due_date.strip(), "%Y-%m-%d").date()
        self.status = status.strip()

    def set_tags(self, tags, remove_if_not_exist=False):
        """Method to add tags to a task"""
        from app.models.tag import Tag
        if isinstance(tags, str):
            tags = [tags]
        elif not isinstance(tags, list):
            raise TypeError

        if remove_if_not_exist:
            tags_to_remove = []
            for tag in self.tags:
                if tag.name not in tags:
                    tags_to_remove.append(tag)
            self.unset_tags(tags_to_remove)

        for tag_word in tags:
            tag = Tag.query.filter_by(name=tag_word.lower()).first()
            if tag is None:
                tag = Tag(name=tag_word)
            self.tags.append(tag)

    def unset_tags(self, tags):
        """Remove tags from a task"""
        from app.models.tag import Tag
        if isinstance(tags, str) or isinstance(tags, Tag):
            tags = [tags]
        elif not isinstance(tags, list):
            raise TypeError

        for tag_name in tags:
            if isinstance(tag_name, str):
                tag = Tag.query.filter_by(name=tag_name.lower()).first()
            elif isinstance(tag_name, Tag):
                tag = tag_name
            else:
                raise TypeError
            if tag:
                if tag in self.tags:
                    self.tags.remove(tag)
