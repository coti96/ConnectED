# CAHIER DES CHARGES FONCTIONNEL – PROJET CONNECTED

## 1. VISION ET OBJECTIFS
**ConnectED** est une plateforme collaborative (SaaS) type "Réseau Social Professionnel" dédiée au monde académique et pro. Elle vise à fluidifier la formation d'équipes autour de projets en utilisant un **matching intelligent**.

*   **Promesse** : "Ne cherchez plus, trouvez le projet ou le partenaire qui matche avec vos compétences."
*   **Cœur de valeur** : L'utilisation d'une base de données graphe (Neo4j) pour recommander des connexions basées sur les compétences techniques, les centres d'intérêt et la localisation.

---

## 2. ACTEURS ET RÔLES

| Acteur | Description & Besoins |
| :--- | :--- |
| **Étudiant** | Cherche à rejoindre des projets pour valider son cursus ou monter en compétence. Veut voir les projets "accessibles" à son niveau. |
| **Professionnel** | Cherche des talents pour des projets d'entreprise ou R&D. Veut filtrer les candidats par stack technique précise. |
| **Encadrant** | (Professeur/Tuteur) Propose des projets pédagogiques et supervise les équipes. |
| **Admin** | Gestion globale (modération, maintenance). |

---

## 3. FONCTIONNALITÉS DÉTAILLÉES

### 3.1 Authentification & Onboarding (Le Sas d'entrée)
*   **Inscription (Sign-up)** :
    *   Formulaire classique : Nom, Prénom, Email, MDP, Rôle (Select: Étudiant/Pro/Encadrant).
    *   *Logique Back* : Création du nœud `User` dans Neo4j + Hashage MDP (Bcrypt).
*   **Connexion (Login)** :
    *   Email + MDP.
    *   *Sécurité* : Génération d'un **Token JWT** (stocké en LocalStorage côté Front).
    *   *Redirection* : Vers le Tableau de Bord (Dashboard).
*   **Onboarding (Première visite)** :
    *   **Warning UX** : Si le profil est incomplet (pas de technos/ville), un bandeau d'alerte incite l'utilisateur à le remplir ("Complétez votre profil pour voir les projets qui vous correspondent").

### 3.2 Gestion de Profil (La "Carte d'Identité")
Chaque utilisateur gère sa propre fiche. C'est la source de données du matching.

*   **Données Communes** : Bio, Ville (Localisation), Avatar (optionnel).
*   **Données Spécifiques** :
    *   *Étudiant* : École, Filière, Année.
    *   *Pro* : Entreprise, Fonction.
*   **Le "Skill Graph" (Crucial pour Neo4j)** :
    *   L'utilisateur ajoute des **Tags** de compétences (ex: `Python`, `Angular`, `Figma`).
    *   *Logique* : Création de relations `[:MAITRISE]` entre le `User` et les nœuds `Technology`.

### 3.3 Place de Marché des Projets (Le Cœur)
*   **Création de Projet (Wizard)** :
    *   Infos : Titre, Description riche, Domaine (ex: IA, Web, Mobile).
    *   **Contraintes** :
        *   `Deadline` (Date de fin).
        *   `Nombre de places` (Jauge).
    *   **Ciblage** : Le créateur définit les **Technos requises** (ex: "Besoin de React + Node").
*   **Affichage des Projets (Cartes Intelligentes)** :
    *   Les cartes affichent des **Badges dynamiques** :
        *   🔴 **COMPLET** : Si `places_restantes == 0`.
        *   🟠 **URGENT** : Si `places > 0` ET `deadline < 7 jours`.
        *   🟢 **EN COURS** : Cas standard.
    *   **Indicateur Social** : Affichage du nombre de postulants (ex: "👤 3 candidatures").

### 3.4 Moteur de Matching & Recherche
C'est ici que ton code doit être "intelligent".

*   **Algorithme de Recommandation (Page "Pour vous")** :
    *   Le système score les projets selon 3 axes :
        1.  **Match Technique** : % de technos communes entre le profil et le projet.
        2.  **Match Localisation** : Projets dans la même ville/région.
        3.  **Historique** : "Similaire aux projets que j'ai déjà likés/faits".
*   **Notifications Intelligentes** :
    *   Push/Email envoyé si un nouveau projet matche à >80% avec le profil.
*   **Filtres Manuels** :
    *   Barre de recherche par mots-clés, technos, ville.

### 3.5 Workflow de Candidature (L'Interaction)
1.  **Postuler** : L'étudiant clique sur "Je suis intéressé" + Ajoute un message de motivation ("Cover Letter" courte).
2.  **Réception** : Le créateur voit la candidature dans son tableau de bord "Mes Projets".
3.  **Décision** :
    *   ❌ **Refuser** : Notif "Désolé..." à l'étudiant.
    *   ✅ **Accepter** :
        *   L'étudiant devient `MEMBER_OF` du projet.
        *   Décrémentation automatique du nombre de places.
        *   **Email Automatique** : Envoyé à l'étudiant avec les contacts du créateur pour démarrer.

---

## 4. ARCHITECTURE & DONNÉES

### 4.1 Modèle de Données (Graphe Neo4j)
Le schéma doit refléter ces interactions :
*   `(User)-[:CREATED]->(Project)`
*   `(User)-[:APPLIED_TO {date, message}]->(Project)`
*   `(User)-[:MEMBER_OF]->(Project)`
*   `(Project)-[:NEEDS]->(Technology)`
*   `(User)-[:KNOWS]->(Technology)`

### 4.2 Stack Technique
*   **Frontend** : Angular 17+ (Signals, Standalone Components). Design System SCSS modulaire.
*   **Backend** : Python Flask (API REST).
*   **Database** : Neo4j (Driver Bolt).
*   **Infra** : Docker Compose (Orchestration locale pour le dev).

---

## 5. UI/UX - STRUCTURE DES PAGES (Sitemap)

1.  **Landing Page** (Publique) : Présentation, Call to Action "Rejoindre".
2.  **Auth** : `/login`, `/register`.
3.  **Dashboard** (Privé - Accueil) :
    *   Section "À compléter" (si profil < 100%).
    *   Section "Recommandés pour vous" (Algorithme).
4.  **Explorateur de Projets** (`/projects`) : Liste complète avec filtres.
5.  **Mes Projets** (`/my-projects`) :
    *   Onglet "J'ai créé" (Gestion des candidatures).
    *   Onglet "J'ai postulé" (Suivi des statuts).
    *   Onglet "Je participe" (Projets actifs).
6.  **Profil** (`/profile`) : Édition des infos et des tags technos.
7.  **Détail Projet** (`/projects/:id`) : Vue complète + Bouton Postuler.
