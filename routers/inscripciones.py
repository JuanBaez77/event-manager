from fastapi import APIRouter, Depends
from middlewares.jwt_bearer import JWTBearer

router = APIRouter(prefix="/inscripciones", tags=["inscripciones"], dependencies=[Depends(JWTBearer())])


