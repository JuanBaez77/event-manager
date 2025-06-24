from sqlalchemy.orm import Session
from models.categorias import CategoriaDB
from schemas.categorias import CategoriaCreate

def crear_categoria(db: Session, categoria: CategoriaCreate):
    nueva_categoria = CategoriaDB(**categoria.dict())
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return nueva_categoria

def obtener_categorias(db: Session):
    return db.query(CategoriaDB).all()

def obtener_categoria(db: Session, categoria_id: int):
    return db.query(CategoriaDB).filter_by(id=categoria_id).first()

def obtener_por_nombre(db: Session, nombre: str):
    return db.query(CategoriaDB).filter_by(nombre=nombre).first()
