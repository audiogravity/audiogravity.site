# Audiogravity — Test Report

Generated: **2026-07-13 10:12 UTC**

## Summary

| | Tests | Passed | Failed | Skipped | Duration |
|---|---:|---:|---:|---:|---:|
| **core** FAIL | 1 | 0 | 1 | 0 | 1.3s |
| **ui** PASS | 441 | 441 | 0 | 0 | 1.0s |
| **Total** FAIL | **442** | **441** | **1** | **0** | **2.2s** |

## Failures

- **core** / `::tests.test_now_playing` — collection failure

## Detail

### core

**(root)**

  - [!] tests.test_now_playing — collection failure

### ui

**js/api.test.js**

  - [+] buildAuthedUrl — URL construction > includes api_key param when provided
  - [+] buildAuthedUrl — URL construction > does not include api_key when empty
  - [+] buildAuthedUrl — URL construction > appends JWT token when provided
  - [+] buildAuthedUrl — URL construction > does not append token param when token is null
  - [+] buildAuthedUrl — URL construction > forwards extra params
  - [+] buildAuthedUrl — URL construction > does not append extra params with null/undefined/empty values
  - [+] buildAuthedUrl — URL construction > includes the path in the returned URL
  - [+] buildAuthedUrl — URL construction > returns a string
  - [+] buildAuthedUrl — URL construction > api_key and token both present when both provided

**js/auth-init.test.js**

  - [+] initAuth — corrupted localStorage (JSON.parse regression) > returns false without throwing when jwt_user is malformed JSON (0.03s)
  - [+] initAuth — corrupted localStorage (JSON.parse regression) > clears auth state when jwt_user is invalid JSON
  - [+] initAuth — corrupted localStorage (JSON.parse regression) > returns true for a valid unexpired token
  - [+] initAuth — corrupted localStorage (JSON.parse regression) > does not authenticate with an expired token
  - [+] clearAuth > removes all auth keys from localStorage

**js/auth.test.js**

  - [+] Auth state checkers > isAuthenticated > returns false when not authenticated
  - [+] Auth state checkers > isAuthenticated > returns true when authenticated with valid token
  - [+] Auth state checkers > isAuthenticated > returns false when token is expired (0.01s)
  - [+] Auth state checkers > isAuthenticated > returns false when no token
  - [+] Auth state checkers > getCurrentUser > returns null when not authenticated
  - [+] Auth state checkers > getCurrentUser > returns user when authenticated
  - [+] Auth state checkers > isAdmin > returns false when not authenticated
  - [+] Auth state checkers > isAdmin > returns true for admin role
  - [+] Auth state checkers > isAdmin > returns false for user role
  - [+] Auth state checkers > isGuest > returns false when not authenticated
  - [+] Auth state checkers > isGuest > returns true for guest role
  - [+] Auth state checkers > isGuest > returns false for admin role
  - [+] Auth state checkers > getAuthToken > returns null when not authenticated
  - [+] Auth state checkers > getAuthToken > returns token when authenticated

**js/common.test.js**

  - [+] escapeHtml (P1 — XSS prevention) > escapes < and > as entities
  - [+] escapeHtml (P1 — XSS prevention) > escapes & as &amp;
  - [+] escapeHtml (P1 — XSS prevention) > neutralises XSS payload — no executable HTML tag
  - [+] escapeHtml (P1 — XSS prevention) > leaves plain text unchanged
  - [+] escapeHtml (P1 — XSS prevention) > passes through non-string values unchanged
  - [+] escapeHtml (P1 — XSS prevention) > empty string returns empty string
  - [+] SW reload guard (sw-reloading sessionStorage key) > reloads on first controllerchange and sets guard key
  - [+] SW reload guard (sw-reloading sessionStorage key) > does NOT reload if guard key is already set (loop prevention)
  - [+] SW reload guard (sw-reloading sessionStorage key) > clearGuard removes the key so the next update can reload
  - [+] SW reload guard (sw-reloading sessionStorage key) > clearGuard is idempotent when key is absent
  - [+] SW reload guard (sw-reloading sessionStorage key) > two rapid controllerchange events only reload once

**js/library-api.test.js**

  - [+] queueItem > routes to /library/queue by default
  - [+] queueItem > routes to /hqplayer/play-library when hqplayer_output is true
  - [+] upnpPlay > routes to /library/upnp-play by default
  - [+] upnpPlay > routes to /hqplayer/play when hqplayer_output is true
  - [+] upnpPlay > passes duration as null when not provided
  - [+] queueWithFeedback > calls queueFn and shows success toast on success
  - [+] queueWithFeedback > shows error toast when queueFn throws
  - [+] queueWithFeedback > uses fallback label when label is empty

