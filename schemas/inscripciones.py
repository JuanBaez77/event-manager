from pydantic import BaseModel
from datetime import date
from typing import Optional

class InscripcionBase(BaseModel):
    evento_id: int
    usuario_id: int
    fecha_inscripcion: date

class InscripcionCreate(InscripcionBase):
    pass

class Inscripcion(InscripcionBase):
    id: int

    class Config:
        from_attributes = True
