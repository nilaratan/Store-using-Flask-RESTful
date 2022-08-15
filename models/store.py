from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    items = db.relationship('ItemModel', backref='stores', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_store_by_name(cls, name):
        store = cls.query.filter_by(name=name).first()
        return store

    @classmethod
    def get_store_by_id(cls, id):
        store = cls.query.filter_by(id=id).first()
        return store

    def get_json(self):
        return {"id": self.id, "name": self.name, "items": list(item.get_json() for item in self.items)}
    