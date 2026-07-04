from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import ObjectNotFound
from app.routers import master_router

app = FastAPI()
app.include_router(master_router)


@app.exception_handler(ObjectNotFound)
async def not_found_exception_handler(req: Request, exc: ObjectNotFound):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
