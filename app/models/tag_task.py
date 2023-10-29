from app import db

tag_task = db.Table('tag_task',
                    db.Column('tag_id', db.Integer, db.ForeignKey(
                              'tag.id'), primary_key=True),
                    db.Column('task_id', db.Integer, db.ForeignKey(
                              'task.id'), primary_key=True)
                    )

db.Index('tasks', tag_task.c.task_id)
