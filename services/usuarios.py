from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.usuarios import UserDB
from schemas.usuarios import UsuarioCreate, UsuarioUpdate, UsuarioResponse, RolUsuario
from passlib.context import CryptContext
from typing import List, Optional

# Configuración para hashear contraseñas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Genera el hash de una contraseña en texto plano
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verifica si una contraseña en texto plano coincide con su hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Obtiene un usuario por su ID
def get_user_by_id(db: Session, user_id: int) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.id == user_id).first()

# Obtiene un usuario por su email
def get_user_by_email(db: Session, email: str) -> Optional[UserDB]:
    return db.query(UserDB).filter(UserDB.email == email).first()

# Obtiene una lista de usuarios con paginación
def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserDB]:
    return db.query(UserDB).offset(skip).limit(limit).all()

# Crea un nuevo usuario en la base de datos
def create_user(db: Session, user: UsuarioCreate) -> UserDB:
    # Verifica si el email ya está registrado
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Hashea la contraseña antes de guardarla
    hashed_password = get_password_hash(user.password.get_secret_value())
    
    # Crea el objeto usuario
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

# Actualiza los datos de un usuario existente
def update_user(db: Session, user_id: int, user_update: UsuarioUpdate) -> Optional[UserDB]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Si se actualiza el email, verifica que no esté en uso por otro usuario
    if "email" in update_data:
        existing_user = get_user_by_email(db, update_data["email"])
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado por otro usuario"
            )
    
    # Si se actualiza la contraseña, la hashea
    if "password" in update_data:
        update_data["passh"] = get_password_hash(update_data["password"].get_secret_value())
        del update_data["password"]
    
    # Si se actualiza el rol, lo convierte a string
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

# Elimina un usuario de la base de datos
def delete_user(db: Session, user_id: int) -> bool:
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

# Autentica un usuario verificando su email y contraseña
def authenticate_user(db: Session, email: str, password: str) -> Optional[UserDB]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.passh):
        return None
    return user

# Obtiene usuarios filtrados por rol con paginación
def get_users_by_role(db: Session, rol: RolUsuario, skip: int = 0, limit: int = 100) -> List[UserDB]:
    return db.query(UserDB).filter(UserDB.rol == rol.value).offset(skip).limit(limit).all()

# Cuenta el total de usuarios en la base de datos
def count_users(db: Session) -> int:
    return db.query(UserDB).count()

# Cuenta la cantidad de usuarios por rol
def count_users_by_role(db: Session, rol: RolUsuario) -> int:
    return db.query(UserDB).filter(UserDB.rol == rol.value).count()
