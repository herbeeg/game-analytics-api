import json, pytest

from pathlib import Path

from app.main import app, db, Match, MatchMeta
from tests.helpers import getMatchData, getTurnData
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

        db.create_all()

        with app.test_client(self) as client:
            yield client

        db.drop_all()

    def testUpdateTurn(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
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
            getTurnData(0),
            access_token
        )

        assert 200 == rv.response_code
        assert 'Turn completed.' in json.loads(rv.data)['message']

        turn_meta = db.session.query(MatchMeta).filter_by(match_id=uuid, key='turns').one()

        assert 1 == len(turn_meta)
        """Metadata from one turn only should have been inserted."""

        assert turn_meta['player_1']
        assert turn_meta['player_1']['characters'][0]

        assert turn_meta['player_2']
        assert turn_meta['player_2']['characters'][0]
