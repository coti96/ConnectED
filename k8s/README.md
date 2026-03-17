# 🚀 Déploiement Kubernetes — ConnectED

Ce dossier contient l'ensemble des manifests Kubernetes pour déployer l'application **ConnectED** sur un cluster local Minikube avec un **Ingress NGINX** comme gateway.

---

## 🏗️ Architecture déployée

```
                        ┌─────────────────────────────┐
                        │       Ingress NGINX           │
                        │     (connected.local)         │
                        └────────┬──────────┬──────────┘
                                 │          │
                    /api/*       │          │  /*
                                 ▼          ▼
                        ┌────────────┐ ┌──────────┐
                        │  Backend   │ │ Frontend │
                        │ Flask/5000 │ │ Nginx/80 │
                        │ (2 pods)   │ │ (2 pods) │
                        └─────┬──────┘ └──────────┘
                              │ bolt://neo4j:7687
                              ▼
                        ┌────────────┐
                        │   Neo4j    │
                        │  (graph DB)│
                        │  + PVC 2Gi │
                        └────────────┘
```

---

## 📁 Structure des fichiers

```
k8s/
├── namespace.yaml                       # Namespace "connected"
├── deploy.sh                            # Script de déploiement tout-en-un
├── generate-configmaps.sh               # Génère les ConfigMaps depuis les fichiers locaux
│
├── database/
│   ├── neo4j-secret.yaml                # Credentials Neo4j (Secret K8s)
│   ├── neo4j-pvc.yaml                   # PersistentVolumeClaim (stockage 2Gi)
│   ├── neo4j-deployment.yaml            # Deployment + Service Neo4j
│   ├── neo4j-init-job.yaml              # Job d'initialisation (CSV + Cypher)
│   ├── neo4j-configmap-init.yaml        # (généré) Script Cypher init
│   └── neo4j-configmap-csv.yaml         # (généré) Fichiers CSV de données
│
├── backend/
│   └── backend-deployment.yaml          # Deployment + Service Flask (2 réplicas)
│
├── frontend/
│   └── frontend-deployment.yaml         # Deployment + Service Angular/Nginx (2 réplicas)
│
└── ingress/
    └── ingress.yaml                     # Ingress NGINX : routage /api → backend, / → frontend
```

---

## ✅ Pré-requis

- [Minikube](https://minikube.sigs.k8s.io/) installé et démarré
- [kubectl](https://kubernetes.io/docs/tasks/tools/) configuré
- [Docker](https://www.docker.com/) disponible
- Un compte [Docker Hub](https://hub.docker.com/) (pour publier les images)

---

## 🚀 Déploiement rapide (script automatique)

```bash
# Depuis la racine du projet ConnectED
chmod +x k8s/deploy.sh k8s/generate-configmaps.sh
./k8s/deploy.sh <votre-username-dockerhub>
```

Le script effectue automatiquement :
1. Active l'addon Ingress sur Minikube
2. Build les images Docker (backend + frontend)
3. Crée le namespace `connected`
4. Génère et applique les ConfigMaps (CSV + scripts Cypher)
5. Déploie Neo4j avec son volume persistant
6. Exécute le Job d'initialisation de la base de données
7. Déploie le Backend et le Frontend
8. Configure l'Ingress

---

## 🛠️ Déploiement manuel étape par étape

### 1. Démarrer Minikube et activer Ingress

```bash
minikube start
minikube addons enable ingress
```

### 2. Pointer Docker vers Minikube

```bash
eval $(minikube docker-env)
```

### 3. Build et push des images

```bash
# Build
docker build -t <dockerhub-user>/connected-backend:latest ./backend
docker build -t <dockerhub-user>/connected-frontend:latest ./frontend

# Push sur Docker Hub
docker push <dockerhub-user>/connected-backend:latest
docker push <dockerhub-user>/connected-frontend:latest
```

> ⚠️ **Important** : remplacez `image: connected-backend:latest` et  
> `image: connected-frontend:latest` dans les fichiers YAML par votre image Docker Hub.

### 4. Créer le namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 5. Générer les ConfigMaps

```bash
bash k8s/generate-configmaps.sh
kubectl apply -f k8s/database/neo4j-configmap-init.yaml
kubectl apply -f k8s/database/neo4j-configmap-csv.yaml
```

### 6. Déployer Neo4j

```bash
kubectl apply -f k8s/database/neo4j-secret.yaml
kubectl apply -f k8s/database/neo4j-pvc.yaml
kubectl apply -f k8s/database/neo4j-deployment.yaml

# Attendre que Neo4j soit prêt
kubectl wait --namespace=connected --for=condition=ready pod --selector=app=neo4j --timeout=180s

# Lancer le job d'initialisation
kubectl apply -f k8s/database/neo4j-init-job.yaml
```

### 7. Déployer Backend et Frontend

```bash
kubectl apply -f k8s/backend/backend-deployment.yaml
kubectl apply -f k8s/frontend/frontend-deployment.yaml
```

### 8. Appliquer l'Ingress

```bash
kubectl apply -f k8s/ingress/ingress.yaml
```

### 9. Configurer /etc/hosts

```bash
echo "$(minikube ip)  connected.local" | sudo tee -a /etc/hosts
```

---

## 🌐 Accès à l'application

| Service | URL |
|---|---|
| Frontend Angular | http://connected.local |
| API Backend | http://connected.local/api |
| Neo4j Browser | `kubectl port-forward svc/neo4j 7474:7474 -n connected` → http://localhost:7474 |

---

## 🔍 Commandes utiles

```bash
# Voir tous les objets déployés
kubectl get all -n connected

# Voir les logs du backend
kubectl logs -n connected deploy/backend -f

# Voir les logs du frontend
kubectl logs -n connected deploy/frontend -f

# Voir le statut de l'Ingress
kubectl describe ingress connected-ingress -n connected

# Vérifier l'IP de Minikube
minikube ip

# Ouvrir dans le navigateur (Minikube)
minikube service frontend -n connected
```

---

## 📊 Correspondance avec les critères du projet

| Critère | Implémentation |
|---|---|
| Web service | Flask (Python) — REST API |
| Docker | `Dockerfile` backend + frontend |
| Multi-conteneurs | 4 services : frontend, backend, neo4j, neo4j-init |
| Kubernetes | Deployments, Services, PVC, Secret, ConfigMap, Job |
| Gateway / Ingress | NGINX Ingress → routage `/api` → backend, `/` → frontend |
| Base de données | Neo4j graph DB avec PersistentVolume |
| Frontend | Angular + Nginx |

---

## 🏆 Pour aller plus loin (bonus)

- **Terraform** : provisionner un cluster GKE/EKS/AKS et y déployer les manifests
- **Cloud** : pousser les images sur Google Container Registry / AWS ECR
- **TLS** : ajouter `cert-manager` pour un certificat HTTPS sur l'Ingress
