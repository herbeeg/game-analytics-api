import datetime
import json
import pytest

from pathlib import Path

from app.database import db
from app.main import create_app
from app.models.activation import Activation
from app.models.match_meta import MatchMeta
from tests.helpers import getMatchData, getSimplifiedPlayer1Data, getSimplifiedPlayer2Data, getSimulationTurnData
from tests.utils import endMatch, login, logout, newMatch, nextTurn, register, startMatch

TEST_DB = 'test.db'

class TestMatchSimulation:
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
        """Use a fixed activation key string for testing purposes."""
        db.session.add(new_key)
        db.session.commit()

        with self.app.test_client(self) as client:
            yield client

        db.drop_all()

    def testFullMatchSimulation(self, client):
        rv = register(client, self.app.config['EMAIL'], self.app.config['USERNAME'], self.app.config['PASSWORD'], self.app.config['ACTIVATION_KEY'])
        rv = login(client, self.app.config['EMAIL'], self.app.config['PASSWORD'])

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

        for n in range(10):
            rv = nextTurn(
                client,
                uuid,
                getSimulationTurnData(n),
                access_token
            )

            assert 200 == rv.status_code

        response = endMatch(
            client,
            uuid,
            access_token
        )

        assert 200 == response.status_code

        turn_meta = db.session.query(MatchMeta).filter_by(match_id=uuid, key='turns').one()
        turn_data = turn_meta.value['turns']

        assert 10 == len(turn_data)
        """Check that the looped turns have passed."""

        for index, turn in enumerate(turn_data):
            count = 0

            for character in turn['player_1']['characters']:
                assert 'move' in character['action']
                assert getSimplifiedPlayer1Data()[index][count][0] == character['position']['x']
                assert getSimplifiedPlayer1Data()[index][count][1] == character['position']['y']

                count += 1

        for index, turn in enumerate(turn_data):
            count = 0

            for character in turn['player_2']['characters']:
                assert 'move' in character['action']
                assert getSimplifiedPlayer2Data()[index][count][0] == character['position']['x']
                assert getSimplifiedPlayer2Data()[index][count][1] == character['position']['y']

                count += 1
