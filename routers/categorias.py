from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.categorias import Categoria, CategoriaCreate
from services import categorias as service
from middlewares.jwt_bearer import JWTBearer

router = APIRouter(
    prefix="/categorias",tags=["categorias"],dependencies=[Depends(JWTBearer())]
)

@router.get("", response_model=List[Categoria], status_code=status.HTTP_200_OK)
async def listar_categorias(db: Session = Depends(get_db)):
    return service.obtener_categorias(db)

@router.get("/{categoria_id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = service.obtener_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    existente = service.obtener_por_nombre(db, categoria.nombre)
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una categoría con ese nombre"
        )
    return service.crear_categoria(db, categoria)

@router.put("/{categoria_id}", response_model=Categoria, status_code=status.HTTP_200_OK)
async def actualizar_categoria(categoria_id: int, categoria: dict, db: Session = Depends(get_db)):
    actualizado = service.actualizar_categoria(db, categoria_id, categoria)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return actualizado

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    eliminado = service.eliminar_categoria(db, categoria_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return None
