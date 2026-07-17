# 2. Installation

Audiogravi<sup>ty</sup> installs in a single command. The installer detects your architecture,
generates security keys, configures the systemd service and starts everything —
usually **under five minutes** from `curl` to the interface. No compilation, no
dependency hell, no manual configuration.

> The installer sets up **Audiogravi<sup>ty</sup> itself**. The audio engines it conducts
> (MPD, AirPlay, UPnP…) are installed afterwards, in a few clicks **from the
> interface** — that's step 3 of [3. First run](03-first-run.md).

## Before you start

- A **Linux host** next to your hi-fi — DietPi or Debian/Ubuntu, on **x86-64** or
  **aarch64** (Raspberry Pi). See
  [1. Introduction → What you need](01-introduction.md#what-you-need).
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

## Getting HTTPS — for passkeys and push

Passkeys (WebAuthn) and push notifications both require the browser to see
Audiogravi<sup>ty</sup> on a **real HTTPS domain** — a bare IP or a self-signed
certificate won't do. The recipe that works well for a home box, without exposing
anything to the internet:

1. **A domain name** you control (any cheap domain works), with a record pointing at
   the box's **LAN address** — e.g. `ag.example.com → 192.168.1.30`. The name only
   has to resolve on your network; nothing needs to be reachable from outside.
2. **A real certificate** via Let's Encrypt using the **DNS-01** challenge (supported
   by certbot and most DNS providers' APIs) — it proves domain ownership through a
   DNS record, so **no port needs opening** to the internet.
3. **A reverse proxy** in front of Audiogravi<sup>ty</sup> that terminates TLS —
   nginx, Caddy or Traefik, on the box itself or another always-on host. The proxy
   now owns TLS, so first re-run the **ui installer** and pick **plain HTTP** mode
   (it serves on port **8080** by default — this also frees port 443 if the proxy
   runs on the box):

   ```nginx
   server {
       listen 443 ssl;
       server_name ag.example.com;
       ssl_certificate     /etc/letsencrypt/live/ag.example.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/ag.example.com/privkey.pem;
       location / {
           proxy_pass http://127.0.0.1:8080;    # the interface, in plain-HTTP mode
           proxy_set_header Host $host;
       }
   }
   ```
   (Proxy on another host? Use the box's LAN IP instead of `127.0.0.1`.)

4. **Tell Audiogravi<sup>ty</sup> its public origin** — re-run the core installer with
   `--public-url https://ag.example.com` (see the flags above). From then on, open
   the app through that URL and the passkey / notification features light up.

Caddy users get steps 2–3 in two lines (`caddy` obtains and renews certificates
automatically). This is the standard self-hosting pattern — any guide on "Let's
Encrypt DNS-01 + reverse proxy" applies as-is.

## First contact

Open `https://<box-ip>` in a browser. On first run, Audiogravi<sup>ty</sup> activates a
**30-day trial** automatically — no action required — and you sign in with the
**default admin account** (then change its password right away — see
[3. First run](03-first-run.md#2-sign-in--and-secure-your-account)). Continue to
**[3. First run](03-first-run.md)**.

## Uninstalling

```bash
sudo /opt/audiogravity/uninstall.sh          # core
sudo /var/www/audiogravity-ui/uninstall.sh   # ui
```
