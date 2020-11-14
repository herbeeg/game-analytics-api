import json, pytest

from pathlib import Path

from app.main import app, db, Activation, Match, MatchMeta
from tests.helpers import getMatchData, getProjectedMatrix, getSingleTurnData
from tests.utils import login, newMatch, nextTurn, register, startMatch, viewTurn

TEST_DB = 'test.db'

class TestLiveMatchViewing:
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
        app.config['ACTIVATION_KEY_2'] = '97a56754b27e4cbea94e6c7ca9884b2b'

        db.create_all()

        key_first = Activation(app.config['ACTIVATION_KEY'])
        key_second = Activation(app.config['ACTIVATION_KEY_2'])
        """Use fixed activation key strings for testing purposes."""
        db.session.add(key_first)
        db.session.add(key_second)
        db.session.commit()

        with app.test_client(self) as client:
            yield client

        db.drop_all()

    def testViewSingleTurn(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']
        rv = newMatch(
            client,
            getMatchData(),
            access_token
        )

        uuid = json.loads(rv.data)['uuid']
        response = startMatch(
            client,
            uuid,
            access_token
        )

        rv = nextTurn(
            client,
            uuid,
            getSingleTurnData(),
            access_token
        )

        response = viewTurn(
            client,
            uuid,
            1,
            access_token
        )

        assert 200 == response.status_code
        assert 'Turn data retrieved successfully.' in response.json['message']
        assert response.json['data']

        assert response.json['data']['player_1']
        """Player 1 response data validation."""

        assert response.json['data']['player_1']['characters'][0]
        assert 30 == response.json['data']['player_1']['characters'][0]['health']['current']
        assert 30 == response.json['data']['player_1']['characters'][0]['health']['max']
        assert 'move' in response.json['data']['player_1']['characters'][0]['action']
        assert 1 == response.json['data']['player_1']['characters'][0]['position']['x']
        assert 0 == response.json['data']['player_1']['characters'][0]['position']['y']

        assert response.json['data']['player_1']['characters'][1]
        assert 20 == response.json['data']['player_1']['characters'][1]['health']['current']
        assert 20 == response.json['data']['player_1']['characters'][1]['health']['max']
        assert 'move' in response.json['data']['player_1']['characters'][1]['action']
        assert 1 == response.json['data']['player_1']['characters'][1]['position']['x']
        assert 3 == response.json['data']['player_1']['characters'][1]['position']['y']

        assert response.json['data']['player_1']['characters'][2]
        assert 40 == response.json['data']['player_1']['characters'][2]['health']['current']
        assert 40 == response.json['data']['player_1']['characters'][2]['health']['max']
        assert 'move' in response.json['data']['player_1']['characters'][2]['action']
        assert 1 == response.json['data']['player_1']['characters'][2]['position']['x']
        assert 6 == response.json['data']['player_1']['characters'][2]['position']['y']

        assert response.json['data']['player_2']
        """Player 2 response data validation."""

        assert response.json['data']['player_2']['characters'][0]
        assert 50 == response.json['data']['player_2']['characters'][0]['health']['current']
        assert 50 == response.json['data']['player_2']['characters'][0]['health']['max']
        assert 'move' in response.json['data']['player_2']['characters'][0]['action']
        assert 14 == response.json['data']['player_2']['characters'][0]['position']['x']
        assert 0 == response.json['data']['player_2']['characters'][0]['position']['y']

        assert response.json['data']['player_2']['characters'][1]
        assert 30 == response.json['data']['player_2']['characters'][1]['health']['current']
        assert 30 == response.json['data']['player_2']['characters'][1]['health']['max']
        assert 'move' in response.json['data']['player_2']['characters'][1]['action']
        assert 14 == response.json['data']['player_2']['characters'][1]['position']['x']
        assert 3 == response.json['data']['player_2']['characters'][1]['position']['y']

        assert response.json['data']['player_2']['characters'][2]
        assert 20 == response.json['data']['player_2']['characters'][2]['health']['current']
        assert 20 == response.json['data']['player_2']['characters'][2]['health']['max']
        assert 'move' in response.json['data']['player_2']['characters'][2]['action']
        assert 14 == response.json['data']['player_2']['characters'][2]['position']['x']
        assert 6 == response.json['data']['player_2']['characters'][2]['position']['y']

    def testViewMatrixState(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']
        rv = newMatch(
            client,
            getMatchData(),
            access_token
        )

        uuid = json.loads(rv.data)['uuid']
        response = startMatch(
            client,
            uuid,
            access_token
        )

        rv = nextTurn(
            client,
            uuid,
            getSingleTurnData(),
            access_token
        )

        response = viewTurn(
            client,
            uuid,
            1,
            access_token
        )

        assert response.json['data']['matrix']

        matrix = getProjectedMatrix()
        same = True
        """Matrix validation setup."""

        for i in range(8):
            """Default battleground size is 16x8 tiles."""
            for actual, provided in zip(response.json['data']['matrix'][i], matrix[i]):
                """Use simple looping of list items to make direct comparisons on each value."""
                if actual != provided:
                    same = False

        assert True == same
