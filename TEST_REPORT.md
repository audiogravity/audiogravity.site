# Audiogravity — Test Report

Generated: **2026-07-06 10:53 UTC**

## Summary

| | Tests | Passed | Failed | Skipped | Duration |
|---|---:|---:|---:|---:|---:|
| **core** PASS | 1002 | 1002 | 0 | 0 | 41.4s |
| **ui** PASS | 363 | 363 | 0 | 0 | 0.7s |
| **Total** PASS | **1365** | **1365** | **0** | **0** | **42.1s** |

## Detail

### core

**tests.test_app**

  - [+] test_coreapp_uses_default_json_response_class (0.01s)
  - [+] test_responses_serialize_to_json

**tests.test_audio_app_config.TestAudioAppConfig**

  - [+] test_services_route (0.51s)

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

  - [+] test_devices_returns_200 (0.01s)
  - [+] test_devices_response_shape
  - [+] test_devices_returns_empty_when_no_proc
  - [+] test_force_refresh_param_accepted
  - [+] test_mock_route_via_conftest_fixture

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

  - [+] test_cover_returns_24h_cache (0.01s)
  - [+] test_cover_404_no_store (0.02s)

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

  - [+] test_status_returns_200 (0.01s)
  - [+] test_provision_200_maps_request_to_provisioner (0.01s)
  - [+] test_provision_initial_requires_valid_password (0.01s)
  - [+] test_provision_wrong_password_returns_401 (0.01s)
  - [+] test_provision_missing_password_returns_401 (0.02s)
  - [+] test_provision_regenerate_missing_password_returns_401 (0.01s)
  - [+] test_provision_passes_library_usb_fields (0.01s)
  - [+] test_provision_value_error_returns_400 (0.01s)
  - [+] test_provision_missing_card_name_returns_422 (0.01s)
  - [+] test_patch_output_200_no_password_required (0.01s)
  - [+] test_patch_output_missing_card_name_returns_422 (0.01s)
  - [+] test_patch_output_value_error_returns_400 (0.01s)
  - [+] test_patch_library_200_no_password_required (0.01s)

**tests.test_auth.TestLogin**

  - [+] test_login_valid (0.38s)
  - [+] test_login_wrong_password (0.38s)
  - [+] test_login_unknown_user (0.39s)

**tests.test_auth.TestUsersCRUD**

  - [+] test_list_users (0.02s)
  - [+] test_create_and_delete_user (0.39s)
  - [+] test_update_user_role (0.39s)
  - [+] test_cannot_delete_self (0.02s)

**tests.test_auth.TestProtectedFlag**

  - [+] test_user_model_has_protected_field
  - [+] test_create_user_accepts_protected_flag (0.36s)
  - [+] test_unprotected_user_has_protected_false_by_default (0.36s)
  - [+] test_delete_guard_rejects_protected (0.37s)
  - [+] test_update_disable_guard_rejects_protected (0.37s)
  - [+] test_cannot_delete_self (0.02s)
  - [+] test_unprotected_account_can_be_deleted (0.39s)
  - [+] test_unprotected_account_can_be_disabled (0.38s)

**tests.test_auth.TestCreateUserReturns201**

  - [+] test_create_user_returns_201 (0.38s)

**tests.test_auth.TestUpdateUserEmptyPassword**

  - [+] test_short_password_rejected_by_pydantic (0.39s)
  - [+] test_whitespace_only_password_rejected (0.41s)

**tests.test_auth.TestDisabledUserLogin**

  - [+] test_disabled_user_cannot_login (0.75s)

**tests.test_auth.TestJwtContainsJti**

  - [+] test_jwt_has_jti_claim (0.01s)

**tests.test_auth.TestCreateUserWhitespacePassword**

  - [+] test_whitespace_only_password_rejected_on_create (0.01s)
  - [+] test_normal_password_accepted_on_create (0.38s)

**tests.test_auth.TestDisabledUserTimingOracle**

  - [+] test_disabled_user_returns_401 (0.80s)

**tests.test_auth.TestWebAuthnChallengeIsolation**

  - [+] test_registration_and_auth_challenges_are_independent
  - [+] test_double_begin_registration_does_not_clobber

**tests.test_auth.TestUpdateUserReturnsUpdatedState**

  - [+] test_update_returns_new_role (0.39s)

**tests.test_auth.TestVerifyAdminPassword**

  - [+] test_skips_when_jwt_disabled
  - [+] test_valid_password_when_jwt_enabled
  - [+] test_wrong_password_when_jwt_enabled
  - [+] test_unknown_user_when_jwt_enabled

