import pytest

from pathlib import Path

from app.main import app, initDb

class TestMainCase:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True

        with app.test_client(self) as client:
            yield client

    def testIndex(self, client):
        response = client.get('/', content_type='html/text')
        
        assert 200 == response.status_code
        assert b'There is no ignorance, there is knowledge.' == response.data

    def testDatabase(self):
        initDb()
        assert Path('analytics.db').is_file()