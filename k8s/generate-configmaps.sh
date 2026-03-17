#!/bin/bash
# =============================================================
# generate-configmaps.sh
# Génère les ConfigMaps Kubernetes depuis les fichiers locaux
# À lancer DEPUIS la racine du projet ConnectED
# =============================================================

set -e

NAMESPACE="connected"

echo "🔧 Génération des ConfigMaps depuis les fichiers locaux..."

# ConfigMap pour les scripts d'initialisation Neo4j
kubectl create configmap neo4j-init-scripts \
  --from-file=db_init.cypher=database/init/db_init.cypher \
  --namespace=$NAMESPACE \
  --dry-run=client -o yaml > k8s/database/neo4j-configmap-init.yaml

# ConfigMap pour les fichiers CSV
kubectl create configmap neo4j-csv-data \
  --from-file=database/csv/domains.csv \
  --from-file=database/csv/projects.csv \
  --from-file=database/csv/technologies.csv \
  --from-file=database/csv/users.csv \
  --from-file=database/csv/relations_project_tech.csv \
  --from-file=database/csv/relations_user_project_applied.csv \
  --from-file=database/csv/relations_user_project_member.csv \
  --namespace=$NAMESPACE \
  --dry-run=client -o yaml > k8s/database/neo4j-configmap-csv.yaml

echo "✅ ConfigMaps générés :"
echo "   → k8s/database/neo4j-configmap-init.yaml"
echo "   → k8s/database/neo4j-configmap-csv.yaml"
