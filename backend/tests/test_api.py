"""
Suite de tests automatisés pour l'API Flask (Domains, Technologies, Projects, Users)
Utilise pytest + requests pour tester tous les endpoints.

Installation :
    pip install pytest requests

Configuration :
    Modifier BASE_URL si votre serveur tourne sur un autre port.

Lancement :
    pytest test_api.py -v
    pytest test_api.py -v --tb=short          # traceback court
    pytest test_api.py -v -k "domain"         # uniquement les tests domains
    pytest test_api.py -v -k "not delete"     # exclure les tests delete
"""

import pytest
import requests

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
BASE_URL = "http://localhost:5000"  # ← adapter si besoin


def url(path: str) -> str:
    return f"{BASE_URL}{path}"


# ═══════════════════════════════════════════════════════════════
# FIXTURES — données créées une fois par session et réutilisées
# ═══════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def created_domain():
    """Crée un domaine de test et le supprime à la fin de la session."""
    payload = {"libelle": "Test Domain pytest"}
    r = requests.post(url("/domains"), json=payload)
    assert r.status_code == 201, f"Impossible de créer le domaine : {r.text}"
    domain = r.json()["domains"][0]
    yield domain
    # Nettoyage
    requests.delete(url(f"/domains/{domain['id']}"))


@pytest.fixture(scope="session")
def created_technology(created_domain):
    """Crée une technologie de test liée au domaine et la supprime à la fin."""
    payload = {"libelle": "TechTest pytest", "domain_id": created_domain["id"]}
    r = requests.post(url("/technologies"), json=payload)
    assert r.status_code == 201, f"Impossible de créer la technologie : {r.text}"
    tech = r.json()["technologies"][0]
    yield tech
    requests.delete(url(f"/technologies/{tech['id']}"))


@pytest.fixture(scope="session")
def created_project(created_domain, created_technology):
    """Crée un projet de test et le supprime à la fin."""
    payload = {
        "titre": "Projet pytest",
        "description": "Description de test",
        "localisation": "Paris",
        "nombre_places": 5,
        "statut": "ouvert"
    }
    r = requests.post(url("/projects"), json=payload)
    assert r.status_code == 201, f"Impossible de créer le projet : {r.text}"
    project = r.json()["projects"][0]
    yield project
    requests.delete(url(f"/projects/{project['id']}"))


# ═══════════════════════════════════════════════
# TESTS — DOMAINS
# ═══════════════════════════════════════════════

class TestDomains:

    def test_get_all_domains(self):
        """GET /domains → 200 avec liste."""
        r = requests.get(url("/domains"))
        assert r.status_code == 200
        body = r.json()
        assert "domains" in body
        assert isinstance(body["domains"], list)

    def test_create_domain(self, created_domain):
        """POST /domains → 201, champs présents."""
        assert "id" in created_domain
        assert created_domain["libelle"] == "Test Domain pytest"

    def test_create_domain_missing_field(self):
        """POST /domains sans libelle → 400."""
        r = requests.post(url("/domains"), json={})
        assert r.status_code == 400

    def test_create_domain_invalid_json(self):
        """POST /domains sans body → 400."""
        r = requests.post(url("/domains"), data="not json",
                          headers={"Content-Type": "application/json"})
        assert r.status_code == 400

    def test_create_domain_duplicate(self, created_domain):
        """POST /domains avec libelle existant → 409."""
        r = requests.post(url("/domains"), json={"libelle": created_domain["libelle"]})
        assert r.status_code == 409

    def test_get_domain_by_id(self, created_domain):
        """GET /domains/<id> → 200, bon domaine."""
        r = requests.get(url(f"/domains/{created_domain['id']}"))
        assert r.status_code == 200
        assert r.json()["id"] == created_domain["id"]

    def test_get_domain_not_found(self):
        """GET /domains/<id_inexistant> → 404."""
        r = requests.get(url("/domains/nonexistent-id-000"))
        assert r.status_code == 404

    def test_filter_domains_by_libelle(self, created_domain):
        """GET /domains/filter?libelle=... → résultat non vide."""
        r = requests.get(url("/domains/filter"), params={"libelle": "Test Domain"})
        assert r.status_code == 200
        domains = r.json()["domains"]
        assert any(d["id"] == created_domain["id"] for d in domains)

    def test_update_domain(self, created_domain):
        """PUT /domains/<id> → 200, libelle mis à jour."""
        new_libelle = "Test Domain pytest updated"
        r = requests.put(url(f"/domains/{created_domain['id']}"),
                         json={"libelle": new_libelle})
        assert r.status_code == 200
        assert r.json()["domains"][0]["libelle"] == new_libelle

    def test_update_domain_not_found(self):
        """PUT /domains/<id_inexistant> → 404."""
        r = requests.put(url("/domains/nonexistent-id-000"), json={"libelle": "x"})
        assert r.status_code == 404

    def test_update_domain_invalid_json(self, created_domain):
        """PUT /domains/<id> sans body → 400."""
        r = requests.put(url(f"/domains/{created_domain['id']}"),
                         data="not json",
                         headers={"Content-Type": "application/json"})
        assert r.status_code == 400

    def test_delete_domain_not_found(self):
        """DELETE /domains/<id_inexistant> → 404."""
        r = requests.delete(url("/domains/nonexistent-id-000"))
        assert r.status_code == 404

    # test_delete_domain_success géré implicitement par la fixture (cleanup)


