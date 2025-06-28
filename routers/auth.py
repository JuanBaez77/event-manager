from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.usuarios import UsuarioResponse, LoginRequest
from services.usuarios import authenticate_user
from utils.jwt_manager import create_token
from config.database import get_db

router = APIRouter()

@router.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    email = data.email
    password = data.password
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_token({"email": user.email, "id": user.id, "rol": user.rol})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "rol": user.rol
        }
    }

@router.post("/auth/logout")
def logout():
    return {"message": "Logout exitoso. Elimina el token en el cliente."} 