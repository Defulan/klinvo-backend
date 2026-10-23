from fastapi import status
from enums import ModuleName
from app import position
from app.enums import ErrorCode


# GET /categories/<category_id>
def test_get_category_private_success(client, create_random_user, create_random_language, create_random_category, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    category = create_random_category(language_id=language.id)
    create_session_id(module_name=ModuleName.CATEGORY, user_id=user.id)

    response = client.get(f"/categories/{category.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is True
    
    data = response.json()
    assert data["id"] == category.id
    assert data["languageId"] == category.language_id
    assert data["position"] == position.get_none_position()
    assert data["name"] == category.name


def test_get_category_public_success(client, create_random_user, create_random_language, create_random_category):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)
    category = create_random_category(language_id=language.id)

    response = client.get(f"/categories/{category.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is False
    
    data = response.json()
    assert data["id"] == category.id
    assert data["languageId"] == category.language_id
    assert data["position"] == position.get_none_position()
    assert data["name"] == category.name


def test_get_category_after_multiple_public_success(client, create_random_user, create_random_language, create_random_category):
    user = create_random_user()
    language = create_random_language(author_id=user.id, is_private=False)
    for _ in range(5):
        create_random_category(language_id=language.id)
    category = create_random_category(language_id=language.id)

    response = client.get(f"/categories/{category.id}")
    assert response.status_code == status.HTTP_200_OK
    assert language.is_private is False
    
    data = response.json()
    assert data["id"] == category.id
    assert data["languageId"] == category.language_id
    assert data["position"] == category.position
    assert data["name"] == category.name


# GET /categories/<category_id>
def test_create_category_not_found_error(client):
    response = client.get("/categories/9281")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.CATEGORY_DOESNT_EXIST


def test_get_category_private_error(client, create_random_user, create_random_language, create_random_category):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    category = create_random_category(language_id=language.id)

    response = client.get(f"/categories/{category.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == ErrorCode.CATEGORY_DOESNT_EXIST
