from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse, RolUsuario
from services import usuarios as service
from middlewares.jwt_bearer import JWTBearer

router = APIRouter(
    prefix="/usuarios", 
    tags=["usuarios"],
    dependencies=[Depends(JWTBearer())]
)

@router.get("", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
async def listar_usuarios(
    db: Session = Depends(get_db)
):

    return service.get_users(db)

@router.get("/buscar", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
async def buscar_usuarios_por_email(
    email: str = Query(..., description="Email del usuario a buscar"),
    db: Session = Depends(get_db)
):
    user = service.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return [user]

@router.get("/rol/{rol}", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
async def listar_usuarios_por_rol(
    rol: RolUsuario,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    
    return service.get_users_by_role(db, rol, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
async def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return user

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, dependencies=[])
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return service.create_user(db, usuario)

@router.put("/{user_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
async def actualizar_usuario(
    user_id: int, 
    usuario: UsuarioUpdate, 
    db: Session = Depends(get_db)
):
    return service.update_user(db, user_id, usuario)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    service.delete_user(db, user_id)
    return None

@router.get("/stats/count", status_code=status.HTTP_200_OK)
async def contar_usuarios(db: Session = Depends(get_db)):
    total = service.count_users(db)
    administradores = service.count_users_by_role(db, RolUsuario.ADMINISTRADOR)
    clientes = service.count_users_by_role(db, RolUsuario.CLIENTE)
    
    return {
        "total": total,
        "administradores": administradores,
        "clientes": clientes
    }