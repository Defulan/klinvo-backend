import random
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db, User
from app.config import settings
from app.security import hash_password
from app.enums import CookieKey

test_engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def create_random_user(db_session):
    def _create_random_user(password: str | None = None):
        letters = "qwertyuiopasdfghjklzxcvbnm"
        name = "".join(random.choices(letters, k=6))

        if password is None:
            password = "".join(random.choices(letters, k=12))

        user = User(name=name, password_hash=hash_password(password))
        db_session.add(user)
        db_session.commit()
        return user
    
    return _create_random_user


@pytest.fixture()
def create_session_id(client, monkeypatch):
    def _create_session_id(module_name: str, user_id: int):
        monkeypatch.setattr(f"app.routers.{module_name}.get_value_from_cookie", lambda session_id: user_id)
        client.cookies.set(CookieKey.SESSION_ID, "IDontCareMonkeypatchWillDoEverythingForMe")
    return _create_session_id
