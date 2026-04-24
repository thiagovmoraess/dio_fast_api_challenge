import pytest


@pytest.mark.asyncio
async def test_read_my_account_success(client):
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

    account_response = await client.get(
        "/accounts/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert account_response.status_code == 200

    data = account_response.json()
    assert data["user_id"] == create_response.json()["id"]
    assert data["balance"] == "0.00"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_read_my_account_without_token_returns_401(client):
    response = await client.get("/accounts/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_read_my_account_with_invalid_token_returns_401(client):
    response = await client.get(
        "/accounts/me",
        headers={"Authorization": "Bearer invalidtoken"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
