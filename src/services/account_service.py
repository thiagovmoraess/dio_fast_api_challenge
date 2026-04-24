from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.account import Account


class AccountNotFoundError(Exception):
    pass


class AccountService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_account_by_user_id(self, user_id: int) -> Account:
        result = await self.db_session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        account = result.scalar_one_or_none()
        if account is None:
            raise AccountNotFoundError(f"Account with user_id {user_id} not found")
        return account
