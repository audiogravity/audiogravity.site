# Audiogravity

Public marketing site and token-authenticated install scripts for Audiogravity.

Live at [audiogravity.app](https://audiogravity.app) via Cloudflare Pages.

## Repository layout

```
.
├── index.html           Single-page landing
├── assets/
│   ├── style.css        All styles (light/dark theme, responsive)
│   ├── main.js          Hero carousel, theme toggle, ribbon shake
│   ├── og-image.svg     Social preview placeholder
│   └── pics/            App screenshots (WebP, 760px wide)
├── install-backend.sh   Token-authenticated backend installer
├── install-frontend.sh  Token-authenticated frontend installer
├── EDITIONS.md          Edition and licensing terms
└── EULA.md              End-user license agreement
```

Custom domain is configured in the Cloudflare Pages dashboard, not via a `CNAME` file.

## Install scripts

The release binaries are hosted on a private repo (`ad5030/audiogravity-releases`). The install scripts here are public and accept a Personal Access Token to authenticate downloads via the GitHub API.

```bash
# Backend — latest
curl -fsSL https://audiogravity.app/install-backend.sh | sudo bash -s -- --token ghp_xxx

# Backend — specific version
curl -fsSL https://audiogravity.app/install-backend.sh | sudo bash -s -- --token ghp_xxx --version 1.2.0

# Frontend — latest
curl -fsSL https://audiogravity.app/install-frontend.sh | sudo bash -s -- --token ghp_xxx

# Frontend — specific version
curl -fsSL https://audiogravity.app/install-frontend.sh | sudo bash -s -- --token ghp_xxx --version 1.2.0
```

The token is shared during the **early access phase** with approved testers. It requires `Contents: Read` on the private releases repo only.
