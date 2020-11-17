from app.database import db

class MatchMeta(db.Model):
    """
    Scaffold a datastore to hold additional
    match metadata linked to user created
    matches for detailed statistic
    monitoring via a dashboard.

    Extends the SQLAlchemy.Model class.
    """
    id = db.Column(db.Integer, unique=True, primary_key=True)
    match_id = db.Column(db.String(36), unique=False, nullable=False)
    key = db.Column(db.String(), unique=False, nullable=False)
    value = db.Column(db.JSON(), unique=False, nullable=True)

    def __init__(self, match_id, key, value):
        self.match_id = match_id
        self.key = key
        self.value = value

    def __repr__(self):
        return f'<MatchMeta {self.key}>'
        