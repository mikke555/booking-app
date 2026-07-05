from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppException
from app.routers import master_router

app = FastAPI()
app.include_router(master_router)


@app.exception_handler(AppException)
async def app_exception_handler(req: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail}, headers=exc.headers
    )