**js/library-store.test.js**

  - [+] subscribeRendererStatus > invokes callback when renderer-status-update event fires
  - [+] subscribeRendererStatus > stops invoking callback after unsubscribe
  - [+] subscribeRendererStatus > supports multiple independent subscribers
  - [+] subscribeRendererStatus > does not invoke other subscribers after one unsubscribes
  - [+] subscribeRendererStatus > ignores events with null detail
  - [+] subscribeRendererStatus > isolates callback errors — one failing callback does not prevent others
  - [+] getOfflinePlayerSnapshot > returns null when localStorage is empty
  - [+] getOfflinePlayerSnapshot > returns the parsed object when a valid snapshot exists
  - [+] getOfflinePlayerSnapshot > returns null when localStorage contains malformed JSON
  - [+] getOfflinePlayerSnapshot > returns null for empty string value
  - [+] pwa-install-prompt dismiss persistence > banner is not dismissed when localStorage is empty
  - [+] pwa-install-prompt dismiss persistence > sets a numeric timestamp string on dismiss
  - [+] pwa-install-prompt dismiss persistence > is considered dismissed when timestamp is recent (< 30 days)
  - [+] pwa-install-prompt dismiss persistence > is NOT considered dismissed when timestamp is older than 30 days

**js/player-utils.test.js**

  - [+] TRANSITION_GUARD_MS > is 8 seconds
  - [+] inTransition > returns false for null
  - [+] inTransition > returns true when within guard window
  - [+] inTransition > returns false when outside guard window
  - [+] isDsd > detects DSD in string
  - [+] isDsd > returns false for PCM
  - [+] isDsd > detects DSD in format object
  - [+] isDsd > returns false for PCM object
  - [+] isDsd > handles null/undefined

**js/push-manager.test.js**

  - [+] push-manager unsubscribe (Fix P3) > calls apiDelete (not apiPost) on unsubscribe (0.15s)
  - [+] push-manager unsubscribe (Fix P3) > passes endpoint as query param in the URL
  - [+] push-manager unsubscribe (Fix P3) > URLSearchParams encodes the endpoint correctly

**js/ui-helpers.test.js**

  - [+] getUserFriendlyError > maps "Failed to fetch" to connection error
  - [+] getUserFriendlyError > maps "NetworkError" to network error
  - [+] getUserFriendlyError > maps HTTP 401
  - [+] getUserFriendlyError > maps HTTP 403
  - [+] getUserFriendlyError > maps HTTP 404
  - [+] getUserFriendlyError > maps HTTP 500
  - [+] getUserFriendlyError > maps HTTP 503
  - [+] getUserFriendlyError > returns error.detail when available
  - [+] getUserFriendlyError > returns error.message for unknown errors
  - [+] getUserFriendlyError > returns default for empty error

**js/validation.test.js**

  - [+] validation.js > validateAudioConfig > posts the config to the audio-config validation route
  - [+] validation.js > validateTopologyConfig > posts the topology to the topology validation route
  - [+] validation.js > validateTopologyConfig > returns the validation response verbatim (errors + warnings)
  - [+] validation.js > validateTopologyConfig > rethrows when the API call fails

**js/version.test.js**

  - [+] version propagation (single source: audiogravity.ops/VERSION) > VERSION is a valid semver (0.9.15)
  - [+] version propagation (single source: audiogravity.ops/VERSION) > js/core/config.js UI_VERSION matches VERSION (UI display)
  - [+] version propagation (single source: audiogravity.ops/VERSION) > sw.js CACHE_NAME matches VERSION (PWA cache busting)

**js/components/library-constants.test.js**

  - [+] originBadge > returns null for empty/unknown origin
  - [+] originBadge > maps a known origin to its label and an icon
  - [+] originBadge > uses the explicit name over the generic label
  - [+] originBadge > falls back to the library icon for an unknown but truthy origin
  - [+] originBadge > exposes a label for every mapped origin
  - [+] initOriginLabels > merges new origin keys from the backend into ORIGIN_LABELS
  - [+] initOriginLabels > overwrites existing labels with backend values
  - [+] initOriginLabels > keeps static fallbacks intact when the backend is unreachable
  - [+] initOriginLabels > calls GET /player/origins
  - [+] queueSourceLabel — header labels by playing origin > shows the origin label for streams that play over MPD (radio, upnp)
  - [+] queueSourceLabel — header labels by playing origin > keeps the full source label for local library and HIGHRESAUDIO (not "Library"/"HRA")
  - [+] queueSourceLabel — header labels by playing origin > reuses the source label for Qobuz/Tidal (origin and source agree)
  - [+] queueSourceLabel — header labels by playing origin > falls back to the browsed source label when there is no origin
  - [+] queueSourceLabel — header labels by playing origin > falls back to the source label for an unknown origin
  - [+] resolvePlayingSource — SOURCE vs engine > resolves a Qobuz stream (MPD engine) to the Qobuz browse source, not "Local Library"
  - [+] resolvePlayingSource — SOURCE vs engine > resolves Tidal and HIGHRESAUDIO streams to their own browse source
  - [+] resolvePlayingSource — SOURCE vs engine > keeps a local-file stream on the MPD engine ("Local Library")
  - [+] resolvePlayingSource — SOURCE vs engine > leaves non-MPD engines (Roon) on their own source_id
  - [+] resolvePlayingSource — SOURCE vs engine > prefers an explicit origin_name (e.g. UPnP server) for the label
  - [+] resolvePlayingSource — SOURCE vs engine > falls back gracefully for an unknown source
  - [+] normalizeSearchSources > maps a pipeline source to {id,label,group,location}
  - [+] normalizeSearchSources > dedups Roon (src_roon + src_mono-sgen → one)
  - [+] normalizeSearchSources > drops mpris receivers (no library API)
  - [+] normalizeSearchSources > appends known UPnP servers with their location URL
  - [+] normalizeSearchSources > falls back to "UPnP" label and empty location when missing
  - [+] normalizeSearchSources > does not add the same UPnP server twice
  - [+] normalizeSearchSources > tolerates null/undefined inputs

