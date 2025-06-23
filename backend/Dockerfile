# backend/Dockerfile

# Usamos una imagen base ligera de Python 3.10
FROM python:3.10-slim-buster

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app/backend

# Copiamos el archivo de dependencias y las instalamos.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la aplicación (código fuente, Alembic, etc.)
COPY ./app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Exponemos el puerto en el que correrá la aplicación FastAPI
EXPOSE 8000

# CAMBIO CLAVE AQUÍ: Especifica la ruta completa a gunicorn
# Normalmente, se encuentra en /usr/local/bin/gunicorn en imágenes Python de Docker.
CMD ["sh", "-c", "/usr/local/bin/alembic upgrade head && /usr/local/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]