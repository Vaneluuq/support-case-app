# frontend/Dockerfile

# --------------- FASE DE CONSTRUCCIÓN (Build Stage) ---------------
# Usamos una imagen Node.js para construir la aplicación React.
# La versión 18 es una buena elección para React.
FROM node:18-alpine as build

# Establecemos el directorio de trabajo para el frontend
WORKDIR /app/frontend

# Copiamos los archivos de configuración de dependencias (package.json, yarn.lock, etc.)
# Esto permite que la instalación de dependencias se cachee si no cambian.
COPY package.json yarn.lock* ./

# Instalamos las dependencias. Usamos 'yarn install --frozen-lockfile' para Yarn
# o 'npm ci' para npm, que son más robustos para builds en CI/CD.
RUN yarn install --frozen-lockfile
# Si usas npm, descomenta la siguiente línea y comenta la de yarn:
# RUN npm ci

# Copiamos el resto del código fuente de la aplicación React
COPY . .

# Construimos la aplicación React para producción.
# Esto genera los archivos estáticos (HTML, CSS, JS) en la carpeta 'build'.
RUN yarn build
# Si usas npm, descomenta la siguiente línea y comenta la de yarn:
# RUN npm run build

# --------------- FASE DE SERVICIO (Serve Stage) ---------------
# Usamos una imagen ligera de Nginx para servir los archivos estáticos.
# Esta etapa solo contiene Nginx y los archivos de tu app, lo que resulta en una imagen más pequeña y segura.
FROM nginx:stable-alpine

# Copiamos los archivos estáticos generados en la fase de construcción
# al directorio por defecto de Nginx para servir páginas web.
COPY --from=build /app/frontend/build /usr/share/nginx/html

# Opcional: Si necesitas alguna configuración específica para Nginx, puedes copiarla.
# Por ahora, la configuración por defecto de Nginx para servir archivos estáticos es suficiente.
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponemos el puerto 80, que es el puerto HTTP estándar para Nginx.
EXPOSE 80

# El comando por defecto para iniciar Nginx en primer plano (requerido por Docker).
CMD ["nginx", "-g", "daemon off;"]