**js/components/utils-lit.test.js**

  - [+] svgIcon > wraps an icon in a sized <svg> with the Lucide stroke convention
  - [+] svgIcon > honours a custom size
  - [+] safeToFixed > formats valid numbers
  - [+] safeToFixed > returns fallback for null/undefined/NaN
  - [+] safeToFixed > supports custom fallback
  - [+] formatMemory > formats MB
  - [+] formatMemory > formats GB
  - [+] formatMemory > handles null
  - [+] formatUptime > formats days
  - [+] formatUptime > formats hours
  - [+] formatUptime > formats minutes
  - [+] formatUptime > handles null
  - [+] formatRate > formats MB/s
  - [+] formatRate > formats GB/s
  - [+] formatRate > formats KB/s
  - [+] formatRate > handles non-number
  - [+] fmtDuration > formats seconds as M:SS
  - [+] fmtDuration > returns --:-- for null/NaN
  - [+] getActivityLevel > returns correct levels
  - [+] getActivityLevel > handles non-number
  - [+] getActivityLevelForCPU > returns correct levels
  - [+] getActivityLevelForMemory > returns correct levels
  - [+] getActivityLevelForRate > returns correct levels
  - [+] pickPrimaryCoverToken > returns track token when only track
  - [+] pickPrimaryCoverToken > returns station token when only station
  - [+] pickPrimaryCoverToken > returns null for empty item
  - [+] pickPrimaryCoverToken > returns null for null
  - [+] pickPrimaryCoverToken > prefers track when both present (default)
  - [+] pickPrimaryCoverToken > prefers station when preferStation=true
  - [+] formatTimestamp > returns -- for null
  - [+] formatTimestamp > returns -- for undefined
  - [+] formatTimestamp > returns "Just now" for recent timestamps
  - [+] formatTimestamp > returns Xm ago for timestamps within an hour
  - [+] formatTimestamp > returns Xh ago for timestamps within 24h
  - [+] formatTimestamp > returns locale string for timestamps older than 24h (0.02s)
  - [+] loadConnection > sets _connection on success and clears _loading
  - [+] loadConnection > sets _connection to null on fetch failure
  - [+] loadConnection > always clears _loading even on failure

**js/components/molecules/ag-announcement-banner.test.js**

  - [+] ag-announcement-banner — localStorage helpers > getDismissed returns empty Set when storage is empty
  - [+] ag-announcement-banner — localStorage helpers > getDismissed survives malformed JSON without throwing
  - [+] ag-announcement-banner — localStorage helpers > saveDismissed + getDismissed round-trip
  - [+] ag-announcement-banner — _icon > returns correct emoji for each known type
  - [+] ag-announcement-banner — _icon > falls back to ℹ️ for unknown type
  - [+] ag-announcement-banner — _emitBadge > emits count=0 when all announcements are dismissed
  - [+] ag-announcement-banner — _emitBadge > emits correct count with partial dismissals
  - [+] ag-announcement-banner — _emitBadge > emits count=N when nothing is dismissed

**js/components/molecules/ag-config-card.test.js**

  - [+] handleEdit > dispatches a bubbling edit-config event with the service id
  - [+] handleEdit > stops propagation so the tile click does not also fire
  - [+] provisioning state defaults > defaults provisionable and configured to false

**js/components/molecules/ag-highresaudio-output.test.js**

  - [+] AgHighresaudioOutput render > shows the login form when disconnected
  - [+] AgHighresaudioOutput render > shows connected card with name and username when connected
  - [+] AgHighresaudioOutput._connect > sets an error when fields are empty (no API call)
  - [+] AgHighresaudioOutput._connect > posts credentials and fires event on success
  - [+] AgHighresaudioOutput._connect > surfaces the error message on failed login

