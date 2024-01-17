from flask import Blueprint, request, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from marshmallow import ValidationError
from flask_marshmallow import Marshmallow
from extensions import db
from app.account.models import User

api_users = Blueprint('api_user', __name__)
api = Api(api_users)

ma = Marshmallow(api_users)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'image_file': fields.String,
    'password': fields.String,
    'about_me': fields.String,
    'last_seen': fields.DateTime(dt_format='rfc822')
}

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get(id)

        if not user:
            return {'message': "Користувач не існує"}, 400
        
        return user

    @marshal_with(user_fields)
    def put(self, id):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'Введіть дані'}, 400
        
        try:
            parsed_args = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        user = User.query.get(id)

        if not user:
            return {'message': "Користувач не існує"}, 400

        user.username = parsed_args.username
        user.email = parsed_args.email

        db.session.add(user)
        db.session.commit()

        return user, 201

    def delete(self, id):
        user = User.query.get(id)

        if not user:
            return {'message': "Користувач не існує"}, 400

        db.session.delete(user)
        db.session.commit()

        return {}, 204

class UserListResource(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        json_data = request.get_json()

        if not json_data:
            return {'message': 'Введіть дані'}, 400
        
        try:
            parsed_args = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        exist_user = User.query.filter_by(username=parsed_args.username).first()
        if exist_user:
            return {"message": "Користувач вже існує"}, 401
        
        user = User(username=parsed_args.username, email=parsed_args.email, password=parsed_args.password)
        db.session.add(user)
        db.session.commit()

        return user, 201

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')