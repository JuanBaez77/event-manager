from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        try:
            data = validate_token(auth.credentials)
            # Si el token es válido permite el acceso
            return data
        except Exception:
            raise HTTPException(status_code=403, detail="Credenciales son inválidas")