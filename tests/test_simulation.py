import datetime, json, pytest

from pathlib import Path

from app.models.activation import Activation
from app.main import create_app
from app.database import db
from tests.helpers import getMatchData, getSimulationTurnData
from tests.utils import login, logout, newMatch, nextTurn, register, startMatch

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
