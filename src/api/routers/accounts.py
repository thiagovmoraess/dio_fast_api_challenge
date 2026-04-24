from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.core.database import get_db_session
from src.models.user import User
from src.schemas.account import AccountOut
from src.services.account_service import AccountNotFoundError, AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/me", response_model=AccountOut)
async def read_my_account(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> AccountOut:
    service = AccountService(session)

    try:
        account = await service.get_account_by_user_id(current_user.id)
    except AccountNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found.",
        )

    return account
