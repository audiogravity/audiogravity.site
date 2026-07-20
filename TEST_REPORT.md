# Audiogravi<sup>ty</sup> — Test Report

Generated: **2026-07-20 18:39 UTC**

## Summary

| | Tests | Passed | Failed | Skipped | Duration |
|---|---:|---:|---:|---:|---:|
| **core** PASS | 1387 | 1387 | 0 | 0 | 41.0s |
| **ui** PASS | 607 | 607 | 0 | 0 | 1.8s |
| **Total** PASS | **1994** | **1994** | **0** | **0** | **42.7s** |

## Detail

### core

**tests.test_album_tracks.TestParseMpdTracks**

  - [+] test_parses_multiple_tracks_sorted_by_track_number
  - [+] test_track_number_slash_form_and_missing
  - [+] test_entry_without_title_is_dropped
  - [+] test_album_filter_case_insensitive
  - [+] test_empty_input

**tests.test_album_tracks.TestGetAlbumTracks**

  - [+] test_non_mpd_source_returns_empty
  - [+] test_unknown_source_returns_empty
  - [+] test_no_album_metadata_returns_empty
  - [+] test_mpd_source_with_album_delegates_to_fetch

**tests.test_album_tracks.TestFetchMpdAlbumTracks**

  - [+] test_find_hit_returns_tracks_and_escapes_album
  - [+] test_falls_back_to_playlistinfo_filtered_by_album
  - [+] test_mpd_error_returns_empty

**tests.test_alsa_control.TestAmixerNoSudo**

  - [+] test_runs_amixer_directly_without_sudo

**tests.test_alsa_control.TestGetVolumeCaching**

  - [+] test_transient_failure_uses_short_miss_cache
  - [+] test_successful_read_uses_long_cache

**tests.test_alsa_control.TestControlChange**

  - [+] test_invalidates_cache_and_notifies
  - [+] test_register_on_change_dedups
  - [+] test_callback_exception_does_not_break_others

**tests.test_alsa_control.TestAlsactlPath**

  - [+] test_returns_first_existing
  - [+] test_none_when_missing

**tests.test_alsa_control.TestMonitorLoop**

  - [+] test_parses_value_events_and_invalidates
  - [+] test_returns_quietly_when_alsactl_missing
  - [+] test_start_monitor_is_idempotent

**tests.test_app**

  - [+] test_coreapp_uses_default_json_response_class
  - [+] test_responses_serialize_to_json

**tests.test_audio_app_config.TestAudioAppConfig**

  - [+] test_services_route (0.54s)

**tests.test_audio_app_config.TestResolveConfigPath**

  - [+] test_declared_path_kept_when_it_exists
  - [+] test_falls_back_when_declared_missing
  - [+] test_unchanged_when_nothing_found
  - [+] test_empty_path_passthrough

**tests.test_audio_app_config.TestPackageEventReload**

  - [+] test_reload_on_package_events[package_state-True] (0.70s)
  - [+] test_reload_on_package_events[packages_updated-True] (0.70s)
  - [+] test_reload_on_package_events[some_other_event-False] (0.70s)

**tests.test_audio_app_config.TestPathValidation**

  - [+] test_etc_path_accepted
  - [+] test_tmp_path_always_rejected
  - [+] test_var_path_always_rejected
  - [+] test_symlink_resolving_outside_whitelist_rejected

**tests.test_audio_app_config.TestRestartServiceDedup**

  - [+] test_restart_service_returns_success
  - [+] test_restart_service_returns_failed_on_error

**tests.test_audio_app_config.TestRunCommandTimeout**

  - [+] test_timeout_kills_hanging_process (1.00s)
  - [+] test_successful_command_returns_output

**tests.test_audio_app_config.TestListBackupsTotalCount**

  - [+] test_total_count_before_limit
  - [+] test_total_count_without_limit

**tests.test_audio_app_config.TestValidatePath**

  - [+] test_etc_direct_path
  - [+] test_var_path_rejected
  - [+] test_symlink_traversal_outside_whitelist_rejected

**tests.test_audio_app_config.TestDebounceTaskCleanup**

  - [+] test_cleanup_cancels_debounce_task

**tests.test_audio_app_config.TestMapDeviceToName**

  - [+] test_uses_get_card_by_id
  - [+] test_non_hw_device_passthrough

**tests.test_audio_app_config.TestShairportIndent**

  - [+] test_nested_block_indented
  - [+] test_double_nested_block_indented

**tests.test_audio_app_config.TestConfigUpdateModelValidator**

  - [+] test_neither_content_nor_data_raises
  - [+] test_content_only_accepted
  - [+] test_data_only_accepted

**tests.test_audio_app_config**

  - [+] test_extract_mpd_output_map_parses_all_blocks

**tests.test_audio_app_config.TestBackupPruneAndOwnership**

  - [+] test_prune_removes_oldest_beyond_cap
  - [+] test_prune_noop_under_cap
  - [+] test_write_file_sudo_forces_root_ownership

**tests.test_audio_hw.TestAudioDeviceListModel**

  - [+] test_total_cards_computed_from_cards
  - [+] test_total_cards_zero_when_empty
  - [+] test_total_cards_in_serialized_output

**tests.test_audio_hw.TestGetAudioDevicesScanning**

  - [+] test_no_cards_file_returns_empty
  - [+] test_no_cards_file_result_is_cached
  - [+] test_single_card_parsed
  - [+] test_two_cards_parsed
  - [+] test_capture_devices_are_excluded
  - [+] test_device_order_is_deterministic

**tests.test_audio_hw.TestSubdeviceParsing**

  - [+] test_subdevices_read_from_proc
  - [+] test_subdevices_default_to_1_when_no_sub0_info

**tests.test_audio_hw.TestCardParsing**

  - [+] test_long_name_equals_short_name_when_no_continuation
  - [+] test_card_dir_missing_yields_card_with_no_devices

**tests.test_audio_hw.TestCacheBehaviour**

  - [+] test_cache_hit_on_second_call
  - [+] test_force_refresh_bypasses_cache
  - [+] test_read_error_does_not_poison_cache

**tests.test_audio_hw.TestGetCardById**

  - [+] test_returns_correct_card
  - [+] test_returns_none_for_unknown_id
  - [+] test_returns_none_when_no_cards_present

**tests.test_audio_hw.TestAudioHwRoutes**

  - [+] test_devices_returns_200
  - [+] test_devices_response_shape (0.01s)
  - [+] test_devices_returns_empty_when_no_proc
  - [+] test_force_refresh_param_accepted
  - [+] test_mock_route_via_conftest_fixture

**tests.test_audio_hw.TestClassifyOutputType**

  - [+] test_usb_audio_driver_is_usb
  - [+] test_digital_device_name_is_spdif
  - [+] test_iec958_device_name_is_spdif
  - [+] test_analog_device_name_is_analog
  - [+] test_hdmi_device_name_is_hdmi
  - [+] test_generic_onboard_defaults_to_analog
  - [+] test_usb_driver_wins_over_digital_name
  - [+] test_spdif_marker_in_card_name_does_not_leak_to_analog_device

**tests.test_audio_hw.TestConnectorToOutputType**

  - [+] test_usb_variants
  - [+] test_digital_variants_map_to_spdif
  - [+] test_hdmi_and_displayport
  - [+] test_analog_connectors
  - [+] test_unknown_or_empty_is_none

**tests.test_audio_hw.TestCategorizeDerivation**

  - [+] test_usb_stays_usb
  - [+] test_hdmi_stays_hdmi
  - [+] test_spdif_collapses_to_onboard
  - [+] test_analog_collapses_to_onboard

**tests.test_audio_hw.TestListOutputCandidatesSemanticType**

  - [+] test_output_type_populated_for_usb_and_onboard

**tests.test_audio_hw_output**

  - [+] test_candidates_reference_box
  - [+] test_ambiguous_two_usb_dacs_no_recommendation
  - [+] test_no_usb_single_onboard_recommended
  - [+] test_no_usb_multiple_onboard_no_recommendation
  - [+] test_resolve_by_usb_id
  - [+] test_resolve_survives_reenumeration
  - [+] test_resolve_identical_dacs_picks_lowest_index
  - [+] test_resolve_fallback_to_card_name_when_no_usb_id
  - [+] test_resolve_unknown_returns_none
  - [+] test_resolve_absent_usb_dac_does_not_rebind_to_foreign_usb_dac_by_name
  - [+] test_resolve_absent_usbid_still_matches_same_card_by_name
  - [+] test_resolve_device_id_fallback

**tests.test_audio_library_sources**

  - [+] test_parse_usb_candidates_filters_supported_fs
  - [+] test_parse_usb_candidates_bad_json
  - [+] test_parse_existing_mounts_network_and_local
  - [+] test_build_mount_unit_ext4
  - [+] test_build_mount_unit_exfat_world_readable_no_uid_pinning
  - [+] test_build_automount_unit

**tests.test_audio_pipeline.TestAudioPipeline**

  - [+] test_now_playing (0.02s)
  - [+] test_control (0.02s)

**tests.test_audio_pipeline.TestCoverCache**

  - [+] test_cover_returns_24h_cache (0.02s)
  - [+] test_cover_404_no_store (0.01s)

**tests.test_audio_pipeline.TestAirplayNowPlaying**

  - [+] test_variant_values_unwrapped
  - [+] test_native_values_passthrough

**tests.test_audio_pipeline.TestDsdParsing**

  - [+] test_dsd64_sample_rate
  - [+] test_dsd128_sample_rate
  - [+] test_pcm_passthrough
  - [+] test_malformed_returns_none

**tests.test_audio_pipeline.TestCgroupParsing**

  - [+] test_cgroup_v2_format
  - [+] test_cgroup_v1_format
  - [+] test_cgroup_v1_multi_line
  - [+] test_cgroup_non_system_slice_returns_none

**tests.test_audio_pipeline.TestTopologySaveValidation**

  - [+] test_non_dict_topology_returns_400 (0.02s)
  - [+] test_valid_dict_topology_is_accepted (0.02s)

**tests.test_audio_pipeline.TestTopologyCycleDetection**

  - [+] test_cycle_stops_traversal
  - [+] test_linear_chain_no_false_positive

**tests.test_audio_pipeline.TestDetectMpdFormat**

  - [+] test_canonical_import_equals_alias_import
  - [+] test_m4a_returns_alac
  - [+] test_flac
  - [+] test_dsf_returns_dsd
  - [+] test_dff_returns_dsd
  - [+] test_tidal_url_returns_flac
  - [+] test_empty_returns_none
  - [+] test_unknown_extension_returns_none

**tests.test_audio_pipeline.TestAlsaPcmState**

  - [+] test_latency_computed_correctly
  - [+] test_wraparound_uses_2_64
  - [+] test_closed_device_returns_none

**tests.test_audio_pipeline.TestHqplayerVolume**

  - [+] test_nominal_volume
  - [+] test_zero_db_is_100
  - [+] test_minus_60_db_is_0
  - [+] test_below_minus_60_clamped_to_0
  - [+] test_muted_minus_144_clamped_to_0
  - [+] test_none_volume_db_returns_none

**tests.test_audio_pipeline.TestPidIdentifyCacheType**

  - [+] test_cache_is_ttl_dict_cache

**tests.test_audio_pipeline.TestHqpCacheInvalidation**

  - [+] test_truly_stopped_invalidates_cache
  - [+] test_unreachable_preserves_stale_cache
  - [+] test_network_error_preserves_stale_cache
  - [+] test_playing_item_updates_cache

**tests.test_audio_stack_router**

  - [+] test_status_returns_200 (0.02s)
  - [+] test_provision_200_maps_request_to_provisioner (0.02s)
  - [+] test_provision_initial_requires_valid_password (0.03s)
  - [+] test_provision_wrong_password_returns_401 (0.02s)
  - [+] test_provision_missing_password_returns_401 (0.02s)
  - [+] test_provision_regenerate_missing_password_returns_401 (0.02s)
  - [+] test_provision_passes_library_usb_fields (0.02s)
  - [+] test_provision_value_error_returns_400 (0.02s)
  - [+] test_provision_missing_card_name_returns_422 (0.02s)
  - [+] test_patch_output_200_no_password_required (0.02s)
  - [+] test_patch_output_missing_card_name_returns_422 (0.02s)
  - [+] test_patch_output_value_error_returns_400 (0.03s)
  - [+] test_patch_library_200_no_password_required (0.02s)

**tests.test_auth.TestGetApiKeyNotifyExemption**

  - [+] test_notify_callback_with_udn_is_public[/upnp-renderer/uuid:30fd2f17-453c/notify]
  - [+] test_notify_callback_with_udn_is_public[/api/upnp-renderer/uuid:30fd2f17-453c/notify]
  - [+] test_other_renderer_routes_still_require_key[/upnp-renderer/known]
  - [+] test_other_renderer_routes_still_require_key[/upnp-renderer/uuid:abc/connection]

**tests.test_auth.TestLogin**

  - [+] test_login_valid (0.38s)
  - [+] test_login_wrong_password (0.39s)
  - [+] test_login_unknown_user (0.38s)

**tests.test_auth.TestUsersCRUD**

  - [+] test_list_users (0.02s)
  - [+] test_create_and_delete_user (0.39s)
  - [+] test_update_user_role (0.39s)
  - [+] test_cannot_delete_self (0.02s)

**tests.test_auth.TestProtectedFlag**

  - [+] test_user_model_has_protected_field
  - [+] test_create_user_accepts_protected_flag (0.37s)
  - [+] test_unprotected_user_has_protected_false_by_default (0.36s)
  - [+] test_delete_guard_rejects_protected (0.37s)
  - [+] test_update_disable_guard_rejects_protected (0.45s)
  - [+] test_cannot_delete_self (0.02s)
  - [+] test_unprotected_account_can_be_deleted (0.41s)
  - [+] test_unprotected_account_can_be_disabled (0.40s)

**tests.test_auth.TestCreateUserReturns201**

  - [+] test_create_user_returns_201 (0.41s)

**tests.test_auth.TestUpdateUserEmptyPassword**

  - [+] test_short_password_rejected_by_pydantic (0.40s)
  - [+] test_whitespace_only_password_rejected (0.39s)

**tests.test_auth.TestDisabledUserLogin**

  - [+] test_disabled_user_cannot_login (0.75s)

**tests.test_auth.TestJwtContainsJti**

  - [+] test_jwt_has_jti_claim (0.01s)

**tests.test_auth.TestCreateUserWhitespacePassword**

  - [+] test_whitespace_only_password_rejected_on_create (0.02s)
  - [+] test_normal_password_accepted_on_create (0.38s)