**tests.test_config_validation.TestConfigValidation**

  - [+] test_post_validate (0.03s)

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

  - [+] test_validation_error_returns_400

**tests.test_core.TestEventBus**

  - [+] test_publish_reaches_subscriber
  - [+] test_history_returned_on_subscribe
  - [+] test_queue_full_drops_subscriber_not_event
  - [+] test_different_channels_isolated

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

  - [+] test_dsd_ended_restores_volume (0.01s)
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
  - [+] test_stream_redirect_mode_returns_302_to_cdn (0.01s)
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

**tests.test_hqplayer.TestHQPlayer**

  - [+] test_status (0.03s)
  - [+] test_filters (0.03s)
  - [+] test_shapers (0.03s)
  - [+] test_modes (0.03s)
  - [+] test_discover (0.03s)

**tests.test_hqplayer.TestHQPlayerStop**

  - [+] test_stop_returns_success (0.04s)
  - [+] test_stop_503_on_hqplayer_error (0.03s)

**tests.test_hqplayer.TestHQPlayerLiteralValidation**

  - [+] test_invalid_item_type_returns_422 (0.03s)
  - [+] test_invalid_action_returns_422 (0.03s)
  - [+] test_valid_item_type_accepted (0.03s)

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

  - [+] test_naa_available_true_when_service_active (0.03s)
  - [+] test_naa_available_false_when_service_inactive (0.04s)

**tests.test_hqplayer.TestHQPlayerPlayValidation**

  - [+] test_play_without_path_or_uri_returns_400 (0.03s)
  - [+] test_play_with_uri_accepted (0.03s)

**tests.test_library.TestLibrary**

  - [+] test_upnp_known_servers_route_exists (0.07s)
  - [+] test_search_route_exists (0.07s)
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

**tests.test_library.TestUpnpQueueRouting**

  - [+] test_upnp_source_routes_to_upnp_queue (0.07s)
  - [+] test_mpd_source_still_routes_to_mpd_queue (0.08s)

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

  - [+] test_browse_delegates_to_dms
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
  - [+] test_range_returns_206_partial (0.19s)
  - [+] test_head_returns_headers_no_body (0.07s)
  - [+] test_bad_signature_rejected (0.07s)
  - [+] test_missing_signature_rejected (0.07s)
  - [+] test_missing_file_returns_404 (0.07s)

**tests.test_library_files.TestLibraryCoverEndpoint**

  - [+] test_valid_sig_returns_cover (0.01s)
  - [+] test_bad_sig_rejected_without_resolving (0.01s)
  - [+] test_missing_sig_rejected (0.01s)
  - [+] test_cover_not_found_returns_404 (0.01s)

**tests.test_license.TestGetStatus**

  - [+] test_no_license (0.04s)
  - [+] test_valid_lifetime_license (0.04s)
  - [+] test_beta_version_accepts_v1_scope (0.07s)
  - [+] test_version_expired (0.04s)
  - [+] test_tampered_license (0.05s)

**tests.test_license.TestUploadLicense**

  - [+] test_upload_valid_lic (0.05s)
  - [+] test_upload_invalid_signature (0.01s)

**tests.test_license.TestDeleteLicense**

  - [+] test_delete_existing_license (0.06s)
  - [+] test_delete_wrong_password (0.03s)
  - [+] test_delete_no_license (0.01s)
  - [+] test_no_name_error (0.05s)

**tests.test_license.TestVerifyHeaders**

  - [+] test_returns_key_when_configured
  - [+] test_returns_empty_when_not_configured

**tests.test_license.TestPortalBase**

  - [+] test_strips_verify_suffix
  - [+] test_invalid_url_returns_empty

**tests.test_license.TestCheckEndpointStatusHandling**

  - [+] test_server_5xx_returns_502 (0.02s)
  - [+] test_unexpected_response_shape_returns_502 (0.02s)

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

**tests.test_minimal_configs**

  - [+] test_supported_services
  - [+] test_mpd_minimal_content_and_roundtrip
  - [+] test_upmpdcli_minimal_content_and_roundtrip
  - [+] test_shairport_minimal_content_and_roundtrip
  - [+] test_device_is_not_hardcoded
  - [+] test_unknown_service_raises
  - [+] test_generated_config_carries_ag_marker_and_still_parses[mpd]
  - [+] test_generated_config_carries_ag_marker_and_still_parses[upmpdcli]
  - [+] test_generated_config_carries_ag_marker_and_still_parses[airplay]
  - [+] test_has_ag_marker_false_for_distro_default

