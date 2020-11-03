import datetime, json, pytest

from pathlib import Path

from app.main import app, db
from tests.utils import login, logout, register

TEST_DB = 'test.db'

class TestProtectedProfile:
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

    def testProfile(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        response = client.get(
            '/profile/1',
            headers={
                'Authorization': 'Bearer ' + json.loads(rv.data)['access_token']
            },
            follow_redirects=False
        )

        assert 200 == response.status_code
        assert app.config['EMAIL'] in response.json['email']
        assert app.config['USERNAME'] in response.json['username']

        date_obj = datetime.datetime.strptime(response.json['created_at'], '%a, %d %b %Y %H:%M:%S %Z')
        assert datetime.datetime.now().strftime('%Y-%m-%d') in date_obj.strftime('%Y-%m-%d')

        response = client.get(
            '/profile/1',
            follow_redirects=False
        )

        assert 401 == response.status_code

        response = client.get(
            '/profile/117',
            headers={
                'Authorization': 'Bearer ' + json.loads(rv.data)['access_token']
            },
            follow_redirects=False
        )

        assert 400 == response.status_code
        assert 'User does not exist.' in response.json['message']

        new_rv = register(client, '1' + app.config['EMAIL'], '1' + app.config['USERNAME'], app.config['PASSWORD'])
        new_rv = login(client, '1' + app.config['EMAIL'], app.config['PASSWORD'])

        response = client.get(
            '/profile/2',
            headers={
                'Authorization': 'Bearer ' + json.loads(new_rv.data)['access_token']
            },
            follow_redirects=False
        )

        assert 200 == response.status_code

        response = client.get(
            '/profile/2',
            headers={
                'Authorization': 'Bearer ' + json.loads(rv.data)['access_token']
            },
            follow_redirects=False
        )

        assert 400 == response.status_code
        assert 'Cannot retrieve data from another user.' in response.json['message']
