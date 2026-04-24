from sqlalchemy import select

from src.models.account import Account
from src.schemas.user import UserCreateIn
from src.services.user_service import UserService


async def test_create_user_creates_account(db_session):
    service = UserService(db_session)

    user = await service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    result = await db_session.execute(select(Account).where(Account.user_id == user.id))
    account = result.scalar_one_or_none()

    assert account is not None
    assert account.user_id == user.id
    assert float(account.balance) == 0.0
