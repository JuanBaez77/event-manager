from sqlalchemy import Column, Integer, String
from config.database import Base
from sqlalchemy.orm import relationship

class CategoriaDB(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)

    eventos = relationship("EventoDB", back_populates="categoria", cascade="all, delete-orphan")