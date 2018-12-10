import pytest
import os
from . import app
from .models import db


@pytest.fixture
def client():
    """
    Fixture to supply a test client
    Can be full featured, spin up / shut down database connections
    """

    def do_nothing():
        pass

    db.session.commit = do_nothing

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL')

    yield app.test_client()

    db.session.rollback()


def test_client(client):
    assert client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'<h1>Welcome to the site</h1>' in rv.data

def test_search_get(client):
    rv = client.get('/search')
    assert b'<h2>Search for stocks</h2>' in rv.data

def test_search_post_before_redirect(client):
    rv = client.post('/search', data = {'symbol':'goog'})
    assert rv.status_code == 302

def test_search_post_with_redirect(client):
    rv = client.post('/search', data = {'symbol':'goog'}, follow_redirects = True)
    assert rv.status_code == 200
    assert b'<h2>Welcome to the Portfolio</h2>' in rv.data

