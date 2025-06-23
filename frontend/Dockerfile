# frontend/Dockerfile

# --------------- FASE DE CONSTRUCCIÓN (Build Stage) ---------------
# Usamos una imagen Node.js para construir la aplicación React.
FROM node:18-alpine as build

# Establecemos el directorio de trabajo para el frontend
WORKDIR /app/frontend

# Copiamos los archivos de configuración de dependencias (package.json, package-lock.json)
# Asegúrate de que package-lock.json existe y está actualizado con las dependencias correctas
COPY package.json package-lock.json ./

# Invalidar caché: Este truco ayuda a que Docker no use caché de capas problemáticas
ARG CACHE_BREAKER=$(date +%s)
RUN echo $CACHE_BREAKER

# Instalamos las dependencias usando npm ci (limpio y consistente para CI/CD)
# Asegúrate de que 'react-scripts' esté en las 'dependencies' o 'devDependencies' de tu package.json.
RUN npm ci

# Copiamos el resto del código fuente de la aplicación React
COPY . .

# Ejecutamos el build, forzando la inclusión de node_modules/.bin en el PATH para encontrar react-scripts
RUN export PATH=$(pwd)/node_modules/.bin:$PATH && npm run build

# --------------- FASE DE SERVICIO (Serve Stage) ---------------
FROM nginx:stable-alpine

# Copiamos los archivos estáticos generados en la fase de construcción
COPY --from=build /app/frontend/build /usr/share/nginx/html

# Exponemos el puerto 80, el puerto HTTP estándar para Nginx.
EXPOSE 80

# El comando por defecto para iniciar Nginx en primer plano.
CMD ["nginx", "-g", "daemon off;"]