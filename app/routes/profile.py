from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required

from app.database import db
from app.models.match import Match
from app.models.match_meta import MatchMeta
from app.models.user import User

user_profile = Blueprint('user_profile', __name__)

@user_profile.route('/profile', methods=['GET'])
@jwt_required
def profile():
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    if not claims['id']:
        error = 'Invalid JWT claims provided.'
    else:
        user = db.session.query(User).filter_by(id=claims['id']).first()

        if not user:
            error = 'User does not exist.'
        else:
            return jsonify({
                'email': user.email,
                'username': username,
                'created_at': user.created_at
            }), 200
    
    return jsonify({
        'message': error
    }), 400

@user_profile.route('/profile/history', methods=['GET'])
@jwt_required
def history():
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    if not claims['id']:
        error = 'Invalid JWT claims provided.'
    else:
        user = db.session.query(User).filter_by(id=claims['id']).first()

        if not user:
            error = 'User does not exist.'
        else:
            matches = db.session.query(
                Match
            ).join(
                MatchMeta, Match.uuid == MatchMeta.match_id
            ).filter(
                Match.user_id == claims['id'],
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

@user_profile.route('/profile/stats', methods=['GET'])
@jwt_required
def stats():
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    if not claims['id']:
        error = 'Invalid JWT claims provided.'
    else:
        user = db.session.query(User).filter_by(id=claims['id']).first()

        if not user:
            error = 'User does not exist.'
        else:
            matches = db.session.query(
                Match
            ).join(
                MatchMeta, Match.uuid == MatchMeta.match_id
            ).filter(
                Match.user_id == claims['id'],
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
                'match_time': total,
                'completed': len(matches)
            }), 200
    
    return jsonify({
        'message': error
    }), 400
