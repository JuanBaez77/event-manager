from pydantic import BaseModel
from datetime import date
from typing import Optional
from schemas.categorias import Categoria

class EventoBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: date
    lugar: str
    cupos: int
    categoria_id: Optional[int] = None

class EventoCreate(EventoBase):
    pass

class Evento(EventoBase):
    id: int
    categoria: Optional[Categoria] = None

    class Config:
        from_attributes = True
