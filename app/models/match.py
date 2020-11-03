import datetime

from app.main import db

class Match(db.Model):
    """
    Scaffold a datastore to hold information
    about currently running matches and
    previous match history.

    Extends the SQLAlchemy.Model class.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    live = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, live, title):
        self.user_id = user_id
        self.live = live
        self.title = title
        self.created_at = int(datetime.datetime.utcnow().timestamp())

    def __repr__(self):
        return f'<Match {self.title}>'
        