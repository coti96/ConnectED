# =========================
# Étape 1 : Build Angular
# =========================
FROM node:20-alpine3.20 AS build

WORKDIR /app

RUN apk update && apk upgrade --no-cache

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
FROM nginx:1.27-alpine

RUN apk update && apk upgrade --no-cache

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/*/browser /usr/share/nginx/html

EXPOSE 4200

CMD ["nginx", "-g", "daemon off;"]
