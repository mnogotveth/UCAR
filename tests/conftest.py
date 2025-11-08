import pytest
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

import app.main as app_main
import app.database as app_database

@pytest.fixture()
def client(monkeypatch):
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    monkeypatch.setattr(app_database, "engine", test_engine)
    monkeypatch.setattr(app_main, "engine", test_engine)

    SQLModel.metadata.create_all(test_engine)

    with TestClient(app_main.app) as c:
        yield c