**js/components/molecules/ag-hqplayer-output.test.js**

  - [+] AgHqplayerOutput._renderCard — connection state display > fully connected (available + naa_available) > adds "connected" CSS class to the card
  - [+] AgHqplayerOutput._renderCard — connection state display > fully connected (available + naa_available) > shows "Connected" status label
  - [+] AgHqplayerOutput._renderCard — connection state display > fully connected (available + naa_available) > renders the "Use as output" toggle
  - [+] AgHqplayerOutput._renderCard — connection state display > HQPlayer reachable but NAA offline (available + !naa_available) > does not add "connected" CSS class
  - [+] AgHqplayerOutput._renderCard — connection state display > HQPlayer reachable but NAA offline (available + !naa_available) > shows "NAA offline" status label
  - [+] AgHqplayerOutput._renderCard — connection state display > HQPlayer reachable but NAA offline (available + !naa_available) > hides the "Use as output" toggle
  - [+] AgHqplayerOutput._renderCard — connection state display > HQPlayer offline (!available) > does not add "connected" CSS class
  - [+] AgHqplayerOutput._renderCard — connection state display > HQPlayer offline (!available) > shows "Offline" status label
  - [+] AgHqplayerOutput._renderCard — connection state display > HQPlayer offline (!available) > hides the "Use as output" toggle
  - [+] AgHqplayerOutput.updated() — clears output flag when NAA goes offline > clears _useAsOutput and localStorage when naa_available transitions to false
  - [+] AgHqplayerOutput.updated() — clears output flag when NAA goes offline > does NOT clear flag when naa_available is undefined (transient fetch failure)
  - [+] AgHqplayerOutput.updated() — clears output flag when NAA goes offline > does NOT clear flag when _connection was not in changedProps
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > updates naa_available to false when hqplayer service goes inactive
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > updates naa_available to true when hqplayer service becomes active
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > ignores events for other services
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > does nothing when _connection is null
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > does not mutate _connection when state is unchanged

**js/components/molecules/ag-license-status.test.js**

  - [+] _portalUrl safety validation > accepts https:// URLs
  - [+] _portalUrl safety validation > accepts http:// URLs
  - [+] _portalUrl safety validation > rejects javascript: URLs
  - [+] _portalUrl safety validation > rejects data: URLs
  - [+] _portalUrl safety validation > rejects empty string
  - [+] _portalUrl safety validation > rejects null / undefined
  - [+] _portalUrl safety validation > rejects protocol-relative URLs
  - [+] _priceDisplay — price formatting > formats a valid numeric price (0.02s)
  - [+] _priceDisplay — price formatting > returns empty string for non-numeric price (backend sends garbage)
  - [+] _priceDisplay — price formatting > returns empty string for null
  - [+] _renderAcquisitionSteps — price as text node > embeds price as plain text, XSS payload is inert
  - [+] _renderAcquisitionSteps — price as text node > embeds a valid price string correctly

**js/components/molecules/ag-prov-library-picker.test.js**

  - [+] payloadFor > manual path → music_directory
  - [+] payloadFor > manual empty/whitespace → null
  - [+] payloadFor > usb source → library_usb_uuid + fstype
  - [+] payloadFor > mount source → music_directory
  - [+] payloadFor > no choice → null
  - [+] payloadFor > out-of-range source index → null
  - [+] _emit > updates state and emits library-change with the resolved payload (usb)
  - [+] _emit > emits null payload for an empty manual path

**js/components/molecules/ag-prov-output-picker.test.js**

  - [+] _select > sets selected to the candidate hw and emits output-select with the candidate

**js/components/molecules/ag-rt-monitor.test.js**

  - [+] ag-rt-monitor — _load array coercion > keeps an array response as-is
  - [+] ag-rt-monitor — _load array coercion > coerces an undefined response to [] (no .map crash)
  - [+] ag-rt-monitor — _load array coercion > coerces a non-array object response to []
  - [+] ag-rt-monitor — _load array coercion > leaves _processes an array and records the error when apiGet throws

**js/components/molecules/ag-tabs.test.js**

  - [+] ag-tabs — drag transform cleanup > _clearDragTransform > removes the inline transform from the sidebar and the toggle button
  - [+] ag-tabs — drag transform cleanup > _clearDragTransform > also resets the config modal when present
  - [+] ag-tabs — drag transform cleanup > _clearDragTransform > is safe when the toggle button is not present
  - [+] ag-tabs — drag transform cleanup > _handleTouchMove — edge-swipe turned vertical > clears the inline transform instead of leaving it stuck
  - [+] ag-tabs — drag transform cleanup > _handleTouchEnd — ends with no active/opening drag > clears any orphaned transform before the early return

**js/components/molecules/ag-update-banner.test.js**

  - [+] ag-update-banner — isUpdateAvailable > is false for null / undefined / empty
  - [+] ag-update-banner — isUpdateAvailable > is false when available is false
  - [+] ag-update-banner — isUpdateAvailable > is false when available but latest is missing
  - [+] ag-update-banner — isUpdateAvailable > is true when available with a latest version
  - [+] ag-update-banner — updatePhaseLabel > maps known phases to human labels
  - [+] ag-update-banner — updatePhaseLabel > falls back to a generic label for unknown/empty phases
  - [+] ag-update-banner — terminal phases > treats done/rolled_back/failed as terminal
  - [+] ag-update-banner — terminal phases > does not treat in-progress phases as terminal
  - [+] ag-update-banner — _emitBadge (update-badge event) > emits available:true for an available update, clearing on none
  - [+] ag-update-banner — _emitBadge (update-badge event) > flags a mandatory update
  - [+] ag-update-banner — _emitBadge (update-badge event) > emits available:false when available but latest is missing