**tests.test_auth.TestDisabledUserTimingOracle**

  - [+] test_disabled_user_returns_401 (0.77s)

**tests.test_auth.TestWebAuthnChallengeIsolation**

  - [+] test_registration_and_auth_challenges_are_independent
  - [+] test_double_begin_registration_does_not_clobber

**tests.test_auth.TestUpdateUserReturnsUpdatedState**

  - [+] test_update_returns_new_role (0.38s)

**tests.test_auth.TestVerifyAdminPassword**

  - [+] test_skips_when_jwt_disabled
  - [+] test_valid_password_when_jwt_enabled
  - [+] test_wrong_password_when_jwt_enabled
  - [+] test_unknown_user_when_jwt_enabled

**tests.test_auth.TestWebauthnLoginBeginNoEnumeration**

  - [+] test_uniform_response_for_known_and_unknown_user (0.02s)

**tests.test_auth.TestUsersFilePermissions**

  - [+] test_users_json_is_0600 (0.36s)

**tests.test_auth.TestApiKeyNonAscii**

  - [+] test_non_ascii_api_key_returns_403_not_500

**tests.test_auth.TestStdlibLogRedaction**

  - [+] test_filter_redacts_token_in_message
  - [+] test_filter_redacts_jwt

**tests.test_config_validation.TestConfigValidation**

  - [+] test_post_validate (0.01s)

**tests.test_config_validation.TestConfigValidationAppconfigWhitelist**

  - [+] test_tmp_path_rejected
  - [+] test_var_path_rejected
  - [+] test_empty_appconfigfile_accepted

**tests.test_config_validation.TestSystemdUnitMaxLength**

  - [+] test_long_name_rejected
  - [+] test_normal_name_accepted

**tests.test_config_validation.TestDependsOnDuplicates**

  - [+] test_duplicate_depends_on_rejected
  - [+] test_unique_depends_on_accepted

**tests.test_config_validation.TestCircularDependencies**

  - [+] test_direct_cycle_detected
  - [+] test_no_cycle_accepted
  - [+] test_unknown_dependency_rejected

**tests.test_config_validation.TestCriticalConsistencyWarnings**

  - [+] test_critical_profile_with_non_critical_service_warns
  - [+] test_empty_profile_warns

**tests.test_config_validation.TestAsyncSystemStateChecks**

  - [+] test_missing_systemd_unit_returns_invalid
  - [+] test_missing_config_file_returns_invalid

**tests.test_config_validation.TestConfigValidationRouterErrorCodes**

  - [+] test_validation_error_returns_400 (0.01s)

**tests.test_config_validation.TestTopologyValidation**

  - [+] test_shipped_example_validates_clean
  - [+] test_minimal_topology_valid_no_warnings
  - [+] test_streamer_and_controller_types_accepted
  - [+] test_unknown_device_type_is_error
  - [+] test_broken_target_device_is_warning
  - [+] test_broken_target_input_is_warning
  - [+] test_streamer_unknown_connector_is_warning
  - [+] test_validate_topology_file_missing_is_valid_with_warning
  - [+] test_validate_topology_file_reads_and_validates
  - [+] test_validate_topology_file_unreadable_is_error

**tests.test_config_validation.TestTopologyValidationRoute**

  - [+] test_route_reachable_and_returns_result (0.01s)

**tests.test_core.TestEventBus**

  - [+] test_publish_reaches_subscriber
  - [+] test_history_returned_on_subscribe
  - [+] test_queue_full_drops_subscriber_not_event
  - [+] test_different_channels_isolated (0.01s)

**tests.test_core.TestJwtHandler**

  - [+] test_create_access_token_has_jti
  - [+] test_token_contains_correct_role
  - [+] test_invalid_token_returns_none
  - [+] test_invalid_token_does_not_log_payload
  - [+] test_expired_token_returns_none

**tests.test_core.TestTTLCache**

  - [+] test_valid_within_ttl
  - [+] test_expired_after_ttl (0.05s)
  - [+] test_get_stale_returns_after_expiry (0.05s)
  - [+] test_invalidate_clears_value

**tests.test_core.TestRoonDisconnectTimeout**

  - [+] test_disconnect_timeout_does_not_raise
  - [+] test_disconnect_clears_state_on_exception

**tests.test_core.TestRoonServiceGating**

  - [+] test_connect_skips_when_roonbridge_inactive
  - [+] test_connect_proceeds_when_roonbridge_active
  - [+] test_connect_proceeds_when_dbus_unavailable
  - [+] test_sync_connect_creates_roon_api_when_reachable
  - [+] test_sync_connect_skips_roon_api_when_core_unreachable
  - [+] test_sync_connect_skips_discovery_when_core_unreachable
  - [+] test_is_roon_reachable_returns_false_when_refused
  - [+] test_is_roon_reachable_returns_true_when_connected

**tests.test_cover_art.TestCleanSearchTerm**

  - [+] test_strips_parenthetical_and_feat
  - [+] test_leaves_plain_title_untouched
  - [+] test_collapses_whitespace

**tests.test_cover_art.TestBuildCoverToken**

  - [+] test_roon_token_carries_fallback_suffix
  - [+] test_mpd_local_file_token
  - [+] test_mpd_http_stream_uses_registered_art
  - [+] test_mb_fallback_when_only_artist_album
  - [+] test_mbs_fallback_when_only_artist_title
  - [+] test_returns_none_when_insufficient_metadata

**tests.test_cover_art.TestMpdFileUriControlChars**

  - [+] test_newline_rejected
  - [+] test_tab_rejected
  - [+] test_null_byte_rejected
  - [+] test_clean_uri_not_rejected

**tests.test_dbus_client.TestUnwrapVariant**

  - [+] test_native_values_passthrough
  - [+] test_single_wrap
  - [+] test_nested_wrap

**tests.test_dbus_client.TestProxyCacheEviction**

  - [+] test_stale_proxy_evicted_on_call_get_all_failure
  - [+] test_working_proxy_stays_in_cache

**tests.test_deploy_layout**

  - [+] test_audiogravity_home_default_points_to_core_layout
  - [+] test_core_service_unit_name (0.03s)

**tests.test_dsd_volume.TestDsdDetection**

  - [+] test_dsd_format_activates_protection
  - [+] test_pcm_does_not_activate_protection
  - [+] test_hqplayer_item_excluded_from_dsd_detection

**tests.test_dsd_volume.TestDsdRestore**

  - [+] test_dsd_ended_restores_volume
  - [+] test_stopped_state_clears_dsd_active
  - [+] test_empty_items_clears_dsd_active

**tests.test_dsd_volume.TestPreDsdVolumeSave**

  - [+] test_volume_100_not_saved
  - [+] test_pre_dsd_volume_from_fast_lock

**tests.test_dsd_volume.TestHqplayerStaleTrack**

  - [+] test_current_track_cleared_after_30s_stopped

**tests.test_dsd_volume.TestExceptionHandler**

  - [+] test_hqplayer_guard_catches_any_exception

**tests.test_highresaudio.TestSecretStore**

  - [+] test_roundtrip
  - [+] test_key_file_created_0600
  - [+] test_decrypt_invalid_returns_none
  - [+] test_distinct_homes_use_distinct_keys

**tests.test_highresaudio.TestHighresaudioLogin**

  - [+] test_login_success_persists
  - [+] test_login_bad_credentials_raises
  - [+] test_login_no_subscription_raises

**tests.test_highresaudio.TestSessionDeadDetection**

  - [+] test_vault_album_dead_form
  - [+] test_vault_track_dead_form
  - [+] test_keepalive_invalid_token_form
  - [+] test_valid_session_not_dead

**tests.test_highresaudio.TestHighresaudioSession**

  - [+] test_api_get_relogins_on_not_logged_in
  - [+] test_api_get_raises_when_relogin_fails
  - [+] test_api_get_raises_when_still_dead_after_relogin
  - [+] test_valid_session_does_not_relogin
  - [+] test_api_get_not_connected_raises
  - [+] test_relogin_double_checked_under_concurrency
  - [+] test_stream_redirect_mode_returns_302_to_cdn
  - [+] test_relogin_skips_when_session_already_refreshed

**tests.test_highresaudio.TestHighresaudioStream**

  - [+] test_resolve_stream_returns_url_and_meta_in_one_call
  - [+] test_resolve_stream_url
  - [+] test_resolve_stream_dead_session_raises

**tests.test_highresaudio.TestHighresaudioPersistence**

  - [+] test_not_connected_when_no_config
  - [+] test_disconnect_removes_file
  - [+] test_disconnect_no_running_loop_does_not_raise
  - [+] test_disconnect_schedules_released_logout

**tests.test_highresaudio.TestHighresaudioModels**

  - [+] test_connection_defaults
  - [+] test_login_model

**tests.test_highresaudio_library.TestHraHelpers**

  - [+] test_cover_from_dict_master
  - [+] test_cover_from_full_url_string
  - [+] test_cover_none_when_absent
  - [+] test_cover_from_str_handles_dict_form
  - [+] test_year_production_preferred
  - [+] test_year_from_release_date
  - [+] test_year_none

**tests.test_highresaudio_library.TestHraFavorites**

  - [+] test_parses_and_skips_invalid

**tests.test_highresaudio_library.TestHraDiscover**

  - [+] test_resolves_category_then_lists
  - [+] test_prefix_is_memoised

**tests.test_highresaudio_library.TestHraCategory**

  - [+] test_known_category_lists_albums
  - [+] test_unknown_category_returns_empty

**tests.test_highresaudio_library.TestHraAlbumTracks**

  - [+] test_uses_playlistadd_as_id

**tests.test_highresaudio_library.TestHraSearch**

  - [+] test_parses_albums_and_artists
  - [+] test_short_query_returns_empty_without_api_call
  - [+] test_caps_both_albums_and_artists_at_limit

**tests.test_highresaudio_library.TestHraQueueMpd**

  - [+] test_album_enqueues_stable_redirect_proxy_urls
  - [+] test_single_track_resolves_metadata_once_and_enqueues_proxy
  - [+] test_rejects_unsupported_item_type

**tests.test_highresaudio_library.TestHraArtistAlbums**

  - [+] test_quicksearch_by_name_keeps_only_exact_artist_albums
  - [+] test_searches_leading_token_but_filters_full_name
  - [+] test_short_name_returns_empty_without_calling_api
  - [+] test_nonzero_offset_returns_empty

**tests.test_highresaudio_library.TestHraSearchArtistId**

  - [+] test_artist_result_id_is_name

**tests.test_hqplayer.TestHQPlayer**

  - [+] test_status (0.04s)
  - [+] test_filters (0.03s)
  - [+] test_shapers (0.03s)
  - [+] test_modes (0.03s)
  - [+] test_discover (0.03s)

**tests.test_hqplayer.TestHQPlayerStop**

  - [+] test_stop_returns_success (0.03s)
  - [+] test_stop_503_on_hqplayer_error (0.04s)

**tests.test_hqplayer.TestHQPlayerLiteralValidation**

  - [+] test_invalid_item_type_returns_422 (0.03s)
  - [+] test_invalid_action_returns_422 (0.03s)
  - [+] test_valid_item_type_accepted (0.04s)

**tests.test_hqplayer.TestHQPlayerHasDspConfig**

  - [+] test_false_when_no_dsp
  - [+] test_false_when_empty_dict
  - [+] test_true_when_dsp_set

**tests.test_hqplayer.TestReadXmlResponse**

  - [+] test_parses_valid_xml
  - [+] test_returns_ok_element_on_empty_with_allow_empty
  - [+] test_raises_on_empty_without_allow_empty

**tests.test_hqplayer.TestResolveFilePath**

  - [+] test_valid_path_returns_absolute
  - [+] test_path_traversal_rejected
  - [+] test_leading_slash_stripped
  - [+] test_symlink_outside_root_rejected

**tests.test_hqplayer.TestSendBatchAllowEmpty**

  - [+] test_allow_empty_true_accepts_empty_response

**tests.test_hqplayer.TestHQPlayerRateZero**

  - [+] test_rate_zero_preserved

**tests.test_hqplayer.TestGetStatusNoHost**

  - [+] test_returns_unavailable_without_warning
  - [+] test_does_not_call_fetch_status

**tests.test_hqplayer.TestFetchStatusCachesFailure**

  - [+] test_failure_sets_cache
  - [+] test_failure_prevents_immediate_retry

**tests.test_hqplayer.TestNaaAvailableInConnection**

  - [+] test_naa_available_true_when_service_active (0.04s)
  - [+] test_naa_available_false_when_service_inactive (0.04s)

**tests.test_hqplayer.TestHQPlayerPlayValidation**

  - [+] test_play_without_path_or_uri_returns_400 (0.03s)
  - [+] test_play_with_uri_accepted (0.03s)

**tests.test_hqplayer.TestNaaLiveness**

  - [+] test_job_removed_ignores_other_units
  - [+] test_job_removed_schedules_refresh_for_naa
  - [+] test_read_naa_active_uses_services_manager
  - [+] test_naa_active_fast_path_does_not_reseed
  - [+] test_naa_active_seeds_and_subscribes_once
  - [+] test_refresh_naa_coalesces_second_event

**tests.test_hqplayer.TestFetchStatusLogging**

  - [+] test_warns_once_across_repeated_failures

**tests.test_hqplayer.TestFetchStatusMalformedNumbers**

  - [+] test_bad_position_does_not_raise

**tests.test_hqplayer.TestPlayLibraryItemAlbumMetadata**

  - [+] test_track_play_keeps_album
  - [+] test_add_does_not_touch_the_playing_track

**tests.test_hqplayer.TestConfirmPlaybackStarted**

  - [+] test_playing_confirms_silently
  - [+] test_stopped_raises_with_an_actionable_reason (0.31s)
  - [+] test_a_slow_start_is_still_confirmed (0.02s)
  - [+] test_spurious_exchange_error_is_ignored_when_playing
  - [+] test_exchange_error_surfaces_when_playback_never_starts (0.31s)
  - [+] test_ambiguous_state_keeps_the_exchange_error (0.31s)
  - [+] test_ambiguous_state_without_exchange_error_does_not_raise (0.30s)

**tests.test_hqplayer.TestUseAsOutputFlag**

  - [+] test_enabling_persists_the_flag
  - [+] test_disabling_releases_the_sound_card
  - [+] test_toggling_to_the_same_value_is_a_no_op
  - [+] test_a_failing_stop_does_not_break_the_toggle
  - [+] test_flag_survives_a_restart
  - [+] test_absent_flag_defaults_to_false
  - [+] test_disconnect_clears_the_flag
  - [+] test_disconnect_releases_the_sound_card_first
  - [+] test_disconnect_completes_even_if_the_stop_fails
  - [+] test_disconnect_without_a_host_sends_nothing
  - [+] test_connection_exposes_the_flag_even_when_unreachable

