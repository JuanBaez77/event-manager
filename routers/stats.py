from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Dict, Any
from datetime import datetime

from config.database import get_db
from models.eventos import EventoDB as Evento
from models.inscripciones import InscripcionDB as Inscripcion
from models.usuarios import UserDB as Usuario
from middlewares.jwt_bearer import JWTBearer

router = APIRouter(prefix="/stats", tags=["Estadísticas"])

@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(JWTBearer())
) -> Dict[str, Any]:
    """
    Obtiene estadísticas para el dashboard
    """
    try:
        # 1. Número total de eventos
        total_eventos = db.query(func.count(Evento.id)).scalar()
        
        # 2. Número total de inscripciones activas (eventos futuros)
        inscripciones_activas = db.query(func.count(Inscripcion.id)).join(
            Evento, Inscripcion.evento_id == Evento.id
        ).filter(
            Evento.fecha_inicio > datetime.now()
        ).scalar()
        
        # 3. Promedio de usuarios inscritos por evento
        inscripciones_por_evento = db.query(
            Inscripcion.evento_id, func.count(Inscripcion.id).label('total')
        ).group_by(Inscripcion.evento_id).all()
        if inscripciones_por_evento:
            promedio_inscripciones = sum([x.total for x in inscripciones_por_evento]) / len(inscripciones_por_evento)
        else:
            promedio_inscripciones = 0
        
        # Si no hay eventos, el promedio es 0
        promedio_inscripciones = promedio_inscripciones or 0
        
        # 4. Evento con más inscripciones
        evento_mas_inscripciones = db.query(
            Evento.nombre,
            func.count(Inscripcion.id).label('total_inscripciones')
        ).outerjoin(
            Inscripcion, Evento.id == Inscripcion.evento_id
        ).group_by(
            Evento.id, Evento.nombre
        ).order_by(
            desc('total_inscripciones')
        ).first()
        
        evento_top = {
            "nombre": evento_mas_inscripciones.nombre if evento_mas_inscripciones else "N/A",
            "inscripciones": evento_mas_inscripciones.total_inscripciones if evento_mas_inscripciones else 0
        }
        
        return {
            "total_eventos": total_eventos,
            "inscripciones_activas": inscripciones_activas,
            "promedio_inscripciones_por_evento": round(float(promedio_inscripciones), 1),
            "evento_mas_inscripciones": evento_top
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}") 