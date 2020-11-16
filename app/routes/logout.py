from flask import Blueprint

user_logout = Blueprint('user_logout', __name__)

@user_logout.route('/logout', methods=['GET'])
def logout():
    """
    Invalidate current user session via
    a GET request.
    """
    message = 'Logout successful.'

    return jsonify({
        'message': message
    }), 200
