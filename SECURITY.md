# Sécurité

## Dépendances & images Docker

Ce projet utilise des images de base (Node/Nginx) et des dépendances npm/pip. Des outils de scan peuvent remonter des vulnérabilités sur les images upstream.

Mesures prises :
- Images Docker taggées avec des versions explicites (Node Alpine, Nginx Alpine).
- Mise à jour des paquets OS dans les images (`apk upgrade`) pendant le build.
- Recommandation : mettre à jour régulièrement les images et dépendances, et scanner en CI (Docker Scout/Trivy).

## Authentification

- Authentification par JWT.
- Les endpoints sensibles nécessitent un token.

