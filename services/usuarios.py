from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.usuarios import UserDB
from schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse, RolUsuario
from passlib.context import CryptContext
from typing import List, Optional

# Configuración para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_id(db: Session, user_id: int) -> Optional[UserDB]:
    """Obtiene un usuario por su ID"""
    return db.query(UserDB).filter(UserDB.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[UserDB]:
    """Obtiene un usuario por su email"""
    return db.query(UserDB).filter(UserDB.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserDB]:
    """Obtiene una lista de usuarios con paginación"""
    return db.query(UserDB).offset(skip).limit(limit).all()

def create_user(db: Session, user: UsuarioCreate) -> UserDB:
    """Crea un nuevo usuario"""
    # Verificar si el email ya existe
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear hash de la contraseña
    hashed_password = get_password_hash(user.password.get_secret_value())
    
    # Crear el usuario en la base de datos
    db_user = UserDB(
        nombre=user.nombre,
        email=user.email,
        passh=hashed_password,
        rol=user.rol.value
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario. Verifique los datos."
        )

def update_user(db: Session, user_id: int, user_update: UsuarioUpdate) -> Optional[UserDB]:
    """Actualiza un usuario existente"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Actualizar campos si están presentes
    update_data = user_update.dict(exclude_unset=True)
    
    # Si se actualiza el email, verificar que no exista
    if "email" in update_data:
        existing_user = get_user_by_email(db, update_data["email"])
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado por otro usuario"
            )
    
    # Si se actualiza la contraseña, hacer hash
    if "password" in update_data:
        update_data["passh"] = get_password_hash(update_data["password"].get_secret_value())
        del update_data["password"]
    
    # Si se actualiza el rol, convertir a string
    if "rol" in update_data:
        update_data["rol"] = update_data["rol"].value
    
    try:
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el usuario. Verifique los datos."
        )

def delete_user(db: Session, user_id: int) -> bool:
    """Elimina un usuario"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    try:
        db.delete(db_user)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el usuario. Puede tener registros asociados."
        )

def authenticate_user(db: Session, email: str, password: str) -> Optional[UserDB]:
    """Autentica un usuario con email y contraseña"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.passh):
        return None
    return user

def get_users_by_role(db: Session, rol: RolUsuario, skip: int = 0, limit: int = 100) -> List[UserDB]:
    """Obtiene usuarios filtrados por rol"""
    return db.query(UserDB).filter(UserDB.rol == rol.value).offset(skip).limit(limit).all()

def count_users(db: Session) -> int:
    """Cuenta el total de usuarios"""
    return db.query(UserDB).count()

def count_users_by_role(db: Session, rol: RolUsuario) -> int:
    """Cuenta usuarios por rol"""
    return db.query(UserDB).filter(UserDB.rol == rol.value).count()
