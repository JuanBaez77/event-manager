from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from fastapi.middleware.cors import CORSMiddleware
#from routers.usuarios import router as  usuarios
from routers.eventos  import router as eventos
#from routers.inscripciones import router as inscripciones
from routers.categorias import router as categorias
from fastapi.staticfiles import StaticFiles



app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)


## defino todos los origenes que van a poder utitlizar/consultar el backend (sacado del profe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#app.include_router(usuarios)
app.include_router(eventos)
#app.include_router(inscripciones)
app.include_router(categorias)


# 1. Servimos todos los archivos estáticos del directorio frontend en la ruta "/" (raíz)
app.mount("/", StaticFiles(directory="frontend", html=True ), name="frontend")


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
