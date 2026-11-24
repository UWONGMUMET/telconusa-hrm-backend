from typing import Literal
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health", summary="Check API status")
def check_health() -> dict[str, Literal["ok"]]:
    return {"status": "ok"}