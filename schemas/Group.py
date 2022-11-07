from marshmallow import Schema, fields, post_load, ValidationError
from models import Group

class CreateGroupSchema(Schema):
    owner_id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str()
    @post_load
    def make_user(self, data, **kwargs):
        return Group(**data)

class GroupInfoSchema(CreateGroupSchema):
    id = fields.Int()

class GroupMemberInfoSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    group_id = fields.Int()
    name = fields.Str()
    surname = fields.Str()
    email = fields.Email()
