from fastapi import status
from app.enums import ErrorCode
from enums import ModuleName


def test_get_public_languages_success(client, create_random_user, create_random_language):
    author_id = create_random_user().id
    languages = [create_random_language(author_id=author_id, is_private=bool(i % 2)) for i in range(5)]

    response = client.get("/languages/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 3

    languages_map = {lang.id: lang for lang in languages}

    for response_language in data:
        language = languages_map[response_language["id"]]

        assert response_language["id"] == language.id
        assert response_language["authorId"] == language.author_id
        assert response_language["name"] == language.name
        assert response_language["createdAt"] is not None
        assert response_language["isPrivate"] is False


def test_get_language_success(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name=ModuleName.LANGUAGES, user_id=user.id)

    response = client.get(f"/languages/{language.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] == language.id
    assert data["authorId"] == language.author.id == user.id
    assert data["name"] == language.name
    assert data["createdAt"] is not None
    assert data["isPrivate"] is True


def test_get_language_not_found_error(client):
    response = client.get("/languages/8721321")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_get_language_no_permissions_error(client, create_random_user, create_random_language):
    user = create_random_user()
    language = create_random_language(author_id=user.id)

    response = client.get(f"/languages/{language.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_get_language_notes_success(client, create_random_user, create_random_language, create_random_note):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)

    for _ in range(3):
        create_random_note(language_id=language.id)

    response = client.get(f"/languages/{language.id}/notes")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 3
    
    for note in data:
        assert note["languageId"] == language.id
        assert len(note["title"]) > 0
        assert note["content"] is None
        assert note["createdAt"] is not None


def test_get_language_notes_not_found_error(client):
    response = client.get("/languages/2831924/notes")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_get_language_notes_private_error(client, create_random_user, create_random_language, create_random_note):
    user = create_random_user()
    language = create_random_language(author_id=user.id)

    for _ in range(3):
        create_random_note(language_id=language.id)

    response = client.get(f"/languages/{language.id}/notes")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_get_language_words_uncategorized_success(
        client, create_random_user, create_random_language, create_random_word
    ):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)

    for _ in range(3):
        create_random_word(language_id=language.id)

    response = client.get(f"/languages/{language.id}/words")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 3

    for word in data:
        assert word["languageId"] == language.id
        assert word["categoryId"] is None
        assert word["position"] is not None
        assert word["value"] is not None
        assert word["meaning"] is not None


def test_get_language_words_many_categories_success(
        client, create_random_user, create_random_language, create_random_word, create_random_category
    ):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)

    category_1 = create_random_category(language_id=language.id)
    category_2 = create_random_category(language_id=language.id)

    words_quantity = 20
    possible_categories = (None, category_1.id, category_2.id)
    for i in range(words_quantity):
        category_id = possible_categories[i % 3]
        create_random_word(language_id=language.id, category_id=category_id)

    response = client.get(f"/languages/{language.id}/words")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == words_quantity

    for word in data:
        assert word["languageId"] == language.id
        assert word["categoryId"] in possible_categories
        assert word["position"] is not None
        assert word["value"] is not None
        assert word["meaning"] is not None


def test_get_language_categories_success(
        client, create_random_user, create_random_language, create_random_category
    ):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)

    categories_quantity = 6
    for _ in range(categories_quantity):
        create_random_category(language_id=language.id)

    response = client.get(f"/languages/{language.id}/categories")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == categories_quantity

    for category in data:
        assert category["languageId"] == language.id
        assert category["position"] is not None
        assert len(category["name"]) > 0


def test_create_language_success(client, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name=ModuleName.LANGUAGES, user_id=user.id)

    payload = {
        "name": "qwertyu"
    }

    response = client.post("/languages/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["authorId"] == user.id
    assert data["name"] == payload["name"]
    assert data["createdAt"] is not None
    assert data["isPrivate"] == True


def test_create_language_validation_error(client):
    payload = {
        "name": "qwertyu"*255
    }

    response = client.post("/languages/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_language_unauthorized_error(client):
    payload = {
        "name": "qwertyu"
    }

    response = client.post("/languages/", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == ErrorCode.UNAUTHORIZED


def test_change_language_full_success(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name=ModuleName.LANGUAGES, user_id=user.id)

    payload = {
        "name": "New language name",
        "isPrivate": False
    }

    response = client.patch(f"/languages/{language.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["is_private"] == payload["isPrivate"]
