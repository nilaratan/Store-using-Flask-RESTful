from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import User
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db


# creating flask app
app = Flask(__name__)
app.secret_key = 'secret'  # secret key for jwt

# jwt configuration
app.config["JWT_AUTH_URL_RULE"] = "/login"  # changing the default auth endpoint /auth to /login
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=600)  # setting jwt token expiration time
# app.config["JWT_AUTH_USERNAME_KEY"] = "email"  # used to change default auth key username to email
jwt = JWT(app, authenticate, identity)  # creating jwt instance


# custom jwt error message
@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        "message": error.description,
    }), error.status_code


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        "access_token": access_token.decode("utf-8"),
        "user_id": identity.id
    })


#  Sqlalchemy settings
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"


# automatically creating the databases

db.init_app(app)


@app.before_first_request
def create_all_db():
    db.create_all()


# adding end points to api
api = Api(app)
api.add_resource(Item, '/item', '/item/<string:name>')
api.add_resource(ItemList, "/items")
api.add_resource(User, "/register", "/users")
api.add_resource(Store, "/store", "/store/<string:name>")
api.add_resource(StoreList, "/stores")
if __name__ == "__main__":
    app.run(port=5000, debug=True)
