from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import __version__
from app.exceptions import AppException
from app.routers import master_router

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