**tests.test_net**

  - [+] test_is_local_url_matches_loopback_and_localhost
  - [+] test_is_local_url_matches_primary_ip
  - [+] test_is_local_url_rejects_remote_host
  - [+] test_is_local_url_empty_or_unparseable_is_remote
  - [+] test_is_local_url_handles_detection_failure

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
  - [+] test_mpris_spotify
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

**tests.test_now_playing.TestDbusControlTimeout**

  - [+] test_dbus_send_timeout_returns_false

**tests.test_now_playing.TestMpdFileUriControlChars**

  - [+] test_newline_rejected
  - [+] test_tab_rejected
  - [+] test_null_byte_rejected
  - [+] test_clean_uri_not_rejected

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

  - [+] test_runs_standalone_without_package_context (7.67s)

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

  - [+] test_poll_loop_continues_after_get_now_playing_exception (10.02s)

**tests.test_packages.TestPlayerDsdGatherFailure**

  - [+] test_dsd_active_reset_on_gather_failure (0.01s)

**tests.test_performance.TestPerformance**

  - [+] test_cpu_info_route (0.11s)
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
  - [+] test_renderer_prepended_when_active
  - [+] test_no_renderer_step_when_no_active_service
  - [+] test_source_prepended_from_origin
  - [+] test_full_chain_renderer_active
  - [+] test_full_chain_no_renderer
  - [+] test_radio_shows_canonical_label_not_station_name
  - [+] test_upnp_uses_server_name_from_origin_name
  - [+] test_upnp_falls_back_to_upnp_label_when_no_server_name
  - [+] test_native_renderer_signal_path_ends_at_renderer
  - [+] test_native_renderer_with_source_prepended
  - [+] test_renderer_unreachable_does_not_appear_in_signal_path

**tests.test_player.TestTryRendererControl**

  - [+] test_toggle_pauses_when_playing
  - [+] test_toggle_resumes_when_stopped
  - [+] test_handles_local_mpd_renderer_via_avtransport
  - [+] test_toggle_on_local_mpd_falls_through_to_mpd
  - [+] test_seek_on_local_mpd_falls_through_to_mpd
  - [+] test_set_volume_on_local_mpd_falls_through_to_mpd
  - [+] test_returns_false_when_no_active_renderer
  - [+] test_next_calls_advance_queue
  - [+] test_set_volume_calls_renderer_set_volume
  - [+] test_unknown_action_returns_false

**tests.test_player.TestControlRoutesThroughActiveRenderer**

  - [+] test_next_routed_to_renderer_not_mpd (0.15s)
  - [+] test_falls_back_to_mpd_when_no_renderer (0.16s)

**tests.test_player.TestBuildNativeRendererState**

  - [+] test_native_renderer_active_returns_state
  - [+] test_local_mpd_renderer_returns_none
  - [+] test_renderer_not_reachable_returns_none
  - [+] test_no_active_renderer_returns_none
  - [+] test_playing_transport_state_maps_correctly
  - [+] test_paused_transport_state_maps_correctly
  - [+] test_can_next_true_when_not_at_last_track
  - [+] test_can_next_false_at_last_track
  - [+] test_origin_library_for_cast_local_file
  - [+] test_origin_qobuz_for_qobuz_proxy_stream
  - [+] test_origin_upnp_for_plain_server_stream
  - [+] test_origin_upnp_when_no_uri

**tests.test_player.TestPlayer**

  - [+] test_snapshot (0.02s)
  - [+] test_control (0.02s)
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
  - [+] test_stale_active_udn_cleared_not_raised (0.02s)
  - [+] test_stale_active_udn_calls_save_config (0.02s)

**tests.test_profiles.TestActivateProfile**

  - [+] test_activate (0.04s)
  - [+] test_deactivate (0.02s)

**tests.test_profiles.TestProfilesGatherTimeout**

  - [+] test_stop_timeout_does_not_raise

**tests.test_profiles.TestStoppedCountFailedLogic**

  - [+] test_failed_state_is_not_stopped

**tests.test_profiles.TestProfileExportPath**

  - [+] test_export_not_in_tmp

