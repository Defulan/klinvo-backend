from app.enums import ErrorCode


def test_get_languages_success(client, create_random_user, create_random_language):
    author_id = create_random_user().id
    languages = [create_random_language(author_id=author_id) for _ in range(3)]

    response = client.get("/languages/")
    assert response.status_code == 200

    data = response.json()
    for index, language in enumerate(languages):
        response_language = data[index]

        assert response_language["id"] == language.id
        assert response_language["authorId"] == language.author.id
        assert response_language["name"] == language.name
        assert response_language["createdAt"] is not None


def test_get_language_success(client, create_random_user, create_random_language):
    user = create_random_user()
    language = create_random_language(author_id=user.id)

    response = client.get(f"/languages/{language.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == language.id
    assert data["authorId"] == language.author.id == user.id
    assert data["name"] == language.name
    assert data["createdAt"] is not None


def test_get_language_not_found_error(client):
    response = client.get(f"/languages/8721321")
    assert response.status_code == 404
    assert response.json()["detail"] == ErrorCode.LANGUAGE_DOESNT_EXIST


def test_create_language_success(client, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id("languages", user.id)

    payload = {
        "name": "qwertyu"
    }

    response = client.post("/languages/", json=payload)
    assert response.status_code == 201

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
    assert response.status_code == 422


def test_create_language_unauthorized_error(client):
    payload = {
        "name": "qwertyu"
    }

    response = client.post("/languages/", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == ErrorCode.UNAUTHORIZED


def test_change_language_full_success(client, create_random_user, create_random_language, create_session_id):
    user = create_random_user()
    language = create_random_language(author_id=user.id)
    create_session_id(module_name="languages", user_id=user.id)

    payload = {
        "name": "New language name",
        "isPrivate": False
    }

    response = client.patch(f"/languages/{language.id}", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["is_private"] == payload["isPrivate"]
