from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import User
from app.crud import create_user, get_users
from app.deps import get_session, get_current_user
from app.security import get_password_hash
from app.schemas import UserCreate, UserRead
from pydantic import BaseModel

router = APIRouter()

class PasswordUpdate(BaseModel):
    password: str

@router.patch("/me/password", tags=["users"])
def update_my_password(
    password_update: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update the password for the current logged-in user.
    """
    user = session.exec(select(User).where(User.id == current_user.id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(password_update.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"msg": "Password updated successfully"}

@router.get("/me", response_model=UserRead, tags=["users"])
def read_own_user_me(current_user: User = Depends(get_current_user)):
    """
    Get info about the current logged-in user.
    """
    return current_user

@router.post("/users", response_model=UserRead)
def create_user_endpoint(user: UserCreate, session: Session = Depends(get_session)):
    return create_user(session, user.email, user.password)

@router.get("/users", response_model=list[UserRead])
def get_users_endpoint(session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    return get_users(session)
