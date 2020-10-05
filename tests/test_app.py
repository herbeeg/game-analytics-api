import pytest

from app import app

class MainTestCase:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True

        with app.test_client(self) as client:
            yield client


    def testIndex(self, client):
        response = client.get('/', content_type='html/text')
        
        assert 200 == response.status_code
        assert b'Hello, World!' == response.data