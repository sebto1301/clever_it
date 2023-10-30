from datetime import datetime
from app import db
from app.models.tag import Tag
from app.models.task import Task


def create_task(data):
    """Creates task with provided data"""
    tags = data.get('tags')

    new_task = Task(title=data['title'], description=data['description'],
                    due_date=data['due_date'], status=data['status'])
    new_task.set_tags(tags)

    db.session.add(new_task)
    db.session.commit()


def task_to_dict(task):
    """Converts task object to dictionary"""
    tags = []
    for tag in task.tags:
        tags.append(tag.name)

    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.strftime('%Y-%m-%d'),
        'status': task.status,
        'tags': tags
    }


def get_tasks():
    """Get all tasks"""
    tasks = Task.query.all()
    return [task_to_dict(x) for x in tasks]


def get_task(task_id):
    """Get an specific task"""
    task = db.session.get(Task, task_id)
    if not task:
        raise FileNotFoundError
    return task_to_dict(task)


def update_task(task_id, fields):
    """Update task data, removes the current tags if those are not added"""
    task = db.session.get(Task, task_id)
    if not task:
        raise FileNotFoundError
    if 'title' in fields:
        task.title = fields['title']
    if 'description' in fields:
        task.description = fields['description']
    if 'due_date' in fields:
        task.due_date = datetime.strptime(
            fields['due_date'].strip(), "%Y-%m-%d").date()
    if 'status' in fields:
        task.status = fields['status']
    tags = fields['tags']

    task.set_tags(tags, remove_if_not_exist=True)

    db.session.commit()


def delete_task(task_id):
    """Delete a task"""
    task = db.session.get(Task, task_id)
    if not task:
        raise FileNotFoundError
    db.session.delete(task)
    db.session.commit()


def add_tag_to_task(task_id, tag_name):
    """Add tag to an specific task by id"""
    task = db.session.get(Task, task_id)
    if not task:
        raise FileNotFoundError
    task.set_tags(tag_name)
    db.session.commit()


def remove_tag(task_id, tag_name):
    """Removes tag of a task"""
    task = db.session.get(Task, task_id)
    if not task:
        raise FileNotFoundError

    task.unset_tags(tag_name)
    db.session.commit()

    tag = Tag.query.filter_by(name=tag_name.lower()).first()
    if tag:
        tag.clean_unused()


def update_status(task_id, status):
    """Updates the status of a task"""
    task = db.session.get(Task, task_id)
    if not task:
        raise FileNotFoundError

    task.status = status
    db.session.commit()
