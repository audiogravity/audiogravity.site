# Audiogravity

**Your streamer is your source. Audiogravity is the conductor.**

A native iOS / Android app (PWA) — and any modern browser — to pilot every audio engine your streamer runs (MPD, Roon Bridge, HQPlayer NAA, AirPlay, UPnP), all the way down to the RT kernel.

→ [audiogravity.app](https://audiogravity.app)

## What it does

Audiogravity orchestrates the audio engines that audiophiles already trust. It does not replace them — it conducts them from one place:

- **Unified transport** across MPD, Roon, HQPlayer NAA, AirPlay and UPnP
- **Live signal-path visualisation** of your entire Hi-Fi chain
- **Kernel-level tuning** — RT scheduling, CPU pinning, MEMLOCK — applied via systemd drop-ins (upgrade-safe, reversible)
- **High-resolution library** browsing across Roon, MPD, MinimServer, upmpdcli, Qobuz and Tidal
- **Bit-perfect lock** with DSD volume protection
- **µs-scale latency benchmarks** from the browser
- **WebAuthn / passkeys** login, multi-user with role-based access
- **PWA-installable** on iOS and Android, accessible from any browser on your network

No cloud account. Self-hosted on your own streamer (DietPi x86_64 or Raspberry Pi aarch64).

## Editions

| Edition | Price | What it unlocks |
|---|---|---|
| **Trial** | Free · 30 days | Full access to every Pro feature, auto-activated on first run |
| **Starter** | Free · forever | Profiles, Services, Audio Software, System, Users |
| **Pro** | €49 lifetime · 1 machine | Audio Pipeline, Player, Library, Audio Services Config, Systemd Config, Performance |

Pro is a lifetime license — no subscription, no renewal. Pro holders receive a preferential upgrade price for future major versions.

See [EDITIONS.md](EDITIONS.md) for the full edition breakdown and [EULA.md](EULA.md) for licensing terms.

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

To request access: [audiogravity@di-marco.net](mailto:audiogravity@di-marco.net?subject=Audiogravity%20-%20Early%20access%20request)

## Coming soon

Audiogravity is in early access. Public release scheduled for **Summer 2026**. To get notified, request access at the email above.