**js/components/molecules/ag-upnp-renderer-card.test.js**

  - [+] AgUpnpRendererCard._activeUdn > returns null when no renderer is active
  - [+] AgUpnpRendererCard._activeUdn > returns the UDN of the active renderer
  - [+] AgUpnpRendererCard._activeUdn > returns null when _known is empty
  - [+] AgUpnpRendererCard._onStatusEvent() > updates _status from SSE event
  - [+] AgUpnpRendererCard._onStatusEvent() > does not update _volume when volume is null in event
  - [+] AgUpnpRendererCard._onStatusEvent() > ignores null payload
  - [+] AgUpnpRendererCard._onStatusEvent() > syncs reachable in _known list
  - [+] AgUpnpRendererCard._onStatusEvent() > clears active flag in _known when connected=false
  - [+] AgUpnpRendererCard._onStatusEvent() > does not change other renderers reachable when connected=false
  - [+] AgUpnpRendererCard._onStatusEvent() > clears active on all other renderers when connected=true (prevents double-active)
  - [+] AgUpnpRendererCard._renderMpdRow() > shows Active indicator when MPD output is the active output
  - [+] AgUpnpRendererCard._renderMpdRow() > shows Idle indicator when MPD output is not active
  - [+] AgUpnpRendererCard._renderMpdRow() > shows Switching label while switching to this output
  - [+] AgUpnpRendererCard._renderMpdRow() > shows the output name
  - [+] AgUpnpRendererCard._renderRendererRow() > shows renderer name
  - [+] AgUpnpRendererCard._renderRendererRow() > shows Active indicator when active and reachable
  - [+] AgUpnpRendererCard._renderRendererRow() > shows Reconnecting indicator when active but not reachable
  - [+] AgUpnpRendererCard._renderRendererRow() > shows Idle indicator when not active
  - [+] AgUpnpRendererCard._renderRendererRow() > shows Disconnect button when active
  - [+] AgUpnpRendererCard._renderRendererRow() > does not show Disconnect button when idle
  - [+] AgUpnpRendererCard._renderRendererRow() > shows volume popover when active and volume available
  - [+] AgUpnpRendererCard._renderRendererRow() > does not show volume popover when volume is null
  - [+] AgUpnpRendererCard._renderRendererRow() > shows Switching label while switching
  - [+] AgUpnpRendererCard._renderRendererRow() > shows transport state description when active
  - [+] AgUpnpRendererCard._renderScanSection() > shows Scan renderers button when not scanning
  - [+] AgUpnpRendererCard._renderScanSection() > shows Scanning… while scanning
  - [+] AgUpnpRendererCard._renderScanSection() > shows discovered renderers not in known list
  - [+] AgUpnpRendererCard._renderScanSection() > filters out renderers already in known list
  - [+] AgUpnpRendererCard._renderScanSection() > shows "No new renderer found" when all discovered are already known
  - [+] AgUpnpRendererCard._renderScanSection() > shows "No UPnP renderer found" when known list is empty and nothing discovered
  - [+] AgUpnpRendererCard._renderScanSection() > shows nothing when discovered is null (before first scan)
  - [+] AgUpnpRendererCard._renderScanSection() > renders a co-located (is_local) renderer as a non-selectable info row
  - [+] AgUpnpRendererCard._renderScanSection() > still offers remote renderers as selectable alongside a local one

**js/components/molecules/ag-version-skew-banner.test.js**

  - [+] ag-version-skew-banner — versionsMatch > matches on identical major.minor (patch/pre-release differences ignored)
  - [+] ag-version-skew-banner — versionsMatch > flags a minor-level difference (0.x treats minor as breaking)
  - [+] ag-version-skew-banner — versionsMatch > flags a major-level difference
  - [+] ag-version-skew-banner — versionsMatch > treats unknown versions as compatible (no false warning)

**js/components/organisms/ag-audio-software-page.test.js**

  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > escapes a malicious package label
  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > escapes malicious version strings
  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > renders a normal package correctly after escaping
  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > handles undefined version gracefully

**js/components/organisms/ag-audio-stack-provisioning.test.js**

  - [+] _libraryPayload > manual path → music_directory
  - [+] _libraryPayload > manual with empty path → null
  - [+] _libraryPayload > usb source → library_usb_uuid + fstype
  - [+] _libraryPayload > mount source → music_directory
  - [+] _libraryPayload > no choice → null
  - [+] _canProvision > false without a library
  - [+] _canProvision > true with output + library
  - [+] _canProvision > false while provisioning
  - [+] _disabledReason > asks to select an output when none is selected
  - [+] _disabledReason > asks to select a library when output is set but no library
  - [+] _disabledReason > empty once output + library are chosen
  - [+] _provision > posts the selected output + usb library (with the admin password) and reports success
  - [+] _provision > aborts without posting when the password prompt is cancelled
  - [+] _provision > posts music_directory for a manual library
  - [+] _provision > sets error state on failure
  - [+] _provision > re-fetches status after success so the page refreshes its selected output
  - [+] _loadStatus > loads outputs/sources, pre-selects the recommended output, emits status-loaded

