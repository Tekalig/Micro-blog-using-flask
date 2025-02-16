from marshmallow import Schema, fields

class PlainPostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)

class UpdatePostSchema(Schema):
    title = fields.Str()
    content = fields.Str()