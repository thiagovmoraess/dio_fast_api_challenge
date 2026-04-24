from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash
from src.models.account import Account
from src.models.user import User
from src.schemas.user import UserCreateIn


class UserAlreadyExistsError(Exception):
    pass


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_in: UserCreateIn) -> User:
        normalized_username = user_in.username.strip()
        normalized_email = user_in.email.strip().lower()

        result = await self.session.execute(
            select(User).where(
                or_(
                    User.username == normalized_username,
                    User.email == normalized_email,
                )
            )
        )
        existing_user = result.scalar_one_or_none()

        if existing_user is not None:
            raise UserAlreadyExistsError(
                "A user with the same username or email already exists."
            )

        user = User(
            username=normalized_username,
            email=normalized_email,
            password=get_password_hash(user_in.password),
        )

        self.session.add(user)
        await self.session.flush()

        account = Account(
            user_id=user.id,
            balance=0,
        )
        self.session.add(account)

        await self.session.commit()
        await self.session.refresh(user)

        return user
