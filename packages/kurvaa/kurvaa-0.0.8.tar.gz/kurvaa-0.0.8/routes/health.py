from fastapi import APIRouter

router = APIRouter()


@router.get("/liveness")
def get_health_check():
    return {"status": "Ping OK"}


@router.get("/readiness")
def get_readiness_check():
    return {"status": "Ping OK"}


@router.get("/summary")
async def get_summary_check():
    return {"status": "Health check success"}
