from fastapi import status
from enums import ModuleName
from app import position
from app.enums import ErrorCode

# GET /words/<word_id> - success
def test_get_word_private_success(client, create_random_user, create_random_language, create_random_word, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    word = create_random_word(language_id=language.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=user.id)

    response = client.get(f"/words/{word.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is True
    
    data = response.json()
    assert data["id"] == word.id
    assert data["languageId"] == word.language_id
    assert data["categoryId"] is None
    assert data["position"] == position.get_none_position()
    assert data["value"] == word.value
    assert data["meaning"] == word.meaning


def test_get_word_public_success(client, create_random_user, create_random_language, create_random_word):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)
    word = create_random_word(language_id=language.id)

    response = client.get(f"/words/{word.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is False
    
    data = response.json()
    assert data["id"] == word.id
    assert data["languageId"] == word.language_id
    assert data["categoryId"] is None
    assert data["position"] == position.get_none_position()
    assert data["value"] == word.value
    assert data["meaning"] == word.meaning


def test_get_word_after_multiple_public_success(client, create_random_user, create_random_language, create_random_word):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)
    for _ in range(5):
        create_random_word(language_id=language.id)
    word = create_random_word(language_id=language.id)

    response = client.get(f"/words/{word.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is False
    
    data = response.json()
    assert data["id"] == word.id
    assert data["languageId"] == word.language_id
    assert data["categoryId"] is None
    assert data["position"] == word.position
    assert data["value"] == word.value
    assert data["meaning"] == word.meaning


# GET /words/<word_id> - error
def test_get_word_not_found_error(client):
    response = client.get("/words/842661")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.WORD_DOESNT_EXIST


def test_get_word_private_error(client, create_random_user, create_random_language, create_random_word):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    word = create_random_word(language_id=language.id)

    response = client.get(f"/words/{word.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert language.is_private is True
    assert response.json()["detail"] == ErrorCode.WORD_DOESNT_EXIST


# POST /words/<language_id> - success
def test_create_word_no_category_success(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=user.id)

    payload = {
        "value": "nggyu",
        "meaning": "nglyd"
    }

    response = client.post(f"/words/{language.id}", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["id"] is not None
    assert data["languageId"] == language.id
    assert data["categoryId"] is None
    assert data["position"] == position.get_none_position()
    assert data["value"] == payload["value"]
    assert data["meaning"] == payload["meaning"]


def test_create_word_with_category_success(client, create_random_user, create_random_language, create_random_category, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    category = create_random_category(language_id=language.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=user.id)

    payload = {
        "value": "nggyu",
        "meaning": "nglyd",
        "categoryId": category.id
    }

    response = client.post(f"/words/{language.id}", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["id"] is not None
    assert data["languageId"] == language.id
    assert data["categoryId"] == category.id
    assert data["position"] == position.get_none_position()
    assert data["value"] == payload["value"]
    assert data["meaning"] == payload["meaning"]


# POST /words/<language_id> - error
def test_create_word_unauthorized_error(client):
    payload = {
        "value": "nggyu",
        "meaning": "nglyd"
    }

    response = client.post("/words/62234", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == ErrorCode.UNAUTHORIZED


def test_create_word_no_language_error(client, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name=ModuleName.WORDS, user_id=user.id)

    payload = {
        "value": "nggyu",
        "meaning": "nglyd"
    }

    response = client.post("/words/72117", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_create_word_no_user_error(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=12456789)

    payload = {
        "value": "nggyu",
        "meaning": "nglyd"
    }

    response = client.post(f"/words/{language.id}", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.USER_DOESNT_EXIST


def test_create_word_invalid_payload_error(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=user.id)

    payload = {
        "value": "nggyu",
        "meaning": None
    }

    response = client.post(f"/words/{language.id}", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_word_non_author_private_error(client, create_random_user, create_random_language, create_session_id):
    author_user = create_random_user()
    side_user = create_random_user()
    language = create_random_language(author_id=author_user.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=side_user.id)

    payload = {
        "value": "nggyu",
        "meaning": "nglyd"
    }

    response = client.post(f"/words/{language.id}", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_create_word_non_author_public_error(client, create_random_user, create_random_language, create_session_id):
    author_user = create_random_user()
    side_user = create_random_user()
    language = create_random_language(author_id=author_user.id, is_private=False)
    create_session_id(module_name=ModuleName.WORDS, user_id=side_user.id)

    payload = {
        "value": "nggyu",
        "meaning": "nglyd"
    }

    response = client.post(f"/words/{language.id}", json=payload)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == ErrorCode.NO_PERMISSIONS


# PATCH /words/<word_id> - success
def test_change_word_full_success(client, create_random_user, create_random_language, create_random_word, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    word = create_random_word(language_id=language.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=user.id)

    old_value = word.value
    old_meaning = word.meaning

    payload = {
        "value": "wertykfywquvbnm,.rtyuioxcvbnm,rtyuhjk",
        "meaning": "Author playing on piano with keyboard, don't pay attention"
    }

    response = client.patch(f"/words/{word.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == word.id
    assert data["languageId"] == language.id
    assert data["categoryId"] == word.category_id
    assert data["position"] == position.get_none_position()
    assert data["value"] == payload["value"]
    assert data["value"] != old_value
    assert data["meaning"] == payload["meaning"]
    assert data["meaning"] != old_meaning


def test_change_word_partial_success(client, create_random_user, create_random_language, create_random_word, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    word = create_random_word(language_id=language.id)
    create_session_id(module_name=ModuleName.WORDS, user_id=user.id)

    old_value = word.value
    old_meaning = word.meaning

    payload = {
        "meaning": "I've changed my mind now it means different"
    }

    response = client.patch(f"/words/{word.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == word.id
    assert data["languageId"] == language.id
    assert data["categoryId"] == word.category_id
    assert data["position"] == position.get_none_position()
    assert data["value"] == old_value
    assert data["meaning"] == payload["meaning"]
    assert data["meaning"] != old_meaning
