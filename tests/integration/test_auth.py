import pytest


@pytest.mark.asyncio
async def test_login_route_with_username_success(client):
    create_response = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago@example.com",
            "password": "123456",
        },
    )

    assert create_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        json={
            "login": "thiago",
            "password": "123456",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["access_token"] != ""
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_route_with_email_success(client):
    create_response = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago@example.com",
            "password": "123456",
        },
    )

    assert create_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        json={
            "login": "thiago@example.com",
            "password": "123456",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_route_fails_with_invalid_password(client):
    create_response = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago@example.com",
            "password": "123456",
        },
    )

    assert create_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        json={
            "login": "thiago",
            "password": "senha-errada",
        },
    )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_route_fails_with_nonexistent_user(client):
    login_response = await client.post(
        "/auth/login",
        json={
            "login": "inexistente",
            "password": "123456",
        },
    )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_route_fails_with_invalid_payload(client):
    login_response = await client.post(
        "/auth/login",
        json={
            "login": "thiago",
            "password": "123",
        },
    )

    assert login_response.status_code == 422


@pytest.mark.asyncio
async def test_get_me_success(client):
    create_response = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago@example.com",
            "password": "123456",
        },
    )
    assert create_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        json={
            "login": "thiago",
            "password": "123456",
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200

    data = me_response.json()
    assert "id" in data
    assert data["username"] == "thiago"
    assert data["email"] == "thiago@example.com"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_me_without_token(client):
    me_response = await client.get("/auth/me")
    assert me_response.status_code == 401
    assert me_response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_me_with_invalid_token(client):
    me_response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert me_response.status_code == 401
    assert me_response.json()["detail"] == "Could not validate credentials"
