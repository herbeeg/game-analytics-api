from flask import Blueprint
from flask_jwt_extended import jwt_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard', methods=['GET'])
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