# ═══════════════════════════════════════════════
# TESTS — TECHNOLOGIES
# ═══════════════════════════════════════════════

class TestTechnologies:

    def test_get_all_technologies(self):
        """GET /technologies → 200 avec liste."""
        r = requests.get(url("/technologies"))
        assert r.status_code == 200
        assert "technologies" in r.json()

    def test_create_technology(self, created_technology):
        """POST /technologies → 201, champs présents."""
        assert "id" in created_technology
        assert created_technology["libelle"] == "TechTest pytest"

    def test_create_technology_missing_libelle(self, created_domain):
        """POST /technologies sans libelle → 400."""
        r = requests.post(url("/technologies"), json={"domain_id": created_domain["id"]})
        assert r.status_code == 400

    def test_create_technology_missing_domain(self):
        """POST /technologies sans domain_id → 400."""
        r = requests.post(url("/technologies"), json={"libelle": "orphan tech"})
        assert r.status_code == 400

    def test_create_technology_invalid_domain(self):
        """POST /technologies avec domain_id inexistant → 404."""
        r = requests.post(url("/technologies"),
                          json={"libelle": "ghost tech", "domain_id": "nonexistent"})
        assert r.status_code == 404

    def test_create_technology_duplicate(self, created_technology, created_domain):
        """POST /technologies avec libelle existant → 409."""
        r = requests.post(url("/technologies"),
                          json={"libelle": created_technology["libelle"],
                                "domain_id": created_domain["id"]})
        assert r.status_code == 409

    def test_get_technology_by_id(self, created_technology):
        """GET /technologies/<id> → 200."""
        r = requests.get(url(f"/technologies/{created_technology['id']}"))
        assert r.status_code == 200
        assert r.json()["id"] == created_technology["id"]

    def test_get_technology_not_found(self):
        """GET /technologies/<id_inexistant> → 404."""
        r = requests.get(url("/technologies/nonexistent-id-000"))
        assert r.status_code == 404

    def test_filter_technologies_by_libelle(self, created_technology):
        """GET /technologies/filter?libelle=... → résultat non vide."""
        r = requests.get(url("/technologies/filter"),
                         params={"libelle": "TechTest"})
        assert r.status_code == 200
        techs = r.json()["technologies"]
        assert any(t["id"] == created_technology["id"] for t in techs)

    def test_filter_technologies_by_domain(self, created_technology, created_domain):
        """GET /technologies/filter?domain_id=... → résultat non vide."""
        r = requests.get(url("/technologies/filter"),
                         params={"domain_id": created_domain["id"]})
        assert r.status_code == 200
        techs = r.json()["technologies"]
        assert any(t["id"] == created_technology["id"] for t in techs)

    def test_update_technology(self, created_technology):
        """PUT /technologies/<id> → 200, libelle mis à jour."""
        r = requests.put(url(f"/technologies/{created_technology['id']}"),
                         json={"libelle": "TechTest pytest updated"})
        assert r.status_code == 200
        assert r.json()["technologies"][0]["libelle"] == "TechTest pytest updated"

    def test_update_technology_not_found(self):
        """PUT /technologies/<id_inexistant> → 404."""
        r = requests.put(url("/technologies/nonexistent-id-000"), json={"libelle": "x"})
        assert r.status_code == 404

    def test_add_technology_to_domain(self, created_technology, created_domain):
        """POST /technologies/<id>/domains/<id> → 201."""
        r = requests.post(
            url(f"/technologies/{created_technology['id']}/domains/{created_domain['id']}")
        )
        assert r.status_code == 201

    def test_add_technology_to_domain_not_found(self, created_technology):
        """POST /technologies/<id>/domains/<id_inexistant> → 404."""
        r = requests.post(
            url(f"/technologies/{created_technology['id']}/domains/nonexistent-domain")
        )
        assert r.status_code == 404


