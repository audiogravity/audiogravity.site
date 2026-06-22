# Changelog — Audiogravity

All notable changes to Audiogravity (backend, frontend, license server, installers
and this landing) are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Fixed
- **[backend] audio_pipeline — subprocess blocks event loop on NI data fetch** — `_get_local_ni_data()` called `subprocess.run("ip"/"iw")` synchronously from a coroutine, stalling the event loop for up to 3s on every cache miss (TTL was 10s). Calls are now pre-warmed via `asyncio.to_thread` before pipeline construction; TTL raised to 60s.
- **[backend] audio_pipeline — HQPlayer volume returned negative integers** — formula `100 * (1 + volume_db / 60)` produced negative values for `volume_db < -60` (e.g. `-140` for muted). Now clamped to `[0, 100]`; `None` when `volume_db` is unknown.
- **[backend] audio_pipeline — `cpu_percent()` always returned 0.0** — a new `psutil.Process` instance was created on every cycle; the first call always returns 0.0 without a prior snapshot. Instances are now reused via `_psutil_procs`.
- **[backend] audio_pipeline — incoherent double `/proc/asound` read** — `_get_alsa_latency` and `_get_alsa_buffer_fill` each read `status` and `hw_params` independently, yielding different hardware snapshots. A shared `_read_alsa_pcm_state` helper performs a single coherent read.
- **[backend] audio_pipeline — ALSA pointer wraparound incorrect on ARM64** — `appl_ptr - hw_ptr < 0` was corrected with `+ 2**32`; on ARM64 `snd_pcm_uframes_t` is 64-bit, causing negative or absurd latencies after ~6h. Fixed with `+ 2**64`.
- **[backend] audio_pipeline — `_pid_identify_cache` unbounded** — raw dict with no TTL or size limit; replaced with `TTLDictCache(300)`.
- **[backend] audio_pipeline — M4A codec mismatch between modules** — `_enrich_with_topology` mapped `.m4a → ALAC` while `service._query_mpd` mapped `M4A → AAC` for the same file. `_detect_mpd_format` is now the single source of truth; `service.py` imports it directly.
- **[backend] audio_pipeline — `_mpd_command` duplicated `core.mpd_client.mpd()`** — redundant implementation removed from `now_playing.py`; all calls go through `core.mpd_client`.
- **[backend] audio_pipeline — `_get_mpd_now_playing` used direct Unix socket** — replaced with `core.mpd_client.mpd_batch` (TCP), consistent with all other MPD consumers. `currentsong` + `status` sent in a single connection via `command_list_ok_begin`.
- **[backend] audio_pipeline — blocking file I/O in async endpoint** — `open(topology_path)` in `async def get_topology()` blocked the event loop; replaced with `asyncio.to_thread(topology_path.read_bytes)`.
- **[backend] audio_pipeline — dead variable + deprecated API** — `now = asyncio.get_event_loop().time()` removed (`now` never used; `get_event_loop()` deprecated since Python 3.10).
- **[backend] audio_hw — blocking I/O in async event loop** — `read_text()`, `exists()`, `iterdir()` called directly from coroutines, stalling the event loop on every scan. All filesystem access moved to `_scan_card_dir()` (synchronous method) called via `asyncio.to_thread`; per-card details now fetched in parallel via `asyncio.gather`.
- **[backend] audio_hw — exception path poisoned the 60 s cache** — a transient I/O error (e.g. USB hotplug race) fell through to `_cache.set()`, serving an empty or partial device list for the full TTL. The error path now returns without caching.
- **[backend] audio_hw — subdevice availability always reported as 1/1** — the `if sub_info_file.exists()` block contained only `pass`; `subdevices_total` and `subdevices_available` were always hardcoded to 1 regardless of actual device state. `sub0/info` is now parsed for `subdevices_count` and `subdevices_avail`.
- **[backend] audio_hw — early return did not cache the negative result** — when `/proc/asound/cards` is absent the empty result was returned without `_cache.set()`, causing a `/proc` stat on every subsequent call with no back-off.
- **[backend] audio_hw — non-deterministic device ordering** — `iterdir()` returns entries in filesystem order; a `sorted()` call now guarantees stable ordering by `pcmNp` name.
- **[backend] hqplayer — `play_uri` / `play_library_item` silently failed on every play attempt** — `_send_batch` passed `allow_empty=False` to all commands including `<Play/>`, which closes the connection without a body; `_read_xml_response` blocked for 3 s then raised `HQPlayerError`. Every HQPlayer playback call failed after loading the queue. Fixed by passing `allow_empty=True` for the `Play` command.
- **[backend] hqplayer — `resolve_file_path` rejected all files when `music_root='/'`** — path-traversal guard used `startswith(root + os.sep)` which fails for root `'/'`; replaced with `Path.relative_to()`.
- **[backend] hqplayer — `active_rate=0` collapsed to `None`** — `rate if rate else None` treated 0 Hz (DAC idle) as "no rate data"; fixed to `rate if rate is not None else None`.
- **[backend] library — `asyncio.get_event_loop()` deprecated in `upnp_service`** — replaced with `asyncio.get_running_loop()` (correct API inside async context, avoids `DeprecationWarning` on Python 3.13).
- **[backend] library — `_probe_port` made two HTTP GETs per candidate URL** — body was fetched once, then `_fetch_device` fetched the same URL again; `_parse_device_text()` helper now reuses the first response.
- **[backend] library — `_mpd_album_cache` was an unbounded raw dict** — replaced with `TTLDictCache(60)` + `prune_to_size(100)` to prevent unbounded RAM growth on large libraries.
- **[backend] library — `get_ext_stream_meta` called twice per HTTP track in `mpd_queue_list`** — result stored once and reused for both display enrichment and cover_token construction.
- **[backend] library — Roon `_subkey` race in `roon_queue_list`** — concurrent `run_in_executor` calls both read-modify-write `sock._subkey` without a lock; replaced with `time.time_ns()` as the subscription key.
- **[backend] license — `_ping` leaked the aiohttp TCP connection** — `await session.post(...)` without `async with` left the `ClientResponse` unclosed; fixed with `async with session.post(...) as _resp: pass`.
- **[backend] license — online `_fetch` treated 4xx (revoked, not found) as "unreachable"** — `resp.raise_for_status()` raised for 4xx and 5xx alike; now 5xx → "unreachable", 4xx → structured status from the LS (e.g. "revoked").
- **[backend] license — `start_checker` leaked old background loop on double call** — previous `asyncio.Task` was not cancelled before creating a new one; fixed with cancel guard.
- **[backend] license — trial file non-atomic write → false "tampering detected" on crash** — `open(path, 'w'); json.dump(...)` truncates on power loss; replaced with `atomic_write_json` (write-to-temp + rename).
- **[backend] license — trial only written to first location on creation** — `any(...)` short-circuited after first success, leaving the fallback location empty; tampering detection now requires all-locations consistency. Fixed with explicit list comprehension.
- **[backend] license — `require_full_license` silently bypassed when service not initialised** — `if _service is None: return` allowed all protected endpoints without a license check; now returns HTTP 503.
- **[backend] packages — `www.lesbonscomptes.com` domain did not match after `www.` stripping** — `_validate_download_url` strips `www.` before comparison; the set entry had the prefix, causing intermittent failures when set iteration returned that domain first. Changed to `lesbonscomptes.com`.
- **[backend] config_validation — blocking subprocess and filesystem I/O in Pydantic validators** — `subprocess.run(['systemctl', ...])` and `Path.exists()` ran synchronously inside field validators on the async event loop, blocking for up to N×5 s per validation request. System-state checks (unit existence, file existence) moved to an async service method using `asyncio.gather + asyncio.to_thread`; validators now only check structure and path safety.
- **[backend] config_validation — `depends_on` accepted duplicates silently** — `validate_no_duplicates` covered `start` and `stop` but not `depends_on`; `["a","a"]` was accepted without error. Fixed by extending the validator to all three list fields.
- **[backend] auth — `create_user` accepted whitespace-only passwords** — `update_user` rejected passwords where `.strip() == \"\"` but `create_user` did not; `\"      \"` (6 spaces) was hashed and stored. Fixed via a `model_validator` on `CreateUserRequest`.
- **[backend] auth — timing oracle on disabled accounts** — `authenticate_user` returned immediately for disabled accounts (~1 ms) vs. burning a dummy bcrypt hash for nonexistent accounts (~250 ms), enabling username enumeration. Disabled-account path now also runs `verify_password(password, _DUMMY_HASH)` to equalise timing.
- **[backend] auth — WebAuthn concurrent flows clobbered each other's challenge** — `_pending` was keyed by username only; a second `begin_*` call for the same user overwrote the first challenge regardless of flow type (register vs. authenticate). Key changed to `\"username:kind\"` so both flows can coexist independently.
- **[backend] `core/users.py` — `_load_users` read cache outside the lock** — `_cache` and `_cache_mtime` were read without holding `_lock` while `_save_users` wrote them under `_lock`; concurrent async calls could observe a stale cache. `Lock` upgraded to `RLock`; `_load_users` now holds the lock for the full mtime-check + read sequence.
- **[backend] audio_app_config — `_run_command` timeout covered only process creation** — `asyncio.wait_for` was applied to `create_subprocess_exec` only; `communicate()` had no timeout and could block the event loop indefinitely on a hung `sudo systemctl restart` or stalled NFS mount. The timeout now wraps `communicate()` and kills the process on expiry.
- **[backend] audio_app_config — `restore_backup` broken in production** — `sudo cp /var/backups/.../* /etc/...` was not listed in the sudoers allowlist; every restore failed silently. Added the missing entries to the installer.
- **[backend] audio_app_config — backup files world-readable** — `sudo chmod 600 /var/backups/audiogravity/*/*` was not in sudoers; the chmod silently failed, leaving backup files (which may contain MPD passwords or Shairport auth keys) world-readable. Return value now checked; sudoers entry added.
- **[backend] audio_app_config — `total_count` in backup list wrong under `limit`** — `BackupListResponse.total_count` was computed from the already-sliced list; callers received `total_count == limit` instead of the real file count. Total is now captured before slicing.
- **[backend] audio_app_config — `debounce_task` leaked on shutdown** — the reload task created by the package-event listener was not stored on `self` and therefore not cancelled by `cleanup()`. It now fires `_load_service_map` on a partially-torn-down service on shutdown.
- **[backend] audio_app_config — blocking `open()` in async `_load_service_map`** — `audio-config.json` was read synchronously on every package-install reload event; replaced with `asyncio.to_thread`.
- **[backend] audio_app_config — dead symlink check in `_validate_path`** — `path.is_symlink()` was called after `Path.resolve()`, which always returns False; comment claimed a defence that did not exist. Removed; `resolve()` already handles symlink traversal via `is_relative_to`.
- **[backend] audio_app_config — shairport serialiser produced unindented nested blocks** — `_dict_to_libconfig` applied `indent_str` to leaf values but not to block headers or delimiters, producing malformed libconfig on save; round-trip parse→save→parse was broken for any config with nested sections.
- **[backend] audio_app_config — `_map_device_to_name` O(n×m) scan** — iterated all cards then all devices to find a card by ID; replaced with `audio_hw_service.get_card_by_id()` which is O(1) via the card index.
- **[tests] `test_version.py` + `test_push.py` — paths broken after monorepo split** — `parents[2]` pointed to `/home/ad` (old monorepo root); fixed to `parents[1]` (repo root). Script path updated to `scripts/generate_vapid_keys.py`.
- **[backend] packages — `_validate_destination_path` path-traversal bypass** — bare `startswith(allowed_path)` matched `/tmp/audiogravity-packages-evil`; fixed with separator-aware check (`startswith(root + "/") or == root`).
- **[backend] packages — `yes_proc` leaked on install timeout** — when `use_yes=True` and `communicate()` timed out, only the main process was killed; the `yes` subprocess kept running indefinitely. Fixed with `yes_proc.kill()` in the timeout handler.
- **[backend] packages — `installation_logs` O(n) eviction** — `list.pop(0)` shifted 499 entries per log line; replaced with `deque(maxlen=500)` for O(1) eviction.
- **[backend] packages — background version-check task not tracked** — `asyncio.create_task` result discarded; `cleanup()` method added to cancel it on shutdown.
- **[backend] performance — `subprocess.run` blocking in async governor methods** — `_write_cpu_file`, `save_governor_config`, and `create_systemd_service` blocked the event loop; wrapped in `asyncio.to_thread`.
- **[backend] performance — `cancel_test` blocked event loop on `process.wait()`** — `subprocess.Popen.wait(timeout=2)` ran synchronously inside an `async def`; replaced with `await asyncio.to_thread(process.wait, timeout=2)`.
- **[backend] performance — stddev computed by expanding histogram to 1 M-entry list** — `statistics.pstdev([lat]*count …)` allocated ~28 MB per test on Pi; replaced with weighted variance over histogram buckets (O(k), k ≤ 200).
- **[backend] performance — `cleanup()` published `service_started` on shutdown** — wrong `event_type`; corrected to `service_stopped`.
- **[backend] performance — `logger.warn()` removed in Python 3.13** — replaced with `logger.warning()`.
- **[backend] profiles — critical-stop error recorded but service start not gated** — French error string only; the `if/else` already gates the start correctly (finding was a false positive on the logic, only the French string was fixed).
- **[backend] profiles — bare `except: pass` in `_listen_for_service_events`** — silently discarded all `ServiceState` parse errors; replaced with `except (ValueError, KeyError) as exc: logger.debug(...)`.
- **[backend] push — `ec.generate_private_key` monkey-patch applied on every instantiation** — double-wrapping risk; guarded with `getattr(..., '__name__') != '_patched_generate'` so the patch is applied at most once per process.
- **[backend] services — `_get_cgroup_path` called `subprocess.run` without `asyncio.to_thread`** — blocked the event loop on every service monitoring poll; wrapped with `to_thread` at all three call sites.
- **[backend] steering — `_verify_alsa_device_exists`, `_verify_audio_flow`, `_get_active_alsa_devices` blocked event loop** — synchronous `/proc/asound` reads in async methods; extracted into `_*_sync` static methods called via `asyncio.to_thread`.
- **[backend] sysinfo — `CPUInfo` with stale `current_freq` cached permanently** — the full object including the dynamic frequency was cached on first call; now only immutable fields are cached and `current_freq` is re-read on every call.
- **[backend] sysinfo — `"Moins d'une minute"` returned as API `uptime_duration`** — French string in a user-facing JSON field; replaced with `"Less than a minute"`.
- **[backend] sysinfo — `asyncio.get_event_loop()` deprecated in log streamer and WebSocket terminal** — replaced with `asyncio.get_running_loop()`.
- **[backend] sysinfo — thermal zone reads blocking in async `_get_temperature_info`** — synchronous `open()` calls inside async method; extracted to `_read_zone_temps` sync helper called via `asyncio.to_thread`.
- **[backend] radio — missing `await` on `add_custom_station`** — the endpoint returned a coroutine object, making custom station creation permanently broken; `await` added.
- **[backend] tidal — `submit_redirect` failure not surfaced** — the router ignored the `bool` return value and always responded HTTP 200; now raises HTTP 400 on failure.
- **[backend] tidal — `out.read()` blocking in async stream generator** — every audio chunk read called `out.read()` synchronously on the event loop; replaced with `await asyncio.to_thread(out.read, _CHUNK)`.
- **[backend] tidal — PKCE `code_verifier` logged on token-exchange failure** — full error response body written to logs; now only `error` and `error_description` fields are logged.
- **[backend] tidal — concurrent `start_pkce()` calls silently corrupted each other's verifier** — logged a warning when a flow is already pending; callers should not call `start_pkce` twice without completing the flow.
- **[backend] qobuz — `_extract_secrets` silently produced wrong secrets when bundle regex found no matches** — now raises `RuntimeError` when no timezone has a complete seed+info+extras triplet.
- **[backend] qobuz — concurrent bundle cache misses fetched the 200 KB JS twice** — `asyncio.Lock` added with double-checked locking.
- **[backend] radio — `_discover_mirrors` fire-and-forget task not tracked** — `_discover_task` stored on instance; `stop()` added to cancel it; exceptions now surface via `add_done_callback`.
- **[backend] radio — `_by_url` dict grew unbounded from search hits** — capped at 1000 entries with eviction of non-saved entries.
- **[backend] player — `_get_active_alsa_card` blocked event loop on `/proc/asound` scan during DSD poll** — synchronous filesystem walk extracted to `_scan_active_alsa_card_sync` and called via `asyncio.to_thread`.
- **[core] sse_manager — `shutdown()` called `.cancel()` on a `List[Task]` instead of each task** — `AttributeError` on every graceful shutdown; monitoring loops kept running after the event loop closed.
- **[core] utils/files — `os.fsync()` in `atomic_write_json` blocked event loop 50–300 ms on SD card flush** — removed; `os.replace()` atomic rename is sufficient for config-file integrity.
- **[core] dbus_client — `get_dbus_client()` singleton had no concurrency guard** — two concurrent callers both created separate D-Bus connections; `asyncio.Lock` added.
- **[core] roon_client — `get_roon_client()` singleton had no concurrency guard** — `asyncio.Lock` with double-checked locking added.
- **[core] http — `_get_shared_session()` not coroutine-safe** — two concurrent first callers both created `ClientSession`; `asyncio.Lock` added.
- **[core] dbus_client — bare `except: pass` swallowed `asyncio.CancelledError`** — replaced with `except (TypeError, ValueError): pass`.
- **[core] ttl_cache — `TTLCache.get()` always missed for a cached `None` value** — `_value is not None` guard prevented `None` from being representable as a cache hit; replaced with `_UNSET` sentinel.
- **[core] JWT and auth error messages in French** — `"Token invalide ou expiré"`, `"Accès réservé aux administrateurs"`, `"Les invités ne sont pas autorisés"` translated to English (returned verbatim in JSON API responses).
- **[packages] `www.lesbonscomptes.com` domain entry did not survive `www.` stripping** — changed to `lesbonscomptes.com` fixing an intermittent test failure.
- **[license-server] XSS in portal upgrade and download forms** — `filename` from the server `Content-Disposition` header and `newKey` from user input were injected into `.innerHTML` without escaping; a crafted value could exfiltrate the admin session token. HTML-escaping helper `_esc()` added to both components.
- **[license-server] `version_scope` stripped on license resend, bulk-resend, and transfer** — `generate_lic()` was called without the `version_scope` parameter, silently converting v1-scoped licenses to all-versions licenses and bypassing the upgrade paywall.
- **[license-server] All-versions lifetime licenses incorrectly rejected on AG v2** — `payload.get('version_scope', '1')` defaulted absent scope to `"1"`, causing `version_expired` for licenses issued before scoping was introduced. Default changed to `None` (no check when field is absent).
- **[license-server] Admin token comparison was not constant-time** — `!=` string comparison allowed character-by-character brute-force timing attack; replaced with `hmac.compare_digest`.
- **[license-server] Blocking SMTP calls on the async event loop** — all `mailer.send_*()` in admin handlers now use `await asyncio.to_thread(...)`.
- **[license-server] Blocking file I/O in `import_db`** — `shutil.copy2` and `Path.write_bytes` wrapped with `asyncio.to_thread`.
- **[license-server] `purge_audit` read `db.total_changes` (cumulative) before `commit()`** — now reads `cur.rowcount` after the DELETE for an accurate count.
- **[license-server] `/deactivate` unprotected when `VERIFY_KEY` is empty** — `@limiter.limit("10/minute")` added.
- **[license-server] Revoked license could be deactivated, corrupting audit trail** — `AND revoked_at IS NULL` added to the `deactivate_order` UPDATE condition.

