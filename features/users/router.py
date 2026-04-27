from features.core.database import get_db
from features.core.schema import ApiResponse
from features.users.models import User
from features.users.schema import UserResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=ApiResponse[list[UserResponse]])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return ApiResponse.ok(data=users, message="Users fetched successfully")