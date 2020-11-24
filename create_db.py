from app.database import db
from app.main import create_app

with create_app().app_context():
    db.create_all()
    """Create the database and requisite tables."""

    db.session.commit()
    """Make said changes."""
