from app.database import db

db.create_all()
"""Create the database and requisite tables."""

db.session.commit()
"""Make said changes."""
