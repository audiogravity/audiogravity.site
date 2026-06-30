# Changelog — Audiogravity

All notable changes to Audiogravity (core, ui, license server, installers
and this landing) are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed
- **[ops] Deployment nomenclature renamed `frontend`→`ui` and `backend`→`core`** — build/packaging scripts (`build-core.sh`, `build-core-package.sh`, `build-ui-package.sh`, `dev-core.sh`), release assets (`audiogravity-core-<ver>-<arch>.tar.gz`, `audiogravity-ui-<ver>.tar.gz`) and public install scripts (`install-core.sh`, `install-ui.sh`) now use the new names. Old release assets from past versions keep their original names.
- **[core] systemd unit `ag-backend-server` → `ag-core-server`** — data directory `/opt/audiogravity/backend` → `/opt/audiogravity/core` (`AUDIOGRAVITY_HOME`). The service-metrics map key exposed over SSE renamed `backend` → `core`. The `sudo systemctl restart ag-core-server` path is covered by the existing generic `systemctl` sudoers rule (no new alias needed).
- **[ui] systemd unit `ag-frontend-server` → `ag-ui-server`** — deploy directory `/var/www/audiogravity-frontend` → `/var/www/audiogravity-ui`; version constant `FRONTEND_VERSION` → `UI_VERSION`; dev proxy env var `BACKEND_PORT` → `CORE_PORT` (`dev.sh` + `vite.config.js`).

### Added
- **[ops] `scripts/migrate-deploy-layout.sh`** — standalone, idempotent migration for hosts on the old layout. Run once as root *before* reinstalling: it backs up the existing layout (`tar`), stops/removes the old units, renames `/opt/audiogravity/backend`→`/opt/audiogravity/core` and `/var/www/audiogravity-frontend`→`/var/www/audiogravity-ui`, and rewrites `AUDIOGRAVITY_HOME` — preserving `.env`, secrets, users and tokens. Works on single-host and split-host topologies (migrates only the component present locally). `/etc/audiogravity` is left untouched.

### Fixed
- **[core] UPnP renderer — auto-reconnect race condition** — after `connect()` completes, the manager checks whether the renderer was removed during the async call and tears it down cleanly if so; prevents a connected/disconnecting oscillation when a renderer is removed while a reconnect is in progress.
- **[core] player — active UDN not persisted when MPD output selection clears it** — `select_mpd_output` now calls `_save_config()` in the else branch so the cleared active UDN survives a restart.
- **[core] track_number missing for Qobuz, Tidal and MinimServer streams** — `now_playing.py` reads `track_number` from `ext_stream_meta` even when MPD already has a title; `library/service.py` registers `track_number` for all Qobuz, Tidal and UPnP album queue paths; `library/upnp_service.py` extracts `upnp:originalTrackNumber` from DIDL-Lite with a safe `int()` guard against empty strings.
- **[ui] fullscreen player — source badge moved onto cover art** — the origin badge (❖ QOBUZ / ❖ TIDAL / ❖ UPNP) now appears top-left on the cover art; the track badge (A1 · TRACK 01) appears bottom-left. Duplicate source badge below the cover removed; `• MPD` fallback label removed.
- **[ui] output panel — wording** — section label "UPnP Renderer" → "Audio Output"; button "Scan network" → "Scan renderers"; "Refresh" → "Reload".

## [0.9.8] - 2026-06-29

### Added
- **[core] UPnP renderer — DSD detection** — `RendererStatus.format` is set to `"DSD"` when the current URI has a `.dsf` or `.dff` extension (MinimServer DSD tracks). `PlayerState.format` is populated for native renderers so the fullscreen player shows the DSD lock and hides the volume control automatically via the existing `isDsd()` check.
- **[core] `RendererStatus.renderer_udn`** — new field on `RendererStatus` mirroring the value already injected into the SSE payload; the UI now has the UDN from the HTTP GET response without waiting for the first SSE event.
- **[core] `UPnPRendererService.reachable` / `.uses_local_mpd` properties** — expose the two previously-private attributes as public properties; `get_known()` and `_try_renderer_control()` use these properties instead of accessing `_reachable` / `_uses_local_mpd` directly.
- **[core] `GET /player/origins`** — new endpoint returning the canonical `origin → label` map (`ORIGIN_LABELS`). Clients call it at startup and merge the result into their static fallback, making the backend the single source of truth for origin display labels.
- **[core] signal path — enriched real-time chain display** — `_build_state()` builds the full audio chain dynamically: Source → [Renderer] → [MPD] → [Connector] → DAC. Connector (USB / TOSLINK) inserted before the DAC. UPnP renderer prepended when active. Audio source (Qobuz, Tidal, Radio, Library…) prepended from `origin`. New `uses_local_mpd: bool` field in `RendererStatus` distinguishes upmpdcli (bridges to local MPD) from native network renderers (Marantz, Linn…) — for those, the signal path is `Source → Renderer` only.
- **[ui] fullscreen player — signal path replaces separate renderer badge** — the signal path chain (e.g. `• Qobuz → • music.#1 → • MPD → • USB → • Heed Abacus`) is now built entirely by the backend and rendered as individual steps; the previously separate `→ music.#1` overlay badge has been removed.
- **[ui] mini player — renderer badge in source row** — when a UPnP renderer is active, a `→ renderer_name` badge appears in the source row; the USB/TOSLINK connector badge is hidden in that state (already visible in the fullscreen signal path).
- **[core] Qobuz — streaming proxy** (`GET /qobuz/stream/{track_id}`) — stable, never-expiring URL for UPnP renderers; resolves HMAC-signed CDN URL just-in-time on each renderer fetch. Endpoint is public (no api_key required). Pass-through FLAC, no transcoding, same design as the existing Tidal proxy.
- **[core] UPnP renderer — NEXT / PREV** — `POST /upnp-renderer/next` and `/prev` skip to the next or previous track in the active renderer queue. Returns 409 if no queue is active, already at boundary, or a transition is in progress. Qobuz proxy URLs are stable so PREV can re-request an already-played track without re-signing.
- **[ui] fullscreen player — NEXT / PREV routed to renderer** — when a renderer queue is active, the NEXT / PREV transport buttons route through `POST /player/control`; `can-next` / `can-prev` are derived from queue position so buttons are correctly disabled at boundaries.
- **[core] UPnP renderer — multi-track queue playback** — `play_queue()` sends a full album to the renderer via `SetAVTransportURI` + `SetNextAVTransportURI` (gapless pre-loading where supported). Tracks are chained automatically: end-of-track detection via NOTIFY polling, `_advance_queue()` re-resolves Qobuz HMAC-signed CDN URLs just-in-time. Supports Qobuz, Tidal and UPnP/MinimServer albums.
- **[core] UPnP renderer — `RendererStatus` queue fields** — `queue_position` (0-based index), `queue_total`, `queue_next_title`, `queue_next_artist`, `queue_next_album`, `queue_next_cover_token` exposed in `GET /upnp-renderer/status` and `renderer_status` SSE event.
- **[ui] fullscreen player — "Up next" for renderer queue** — when a renderer queue is active, the "Up next" strip below the controls shows the next track's title, artist and cover art, updated in real time via the `renderer_status` SSE event (no MPD queue call needed).
- **[core] UPnP renderer — `RendererManager` multi-renderer pool** — replaces the singleton `UPnPRendererService`. Manages a `dict[udn → UPnPRendererService]`; exactly one renderer is active at a time (policy, not architecture). Config persisted in `upnp_renderer_known.json`; migrates silently from the legacy single-renderer format. Exposes `GET /upnp-renderer/known`, `get_active_service()`, `connect(renderer)`, `disconnect(udn)`, `discover()`. Auto-reconnect background task with exponential backoff (30 s → 5 min).
- **[core] UPnP renderer — UDN-based route architecture** — all renderer routes reworked to `/upnp-renderer/{udn}/action`. Manager-level: `GET /discover`, `GET /known`. Per-renderer: `GET|PUT|DELETE /{udn}/connection`, `GET /{udn}/status`, `POST /{udn}/play|next|prev|stop|pause|seek`, `PUT /{udn}/volume`, `POST /{udn}/notify`. Route `PUT /bypass` removed.
- **[core] UPnP renderer — `resume()` method** — resumes playback from PAUSED or STOPPED without loading a new URI. Called by the native-renderer transport fallback when Play is pressed and the renderer already has a track loaded.
- **[core] player — native renderer transport fallback** — `_try_renderer_control()` dispatches toggle/next/prev/stop/seek to a non-local-MPD renderer (ARM UpMPd, Marantz, Linn…) when `get_now_playing()` returns nothing for that renderer. Wired in both `control()` paths: explicit `source_id` branch and auto-resolve branch.
- **[core] GET /player/outputs** — unified output list: one entry per MPD `audio_output` config block (`type: "mpd_output"`, real device name from MPD `outputs` command) + all known UPnP renderers (`type: "upnp_renderer"`), with live `reachable` and `active` flags. Falls back to a single "Local DAC" entry when MPD is unreachable.
- **[core] PUT /player/mpd-output/{output_id}** — enables one MPD audio output exclusively (all others disabled) and disconnects any active UPnP renderer. `output_id` is the MPD `outputid` integer. Returns 503 when MPD is unreachable.
- **[core] player — native renderer state when local pipeline is idle** — `_build_native_renderer_state()` provides title, artist, album, cover art, transport state, `output_label`, and `signal_path` when a non-local-MPD renderer is active but `get_now_playing()` returns nothing. Fixes "Nothing playing" and "No output selected" with a native ARM renderer.
- **[core] RendererStatus — `cover_token` and `can_seek` fields** — `cover_token` exposes the current track's cover art token so the fullscreen player can render cover art for a native renderer; `can_seek` exposes AVTransport seek capability for the playback controls.
- **[core] Push notifications — temperature and service-down alerts** — `notify_temperature_alert()` fires when CPU exceeds 85°C (15-min cooldown); `notify_service_down()` fires on `active → failed` systemd state transition (stale states pruned each cycle to prevent false positives on re-registration).
- **[core] radio → renderer routing** — `RadioService.play()` now routes to the active UPnP renderer via `play_queue()` (AVTransport) when one is connected. Falls back to local MPD only when no renderer is active.
- **[core] `DELETE /upnp-renderer/{udn}`** — permanently removes a renderer from the known list (disconnects if active, clears from `upnp_renderer_known.json`). Distinct from `DELETE /{udn}/connection` (disconnect only, keeps in list).
- **[ui] UPnP renderer card — swipe-to-delete** — left-swipe gesture on an inactive renderer row reveals a red "Remove" zone; completing the swipe (≥ 140 px) calls `DELETE /upnp-renderer/{udn}` and removes the row. Uses the Pointer Events API (same pattern as `ag-radio-card.js`). The active output row is not swipeable.
- **[ui] PWA — App Shell precaching** — vite-plugin-pwa (injectManifest) precaches all Vite-hashed JS/CSS/image assets at SW install (~1 MiB); first load after install is fully offline-capable on Chrome/Android.
- **[ui] PWA — differentiated cache strategies** — cache-first for hashed Vite assets and version-pinned CDN (cdn.jsdelivr.net); stale-while-revalidate for Google Fonts and static images; network-first for HTML navigation.
- **[ui] PWA — install prompt (Android/Chrome)** — compact banner when Chrome offers installation (`beforeinstallprompt`); dismissal persisted 30 days via `localStorage`; complete rewrite of `pwa-install-prompt.js` (English, CSS tokens, no duplicate SW handler).
- **[ui] PWA — offline UI** — last known player state persisted to `localStorage` (5 s debounce); cold offline reload restores the mini-player instead of showing an empty screen; discrete `Offline` badge in the source row.
- **[ui] PWA — `Link: rel=preload` response headers** — `serve_https.py` emits preload hints for critical JS/CSS chunks so the browser fetches them in parallel without waiting for the HTML parser.
- **[ui] PWA — `apple-mobile-web-app-title`** — short label for the iOS home screen icon.
- **[ui] build — granular bundle splitting** — main chunk reduced from 570 KB to 413 KB (−27%); 6 stable independent chunks: `lit`, `icons`, `atoms`, `nowplaying`, `streaming`, `library-core`.

