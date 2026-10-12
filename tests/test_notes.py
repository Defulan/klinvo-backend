from fastapi import status
from app.enums import ErrorCode


def test_get_note_private_success(client, create_random_user, create_random_language, create_random_note, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    note = create_random_note(language_id=language.id)
    create_session_id(module_name="notes", user_id=user.id)

    response = client.get(f"/notes/{note.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is True
    
    data = response.json()
    assert data["id"] == note.id
    assert data["languageId"] == language.id
    assert data["title"] == note.title
    assert data["content"] is None
    assert data["createdAt"] is not None


def test_get_note_public_success(client, create_random_user, create_random_language, create_random_note):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)
    note = create_random_note(language_id=language.id)

    response = client.get(f"/notes/{note.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is False
    
    data = response.json()
    assert data["id"] == note.id
    assert data["languageId"] == language.id
    assert data["title"] == note.title
    assert data["content"] is None
    assert data["createdAt"] is not None


def test_get_note_private_error(client, create_random_user, create_random_language, create_random_note, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    note = create_random_note(language_id=language.id)
    create_session_id(module_name="notes", user_id=456789)

    response = client.get(f"/notes/{note.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.NOTE_DOESNT_EXIST
    assert language.is_private is True


def test_get_note_not_found_error(client):
    response = client.get("/notes/9218")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.NOTE_DOESNT_EXIST


def test_create_note_success(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name="notes", user_id=user.id)

    payload = {
        "title": "qwertyui"
    }

    response = client.post(f"/notes/{language.id}", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["languageId"] == language.id
    assert data["title"] == payload["title"]
    assert data["content"] is None
    assert data["createdAt"] is not None


def test_create_note_validation_too_long_error(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name="notes", user_id=user.id)

    payload = {
        "title": "qwertyui"*256
    }

    response = client.post(f"/notes/{language.id}", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_note_validation_empty_error(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name="notes", user_id=user.id)

    payload = {
        "title": None
    }

    response = client.post(f"/notes/{language.id}", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_note_unauthorized_error(client, create_random_user, create_random_language):
    user = create_random_user()
    language = create_random_language(author_id=user.id)

    payload = {
        "title": "qwertyui"
    }

    response = client.post(f"/notes/{language.id}", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == ErrorCode.UNAUTHORIZED


def test_create_note_user_not_found_error(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name="notes", user_id=1920827)

    payload = {
        "title": "qwertyui"
    }

    response = client.post(f"/notes/{language.id}", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.USER_DOESNT_EXIST


def test_create_note_language_not_found_error(client, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name="notes", user_id=user.id)

    payload = {
        "title": "qwertyui"
    }

    response = client.post("/notes/124567", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_create_note_not_author_public_error(client, create_random_user, create_random_language, create_session_id):
    author_user = create_random_user()
    other_user = create_random_user()
    language = create_random_language(author_id=author_user.id, is_private=False)
    create_session_id(module_name="notes", user_id=other_user.id)

    payload = {
        "title": "qwertyui"
    }

    response = client.post(f"/notes/{language.id}", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == ErrorCode.NO_PERMISSIONS


def test_create_note_not_author_private_error(client, create_random_user, create_random_language, create_session_id):
    author_user = create_random_user()
    other_user = create_random_user()
    language = create_random_language(author_id=author_user.id)
    create_session_id(module_name="notes", user_id=other_user.id)

    payload = {
        "title": "qwertyui"
    }

    response = client.post(f"/notes/{language.id}", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_change_note_full_success(client, create_random_user, create_random_language, create_random_note, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    note = create_random_note(language_id=language.id)
    create_session_id(module_name="notes", user_id=user.id)

    payload = {
        "title": "Juaqo, lasiUQm llas",
        "content": (
            "**This is**\nstill a line\n\n"
            "but this is something new!\n\n"
            "* list item 1\n* *list* item2\n* **list item 3**\n\n"
            "* ***list*** item... oh, it's already a different list"
        )}

    response = client.patch(f"/notes/{note.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == note.id
    assert data["languageId"] == language.id
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert data["createdAt"] is not None


def test_change_note_only_content_success(client, create_random_user, create_random_language, create_random_note, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    note = create_random_note(language_id=language.id)
    create_session_id(module_name="notes", user_id=user.id)

    payload = {
        "content": (
            "**This is**\nstill a line\n\n"
            "but this is something new!\n\n"
            "* list item 1\n* *list* item2\n* **list item 3**\n\n"
            "* ***list*** item... oh, it's already a different list"
        )}

    response = client.patch(f"/notes/{note.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == note.id
    assert data["languageId"] == language.id
    assert data["title"] == note.title
    assert data["content"] == payload["content"]
    assert data["createdAt"] is not None


def test_change_note_empty_success(client, create_random_user, create_random_language, create_random_note, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    note = create_random_note(language_id=language.id)
    create_session_id(module_name="notes", user_id=user.id)

    payload = {}

    response = client.patch(f"/notes/{note.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == note.id
    assert data["languageId"] == language.id
    assert data["title"] == note.title
    assert data["content"] == note.content
    assert data["createdAt"] is not None