**tests.test_hqplayer.TestUseAsOutputGuards**

  - [+] test_enabling_without_a_configured_hqplayer_is_refused
  - [+] test_enabling_with_the_naa_down_is_refused
  - [+] test_disabling_is_always_allowed
  - [+] test_host_accessor_reflects_configuration (0.12s)

**tests.test_hqplayer.TestPlayUriHonoursAction**

  - [+] test_add_never_clears_the_queue
  - [+] test_add_leaves_the_now_playing_metadata_alone
  - [+] test_add_does_not_wait_for_a_playback_confirmation
  - [+] test_add_propagates_an_exchange_failure
  - [+] test_play_still_clears_adds_and_plays
  - [+] test_play_defaults_when_no_action_is_given
  - [+] test_play_records_the_content_origin

**tests.test_hqplayer.TestConfirmPlaybackTiming**

  - [+] test_a_slow_start_is_not_reported_as_a_failure (0.03s)
  - [+] test_a_play_that_never_starts_still_fails (0.41s)
  - [+] test_an_immediate_start_checks_without_waiting_first
  - [+] test_the_shared_status_cache_is_never_evicted
  - [+] test_the_default_window_covers_a_heavy_dsp_warm_up

**tests.test_hqplayer.TestCanDecode**

  - [+] test_supported_codecs_pass[MP3]
  - [+] test_supported_codecs_pass[FLAC]
  - [+] test_supported_codecs_pass[WAV]
  - [+] test_supported_codecs_pass[AIFF]
  - [+] test_supported_codecs_pass[WV]
  - [+] test_supported_codecs_pass[DSF]
  - [+] test_supported_codecs_pass[DFF]
  - [+] test_undecodable_codecs_are_refused[AAC]
  - [+] test_undecodable_codecs_are_refused[AAC+]
  - [+] test_undecodable_codecs_are_refused[AACP]
  - [+] test_undecodable_codecs_are_refused[OGG]
  - [+] test_undecodable_codecs_are_refused[OPUS]
  - [+] test_undecodable_codecs_are_refused[WMA]
  - [+] test_undecodable_codecs_are_refused[ALAC]
  - [+] test_undecodable_codecs_are_refused[APE]
  - [+] test_matching_ignores_case_and_padding[aac]
  - [+] test_matching_ignores_case_and_padding[ AAC ]
  - [+] test_matching_ignores_case_and_padding[Aac]
  - [+] test_an_unclassifiable_codec_is_attempted_not_blocked[None]
  - [+] test_an_unclassifiable_codec_is_attempted_not_blocked[]
  - [+] test_an_unclassifiable_codec_is_attempted_not_blocked[   ]
  - [+] test_an_unclassifiable_codec_is_attempted_not_blocked[UNKNOWN]

**tests.test_http_ssrf.TestAssertFetchable**

  - [+] test_rejects_non_http_scheme
  - [+] test_rejects_loopback_and_link_local
  - [+] test_allows_public_and_private_lan

**tests.test_library.TestLibrary**

  - [+] test_upnp_known_servers_route_exists (0.08s)
  - [+] test_search_route_exists (0.08s)
  - [+] test_queue_route_exists (0.08s)

**tests.test_library.TestUpnpSearchTrackId**

  - [+] test_track_id_is_res_url
  - [+] test_search_pre_registers_title_and_art
  - [+] test_search_skips_art_registration_when_absent
  - [+] test_track_without_res_falls_back_to_object_id

**tests.test_library.TestUpnpSearchQueue**

  - [+] test_track_add_calls_mpd_add
  - [+] test_track_play_uses_mpd_batch_with_clear
  - [+] test_no_mpd_port_raises
  - [+] test_album_no_known_server_raises
  - [+] test_album_browses_children_and_adds_all
  - [+] test_album_play_clears_queue
  - [+] test_album_no_tracks_raises
  - [+] test_unsupported_item_type_raises
  - [+] test_queue_tags_radio_origin_and_station_logo
  - [+] test_queue_local_track_origin_library

**tests.test_library.TestUpnpQueueRouting**

  - [+] test_upnp_source_routes_to_upnp_queue (0.08s)
  - [+] test_mpd_source_still_routes_to_mpd_queue (0.07s)

**tests.test_library.TestQueueRequestValidation**

  - [+] test_valid_request_accepted
  - [+] test_invalid_item_type_rejected
  - [+] test_invalid_action_rejected
  - [+] test_invalid_hierarchy_rejected
  - [+] test_item_id_too_long_rejected
  - [+] test_source_id_too_long_rejected
  - [+] test_all_valid_item_types_accepted
  - [+] test_all_valid_actions_accepted

**tests.test_library.TestUpnpQueueOutputId**

  - [+] test_uses_output_id_port_when_specified
  - [+] test_falls_back_to_first_port_when_output_id_absent

**tests.test_library.TestUpnpContentDirectoryClient**

  - [+] test_browse_delegates_to_dms (0.01s)
  - [+] test_browse_uses_location_not_control_url
  - [+] test_parse_duration_valid
  - [+] test_parse_duration_invalid

**tests.test_library.TestMapResultTrackNumber**

  - [+] test_valid_track_number_extracted
  - [+] test_empty_string_track_number_returns_none
  - [+] test_absent_track_number_returns_none

**tests.test_library.TestProbePortSingleFetch**

  - [+] test_non_xml_body_yields_one_get_not_two
  - [+] test_xml_body_with_content_directory_calls_fetch_server

**tests.test_library.TestKnownUpnpServerMigration**

  - [+] test_loads_without_last_location
  - [+] test_loads_with_last_location

**tests.test_library.TestMpdAlbumBatchChunking**

  - [+] test_large_album_list_is_chunked

**tests.test_library.TestStreamTagCommands**

  - [+] test_builds_addtagid_for_each_present_tag
  - [+] test_skips_empty_and_missing_tags
  - [+] test_no_metadata_yields_no_commands
  - [+] test_escapes_quotes_in_values
  - [+] test_collapses_newlines_in_tag_values

**tests.test_library.TestParseAddedIds**

  - [+] test_parses_ids_in_order
  - [+] test_empty_when_no_ids

**tests.test_library.TestMpdQueueListReadPath**

  - [+] test_streaming_source_falls_back_to_engine_port
  - [+] test_no_engine_returns_empty_not_error
  - [+] test_limit_windows_playlistinfo_with_absolute_positions

**tests.test_library.TestMpdQueueRemoveFallback**

  - [+] test_streaming_source_removes_by_id_via_engine_port

**tests.test_library.TestParseCurrentPos**

  - [+] test_reads_song_line
  - [+] test_none_when_absent

**tests.test_library.TestQobuzQueueRenderer**

  - [+] test_track_play_routes_to_renderer (0.02s)
  - [+] test_add_bypasses_renderer_goes_to_mpd
  - [+] test_no_renderer_uses_mpd
  - [+] test_album_queues_all_tracks_via_play_queue
  - [+] test_album_proxy_url_is_lan_reachable

**tests.test_library.TestTidalQueueRenderer**

  - [+] test_track_play_routes_to_renderer_with_external_url
  - [+] test_add_bypasses_renderer_goes_to_mpd
  - [+] test_no_renderer_uses_mpd
  - [+] test_tidal_proxy_url_local_only_false_uses_lan_ip

**tests.test_library.TestGetRendererServiceBypass**

  - [+] test_active_renderer_is_returned
  - [+] test_no_active_service_returns_none
  - [+] test_no_dmr_returns_none

**tests.test_library.TestFavorites**

  - [+] test_qobuz_add_uses_favorite_create_with_album_ids
  - [+] test_qobuz_remove_uses_favorite_delete
  - [+] test_qobuz_ids_parses_getuserfavorites
  - [+] test_tidal_add_posts_album_ids
  - [+] test_tidal_remove_deletes_by_id
  - [+] test_tidal_ids_unwraps_item
  - [+] test_hra_add_hits_myalbum_add
  - [+] test_hra_remove_hits_myalbum_delete
  - [+] test_hra_ids_parses_myalbum
  - [+] test_dispatch_routes_add_to_the_right_service
  - [+] test_dispatch_rejects_non_streaming_source
  - [+] test_unsupported_type_rejected

**tests.test_library.TestContentKindClassification**

  - [+] test_local_mpd_source_is_local_library
  - [+] test_streaming_services_are_classified_as_such[src_qobuz]
  - [+] test_streaming_services_are_classified_as_such[src_tidal]
  - [+] test_streaming_services_are_classified_as_such[src_highresaudio]
  - [+] test_roon_gets_its_own_kind

**tests.test_library.TestResolveOutput**

  - [+] test_local_when_hqplayer_is_not_the_output
  - [+] test_hqplayer_takes_the_local_library
  - [+] test_hqplayer_takes_a_stream_url
  - [+] test_streaming_services_are_refused_with_501
  - [+] test_roon_is_never_diverted_to_hqplayer
  - [+] test_roon_is_local_even_without_hqplayer
  - [+] test_two_selected_outputs_raise_a_conflict
  - [+] test_renderer_alone_is_not_a_conflict
  - [+] test_refuses_when_the_naa_is_not_running
  - [+] test_a_dead_naa_does_not_break_local_playback
  - [+] test_roon_is_unaffected_by_a_dead_naa
  - [+] test_unknown_content_kind_fails_closed

**tests.test_library.TestHqplayerServiceLookup**

  - [+] test_selects_hqplayer_when_it_is_the_output
  - [+] test_ignores_hqplayer_when_it_is_not_the_output
  - [+] test_refuses_to_route_without_a_configured_host
  - [+] test_is_none_when_the_module_is_absent

**tests.test_library_files.TestLocalLibraryRoots**

  - [+] test_parses_music_directory_from_mpd_conf
  - [+] test_commented_music_directory_is_skipped
  - [+] test_fallback_when_conf_missing
  - [+] test_fallback_when_no_music_directory_key
  - [+] test_returns_list_never_empty
  - [+] test_result_is_cached_by_mtime

**tests.test_library_files.TestResolveWithinRoots**

  - [+] test_valid_path
  - [+] test_leading_slash_tolerated
  - [+] test_traversal_rejected
  - [+] test_empty_roots_rejected
  - [+] test_multi_root_prefers_existing_file
  - [+] test_missing_file_resolves_for_clean_404

**tests.test_library_files.TestUrlSigning**

  - [+] test_roundtrip
  - [+] test_wrong_message_rejected
  - [+] test_empty_sig_rejected
  - [+] test_non_ascii_sig_rejected_without_crashing
  - [+] test_signature_is_sha256_hex

**tests.test_library_files.TestStreamEndpoint**

  - [+] test_full_get_returns_all_bytes (0.07s)
  - [+] test_range_returns_206_partial (0.08s)
  - [+] test_head_returns_headers_no_body (0.07s)
  - [+] test_bad_signature_rejected (0.07s)
  - [+] test_missing_signature_rejected (0.07s)
  - [+] test_missing_file_returns_404 (0.08s)

**tests.test_library_files.TestLibraryCoverEndpoint**

  - [+] test_valid_sig_returns_cover (0.01s)
  - [+] test_bad_sig_rejected_without_resolving (0.01s)
  - [+] test_missing_sig_rejected (0.01s)
  - [+] test_cover_not_found_returns_404 (0.01s)

**tests.test_license.TestGetStatus**

  - [+] test_no_license (0.01s)
  - [+] test_valid_lifetime_license (0.02s)
  - [+] test_beta_version_accepts_v1_scope (0.01s)
  - [+] test_version_expired (0.01s)
  - [+] test_tampered_license (0.01s)

**tests.test_license.TestUploadLicense**

  - [+] test_upload_valid_lic (0.02s)
  - [+] test_upload_invalid_signature (0.01s)

**tests.test_license.TestDeleteLicense**

  - [+] test_delete_existing_license (0.02s)
  - [+] test_delete_wrong_password (0.01s)
  - [+] test_delete_no_license (0.01s)
  - [+] test_no_name_error (0.01s)

**tests.test_license.TestVerifyHeaders**

  - [+] test_returns_key_when_configured
  - [+] test_returns_empty_when_not_configured

**tests.test_license.TestPortalBase**

  - [+] test_strips_verify_suffix
  - [+] test_invalid_url_returns_empty

**tests.test_license.TestCheckEndpointStatusHandling**

  - [+] test_server_5xx_returns_502 (0.01s)
  - [+] test_unexpected_response_shape_returns_502 (0.01s)

**tests.test_license.TestRequireFullLicenseServiceNone**

  - [+] test_returns_503_when_service_not_initialised

**tests.test_license.TestTrialTamperDetection**

  - [+] test_inconsistent_started_returns_none
  - [+] test_consistent_started_returns_trial
  - [+] test_create_writes_all_locations

**tests.test_license.TestDaysRemaining**

  - [+] test_expired_trial_returns_zero
  - [+] test_fresh_trial_returns_full_days

**tests.test_license.TestOnlineFetchStatusCodes**

  - [+] test_403_returns_structured_status
  - [+] test_503_returns_unreachable

**tests.test_license.TestActivateEndpointLicContentValidation**

  - [+] test_non_json_lic_content_returns_502 (0.02s)

**tests.test_license.TestAnnouncementModel**

  - [+] test_announcement_model_valid
  - [+] test_online_license_status_defaults_empty_announcements
  - [+] test_online_license_status_coerces_announcement_dicts
  - [+] test_online_result_includes_announcements_key
  - [+] test_get_cached_spreads_announcements

**tests.test_license.TestUpdateInfoPropagation**

  - [+] test_update_info_defaults
  - [+] test_online_status_defaults_update_unavailable
  - [+] test_online_status_coerces_update_dict
  - [+] test_result_always_includes_update_key
  - [+] test_fetch_captures_update_field

**tests.test_license.TestTrialDaysRemainingClamp**

  - [+] test_future_started_does_not_exceed_full_duration
  - [+] test_normal_elapsed
  - [+] test_expired_returns_zero

**tests.test_minimal_configs**

  - [+] test_supported_services
  - [+] test_mpd_minimal_content_and_roundtrip
  - [+] test_mpd_multi_output_blocks_one_enabled
  - [+] test_mpd_multi_output_defaults_enabled_to_first
  - [+] test_upmpdcli_minimal_content_and_roundtrip
  - [+] test_shairport_minimal_content_and_roundtrip
  - [+] test_device_is_not_hardcoded
  - [+] test_unknown_service_raises
  - [+] test_generated_config_carries_ag_marker_and_still_parses[mpd]
  - [+] test_generated_config_carries_ag_marker_and_still_parses[upmpdcli]
  - [+] test_generated_config_carries_ag_marker_and_still_parses[airplay]
  - [+] test_has_ag_marker_false_for_distro_default

