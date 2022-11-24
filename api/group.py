from flask import Blueprint, request, jsonify, abort
from db import get_session
from models import *
from schemas import *
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

group = Blueprint('group', __name__, url_prefix='/groups')
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
# temporary using query parameters for user id
@group.route('', methods=['POST', 'GET'])
@auth.login_required
def groups():
    session = get_session()
    user_id = get_current_user().id #temporary

    if request.method == 'POST':
        try:
            new_group = CreateGroupSchema().load(request.json)
            new_group.owner_id = user_id
        except (ValidationError, AssertionError):
            abort(400)

        session.add(new_group)
        session.commit()
        session.refresh(new_group)

        # add owner to group members
        new_group_member = GroupMember(user_id=user_id, group_id=new_group.id)
        session.add(new_group_member)
        session.commit()
        return jsonify(GroupInfoSchema().dump(new_group))

    elif request.method == 'GET':
        memberships = session.query(GroupMember).filter(GroupMember.user_id==user_id)
        my_groups = []

        for membership in memberships:
            for group in session.query(Group).filter(Group.id==membership.group_id):
                my_groups.append(GroupInfoSchema().dump(group))
        return jsonify(my_groups)

@group.route('/<group_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def group_by_id(group_id):
    session = get_session()
    if not group_id.isnumeric():
        abort(400)

    group = session.query(Group).filter(Group.id==group_id).first()
    if not group:
        return {
                'code': 'group',
                'message': 'Group not found',
            }, 404

    if request.method == 'GET':
        membership = session.query(GroupMember).filter(GroupMember.user_id==get_current_user().id, GroupMember.group_id==group_id).first()
        if membership is None:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        return jsonify(GroupInfoSchema().dump(group))
    elif request.method == 'PUT':
        if get_current_user().id != group.owner_id:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        updated_info = dict()
        print(request.args.get("name"))
        if request.args.get("name"):
            updated_info["name"] = request.args.get("name")
        if request.args.get("description"):
            updated_info["description"] = request.args.get("description")
        
        for key, val in updated_info.items():
            session.query(Group).filter(Group.id==group.id).update({key: val})
        session.commit()
        session.refresh(group)
        return jsonify(GroupInfoSchema().dump(group))
    elif request.method == 'DELETE':
        if get_current_user().id != group.owner_id:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        session.query(Group).filter(Group.id==group.id).delete()
        session.commit()
        return jsonify({'Message': 'There is no such group now!'})

@group.route('/<group_id>/members', methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def group_members(group_id):
    session = get_session()
    if not group_id.isnumeric():
        abort(400)

    group = session.query(Group).filter(Group.id==group_id).first()
    if not group:
        return {
                'code': 'group',
                'message': 'Group not found',
            }, 404

    def get_groupmember_schema(member, user):
        member_schema = GroupMemberInfoSchema().dump(member)
        member_schema["name"] = user.name
        member_schema["surname"] = user.surname
        member_schema["email"] = user.email
        return member_schema

    if request.method == 'GET':
        if get_current_user().id != group.owner_id:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        members = session.query(GroupMember).filter(
            GroupMember.group_id==group_id).all()
        res = []
        for member in members:
            user = session.query(User).filter(User.id==member.user_id).first()
            res.append(get_groupmember_schema(member, user))
        return jsonify(res)
    
    elif request.method == 'POST':
        if get_current_user().id != group.owner_id:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        email = request.args.get("email")
        user = session.query(User).filter(User.email==email).first()
        if not user:
            abort(404)
        new_member = GroupMember(user_id=user.id, group_id=group_id)
        session.add(new_member)
        session.flush()
        session.refresh(new_member)
        session.commit()
        return jsonify(get_groupmember_schema(new_member, user))
    elif request.method == 'DELETE':
        if get_current_user().id != group.owner_id:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        member_id = request.args.get("member_id")
        session.query(GroupMember).filter(GroupMember.id==member_id).delete()
        session.commit()
        return jsonify({'Message': 'There is no such group member now!'})

@group.route('/<group_id>/tasks', methods=['GET', 'POST'])
@auth.login_required
def group_tasks(group_id):
    session = get_session()
    if not group_id.isnumeric():
        abort(400)
        
    group = session.query(Group).filter(Group.id==group_id).first()
    if not group:
        return {
                'code': 'group',
                'message': 'Group not found',
            }, 404

    if request.method == 'GET':
        membership = session.query(GroupMember).filter(GroupMember.user_id==get_current_user().id, GroupMember.group_id==group_id).first()
        if membership is None:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        group_tasks = session.query(GroupTask).filter(GroupTask.group_id==group_id).all()
        tasks = []
        for task in group_tasks:
            tasks.append(GroupTaskInfoSchema().dump(task))
        return jsonify(tasks)
    elif request.method == 'POST':
        if get_current_user().id != group.owner_id:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        try:
            new_task = CreateTaskSchema().load(request.json)
            new_task.group_id = group_id
        except ValidationError:
            abort(400)
        session.add(new_task)
        session.flush()
        session.refresh(new_task)

        group_members = session.query(GroupMember).filter(
            GroupMember.group_id==group_id).all()

        user_tasks = []
        for member in group_members:
            user_tasks.append(UserTask(
                groupTask_id = new_task.id,
                user_id = member.user_id,
                status = "undone"))
        session.add_all(user_tasks)
        session.commit()
        return jsonify(GroupTaskInfoSchema().dump(new_task))

@group.route('/<group_id>/tasks/<task_id>', methods=['GET', 'DELETE'])
@auth.login_required
def delete_group_task(group_id, task_id):
    session = get_session()
    group = session.query(Group).filter(Group.id==group_id).first()
    task = session.query(GroupTask).filter(GroupTask.id==task_id).first()
    if not task or not group:
        abort(404)

    if request.method == 'GET':
        membership = session.query(GroupMember).filter(GroupMember.user_id==get_current_user().id, GroupMember.group_id==group_id).first()
        if membership is None:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        return jsonify(GroupTaskInfoSchema().dump(task))
    elif request.method == 'DELETE':
        if get_current_user().id != group.owner_id:
            return {
                'code': 'user',
                'message': 'Unauthorized user access/No rights',
            }, 401
        session.query(GroupTask).filter(GroupTask.id==task_id).delete()
        session.commit()
        return jsonify({'Message': 'Deleted successfully'})














# @group.route('/all', methods=['GET'])
# def get_all_groups():
#     session = get_session()

#     groups = []
#     for group in session.query(Group).all():
#         groups.append(GroupInfoSchema().dump(group))
#     return jsonify(groups)
