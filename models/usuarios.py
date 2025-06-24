from sqlalchemy import Column, Integer, String
from config.database import Base

class UserDB(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    passh = Column(String(255), nullable=False)  # contraseña hasheada
    rol = Column(String(20), nullable=False)  # "Administrador" o "Cliente"