import pytest
import app

@pytest.fixture(scope='module')
def test_client():
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    yield client