**tests.test_mpd_client.TestClearErrorInjectionSingleCommand**

  - [+] test_playback_starters_are_prefixed_with_clearerror[play]
  - [+] test_playback_starters_are_prefixed_with_clearerror[playid 12]
  - [+] test_playback_starters_are_prefixed_with_clearerror[next]
  - [+] test_playback_starters_are_prefixed_with_clearerror[previous]
  - [+] test_other_commands_are_sent_untouched[status]
  - [+] test_other_commands_are_sent_untouched[playlistinfo]
  - [+] test_other_commands_are_sent_untouched[outputs]
  - [+] test_other_commands_are_sent_untouched[stop] (0.01s)
  - [+] test_prefix_matches_on_the_verb_not_a_substring
  - [+] test_response_is_still_returned_verbatim

**tests.test_mpd_client.TestClearErrorInjectionCommandList**

  - [+] test_clear_add_play_gets_a_leading_clearerror
  - [+] test_read_only_list_is_not_prefixed
  - [+] test_fault_tolerant_lists_are_never_prefixed
  - [+] test_only_one_clearerror_for_several_playback_starters

**tests.test_net**

  - [+] test_is_local_url_matches_loopback_and_localhost
  - [+] test_is_local_url_matches_primary_ip
  - [+] test_is_local_url_rejects_remote_host
  - [+] test_is_local_url_empty_or_unparseable_is_remote
  - [+] test_is_local_url_handles_detection_failure

**tests.test_network_mounts**

  - [+] test_slugify_collapses_and_lowercases
  - [+] test_unique_slug_appends_counter_on_collision
  - [+] test_mount_options_guest_vs_credentials
  - [+] test_cred_file_text
  - [+] test_unit_roundtrip_through_parser
  - [+] test_parse_rejects_foreign_units
  - [+] test_proc_mount_types_parses_and_decodes
  - [+] test_request_rejects_control_chars_in_password
  - [+] test_request_rejects_bad_host
  - [+] test_request_normalises_share_and_rejects_spaces
  - [+] test_create_installs_units_and_mounts_without_blocking_start
  - [+] test_create_guest_share_needs_no_credentials
  - [+] test_create_rejects_partial_credentials
  - [+] test_create_rolls_back_when_mount_fails
  - [+] test_create_times_out_within_budget_and_rolls_back
  - [+] test_create_leaves_no_credentials_when_unit_naming_fails
  - [+] test_create_avoids_existing_mnt_directories
  - [+] test_create_installs_cifs_utils_when_missing
  - [+] test_cifs_utils_probe_is_cached
  - [+] test_list_distinguishes_cifs_from_armed_autofs
  - [+] test_list_flags_the_share_the_library_lives_on
  - [+] test_delete_refuses_active_library_without_force
  - [+] test_delete_refuses_busy_unmount_and_rearms_automount
  - [+] test_delete_force_removes_all_artifacts
  - [+] test_delete_unknown_slug_raises
  - [+] test_wake_touches_only_idle_autofs_mounts_and_runs_once
  - [+] test_wake_survives_unreachable_share

**tests.test_now_playing.TestResolveOrigin**

  - [+] test_tidal_proxy_url
  - [+] test_qobuz_eid_url
  - [+] test_local_file
  - [+] test_local_stream_proxy_is_library
  - [+] test_empty_file_is_library
  - [+] test_http_stream_is_upnp_by_default
  - [+] test_http_stream_flagged_radio
  - [+] test_radio_wins_over_url_markers
  - [+] test_upnp_resolves_registered_server_name
  - [+] test_roon_protocol
  - [+] test_mpris_airplay
  - [+] test_mpris_unknown_player_is_generic
  - [+] test_mpris_generic
  - [+] test_unknown_protocol

**tests.test_now_playing.TestExtStreamKey**

  - [+] test_tidal_proxy_url_returns_tidal_key
  - [+] test_qobuz_eid_url_returns_qobuz_key
  - [+] test_library_stream_url_returns_local_key
  - [+] test_local_key_stable_across_hosts_and_sig
  - [+] test_tidal_key_stable_across_hosts_and_api_keys
  - [+] test_upnp_url_with_tidal_stream_in_path_is_tidal
  - [+] test_tidal_stream_in_query_not_matched
  - [+] test_eid_in_url_path_not_matched_as_qobuz
  - [+] test_qobuz_proxy_url_returns_qobuz_key
  - [+] test_qobuz_proxy_key_stable_across_hosts_and_api_keys
  - [+] test_highresaudio_proxy_url_returns_hra_key
  - [+] test_highresaudio_cdn_key_is_path_based_and_token_stable
  - [+] test_highresaudio_cdn_distinct_tracks_distinct_keys
  - [+] test_highresaudio_real_cdn_hosts_matched
  - [+] test_highres_substring_host_not_misclassified
  - [+] test_qobuz_proxy_url_not_confused_with_eid
  - [+] test_plain_upnp_url_returns_url_as_key
  - [+] test_local_file_returns_path_as_key

**tests.test_now_playing.TestUpnpServerRegistry**

  - [+] test_register_and_get
  - [+] test_missing_returns_none
  - [+] test_empty_inputs_ignored

**tests.test_now_playing.TestExtStreamMetaMerge**

  - [+] test_register_creates_new_entry
  - [+] test_register_without_merge_overwrites
  - [+] test_register_merge_preserves_existing_keys
  - [+] test_register_merge_updates_existing_key
  - [+] test_register_merge_on_absent_key_creates_entry
  - [+] test_empty_url_is_ignored
  - [+] test_merge_repositions_entry_to_end_of_lru
  - [+] test_merge_with_empty_dict_is_noop_on_content

**tests.test_now_playing.TestTrackNumberFromExtMeta**

  - [+] test_track_number_populated_when_mpd_has_title

**tests.test_now_playing.TestHqplayerNaaGate**

  - [+] test_skips_poll_and_clears_cache_when_naa_inactive
  - [+] test_polls_when_naa_active

**tests.test_now_playing.TestRendererAsSource**

  - [+] test_item_for_native_playing_renderer
  - [+] test_no_item_when_stopped_or_unreachable
  - [+] test_no_item_when_no_active_renderer
  - [+] test_paused_maps_to_paused
  - [+] test_stopped_returns_none_by_default
  - [+] test_cast_item_is_rebadged_with_content_identity
  - [+] test_origin_derived_from_uri (0.02s)
  - [+] test_control_toggle_pauses_when_playing
  - [+] test_control_toggle_resumes_when_stopped
  - [+] test_control_next_seek_volume
  - [+] test_control_no_renderer_false
  - [+] test_mpd_control_goes_straight_to_mpd

**tests.test_now_playing.TestHqplayerAsProcessor**

  - [+] test_pushed_track_badged_with_content_origin
  - [+] test_pushed_track_without_origin_defaults_to_library
  - [+] test_external_playback_falls_back_to_processor_active_format

**tests.test_now_playing.TestRendererContentIdentity**

  - [+] test_queue_origin_wins_for_an_ag_radio_cast
  - [+] test_queue_origin_wins_for_a_media_server_cast
  - [+] test_non_http_uri_is_external_not_library
  - [+] test_unknown_http_uri_stays_external
  - [+] test_no_uri_is_external
  - [+] test_ag_proxy_url_is_still_classified_from_the_url

**tests.test_packages.TestPackages**

  - [+] test_route_exists (0.02s)

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

  - [+] test_install_feeds_affirmative_stdin

**tests.test_packages.TestRoonRegistryUninstall**

  - [+] test_uninstall_is_complete[roon-roonbridge-/opt/RoonBridge]
  - [+] test_uninstall_is_complete[roonserver-roonserver-/opt/RoonServer]
  - [+] test_version_file_matches_install_dir_case[roon-/opt/RoonBridge]
  - [+] test_version_file_matches_install_dir_case[roonserver-/opt/RoonServer]

**tests.test_packages.TestOsResolverStandalone**

  - [+] test_runs_standalone_without_package_context (7.90s)

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

  - [+] test_runs_all_commands_in_order_continue_on_failure
  - [+] test_does_not_double_prefix_sudo

**tests.test_packages.TestScriptInstallerDryRun**

  - [+] test_dry_run_supported_arch_no_download
  - [+] test_dry_run_unsupported_arch_fails
  - [+] test_dry_run_unreachable_url_returns_false

**tests.test_packages.TestAptDebSingle**

  - [+] test_single_deb_dpkg_install
  - [+] test_single_deb_fixes_deps_on_dpkg_failure

**tests.test_packages.TestScriptInstallerNoShellInjection**

  - [+] test_install_script_args_passed_as_exec_tokens
  - [+] test_version_check_url_validated_against_whitelist
  - [+] test_version_check_url_allowed_domain_accepted

**tests.test_packages.TestAptRepoPathValidation**

  - [+] test_path_traversal_gpg_key_rejected
  - [+] test_path_traversal_sources_list_rejected
  - [+] test_invalid_package_name_rejected

**tests.test_packages.TestValidateDestinationPath**

  - [+] test_allowed_path_accepted
  - [+] test_prefix_sibling_rejected
  - [+] test_exact_allowed_root_accepted
  - [+] test_outside_whitelist_rejected

**tests.test_packages.TestPackagesManagerLogBuffer**

  - [+] test_log_buffer_caps_at_500

**tests.test_packages.TestPackagesManagerCleanup**

  - [+] test_cleanup_cancels_bg_task

**tests.test_packages.TestPlayerPollLoop**

  - [+] test_poll_loop_continues_after_get_now_playing_exception (10.01s)

**tests.test_packages.TestPlayerDsdGatherFailure**

  - [+] test_dsd_active_reset_on_gather_failure

**tests.test_packages.TestDownloadUrlValidation**

  - [+] test_https_allowed_domain_accepted
  - [+] test_http_rejected
  - [+] test_disallowed_domain_rejected

**tests.test_packages.TestDebDownloadSizeCap**

  - [+] test_rejects_oversized_content_length
  - [+] test_aborts_when_stream_exceeds_limit

**tests.test_performance.TestPerformance**

  - [+] test_cpu_info_route (0.06s)
  - [+] test_rt_processes (0.03s)

**tests.test_performance.TestGovernorBootScript**

  - [+] test_boot_script_does_not_import_orjson
  - [+] test_boot_script_python_is_valid
  - [+] test_systemd_unit_is_oneshot

**tests.test_performance.TestCyclictestParsing**

  - [+] test_trailing_t_does_not_raise
  - [+] test_normal_line_parsed
  - [+] test_empty_line_no_crash

**tests.test_performance.TestBootScriptConfigFile**

  - [+] test_config_file_passed_as_argv
  - [+] test_config_file_quoted_in_shell

**tests.test_performance.TestSetCpuGovernorReview**

  - [+] test_unknown_cpu_id_returns_error_not_raise
  - [+] test_write_cpu_file_uses_async_sudo_tee

**tests.test_player.TestParseFormat**

  - [+] test_alac_with_mpd_bitrate_is_shown
  - [+] test_flac_with_mpd_bitrate_is_shown
  - [+] test_wav_with_mpd_bitrate_is_shown
  - [+] test_lossy_aac_bitrate_shown
  - [+] test_lossy_mp3_bitrate_shown
  - [+] test_mpd_zero_bitrate_triggers_pcm_fallback
  - [+] test_roon_32bit_96khz_pcm_computed
  - [+] test_roon_24bit_48khz_pcm_computed
  - [+] test_airplay_16bit_441khz_pcm_computed
  - [+] test_mpd_bitrate_takes_precedence_over_pcm
  - [+] test_dsd64_bitrate_from_table
  - [+] test_dsd128_bitrate_from_table
  - [+] test_none_source_format_and_codec_returns_null_format
  - [+] test_codec_only_no_source_format_no_crash

**tests.test_player.TestBuildStateSignalPathEnrichment**

  - [+] test_connector_inserted_before_dac
  - [+] test_no_renderer_step_when_no_active_service
  - [+] test_source_prepended_from_origin
  - [+] test_full_chain_no_renderer
  - [+] test_radio_shows_canonical_label_not_station_name
  - [+] test_upnp_uses_server_name_from_origin_name
  - [+] test_renderer_active_output_label_is_renderer_not_local_dac
  - [+] test_upnp_falls_back_to_upnp_label_when_no_server_name
  - [+] test_native_renderer_signal_path_ends_at_renderer
  - [+] test_native_renderer_with_source_prepended
  - [+] test_renderer_unreachable_does_not_appear_in_signal_path

**tests.test_player.TestBuildSourcesVirtual**

  - [+] test_stopped_virtual_source_not_playing
  - [+] test_playing_virtual_source_is_playing
  - [+] test_paused_virtual_source_is_playing

**tests.test_player.TestControlRouting**

  - [+] test_explicit_renderer_source_routed_to_now_playing (0.15s)
  - [+] test_stopped_renderer_still_controllable (0.15s)
  - [+] test_unknown_source_returns_false
  - [+] test_no_source_resolves_active (0.15s)

**tests.test_player.TestPlayer**

  - [+] test_snapshot (0.02s)
  - [+] test_control (0.14s)
  - [+] test_origins_returns_all_known_keys (0.02s)
  - [+] test_sleep_timer_get (0.02s)

**tests.test_player.TestGetOutputs**

  - [+] test_returns_mpd_and_renderer_outputs (0.02s)
  - [+] test_local_active_true_when_no_renderer (0.02s)
  - [+] test_local_active_false_when_renderer_reachable (0.02s)
  - [+] test_local_active_true_when_renderer_not_reachable (0.02s)

**tests.test_player.TestSelectMpdOutput**

  - [+] test_switch_succeeds (0.02s)
  - [+] test_unknown_output_id_returns_404 (0.02s)
  - [+] test_stale_active_udn_cleared_not_raised (0.03s)
  - [+] test_stale_active_udn_calls_save_config (0.02s)

**tests.test_player.TestDsdRendererExcluded**

  - [+] test_renderer_active_dsd_not_volume_forced
  - [+] test_collect_other_sources_excludes_renderer

**tests.test_player.TestDsdStartPartialFailure**

  - [+] test_partial_failure_keeps_state_and_original_volume

**tests.test_player.TestControlIdRouting**

  - [+] test_control_id_wins_over_source_id
  - [+] test_rebadged_item_found_by_control_id
  - [+] test_source_id_fallback_dispatches_driver_handle
  - [+] test_stopped_renderer_still_controllable_by_handle

