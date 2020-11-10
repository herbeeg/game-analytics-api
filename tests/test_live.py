import json, pytest

from pathlib import Path

from app.main import app, db, Match, MatchMeta
from tests.helpers import getMatchData
from tests.utils import login, newMatch, register, startMatch

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

        db.create_all()

        with app.test_client(self) as client:
            yield client

        db.drop_all()