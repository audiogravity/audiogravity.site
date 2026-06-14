# Audiogravity — Test Report

Generated: **2026-06-14 16:35 UTC**

## Summary

| | Tests | Passed | Failed | Skipped | Duration |
|---|---:|---:|---:|---:|---:|
| **backend** PASS | 200 | 200 | 0 | 0 | 14.9s |
| **frontend** PASS | 65 | 65 | 0 | 0 | 0.3s |
| **license-js** PASS | 9 | 9 | 0 | 0 | 0.1s |
| **license-py** PASS | 21 | 21 | 0 | 0 | 1.1s |
| **Total** PASS | **295** | **295** | **0** | **0** | **16.3s** |

## Detail

### backend

**tests.test_app**

  - [+] test_coreapp_uses_default_json_response_class (0.03s)
  - [+] test_responses_serialize_to_json (0.01s)

**tests.test_audio_app_config.TestAudioAppConfig**

  - [+] test_services_route (0.06s)

**tests.test_audio_app_config.TestResolveConfigPath**

  - [+] test_declared_path_kept_when_it_exists
  - [+] test_falls_back_when_declared_missing
  - [+] test_unchanged_when_nothing_found
  - [+] test_empty_path_passthrough

**tests.test_audio_app_config.TestPackageEventReload**

  - [+] test_reload_on_package_events[package_state-True] (0.71s)
  - [+] test_reload_on_package_events[packages_updated-True] (0.71s)
  - [+] test_reload_on_package_events[some_other_event-False] (0.71s)

**tests.test_audio_hw.TestAudioHw**

  - [+] test_devices_route (0.03s)

**tests.test_audio_pipeline.TestAudioPipeline**

  - [+] test_now_playing (0.06s)
  - [+] test_control (0.04s)

**tests.test_audio_pipeline.TestCoverCache**

  - [+] test_cover_returns_24h_cache (0.04s)
  - [+] test_cover_404_no_store (0.03s)

**tests.test_audio_pipeline.TestAirplayNowPlaying**

  - [+] test_variant_values_unwrapped
  - [+] test_native_values_passthrough

**tests.test_auth.TestLogin**

  - [+] test_login_valid (0.66s)
  - [+] test_login_wrong_password (0.45s)
  - [+] test_login_unknown_user (0.44s)

**tests.test_auth.TestUsersCRUD**

  - [+] test_list_users (0.04s)
  - [+] test_create_and_delete_user (0.46s)
  - [+] test_update_user_role (0.45s)
  - [+] test_cannot_delete_self (0.05s)

**tests.test_config_validation.TestConfigValidation**

  - [+] test_post_validate (0.06s)

**tests.test_dbus_client.TestUnwrapVariant**

  - [+] test_native_values_passthrough
  - [+] test_single_wrap
  - [+] test_nested_wrap

**tests.test_dsd_volume.TestDsdDetection**

  - [+] test_dsd_format_activates_protection
  - [+] test_pcm_does_not_activate_protection
  - [+] test_hqplayer_item_excluded_from_dsd_detection

**tests.test_dsd_volume.TestDsdRestore**

  - [+] test_dsd_ended_restores_volume (0.03s)
  - [+] test_stopped_state_clears_dsd_active
  - [+] test_empty_items_clears_dsd_active

**tests.test_dsd_volume.TestPreDsdVolumeSave**

  - [+] test_volume_100_not_saved
  - [+] test_pre_dsd_volume_from_fast_lock

**tests.test_dsd_volume.TestHqplayerStaleTrack**

  - [+] test_current_track_cleared_after_30s_stopped

**tests.test_dsd_volume.TestExceptionHandler**

  - [+] test_hqplayer_guard_catches_any_exception

**tests.test_hqplayer.TestHQPlayer**

  - [+] test_status (0.07s)
  - [+] test_filters (0.22s)
  - [+] test_shapers (0.07s)
  - [+] test_modes (0.07s)
  - [+] test_discover (0.07s)

**tests.test_library.TestLibrary**

  - [+] test_upnp_known_servers_route_exists (0.18s)
  - [+] test_search_route_exists (0.18s)
  - [+] test_queue_route_exists (0.16s)

**tests.test_license.TestGetStatus**

  - [+] test_no_license (0.06s)
  - [+] test_valid_lifetime_license (0.06s)
  - [+] test_beta_version_accepts_v1_scope (0.06s)
  - [+] test_version_expired (0.06s)
  - [+] test_tampered_license (0.07s)

**tests.test_license.TestUploadLicense**

  - [+] test_upload_valid_lic (0.06s)
  - [+] test_upload_invalid_signature (0.04s)