### Added
- **[backend] audio_hw — `force_refresh` query parameter on `GET /audio-hw/devices`** — `?force_refresh=true` bypasses the 60 s cache and triggers an immediate rescan, useful after a USB hotplug event.
- **[backend] audio_hw — `total_cards` as a computed field** — converted to Pydantic v2 `@computed_field`; can no longer diverge from `len(cards)`.
- **[backend] `requirements-dev.txt`** — test dependencies (`pytest`, `pytest-asyncio`, `httpx`) separated from `requirements.txt` in `audiogravity.core`.
- **[tests] audio_pipeline** — `TestDetectMpdFormat`, `TestAlsaPcmState` (latency, 2**64 wraparound, closed device), `TestHqplayerVolume` (clamping, None), `TestPidIdentifyCacheType` — 64 tests passing.
- **[landing] `THIRD_PARTY_NOTICES.md`** — full attribution for all open-source components: frontend (Lit, Cytoscape, dagre, Lucide, Chart.js, CodeMirror, Inter, JetBrains Mono), backend (FastAPI, Pydantic, pywebpush/MPL-2.0, cryptography, roonapi, 15+ libraries), runtime binaries (ffmpeg/LGPL, cyclictest/GPL-2, iperf3/BSD-3, smartctl/GPL-2), external API (Radio Browser), and optionally-installable audio software (MPD, upmpdcli, shairport-sync, HQPlayer NAA, Roon Bridge/Server).
- **[landing] `index.html`** — announce bar updated to v0.9.4; Features section: title includes Tidal, Unified Transport card adds stream origin badge, High-resolution library card mentions UPnP search playable, MQA removed from signal-path description; Compare table: new row for native Tidal & Qobuz streaming (OAuth2/PKCE), UPnP row updated to mention search + directly playable results; footer version v0.9.4 and "Open Source" link in Legal.
- **[landing] `README.md`** — reference to `THIRD_PARTY_NOTICES.md` in license paragraph and Documentation section.

