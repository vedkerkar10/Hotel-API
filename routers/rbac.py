# routers/rbac.py
from fastapi import Depends, HTTPException, APIRouter
from routers.auth import get_current_user

router = APIRouter(tags=["RBAC"])

def staff_required(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "staff":
        raise HTTPException(status_code=403, detail="staff role required")
    return current_user