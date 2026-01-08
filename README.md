

# ConnectED 

## Phase 0 : Guide installation projet

Cette **Phase 0** correspond à l'initialisation technique du projet avec Docker et Git.

---

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
│
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
Cette commande fait deux choses :

Construit les images Docker pour backend et frontend (à partir des Dockerfile)

Et lance les containers correspondants

Attention : ça peut prendre quelques minutes car Docker télécharge les images de base et installe les dépendances.

Après ça, le projet est accessible depuis le navigateur :

Backend : http://localhost:5000

Frontend : http://localhost:4200

Let's go!