## [0.9.4] - 2026-06-20

### Fixed
- **[backend] Pydantic v2 deprecation — `.dict()` → `.model_dump()`** — `services/service.py` was using the deprecated `.dict()` method; replaced with `.model_dump()`.
- **[tests] RuntimeWarning coroutines never awaited** — two test helpers left coroutines unawaited when patching `asyncio.wait_for`; both fixed by closing coroutines before raising or restructuring the mock.
- **[frontend] Code duplication removed across components** — `loadConnection(host, fetchFn, tag)` helper extracted to `utils-lit.js`, used by Qobuz/Tidal/HQPlayer output molecules (3×10 lines removed). `queueWithFeedback(queueFn, label)` helper added to `library-api.js`, used by `ag-library-search` and `ag-library-browse`. `_formatRelativeTime()` removed from `ag-service-card` and `ag-profile-card` in favour of the existing `formatTimestamp()` from `utils-lit.js`. 16 unit tests added (formatTimestamp, loadConnection, queueWithFeedback, escapeHtml XSS, jitterChart destroy, push URL format, password trim).
- **[frontend] XSS — `escapeHtml` imported directly in `ag-admin-page`** — removed `window.escapeHtml ? ... : username` ternary; `escapeHtml` now imported as an ES6 module so username is always escaped in the delete-user confirmation dialog.
- **[frontend] XSS — `unsafeHTML(this.label)` removed from `ag-metric-detail`** — label prop now bound with Lit's auto-escaping (`${this.label}`); unused `unsafeHTML` import removed.
- **[frontend] Memory leak — `ag-network-test` jitter Chart.js not destroyed** — `this._jitterChart.destroy()` added to `disconnectedCallback()`.
- **[frontend] Push unsubscribe used wrong HTTP method** — changed from `POST` with JSON body to `DELETE` with query param (`apiDelete('/push/unsubscribe?endpoint=...')`), matching the backend router.
- **[frontend] Password trim in user modal** — `this._password` now `.trim()`-ed before validation; whitespace-only passwords are caught by the existing `length < 6` check instead of reaching the backend.
- **[backend] core — D-Bus proxy cache eviction on error** — stale unit proxies are now removed from `_unit_proxy_cache` on `call_get_all` failure so the next call rebuilds a fresh proxy instead of reusing a dead one indefinitely.
- **[backend] core — Roon disconnect timeout** — `_roon_api.stop()` wrapped in `asyncio.wait_for(timeout=5)` to prevent indefinite hang; state is always cleaned up in `finally`.
- **[backend] core — JWT decode error log sanitised** — exception logged as `type(e).__name__` only, preventing any token fragment from appearing in logs.
- **[backend] core — EventBus `QueueFull` now logged** — slow subscriber drop logged at DEBUG level for diagnostics; `logging` module added to `events.py`.
- **[backend] sysinfo — `smartctl` `FileNotFoundError` crashes monitor** — caught and degraded gracefully; disk temperature returns `None` when `smartctl` is absent. `SYSLOG_IDENTIFIER` fixed to `_SYSLOG_IDENTIFIER=` (journalctl match syntax). Invalid `grep_pattern` regex now returns 400. `lscpu` absence caught. Admin PTY shell logs an audit entry.
- **[backend] push — `webpush()` without timeout** — `timeout=10` added to prevent indefinite blocking on unreachable endpoints. Endpoint now validated as HTTPS URL. `endpoint` query param annotated with `Query()`. `logger.error` on successful unsubscribe changed to `logger.info`.
- **[backend] config_validation — `appconfigfile` path traversal** — paths now validated against `/etc` and `/usr/local/etc` whitelist (mirrors `audio_app_config`). `systemd_unit` bounded to `max_length=255`. Substring match replaced with line-start check. `ValueError` in validation now returns 400 instead of 500.
- **[backend] Steering — ALSA device injection via config write** — `alsa_device` now validated against `^hw:\d+,\d+$` before any config file substitution; `get_steerability()` no longer hardcodes `upmpdcli`/`roonbridge` as always available; `_verify_alsa_device_exists()` checks `/proc/asound/cardX/pcmYp` (playback subdevice), not just the card directory.
- **[backend] Performance — cyclictest `IndexError` on trailing token** — bounds check (`i + 1 < len(tokens)`) added to the cyclictest line parser.
- **[backend] Performance — `$CONFIG_FILE` unquoted in boot script** — config path now passed as `sys.argv[1]` and shell-quoted (`"$CONFIG_FILE"`), preventing word-splitting on paths with spaces.
- **[backend] Performance — `duration_seconds` always 0** — test start captured with `time.monotonic()`; actual elapsed time stored in `LatencyTestResult`.
- **[backend] Performance — bare `except:` clauses** — replaced with `except (ValueError, IndexError)` and `except (subprocess.TimeoutExpired, OSError)`.
- **[backend] Profiles — `asyncio.gather()` without timeout** — both stop and start phases wrapped in `asyncio.wait_for(timeout=30)`.
- **[backend] Profiles — `stopped_count` counted FAILED as stopped** — FAILED state now goes to `failed_count`; only INACTIVE/DEAD states increment `stopped_count`.
- **[backend] Profiles — export written to world-readable `/tmp`** — export path moved to `settings.audiogravity_home` with `chmod(0o600)`.
- **[backend] License — server response handling hardened** — `/check` and `/activate` now verify HTTP status before calling `resp.json()`; unexpected Pydantic shapes return 502; `lic_content` validated as JSON before writing to disk; `X-Verify-Key` header extracted to `_verify_headers()` helper; `_portal_base()` validates URL structure.
- **[backend] Services — enum comparison bug** — `validate_service_properties` was comparing `CPUSchedulingPolicy`/`IOSchedulingClass` enum members to plain strings (always-false conditions); corrected to compare against enum values.
- **[backend] Services — D-Bus call unguarded** — `get_unit_file_state()` now wrapped in `asyncio.wait_for(timeout=2s)`; timeout logs a warning and falls back to subprocess.
- **[backend] Services — stale cgroup FD not evicted** — `fd.seek(0)` failure now evicts the dead FD from the LRU cache instead of leaving it for the next call.
- **[backend] Services — `service_name` path param unvalidated** — all `service_name` Path params now carry `pattern=r"^[a-zA-Z0-9._@-]+(?:\.service)?$"` → 422 on invalid input.
- **[backend] audio_app_config — path traversal via symlink** — `_validate_path` now calls `resolve()` first, then checks `is_relative_to()` on the resolved path; a symlink pointing outside `/etc` is rejected even if the link itself lives inside `/etc`.
- **[backend] audio_app_config — restart duplication** — `_restart_service()` extracted; `update_config` and `restore_backup` both delegate to it.
- **[backend] audio_app_config — `model_validator` incorrect** — `@field_validator('content','data')` replaced with `@model_validator(mode='after')` for correct single-evaluation semantics.
- **[backend] Packages — shell injection via installer config** — `install_script_args`, `check_command`, `uninstall_commands` and `version_check_command` now use `shlex.split` + `create_subprocess_exec` instead of `shell=True` f-strings. `version_check_url` validated against `ALLOWED_DOWNLOAD_DOMAINS`. `gpg_key_path` and `sources_list_path` validated by `_validate_destination_path()` before any `sudo cp`. `_validate_package_name()` added in `apt_repo.py`. 9 security tests added.
- **[backend] Player `_poll_loop` NameError on `get_now_playing()` failure** — `items` now initialised to `[]` before the try block, preventing `NameError` when `get_now_playing()` raises.
- **[backend] Player DSD state inconsistent after partial `gather()` failure** — `_dsd_active` reset to `False` on exception so volumes are not left partially forced.
- **[backend] Auth `POST /users` returned 200 instead of 201** — corrected to `HTTP_201_CREATED`.
- **[backend] Auth `PATCH /users/{u}` accepted whitespace-only password** — passwords that are blank after `.strip()` are now rejected with 400.
- **[backend] Auth `update_user` race condition post-update** — `update_user()` now returns `Optional[User]` directly, eliminating the separate `get_user()` call after write.
- **[backend] Auth WebAuthn userHandle exception was silent** — bare `except` replaced with `logger.warning()` for diagnosis; `_b64url_to_bytes` moved to module top.
- **[core] `users.py` write race condition** — `_save_users` now holds a `threading.Lock` for thread-safe concurrent writes.
- **[core] JWT missing `jti` claim** — `uuid.uuid4()` added to every token payload, enabling future revocation support.

