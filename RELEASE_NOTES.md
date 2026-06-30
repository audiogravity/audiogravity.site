# Audiogravity — Release Notes

Synthesized overview of each release. For the full line-by-line changelog, see
[CHANGELOG.md](CHANGELOG.md).

---

## Unreleased

### Deployment renamed: `core` and `ui` (was `backend` / `frontend`)

The two installable components are now called **core** and **ui** everywhere — packages, systemd services, install scripts and data directories. New installs use `install-core.sh` / `install-ui.sh`, the services are `ag-core-server` / `ag-ui-server`, and data lives under `/opt/audiogravity/core` and `/var/www/audiogravity-ui`.

Existing systems are not touched automatically. To move an already-installed host to the new layout, run the new `migrate-deploy-layout.sh` once (as root) before reinstalling: it backs everything up first, then renames the layout while preserving your configuration, secrets and user accounts. It works whether core and ui share a host or run on separate machines.

### Fullscreen player — source badge on the cover art

The origin badge (❖ QOBUZ, ❖ TIDAL, ❖ UPNP) is now displayed directly on the cover art, top-left. The track badge (A1 · TRACK 01) appears bottom-left. The duplicate source badge that appeared below the cover has been removed.

### Track number badge now shown for all sources

The A1 · TRACK 01 badge was missing for Qobuz, Tidal and MinimServer streams. It now appears correctly for all sources, via both the direct MPD path and the UPnP renderer path.

---

## 0.9.8 — 2026-06-29

### Signal path — the real audio chain, in real time

The fullscreen player now shows the full audio chain as it actually exists at any moment, not a static topology.

