# ConnectED

ConnectED est une plateforme de mise en relation entre étudiants, porteurs de projets et encadrants. Le cœur de la valeur repose sur un moteur de recommandation basé sur un modèle graphe (Neo4j) et sur un workflow complet de candidature jusqu’à la constitution d’équipes.

## Fonctionnalités
- Authentification sécurisée (JWT) et gestion de profil (compétences, liens, disponibilité, changement de mot de passe).
- Projets : création (tout utilisateur authentifié), liste avec recherche/tri/filtres, page détail.
- Recommandations : score et technologies communes (explicabilité).
- Candidatures : postuler, suivi de statut, annulation (si en attente), gestion côté créateur.
- Équipe : ajout automatique des membres à l’acceptation, respect de la capacité.
- Messagerie et notifications in-app (messages reçus, changements de statut).
- Administration minimale : liste projets et ouverture/fermeture.
- Page “Aide” intégrée.

## Stack et architecture
- Frontend : Angular (standalone components, signals).
- Backend : Flask (API REST).
- Base de données : Neo4j (Bolt).
- Déploiement local : Docker Compose.

## Démarrage rapide (Docker Compose)

Prérequis :
- Docker Desktop
- Git

Configuration (recommandé) :
```bash
cp .env.example .env
```

Lancer l’application :
```bash
docker-compose up --build
```

Accès :
- Frontend : http://localhost:4200
- Backend : http://localhost:5000
- Neo4j Browser : http://localhost:7474 (neo4j / connected_password)

## Comptes de démonstration
Après une initialisation “propre” (volume Neo4j recréé), les comptes suivants sont disponibles avec le mot de passe `password` :
- Étudiant : paul@etudiant.com / password
- Professionnel : pro1@company.com / password
- Encadrant : encadrant@esiee.fr / password
- Admin : admin@connected.com / password

Note : si vous aviez déjà une base Neo4j existante, faites `docker-compose down -v` puis `docker-compose up --build` pour repartir de la base de démonstration et appliquer les index/contraintes.

## Configuration de l’API côté frontend
Par défaut, le frontend calcule l’URL de l’API depuis le hostname courant : `http(s)://<hostname>:5000`.  
Pour un déploiement différent, il est possible de définir `window.__API_URL__` afin de forcer l’URL d’API.

## Tests backend (smoke)
Exécuter la suite de tests API dans le conteneur backend :
```bash
docker exec connected-backend python -m pytest -q
```

## Documentation projet
- Cahier des charges : [Cahier_des_charges.md](Cahier_des_charges.md)
- Sécurité : [SECURITY.md](SECURITY.md)

## Commandes utiles
```bash
docker-compose up -d
docker-compose up -d --build
docker-compose stop
docker-compose down -v
```
