# 8. Updating

Audiogravi<sup>ty</sup> updates itself from the browser — no terminal, no re-running scripts.

## One-click self-update

When a newer release is available, the **Admin** page shows an update banner with the
new version, a release-notes link, and a **required** badge if the update is critical.
You don't need the page open to notice: the **Admin tab** itself carries a small
download marker whenever an update is waiting — in the warning colour when it is
**required**.

<img src="images/ios-update-banner.webp" alt="The update banner: new version, release-notes link and the one-click Update now button" width="360">

Installing it is one action:

1. A short confirmation (playback briefly stops) and your **admin password**.
2. The box **downloads** the new version, **swaps** the binary, and **health-checks**
   that it comes back up on the **right version**.
3. Live progress the whole way — *downloading → installing → verifying* — even across
   the service restart.

On an **all-in-one** box, the same click updates the **core and the interface
together**, so everything lands on the new version at once.

While software is being installed on the box — from **Audio Software**, the
**Terminal** tab or over SSH — the update is refused, with a message naming what is
being installed. Try again once it has finished.

### Safety: automatic rollback

If anything goes wrong, the box **automatically rolls back** to the previous version
and tells you — you're never left on a broken update. There's **no OS reboot**; only a
brief pause while the audio service restarts.

## Split installs (different hosts)

One-click self-update covers a **co-located** core + ui. If your core and interface
run on **different hosts**, update each side separately (see below) — the one-click
action updates the box it runs on.

## Manual update

You can always update by re-running the installer; your configuration is preserved —
both `.env` and your files under `/etc/audiogravity` (the signal-chain map, and your saved
radio stations). A **fresh** install seeds those files with sensible defaults; an
**upgrade never overwrites them**, so your edits survive. The services and profiles are
the exception: they come with each version, and the installer puts them back every time
it runs (see [7. Administration](07-administration.md#audio-configuration-services--profiles)):

```bash
curl -fsSL https://audiogravity.app/install.sh | sudo bash
```

## Version-mismatch banner

If the interface and the core end up on different versions (for example after a
partial or multi-host update), a banner appears in the Admin tab prompting you to
update the other component. It's silent when the two match.

## Backup & restore

Everything that makes your box *yours* lives in a handful of files. Copy them before
an OS reinstall (or on a schedule) and you can rebuild the box in minutes:

| What | Where |
|------|-------|
| Audio setup — hi-fi chain map, saved radio stations | `/etc/audiogravity/` (`audio-topology.json`, `radio.json`) |
| Your **licence** and its public key — valid on this installation only (see below) | `/etc/audiogravity/audiogravity.lic`, `license.pub` |
| **Accounts** — users, roles, password hashes, passkeys | `/opt/audiogravity/core/users.json` |
| Core **runtime config** — API key, security secrets, enabled modules | `/opt/audiogravity/core/.env` |

The simplest habit — grab everything in one archive:

```bash
sudo tar -czf ag-backup-$(hostname)-$(date +%F).tar.gz \
    /etc/audiogravity \
    /var/backups/audiogravity \
    /opt/audiogravity/core/users.json \
    /opt/audiogravity/core/.env
```

**Restore** on a fresh install: run the installer first
(see [2. Installation](02-installation.md)), then unpack the archive over the new
files and restart the core:

```bash
sudo tar -xzf ag-backup-….tar.gz -C / --exclude=etc/audiogravity/audiogravity.lic \
    --exclude='etc/audiogravity/audio-config.json*' \
    --exclude=etc/audiogravity/packages-registry.json \
    --exclude=etc/audiogravity/packages-config.json
sudo systemctl restart ag-core-server
```

Service config files regenerate through the guided setup, and streaming-service logins
are simply re-entered in **Library → Sources**. Your music itself lives on the NAS/USB
drive — it is never stored on the box.

The licence file is left out on purpose: it only matches the installation it was
activated on, and a reinstalled system has a new **Device ID**. Brought back, it would be
refused, and would keep the free trial from starting. To have your licence reset, see
[9. Troubleshooting](09-troubleshooting.md#licence-not-recognised-after-a-reinstall-or-a-new-machine).

The services and profiles, and the list of audio software, are left out too: they come
with the version you install, and the archive's would bring back those of the version you
backed up.

> Editor-level backups (the timestamped copies the Config editor keeps before every
> save) live under `/var/backups/audiogravity` — that's why the archive above
> includes it.

---

*Roon, HQPlayer, AirPlay, Qobuz, Tidal and HIGHRESAUDIO, and their respective logos, are
trademarks of their respective owners. Audiogravi<sup>ty</sup> is not affiliated with,
endorsed by, or sponsored by any of them: it interoperates with their software as a client,
and each remains the property of its owner.*
