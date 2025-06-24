from sqlalchemy import Column, Integer, String, Date
from config.database import Base

class EventoDB(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    lugar = Column(String, nullable=False)
    cupos = Column(Integer, nullable=False)




    # Cuando el fran haga lo de categorias lo puedo/pueden agregar aca
