import os, sqlite3

from flask import Flask, g, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from pathlib import Path

basedir = Path(__file__).resolve().parent

DATABASE = "analytics.db"
EMAIL = 'admin@test.com'
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
        users = db.session.query(models.User).filter_by(email=request.form['email']).all()

        if users:
            error = 'A user with that email already exists.'
        else:
            new_user = models.User(request.form['email'], request.form['password'])
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
        if app.config['EMAIL'] != request.form['email']:
            error = 'Invalid email.'
        elif app.config['PASSWORD'] != request.form['password']:
            error = 'Invalid password.'
        else:
            message = 'Login successful.'

            return jsonify({
                'message': message
            }), 200

        return jsonify({
            'message': error
        }), 400

@app.route('/logout')
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
