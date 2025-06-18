# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables de entorno del archivo .env
load_dotenv()

from app.core.config import settings
from app.api.endpoints import support_cases # Importar los endpoints de casos
from app.db.session import Base, engine # Para crear tablas automáticamente si no usas Alembic (no recomendado en prod)

app = FastAPI(title="Support Case API")

# Configuración de CORS para permitir que el frontend se conecte
origins = [
    "http://localhost:3000",  # Origen del frontend React en desarrollo
    # Agrega aquí la URL de tu frontend desplegado en producción cuando sea el momento
    # "https://tu-frontend-desplegado.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"], # Permitir todos los headers
)

# Incluir los routers de la API
app.include_router(support_cases.router)

@app.on_event("startup")
def on_startup():
    # Opcional: Crear todas las tablas en la base de datos al inicio.
    # Esto es conveniente para el desarrollo rápido sin Alembic al principio,
    # pero para entornos de producción y gestión de cambios de esquema,
    # Alembic es la herramienta preferida y más robusta.
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Support Case API!"}

if __name__ == "__main__":
    import uvicorn
    # Para ejecutar directamente sin Docker Compose en desarrollo:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, app_dir=".")