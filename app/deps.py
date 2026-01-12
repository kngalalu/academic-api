from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session
from app.database import get_session
from app.models import User
from app.security import SECRET_KEY, ALGORITHM

# FastAPI will use this to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/access-token")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    # If anything goes wrong while decoding the token,
    # we treat it as an authentication failure
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Load the user from the database
    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user
