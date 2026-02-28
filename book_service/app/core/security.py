from jose import jwt, JWTError
from app.core.config import settings

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        user_role: str = payload.get("role")
        
        if user_id is None or user_role is None:
            return None
            
        return {"id": user_id, "role": user_role}
    except JWTError:
        return None