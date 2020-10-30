import json
import pytest

from pathlib import Path

from app.main import app, db

TEST_DB = 'test.db'

class TestMainCase:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        app.config['TESTING'] = True
        app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR.joinpath(TEST_DB)}'

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
    
    def resetAppConfig(self):
        """
        Allowing on the fly changes to the
        app config where the fields can
        be reset back to the defaults
        at any time.
        """
        app.config['EMAIL'] = 'admin@test.com'
        app.config['USERNAME'] = 'admin'
        app.config['PASSWORD'] = 'password'

    def testIndex(self, client):
        response = client.get('/', content_type='html/text')
        
        assert 200 == response.status_code
        assert b'There is no ignorance, there is knowledge.' == response.data

    def testDatabase(self):
        assert Path('test.db').is_file()

    def testRegister(self, client):
        rv = self.register(client, 'newuser@test.com', 'newuser', app.config['PASSWORD'])
        assert 'Registration successful.' in json.loads(rv.data)['message']

        app.config['EMAIL'] = 'newuser@test.com'
        """Update app config email to allow checks against existing database rows."""

        rv = self.login(client, 'newuser@test.com', app.config['PASSWORD'])
        assert 200 == rv.status_code
        assert 'Login successful.' in json.loads(rv.data)['message']

        rv = self.logout(client)
        assert 200 == rv.status_code
        assert 'Logout successful.' in json.loads(rv.data)['message']

        rv = self.register(client, 'j' + app.config['EMAIL'], 'newuser', app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert 'A user with that name already exists.' in json.loads(rv.data)['message']

        rv = self.register(client, app.config['EMAIL'], 'newuser1', app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert 'A user with that email already exists.' in json.loads(rv.data)['message']

        self.resetAppConfig()
        """Set app config back to defaults for the remainder of the test suite."""

    def testLoginLogout(self, client):
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