**tests.test_player.TestBuildOutputs**

  - [+] test_local_only_when_no_renderer_selected
  - [+] test_selected_renderer_carries_state_and_wins_active
  - [+] test_stopped_selected_renderer_visible_in_outputs
  - [+] test_unreachable_renderer_kept_with_unknown_state_local_active
  - [+] test_playing_local_wins_over_an_idle_renderer
  - [+] test_a_local_error_stays_visible_when_the_renderer_is_idle
  - [+] test_a_playing_renderer_still_wins_over_local
  - [+] test_idle_everywhere_keeps_the_selected_renderer_visible
  - [+] test_a_paused_local_source_also_holds_the_active_spot
  - [+] test_queue_next_populated_from_renderer_queue

**tests.test_player.TestDsdRekeyOnDriver**

  - [+] test_rebadged_cast_item_never_volume_forced
  - [+] test_dsd_start_on_cast_skips_software_forcing

**tests.test_player.TestOutputErrorSurfacing**

  - [+] test_busy_dac_error_lands_on_the_local_output
  - [+] test_no_error_in_the_normal_case
  - [+] test_error_from_a_non_local_item_is_ignored
  - [+] test_state_changed_detects_an_appearing_output_error

**tests.test_player.TestIdleStateKeepsTheRendererControllable**

  - [+] test_handle_is_derived_from_outputs_after_a_core_restart
  - [+] test_handle_is_derived_after_another_source_played
  - [+] test_no_handle_when_the_local_output_is_the_active_one
  - [+] test_the_selected_output_still_shows_its_name_while_idle

**tests.test_profiles.TestActivateProfile**

  - [+] test_activate (0.05s)
  - [+] test_deactivate (0.02s)

**tests.test_profiles.TestProfilesGatherTimeout**

  - [+] test_stop_timeout_does_not_raise

**tests.test_profiles.TestStoppedCountFailedLogic**

  - [+] test_failed_state_is_not_stopped

**tests.test_profiles.TestProfileExportPath**

  - [+] test_export_not_in_tmp

**tests.test_provisioning**

  - [+] test_generates_when_absent
  - [+] test_mpd_multi_output_config_from_detected_hardware
  - [+] test_provision_writes_alsa_index_pin_for_usb_dac
  - [+] test_provision_no_pin_for_non_usb_output
  - [+] test_provision_respects_existing_user_pin
  - [+] test_user_pins_usb_device_matches_hex_forms
  - [+] test_overwrites_when_exists
  - [+] test_regenerate_backups_then_overwrites
  - [+] test_provision_mpd_without_library_raises
  - [+] test_regenerate_mpd_reuses_existing_library
  - [+] test_regenerate_mpd_without_existing_config_raises
  - [+] test_provision_airplay_only_without_library_ok
  - [+] test_unresolved_device_raises
  - [+] test_persists_stable_id_not_hw
  - [+] test_persist_preserves_existing_topology
  - [+] test_ensure_usb_library_writes_units_and_enables
  - [+] test_ensure_usb_library_exfat_installs_exfatprogs
  - [+] test_provision_with_usb_library_uses_mountpoint
  - [+] test_per_service_outputs_are_independent
  - [+] test_read_outputs_migrates_legacy_single_pin
  - [+] test_persist_output_preserves_other_service_on_legacy_migration
  - [+] test_discover_library_sources_usb_and_network (0.18s)
  - [+] test_status_includes_library_sources
  - [+] test_status_reports_outputs_and_config_state
  - [+] test_patch_output_retargets_device_and_pins (0.01s)
  - [+] test_patch_output_rejects_service_without_output
  - [+] test_patch_output_raises_when_output_absent
  - [+] test_patch_library_changes_music_directory_only
  - [+] test_patch_library_with_usb_uuid_mounts
  - [+] test_patch_library_requires_a_library
  - [+] test_provision_rejects_music_dir_with_quote
  - [+] test_patch_library_rejects_music_dir_with_quote
  - [+] test_patch_output_mpd_uses_native_enable
  - [+] test_patch_output_mpd_falls_back_to_restart
  - [+] test_patch_library_triggers_mpd_rescan
  - [+] test_provision_triggers_mpd_rescan_when_mpd_generated
  - [+] test_provision_airplay_only_does_not_rescan
  - [+] test_mpd_port_from_config_parses_and_defaults
  - [+] test_patch_library_rescan_uses_configured_port
  - [+] test_trigger_mpd_rescan_is_best_effort
  - [+] test_library_scan_status_reports_scanning
  - [+] test_library_scan_status_reports_idle
  - [+] test_library_scan_status_tolerates_mpd_down
  - [+] test_library_scan_status_targets_the_configured_port
  - [+] test_rescan_detaches_retry_when_mpd_not_ready

**tests.test_push.TestVapidKey**

  - [+] test_get_key

**tests.test_push.TestSubscribe**

  - [+] test_subscribe

**tests.test_push.TestUnsubscribe**

  - [+] test_unsubscribe

**tests.test_push.TestGenerateVapidKeysScript**

  - [+] test_script_produces_valid_keys (0.08s)

**tests.test_push.TestRegisterLoadsVapidJson**

  - [+] test_register_initializes_service_from_json
  - [+] test_register_without_keys_does_not_initialize

**tests.test_push.TestPushEndpointValidation**

  - [+] test_http_endpoint_rejected
  - [+] test_empty_endpoint_rejected
  - [+] test_https_endpoint_accepted

**tests.test_push.TestPushWebpushTimeout**

  - [+] test_webpush_called_with_timeout

**tests.test_push.TestPushUnsubscribeQueryParam**

  - [+] test_endpoint_is_query_param

**tests.test_push.TestServiceDownPushHook**

  - [+] test_transition_active_to_failed_detected
  - [+] test_no_alert_on_first_appearance_as_failed
  - [+] test_no_alert_on_active_to_active
  - [+] test_stale_state_pruned_when_service_disappears
  - [+] test_no_false_positive_after_prune_and_reappearance
  - [+] test_label_uses_systemd_unit_name
  - [+] test_label_fallback_to_service_id

**tests.test_push.TestPush410Pruning**

  - [+] test_410_prunes_once
  - [+] test_non_410_error_with_410_in_text_is_kept
  - [+] test_save_writes_0600_file

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

  - [+] test_get_connection_connected (0.01s)
  - [+] test_delete_connection
  - [+] test_get_connection_after_disconnect (0.01s)
  - [+] test_stream_redirect_mode_returns_302_to_cdn
  - [+] test_oauth_callback_no_code
  - [+] test_oauth_callback_with_code
  - [+] test_oauth_callback_failure (0.01s)
  - [+] test_post_connection_starts_oauth

**tests.test_qobuz.TestQobuzStreamProxy**

  - [+] test_stream_full_returns_200 (0.01s)
  - [+] test_stream_range_request_relayed_to_cdn (0.01s)
  - [+] test_stream_cdn_error_raises_503 (0.01s)
  - [+] test_presigned_url_sent_byte_for_byte (0.01s)

**tests.test_qobuz.TestQobuzRotation**

  - [+] test_persistent_401_raises_rotated
  - [+] test_persistent_403_raises_rotated
  - [+] test_rotation_error_message_mentions_rotated
  - [+] test_rotation_logs_error
  - [+] test_first_401_triggers_retry_not_rotation

**tests.test_qobuz.TestQobuzOAuthEdgeCases**

  - [+] test_handle_callback_returns_false_when_no_secret
  - [+] test_user_id_is_none_when_json_id_is_null
  - [+] test_user_id_is_none_when_id_key_absent

**tests.test_qobuz.TestGetStreamUrl**

  - [+] test_raises_when_not_connected
  - [+] test_happy_path_returns_cdn_url
  - [+] test_non_200_raises_runtime_error
  - [+] test_missing_url_in_response_raises

**tests.test_qobuz.TestQobuzCallbackErrorHandling**

  - [+] test_callback_exception_returns_502_error_page (0.01s)
  - [+] test_start_connection_exception_returns_502 (0.01s)

**tests.test_qobuz.TestQobuzBundleSingleFlight**

  - [+] test_concurrent_callers_fetch_once

**tests.test_qobuz_library.TestQobuzCover**

  - [+] test_returns_url_token
  - [+] test_returns_none_when_no_image
  - [+] test_returns_none_when_image_is_null
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

  - [+] test_featured_albums (0.08s)
  - [+] test_featured_albums_default_type (0.07s)
  - [+] test_playlists (0.07s)
  - [+] test_playlist_tracks (0.09s)
  - [+] test_playlist_tracks_missing_id (0.07s)
  - [+] test_featured_service_error (0.07s)

**tests.test_qobuz_library.TestQobuzQueueHelper**

  - [+] test_adds_tracks_as_stable_redirect_proxy_urls
  - [+] test_play_action_triggers_playid
  - [+] test_persists_metadata_as_durable_mpd_tags

**tests.test_qobuz_library.TestQobuzQueueSingleTrack**

  - [+] test_single_track_persists_durable_tags

**tests.test_qobuz_library.TestQobuzGetRetry**

  - [+] test_success_no_relogin
  - [+] test_401_relogins_then_succeeds
  - [+] test_401_relogin_fails_raises_session_expired (0.01s)
  - [+] test_401_after_relogin_raises_rotated
  - [+] test_not_connected_raises

**tests.test_radio.TestRadio**

  - [+] test_search_route (0.04s)
  - [+] test_library_route (0.03s)
  - [+] test_favorites_route (0.03s)

**tests.test_radio.TestRadioEditStation**

  - [+] test_edit_station_returns_updated_station (0.03s)
  - [+] test_edit_station_404_when_not_saved (0.03s)

**tests.test_radio.TestRadioSavedStationDatetime**

  - [+] test_added_at_is_timezone_aware

**tests.test_radio.TestRadioResolveRobustness**

  - [+] test_resolve_falls_back_to_saved_on_rbi_failure
  - [+] test_resolve_returns_none_when_not_found_anywhere

**tests.test_radio.TestRadioApplyEntryUpdate**

  - [+] test_update_clears_flag
  - [+] test_update_pops_when_both_flags_cleared
  - [+] test_remove_from_library_uses_apply_entry_update
  - [+] test_remove_from_library_returns_false_when_not_in_library
  - [+] test_remove_favorite_keeps_entry_if_still_in_library

**tests.test_radio.TestRadioPlayRendererRouting**

  - [+] test_play_routes_to_renderer_when_active
  - [+] test_play_cover_token_none_when_no_favicon
  - [+] test_play_uses_mpd_when_no_renderer_active
  - [+] test_play_uses_mpd_when_no_manager_bound
  - [+] test_play_propagates_renderer_error_without_mpd_fallback

**tests.test_radio.TestMpdEscapeNewlineStripping**

  - [+] test_escape_strips_newlines_and_carriage_returns
  - [+] test_escape_still_escapes_quotes_and_backslashes
  - [+] test_play_command_carries_no_newline

**tests.test_radio.TestRadioSearchHiRes**

  - [+] test_hi_res_overfetches_and_truncates
  - [+] test_no_criteria_returns_empty_without_rbi_call

**tests.test_radio.TestRadioSetFlagResolve**

  - [+] test_add_favorite_resolves_unknown_and_adds
  - [+] test_add_favorite_unknown_unresolvable_raises

**tests.test_radio.TestRadioDiscoverCallback**

  - [+] test_callback_ignores_cancelled_task
  - [+] test_callback_logs_failure

**tests.test_radio.TestRadioHonoursOutputSelection**

  - [+] test_station_is_pushed_to_hqplayer_when_it_is_the_output (0.01s)
  - [+] test_hqplayer_push_carries_the_radio_identity
  - [+] test_hqplayer_push_never_touches_mpd
  - [+] test_local_output_still_goes_to_mpd
  - [+] test_routing_refusal_propagates

**tests.test_radio.TestRadioHqplayerFailureIsNotA500**

  - [+] test_a_busy_dac_surfaces_as_a_routing_refusal
  - [+] test_the_original_cause_is_kept_as_the_chained_error

**tests.test_radio.TestRadioConfirmWindow**

  - [+] test_a_station_gets_the_remote_confirmation_window
  - [+] test_the_remote_window_is_clear_of_the_measured_start_time

**tests.test_radio.TestRadioCodecGate**

  - [+] test_an_aac_station_is_refused_without_being_pushed
  - [+] test_an_mp3_station_goes_through
  - [+] test_an_unknown_codec_is_still_attempted

**tests.test_renderer_manager.TestLoadConfig**

  - [+] test_no_config_file_leaves_empty_state
  - [+] test_reads_known_renderers
  - [+] test_active_flag_sets_active_udn
  - [+] test_only_first_active_entry_wins
  - [+] test_migration_from_legacy_config
  - [+] test_migration_skipped_when_new_config_exists
  - [+] test_migrate_drops_local_renderer_and_clears_active
  - [+] test_migrate_keeps_remote_renderers

**tests.test_renderer_manager.TestGetKnown**

  - [+] test_no_service_reachable_false
  - [+] test_live_reachable_from_service

**tests.test_renderer_manager.TestGetService**

  - [+] test_get_service_raises_for_unknown_udn
  - [+] test_get_service_returns_registered_service
  - [+] test_get_active_service_none_when_no_active_udn
  - [+] test_get_active_service_none_when_service_not_instantiated
  - [+] test_get_active_service_returns_active

**tests.test_renderer_manager.TestNotifyUrl**

  - [+] test_notify_url_includes_udn
  - [+] test_trailing_slash_stripped_from_base

**tests.test_renderer_manager.TestConnect**

  - [+] test_connect_sets_active_udn
  - [+] test_connect_calls_svc_connect
  - [+] test_connect_stops_previous_active
  - [+] test_connect_upserts_known_list
  - [+] test_connect_rejects_local_renderer

**tests.test_renderer_manager.TestDisconnect**

  - [+] test_disconnect_raises_for_unknown_udn
  - [+] test_disconnect_clears_active_udn
  - [+] test_disconnect_keeps_renderer_in_known

**tests.test_self_update.TestState**

  - [+] test_read_state_idle_when_absent
  - [+] test_write_initial_and_read_roundtrip
  - [+] test_write_initial_none_version_is_latest
  - [+] test_is_in_progress
  - [+] test_read_state_tolerates_corrupt_file
  - [+] test_stale_in_progress_is_ignored
  - [+] test_fresh_in_progress_without_timestamp_is_conservative
  - [+] test_stale_in_progress_from_updated_at_is_ignored
  - [+] test_fresh_in_progress_from_updated_at_still_locks
  - [+] test_paths_derive_from_settings

