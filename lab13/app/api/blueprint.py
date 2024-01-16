from extensions import db
from flask import jsonify, request, Blueprint
from app.tasks.models import Todo
from werkzeug.exceptions import BadRequest, NotFound

api = Blueprint('api', __name__)

@api.route('/todos', methods=['GET'])
def get_all_todos():
    found_todos = Todo.query.all()
    mapped = [{"id": todo.id, "title": todo.title, "complete": todo.complete, "description": todo.description} for todo in found_todos]
    return jsonify(mapped)

@api.route('/todos', methods=['POST'])
def create_new_todo():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    complete = data.get('complete', False)

    if not title or not description:
        raise BadRequest('Додайте загаловок та опис')

    new_todo = Todo(title=title, complete=complete, description=description)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Завдання було додано"}), 201

@api.route('/todos/<int:id>', methods=['GET'])
def get_todo_by_id(id):
    found_todo = Todo.query.get(id)

    if not found_todo:
        raise NotFound('Невірний id')

    mapped = {"id": found_todo.id, "title": found_todo.title, "complete": found_todo.complete, "description": found_todo.description}
    return jsonify(mapped)

@api.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo_to_update = Todo.query.get(id)

    if not todo_to_update:
        raise NotFound('Невірний id.')

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    complete = data.get('complete', False)

    if not title or not description:
        raise BadRequest('Додайте загаловок та опис')

    todo_to_update.title = title
    todo_to_update.complete = complete
    todo_to_update.description = description

    db.session.commit()

    return jsonify({"message": "Завдання оновлено"})

@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo_to_delete = Todo.query.get(id)

    if not todo_to_delete:
        raise NotFound('Невірний id.')

    db.session.delete(todo_to_delete)
    db.session.commit()
    return jsonify({"message": "Завдання видалено"})