**js/components/organisms/ag-config-editor.test.js**

  - [+] AgConfigEditor.disconnectedCallback — CodeMirror cleanup > calls toTextArea() on the CodeMirror instance and nulls the reference
  - [+] AgConfigEditor.disconnectedCallback — CodeMirror cleanup > does not throw when _cmInstance is null (never initialised)
  - [+] AgConfigEditor.disconnectedCallback — CodeMirror cleanup > does not call toTextArea after a second disconnectedCallback
  - [+] AgConfigEditor — guided/structured/expert mode switching > _applyMode sets the mode and reverts unsaved changes
  - [+] AgConfigEditor — guided/structured/expert mode switching > _setMode is a no-op when already in that mode
  - [+] AgConfigEditor — guided/structured/expert mode switching > _setMode applies directly when not dirty
  - [+] AgConfigEditor — guided/structured/expert mode switching > _setMode confirms before applying when there are unsaved changes
  - [+] AgConfigEditor — guided/structured/expert mode switching > willUpdate opens a provisionable service in guided mode
  - [+] AgConfigEditor — guided/structured/expert mode switching > willUpdate opens a non-provisionable service in form mode
  - [+] AgConfigEditor — originals capture on parent reload (guided-apply safety) > re-captures originals when the parent reloads the config (both props change)
  - [+] AgConfigEditor — originals capture on parent reload (guided-apply safety) > does not re-capture originals on a single-mode edit (only one prop changes)

**js/components/organisms/ag-guided-config.test.js**

  - [+] descriptor > mpd has output + library, airplay has output, upmpdcli none
  - [+] _initialOutputId > matches the pinned output
  - [+] _initialOutputId > falls back to the recommended output when no pin
  - [+] _outputChanged > false when selection equals the pin
  - [+] _outputChanged > true when selection differs from the pin
  - [+] _canApply > false with no changes
  - [+] _canApply > true when the output changed
  - [+] _canApply > true when a library is chosen
  - [+] _canApply > false while busy
  - [+] _apply > patches only the output when only the output changed (airplay)
  - [+] _apply > patches output AND library for mpd, and clears the library choice
  - [+] _apply > does nothing when there is no change
  - [+] _apply > reports an error and does not emit on failure
  - [+] _reset > regenerates with the admin password and emits guided-changed
  - [+] _reset > aborts when the password prompt is cancelled

**js/components/organisms/ag-json-config-modal.test.js**

  - [+] ag-json-config-modal file transfer > _handleDownload > downloads the live editor content under the configured filename
  - [+] ag-json-config-modal file transfer > _handleDownload > falls back to configText when there is no editor yet
  - [+] ag-json-config-modal file transfer > _handleUploadClick > clicks the hidden file input
  - [+] ag-json-config-modal file transfer > _handleFileSelected > loads the file content into the editor and enters edit mode
  - [+] ag-json-config-modal file transfer > _handleFileSelected > does nothing when no file is picked
  - [+] ag-json-config-modal file transfer > _handleFileSelected > surfaces a read error without throwing

**js/components/organisms/ag-library-browse.test.js**

  - [+] ag-library-browse — artist drill-down > _fetchPage hits /library/albums?artist_id=… when an artist is set
  - [+] ag-library-browse — artist drill-down > _fetchPage bypasses the streaming pill routing in artist mode (Tidal)
  - [+] ag-library-browse — artist drill-down > _fetchPage carries the name-as-id for HRA (name-based backend)
  - [+] ag-library-browse — artist drill-down > _sectionLabel shows "Albums by <name>" in artist mode
  - [+] ag-library-browse — artist drill-down > _sectionLabel falls back to "artist" when the name is missing

**js/components/organisms/ag-library-outputs.test.js**

  - [+] ag-library-outputs _activate > success → posts, dispatches change, re-fetches, no toast
  - [+] ag-library-outputs _activate > not applied (backend raises) → surfaces the backend message, no dispatch, still re-fetches (0.01s)
  - [+] ag-library-outputs _activate > network error → toast with fallback message, re-fetch runs in finally
  - [+] ag-library-outputs _activate > clicking the already-active output is a no-op
  - [+] ag-library-outputs _activate > ignores clicks while a switch is already in flight
  - [+] ag-library-outputs _activate > derives the roonbridge service from a roon source
  - [+] ag-library-outputs _activate > MPD switch does not prompt for confirmation
  - [+] ag-library-outputs _activate > AirPlay switch confirms first, then posts when accepted
  - [+] ag-library-outputs _activate > AirPlay switch is aborted when the user cancels the confirm

