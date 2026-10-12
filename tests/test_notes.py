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


def test_get_note_public_success(client, create_random_user, create_random_language, create_random_note, create_session_id):
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
