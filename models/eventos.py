from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base  # o db.database según tu proyecto

class EventoDB(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    lugar = Column(String, nullable=False)
    cupos = Column(Integer, nullable=False)

    # Clave foránea hacia CategoriaDB
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)

    # Relación ORM
    categoria = relationship("CategoriaDB", back_populates="eventos")