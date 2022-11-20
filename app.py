import os

from flask import Flask, jsonify

def create_app(test_config=None):
    global app
    app = Flask(__name__)

    from db import session_init
    session_init()

    from api import auth, user, group
    app.register_blueprint(auth.authMaksym)
    app.register_blueprint(user.user)
    app.register_blueprint(group.group)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


app = create_app()

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response

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