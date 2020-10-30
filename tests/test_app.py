import json
import pytest
import datetime

from pathlib import Path

from api.main import app, db
from api.models import User

TEST_DB = 'test.db'

class TestMainCase:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        app.config['TESTING'] = True
        app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR.joinpath(TEST_DB)}'

        app.config['EMAIL'] = 'admin@test.com'
        app.config['USERNAME'] = 'admin'
        app.config['PASSWORD'] = 'password'

        db.create_all()

        with app.test_client(self) as client:
            yield client

        db.drop_all()

    def register(self, client, email, username, password):
        return client.post(
            '/register',
            data=json.dumps({'email': email, 'username': username, 'password': password}),
            content_type='application/json'
        )

    def login(self, client, email, password):
        return client.post(
            '/login',
            data=json.dumps({'email': email, 'password': password}),
            content_type='application/json'
        )

    def logout(self, client):
        return client.get(
            '/logout',
            follow_redirects=False
        )

    def testIndex(self, client):
        response = client.get('/', content_type='html/text')
        
        assert 200 == response.status_code
        assert b'There is no ignorance, there is knowledge.' == response.data

    def testDatabase(self):
        assert Path('test.db').is_file()

    def testRegister(self, client):
        app.config['EMAIL'] = 'newuser@test.com'
        """Update app config email to allow checks against existing database rows."""
        app.config['USERNAME'] = 'newuser'

        rv = self.register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
        assert 'Registration successful.' in json.loads(rv.data)['message']
        
        users = db.session.query(User).filter_by(email=app.config['EMAIL']).all()
        assert datetime.datetime.now().strftime('%Y-%m-%d') == users[0].created_at.strftime('%Y-%m-%d')
        """Fairly vague check to ensure that the created_at timestamp is on the same day."""

        rv = self.login(client, app.config['EMAIL'], app.config['PASSWORD'])
        assert 200 == rv.status_code
        assert 'Login successful.' in json.loads(rv.data)['message']

        rv = self.logout(client)
        assert 200 == rv.status_code
        assert 'Logout successful.' in json.loads(rv.data)['message']

        rv = self.register(client, 'j' + app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert 'A user with that name already exists.' in json.loads(rv.data)['message']

        rv = self.register(client, app.config['EMAIL'], app.config['USERNAME'] + '1', app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert 'A user with that email already exists.' in json.loads(rv.data)['message']

    def testLoginLogout(self, client):
        rv = self.register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
        assert 200 == rv.status_code

        rv = self.login(client, app.config['EMAIL'], app.config['PASSWORD'])
        assert 200 == rv.status_code
        assert 'Login successful.' in json.loads(rv.data)['message']

        rv = self.logout(client)
        assert 200 == rv.status_code
        assert 'Logout successful.' in json.loads(rv.data)['message']

        rv = self.login(client, app.config['EMAIL'] + 'j', app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert 'Invalid email.' in json.loads(rv.data)['message']

        rv = self.login(client, app.config['EMAIL'], app.config['PASSWORD'] + 'j')
        assert 400 == rv.status_code
        assert 'Invalid password.' in json.loads(rv.data)['message']
