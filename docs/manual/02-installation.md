# 2. Installation

Audiogravi<sup>ty</sup> installs in a single command. The installer detects your architecture,
generates security keys, configures the systemd service and starts everything —
usually **under five minutes** from `curl` to the interface. No compilation, no
dependency hell, no manual configuration.

> The installer sets up **Audiogravi<sup>ty</sup> itself**, and **MPD** with it — the
> player everything goes through. The other engines it conducts (AirPlay, UPnP, Roon
> Bridge, HQPlayer NAA, HQPlayer Embedded) are yours to choose afterwards, in a few
> clicks **from the interface** — that's step 3 of [3. First run](03-first-run.md).

## Before you start

- A **Linux host** next to your hi-fi running **Debian 13 (Trixie) or later** — DietPi
  and Raspberry Pi OS included, in their Trixie release — on **x86-64** or **aarch64**
  (Raspberry Pi). On another system, the core installer stops and says why. See
  [1. Introduction → What you need](01-introduction.md#what-you-need).
- The host reachable on your **local network**.

## Recommended — all-in-one (one box)

Installs the **core** (the engine) and the **ui** (the interface) on the same box.
This is the standard setup and the one one-click self-update fully supports.

```bash
curl -fsSL https://audiogravity.app/install.sh | sudo bash
```

Then open the interface in any browser on your network:

```text nocopy
https://<ip-of-your-streamer>
```

## Advanced — core and ui separately

You can install the two parts independently — for example to run the interface on a
different machine. Run each installer on its target host:

```bash
curl -fsSL https://audiogravity.app/install-core.sh | sudo bash
curl -fsSL https://audiogravity.app/install-ui.sh   | sudo bash
```

> **Split installs and updates.** One-click self-update updates a **co-located**
> core + ui together. If core and ui live on **different hosts**, update each side
> separately (see [8. Updating](08-updating.md)).

## Optional flags (core installer)

| Flag | What it does |
|------|--------------|
| `--vapid-email you@example.com` | Contact address for Web Push notifications (the VAPID `sub`). Omitted → a placeholder is used and push stays basic. |
| `--public-url https://your.domain` | Enables **passkeys** (WebAuthn) and derives the WebAuthn origin / RP ID. Passkeys need a real HTTPS **domain** — they do **not** work over a bare IP. |

```bash nocopy
curl -fsSL https://audiogravity.app/install-core.sh | sudo bash -s -- \
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
> **Roon needs nothing here either**: install Roon Bridge from the Audio Software page and
> authorize the extension once inside Roon. See
> [6. Outputs & engines → Roon](06-outputs-engines.md#roon).

## Optional flags (ui installer)

| Flag | What it does |
|------|--------------|
| `--https` | Serves the interface over **HTTPS**, with the box's own certificate, on port **443**. What a new install chooses when you just press Enter. |
| `--http` | Serves it in **plain HTTP**, on port **8080** — for a box behind a reverse proxy that handles HTTPS (see below). |
| `--port 9000` | Another port: **80**, **443**, or from **1024** to **65535** — except the core's port when it runs on the same box (**8000**), and in HTTPS **8081**, where the box hands out its certificate. |

Without them, a new install asks the two questions, and an existing one keeps its mode
and its port without asking. So these flags are also how you change them later — re-run
the installer with the one you want:

```bash
curl -fsSL https://audiogravity.app/install-ui.sh | sudo bash -s -- --http
```

`--http` or `--https` alone always means that mode's own port; add `--port` to choose
another. The all-in-one installer takes them too.

They exist from version **0.9.75**; an older installer refuses them. With one of those,
uninstall the interface (`sudo /var/www/audiogravity-ui/uninstall.sh`), run its installer
again without flags and answer **2** to the mode question.

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
   now owns TLS, so first switch the interface to **plain HTTP** — it then serves on
   port **8080**, which also frees port 443 if the proxy runs on the box (see
   [Optional flags (ui installer)](#optional-flags-ui-installer)):

   ```bash
   curl -fsSL https://audiogravity.app/install-ui.sh | sudo bash -s -- --http
   ```

   Then point the proxy at it:

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

Open the address the installer prints at the end — the one its QR code carries:
`https://<name>.local`. `<name>` is the first part of the box's hostname
(`musics` → `musics.local`). The box announces that name on the network, and unlike its
address the name does not change when the router hands out a new lease, so it is the one
to bookmark and the one to add the app from. Should it not open, the box's address,
`https://<box-ip>`, is printed just below it.

When another device on your network already answers to that name, the box takes
`<name>-2.local`, and the installer says so in yellow. Such a name is not one to keep:
which of the two devices gets the `-2` can change when they restart. Give the box a
hostname of its own, then run the installer again — see
[9. Troubleshooting](09-troubleshooting.md#a-bookmark-or-the-home-screen-icon-opens-on-nothing).
On first run, Audiogravi<sup>ty</sup> activates a
**30-day trial** automatically — no action required — and you sign in with the
**default admin account** (then change its password right away — see
[3. First run](03-first-run.md#2-sign-in--and-secure-your-account)). Continue to
**[3. First run](03-first-run.md)**.

## Uninstalling

```bash
sudo /opt/audiogravity/uninstall.sh          # core — keeps your configuration
sudo /var/www/audiogravity-ui/uninstall.sh   # ui
```

This removes the services, the programs, the privileged rules Audiogravi<sup>ty</sup>
granted itself and its system account — but **keeps your configuration** in
`/etc/audiogravity` (your signal-chain map, saved radio stations and licence), the
backups of your audio services' configuration files in `/var/backups/audiogravity`, and
the processor setting of the **Performance** page in `/etc/cpu-governor.conf`.
Reinstalling afterwards picks up where you left off.

To remove those too, add `--purge` to the first command — **in place of** running it
without, not after it: the uninstaller is removed with the programs, so there is no
second run.

```bash
sudo /opt/audiogravity/uninstall.sh --purge  # core — removes your configuration too
sudo /var/www/audiogravity-ui/uninstall.sh   # ui
```

Already uninstalled without `--purge`? Remove what was kept yourself:

```bash
sudo rm -rf /etc/audiogravity /var/backups/audiogravity /etc/cpu-governor.conf
```

The interface's uninstaller also keeps the box's **certificate authority**, in
`/var/lib/audiogravity-ui`, so that your devices still trust the box when you
reinstall. To start from a new one, delete that directory too — each of your devices
will then have to trust the new certificate (see
[3. First run → Trust the box's certificate](03-first-run.md#7-trust-the-boxs-certificate-once-per-device)).

**What is never removed, on purpose:** the audio software itself — MPD, which came
with the installer, and whatever you added from the **Audio Software** page
(Shairport-Sync, upmpdcli, HQPlayer NAA, HQPlayer Embedded, Roon Bridge) — along with
their own configuration files. They are ordinary system packages that keep working without
Audiogravi<sup>ty</sup>; remove them with your package manager if you want them gone.
