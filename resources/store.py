from models.store import StoreModel
from flask_restful import Resource, reqparse


class Store(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument("name", type=str, required=True, help="This field is required.")
    put_req_parser = reqparse.RequestParser()
    put_req_parser.add_argument("id", type=int, required=True, help="This field is required.")
    put_req_parser.add_argument("name", type=str, required=True, help="This field is required.")

    def get(self, name):
        try:
            store = StoreModel.get_store_by_name(name)
            if store:
                return store.get_json(), 200
            return {"message": "Store with this name is not found."}, 404
        except:
            return {"message": "An error has occurred while fetching the store."}, 500

    def post(self):
        data = self.req_parser.parse_args()
        store = StoreModel(**data)
        if StoreModel.get_store_by_name(data["name"]):
            return {"message": "Store name is already exist."}, 400
        try:
            store.save_to_db()
            return store.get_json(), 201
        except:
            return {"message": "An error has occurred while creating the store."}, 500

    def delete(self, name):
        store = StoreModel.get_store_by_name(name)
        if store:
            try:
                store.delete()
                return {"message": "Store deleted successfully."}, 202
            except:
                return {"message": "An error has occurred while deleting the store."}, 500
        return {"message": "No such store exists."}, 400

    def put(self):
        data = self.put_req_parser.parse_args()
        store = StoreModel.get_store_by_id(data["id"])
        if store:
            try:
                update_store = StoreModel(data["name"])
                update_store.save_to_db()
                return update_store.get_json()
            except:
                return {"message": "An error has occurred while updating the store."}
        return {"message": "Store does not exist."}


class StoreList(Resource):

    def get(self):
        return {"stores":list(store.get_json().get("name") for store in StoreModel.query.all())}
