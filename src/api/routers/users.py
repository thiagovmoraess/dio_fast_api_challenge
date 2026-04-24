from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.schemas.user import UserCreateIn, UserCreateOut
from src.services.user_service import UserAlreadyExistsError, UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserCreateOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreateIn,
    session: AsyncSession = Depends(get_db_session),
) -> UserCreateOut:
    user_service = UserService(session)
    try:
        user = await user_service.create_user(user_in)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e

    return UserCreateOut.model_validate(user)
