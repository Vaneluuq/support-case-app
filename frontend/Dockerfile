# frontend/Dockerfile

# --------------- FASE DE CONSTRUCCIÓN (Build Stage) ---------------
# Usamos una imagen Node.js para construir la aplicación React.
FROM node:18-alpine as build

# Establecemos el directorio de trabajo para el frontend
WORKDIR /app/frontend

# Copiamos los archivos de configuración de dependencias (package.json, yarn.lock, etc.)
COPY package.json yarn.lock* ./

# Instalamos las dependencias.
RUN yarn install --frozen-lockfile
# Si usas npm, descomenta la siguiente línea y comenta la de yarn:
# RUN npm ci

# Copiamos el resto del código fuente de la aplicación React
COPY . .

# CAMBIO CLAVE AQUÍ: Asegúrate de que el comando de build se ejecute a través de yarn o npm
# Si usas Yarn:
RUN yarn build
# Si usas npm, descomenta la siguiente línea y comenta la de yarn:
# RUN npm run build

# --------------- FASE DE SERVICIO (Serve Stage) ---------------
FROM nginx:stable-alpine

COPY --from=build /app/frontend/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]