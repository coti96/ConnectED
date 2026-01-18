# =========================
# Étape 1 : Build Angular
# =========================
FROM node:20-alpine AS build

WORKDIR /app

# On copie les fichiers de dépendances en premier (Optimisation du cache Docker)
COPY package*.json ./
# À la place de RUN npm install
RUN npm install --legacy-peer-deps

# Copie le reste du code
COPY . .

# Build de production (plus rapide et léger que --dev)
RUN npm run build -- --configuration=production

# =========================
# Étape 2 : Serveur Nginx
# =========================
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/*/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]