import pytest

from pathlib import Path

from app.main import app, initDb

TEST_DB = 'test.db'

class TestMainCase:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        app.config['TESTING'] = True
        app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)
        app.config['EMAIL'] = 'admin@test.com'
        app.config['PASSWORD'] = 'password'

        initDb()

        with app.test_client(self) as client:
            yield client

        initDb()

    def register(self, client, email, password):
        return client.post(
            '/register',
            data={'email': email, 'password': password},
            follow_redirects=False
        )

    def login(self, client, email, password):
        return client.post(
            '/login',
            data={'email': email, 'password': password},
            follow_redirects=False
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
        rv = self.register(client, 'newuser@test.com', app.config['PASSWORD'])
        assert b'Registration successful.'

        rv = self.login(client, 'newuser@test.com', app.config['PASSWORD'])
        assert 200 == rv.status_code
        assert b'Login successful.' in rv.data

        rv = self.logout(client)
        assert 200 == rv.status_code
        assert b'Logout successful.' in rv.data

        rv = self.register(client, app.config['EMAIL'], app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert b'A user with that email already exists.'

    def testLoginLogout(self, client):
        rv = self.login(client, app.config['EMAIL'], app.config['PASSWORD'])
        assert 200 == rv.status_code
        assert b'Login successful.' in rv.data

        rv = self.logout(client)
        assert 200 == rv.status_code
        assert b'Logout successful.' in rv.data

        rv = self.login(client, app.config['EMAIL'] + 'j', app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert b'Invalid email.' in rv.data

        rv = self.login(client, app.config['EMAIL'], app.config['PASSWORD'] + 'j')
        assert 400 == rv.status_code
        assert b'Invalid password.' in rv.data
