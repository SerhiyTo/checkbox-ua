import uvicorn
from fastapi import FastAPI

from src.__version__ import __version__
from src.config import Settings

settings = Settings()
app = FastAPI(
    title="Evento API",
    description="API for Evento",
    version=__version__,
)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
