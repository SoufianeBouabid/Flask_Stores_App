from db import db


class ItemModel(
    db.Model
):  # this becomes a maaping between a row ina table to a python class and therefore object
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)  # it will be prepopulated by postgres
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    description = db.Column(db.String)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")

    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
