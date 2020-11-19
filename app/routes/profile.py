from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required

from app.database import db
from app.models.match import Match
from app.models.match_meta import MatchMeta
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
        matches = db.session.query(
            Match
        ).join(
            MatchMeta, Match.uuid == MatchMeta.match_id
        ).filter(
            Match.user_id == user_id,
            MatchMeta.key == 'timing'
        ).all()

        history = []

        if not matches:
            message = 'No previous matches found.'
        else:
            for match in matches:
                ended = db.session.query(
                    MatchMeta
                ).filter_by(
                    match_id=match.uuid, key='timing'
                ).first().value['elapsed_time'] + match.created_at

                history.append({
                    'id': match.uuid,
                    'name': match.title + ' - ' + match.uuid,
                    'ended_at': ended
                })

            message = 'Match data returned successfully.'

        return jsonify({
            'message': message,
            'match_history': history
        }), 200
    
    return jsonify({
        'message': error
    }), 400

@user_profile.route('/profile/<user_id>/stats', methods=['GET'])
@jwt_required
def stats(user_id):
    claims = get_jwt_claims()
    username = get_jwt_identity()
    users = db.session.query(User).filter_by(id=user_id).all()

    error = None

    if not users:
        error = 'User does not exist.'
    elif int(user_id) != claims['id']:
        error = 'Cannot retrieve statistics from another user.'
    else:
        matches = db.session.query(
            Match
        ).join(
            MatchMeta, Match.uuid == MatchMeta.match_id
        ).filter(
            Match.user_id == user_id,
            MatchMeta.key == 'timing'
        ).all()

        total = 0

        for match in matches:
            total += db.session.query(
                MatchMeta
            ).filter_by(
                match_id=match.uuid, key='timing'
            ).first().value['elapsed_time']

        return jsonify({
            'stats': {
                'match_time': total,
                'completed': len(matches)
            }
        })
    
    return jsonify({
        'message': error
    }), 400
