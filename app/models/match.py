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

    def __init__(self):
        return

    def __repr__(self):
        return f'<Match {self}>'
        