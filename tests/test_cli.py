import pytest

from pathlib import Path

from app.database import db
from app.main import create_app
from app.models.activation import Activation
from app.models.user import User

TEST_DB = 'test.db'

class TestTaskCLI:
    @pytest.fixture
    def client(self):
        BASE_DIR = Path(__file__).resolve().parent.parent

        self.app = create_app()

        self.app.config['TESTING'] = True
        self.app.config['DATABASE'] = BASE_DIR.joinpath(TEST_DB)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR.joinpath(TEST_DB)}'

        db.create_all()

        with self.app.test_client(self) as client:
            yield client

        db.drop_all()

    def testActivationKeyGeneration(self, client):
        runner = self.app.test_cli_runner()
        result = runner.invoke(args=['task','generate-activation-key'])

        print(result.output)

        activation = db.session.query(Activation).filter_by(id=1).first()

        assert result.output == activation.key
