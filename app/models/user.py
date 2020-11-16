from app.database import db

class User(db.Model):
    """
    Scaffold a datastore to verify and authenticate 
    users upon interacting with the API
    through the provided React app.

    Extends the SQLAlchemy.Model class.
    """
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    created_at = db.Column(db.DateTime(), unique=False, nullable=False)

    def __init__(self, email, username, password, created_at):
        self.email = email
        self.username = username
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        return f'<User {self.email}>'
        