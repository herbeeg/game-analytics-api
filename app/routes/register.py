from flask import Blueprint, jsonify, request

registration = Blueprint('registration', __name__)

@registration.route('/register', methods=['POST'])
def register():
    """
    Allow users to register themselves for
    the service using a unique email
    address and password.
    """
    error = None

    if 'POST' == request.method:
        emails = db.session.query(User).filter_by(email=request.json['email']).all()
        usernames = db.session.query(User).filter_by(username=request.json['username']).all()
        activation_keys = db.session.query(Activation).filter_by(key=request.json['activation_key']).first()

        if emails:
            error = 'A user with that email already exists.'
        elif usernames:
            error = 'A user with that name already exists.'
        elif not activation_keys:
            error = 'An activation key with that value does not exist.'
        elif 1 == activation_keys.claimed:
            error = 'That activation key has already been used.'
        else:
            new_user = User(
                request.json['email'], 
                request.json['username'], 
                generate_password_hash(request.json['password']), 
                datetime.datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()

            activation_keys.claimed = 1
            activation_keys.user_id = db.session.query(User).filter_by(username=request.json['username']).first().id
            db.session.commit()

            message = 'Registration successful.'

            return jsonify({
                'message': message
            }), 200
        return jsonify({
            'message': error
        }), 400
