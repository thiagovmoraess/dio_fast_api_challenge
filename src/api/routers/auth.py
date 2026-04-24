from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user
from src.core.database import get_db_session
from src.models.user import User
from src.schemas.auth import LoginIn, TokenOut
from src.schemas.user import UserCreateOut
from src.services.auth_service import AuthService, InvalidCredentialsException

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut, status_code=status.HTTP_200_OK)
async def login(
    login_in: LoginIn,
    session: AsyncSession = Depends(get_db_session),
):
    auth_service = AuthService(session)

    try:
        return await auth_service.login(login_in)
    except InvalidCredentialsException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.get("/me", response_model=UserCreateOut, status_code=status.HTTP_200_OK)
async def read_me(current_user: User = Depends(get_current_user)) -> UserCreateOut:
    return current_user
