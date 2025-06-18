# backend/app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Para SQLite, es necesario "check_same_thread": False
# si se usa la misma instancia de DB en múltiples hilos/requests,
# lo cual es común en FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        # result = db.execute("SELECT * FROM items").fetchall()
        # print(result)
        yield db
    finally:
        db.close()