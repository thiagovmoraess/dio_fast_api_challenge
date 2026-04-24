from fastapi import FastAPI

from src.api.routers.users import router as users_router
from src.api.routers.auth import router as auth_router
from src.api.routers.accounts import router as accounts_router
from src.api.routers.transactions import router as transactions_router
from src.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(transactions_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}
