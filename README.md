

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
├─ backend/           # API Flask (Python)
│   ├─ run.py         # Point d'entrée avec driver Neo4j
│   ├─ requirements.txt
│   └─ Dockerfile
│
├─ frontend/          # Application Angular
│   └─ Dockerfile
│
├─ database/          # Initialisation de la BDD
│   └─ init/ 
│       └─ db.cypher  # Scripts de création du graphe (NoSQL)
│
├─ docker-compose.yml # Orchestration des services
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
Cette commande lance 4 conteneurs :
- connected-db : Base de données Neo4j (Port 7474 pour l'interface, 7687 pour le backend).
- connected-db-init : Script automatique qui injecte les données de test (s'arrête après exécution).
- connected-backend : API Flask (Port 5000).
- connected-frontend : App Angular via Nginx (Port 4200).

Attention : ça peut prendre quelques minutes car Docker télécharge les images de base et installe les dépendances.

Après ça, le projet est accessible depuis le navigateur :

- Frontend Angular : http://localhost:4200
- Backend API : http://localhost:5000
- Neo4j Browser (Explorateur de graphe) : http://localhost:7474
    - Login : neo4j
    - Password : connected_password
    - Commande de test : Tape MATCH (n) RETURN n pour voir les bulles.

## 3. Commandes utiles au quotidien

Lancer le projet : 

Vérifier les images dockers 
```bash
docker images          
```

Vérifier les conteneurs en cours d'executions
```bash
docker ps          
```

Démarrer le projet

Pour lancer tous les services en arrière-plan et continuer à utiliser ton terminal :
```bash
docker-compose up -d
```

Appliquer des changements
```bash
docker-compose up -d --build
```

Eteindre le conteneur
```bash
docker-compose stop
```

Reinitialiser le conteneur
```bash
docker-compose down -v
```