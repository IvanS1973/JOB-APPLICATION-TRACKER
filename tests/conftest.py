"""Test setup.

By default the route tests use a temporary in-memory SQLite database so they run anywhere.
To run them against real MySQL, create an EMPTY database (e.g. job_tracker_test) and set:
    set TEST_DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/job_tracker_test
NEVER point this at your real job_tracker database: the tests drop all tables.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from config import Config  # noqa: E402
from models import db  # noqa: E402


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    SQLALCHEMY_ENGINE_OPTIONS = {}


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
