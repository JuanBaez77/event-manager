from pydantic import BaseModel
from datetime import date

class EventoBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: date
    lugar: str
    cupos: int

class EventoCreate(EventoBase):
    pass

class Evento(EventoBase):
    id: int

    class Config:
        orm_mode = True