**tests.test_license.TestDeleteLicense**

  - [+] test_delete_existing_license (0.07s)
  - [+] test_delete_wrong_password (0.04s)
  - [+] test_delete_no_license (0.03s)
  - [+] test_no_name_error (2.08s)

**tests.test_packages.TestPackages**

  - [+] test_route_exists (0.05s)

**tests.test_packages.TestRoonArchUrl**

  - [+] test_placeholder_resolves_per_arch[x86_64-linuxx64]
  - [+] test_placeholder_resolves_per_arch[aarch64-linuxarmv8]
  - [+] test_placeholder_resolves_per_arch[armv7l-linuxarmv7hf]
  - [+] test_unsupported_arch_raises
  - [+] test_url_without_placeholder_is_untouched
  - [+] test_current_roon_domain_is_allowed

**tests.test_packages.TestScriptSupportProbe**

  - [+] test_probe_resolves_placeholder_before_http

**tests.test_packages.TestScriptInstallerStdin**

  - [+] test_install_feeds_affirmative_stdin (0.04s)

**tests.test_packages.TestRoonRegistryUninstall**

  - [+] test_uninstall_is_complete[roon-roonbridge-/opt/RoonBridge]
  - [+] test_uninstall_is_complete[roonserver-roonserver-/opt/RoonServer]
  - [+] test_version_file_matches_install_dir_case[roon-/opt/RoonBridge]
  - [+] test_version_file_matches_install_dir_case[roonserver-/opt/RoonServer]

**tests.test_packages.TestOsResolverStandalone**

  - [+] test_runs_standalone_without_package_context (1.34s)

**tests.test_packages.TestArchFallback**

  - [+] test_fallback_used_when_arch_missing
  - [+] test_no_fallback_when_official_covers_arch
  - [+] test_no_fallback_for_arch_without_entry

**tests.test_packages.TestAptDebBundle**

  - [+] test_bundle_downloads_all_and_single_apt_install

**tests.test_packages.TestAptDebChecksum**

  - [+] test_parse_sha256sums
  - [+] test_sha256_file
  - [+] test_valid_checksum_installs
  - [+] test_mismatch_aborts
  - [+] test_missing_entry_aborts

**tests.test_packages.TestScriptInstallerUninstall**

  - [+] test_runs_all_commands_in_order_continue_on_failure (0.01s)
  - [+] test_does_not_double_prefix_sudo

**tests.test_packages.TestScriptInstallerDryRun**

  - [+] test_dry_run_supported_arch_no_download
  - [+] test_dry_run_unsupported_arch_fails

**tests.test_packages.TestAptDebSingle**

  - [+] test_single_deb_dpkg_install
  - [+] test_single_deb_fixes_deps_on_dpkg_failure (0.01s)

**tests.test_performance.TestPerformance**

  - [+] test_cpu_info_route (0.15s)
  - [+] test_rt_processes (0.09s)

**tests.test_performance.TestGovernorBootScript**

  - [+] test_boot_script_does_not_import_orjson
  - [+] test_boot_script_python_is_valid
  - [+] test_systemd_unit_is_oneshot

**tests.test_player.TestPlayer**

  - [+] test_snapshot (0.04s)
  - [+] test_control (0.06s)
  - [+] test_sleep_timer_get (0.03s)

**tests.test_profiles.TestActivateProfile**

  - [+] test_activate (0.17s)
  - [+] test_deactivate (0.06s)

**tests.test_push.TestVapidKey**

  - [+] test_get_key (0.02s)

**tests.test_push.TestSubscribe**

  - [+] test_subscribe (0.02s)

**tests.test_push.TestUnsubscribe**

  - [+] test_unsubscribe (0.02s)

**tests.test_push.TestGenerateVapidKeysScript**

  - [+] test_script_produces_valid_keys (0.21s)

**tests.test_push.TestRegisterLoadsVapidJson**

  - [+] test_register_initializes_service_from_json
  - [+] test_register_without_keys_does_not_initialize

**tests.test_qobuz.TestBundleExtractAppId**

  - [+] test_extracts_nine_digit_id
  - [+] test_raises_on_missing_app_id

**tests.test_qobuz.TestBundleExtractPrivateKey**

  - [+] test_extracts_key
  - [+] test_returns_none_when_missing

**tests.test_qobuz.TestBundleExtractSecrets**

  - [+] test_raises_on_single_seed
  - [+] test_raises_on_no_seeds
  - [+] test_extracts_two_seeds

**tests.test_qobuz.TestQobuzOAuthServicePersistence**

  - [+] test_loads_config_on_init
  - [+] test_not_connected_when_no_config
  - [+] test_disconnect_removes_file
  - [+] test_disconnect_noop_when_no_file
  - [+] test_save_config_roundtrip
  - [+] test_corrupt_config_is_handled