### Added
- **[backend] HQPlayer `POST /hqplayer/stop`** — endpoint to stop playback (was documented but not implemented); also adds `stop()` service method and `has_dsp_config` public property. 13 unit tests added covering stop, Literal validation, `has_dsp_config`, `_read_xml_response` helper, and play request validation.

### Fixed
- **[backend] Radio `PUT /radio/{uuid}` broken** — `edit_station()` was awaited incorrectly (missing `await`), causing `PUT` to always return a coroutine instead of the result.
- **[backend] Radio `added_at` timezone-unaware** — `datetime.utcnow()` (deprecated Python 3.12) replaced with `datetime.now(timezone.utc)`.
- **[backend] Audio pipeline DSD stream not detected** — `audio_str="dsd64:2"` caused `int("dsd64")` → ValueError silently swallowed; DSD multiplier now parsed correctly (`dsd_mult × 44100`, 1-bit).
- **[backend] Audio pipeline cgroup v1 PID→service mapping** — `split("::", 1)` only matched cgroup v2; now uses `fields[-1]` to support both formats.
- **[backend] Audio pipeline `dbus-send` without timeout** — both subprocess `communicate()` calls now wrapped with `asyncio.wait_for(timeout=3.0)` + `proc.kill()` on expiry.
- **[backend] Audio pipeline MPD URI control-char filter** — `any(ord(c) < 0x20)` replaces the newline-only check.
- **[backend] Library UPnP queue ignores `output_id`** — `upnp_search_queue` now honours `req.output_id` like Qobuz/Tidal.
- **[backend] Library SOAP Browse object_id not XML-escaped** — `_sax.escape(object_id)` applied before template formatting.
- **[backend] Library Qobuz album/playlist queue duplicated** — extracted `_queue_qobuz_tracks()` helper (~25 lines removed).
- **[backend] Library `_tidal_cover` crashes on dict uuid** — `isinstance(uuid, str)` guard added.
- **[backend] Qobuz `private_key` leaked in query string** — `_exchange_code` changed from GET+params to POST+body.
- **[backend] Qobuz token refresh race condition** — `asyncio.Lock` added to `TidalOAuthService.get_access_token` with double-check pattern.
- **[backend] Qobuz half-authenticated state** — `handle_callback` returns `False` when `_find_working_secret()` returns None instead of saving an `app_secret=None` state.
- **[backend] Qobuz `user_id` could be string `"None"`** — `str(user.get("id"))` when id is JSON null now correctly returns `None`.
- **[backend] Tidal stale token not cleared on network error** — `_access_token` set to `None` when refresh fails and token is past expiry.
- **[backend] HQPlayer `item_type`/`action` unvalidated** — changed from `str` to `Literal["track","album","artist"]` / `Literal["play","add"]` in `HQPlayerPlayLibraryRequest`.
- **[backend] HQPlayer XML parsing duplicated** — extracted `_read_xml_response()` static helper used by both `_send()` and `_send_batch()`.
- **[core] `get_shared_session()` exported** — `LibraryService._http_session()` now delegates to the app-wide shared session (closed on graceful shutdown), eliminating socket leak.

