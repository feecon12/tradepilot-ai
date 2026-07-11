from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return{
        "application": "TradePilot AI",
        "status": "Running",
    }