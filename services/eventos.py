from sqlalchemy.orm import Session, joinedload
from models.eventos import EventoDB
from schemas.eventos import EventoCreate
from datetime import date

# Función para crear un nuevo evento en la base de datos
def crear_evento(db: Session, evento: EventoCreate):
    nuevo_evento = EventoDB(**evento.dict())
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)
    return nuevo_evento

# Función para actualizar un evento existente
def actualizar_evento(db: Session, evento_id: int, evento_data: dict):
    evento = db.query(EventoDB).filter_by(id=evento_id).first()
    if not evento:
        return None
    for key, value in evento_data.items():
        setattr(evento, key, value)
    db.commit()
    db.refresh(evento)
    return evento

# Función para eliminar un evento
def eliminar_evento(db: Session, evento_id: int):
    evento = db.query(EventoDB).filter_by(id=evento_id).first()
    if not evento:
        return False
    db.delete(evento)
    db.commit()
    return True

# Función para obtener eventos que todavía no comenzaron y tienen cupos disponibles
def obtener_eventos_disponibles(db: Session):
    hoy = date.today()
    eventos = db.query(EventoDB).options(joinedload(EventoDB.categoria)).filter(
        EventoDB.fecha_inicio > hoy,
        EventoDB.cupos > 0
    ).all()
    return eventos

# Función para buscar eventos por texto (en nombre o descripción)
def buscar_eventos(db: Session, texto_busqueda: str):
    eventos = db.query(EventoDB).options(joinedload(EventoDB.categoria)).filter(
        EventoDB.nombre.ilike(f"%{texto_busqueda}%") |
        EventoDB.descripcion.ilike(f"%{texto_busqueda}%")
    ).all()
    return eventos

# Función para obtener un único evento por su ID
def obtener_evento(db: Session, evento_id: int):
    evento = db.query(EventoDB).options(joinedload(EventoDB.categoria)).filter_by(id=evento_id).first()
    return evento

#Esto lo tuve que buscar con chatgpt pq nunca en mi vida hice un service y como vi que el profe lo hace lo meti pero cualquier cosa se borra ns 
# Le pasa a los mejores agucho AT: AN