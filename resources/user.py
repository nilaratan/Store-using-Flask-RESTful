import sqlite3
from models.user import UserModel
from flask_restful import Resource, reqparse


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field is required.")
    parser.add_argument("password", type=str, required=True, help="This field is required.")

    def post(self):
        data = User.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "User is already exist."}, 400
        try:
            user = UserModel(**data)
            user.save_to_db()
            return {"message": "Registered successfully."}, 201
        except:
            return {"message": "An error has occurred while registration."}, 500

    def get(self):
        return {"users": [ user.get_json() for user in UserModel.query.all()]}
