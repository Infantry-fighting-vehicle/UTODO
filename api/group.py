from flask import Blueprint, request, jsonify, abort
from db import get_session
from models import *
from schemas import *
group = Blueprint('group', __name__, url_prefix='/groups')

# temporary using query parameters for user id
@group.route('/', methods=['POST', 'GET'])
def groups():
    session = get_session()
    user_id = request.args.get("user_id") #temporary

    if request.method == 'POST':
        try:
            new_group = CreateGroupSchema().load(request.json)
            assert(user_id)
            new_group.owner_id = user_id
        except (ValidationError, AssertionError):
            abort(400)

        session.add(new_group)
        session.flush()
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
def group_by_id(group_id):
    session = get_session()
    if not group_id.isnumeric():
        abort(400)

    group = session.query(Group).filter(Group.id==group_id).first()
    if not group:
        abort(404)

    if request.method == 'GET':
        return jsonify(GroupInfoSchema().dump(group))
    elif request.method == 'PUT':
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
        session.query(Group).filter(Group.id==group.id).delete()
        session.commit()
        return jsonify({'Message': 'There is no such group now!'})

@group.route('/<group_id>/members', methods=['GET', 'POST', 'DELETE'])
def group_members(group_id):
    session = get_session()
    if not group_id.isnumeric():
        abort(400)

    group = session.query(Group).filter(Group.id==group_id).first()
    if not group:
        abort(404)

    def get_groupmember_schema(member, user):
        member_schema = GroupMemberInfoSchema().dump(member)
        member_schema["name"] = user.name
        member_schema["surname"] = user.surname
        member_schema["email"] = user.email
        return member_schema

    if request.method == 'GET':
        members = session.query(GroupMember).filter(
            GroupMember.group_id==group_id).all()
        res = []
        for member in members:
            user = session.query(User).filter(User.id==member.user_id).first()
            res.append(get_groupmember_schema(member, user))
        return jsonify(res)
    
    elif request.method == 'POST':
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
        member_id = request.args.get("member_id")
        session.query(GroupMember).filter(GroupMember.id==member_id).delete()
        session.commit()
        return jsonify({'Message': 'There is no such group member now!'})

@group.route('/<group_id>/tasks', methods=['GET', 'POST'])
def group_tasks(group_id):
    session = get_session()
    if not group_id.isnumeric():
        abort(400)
        
    group = session.query(Group).filter(Group.id==group_id).first()
    if not group:
        abort(404)

    if request.method == 'GET':
        group_tasks = session.query(GroupTask).filter(GroupTask.group_id==group_id).all()
        tasks = []
        for task in group_tasks:
            tasks.append(GroupTaskInfoSchema().dump(task))
        return jsonify(tasks)
    elif request.method == 'POST':
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
def delete_group_task(group_id, task_id):
    session = get_session()
    group = session.query(Group).filter(Group.id==group_id).first()
    task = session.query(GroupTask).filter(GroupTask.id==task_id).first()
    if not task or not group:
        abort(404)

    if request.method == 'GET':
        return jsonify(GroupTaskInfoSchema().dump(task))
    elif request.method == 'DELETE':
        session.query(GroupTask).filter(GroupTask.id==task_id).delete()
        session.commit()
        return jsonify({'Message': 'There is no such group task now!'})














@group.route('/all', methods=['GET'])
def get_all_groups():
    session = get_session()

    groups = []
    for group in session.query(Group).all():
        groups.append(GroupInfoSchema().dump(group))
    return jsonify(groups)
