# Audiogravity — Landing Page

Public marketing site and token-authenticated install scripts for Audiogravity.

Live at [audiogravity.di-marco.net](https://audiogravity.di-marco.net) via GitHub Pages.

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
├── CNAME                GitHub Pages custom domain
├── EDITIONS.md          Edition and licensing terms
└── EULA.md              End-user license agreement
```

## Local development

```bash
./dev.sh
```

Serves `index.html` on `http://10.0.4.254:8080`. Stops with `Ctrl+C`.

`dev.sh` is git-ignored.

## Install scripts

The release binaries are hosted on a private repo (`ad5030/audiogravity-releases`). The install scripts here are public and accept a Personal Access Token to authenticate downloads via the GitHub API.

```bash
# Backend — latest
curl -fsSL https://audiogravity.di-marco.net/install-backend.sh | sudo bash -s -- --token ghp_xxx

# Backend — specific version
curl -fsSL https://audiogravity.di-marco.net/install-backend.sh | sudo bash -s -- --token ghp_xxx --version 1.2.0

# Frontend — latest
curl -fsSL https://audiogravity.di-marco.net/install-frontend.sh | sudo bash -s -- --token ghp_xxx

# Frontend — specific version
curl -fsSL https://audiogravity.di-marco.net/install-frontend.sh | sudo bash -s -- --token ghp_xxx --version 1.2.0
```

The token is shared during the **early access phase** with approved testers. It requires `Contents: Read` on the private releases repo only.

## Image optimisation

Screenshots in `assets/pics/` are WebP, resized to 760px wide (≈2× retina for the 380px display). Total weight is around 530 KB for nine screenshots.

## Theme

Auto-detects `prefers-color-scheme`. Manual override via the toggle in the nav, persisted in `localStorage` under the key `ag-theme`. An anti-flash inline script in `<head>` applies the saved theme before first paint.
