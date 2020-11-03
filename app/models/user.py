from app.main import db

class User(db.Model):
    """
    Scaffold a datastore to verify and authenticate 
    users upon interacting with the API
    through the provided React app.

    Extends the SQLAlchemy.Model class.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __init__(self, email, username, password, created_at):
        self.email = email
        self.username = username
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        return f'<User {self.email}>'
        