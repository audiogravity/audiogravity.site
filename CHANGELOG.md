# Changelog — Audiogravity

All notable changes to Audiogravity (backend, frontend, license server, installers
and this landing) are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **[frontend] Top bar — mobile navigation toggle** — a left-side button opens the
  vertical tab menu on mobile, mirroring the settings burger on the right.
- **[frontend] Top bar — Library shortcut** — a one-tap button (left of Logout)
  jumps straight to the Library tab; licence gating is preserved (a locked tab
  opens the licence modal instead).
- **[frontend] Roon source logo** — the `RN` text placeholder for Roon sources is
  replaced by a Roon logo rendered as a `currentColor` mask, so it stays visible in
  light, dark and the active (selected) state.

### Changed
- **[frontend] DRY-RUN toggle is now admin-only** — the Audio Software DRY-RUN
  simulation is scoped to administrators (a command-preview / catalog-validation
  tool, not a dependency-resolving simulation); its size now matches the settings
  toggles.

### Fixed
- **[frontend] Login page version label** — shown as `v0.9.2` (lowercase prefix,
  no space).

### Removed
- **[frontend] Obsolete top-bar buttons** — the documentation (audiogravity.app)
  button and the admin "Components" (bundle stats) button were removed.
- **[frontend] Tab-bar now-playing** — the vertical tab sidebar no longer displays
  the current stream (redundant with the mini player).

---

## [0.9.2] - 2026-06-09

**Focus: Qobuz Hi-Res streaming integration + DSD volume safety.**

### Added
- **[backend] Qobuz OAuth2 module** (`modules/qobuz/`): full OAuth2 authentication
  replacing the deprecated username/password login. Bundle credential extraction from
  the Qobuz web player JS, OAuth URL generation, browser-based login, code-to-token
  exchange, working secret discovery, and persistent config storage.
- **[backend] Qobuz search, browse, and playback** (`library/service.py`): header-based
  API auth (`X-App-Id`/`X-User-Auth-Token`), correct API signature format (float
  timestamp, ASCII+UTF-8 byte concatenation), 3 parallel single-type search calls,
  album queueing, cover art on all browse/search methods.
- **[backend] Qobuz catalog browsing** — featured albums (`album/getFeatured`),
  editorial playlists (`playlist/getFeatured`, `playlist/get`). Three new endpoints:
  `GET /library/qobuz-featured`, `GET /library/qobuz-playlists`,
  `GET /library/qobuz-playlist-tracks`. Playlist queueing support.
- **[backend] External stream metadata registry** (`now_playing.py`): stable key
  derivation from `eid` query parameter for Qobuz streams — correct title, artist,
  album, and cover art in now-playing and queue despite ephemeral signed URLs.
- **[backend] Qobuz as virtual source** — `src_qobuz` injected in the player when
  connected; bitrate displayed for Qobuz FLAC streams.
- **[frontend] Qobuz connection card** (`ag-qobuz-output.js`): OAuth2 connect/disconnect
  molecule for the Sources view, with polling and events.
- **[frontend] Qobuz catalog pills** (`ag-library-browse.js`): browse pills switch to
  Favorites / New Releases / Selection / Playlists when Qobuz is selected.
- **[frontend] Qobuz icon** on source cards (optimized 56×56 webp).
- **[tests] Qobuz OAuth2 unit tests** (24 tests): bundle extraction, service
  persistence, OAuth flow, Pydantic models, router endpoints.
- **[tests] Qobuz catalog browsing unit tests** (22 tests): featured albums,
  playlists, playlist tracks, search, cover helper, library router endpoints.
- **[tests] DSD volume unit tests** (10 tests).
- **[dev] `./dev.sh test --report`** generates `TEST_REPORT.md` — markdown summary
  with per-suite pass/fail/skip counts, durations, and failure detail.

### Changed
- **[backend] Qobuz config cleanup** — removed `qobuz_app_id`, `qobuz_app_secret`,
  `qobuz_username`, `qobuz_password` settings; OAuth2 manages credentials via UI.
- **[build] `build-backend-package.sh`** — `qobuz` added to `ENABLED_MODULES` template
  and upgrade migration loop; `QOBUZ_FORMAT_ID=27` in `.env` template.
- **[frontend] Topbar doc button** opens `audiogravity.app`; internal doc links removed
  from settings panel.
- **[docs] Single source of truth** — `CHANGELOG.md` and `RELEASE_NOTES.md` consolidated
  in the landing repository; AG-repo copies marked obsolete in `CLAUDE.md`.

### Fixed
- **[backend] DSD volume protection** (`player/service.py`): 6 bugs causing volume to
  snap to 100% during non-DSD playback — stale HQPlayer cache, race conditions,
  incorrect restore target.
- **[backend] HQPlayer stale track** — `_current_track` cleared after 30s stopped.

---

## [0.9.1] - 2026-06-07

Changes since **0.9.0**. Range: `74a7897` (0.9.0 baseline — *Merge
feat/hqplayer-integration into master*, 2026-05-30) → release HEAD. The earlier
`v0.9.1` git tag (`b3ab0c2`) was never a release and is superseded by this one.