### Added
- **[frontend] Config editor — blank configuration hint** — when a service
  config file has all sections empty (package defaults active), the form view
  now shows an info banner explaining the state and offering a direct link to
  Expert Mode to view and uncomment the full file.
- **[backend] Tidal/Qobuz credential rotation detection** — 401/403 responses
  from `playbackinfopostpaywall` (Tidal) and `track/getFileUrl` (Qobuz) after
  token refresh now raise typed exceptions (`TidalClientRotatedError`,
  `QobuzClientRotatedError`) logged at ERROR level with a remediation hint.
  The Tidal stream endpoint returns HTTP 503 instead of 404 on rotation. 10
  unit tests cover both services.
- **[frontend+backend] Stream origin badge in the players** — the mini and
  fullscreen Now Playing views now show where the audio comes from (Tidal, Qobuz,
  a UPnP/DLNA server by name, radio, a local file, Roon, AirPlay…) with a logo +
  label, instead of an undifferentiated "MPD". The backend tags each playing
  source with its provider, independent of transport.
- **[landing] FAQ — connecting Qobuz or Tidal** — one entry covering both flows:
  Qobuz OAuth (auto-redirect, no paste) and Tidal PKCE (copy/paste the redirect
  URL), noting the required subscription tier for each.
- **[backend] UPnP search queue** — clicking "+" or play on a UPnP/DLNA search
  result now works: track stream URLs are passed directly to MPD, album items are
  resolved via ContentDirectory Browse. Titles and cover art are pre-registered
  during search so the queue display and Now Playing badge are enriched immediately.
  17 unit tests cover track/album/routing/metadata-registration cases.