**tests.test_self_update.TestBuildCommand**

  - [+] test_latest_when_no_version
  - [+] test_explicit_version
  - [+] test_token_passed_as_leading_wrapper_arg

**tests.test_self_update.TestLaunchTokenFallback**

  - [+] test_falls_back_to_configured_token
  - [+] test_explicit_token_wins_over_configured
  - [+] test_launcher_failure_marks_state_failed
  - [+] test_launcher_success_keeps_starting

**tests.test_self_update.TestUpdateEndpoints**

  - [+] test_update_rejects_bad_password (0.03s)
  - [+] test_update_conflict_when_in_progress (0.03s)
  - [+] test_update_happy_path_launches (0.03s)
  - [+] test_update_status_reflects_state (0.03s)

**tests.test_services.TestListServices**

  - [+] test_list_all (0.04s)

**tests.test_services.TestServiceInfo**

  - [+] test_get_service (0.03s)

**tests.test_services.TestServiceActions**

  - [+] test_restart_service (0.04s)
  - [+] test_stop_service (0.04s)
  - [+] test_start_service (0.04s)

**tests.test_services.TestServiceNameValidation**

  - [+] test_valid_name_accepted (0.04s)
  - [+] test_semicolon_rejected (0.03s)
  - [+] test_slash_rejected (0.03s)
  - [+] test_ampersand_rejected (0.04s)

**tests.test_services.TestEnumComparison**

  - [+] test_fifo_policy_triggers_warning
  - [+] test_realtime_io_triggers_warning

**tests.test_services.TestDbusTimeout**

  - [+] test_dbus_timeout_falls_back_gracefully

**tests.test_services.TestIsServiceActive**

  - [+] test_returns_true_when_active
  - [+] test_returns_false_when_inactive
  - [+] test_appends_service_suffix
  - [+] test_returns_false_on_dbus_error
  - [+] test_returns_false_when_dbus_unavailable

**tests.test_services.TestCgroupFdEviction**

  - [+] test_stale_fd_evicted_on_ioerror

**tests.test_services.TestPropertyInjectionValidation**

  - [+] test_cpu_affinity_rejects_directive_injection
  - [+] test_cpu_affinity_accepts_valid
  - [+] test_cpu_affinity_rejects_newline_between_indices
  - [+] test_count_fields_reject_injection
  - [+] test_count_fields_accept_int_and_infinity
  - [+] test_memory_rejects_multiline

**tests.test_services.TestManagedUnitGuard**

  - [+] test_managed_units_includes_core_not_ssh
  - [+] test_perform_action_rejects_unmanaged_unit
  - [+] test_update_properties_rejects_unmanaged_unit

**tests.test_steering.TestSteeringRoutes**

  - [+] test_outputs_route_exists (0.01s)
  - [+] test_status_route_exists (0.01s)

**tests.test_steering.TestAlsaDeviceValidation**

  - [+] test_shell_metachar_rejected
  - [+] test_newline_rejected
  - [+] test_valid_format_passes_regex

**tests.test_steering.TestGetSteerability**

  - [+] test_absent_services_excluded
  - [+] test_installed_services_included

**tests.test_steering.TestSwitchDispatch**

  - [+] test_mpd_uses_native_switch_no_restart
  - [+] test_mpd_native_error_reports_failure_no_fallback (0.01s)
  - [+] test_mpd_fallback_uses_restart
  - [+] test_airplay_uses_restart_path

**tests.test_steering.TestVerifyAlsaDevice**

  - [+] test_returns_false_when_pcm_missing
  - [+] test_returns_true_when_pcm_exists

**tests.test_steering.TestHardwareDrivenResolution**

  - [+] test_join_by_connector_uses_topology_port_id_and_live_hw
  - [+] test_hardware_without_topology_match_falls_back_to_type
  - [+] test_active_flag_reflects_running_pcm
  - [+] test_switch_resolves_live_hw_and_targets_output_by_name
  - [+] test_switch_not_applied_reports_failure

**tests.test_steering.TestMpdNativeSwitch**

  - [+] test_enables_target_and_disables_others_atomically
  - [+] test_unknown_output_name_falls_back
  - [+] test_mpd_ack_is_a_real_error
  - [+] test_no_outputs_falls_back

**tests.test_steering.TestConfirmAudioFlow**

  - [+] test_returns_true_as_soon_as_running
  - [+] test_returns_false_after_window_when_idle

**tests.test_steering.TestReplaceMpdDeviceScoped**

  - [+] test_replaces_only_the_alsa_block
  - [+] test_refuses_multiple_alsa_blocks
  - [+] test_none_when_no_alsa_device

**tests.test_steering.TestSteeringBackgroundTasks**

  - [+] test_spawn_bg_keeps_and_releases_reference

**tests.test_stream_renderer.TestStreamQueueRendererBase**

  - [+] test_pushes_entries_and_returns_count
  - [+] test_empty_entries_raises_and_does_not_play

**tests.test_stream_renderer.TestStreamTrackEntry**

  - [+] test_maps_object_track_with_on_play

**tests.test_stream_renderer.TestHraRendererPort**

  - [+] test_album_builds_entries_registers_meta_and_plays
  - [+] test_album_empty_raises_specific_message

**tests.test_stream_renderer.TestLocalLibraryRendererCast**

  - [+] test_local_library_tracks_album_uses_find_album
  - [+] test_local_library_tracks_rejects_bad_item_type
  - [+] test_local_signed_url_keeps_slashes_signs_path
  - [+] test_build_renderer_entries_signs_and_registers
  - [+] test_mpd_queue_routes_to_remote_renderer
  - [+] test_mpd_queue_no_renderer_stays_direct
  - [+] test_mpd_queue_add_action_never_routes_to_renderer

**tests.test_sysinfo.TestMetrics**

  - [+] test_metrics (0.02s)

**tests.test_sysinfo.TestDetectCpuModel**

  - [+] test_x86_uses_model_name
  - [+] test_arm_falls_back_to_lscpu
  - [+] test_unknown_when_nothing_found
  - [+] test_never_raises_on_error

**tests.test_sysinfo.TestSysinfoSmartctlSafe**

  - [+] test_smartctl_not_found_returns_none (0.04s)

**tests.test_sysinfo.TestSysinfoGrepPatternValidation**

  - [+] test_invalid_regex_returns_400 (0.02s)
  - [+] test_valid_regex_accepted (0.04s)

**tests.test_sysinfo.TestSysinfoSyslogIdentifierFormat**

  - [+] test_shared_builder_uses_match_syntax

**tests.test_sysinfo.TestTemperaturePushAlert**

  - [+] test_cooldown_not_updated_when_push_raises
  - [+] test_cooldown_below_threshold_no_alert
  - [+] test_cooldown_prevents_second_alert_within_15min
  - [+] test_alert_allowed_after_cooldown_elapsed

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

  - [+] test_get_connection_connected (0.01s)
  - [+] test_post_connection_starts_pkce (0.02s)
  - [+] test_submit_connection (0.01s)
  - [+] test_delete_connection (0.13s)

**tests.test_tidal.TestTidalRotation**

  - [+] test_fetch_manifest_401_raises_rotated
  - [+] test_fetch_manifest_403_raises_rotated
  - [+] test_fetch_manifest_404_returns_none
  - [+] test_refresh_401_logs_rotation_hint
  - [+] test_stream_endpoint_returns_503_on_rotation (0.01s)

**tests.test_tidal.TestParseDashFormat**

  - [+] test_flac_hires_bandwidth_kbps
  - [+] test_flac_cd_bandwidth_kbps
  - [+] test_flac_sample_rate_extracted
  - [+] test_flac_codec_identified
  - [+] test_aac_codec_identified
  - [+] test_aac_bandwidth_kbps
  - [+] test_manifest_without_namespace
  - [+] test_bandwidth_is_integer_kbps
  - [+] test_empty_string_returns_empty_dict
  - [+] test_malformed_xml_returns_empty_dict
  - [+] test_missing_representation_returns_empty_dict
  - [+] test_non_integer_sample_rate_does_not_drop_bitrate_kbps
  - [+] test_non_integer_bandwidth_does_not_drop_sample_rate

**tests.test_tidal.TestTidalRefreshTokenClearing**

  - [+] test_expired_token_cleared_on_refresh_failure
  - [+] test_valid_token_kept_on_refresh_failure

**tests.test_tidal.TestTidalRefreshClearsOnAllFailures**

  - [+] test_expired_token_cleared_on_401
  - [+] test_expired_token_cleared_on_network_exception
  - [+] test_get_access_token_returns_none_after_failed_refresh

**tests.test_tidal.TestTidalStreamCleanup**

  - [+] test_cancellation_removes_partial_output

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
  - [+] test_stream_serves_cached_file_with_range (0.01s)

**tests.test_tidal_library.TestTidalDiscovery**

  - [+] test_featured_extracts_album_lists_deduped
  - [+] test_featured_no_pagination
  - [+] test_charts_keeps_only_chart_modules
  - [+] test_editorial_excludes_charts_and_albums
  - [+] test_editorial_no_pagination

**tests.test_tidal_library.TestTidalFavoritesPlaylists**

  - [+] test_favorites_albums_unwraps_item_wrapper
  - [+] test_playlists_maps_uuid_to_album

**tests.test_tidal_library.TestTidalCoverGuard**

  - [+] test_returns_none_for_dict_uuid
  - [+] test_returns_none_for_none
  - [+] test_returns_none_for_empty_string
  - [+] test_returns_url_for_valid_uuid

**tests.test_tidal_library.TestTidalArtistAlbums**

  - [+] test_hits_artist_endpoint_and_maps

**tests.test_transport_control.TestTransportActions**

  - [+] test_action_set_contents

**tests.test_transport_control.TestControlRouting**

  - [+] test_unknown_service_returns_false
  - [+] test_mpd_protocol_routes_to_control_mpd_and_invalidates
  - [+] test_failed_dispatch_does_not_invalidate
  - [+] test_hqplayer_virtual_source_routes_to_control_hqplayer
  - [+] test_renderer_virtual_source_routes_to_control_renderer
  - [+] test_mpris_protocol_routes_with_mpris_name

**tests.test_transport_control.TestControlHqplayerRefreshesCache**

  - [+] test_toggle_refreshes_owning_service_cache

**tests.test_transport_control.TestDbusControlTimeout**

  - [+] test_dbus_send_timeout_returns_false

**tests.test_upmpdcli_cover.TestParseAvtUrl**

  - [+] test_returns_control_url_for_avt_service
  - [+] test_returns_none_when_no_avt_service
  - [+] test_returns_none_on_http_error

**tests.test_upmpdcli_cover.TestSoapGetArt**

  - [+] test_extracts_album_art_uri
  - [+] test_returns_none_when_no_track_metadata
  - [+] test_returns_none_on_soap_error

**tests.test_upmpdcli_cover.TestGetArtForMpdUrl**

  - [+] test_returns_art_url_from_avt
  - [+] test_result_is_cached_no_second_soap_call
  - [+] test_returns_none_when_no_renderer_found
  - [+] test_miss_is_cached_no_repeated_discovery
  - [+] test_avt_url_cache_reused_for_different_track
  - [+] test_cache_expires_and_retries
  - [+] test_miss_url_cache_prevents_ssdp_on_per_track_expiry

**tests.test_upnp_renderer.TestAgNotifyServer**

  - [+] test_callback_url
  - [+] test_async_start_stop_are_noops
  - [+] test_handle_incoming_no_handler_returns_503
  - [+] test_handle_incoming_delegates_to_event_handler

**tests.test_upnp_renderer.TestRendererServiceConfig**

  - [+] test_load_config_missing_file
  - [+] test_load_config_valid
  - [+] test_load_config_invalid_json
  - [+] test_disconnect_clears_state_and_config
  - [+] test_disconnect_calls_async_stop_before_unsubscribe

**tests.test_upnp_renderer.TestRendererServicePlayback**

  - [+] test_play_calls_set_uri_then_play
  - [+] test_stop_delegates
  - [+] test_pause_calls_avtransport_action_directly
  - [+] test_resume_calls_avtransport_play_directly
  - [+] test_pause_sends_action_without_stale_publish
  - [+] test_pause_noop_when_no_avtransport_action
  - [+] test_seek_abs_time
  - [+] test_seek_refreshes_position_after_success
  - [+] test_seek_raises_when_not_supported
  - [+] test_seek_falls_back_to_rel_time_when_abs_fails
  - [+] test_seek_marks_track_nonseekable_when_device_rejects
  - [+] test_set_volume_normalises_0_100_to_0_1
  - [+] test_set_volume_raises_when_not_supported
  - [+] test_no_dmr_raises_on_play

**tests.test_upnp_renderer.TestRendererServiceStatus**

  - [+] test_status_no_dmr_returns_disconnected
  - [+] test_status_with_dmr_returns_state
  - [+] test_status_exposes_queue_next_track
  - [+] test_status_queue_next_is_none_at_end
  - [+] test_status_cover_token_from_active_queue_entry
  - [+] test_status_cover_token_none_when_no_queue
  - [+] test_status_can_seek_true_when_abs_time_supported
  - [+] test_status_can_seek_false_when_unsupported
  - [+] test_status_dsd_uri_sets_format
  - [+] test_status_pcm_uri_format_is_none
  - [+] test_status_queue_fields_none_when_no_queue

**tests.test_upnp_renderer.TestMinimalDidl**

  - [+] test_builds_valid_xml
  - [+] test_escapes_special_chars
  - [+] test_empty_title_falls_back_to_uri

**tests.test_upnp_renderer.TestPublishStatus**

  - [+] test_publish_calls_event_bus
  - [+] test_publish_dedup_suppresses_identical_payload
  - [+] test_publish_skipped_when_no_event_bus
  - [+] test_disconnect_event_not_suppressed_by_previous_hash
  - [+] test_on_dmr_event_coalesces_publish_tasks
  - [+] test_on_dmr_event_calls_check_queue_advance
  - [+] test_publish_status_force_always_publishes_and_updates_hash
  - [+] test_publish_status_force_then_nonforce_dedup_works (0.01s)

**tests.test_upnp_renderer.TestSsdpTargetsRenderer**

  - [+] test_ssdp_message_targets_media_renderer

**tests.test_upnp_renderer.TestNotifySenderAllowed**

  - [+] test_matching_ipv4_allowed
  - [+] test_mismatched_ipv4_rejected
  - [+] test_ipv6_canonical_variants_match
  - [+] test_hostname_location_fails_open
  - [+] test_unknown_side_fails_open
  - [+] test_route_calls_handle_notify_when_allowed (0.04s)

