from extensions import db, auth
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from app.account.models import User
from werkzeug.security import generate_password_hash, check_password_hash

api_auth = Blueprint('api_auth', __name__)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            return username
        
    return None
    
@api_auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username:
        return jsonify({"message": "Надішліть username"}), 401
    
    if not password:
        return jsonify({"message": "Надішліть пароль"}), 401
    
    if not email:
        return jsonify({"message": "Надішліть email"}), 401
    
    exist_user = User.query.filter_by(username=username).first()

    if not exist_user:
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Реєстрація пройшла успішно"}) 

    return jsonify({"message": "Користувач вже існує"}), 401
    

@api_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username:
        return jsonify({"message": "Надішліть username"}), 401
    
    if not password:
        return jsonify({"message": "Надішліть password"}), 401
    
    exist_user = User.query.filter_by(username=username).first()

    if exist_user:
        if check_password_hash(exist_user.password, password):
            return jsonify(
                access_token=create_access_token(identity=username), 
                refresh_token=create_refresh_token(identity="example_user")
            )
        else:
            return jsonify({"message": "Невірний пароль"}), 401
    else:
        return jsonify({"message": "Користувача не знайдено"}), 401
    
@api_auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return jsonify(access_token=create_access_token(identity=identity))