import os
import uuid

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from pathlib import Path

from app.database import db
from app.jwt import jwt
from app.routes.cli import task
from app.routes.dashboard import home
from app.routes.index import overview
from app.routes.jwt import claims
from app.routes.login import user_login
from app.routes.logout import user_logout
from app.routes.match import match
from app.routes.profile import user_profile
from app.routes.register import registration
from app.routes.turn import turn

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

def create_app():
    """
    Register all of our separated route files as Flask 
    Blueprints with their own group names to
    maintain a readable and coherent
    structure.

    Returns:
        Flask: Main app Flask object
    """
    app = Flask(__name__)
    app.config.from_object(__name__)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(claims)
    app.register_blueprint(overview)
    app.register_blueprint(registration)
    app.register_blueprint(user_login)
    app.register_blueprint(user_logout)
    app.register_blueprint(user_profile)
    app.register_blueprint(home)
    app.register_blueprint(match)
    app.register_blueprint(turn)
    app.register_blueprint(task)

    return app

if '__main__' == __name__:
    app = create_app()

    app.run(port=5000)