### Changed
- **[core] Steering — renderer pre-disconnect** — `switch_output()` now disconnects a local renderer (`uses_local_mpd=True`, e.g. upmpdcli) before switching the ALSA device. Native/distant renderers (`uses_local_mpd=False`) are left running — their audio stack is independent of AG's ALSA configuration.
- **[core] `GET /player/outputs` — `local_active` during reconnect window** — MPD outputs now show `active: true` when the persisted renderer is selected but not yet reachable (auto-reconnect still pending at startup), matching actual audio routing.
- **[core] UPnP NOTIFY after disconnect** — orphaned NOTIFY requests (arriving after `disconnect()` but within the UPnP subscription TTL) now return HTTP 200 instead of 404, preventing upmpdcli from treating the subscription as lost.
- **[core] `_try_renderer_control()` — uses_local_mpd short-circuit** — `uses_local_mpd` is now checked via the new property before calling `get_status()` (no await); `get_status()` is only called for the `toggle` action which needs `transport_state`.
- **[core] `select_mpd_output` — stale `_active_udn` guard** — if `_active_udn` is set from persisted config but the service is not yet in `_services` (auto-reconnect pending), `_active_udn` is cleared instead of calling `disconnect()` (which would raise `KeyError`).
- **[ui] UPnP renderer card — reworked as multi-output selector** — `ag-upnp-renderer-card` is now the unified output selector, loading from `GET /player/outputs`: one row per physical MPD audio output (USB, TOSLINK…) then all known UPnP renderers. Clicking a physical output calls `PUT /player/mpd-output/{output_id}` (enables exclusively, auto-disconnects renderer); clicking a renderer calls `PUT /{udn}/connection`. Active renderer shows Disconnect button + volume slider. States: Active (green) / Reconnecting (orange) / Idle (grey). SSE sync updates `active`/`reachable` in the list without full reload.
- **[core/ui] UPnP renderer — bypass mode removed** — replaced by the output manager pattern: selecting Local DAC disconnects the renderer; re-selecting the renderer reconnects it. Endpoint `PUT /upnp-renderer/bypass` removed. Field `bypassed` removed from `RendererStatus`.
- **[ui] fullscreen/mini player — renderer references updated** — bypass conditions removed; routes updated to UDN-based API.

### Fixed
- **[ui] mini player — cover art popover broken image** — the detail popover (`np-detail-cover`) now applies the same `_brokenCovers` check as the thumbnail; images that failed to load (404 / network error) are skipped in the popover instead of showing a broken image icon. The `@error` handler is also added on the popover `<img>` to capture failures that occur before the thumbnail has had a chance to error.
- **[core] UPnP renderer — `connect()` UDN mismatch** — `POST /upnp-renderer/{udn}/connection` was looking up the service by the path parameter instead of the request body `udn`, causing a KeyError (HTTP 500) when they differed.
- **[core] player — `PUT /player/mpd-output/{output_id}`** — unknown `output_id` now returns 404 instead of silently disabling all outputs; existence check runs before the batch MPD command.
- **[core] UPnP renderer — queue index underflow** — concurrent `play_queue()` + `_advance_queue()` could decrement `_queue_idx` to −1 on rollback; guard now requires `_queue_idx > 0` before decrementing.
- **[core] library — Qobuz single-track to renderer** — `qobuz_queue()` now calls `play_queue([QueueEntry(…)])` instead of the removed `play()` method; cover token forwarded.
- **[core] sysinfo — temperature alert push spam** — cooldown timestamp is advanced before the push attempt so a misconfigured push service cannot trigger repeated alerts on the same event.
- **[core] Qobuz proxy — shared HTTP session** — `GET /qobuz/stream/{track_id}` reuses the shared `aiohttp.ClientSession` pool; per-request headers forwarded on `.get()` call, no session closed between requests.
- **[core] player — native renderer detection** — `_try_renderer_control()` and `_build_native_renderer_state()` use the public `status.uses_local_mpd` field from `RendererStatus` instead of the private attribute.
- **[ui] renderer card — SSE unknown renderer** — when a `renderer_status` SSE event arrives with a `renderer_udn` not yet in the known list, the card now triggers a reload instead of silently discarding the update.
- **[ui] library sources — CSS tokens** — replaced hardcoded `10px` with `var(--spacing-xs)`, removed duplicate `user-select: none` rule, documented intentional `#ffffff` on error background.
- **[ui] UPnP renderer card — double "Active" badge via SSE path** — `_onStatusEvent` did not clear `active` on the previously active renderer when a new one received `connected: true`. Fixed: when `isNowActive=true`, all non-target renderers in `_known` now force `active: false`.
- **[core] UPnP renderer — `disconnect()` removed renderer from known list** — `disconnect()` filtered the renderer out of `_services` pool AND from `_known`, making it disappear from the card after disconnect. Fixed: only `_active_udn` is cleared; the renderer stays in `_known` so it can be re-selected without re-scanning.
- **[ui] UPnP renderer card — list not refreshed after backend restart** — the backend publishes a `renderer_status` SSE event on startup before the frontend SSE stream reconnects, so the event was missed. Fixed: the card now listens to `window.EventEmitter 'connection-status'` and calls `_load()` on every SSE reconnection.
- **[core] player — 503 on Play with native (ARM) renderer** — when the fullscreen player sent `source_id` explicitly, `control()` found nothing in `get_now_playing()` and returned 503 without reaching the renderer fallback. Fixed: `_try_renderer_control()` fallback now wired in both branches of `control()`.
- **[core] UPnP renderer — `_publish_status(force=True)` didn't update the hash baseline** — on forced publishes, `_last_sse_hash` was not updated because the hash computation lived inside the `if not force:` block. Hash is now always computed and `_last_sse_hash` always updated; only the early-return dedup check is gated on `not force`.
- **[core] UPnP renderer — `_resubscribe_and_refresh()` didn't restore reachability after SID recovery** — `_handle_update_result(success=True)` was not called after a successful `async_update()` post-resubscribe; `_reachable` stayed `False` and the renderer card showed "offline" for up to 30 s after the SID mismatch was resolved.
- **[core] UPnP renderer — `_retreat_queue` pre-decrement unguarded against `stop()` race** — `stop()` can clear `_queue` and reset `_queue_idx = 0` between the public `retreat_queue()` guard check and the unconditional `_queue_idx -= 1` inside `_retreat_queue()`. Guard added before the decrement.
- **[core] player — renderer included in signal path during startup reconnect window** — `_build_state()` used only the `connected` flag; guard tightened to require `connected AND reachable`.
- **[core] library — `asyncio.TimeoutError` not caught in MPD queue-list endpoints** — a stalled MPD during restart raised `asyncio.TimeoutError` which bypassed the `(OSError, ConnectionRefused, BrokenPipe)` empty-list handler and returned HTTP 500.
- **[ui] fullscreen player — "Up next" strip showed stale track after renderer disconnect** — `_nextTrack` was only cleared when the renderer sent `queue_next_title=null` while still connected. Cleared explicitly on disconnect.
- **[ui] fullscreen player — cover error token not reset between consecutive album tracks** — `_coverErrorToken` was only cleared on page reload or full source reconnect. Token is now reset on every track-title or source change.
- **[ui] fullscreen player — idle renderer badge missing when nothing is playing** — the source row was conditioned on `origin || source_name || hasSignal`, all of which are falsy when the renderer is idle. Condition extended to include `_rendererActive`.
- **[ui] mini player — connector badge hidden for upmpdcli (local-MPD renderer)** — the badge was unconditionally hidden when any renderer was active. upmpdcli routes audio through the local MPD stack, so the physical connector IS in the chain. Visibility now also passes when `_rendererStatus?.uses_local_mpd` is true.
- **[core] signal path — radio source shows "Radio" not the station name** — `origin_name` for radio is content metadata (station name), not a chain step. Canonical label now comes from the `ORIGIN_LABELS` map keyed on `origin`.
- **[core] UPnP renderer — `_retreat_queue` rollback unsafe when `stop()` fires mid-retreat** — mirror of the earlier `_advance_queue` fix: guard `if self._queue:` added before rollback.
- **[core] UPnP renderer — `_uses_local_mpd` stale after disconnect or failed reconnect** — `disconnect()` now resets `_uses_local_mpd = True`; `get_status()` re-derives it from the saved location URL when `_dmr is None` via the extracted `_is_local_renderer()` helper.
- **[core] player — renderer status error swallowed silently in `_build_state()`** — bare `except Exception: pass` replaced with `logger.debug(..., exc_info=True)`.
- **[core] Roon — suppress ERROR logs when roonbridge service is stopped** — `connect()` now gates on `ActiveState` via the existing D-Bus client before creating `RoonApi`; the daemon threads that emit `ERROR: Connection is not (yet) ready!` are never started.
- **[core] Roon — TCP pre-check before mDNS discovery** — `_sync_connect()` now verifies the configured host is reachable (port 9330) before running `RoonDiscovery.first()`, which can block for several seconds when Roon Core is offline.
- **[core] Qobuz proxy — Range headers relayed end-to-end** — `GET /qobuz/stream/{track_id}` now forwards the `Range` request header to the CDN and relays `Content-Range`, `Content-Length` and `Accept-Ranges` response headers with the correct status code (206 Partial Content).
- **[core] UPnP renderer — `_check_queue_advance` stacked `create_task` on rapid NOTIFYs** — fixed by storing the task reference in `_advance_task` and skipping if the previous task is still running.
- **[core] UPnP renderer — `_ext_stream_key` missed `/qobuz/stream/` proxy URLs** — Qobuz proxy URLs (path `/qobuz/stream/{id}`) fell through to the raw URL fallback, causing a spurious AVTransport art fetch. Added a path-anchored check before the CDN `?eid=` query-param check.
- **[core] UPnP renderer — `_advance_queue` rollback unsafe when `stop()` fires mid-advance** — rollback now only applies when the queue is still populated.
- **[core] UPnP renderer — `_publish_status(force=True)` computed JSON hash unnecessarily** — hash computation now skipped in the force path.
- **[core] UPnP renderer — renderer pinged every 30 s in SUBSCRIBE mode** — ping interval extended to 60 s while the SSE heartbeat remains 30 s, halving outbound HTTP GETs to the renderer.
- **[core] Qobuz — `ClientSession` created per API call** — `get_stream_url()`, `handle_callback()`, and `validate_token()` migrated to `get_shared_session()` from `core.http`.
- **[core] UPnP renderer — NOTIFY SID mismatch after AG restart** — `handle_notify()` now detects 412, schedules `_resubscribe_and_refresh()` — a background task that unsubscribes, re-subscribes (fresh SID), and calls `async_update()` immediately so badge and transport state are accurate without waiting for the heartbeat.
- **[core] Qobuz — single-track play to renderer used expiring CDN URL** — `qobuz_queue()` for a single track now uses the stable proxy URL like the multi-track album path.
- **[core] Qobuz proxy — CDN stall leaked aiohttp session indefinitely** — `ClientTimeout(total=None)` meant a stalled CDN connection held the session open forever. Fixed: `sock_read=300`.
- **[core] Qobuz proxy — network errors returned HTTP 500 instead of 503** — `except RuntimeError` did not catch `aiohttp.ClientConnectorError` / `asyncio.TimeoutError`. Fixed: `except Exception`.
- **[core] UPnP renderer — NEXT / PREV returned ok:True when transition already in progress** — public methods now raise `RuntimeError("Queue transition in progress")` → router returns 409.
- **[core] UPnP renderer — spurious URI-change detection after explicit play** — `_prev_track_uri` was not updated after `_advance_queue()` started a track explicitly; the incoming PLAYING NOTIFY was misidentified as a natural transition, double-advancing the queue. Fixed by anchoring `_prev_track_uri` to the URI just played.
- **[core/ui] UPnP renderer — reachability tracking** — renderer card now shows 🟠 Unreachable when the device goes offline (2 consecutive heartbeat failures) and recovers to 🟢 Connected automatically. Field `reachable` added to `RendererStatus`.
- **[core] UPnP renderer — auto-reconnect retry loop** — on backend startup, auto-reconnect now retries with exponential backoff (30 s → 60 s → … → 5 min ceiling) instead of giving up after one attempt.
- **[ui] UPnP renderer — `renderer_status` SSE event missing from worker** — `sse-worker.js` did not register a listener for `renderer_status` events, so the renderer card never received real-time status updates.
- **[core] library — MPD queue/albums return empty when MPD is stopped** — `GET /library/queue` and `GET /library/albums` now return an empty list instead of HTTP 500 when MPD is unreachable.
- **[core] UPnP renderer — disconnect now stops playback** — `disconnect()` calls `AVTransport Stop` before unsubscribing so the renderer stops playing immediately.
- **[ui] now-playing — radio cover art fallback** — mini-player shows the music-note placeholder instead of the broken image icon when the cover proxy returns 404; fullscreen player uses a hidden probe `<img>` to detect silent CSS `background-image` 404s and shows the placeholder.
- **[ui] PWA — `skipWaiting()` removed from SW install event** — prevented chunk 404s on update (new SW was taking control before the page reloaded with new asset hashes).
- **[ui] PWA — SW update reload loop** — `controllerchange` triggers a single conditional reload guarded by `sessionStorage`; toast correctly says "Updating…".
- **[ui] PWA — SWR background refresh lifetime** — `fetchPromise` now covered by `event.waitUntil()` so the SW is not killed before `cache.put()` completes.
- **[ui] PWA — isCDN too broad** — replaced `url.origin !== location.origin` with explicit `CDN_SWR` / `CDN_IMMUTABLE` Sets; mutable cross-origin resources no longer routed into stale-while-revalidate.
- **[ui] PWA — dead `icomoon.woff` path** — removed non-existent `/fonts/icomoon.woff?1zo0jr` from `CACHE_URLS`.
- **[ui] PWA manifest — broken screenshot references** — removed `screenshots` field pointing to non-existent files (silent 404, degraded Chrome install dialog).
- **[ui] build — `@lit/context` chunk assignment** — `@lit/context` and `@lit/reactive-element` now land in the stable `lit` chunk instead of `main`.
- **[ui] push notifications — `push-manager.js`** — replaced raw `fetch()` with `apiGet`/`apiPost` for consistency; `PushSubscription` destructured explicitly via `toJSON()` before posting.

