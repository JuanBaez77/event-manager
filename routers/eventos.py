from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.eventos import Evento, EventoCreate
from services import eventos as service
from middlewares.jwt_bearer import JWTBearer

router = APIRouter(prefix="/eventos",tags=["eventos"],dependencies=[Depends(JWTBearer())])

@router.get("", response_model=List[Evento], status_code=status.HTTP_200_OK)
async def listar_eventos_disponibles(db: Session = Depends(get_db)):
    return service.obtener_eventos_disponibles(db)

@router.get("/buscar", response_model=List[Evento], status_code=status.HTTP_200_OK)
async def buscar_eventos(q: str, db: Session = Depends(get_db)):
    return service.buscar_eventos(db, q)

@router.get("/{evento_id}", response_model=Evento, status_code=status.HTTP_200_OK)
async def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = service.obtener_evento(db, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento

@router.post("", response_model=Evento, status_code=status.HTTP_201_CREATED)
async def crear_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    return service.crear_evento(db, evento)

@router.put("/{evento_id}", response_model=Evento, status_code=status.HTTP_200_OK)
async def actualizar_evento(evento_id: int, evento: dict, db: Session = Depends(get_db)):
    actualizado = service.actualizar_evento(db, evento_id, evento)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return actualizado

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    eliminado = service.eliminar_evento(db, evento_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return None
