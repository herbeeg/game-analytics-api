import os, sqlite3

from flask import Flask, g, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from pathlib import Path

basedir = Path(__file__).resolve().parent

DATABASE = "analytics.db"
EMAIL = 'admin@test.com'
USERNAME = 'admin'
PASSWORD = 'password'
SECRET_KEY = b'*\x15ulC6\xd0n\x0b]\xb3\xac\xf0+\x97\x8c'
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)

from app import models

@app.route('/')
def index():
    return 'There is no ignorance, there is knowledge.'

@app.route('/register', methods=['POST'])
def register():
    """
    Allow users to register themselves for
    the service using a unique email
    address and password.
    """
    error = None

    if 'POST' == request.method:
        emails = db.session.query(models.User).filter_by(email=request.json['email']).all()
        usernames = db.session.query(models.User).filter_by(username=request.json['username']).all()

        if emails:
            error = 'A user with that email already exists.'
        elif usernames:
            error = 'A user with that name already exists.'
        else:
            new_user = models.User(request.json['email'], request.json['username'], request.json['password'])
            db.session.add(new_user)
            db.session.commit()

            message = 'Registration successful.'

            return jsonify({
                'message': message
            }), 200
        return jsonify({
            'message': error
        }), 400

@app.route('/login', methods=['POST'])
def login():
    """
    Manage user login authentication via
    POST only, through offsite React
    input fields.
    """
    error = None

    if 'POST' == request.method:
        users = db.session.query(models.User).filter_by(email=request.json['email']).all()

        if not users:
            error = 'Invalid email.'
        elif users[0].password != request.json['password']:
            error = 'Invalid password.'
        else:
            message = 'Login successful.'

            return jsonify({
                'message': message
            }), 200

        return jsonify({
            'message': error
        }), 400

@app.route('/logout', methods=['GET'])
def logout():
    """
    Invalidate current user session via
    a GET request.
    """
    message = 'Logout successful.'

    return jsonify({
        'message': message
    }), 200

if '__main__' == __name__:
    app.run(port=5000)