### Refactored
- **[core] `mpd_client.fetch_outputs()`** — MPD audio output parsing (previously `_fetch_mpd_outputs()` inline in `modules/player/router.py`) moved to `core/mpd_client.py` as a public `fetch_outputs(pipeline)` function. Router now calls `mpd_client.fetch_outputs()`. The router no longer parses MPD wire format directly; the helper is independently testable.
- **[core] `_try_renderer_control()` — single dispatch block** — removed the two-phase approach (separate `if action == "toggle"` to fetch transport state, then a second `if/elif` dispatch); merged into one `try` block. `transport_state` intermediate variable eliminated.
- **[core] `LibraryService.is_mpd_source()`** — new public method replacing direct calls to the private `_mpd_port()` from `modules/library/router.py`. Two call-sites in the router updated.
- **[ui] `fetchActiveRendererStatus()`** — the `known → active UDN → status` bootstrap chain, previously copy-pasted identically in `ag-now-playing.js` and `ag-now-playing-fullscreen.js`, extracted into `library-store.js` as a shared async helper.
- **[ui] fullscreen player — renderer transport routing** — `_control()` now sends all transport actions (including `next`/`prev`) through `POST /player/control`. The UI-side shortcut that routed renderer queue next/prev directly to `POST /upnp-renderer/{udn}/next|prev` has been removed.
- **[core] `PlayerService._get_active_renderer_svc()`** — new private helper centralises the `get_container().get(RendererManager).get_active_service()` lookup, previously repeated verbatim in three methods.
- **[core] `PlayerService._renderer_queue_nav()`** — new static helper returns `(can_next, can_prev)` from a `RendererStatus`, replacing duplicated `queue_total is not None and queue_position is not None` guards.
- **[core] `_save_config()` dict comprehension** — simplified from `{**{k: v for k, v in r.items() if k != "active"}, ...}` to `{**r, "active": ...}`.
- **[ui] Remove stale `!bypassed` guards** — `bypassed` was removed from `RendererStatus`; all six `!data.bypassed` / `!rs.bypassed` guards in `ag-now-playing.js` and `ag-now-playing-fullscreen.js` replaced with the simpler `connected` check.
- **[core] `_upsert_known()`** — renderer dict built once before the if/else branch instead of duplicated in each arm.
- **[core] `_make_stream_on_play()`** — extracted shared static method replacing `_make_qobuz_on_play` / `_make_tidal_on_play` copy-paste closures in `library/service.py`.
- **[core] service monitoring — set construction** — replaced `set(dict) - set(dict)` (two allocations per 10 s tick) with a list comprehension over the dict keys.
- **[ui] `_rendererCanNext` / `_rendererCanPrev` getters** — replaced inline IIFEs in `ag-now-playing-fullscreen.js` template with named getters; return `null` when no renderer queue is active so the template falls back to player state.

## [0.9.7] - 2026-06-26

### Fixed
- **[ui] library — radio form font harmonization** — `type="url"` inputs changed to `type="text" + inputmode="url"` so Safari/iOS no longer renders the value in monospace; `::placeholder` inherits typography from the input element; `image_url` field now validates with `pattern="https?://.+"`.
- **[ui] library — "Add custom station" button border** — dashed border changed to solid.
- **[ui] library — genre/country select font size** — increased from `font-size-xs` to `font-size-sm` for readability in the native dropdown.
- **[ui] sources — redundant source descriptions removed** — Roon, Tidal, Qobuz source cards no longer repeat the source name as description; MPD keeps "Music Player Daemon"; Roon active source always shows at least the source name while zones are loading.
- **[ui] sources — Qobuz and Tidal merged under "Streaming Services"** — reduces visual noise; service name shown in each molecule's own header.
- **[ui] sources — `lib-settings-section` CSS class** — decoupled from `lib-hqp-section` so HQPlayer-specific style changes cannot bleed into other sections.

### Added
- **[core] upnp_renderer — UPnP Control Point** — AG can now send audio to any UPnP/DLNA MediaRenderer on the network. New module `modules/upnp_renderer/`: SSDP discovery, AVTransport control (SetAVTransportURI, Play, Stop, Pause, Seek, Volume), SUBSCRIBE/NOTIFY eventing via AG's own FastAPI callback, connection persistence across restarts. Auto-reconnects to the last renderer on startup.
- **[core] upnp_renderer — renderer dispatch in library queue** — `upnp_play()`, `qobuz_queue()` and `tidal_queue()` route to the connected renderer when `action='play'`. MinimServer tracks use URI handoff (renderer pulls directly from CDN/MinimServer). Qobuz uses self-authenticated CDN URL (no proxy). Tidal uses the existing DASH→FLAC proxy with LAN-reachable IP.
- **[core] upnp_renderer — SSE `renderer_status`** — live renderer state published on the `dashboard` SSE channel on every NOTIFY event, with a 30 s heartbeat fallback for renderers that don't SUBSCRIBE reliably.
- **[core] library — `GET /library/upnp-browse` and `GET /library/search` now use `location` parameter** — replaces `control_url`; `location` is the device description URL used by async-upnp-client. Breaking change for UI clients.
- **[core] library — `upnp_service.py` rewritten with async-upnp-client** — replaces hand-rolled SOAP/SSDP with `async-upnp-client` (python-didl-lite, defusedxml). Adds `DmsDevice` profile for ContentDirectory Browse/Search with proper DIDL-Lite parsing.
- **[core] `/tidal/stream/` added to PUBLIC_PATH_PREFIXES** — UPnP renderers can fetch the Tidal proxy without api_key in the URL (avoids key exposure in plaintext AVTransport traffic).
- **[core] `core/utils/net.py`** — shared `get_local_ip()` helper (cached, replaces 3 duplicates).
- **[ui] ag-upnp-renderer-card** — new molecule in the Sources panel: discovery, connect/disconnect, live playback status, Play/Pause/Stop/Volume controls.
- **[ui] renderer routing badge** — `→ music.#1` badge in mini player and fullscreen player when a renderer is connected.
- **[ui] `subscribeRendererStatus`** — shared SSE subscription in `library-store.js` (replaces 3 independent `window.addEventListener` calls).
- **[ui] library-api.js `upnpPlay`** — routes MinimServer browser plays through `/library/upnp-play` which now dispatches to renderer when connected.

### Changed
- **[core] `async-upnp-client`** added to `requirements.txt` (pure Python, `none-any` wheels, Nuitka-compatible).
- **[core] `upnp-browse` param renamed** — `control_url` → `location` in router and service.

## [0.9.6] - 2026-06-25

