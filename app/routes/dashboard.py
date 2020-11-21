from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt_claims, jwt_required

home = Blueprint('home', __name__)

@home.route('/dashboard', methods=['GET'])
@jwt_required
def dashboard():
    claims = get_jwt_claims()
    username = get_jwt_identity()

    if not username:
        error = 'Invalid username identity.'
    else:
        return jsonify({
            'live_view': ['1'],
            'stats': ['2'],
            'last_match': ['3'],
            'previous_matches': ['4']
        }), 200

    return jsonify({
        'message': error
    }), 400
