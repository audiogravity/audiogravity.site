# 7. Administration

Everything you need to run the box lives in the interface — no SSH required. Most of
this section is **Pro**; a few tabs (System, Services, Users, Software) are available
on **Starter** too. Every tab has an **INFO** badge that opens an in-app explanation.

## Users & access

Three roles control who can do what:

- **Admin** — full access to all features and user management. Cannot be deleted or
  demoted by others, and cannot delete their own account.
- **User** — standard access to features, but cannot manage users or core settings.
- **Guest** — read-only: can view status and logs but not change settings or toggle
  services.

**Passkeys** — the *Passkeys* button on your own card registers WebAuthn credentials
(Face ID, Touch ID, a hardware key). Each passkey is tied to one device and can be
removed individually; use it instead of a password at login. Password changes take
effect immediately on current sessions.

**Session persistence** — the *Persist* toggle chooses how your session is stored:
persistent (stay logged in across browser restarts) or session-only (log out when
the tab closes). Takes effect on your next login.

## Services

Monitor and control individual systemd services in real time.

- **Status** — active (green), inactive (grey) or failed (red); the dot blinks orange
  while a start/stop is pending. A segmented **health bar** shows the running / stopped
  / failed proportions at a glance.
- **Control** — start, stop or restart any service from its tile. The **ENABLED /
  DISABLED** badge controls whether it starts at boot. Uptime is shown next to the
  unit name.
- **Detail** — click a service name for live metrics (CPU, memory, tasks, network,
  disk) and the session action history. Metrics are colour-coded LOW / MEDIUM / HIGH,
  tuned per audio service (e.g. CPU: ≤5 % low, 5–20 % medium, >20 % high).
- **Filter** — ALL / RUNNING / STOPPED / FAILED.

## Config editor

Safely edit the real configuration files of your audio services (see also
[3. First run](03-first-run.md) for the guided setup).

- **Guided mode** (MPD / AirPlay / UPnP) — change output or library in a couple of
  clicks; only the changed setting is rewritten. *Reset to default* regenerates a
  minimal config (current file backed up first).
- **Form mode** — edit common settings through a friendly interface with field
  descriptions and validation.
- **Expert (Raw) mode** — edit the raw file directly, with syntax validation before
  save.
- **Preview changes (Diff)** — a unified diff (raw) or a before/after field table
  (form) of your unsaved edits.
- **Automatic backups** — every save creates a timestamped backup; the **Backups**
  button browses and restores any previous version.
- **Restart after save** — on by default (applies changes immediately); uncheck to
  batch several edits.

## Audio Software

Install, update and uninstall the services Audiogravi<sup>ty</sup> uses (MPD, upmpdcli,
shairport-sync, Roon Bridge…).

- **States** — NOT INSTALLED, INSTALLED, INSTALLING/UPDATING (progress bar), ERROR.
- **Actions** — INSTALL, UPDATE (to the latest version), UNINSTALL.
- **Version check** — per-card or **CHECK UPDATES** in the header to refresh all.
- **Restart required** — a pulsing badge appears when a service needs a restart after
  install/update; click to restart it.
- **Architecture** — the CPU badge shows supported architectures (amd64, arm64…);
  unsupported cards are dimmed. A **DRY-RUN** mode simulates operations safely.

## System

Real-time monitoring and box-level actions.

- **Metrics** — CPU, temperature, memory, disk and network, updated every few seconds
  over SSE (the **LIVE** badge shows the stream is active).
- **System & audio hardware** — hostname, OS, kernel, CPU model/cores; every audio
  card, USB interface and subdevice.
- **Event log** — system events and SSE messages; RUNNING/STOPPED to pause, CLEAR to
  reset.
- **Actions (admin)** — *Restart Backend* restarts the Audiogravi<sup>ty</sup> service without
  rebooting; *Reboot OS* performs a full reboot (double confirmation). The UI
  reconnects automatically.
- **Terminal (admin)** — a full interactive bash shell in the browser (runs as the
  backend user — use with care).

## Performance tuning (Pro)

Tune CPU scheduling for bit-perfect, glitch-free playback.

- **CPU governor** — *performance* (max frequency always, lowest latency),
  *schedutil* (adapts to load), *powersave* (not recommended for audio). *Apply All*
  sets it on every core; *Save Conf* persists it; *Create Service* restores it at boot.
- **THROTTLED badge** — appears on a core when the kernel reports thermal throttling;
  sustained throttling during playback causes glitches.
- **Latency test** — runs `cyclictest` to measure real-time scheduling latency (µs);
  lower max = fewer dropouts. History of the last 10 runs.
- **Network test** — ping jitter/loss or iperf3 throughput; useful for Roon, AirPlay
  or NAS playback.
- **RT process monitor** — shows the scheduling policy of audio processes: SCHED_FIFO
  / SCHED_RR = real-time (green); NON-RT = risk of glitches under load (red).

## Systemd tuning (Pro)

Low-level, per-service OS tuning using systemd **drop-in overrides** — the native
`.service` files are **never modified**; everything lives in an isolated
`.d/override.conf`.

- **CPU affinity** — pin a service to specific cores to cut context-switching jitter.
- **RT scheduling** — FIFO/RR policy and priority (1–99) for guaranteed CPU time.
- **CPU weight / I/O priority / OOM score** — bias the scheduler, disk/network I/O and
  the out-of-memory killer in favour of audio.
- **RT preset** — *Audio Optimized* pre-fills a battle-tested config (SCHED_FIFO 80,
  LimitRTPRIO 99, MEMLOCK infinity, I/O realtime, OOMScoreAdjust −500, CPUWeight 1000).
- **Safety** — a diff preview before applying, automatic backups (*Restore Backup*),
  and *Remove Override* to roll a service back to factory behaviour instantly.

## Licence

- **Trial** — 30 days of full access, auto-activated on first run.
- **Lifetime** — a single-device `.lic` file cryptographically tied to this device's
  hardware fingerprint (the **Device ID**). One-time payment, no expiry, no
  subscription.
- **Import / re-download** — import a `.lic` file, or re-download yours from the
  self-service portal (purchase email + Device ID, no account needed) after an OS
  reinstall.

## Related

- [8. Updating](08-updating.md) — keeping the box current
- [9. Troubleshooting](09-troubleshooting.md) — when something misbehaves
