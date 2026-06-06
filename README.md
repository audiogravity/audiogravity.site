<p align="center">
  <img src="assets/og-image_black.png" alt="Audiogravity" width="600" />
</p>

<p align="center">
  <strong>Your streamer is your source. Audiogravity is the conductor.</strong>
  <br/>
  A native iOS / Android app (PWA) to pilot every audio engine your streamer runs —<br/>
  MPD, Roon Bridge, HQPlayer NAA, AirPlay, UPnP — all the way down to the RT kernel.
  <br/><br/>
  <a href="https://audiogravity.app"><strong>audiogravity.app →</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.9.0_beta-blue" alt="Version" />
  <img src="https://img.shields.io/badge/platform-DietPi_x86__64_%7C_aarch64-green" alt="Platform" />
  <img src="https://img.shields.io/badge/license-proprietary-lightgrey" alt="License" />
  <img src="https://img.shields.io/badge/tests-154_passing-brightgreen" alt="Tests" />
</p>

---

## Features

<table>
  <tr>
    <td width="50%">

**Audio Control**
- Unified transport across MPD, Roon, HQPlayer NAA, AirPlay and UPnP
- HQPlayer DSP remote — filter, shaper, output mode, volume with auto-discovery
- Output steering — USB, Toslink, HDMI
- One-tap profile scenarios (switch entire audio chains instantly)
- Bit-perfect lock with DSD volume protection
- Sleep timer

</td>
    <td width="50%">

**Library & Radio**
- High-resolution browsing — Roon, MPD, MinimServer, Qobuz, Tidal
- Qobuz Hi-Res streaming up to 24-bit / 192 kHz
- Internet radio — Radio Browser, custom stations, favourites
- UPnP server auto-discovery & browsing

</td>
  </tr>
  <tr>
    <td>

**System & Performance**
- Live signal-path visualisation of your entire Hi-Fi chain
- RT scheduling, CPU pinning, per-core governor control — via systemd drop-ins
- µs-scale latency benchmarks from the browser
- Service monitoring with 60s sparklines
- Audio device inventory (ALSA cards, USB DACs)
- Audio software manager — install, update, configure

</td>
    <td>

**Security & Access**
- WebAuthn / passkeys login
- Multi-user with role-based access (admin, user, guest)
- Push notifications (iOS, Android, desktop)
- PWA-installable on iOS and Android
- No cloud account — fully self-hosted

</td>
  </tr>
</table>

## Editions

| Edition | Price | What it unlocks |
|---------|-------|-----------------|
| **Trial** | Free · 30 days | Full access to every Pro feature |
| **Starter** | Free · forever | Profiles, Services, Audio Software, System, Users |
| **Pro** | €49 lifetime · 1 machine | Pipeline, Player, Library, Config, Performance |

Pro is a lifetime license — no subscription, no renewal. See [EDITIONS.md](EDITIONS.md) and [EULA.md](EULA.md).

## Quick install

```bash
# All-in-one (backend + frontend)
curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --token ghp_xxx

# Or separately
curl -fsSL https://audiogravity.app/install-backend.sh | sudo bash -s -- --token ghp_xxx
curl -fsSL https://audiogravity.app/install-frontend.sh | sudo bash -s -- --token ghp_xxx
```

> The token is shared during **early access** with approved testers. [Request access →](mailto:audiogravity@di-marco.net?subject=Audiogravity%20-%20Early%20access%20request)

### Options

The backend installer accepts an optional contact address for push
notifications (the VAPID `sub`). If omitted, a generic placeholder is used
and the installer prints a warning.

```bash
curl -fsSL https://audiogravity.app/install-backend.sh | sudo bash -s -- \
    --token ghp_xxx --vapid-email you@example.com
```

## Install as PWA

<details>
<summary><strong>iOS (Safari)</strong></summary>

1. Open **Safari** → navigate to your Audiogravity URL
2. Tap **Share** (square with arrow)
3. **Add to Home Screen** → **Add**
4. Open from home screen — runs fullscreen

> iOS requires Safari. Chrome/Firefox on iOS cannot install PWAs.
</details>

<details>
<summary><strong>Android (Chrome)</strong></summary>

1. Open **Chrome** → navigate to your Audiogravity URL
2. Tap **⋮** menu → **Add to Home screen** or **Install app**
3. Tap **Install**
4. Open from home screen — runs fullscreen
</details>

## Test report

| Suite | Tests | Status |
|-------|------:|--------|
| Backend (Python) | 102 | ✅ |
| License Server (Python) | 0 | ✅ |
| License Server (JS) | 0 | ✅ |
| Frontend (JS) | 65 | ✅ |
| **Total** | **167** | ✅ |

Last run: 2026-06-05 12:54 UTC

## Coming soon

Audiogravity is in early access. Public release scheduled for **Summer 2026**.

To get notified: [audiogravity@di-marco.net](mailto:audiogravity@di-marco.net?subject=Audiogravity%20-%20Early%20access%20request)
