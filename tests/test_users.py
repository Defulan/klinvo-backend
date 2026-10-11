from fastapi import status
from app.database import User
from app.security import verify_password
from app.enums import CookieKey, ErrorCode


def test_get_user_success(client, create_random_user):
    user = create_random_user()

    response = client.get(f"/users/{user.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] == user.id
    assert data["name"] == user.name


def test_get_user_not_found_error(client):
    response = client.get("/users/2112222")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.USER_DOESNT_EXIST


def test_get_user_invalid_id_error(client):
    response = client.get("/users/jsadh")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_users_success(client, create_random_user):
    user1 = create_random_user()
    user2 = create_random_user()

    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == user1.name
    assert data[1]["name"] == user2.name


def test_get_user_languages_by_guest_success(client, create_random_user, create_random_language):
    user = create_random_user()

    user_languages = [create_random_language(author_id=user.id, is_private=bool(i % 2)) for i in range(3)]
    other_user_languages = [create_random_language(author_id=create_random_user().id) for _ in range(4)]

    response = client.get(f"/users/{user.id}/languages")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2

    for language in data:
        assert language["authorId"] == user.id
        assert language["isPrivate"] is False


def test_get_user_languages_by_author_success(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    create_session_id(module_name="users", user_id=user.id)

    user_languages = [create_random_language(author_id=user.id, is_private=bool(i % 2)) for i in range(3)]
    other_user_languages = [create_random_language(author_id=create_random_user().id) for _ in range(4)]

    response = client.get(f"/users/{user.id}/languages")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 3

    for language in data:
        assert language["authorId"] == user.id


def test_create_user_success(client, db_session):
    payload = {
        "name": "qwerty",
        "password": "123457",
        "repassword": "123457"
    }

    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    assert CookieKey.SESSION_ID in response.cookies

    user = db_session.query(User).filter_by(name=payload["name"]).first()
    assert user is not None
    assert verify_password(payload["password"], user.password_hash)


def test_create_user_authorized_error(client):
    payload = {
        "name": "qwerty",
        "password": "123457",
        "repassword": "123457"
    }

    client.cookies.set(CookieKey.SESSION_ID, "some_value")

    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == ErrorCode.AUTHORIZED


def test_create_user_passwords_doesnt_match_error(client):
    payload = {
        "name": "qwerty",
        "password": "123457",
        "repassword": "fff1234508"
    }

    response = client.post("/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_change_user_success_all(client, db_session, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name="users", user_id=user.id)

    payload = {
        "name": "asdasd",
        "bio": "KOKOKOOKKOKOOOKOKOKOOKOKO"
    }

    response = client.patch("/users/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    db_session.refresh(user)
    assert payload["name"] == user.name
    assert payload["bio"] == user.bio


def test_change_user_success_partial(client, db_session, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name="users", user_id=user.id)

    payload = {
        "name": None,
        "bio": "KOKOKOOKKOKOOOKOKOKOOKOKO"
    }
    old_name = user.name

    response = client.patch("/users/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    db_session.refresh(user)
    assert old_name == user.name
    assert payload["bio"] == user.bio


def test_change_user_validation_error(client, create_session_id):
    create_session_id(module_name="users", user_id=1337)

    payload = {
        "name": "VERYMUCHTEXT"*256,
        "bio": "KOKOKOOKKOKOOOKOKOKOOKOKO"
    }

    response = client.patch("/users/", json=payload)
    assert response.status_code == 422


def test_change_user_unauthorized_error(client):
    payload = {
        "name": "example_data",
        "bio": "IDontCareAnywayThereIsTestedSessionId"
    }

    response = client.patch("/users/", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == ErrorCode.UNAUTHORIZED



def test_change_user_not_exist_error(client, create_session_id):
    create_session_id(module_name="users", user_id=823712)

    payload = {
        "name": "example_data",
        "bio": "KOKOKOOKKOKOOOKOKOKOOKOKO"
    }

    response = client.patch("/users/", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.USER_DOESNT_EXIST
