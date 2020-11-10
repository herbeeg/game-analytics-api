import datetime, os, sqlite3

from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_claims
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash

basedir = Path(__file__).resolve().parent
load_dotenv(find_dotenv())

DATABASE = os.getenv('DATABASE')
SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{Path(basedir).joinpath(DATABASE)}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

app = Flask(__name__)
app.config.from_object(__name__)

jwt = JWTManager(app)
"""Setup the Flask-JWT-Extended extension."""

db = SQLAlchemy(app)

from app.models.user import User
from app.models.match import Match
from app.models.match_meta import MatchMeta

@jwt.user_claims_loader
def addClaimsToAccessToken(identity):
    users = db.session.query(User).filter_by(username=identity).all()

    return {
        'username': identity,
        'id': users[0].id
    }

@app.route('/')
def index():
    return 'There is no ignorance, there is knowledge.'

@app.route('/register', methods=['POST'])
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

        if emails:
            error = 'A user with that email already exists.'
        elif usernames:
            error = 'A user with that name already exists.'
        else:
            new_user = User(
                request.json['email'], 
                request.json['username'], 
                generate_password_hash(request.json['password']), 
                datetime.datetime.utcnow()
            )
            db.session.add(new_user)
            db.session.commit()

            message = 'Registration successful.'

            return jsonify({
                'message': message
            }), 200
        return jsonify({
            'message': error
        }), 400

@app.route('/login', methods=['POST'])
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

@app.route('/logout', methods=['GET'])
def logout():
    """
    Invalidate current user session via
    a GET request.
    """
    message = 'Logout successful.'

    return jsonify({
        'message': message
    }), 200

@app.route('/dashboard', methods=['GET'])
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

@app.route('/profile/<user_id>', methods=['GET'])
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

@app.route('/match/new', methods=['POST'])
@jwt_required
def newMatch():
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    if 'POST' == request.method:
        if not username:
            error = 'Invalid username identity.'
        else:
            try:
                new_match = Match(
                    claims['id'],
                    0,
                    request.json['title']
                )
                db.session.add(new_match)
                db.session.commit()

                match_data = db.session.query(Match).filter_by(user_id=claims['id']).order_by(Match.created_at.desc()).one()

                try:
                    uuid = match_data.uuid

                    match_meta = MatchMeta(
                        uuid,
                        'player_1',
                        request.json['player_1']
                    )
                    db.session.add(match_meta)
                    db.session.commit()

                    match_meta = MatchMeta(
                        uuid,
                        'player_2',
                        request.json['player_2']
                    )
                    db.session.add(match_meta)
                    db.session.commit()

                    message = 'New match setup successfully.'
   
                    return jsonify({
                        'uuid': match_data.uuid,
                        'message': message
                    }), 200
                except AttributeError:
                    error = 'Malformed uuid column data.'

                    return jsonify({
                        'message': error
                    }), 400
                except KeyError:
                    error = 'Malformed match metadata provided.'

                    return jsonify({
                        'message': error
                    }), 400
            except KeyError:
                error = 'Malformed match data provided.'

                return jsonify({
                    'message': error
                }), 400

        return jsonify({
            'message': error
        }), 400

@app.route('/match/start/<uuid>', methods=['GET'])
@jwt_required
def startMatch(uuid):
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    match = db.session.query(Match).filter_by(uuid=uuid).first()

    if not match:
        return 404
    elif match.user_id != claims['id']:
        error = 'Cannot start matches owned by other users.'

        return jsonify({
            'message': error
        }), 401
    else:
        try:
            match.live = 1
            db.session.commit()

            uri = f'/match/view/{match.uuid}'
            message = 'Match started successfully.'

            return jsonify({
                'match_uri': uri,
                'message': message
            }), 200
        except AttributeError:
            error = 'Match could not be started.'

            return jsonify({
                'message': error
            }), 400

    return jsonify({
        'message': error
    }), 400

@app.route('/match/end/<uuid>', methods=['GET'])
@jwt_required
def endMatch(uuid):
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    match = db.session.query(Match).filter_by(uuid=uuid).first()

    if not match:
        return 404
    elif 0 == match.live:
        error = 'Cannot end matches that are not in progress.'
    elif match.user_id != claims['id']:
        error = 'Cannot end matches owned by other users.'

        return jsonify({
            'message': error
        }), 401
    else:
        try:
            match.live = 0
            db.session.commit()

            timing_meta = {
                'elapsed_time': int(datetime.datetime.utcnow().timestamp()) - match.created_at
            }

            match_meta = MatchMeta(
                uuid,
                'timing',
                timing_meta
            )
            db.session.add(match_meta)
            db.session.commit()

            uri = f'/match/view/{match.uuid}'
            message = 'Match ended successfully.'

            return jsonify({
                'match_uri': uri,
                'message': message
            }), 200
        except AttributeError:
            error = 'Match could not be ended.'

            return jsonify({
                'message': error
            }), 400

    return jsonify({
        'message': error
    }), 400

@app.route('/turn/update/<uuid>', methods=['POST'])
@jwt_required
def nextTurn(uuid):
    claims = get_jwt_claims()
    username = get_jwt_identity()

    error = None

    if 'POST' == request.method:
        if not username:
            error = 'Invalid username identity.'
        else:
            match = db.session.query(Match).filter_by(uuid=uuid).first()

            if not match:
                return 404
            elif 0 == match.live:
                error = 'Cannot update matches that are not in progress.'
            elif match.user_id != claims['id']:
                error = 'Cannot update matches owned by other users.'

                return jsonify({
                    'message': error
                }), 401
            else:
                turn_meta = db.session.query(MatchMeta).filter_by(match_id=uuid, key='turns').first()

                if not turn_meta:
                    match_meta = MatchMeta(
                        uuid,
                        'turns',
                        request.json
                    )
                
                db.session.add(match_meta)
                db.session.commit()

                message = 'Turn completed.'

                return jsonify({
                    'message': message
                }), 200

    return jsonify({
        'message': error
    }), 400

if '__main__' == __name__:
    app.run(port=5000)
