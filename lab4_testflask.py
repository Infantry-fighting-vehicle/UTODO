from venv import create
from click import echo
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route(f'/api/v1/hello-world-<student_id>')
def func(student_id):
    return jsonify({'job': 'student', 
                        'id': student_id,
                        'moro lox': True})