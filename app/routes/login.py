from flask import Blueprint

login = Blueprint('login', __name__)

@login.route('/login', methods=['POST'])
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