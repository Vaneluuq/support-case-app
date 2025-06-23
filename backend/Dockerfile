# backend/Dockerfile

# Usamos una imagen base ligera de Python 3.10
FROM python:3.10-slim-buster

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app/backend

# Copiamos el archivo de dependencias y las instalamos.
# Esto se hace en un paso separado para aprovechar el cache de Docker:
# si las dependencias no cambian, Docker no las reinstala.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la aplicación (código fuente, Alembic, etc.)
# Asegúrate de que estos paths sean correctos respecto a tu WORKDIR.
COPY ./app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Exponemos el puerto en el que correrá la aplicación FastAPI
EXPOSE 8000

# El comando por defecto para iniciar el servidor.
# - Primero, ejecuta las migraciones de Alembic.
# - Luego, inicia Gunicorn con Uvicorn workers para un rendimiento óptimo.
# La URL de la base de datos se pasará como variable de entorno desde Docker Compose o Render.
CMD ["sh", "-c", "alembic upgrade head && gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]