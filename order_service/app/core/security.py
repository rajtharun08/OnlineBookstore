from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user_id is None:
            return None
            
        return {"id": user_id, "role": role, "token": token}
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_data = decode_access_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data

def role_required(required_role: str):
    def role_checker(user_context: dict = Depends(get_current_user)):
        if user_context["role"] != required_role:
            raise HTTPException(
                status_code=403, 
                detail="Operation restricted to Administrators"
            )
        return user_context
    return role_checker