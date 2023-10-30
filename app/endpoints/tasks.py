from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services import tasks

task_bp = Blueprint('task', __name__)


@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """Endpoint to create a task"""
    data = request.get_json()

    try:
        tasks.create_task(data)
    except KeyError:
        return jsonify({'message': 'Missing fields'}), 422
    except ValueError as error:
        return jsonify({'message': str(error)}), 422

    return jsonify({'message': 'Tarea creada con éxito!'})


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Ruta para obtener todas las tareas"""
    return jsonify({'tasks': tasks.get_tasks()})


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get an specific task endpoint"""
    try:
        task = tasks.get_task(task_id)
    except FileNotFoundError:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required
def update_task(task_id):
    """Ruta para actualizar una tarea"""
    data = request.get_json()
    try:
        tasks.update_task(task_id, data)
    except FileNotFoundError:
        return jsonify({'error': 'Task not found'}), 404
    except KeyError:
        return jsonify({'message': 'Missing fields'}), 422
    except ValueError as error:
        return jsonify({'message': str(error)}), 422

    return jsonify({'message': 'Updated task successfully!'})


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Ruta para eliminar una tarea"""
    try:
        tasks.delete_task(task_id)
    except FileNotFoundError:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Removed task successfully!'})


@task_bp.route('/tasks/<int:task_id>/<string:tag_name>', methods=['POST'])
@jwt_required()
def add_tag_to_task(task_id, tag_name):
    """Add tag to an specific task by id"""
    try:
        tasks.add_tag_to_task(task_id, tag_name)
    except FileNotFoundError:
        return jsonify({'error': 'Task not found'}), 404
    except ValueError as error:
        return jsonify({'message': str(error)}), 422

    return jsonify({'message': f'{tag_name} added as a tag'})


@task_bp.route('/tasks/<int:task_id>/<string:tag_name>', methods=['DELETE'])
@jwt_required()
def remove_tag(task_id, tag_name):
    """Rest endpoint for remotion tag of a task"""
    try:
        tasks.remove_tag(task_id, tag_name)
    except FileNotFoundError:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': f'Successfully removed tag {tag_name}.'})


@task_bp.route('/tasks/status/<int:task_id>/<string:status>', methods=['POST'])
@jwt_required()
def update_status(task_id, status):
    """Rest endpoint to update status"""
    try:
        tasks.update_status(task_id, status)
    except FileNotFoundError:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': f'Successfully updated status to {status}.'})
