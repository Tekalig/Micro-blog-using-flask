from marshmallow import Schema, fields

class PlainPostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    posted_date = fields.Date(dump_only=True)
    updated_date = fields.Date(dump_only=True)

class PlainCommentSchema(Schema):
    id = fields.Int(dump_only=True)
    comment = fields.Str(required=True)
    post_id = fields.Int(required=True)
    commented_date = fields.Date(dump_only=True)
    updated_date = fields.Date(dump_only=True)

class UpdateCommentSchema(Schema):
    comment = fields.Str()
    updated_date = fields.Date()

class UpdatePostSchema(Schema):
    title = fields.Str()
    content = fields.Str()
    updated_date = fields.Date()