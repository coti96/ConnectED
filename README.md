

# ConnectED 

ConnectED est une plateforme innovante de mise en relation entre étudiants et porteurs de projets, propulsée par l'intelligence artificielle et une base de données orientée graphe.

## 🌟 Fonctionnalités Principales

Le projet est désormais complet et inclut les modules suivants :

### 1. Authentification & Profils
- **Inscription/Connexion** sécurisée (JWT).
- **Profils Utilisateurs** détaillés avec gestion des compétences dynamiques.
- **Rôles** : Étudiants, Créateurs de projets, Administrateurs.

### 2. Gestion des Projets
- **Création de projets** avec description, compétences requises et date limite.
- **Catalogue de projets** avec recherche et filtres.
- **Détails complets** : Visualisation des besoins et du créateur.

### 3. Système de Matching Intelligent (Graph-Based)
- Algorithme de recommandation basé sur **Neo4j**.
- Analyse la compatibilité entre les compétences de l'utilisateur et les besoins du projet.
- Score de pertinence (%) affiché en temps réel.

### 4. Gestion des Candidatures
- **Postuler** en un clic aux projets recommandés.
- **Suivi des candidatures** : En attente, Accepté, Refusé.
- **Pour les créateurs** : Interface de gestion des candidats avec validation/refus.

### 5. Messagerie Instantanée
- **Chat intégré** en temps réel entre candidats et porteurs de projet.
- Historique des conversations.
- Accès direct depuis le profil ou la candidature.

### 6. Tableau de Bord (Dashboard)
- Vue d'ensemble personnalisée à la connexion.
- Statistiques clés (Candidatures, Projets, Messages).
- Fil d'activité récent.

---

## 🛠️ Architecture Technique

- **Frontend** : Angular 16+ (Standalone Components, Signals).
- **Backend** : Python Flask (REST API).
- **Base de Données** : Neo4j (Graph Database) pour gérer les relations complexes (User -[:HAS_SKILL]-> Skill <-[:REQUIRES]- Project).
- **Conteneurisation** : Docker & Docker Compose.

---

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
│   ├─ app.py         # Point d'entrée avec driver Neo4j
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
