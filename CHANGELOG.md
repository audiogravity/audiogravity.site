# Changelog — Audiogravity

All notable changes to Audiogravity (backend, frontend, license server, installers
and this landing) are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
