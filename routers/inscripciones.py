from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from config.database import get_db
from schemas.inscripciones import Inscripcion, InscripcionCreate
from services import inscripciones as service
from middlewares.jwt_bearer import JWTBearer
from datetime import datetime
from models.inscripciones import InscripcionDB as InscripcionDB
from models.eventos import EventoDB as EventoDB

router = APIRouter(
    prefix="/inscripciones",
    tags=["inscripciones"],
    dependencies=[Depends(JWTBearer())]
)

@router.get("", response_model=List[Inscripcion], status_code=status.HTTP_200_OK)
async def listar_inscripciones(db: Session = Depends(get_db)):
    inscripciones = service.obtener_inscripciones(db)
    return [Inscripcion.model_validate(i) for i in inscripciones]

@router.get("/{inscripcion_id}", response_model=Inscripcion, status_code=status.HTTP_200_OK)
async def obtener_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    inscripcion = service.obtener_inscripcion(db, inscripcion_id)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return Inscripcion.model_validate(inscripcion)

@router.post("", response_model=Inscripcion, status_code=status.HTTP_201_CREATED)
async def crear_inscripcion(inscripcion: InscripcionCreate, db: Session = Depends(get_db)):
    try:
        inscripcion_db = service.crear_inscripcion(db, inscripcion)
        return Inscripcion.model_validate(inscripcion_db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{inscripcion_id}", response_model=Inscripcion, status_code=status.HTTP_200_OK)
async def actualizar_inscripcion(inscripcion_id: int, inscripcion: dict, db: Session = Depends(get_db)):
    actualizado = service.actualizar_inscripcion(db, inscripcion_id, inscripcion)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return Inscripcion.model_validate(actualizado)

@router.delete("/{inscripcion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_inscripcion(inscripcion_id: int, db: Session = Depends(get_db)):
    eliminado = service.eliminar_inscripcion(db, inscripcion_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return None

@router.get("/activas/{usuario_id}", response_model=List[Inscripcion])
def inscripciones_activas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    hoy = datetime.now()
    inscripciones = db.query(InscripcionDB).join(EventoDB).filter(
        InscripcionDB.usuario_id == usuario_id,
        EventoDB.fecha_inicio >= hoy
    ).all()
    return [Inscripcion.model_validate(i) for i in inscripciones]

@router.get("/historial/{usuario_id}", response_model=List[Inscripcion])
def historial_inscripciones_usuario(usuario_id: int, db: Session = Depends(get_db)):
    inscripciones = db.query(InscripcionDB).filter(
        InscripcionDB.usuario_id == usuario_id
    ).order_by(InscripcionDB.fecha_inscripcion.desc()).all()
    return [Inscripcion.model_validate(i) for i in inscripciones]


