from app.main import db
from app.models import User

db.create_all()
"""Create the database and requisite tables."""

db.session.commit()
"""Make said changes."""