**js/components/organisms/ag-library-radio.test.js**

  - [+] AbortController — race condition guard > creates a new AbortController on each call
  - [+] AbortController — race condition guard > aborts the previous controller when called a second time
  - [+] AbortController — race condition guard > ignores results from a cancelled request (signal.aborted guard)
  - [+] AbortController — race condition guard > clears loading flag after a successful non-aborted search
  - [+] AbortController — race condition guard > does not clear loading flag when the request is aborted

**js/components/organisms/ag-manual-modal.test.js**

  - [+] ag-manual-modal > exposes the 9 manual chapters in order (0.01s)
  - [+] ag-manual-modal > starts closed
  - [+] ag-manual-modal > open() shows the modal and loads the default (first) chapter (0.03s)
  - [+] ag-manual-modal > open(id) loads the requested chapter
  - [+] ag-manual-modal > auto-loads a chapter when opened via the is-open property (not open())
  - [+] ag-manual-modal > does not double-load: open() sets _loading so updated() skips the auto-load
  - [+] ag-manual-modal > fetches the right URL, renders via marked, and caches (no refetch) (0.04s)
  - [+] ag-manual-modal > de-duplicates concurrent loads of the same uncached chapter (single fetch)
  - [+] ag-manual-modal > shows an error state on a non-OK response and logs it (not swallowed)
  - [+] ag-manual-modal > shows an error state when the network throws (offline box)
  - [+] ag-manual-modal > close() hides the modal and emits manual-close
  - [+] ag-manual-modal > Escape closes an open modal but is ignored when closed
  - [+] ag-manual-modal > renders the 9-item TOC and the rendered chapter body (0.02s)
  - [+] ag-manual-modal > click handling (never navigate the host app away) > switches chapter in place for a tagged intra-manual link
  - [+] ag-manual-modal > click handling (never navigate the host app away) > passes the anchor for a tagged chapter+anchor link
  - [+] ag-manual-modal > click handling (never navigate the host app away) > scrolls for an in-page anchor without loading a chapter
  - [+] ag-manual-modal > click handling (never navigate the host app away) > leaves rewritten external links to the browser (no preventDefault, no in-modal load)
  - [+] ag-manual-modal > click handling (never navigate the host app away) > leaves mailto: links to the OS
  - [+] ag-manual-modal > click handling (never navigate the host app away) > ignores clicks that are not on a link
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceRenderedContent) > tags an intra-manual chapter link and points it at the published URL
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceRenderedContent) > carries the anchor on a chapter+anchor link
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceRenderedContent) > absolutises a sibling repo doc and opens it in a new tab
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceRenderedContent) > leaves in-page anchors and mailto untouched
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceRenderedContent) > is idempotent — a second pass does not re-rewrite a chapter link
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceRenderedContent) > stamps GitHub-style slug ids (punctuation, duplicate dedup, unicode) (0.01s)

**js/components/organisms/ag-network-test.test.js**

  - [+] AgNetworkTest.disconnectedCallback — jitterChart destroy (Fix P2) > destroys _jitterChart when component is disconnected (0.08s)
  - [+] AgNetworkTest.disconnectedCallback — jitterChart destroy (Fix P2) > does not throw when _jitterChart is null

**js/components/organisms/ag-now-playing-fullscreen.test.js**

  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > auto-follows when the backend switches to a new active source
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > does not reconnect SSE when source_id already matches targetSourceId
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > does not auto-follow when playing is false
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > auto-follows across multiple source changes
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > _switchSource sets userOverride and updates targetSourceId
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > _switchSource is a no-op when already on the target source
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > respects override — does not auto-follow after manual navigation
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > override is not lifted while user-chosen source is still playing
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > lifts override and auto-follows when user-chosen source stops playing
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > lifts override and follows new active after chosen source stops
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > SSE reconnects once when override is lifted and source switches
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > immediately follows new source when override is lifted on a playing:false tick
  - [+] AgNowPlayingFullscreen — auto-follow (_applyState) > does not crash when override lifts and no source is playing
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > rendererActive: true when connected and not bypassed
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > rendererActive: false when bypassed
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > rendererActive: false when disconnected
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > rendererActive: false when no renderer status
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > hasSignal: true with non-empty signal_path
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > hasSignal: true with output_label only
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > hasSignal: false with empty path and no label
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > signal path shown when renderer bypassed and signal present
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > signal path shown when no renderer and signal present
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > renderer step present in signal_path when renderer active (backend enrichment)
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > idle renderer badge shown when renderer active but signal_path is empty
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path > idle renderer badge NOT shown when renderer disconnected and no signal
  - [+] AgNowPlayingFullscreen — _nextTrack cleared on renderer disconnect > _nextTrack set from renderer queue when connected
  - [+] AgNowPlayingFullscreen — _nextTrack cleared on renderer disconnect > _nextTrack set to null when queue_next_title is null
  - [+] AgNowPlayingFullscreen — _nextTrack cleared on renderer disconnect > _nextTrack cleared when renderer disconnects
  - [+] AgNowPlayingFullscreen — _nextTrack cleared on renderer disconnect > _nextTrack cleared when renderer is bypassed
  - [+] AgNowPlayingFullscreen — _nextTrack cleared on renderer disconnect > _nextTrack not touched when renderer is connected but queue_total is null
  - [+] AgNowPlayingFullscreen — _coverErrorToken reset on track/source change > cover error token cleared when track title changes
  - [+] AgNowPlayingFullscreen — _coverErrorToken reset on track/source change > cover error token cleared when source changes
  - [+] AgNowPlayingFullscreen — _coverErrorToken reset on track/source change > cover error token preserved when same track and source
  - [+] AgNowPlayingFullscreen — _coverErrorToken reset on track/source change > cover error token null when no error was set
  - [+] AgNowPlayingFullscreen — _coverErrorToken reset on track/source change > cover error token cleared when title changes to null (track ends)
  - [+] AgNowPlayingFullscreen — track number badge (tnLabel) > formats track 5 as A1 · TRACK 05
  - [+] AgNowPlayingFullscreen — track number badge (tnLabel) > formats track 10 as A1 · TRACK 10 (ceiling boundary: last track of side A)
  - [+] AgNowPlayingFullscreen — track number badge (tnLabel) > formats track 11 as A2 · TRACK 11 (next vinyl side)
  - [+] AgNowPlayingFullscreen — track number badge (tnLabel) > returns null when track_number is null (backend did not populate it)
  - [+] AgNowPlayingFullscreen — track number badge (tnLabel) > returns null when track_number is absent from the state object
  - [+] AgNowPlayingFullscreen — track number badge (tnLabel) > returns null when state is null (nothing playing)

