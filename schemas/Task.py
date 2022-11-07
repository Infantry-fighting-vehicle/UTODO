from marshmallow import Schema, fields, post_load, ValidationError
from models import GroupTask

class CreateTaskSchema(Schema):
    group_id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    @post_load
    def make_user(self, data, **kwargs):
        return GroupTask(**data)

class GroupTaskInfoSchema(CreateTaskSchema):
    id = fields.Int()

class UserTaskInfoSchema(Schema):
    id = fields.Int()
    task_id = fields.Int()
    user_id = fields.Int()
    name = fields.Str()
    status = fields.Str() # done or undone
    description = fields.Str()
