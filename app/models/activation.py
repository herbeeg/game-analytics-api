import uuid

from app.database import db

class Activation(db.Model):
    """
    Scaffold a datastore to verify and authenticate 
    users upon registering with the API by
    validating requests with existing
    valid activation keys.

    Extends the SQLAlchemy.Model class.
    """
    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=True)
    key = db.Column(db.String(32), unique=True, nullable=False)
    claimed = db.Column(db.Integer, default=0, unique=False, nullable=False)

    def __init__(self, key=''):
        if not key:
            self.key = ''.join(str(uuid.uuid4()).split('-'))
        else:
            self.key = key

    def __repr__(self):
        return f'<Activation {self.id}>'
        