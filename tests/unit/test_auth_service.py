import pytest

from src.schemas.auth import LoginIn
from src.schemas.user import UserCreateIn
from src.services.auth_service import AuthService, InvalidCredentialsException
from src.services.user_service import UserService


@pytest.mark.asyncio
async def test_login_with_username_success(db_session):
    user_service = UserService(db_session)
    auth_service = AuthService(db_session)

    await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    result = await auth_service.login(
        LoginIn(
            login="thiago",
            password="123456",
        )
    )

    assert result.access_token is not None
    assert isinstance(result.access_token, str)
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_login_with_email_success(db_session):
    user_service = UserService(db_session)
    auth_service = AuthService(db_session)

    await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    result = await auth_service.login(
        LoginIn(
            login="thiago@example.com",
            password="123456",
        )
    )

    assert result.access_token is not None
    assert isinstance(result.access_token, str)
    assert result.token_type == "bearer"


@pytest.mark.asyncio
async def test_login_fails_when_user_does_not_exist(db_session):
    auth_service = AuthService(db_session)

    with pytest.raises(InvalidCredentialsException) as exc:
        await auth_service.login(
            LoginIn(
                login="inexistente",
                password="123456",
            )
        )

    assert str(exc.value) == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_fails_when_password_is_invalid(db_session):
    user_service = UserService(db_session)
    auth_service = AuthService(db_session)

    await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    with pytest.raises(InvalidCredentialsException) as exc:
        await auth_service.login(
            LoginIn(
                login="thiago",
                password="senha-errada",
            )
        )

    assert str(exc.value) == "Invalid username or password"
