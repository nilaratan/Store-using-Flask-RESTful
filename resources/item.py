from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    req_parser = reqparse.RequestParser()
    req_parser.add_argument("name", type=str, required=True, help="This field cant be left blank.")
    req_parser.add_argument("price", type=float, required=True, help="This field cant be left blank.")
    req_parser.add_argument("store_id", type=int, required=True, help="This field cant be left blank.")

    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.get_json(), 200
        return {"message": "Item is not found."}, 404

    @jwt_required()
    def post(self):
        data = Item.req_parser.parse_args()
        item = ItemModel(**data)
        if ItemModel.find_item_by_name(data["name"]) is None:
            try:
                item.save_to_db()
                return item.get_json(), 201
            except:
                return {"message": "An error has occurred while inserting."}, 500
        return {"message": "Item is already exist"}, 400

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            try:
                item.delete()
                return {"message": "Item deleted successfully."}, 202
            except:
                return {"message": "An error has occurred while deleting."}, 500
        return {"message": "Item not found."}, 404

    @jwt_required()
    def put(self):
        data = Item.req_parser.parse_args()
        item = ItemModel.find_item_by_name(data["name"])
        if item is None:
            item = ItemModel(**data)
        try:
            item.save_to_db()
            return item.get_json()
        except:
            return {"message": "An error has occurred while updating."}, 500


class ItemList(Resource):

    def get(self):
        return {"items": list(map(lambda item: item.get_json(), ItemModel.query.all()))}, 200
