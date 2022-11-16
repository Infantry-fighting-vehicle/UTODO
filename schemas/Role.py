from marshmallow import Schema, fields

class RoleSchema(Schema):
    id = fields.Int()
    value = fields.Str()