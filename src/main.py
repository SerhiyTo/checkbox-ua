import uvicorn
from fastapi import FastAPI

from src.__version__ import __version__
from src.auth.router import router as auth_router
from src.checks.router import router as checks_router
from src.config import settings

app = FastAPI(
    title="Checkbox API",
    description="API for Checkbox Test Task",
    version=__version__,
)
app.include_router(auth_router)
app.include_router(checks_router)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
