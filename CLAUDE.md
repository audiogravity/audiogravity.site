APP CONTEXT
Ce repo est le **repo de publication d'AudioGravity** : landing page, changelogs, release notes et packages distribués.
Il n'est pas un repo de développement — ne pas y modifier du code métier.

CONTENU
- `CHANGELOG.md` — changelog consolidé de tous les repos (backend + frontend + landing). Seule source de vérité.
- `RELEASE_NOTES.md` — synthèse narrative par feature, user-facing.
- `packages/` — archives de release générées par `../audiogravity.ops/`.
- `index.html` / `assets/` — landing page publique.
- `install.sh`, `install-backend.sh`, `install-frontend.sh` — scripts d'installation livrés aux utilisateurs.

RÈGLES
1. `CHANGELOG.md` et `RELEASE_NOTES.md` sont mis à jour **uniquement au moment d'un commit** sur un autre repo (jamais en cours de développement).
2. Ne jamais modifier `packages/` manuellement — ce répertoire est alimenté par `../audiogravity.ops/build-*.sh`.
3. Les scripts d'installation (`install.sh`, `install-backend.sh`, `install-frontend.sh`) sont générés ou copiés par `../audiogravity.ops/` — ne pas les éditer directement ici.
4. Démarrer la landing en local avec `./dev.sh` (serveur HTTP simple sur le port 8080).