# ═══════════════════════════════════════════════
# TESTS — PROJECTS
# ═══════════════════════════════════════════════

class TestProjects:

    def test_get_all_projects(self):
        """GET /projects → 200 avec liste."""
        r = requests.get(url("/projects"))
        assert r.status_code == 200
        assert "projects" in r.json()

    def test_create_project(self, created_project):
        """POST /projects → 201, champs présents."""
        assert "id" in created_project
        assert created_project["titre"] == "Projet pytest"
        assert created_project["nombre_places"] == 5

    def test_create_project_missing_field(self):
        """POST /projects sans champ obligatoire → 400."""
        r = requests.post(url("/projects"), json={"titre": "incomplet"})
        assert r.status_code == 400

    def test_create_project_invalid_nombre_places(self):
        """POST /projects avec nombre_places non entier → 400."""
        r = requests.post(url("/projects"), json={
            "titre": "bad project",
            "description": "desc",
            "localisation": "Lyon",
            "nombre_places": "beaucoup",
            "statut": "ouvert"
        })
        assert r.status_code == 400

    def test_create_project_duplicate(self, created_project):
        """POST /projects avec titre existant → 409."""
        r = requests.post(url("/projects"), json={
            "titre": created_project["titre"],
            "description": "dup",
            "localisation": "Paris",
            "nombre_places": 1,
            "statut": "ouvert"
        })
        assert r.status_code == 409

    def test_get_project_by_id(self, created_project):
        """GET /projects/<id> → 200."""
        r = requests.get(url(f"/projects/{created_project['id']}"))
        assert r.status_code == 200
        assert r.json()["id"] == created_project["id"]

    def test_get_project_not_found(self):
        """GET /projects/<id_inexistant> → 404."""
        r = requests.get(url("/projects/nonexistent-id-000"))
        assert r.status_code == 404

    def test_filter_projects_by_titre(self, created_project):
        """GET /projects/filter?titre=... → résultat non vide."""
        r = requests.get(url("/projects/filter"), params={"titre": "Projet pytest"})
        assert r.status_code == 200
        projects = r.json()["projects"]
        assert any(p["id"] == created_project["id"] for p in projects)

    def test_filter_projects_by_localisation(self, created_project):
        """GET /projects/filter?localisation=Paris → résultat non vide."""
        r = requests.get(url("/projects/filter"), params={"localisation": "Paris"})
        assert r.status_code == 200

    def test_filter_projects_by_statut(self, created_project):
        """GET /projects/filter?statut=ouvert → résultat non vide."""
        r = requests.get(url("/projects/filter"), params={"statut": "ouvert"})
        assert r.status_code == 200

    def test_add_domain_to_project(self, created_project, created_domain):
        """POST /projects/<id>/domains/<id> → 201."""
        r = requests.post(
            url(f"/projects/{created_project['id']}/domains/{created_domain['id']}")
        )
        assert r.status_code == 201

    def test_add_domain_to_project_not_found(self, created_project):
        """POST /projects/<id>/domains/<id_inexistant> → 404."""
        r = requests.post(
            url(f"/projects/{created_project['id']}/domains/nonexistent-domain")
        )
        assert r.status_code == 404

    def test_add_technology_to_project(self, created_project, created_technology):
        """POST /projects/<id>/technologies/<id> → 201."""
        r = requests.post(
            url(f"/projects/{created_project['id']}/technologies/{created_technology['id']}")
        )
        assert r.status_code == 201

    def test_filter_projects_by_domain(self, created_project, created_domain):
        """GET /projects/filter?domain_id=... (après liaison) → résultat non vide."""
        r = requests.get(url("/projects/filter"),
                         params={"domain_id": created_domain["id"]})
        assert r.status_code == 200

    def test_filter_projects_by_technology(self, created_project, created_technology):
        """GET /projects/filter?technology_id=... (après liaison) → résultat non vide."""
        r = requests.get(url("/projects/filter"),
                         params={"technology_id": created_technology["id"]})
        assert r.status_code == 200

    def test_update_project(self, created_project):
        """PUT /projects/<id> → 200, champ mis à jour."""
        r = requests.put(url(f"/projects/{created_project['id']}"),
                         json={"statut": "fermé"})
        assert r.status_code == 200
        assert r.json()["projects"][0]["statut"] == "fermé"

    def test_update_project_nombre_places(self, created_project):
        """PUT /projects/<id> avec nombre_places valide → 200."""
        r = requests.put(url(f"/projects/{created_project['id']}"),
                         json={"nombre_places": 10})
        assert r.status_code == 200
        assert r.json()["projects"][0]["nombre_places"] == 10

    def test_update_project_invalid_nombre_places(self, created_project):
        """PUT /projects/<id> avec nombre_places invalide → 400."""
        r = requests.put(url(f"/projects/{created_project['id']}"),
                         json={"nombre_places": "abc"})
        assert r.status_code == 400

    def test_update_project_not_found(self):
        """PUT /projects/<id_inexistant> → 404."""
        r = requests.put(url("/projects/nonexistent-id-000"), json={"statut": "x"})
        assert r.status_code == 404

    def test_delete_project_not_found(self):
        """DELETE /projects/<id_inexistant> → 404."""
        r = requests.delete(url("/projects/nonexistent-id-000"))
        assert r.status_code == 404


