from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.database import db
from app.models.user import User

user_login = Blueprint('user_login', __name__)

@user_login.route('/login', methods=['POST'])
def login():
    """
    Manage user login authentication via
    POST only, through offsite React
    input fields.
    """
    error = None

    if 'POST' == request.method:
        users = db.session.query(User).filter_by(email=request.json['email']).all()

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