### Fixed
- **[core] audio_pipeline — cover art missing or wrong when playing via upmpdcli renderer** — when an external UPnP control point (BubbleUPnP, Kazoo…) pushed music or radio to upmpdcli, AG fell back to MusicBrainz/iTunes which returned the wrong album cover or nothing. A new `upmpdcli_cover` module queries upmpdcli's AVTransport `GetPositionInfo` to retrieve the exact `upnp:albumArtURI` the controller sent (including radio station logos). Discovery is restricted to the local machine to avoid picking up network renderers (Marantz, etc.). Tidal and Qobuz proxy streams are excluded from the AVTransport path. Miss backoff (60 s TTL) and a provisional sentinel prevent SSDP storms on concurrent SSE ticks.
- **[core] hqplayer — WARNING flood at startup when HQPlayer not yet configured** — `get_status()` attempted a TCP connection even when `_host` was `None` (not yet configured via UI), generating a warning on every poll. Guard added: returns `HQPlayerStatus(available=False)` immediately without attempting connection. Regression from `0409bb5`.
- **[core] hqplayer — WARNING flood during DSD playback startup** — `_fetch_status()` on TCP error did not cache the failure result, causing immediate retries on every poll cycle instead of respecting the 2 s TTL backoff. Failure path now caches `HQPlayerStatus(available=False)`. Regression from `c230b1b`.
- **[core] hqplayer — `naa_available` field added to `/hqplayer/connection`** — the connection response now includes whether the local `networkaudiod` service is active, queried via D-Bus (no subprocess). `ServicesManager.is_service_active()` added as the canonical D-Bus ActiveState helper.
- **[ui] hqplayer — connected state reflects full chain (HQPlayer + NAA)** — the card now shows "Connected" only when both HQPlayer is reachable and `networkaudiod` is active. Shows "NAA offline" when HQPlayer is reachable but NAA is down. "Use as output" toggle hidden when NAA is offline. Toggle flag cleared automatically via `updated()` lifecycle when NAA availability drops, guarded against transient fetch failures (`=== false` not falsy). `naa_available` updated in real-time via `service-metrics-sse` SSE event (serviceId `"hqplayer"`, no round-trip to `/hqplayer/connection`).
- **[core] services — `is_service_active()` handles absent `ActiveState` key** — D-Bus response dict uses a filter comprehension; if both interfaces fail the key is absent. Changed `props.get("ActiveState") == "active"` to `props.get("ActiveState", "inactive") == "active"` to avoid false-inactive on empty response.
- **[core] hqplayer — `_naa_available()` logs D-Bus failures at DEBUG** — bare `except Exception: return False` was silent; now logs the exception before returning False. Service name extracted to `_NAA_SERVICE` constant.
- **[ui] ag-tabs — bell animation missing on iOS** — CSS `transform` animation applied directly on an `<svg>` element is not supported by iOS WebKit; the bell icon is now wrapped in a `<span>` that carries the animation.
- **[ui] ag-tabs — admin tab stat reverted to connected/total ratio** — the previous change showed only the total account count, losing the connected context; reverted to `num/den` format (active sessions / total accounts).
- **[ui] beta badge missing in production** — `.env.production` was absent from the build host; `VITE_BETA=true` was not substituted by Vite at build time, causing the badge to be tree-shaken out of the bundle.
- **[ui] ag-tabs — bell animation suppressed on iOS when OS Reduce Motion is active** — the bell had no `prefers-reduced-motion` override; added explicit restore of the animation when the app animations toggle is ON, following the same pattern as status dots. Added `will-change: transform` for GPU compositing.
- **[ui] mini-player / fullscreen — active source not followed automatically when multiple sources play** — both players now auto-follow the backend-active source by default; the user can override by tapping a dot or swiping, and the override is lifted when the chosen source stops playing.
- **[ui] mini-player — dot click did not suspend auto-follow** — tapping a dot set `_activeSourceIdx` without setting `_userSourceOverride`, so the next SSE tick silently reverted the selection to the auto-followed source.
- **[ui] mini-player — `prevShownId` read from new items after clamp** — the override-lift check identified the wrong source when the user's chosen source disappeared and the item list shrank, causing the override to stay active indefinitely. Fixed by capturing `prevShownId` before `this._items` is replaced.
- **[ui] fullscreen — player stuck on stopped source after override lift** — when the override was lifted on the same SSE tick as `state.playing=false` (dead source's final tick), `_followSource` was never called because the `state.playing &&` guard failed. Now immediately follows `_sources.find(s => s.playing)` when the override is lifted.
- **[ui] mini-player — `apiGet` missing from import** — `apiGet` was called in `_fetchAlbumTracks` but only `apiPost` was imported, causing a `ReferenceError` when the album detail popover was opened.
- **[core] player — bitrate no longer displayed for ALAC, FLAC, TIDAL and Roon sources** — a `_LOSSLESS_FILE` filter introduced in the Qobuz commit (78ef364) combined with a codec-detection fix (828ee91) silently hid the bitrate for all lossless and streaming sources. The filter is removed; MPD's reported bitrate is now shown for all MPD sources (ALAC, FLAC, WAV, streaming). For sources with no MPD bitrate (Roon, AirPlay), a PCM-equivalent is computed from bit-depth × sample-rate × 2 ch.
- **[core] player — TIDAL bitrate always 0** — MPD reports `bitrate: 0` for the growing FLAC proxy stream (STREAMINFO `total_samples=0` during progressive remux). The DASH manifest's `bandwidth` attribute is now parsed at stream-request time and injected into the format metadata via `ext_stream_meta`, providing the exact bitrate immediately.
- **[core] player — TIDAL format strip showed `—` for format and sample rate during warm-up** — `sample_rate_hz` and `codec` from the DASH manifest were stored in `ext_stream_meta` but never consumed. `audio_pipeline/service.py` now builds a partial `source_format` (`"FLAC | 96kHz"`) from the manifest when MPD's `audio` field is not yet available, so sample rate and codec appear immediately.
- **[core] audio_pipeline — `ext_stream_meta` LRU contract broken on `merge=True`** — in-place dict update did not reposition the entry; merged entries could be evicted before genuinely older ones. Fixed with delete-then-reinsert.
- **[core] tidal — `parse_dash_format` broad `except` could silently drop `bitrate_kbps`** — a `ValueError` on `audioSamplingRate` would discard a successfully parsed `bitrate_kbps`. Each field conversion now has its own try/except; failures are logged at DEBUG level and do not affect other fields.

### Added
- **[core+lic] announcements — broadcast polling** — license server admins can create broadcast announcements (type version/promo/alert/info, optional body/URL/expiry). Active announcements are delivered to AG instances via the existing 24 h `/verify` check-in. A delivery count is shown in the LS admin panel per announcement. AG admin tab shows a Lucide Bell icon (warning color, ring animation) when unread announcements exist; dismissal persists in localStorage.
- **[lic] ls-announcements — admin panel section** — new `ls-announcements` molecule in the LS admin UI with a creation form (type, title, body, URL, expires_at) and a management table (activate/deactivate/delete, delivered count).
- **[ui] ag-announcement-banner** — new light-DOM molecule displaying dismissable banners in the AG Admin tab. Fetches `GET /license/online-status`.
- **[ui] ag-tabs — Admin tab badge** — animated Lucide Bell icon (--color-warning) on the Admin tab when unread announcements exist. Animation follows the global animations toggle. Admin tab stat now shows total account count instead of the meaningless active/total ratio.
- **[lic] campaign mailing** — LS admins can compose and send HTML campaign emails to all active licence holders. Features: visual preview iframe (sandboxed, no test send needed), ls_base_url persisted in settings, concurrent SMTP (Semaphore(5)), campaign history log with recipient count.
- **[lic] GDPR unsubscribe** — stateless HMAC-signed opt-out link injected in every campaign email (`List-Unsubscribe` header + footer). `GET /ls/portal/unsubscribe` sets `email_opt_out=1` without login. `UNSUBSCRIBE_SECRET` separate from `ADMIN_TOKEN` so token rotation doesn't invalidate past links.
- **[lic] ls-mailing — admin panel section** — new `ls-mailing` molecule: compose form, show/hide preview iframe, send to all button with confirmation, campaign history table.

## [0.9.5] - 2026-06-22

### Fixed
- **[core] packages — dry-run always reported success regardless of URL reachability** — `install()` in `ScriptInstaller`, `AptDebInstaller` and `AptRepoInstaller` returned `(True, "Dry-run completed successfully")` unconditionally. Dry-run now sends a HEAD request to the download URL; an unreachable or 4xx/5xx response surfaces as `(False, …)`. `AptRepoInstaller` additionally runs `apt-get install --simulate` to surface dependency conflicts when the package is already in the apt cache.
- **[core] audio_pipeline — HQPlayer stale cache persisted forever after stop** — `_refresh_hqplayer_cache` never wrote `None` to `_hqp_cache` to guard against transient stopped states, but this also prevented clearing the cache when HQPlayer truly stopped (no track loaded). `_get_hqplayer_item` now raises `_HQPlayerTrulyStopped` (private sentinel) on confirmed stop; the cache is explicitly invalidated in that case while network errors keep the stale value.
- **[core] license — per-request `aiohttp.ClientSession` in license router** — `check_key`, `activate_license`, `get_public_config` and the deactivate notify in `delete_license` each created a new `ClientSession` (TCP handshake + TLS) per call. Replaced with `core.http.get_shared_session()`, the same pool already used by `library`, `tidal` and `qobuz`.
- **[core] audio_pipeline — subprocess blocks event loop on NI data fetch** — `_get_local_ni_data()` called `subprocess.run("ip"/"iw")` synchronously from a coroutine, stalling the event loop for up to 3s on every cache miss (TTL was 10s). Calls are now pre-warmed via `asyncio.to_thread` before pipeline construction; TTL raised to 60s.
- **[core] audio_pipeline — HQPlayer volume returned negative integers** — formula `100 * (1 + volume_db / 60)` produced negative values for `volume_db < -60` (e.g. `-140` for muted). Now clamped to `[0, 100]`; `None` when `volume_db` is unknown.
- **[core] audio_pipeline — `cpu_percent()` always returned 0.0** — a new `psutil.Process` instance was created on every cycle; the first call always returns 0.0 without a prior snapshot. Instances are now reused via `_psutil_procs`.
- **[core] audio_pipeline — incoherent double `/proc/asound` read** — `_get_alsa_latency` and `_get_alsa_buffer_fill` each read `status` and `hw_params` independently, yielding different hardware snapshots. A shared `_read_alsa_pcm_state` helper performs a single coherent read.
- **[core] audio_pipeline — ALSA pointer wraparound incorrect on ARM64** — `appl_ptr - hw_ptr < 0` was corrected with `+ 2**32`; on ARM64 `snd_pcm_uframes_t` is 64-bit, causing negative or absurd latencies after ~6h. Fixed with `+ 2**64`.
- **[core] audio_pipeline — `_pid_identify_cache` unbounded** — raw dict with no TTL or size limit; replaced with `TTLDictCache(300)`.
- **[core] audio_pipeline — M4A codec mismatch between modules** — `_enrich_with_topology` mapped `.m4a → ALAC` while `service._query_mpd` mapped `M4A → AAC` for the same file. `_detect_mpd_format` is now the single source of truth; `service.py` imports it directly.
- **[core] audio_pipeline — `_mpd_command` duplicated `core.mpd_client.mpd()`** — redundant implementation removed from `now_playing.py`; all calls go through `core.mpd_client`.
- **[core] audio_pipeline — `_get_mpd_now_playing` used direct Unix socket** — replaced with `core.mpd_client.mpd_batch` (TCP), consistent with all other MPD consumers. `currentsong` + `status` sent in a single connection via `command_list_ok_begin`.
- **[core] audio_pipeline — blocking file I/O in async endpoint** — `open(topology_path)` in `async def get_topology()` blocked the event loop; replaced with `asyncio.to_thread(topology_path.read_bytes)`.
- **[core] audio_pipeline — dead variable + deprecated API** — `now = asyncio.get_event_loop().time()` removed (`now` never used; `get_event_loop()` deprecated since Python 3.10).
- **[core] audio_hw — blocking I/O in async event loop** — `read_text()`, `exists()`, `iterdir()` called directly from coroutines, stalling the event loop on every scan. All filesystem access moved to `_scan_card_dir()` (synchronous method) called via `asyncio.to_thread`; per-card details now fetched in parallel via `asyncio.gather`.
- **[core] audio_hw — exception path poisoned the 60 s cache** — a transient I/O error (e.g. USB hotplug race) fell through to `_cache.set()`, serving an empty or partial device list for the full TTL. The error path now returns without caching.
- **[core] audio_hw — subdevice availability always reported as 1/1** — the `if sub_info_file.exists()` block contained only `pass`; `subdevices_total` and `subdevices_available` were always hardcoded to 1 regardless of actual device state. `sub0/info` is now parsed for `subdevices_count` and `subdevices_avail`.
- **[core] audio_hw — early return did not cache the negative result** — when `/proc/asound/cards` is absent the empty result was returned without `_cache.set()`, causing a `/proc` stat on every subsequent call with no back-off.
- **[core] audio_hw — non-deterministic device ordering** — `iterdir()` returns entries in filesystem order; a `sorted()` call now guarantees stable ordering by `pcmNp` name.
- **[core] hqplayer — `play_uri` / `play_library_item` silently failed on every play attempt** — `_send_batch` passed `allow_empty=False` to all commands including `<Play/>`, which closes the connection without a body; `_read_xml_response` blocked for 3 s then raised `HQPlayerError`. Every HQPlayer playback call failed after loading the queue. Fixed by passing `allow_empty=True` for the `Play` command.
- **[core] hqplayer — `resolve_file_path` rejected all files when `music_root='/'`** — path-traversal guard used `startswith(root + os.sep)` which fails for root `'/'`; replaced with `Path.relative_to()`.
- **[core] hqplayer — `active_rate=0` collapsed to `None`** — `rate if rate else None` treated 0 Hz (DAC idle) as "no rate data"; fixed to `rate if rate is not None else None`.
- **[core] library — `asyncio.get_event_loop()` deprecated in `upnp_service`** — replaced with `asyncio.get_running_loop()` (correct API inside async context, avoids `DeprecationWarning` on Python 3.13).
- **[core] library — `_probe_port` made two HTTP GETs per candidate URL** — body was fetched once, then `_fetch_device` fetched the same URL again; `_parse_device_text()` helper now reuses the first response.
- **[core] library — `_mpd_album_cache` was an unbounded raw dict** — replaced with `TTLDictCache(60)` + `prune_to_size(100)` to prevent unbounded RAM growth on large libraries.
- **[core] library — `get_ext_stream_meta` called twice per HTTP track in `mpd_queue_list`** — result stored once and reused for both display enrichment and cover_token construction.
- **[core] library — Roon `_subkey` race in `roon_queue_list`** — concurrent `run_in_executor` calls both read-modify-write `sock._subkey` without a lock; replaced with `time.time_ns()` as the subscription key.
- **[core] license — `_ping` leaked the aiohttp TCP connection** — `await session.post(...)` without `async with` left the `ClientResponse` unclosed; fixed with `async with session.post(...) as _resp: pass`.
- **[core] license — online `_fetch` treated 4xx (revoked, not found) as "unreachable"** — `resp.raise_for_status()` raised for 4xx and 5xx alike; now 5xx → "unreachable", 4xx → structured status from the LS (e.g. "revoked").
- **[core] license — `start_checker` leaked old background loop on double call** — previous `asyncio.Task` was not cancelled before creating a new one; fixed with cancel guard.
- **[core] license — trial file non-atomic write → false "tampering detected" on crash** — `open(path, 'w'); json.dump(...)` truncates on power loss; replaced with `atomic_write_json` (write-to-temp + rename).
- **[core] license — trial only written to first location on creation** — `any(...)` short-circuited after first success, leaving the fallback location empty; tampering detection now requires all-locations consistency. Fixed with explicit list comprehension.
- **[core] license — `require_full_license` silently bypassed when service not initialised** — `if _service is None: return` allowed all protected endpoints without a license check; now returns HTTP 503.
- **[core] packages — `www.lesbonscomptes.com` domain did not match after `www.` stripping** — `_validate_download_url` strips `www.` before comparison; the set entry had the prefix, causing intermittent failures when set iteration returned that domain first. Changed to `lesbonscomptes.com`.
- **[core] config_validation — blocking subprocess and filesystem I/O in Pydantic validators** — `subprocess.run(['systemctl', ...])` and `Path.exists()` ran synchronously inside field validators on the async event loop, blocking for up to N×5 s per validation request. System-state checks (unit existence, file existence) moved to an async service method using `asyncio.gather + asyncio.to_thread`; validators now only check structure and path safety.
- **[core] config_validation — `depends_on` accepted duplicates silently** — `validate_no_duplicates` covered `start` and `stop` but not `depends_on`; `["a","a"]` was accepted without error. Fixed by extending the validator to all three list fields.
- **[core] auth — `create_user` accepted whitespace-only passwords** — `update_user` rejected passwords where `.strip() == \"\"` but `create_user` did not; `\"      \"` (6 spaces) was hashed and stored. Fixed via a `model_validator` on `CreateUserRequest`.
- **[core] auth — timing oracle on disabled accounts** — `authenticate_user` returned immediately for disabled accounts (~1 ms) vs. burning a dummy bcrypt hash for nonexistent accounts (~250 ms), enabling username enumeration. Disabled-account path now also runs `verify_password(password, _DUMMY_HASH)` to equalise timing.
- **[core] auth — WebAuthn concurrent flows clobbered each other's challenge** — `_pending` was keyed by username only; a second `begin_*` call for the same user overwrote the first challenge regardless of flow type (register vs. authenticate). Key changed to `\"username:kind\"` so both flows can coexist independently.
- **[core] `core/users.py` — `_load_users` read cache outside the lock** — `_cache` and `_cache_mtime` were read without holding `_lock` while `_save_users` wrote them under `_lock`; concurrent async calls could observe a stale cache. `Lock` upgraded to `RLock`; `_load_users` now holds the lock for the full mtime-check + read sequence.
- **[core] audio_app_config — `_run_command` timeout covered only process creation** — `asyncio.wait_for` was applied to `create_subprocess_exec` only; `communicate()` had no timeout and could block the event loop indefinitely on a hung `sudo systemctl restart` or stalled NFS mount. The timeout now wraps `communicate()` and kills the process on expiry.
- **[core] audio_app_config — `restore_backup` broken in production** — `sudo cp /var/backups/.../* /etc/...` was not listed in the sudoers allowlist; every restore failed silently. Added the missing entries to the installer.
- **[core] audio_app_config — backup files world-readable** — `sudo chmod 600 /var/backups/audiogravity/*/*` was not in sudoers; the chmod silently failed, leaving backup files (which may contain MPD passwords or Shairport auth keys) world-readable. Return value now checked; sudoers entry added.
- **[core] audio_app_config — `total_count` in backup list wrong under `limit`** — `BackupListResponse.total_count` was computed from the already-sliced list; callers received `total_count == limit` instead of the real file count. Total is now captured before slicing.
- **[core] audio_app_config — `debounce_task` leaked on shutdown** — the reload task created by the package-event listener was not stored on `self` and therefore not cancelled by `cleanup()`. It now fires `_load_service_map` on a partially-torn-down service on shutdown.
- **[core] audio_app_config — blocking `open()` in async `_load_service_map`** — `audio-config.json` was read synchronously on every package-install reload event; replaced with `asyncio.to_thread`.
- **[core] audio_app_config — dead symlink check in `_validate_path`** — `path.is_symlink()` was called after `Path.resolve()`, which always returns False; comment claimed a defence that did not exist. Removed; `resolve()` already handles symlink traversal via `is_relative_to`.
- **[core] audio_app_config — shairport serialiser produced unindented nested blocks** — `_dict_to_libconfig` applied `indent_str` to leaf values but not to block headers or delimiters, producing malformed libconfig on save; round-trip parse→save→parse was broken for any config with nested sections.
- **[core] audio_app_config — `_map_device_to_name` O(n×m) scan** — iterated all cards then all devices to find a card by ID; replaced with `audio_hw_service.get_card_by_id()` which is O(1) via the card index.
- **[core] `test_version.py` + `test_push.py` — paths broken after monorepo split** — `parents[2]` pointed to `/home/ad` (old monorepo root); fixed to `parents[1]` (repo root). Script path updated to `scripts/generate_vapid_keys.py`.
- **[core] packages — `_validate_destination_path` path-traversal bypass** — bare `startswith(allowed_path)` matched `/tmp/audiogravity-packages-evil`; fixed with separator-aware check (`startswith(root + "/") or == root`).
- **[core] packages — `yes_proc` leaked on install timeout** — when `use_yes=True` and `communicate()` timed out, only the main process was killed; the `yes` subprocess kept running indefinitely. Fixed with `yes_proc.kill()` in the timeout handler.
- **[core] packages — `installation_logs` O(n) eviction** — `list.pop(0)` shifted 499 entries per log line; replaced with `deque(maxlen=500)` for O(1) eviction.
- **[core] packages — background version-check task not tracked** — `asyncio.create_task` result discarded; `cleanup()` method added to cancel it on shutdown.
- **[core] performance — `subprocess.run` blocking in async governor methods** — `_write_cpu_file`, `save_governor_config`, and `create_systemd_service` blocked the event loop; wrapped in `asyncio.to_thread`.
- **[core] performance — `cancel_test` blocked event loop on `process.wait()`** — `subprocess.Popen.wait(timeout=2)` ran synchronously inside an `async def`; replaced with `await asyncio.to_thread(process.wait, timeout=2)`.
- **[core] performance — stddev computed by expanding histogram to 1 M-entry list** — `statistics.pstdev([lat]*count …)` allocated ~28 MB per test on Pi; replaced with weighted variance over histogram buckets (O(k), k ≤ 200).
- **[core] performance — `cleanup()` published `service_started` on shutdown** — wrong `event_type`; corrected to `service_stopped`.
- **[core] performance — `logger.warn()` removed in Python 3.13** — replaced with `logger.warning()`.
- **[core] profiles — critical-stop error recorded but service start not gated** — French error string only; the `if/else` already gates the start correctly (finding was a false positive on the logic, only the French string was fixed).
- **[core] profiles — bare `except: pass` in `_listen_for_service_events`** — silently discarded all `ServiceState` parse errors; replaced with `except (ValueError, KeyError) as exc: logger.debug(...)`.
- **[core] push — `ec.generate_private_key` monkey-patch applied on every instantiation** — double-wrapping risk; guarded with `getattr(..., '__name__') != '_patched_generate'` so the patch is applied at most once per process.
- **[core] services — `_get_cgroup_path` called `subprocess.run` without `asyncio.to_thread`** — blocked the event loop on every service monitoring poll; wrapped with `to_thread` at all three call sites.
- **[core] steering — `_verify_alsa_device_exists`, `_verify_audio_flow`, `_get_active_alsa_devices` blocked event loop** — synchronous `/proc/asound` reads in async methods; extracted into `_*_sync` static methods called via `asyncio.to_thread`.
- **[core] sysinfo — `CPUInfo` with stale `current_freq` cached permanently** — the full object including the dynamic frequency was cached on first call; now only immutable fields are cached and `current_freq` is re-read on every call.
- **[core] sysinfo — `"Moins d'une minute"` returned as API `uptime_duration`** — French string in a user-facing JSON field; replaced with `"Less than a minute"`.
- **[core] sysinfo — `asyncio.get_event_loop()` deprecated in log streamer and WebSocket terminal** — replaced with `asyncio.get_running_loop()`.
- **[core] sysinfo — thermal zone reads blocking in async `_get_temperature_info`** — synchronous `open()` calls inside async method; extracted to `_read_zone_temps` sync helper called via `asyncio.to_thread`.
- **[core] radio — missing `await` on `add_custom_station`** — the endpoint returned a coroutine object, making custom station creation permanently broken; `await` added.
- **[core] tidal — `submit_redirect` failure not surfaced** — the router ignored the `bool` return value and always responded HTTP 200; now raises HTTP 400 on failure.
- **[core] tidal — `out.read()` blocking in async stream generator** — every audio chunk read called `out.read()` synchronously on the event loop; replaced with `await asyncio.to_thread(out.read, _CHUNK)`.
- **[core] tidal — PKCE `code_verifier` logged on token-exchange failure** — full error response body written to logs; now only `error` and `error_description` fields are logged.
- **[core] tidal — concurrent `start_pkce()` calls silently corrupted each other's verifier** — logged a warning when a flow is already pending; callers should not call `start_pkce` twice without completing the flow.
- **[core] qobuz — `_extract_secrets` silently produced wrong secrets when bundle regex found no matches** — now raises `RuntimeError` when no timezone has a complete seed+info+extras triplet.
- **[core] qobuz — concurrent bundle cache misses fetched the 200 KB JS twice** — `asyncio.Lock` added with double-checked locking.
- **[core] radio — `_discover_mirrors` fire-and-forget task not tracked** — `_discover_task` stored on instance; `stop()` added to cancel it; exceptions now surface via `add_done_callback`.
- **[core] radio — `_by_url` dict grew unbounded from search hits** — capped at 1000 entries with eviction of non-saved entries.
- **[core] player — `_get_active_alsa_card` blocked event loop on `/proc/asound` scan during DSD poll** — synchronous filesystem walk extracted to `_scan_active_alsa_card_sync` and called via `asyncio.to_thread`.
- **[core] sse_manager — `shutdown()` called `.cancel()` on a `List[Task]` instead of each task** — `AttributeError` on every graceful shutdown; monitoring loops kept running after the event loop closed.
- **[core] utils/files — `os.fsync()` in `atomic_write_json` blocked event loop 50–300 ms on SD card flush** — removed; `os.replace()` atomic rename is sufficient for config-file integrity.
- **[core] dbus_client — `get_dbus_client()` singleton had no concurrency guard** — two concurrent callers both created separate D-Bus connections; `asyncio.Lock` added.
- **[core] roon_client — `get_roon_client()` singleton had no concurrency guard** — `asyncio.Lock` with double-checked locking added.
- **[core] http — `_get_shared_session()` not coroutine-safe** — two concurrent first callers both created `ClientSession`; `asyncio.Lock` added.
- **[core] dbus_client — bare `except: pass` swallowed `asyncio.CancelledError`** — replaced with `except (TypeError, ValueError): pass`.
- **[core] ttl_cache — `TTLCache.get()` always missed for a cached `None` value** — `_value is not None` guard prevented `None` from being representable as a cache hit; replaced with `_UNSET` sentinel.
- **[core] JWT and auth error messages in French** — `"Token invalide ou expiré"`, `"Accès réservé aux administrateurs"`, `"Les invités ne sont pas autorisés"` translated to English (returned verbatim in JSON API responses).
- **[core] `www.lesbonscomptes.com` domain entry did not survive `www.` stripping** — changed to `lesbonscomptes.com` fixing an intermittent test failure.
- **[lic] XSS in portal upgrade and download forms** — `filename` from the server `Content-Disposition` header and `newKey` from user input were injected into `.innerHTML` without escaping; a crafted value could exfiltrate the admin session token. HTML-escaping helper `_esc()` added to both components.
- **[lic] `version_scope` stripped on license resend, bulk-resend, and transfer** — `generate_lic()` was called without the `version_scope` parameter, silently converting v1-scoped licenses to all-versions licenses and bypassing the upgrade paywall.
- **[lic] All-versions lifetime licenses incorrectly rejected on AG v2** — `payload.get('version_scope', '1')` defaulted absent scope to `"1"`, causing `version_expired` for licenses issued before scoping was introduced. Default changed to `None` (no check when field is absent).
- **[lic] Admin token comparison was not constant-time** — `!=` string comparison allowed character-by-character brute-force timing attack; replaced with `hmac.compare_digest`.
- **[lic] Blocking SMTP calls on the async event loop** — all `mailer.send_*()` in admin handlers now use `await asyncio.to_thread(...)`.
- **[lic] Blocking file I/O in `import_db`** — `shutil.copy2` and `Path.write_bytes` wrapped with `asyncio.to_thread`.
- **[lic] `purge_audit` read `db.total_changes` (cumulative) before `commit()`** — now reads `cur.rowcount` after the DELETE for an accurate count.
- **[lic] `/deactivate` unprotected when `VERIFY_KEY` is empty** — `@limiter.limit("10/minute")` added.
- **[lic] Revoked license could be deactivated, corrupting audit trail** — `AND revoked_at IS NULL` added to the `deactivate_order` UPDATE condition.
- **[ui] XSS in license status acquisition steps** — `unsafeHTML(_acquisitionStepsHtml())` replaced with a safe Lit `html` template; `_priceDisplay` (from backend `license_price`) is now a text node.
- **[ui] XSS in license status portal URL** — `_portalUrl` from the backend now validated as `https?://` before embedding in `InfoModal` HTML string; `javascript:` and `data:` URLs are rejected.
- **[ui] XSS in package update confirm dialog** — `pkg.label`, `pkg.installed_version`, `pkg.available_version` (from package registry) are now HTML-escaped with `escapeHtml()` before injection into `showConfirm` HTML string.
- **[ui] `JSON.parse` on corrupted localStorage crashes auth init** — `auth.js:initAuth` now wraps `JSON.parse(userStr)` in `try/catch`; a corrupted `jwt_user` value calls `clearAuth()` and returns `false` instead of throwing.
- **[ui] `showToast` without `window.` prefix throws `ReferenceError`** — `ag-config-editor.js:_handleCancel` was calling bare `showToast`; fixed to `window.showToast`.
- **[ui] CodeMirror instance leaks on every config editor open/close** — `disconnectedCallback` added to destroy the CodeMirror instance and prevent DOM accumulation over long admin sessions.
- **[ui] `@lit/context` imported from CDN (no SRI, supply chain risk)** — replaced with local npm package `@lit/context` (installed as proper dependency).
- **[ui] `addToHistory` used as implicit global in `ag-admin-page`** — added to named imports from `common.js`; was silently broken in module-isolated test environments.
- **[ui] `this.loading` not reactive in `ag-config-page`** — `loading: { type: Boolean }` added to `static properties`; the loading guard now prevents concurrent service config requests.
- **[ui] Stale radio search results overwrote current ones** — `_loadSearch` now uses `AbortController`; results from cancelled requests are discarded.
- **[ui] `version.test.js` path broken after monorepo split** — `ROOT` corrected to `audiogravity.ui/` repo root; `VERSION` resolved from sibling `audiogravity.ops/VERSION`; `frontend/` prefix removed from file paths.

### Added
- **[core] audio_hw — `force_refresh` query parameter on `GET /audio-hw/devices`** — `?force_refresh=true` bypasses the 60 s cache and triggers an immediate rescan, useful after a USB hotplug event.
- **[core] audio_hw — `total_cards` as a computed field** — converted to Pydantic v2 `@computed_field`; can no longer diverge from `len(cards)`.
- **[core] `requirements-dev.txt`** — test dependencies (`pytest`, `pytest-asyncio`, `httpx`) separated from `requirements.txt` in `audiogravity.core`.
- **[core] audio_pipeline** — `TestDetectMpdFormat`, `TestAlsaPcmState` (latency, 2**64 wraparound, closed device), `TestHqplayerVolume` (clamping, None), `TestPidIdentifyCacheType` — 64 tests passing.
- **[site] `THIRD_PARTY_NOTICES.md`** — full attribution for all open-source components: frontend (Lit, Cytoscape, dagre, Lucide, Chart.js, CodeMirror, Inter, JetBrains Mono), backend (FastAPI, Pydantic, pywebpush/MPL-2.0, cryptography, roonapi, 15+ libraries), runtime binaries (ffmpeg/LGPL, cyclictest/GPL-2, iperf3/BSD-3, smartctl/GPL-2), external API (Radio Browser), and optionally-installable audio software (MPD, upmpdcli, shairport-sync, HQPlayer NAA, Roon Bridge/Server).
- **[site] `index.html`** — announce bar updated to v0.9.4; Features section: title includes Tidal, Unified Transport card adds stream origin badge, High-resolution library card mentions UPnP search playable, MQA removed from signal-path description; Compare table: new row for native Tidal & Qobuz streaming (OAuth2/PKCE), UPnP row updated to mention search + directly playable results; footer version v0.9.4 and "Open Source" link in Legal.
- **[site] `README.md`** — reference to `THIRD_PARTY_NOTICES.md` in license paragraph and Documentation section.

## [0.9.4] - 2026-06-20

### Fixed
- **[core] Pydantic v2 deprecation — `.dict()` → `.model_dump()`** — `services/service.py` was using the deprecated `.dict()` method; replaced with `.model_dump()`.
- **[core] RuntimeWarning coroutines never awaited** — two test helpers left coroutines unawaited when patching `asyncio.wait_for`; both fixed by closing coroutines before raising or restructuring the mock.
- **[ui] Code duplication removed across components** — `loadConnection(host, fetchFn, tag)` helper extracted to `utils-lit.js`, used by Qobuz/Tidal/HQPlayer output molecules (3×10 lines removed). `queueWithFeedback(queueFn, label)` helper added to `library-api.js`, used by `ag-library-search` and `ag-library-browse`. `_formatRelativeTime()` removed from `ag-service-card` and `ag-profile-card` in favour of the existing `formatTimestamp()` from `utils-lit.js`. 16 unit tests added (formatTimestamp, loadConnection, queueWithFeedback, escapeHtml XSS, jitterChart destroy, push URL format, password trim).
- **[ui] XSS — `escapeHtml` imported directly in `ag-admin-page`** — removed `window.escapeHtml ? ... : username` ternary; `escapeHtml` now imported as an ES6 module so username is always escaped in the delete-user confirmation dialog.
- **[ui] XSS — `unsafeHTML(this.label)` removed from `ag-metric-detail`** — label prop now bound with Lit's auto-escaping (`${this.label}`); unused `unsafeHTML` import removed.
- **[ui] Memory leak — `ag-network-test` jitter Chart.js not destroyed** — `this._jitterChart.destroy()` added to `disconnectedCallback()`.
- **[ui] Push unsubscribe used wrong HTTP method** — changed from `POST` with JSON body to `DELETE` with query param (`apiDelete('/push/unsubscribe?endpoint=...')`), matching the backend router.
- **[ui] Password trim in user modal** — `this._password` now `.trim()`-ed before validation; whitespace-only passwords are caught by the existing `length < 6` check instead of reaching the backend.
- **[core] core — D-Bus proxy cache eviction on error** — stale unit proxies are now removed from `_unit_proxy_cache` on `call_get_all` failure so the next call rebuilds a fresh proxy instead of reusing a dead one indefinitely.
- **[core] core — Roon disconnect timeout** — `_roon_api.stop()` wrapped in `asyncio.wait_for(timeout=5)` to prevent indefinite hang; state is always cleaned up in `finally`.
- **[core] core — JWT decode error log sanitised** — exception logged as `type(e).__name__` only, preventing any token fragment from appearing in logs.
- **[core] core — EventBus `QueueFull` now logged** — slow subscriber drop logged at DEBUG level for diagnostics; `logging` module added to `events.py`.
- **[core] sysinfo — `smartctl` `FileNotFoundError` crashes monitor** — caught and degraded gracefully; disk temperature returns `None` when `smartctl` is absent. `SYSLOG_IDENTIFIER` fixed to `_SYSLOG_IDENTIFIER=` (journalctl match syntax). Invalid `grep_pattern` regex now returns 400. `lscpu` absence caught. Admin PTY shell logs an audit entry.
- **[core] push — `webpush()` without timeout** — `timeout=10` added to prevent indefinite blocking on unreachable endpoints. Endpoint now validated as HTTPS URL. `endpoint` query param annotated with `Query()`. `logger.error` on successful unsubscribe changed to `logger.info`.
- **[core] config_validation — `appconfigfile` path traversal** — paths now validated against `/etc` and `/usr/local/etc` whitelist (mirrors `audio_app_config`). `systemd_unit` bounded to `max_length=255`. Substring match replaced with line-start check. `ValueError` in validation now returns 400 instead of 500.
- **[core] Steering — ALSA device injection via config write** — `alsa_device` now validated against `^hw:\d+,\d+$` before any config file substitution; `get_steerability()` no longer hardcodes `upmpdcli`/`roonbridge` as always available; `_verify_alsa_device_exists()` checks `/proc/asound/cardX/pcmYp` (playback subdevice), not just the card directory.
- **[core] Performance — cyclictest `IndexError` on trailing token** — bounds check (`i + 1 < len(tokens)`) added to the cyclictest line parser.
- **[core] Performance — `$CONFIG_FILE` unquoted in boot script** — config path now passed as `sys.argv[1]` and shell-quoted (`"$CONFIG_FILE"`), preventing word-splitting on paths with spaces.
- **[core] Performance — `duration_seconds` always 0** — test start captured with `time.monotonic()`; actual elapsed time stored in `LatencyTestResult`.
- **[core] Performance — bare `except:` clauses** — replaced with `except (ValueError, IndexError)` and `except (subprocess.TimeoutExpired, OSError)`.
- **[core] Profiles — `asyncio.gather()` without timeout** — both stop and start phases wrapped in `asyncio.wait_for(timeout=30)`.
- **[core] Profiles — `stopped_count` counted FAILED as stopped** — FAILED state now goes to `failed_count`; only INACTIVE/DEAD states increment `stopped_count`.
- **[core] Profiles — export written to world-readable `/tmp`** — export path moved to `settings.audiogravity_home` with `chmod(0o600)`.
- **[core] License — server response handling hardened** — `/check` and `/activate` now verify HTTP status before calling `resp.json()`; unexpected Pydantic shapes return 502; `lic_content` validated as JSON before writing to disk; `X-Verify-Key` header extracted to `_verify_headers()` helper; `_portal_base()` validates URL structure.
- **[core] Services — enum comparison bug** — `validate_service_properties` was comparing `CPUSchedulingPolicy`/`IOSchedulingClass` enum members to plain strings (always-false conditions); corrected to compare against enum values.
- **[core] Services — D-Bus call unguarded** — `get_unit_file_state()` now wrapped in `asyncio.wait_for(timeout=2s)`; timeout logs a warning and falls back to subprocess.
- **[core] Services — stale cgroup FD not evicted** — `fd.seek(0)` failure now evicts the dead FD from the LRU cache instead of leaving it for the next call.
- **[core] Services — `service_name` path param unvalidated** — all `service_name` Path params now carry `pattern=r"^[a-zA-Z0-9._@-]+(?:\.service)?$"` → 422 on invalid input.
- **[core] audio_app_config — path traversal via symlink** — `_validate_path` now calls `resolve()` first, then checks `is_relative_to()` on the resolved path; a symlink pointing outside `/etc` is rejected even if the link itself lives inside `/etc`.
- **[core] audio_app_config — restart duplication** — `_restart_service()` extracted; `update_config` and `restore_backup` both delegate to it.
- **[core] audio_app_config — `model_validator` incorrect** — `@field_validator('content','data')` replaced with `@model_validator(mode='after')` for correct single-evaluation semantics.
- **[core] Packages — shell injection via installer config** — `install_script_args`, `check_command`, `uninstall_commands` and `version_check_command` now use `shlex.split` + `create_subprocess_exec` instead of `shell=True` f-strings. `version_check_url` validated against `ALLOWED_DOWNLOAD_DOMAINS`. `gpg_key_path` and `sources_list_path` validated by `_validate_destination_path()` before any `sudo cp`. `_validate_package_name()` added in `apt_repo.py`. 9 security tests added.
- **[core] Player `_poll_loop` NameError on `get_now_playing()` failure** — `items` now initialised to `[]` before the try block, preventing `NameError` when `get_now_playing()` raises.
- **[core] Player DSD state inconsistent after partial `gather()` failure** — `_dsd_active` reset to `False` on exception so volumes are not left partially forced.
- **[core] Auth `POST /users` returned 200 instead of 201** — corrected to `HTTP_201_CREATED`.
- **[core] Auth `PATCH /users/{u}` accepted whitespace-only password** — passwords that are blank after `.strip()` are now rejected with 400.
- **[core] Auth `update_user` race condition post-update** — `update_user()` now returns `Optional[User]` directly, eliminating the separate `get_user()` call after write.
- **[core] Auth WebAuthn userHandle exception was silent** — bare `except` replaced with `logger.warning()` for diagnosis; `_b64url_to_bytes` moved to module top.
- **[core] `users.py` write race condition** — `_save_users` now holds a `threading.Lock` for thread-safe concurrent writes.
- **[core] JWT missing `jti` claim** — `uuid.uuid4()` added to every token payload, enabling future revocation support.

### Added
- **[core] HQPlayer `POST /hqplayer/stop`** — endpoint to stop playback (was documented but not implemented); also adds `stop()` service method and `has_dsp_config` public property. 13 unit tests added covering stop, Literal validation, `has_dsp_config`, `_read_xml_response` helper, and play request validation.

### Fixed
- **[core] Radio `PUT /radio/{uuid}` broken** — `edit_station()` was awaited incorrectly (missing `await`), causing `PUT` to always return a coroutine instead of the result.
- **[core] Radio `added_at` timezone-unaware** — `datetime.utcnow()` (deprecated Python 3.12) replaced with `datetime.now(timezone.utc)`.
- **[core] Audio pipeline DSD stream not detected** — `audio_str="dsd64:2"` caused `int("dsd64")` → ValueError silently swallowed; DSD multiplier now parsed correctly (`dsd_mult × 44100`, 1-bit).
- **[core] Audio pipeline cgroup v1 PID→service mapping** — `split("::", 1)` only matched cgroup v2; now uses `fields[-1]` to support both formats.
- **[core] Audio pipeline `dbus-send` without timeout** — both subprocess `communicate()` calls now wrapped with `asyncio.wait_for(timeout=3.0)` + `proc.kill()` on expiry.
- **[core] Audio pipeline MPD URI control-char filter** — `any(ord(c) < 0x20)` replaces the newline-only check.
- **[core] Library UPnP queue ignores `output_id`** — `upnp_search_queue` now honours `req.output_id` like Qobuz/Tidal.
- **[core] Library SOAP Browse object_id not XML-escaped** — `_sax.escape(object_id)` applied before template formatting.
- **[core] Library Qobuz album/playlist queue duplicated** — extracted `_queue_qobuz_tracks()` helper (~25 lines removed).
- **[core] Library `_tidal_cover` crashes on dict uuid** — `isinstance(uuid, str)` guard added.
- **[core] Qobuz `private_key` leaked in query string** — `_exchange_code` changed from GET+params to POST+body.
- **[core] Qobuz token refresh race condition** — `asyncio.Lock` added to `TidalOAuthService.get_access_token` with double-check pattern.
- **[core] Qobuz half-authenticated state** — `handle_callback` returns `False` when `_find_working_secret()` returns None instead of saving an `app_secret=None` state.
- **[core] Qobuz `user_id` could be string `"None"`** — `str(user.get("id"))` when id is JSON null now correctly returns `None`.
- **[core] Tidal stale token not cleared on network error** — `_access_token` set to `None` when refresh fails and token is past expiry.
- **[core] HQPlayer `item_type`/`action` unvalidated** — changed from `str` to `Literal["track","album","artist"]` / `Literal["play","add"]` in `HQPlayerPlayLibraryRequest`.
- **[core] HQPlayer XML parsing duplicated** — extracted `_read_xml_response()` static helper used by both `_send()` and `_send_batch()`.
- **[core] `get_shared_session()` exported** — `LibraryService._http_session()` now delegates to the app-wide shared session (closed on graceful shutdown), eliminating socket leak.

### Added
- **[ui] Config editor — blank configuration hint** — when a service
  config file has all sections empty (package defaults active), the form view
  now shows an info banner explaining the state and offering a direct link to
  Expert Mode to view and uncomment the full file.
- **[core] Tidal/Qobuz credential rotation detection** — 401/403 responses
  from `playbackinfopostpaywall` (Tidal) and `track/getFileUrl` (Qobuz) after
  token refresh now raise typed exceptions (`TidalClientRotatedError`,
  `QobuzClientRotatedError`) logged at ERROR level with a remediation hint.
  The Tidal stream endpoint returns HTTP 503 instead of 404 on rotation. 10
  unit tests cover both services.
- **[core+ui] Stream origin badge in the players** — the mini and
  fullscreen Now Playing views now show where the audio comes from (Tidal, Qobuz,
  a UPnP/DLNA server by name, radio, a local file, Roon, AirPlay…) with a logo +
  label, instead of an undifferentiated "MPD". The backend tags each playing
  source with its provider, independent of transport.
- **[site] FAQ — connecting Qobuz or Tidal** — one entry covering both flows:
  Qobuz OAuth (auto-redirect, no paste) and Tidal PKCE (copy/paste the redirect
  URL), noting the required subscription tier for each.
- **[core] UPnP search queue** — clicking "+" or play on a UPnP/DLNA search
  result now works: track stream URLs are passed directly to MPD, album items are
  resolved via ContentDirectory Browse. Titles and cover art are pre-registered
  during search so the queue display and Now Playing badge are enriched immediately.
  17 unit tests cover track/album/routing/metadata-registration cases.

### Fixed
- **[core] `_ext_stream_key` anchored to URL path/query** — Tidal detection
  now checks the URL *path* for `/tidal/stream/` and Qobuz detection checks the
  *query string* for `eid=`, instead of raw substring matching. Prevents a UPnP
  URL whose path contains `/tidal/stream/` or `eid=` from being misclassified.
  8 regression tests added.
- **[ui] Software tab description** — removed the "dry-run simulation"
  claim from the Pro feature list; the toggle is admin-only and not visible to
  regular Pro users.

### Changed
- **[ui] Library search lists UPnP/DLNA servers** — known media servers
  (e.g. MinimServer) now appear as sources in Library search, alongside MPD, Roon,
  Qobuz and Tidal (previously missing).
- **[ui] UPnP/DLNA text search from the Search tab** — selecting a UPnP/DLNA
  server badge while in the Search tab now stays in search mode and runs a text
  query against the server (previously always redirected to the UPnP browser).
- **[ui] Settings: single version + logout moved in** — the panel now shows
  one unified product version (front and back share it) with the Swagger API link,
  and the Logout button moved from the top bar into the Settings footer.
- **[ui] Top-bar icons** — the settings button now uses a gear icon and the
  mobile navigation button a hamburger (swapped for clarity).
- **[ui] Source connection status uses the shared status dot** — Qobuz,
  Tidal and HQPlayer now render the same status indicator as the other sources.

### Fixed
- **[ui] Qobuz sign-in flow** — the Qobuz OAuth page now opens in a popup
  (the AG UI stays underneath) that closes itself once authentication succeeds, so
  you land back in AudioGravity automatically instead of having to close the tab
  and reopen the app.
- **[ui] Missing-cover icon in the fullscreen player** — the "no artwork"
  placeholder icon was rendered far too small; it now fills the cover area again.
- **[core] Tidal playback skipped every track** — the seek cache pre-created
  the remux output file, so ffmpeg (run without `-y`) refused to overwrite it and
  exited having written 0 bytes; MPD received an empty stream and skipped to the
  next track. ffmpeg now overwrites the placeholder, and a 0-byte remux is never
  cached.
- **[ui] Bundle analysis report no longer deployed** — the Vite `stats.html`
  bundle treemap was copied into the build output and shipped to production
  (reachable at `/stats.html`). It is now opt-in only (`vite build --mode analyze`)
  and written outside the deployed output, so it never ships.

### Removed
- **[ui] Standalone styleguide page** — the unused `styleguide.html`
  design-system gallery was removed (Storybook is the live component reference).

## [0.9.3] - 2026-06-14

### Added
- **[core+ui] Tidal streaming source** — connect a Tidal HiFi account
  (PKCE login) and browse Favorites / New Releases / Playlists, plus search;
  playback streams **lossless FLAC** through a local DASH→FLAC ffmpeg proxy (Tidal
  delivers FLAC as segmented DASH, not a direct URL). Requires `ffmpeg` (added to
  the backend installer).
- **[core+ui] Tidal Charts & Editorial browse** — two new browse pills:
  **Charts** (TIDAL's Top Hits, Viral / Rap / R&B / Pop Hits…) and **Editorial**
  (Popular, Trending, TIDAL Rising, Podcasts…), extracted from Tidal's home page
  and rendered as playlists; tapping one opens its tracks like any playlist.
- **[core] Tidal in-track seek** — the proxy remuxes each track to a seekable
  FLAC file (served as it is produced, so start-up stays fast) and keeps it in a
  small, disk-backed cache (current track + a couple of recent, wiped at startup).
  Replays and reopens are served with HTTP Range, so you can seek within Tidal
  tracks. The very first play of a track in a session is not seekable; replays are.
- **[ui] Top bar — mobile navigation toggle** — a left-side button opens the
  vertical tab menu on mobile, mirroring the settings burger on the right.
- **[ui] Top bar — Library shortcut** — a one-tap button (left of Logout)
  jumps straight to the Library tab; licence gating is preserved (a locked tab
  opens the licence modal instead).
- **[ui] Roon source logo** — the `RN` text placeholder for Roon sources is
  replaced by a Roon logo rendered as a `currentColor` mask, so it stays visible in
  light, dark and the active (selected) state.

### Changed
- **[ui] DRY-RUN toggle is now admin-only** — the Audio Software DRY-RUN
  simulation is scoped to administrators (a command-preview / catalog-validation
  tool, not a dependency-resolving simulation); its size now matches the settings
  toggles.

### Fixed
- **[ui] Login page version label** — shown as `v0.9.2` (lowercase prefix,
  no space).
- **[core] AirPlay now-playing on ARM** — shairport-sync track metadata leaked the
  raw `<dbus_fast…Variant…>` repr in the pipeline now-playing; the `a{sv}` values are
  now unwrapped (portable, no-op on x86).
- **[ui] Fullscreen player volume swipe** — adjusting the volume slider no longer
  triggers the player's multi-source swipe.
- **[ui] Library horizontal scroll** — scrolling a horizontal row (pills, album
  shelves) no longer switches tabs; the swipe-to-switch handler now yields to any
  horizontally-scrollable ancestor (CSS class or inline overflow), not just inline ones.
- **[ui] Fullscreen player pull-down dismiss** — swiping down to scroll back up in
  a long tracklist no longer dismisses the player; the dismiss gesture only fires when
  the scroll area is already at the top.

### Removed
- **[ui] Obsolete top-bar buttons** — the documentation (audiogravity.app)
  button and the admin "Components" (bundle stats) button were removed.
- **[ui] Tab-bar now-playing** — the vertical tab sidebar no longer displays
  the current stream (redundant with the mini player).

---

## [0.9.2] - 2026-06-09

**Focus: Qobuz Hi-Res streaming integration + DSD volume safety.**

### Added
- **[core] Qobuz OAuth2 module** (`modules/qobuz/`): full OAuth2 authentication
  replacing the deprecated username/password login. Bundle credential extraction from
  the Qobuz web player JS, OAuth URL generation, browser-based login, code-to-token
  exchange, working secret discovery, and persistent config storage.
- **[core] Qobuz search, browse, and playback** (`library/service.py`): header-based
  API auth (`X-App-Id`/`X-User-Auth-Token`), correct API signature format (float
  timestamp, ASCII+UTF-8 byte concatenation), 3 parallel single-type search calls,
  album queueing, cover art on all browse/search methods.
- **[core] Qobuz catalog browsing** — featured albums (`album/getFeatured`),
  editorial playlists (`playlist/getFeatured`, `playlist/get`). Three new endpoints:
  `GET /library/qobuz-featured`, `GET /library/qobuz-playlists`,
  `GET /library/qobuz-playlist-tracks`. Playlist queueing support.
- **[core] External stream metadata registry** (`now_playing.py`): stable key
  derivation from `eid` query parameter for Qobuz streams — correct title, artist,
  album, and cover art in now-playing and queue despite ephemeral signed URLs.
- **[core] Qobuz as virtual source** — `src_qobuz` injected in the player when
  connected; bitrate displayed for Qobuz FLAC streams.
- **[ui] Qobuz connection card** (`ag-qobuz-output.js`): OAuth2 connect/disconnect
  molecule for the Sources view, with polling and events.
- **[ui] Qobuz catalog pills** (`ag-library-browse.js`): browse pills switch to
  Favorites / New Releases / Selection / Playlists when Qobuz is selected.
- **[ui] Qobuz icon** on source cards (optimized 56×56 webp).
- **[core] Qobuz OAuth2 unit tests** (24 tests): bundle extraction, service
  persistence, OAuth flow, Pydantic models, router endpoints.
- **[core] Qobuz catalog browsing unit tests** (22 tests): featured albums,
  playlists, playlist tracks, search, cover helper, library router endpoints.
- **[core] DSD volume unit tests** (10 tests).
- **[ops] `./dev.sh test --report`** generates `TEST_REPORT.md` — markdown summary
  with per-suite pass/fail/skip counts, durations, and failure detail.

### Changed
- **[core] Qobuz config cleanup** — removed `qobuz_app_id`, `qobuz_app_secret`,
  `qobuz_username`, `qobuz_password` settings; OAuth2 manages credentials via UI.
- **[ops] `build-backend-package.sh`** — `qobuz` added to `ENABLED_MODULES` template
  and upgrade migration loop; `QOBUZ_FORMAT_ID=27` in `.env` template.
- **[ui] Topbar doc button** opens `audiogravity.app`; internal doc links removed
  from settings panel.
- **[docs] Single source of truth** — `CHANGELOG.md` and `RELEASE_NOTES.md` consolidated
  in the landing repository; AG-repo copies marked obsolete in `CLAUDE.md`.

### Fixed
- **[core] DSD volume protection** (`player/service.py`): 6 bugs causing volume to
  snap to 100% during non-DSD playback — stale HQPlayer cache, race conditions,
  incorrect restore target.
- **[core] HQPlayer stale track** — `_current_track` cleared after 30s stopped.

---

## [0.9.1] - 2026-06-07

Changes since **0.9.0**. Range: `74a7897` (0.9.0 baseline — *Merge
feat/hqplayer-integration into master*, 2026-05-30) → release HEAD. The earlier
`v0.9.1` git tag (`b3ab0c2`) was never a release and is superseded by this one.


**Focus: ARM/Debian (aarch64) portability.** Audiogravity now installs and runs on
aarch64 (Raspberry Pi 4 / Debian) **alongside** x86/DietPi — with the absolute
constraint of never regressing the existing x86/DietPi target. This cycle also
hardens the install/packaging path, configures the production environment at
install time, fixes the standalone prod server (SSE + WebSocket), and adds test
coverage. Period: 2026-05-30 → 2026-06-07.

### Added
- **ARM64 (aarch64) as a first-class target** — backend, frontend, license server
  and audio-software installs validated end-to-end on a Raspberry Pi 4 (Debian),
  with x86/DietPi kept non-regressed.
- **[ops] upmpdcli on ARM64** — `scripts/build-upmpdcli-arm64.sh` builds the
  libnpupnp → libupnpp → upmpdcli chain natively for aarch64 and publishes a
  checksum-verified `.deb` bundle on `audiogravity.app`. The package registry
  installs it via a per-arch `arch_fallback` (no upstream arm64 package exists
  anywhere); the official source still wins where it covers the arch.
- **[ops] WebAuthn passkeys at install** — `--public-url` sets
  `WEBAUTHN_ORIGIN` and derives `WEBAUTHN_RP_ID`; forwarded by the bootstrap and
  all-in-one installers and documented in the README (passkeys require a real
  HTTPS domain, not a bare IP).
- **[ops] Push contact** — `--vapid-email` sets the VAPID `sub`; forwarded by
  the installers.
- **[ui] HQPlayer manual IP entry** — connect to a HQPlayer on a different
  (but routable) subnet that the local /24 discovery scan can't reach.
- **[ui] Standalone server WebSocket proxy** — the prod Python server now
  proxies the admin terminal WebSocket (`/sysinfo/terminal/ws`) via raw tunneling.
- **[site] Page** — the "Releases" link now points to the public GitHub repo;
  install section clarified (works on the LAN by default, passkeys/push moved to an
  optional block that requires a public domain); portable local preview `dev.sh`
  (auto-detected LAN IP).
- **[ops] Deterministic dependencies** — `requirements.lock` (68 packages pinned,
  wheels verified for x86_64 **and** aarch64, Python 3.13.5) + runtime/build split
  (`requirements-dev.lock`); license server dev requirements (`requirements-dev.txt`).
- **[core]** — VAPID key loading, PayPal IPN webhook flow (8 tests), and scoped
  pytest warning filters for third-party deprecations.

### Changed
- **[core] Auth** — replaced `passlib` with direct `bcrypt` calls.
- **[ui] Prod server consolidation** — the frontend package now bundles the
  canonical `serve_https.py` (line-by-line SSE streaming + gzip) instead of a
  divergent, broken inline copy; the systemd unit invokes it with args +
  `WorkingDirectory`.
- **[ops] Production `.env` configured at install** — license server URL/key,
  VAPID, and `ENABLED_MODULES` (incl. `hqplayer`).
- **[ops] `build-backend.sh` self-bootstraps** — installs system prerequisites
  and `python3`; the generated installer uses non-interactive `apt`; deps synced
  via `pip install -r` with wheels only.

### Fixed
- **[ui] Prod SSE stuck on "Connecting…"** — the packaged proxy buffered the
  event stream (`shutil.copyfileobj`); now streamed so the UI connects.
- **[ui] Broken-pipe traceback noise** in the standalone server when a client
  drops a keep-alive connection (e.g. after closing an SSE tab).
- **[core] Runtime bugs surfaced on ARM** — CPU model (lscpu fallback), governor
  field (`current_governor`), `cpu-governor.service` boot script (stdlib `json`),
  and `ORJSONResponse` deprecation warnings.
- **[core] Service config paths** resolved across OS layouts (`/etc` vs
  `/usr/local/etc`) and reloaded when software is installed/removed at runtime.
- **[core] `hqplayer` module** missing from the packaged `.env` `ENABLED_MODULES`
  (its endpoints returned 404).
- **[core] aarch64 startup crash** — caused by `passlib` vs `bcrypt>=4.1`.
- **[ops] Audio-software install made arch-aware** — Roon per-arch URLs
  (`{roon_arch}`), download allowlist, stdin for interactive vendor installers, and
  complete uninstall; upmpdcli `.deb` ships its systemd unit, creates its system
  user, and stops/disables cleanly on removal.
- **[ops] sudoers** completed (including Roon uninstall) and hardened
  (`sudo tee` instead of `sudo sh -c`).
- **[ops] Nuitka / packaging** — explicit includes (psutil, distro, orjson,
  pydantic, ntplib), `SHA256SUMS` merge + checksum verification in installers,
  missing transitive deps (pyparsing, ifaddr), `gh` auto-install, `license.pub`
  lookup, and miscellaneous installer robustness fixes.
- **[ops] Environment scripts** — no longer hardcode `/home/dietpi` paths or LAN
  IPs (runtime detection); seed a default `admin` user; provision dev sudoers/polkit;
  resolve `visudo` by absolute path on DietPi.

### Removed
- **[ops]** obsolete `backend/update.sh` (incompatible with the Nuitka-binary
  production model).

---

> Scope note: this release consolidates the `arm-debian-compat` work (main repo)
> plus this landing repository. The earlier `v0.9.1` tag (`b3ab0c2`) was never a
> release — delete it (local + remote) and re-tag the release commit as `v0.9.1`.
