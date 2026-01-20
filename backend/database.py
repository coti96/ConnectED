import os
from neo4j import GraphDatabase

# 1. On définit les variables au niveau du module (MAJUSCULES pour les constantes)
URI = os.getenv("DB_URI", "bolt://connected-db:7687")
USER = os.getenv("DB_USER", "neo4j")
PASSWORD = os.getenv("DB_PASSWORD", "connected_password")

class Neo4jDatabase:
    def __init__(self):
        self.driver = None

    def connect(self):
        if not self.driver:
            # 2. Ici, on utilise les variables globales définies plus haut
            self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
            print(f"✅ Connecté à Neo4j sur {URI}")

    def get_db(self):
        if not self.driver:
            self.connect()
        return self.driver

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

# 3. On crée l'instance unique
db = Neo4jDatabase()