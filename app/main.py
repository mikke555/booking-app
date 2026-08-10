import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import __version__
from app.config import configure_logging, settings
from app.exceptions import AppException
from app.routers import master_router

configure_logging(debug=settings.debug)
logger = logging.getLogger(__name__)
logger.info(
    "Starting v%s: db=%s@%s:%s, db_echo=%s, debug=%s",
    __version__,
    settings.postgres_db,
    settings.postgres_host,
    settings.postgres_port,
    settings.db_echo,
    settings.debug,
)

app = FastAPI(
    title="Hotel Booking API",
    version=__version__,
)
app.include_router(master_router)


@app.exception_handler(AppException)
async def app_exception_handler(req: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(req: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", req.method, req.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get(
    "/",
    tags=["Meta"],
    summary="Service info",
    description="Service name, version, and links to docs and healthcheck.",
)
def read_root() -> dict[str, str]:
    return {
        "app": app.title,
        "version": app.version,
        "docs": "/docs",
        "health": "/health",
    }
