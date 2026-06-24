from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.database import sessionDep

router = APIRouter(tags=["meta"])


@router.get("/health")
async def healthcheck(session: sessionDep):
    try:
        result = await session.execute(text("SELECT 1"))
        return {"status": "healthy", "db_result": result.scalar()}
    except Exception:
        return JSONResponse(
            {"status": "unhealthy"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
