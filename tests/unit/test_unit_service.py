import pytest

from src.schemas.user import UserCreateIn
from src.services.user_service import UserAlreadyExistsError, UserService


@pytest.mark.asyncio
async def test_create_user_success(db_session):
    service = UserService(db_session)

    user = await service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    assert user.id is not None
    assert user.username == "thiago"
    assert user.email == "thiago@example.com"
    assert user.password != "123456"
    assert user.created_at is not None


@pytest.mark.asyncio
async def test_create_user_duplicate_username(db_session):
    service = UserService(db_session)

    await service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago1@example.com",
            password="123456",
        )
    )

    with pytest.raises(UserAlreadyExistsError) as exc:
        await service.create_user(
            UserCreateIn(
                username="thiago",
                email="thiago2@example.com",
                password="123456",
            )
        )

    assert str(exc.value) == "A user with the same username or email already exists."


@pytest.mark.asyncio
async def test_create_user_duplicate_email(db_session):
    service = UserService(db_session)

    await service.create_user(
        UserCreateIn(
            username="thiago1",
            email="thiago@example.com",
            password="123456",
        )
    )

    with pytest.raises(UserAlreadyExistsError) as exc:
        await service.create_user(
            UserCreateIn(
                username="thiago2",
                email="thiago@example.com",
                password="123456",
            )
        )

    assert str(exc.value) == "A user with the same username or email already exists."


@pytest.mark.asyncio
async def test_create_user_normalizes_fields(db_session):
    service = UserService(db_session)

    user = await service.create_user(
        UserCreateIn(
            username="  thiago  ",
            email="THIAGO@EXAMPLE.COM",
            password="123456",
        )
    )

    assert user.username == "thiago"
    assert user.email == "thiago@example.com"