**tests.test_upnp_renderer.TestRendererRouterEndpoints**

  - [+] test_discover_route_exists (0.04s)
  - [+] test_known_route_exists (0.03s)
  - [+] test_connection_route_exists (0.03s)
  - [+] test_status_route_exists (0.03s)
  - [+] test_notify_route_exists (0.05s)
  - [+] test_bypass_route_removed (0.03s)
  - [+] test_remove_renderer_route_exists (0.03s)

**tests.test_upnp_renderer.TestRendererManagerRemove**

  - [+] test_remove_known_renderer_removes_from_list
  - [+] test_remove_persists_config
  - [+] test_remove_unknown_udn_is_noop
  - [+] test_remove_active_renderer_clears_active_udn
  - [+] test_remove_active_renderer_calls_disconnect

**tests.test_upnp_renderer.TestPlayQueue**

  - [+] test_play_queue_single_entry_calls_play
  - [+] test_play_queue_empty_is_noop
  - [+] test_play_queue_preloads_second_track_via_set_next
  - [+] test_play_queue_no_set_next_when_not_supported
  - [+] test_play_queue_lazy_resolver_called_at_play_time
  - [+] test_play_queue_on_play_called_with_resolved_uri
  - [+] test_advance_queue_stopped_plays_next
  - [+] test_advance_queue_uri_changed_registers_metadata_only
  - [+] test_advance_queue_at_end_clears_queue
  - [+] test_advance_queue_guard_prevents_concurrent_advances
  - [+] test_check_queue_advance_playing_to_stopped_schedules_task
  - [+] test_check_queue_advance_uri_change_while_playing_schedules_task (0.01s)
  - [+] test_check_queue_advance_no_trigger_when_queue_empty
  - [+] test_check_queue_advance_deduplicates_when_task_pending
  - [+] test_check_queue_advance_creates_task_when_previous_done
  - [+] test_stop_clears_queue
  - [+] test_direct_play_clears_queue
  - [+] test_advance_queue_resolver_failure_rolls_back_queue_idx
  - [+] test_play_queue_entry_always_re_resolves_with_resolver
  - [+] test_advance_queue_uri_changed_re_resolves_for_on_play
  - [+] test_stop_resets_prev_transport_state_and_uri
  - [+] test_advance_queue_stopped_anchors_prev_track_uri
  - [+] test_advance_queue_rollback_safe_when_stop_clears_queue

**tests.test_upnp_renderer.TestHandleUpdateResult**

  - [+] test_success_resets_failure_counter
  - [+] test_success_recovers_reachable_and_returns_true
  - [+] test_failure_increments_counter
  - [+] test_failure_flips_reachable_false_at_threshold
  - [+] test_failure_below_threshold_does_not_flip
  - [+] test_failure_already_unreachable_does_not_return_changed

**tests.test_upnp_renderer.TestQueueNavigation**

  - [+] test_advance_queue_public_plays_next_track
  - [+] test_advance_queue_raises_at_end
  - [+] test_advance_queue_raises_when_no_queue
  - [+] test_retreat_queue_plays_previous_track
  - [+] test_retreat_queue_raises_at_first_track
  - [+] test_retreat_queue_raises_when_no_queue
  - [+] test_retreat_queue_anchors_prev_track_uri

**tests.test_upnp_renderer.TestSidMismatchRecovery**

  - [+] test_handle_notify_ok_does_not_resubscribe
  - [+] test_handle_notify_412_schedules_resubscribe
  - [+] test_handle_notify_412_no_dmr_does_not_schedule
  - [+] test_resubscribe_and_refresh_calls_unsubscribe_then_subscribe
  - [+] test_resubscribe_guard_prevents_concurrent_calls (0.05s)
  - [+] test_resubscribe_no_dmr_is_noop

**tests.test_upnp_renderer.TestDiscoverIsLocal**

  - [+] test_discover_sets_is_local_flag

**tests.test_upnp_renderer.TestRetreatQueueRaceGuard**

  - [+] test_retreat_queue_clears_when_stop_races
  - [+] test_retreat_queue_guard_exits_when_queue_empty_at_entry

**tests.test_upnp_renderer.TestResubscribeRestoresReachability**

  - [+] test_resubscribe_restores_reachable_after_successful_update
  - [+] test_resubscribe_marks_unreachable_on_update_failure

**tests.test_upnp_renderer.TestAutoReconnectRaceGuard**

  - [+] test_ghost_connection_torn_down_when_service_removed_during_connect
  - [+] test_no_teardown_when_service_still_present_after_connect

**tests.test_upnp_renderer.TestBackgroundTaskRefs**

  - [+] test_send_play_tracks_poll_task
  - [+] test_handle_notify_412_tracks_resubscribe_task

**tests.test_upnp_renderer.TestPlayingQueueOrigin**

  - [+] test_returns_the_origin_of_the_entry_being_played
  - [+] test_returns_none_when_the_device_plays_something_else
  - [+] test_returns_none_on_an_empty_queue
  - [+] test_returns_none_without_a_current_uri
  - [+] test_returns_none_when_the_entry_carries_no_origin
  - [+] test_reads_the_entry_at_the_current_index
  - [+] test_out_of_range_index_is_survivable

**tests.test_version**

  - [+] test_product_version_is_semver
  - [+] test_backend_version_matches_product_version

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
  - [+] queueItem > always posts to /library/queue — HQPlayer routing is the backend's call
  - [+] upnpPlay > routes to /library/upnp-play by default
  - [+] upnpPlay > always posts to /library/upnp-play — HQPlayer routing is the backend's call
  - [+] queueWithFeedback > calls queueFn and shows success toast on success
  - [+] queueWithFeedback > shows error toast when queueFn throws (0.01s)
  - [+] queueWithFeedback > uses fallback label when label is empty
  - [+] playWithFeedback > returns true and stays silent when the play is accepted
  - [+] playWithFeedback > relays the server message verbatim rather than a generic one
  - [+] playWithFeedback > returns false on failure so the caller can skip opening the player
  - [+] playWithFeedback > never rethrows — the caller must not need its own catch
  - [+] playWithFeedback > falls back to a readable message when the error carries none
  - [+] playWithFeedback > survives a rejection that is not an Error object

**js/library-store.favorites.test.js**

  - [+] library-store favorites > fetches once and serves subsequent reads from the cache (dedup + TTL)
  - [+] library-store favorites > returns a copy — mutating the result never leaks into the cache
  - [+] library-store favorites > setAlbumFavorited optimistically updates the cache, persists, and notifies
  - [+] library-store favorites > reverts the cache and re-notifies when persistence fails
  - [+] library-store favorites > unsubscribe stops notifications

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
  - [+] notifyOutputError > raises a toast when the active output starts failing
  - [+] notifyOutputError > does not repeat the toast while the same failure persists
  - [+] notifyOutputError > announces a different failure even without recovery in between
  - [+] notifyOutputError > re-arms after recovery so the next failure is announced again
  - [+] notifyOutputError > stays silent when the output is healthy
  - [+] notifyOutputError > ignores an error on an output that is not active

**js/orientation-lock.test.js**

  - [+] applyOrientationLock > touch device, locked while in landscape: adds the class and calls lock("portrait")
  - [+] applyOrientationLock > touch device, locked but already portrait: skips the redundant lock (manifest handles it)
  - [+] applyOrientationLock > touch device, unlocked: removes the class and calls lock("any") to override the manifest
  - [+] applyOrientationLock > non-touch (desktop/mouse): never touches the Screen Orientation API, still toggles the class
  - [+] applyOrientationLock > no Screen Orientation API (iOS): no-op on the API, still toggles the class
  - [+] applyOrientationLock > swallows a rejected lock()
  - [+] applyOrientationLock > swallows a SYNCHRONOUS throw from lock() (legacy engines)

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
  - [+] isSelfManagedDriver > true for the HQPlayer driver (control_id)
  - [+] isSelfManagedDriver > true for a renderer cast even when re-badged (display != routing)
  - [+] isSelfManagedDriver > false for local MPD playback
  - [+] isSelfManagedDriver > falls back to source_id when control_id is absent (legacy state)
  - [+] isSelfManagedDriver > false for null/empty
  - [+] applySeekGuard > passes the state through when no seek is pending
  - [+] applySeekGuard > holds the target while a stale position arrives
  - [+] applySeekGuard > releases as soon as the backend position reaches the target
  - [+] applySeekGuard > expires so a refused seek cannot freeze the bar
  - [+] applySeekGuard > releases on a track change instead of holding the old target
  - [+] applySeekGuard > treats a missing elapsed as position zero, not as arrival
  - [+] applySeekGuard > does not mutate the incoming state object
  - [+] applySeekGuard > tolerates a small drift as arrival rather than fighting the backend

**js/push-manager.test.js**

  - [+] push-manager unsubscribe (Fix P3) > calls apiDelete (not apiPost) on unsubscribe (0.08s)
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

  - [+] version propagation (single source: audiogravity.ops/VERSION) > VERSION is a valid semver (0.9.19)
  - [+] version propagation (single source: audiogravity.ops/VERSION) > js/core/config.js UI_VERSION matches VERSION (UI display)
  - [+] version propagation (single source: audiogravity.ops/VERSION) > sw.js CACHE_NAME matches VERSION (PWA cache busting)

**js/webauthn.test.js**

  - [+] loginWithPasskey > short-circuits (NoPasskeyError) without prompting when the username has no passkey
  - [+] loginWithPasskey > prompts and completes when the user has passkeys
  - [+] loginWithPasskey > discoverable flow (no username) still prompts even with empty allowCredentials

**js/components/component-imports.test.js**

  - [+] component import graph > every <ag-*> tag used in a component template is imported by that component (0.13s)

**js/components/library-constants.test.js**

  - [+] originBadge > returns null for empty/unknown origin
  - [+] originBadge > maps a known origin to its label and an icon
  - [+] originBadge > uses the explicit name over the generic label
  - [+] originBadge > falls back to the library icon for an unknown but truthy origin
  - [+] originBadge > exposes a label for every mapped origin
  - [+] originBadge > badges "external" properly instead of showing the raw key
  - [+] originBadge > gives "external" its own icon, not the generic fallback
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
  - [+] formatTimestamp > returns locale string for timestamps older than 24h (0.03s)
  - [+] loadConnection > sets _connection on success and clears _loading
  - [+] loadConnection > sets _connection to null on fetch failure
  - [+] loadConnection > always clears _loading even on failure

**js/core/FavoritesController.test.js**

  - [+] FavoritesController > registers with the host
  - [+] FavoritesController > load() subscribes, fills the id set, and requests an update
  - [+] FavoritesController > load() re-subscribes when the source changes (unsubscribing the previous one)
  - [+] FavoritesController > a favorites notification re-syncs from the cache
  - [+] FavoritesController > hostDisconnected unsubscribes
  - [+] FavoritesController > toggle(add) optimistically adds and persists
  - [+] FavoritesController > toggle(remove) optimistically removes and persists
  - [+] FavoritesController > reverts the optimistic change and toasts when persistence fails

**js/core/SwipeToDismissController.test.js**

  - [+] SwipeToDismissController > registers itself with the host
  - [+] SwipeToDismissController > drags the element left imperatively past the slop
  - [+] SwipeToDismissController > does not move within the slop
  - [+] SwipeToDismissController > clamps right swipes to zero (left only)
  - [+] SwipeToDismissController > commits onCommit(key) and snaps back when released past the threshold
  - [+] SwipeToDismissController > does NOT commit when released below the threshold
  - [+] SwipeToDismissController > never commits on pointercancel, even past the threshold
  - [+] SwipeToDismissController > respects a custom commit threshold
  - [+] SwipeToDismissController > ignores non-primary buttons
  - [+] SwipeToDismissController > carries the SINGLE key for single-element hosts
  - [+] SwipeToDismissController > screen-edge guard (panel-open swipe coexistence) > ignores a gesture that starts in the right-edge band (reserved for the settings panel)
  - [+] SwipeToDismissController > screen-edge guard (panel-open swipe coexistence) > ignores a gesture that starts in the left-edge band (reserved for the sidebar)
  - [+] SwipeToDismissController > screen-edge guard (panel-open swipe coexistence) > still arms and commits a gesture that starts clear of the reserved bands
  - [+] SwipeToDismissController > screen-edge guard (panel-open swipe coexistence) > exempts the MOUSE: an edge-start mouse drag still arms (no touch panel to coexist with)
  - [+] SwipeToDismissController > multi-touch / pointer isolation > ignores a second concurrent pointerdown and never mixes their state
  - [+] SwipeToDismissController > multi-touch / pointer isolation > ignores move/end from a foreign pointerId
  - [+] SwipeToDismissController > trailing-click suppression + timer cleanup > keeps `swiping` true through the trailing click, then clears it
  - [+] SwipeToDismissController > trailing-click suppression + timer cleanup > does not leave `swiping` set after a plain tap (never crossed the slop)
  - [+] SwipeToDismissController > trailing-click suppression + timer cleanup > hostDisconnected clears the pending timer
  - [+] swipeRow directive > stamps the coexistence contract and wires the four pointer listeners
  - [+] swipeRow directive > does not wire or stamp when enabled is false
  - [+] swipeRow directive > tears down listeners and the contract on disconnect
  - [+] swipeRow directive > throws when used outside an element binding

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
  - [+] AgHqplayerOutput._renderCard — connection state display > setting is ON but HQPlayer cannot be reached > keeps the toggle visible when HQPlayer is offline
  - [+] AgHqplayerOutput._renderCard — connection state display > setting is ON but HQPlayer cannot be reached > keeps the toggle visible when the NAA is offline
  - [+] AgHqplayerOutput._renderCard — connection state display > setting is ON but HQPlayer cannot be reached > still reports the connection as offline — visibility is not connectivity
  - [+] AgHqplayerOutput — a view must not mutate the shared setting > no longer defines an updated() hook that writes the setting
  - [+] AgHqplayerOutput — a view must not mutate the shared setting > keeps the setting untouched when the NAA goes offline
  - [+] AgHqplayerOutput — a view must not mutate the shared setting > leaves the toggle reachable so the user can turn it off themselves
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > updates naa_available to false when hqplayer service goes inactive
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > updates naa_available to true when hqplayer service becomes active
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > ignores events for other services
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > does nothing when _connection is null
  - [+] AgHqplayerOutput._handleNaaMetrics() — SSE real-time update > does not mutate _connection when state is unchanged
  - [+] AgHqplayerOutput._toggleOutput — server-side setting > switching ON persists the choice on the backend
  - [+] AgHqplayerOutput._toggleOutput — server-side setting > never overwrites _connection with the toggle response
  - [+] AgHqplayerOutput._toggleOutput — server-side setting > switching OFF persists it too — the backend releases the sound card
  - [+] AgHqplayerOutput._toggleOutput — server-side setting > adopts the server answer even if it differs from the request
  - [+] AgHqplayerOutput._toggleOutput — server-side setting > reverts the switch when the call fails (0.02s)
  - [+] AgHqplayerOutput._toggleOutput — one write at a time > ignores a second flip while the first is still in flight
  - [+] AgHqplayerOutput._toggleOutput — one write at a time > accepts the next flip once the first has settled
  - [+] AgHqplayerOutput._toggleOutput — one write at a time > releases the lock even when the call fails