**tests.test_qobuz.TestQobuzOAuthFlow**

  - [+] test_start_oauth_builds_url

**tests.test_qobuz.TestQobuzModels**

  - [+] test_connection_defaults
  - [+] test_connection_connected
  - [+] test_oauth_start

**tests.test_qobuz.TestQobuzRouter**

  - [+] test_get_connection_connected (0.02s)
  - [+] test_delete_connection (0.02s)
  - [+] test_get_connection_after_disconnect (0.02s)
  - [+] test_oauth_callback_no_code (0.02s)
  - [+] test_oauth_callback_with_code (0.02s)
  - [+] test_oauth_callback_failure (0.02s)
  - [+] test_post_connection_starts_oauth (0.02s)

**tests.test_qobuz_library.TestQobuzCover**

  - [+] test_returns_url_token
  - [+] test_returns_none_when_no_image
  - [+] test_returns_none_when_no_size
  - [+] test_respects_size_param

**tests.test_qobuz_library.TestQobuzFeaturedAlbums**

  - [+] test_parses_albums
  - [+] test_skips_items_without_id
  - [+] test_handles_missing_release_date
  - [+] test_empty_response

**tests.test_qobuz_library.TestQobuzFeaturedPlaylists**

  - [+] test_parses_playlists_as_albums
  - [+] test_falls_back_to_image_large
  - [+] test_skips_playlists_without_id

**tests.test_qobuz_library.TestQobuzPlaylistTracks**

  - [+] test_parses_tracks
  - [+] test_performer_fallback_to_artist
  - [+] test_album_fallback_to_playlist_name
  - [+] test_skips_tracks_without_id

**tests.test_qobuz_library.TestQobuzSearch**

  - [+] test_parallel_search

**tests.test_qobuz_library.TestQobuzLibraryRouter**

  - [+] test_featured_albums (0.18s)
  - [+] test_featured_albums_default_type (0.17s)
  - [+] test_playlists (0.16s)
  - [+] test_playlist_tracks (0.16s)
  - [+] test_playlist_tracks_missing_id (0.18s)
  - [+] test_featured_service_error (0.16s)

**tests.test_radio.TestRadio**

  - [+] test_search_route (0.09s)
  - [+] test_library_route (0.07s)
  - [+] test_favorites_route (0.09s)

**tests.test_services.TestListServices**

  - [+] test_list_all (0.14s)

**tests.test_services.TestServiceInfo**

  - [+] test_get_service (0.08s)

**tests.test_services.TestServiceActions**

  - [+] test_restart_service (0.08s)
  - [+] test_stop_service (0.08s)
  - [+] test_start_service (0.08s)

**tests.test_steering.TestSteeringRoutes**

  - [+] test_outputs_route_exists (0.04s)
  - [+] test_status_route_exists (0.02s)

**tests.test_sysinfo.TestMetrics**

  - [+] test_metrics (0.10s)

**tests.test_sysinfo.TestDetectCpuModel**

  - [+] test_x86_uses_model_name (0.03s)
  - [+] test_arm_falls_back_to_lscpu
  - [+] test_unknown_when_nothing_found
  - [+] test_never_raises_on_error

**tests.test_tidal.TestTidalServicePersistence**

  - [+] test_loads_config_on_init
  - [+] test_not_connected_when_no_config
  - [+] test_disconnect_removes_file
  - [+] test_save_config_roundtrip
  - [+] test_corrupt_config_is_handled

**tests.test_tidal.TestTidalPKCE**

  - [+] test_start_pkce_builds_authorize_url
  - [+] test_extract_code_from_redirect_url
  - [+] test_extract_code_bare
  - [+] test_extract_code_rejects_login_url
  - [+] test_extract_code_empty
  - [+] test_apply_token_sets_state
  - [+] test_submit_without_pending_flow_fails

**tests.test_tidal.TestTidalModels**

  - [+] test_connection_defaults
  - [+] test_oauth_start

**tests.test_tidal.TestTidalRouter**

  - [+] test_get_connection_connected (0.02s)
  - [+] test_post_connection_starts_pkce (0.02s)
  - [+] test_submit_connection (0.02s)
  - [+] test_delete_connection (0.02s)

**tests.test_tidal_library.TestTidalMapping**

  - [+] test_cover_uuid_to_url
  - [+] test_map_track
  - [+] test_map_album
  - [+] test_search_maps_all_kinds

**tests.test_tidal_library.TestTidalQueue**

  - [+] test_single_track_builds_proxy_url_and_registers_meta

**tests.test_tidal_library.TestExtStreamKey**

  - [+] test_tidal_proxy_url_keys_on_track_id

