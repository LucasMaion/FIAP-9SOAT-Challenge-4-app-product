from fastapi import APIRouter, HTTPException
from loguru import logger
from builder import build_db, seed_db

router = APIRouter(
    prefix="/maintenance",
    tags=["maintenance"],
)


@router.post("/build_db", include_in_schema=False)
async def build_db_api() -> bool:
    try:
        build_db()
        return True
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/seed_db", include_in_schema=False)
async def seed_db_api() -> bool:
    try:
        seed_db()
        return True
    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
