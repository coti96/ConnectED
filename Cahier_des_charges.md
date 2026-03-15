# Cahier des charges fonctionnel — ConnectED

## 1. Contexte et objectifs
ConnectED est une plateforme de mise en relation entre étudiants, porteurs de projets et encadrants. L’objectif est de faciliter la constitution d’équipes projet grâce à un moteur de recommandation basé sur les compétences (modèle graphe Neo4j).

Objectifs principaux :
- Permettre de publier et découvrir des projets.
- Mettre en place un workflow complet de candidature et de constitution d’équipe.
- Proposer des recommandations explicables à partir des compétences.
- Fournir des fonctionnalités de communication et de suivi (messagerie, notifications).

## 2. Acteurs et rôles
Rôles applicatifs (valeurs normalisées) :
- Étudiant (`etudiant`) : explore les projets, postule, suit ses candidatures.
- Professionnel (`professionnel`) : crée des projets, sélectionne des candidats, gère son équipe.
- Encadrant (`encadrant`) : crée et supervise des projets pédagogiques, gère les candidatures.
- Admin (`admin`) : modération minimale et maintenance.

## 3. Périmètre fonctionnel

### 3.1 Authentification et session
- Inscription et connexion sécurisées.
- Authentification par JWT.
- Protection des pages privées (dashboard, profil, candidatures, messagerie).

### 3.2 Gestion de profil
- Consultation et édition du profil.
- Gestion des compétences sous forme de tags (technologies).
- Champs complémentaires : école/filière (étudiant), entreprise/fonction (professionnel), liens (GitHub/LinkedIn/portfolio) et disponibilité.
- Changement de mot de passe depuis le profil.

### 3.3 Projets
- Liste des projets, recherche par titre/technologies, filtres et tri.
- Détail d’un projet : description, technologies requises, créateur, capacité et places restantes.
- Création de projet possible pour tout utilisateur authentifié (étudiant compris) afin de proposer une idée et recruter des collaborateurs.
- Recommandations “pour vous” basées sur les technologies en commun, avec explication (technologies communes et score).

### 3.4 Candidatures et constitution d’équipe
- Candidature à un projet (étudiant) et suivi du statut : `PENDING`, `ACCEPTED`, `REJECTED`.
- Annulation possible d’une candidature tant qu’elle est `PENDING`.
- Gestion des candidatures par le créateur (accepter/refuser).
- À l’acceptation : ajout automatique du candidat comme membre du projet (`MEMBER_OF`).
- Respect de la capacité : blocage des acceptations quand il n’y a plus de places disponibles.

### 3.5 Messagerie
- Conversations et historique des messages entre utilisateurs authentifiés.

### 3.6 Notifications (in-app)
- Notifications dans l’interface pour :
  - changement de statut de candidature ;
  - réception d’un message.
- Marquage “lu/non lu” et compteur.

### 3.7 Administration (minimum viable)
- Liste des projets.
- Modification du statut d’un projet (ouvert/fermé).

### 3.8 Aide et support
- Page “Aide” présentant les parcours principaux et limitations.

## 4. Exigences non fonctionnelles
- Sécurité : mots de passe hashés (bcrypt), endpoints sensibles protégés par JWT.
- Robustesse : réponses JSON d’erreur homogènes côté API.
- Qualité : tests “smoke” sur les endpoints essentiels.
- Déploiement : exécution locale via Docker Compose.

## 5. Modèle de données (Neo4j)

### 5.1 Nœuds
- `User` : email (unique), nom, prenom, role, champs profil, password_hash.
- `Project` : id (UUID), titre, description, statut, nombre_places, deadline, created_at.
- `Technology` : libelle.
- `Domain` : libelle.
- `Notification` : id, type, message, data, read, created_at.

### 5.2 Relations
- `(User)-[:CREATED_BY]->(Project)`
- `(Project)-[:IN_DOMAIN]->(Domain)`
- `(Project)-[:REQUIRES_TECH]->(Technology)`
- `(User)-[:HAS_TECH]->(Technology)`
- `(User)-[:APPLIED_TO {date, status, motivation_message}]->(Project)`
- `(User)-[:MEMBER_OF {joined_at}]->(Project)`
- `(User)-[:HAS_NOTIFICATION]->(Notification)`

## 6. Parcours utilisateur (résumé)
- Étudiant : compléter profil → consulter projets → voir recommandations → postuler → suivre statut → rejoindre l’équipe si accepté.
- Créateur/encadrant : créer projet → consulter candidatures → accepter/refuser → équipe constituée → échanges via messagerie.
- Admin : supervision minimale via page dédiée.
