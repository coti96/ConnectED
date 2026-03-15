def normalize_role(value):
    if value is None:
        return None

    raw = str(value).strip().lower()
    raw = raw.replace("é", "e").replace("è", "e").replace("ê", "e").replace("ë", "e")

    mapping = {
        "student": "etudiant",
        "etudiant": "etudiant",
        "etudiante": "etudiant",
        "pro": "professionnel",
        "professional": "professionnel",
        "professionnel": "professionnel",
        "encadrant": "encadrant",
        "supervisor": "encadrant",
        "admin": "admin",
        "administrator": "admin",
    }

    return mapping.get(raw, raw)


def is_valid_role(value):
    return normalize_role(value) in {"etudiant", "professionnel", "encadrant", "admin"}

