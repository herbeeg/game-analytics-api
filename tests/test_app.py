import datetime, json, pytest

from pathlib import Path

from app.main import app, db, Activation, User
from tests.utils import login, logout, register

TEST_DB = 'test.db'

class TestMainCase:
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

        new_key = Activation(app.config['ACTIVATION_KEY'])
        """Use a fixed activation key string for testing purposes."""
        db.session.add(new_key)
        db.session.commit()

        with app.test_client(self) as client:
            yield client

        db.drop_all()

    def testIndex(self, client):
        response = client.get('/', content_type='html/text')
        
        assert 200 == response.status_code
        assert b'There is no ignorance, there is knowledge.' == response.data

    def testDatabase(self):
        assert Path(TEST_DB).is_file()

    def testRegister(self, client):
        app.config['EMAIL'] = 'newuser@test.com'
        """Update app config email to allow checks against existing database rows."""
        app.config['USERNAME'] = 'newuser'

        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        assert 'Registration successful.' in json.loads(rv.data)['message']

        activation = db.session.query(Activation).filter_by(claimed=1, user_id=1).one()
        """Test redeeming of stored activation keys."""
        assert 1 == activation.id
        assert 1 == activation.user_id
        assert '08fe47e8814b410cbaf742463e8c9252' == activation.key
        assert 1 == activation.claimed
        
        users = db.session.query(User).filter_by(email=app.config['EMAIL']).all()
        assert datetime.datetime.now().strftime('%Y-%m-%d') == users[0].created_at.strftime('%Y-%m-%d')
        """Fairly vague check to ensure that the created_at timestamp is on the same day."""

        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])
        assert 200 == rv.status_code
        assert 'Login successful.' in json.loads(rv.data)['message']

        rv = logout(client)
        assert 200 == rv.status_code
        assert 'Logout successful.' in json.loads(rv.data)['message']

        rv = register(client, 'j' + app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        assert 400 == rv.status_code
        assert 'A user with that name already exists.' in json.loads(rv.data)['message']

        rv = register(client, app.config['EMAIL'], app.config['USERNAME'] + '1', app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        assert 400 == rv.status_code
        assert 'A user with that email already exists.' in json.loads(rv.data)['message']

        rv = register(client, 'act' + app.config['EMAIL'], 'act' + app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        """Already used activation key testing."""
        assert 400 == rv.status_code
        assert 'That activation key has already been used.' in json.loads(rv.data)['message']

        rv = register(client, 'act' + app.config['EMAIL'], 'act' + app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'] + '1')
        """Invalid activation key testing."""
        assert 400 == rv.status_code
        assert 'An activation key with that value does not exist.' in json.loads(rv.data)['message']

    def testLoginLogout(self, client):
        rv = register(client, app.config['EMAIL'], app.config['USERNAME'], app.config['PASSWORD'], app.config['ACTIVATION_KEY'])
        assert 200 == rv.status_code

        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'])
        assert 200 == rv.status_code
        assert 'Login successful.' in json.loads(rv.data)['message']

        rv = logout(client)
        assert 200 == rv.status_code
        assert 'Logout successful.' in json.loads(rv.data)['message']

        rv = login(client, app.config['EMAIL'] + 'j', app.config['PASSWORD'])
        assert 400 == rv.status_code
        assert 'Invalid email.' in json.loads(rv.data)['message']

        rv = login(client, app.config['EMAIL'], app.config['PASSWORD'] + 'j')
        assert 400 == rv.status_code
        assert 'Invalid password.' in json.loads(rv.data)['message']
