import sqlite3

from flask import Flask, g

DATABASE = "analytics.db"

app = Flask(__name__)

app.config.from_object(__name__)

def connectDb():
    """
    Connect to the database.
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row

    return rv

def initDb():
    """
    Create the database.
    """
    with app.app_context():
        db = getDb()

        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())

        db.commit()

        db.execute('INSERT INTO users (email, password) values ("admin", "password")')
        db.commit()

def getDb():
    """
    Open database connection.
    """
    if not hasattr(g, 'analytics.db'):
        g.sqlite_db = connectDb()

    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """
    Close database connection.
    """
    if hasattr(g, 'analytics.db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return 'There is no ignorance, there is knowledge.'

if '__main__' == __name__:
    app.run(port=5000)