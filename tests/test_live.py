import datetime, json, pytest, time

from pathlib import Path

from app.main import app, db, Match, MatchMeta
from tests.utils import login, newMatch, register, startMatch

TEST_DB = 'test.db'

class TestLiveMatch:
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

    def testSetupMatch(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']
        timestamp = int(datetime.datetime.utcnow().timestamp())

        time.sleep(1)
        """Wait one second before creating a new match to allow timestamp comparisons."""

        rv = newMatch(
            client,
            self.getMatchData(),
            access_token
        )

        assert 200 == rv.status_code
        assert 'New match setup successfully.' in json.loads(rv.data)['message']

        match = db.session.query(Match).filter_by(user_id=1, live=0).one()

        assert 'Match 1' == match.title
        assert 1 == match.id
        assert 1 == match.user_id
        assert 0 == match.live
        assert timestamp < match.created_at

        rv = newMatch(
            client,
            self.getMatchData(),
            ''
        )

        assert 422 == rv.status_code

        rv = newMatch(
            client,
            json.dumps({}),
            access_token
        )

        assert 400 == rv.status_code
        assert 'Malformed match data provided.' in json.loads(rv.data)['message']

    def testStartMatch(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']

        rv = newMatch(
            client,
            self.getMatchData(),
            access_token
        )

        uuid = json.loads(rv.data)['uuid']

        assert 36 == len(uuid)

        response = startMatch(
            client,
            uuid,
            access_token
        )

        assert 200 == response.status_code
        assert 'Match started successfully.' in response.json['message']
        assert (f'/match/view/{uuid}') in response.json['match_uri']

        match = db.session.query(Match).filter_by(user_id=1, live=1).one()

        assert 1 == match.user_id
        assert 1 == match.live

        p1_metadata = db.session.query(MatchMeta).filter_by(match_id=uuid, key='player_1').one()

        assert 'Player 1' == p1_metadata.value['name']

        assert 0 == p1_metadata.value['characters'][0]['id']
        assert 0 == p1_metadata.value['characters'][0]['position']['x']
        assert 0 == p1_metadata.value['characters'][0]['position']['y']

        assert 1 == p1_metadata.value['characters'][1]['id']
        assert 0 == p1_metadata.value['characters'][1]['position']['x']
        assert 3 == p1_metadata.value['characters'][1]['position']['y']

        assert 2 == p1_metadata.value['characters'][2]['id']
        assert 0 == p1_metadata.value['characters'][2]['position']['x']
        assert 6 == p1_metadata.value['characters'][2]['position']['y']

        p2_metadata = db.session.query(MatchMeta).filter_by(match_id=uuid, key='player_2').one()

        assert 'Player 2' == p2_metadata.value['name']

        assert 3 == p2_metadata.value['characters'][0]['id']
        assert 15 == p2_metadata.value['characters'][0]['position']['x']
        assert 0 == p2_metadata.value['characters'][0]['position']['y']

        assert 4 == p2_metadata.value['characters'][1]['id']
        assert 15 == p2_metadata.value['characters'][1]['position']['x']
        assert 3 == p2_metadata.value['characters'][1]['position']['y']

        assert 5 == p2_metadata.value['characters'][2]['id']
        assert 15 == p2_metadata.value['characters'][2]['position']['x']
        assert 6 == p2_metadata.value['characters'][2]['position']['y']

        response = startMatch(
            client,
            '',
            access_token
        )

        assert 404 == response.status_code

        response = startMatch(
            client,
            uuid,
            ''
        )

        assert 422 == response.status_code

    def testEndMatch(self, client):
        return

    def testViewMatch(self, client):
        return

    def getMatchData(self):
        return json.dumps({
            'title': 'Match 1',
            'size': {
                'x': 16,
                'y': 8
            },
            'player_1': {
                'name': 'Player 1',
                'characters': [
                    {
                        'id': 0,
                        'position': {
                            'x': 0,
                            'y': 0
                        }
                    },
                    {
                        'id': 1,
                        'position': {
                            'x': 0,
                            'y': 3
                        }
                    },
                    {
                        'id': 2,
                        'position': {
                            'x': 0,
                            'y': 6
                        }
                    }
                ]
            },
            'player_2': {
                'name': 'Player 2',
                'characters': [
                    {
                        'id': 3,
                        'position': {
                            'x': 15,
                            'y': 0
                        }
                    },
                    {
                        'id': 4,
                        'position': {
                            'x': 15,
                            'y': 3
                        }
                    },
                    {
                        'id': 5,
                        'position': {
                            'x': 15,
                            'y': 6
                        }
                    }
                ]
            }
        })
