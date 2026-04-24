import pytest

from src.schemas.user import UserCreateIn
from src.services.account_service import AccountNotFoundError, AccountService
from src.services.user_service import UserService


@pytest.mark.asyncio
async def test_get_account_by_user_id_returns_account(db_session):
    user_service = UserService(db_session)
    created_user = await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    service = AccountService(db_session)
    account = await service.get_account_by_user_id(created_user.id)

    assert account is not None
    assert account.user_id == created_user.id
    assert float(account.balance) == 0.0


@pytest.mark.asyncio
async def test_get_account_by_user_id_raises_when_not_found(db_session):
    service = AccountService(db_session)

    with pytest.raises(AccountNotFoundError):
        await service.get_account_by_user_id(9999)
