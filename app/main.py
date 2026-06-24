from fastapi import FastAPI
from app.routers import master_router

app = FastAPI()
app.include_router(master_router)
