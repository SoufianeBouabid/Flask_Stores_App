from marshmallow import Schema, fields

class ItemSchema(Schema):
    id = fields.Str(dump_only=True) #ID should not be expected or considered when parsing incoming JSON data to create an item (deserialization).
    name = fields.Str(required=True)  #required for both req and res
    price=fields.Float(required=True)
    store_id=fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price=fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)

