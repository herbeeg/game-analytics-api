import datetime
import uuid

from app.database import db

class Match(db.Model):
    """
    Scaffold a datastore to hold information
    about currently running matches and
    previous match history.

    Extends the SQLAlchemy.Model class.
    """
    __tablename__ = 'matches'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    live = db.Column(db.Integer, unique=False, nullable=True)
    title = db.Column(db.String, unique=False, nullable=False)
    created_at = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, user_id, live, title):
        self.user_id = user_id
        self.uuid = str(uuid.uuid4())
        self.live = live
        self.title = title
        self.created_at = int(datetime.datetime.utcnow().timestamp())

    def __repr__(self):
        return f'<Match {self.title}>'
        