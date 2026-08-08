from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.dependencies import DBDep

router = APIRouter(tags=["Meta"])


@router.get(
    "/health",
    description="Check service status and database connectivity. Returns 503 if the database is unreachable.",
)
async def healthcheck(db: DBDep):
    try:
        await db.session.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception:
        return JSONResponse(
            {"status": "unhealthy"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
