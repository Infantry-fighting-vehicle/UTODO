# https://flask.palletsprojects.com/en/2.2.x/tutorial/views/

import functools

from flask import Blueprint, request

from werkzeug.security import check_password_hash, generate_password_hash
from db import get_session
from models import *
from schemas import *

from flask import jsonify, request, abort
from marshmallow import ValidationError
from models import *
from schemas import *
from schemas.Role import RoleSchema

from flask_httpauth import HTTPBasicAuth

authMaksym = Blueprint("auth", __name__, url_prefix="/")
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
    Session = get_session()()
    username = auth.current_user()
    return Session.query(User).filter(User.email == username).first()


@authMaksym.route("/user", methods=["POST"])
def user():
    session = get_session()
    try:
        new_user = CreateUserSchema().load(request.json)
        is_unique_email = (
            not session.query(User).filter(User.email == new_user.email).first()
        )
        assert is_unique_email
    except (ValidationError, AssertionError):
        abort(400)

    new_user.password = generate_password_hash(new_user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    userObj = session.query(User).filter(User.email == new_user.email).first()
    new_role = Role(id=userObj.id, value="User")
    session.add(new_role)
    session.commit()
    return jsonify(UserFullInfoSchema().dump(new_user))


@authMaksym.route("/user/me", methods=["GET"])
def login():
    session = get_session()
    email = request.args.get("email")
    password = request.args.get("password")
    if not password:
        password = ""

    user = session.query(User).filter(User.email == email).first()
    if user and check_password_hash(user.password, password):
        return UserFullInfoSchema().dump(user)
    elif user:
        abort(403)
    else:
        abort(404)
