from marshmallow import Schema, fields, post_load, ValidationError
from models import User

class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class UserFullInfoSchema(CreateUserSchema):
    id = fields.Int(required=True)

class UserPublicInfoSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    surname = fields.Str()
    email = fields.Email()

class UserTaskInfoSchema(Schema):
    id = fields.Int()
    task_id = fields.Int()
    name = fields.Str()
    status = fields.Str()
    description = fields.Str()