**tests.test_provisioning**

  - [+] test_generates_when_absent
  - [+] test_provision_writes_alsa_index_pin_for_usb_dac
  - [+] test_provision_no_pin_for_non_usb_output
  - [+] test_provision_respects_existing_user_pin
  - [+] test_user_pins_usb_device_matches_hex_forms
  - [+] test_overwrites_when_exists
  - [+] test_regenerate_backups_then_overwrites
  - [+] test_provision_mpd_without_library_raises
  - [+] test_regenerate_mpd_reuses_existing_library
  - [+] test_regenerate_mpd_without_existing_config_raises
  - [+] test_provision_airplay_only_without_library_ok (0.01s)
  - [+] test_unresolved_device_raises
  - [+] test_persists_stable_id_not_hw
  - [+] test_persist_preserves_existing_topology
  - [+] test_ensure_usb_library_writes_units_and_enables
  - [+] test_ensure_usb_library_exfat_installs_exfatprogs
  - [+] test_provision_with_usb_library_uses_mountpoint
  - [+] test_per_service_outputs_are_independent
  - [+] test_read_outputs_migrates_legacy_single_pin
  - [+] test_persist_output_preserves_other_service_on_legacy_migration
  - [+] test_discover_library_sources_usb_and_network
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

  - [+] test_get_connection_connected
  - [+] test_delete_connection
  - [+] test_get_connection_after_disconnect
  - [+] test_stream_redirect_mode_returns_302_to_cdn (0.01s)
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

  - [+] test_featured_albums (0.07s)
  - [+] test_featured_albums_default_type (0.07s)
  - [+] test_playlists (0.08s)
  - [+] test_playlist_tracks (0.07s)
  - [+] test_playlist_tracks_missing_id (0.07s)
  - [+] test_featured_service_error (0.07s)

**tests.test_qobuz_library.TestQobuzQueueHelper**

  - [+] test_adds_tracks_as_stable_redirect_proxy_urls
  - [+] test_play_action_triggers_playid

**tests.test_radio.TestRadio**

  - [+] test_search_route (0.05s)
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
  - [+] test_connect_stops_previous_active (0.01s)
  - [+] test_connect_upserts_known_list
  - [+] test_connect_rejects_local_renderer

**tests.test_renderer_manager.TestDisconnect**

  - [+] test_disconnect_raises_for_unknown_udn
  - [+] test_disconnect_clears_active_udn
  - [+] test_disconnect_keeps_renderer_in_known (0.11s)

**tests.test_self_update.TestState**

  - [+] test_read_state_idle_when_absent
  - [+] test_write_initial_and_read_roundtrip
  - [+] test_write_initial_none_version_is_latest
  - [+] test_is_in_progress
  - [+] test_read_state_tolerates_corrupt_file
  - [+] test_stale_in_progress_is_ignored
  - [+] test_fresh_in_progress_without_timestamp_is_conservative
  - [+] test_paths_derive_from_settings

**tests.test_self_update.TestBuildCommand**

  - [+] test_latest_when_no_version
  - [+] test_explicit_version
  - [+] test_token_passed_as_leading_wrapper_arg

**tests.test_self_update.TestLaunchTokenFallback**

  - [+] test_falls_back_to_configured_token
  - [+] test_explicit_token_wins_over_configured

**tests.test_self_update.TestUpdateEndpoints**

  - [+] test_update_rejects_bad_password (0.03s)
  - [+] test_update_conflict_when_in_progress (0.03s)
  - [+] test_update_happy_path_launches (0.02s)
  - [+] test_update_status_reflects_state (0.02s)

**tests.test_services.TestListServices**

  - [+] test_list_all (0.04s)

**tests.test_services.TestServiceInfo**

  - [+] test_get_service (0.03s)

**tests.test_services.TestServiceActions**

  - [+] test_restart_service (0.05s)
  - [+] test_stop_service (0.03s)
  - [+] test_start_service (0.03s)

**tests.test_services.TestServiceNameValidation**

  - [+] test_valid_name_accepted (0.03s)
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

**tests.test_steering.TestRendererPreDisconnect**

  - [+] test_local_renderer_disconnected_before_alsa_switch (1.51s)
  - [+] test_native_renderer_not_disconnected (1.51s)
  - [+] test_no_active_renderer_switch_proceeds (1.50s)

**tests.test_steering.TestVerifyAlsaDevice**

  - [+] test_returns_false_when_pcm_missing
  - [+] test_returns_true_when_pcm_exists

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
  - [+] test_mpd_queue_local_mpd_renderer_stays_direct
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

  - [+] test_smartctl_not_found_returns_none (0.03s)

**tests.test_sysinfo.TestSysinfoGrepPatternValidation**

  - [+] test_invalid_regex_returns_400 (0.02s)
  - [+] test_valid_regex_accepted (0.05s)

