from fastapi import APIRouter
from .schema import LoginRequest
from .service import login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(data: LoginRequest):
    return login_user(data)