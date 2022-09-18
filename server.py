from flask import Flask
app = Flask(__name__)

@app.route(f'/api/v1/hello-world-<student_id>')
def func(student_id):
    return f"<p>Hello World {student_id}</p>"