# ═══════════════════════════════════════════════
# TESTS — USERS
# ═══════════════════════════════════════════════

class TestUsers:

    def test_get_all_users(self):
        """GET /users → 200 avec liste."""
        r = requests.get(url("/users"))
        assert r.status_code == 200
        assert "users" in r.json()

    def test_get_user_not_found(self):
        """GET /users/<id_inexistant> → 404."""
        r = requests.get(url("/users/nonexistent-id-000"))
        assert r.status_code == 404

    def test_filter_users_empty_params(self):
        """GET /users/filter sans paramètre → 200."""
        r = requests.get(url("/users/filter"))
        assert r.status_code == 200
        assert "users" in r.json()

    def test_filter_users_by_name(self):
        """GET /users/filter?name=... → 200."""
        r = requests.get(url("/users/filter"), params={"name": "Alice"})
        assert r.status_code == 200

    def test_add_technology_to_user_not_found(self):
        """POST /users/<id_inexistant>/technologies/<id> → 404."""
        r = requests.post(url("/users/nonexistent-user/technologies/nonexistent-tech"))
        assert r.status_code == 404

    # ── Tests avec un vrai utilisateur (si votre API permet d'en créer) ──────
    # Si vous avez un endpoint POST /users, décommentez et adaptez ce bloc :
    #
    # @pytest.fixture(scope="class")
    # def created_user(self, created_technology):
    #     payload = {"name": "User pytest", "email": "pytest@test.com"}
    #     r = requests.post(url("/users"), json=payload)
    #     assert r.status_code == 201
    #     user = r.json()["users"][0]
    #     yield user
    #     requests.delete(url(f"/users/{user['id']}"))
    #
    # def test_get_user_by_id(self, created_user):
    #     r = requests.get(url(f"/users/{created_user['id']}"))
    #     assert r.status_code == 200
    #
    # def test_add_technology_to_user(self, created_user, created_technology):
    #     r = requests.post(url(f"/users/{created_user['id']}/technologies/{created_technology['id']}"))
    #     assert r.status_code == 201
    #
    # def test_recommended_projects(self, created_user):
    #     r = requests.get(url(f"/users/{created_user['id']}/recommended_projects"))
    #     assert r.status_code == 200
    #     assert "recommended_projects" in r.json() or "message" in r.json()


# ═══════════════════════════════════════════════
# POINT D'ENTRÉE DIRECT
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v", "--tb=short"]))