**With a UPnP renderer active** (e.g. upmpdcli / music.#1):
`• Qobuz → • music.#1 → • MPD → • USB → • Heed Abacus`

**In bypass mode or without renderer:**
`• Qobuz → • MPD → • USB → • Heed Abacus`

**With a native network renderer** (Marantz, Linn…) that has its own internal DAC:
`• Qobuz → • Marantz PM7000N`

The connector (USB / TOSLINK) is inserted automatically based on the active ALSA output and updates live when you switch. The source (Qobuz, Tidal, Radio, Library…) is always the first step.

The separate `→ music.#1` overlay in the fullscreen player has been removed — the renderer is now one step among others in the chain. The mini player source row gains a compact `→ renderer_name` badge when a renderer is active.

### Output selector — switch between physical outputs and network renderers

The Sources panel now shows a unified **output selector** with every available audio destination in one place:

- **Physical outputs** — one row per MPD audio output block (USB DAC, TOSLINK…), named exactly as configured in `mpd.conf`. Tapping one enables it exclusively and disconnects any active renderer.
- **Network renderers** — all known UPnP renderers (upmpdcli, Marantz, Linn…) listed below. Tap to connect; the active renderer shows a Disconnect button and a volume slider.

The active output is highlighted in green. An unreachable renderer shows orange. Switching between a physical output and a renderer requires no page refresh and fires no extra commands — one tap routes audio.

**Radio cast to renderer** — playing an internet radio station while a UPnP renderer is selected now sends the stream to the renderer via AVTransport, just like Qobuz or library tracks. If no renderer is active, playback falls back to the local MPD output.

**Remove a renderer** — swipe a renderer row to the left to permanently remove it from the list. No need to reconnect or scan again to add it back — use the Scan button.

### UPnP renderer — full album playback, NEXT / PREV and "Up next"

When you play an album from Qobuz, Tidal or a MinimServer library to a UPnP renderer, AG now queues all tracks and chains them automatically — gapless where the renderer supports it, seamless in any case. Qobuz tracks are served through AG's internal proxy so URLs never expire, enabling both uninterrupted album play and manual navigation.

The **NEXT** and **PREV** transport buttons in the fullscreen player now skip between tracks in the renderer queue. Buttons are disabled at boundaries (first / last track). Pressing both rapidly is safe — a 409 is returned if a transition is already in progress.

The fullscreen player shows an **Up next** strip at the bottom with the next track's title, artist and cover art, updated in real time as the album progresses.

### UPnP renderer — seeking within a Qobuz track

UPnP renderers can now seek mid-track within a Qobuz stream. The AG proxy forwards HTTP `Range` requests from the renderer to the Qobuz CDN and relays the `206 Partial Content` response, so transport position scrubbing in the renderer's own UI (or any control point) works without restarting the stream from the beginning.

### UPnP renderer — live status indicator

The renderer card in the Sources panel now reflects the true state of the device in real time:

- **Connected** (green) — renderer is reachable and responding
- **Unreachable** (orange) — the connection object is active but the device stopped responding (powered off, network loss). The card shows "unreachable — check device" and recovers automatically within 30 s when the device comes back — no page refresh, no manual reconnect.
- **Offline** (red) — no renderer configured

After a backend restart, the auto-reconnect now retries with exponential backoff (30 s → 60 s → … → 5 min cap) instead of giving up after one attempt. If upmpdcli or the renderer starts later than the AG core, the badge goes green as soon as the device responds.

### Install on your home screen (Android / Chrome)

On Android, Chrome will now offer a compact **Install** banner at the bottom of the screen when Audiogravity is eligible for installation as a standalone app. Tap **Install** to add it to your home screen — the app then opens full-screen without the browser chrome, exactly like a native app. Dismissing the banner suppresses it for 30 days.

On iPhone, use Safari's Share sheet → "Add to Home Screen" as before (iOS does not expose an install event to web apps).

### Player stays visible when offline

If you lose your network connection while Audiogravity is open, the player now keeps showing the last known track and source instead of going blank. A small **Offline** label appears in the source row to make the stale state explicit.

On a cold reload (opening the app while offline), the last known player state is restored from local cache — so you can still see what was playing last, even without a live connection to the streamer.

### Reliability & fixes

- **Native renderer — "Nothing playing" fixed** — with a network renderer (Marantz, Linn…) whose audio stack is self-contained, the fullscreen player was showing "Nothing playing" even when a track was actively playing. AG now reads the renderer's internal state directly: title, artist, album, cover art and transport position all appear correctly without requiring the local MPD to be in the chain.
- **Native renderer — output bar "No output selected" fixed** — same root cause: when no local source was active the output bar could not determine the routing. The output label and signal path (e.g. `• Marantz PM7000N`) now reflect the renderer correctly.
- **Disconnect stops playback** — clicking Disconnect in the Sources panel now immediately stops the renderer. Previously the renderer kept playing its stream independently until it finished.
- **Renderer snaps back after restart** — after an AG backend restart, the renderer badge now reflects the correct state (PLAYING / STOPPED) within seconds instead of waiting up to 30 s. The backend detects the stale subscription ID, re-subscribes immediately, and refreshes the display.
- **Signal path during reconnect window** — the renderer step is no longer shown in the signal path while the connection is being re-established after a restart.
- **Qobuz single track to renderer** — playing a single Qobuz track (not a full album) to an active renderer was silently broken since the queue refactor. Now correctly routes via `play_queue()` with cover art forwarded.
- **Renderer card stale on new session** — if a renderer status event arrived before the renderer list finished loading, the card was left stale. It now triggers a reload and applies the event on completion.
- **Cover art on consecutive album tracks** — if a track returned a 404 cover, subsequent tracks on the same album were permanently blocked. The error is now cleared on every track change.
- **"Up next" strip cleared on disconnect** — the next-track strip now disappears when the renderer disconnects or is bypassed, instead of lingering indefinitely.
- **Idle renderer badge** — when the renderer is connected but nothing is playing, the fullscreen player now shows the renderer name in the source row so you can confirm the routing without starting playback.
- **Connector badge for upmpdcli** — the USB/TOSLINK badge was incorrectly hidden when upmpdcli was active; it is now always visible since the physical connector is in the chain.
- **MPD output — invalid ID now returns 404** — selecting an MPD output with an unknown `output_id` would previously silently disable all outputs. Now correctly returns 404 before issuing any MPD command.

---

## 0.9.7 — 2026-06-26

### UPnP Control Point — send audio to network renderers

AG can now control any UPnP/DLNA MediaRenderer on the local network (network amplifiers, DLNA speakers, upmpdcli…). Select a renderer in the Sources panel, connect it, then play from the MinimServer library, Qobuz or Tidal — the stream goes directly to the renderer.

**What's new:**
- New "UPnP Renderer" section in the Sources panel: network discovery, connection persisted across restarts, Play/Pause/Stop/Volume controls from the interface.
- `→ renderer` badge in the mini player and fullscreen player to indicate active routing.
- MinimServer → renderer: URI handoff (zero AG proxy, zero extra CPU load).
- Qobuz → renderer: self-authenticated CDN URL (HMAC, no proxy).
- Tidal → renderer: existing DASH→FLAC proxy with LAN-reachable IP (same quality as MPD).
- Renderer state updated in real time via SSE (SUBSCRIBE/NOTIFY + 30 s heartbeat fallback).

---

## 0.9.6 — 2026-06-25

### Cover art when playing via upmpdcli

When an external UPnP control point (BubbleUPnP, Kazoo, Linn app…) pushes music or radio to your streamer via upmpdcli, Audiogravity now displays the correct cover art — including radio station logos — by querying upmpdcli's AVTransport directly to retrieve the artwork the controller originally sent.

### HQPlayer — accurate connection status

The HQPlayer card in the Sources view now reflects the true state of the full audio chain:

- **Connected** — HQPlayer reachable and `networkaudiod` active (audio can reach the DAC).
- **NAA offline** — HQPlayer reachable but `networkaudiod` inactive (no audio output possible).
- **Offline** — HQPlayer unreachable.

The "Use as output" toggle is only shown when the full chain is operational. It is cleared automatically if `networkaudiod` stops during a session.

Several core polling regressions fixed: logs no longer flood with WARNING messages at startup or during DSD stream loading.

### Player auto-follows the active source

The mini-player and fullscreen player now automatically display the currently playing source — no manual dot navigation required when switching between sources (MPD, Roon, AirPlay, TIDAL…).

Tapping a dot or swiping to another source suspends auto-follow so you can browse at your own pace. Auto-follow resumes automatically when the source you selected stops playing.

### Format strip — bitrate now shown for all sources

The fullscreen player's format strip now displays a bitrate for every source and format — ALAC, FLAC, WAV local files, TIDAL, Qobuz, radio, Roon and AirPlay.

- **MPD sources (ALAC, FLAC, WAV, radio, Qobuz)** — instantaneous decode bitrate as reported by MPD.
- **TIDAL** — exact bitrate read from the DASH manifest, available from the very first second of playback (no more `—` during stream warm-up).
- **Roon / AirPlay** — PCM-equivalent computed from bit depth × sample rate × 2 ch (e.g. 24bit/96kHz → 4608 kbps).

### Communications from Audiogravity

Two new channels so you never miss important news about the product.

**In-app announcements** — When Audiogravity publishes a notice (new version, maintenance window, special offer), a 🔔 bell appears on your Admin tab. Open it to see the message as a dismissable banner. Dismissal is stored locally — the banner won't come back. Notices are fetched passively during the regular 24 h licence check-in; no additional data is collected.

**Email** — Important communications (release announcements, early-access offers) are sent to the email address associated with your licence. Every message includes a one-click unsubscribe link — no account required.

---

## 0.9.5 — 2026-06-22

### Core — Audio reliability & under-the-hood fixes

Two core modules (`audio_pipeline` and `audio_hw`) went through a thorough code review. The fixes are transparent to the end user but protect audio quality under load:

- **Event loop no longer blocked** — all filesystem access in `audio_hw` and `audio_pipeline` is now off the event loop (`asyncio.to_thread`). On the Pi, a scan could stall for 50–200 ms, delaying SSE heartbeats and potentially causing audio glitches.
- **Accurate ALSA subdevice availability** — `GET /audio-hw/devices` now reflects the real occupation state of ALSA devices (read from `/proc/asound`). Previously `subdevices_available` was always `1` even when MPD or HQPlayer held the device exclusively.
- **`?force_refresh=true`** — new query parameter on `GET /audio-hw/devices` to force an immediate rescan after a USB hotplug event, without waiting for the 60 s cache to expire.
- **Cache not corrupted on I/O error** — a transient error during a scan (hotplug race, permission) no longer caches an empty or partial list; the next call retries cleanly.
- **Pipeline metrics corrected** — HQPlayer volume clamped to `[0, 100]`, `cpu_percent()` initialised correctly, ALSA latency accurate on ARM64 (64-bit wraparound).
- **HQPlayer "ghost track" in mini player fixed** — after stopping HQPlayer completely (no track loaded), the mini player kept displaying the last played track indefinitely. The now-playing cache is now explicitly cleared when HQPlayer confirms it has nothing to play, while transient stops (DSP transitions, buffering) still show the last known state.
- **Config backup restore now works** — `restore_backup` was silently rejected by sudoers in production (missing `cp` rule); backups can now be restored from the UI.
- **Backup files are now private** — backup files (which may contain service passwords) are now correctly set to mode 600; previously the `chmod` silently failed and files were world-readable.
- **Config editor save/reload no longer stalls** — all blocking I/O in the config service (file reads, sudo commands) now runs off the event loop, preventing audio glitches during a config save or package install.
- **Config validation no longer freezes the server** — `POST /config_validation/validate` previously ran a `systemctl` subprocess per service synchronously on the event loop (up to N×5 s); checks are now parallel and non-blocking.
- **Login timing hardened** — disabled accounts and nonexistent accounts now take the same response time, preventing username enumeration by measuring login latency.
- **Passkey registration and login no longer interfere** — starting a passkey registration and a passkey login simultaneously for the same account no longer causes both flows to fail.
- **HQPlayer playback now works** — every `play_uri` and `play_library_item` call was silently failing after loading the queue because the `<Play/>` command closes the connection without responding; the batch transport now handles this correctly.
- **Trial period survives a power loss** — the trial file is now written atomically; a crash mid-write no longer produces corrupted JSON that is misdiagnosed as tampering and locks the user out of their trial.
- **License gate no longer bypassed at startup** — if the license service fails to initialise, protected endpoints now return HTTP 503 instead of silently allowing all access.
- **Radio custom stations now actually work** — a missing `await` made `POST /radio/library/custom` always fail with a serialisation error since the feature was introduced.
- **Tidal login errors are now reported correctly** — previously the callback endpoint returned HTTP 200 even when the token exchange failed; it now returns HTTP 400 with a clear error message.
- **Server shutdown no longer hangs** — SSE monitoring loops were never cancelled on shutdown due to a type mismatch (`List[Task]` iterated as a single `Task`); fixed so graceful restart is reliable.
- **Reduced CPU/memory pressure on Pi under load** — several long-running blocking operations (audio ALSA scan, thermal zone reads, governor writes, stddev histogram expansion, `os.fsync`) are now off the event loop, reducing audio dropout risk and RAM pressure under sustained load.
- **License server XSS fixed** — a crafted license key or server-controlled filename could inject HTML into the portal activation pages; the admin session token could be exfiltrated if the admin panel was open in the same browser session.
- **License resend and transfer now preserve version scope** — resending or transferring a v1-scoped license was silently upgrading it to an all-versions license; upgrade paywall is now enforced correctly.
- **All-versions lifetime licenses no longer falsely rejected on AG v2** — licenses issued before version scoping was introduced are now correctly accepted on all AG versions.
- **UI XSS vulnerabilities fixed** — three injection points in the license status and package update UI now HTML-escape or validate server-controlled values before rendering. A crafted core response could previously exfiltrate the admin JWT token.
- **UI no longer crashes on corrupted browser storage** — auth initialisation handles a malformed `jwt_user` in localStorage gracefully instead of throwing an uncaught `SyntaxError` that left the app blank.
- **Config editor no longer accumulates memory** — opening and closing the config editor multiple times no longer leaks CodeMirror instances; a `disconnectedCallback` now properly cleans up.

---

## 0.9.4 — 2026-06-20

### UI — Security, reliability & code quality

A targeted UI review produced the following improvements:

- **XSS hardening** — `escapeHtml` now imported as an ES6 module in the admin panel (no more `window.escapeHtml` fallback that could silently skip escaping); metric chart labels use Lit's built-in auto-escaping instead of `unsafeHTML`.
- **Push notifications fixed** — unsubscribing from push notifications now uses the correct `DELETE` HTTP method with the endpoint as a query parameter, matching the backend router. Previously the call was a `POST` with a JSON body that was silently ignored.
- **Password validation** — whitespace-only passwords (e.g. 6 spaces) are now rejected in the user modal before reaching the backend.
- **Memory leak fixed** — the jitter latency Chart.js instance in the network test page is now destroyed when the component is removed from the DOM.

### Reliability & Security — Core hardening

An extensive review of all 20 core modules produced 40+ targeted fixes. None break existing functionality; the most impactful for daily use:

- **Radio station editing now works** — `PUT /radio/{uuid}` was silently returning a coroutine instead of the result; station edits are now persisted correctly.
- **DSD streams detected in the pipeline** — `audio_str="dsd64:2"` was silently discarded; DSD sample rate and bit depth now appear correctly in the pipeline graph and metrics.
- **UPnP queue routes to the right output** — when multiple MPD outputs are configured, UPnP queue operations now honour the requested `output_id` instead of always using the first output.
- **Profile activation resilient to slow services** — stop and start phases are now bounded to 30 s each; a hung service can no longer freeze a profile switch indefinitely.
- **Player poll loop no longer crashes silently** — a network error during `get_now_playing()` now degrades gracefully instead of causing a `NameError` that killed the SSE stream.
- **Package installer hardened against injection** — `install_script_args`, `check_command` and `uninstall_commands` now use `shlex.split` + `subprocess_exec` instead of `shell=True`; GPG key and sources-list destination paths are validated before any `sudo cp`.
- **Steering output switch validated** — ALSA device strings are checked against `hw:<card>,<device>` before being written into any config file, preventing malformed values from corrupting MPD or shairport-sync config.
- **Auth & JWT tightened** — `POST /auth/users` correctly returns 201; whitespace-only passwords rejected; JWT tokens now carry a `jti` (unique ID) for future revocation; token decode errors no longer expose fragments in logs.

### HQPlayer — Stop playback

`POST /hqplayer/stop` is now implemented (it was documented but missing). The button in the HQPlayer output card can reliably stop playback and clear the current track metadata.

### Stream Origin Badge

The Now Playing players (mini bar and fullscreen) now show **where the current
track is streaming from** — a small logo + label such as Tidal, Qobuz, your
UPnP/DLNA server (by name, e.g. *MinimServer*), a radio station, a local file,
Roon or AirPlay. Previously every source that played through MPD looked
identical ("MPD"), so you couldn't tell a Tidal track from a Qobuz one or from a
file on your NAS. The badge is derived server-side from the active stream, so it
stays accurate as you switch sources.

### Reliability — Tidal & Qobuz

When Tidal or Qobuz reverse-engineered client credentials rotate (which happens
periodically without notice), AG now detects the 401/403 response and logs a
clear ERROR with a remediation hint instead of returning an opaque failure. The
Tidal stream endpoint returns HTTP 503 so MPD gets a clean error rather than a
broken stream.

### Library & Settings refinements

- **UPnP/DLNA search fully playable** — media servers such as MinimServer now
  appear as search sources next to MPD, Roon, Qobuz and Tidal. Selecting one while
  in the Search tab runs a text query against that server; clicking "+" or play on
  a result adds it to MPD with correct title, cover art and server badge.
- **Config editor — blank file hint** — when a service config has all sections
  empty (package defaults, e.g. a fresh Debian shairport-sync install), the form
  view now shows a clear banner instead of a series of empty `{}` boxes, with a
  direct link to Expert Mode to view and uncomment the full file.
- **Settings panel** — a single unified product version (front and back share it)
  next to the Swagger API link, and the **Logout** button moved from the top bar
  into the Settings footer for a cleaner top bar.
- **Polish** — the settings button uses a gear icon (mobile nav uses a hamburger),
  and Qobuz/Tidal/HQPlayer now share the same connection status indicator as the
  other sources.

---

## 0.9.3 — 2026-06-14

### Tidal HiFi Streaming

Tidal joins Qobuz as a streaming source. Connect a Tidal HiFi account via PKCE
login (open the link, sign in, paste the redirect URL back — Tidal's fixed
redirect cannot be intercepted in a browser), then browse Favorites, New Releases,
Charts (TIDAL's Top Hits, Viral / Rap / R&B / Pop Hits…), Editorial playlists
(Popular, Trending, TIDAL Rising…) and your own Playlists, or search the full
catalogue. Playback is **lossless FLAC**:
unlike Qobuz's direct URL, Tidal delivers FLAC as a segmented DASH manifest, so a
local proxy remuxes it on the fly with ffmpeg (`-c:a copy`, no re-encoding) and
streams it to MPD as it is produced — playback starts in about a second. The
remux is written to a seekable FLAC file and kept in a small, disk-backed cache
(the current track plus a couple of recent ones, wiped at startup), so replaying
or reopening a track serves it with HTTP Range and **in-track seek works**. The
first play of a given track in a session isn't seekable; replays are. Requires
`ffmpeg` (installed by the backend installer).

### Top Bar — Mobile Navigation & Library Shortcut

The top bar gains two buttons. On the left, a navigation toggle opens the
vertical tab menu on mobile — symmetric to the settings burger on the right. A
new Library shortcut (left of Logout) jumps straight to the Library tab from
anywhere; licence gating is preserved, so a locked tab opens the licence modal
instead. The obsolete documentation and admin "Components" buttons were removed.

### Roon Source Logo

The Roon source dropped its "RN" text placeholder for a proper logo, sized like
the other source icons (MinimServer, Qobuz, HQPlayer). Because the mark is
monochrome, it is rendered as a `currentColor` mask, so it stays visible across
light, dark and the active (selected) card state.

### DRY-RUN Restricted to Admins

The Audio Software DRY-RUN toggle is scoped to administrators. It now performs
real validation: a HEAD request is sent to the download URL before reporting
success, so a dead URL or unreachable server surfaces as a failure instead of a
fake `Success`. For APT repository packages, `apt-get install --simulate` is
also run when possible to surface dependency conflicts.

### Login Page

The version label now reads `v0.9.2` (lowercase prefix, no space).

### Bug Fixes

- **AirPlay now-playing on ARM** — shairport-sync track metadata is read from an
  `a{sv}` D-Bus dict whose values arrived wrapped as Variants on ARM/Debian, leaking
  the raw `<dbus_fast…Variant…>` repr into the pipeline now-playing. The values are now
  unwrapped (recursively; no-op on x86 where they are already native).
- **Fullscreen player volume swipe** — adjusting the volume slider no longer triggers
  the player's multi-source switch swipe; the volume popover now isolates its own touch
  gestures.
- **Library horizontal scroll vs tab switch** — scrolling a horizontal row (browse pills,
  album shelves) no longer flips to the next tab; the swipe-to-switch handler now defers
  to any horizontally-scrollable element under the finger.
- **Fullscreen player pull-down vs scroll** — in a long tracklist, swiping down to scroll
  back up no longer closes the player; pull-to-dismiss only engages when the content is
  already scrolled to the top.

---

## 0.9.2 — 2026-06-09

### Qobuz Hi-Res Streaming (full stack)

Qobuz authentication migrated from deprecated username/password to **OAuth2**.
New backend module handles the full lifecycle: bundle credential extraction,
OAuth URL generation, browser login, token exchange, secret discovery, and
persistent config. The library service uses header-based auth and correct API
signature format. Search runs 3 parallel single-type calls; album and track
queueing registers external stream metadata (title, artist, album, cover art)
keyed by stable `eid`, so now-playing displays are correct despite ephemeral
signed URLs. Qobuz appears as a virtual source in the player when connected.

**Catalog browsing** — browse pills switch to Favorites / New Releases /
Selection / Playlists when Qobuz is selected. Each category fetches from a
dedicated Qobuz API endpoint. Editorial playlists are playable — clicking one
queues all tracks to MPD with full metadata.

### DSD Volume Protection — 6 Bug Fixes

Fixed intermittent regression where volume snapped to 100% during non-DSD
playback. Root causes: stale HQPlayer cache items triggering false DSD
detection, race conditions corrupting saved volume state. 10 unit tests added.

---

## 0.9.1 — 2026-06-07

**Focus: ARM/Debian (aarch64) portability + production hardening.**

### ARM64 as First-Class Target

Audiogravity now installs and runs on aarch64 (Raspberry Pi 4 / Debian)
alongside x86/DietPi. Backend, frontend, license server, and audio-software
installs validated end-to-end on both architectures.

- Deterministic dependencies: `requirements.lock` (68 packages, wheels verified
  for x86_64 and aarch64, Python 3.13.5)
- upmpdcli on ARM64: native build script for the libnpupnp → libupnpp →
  upmpdcli chain, published as a checksum-verified `.deb` bundle
- Roon per-arch URLs, download allowlist, complete uninstall support

### HQPlayer Integration

Discovery panel with manual IP entry for cross-subnet setups. Volume protection
for DSD streams (DSD playback forces 100% hardware volume, restored on
non-DSD). Auto-cleared stale track state after 30s stopped.

### Qobuz OAuth2 Foundation

Full OAuth2 flow replacing deprecated username/password login. Bundle credential
extraction from the Qobuz web player JS, browser-based login, code-to-token
exchange. Frontend connect/disconnect card in the Sources view.

### Library Player — Fullscreen Music Browser

Bottom-sheet overlay hosting six views: Browse, Search, Queue, Sources, Outputs,
Now Playing. Artist → album → track drill-down for MPD, Roon, and Qobuz. Album
card grid with infinite-scroll pagination (IntersectionObserver, 50 albums per
page). Queue management (MPD: remove/clear; Roon: read-only).

### Now Playing — Complete Playback Control

Fullscreen panel driven by SSE: cover art, title, artist, album, format strip
(sample rate, bitrate, codec, hi-res highlight), signal path, seekable progress
bar, transport controls (prev/play/next/repeat/shuffle), volume slider. Dynamic
background tint extracted via canvas color sampling. Horizontal swipe between
active sources. Album detail popover with tracklist. Mini player bar with swipe
gestures.

### Audio Pipeline

Interactive SVG graph: pan, zoom, minimap, draggable nodes with persisted
positions. Live status on nodes (playback state, now-playing info). Output
steering: click any link to switch a service's ALSA output on the fly. Roon zone
display and transfer. Network connectivity view (WiFi signal quality). Mobile
responsive layout.

### License System

- **Trial**: 30-day auto-activated, HMAC-signed with device fingerprint
- **Lifetime**: single-device `.lic` file, Ed25519-signed, uploaded via UI
- **License Server**: admin panel (orders, audit log, email templates, bulk ops,
  device transfer), customer self-service portal, PayPal IPN automation, online
  verification (24h refresh)
- **Feature gating**: `require_full_license` dependency on premium endpoints;
  `version_expired` handling for v1→v2 upgrades
- **Self-service activation**: 3-step stepper (key → hostname → activate) with
  `.lic` download

### Passkeys — Face ID / Touch ID (WebAuthn / FIDO2)

Passwordless authentication via discoverable credentials. One-time setup offer
after password login. Burger menu toggle to register/remove passkeys. Backend:
6 endpoints, replay-attack prevention via sign-count tracking.

### Services & Profiles Management

- **Services tab**: quick filter (All/Running/Stopped/Failed), global health
  bar, inline metrics (CPU/Memory/Disk/NET), uptime display, restart button,
  boot icon, detail modal with session history, dual-line sparklines
- **Profiles tab**: health bar per tile, quick filter (All/Active/Idle), detail
  modal, instant activation (async, SSE-driven status updates)

### Audio Software Management

Quick filter (All/Installed/Updates), restart-required badge, documentation
links per package, per-arch support badges.

### Configuration Editor

Service status badges (Running/Stopped/Failed), diff preview before save,
restart-after-save toggle, backup management. Generic JSON/INI/XML/Libconfig
editor via CodeMirror.

### Systemd Overrides

RT presets (Audio Optimized / Reset to Defaults), OOM Score Adjust, CPU Weight,
diff preview before save.

### Performance Monitoring

CPU governor management, throttle detection badge, latency and network stability
tests with 10-result history, RT process monitor (SCHED_FIFO/RR detection).

### System Administration

Terminal (full interactive PTY shell in browser via WebSocket), backend restart,
OS reboot (with password confirmation), role-based access (admin/user/guest).

### Mobile & PWA

- Touch-first gesture navigation: edge swipes for sidebar/panel, vertical
  "molette" for fast tab cycling, gallery content swipe
- View Transitions API between tabs (direction-aware)
- GPU-accelerated gestures (will-change, RAF batching, passive listeners)
- In-app splash screen, offline indicator, intelligent cache warming
- iOS: safe-area insets, notch handling, rubber-band prevention, PWA splash
  screens (40 device-specific tags)

### Security

- mTLS / PKI: optional nginx mutual TLS client certificate authentication
- Guest role enforcement across all tabs and API endpoints
- CSP hardening, hidden source maps
- Security lock: blocks UI rendering without valid session

### Performance & Architecture

- Event-driven pipeline monitoring (inotify + D-Bus signals, replacing 2s
  polling — CPU drops to near zero at idle)
- Lazy loading, IntersectionObserver pause, Lit chunk splitting
- Backend: `orjson` (5× JSON), `uvloop`, Pydantic v2 `__slots__`, unified
  TTL cache, parallel pipeline construction
- Frontend: `content-visibility: auto` on inactive tabs, concurrent queue
  operations, MPD `command_list` batching, MPD `window` server-side limits
- 3 themes: Slate, Minimal, Gravity

### Codebase Quality

- 54 Lit 3.0 Web Components (Atomic Design: atoms/molecules/organisms/pages)
- Stylelint Phase 3: all CSS files lint-clean, Husky pre-commit hook
- Unified TTL cache replacing 15 ad-hoc implementations
- Dead code audit (frontend + backend), formatter consolidation
- Full CSS custom properties architecture with design tokens

---

## 0.9.0 — 2026-03-06

Full-stack rewrite. Frontend migrated from vanilla JS to **Lit 3.0 Web
Components** (54 components, Light DOM, Storybook 10, Vite 7). Backend moved to
**native D-Bus** (`dbus-fast`) with JWT authentication, adaptive monitoring
(2s→30s intervals, 40-60% CPU reduction at idle), and 9 modular FastAPI
services. Dual-layer security (API key + JWT RBAC), BCrypt hashing, role-based
access (Admin/User/Guest). WCAG 2.1 Level AA accessibility.
