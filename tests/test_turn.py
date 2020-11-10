import json, pytest

from pathlib import Path

from app.main import app, db, Match, MatchMeta
from tests.helpers import getMatchData, getSingleTurnData
from tests.utils import login, newMatch, nextTurn, register, startMatch

TEST_DB = 'test.db'

class TestNextTurn:
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

    def testUpdateTurn(self, client):
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

        assert 200 == rv.status_code
        assert 'Turn completed.' in json.loads(rv.data)['message']

        turn_meta = db.session.query(MatchMeta).filter_by(match_id=uuid, key='turns').one()

        assert 1 == len(turn_meta.value['turns'])
        """Metadata from one turn only should have been inserted."""

        turn_meta = turn_meta.value['turns'][0]
        """Get first and only item of turn metadata for shorter references."""

        assert turn_meta['player_1']
        """Player 1 metadata validation."""

        assert turn_meta['player_1']['characters'][0]
        assert 30 == turn_meta['player_1']['characters'][0]['health']['current']
        assert 30 == turn_meta['player_1']['characters'][0]['health']['max']
        assert 'move' in turn_meta['player_1']['characters'][0]['action']
        assert 1 == turn_meta['player_1']['characters'][0]['position']['x']
        assert 0 == turn_meta['player_1']['characters'][0]['position']['y']

        assert turn_meta['player_1']['characters'][1]
        assert 20 == turn_meta['player_1']['characters'][1]['health']['current']
        assert 20 == turn_meta['player_1']['characters'][1]['health']['max']
        assert 'move' in turn_meta['player_1']['characters'][1]['action']
        assert 1 == turn_meta['player_1']['characters'][1]['position']['x']
        assert 3 == turn_meta['player_1']['characters'][1]['position']['y']

        assert turn_meta['player_1']['characters'][2]
        assert 40 == turn_meta['player_1']['characters'][2]['health']['current']
        assert 40 == turn_meta['player_1']['characters'][2]['health']['max']
        assert 'move' in turn_meta['player_1']['characters'][2]['action']
        assert 1 == turn_meta['player_1']['characters'][2]['position']['x']
        assert 6 == turn_meta['player_1']['characters'][2]['position']['y']

        assert turn_meta['player_2']
        """Player 2 metadata validation."""

        assert turn_meta['player_2']['characters'][0]
        assert 50 == turn_meta['player_2']['characters'][0]['health']['current']
        assert 50 == turn_meta['player_2']['characters'][0]['health']['max']
        assert 'move' in turn_meta['player_2']['characters'][0]['action']
        assert 14 == turn_meta['player_2']['characters'][0]['position']['x']
        assert 0 == turn_meta['player_2']['characters'][0]['position']['y']

        assert turn_meta['player_2']['characters'][1]
        assert 30 == turn_meta['player_2']['characters'][1]['health']['current']
        assert 30 == turn_meta['player_2']['characters'][1]['health']['max']
        assert 'move' in turn_meta['player_2']['characters'][1]['action']
        assert 14 == turn_meta['player_2']['characters'][1]['position']['x']
        assert 3 == turn_meta['player_2']['characters'][1]['position']['y']

        assert turn_meta['player_2']['characters'][2]
        assert 20 == turn_meta['player_2']['characters'][2]['health']['current']
        assert 20 == turn_meta['player_2']['characters'][2]['health']['max']
        assert 'move' in turn_meta['player_2']['characters'][2]['action']
        assert 14 == turn_meta['player_2']['characters'][2]['position']['x']
        assert 6 == turn_meta['player_2']['characters'][2]['position']['y']

    def testUpdateTurnOtherOwners(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']
        rv = newMatch(
            client,
            getMatchData(),
            access_token
        )

        uuid = json.loads(rv.data)['uuid']

        rv = nextTurn(
            client,
            uuid,
            getSingleTurnData(),
            access_token
        )

        assert 400 == rv.status_code
        """Match hasn't started yet."""
        assert 'Cannot update matches that are not in progress.' in json.loads(rv.data)['message']

        response = startMatch(
            client,
            uuid,
            access_token
        )

        new_rv = register(client, '1' + app.config['EMAIL'], '1' + app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        new_rv = login(client, '1' + app.config['EMAIL'], app.config['PASSWORD'])

        new_access_token = json.loads(new_rv.data)['access_token']

        rv = client.post(
            f'/turn/update/{uuid}',
            data=getSingleTurnData(),
            content_type='application/json'
        )

        assert 401 == rv.status_code
        """Cannot update matches without authorisation."""

        rv = nextTurn(
            client,
            '',
            getSingleTurnData(),
            access_token
        )

        assert 404 == rv.status_code
        """Cannot update matches that don't exist in the database."""

        rv = nextTurn(
            client,
            uuid,
            getSingleTurnData(),
            ''
        )

        assert 422 == rv.status_code
        """Cannot update matches without a valid access token."""

        rv = nextTurn(
            client,
            uuid,
            getSingleTurnData(),
            new_access_token
        )

        assert 401 == rv.status_code
        """Cannot start matches that were created by other users."""
        assert 'Cannot update matches owned by other users.' in json.loads(rv.data)['message']
