import sqlite3

from flask import Flask, g, jsonify, request

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
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connectDb()

    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """
    Close database connection.
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return 'There is no ignorance, there is knowledge.'

@app.route('/login', methods=['POST'])
def login():
    """
    Manage user login authentication via
    POST only, through offsite React
    input fields.
    """
    error = None

    if 'POST' == request.method:
        if app.config['EMAIL'] != request.form['email']:
            error = 'Invalid email.'
        elif app.config['PASSWORD'] != request.form['password']:
            error = 'Invalid password.'
        else:
            message = 'Login successful.'

            return jsonify({
                'message': message
            }), 200

        return jsonify({
            'message': error
        }), 400

if '__main__' == __name__:
    app.run(port=5000)
