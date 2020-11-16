import datetime, json, pytest, time

from pathlib import Path

from app.models.activation import Activation
from app.models.match import Match
from app.models.match_meta import MatchMeta
from app.main import create_app
from app.database import db
from tests.helpers import getMatchData
from tests.utils import endMatch, login, newMatch, register, startMatch

TEST_DB = 'test.db'

class TestMatchManipulation:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        app = create_app()

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

    def testSetupMatch(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']
        timestamp = int(datetime.datetime.utcnow().timestamp())

        time.sleep(1)
        """Wait one second before creating a new match to allow timestamp comparisons."""

        rv = newMatch(
            client,
            getMatchData(),
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
            getMatchData(),
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
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']

        rv = newMatch(
            client,
            getMatchData(),
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

    def testStartMatchOtherOwners(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']

        rv = newMatch(
            client,
            getMatchData(),
            access_token
        )

        uuid = json.loads(rv.data)['uuid']

        new_rv = register(client, '1' + app.config['EMAIL'], '1' + app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY_2'])
        new_rv = login(client, '1' + app.config['EMAIL'], app.config['PASSWORD'])

        new_access_token = json.loads(new_rv.data)['access_token']

        response = client.get(
            f'/match/start/{uuid}',
            follow_redirects=False
        )

        assert 401 == response.status_code
        """Cannot start matches without authorisation."""

        response = startMatch(
            client,
            '',
            access_token
        )

        assert 404 == response.status_code
        """Cannot start matches that don't exist in the database."""

        response = startMatch(
            client,
            uuid,
            ''
        )

        assert 422 == response.status_code
        """Cannot start matches without a valid access token."""

        response = startMatch(
            client,
            uuid,
            new_access_token
        )

        assert 401 == response.status_code
        """Cannot start matches that were created by other users."""
        assert 'Cannot start matches owned by other users.' in response.json['message']

    def testEndMatch(self, client):
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

        match = db.session.query(Match).filter_by(user_id=1, live=1).one()
        assert 1 == match.live

        time.sleep(5)
        """Wait before ending the match to test final elapsed time."""

        response = endMatch(
            client,
            uuid,
            access_token
        )

        assert 200 == response.status_code
        assert 'Match ended successfully.' in response.json['message']
        assert (f'/match/view/{uuid}') in response.json['match_uri']

        match = db.session.query(Match).filter_by(user_id=1, uuid=uuid, live=0).one()
        assert 0 == match.live

        timing_metadata = db.session.query(MatchMeta).filter_by(match_id=uuid, key='timing').one()
        assert 5 == timing_metadata.value['elapsed_time']

    def testEndMatchOtherOwners(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']

        rv = newMatch(
            client,
            getMatchData(),
            access_token
        )

        uuid = json.loads(rv.data)['uuid']

        new_rv = register(client, '1' + app.config['EMAIL'], '1' + app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY_2'])
        new_rv = login(client, '1' + app.config['EMAIL'], app.config['PASSWORD'])

        new_access_token = json.loads(new_rv.data)['access_token']

        response = endMatch(
            client,
            uuid,
            access_token
        )

        assert 400 == response.status_code
        """Cannot end matches not in progress."""
        assert 'Cannot end matches that are not in progress.' in response.json['message']

        response = startMatch(
            client,
            uuid,
            access_token
        )

        response = endMatch(
            client,
            uuid,
            ''
        )

        assert 422 == response.status_code
        """Cannot end matches without a valid access token."""

        response = endMatch(
            client,
            '',
            access_token
        )

        assert 404 == response.status_code
        """Cannot end matches that don't exist in the database."""

        response = endMatch(
            client,
            uuid,
            new_access_token
        )

        assert 401 == response.status_code
        """Cannot end matches that were created by other users."""
        assert 'Cannot end matches owned by other users.' in response.json['message']
