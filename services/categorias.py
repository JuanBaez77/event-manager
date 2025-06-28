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

# Función para actualizar una categoría existente
def actualizar_categoria(db: Session, categoria_id: int, categoria_data: dict):
    categoria = db.query(CategoriaDB).filter_by(id=categoria_id).first()
    if not categoria:
        return None
    for key, value in categoria_data.items():
        setattr(categoria, key, value)
    db.commit()
    db.refresh(categoria)
    return categoria

# Función para eliminar una categoría
def eliminar_categoria(db: Session, categoria_id: int):
    categoria = db.query(CategoriaDB).filter_by(id=categoria_id).first()
    if not categoria:
        return False
    db.delete(categoria)
    db.commit()
    return True