**js/components/organisms/ag-now-playing.test.js**

  - [+] AgNowPlaying — auto-follow (_onState) > follows the active source on first state
  - [+] AgNowPlaying — auto-follow (_onState) > auto-switches when the active source changes
  - [+] AgNowPlaying — auto-follow (_onState) > stays on active source when it remains active across ticks
  - [+] AgNowPlaying — auto-follow (_onState) > clamps index to 0 when item count shrinks (no override)
  - [+] AgNowPlaying — auto-follow (_onState) > shows first item when no source is flagged active
  - [+] AgNowPlaying — auto-follow (_onState) > respects override — does not auto-switch after manual navigation
  - [+] AgNowPlaying — auto-follow (_onState) > override is not lifted while user-chosen source is still playing
  - [+] AgNowPlaying — auto-follow (_onState) > lifts override and auto-follows when user-chosen source stops playing
  - [+] AgNowPlaying — auto-follow (_onState) > lifts override and follows new active source after chosen source stops
  - [+] AgNowPlaying — auto-follow (_onState) > clamping also lifts override when items shrink below user index
  - [+] AgNowPlaying — auto-follow (_onState) > prevShownId uses old items — override is lifted when chosen source disappears even after clamp
  - [+] AgNowPlaying — auto-follow (_onState) > dot-click sets userOverride — next auto-follow tick respects it
  - [+] AgNowPlaying — _rendererActive + connector badge > rendererActive: true when connected and not bypassed
  - [+] AgNowPlaying — _rendererActive + connector badge > rendererActive: false when bypassed
  - [+] AgNowPlaying — _rendererActive + connector badge > rendererActive: false when disconnected
  - [+] AgNowPlaying — _rendererActive + connector badge > rendererActive: false when no renderer status
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge hidden when native renderer active (uses_local_mpd=false)
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge VISIBLE when local-MPD renderer active (upmpdcli, uses_local_mpd=true)
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge visible when renderer bypassed
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge visible when no renderer
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge hidden when output_connector absent (no renderer)
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge hidden when output_connector absent (renderer active)
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge visible with TOSLINK when bypassed
  - [+] AgNowPlaying — _rendererActive + connector badge > connector badge visible with TOSLINK when renderer disconnected

**js/components/organisms/ag-pipeline-page.test.js**

  - [+] ag-pipeline-page topology save > persists directly when the topology is valid with no warnings
  - [+] ag-pipeline-page topology save > blocks the save and shows the modal on structural errors
  - [+] ag-pipeline-page topology save > asks for confirmation before persisting when there are warnings
  - [+] ag-pipeline-page topology save > persists once the warning confirmation callback runs
  - [+] ag-pipeline-page topology save > falls through to the save when validation is unreachable (0.01s)
  - [+] ag-pipeline-page topology save > reports a backend save failure without closing the modal

**js/components/organisms/ag-user-modal.test.js**

  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (6 spaces) is rejected (0.01s)
  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (tabs) is rejected
  - [+] AgUserModal._handleSave — password trim (Fix P3) > valid password passes validation
  - [+] AgUserModal._handleSave — password trim (Fix P3) > password with surrounding spaces is trimmed before sending
  - [+] AgUserModal._handleSave — password trim (Fix P3) > short username is rejected regardless of password