### Fixed
- **[backend] `_ext_stream_key` anchored to URL path/query** — Tidal detection
  now checks the URL *path* for `/tidal/stream/` and Qobuz detection checks the
  *query string* for `eid=`, instead of raw substring matching. Prevents a UPnP
  URL whose path contains `/tidal/stream/` or `eid=` from being misclassified.
  8 regression tests added.
- **[frontend] Software tab description** — removed the "dry-run simulation"
  claim from the Pro feature list; the toggle is admin-only and not visible to
  regular Pro users.

### Changed
- **[frontend] Library search lists UPnP/DLNA servers** — known media servers
  (e.g. MinimServer) now appear as sources in Library search, alongside MPD, Roon,
  Qobuz and Tidal (previously missing).
- **[frontend] UPnP/DLNA text search from the Search tab** — selecting a UPnP/DLNA
  server badge while in the Search tab now stays in search mode and runs a text
  query against the server (previously always redirected to the UPnP browser).
- **[frontend] Settings: single version + logout moved in** — the panel now shows
  one unified product version (front and back share it) with the Swagger API link,
  and the Logout button moved from the top bar into the Settings footer.
- **[frontend] Top-bar icons** — the settings button now uses a gear icon and the
  mobile navigation button a hamburger (swapped for clarity).
- **[frontend] Source connection status uses the shared status dot** — Qobuz,
  Tidal and HQPlayer now render the same status indicator as the other sources.

### Fixed
- **[frontend] Qobuz sign-in flow** — the Qobuz OAuth page now opens in a popup
  (the AG UI stays underneath) that closes itself once authentication succeeds, so
  you land back in AudioGravity automatically instead of having to close the tab
  and reopen the app.
