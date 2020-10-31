import datetime, os, sqlite3

from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash

basedir = Path(__file__).resolve().parent
load_dotenv(find_dotenv())

DATABASE = os.getenv('DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

app = Flask(__name__)
app.config.from_object(__name__)

jwt = JWTManager(app)
"""Setup the Flask-JWT-Extended extension."""

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
            new_user = models.User(
                request.json['email'], 
                request.json['username'], 
                generate_password_hash(request.json['password']), 
                datetime.datetime.utcnow()
            )
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
        elif not check_password_hash(users[0].password, request.json['password']):
            error = 'Invalid password.'
        else:
            message = 'Login successful.'
            access_token = create_access_token(identity=users[0].username)

            return jsonify({
                'access_token': access_token,
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

@app.route('/profile/<user_id>', methods=['GET'])
@jwt_required
def profile(user_id):
    current_user = get_jwt_identity()

    return jsonify({
        'logged_in_as': current_user
    }), 200

if '__main__' == __name__:
    app.run(port=5000)
