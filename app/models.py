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
    password = db.Column(db.String, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'
        