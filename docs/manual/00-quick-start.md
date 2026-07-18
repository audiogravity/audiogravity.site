# Quick start — from zero to music

The whole journey on one page. Every step links to its full chapter when you want
the detail.

## 1. Install Audiogravi<sup>ty</sup> on the box

```bash
curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --token ghp_xxx
```

One command on your DietPi / Debian box — core and interface together, keys
generated, services started. *(Early-access token required — see
[2. Installation](02-installation.md).)*

## 2. Open it and sign in

Browse to `https://<ip-of-your-box>`. Your **30-day trial** activates by itself.
Sign in as **`admin` / `admin123`** — and change that password right away (**Admin**
tab → your card). *(Details and passkeys: [3. First run](03-first-run.md).)*

## 3. Install the audio engines

**Audio Software** tab → **INSTALL** on **Music Player Daemon** (the core player),
plus **Shairport Sync** (AirPlay) and **UPnP Bridge** if you want them.

## 4. Initialize the audio stack

**Config** tab → **Initialize audio stack**: pick your **DAC** and your **music
library** — a USB drive, or a NAS share
[added right from the picker](03-first-run.md#music-on-a-nas-add-the-share-from-the-picker)
(mounted and tested on the spot) — and confirm with your admin password. The
generated configs are minimal and **bit-perfect**.

## 5. Connect your music

- **Local library** — already there: whatever you picked in step 4.
- **Qobuz, Tidal, HIGHRESAUDIO** — **Library → Sources**, sign in to each service
  with your own subscription *(walkthroughs:
  [5. Library & streaming](05-library-streaming.md))*.
- **Internet radio** — works out of the box, starter stations included.

## 6. Play

**Library** tab → pick an album → it plays on your DAC. Tap the Now Playing bar for
the fullscreen player and the live hi-fi readout — format, sample rate, bitrate
*(tour: [4. Listening](04-listening.md))*.

## 7. Make it yours (optional, five more minutes)

- **[Add it to your phone's home screen](03-first-run.md#7-install-it-as-an-app-recommended-on-phones)** — fullscreen app, portrait lock.
- **[Register a passkey](03-first-run.md#2-sign-in--and-secure-your-account)** — Face ID / Touch ID login (needs
  [HTTPS](02-installation.md#getting-https--for-passkeys-and-push)).
- **[Send music elsewhere](06-outputs-engines.md)** — network renderers, HQPlayer, AirPlay.
- **[Tune the OS for audio](07-administration.md#performance-tuning-pro)** (Pro) — real-time scheduling,
  CPU pinning, latency tests.
