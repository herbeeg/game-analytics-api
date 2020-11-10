import datetime, json, pytest

from pathlib import Path

from app.main import app, db, Activation
from tests.utils import login, logout, register

TEST_DB = 'test.db'

class TestDashboardHomeView:
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

        new_key = Activation(app.config['ACTIVATION_KEY'])
        """Use a fixed activation key string for testing purposes."""
        db.session.add(new_key)
        db.session.commit()

        with app.test_client(self) as client:
            yield client

        db.drop_all()

    def testHome(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        response = client.get(
            '/dashboard',
            headers={
                'Authorization': 'Bearer ' + json.loads(rv.data)['access_token']
            },
            follow_redirects=False
        )

        assert 200 == response.status_code

        assert response.json['live_view']
        assert response.json['stats']
        assert response.json['last_match']
        assert response.json['previous_matches']
