import pytest


@pytest.mark.asyncio
async def test_create_user_route_success(client):
    response = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago@example.com",
            "password": "123456",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["username"] == "thiago"
    assert data["email"] == "thiago@example.com"
    assert data["created_at"] is not None
    assert "password" not in data


@pytest.mark.asyncio
async def test_create_user_route_duplicate_username(client):
    response_1 = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago1@example.com",
            "password": "123456",
        },
    )

    response_2 = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago2@example.com",
            "password": "123456",
        },
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 409
    assert (
        response_2.json()["detail"]
        == "A user with the same username or email already exists."
    )


@pytest.mark.asyncio
async def test_create_user_route_duplicate_email(client):
    response_1 = await client.post(
        "/users/",
        json={
            "username": "thiago1",
            "email": "thiago@example.com",
            "password": "123456",
        },
    )

    response_2 = await client.post(
        "/users/",
        json={
            "username": "thiago2",
            "email": "thiago@example.com",
            "password": "123456",
        },
    )

    assert response_1.status_code == 201
    assert response_2.status_code == 409
    assert (
        response_2.json()["detail"]
        == "A user with the same username or email already exists."
    )


@pytest.mark.asyncio
async def test_create_user_route_invalid_email(client):
    response = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "email-invalido",
            "password": "123456",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_route_invalid_password(client):
    response = await client.post(
        "/users/",
        json={
            "username": "thiago",
            "email": "thiago@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422