**Focus: ARM/Debian (aarch64) portability.** Audiogravity now installs and runs on
aarch64 (Raspberry Pi 4 / Debian) **alongside** x86/DietPi — with the absolute
constraint of never regressing the existing x86/DietPi target. This cycle also
hardens the install/packaging path, configures the production environment at
install time, fixes the standalone prod server (SSE + WebSocket), and adds test
coverage. Period: 2026-05-30 → 2026-06-07.

### Added
- **ARM64 (aarch64) as a first-class target** — backend, frontend, license server
  and audio-software installs validated end-to-end on a Raspberry Pi 4 (Debian),
  with x86/DietPi kept non-regressed.
- **[packaging] upmpdcli on ARM64** — `scripts/build-upmpdcli-arm64.sh` builds the
  libnpupnp → libupnpp → upmpdcli chain natively for aarch64 and publishes a
  checksum-verified `.deb` bundle on `audiogravity.app`. The package registry
  installs it via a per-arch `arch_fallback` (no upstream arm64 package exists
  anywhere); the official source still wins where it covers the arch.
- **[install] WebAuthn passkeys at install** — `--public-url` sets
  `WEBAUTHN_ORIGIN` and derives `WEBAUTHN_RP_ID`; forwarded by the bootstrap and
  all-in-one installers and documented in the README (passkeys require a real
  HTTPS domain, not a bare IP).
- **[install] Push contact** — `--vapid-email` sets the VAPID `sub`; forwarded by
  the installers.
- **[frontend] HQPlayer manual IP entry** — connect to a HQPlayer on a different
  (but routable) subnet that the local /24 discovery scan can't reach.
- **[frontend] Standalone server WebSocket proxy** — the prod Python server now
  proxies the admin terminal WebSocket (`/sysinfo/terminal/ws`) via raw tunneling.
- **[landing] Page** — the "Releases" link now points to the public GitHub repo;
  install section clarified (works on the LAN by default, passkeys/push moved to an
  optional block that requires a public domain); portable local preview `dev.sh`
  (auto-detected LAN IP).
- **[deps] Deterministic dependencies** — `requirements.lock` (68 packages pinned,
  wheels verified for x86_64 **and** aarch64, Python 3.13.5) + runtime/build split
  (`requirements-dev.lock`); license server dev requirements (`requirements-dev.txt`).
- **[tests]** — VAPID key loading, PayPal IPN webhook flow (8 tests), and scoped
  pytest warning filters for third-party deprecations.

### Changed
- **[backend] Auth** — replaced `passlib` with direct `bcrypt` calls.
- **[frontend] Prod server consolidation** — the frontend package now bundles the
  canonical `serve_https.py` (line-by-line SSE streaming + gzip) instead of a
  divergent, broken inline copy; the systemd unit invokes it with args +
  `WorkingDirectory`.
- **[install] Production `.env` configured at install** — license server URL/key,
  VAPID, and `ENABLED_MODULES` (incl. `hqplayer`).
- **[build] `build-backend.sh` self-bootstraps** — installs system prerequisites
  and `python3`; the generated installer uses non-interactive `apt`; deps synced
  via `pip install -r` with wheels only.

### Fixed
- **[frontend] Prod SSE stuck on "Connecting…"** — the packaged proxy buffered the
  event stream (`shutil.copyfileobj`); now streamed so the UI connects.
- **[frontend] Broken-pipe traceback noise** in the standalone server when a client
  drops a keep-alive connection (e.g. after closing an SSE tab).
- **[backend] Runtime bugs surfaced on ARM** — CPU model (lscpu fallback), governor
  field (`current_governor`), `cpu-governor.service` boot script (stdlib `json`),
  and `ORJSONResponse` deprecation warnings.
- **[backend] Service config paths** resolved across OS layouts (`/etc` vs
  `/usr/local/etc`) and reloaded when software is installed/removed at runtime.
- **[backend] `hqplayer` module** missing from the packaged `.env` `ENABLED_MODULES`
  (its endpoints returned 404).
- **[backend] aarch64 startup crash** — caused by `passlib` vs `bcrypt>=4.1`.
- **[packaging] Audio-software install made arch-aware** — Roon per-arch URLs
  (`{roon_arch}`), download allowlist, stdin for interactive vendor installers, and
  complete uninstall; upmpdcli `.deb` ships its systemd unit, creates its system
  user, and stops/disables cleanly on removal.
- **[install] sudoers** completed (including Roon uninstall) and hardened
  (`sudo tee` instead of `sudo sh -c`).
- **[build] Nuitka / packaging** — explicit includes (psutil, distro, orjson,
  pydantic, ntplib), `SHA256SUMS` merge + checksum verification in installers,
  missing transitive deps (pyparsing, ifaddr), `gh` auto-install, `license.pub`
  lookup, and miscellaneous installer robustness fixes.
- **[dev] Environment scripts** — no longer hardcode `/home/dietpi` paths or LAN
  IPs (runtime detection); seed a default `admin` user; provision dev sudoers/polkit;
  resolve `visudo` by absolute path on DietPi.

### Removed
- **[build]** obsolete `backend/update.sh` (incompatible with the Nuitka-binary
  production model).

---

> Scope note: this release consolidates the `arm-debian-compat` work (main repo)
> plus this landing repository. The earlier `v0.9.1` tag (`b3ab0c2`) was never a
> release — delete it (local + remote) and re-tag the release commit as `v0.9.1`.
