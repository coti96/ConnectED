#!/bin/bash
# =============================================================
# deploy.sh — Script de déploiement complet ConnectED sur Minikube
# =============================================================
# Pré-requis :
#   - minikube installé et démarré  (minikube start)
#   - kubectl configuré
#   - Docker disponible
# =============================================================

set -e

DOCKERHUB_USER="${1:-your-dockerhub-username}"
IMAGE_TAG="${2:-latest}"
NAMESPACE="connected"

echo "=============================================="
echo "  🚀 Déploiement ConnectED sur Kubernetes"
echo "  DockerHub user : $DOCKERHUB_USER"
echo "=============================================="

# --- 0. Activer l'Ingress controller sur Minikube ---
echo ""
echo "📦 [0/7] Activation de l'addon Ingress sur Minikube..."
minikube addons enable ingress
# Attendre que le contrôleur soit prêt
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# --- 1. Build et push des images Docker ---
echo ""
echo "🐳 [1/7] Build des images Docker..."

# Pointer Docker vers le daemon Minikube pour éviter de push sur Docker Hub
eval $(minikube docker-env)

docker build -t $DOCKERHUB_USER/connected-backend:$IMAGE_TAG ./backend
docker build -t $DOCKERHUB_USER/connected-frontend:$IMAGE_TAG ./frontend

# (Optionnel) Push vers Docker Hub si vous avez un compte
# docker push $DOCKERHUB_USER/connected-backend:$IMAGE_TAG
# docker push $DOCKERHUB_USER/connected-frontend:$IMAGE_TAG

# Mettre à jour les noms d'images dans les manifests
sed -i "s|image: connected-backend:latest|image: $DOCKERHUB_USER/connected-backend:$IMAGE_TAG|g" k8s/backend/backend-deployment.yaml
sed -i "s|image: connected-frontend:latest|image: $DOCKERHUB_USER/connected-frontend:$IMAGE_TAG|g" k8s/frontend/frontend-deployment.yaml

# --- 2. Créer le namespace ---
echo ""
echo "🗂  [2/7] Création du namespace '$NAMESPACE'..."
kubectl apply -f k8s/namespace.yaml

# --- 3. Générer et appliquer les ConfigMaps ---
echo ""
echo "📄 [3/7] Génération des ConfigMaps (CSV + scripts init)..."
bash k8s/generate-configmaps.sh
kubectl apply -f k8s/database/neo4j-configmap-init.yaml
kubectl apply -f k8s/database/neo4j-configmap-csv.yaml

# --- 4. Déployer la base de données Neo4j ---
echo ""
echo "🗄  [4/7] Déploiement Neo4j..."
kubectl apply -f k8s/database/neo4j-secret.yaml
kubectl apply -f k8s/database/neo4j-pvc.yaml
kubectl apply -f k8s/database/neo4j-deployment.yaml

echo "   ⏳ Attente de Neo4j (readiness)..."
kubectl wait --namespace=$NAMESPACE \
  --for=condition=ready pod \
  --selector=app=neo4j \
  --timeout=180s

# --- 5. Initialiser la base de données ---
echo ""
echo "🌱 [5/7] Initialisation de la base de données..."
kubectl apply -f k8s/database/neo4j-init-job.yaml
kubectl wait --namespace=$NAMESPACE \
  --for=condition=complete job/neo4j-init \
  --timeout=120s
echo "   ✅ Base de données initialisée."

# --- 6. Déployer le Backend et le Frontend ---
echo ""
echo "⚙️  [6/7] Déploiement Backend + Frontend..."
kubectl apply -f k8s/backend/backend-deployment.yaml
kubectl apply -f k8s/frontend/frontend-deployment.yaml

kubectl wait --namespace=$NAMESPACE \
  --for=condition=ready pod \
  --selector=app=backend \
  --timeout=120s

kubectl wait --namespace=$NAMESPACE \
  --for=condition=ready pod \
  --selector=app=frontend \
  --timeout=120s

# --- 7. Appliquer l'Ingress ---
echo ""
echo "🌐 [7/7] Configuration de l'Ingress..."
kubectl apply -f k8s/ingress/ingress.yaml

# --- Résumé ---
MINIKUBE_IP=$(minikube ip)
echo ""
echo "=============================================="
echo "  ✅ Déploiement terminé avec succès !"
echo "=============================================="
echo ""
echo "  Ajoute cette ligne à ton fichier /etc/hosts :"
echo "  $MINIKUBE_IP   connected.local"
echo ""
echo "  Accès à l'application :"
echo "  🌍 Frontend  : http://connected.local"
echo "  🔌 API       : http://connected.local/api"
echo "  🗄  Neo4j UI  : kubectl port-forward svc/neo4j 7474:7474 -n $NAMESPACE"
echo "                 puis ouvrir http://localhost:7474"
echo ""
echo "  Commandes utiles :"
echo "  kubectl get all -n $NAMESPACE"
echo "  kubectl logs -n $NAMESPACE deploy/backend"
echo "  kubectl logs -n $NAMESPACE deploy/frontend"
echo "=============================================="
