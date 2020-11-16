from flask import Blueprint

logout = Blueprint('logout', __name__)

@logout.route('/logout', methods=['GET'])
def logout():
    """
    Invalidate current user session via
    a GET request.
    """
    message = 'Logout successful.'

    return jsonify({
        'message': message
    }), 200
