from decimal import Decimal

import pytest
from sqlalchemy import select

from src.models.account import Account
from src.schemas.user import UserCreateIn
from src.services.transaction_service import (
    AccountNotFoundError,
    InsufficientBalanceError,
    InvalidTransactionAmountError,
    TransactionService,
)
from src.services.user_service import UserService


@pytest.mark.asyncio
async def test_deposit_updates_balance_and_creates_transaction(db_session):
    user_service = UserService(db_session)
    user = await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    service = TransactionService(db_session)
    transaction = await service.deposit(user.id, Decimal("100.00"))

    assert transaction.id is not None
    assert transaction.account_id is not None
    assert transaction.type == "deposit"
    assert transaction.amount == Decimal("100.00")

    result = await db_session.execute(select(Account).where(Account.user_id == user.id))
    account = result.scalar_one()

    assert account.balance == Decimal("100.00")


@pytest.mark.asyncio
async def test_withdraw_updates_balance_and_creates_transaction(db_session):
    user_service = UserService(db_session)
    user = await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    service = TransactionService(db_session)
    await service.deposit(user.id, Decimal("100.00"))
    transaction = await service.withdraw(user.id, Decimal("40.00"))

    assert transaction.id is not None
    assert transaction.account_id is not None
    assert transaction.type == "withdraw"
    assert transaction.amount == Decimal("40.00")

    result = await db_session.execute(select(Account).where(Account.user_id == user.id))
    account = result.scalar_one()

    assert account.balance == Decimal("60.00")


@pytest.mark.asyncio
async def test_withdraw_raises_when_balance_is_insufficient(db_session):
    user_service = UserService(db_session)
    user = await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    service = TransactionService(db_session)

    with pytest.raises(InsufficientBalanceError):
        await service.withdraw(user.id, Decimal("10.00"))


@pytest.mark.asyncio
async def test_deposit_raises_when_amount_is_invalid(db_session):
    service = TransactionService(db_session)

    with pytest.raises(InvalidTransactionAmountError):
        await service.deposit(user_id=1, amount=Decimal("0.00"))


@pytest.mark.asyncio
async def test_withdraw_raises_when_amount_is_invalid(db_session):
    service = TransactionService(db_session)

    with pytest.raises(InvalidTransactionAmountError):
        await service.withdraw(user_id=1, amount=Decimal("-1.00"))


@pytest.mark.asyncio
async def test_deposit_raises_when_account_is_not_found(db_session):
    service = TransactionService(db_session)

    with pytest.raises(AccountNotFoundError):
        await service.deposit(user_id=9999, amount=Decimal("10.00"))


@pytest.mark.asyncio
async def test_withdraw_raises_when_account_is_not_found(db_session):
    service = TransactionService(db_session)

    with pytest.raises(AccountNotFoundError):
        await service.withdraw(user_id=9999, amount=Decimal("10.00"))


@pytest.mark.asyncio
async def test_list_by_user_id_returns_transactions_in_desc_order(db_session):
    user_service = UserService(db_session)
    user = await user_service.create_user(
        UserCreateIn(
            username="thiago",
            email="thiago@example.com",
            password="123456",
        )
    )

    service = TransactionService(db_session)
    await service.deposit(user.id, Decimal("100.00"))
    await service.withdraw(user.id, Decimal("40.00"))

    transactions = await service.list_by_user_id(user.id)

    assert len(transactions) == 2
    assert transactions[0].type == "withdraw"
    assert transactions[1].type == "deposit"
