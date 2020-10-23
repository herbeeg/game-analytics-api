import pytest

from pathlib import Path

from app.main import app, initDb

TEST_DB = 'test.db'

class TestMainCase:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        app.config['TESTING'] = True
        app.config['DATABASE'] = BASE_DIR
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
        return

    def testLoginLogout(self, client):
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])
        assert b'You were logged in.' in rv.data

        rv = logout(client)
        assert b'You were logged out.' in rv.data

        rv = login(client, app.config['EMAIL'] + 'j', app.config['PASSWORD'])
        assert b'Invalid email.' in rv.data
        assert 400 == rv.status_code

        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'] + 'j')
        assert b'Invalid password' in rv.data
        assert 400 == rv.status_code