- **[frontend] Missing-cover icon in the fullscreen player** — the "no artwork"
  placeholder icon was rendered far too small; it now fills the cover area again.
- **[backend] Tidal playback skipped every track** — the seek cache pre-created
  the remux output file, so ffmpeg (run without `-y`) refused to overwrite it and
  exited having written 0 bytes; MPD received an empty stream and skipped to the
  next track. ffmpeg now overwrites the placeholder, and a 0-byte remux is never
  cached.
- **[frontend] Bundle analysis report no longer deployed** — the Vite `stats.html`
  bundle treemap was copied into the build output and shipped to production
  (reachable at `/stats.html`). It is now opt-in only (`vite build --mode analyze`)
  and written outside the deployed output, so it never ships.

### Removed
- **[frontend] Standalone styleguide page** — the unused `styleguide.html`
  design-system gallery was removed (Storybook is the live component reference).

## [0.9.3] - 2026-06-14

### Added
- **[backend+frontend] Tidal streaming source** — connect a Tidal HiFi account
  (PKCE login) and browse Favorites / New Releases / Playlists, plus search;
  playback streams **lossless FLAC** through a local DASH→FLAC ffmpeg proxy (Tidal
  delivers FLAC as segmented DASH, not a direct URL). Requires `ffmpeg` (added to
  the backend installer).
