from sqlalchemy.orm import Session
from models.inscripciones import InscripcionDB
from schemas.inscripciones import InscripcionCreate
from models.eventos import EventoDB

# Crear una inscripción
def crear_inscripcion(db: Session, inscripcion: InscripcionCreate):
    # Obtener el evento
    evento = db.query(EventoDB).filter_by(id=inscripcion.evento_id).first()
    if not evento:
        raise Exception("Evento no encontrado")
    # Contar inscripciones actuales para ese evento
    inscriptos = db.query(InscripcionDB).filter_by(evento_id=inscripcion.evento_id).count()
    # Verificar cupo
    if inscriptos >= evento.cupos:
        raise Exception("No hay cupos disponibles para este evento")
    # Si hay cupo, crear la inscripción
    nueva = InscripcionDB(**inscripcion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Obtener todas las inscripciones
def obtener_inscripciones(db: Session):
    return db.query(InscripcionDB).all()

# Obtener una inscripción por ID
def obtener_inscripcion(db: Session, inscripcion_id: int):
    return db.query(InscripcionDB).filter_by(id=inscripcion_id).first()

# Actualizar una inscripción
def actualizar_inscripcion(db: Session, inscripcion_id: int, inscripcion_data: dict):
    inscripcion = db.query(InscripcionDB).filter_by(id=inscripcion_id).first()
    if not inscripcion:
        return None
    for key, value in inscripcion_data.items():
        setattr(inscripcion, key, value)
    db.commit()
    db.refresh(inscripcion)
    return inscripcion

# Eliminar una inscripción
def eliminar_inscripcion(db: Session, inscripcion_id: int):
    inscripcion = db.query(InscripcionDB).filter_by(id=inscripcion_id).first()
    if not inscripcion:
        return False
    db.delete(inscripcion)
    db.commit()
    return True
