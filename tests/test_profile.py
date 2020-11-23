import datetime
import json
import pytest
import time

from pathlib import Path

from app.database import db
from app.main import create_app
from app.models.activation import Activation
from tests.helpers import getMatchData, getSimulationTurnData
from tests.utils import endMatch, login, logout, newMatch, nextTurn, profile, register, startMatch, viewHistory, viewStats

TEST_DB = 'test.db'

class TestProtectedProfile:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        self.app = create_app()

        self.app.config['TESTING'] = True
        self.app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR.joinpath(TEST_DB)}'

        self.app.config['EMAIL'] = 'admin@test.com'
        self.app.config['USERNAME'] = 'admin'
        self.app.config['PASSWORD'] = 'password'
        self.app.config['ACTIVATION_KEY'] = '08fe47e8814b410cbaf742463e8c9252'

        db.create_all()

        new_key = Activation(self.app.config['ACTIVATION_KEY'])
        """Use fixed activation key strings for testing purposes."""
        db.session.add(new_key)
        db.session.commit()

        with self.app.test_client(self) as client:
            yield client

        db.drop_all()

    def testProfile(self, client):
        rv = register(client, self.app.config['EMAIL'], self.app.config['USERNAME'], self.app.config['PASSWORD'], self.app.config['ACTIVATION_KEY'])
        rv = login(client, self.app.config['EMAIL'], self.app.config['PASSWORD'])

        response = profile(client, json.loads(rv.data)['access_token'])

        assert 200 == response.status_code
        assert self.app.config['EMAIL'] in response.json['email']
        assert self.app.config['USERNAME'] in response.json['username']

        date_obj = datetime.datetime.strptime(response.json['created_at'], '%a, %d %b %Y %H:%M:%S %Z')
        assert datetime.datetime.now().strftime('%Y-%m-%d') in date_obj.strftime('%Y-%m-%d')

        response = client.get(
            '/profile',
            follow_redirects=False
        )

        assert 401 == response.status_code

    def testMatchHistory(self, client):
        rv = register(client, self.app.config['EMAIL'], self.app.config['USERNAME'], self.app.config['PASSWORD'], self.app.config['ACTIVATION_KEY'])
        rv = login(client, self.app.config['EMAIL'], self.app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']
        uuids = []
        test_started = int(datetime.datetime.utcnow().timestamp())

        for m in range(5):
            rv = newMatch(
                client,
                getMatchData(),
                access_token
            )

            uuids.append(json.loads(rv.data)['uuid'])
            response = startMatch(
                client,
                uuids[m],
                access_token
            )

            for n in range(10):
                rv = nextTurn(
                    client,
                    uuids[m],
                    getSimulationTurnData(n),
                    access_token
                )

                assert 200 == rv.status_code

            time.sleep(2)
            """Wait before ending the match to test final elapsed time."""

            response = endMatch(
                client,
                uuids[m],
                access_token
            )

        response = viewHistory(
            client,
            1,
            access_token
        )

        assert 200 == response.status_code

        assert response.json['match_history']
        assert 5 == len(response.json['match_history'])

        assert uuids[0] in response.json['match_history'][0]['id']
        assert uuids[1] in response.json['match_history'][1]['id']
        assert uuids[2] in response.json['match_history'][2]['id']
        assert uuids[3] in response.json['match_history'][3]['id']
        assert uuids[4] in response.json['match_history'][4]['id']

        assert ('Match 1 - ' + uuids[0]) in response.json['match_history'][0]['name']
        assert ('Match 1 - ' + uuids[1]) in response.json['match_history'][1]['name']
        assert ('Match 1 - ' + uuids[2]) in response.json['match_history'][2]['name']
        assert ('Match 1 - ' + uuids[3]) in response.json['match_history'][3]['name']
        assert ('Match 1 - ' + uuids[4]) in response.json['match_history'][4]['name']

        assert test_started < response.json['match_history'][0]['ended_at']
        assert test_started < response.json['match_history'][1]['ended_at']
        assert test_started < response.json['match_history'][2]['ended_at']
        assert test_started < response.json['match_history'][3]['ended_at']
        assert test_started < response.json['match_history'][4]['ended_at']

        response = client.get(
            '/profile/1/history',
            follow_redirects=False
        )

        assert 401 == response.status_code

        response = viewHistory(client, 117, access_token)

        assert 400 == response.status_code
        assert 'User does not exist.' in response.json['message']

        new_rv = register(client, '1' + self.app.config['EMAIL'], '1' + self.app.config['USERNAME'], self.app.config['PASSWORD'], self.app.config['ACTIVATION_KEY_2'])
        new_rv = login(client, '1' + self.app.config['EMAIL'], self.app.config['PASSWORD'])

        response = viewHistory(client, 2, access_token)

        assert 400 == response.status_code
        assert 'Cannot retrieve match history from another user.' in response.json['message']

    def testUserStatistics(self, client):
        rv = register(client, self.app.config['EMAIL'], self.app.config['USERNAME'], self.app.config['PASSWORD'], self.app.config['ACTIVATION_KEY'])
        rv = login(client, self.app.config['EMAIL'], self.app.config['PASSWORD'])

        access_token = json.loads(rv.data)['access_token']

        for m in range(5):
            """Scaffold some test match data for stats fetching."""
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

            for n in range(10):
                rv = nextTurn(
                    client,
                    uuid,
                    getSimulationTurnData(n),
                    access_token
                )

            time.sleep(4.95)
            """Wait before ending the match to test final elapsed time."""

            response = endMatch(
                client,
                uuid,
                access_token
            )

        response = viewStats(
            client,
            1,
            access_token
        )

        assert 200 == response.status_code
        assert response.json['stats']

        assert 25 == response.json['stats']['match_time']

        assert 5 == response.json['stats']['completed']

        response = client.get(
            '/profile/1/stats',
            follow_redirects=False
        )

        assert 401 == response.status_code

        response = viewStats(client, 117, access_token)

        assert 400 == response.status_code
        assert 'User does not exist.' in response.json['message']

        new_rv = register(client, '1' + self.app.config['EMAIL'], '1' + self.app.config['USERNAME'], self.app.config['PASSWORD'], self.app.config['ACTIVATION_KEY_2'])
        new_rv = login(client, '1' + self.app.config['EMAIL'], self.app.config['PASSWORD'])

        response = viewStats(client, 2, access_token)

        assert 400 == response.status_code
        assert 'Cannot retrieve statistics from another user.' in response.json['message']
