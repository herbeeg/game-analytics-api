from flask import Blueprint

from app.database import db
from app.jwt import jwt
from app.models.user import User

claims = Blueprint('claims', __name__)

@jwt.user_claims_loader
def addClaimsToAccessToken(identity):
    users = db.session.query(User).filter_by(username=identity).all()

    return {
        'username': identity,
        'id': users[0].id
    }
