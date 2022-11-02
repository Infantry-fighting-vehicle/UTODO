from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

from venv import create
from click import echo
from flask import Flask, jsonify, request, abort
import json

from marshmallow import Schema, ValidationError, fields, post_load

connection_string = 'mysql://root:000000@127.0.0.1:3306/utodolist'
engine = create_engine(connection_string, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

class CreateUserSchema(Schema):
    name = fields.Str()
    surname = fields.Str()
    email = fields.Email()
    password = fields.Str()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class UserFullInfoSchema(CreateUserSchema):
    id = fields.Int()

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

@app.route('/user', methods=['POST', 'PUT'])
def user():
    if request.method == 'POST':
        try:
            new_user = CreateUserSchema().load(request.json)
        except ValidationError:
            abort(400)
        session.add(new_user)
        session.commit()
        return jsonify(UserFullInfoSchema().dump(
            session.query(User).filter(User.email == new_user.email).first()))
    elif request.method == 'PUT':
        try:
            user = UserFullInfoSchema().load(request.json)
        except ValidationError:
            abort(400)
        session.query(User).filter(User.id == user.id).update(UserFullInfoSchema().dump(user))
        session.commit()
        return jsonify(UserFullInfoSchema().dump(
            session.query(User).filter(User.email == new_user.email).first()))

@app.route('/user/login', methods=['GET'])
def login():
    email = request.args.get("email")
    password = request.args.get("password")

    user = session.query(User).filter(User.email==email).first()
    if user and user.password==password:
        return UserFullInfoSchema().dump(user)
    elif user:
        abort(403)
    else:
        abort(404)

@app.route('/user/logout', methods=['GET'])
def logout():
    return jsonify({'Message': 'Successfully logged out =)'})

@app.route('/user/<user_id>', methods=['GET', 'DELETE'])
def user_by_id(user_id):
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(UserPublicInfoSchema().dump(user))
    elif request.method == 'DELETE':
        session.query(User).filter(User.id==user_id).delete()
        session.commit()
        return jsonify({'Message': 'Successfully deleted =)'})

# temporary use query for defining the user
@app.route('/user/tasks', methods=['GET'])
def get_user_tasks():
    user_id = request.args.get("id")
    user_tasks = session.query(UserTask)\
        .filter(UserTask.user_id==user_id).all()

    tasks = []
    for user_task in user_tasks:
        tasks.append(UserTaskInfoSchema().dump(user_task))
    return jsonify(tasks)

# temporary use query for defining the user
@app.route('/user/tasks/<task_id>', methods=['GET'])
def change_user_task_status(task_id):
    status = request.args.get("status")
    user_task = session.query(UserTask)\
        .filter(UserTask.task_id==task_id).first()
    if not user_task:
        abort(404)

    user_task.status = status
    session.commit()
    return jsonify(UserTaskInfoSchema().dump(user_task))











# temporary use query for defining the user
@app.route('/user/update/<user_id>', methods=['PUT'])
def test_update(user_id):
    new_name = request.args.get("name")
    user = session.query(User)\
        .filter(User.id==user_id).first()
    if not user:
        abort(404)
    user.name = new_name
    session.commit()

    return jsonify(UserFullInfoSchema().dump(user))

@app.route(f'/user/byname/<user_name>', methods=['GET'])
def get_user(user_name):
    user = session.query(User).filter(User.name==user_name).first()
    if user:
        return jsonify(UserPublicInfoSchema().dump(user))
    else:
        abort(404)

@app.route(f'/users', methods=['GET'])
def get_users():
    users = []
    for user in session.query(User).all():
        users.append(UserPublicInfoSchema().dump(user))
    return jsonify(users)



@app.errorhandler(400)
def BadRequest(e):
    return jsonify({'Error': 'Invalid input'}), 400

@app.errorhandler(401)
def Unauthorized(e):
    return jsonify({'Error': 'Unauthorized user'}), 401

@app.errorhandler(403)
def Forbidden(e):
    return jsonify({'Error': 'The user does not have the necessary permissions for the resource'}), 403

@app.errorhandler(404)
def NotFound(e):
    return jsonify({'Error': 'The resourse is not found'}), 404