**tests.test_tidal_library.TestTidalStreamProxy**

  - [+] test_fetch_manifest_none_when_not_connected
  - [+] test_stream_track_remuxes_to_seekable_file_and_caches
  - [+] test_stream_track_discards_incomplete_on_ffmpeg_failure
  - [+] test_cache_keeps_only_most_recent
  - [+] test_cache_rejects_bad_track_id
  - [+] test_stream_serves_cached_file_with_range (0.03s)

**tests.test_tidal_library.TestTidalDiscovery**

  - [+] test_featured_extracts_album_lists_deduped
  - [+] test_featured_no_pagination
  - [+] test_charts_keeps_only_chart_modules
  - [+] test_editorial_excludes_charts_and_albums
  - [+] test_editorial_no_pagination

**tests.test_tidal_library.TestTidalFavoritesPlaylists**

  - [+] test_favorites_albums_unwraps_item_wrapper
  - [+] test_playlists_maps_uuid_to_album

### frontend

**js/auth.test.js**

  - [+] Auth state checkers > isAuthenticated > returns false when not authenticated
  - [+] Auth state checkers > isAuthenticated > returns true when authenticated with valid token
  - [+] Auth state checkers > isAuthenticated > returns false when token is expired (0.06s)
  - [+] Auth state checkers > isAuthenticated > returns false when no token
  - [+] Auth state checkers > getCurrentUser > returns null when not authenticated (0.01s)
  - [+] Auth state checkers > getCurrentUser > returns user when authenticated
  - [+] Auth state checkers > isAdmin > returns false when not authenticated
  - [+] Auth state checkers > isAdmin > returns true for admin role
  - [+] Auth state checkers > isAdmin > returns false for user role
  - [+] Auth state checkers > isGuest > returns false when not authenticated
  - [+] Auth state checkers > isGuest > returns true for guest role
  - [+] Auth state checkers > isGuest > returns false for admin role
  - [+] Auth state checkers > getAuthToken > returns null when not authenticated
  - [+] Auth state checkers > getAuthToken > returns token when authenticated

**js/library-api.test.js**

  - [+] queueItem > routes to /library/queue by default (0.02s)
  - [+] queueItem > routes to /hqplayer/play-library when hqplayer_output is true
  - [+] upnpPlay > routes to /library/upnp-play by default
  - [+] upnpPlay > routes to /hqplayer/play when hqplayer_output is true
  - [+] upnpPlay > passes duration as null when not provided

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

**js/components/utils-lit.test.js**

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

### license-js

**js/ls-api.test.js**

  - [+] fmtDate > returns "—" for null (0.02s)
  - [+] fmtDate > returns "—" for empty string
  - [+] fmtDate > formats a valid ISO date (0.05s)
  - [+] shortId > returns "—" for null
  - [+] shortId > truncates a long ID
  - [+] shortId > handles short ID
  - [+] token management > getToken returns empty string when no token
  - [+] token management > setToken + getToken round-trips
  - [+] token management > clearToken removes the token

### license-py

**tests.test_admin.TestListOrders**

  - [+] test_list_orders (0.56s)
  - [+] test_list_orders_no_auth (0.01s)

**tests.test_admin.TestStats**

  - [+] test_stats (0.01s)

**tests.test_admin.TestCreateOrder**

  - [+] test_create (0.02s)

**tests.test_admin.TestDevicePings**

  - [+] test_list_pings (0.01s)

**tests.test_admin.TestAuditLog**

  - [+] test_list_audit (0.02s)

**tests.test_portal.TestPubConfig**

  - [+] test_returns_config (0.01s)

**tests.test_portal.TestCheck**

  - [+] test_check_invalid_key (0.02s)
  - [+] test_check_empty_key (0.01s)

**tests.test_portal.TestVerify**

  - [+] test_verify_invalid_lic (0.02s)
  - [+] test_verify_with_ag_version (0.01s)
  - [+] test_verify_without_verify_key (0.01s)

**tests.test_portal.TestActivate**

  - [+] test_activate_invalid_key (0.02s)

**tests.test_webhook.TestPayPalWebhookReceive**

  - [+] test_ipn_returns_200 (0.02s)
  - [+] test_ipn_empty_body (0.01s)

**tests.test_webhook.TestPayPalWebhookProcessing**

  - [+] test_verified_completed_creates_order (0.03s)
  - [+] test_invalid_pingback_creates_no_order (0.02s)
  - [+] test_non_completed_status_ignored (0.02s)
  - [+] test_receiver_email_mismatch_ignored (0.02s)
  - [+] test_idempotent_duplicate_txn (0.03s)
  - [+] test_upgrade_price_sets_v2_scope (0.03s)
