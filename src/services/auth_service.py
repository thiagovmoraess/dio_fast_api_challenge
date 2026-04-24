from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import create_access_token, verify_password
from src.models.user import User
from src.schemas.auth import LoginIn, TokenOut


class InvalidCredentialsException(Exception):
    pass


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, login_in: LoginIn) -> TokenOut:
        login = login_in.login.strip().lower()

        query = select(User).where(or_(User.username == login, User.email == login))
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not verify_password(login_in.password, user.password):
            raise InvalidCredentialsException("Invalid username or password")

        access_token = create_access_token(subject=user.username)

        return TokenOut(access_token=access_token, token_type="bearer")
