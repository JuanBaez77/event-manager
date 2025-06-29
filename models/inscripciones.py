from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class InscripcionDB(Base):
    __tablename__ = "inscripciones"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    fecha_inscripcion = Column(Date, nullable=False)

    evento = relationship("EventoDB")
    usuario = relationship("UserDB")
