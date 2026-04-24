from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.account import Account
from src.models.transaction import Transaction


class AccountNotFoundError(Exception):
    pass


class InvalidTransactionAmountError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass


class TransactionService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _get_account_by_user_id(self, user_id: int) -> Account:
        result = await self.db_session.execute(
            select(Account).where(Account.user_id == user_id)
        )
        account = result.scalars().one_or_none()

        if account is None:
            raise AccountNotFoundError(f"Account for user_id {user_id} not found")

        return account

    async def deposit(self, user_id: int, amount: Decimal) -> Transaction:
        if amount <= 0:
            raise InvalidTransactionAmountError(
                "Deposit amount must be greater than zero"
            )

        account = await self._get_account_by_user_id(user_id)

        transaction = Transaction(account_id=account.id, type="deposit", amount=amount)
        account.balance += amount

        self.db_session.add(transaction)
        await self.db_session.commit()
        await self.db_session.refresh(transaction)

        return transaction

    async def withdraw(self, user_id: int, amount: Decimal) -> Transaction:
        if amount <= 0:
            raise InvalidTransactionAmountError(
                "withdraw amount must be greater than zero"
            )

        account = await self._get_account_by_user_id(user_id)

        if account.balance < amount:
            raise InsufficientBalanceError("Insufficient balance for withdraw")

        transaction = Transaction(account_id=account.id, type="withdraw", amount=amount)
        account.balance -= amount
        self.db_session.add(transaction)
        await self.db_session.commit()
        await self.db_session.refresh(transaction)

        return transaction

    async def get_transactions_by_user_id(self, user_id: int) -> list[Transaction]:
        account = await self._get_account_by_user_id(user_id)

        result = await self.db_session.execute(
            select(Transaction)
            .where(Transaction.account_id == account.id)
            .order_by(Transaction.created_at.desc(), Transaction.id.desc())
        )
        transactions = result.scalars().all()

        return transactions
