# routers/observability.py
from fastapi import APIRouter
from main import REQUEST_COUNT

router = APIRouter(tags=["Observability"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/metrics")
def metrics():
    return {"requests_total": REQUEST_COUNT}