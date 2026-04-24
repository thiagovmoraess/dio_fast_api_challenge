import pytest


@pytest.mark.asyncio
async def test_deposit_route_success(client):
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

    deposit_response = await client.post(
        "/transactions/deposit",
        json={"amount": "100.00"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert deposit_response.status_code == 201

    data = deposit_response.json()
    assert data["type"] == "deposit"
    assert data["amount"] == "100.00"
    assert "id" in data
    assert "account_id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_withdraw_route_success(client):
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
    headers = {"Authorization": f"Bearer {token}"}

    deposit_response = await client.post(
        "/transactions/deposit",
        json={"amount": "100.00"},
        headers=headers,
    )

    assert deposit_response.status_code == 201

    withdraw_response = await client.post(
        "/transactions/withdraw",
        json={"amount": "40.00"},
        headers=headers,
    )

    assert withdraw_response.status_code == 201

    data = withdraw_response.json()
    assert data["type"] == "withdraw"
    assert data["amount"] == "40.00"
    assert "id" in data
    assert "account_id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_withdraw_route_fails_with_insufficient_balance(client):
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

    withdraw_response = await client.post(
        "/transactions/withdraw",
        json={"amount": "10.00"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert withdraw_response.status_code == 400
    assert withdraw_response.json()["detail"] == "Insufficient balance for withdraw"


@pytest.mark.asyncio
async def test_deposit_route_fails_without_token(client):
    response = await client.post(
        "/transactions/deposit",
        json={"amount": "100.00"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_withdraw_route_fails_without_token(client):
    response = await client.post(
        "/transactions/withdraw",
        json={"amount": "40.00"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_deposit_route_fails_with_invalid_token(client):
    response = await client.post(
        "/transactions/deposit",
        json={"amount": "100.00"},
        headers={"Authorization": "Bearer invalidtoken"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


@pytest.mark.asyncio
async def test_withdraw_route_fails_with_invalid_token(client):
    response = await client.post(
        "/transactions/withdraw",
        json={"amount": "40.00"},
        headers={"Authorization": "Bearer invalidtoken"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


@pytest.mark.asyncio
async def test_list_my_transactions_success(client):
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
    headers = {"Authorization": f"Bearer {token}"}

    deposit_response = await client.post(
        "/transactions/deposit",
        json={"amount": "100.00"},
        headers=headers,
    )
    assert deposit_response.status_code == 201

    withdraw_response = await client.post(
        "/transactions/withdraw",
        json={"amount": "40.00"},
        headers=headers,
    )
    assert withdraw_response.status_code == 201

    statement_response = await client.get(
        "/transactions/me",
        headers=headers,
    )

    assert statement_response.status_code == 200

    data = statement_response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["type"] == "withdraw"
    assert data[0]["amount"] == "40.00"

    assert data[1]["type"] == "deposit"
    assert data[1]["amount"] == "100.00"


@pytest.mark.asyncio
async def test_list_my_transactions_fails_without_token(client):
    response = await client.get("/transactions/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_list_my_transactions_fails_with_invalid_token(client):
    response = await client.get(
        "/transactions/me",
        headers={"Authorization": "Bearer invalidtoken"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
