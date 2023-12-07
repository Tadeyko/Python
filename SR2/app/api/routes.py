from flask import jsonify, request, Blueprint
from werkzeug.exceptions import BadRequest, NotFound
from extensions import db
from .models import Todo

api_bp = Blueprint('api', __name__)

@api_bp.route('/todos', methods=['GET'])
def get_todos():
    foundTodos = Todo.query.all()
    result = [{"id": todo.id, "title": todo.title, "complete": todo.complete, "description": todo.description} for todo in foundTodos]
    return jsonify(result)

@api_bp.route('/todos', methods=['POST'])
def create_todo():
    body = request.get_json()
    if 'title' in body and 'description' in body:
        createdTodo = Todo(title=body['title'], complete=body.get('complete', False), description=body['description'])
        db.session.add(createdTodo)
        db.session.commit()
        return jsonify({"message": "Todo created successfully"}), 201
    else:
        raise BadRequest('Title and description are required fields.')

@api_bp.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    foundTodo = Todo.query.get(id)
    if foundTodo:
        todo_data = {"id": foundTodo.id, "title": foundTodo.title, "complete": foundTodo.complete, "description": foundTodo.description}
        return jsonify(todo_data)
    else:
        raise NotFound('Todo not found for the specified id.')

@api_bp.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    foundTodo = Todo.query.get(id)
    body = request.get_json()
    if foundTodo:
        if 'title' in body or 'description' in body:
            foundTodo.title = body['title']
            foundTodo.complete = body.get('complete', False)
            foundTodo.description = body['description']
            db.session.commit()
            return jsonify({"message": "Todo updated successfully"})
        else:
            raise BadRequest('Title and description are required fields.')
    else:
        raise NotFound('Todo not found for the specified id.')

@api_bp.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    foundTodo = Todo.query.get(id)
    if foundTodo:
        db.session.delete(foundTodo)
        db.session.commit()
        return jsonify({"message": "Todo deleted successfully"})
    else:
        raise NotFound('Todo not found for the specified id.')

    
