# 2. Installation

Audiogravi<sup>ty</sup> installs in a single command. The installer detects your architecture,
generates security keys, configures the systemd service and starts everything —
usually **under five minutes** from `curl` to listening. No compilation, no
dependency hell, no manual configuration.

## Before you start

- A **Linux host** next to your hi-fi — DietPi or Debian/Ubuntu, on **x86-64** or
  **aarch64** (Raspberry Pi). See [Requirements](../../README.md#requirements).
- The host reachable on your **local network**.
- Your **early-access token** — a GitHub token shared with approved testers during
  early access. [Request one](mailto:contact@audiogravity.app?subject=Audiogravi<sup>ty</sup>%20-%20Early%20access%20request) if you don't have it.

## Recommended — all-in-one (one box)

Installs the **core** (the engine) and the **ui** (the interface) on the same box.
This is the standard setup and the one one-click self-update fully supports.

```bash
curl -fsSL https://audiogravity.app/install.sh | sudo bash -s -- --token ghp_xxx
```

Then open the interface in any browser on your network:

```
https://<ip-of-your-streamer>
```

## Advanced — core and ui separately

You can install the two parts independently — for example to run the interface on a
different machine. Run each installer on its target host:

```bash
curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- --token ghp_xxx
curl -fsSL https://audiogravity.app/install-ui.sh   | sudo bash -s -- --token ghp_xxx
```

> **Split installs and updates.** One-click self-update updates a **co-located**
> core + ui together. If core and ui live on **different hosts**, update each side
> separately (see [8. Updating](08-updating.md)).

## Optional flags (core installer)

| Flag | What it does |
|------|--------------|
| `--vapid-email you@example.com` | Contact address for Web Push notifications (the VAPID `sub`). Omitted → a placeholder is used and push stays basic. |
| `--public-url https://your.domain` | Enables **passkeys** (WebAuthn) and derives the WebAuthn origin / RP ID. Passkeys need a real HTTPS **domain** — they do **not** work over a bare IP. |

```bash
curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- \
    --token ghp_xxx \
    --vapid-email you@example.com \
    --public-url https://audiogravity.example.com
```

> Use the exact origin your browser shows (scheme + host + port). Example:
> `--public-url https://ag.example.com:8443` → `WEBAUTHN_ORIGIN=https://ag.example.com:8443`
> and `WEBAUTHN_RP_ID=ag.example.com`.

> **For a standard setup you don't edit `.env` by hand.** The installer generates a
> complete, working configuration: it creates the security secrets (API key, session key)
> and the Web Push keys for you, so the box is **fully functional out of the box** — you
> can log in, control audio, browse the library and radio without touching any file. The
> flags above are simply the recommended way to switch on the two **optional** features
> (passkeys and a real push contact); skip them and everything else still works. To enable
> them later, re-run the installer with the flag — or edit `/opt/audiogravity/core/.env`
> and restart the core (`sudo systemctl restart ag-core-server`).
>
> **The one exception is Roon**, which has no installer flag or UI — you enable it in
> `.env`. See [6. Outputs & engines → Roon](06-outputs-engines.md#roon).

## First contact

Open `https://<box-ip>` in a browser. On first run, Audiogravi<sup>ty</sup> activates a
**30-day trial** automatically — no action required — and you can create your admin
account. Continue to **[3. First run](03-first-run.md)**.

## Uninstalling

```bash
sudo /opt/audiogravity/uninstall.sh          # core
sudo /var/www/audiogravity-ui/uninstall.sh   # ui
```