- **[backend+frontend] Tidal Charts & Editorial browse** — two new browse pills:
  **Charts** (TIDAL's Top Hits, Viral / Rap / R&B / Pop Hits…) and **Editorial**
  (Popular, Trending, TIDAL Rising, Podcasts…), extracted from Tidal's home page
  and rendered as playlists; tapping one opens its tracks like any playlist.
- **[backend] Tidal in-track seek** — the proxy remuxes each track to a seekable
  FLAC file (served as it is produced, so start-up stays fast) and keeps it in a
  small, disk-backed cache (current track + a couple of recent, wiped at startup).
  Replays and reopens are served with HTTP Range, so you can seek within Tidal
  tracks. The very first play of a track in a session is not seekable; replays are.
- **[frontend] Top bar — mobile navigation toggle** — a left-side button opens the
  vertical tab menu on mobile, mirroring the settings burger on the right.
- **[frontend] Top bar — Library shortcut** — a one-tap button (left of Logout)
  jumps straight to the Library tab; licence gating is preserved (a locked tab
  opens the licence modal instead).
- **[frontend] Roon source logo** — the `RN` text placeholder for Roon sources is
  replaced by a Roon logo rendered as a `currentColor` mask, so it stays visible in
  light, dark and the active (selected) state.

### Changed
- **[frontend] DRY-RUN toggle is now admin-only** — the Audio Software DRY-RUN
  simulation is scoped to administrators (a command-preview / catalog-validation
  tool, not a dependency-resolving simulation); its size now matches the settings
  toggles.

### Fixed
- **[frontend] Login page version label** — shown as `v0.9.2` (lowercase prefix,
  no space).
- **[backend] AirPlay now-playing on ARM** — shairport-sync track metadata leaked the
  raw `<dbus_fast…Variant…>` repr in the pipeline now-playing; the `a{sv}` values are
  now unwrapped (portable, no-op on x86).
- **[frontend] Fullscreen player volume swipe** — adjusting the volume slider no longer
  triggers the player's multi-source swipe.
- **[frontend] Library horizontal scroll** — scrolling a horizontal row (pills, album
  shelves) no longer switches tabs; the swipe-to-switch handler now yields to any
  horizontally-scrollable ancestor (CSS class or inline overflow), not just inline ones.
- **[frontend] Fullscreen player pull-down dismiss** — swiping down to scroll back up in
  a long tracklist no longer dismisses the player; the dismiss gesture only fires when
  the scroll area is already at the top.

### Removed
- **[frontend] Obsolete top-bar buttons** — the documentation (audiogravity.app)
  button and the admin "Components" (bundle stats) button were removed.
- **[frontend] Tab-bar now-playing** — the vertical tab sidebar no longer displays
  the current stream (redundant with the mini player).

---

## [0.9.2] - 2026-06-09

**Focus: Qobuz Hi-Res streaming integration + DSD volume safety.**

### Added
- **[backend] Qobuz OAuth2 module** (`modules/qobuz/`): full OAuth2 authentication
  replacing the deprecated username/password login. Bundle credential extraction from
  the Qobuz web player JS, OAuth URL generation, browser-based login, code-to-token
  exchange, working secret discovery, and persistent config storage.
- **[backend] Qobuz search, browse, and playback** (`library/service.py`): header-based
  API auth (`X-App-Id`/`X-User-Auth-Token`), correct API signature format (float
  timestamp, ASCII+UTF-8 byte concatenation), 3 parallel single-type search calls,
  album queueing, cover art on all browse/search methods.
- **[backend] Qobuz catalog browsing** — featured albums (`album/getFeatured`),
  editorial playlists (`playlist/getFeatured`, `playlist/get`). Three new endpoints:
  `GET /library/qobuz-featured`, `GET /library/qobuz-playlists`,
  `GET /library/qobuz-playlist-tracks`. Playlist queueing support.
- **[backend] External stream metadata registry** (`now_playing.py`): stable key
  derivation from `eid` query parameter for Qobuz streams — correct title, artist,
  album, and cover art in now-playing and queue despite ephemeral signed URLs.
- **[backend] Qobuz as virtual source** — `src_qobuz` injected in the player when
  connected; bitrate displayed for Qobuz FLAC streams.
- **[frontend] Qobuz connection card** (`ag-qobuz-output.js`): OAuth2 connect/disconnect
  molecule for the Sources view, with polling and events.
- **[frontend] Qobuz catalog pills** (`ag-library-browse.js`): browse pills switch to
  Favorites / New Releases / Selection / Playlists when Qobuz is selected.
- **[frontend] Qobuz icon** on source cards (optimized 56×56 webp).
- **[tests] Qobuz OAuth2 unit tests** (24 tests): bundle extraction, service
  persistence, OAuth flow, Pydantic models, router endpoints.
- **[tests] Qobuz catalog browsing unit tests** (22 tests): featured albums,
  playlists, playlist tracks, search, cover helper, library router endpoints.
- **[tests] DSD volume unit tests** (10 tests).
- **[dev] `./dev.sh test --report`** generates `TEST_REPORT.md` — markdown summary
  with per-suite pass/fail/skip counts, durations, and failure detail.

### Changed
- **[backend] Qobuz config cleanup** — removed `qobuz_app_id`, `qobuz_app_secret`,
  `qobuz_username`, `qobuz_password` settings; OAuth2 manages credentials via UI.
- **[build] `build-backend-package.sh`** — `qobuz` added to `ENABLED_MODULES` template
  and upgrade migration loop; `QOBUZ_FORMAT_ID=27` in `.env` template.
- **[frontend] Topbar doc button** opens `audiogravity.app`; internal doc links removed
  from settings panel.
- **[docs] Single source of truth** — `CHANGELOG.md` and `RELEASE_NOTES.md` consolidated
  in the landing repository; AG-repo copies marked obsolete in `CLAUDE.md`.

### Fixed
- **[backend] DSD volume protection** (`player/service.py`): 6 bugs causing volume to
  snap to 100% during non-DSD playback — stale HQPlayer cache, race conditions,
  incorrect restore target.
- **[backend] HQPlayer stale track** — `_current_track` cleared after 30s stopped.

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
- **[packaging] upmpdcli on ARM64** — `scripts/build-upmpdcli-arm64.sh` builds the
  libnpupnp → libupnpp → upmpdcli chain natively for aarch64 and publishes a
  checksum-verified `.deb` bundle on `audiogravity.app`. The package registry
  installs it via a per-arch `arch_fallback` (no upstream arm64 package exists
  anywhere); the official source still wins where it covers the arch.
- **[install] WebAuthn passkeys at install** — `--public-url` sets
  `WEBAUTHN_ORIGIN` and derives `WEBAUTHN_RP_ID`; forwarded by the bootstrap and
  all-in-one installers and documented in the README (passkeys require a real
  HTTPS domain, not a bare IP).
- **[install] Push contact** — `--vapid-email` sets the VAPID `sub`; forwarded by
  the installers.
- **[frontend] HQPlayer manual IP entry** — connect to a HQPlayer on a different
  (but routable) subnet that the local /24 discovery scan can't reach.
- **[frontend] Standalone server WebSocket proxy** — the prod Python server now
  proxies the admin terminal WebSocket (`/sysinfo/terminal/ws`) via raw tunneling.
- **[landing] Page** — the "Releases" link now points to the public GitHub repo;
  install section clarified (works on the LAN by default, passkeys/push moved to an
  optional block that requires a public domain); portable local preview `dev.sh`
  (auto-detected LAN IP).
- **[deps] Deterministic dependencies** — `requirements.lock` (68 packages pinned,
  wheels verified for x86_64 **and** aarch64, Python 3.13.5) + runtime/build split
  (`requirements-dev.lock`); license server dev requirements (`requirements-dev.txt`).
- **[tests]** — VAPID key loading, PayPal IPN webhook flow (8 tests), and scoped
  pytest warning filters for third-party deprecations.

### Changed
- **[backend] Auth** — replaced `passlib` with direct `bcrypt` calls.
- **[frontend] Prod server consolidation** — the frontend package now bundles the
  canonical `serve_https.py` (line-by-line SSE streaming + gzip) instead of a
  divergent, broken inline copy; the systemd unit invokes it with args +
  `WorkingDirectory`.
- **[install] Production `.env` configured at install** — license server URL/key,
  VAPID, and `ENABLED_MODULES` (incl. `hqplayer`).
- **[build] `build-backend.sh` self-bootstraps** — installs system prerequisites
  and `python3`; the generated installer uses non-interactive `apt`; deps synced
  via `pip install -r` with wheels only.

### Fixed
- **[frontend] Prod SSE stuck on "Connecting…"** — the packaged proxy buffered the
  event stream (`shutil.copyfileobj`); now streamed so the UI connects.
- **[frontend] Broken-pipe traceback noise** in the standalone server when a client
  drops a keep-alive connection (e.g. after closing an SSE tab).
- **[backend] Runtime bugs surfaced on ARM** — CPU model (lscpu fallback), governor
  field (`current_governor`), `cpu-governor.service` boot script (stdlib `json`),
  and `ORJSONResponse` deprecation warnings.
- **[backend] Service config paths** resolved across OS layouts (`/etc` vs
  `/usr/local/etc`) and reloaded when software is installed/removed at runtime.
- **[backend] `hqplayer` module** missing from the packaged `.env` `ENABLED_MODULES`
  (its endpoints returned 404).
- **[backend] aarch64 startup crash** — caused by `passlib` vs `bcrypt>=4.1`.
- **[packaging] Audio-software install made arch-aware** — Roon per-arch URLs
  (`{roon_arch}`), download allowlist, stdin for interactive vendor installers, and
  complete uninstall; upmpdcli `.deb` ships its systemd unit, creates its system
  user, and stops/disables cleanly on removal.
- **[install] sudoers** completed (including Roon uninstall) and hardened
  (`sudo tee` instead of `sudo sh -c`).
- **[build] Nuitka / packaging** — explicit includes (psutil, distro, orjson,
  pydantic, ntplib), `SHA256SUMS` merge + checksum verification in installers,
  missing transitive deps (pyparsing, ifaddr), `gh` auto-install, `license.pub`
  lookup, and miscellaneous installer robustness fixes.
- **[dev] Environment scripts** — no longer hardcode `/home/dietpi` paths or LAN
  IPs (runtime detection); seed a default `admin` user; provision dev sudoers/polkit;
  resolve `visudo` by absolute path on DietPi.

### Removed
- **[build]** obsolete `backend/update.sh` (incompatible with the Nuitka-binary
  production model).

---

> Scope note: this release consolidates the `arm-debian-compat` work (main repo)
> plus this landing repository. The earlier `v0.9.1` tag (`b3ab0c2`) was never a
> release — delete it (local + remote) and re-tag the release commit as `v0.9.1`.