**js/components/molecules/ag-library-scan-indicator.test.js**

  - [+] ag-library-scan-indicator > renders nothing while idle (0.03s)
  - [+] ag-library-scan-indicator > shows the indexing row once a scan is observed (0.04s)
  - [+] ag-library-scan-indicator > flashes "indexed" then hides when the scan completes (0.02s)
  - [+] ag-library-scan-indicator > gives up quietly when no scan is ever caught (too fast)
  - [+] ag-library-scan-indicator > tolerates a failing status endpoint without throwing
  - [+] ag-library-scan-indicator > stops polling once disconnected
  - [+] ag-library-scan-indicator > resumes the indicator on mount when a scan is already running

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

**js/components/molecules/ag-network-mount-form.test.js**

  - [+] ag-network-mount-form > validates required fields and credential pairing (0.04s)
  - [+] ag-network-mount-form > asks for the admin password transiently and submits a trimmed payload
  - [+] ag-network-mount-form > does nothing when the password prompt is cancelled
  - [+] ag-network-mount-form > surfaces the core mount error and keeps the form
  - [+] ag-network-mount-form > does not prompt nor call the API when client validation fails
  - [+] ag-network-mount-form > removes a share after showConfirm, clearing any stale error
  - [+] ag-network-mount-form > does not delete when the confirm is declined
  - [+] ag-network-mount-form > deletes with force directly when the share is the active library
  - [+] ag-network-mount-form > offers a forced retry on a 409 busy and honors the second confirm
  - [+] ag-network-mount-form > keeps the 409 error when the forced retry is declined
  - [+] ag-network-mount-form > loads the existing AG mounts when opened (0.03s)

**js/components/molecules/ag-prov-library-picker.test.js**

  - [+] payloadFor > manual path → music_directory
  - [+] payloadFor > manual empty/whitespace → null
  - [+] payloadFor > usb source → library_usb_uuid + fstype
  - [+] payloadFor > mount source → music_directory
  - [+] payloadFor > no choice → null
  - [+] payloadFor > out-of-range source index → null
  - [+] _emit > updates state and emits library-change with the resolved payload (usb)
  - [+] _emit > emits null payload for an empty manual path
  - [+] reindexChoice > passes manual and null choices through unchanged
  - [+] reindexChoice > re-anchors a card selection to its new index by identity
  - [+] reindexChoice > keeps the index when nothing before it changed
  - [+] reindexChoice > clears the selection when its source is gone
  - [+] reindexChoice > matches USB sources by uuid, not path
  - [+] reindexChoice > clears when the previous index is out of range
  - [+] clearRemovedManual > clears a manual selection pointing at the removed mountpoint
  - [+] clearRemovedManual > keeps a manual selection pointing elsewhere
  - [+] clearRemovedManual > leaves a card (src:) or empty selection untouched

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
  - [+] _onMountCreated > refreshes sources then selects the new share via the manual path
  - [+] _onMountCreated > still refreshes, but selects nothing, on a malformed event
  - [+] _onMountRemoved > clears a manual selection pointing at the removed share, and refreshes
  - [+] _onMountRemoved > keeps a manual selection pointing elsewhere, but still refreshes
  - [+] _refreshSources > preserves the user DAC pick and never flips the loading flag
  - [+] _refreshSources > re-anchors a card selection by identity when the list shifts
  - [+] _refreshSources > clears a card selection whose source is gone
  - [+] _refreshSources > keeps the current view on a transient fetch failure (0.01s)

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
  - [+] _apply > patches only the output when only the output changed (airplay) (0.01s)
  - [+] _apply > patches output AND library for mpd, and clears the library choice
  - [+] _apply > does nothing when there is no change (0.01s)
  - [+] _apply > reports an error and does not emit on failure
  - [+] _reset > regenerates with the admin password and emits guided-changed
  - [+] _reset > aborts when the password prompt is cancelled
  - [+] _onMountCreated > selects the freshly mounted share via the manual path (index-proof)
  - [+] _onMountCreated > ignores a malformed event
  - [+] _onMountRemoved > clears the selection when it pointed at the removed share
  - [+] _onMountRemoved > leaves a selection that pointed elsewhere untouched
  - [+] willUpdate — library selection re-anchor > re-anchors a card selection when the parent re-fetches librarySources
  - [+] willUpdate — library selection re-anchor > clears a card selection whose source disappeared
  - [+] willUpdate — library selection re-anchor > leaves a manual selection untouched

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

**js/components/organisms/ag-library-queue.test.js**

  - [+] ag-library-queue — source filter > _distinctOrigins dedups, preserves first-seen order, ignores empties
  - [+] ag-library-queue — source filter > single-source up-next is not "mixed" and offers no filter options
  - [+] ag-library-queue — source filter > mixed up-next defaults to showing every source, with All + one option per origin
  - [+] ag-library-queue — source filter > origins come from up-next only — a current-only origin is not a filter option
  - [+] ag-library-queue — source filter > filtering keeps only the chosen source and preserves real MPD positions
  - [+] ag-library-queue — source filter > a stale filter (its source gone from up-next) falls back to all for display
  - [+] ag-library-queue — source filter > _onFilterChange updates the active filter
  - [+] ag-library-queue — Clear respects the filter > _clear removes only the shown (filtered) items, not the whole queue
  - [+] ag-library-queue — Clear respects the filter > _clear with no filter clears every up-next item
  - [+] ag-library-queue — _load prunes a stale filter > drops a filter whose source is no longer up-next
  - [+] ag-library-queue — _load prunes a stale filter > keeps a filter whose source is still up-next

**js/components/organisms/ag-library-radio.test.js**

  - [+] AbortController — race condition guard > creates a new AbortController on each call
  - [+] AbortController — race condition guard > aborts the previous controller when called a second time
  - [+] AbortController — race condition guard > ignores results from a cancelled request (signal.aborted guard)
  - [+] AbortController — race condition guard > clears loading flag after a successful non-aborted search
  - [+] AbortController — race condition guard > does not clear loading flag when the request is aborted

**js/components/organisms/ag-manual-modal.test.js**

  - [+] ag-manual-modal > fallback chapters are structurally sound (unique ids, NN-prefix order, labels) (0.01s)
  - [+] ag-manual-modal > parseToc (live TOC from README.md) > parses numbered contents entries, including chapter 0, stripping label markup
  - [+] ag-manual-modal > parseToc (live TOC from README.md) > returns empty for markdown with no contents list
  - [+] ag-manual-modal > _loadToc (sidebar derived from the published README) > replaces the fallback with the parsed live TOC
  - [+] ag-manual-modal > _loadToc (sidebar derived from the published README) > keeps the fallback (and allows a retry) when the fetch fails
  - [+] ag-manual-modal > _loadToc (sidebar derived from the published README) > keeps the fallback when the README has no parsable contents list
  - [+] ag-manual-modal > starts closed
  - [+] ag-manual-modal > open() shows the modal and loads the default (first) chapter (0.04s)
  - [+] ag-manual-modal > open(id) loads the requested chapter (0.01s)
  - [+] ag-manual-modal > auto-loads a chapter when opened via the is-open property (not open())
  - [+] ag-manual-modal > does not double-load: open() sets _loading so updated() skips the auto-load
  - [+] ag-manual-modal > fetches the right URL, renders via marked, and caches (no refetch) (0.04s)
  - [+] ag-manual-modal > de-duplicates concurrent loads of the same uncached chapter (single fetch)
  - [+] ag-manual-modal > shows an error state on a non-OK response and logs it (not swallowed)
  - [+] ag-manual-modal > shows an error state when the network throws (offline box)
  - [+] ag-manual-modal > close() hides the modal and emits manual-close
  - [+] ag-manual-modal > Escape closes an open modal but is ignored when closed
  - [+] ag-manual-modal > renders one TOC item per fallback chapter and the rendered chapter body (0.02s)
  - [+] ag-manual-modal > click handling (never navigate the host app away) > switches chapter in place for a tagged intra-manual link
  - [+] ag-manual-modal > click handling (never navigate the host app away) > passes the anchor for a tagged chapter+anchor link
  - [+] ag-manual-modal > click handling (never navigate the host app away) > scrolls for an in-page anchor without loading a chapter
  - [+] ag-manual-modal > click handling (never navigate the host app away) > leaves rewritten external links to the browser (no preventDefault, no in-modal load)
  - [+] ag-manual-modal > click handling (never navigate the host app away) > leaves mailto: links to the OS
  - [+] ag-manual-modal > click handling (never navigate the host app away) > ignores clicks that are not on a link
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > tags an intra-manual chapter link and points it at the published URL
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > carries the anchor on a chapter+anchor link
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > absolutises a sibling repo doc and opens it in a new tab
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > leaves in-page anchors and mailto untouched
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > is idempotent — a second pass does not re-rewrite a chapter link
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > absolutises a manual-relative image against the manual base, lazily
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > keeps absolute and data: image sources as authored (still lazy)
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > is idempotent — a second pass leaves an already-absolutised image unchanged
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > stamps GitHub-style slug ids (punctuation, duplicate dedup, unicode) (0.01s)
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > enhances at cache time: cached HTML already has ids, absolute lazy images

**js/components/organisms/ag-network-test.test.js**

  - [+] AgNetworkTest.disconnectedCallback — jitterChart destroy (Fix P2) > destroys _jitterChart when component is disconnected (0.07s)
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
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > rendererActive: true when an active renderer output is present
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > rendererActive: false when the renderer entry is inactive (unreachable)
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > rendererActive: false with local-only outputs
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > rendererActive: false when no outputs yet
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > hasSignal: true with non-empty signal_path
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > hasSignal: true with output_label only
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > hasSignal: false with empty path and no label
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > signal path shown when renderer inactive and signal present
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > signal path shown when no renderer and signal present
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > renderer step present in signal_path when renderer active (backend enrichment)
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > idle renderer badge shown when renderer active but signal_path is empty
  - [+] AgNowPlayingFullscreen — _rendererActive + signal path (outputs[]-based) > idle renderer badge NOT shown when renderer inactive and no signal
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
  - [+] AgNowPlayingFullscreen — Up next from PlayerState.queue_next > renderer cast: up-next comes from state.queue_next, no fetch
  - [+] AgNowPlayingFullscreen — Up next from PlayerState.queue_next > renderer cast at end of queue: up-next cleared, no fetch
  - [+] AgNowPlayingFullscreen — Up next from PlayerState.queue_next > local playback: falls back to the queue fetch
  - [+] AgNowPlayingFullscreen — control body routing handle > sends the displayed state control_id when it matches the target
  - [+] AgNowPlayingFullscreen — control body routing handle > does not send a mismatched handle after a source switch
  - [+] AgNowPlayingFullscreen — control body routing handle > sends control_id with no explicit target (active-source control)
  - [+] AgNowPlayingFullscreen — output error > reads the error from the ACTIVE output entry
  - [+] AgNowPlayingFullscreen — output error > ignores an error on an inactive output
  - [+] AgNowPlayingFullscreen — output error > no error in the normal case
  - [+] AgNowPlayingFullscreen — output error > a busy device gets an actionable plain-language label
  - [+] AgNowPlayingFullscreen — output error > any other failure falls back to a generic label
  - [+] fullscreen — Up next source selection > uses the renderer queue when the displayed item IS the cast
  - [+] fullscreen — Up next source selection > does NOT use it for another source while a cast runs elsewhere
  - [+] fullscreen — Up next source selection > falls back to source_id when control_id is absent
  - [+] fullscreen — Up next source selection > is false for a plain local source with no outputs listed

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
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > rendererActive: true when an active renderer output is present
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > rendererActive: false when the renderer entry is inactive (unreachable)
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > rendererActive: false with local-only outputs
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > rendererActive: false when no outputs yet
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > renderer badge name comes from the outputs entry
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > connector badge hidden when a renderer is active (renderer = own DAC stack)
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > connector badge visible when no renderer
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > connector badge hidden when output_connector absent (no renderer)
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > connector badge hidden when output_connector absent (renderer active)
  - [+] AgNowPlaying — _rendererActive + connector badge (outputs[]-based) > connector badge visible with TOSLINK when renderer entry inactive
  - [+] AgNowPlaying — control body routing handle > sends control_id from the item alongside source_id
  - [+] AgNowPlaying — control body routing handle > omits control_id when the item has none (legacy fallback)
  - [+] AgNowPlaying — control body routing handle > seek still maps to seek_position with the handle present

**js/components/organisms/ag-orientation-gate.test.js**

  - [+] ag-orientation-gate > tags itself with the .orientation-gate CSS hook on connect (0.23s)
  - [+] ag-orientation-gate > renders the rotate prompt and a landscape escape hatch (0.02s)
  - [+] ag-orientation-gate > _dismiss turns the lock off (state + persisted) and applies it (0.02s)
  - [+] ag-orientation-gate > _setBackgroundInert inerts sibling top-level elements but never itself (0.02s)

**js/components/organisms/ag-pipeline-page.test.js**

  - [+] ag-pipeline-page topology save > persists directly when the topology is valid with no warnings
  - [+] ag-pipeline-page topology save > blocks the save and shows the modal on structural errors
  - [+] ag-pipeline-page topology save > asks for confirmation before persisting when there are warnings
  - [+] ag-pipeline-page topology save > persists once the warning confirmation callback runs
  - [+] ag-pipeline-page topology save > falls through to the save when validation is unreachable (0.01s)
  - [+] ag-pipeline-page topology save > reports a backend save failure without closing the modal

**js/components/organisms/ag-user-modal.test.js**

  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (6 spaces) is rejected (0.02s)
  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (tabs) is rejected
  - [+] AgUserModal._handleSave — password trim (Fix P3) > valid password passes validation
  - [+] AgUserModal._handleSave — password trim (Fix P3) > password with surrounding spaces is trimmed before sending
  - [+] AgUserModal._handleSave — password trim (Fix P3) > short username is rejected regardless of password
