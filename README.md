

# ConnectED 

## Phase 0 : Guide installation projet

Cette **Phase 0** correspond à l'initialisation technique du projet avec Docker et Git.

---
Prérequis:
- Git
- Docker Desktop
- Accès à un terminal (Git Bash, Powershell, VS Code Terminal…)

## 1. Structure du projet

```text
ConnectED/
│
├─ backend/           # Code Flask
│   ├─ app/
│   ├─ requirements.txt
│   └─ Dockerfile
│
├─ frontend/          # Angular (préparé pour Docker)
│   ├─ src/
│   ├─ package.json
│   └─ Dockerfile
│─ database/
│  └─ init/ 
│       ├─ schema.sql         
├─ docker-compose.yml
└─ README.md
```

Chaque service a son Dockerfile

Les dossiers backend et frontend contiennent le code source

docker-compose.yml gère les services.

## 2. Guide installation

Cloner le projet: 

```bash
git clone https://github.com/coti96/ConnectED/
```
```bash
cd ConnectED
```

Lancer le projet pour la première fois
```bash
docker-compose up --build
```
Cette commande construit les images (si nécessaire) et lance 3 conteneurs :

Backend Flask (connected-backend) sur le port 5000

Frontend Angular avec Nginx (connected-frontend) sur le port 4200

Base de données MariaDB (connected-db) sur le port 3306

Le backend dépend de la base, donc elle sera initialisée automatiquement à partir du fichier schema.sql.

Attention : ça peut prendre quelques minutes car Docker télécharge les images de base et installe les dépendances.

Après ça, le projet est accessible depuis le navigateur.

Let's go!

Lancer le projet : 

Vérifier les images dockers 
```bash
docker images          
```

Vérifier les conteneurs en cours d'executions
```bash
docker ps          
```

```bash
docker-compose up
```
