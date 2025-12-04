import pytest
from app_student import app, init_db
import tempfile
from pathlib import Path

@pytest.fixture
def client(monkeypatch, tmp_path):
    # Create a temporary database for tests
    test_db = tmp_path / "test_library.db"

    # Monkeypatch DB path inside app_student.py
    monkeypatch.setattr("app_student.DB", str(test_db))

    # Recreate all tables inside temp DB
    init_db()

    # Enable testing mode
    app.config["TESTING"] = True

    # Create test client
    with app.test_client() as client:
        yield client
