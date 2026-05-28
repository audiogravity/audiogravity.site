# Audiogravity

**Your streamer is your source. Audiogravity is the conductor.**

A native iOS / Android app (PWA) — and any modern browser — to pilot every audio engine your streamer runs (MPD, Roon Bridge, HQPlayer NAA, AirPlay, UPnP), all the way down to the RT kernel.

→ [audiogravity.app](https://audiogravity.app)

## What it does

Audiogravity orchestrates the audio engines that audiophiles already trust. It does not replace them — it conducts them from one place:

- **Unified transport** across MPD, Roon, HQPlayer NAA, AirPlay and UPnP
- **HQPlayer DSP remote** — change filter, noise shaper, output mode and volume from the couch, with automatic network discovery
- **Output steering** — switch between USB, Toslink and HDMI outputs without touching the streamer
- **Live signal-path visualisation** of your entire Hi-Fi chain
- **Kernel-level tuning** — RT scheduling, CPU pinning, MEMLOCK — applied via systemd drop-ins (upgrade-safe, reversible)
- **High-resolution library** browsing across Roon, MPD, MinimServer, upmpdcli, Qobuz and Tidal
- **Qobuz Hi-Res streaming** — native integration up to 24-bit / 192 kHz
- **Internet radio** — Radio Browser directory, custom stations, favourites, Hi-Res filtering
- **Bit-perfect lock** with DSD volume protection
- **µs-scale latency benchmarks** from the browser
- **Audio software manager** — install, update and configure audio services from the UI
- **Sleep timer** — automatic pause after a set duration
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

**All-in-one** (backend + frontend on the same host) :

```bash
curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --token ghp_xxx
```

**Or install each component separately** (e.g. on different hosts):

```bash
# Backend
curl -fsSL https://audiogravity.app/install-backend.sh | sudo bash -s -- --token ghp_xxx

# Frontend
curl -fsSL https://audiogravity.app/install-frontend.sh | sudo bash -s -- --token ghp_xxx
```

The token is shared during the **early access phase** with approved testers. It requires `Contents: Read` on the private releases repo only.

To request access: [audiogravity@di-marco.net](mailto:audiogravity@di-marco.net?subject=Audiogravity%20-%20Early%20access%20request)

## Install the PWA on your phone

Audiogravity is a Progressive Web App — it installs like a native app from the browser, no app store needed.

### iOS (Safari)

1. Open **Safari** and navigate to your Audiogravity URL (e.g. `https://your-streamer.local`)
2. Tap the **Share** button (square with arrow, bottom bar)
3. Scroll down and tap **Add to Home Screen**
4. Tap **Add** — the Audiogravity icon appears on your home screen
5. Open it from the home screen — it runs fullscreen like a native app

> Note: iOS requires Safari. Chrome/Firefox on iOS cannot install PWAs.

### Android (Chrome)

1. Open **Chrome** and navigate to your Audiogravity URL
2. Tap the **three-dot menu** (top right)
3. Tap **Add to Home screen** (or **Install app** if prompted)
4. Tap **Install** — the Audiogravity icon appears on your home screen
5. Open it from the home screen — it runs fullscreen like a native app

> Tip: If Chrome shows an install banner at the bottom of the page, you can tap it directly.

## Test report

| Suite | Tests | Status |
|-------|------:|--------|
| Backend (Python) | 65 | ✅ |
| License Server (Python) | 15 | ✅ |
| License Server (JS) | 9 | ✅ |
| Frontend (JS) | 65 | ✅ |
| **Total** | **154** | ✅ |

Last run: 2026-05-28 11:13 UTC

## Coming soon

Audiogravity is in early access. Public release scheduled for **Summer 2026**. To get notified, request access at the email above.
