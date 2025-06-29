from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from config.database import get_db
from schemas.eventos import Evento, EventoCreate
from services import eventos as service
from middlewares.jwt_bearer import JWTBearer
from models.eventos import EventoDB

router = APIRouter(prefix="/eventos",tags=["eventos"],dependencies=[Depends(JWTBearer())])

@router.get("/disponibles", response_model=List[Evento])
def eventos_disponibles(db: Session = Depends(get_db)):
    hoy = datetime.now()
    eventos = db.query(EventoDB).filter(EventoDB.fecha_inicio >= hoy).all()
    return [Evento.model_validate(e) for e in eventos]

@router.get("/todos", response_model=List[Evento])
def listar_todos_eventos(db: Session = Depends(get_db)):
    eventos = db.query(EventoDB).all()
    return [Evento.model_validate(e) for e in eventos]

@router.get("/buscar", response_model=List[Evento], status_code=status.HTTP_200_OK)
async def buscar_eventos(q: str, db: Session = Depends(get_db)):
    eventos = service.buscar_eventos(db, q)
    return [Evento.model_validate(e) for e in eventos]

@router.get("/categoria/{categoria_id}", response_model=List[Evento])
def eventos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    eventos = db.query(EventoDB).filter(EventoDB.categoria_id == categoria_id).all()
    return [Evento.model_validate(e) for e in eventos]

@router.get("/{evento_id}", response_model=Evento, status_code=status.HTTP_200_OK)
async def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = service.obtener_evento(db, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return Evento.model_validate(evento)

@router.post("/", response_model=Evento, status_code=status.HTTP_201_CREATED)
async def crear_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    evento_db = service.crear_evento(db, evento)
    return Evento.model_validate(evento_db)

@router.put("/{evento_id}", response_model=Evento, status_code=status.HTTP_200_OK)
async def actualizar_evento(evento_id: int, evento: dict, db: Session = Depends(get_db)):
    actualizado = service.actualizar_evento(db, evento_id, evento)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return Evento.model_validate(actualizado)

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    eliminado = service.eliminar_evento(db, evento_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return None

@router.get("/buscar", response_model=List[Evento])
def buscar_eventos_db(q: str, db: Session = Depends(get_db)):
    eventos = db.query(EventoDB).filter(
        (EventoDB.nombre.ilike(f"%{q}%")) | (EventoDB.descripcion.ilike(f"%{q}%"))
    ).all()
    return [Evento.model_validate(e) for e in eventos]
