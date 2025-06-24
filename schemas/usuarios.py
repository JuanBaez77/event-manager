from pydantic import BaseModel, Field, EmailStr, SecretStr
from enum import Enum
from typing import Optional

# Enum para definir los roles de los Users
class RolUsuario(str, Enum):
    ADMINISTRADOR = "Administrador"
    CLIENTE = "Cliente"

# Tabla de el usuario Base
class UsuarioBase(BaseModel):
    nombre: str = Field(
        ..., 
        min_length=2, 
        max_length=50,
        description="Nombre completo del usuario"
    )
    email: EmailStr = Field(
        ..., 
        description="Email válido del usuario"
    )
    password: SecretStr = Field(
        ..., 
        min_length=8,
        description="Contraseña del usuario"
    )
    rol: RolUsuario = Field(
        default=RolUsuario.CLIENTE,
        description="Rol del usuario: Administrador o Cliente"
    )

# Tabla con el pass para crear un nuevo usuario
class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(
        None, 
        min_length=2, 
        max_length=50,
        description="Nombre completo del usuario"
    )
    email: Optional[EmailStr] = Field(
        None, 
        description="Email válido del usuario"
    )
    password: Optional[SecretStr] = Field(
        None, 
        min_length=8,
        description="Contraseña del usuario (mínimo 8 caracteres)"
    )
    rol: Optional[RolUsuario] = Field(
        None,
        description="Rol del usuario: Administrador o Cliente"
    )

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    rol: RolUsuario
    
    class Config:
        from_attributes = True
