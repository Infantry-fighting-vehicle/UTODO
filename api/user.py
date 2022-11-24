
from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash
from db import get_session
from models import *
from schemas import *

from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth


user = Blueprint('user', __name__, url_prefix='/user')
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    session = get_session()
    user = session.query(User).filter(User.email == username).first()
    if not user:
        return False
    if check_password_hash(user.password, password):
        return True
    return False

def get_current_user() -> User:
    Session = get_session()
    username = auth.username()
    return Session.query(User).filter(User.email==username).first()

@user.route('', methods=['PUT'])
@auth.login_required
def user_update():
    session = get_session()
    
    for key, val in request.json.items():
        if key == 'password':
            val = generate_password_hash(val)
        session.query(User).filter(User.id == get_current_user().id).update({key: val})
        print(key, val)

    session.commit()
    return jsonify(UserFullInfoSchema().dump(
        session.query(User).filter(User.id == get_current_user().id).first()))

@user.route('', methods=['POST'])
def user_create():
    session = get_session()

    print(request.get_json())
    try:
        print()
        user = CreateUserSchema().load(request.get_json())
    except (ValidationError, AssertionError):
        abort(400)

    if 'password' in request.json:
        user.password = generate_password_hash(user.password)

    session.add(user)
    session.commit()
    return jsonify(UserFullInfoSchema().dump(
        session.query(User).filter(User.id == get_current_user().id).first()))


@user.route('/<user_id>', methods=['GET', 'DELETE'])
@auth.login_required
def user_by_id(user_id):
    session = get_session()
    if not user_id.isnumeric():
        abort(400)

    user = session.query(User).filter(User.id==user_id).first()
    if user is None:
        return {
                'code': 'user',
                'message': 'User not found',
            }, 404
    try:
        if get_current_user().id != user.id:
                return {
                    'code': 'user',
                    'message': 'Unauthorized user access/No rights',
                }, 401
    except Exception as e:
        abort(e)

    if request.method == 'GET':
        return jsonify(UserPublicInfoSchema().dump(user))
    elif request.method == 'DELETE':
        session.query(User).filter(User.id==user_id).delete()
        session.commit()
        return jsonify({'Message': 'Successfully deleted =)'})

# temporary use query for defining the user
@user.route('/tasks', methods=['GET'])
@auth.login_required
def get_user_tasks():
    session = get_session()
    user_id = get_current_user().id #temporary
    user_tasks = session.query(UserTask).filter(UserTask.user_id==user_id).all()

    tasks = []
    for user_task in user_tasks:
        group_task = session.query(GroupTask).filter(GroupTask.id==user_task.groupTask_id).first()
        tasks.append(UserTaskInfoSchema().dump(user_task))
        tasks[-1]["task_id"] = group_task.id
        tasks[-1]["name"] = group_task.name
        tasks[-1]["description"] = group_task.description
    return jsonify(tasks)

# temporary use query for defining the user
@user.route('/tasks/<task_id>', methods=['GET', 'PUT'])
@auth.login_required
def change_user_task_status(task_id):
    session = get_session()
    if not task_id.isnumeric():
        abort(400)

    user_task = session.query(UserTask)\
        .filter(UserTask.groupTask_id==task_id).first()
    if not user_task:
        abort(404)

    if get_current_user().id != user_task.user_id:
        return {
            'code': 'user',
            'message': 'Unauthorized user access/No rights',
        }, 401

    def get_fullinfo_task(user_task):
        group_task = session.query(GroupTask).filter(GroupTask.id==user_task.groupTask_id).first()
        task = UserTaskInfoSchema().dump(user_task)
        task["task_id"] = group_task.id
        task["name"] = group_task.name
        task["description"] = group_task.description
        task["status"] = user_task.status
        return task

    if request.method == 'GET':
        return jsonify(get_fullinfo_task(user_task))
    elif request.method == 'PUT':
        status = request.args.get("status")
        if status not in ['done', 'undone', 'in_progress']:
            abort(400)
        user_task.status = status
        session.commit()
        return jsonify(get_fullinfo_task(user_task))


# @user.route('/byname/<user_name>', methods=['GET'])
# def get_user(user_name):
#     session = get_session()
#     user = session.query(User).filter(User.name==user_name).first()
#     if user:
#         return jsonify(UserPublicInfoSchema().dump(user))
#     else:
#         abort(404)

# @user.route(f'/all', methods=['GET'])
# def get_users():
#     session = get_session()
#     users = []
#     for user in session.query(User).all():
#         users.append(UserFullInfoSchema().dump(user))
#     return jsonify(users)