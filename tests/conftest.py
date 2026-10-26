import random
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import position
from app.main import app
from app.database import Base, get_db, User, Language, Note, Word, Category, get_last_word, get_last_category
from app.config import settings
from app.security import hash_password
from app.enums import CookieKey
from enums import ModuleName

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
def create_random_language(db_session):
    def _create_random_language(author_id: int, is_private: bool = True):
        letters = "qwertyuiopasdfghjklzxcvbnm"
        name = "".join(random.choices(letters, k=4))

        language = Language(author_id=author_id, name=name, is_private=is_private)
        db_session.add(language)
        db_session.commit()
        return language
    
    return _create_random_language


@pytest.fixture()
def create_random_note(db_session):
    def _create_random_note(language_id: int):
        letters = "qwertyuiopasdfghjklzxcvbnm"
        title = "".join(random.choices(letters, k=12))

        note = Note(language_id=language_id, title=title)
        db_session.add(note)
        db_session.commit()
        return note
    
    return _create_random_note


@pytest.fixture()
def create_random_word(db_session):
    def _create_random_word(language_id: int, category_id: int | None = None):
        letters = "qwertyuiopasdfghjklzxcvbnm"
        value = "".join(random.choices(letters, k=6))
        meaning = "".join(random.choices(letters, k=24))

        last_word = get_last_word(db_session, language_id=language_id, category_id=category_id)

        if last_word is None:
            new_position = position.get_none_position()
        else:
            new_position = position.generate_new_bottom_position(last_word.position)

        word = Word(
            language_id=language_id, category_id=category_id,
            position=new_position, value=value, meaning=meaning,
        )
        db_session.add(word)
        db_session.commit()
        return word
    
    return _create_random_word


@pytest.fixture()
def create_random_category(db_session):
    def _create_random_category(language_id: int) -> Category:
        letters = "qwertyuiopasdfghjklzxcvbnm"
        name = "".join(random.choices(letters, k=5))

        last_category = get_last_category(db_session, language_id=language_id)

        if last_category is None:
            new_position = position.get_none_position()
        else:
            new_position = position.generate_new_bottom_position(last_category.position)

        category = Category(
            language_id=language_id, position=new_position,
            name=name
        )
        db_session.add(category)
        db_session.commit()
        return category
    
    return _create_random_category


@pytest.fixture()
def create_session_id(client, monkeypatch):
    def _create_session_id(module_name: ModuleName, user_id: int):
        monkeypatch.setattr(f"app.routers.{module_name}.get_value_from_cookie", lambda session_id: user_id)
        client.cookies.set(CookieKey.SESSION_ID, "IDontCareMonkeypatchWillDoEverythingForMe")
    return _create_session_id
