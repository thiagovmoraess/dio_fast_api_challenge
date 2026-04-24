from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.core.database import get_db_session
from src.models.user import User
from src.schemas.transaction import DepositIn, TransactionOut, WithdrawIn
from src.services.transaction_service import (
    AccountNotFoundError,
    InsufficientBalanceError,
    InvalidTransactionAmountError,
    TransactionService,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "/deposit", response_model=TransactionOut, status_code=status.HTTP_201_CREATED
)
async def create_deposit(
    payload: DepositIn,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> TransactionOut:
    service = TransactionService(session)

    try:
        transaction = await service.deposit(current_user.id, payload.amount)
    except AccountNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )
    except InvalidTransactionAmountError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return transaction


@router.post(
    "/withdraw", response_model=TransactionOut, status_code=status.HTTP_201_CREATED
)
async def create_withdraw(
    payload: WithdrawIn,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> TransactionOut:
    service = TransactionService(session)

    try:
        transaction = await service.withdraw(current_user.id, payload.amount)
    except AccountNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )
    except InvalidTransactionAmountError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except InsufficientBalanceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return transaction


@router.get("/me", response_model=list[TransactionOut])
async def list_my_transactions(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[TransactionOut]:
    service = TransactionService(session)

    try:
        transactions = await service.get_transactions_by_user_id(current_user.id)
    except AccountNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )

    return transactions
