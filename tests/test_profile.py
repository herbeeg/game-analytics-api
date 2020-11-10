import datetime, json, pytest

from pathlib import Path

from app.main import app, db
from tests.utils import login, logout, profile, register

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
        app.config['ACTIVATION_KEY'] = '08fe47e8814b410cbaf742463e8c9252'

        db.create_all()

        with app.test_client(self) as client:
            yield client

        db.drop_all()

    def testProfile(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        response = profile(client, 1, json.loads(rv.data)['access_token'])

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

        response = profile(client, 117, json.loads(rv.data)['access_token'])

        assert 400 == response.status_code
        assert 'User does not exist.' in response.json['message']

        new_rv = register(client, '1' + app.config['EMAIL'], '1' + app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        new_rv = login(client, '1' + app.config['EMAIL'], app.config['PASSWORD'])

        response = profile(client, 2, json.loads(new_rv.data)['access_token'])

        assert 200 == response.status_code

        response = profile(client, 2, json.loads(rv.data)['access_token'])

        assert 400 == response.status_code
        assert 'Cannot retrieve data from another user.' in response.json['message']
