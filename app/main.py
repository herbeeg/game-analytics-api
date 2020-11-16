import datetime, json, os, sqlite3, uuid

from app.routes.index import overview
from app.routes.register import registration
from app.routes.login import login
from app.routes.logout import logout
from app.routes.dashboard import dashboard
from app.routes.match import match
from app.database import db

from dotenv import find_dotenv, load_dotenv
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_jwt_claims
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

from app.matrix.generator import MatrixGenerator
from app.matrix.position import TurnPositions

from app.models.activation import Activation
from app.models.match import Match
from app.models.match_meta import MatchMeta
from app.models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    db.init_app(app)

    jwt = JWTManager(app)
    """Setup the Flask-JWT-Extended extension."""

    from app.routes.jwt import claims
    app.register_blueprint(claims)

    app.register_blueprint(overview)
    app.register_blueprint(registration)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(dashboard)
    app.register_blueprint(match)

    return app

if '__main__' == __name__:
    app = create_app()

    app.run(port=5000)
