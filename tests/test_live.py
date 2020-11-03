import datetime, json, pytest, time

from pathlib import Path

from app.main import app, db, Match
from tests.utils import login, newMatch, register

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
        test_data = json.dumps({
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
                        'start_pos': {
                            'x': 0,
                            'y': 0
                        }
                    },
                    {
                        'id': 1,
                        'start_pos': {
                            'x': 0,
                            'y': 3
                        }
                    },
                    {
                        'id': 2,
                        'start_pos': {
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
                        'start_pos': {
                            'x': 15,
                            'y': 0
                        }
                    },
                    {
                        'id': 4,
                        'start_pos': {
                            'x': 15,
                            'y': 3
                        }
                    },
                    {
                        'id': 5,
                        'start_pos': {
                            'x': 15,
                            'y': 6
                        }
                    }
                ]
            }
        })

        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']
        timestamp = int(datetime.datetime.utcnow().timestamp())

        time.sleep(1)
        """Wait one second before creating a new match to allow timestamp comparisons."""

        rv = newMatch(
            client,
            test_data,
            access_token
        )

        assert 200 == rv.status_code
        assert 'New match setup successfully.' in json.loads(rv.data)['message']

        live_match = db.session.query(Match).filter_by(user_id=1, live=0).one()

        assert 'Match 1' == live_match.title
        assert 1 == live_match.id
        assert 1 == live_match.user_id
        assert 0 == live_match.live
        assert timestamp < live_match.created_at

        rv = newMatch(
            client,
            test_data,
            'a'
        )
        assert 401 == rv.status_code

        rv = newMatch(
            client, 
            {}, 
            ''
        )
        assert 422 == rv.status_code

    def testStartMatch(self, client):
        return

    def testEndMatch(self, client):
        return

    def testViewMatch(self, client):
        return
