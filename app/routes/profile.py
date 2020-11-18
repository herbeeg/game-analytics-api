from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required

from app.database import db
from app.models.user import User

user_profile = Blueprint('user_profile', __name__)

@user_profile.route('/profile/<user_id>', methods=['GET'])
@jwt_required
def profile(user_id):
    claims = get_jwt_claims()
    username = get_jwt_identity()
    users = db.session.query(User).filter_by(id=user_id).all()

    error = None

    if not users:
        error = 'User does not exist.'
    elif int(user_id) != claims['id']:
        error = 'Cannot retrieve data from another user.'
    else:
        return jsonify({
            'email': users[0].email,
            'username': username,
            'created_at': users[0].created_at
        }), 200
    
    return jsonify({
        'message': error
    }), 400

@user_profile.route('/profile/<user_id>/history', methods=['GET'])
@jwt_required
def history(user_id):
    claims = get_jwt_claims()
    username = get_jwt_identity()
    users = db.session.query(User).filter_by(id=user_id).all()

    error = None

    if not users:
        error = 'User does not exist.'
    elif int(user_id) != claims['id']:
        error = 'Cannot retrieve match history from another user.'
    else:
        # Do something.
        print('do')
    
    return jsonify({
        'message': error
    }), 400
