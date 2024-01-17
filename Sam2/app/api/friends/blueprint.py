from extensions import db
from flask import jsonify, request, Blueprint
from .models import Friend
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required

api_friends = Blueprint('api_friends', __name__)

@api_friends.route('/friends', methods=['GET'])
def get_all_friends():
    found_friends = Friend.query.all()
    mapped = [{"id": friend.id, "name": friend.name, "age": friend.age, "hobby": friend.hobby} for friend in found_friends]
    return jsonify(mapped)

@api_friends.route('/friends', methods=['POST'])
@jwt_required()
def create_new_friend():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    hobby = data.get('hobby')

    if not name:
        return jsonify({"message": "Додайте ім'я"}), 400
    
    if not age:
        return jsonify({"message": "Додайте вік"}), 400

    if not hobby:
        return jsonify({"message": "Додайте хоббі"}), 400

    new_friend = Friend(name=name, age=age, hobby=hobby)
    db.session.add(new_friend)
    db.session.commit()
    return jsonify({"message": "Друга було додано"}), 201

@api_friends.route('/friends/<int:id>', methods=['GET'])
def get_friend_by_id(id):
    found_friend = Friend.query.get(id)

    if not found_friend:
        raise NotFound('Невірний id')

    mapped = {"id": found_friend.id, "name": found_friend.name, "age": found_friend.age, "hobby": found_friend.hobby}
    return jsonify(mapped)

@api_friends.route('/friends/<int:id>', methods=['PUT'])
@jwt_required()
def update_friend(id):
    friend_to_update = Friend.query.get(id)

    if not friend_to_update:
        raise NotFound('Невірний id.')

    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    hobby = data.get('hobby')

    if not name:
        return jsonify({"message": "Додайте ім'я"}), 400
    
    if not age:
        return jsonify({"message": "Додайте вік"}), 400

    if not hobby:
        return jsonify({"message": "Додайте хоббі"}), 400

    friend_to_update.name = name
    friend_to_update.age = age
    friend_to_update.hobby = hobby

    db.session.commit()

    return jsonify({"message": "Друга оновлено"})

@api_friends.route('/friends/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    friend_to_delete = Friend.query.get(id)

    if not friend_to_delete:
        raise NotFound('Невірний id.')

    db.session.delete(friend_to_delete)
    db.session.commit()
    return jsonify({"message": "Друга видалено"})