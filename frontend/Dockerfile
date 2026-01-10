# frontend/Dockerfile

# =========================
# Étape 1 : Build Angular
# =========================

# Utilise l'image Node.js officielle pour builder Angular
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
# Installe les dépendances npm
RUN npm install
# Copie tout le code source Angular dans le container
COPY . .
# Build Angular en mode dev
RUN npm run build --dev

# =========================
# Étape 2 : Serveur Nginx
# =========================

# Utilise l'image Nginx
FROM nginx:alpine
# Copie le build Angular depuis l'étape précédente vers le répertoire de Nginx
COPY --from=build /app/dist/frontend /usr/share/nginx/html
# Expose le port 80 pour accéder à l'application depuis l'extérieur du conteneur
EXPOSE 80
# Démarre Nginx en mode non-démon (foreground)
CMD ["nginx", "-g", "daemon off;"]
