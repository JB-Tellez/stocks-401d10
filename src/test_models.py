import pytest
import os
from . import app
from .models import db, Company

@pytest.fixture
def session():

    def do_nothing():
        pass

    db.session.commit = do_nothing

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URL')

    yield db.session

    db.session.rollback()


def test_company(session):
    companies = Company.query.all()
    assert len(companies) == 0

def test_add_company(session):
    google = Company(symbol = 'goog')
    session.add(google)
    session.commit()
    companies = Company.query.all()
    assert len(companies) == 1

def test_add_different_company(session):
    company = Company(symbol = 'msft')
    session.add(company)
    session.commit()
    companies = Company.query.all()
    assert len(companies) == 1
