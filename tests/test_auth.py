from app.enums import CookieKey, ErrorCode

def test_get_auth_cookie_authorized(client, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name="auth", user_id=user.id)

    response = client.get("auth/me")
    assert response.status_code == 200
    
    data = response.json()
    assert data["userId"] == user.id
    assert data["isAuth"] == True


def test_get_auth_cookie_unauthorized(client):
    response = client.get("auth/me")
    assert response.status_code == 200
    
    data = response.json()
    assert data["userId"] == None
    assert data["isAuth"] == False


def test_login_success(client, create_random_user):
    password = "192"
    user = create_random_user(password=password)

    payload = {
        "id": user.id,
        "password": password
    }

    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert CookieKey.SESSION_ID in response.cookies


def test_login_wrong_login_error(client, create_random_user):
    password = "192"
    user = create_random_user(password=password)

    payload = {
        "id": user.id,
        "password": password*3
    }

    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == ErrorCode.WRONG_LOGIN_DATA


def test_login_authorized_error(client, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name="auth", user_id=user.id)

    payload = {
        "id": 99992221,
        "password": "asadsdasdas"
    }

    response = client.post("/auth/login", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == ErrorCode.AUTHORIZED


def test_logout_success(client, create_random_user, create_session_id):
    user = create_random_user()
    create_session_id(module_name="auth", user_id=user.id)

    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert CookieKey.SESSION_ID not in response.cookies 


def test_logout_unauthorized_error(client):
    response = client.post("/auth/logout")
    assert response.status_code == 401
    assert response.json()["detail"] == ErrorCode.UNAUTHORIZED


def test_logout_not_exist_error(client, create_session_id):
    create_session_id(module_name="auth", user_id=9218374)

    response = client.post("/auth/logout")
    assert response.status_code == 401
    assert response.json()["detail"] == ErrorCode.USER_DOESNT_EXIST
