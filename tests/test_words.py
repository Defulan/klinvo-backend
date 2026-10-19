from fastapi import status
from enums import ModuleName
from app.position import new_last_position
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
    assert data["position"] == new_last_position(None)
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
    assert data["position"] == new_last_position(None)
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
    assert data["position"] == new_last_position(None)
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
    assert data["position"] == new_last_position(None)
    assert data["value"] == payload["value"]
    assert data["meaning"] == payload["meaning"]