**tests.test_sysinfo.TestSysinfoSyslogIdentifierFormat**

  - [+] test_correct_format_in_service

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
  - [+] test_post_connection_starts_pkce (0.01s)
  - [+] test_submit_connection (0.01s)
  - [+] test_delete_connection (0.01s)

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
  - [+] test_pause_delegates_when_supported
  - [+] test_pause_skipped_when_not_supported
  - [+] test_seek_abs_time
  - [+] test_seek_raises_when_not_supported
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
  - [+] test_publish_status_force_then_nonforce_dedup_works

**tests.test_upnp_renderer.TestSsdpTargetsRenderer**

  - [+] test_ssdp_message_targets_media_renderer

**tests.test_upnp_renderer.TestRendererRouterEndpoints**

  - [+] test_discover_route_exists (0.04s)
  - [+] test_known_route_exists (0.04s)
  - [+] test_connection_route_exists (0.04s)
  - [+] test_status_route_exists (0.03s)
  - [+] test_notify_route_exists (0.03s)
  - [+] test_bypass_route_removed (0.03s)
  - [+] test_remove_renderer_route_exists (0.03s)

**tests.test_upnp_renderer.TestRendererManagerRemove**

  - [+] test_remove_known_renderer_removes_from_list
  - [+] test_remove_persists_config
  - [+] test_remove_unknown_udn_is_noop
  - [+] test_remove_active_renderer_clears_active_udn (0.02s)
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
  - [+] test_check_queue_advance_uri_change_while_playing_schedules_task
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

**tests.test_upnp_renderer.TestUsesLocalMpd**

  - [+] test_default_is_true
  - [+] test_is_local_renderer_true_for_local_ip
  - [+] test_is_local_renderer_true_for_loopback
  - [+] test_is_local_renderer_false_for_remote_ip
  - [+] test_get_status_exposes_uses_local_mpd_default
  - [+] test_get_status_exposes_uses_local_mpd_false

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
  - [+] queueItem > routes to /hqplayer/play-library when hqplayer_output is true
  - [+] upnpPlay > routes to /library/upnp-play by default
  - [+] upnpPlay > routes to /hqplayer/play when hqplayer_output is true
  - [+] upnpPlay > passes duration as null when not provided
  - [+] queueWithFeedback > calls queueFn and shows success toast on success
  - [+] queueWithFeedback > shows error toast when queueFn throws (0.01s)
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

  - [+] push-manager unsubscribe (Fix P3) > calls apiDelete (not apiPost) on unsubscribe (0.13s)
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

**js/version.test.js**

  - [+] version propagation (single source: audiogravity.ops/VERSION) > VERSION is a valid semver (0.9.10)
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
  - [+] formatTimestamp > returns locale string for timestamps older than 24h (0.06s)
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
  - [+] _acquisitionStepsHtml — price as text node > embeds price as plain text, XSS payload is inert
  - [+] _acquisitionStepsHtml — price as text node > embeds a valid price string correctly

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

**js/components/molecules/ag-update-banner.test.js**

  - [+] ag-update-banner — isUpdateAvailable > is false for null / undefined / empty
  - [+] ag-update-banner — isUpdateAvailable > is false when available is false
  - [+] ag-update-banner — isUpdateAvailable > is false when available but latest is missing
  - [+] ag-update-banner — isUpdateAvailable > is true when available with a latest version
  - [+] ag-update-banner — updatePhaseLabel > maps known phases to human labels
  - [+] ag-update-banner — updatePhaseLabel > falls back to a generic label for unknown/empty phases
  - [+] ag-update-banner — terminal phases > treats done/rolled_back/failed as terminal
  - [+] ag-update-banner — terminal phases > does not treat in-progress phases as terminal

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

**js/components/organisms/ag-library-radio.test.js**

  - [+] AbortController — race condition guard > creates a new AbortController on each call
  - [+] AbortController — race condition guard > aborts the previous controller when called a second time
  - [+] AbortController — race condition guard > ignores results from a cancelled request (signal.aborted guard)
  - [+] AbortController — race condition guard > clears loading flag after a successful non-aborted search
  - [+] AbortController — race condition guard > does not clear loading flag when the request is aborted

**js/components/organisms/ag-network-test.test.js**

  - [+] AgNetworkTest.disconnectedCallback — jitterChart destroy (Fix P2) > destroys _jitterChart when component is disconnected (0.13s)
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

**js/components/organisms/ag-user-modal.test.js**

  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (6 spaces) is rejected (0.01s)
  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (tabs) is rejected
  - [+] AgUserModal._handleSave — password trim (Fix P3) > valid password passes validation
  - [+] AgUserModal._handleSave — password trim (Fix P3) > password with surrounding spaces is trimmed before sending
  - [+] AgUserModal._handleSave — password trim (Fix P3) > short username is rejected regardless of password
