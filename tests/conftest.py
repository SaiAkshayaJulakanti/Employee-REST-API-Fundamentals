"""
Pytest Fixtures configuration for Employee REST API testing.
"""
import sys
import os
import pytest

# Ensure app package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models import Employee

@pytest.fixture
def app():
    """Create and configure a clean Flask application instance for each test."""
    _app = create_app('test')

    with _app.app_context():
        db.create_all()
        yield _app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()

@pytest.fixture
def sample_employee(app):
    """Seed a sample employee into the testing database."""
    with app.app_context():
        emp = Employee(
            name="Alice Smith",
            email="alice.smith@example.com",
            department="Engineering",
            role="Backend Developer",
            salary=85000.0
        )
        db.session.add(emp)
        db.session.commit()
        db.session.refresh(emp)
        return emp.to_dict()
