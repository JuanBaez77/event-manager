from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse, RolUsuario
from services import usuarios as service
#from middlewares.jwt_bearer import JWTBearer

router = APIRouter(
    prefix="/usuarios", 
    tags=["usuarios"],
    #dependencies=[Depends(JWTBearer())]
)

@router.get("", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
async def listar_usuarios(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    """Obtiene una lista paginada de usuarios"""
    return service.get_users(db, skip=skip, limit=limit)

@router.get("/buscar", response_model=List[UsuarioResponse], status_code=status.HTTP_200_OK)
async def buscar_usuarios_por_email(
    email: str = Query(..., description="Email del usuario a buscar"),
    db: Session = Depends(get_db)
):
    """Busca usuarios por email"""
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
    """Obtiene usuarios filtrados por rol"""
    return service.get_users_by_role(db, rol, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
async def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario específico por su ID"""
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return user

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario"""
    return service.create_user(db, usuario)

@router.put("/{user_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
async def actualizar_usuario(
    user_id: int, 
    usuario: UsuarioUpdate, 
    db: Session = Depends(get_db)
):
    """Actualiza un usuario existente"""
    return service.update_user(db, user_id, usuario)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario"""
    service.delete_user(db, user_id)
    return None

@router.get("/stats/count", status_code=status.HTTP_200_OK)
async def contar_usuarios(db: Session = Depends(get_db)):
    """Obtiene estadísticas de usuarios"""
    total = service.count_users(db)
    administradores = service.count_users_by_role(db, RolUsuario.ADMINISTRADOR)
    clientes = service.count_users_by_role(db, RolUsuario.CLIENTE)
    
    return {
        "total": total,
        "administradores": administradores,
        "clientes": clientes
    }

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_usuario(
    email: str = Query(..., description="Email del usuario"),
    password: str = Query(..., description="Contraseña del usuario"),
    db: Session = Depends(get_db)
):
    """Autentica un usuario con email y contraseña"""
    user = service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    return {
        "message": "Login exitoso",
        "user": {
            "id": user.id,
            "nombre": user.nombre,
            "email": user.email,
            "rol": user.rol
        }
    }
