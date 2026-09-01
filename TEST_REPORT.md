# Audiogravi<sup>ty</sup> — Test Report

Generated: **2026-09-01 19:38 UTC**

## Summary

| | Tests | Passed | Failed | Skipped | Duration |
|---|---:|---:|---:|---:|---:|
| **core** PASS | 2465 | 2465 | 0 | 0 | 73.8s |
| **ui** PASS | 1630 | 1630 | 0 | 0 | 13.1s |
| **Total** PASS | **4095** | **4095** | **0** | **0** | **86.9s** |

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

**tests.test_api_docs_switch**

  - [+] test_default_is_off
  - [+] test_all_three_routes_are_gone_when_off[/docs] (0.01s)
  - [+] test_all_three_routes_are_gone_when_off[/redoc]
  - [+] test_all_three_routes_are_gone_when_off[/openapi.json]
  - [+] test_all_three_routes_answer_when_on[/docs]
  - [+] test_all_three_routes_answer_when_on[/redoc]
  - [+] test_all_three_routes_answer_when_on[/openapi.json] (0.01s)
  - [+] test_schema_describes_the_api_when_on (0.01s)
  - [+] test_entry_point_does_not_advertise_what_it_does_not_serve (0.01s)
  - [+] test_entry_point_advertises_the_reference_when_on

**tests.test_app**

  - [+] test_coreapp_uses_default_json_response_class
  - [+] test_responses_serialize_to_json

**tests.test_audio_app_config.TestAudioAppConfig**

  - [+] test_services_route (0.47s)

**tests.test_audio_app_config.TestPackageEventReload**

  - [+] test_reload_on_package_events[package_state-True] (0.70s)
  - [+] test_reload_on_package_events[packages_updated-True] (0.70s)
  - [+] test_reload_on_package_events[some_other_event-False] (0.71s)

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

**tests.test_audio_app_config.TestLicenceGate**

  - [+] test_config_editing_works_without_a_licence (0.02s)
  - [+] test_guided_provisioning_works_without_a_licence_too (0.02s)
  - [+] test_guided_provisioning_stays_admin_only (0.02s)

**tests.test_audio_app_config.TestConfigTileInstallState**

  - [+] test_absent_package_is_reported_as_not_installed (0.03s)
  - [+] test_idle_but_installed_service_keeps_its_state (0.03s)
  - [+] test_silent_or_failing_lookup_does_not_accuse (0.03s)
  - [+] test_no_dbus_on_the_box_leaves_every_tile_optimistic (0.03s)
  - [+] test_a_non_service_unit_is_not_turned_into_a_missing_one (0.03s)
  - [+] test_a_bare_service_name_is_still_completed (0.03s)

**tests.test_audio_app_config.TestSystemdStateStaysOffTheAudioPath**

  - [+] test_pipeline_refresh_asks_for_no_systemd_state
  - [+] test_opting_out_skips_the_lookup_entirely (0.03s)
  - [+] test_the_default_still_answers_the_config_tab (0.03s)

**tests.test_audio_app_config.TestConfigFileExists**

  - [+] test_a_present_file_is_reported_as_present (0.01s)
  - [+] test_a_missing_file_is_reported_as_missing
  - [+] test_an_unreadable_file_is_not_called_missing

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
  - [+] test_mock_route_via_conftest_fixture (0.01s)

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

**tests.test_audio_pipeline.TestOutputsThatMatchNothingDeclared**

  - [+] test_an_output_in_use_and_undeclared_is_reported
  - [+] test_a_declared_kind_is_not_reported
  - [+] test_a_spare_card_nobody_uses_is_not_reported
  - [+] test_a_second_card_of_a_declared_kind_is_given_the_benefit_of_the_doubt
  - [+] test_an_undeclared_kind_is_reported_even_next_to_a_declared_one
  - [+] test_a_box_with_no_sound_card_reports_nothing

**tests.test_audio_pipeline.TestTheStreamerCarriesTheAnswer**

  - [+] test_the_first_streamer_carries_it_and_keeps_its_metadata
  - [+] test_no_other_device_carries_it
  - [+] test_nothing_to_report_touches_no_node

**tests.test_audio_stack_router**

  - [+] test_status_returns_200 (0.02s)
  - [+] test_provision_200_maps_request_to_provisioner (0.02s)
  - [+] test_provision_initial_requires_valid_password (0.02s)
  - [+] test_provision_wrong_password_returns_401 (0.02s)
  - [+] test_provision_missing_password_returns_401 (0.02s)
  - [+] test_provision_regenerate_missing_password_returns_401 (0.02s)
  - [+] test_provision_passes_library_usb_fields (0.02s)
  - [+] test_provision_value_error_returns_400 (0.02s)
  - [+] test_provision_missing_card_name_returns_422 (0.02s)
  - [+] test_patch_output_200_no_password_required (0.02s)
  - [+] test_patch_output_missing_card_name_returns_422 (0.03s)
  - [+] test_patch_output_value_error_returns_400 (0.02s)
  - [+] test_patch_library_200_no_password_required (0.02s)

**tests.test_auth.TestGetApiKeyNotifyExemption**

  - [+] test_notify_callback_with_udn_is_public[/upnp-renderer/uuid:30fd2f17-453c/notify]
  - [+] test_notify_callback_with_udn_is_public[/api/upnp-renderer/uuid:30fd2f17-453c/notify]
  - [+] test_other_renderer_routes_still_require_key[/upnp-renderer/known]
  - [+] test_other_renderer_routes_still_require_key[/upnp-renderer/uuid:abc/connection]

**tests.test_auth.TestLogin**

  - [+] test_login_valid (0.49s)
  - [+] test_login_wrong_password (0.44s)
  - [+] test_login_unknown_user (0.38s)

**tests.test_auth.TestUsersCRUD**

  - [+] test_list_users (0.02s)
  - [+] test_create_and_delete_user (0.39s)
  - [+] test_update_user_role (0.39s)
  - [+] test_cannot_delete_self (0.02s)

**tests.test_auth.TestProtectedFlag**

  - [+] test_user_model_has_protected_field
  - [+] test_create_user_accepts_protected_flag (0.37s)
  - [+] test_unprotected_user_has_protected_false_by_default (0.37s)
  - [+] test_delete_guard_rejects_protected (0.37s)
  - [+] test_update_disable_guard_rejects_protected (0.36s)
  - [+] test_cannot_delete_self (0.02s)
  - [+] test_unprotected_account_can_be_deleted (0.39s)
  - [+] test_unprotected_account_can_be_disabled (0.40s)

**tests.test_auth.TestCreateUserReturns201**

  - [+] test_create_user_returns_201 (0.41s)

**tests.test_auth.TestUpdateUserEmptyPassword**

  - [+] test_short_password_rejected_by_pydantic (0.39s)
  - [+] test_whitespace_only_password_rejected (0.39s)

**tests.test_auth.TestDisabledUserLogin**

  - [+] test_disabled_user_cannot_login (0.76s)

**tests.test_auth.TestJwtContainsJti**

  - [+] test_jwt_has_jti_claim (0.01s)

**tests.test_auth.TestCreateUserWhitespacePassword**

  - [+] test_whitespace_only_password_rejected_on_create (0.02s)
  - [+] test_normal_password_accepted_on_create (0.39s)

**tests.test_auth.TestDisabledUserTimingOracle**

  - [+] test_disabled_user_returns_401 (0.77s)

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

**tests.test_auth.TestWebauthnLoginBeginNoEnumeration**

  - [+] test_uniform_response_for_known_and_unknown_user (0.02s)

**tests.test_auth.TestUsersFilePermissions**

  - [+] test_users_json_is_0600 (0.37s)

**tests.test_auth.TestApiKeyNonAscii**

  - [+] test_non_ascii_api_key_returns_403_not_500

**tests.test_auth.TestStdlibLogRedaction**

  - [+] test_filter_redacts_token_in_message
  - [+] test_filter_redacts_jwt

**tests.test_broadcast.TestInstalledMajor**

  - [+] test_maps_major_with_v0_as_one[0.9.28-1]
  - [+] test_maps_major_with_v0_as_one[0.9.29-dev-1]
  - [+] test_maps_major_with_v0_as_one[1.4.0-1]
  - [+] test_maps_major_with_v0_as_one[2.0.0-2]
  - [+] test_maps_major_with_v0_as_one[10.1.2-10]

**tests.test_broadcast.TestRefreshPublicBroadcast**

  - [+] test_parses_announcements_and_update_into_broadcast
  - [+] test_sends_box_identity_headers
  - [+] test_missing_broadcast_keys_leave_previous_value (0.01s)

**tests.test_broadcast.TestGetCachedOverlay**

  - [+] test_overlays_broadcast_for_trial_box
  - [+] test_overlays_broadcast_when_expired
  - [+] test_valid_licence_keeps_verify_values

**tests.test_broadcast.TestPublicConfigCache**

  - [+] test_refresh_caches_commercial_config
  - [+] test_failed_fetch_keeps_last_known

**tests.test_broadcast.TestPublicConfigProxy**

  - [+] test_serves_cache_without_ls_call (0.10s)
  - [+] test_cold_cache_falls_back_to_live_fetch

**tests.test_config_validation.TestConfigValidation**

  - [+] test_post_validate (0.01s)

**tests.test_config_validation.TestConfigValidationLicenceGate**

  - [+] test_config_validation_works_without_a_licence (0.01s)
  - [+] test_topology_validation_still_needs_one (0.01s)
  - [+] test_topology_validation_passes_with_a_licence

**tests.test_config_validation.TestAppconfigFileIsInert**

  - [+] test_any_value_parses_without_complaint[/tmp/evil.conf]
  - [+] test_any_value_parses_without_complaint[/var/log/evil.conf]
  - [+] test_any_value_parses_without_complaint[../../etc/shadow]
  - [+] test_any_value_parses_without_complaint[/etc/shadow]
  - [+] test_it_never_changes_which_file_the_editor_opens[/tmp/evil.conf]
  - [+] test_it_never_changes_which_file_the_editor_opens[/var/log/evil.conf]
  - [+] test_it_never_changes_which_file_the_editor_opens[]
  - [+] test_it_never_changes_which_file_the_editor_opens[/etc/mpd-other.conf]
  - [+] test_the_field_is_absent_from_the_shipped_template

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
  - [+] test_critical_profile_starting_one_critical_service_is_fine
  - [+] test_critical_profile_that_starts_nothing_is_fine
  - [+] test_empty_profile_warns

**tests.test_config_validation.TestAsyncSystemStateChecks**

  - [+] test_missing_systemd_unit_returns_invalid
  - [+] test_missing_config_file_returns_invalid

**tests.test_config_validation.TestConfigValidationRouterErrorCodes**

  - [+] test_validation_error_returns_400

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
  - [+] test_sync_connect_creates_no_api_when_no_core_answers
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

**tests.test_cover_art.TestAlbumCacheNeverBlocksADirectSource**

  - [+] test_a_negative_album_entry_does_not_stop_the_url_being_fetched
  - [+] test_a_success_repairs_the_album_entry_for_the_other_tracks
  - [+] test_a_positive_album_entry_still_answers_without_fetching
  - [+] test_a_negative_album_entry_still_spares_the_slow_lookups
  - [+] test_a_token_carrying_no_artist_and_album_is_untouched
  - [+] test_a_known_miss_is_not_re_stamped_by_another_failing_track

**tests.test_dbus_client.TestUnwrapVariant**

  - [+] test_native_values_passthrough
  - [+] test_single_wrap
  - [+] test_nested_wrap

**tests.test_dbus_client.TestProxyCacheEviction**

  - [+] test_stale_proxy_evicted_on_call_get_all_failure
  - [+] test_working_proxy_stays_in_cache

**tests.test_deploy_layout**

  - [+] test_audiogravity_home_default_points_to_core_layout
  - [+] test_core_service_unit_name (0.04s)

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
  - [+] test_login_records_the_subscription

**tests.test_highresaudio.TestHighresaudioLoginWithoutSubscription**

  - [+] test_a_session_labelled_nok_is_still_a_session
  - [+] test_the_state_says_no_subscription_rather_than_lying
  - [+] test_an_ok_answer_that_says_false_is_read_the_same_way
  - [+] test_no_session_is_still_a_refusal
  - [+] test_an_unknown_nok_with_a_session_is_not_read_as_unsubscribed
  - [+] test_a_state_saved_before_this_existed_means_subscribed

**tests.test_highresaudio.TestVaultIds**

  - [+] test_split_reads_the_prefix
  - [+] test_a_prefixed_id_goes_to_the_purchases_route_bare
  - [+] test_a_catalogue_id_goes_to_the_catalogue_route
  - [+] test_a_purchased_looking_id_without_prefix_is_logged_not_rerouted
  - [+] test_a_two_segment_id_raises_no_alarm

**tests.test_highresaudio.TestSessionDeadDetection**

  - [+] test_vault_album_dead_form
  - [+] test_vault_track_dead_form
  - [+] test_keepalive_invalid_token_form
  - [+] test_user_route_dead_form
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
  - [+] test_a_purchased_track_is_resolved_on_the_purchases_route
  - [+] test_an_ok_answer_without_a_url_is_a_failure_not_silence
  - [+] test_no_subscription_on_the_catalogue_route_raises_by_name
  - [+] test_the_proxy_path_carries_the_prefix_to_the_resolver

**tests.test_highresaudio.TestConnectionState**

  - [+] test_a_subscribed_account_says_so
  - [+] test_a_purchases_only_account_says_so
  - [+] test_disconnected_has_no_opinion (0.01s)

**tests.test_highresaudio.TestHighresaudioPersistence**

  - [+] test_not_connected_when_no_config
  - [+] test_disconnect_removes_file
  - [+] test_disconnect_no_running_loop_does_not_raise
  - [+] test_disconnect_schedules_released_logout

**tests.test_highresaudio.TestHighresaudioModels**

  - [+] test_connection_defaults
  - [+] test_login_model

**tests.test_highresaudio.TestHighresaudioTimeouts**

  - [+] test_a_slow_answer_raises_its_own_error
  - [+] test_the_timeout_is_still_a_HighresaudioError
  - [+] test_a_network_failure_is_not_reported_as_slowness
  - [+] test_a_box_that_cannot_reach_hra_is_not_told_they_are_slow

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

**tests.test_highresaudio_library.TestHraCategories**

  - [+] test_lists_titles_in_publication_order
  - [+] test_german_title_is_relabelled_but_stays_the_key
  - [+] test_an_empty_answer_is_not_memoised
  - [+] test_shares_the_memoised_category_map

**tests.test_highresaudio_library.TestHraCategory**

  - [+] test_known_category_lists_albums
  - [+] test_unknown_category_returns_empty

**tests.test_highresaudio_library.TestHraGenres**

  - [+] test_lists_the_tree_with_paths
  - [+] test_sub_genres_are_sorted_too_and_case_does_not_scatter_them
  - [+] test_a_subgenre_named_after_a_genre_keeps_its_own_content
  - [+] test_unknown_path_returns_empty_without_a_content_call
  - [+] test_tree_is_memoised
  - [+] test_an_empty_answer_is_not_memoised

**tests.test_highresaudio_library.TestHraSearchFilters**

  - [+] test_formats_and_moods_are_flattened_into_options
  - [+] test_publishes_the_nine_orders_hra_has_no_endpoint_for
  - [+] test_an_empty_answer_is_not_memoised

**tests.test_highresaudio_library.TestHraAdvancedSearch**

  - [+] test_sends_only_the_filters_that_are_set
  - [+] test_keeps_albums_and_drops_playlists
  - [+] test_a_filter_alone_is_a_search_of_its_own
  - [+] test_forwards_the_year_and_the_order
  - [+] test_an_unknown_order_is_refused_instead_of_forwarded
  - [+] test_that_refusal_has_its_own_class_and_is_not_a_bare_value_error
  - [+] test_reads_a_plus_that_a_query_string_turned_into_a_space
  - [+] test_the_default_order_sends_no_sort_at_all
  - [+] test_never_takes_more_than_two_connections_at_once
  - [+] test_waits_longer_than_the_other_endpoints

**tests.test_highresaudio_library.TestHraPlaylists**

  - [+] test_editorial_listing_uses_the_theme_as_its_byline
  - [+] test_the_accounts_own_listing_decodes_what_it_typed
  - [+] test_an_account_with_no_playlist_is_not_an_error
  - [+] test_the_accounts_pages_are_cut_here
  - [+] test_each_family_is_read_with_its_own_shape
  - [+] test_a_dict_shaped_collection_is_not_dropped

**tests.test_highresaudio_library.TestHraPlaylistAddressing**

  - [+] test_a_prefixed_id_names_its_family
  - [+] test_a_listed_id_is_accepted_as_it_was_given
  - [+] test_a_bare_id_is_read_as_editorial
  - [+] test_an_unknown_prefix_is_left_alone
  - [+] test_the_queue_asks_the_named_family

**tests.test_highresaudio_library.TestHraAlbumTracks**

  - [+] test_uses_playlistadd_as_id

**tests.test_highresaudio_library.TestHraSearch**

  - [+] test_parses_albums_and_artists
  - [+] test_artists_come_back_alphabetical_and_albums_in_relevance_order
  - [+] test_short_query_returns_empty_without_api_call
  - [+] test_caps_both_albums_and_artists_at_limit

**tests.test_highresaudio_library.TestHraQueueMpd**

  - [+] test_album_enqueues_stable_redirect_proxy_urls (0.02s)
  - [+] test_single_track_resolves_metadata_once_and_enqueues_proxy
  - [+] test_rejects_unsupported_item_type

**tests.test_highresaudio_library.TestHraVaultListing**

  - [+] test_reads_the_top_level_list_and_prefixes_every_id
  - [+] test_past_the_end_is_empty_not_an_error
  - [+] test_a_dict_shaped_list_is_not_dropped

**tests.test_highresaudio_library.TestHraVaultAlbumTracks**

  - [+] test_a_purchased_album_lists_prefixed_tracks_from_the_purchases_route
  - [+] test_a_catalogue_album_still_lists_bare_ids

**tests.test_highresaudio_library.TestHraVaultQueue**

  - [+] test_a_purchased_album_is_read_from_the_purchases_route
  - [+] test_the_tracks_keep_the_prefix_so_the_proxy_asks_the_right_tree
  - [+] test_a_catalogue_album_is_untouched
  - [+] test_a_purchased_single_track_is_resolved_through_the_service
  - [+] test_the_renderer_single_track_asks_the_purchases_route

**tests.test_highresaudio_library.TestHraArtistAlbums**

  - [+] test_quicksearch_by_name_keeps_only_exact_artist_albums
  - [+] test_searches_leading_token_but_filters_full_name
  - [+] test_short_name_returns_empty_without_calling_api
  - [+] test_nonzero_offset_returns_empty

**tests.test_highresaudio_library.TestHraSearchArtistId**

  - [+] test_artist_result_id_is_name

**tests.test_highresaudio_library.TestHraPlaylistCategories**

  - [+] test_a_shelf_is_asked_of_hra_not_filtered_here
  - [+] test_no_shelf_asked_means_every_shelf
  - [+] test_the_accounts_own_tree_ignores_a_shelf
  - [+] test_an_unknown_shelf_answers_empty_instead_of_raising

**tests.test_highresaudio_library.TestHraResultsShapes**

  - [+] test_a_list_comes_back_as_it_is
  - [+] test_a_dict_keyed_by_position_is_walked_by_value
  - [+] test_the_string_form_is_not_a_crash
  - [+] test_missing_and_null_shapes_are_empty
  - [+] test_a_row_that_is_not_an_object_costs_one_album_not_the_whole_shelf

**tests.test_highresaudio_library.TestHraLabels**

  - [+] test_lists_the_labels_in_publication_order
  - [+] test_reads_the_content_argument_out_of_the_url_including_the_path_form
  - [+] test_a_literal_ampersand_or_plus_in_the_argument_survives
  - [+] test_lists_the_albums_of_a_known_label
  - [+] test_an_unknown_label_answers_empty_without_asking_for_content
  - [+] test_the_map_is_memoised
  - [+] test_an_empty_answer_is_not_memoised

**tests.test_highresaudio_library.TestHraCharts**

  - [+] test_lists_albums_and_pages_them

**tests.test_highresaudio_library.TestHraPlaylistGroups**

  - [+] test_lists_a_grouping_alphabetically
  - [+] test_the_sort_ignores_case_so_r_and_b_sits_with_rock
  - [+] test_the_title_still_addresses_the_group_after_the_sort
  - [+] test_an_unknown_grouping_asks_for_nothing
  - [+] test_the_two_groupings_do_not_share_one_cache
  - [+] test_a_grouping_is_memoised

**tests.test_highresaudio_library.TestHraPlaylistsByGroup**

  - [+] test_a_genre_goes_to_its_own_endpoint_addressed_by_id
  - [+] test_a_theme_goes_to_the_theme_endpoint
  - [+] test_an_unknown_group_answers_empty_rather_than_the_whole_tree
  - [+] test_a_group_without_its_kind_answers_empty_not_the_whole_tree
  - [+] test_a_kind_without_its_group_answers_empty_without_fetching_the_map
  - [+] test_a_grouping_and_a_shelf_are_not_combined
  - [+] test_the_shelf_still_works_when_no_grouping_is_asked_for
  - [+] test_the_accounts_own_tree_ignores_a_grouping

**tests.test_hqplayer.TestHQPlayer**

  - [+] test_status (0.03s)
  - [+] test_filters (0.03s)
  - [+] test_shapers (0.03s)
  - [+] test_modes (0.03s)
  - [+] test_discover (0.03s)

**tests.test_hqplayer.TestHQPlayerStop**

  - [+] test_stop_returns_success (0.03s)
  - [+] test_stop_503_on_hqplayer_error (0.03s)

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
  - [+] test_naa_available_false_when_service_inactive (0.03s)

**tests.test_hqplayer.TestHQPlayerHasNoDirectPushRoute**

  - [+] test_play_route_is_gone (0.03s)
  - [+] test_play_library_route_is_gone (0.04s)

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

**tests.test_hqplayer.TestPlaybackWatch**

  - [+] test_an_advancing_position_is_the_proof_of_success (0.01s)
  - [+] test_playing_with_a_frozen_position_is_reported (0.11s)
  - [+] test_an_unanswered_status_is_never_a_verdict (0.31s)
  - [+] test_a_silent_warm_up_that_finally_plays_is_not_reported (0.04s)
  - [+] test_a_confirmed_stopped_is_reported (0.31s)
  - [+] test_a_track_stuck_in_pause_is_reported (0.31s)
  - [+] test_pausing_after_it_played_is_a_success
  - [+] test_a_spurious_exchange_error_is_ignored_when_audio_flows (0.01s)
  - [+] test_a_failed_exchange_is_not_excused_by_the_previous_track (0.13s)
  - [+] test_a_failed_exchange_is_excused_once_a_new_track_starts (0.03s)
  - [+] test_an_exchange_error_is_kept_as_the_cause_when_nothing_plays (0.31s)
  - [+] test_the_shared_status_cache_is_never_evicted (0.01s)
  - [+] test_the_first_reading_is_taken_without_waiting (0.50s)
  - [+] test_a_push_over_a_playing_track_still_confirms (0.02s)
  - [+] test_a_stopped_ending_is_not_blamed_on_the_sound_card (0.31s)
  - [+] test_the_window_covers_the_measured_dsd_warm_up
  - [+] test_the_patience_covers_the_measured_radio_start
  - [+] test_a_frozen_position_is_still_caught_before_the_window_ends (0.34s)

**tests.test_hqplayer.TestPlaybackWatchLifecycle**

  - [+] test_a_new_push_clears_the_previous_verdict (0.02s)
  - [+] test_a_new_push_cancels_the_running_watch (0.03s)
  - [+] test_a_moving_position_clears_a_stale_verdict
  - [+] test_a_frozen_position_leaves_the_verdict_in_place
  - [+] test_stopping_drops_the_watch_and_its_verdict

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
  - [+] test_host_accessor_reflects_configuration

**tests.test_hqplayer.TestPlayUriHonoursAction**

  - [+] test_add_never_clears_the_queue
  - [+] test_add_leaves_the_now_playing_metadata_alone
  - [+] test_add_does_not_wait_for_a_playback_confirmation
  - [+] test_add_propagates_an_exchange_failure
  - [+] test_play_still_clears_adds_and_plays
  - [+] test_play_defaults_when_no_action_is_given
  - [+] test_play_records_the_content_origin

**tests.test_hqplayer.TestCanDecode**

  - [+] test_supported_codecs_pass[MP3]
  - [+] test_supported_codecs_pass[FLAC]
  - [+] test_supported_codecs_pass[WAV]
  - [+] test_supported_codecs_pass[AIFF]
  - [+] test_supported_codecs_pass[WV]
  - [+] test_supported_codecs_pass[DSF]
  - [+] test_supported_codecs_pass[DFF]
  - [+] test_both_container_spellings_are_refused[M4A]
  - [+] test_both_container_spellings_are_refused[MP4]
  - [+] test_both_container_spellings_are_refused[mp4]
  - [+] test_every_officially_accepted_format_stays_allowed[FLAC]
  - [+] test_every_officially_accepted_format_stays_allowed[WAV]
  - [+] test_every_officially_accepted_format_stays_allowed[RF64]
  - [+] test_every_officially_accepted_format_stays_allowed[AIFF]
  - [+] test_every_officially_accepted_format_stays_allowed[AIF]
  - [+] test_every_officially_accepted_format_stays_allowed[WV]
  - [+] test_every_officially_accepted_format_stays_allowed[DSF]
  - [+] test_every_officially_accepted_format_stays_allowed[DFF]
  - [+] test_every_officially_accepted_format_stays_allowed[MP3]
  - [+] test_every_officially_accepted_format_stays_allowed[M3U]
  - [+] test_every_officially_accepted_format_stays_allowed[M3U8]
  - [+] test_every_officially_accepted_format_stays_allowed[PLS]
  - [+] test_formats_absent_from_the_official_list_are_refused[AC3]
  - [+] test_formats_absent_from_the_official_list_are_refused[EAC3]
  - [+] test_formats_absent_from_the_official_list_are_refused[DTS]
  - [+] test_formats_absent_from_the_official_list_are_refused[MPC]
  - [+] test_formats_absent_from_the_official_list_are_refused[TAK]
  - [+] test_formats_absent_from_the_official_list_are_refused[TTA]
  - [+] test_formats_absent_from_the_official_list_are_refused[SHN]
  - [+] test_formats_absent_from_the_official_list_are_refused[SPEEX]
  - [+] test_formats_absent_from_the_official_list_are_refused[AMR]
  - [+] test_formats_absent_from_the_official_list_are_refused[MKA]
  - [+] test_formats_absent_from_the_official_list_are_refused[WEBM]
  - [+] test_formats_absent_from_the_official_list_are_refused[AIFC]
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

**tests.test_hqplayer.TestCodecFromPath**

  - [+] test_the_extension_survives_filename_punctuation[music/artist/track.flac-FLAC]
  - [+] test_the_extension_survives_filename_punctuation[music/artist/Track.Aac-AAC]
  - [+] test_the_extension_survives_filename_punctuation[Music/Album #1/track.m4a-M4A]
  - [+] test_the_extension_survives_filename_punctuation[Music/Who's Next?/track.m4a-M4A]
  - [+] test_the_extension_survives_filename_punctuation[Music/50% Off/track.m4a-M4A]
  - [+] test_no_extension_yields_no_guess[]
  - [+] test_no_extension_yields_no_guess[music/artist/track]

**tests.test_hqplayer.TestCodecFromUri**

  - [+] test_same_file_two_servers_two_names[http://10.0.0.42:9790/minimserver/x/01%20Porto%20Vecchio.m4a-M4A]
  - [+] test_same_file_two_servers_two_names[http://10.0.0.42:32469/object/e46a68ac488c1eb01d88/file.mp4-MP4]
  - [+] test_query_and_fragment_are_stripped[http://box:8001/hqplayer/stream/a/b.m4a-M4A]
  - [+] test_query_and_fragment_are_stripped[http://box/stream/Bj%C3%B6rk%20-%20Joga.m4a-M4A]
  - [+] test_query_and_fragment_are_stripped[http://cdn/track.m4a?token=a.b.c-M4A]
  - [+] test_query_and_fragment_are_stripped[http://cdn/track.m4a#chapter.2-M4A]
  - [+] test_an_opaque_uri_yields_no_guess[]
  - [+] test_an_opaque_uri_yields_no_guess[http://srv/track/12345]
  - [+] test_an_opaque_uri_yields_no_guess[http://srv]

**tests.test_hqplayer.TestAssertDecodable**

  - [+] test_an_undecodable_codec_is_refused
  - [+] test_a_supported_codec_passes
  - [+] test_no_signal_is_let_through

**tests.test_hqplayer.TestPlayLibraryItemIsAllOrNothing**

  - [+] test_one_undecodable_track_refuses_the_whole_album

**tests.test_hqplayer.TestSeekAndLength**

  - [+] test_seek_sends_the_position_in_seconds
  - [+] test_seek_clamps_a_negative_target
  - [+] test_seek_reports_a_refusal
  - [+] test_status_parses_the_track_length
  - [+] test_a_length_of_zero_means_unknown_not_zero

**tests.test_hqplayer.TestLengthSurvivesATransientStop**

  - [+] test_a_transient_zero_keeps_the_scale_and_the_scrubber
  - [+] test_a_stream_with_no_length_stays_unseekable

**tests.test_hqplayer.TestRememberedLengthDiesWithItsTrack**

  - [+] test_a_transient_zero_keeps_the_scale_within_one_track
  - [+] test_the_next_track_does_not_inherit_the_scale
  - [+] test_the_pushed_value_is_not_used_as_a_fallback

**tests.test_hqplayer.TestPushPlaylist**

  - [+] test_an_album_is_stopped_cleared_added_in_order_then_played
  - [+] test_only_the_transport_commands_may_answer_nothing
  - [+] test_an_append_neither_stops_clears_nor_plays
  - [+] test_an_empty_push_is_refused_rather_than_sent
  - [+] test_one_undecodable_track_refuses_the_whole_push
  - [+] test_the_declared_codec_wins_over_an_opaque_url
  - [+] test_an_unknown_codec_is_still_attempted
  - [+] test_the_now_playing_record_carries_album_and_cover_together
  - [+] test_no_title_means_no_metadata_at_all

**tests.test_hqplayer.TestPublicCallersKeepTheirMetadata**

  - [+] test_play_uri_now_records_the_album (0.02s)
  - [+] test_play_library_item_now_carries_an_art_uri_key (0.02s)

**tests.test_hqplayer.TestFollowsThePushedPlaylist**

  - [+] test_the_screen_moves_with_the_track (0.01s)
  - [+] test_the_cover_moves_with_it (0.02s)
  - [+] test_a_track_index_of_zero_leaves_the_record_alone (0.02s)
  - [+] test_a_playlist_changed_outside_ag_is_disowned (0.02s)
  - [+] test_an_index_past_the_list_shows_nothing_rather_than_the_wrong_track (0.02s)
  - [+] test_a_push_records_one_entry_per_track (0.01s)
  - [+] test_an_append_extends_the_list_so_indexes_stay_aligned (0.02s)
  - [+] test_an_append_onto_a_playlist_ag_never_saw_starts_nothing
  - [+] test_a_whole_artist_push_is_not_kept_in_memory (0.04s)
  - [+] test_the_class_level_default_is_never_appended_into
  - [+] test_stopping_forgets_the_list

**tests.test_hqplayer.TestParseMpdTracks**

  - [+] test_splits_per_file
  - [+] test_a_repeated_tag_keeps_the_first_value
  - [+] test_lines_before_the_first_file_are_ignored
  - [+] test_an_unparsable_duration_is_dropped_not_fatal

**tests.test_hqplayer.TestLocalAlbumCarriesEveryTrack**

  - [+] test_each_file_keeps_its_own_title
  - [+] test_an_untagged_file_falls_back_to_its_own_name

**tests.test_hqplayer.TestBatchSurvivesALostConnection**

  - [+] test_a_write_failure_mid_batch_becomes_an_hqplayer_error
  - [+] test_a_play_keeps_going_when_the_batch_dies

**tests.test_hqplayer.TestAStatusReadInFlightDoesNotDisownTheNewPush**

  - [+] test_a_stale_answer_is_ignored_and_the_new_album_keeps_its_titles
  - [+] test_a_current_answer_still_disowns_a_foreign_playlist

**tests.test_hqplayer.TestATitlelessPushIsForgottenToo**

  - [+] test_the_list_is_dropped_after_thirty_seconds_of_silence

**tests.test_http_ssrf.TestAssertFetchable**

  - [+] test_rejects_non_http_scheme
  - [+] test_rejects_loopback_and_link_local
  - [+] test_allows_public_and_private_lan

**tests.test_http_user_agent.TestDefaultHeaders**

  - [+] test_carries_the_ag_user_agent
  - [+] test_the_user_agent_names_the_app_and_a_way_to_reach_it

**tests.test_http_user_agent.TestOutboundRequestsIdentifyAG**

  - [+] test_the_raw_shared_session_identifies_ag
  - [+] test_get_json_and_get_bytes_still_identify_ag
  - [+] test_a_caller_can_still_impose_its_own_user_agent

**tests.test_known_services.TestDeclaredPath**

  - [+] test_the_registry_supplies_the_path
  - [+] test_service_without_a_config_file_returns_none
  - [+] test_unknown_service_returns_none
  - [+] test_it_takes_no_argument_but_the_service_id

**tests.test_known_services.TestFormat**

  - [+] test_registry_decides_for_known_services
  - [+] test_registry_wins_over_the_extension
  - [+] test_extension_is_the_fallback_for_unknown_services[/etc/x.xml-xml]
  - [+] test_extension_is_the_fallback_for_unknown_services[/etc/x.ini-ini]
  - [+] test_extension_is_the_fallback_for_unknown_services[/etc/x.conf-conf]
  - [+] test_extension_is_the_fallback_for_unknown_services[/etc/x-conf]

**tests.test_known_services.TestRegistryContent**

  - [+] test_every_entry_declares_an_absolute_path
  - [+] test_paths_are_declared_under_etc

**tests.test_library.TestLibrary**

  - [+] test_upnp_known_servers_route_exists (0.14s)
  - [+] test_search_route_exists (0.14s)
  - [+] test_queue_route_exists (0.14s)

**tests.test_library.TestUpnpSearchTrackId**

  - [+] test_track_id_is_res_url
  - [+] test_search_pre_registers_title_and_art
  - [+] test_search_skips_art_registration_when_absent
  - [+] test_track_without_res_falls_back_to_object_id

**tests.test_library.TestUpnpSearchQueue**

  - [+] test_track_add_calls_mpd_add
  - [+] test_track_play_uses_mpd_batch_with_clear (0.01s)
  - [+] test_no_mpd_port_raises
  - [+] test_album_no_known_server_raises
  - [+] test_album_browses_children_and_adds_all
  - [+] test_album_play_clears_queue
  - [+] test_album_no_tracks_raises
  - [+] test_unsupported_item_type_raises
  - [+] test_queue_tags_radio_origin_and_station_logo
  - [+] test_queue_local_track_origin_library

**tests.test_library.TestUpnpQueueRouting**

  - [+] test_upnp_source_routes_to_upnp_queue (0.14s)
  - [+] test_mpd_source_still_routes_to_mpd_queue (0.14s)
  - [+] test_an_unclassified_source_is_refused_with_501 (0.13s)

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

  - [+] test_track_play_routes_to_renderer
  - [+] test_add_bypasses_renderer_goes_to_mpd
  - [+] test_no_renderer_uses_mpd
  - [+] test_album_queues_all_tracks_via_play_queue
  - [+] test_album_proxy_url_is_lan_reachable

**tests.test_library.TestTidalQueueRenderer**

  - [+] test_track_play_routes_to_renderer_with_external_url
  - [+] test_add_bypasses_renderer_goes_to_mpd
  - [+] test_no_renderer_uses_mpd
  - [+] test_tidal_proxy_url_local_only_false_uses_lan_ip

**tests.test_library.TestRendererRouting**

  - [+] test_a_ready_renderer_becomes_the_destination
  - [+] test_no_renderer_means_the_local_path
  - [+] test_a_renderer_still_reconnecting_is_refused_not_diverted
  - [+] test_nothing_selected_at_all_stays_local
  - [+] test_an_append_never_goes_to_a_renderer
  - [+] test_a_roon_item_is_never_cast
  - [+] test_streaming_services_still_reach_the_renderer

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
  - [+] test_an_unrecognised_source_is_not_declared_local[src_shairport-sync]
  - [+] test_an_unrecognised_source_is_not_declared_local[src_unknown-engine]
  - [+] test_an_unrecognised_source_is_not_declared_local[]
  - [+] test_an_unrecognised_source_is_not_declared_local[nonsense]
  - [+] test_the_local_library_is_recognised_by_its_mpd_port

**tests.test_library.TestResolveOutput**

  - [+] test_local_when_hqplayer_is_not_the_output
  - [+] test_hqplayer_takes_the_local_library
  - [+] test_hqplayer_takes_a_stream_url
  - [+] test_streaming_services_now_reach_hqplayer
  - [+] test_roon_is_never_diverted_to_hqplayer
  - [+] test_roon_is_local_even_without_hqplayer
  - [+] test_two_selected_outputs_raise_a_conflict
  - [+] test_renderer_alone_is_not_a_conflict
  - [+] test_refuses_when_the_naa_is_not_running
  - [+] test_a_dead_naa_does_not_break_local_playback
  - [+] test_roon_is_unaffected_by_a_dead_naa
  - [+] test_unknown_content_kind_fails_closed
  - [+] test_an_unclassified_source_is_refused_with_no_output_selected
  - [+] test_an_unclassified_source_is_refused_before_the_conflict_check

**tests.test_library.TestHqplayerServiceLookup**

  - [+] test_selects_hqplayer_when_it_is_the_output
  - [+] test_ignores_hqplayer_when_it_is_not_the_output
  - [+] test_refuses_to_route_without_a_configured_host
  - [+] test_is_none_when_the_module_is_absent

**tests.test_library.TestTruthfulQueueWrites**

  - [+] test_refused_local_add_raises_with_mpds_reason
  - [+] test_track_play_judges_the_playid_too
  - [+] test_album_play_surfaces_the_empty_findadd
  - [+] test_nominal_local_add_still_answers_ok
  - [+] test_remove_refusal_raises
  - [+] test_remove_nominal_reports_the_removed_id

**tests.test_library.TestTruthfulStreamEnqueue**

  - [+] test_nothing_queued_raises_with_the_reason
  - [+] test_partial_abort_keeps_ok_with_the_real_count
  - [+] test_refused_tags_do_not_fail_a_successful_enqueue
  - [+] test_refused_playid_raises_after_a_successful_add

**tests.test_library.TestQueueRefusalHttpContract**

  - [+] test_upnp_play_refusal_is_a_503_with_mpds_reason (0.13s)
  - [+] test_remove_refusal_is_a_503_with_mpds_reason (0.27s)
  - [+] test_remove_unreachable_is_a_503_not_a_500 (0.13s)

**tests.test_library.TestMpdAddOrPlayUrls**

  - [+] test_refusal_raises_with_context_and_reason
  - [+] test_play_clears_then_plays_in_one_list
  - [+] test_add_neither_clears_nor_plays

**tests.test_library.TestUpnpDurationSurvivesTheTrip**

  - [+] test_browse_item_keeps_the_duration
  - [+] test_a_track_without_one_stays_none
  - [+] test_browse_carries_it_through_the_service
  - [+] test_search_maps_it_on_BOTH_branches
  - [+] test_search_maps_it_onto_the_track

**tests.test_library.TestStoppedMpdIsNamedByTheRoutes**

  - [+] test_playing_says_MPD_is_not_running (0.17s)
  - [+] test_searching_says_it_too (0.14s)
  - [+] test_browsing_says_it_rather_than_showing_an_empty_library (0.13s)
  - [+] test_the_queue_says_it_too (0.14s)
  - [+] test_another_kind_of_unreachable_still_answers_an_empty_list (0.13s)
  - [+] test_the_status_is_503_not_500 (0.14s)

**tests.test_library.TestNoLibraryIsNotAnEmptyLibrary**

  - [+] test_a_refusal_is_raised_rather_than_read_as_zero_albums
  - [+] test_the_message_names_what_to_do
  - [+] test_a_genuinely_empty_library_is_still_empty
  - [+] test_an_album_named_like_the_refusal_is_not_mistaken_for_it

**tests.test_library.TestSearchOnALibrarylessBox**

  - [+] test_a_refusal_is_raised_rather_than_read_as_no_results
  - [+] test_a_search_that_genuinely_finds_nothing_still_finds_nothing

**tests.test_library_album_sort.TestAddedField**

  - [+] test_the_model_carries_a_library_add_date
  - [+] test_it_is_optional
  - [+] test_it_is_not_the_release_year

**tests.test_library_album_sort.TestOrdering**

  - [+] test_title_sort_is_alphabetical_and_case_blind
  - [+] test_added_sort_puts_the_newest_arrival_first
  - [+] test_an_import_pass_reads_alphabetically_despite_jittered_seconds
  - [+] test_a_later_day_still_comes_first
  - [+] test_identical_timestamps_still_fall_back_to_alphabetical
  - [+] test_albums_without_a_date_sort_last
  - [+] test_the_two_orders_actually_differ

**tests.test_library_album_sort.TestFlushKeepsAdded**

  - [+] test_the_album_record_keeps_the_added_key

**tests.test_library_album_sort.TestCacheKey**

  - [+] test_the_cache_holds_one_list_and_the_order_is_applied_on_the_way_out

**tests.test_library_album_sort.TestTheRealPath**

  - [+] test_the_service_fills_the_add_date_from_mpd
  - [+] test_title_sort_returns_them_alphabetically
  - [+] test_added_sort_returns_the_newest_arrival_first

**tests.test_library_files.TestLocalLibraryRoots**

  - [+] test_parses_music_directory_from_mpd_conf
  - [+] test_commented_music_directory_is_skipped
  - [+] test_fallback_when_conf_missing
  - [+] test_no_roots_when_the_conf_names_no_library
  - [+] test_an_empty_root_list_is_refused_by_the_resolver
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

  - [+] test_full_get_returns_all_bytes (0.13s)
  - [+] test_range_returns_206_partial (0.14s)
  - [+] test_head_returns_headers_no_body (0.13s)
  - [+] test_bad_signature_rejected (0.14s)
  - [+] test_missing_signature_rejected (0.13s)
  - [+] test_missing_file_returns_404 (0.14s)

**tests.test_library_files.TestLibraryCoverEndpoint**

  - [+] test_valid_sig_returns_cover (0.01s)
  - [+] test_bad_sig_rejected_without_resolving (0.01s)
  - [+] test_missing_sig_rejected (0.02s)
  - [+] test_cover_not_found_returns_404 (0.01s)

**tests.test_license.TestGetStatus**

  - [+] test_no_license (0.06s)
  - [+] test_valid_lifetime_license (0.06s)
  - [+] test_beta_version_accepts_v1_scope (0.05s)
  - [+] test_version_expired (0.05s)
  - [+] test_tampered_license (0.05s)

**tests.test_license.TestTimeLimitedLicenceContract**

  - [+] test_trial_licence_valid_until_its_expiry_date
  - [+] test_trial_licence_still_valid_on_its_expiry_day
  - [+] test_expired_licence_is_refused_as_expired_not_as_tampering
  - [+] test_a_forged_licence_is_told_apart_from_an_expired_one (0.01s)
  - [+] test_a_licence_for_another_device_says_so
  - [+] test_time_limited_licence_without_a_date_is_refused
  - [+] test_unreadable_expiry_date_is_refused_without_crashing
  - [+] test_lifetime_licence_needs_no_expiry
  - [+] test_today_is_read_in_utc_not_in_the_box_timezone
  - [+] test_a_licence_lapses_on_the_utc_day_not_the_local_one
  - [+] test_a_date_is_enforced_whatever_the_licence_calls_itself
  - [+] test_a_lifetime_licence_with_a_future_date_is_still_valid
  - [+] test_expiry_takes_effect_without_a_restart (0.01s)

**tests.test_license.TestTimeLimitedLicenceStatus**

  - [+] test_a_running_term_says_when_it_ends (0.05s)
  - [+] test_an_ended_term_does_not_accuse_the_customer (0.06s)
  - [+] test_a_lifetime_licence_carries_no_end_date (0.06s)
  - [+] test_a_version_locked_licence_keeps_its_details (0.06s)
  - [+] test_a_paid_term_is_not_called_a_trial (0.05s)
  - [+] test_a_perpetual_licence_is_still_called_lifetime (0.05s)
  - [+] test_a_genuinely_tampered_file_is_still_called_tampered (0.06s)

**tests.test_license.TestUploadLicense**

  - [+] test_upload_valid_lic (0.06s)
  - [+] test_upload_invalid_signature (0.01s)
  - [+] test_an_ended_licence_is_refused_with_its_own_date (0.01s)
  - [+] test_a_licence_for_another_device_says_so (0.01s)
  - [+] test_a_time_limited_licence_with_no_date_is_named_as_such (0.01s)
  - [+] test_an_unreadable_date_is_named_as_such (0.01s)
  - [+] test_a_forged_file_still_gets_the_verification_message (0.01s)

**tests.test_license.TestDeleteLicense**

  - [+] test_delete_existing_license (0.06s)
  - [+] test_delete_wrong_password (0.02s)
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

**tests.test_license.TestOnlineFetchStatusHandling**

  - [+] test_401_bad_verify_key_is_unreachable_not_invalid
  - [+] test_429_rate_limited_is_unreachable_not_invalid
  - [+] test_403_is_not_mistaken_for_a_revoked_verdict
  - [+] test_5xx_is_unreachable
  - [+] test_200_revoked_stays_a_semantic_verdict
  - [+] test_200_valid_passes_through

**tests.test_license.TestRequireFullLicenseServiceNone**

  - [+] test_returns_503_when_service_not_initialised

**tests.test_license.TestTrialRecord**

  - [+] test_existing_record_is_returned
  - [+] test_record_is_created_when_absent
  - [+] test_start_predating_machine_id_is_rejected
  - [+] test_start_within_tolerance_is_accepted
  - [+] test_malformed_signed_record_is_ignored
  - [+] test_record_path_stays_under_config_dir

**tests.test_license.TestServerTrialAnchor**

  - [+] test_deleted_record_adopts_server_anchor
  - [+] test_local_start_reconciled_down_to_earlier_anchor
  - [+] test_anchor_later_than_local_does_not_extend
  - [+] test_rolled_back_record_falls_back_to_the_anchor

**tests.test_license.TestDaysRemaining**

  - [+] test_expired_trial_returns_zero
  - [+] test_fresh_trial_returns_full_days

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

**tests.test_minimal_configs.TestNoLocalLibrary**

  - [+] test_the_directive_is_omitted_not_left_empty
  - [+] test_no_library_is_the_default
  - [+] test_the_rest_of_the_config_is_untouched
  - [+] test_it_still_round_trips_through_the_parser
  - [+] test_a_library_is_still_written_when_there_is_one
  - [+] test_the_library_stays_the_first_directive

**tests.test_mpd_client.TestClearErrorInjectionSingleCommand**

  - [+] test_playback_starters_are_prefixed_with_clearerror[play]
  - [+] test_playback_starters_are_prefixed_with_clearerror[playid 12]
  - [+] test_playback_starters_are_prefixed_with_clearerror[next]
  - [+] test_playback_starters_are_prefixed_with_clearerror[previous]
  - [+] test_other_commands_are_sent_untouched[status]
  - [+] test_other_commands_are_sent_untouched[playlistinfo]
  - [+] test_other_commands_are_sent_untouched[outputs]
  - [+] test_other_commands_are_sent_untouched[stop]
  - [+] test_prefix_matches_on_the_verb_not_a_substring
  - [+] test_response_is_still_returned_verbatim (0.01s)

**tests.test_mpd_client.TestClearErrorInjectionCommandList**

  - [+] test_clear_add_play_gets_a_leading_clearerror
  - [+] test_read_only_list_is_not_prefixed
  - [+] test_fault_tolerant_lists_are_never_prefixed
  - [+] test_only_one_clearerror_for_several_playback_starters

**tests.test_mpd_client.TestPauseAwarePrefix**

  - [+] test_resuming_pause_forms_are_prefixed[pause]
  - [+] test_resuming_pause_forms_are_prefixed[pause 0]
  - [+] test_pause_1_only_suspends_and_is_not_prefixed
  - [+] test_bare_pause_in_a_list_is_prefixed_inside_it

**tests.test_mpd_client.TestRefusalReason**

  - [+] test_success_is_none
  - [+] test_ack_line_is_returned
  - [+] test_empty_response_is_truncated
  - [+] test_fields_without_terminal_ok_are_truncated
  - [+] test_ack_letters_inside_a_tag_value_stay_a_success

**tests.test_mpd_client.TestOverallTimeout**

  - [+] test_silent_banner_trips_the_deadline (5.21s)
  - [+] test_no_timeout_keeps_the_legacy_contract

**tests.test_mpd_client.TestEnableMpdOutput**

  - [+] test_confirmed_switch_is_ok
  - [+] test_ack_is_a_real_error_with_context
  - [+] test_timeout_is_an_error_not_a_fallback
  - [+] test_by_id_beats_duplicate_names
  - [+] test_prefetched_outputs_skip_the_requery
  - [+] test_empty_response_falls_back_not_errors
  - [+] test_socket_failure_falls_back_too
  - [+] test_ack_letters_in_an_output_name_stay_a_success
  - [+] test_unknown_output_name_falls_back

**tests.test_mpd_client.TestRaiseOnRefusal**

  - [+] test_success_is_silent
  - [+] test_refusal_raises_context_plus_reason
  - [+] test_truncated_response_raises_too

**tests.test_mpd_client.TestStoppedDaemonIsNamed**

  - [+] test_a_refused_connection_says_what_to_do (1.00s)
  - [+] test_a_command_list_says_the_same (1.00s)
  - [+] test_it_is_still_an_OSError
  - [+] test_an_mpd_being_restarted_is_not_called_stopped
  - [+] test_a_refusal_is_only_named_after_being_confirmed
  - [+] test_a_wedged_daemon_is_not_called_stopped

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

**tests.test_no_lab_addresses**

  - [+] test_no_test_hardcodes_a_host_address (0.04s)
  - [+] test_guard_catches_a_reintroduction[10.0.4.254]
  - [+] test_guard_catches_a_reintroduction[10.0.4.189]
  - [+] test_guard_ignores_a_clean_tree

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
  - [+] test_no_item_when_stopped_or_unreachable (0.01s)
  - [+] test_no_item_when_no_active_renderer
  - [+] test_paused_maps_to_paused
  - [+] test_stopped_returns_none_by_default (0.23s)
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

  - [+] test_uninstall_is_complete[roon-roonbridge-RoonBridge]
  - [+] test_uninstall_is_complete[roonserver-roonserver-RoonServer]
  - [+] test_purge_runs_before_the_unit_is_removed[roon-roonbridge]
  - [+] test_purge_runs_before_the_unit_is_removed[roonserver-roonserver]
  - [+] test_version_file_defaults_to_the_vendor_layout[roon-/opt/RoonBridge]
  - [+] test_version_file_defaults_to_the_vendor_layout[roonserver-/opt/RoonServer]
  - [+] test_roon_products_declare_their_conflict[roon-roonserver]
  - [+] test_roon_products_declare_their_conflict[roonserver-roon]

**tests.test_packages.TestOsResolverStandalone**

  - [+] test_runs_standalone_without_package_context (4.76s)

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
  - [+] test_reset_keeps_the_maxlen_cap

**tests.test_packages.TestPackageLogRecovery**

  - [+] test_entries_are_numbered_and_filtered_by_after_seq
  - [+] test_response_reports_last_seq_even_when_caught_up
  - [+] test_unknown_package_raises_value_error
  - [+] test_new_operation_keeps_counting_up

**tests.test_packages.TestPackageLogsRoute**

  - [+] test_returns_entries_and_last_seq (0.02s)
  - [+] test_after_seq_returns_only_the_missing_lines (0.02s)
  - [+] test_success_level_does_not_break_the_route (0.02s)
  - [+] test_unknown_package_is_404 (0.02s)

**tests.test_packages.TestLogEntryFromWorkerThread**

  - [+] test_publish_from_worker_thread_reaches_the_event_bus (0.06s)
  - [+] test_publish_without_a_loop_is_dropped_not_raised
  - [+] test_dry_run_install_completes

**tests.test_packages.TestCommandOutputStreaming**

  - [+] test_lines_are_relayed_as_they_arrive
  - [+] test_silent_by_default_so_probes_do_not_flood_the_log
  - [+] test_third_party_failure_wording_is_not_promoted_to_error
  - [+] test_timeout_returns_a_verdict_instead_of_raising (1.01s)
  - [+] test_timeout_holds_when_the_command_forks (1.01s)
  - [+] test_newline_less_output_does_not_grow_without_bound (0.05s)
  - [+] test_reading_the_log_while_a_worker_appends_never_raises (0.10s)

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

**tests.test_packages.TestScriptLayoutResolution**

  - [+] test_derives_from_the_unit_when_installed
  - [+] test_keeps_the_registry_default_when_nothing_is_installed
  - [+] test_uninstall_restores_the_registry_default
  - [+] test_a_fallback_config_is_not_fed_the_base_registry_paths

**tests.test_packages.TestAptRepoProbe**

  - [+] test_arch_absent_from_release_is_unsupported
  - [+] test_declared_arch_without_the_package_is_unsupported
  - [+] test_published_package_is_available
  - [+] test_every_component_is_searched
  - [+] test_architecture_all_covers_every_box
  - [+] test_crlf_index_still_finds_the_package
  - [+] test_index_prefers_the_compressed_form

**tests.test_packages.TestUnreachableIsUnknownNotUnsupported**

  - [+] test_apt_deb_source_unreachable_is_unknown
  - [+] test_apt_deb_404_is_unsupported
  - [+] test_apt_deb_reachable_but_empty_is_unsupported
  - [+] test_apt_deb_published_for_another_arch_says_so
  - [+] test_apt_repo_unreachable_is_unknown
  - [+] test_apt_repo_404_is_unsupported

**tests.test_packages.TestAptSimpleProbe**

  - [+] test_known_package_is_available
  - [+] test_architecture_all_is_kept_as_is
  - [+] test_missing_package_with_lists_is_unsupported
  - [+] test_missing_package_without_lists_is_unknown
  - [+] test_one_apt_cache_call_for_the_whole_registry

**tests.test_packages.TestConflicts**

  - [+] test_installed_product_blocks_the_other
  - [+] test_an_installed_package_is_never_blocked
  - [+] test_block_is_released_when_the_blocker_goes
  - [+] test_systemd_silence_keeps_the_previous_verdict
  - [+] test_a_config_without_the_new_key_keeps_its_verdict
  - [+] test_a_vendor_verdict_outranks_the_conflict
  - [+] test_conflict_is_shown_when_nothing_else_is_wrong
  - [+] test_one_systemd_call_for_the_whole_pass

**tests.test_packages.TestAptSourceDetection**

  - [+] test_finds_a_deb822_source_under_another_name
  - [+] test_finds_a_one_line_source
  - [+] test_another_suite_does_not_count
  - [+] test_a_source_entry_does_not_count
  - [+] test_a_disabled_stanza_does_not_count
  - [+] test_a_longer_path_is_not_the_same_repository
  - [+] test_commented_out_source_does_not_count
  - [+] test_an_unreadable_file_does_not_abort_the_resolution
  - [+] test_the_suite_must_be_known

**tests.test_packages.TestArchFallbackDescribesTheChosenInstaller**

  - [+] test_fallback_arch_list_is_its_own
  - [+] test_fallback_does_not_fire_on_an_unanswered_probe

**tests.test_packages.TestResolutionStamp**

  - [+] test_generate_writes_the_stamp
  - [+] test_a_stale_stamp_is_reported

**tests.test_packages.TestLocalRefreshIsNetworkFree**

  - [+] test_refresh_touches_no_probe

**tests.test_packages.TestScriptProbeSeparatesNoBuildFromNoNetwork**

  - [+] test_404_is_unsupported
  - [+] test_no_answer_is_unknown
  - [+] test_server_error_is_unknown
  - [+] test_200_is_available

**tests.test_packages.TestOperationLocksSurviveARefresh**

  - [+] test_reinitialising_keeps_the_same_lock_objects

**tests.test_packages.TestPackageInfoIsBuiltOneWay**

  - [+] test_a_config_without_installer_type_still_builds

**tests.test_packages.TestVersionsFromTheSourceItself**

  - [+] test_only_self_sourced_installers_are_asked
  - [+] test_one_vendor_failing_does_not_sink_the_others
  - [+] test_the_installers_answer_wins_over_apt (3.76s)

**tests.test_packages.TestVersionCheckStaysOutOfTheOperationLog**

  - [+] test_finding_the_deb_url_is_silent_when_asked

**tests.test_packages.TestAptDebUpdateDoesNotUninstallFirst**

  - [+] test_update_installs_over_the_existing_package

**tests.test_packages.TestBundleReadsItsFileListFromTheManifest**

  - [+] test_file_list_comes_from_the_manifest
  - [+] test_the_version_comes_from_the_same_file
  - [+] test_an_unexpected_package_aborts
  - [+] test_a_path_in_a_filename_aborts
  - [+] test_a_missing_package_aborts
  - [+] test_a_bundle_without_a_declared_package_list_aborts
  - [+] test_install_downloads_exactly_what_the_manifest_named

**tests.test_packages.TestPackagedRegistryBundleShape**

  - [+] test_arm_fallback_declares_its_packages_and_no_pinned_urls

**tests.test_packages.TestSinglePackageRouteReportsBothVersions**

  - [+] test_an_apt_package_reports_its_installed_version
  - [+] test_a_script_package_reads_its_version_file
  - [+] test_the_vendor_answer_overrides_apt_without_losing_the_installed_side

**tests.test_packages.TestABrokenAptCacheIsNotAVerdict**

  - [+] test_a_failed_batch_reports_unknown_not_unsupported

**tests.test_packages.TestArchitectureIndependentRepository**

  - [+] test_all_is_kept_and_the_all_index_is_read

**tests.test_packages.TestCompressedIndexFallsBackWhenItIsNotGzip**

  - [+] test_a_bad_gzip_falls_through_to_the_plain_index

**tests.test_packages.TestBundleManifestIsReadOnce**

  - [+] test_install_does_not_fetch_the_manifest_twice

**tests.test_packages.TestAptListsAreRefreshedBeforeBeingRead**

  - [+] test_fresh_lists_are_left_alone
  - [+] test_stale_lists_are_refreshed
  - [+] test_the_invocation_matches_what_sudoers_grants
  - [+] test_a_box_with_no_lists_at_all_refreshes
  - [+] test_a_hung_mirror_does_not_hold_the_caller (0.06s)
  - [+] test_one_broken_source_does_not_abandon_the_check
  - [+] test_an_explicit_check_refreshes_first
  - [+] test_a_plain_listing_does_not_refresh

**tests.test_packages.TestTheCheckRepeats**

  - [+] test_the_cycle_runs_again

**tests.test_packages.TestAnUpdateIsAnnouncedOnce**

  - [+] test_the_same_news_is_not_repeated
  - [+] test_a_newer_version_is_announced_again
  - [+] test_installing_it_lets_a_later_one_be_announced

**tests.test_packages.TestOversizedIndexIsNotReadAsTruncated**

  - [+] test_a_body_past_the_cap_is_refused_rather_than_truncated

**tests.test_packages.TestRepoLineNamesTheComponentThePackageIsIn**

  - [+] test_the_source_line_uses_the_component_found

**tests.test_packages.TestBundleDryRunInstallsNothing**

  - [+] test_dry_run_only_probes
  - [+] test_dry_run_reports_an_unreachable_file

**tests.test_packages.TestTheCycleSurvivesAFailedPass**

  - [+] test_a_raising_pass_does_not_stop_the_loop

**tests.test_packages.TestDiskSpaceIsCheckedBeforeDownloading**

  - [+] test_enough_room_passes
  - [+] test_too_little_room_refuses_with_the_numbers
  - [+] test_an_unmeasurable_filesystem_does_not_invent_a_refusal
  - [+] test_an_unknown_size_is_not_a_refusal

**tests.test_packages.TestABrokenThirdPartySourceDoesNotBlockAnInstall**

  - [+] test_install_continues_after_a_failed_list_refresh
  - [+] test_the_refresh_uses_the_granted_invocation

**tests.test_packages.TestAnUpgradeKeepsTheConfigurationAlreadyThere**

  - [+] test_apt_repo_install_and_update_keep_it
  - [+] test_a_single_deb_keeps_it
  - [+] test_the_bundle_keeps_it

**tests.test_packages.TestOnlyOneAptRefreshAtATime**

  - [+] test_concurrent_callers_share_one_run (0.06s)

**tests.test_packages.TestAnUnknownVerdictIsEventuallyRetried**

  - [+] test_a_full_reprobe_is_triggered
  - [+] test_a_clean_box_pays_nothing

**tests.test_packages.TestAFailedNotificationIsNotRememberedAsSent**

  - [+] test_a_failed_push_is_retried_next_pass

**tests.test_packages.TestAnUnverifiableConflictIsNotAGreenLight**

  - [+] test_systemd_silence_marks_it_unknown

**tests.test_packages.TestABrokenAptCacheIsNeverAVerdict**

  - [+] test_an_empty_error_is_read_as_could_not_ask

**tests.test_packages.TestASystemFileNotOwnedByRootIsRewritten**

  - [+] test_a_service_user_owned_file_counts_as_not_placed
  - [+] test_a_root_owned_file_is_left_alone
  - [+] test_a_missing_file_must_be_placed

**tests.test_packages.TestRequiredPackagesCannotBeUninstalled**

  - [+] test_a_required_package_is_refused
  - [+] test_the_refusal_names_the_way_out
  - [+] test_the_flag_decides_and_not_the_package_id
  - [+] test_a_package_without_the_flag_is_still_removable

**tests.test_performance.TestPerformance**

  - [+] test_cpu_info_route (0.05s)
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
  - [+] test_no_renderer_step_when_no_active_service (0.01s)
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
  - [+] test_a_routing_handle_is_never_offered_as_a_source[upnp_renderer]
  - [+] test_a_routing_handle_is_never_offered_as_a_source[src_hqplayer]
  - [+] test_the_handle_decides_it_not_the_badge
  - [+] test_the_content_identity_survives_the_trip_to_sources
  - [+] test_a_real_source_stays_selectable

**tests.test_player.TestControlRouting**

  - [+] test_explicit_renderer_source_routed_to_now_playing (0.16s)
  - [+] test_stopped_renderer_still_controllable (0.16s)
  - [+] test_unknown_source_returns_false
  - [+] test_no_source_resolves_active (0.16s)

**tests.test_player.TestPlayer**

  - [+] test_snapshot (0.02s)
  - [+] test_control (0.02s)
  - [+] test_origins_returns_all_known_keys (0.02s)
  - [+] test_sleep_timer_get (0.02s)

**tests.test_player.TestGetOutputs**

  - [+] test_returns_mpd_and_renderer_outputs (0.02s)
  - [+] test_local_active_true_when_no_renderer (0.02s)
  - [+] test_local_active_false_when_renderer_reachable (0.02s)
  - [+] test_local_active_true_when_renderer_not_reachable (0.03s)

**tests.test_player.TestSelectMpdOutput**

  - [+] test_switch_succeeds (0.03s)
  - [+] test_unknown_output_id_returns_404 (0.03s)
  - [+] test_refused_enable_is_a_503_not_success (0.02s)
  - [+] test_stale_active_udn_cleared_not_raised (0.02s)
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
  - [+] test_a_paused_local_source_also_holds_the_active_spot (0.01s)
  - [+] test_queue_next_populated_from_renderer_queue

**tests.test_player.TestDsdRekeyOnDriver**

  - [+] test_rebadged_cast_item_never_volume_forced
  - [+] test_dsd_start_on_cast_skips_software_forcing

**tests.test_player.TestOutputErrorSurfacing**

  - [+] test_busy_dac_error_lands_on_the_local_output
  - [+] test_no_error_in_the_normal_case
  - [+] test_error_from_a_non_local_item_is_ignored
  - [+] test_a_failed_hqplayer_push_is_explained_with_no_item_left
  - [+] test_an_engine_error_still_wins_over_the_hqplayer_verdict
  - [+] test_an_unreachable_speaker_says_so_instead_of_going_quiet
  - [+] test_the_local_chain_is_always_reachable
  - [+] test_state_changed_detects_an_appearing_output_error

**tests.test_player.TestIdleStateKeepsTheRendererControllable**

  - [+] test_handle_is_derived_from_outputs_after_a_core_restart
  - [+] test_handle_is_derived_after_another_source_played
  - [+] test_no_handle_when_the_local_output_is_the_active_one
  - [+] test_the_selected_output_still_shows_its_name_while_idle

**tests.test_player.TestDsdFastLockVerdict**

  - [+] test_confirmed_setvol_stays_quiet
  - [+] test_refused_setvol_is_logged_and_keeps_the_restore_target
  - [+] test_non_dsd_track_sends_no_setvol

**tests.test_player.TestControlPublishesTruth**

  - [+] test_refused_control_still_publishes

**tests.test_player.TestDsdForceRefusalLogged**

  - [+] test_refused_force_is_logged

**tests.test_player.TestNoStaleStateWins**

  - [+] test_control_publish_stamps_the_read_instant (0.15s)
  - [+] test_a_snapshot_read_before_that_instant_is_dropped (0.06s)
  - [+] test_a_fresh_snapshot_still_publishes (0.06s)

**tests.test_player.TestOverlappingControlPublishes**

  - [+] test_a_slower_earlier_control_does_not_publish_last (0.15s)
  - [+] test_it_never_moves_the_watermark_backwards (0.15s)
  - [+] test_a_fresh_control_publishes_and_raises_the_watermark (0.16s)

**tests.test_player.TestEveryPublisherIsGuarded**

  - [+] test_no_publish_site_is_left_unguarded
  - [+] test_every_guarded_site_raises_the_watermark_with_max

**tests.test_player.TestDsdRestoreSurvivesAStoppedPlayer**

  - [+] test_the_level_comes_back_even_with_nothing_playing
  - [+] test_the_other_sources_come_back_too
  - [+] test_the_hardware_level_is_restored_as_well
  - [+] test_the_memory_is_cleared_only_after_the_attempt
  - [+] test_hqplayer_keeps_its_own_level
  - [+] test_one_source_failing_does_not_strand_the_others

**tests.test_player.TestDsdEndNeedsProof**

  - [+] test_a_real_reading_of_playback_is_proof_enough
  - [+] test_an_empty_reading_asks_mpd
  - [+] test_mpd_still_on_a_dsd_file_is_not_over
  - [+] test_an_unreachable_mpd_is_unknown_not_over
  - [+] test_no_mpd_at_all_does_not_strand_the_levels
  - [+] test_without_proof_nothing_is_written_and_nothing_is_forgotten
  - [+] test_a_renderer_is_never_written_back

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
  - [+] test_mpd_multi_output_config_from_detected_hardware
  - [+] test_provision_writes_alsa_index_pin_for_usb_dac
  - [+] test_provision_no_pin_for_non_usb_output
  - [+] test_provision_respects_existing_user_pin
  - [+] test_user_pins_usb_device_matches_hex_forms
  - [+] test_overwrites_when_exists
  - [+] test_regenerate_backups_then_overwrites
  - [+] test_provision_mpd_without_library_is_allowed
  - [+] test_regenerate_mpd_reuses_existing_library
  - [+] test_regenerate_mpd_without_existing_config_generates_libraryless
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
  - [+] test_discover_library_sources_usb_and_network
  - [+] test_status_includes_library_sources
  - [+] test_status_reports_outputs_and_config_state
  - [+] test_status_reports_the_device_each_config_actually_names
  - [+] test_a_pin_still_resolves_when_the_card_was_renamed
  - [+] test_a_multi_output_mpd_conf_reports_the_output_mpd_has_enabled
  - [+] test_status_never_claims_agreement_it_could_not_check
  - [+] test_patch_output_retargets_device_and_pins (0.01s)
  - [+] test_patch_output_rejects_service_without_output
  - [+] test_patch_output_raises_when_output_absent
  - [+] test_patch_library_changes_music_directory_only
  - [+] test_patch_library_with_usb_uuid_mounts
  - [+] test_patch_library_with_no_path_detaches_the_library
  - [+] test_patch_library_adds_the_directive_when_there_is_none
  - [+] test_detaching_does_not_ask_mpd_to_rescan
  - [+] test_provision_rejects_music_dir_with_quote
  - [+] test_patch_library_rejects_music_dir_with_quote
  - [+] test_patch_output_mpd_uses_native_enable
  - [+] test_patch_output_mpd_falls_back_to_restart
  - [+] test_patch_library_triggers_mpd_rescan (0.01s)
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

**tests.test_provisioning.TestNoLibraryIsAllowed**

  - [+] test_provisioning_succeeds_with_no_library_at_all
  - [+] test_the_generated_mpd_config_omits_the_directive
  - [+] test_regenerating_a_box_that_had_none_keeps_having_none
  - [+] test_regenerating_still_reuses_a_library_that_was_set

**tests.test_provisioning.TestAWrongLibraryIsRefused**

  - [+] test_a_bad_path_is_refused_with_a_readable_reason[relative/path-must be absolute]
  - [+] test_a_bad_path_is_refused_with_a_readable_reason[/does/not/exist/anywhere-does not exist]
  - [+] test_a_bad_path_is_refused_with_a_readable_reason[/tmp/with"quote-double-quote]
  - [+] test_a_file_is_not_a_library
  - [+] test_a_directory_mpd_cannot_read_is_refused
  - [+] test_an_undetermined_permission_does_not_block

**tests.test_provisioning.TestFoundByCodeReview**

  - [+] test_provisioning_without_a_library_keeps_the_one_already_set
  - [+] test_a_path_with_a_backslash_is_applied_literally
  - [+] test_both_branches_agree_on_a_backslash_path
  - [+] test_a_bad_path_is_refused_before_anything_is_applied
  - [+] test_a_bare_unit_name_still_reaches_the_readability_check

**tests.test_provisioning.TestFoundBySecondCodeReview**

  - [+] test_choosing_no_library_removes_the_one_already_there
  - [+] test_saying_nothing_still_keeps_the_library
  - [+] test_a_reused_library_is_not_re_checked
  - [+] test_a_padded_path_is_stripped_before_both_checks
  - [+] test_the_path_is_ignored_when_a_usb_drive_is_named
  - [+] test_the_filesystem_probes_do_not_block_the_event_loop (0.31s)
  - [+] test_the_groups_the_unit_grants_are_taken_into_account

**tests.test_provisioning.TestDefaultFriendlyName**

  - [+] test_format_is_audiogravity_dash_short_token
  - [+] test_token_comes_from_the_device_fingerprint
  - [+] test_falls_back_when_fingerprint_unavailable

**tests.test_push.TestVapidKey**

  - [+] test_get_key (0.01s)

**tests.test_push.TestSubscribe**

  - [+] test_subscribe (0.01s)

**tests.test_push.TestUnsubscribe**

  - [+] test_unsubscribe (0.01s)

**tests.test_push.TestGenerateVapidKeysScript**

  - [+] test_script_produces_valid_keys (0.10s)

**tests.test_push.TestRegisterLoadsVapidJson**

  - [+] test_register_initializes_service_from_json
  - [+] test_register_without_keys_does_not_initialize (0.01s)

**tests.test_push.TestPushEndpointValidation**

  - [+] test_http_endpoint_rejected
  - [+] test_empty_endpoint_rejected
  - [+] test_https_endpoint_accepted

**tests.test_push.TestPushWebpushTimeout**

  - [+] test_webpush_called_with_timeout

**tests.test_push.TestPushUnsubscribeQueryParam**

  - [+] test_endpoint_is_query_param (0.02s)

**tests.test_push.TestServiceDownPushHook**

  - [+] test_transition_active_to_failed_detected
  - [+] test_no_alert_on_first_appearance_as_failed
  - [+] test_no_alert_on_active_to_active
  - [+] test_stale_state_pruned_when_service_disappears
  - [+] test_no_false_positive_after_prune_and_reappearance
  - [+] test_label_uses_systemd_unit_name
  - [+] test_label_fallback_to_service_id (0.02s)

**tests.test_push.TestPush410Pruning**

  - [+] test_410_prunes_once (0.02s)
  - [+] test_non_410_error_with_410_in_text_is_kept (0.01s)
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
  - [+] test_delete_connection (0.01s)
  - [+] test_get_connection_after_disconnect (0.01s)
  - [+] test_stream_redirect_mode_returns_302_to_cdn (0.01s)
  - [+] test_oauth_callback_no_code (0.01s)
  - [+] test_oauth_callback_with_code (0.02s)
  - [+] test_oauth_callback_failure (0.01s)
  - [+] test_post_connection_starts_oauth (0.01s)

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

  - [+] test_handle_callback_returns_false_when_no_secret (0.01s)
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

  - [+] test_reads_every_bucket_from_one_request

**tests.test_qobuz_library.TestQobuzLibraryRouter**

  - [+] test_shelves (0.15s)
  - [+] test_genres (0.14s)
  - [+] test_genre_grid (0.14s)
  - [+] test_genre_requires_a_path (0.13s)
  - [+] test_purchases (0.30s)
  - [+] test_playlists_default_to_the_editorial_tree (0.13s)
  - [+] test_playlists_can_ask_for_the_account_tree (0.15s)
  - [+] test_playlists_refuse_an_unknown_tree (0.13s)
  - [+] test_featured_albums (0.14s)
  - [+] test_featured_albums_default_type (0.13s)
  - [+] test_playlists (0.14s)
  - [+] test_playlist_tracks (0.16s)
  - [+] test_playlist_tracks_missing_id (0.13s)
  - [+] test_featured_service_error (0.16s)

**tests.test_qobuz_library.TestQobuzQueueHelper**

  - [+] test_adds_tracks_as_stable_redirect_proxy_urls
  - [+] test_play_action_triggers_playid
  - [+] test_persists_metadata_as_durable_mpd_tags

**tests.test_qobuz_library.TestQobuzQueueSingleTrack**

  - [+] test_single_track_persists_durable_tags

**tests.test_qobuz_library.TestQobuzGetRetry**

  - [+] test_success_no_relogin
  - [+] test_401_relogins_then_succeeds
  - [+] test_401_relogin_fails_raises_session_expired
  - [+] test_401_after_relogin_raises_rotated
  - [+] test_not_connected_raises

**tests.test_qobuz_library.TestQobuzShelves**

  - [+] test_lists_nine_shelves_as_categories
  - [+] test_excludes_the_six_measured_out
  - [+] test_titles_are_unique_and_labels_filled

**tests.test_qobuz_library.TestQobuzFeaturedGenreFilter**

  - [+] test_sends_genre_ids_when_given
  - [+] test_omits_genre_ids_when_empty

**tests.test_qobuz_library.TestQobuzPlaylistTrees**

  - [+] test_editorial_asks_the_featured_endpoint
  - [+] test_mine_asks_the_user_endpoint
  - [+] test_unknown_kind_reads_as_editorial

**tests.test_qobuz_library.TestQobuzPurchases**

  - [+] test_lists_bought_albums_only
  - [+] test_id_carries_no_marker
  - [+] test_no_purchases_is_an_empty_list

**tests.test_qobuz_library.TestQobuzGenres**

  - [+] test_builds_a_two_level_tree
  - [+] test_path_is_the_opaque_id_not_a_title_path
  - [+] test_sub_genres_are_alphabetical
  - [+] test_a_genre_without_sub_genres_is_kept
  - [+] test_one_request_per_genre_plus_one
  - [+] test_tree_is_memoised
  - [+] test_empty_top_level_is_not_memoised
  - [+] test_a_failed_child_request_keeps_its_genre

**tests.test_qobuz_library.TestQobuzGenreGrid**

  - [+] test_browses_the_selection_shelf_narrowed_to_the_genre
  - [+] test_unknown_path_yields_an_empty_list

**tests.test_qobuz_library.TestQobuzAlbumMapper**

  - [+] test_reads_the_year_from_the_original_release_date
  - [+] test_survives_a_missing_or_unparsable_date
  - [+] test_drops_a_row_without_id_or_title

**tests.test_qobuz_library.TestQobuzNullShapes**

  - [+] test_a_null_bucket_is_an_empty_shelf
  - [+] test_a_playlist_with_a_null_name_is_dropped_not_raised
  - [+] test_a_track_with_a_null_album_keeps_its_playlist
  - [+] test_a_year_that_int_refuses_costs_no_shelf

**tests.test_qobuz_library.TestQobuzGenreTreeResilience**

  - [+] test_a_child_answering_a_null_bucket_does_not_lose_the_tree
  - [+] test_a_partial_tree_is_served_but_not_memoised
  - [+] test_concurrent_first_visits_load_the_tree_once
  - [+] test_at_most_three_child_requests_run_together

**tests.test_qobuz_library.TestQobuzUnknownShelf**

  - [+] test_an_unlisted_shelf_is_refused_before_the_request
  - [+] test_the_genre_shelf_is_one_of_the_published_shelves
  - [+] test_the_route_answers_400_not_503 (0.14s)
  - [+] test_shelves_report_a_disconnected_account_like_every_sibling (0.14s)

**tests.test_qobuz_library.TestTitleSortKey**

  - [+] test_accented_titles_sort_where_a_reader_looks_for_them
  - [+] test_an_accent_no_longer_lands_after_every_plain_letter
  - [+] test_it_still_ignores_case_as_it_did
  - [+] test_letters_unicode_will_not_decompose_are_mapped_by_hand
  - [+] test_the_sharp_s_needs_no_mapping_and_has_none
  - [+] test_a_ligature_or_a_typographic_form_sorts_with_its_letters
  - [+] test_a_non_latin_title_keeps_its_characters
  - [+] test_it_reads_a_title_or_a_name_or_neither

**tests.test_radio.TestRadio**

  - [+] test_search_route (0.04s)
  - [+] test_library_route (0.03s)
  - [+] test_favorites_route (0.03s)

**tests.test_radio.TestRadioEditStation**

  - [+] test_edit_station_returns_updated_station (0.04s)
  - [+] test_edit_station_404_when_not_saved (0.03s)

**tests.test_radio.TestRadioSavedStationDatetime**

  - [+] test_added_at_is_timezone_aware

**tests.test_radio.TestRadioResolveRobustness**

  - [+] test_resolve_falls_back_to_saved_on_rbi_failure
  - [+] test_resolve_returns_none_when_the_catalogue_does_not_know_it
  - [+] test_resolve_reports_an_unreachable_catalogue_instead_of_not_found
  - [+] test_a_saved_station_still_wins_over_an_unreachable_catalogue

**tests.test_radio.TestRadioApplyEntryUpdate**

  - [+] test_update_clears_flag
  - [+] test_update_pops_when_both_flags_cleared
  - [+] test_remove_from_library_uses_apply_entry_update
  - [+] test_remove_from_library_returns_false_when_not_in_library
  - [+] test_remove_favorite_keeps_entry_if_still_in_library

**tests.test_radio.TestRadioPlayRendererRouting**

  - [+] test_play_routes_to_renderer_when_active
  - [+] test_play_cover_token_none_when_no_favicon
  - [+] test_play_uses_mpd_when_the_routing_says_local
  - [+] test_play_relays_mpds_refusal
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

  - [+] test_station_is_pushed_to_hqplayer_when_it_is_the_output
  - [+] test_hqplayer_push_carries_the_radio_identity
  - [+] test_hqplayer_push_never_touches_mpd
  - [+] test_local_output_still_goes_to_mpd
  - [+] test_routing_refusal_propagates

**tests.test_radio.TestRadioHqplayerFailureIsNotA500**

  - [+] test_a_busy_dac_surfaces_as_a_routing_refusal
  - [+] test_the_original_cause_is_kept_as_the_chained_error

**tests.test_radio.TestRadioConfirmWindow**

  - [+] test_a_station_gets_the_remote_confirmation_window
  - [+] test_a_remote_stream_gets_more_room_than_a_local_file

**tests.test_radio.TestRadioCodecGate**

  - [+] test_an_aac_station_is_refused_with_its_own_status
  - [+] test_the_station_codec_is_forwarded_to_the_guard
  - [+] test_an_mp3_station_goes_through (0.01s)
  - [+] test_an_unknown_codec_is_still_attempted

**tests.test_radio.TestRadioCatalogueBackoff**

  - [+] test_stops_after_two_attempts_and_spaces_them
  - [+] test_server_error_message_is_written_for_a_listener
  - [+] test_a_server_error_does_not_silence_later_searches
  - [+] test_429_stops_immediately_and_sends_nothing_afterwards
  - [+] test_retry_after_defaults_and_is_capped
  - [+] test_second_mirror_answers_after_the_first_fails

**tests.test_radio.TestRadioMirrorDiscovery**

  - [+] test_a_single_mirror_is_tried_once_not_retried
  - [+] test_distinct_mirrors_still_get_a_failover

**tests.test_radio.TestRadioDnsDiscovery**

  - [+] test_one_machine_on_two_ip_families_is_one_server
  - [+] test_address_without_reverse_dns_is_dropped
  - [+] test_dns_failure_keeps_the_fallback_server
  - [+] test_empty_dns_answer_does_not_wipe_the_server_list

**tests.test_radio.TestRadioStaleSearchFallback**

  - [+] test_serves_the_previous_answer_when_the_catalogue_is_down
  - [+] test_a_search_never_run_before_still_reports_the_failure

**tests.test_radio.TestRadioPlayReporting**

  - [+] test_reports_a_catalogue_station
  - [+] test_never_reports_a_hand_entered_station
  - [+] test_setting_off_keeps_every_play_on_the_box
  - [+] test_a_failing_report_never_reaches_the_caller

**tests.test_radio.TestRadioReviewFixes**

  - [+] test_a_rate_limited_play_report_never_silences_search
  - [+] test_a_cooldown_still_stops_the_optional_call_too
  - [+] test_a_refusal_from_the_only_server_is_asked_once
  - [+] test_a_silent_failure_from_the_only_server_is_asked_again
  - [+] test_a_reverse_lookup_outside_the_catalogue_domain_is_refused
  - [+] test_a_wrong_reverse_lookup_leaves_the_working_server_in_place
  - [+] test_discovery_gives_up_rather_than_hanging_startup (5.01s)
  - [+] test_shutdown_cancels_the_play_reports_still_in_flight
  - [+] test_a_search_older_than_the_bound_is_not_served_as_current
  - [+] test_a_play_that_never_started_is_not_reported
  - [+] test_a_play_that_started_is_reported

**tests.test_radio.TestStaleSearchStaysPlayable**

  - [+] test_a_station_from_a_stale_result_can_still_be_resolved
  - [+] test_a_station_never_seen_still_reports_the_outage

**tests.test_radio.TestReportBackoff**

  - [+] test_a_rate_limited_report_stops_the_next_reports

**tests.test_radio.TestReverseDnsCaseFolding**

  - [+] test_a_mixed_case_ptr_is_accepted
  - [+] test_a_foreign_domain_is_still_refused_whatever_its_case

**tests.test_radio.TestStoppedMpdOnTheRadioPath**

  - [+] test_playing_a_station_says_MPD_is_not_running (0.04s)

**tests.test_readable_by_user.TestUnknownsAreNotRefusals**

  - [+] test_an_unknown_account_gives_no_answer
  - [+] test_a_missing_directory_gives_no_answer

**tests.test_readable_by_user.TestPermissionBits**

  - [+] test_a_directory_the_account_owns_is_readable
  - [+] test_a_directory_closed_to_others_is_refused
  - [+] test_read_alone_is_not_enough_without_traversal
  - [+] test_an_ancestor_that_cannot_be_traversed_refuses_the_leaf
  - [+] test_a_world_readable_directory_is_readable_by_anyone

**tests.test_readable_by_user**

  - [+] test_root_reads_everything

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

**tests.test_resource_fences**

  - [+] test_cpu_weight_yields_to_mpd_without_starving_the_transcoder
  - [+] test_memory_high_throttles_before_the_box_feels_it
  - [+] test_memory_max_is_a_backstop_not_a_ceiling_it_can_reach
  - [+] test_io_weight_is_absent_on_purpose

**tests.test_roon_client.TestWhichCoreWeTalkTo**

  - [+] test_no_configured_address_still_finds_a_core
  - [+] test_an_address_that_answers_skips_the_lookup
  - [+] test_an_address_that_does_not_answer_falls_through
  - [+] test_nothing_anywhere_is_not_an_error

**tests.test_roon_client.TestTheOwnerIsToldWhatToDo**

  - [+] test_the_port_is_roons_own
  - [+] test_no_port_can_be_passed_in
  - [+] test_waiting_for_authorization_is_not_a_fault
  - [+] test_a_timeout_with_a_token_still_warns

**tests.test_roon_client.TestWhenRoonEngagesAtAll**

  - [+] test_no_endpoint_no_connection[stopped]
  - [+] test_no_endpoint_no_connection[not-installed]
  - [+] test_the_retired_keys_stay_retired[roon_enabled]
  - [+] test_the_retired_keys_stay_retired[roon_core_port]
  - [+] test_the_retired_keys_stay_retired[roon_app_name]
  - [+] test_the_extension_name_is_fixed
  - [+] test_either_endpoint_opens_the_door[bridge]
  - [+] test_either_endpoint_opens_the_door[server]

**tests.test_roon_client.TestARetryIsStillPossible**

  - [+] test_the_caller_never_waits_for_the_retry
  - [+] test_a_disconnected_client_is_retried_once_the_cooldown_passes (0.03s)
  - [+] test_a_connected_client_is_left_alone

**tests.test_roon_client.TestTheAttemptIsBounded**

  - [+] test_a_stuck_attempt_is_not_joined_by_another (0.01s)
  - [+] test_a_hung_attempt_ends_at_the_ceiling_and_frees_the_guard (0.06s)
  - [+] test_a_finished_attempt_lets_the_next_one_run (0.03s)

**tests.test_roon_client.TestTheRetryBacksOff**

  - [+] test_the_cooldown_doubles_while_nothing_answers_and_caps (0.07s)
  - [+] test_waiting_for_the_owner_keeps_the_base_cadence (0.01s)

**tests.test_roon_client.TestOnlyOneClientIsEverBuilt**

  - [+] test_concurrent_callers_share_one_client (0.03s)

**tests.test_roon_client.TestWhatTheInterfaceIsTold**

  - [+] test_a_box_without_roon_says_so
  - [+] test_waiting_names_the_extension_to_enable
  - [+] test_connected_counts_the_zones
  - [+] test_zones_are_not_counted_before_there_is_a_session
  - [+] test_a_dead_session_is_corrected_and_reported_aloud
  - [+] test_a_human_looking_resets_the_backoff
  - [+] test_the_card_is_not_made_to_wait_for_the_first_attempt
  - [+] test_a_client_that_could_not_be_built_says_nothing_more
  - [+] test_a_live_session_that_answers_badly_is_still_live

**tests.test_roon_client.TestAStateIsAlwaysSet**

  - [+] test_an_unexpected_failure_clears_the_previous_state
  - [+] test_disconnecting_stops_claiming_a_session
  - [+] test_disconnecting_cancels_the_attempt_in_flight

**tests.test_roon_client.TestTheJournalDoesNotRepeatItself**

  - [+] test_an_unreachable_core_is_reported_once
  - [+] test_a_core_that_moved_is_named_again
  - [+] test_it_speaks_again_after_a_recovery

**tests.test_roon_client.TestTheHandshakeThreadIsBounded**

  - [+] test_a_stuck_handshake_refuses_a_second_thread (0.06s)

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
  - [+] test_dangerous_args_are_not_passed_to_the_root_wrapper
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

  - [+] test_get_service (0.05s)

**tests.test_services.TestServiceActions**

  - [+] test_restart_service (0.04s)
  - [+] test_stop_service (0.04s)
  - [+] test_start_service (0.04s)

**tests.test_services.TestServiceNameValidation**

  - [+] test_valid_name_accepted (0.04s)
  - [+] test_semicolon_rejected (0.04s)
  - [+] test_slash_rejected (0.04s)
  - [+] test_ampersand_rejected (0.26s)

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
  - [+] test_the_three_units_that_never_existed_stay_out
  - [+] test_perform_action_rejects_unmanaged_unit
  - [+] test_update_properties_rejects_unmanaged_unit

**tests.test_services.TestWhenTheKernelCountsNoMemory**

  - [+] test_the_controller_is_seen_when_the_kernel_exposes_it
  - [+] test_its_absence_is_seen_too
  - [+] test_a_kernel_it_cannot_question_is_not_accused
  - [+] test_it_is_read_once_and_kept

**tests.test_services.TestWhatAStoppedServiceReports**

  - [+] test_a_stopped_service_reports_zero
  - [+] test_a_running_service_with_no_measurement_reports_nothing
  - [+] test_a_running_service_that_is_measured_reports_its_figures

**tests.test_ssdp.TestMessage**

  - [+] test_carries_the_requested_search_target
  - [+] test_unicast_message_is_addressed_to_that_host

**tests.test_ssdp.TestMsearch**

  - [+] test_collects_location_headers_without_duplicates (0.06s)
  - [+] test_sends_one_datagram_per_unicast_host_plus_the_multicast_one (0.06s)
  - [+] test_a_refused_unicast_host_does_not_stop_the_search (0.06s)
  - [+] test_a_socket_error_yields_an_empty_list_rather_than_raising
  - [+] test_a_silent_network_is_not_an_error (0.06s)

**tests.test_ssdp.TestErrorLevel**

  - [+] test_a_socket_error_is_a_warning_by_default
  - [+] test_a_caller_can_lower_it

**tests.test_ssdp.TestMulticastFailureDoesNotCancelUnicast**

  - [+] test_unicast_probes_still_go_out (0.06s)
  - [+] test_nothing_sent_means_no_pointless_wait

**tests.test_sse_channels**

  - [+] test_allowlist_covers_every_published_channel (0.01s)
  - [+] test_unknown_channel_is_refused (0.01s)
  - [+] test_refusal_names_the_valid_channels (0.01s)
  - [+] test_sysinfo_is_refused_because_it_is_an_event_not_a_channel (0.01s)
  - [+] test_every_known_channel_passes_the_guard (0.02s)

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
  - [+] test_mpd_native_error_reports_failure_no_fallback
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

**tests.test_stream_hqplayer.TestStreamQueueHqplayer**

  - [+] test_every_track_is_pushed_in_order
  - [+] test_every_track_carries_its_own_metadata (0.01s)
  - [+] test_a_lookup_token_is_not_passed_as_a_cover_url (0.02s)
  - [+] test_no_duration_is_pushed
  - [+] test_the_action_travels_so_an_append_stays_an_append
  - [+] test_nothing_resolved_is_refused_before_the_push
  - [+] test_a_lazily_resolved_entry_is_refused

**tests.test_stream_hqplayer.TestPushedUrls**

  - [+] test_qobuz_pushes_redirecting_lan_urls
  - [+] test_highresaudio_pushes_redirecting_lan_urls
  - [+] test_tidal_stays_pass_through

**tests.test_stream_hqplayer.TestTidalCodecIsTheOneActuallyServed**

  - [+] test_a_lossless_tier_serving_aac_is_still_refused
  - [+] test_the_message_names_a_remedy_that_can_actually_work
  - [+] test_one_manifest_is_fetched_for_a_whole_album
  - [+] test_the_album_is_resolved_once_not_twice
  - [+] test_an_unreadable_manifest_falls_back_to_the_tier
  - [+] test_an_unreadable_manifest_on_a_lossy_tier_still_refuses
  - [+] test_a_playlist_is_not_judged_on_its_first_track
  - [+] test_a_lossy_tier_still_refuses_a_playlist
  - [+] test_rotated_credentials_are_not_reported_as_a_format_problem

**tests.test_stream_hqplayer.TestQueueRouteDispatch**

  - [+] test_a_qobuz_item_goes_to_its_own_service (0.34s)
  - [+] test_a_media_server_item_goes_to_the_upnp_path (0.13s)
  - [+] test_the_local_library_still_resolves_through_mpd (0.14s)

**tests.test_stream_meta.TestBuildStreamMeta**

  - [+] test_keeps_the_known_keys_and_only_those
  - [+] test_empty_and_whitespace_text_becomes_none
  - [+] test_track_number_is_stored_as_str
  - [+] test_duration_normalisation[183-183.0]
  - [+] test_duration_normalisation[90.221-90.221]
  - [+] test_duration_normalisation[0-None]
  - [+] test_duration_normalisation[-5-None]
  - [+] test_duration_normalisation[inf-None]
  - [+] test_duration_normalisation[nan-None]
  - [+] test_duration_normalisation[live-None]
  - [+] test_duration_normalisation[None-None]
  - [+] test_duration_normalisation[True-None]
  - [+] test_duration_normalisation[False-None]

**tests.test_stream_meta.TestPersistence**

  - [+] test_round_trip_survives_a_simulated_restart
  - [+] test_first_write_after_restart_does_not_discard_prior_entries
  - [+] test_corrupt_file_starts_empty_without_crashing
  - [+] test_valid_json_that_is_not_a_dict_starts_empty[[]]
  - [+] test_valid_json_that_is_not_a_dict_starts_empty[null]
  - [+] test_valid_json_that_is_not_a_dict_starts_empty["x"]
  - [+] test_valid_json_that_is_not_a_dict_starts_empty[3]
  - [+] test_unknown_version_is_ignored
  - [+] test_loaded_values_are_sanitized_not_trusted
  - [+] test_load_caps_at_the_registry_bound_keeping_newest
  - [+] test_transient_read_error_disables_writes_instead_of_clobbering
  - [+] test_write_failure_rearms_dirty_and_warns
  - [+] test_identical_reregister_schedules_no_write
  - [+] test_flush_is_debounced_inside_an_event_loop (0.06s)
  - [+] test_stale_timer_from_a_dead_loop_does_not_block_future_flushes (0.06s)
  - [+] test_shutdown_flush_rescues_a_burst_still_in_the_debounce_window
  - [+] test_shutdown_flush_writes_nothing_when_never_used
  - [+] test_shutdown_flush_writes_nothing_after_read_only_use

**tests.test_stream_meta.TestQueueDurationFallback**

  - [+] test_stream_without_mpd_duration_falls_back_to_registry
  - [+] test_zero_duration_from_mpd_counts_as_unknown
  - [+] test_mpd_known_duration_wins_over_the_registry
  - [+] test_upnp_play_registers_the_ui_sent_duration
  - [+] test_radio_stream_stays_without_duration

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

**tests.test_support_report**

  - [+] test_harmless_values_are_not_redacted[the account MPD runs as]
  - [+] test_harmless_values_are_not_redacted[the library path]
  - [+] test_harmless_values_are_not_redacted[a sticker file path]
  - [+] test_harmless_values_are_not_redacted[an XML flag ending in a digit]
  - [+] test_harmless_values_are_not_redacted[a word merely containing "key"]
  - [+] test_harmless_values_are_not_redacted[a friendly name containing a hash]
  - [+] test_harmless_values_are_not_redacted[a device with a trailing comment]
  - [+] test_harmless_values_are_not_redacted[a mixer type]
  - [+] test_xml_tag_stays_a_tag_when_its_attribute_is_redacted
  - [+] test_secret_never_reaches_the_report[mpd password directive]
  - [+] test_secret_never_reaches_the_report[mpd proxy password]
  - [+] test_secret_never_reaches_the_report[upmpdcli qobuz password]
  - [+] test_secret_never_reaches_the_report[upmpdcli hra password]
  - [+] test_secret_never_reaches_the_report[upmpdcli mpd password]
  - [+] test_secret_never_reaches_the_report[upmpdcli qobuz account (an email, not a password-looking key)]
  - [+] test_secret_never_reaches_the_report[shairport-sync password inside a block]
  - [+] test_secret_never_reaches_the_report[credentials embedded in a URL]
  - [+] test_secret_never_reaches_the_report[an unknown directive carrying a token]
  - [+] test_secret_never_reaches_the_report[a commented-out credential left behind by hand]
  - [+] test_secret_never_reaches_the_report[an XML attribute (HQPlayer networkaudiod)]
  - [+] test_secret_never_reaches_the_report[an XML attribute in single quotes]
  - [+] test_secret_never_reaches_the_report[an email inside an XML attribute]
  - [+] test_secret_never_reaches_the_report[a credential inside a multi-line XML comment]
  - [+] test_secret_never_reaches_the_report[a secret in a trailing comment on an innocent directive]
  - [+] test_secret_never_reaches_the_report[api_key as an XML attribute (redacted as a directive, published as an attribute)]
  - [+] test_secret_never_reaches_the_report[a bare key attribute]
  - [+] test_secret_never_reaches_the_report[an unquoted attribute value]
  - [+] test_secret_never_reaches_the_report[a colon separator]
  - [+] test_secret_never_reaches_the_serialized_report[mpd password directive]
  - [+] test_secret_never_reaches_the_serialized_report[mpd proxy password]
  - [+] test_secret_never_reaches_the_serialized_report[upmpdcli qobuz password]
  - [+] test_secret_never_reaches_the_serialized_report[upmpdcli hra password]
  - [+] test_secret_never_reaches_the_serialized_report[upmpdcli mpd password]
  - [+] test_secret_never_reaches_the_serialized_report[upmpdcli qobuz account (an email, not a password-looking key)]
  - [+] test_secret_never_reaches_the_serialized_report[shairport-sync password inside a block]
  - [+] test_secret_never_reaches_the_serialized_report[credentials embedded in a URL]
  - [+] test_secret_never_reaches_the_serialized_report[an unknown directive carrying a token]
  - [+] test_secret_never_reaches_the_serialized_report[a commented-out credential left behind by hand]
  - [+] test_secret_never_reaches_the_serialized_report[an XML attribute (HQPlayer networkaudiod)]
  - [+] test_secret_never_reaches_the_serialized_report[an XML attribute in single quotes]
  - [+] test_secret_never_reaches_the_serialized_report[an email inside an XML attribute]
  - [+] test_secret_never_reaches_the_serialized_report[a credential inside a multi-line XML comment]
  - [+] test_secret_never_reaches_the_serialized_report[a secret in a trailing comment on an innocent directive]
  - [+] test_secret_never_reaches_the_serialized_report[api_key as an XML attribute (redacted as a directive, published as an attribute)]
  - [+] test_secret_never_reaches_the_serialized_report[a bare key attribute]
  - [+] test_secret_never_reaches_the_serialized_report[an unquoted attribute value]
  - [+] test_secret_never_reaches_the_serialized_report[a colon separator]
  - [+] test_redacted_directive_keeps_its_name
  - [+] test_run_as_user_is_not_redacted
  - [+] test_comments_are_dropped_and_counted
  - [+] test_ag_marker_comment_is_kept
  - [+] test_hand_written_config_shows_no_marker
  - [+] test_xml_comments_are_dropped_across_lines
  - [+] test_xml_trailing_comment_does_not_ride_along
  - [+] test_xml_declaration_survives
  - [+] test_block_structure_survives
  - [+] test_directive_values_are_untouched_when_harmless
  - [+] test_counters_report_what_was_removed
  - [+] test_long_config_is_capped_and_says_so
  - [+] test_truncation_is_never_silent
  - [+] test_empty_config
  - [+] test_every_section_is_named_with_its_own_collector
  - [+] test_report_carries_every_declared_section
  - [+] test_a_failing_section_does_not_sink_the_report
  - [+] test_a_failing_section_leaves_the_others_intact
  - [+] test_every_section_keeps_its_own_name
  - [+] test_sections_are_collected_concurrently (0.06s)
  - [+] test_a_section_returning_nothing_is_still_reported
  - [+] test_report_version_is_2
  - [+] test_web_ui_probe_reads_the_served_certificate (0.05s)
  - [+] test_journal_lines_are_redacted
  - [+] test_journal_lines_come_out_ordered_and_folded

**tests.test_support_report.TestUiServerPorts**

  - [+] test_ports_are_read_from_the_effective_command_line
  - [+] test_equals_spelling_matches_too
  - [+] test_defaults_when_systemd_cannot_answer

**tests.test_support_report.TestCertificateSummary**

  - [+] test_identity_validity_and_san_coverage (0.05s)
  - [+] test_the_issue_date_travels_with_the_summary (0.05s)
  - [+] test_a_box_that_changed_address_is_flagged (0.22s)
  - [+] test_unknown_lan_ip_reports_null_not_false (0.06s)

**tests.test_support_report.TestTcpProbe**

  - [+] test_reachable_with_latency
  - [+] test_unreachable_never_raises

**tests.test_support_report.TestEnvSanity**

  - [+] test_missing_and_unknown_keys_names_only
  - [+] test_absent_env_file_is_reported_not_raised
  - [+] test_world_readable_env_is_flagged

**tests.test_support_report.TestAvPeers**

  - [+] test_peers_are_collected_and_shaped
  - [+] test_a_failed_scan_degrades_inside_the_section
  - [+] test_media_server_search_target_is_the_shared_constant

**tests.test_support_report.TestCpuRanges**

  - [+] test_ranges_are_compressed

**tests.test_support_report.TestParseKv**

  - [+] test_parses_show_style_output

**tests.test_support_report.TestRunBounded**

  - [+] test_success_returns_stdout
  - [+] test_timeout_kills_and_reaps (0.22s)
  - [+] test_missing_binary_is_an_answer_not_a_raise (0.02s)

**tests.test_support_report.TestCollectStorage**

  - [+] test_groups_paths_by_mountpoint_with_ro_flag (0.04s)

**tests.test_support_report.TestCollectAudioTuning**

  - [+] test_configured_values_named_and_sentinels_dropped
  - [+] test_a_unit_that_does_not_exist_reports_no_tuning (0.02s)
  - [+] test_a_loaded_unit_is_reported_in_full (0.01s)
  - [+] test_named_policies_pass_through_on_newer_systemd (0.01s)

**tests.test_support_report.TestCollectNetwork**

  - [+] test_gateway_clock_and_probes_from_canned_output

**tests.test_support_report.TestCollectSelfUpdate**

  - [+] test_accessible_repo_carries_the_latest_version
  - [+] test_404_is_no_access_but_403_stays_inconclusive (0.02s)

**tests.test_support_report.TestMpdStats**

  - [+] test_stats_are_parsed_and_calls_are_bounded

**tests.test_support_report.TestUsbLinkForBus**

  - [+] test_resolves_bus_and_devnum_to_speed
  - [+] test_unmatched_or_malformed_returns_none

**tests.test_support_report.TestInterfaceLinks**

  - [+] test_wired_iface_shape_lo_excluded

**tests.test_support_report.TestCollectStreaming**

  - [+] test_a_connected_account_is_reported_as_connected
  - [+] test_a_disconnected_account_is_reported_as_disconnected
  - [+] test_a_disabled_module_is_unknown_not_disconnected
  - [+] test_a_raising_probe_is_unknown_and_names_its_error
  - [+] test_roon_reads_its_token_file
  - [+] test_probes_are_declared_for_every_streaming_service

**tests.test_support_report.TestJournalPresentation**

  - [+] test_lines_are_ordered_by_their_own_timestamp
  - [+] test_a_continuation_line_travels_with_the_line_above_it
  - [+] test_sorting_never_drops_or_duplicates_a_line
  - [+] test_a_dst_change_does_not_scramble_the_order
  - [+] test_a_repeated_block_keeps_its_continuations_together
  - [+] test_a_continuation_never_carries_a_count
  - [+] test_a_repeated_line_is_folded_with_its_count_and_last_time
  - [+] test_a_burst_inside_one_second_does_not_pretend_to_be_a_span
  - [+] test_different_messages_are_never_folded_together
  - [+] test_a_single_occurrence_is_left_exactly_as_it_was

**tests.test_support_report.TestAddressOrigin**

  - [+] test_leased_and_hand_configured_addresses_are_told_apart
  - [+] test_one_call_covers_every_interface
  - [+] test_an_interface_with_no_address_is_absent_not_static

**tests.test_support_report.TestMdnsState**

  - [+] test_the_announced_name_comes_from_avahi_not_from_the_hostname
  - [+] test_a_question_that_could_not_be_asked_stays_unknown (0.01s)
  - [+] test_a_missing_avahi_unit_is_an_answer_not_a_silence

**tests.test_support_report.TestAuthoritySummary**

  - [+] test_the_authority_carries_its_creation_date_and_fingerprint (0.06s)
  - [+] test_two_authorities_never_share_a_fingerprint (0.16s)

**tests.test_support_report.TestProbeDeadlines**

  - [+] test_a_hung_bus_does_not_hold_the_report_open (0.06s)

**tests.test_support_report.TestSeveralAddressesOnOneInterface**

  - [+] test_one_leased_address_makes_the_interface_movable

**tests.test_sysinfo.TestMetrics**

  - [+] test_metrics (0.03s)

**tests.test_sysinfo.TestDetectCpuModel**

  - [+] test_x86_uses_model_name
  - [+] test_arm_falls_back_to_lscpu
  - [+] test_unknown_when_nothing_found
  - [+] test_never_raises_on_error

**tests.test_sysinfo.TestSysinfoSmartctlSafe**

  - [+] test_smartctl_not_found_returns_none (0.04s)

**tests.test_sysinfo.TestSysinfoGrepPatternValidation**

  - [+] test_invalid_regex_returns_400 (0.03s)
  - [+] test_valid_regex_accepted (0.12s)

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

**tests.test_tidal.TestTidalRefreshClearsOnAllFailures**

  - [+] test_expired_token_cleared_on_401 (0.01s)
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
  - [+] test_promotion_happens_at_ffmpeg_exit_not_at_client_pace (0.01s)
  - [+] test_stream_track_remuxes_to_seekable_file_and_caches
  - [+] test_early_disconnect_after_ffmpeg_exit_keeps_the_promoted_file (0.01s)
  - [+] test_promote_failure_is_logged_not_swallowed
  - [+] test_stream_track_discards_incomplete_on_ffmpeg_failure
  - [+] test_cache_keeps_only_most_recent
  - [+] test_cache_rejects_bad_track_id
  - [+] test_stream_serves_cached_file_with_range (0.02s)

**tests.test_tidal_library.TestTidalDiscovery**

  - [+] test_featured_extracts_album_lists_deduped
  - [+] test_featured_no_pagination
  - [+] test_charts_read_the_page_not_the_heading
  - [+] test_a_renamed_row_no_longer_empties_the_shelf
  - [+] test_editorial_drops_the_charts_it_used_to_swallow
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

**tests.test_tidal_library.TestTidalBrowsableLists**

  - [+] test_an_entry_that_answers_nothing_is_dropped
  - [+] test_an_entry_holding_playlists_is_kept_not_dropped
  - [+] test_the_strip_is_ordered_by_what_it_displays
  - [+] test_an_accented_label_sorts_where_a_reader_looks
  - [+] test_genres_are_one_level_and_keep_an_opaque_path
  - [+] test_the_list_is_read_once
  - [+] test_an_empty_list_is_not_memoised
  - [+] test_an_unknown_path_yields_an_empty_grid_not_an_error
  - [+] test_the_grid_carries_offset_and_limit_to_tidal

**tests.test_tidal_library.TestTidalListResilience**

  - [+] test_a_rate_limit_does_not_delete_a_genre_for_good
  - [+] test_a_network_failure_is_not_read_as_an_empty_shelf
  - [+] test_a_404_is_an_answer_and_is_kept
  - [+] test_concurrent_readers_load_the_list_once
  - [+] test_at_most_three_probes_run_together
  - [+] test_editorial_survives_a_dead_charts_page
  - [+] test_editorial_still_fails_when_its_own_page_does
  - [+] test_the_http_error_stays_a_runtime_error

**tests.test_tidal_library.TestTidalExplore**

  - [+] test_the_groups_are_flattened_in_tidal_s_own_order
  - [+] test_a_path_of_the_wrong_shape_never_enters_the_list
  - [+] test_the_page_parameters_are_always_sent
  - [+] test_a_page_separates_what_leads_on_from_what_holds_content
  - [+] test_a_section_with_no_key_of_its_own_is_left_out
  - [+] test_a_page_path_is_matched_not_trusted
  - [+] test_a_section_key_is_matched_not_trusted
  - [+] test_a_section_grid_renders_albums_and_playlists_alike
  - [+] test_the_grid_pages_through_the_section_key

**tests.test_tidal_library.TestTidalSectionRendering**

  - [+] test_an_album_carrying_its_own_duration_still_renders
  - [+] test_albums_and_playlists_share_the_grid
  - [+] test_only_the_types_the_grid_can_render_become_sections

**tests.test_tidal_library.TestTidalProbeSettling**

  - [+] test_a_kind_that_answers_after_another_failed_is_not_frozen
  - [+] test_a_grid_page_does_not_re_run_the_probe

**tests.test_transport_control.TestTransportActions**

  - [+] test_action_set_contents

**tests.test_transport_control.TestControlRouting**

  - [+] test_unknown_service_returns_false
  - [+] test_mpd_protocol_routes_to_control_mpd_and_invalidates
  - [+] test_failed_dispatch_does_not_invalidate
  - [+] test_failed_seek_still_invalidates
  - [+] test_hqplayer_virtual_source_routes_to_control_hqplayer
  - [+] test_renderer_virtual_source_routes_to_control_renderer
  - [+] test_mpris_protocol_routes_with_mpris_name

**tests.test_transport_control.TestControlHqplayerRefreshesCache**

  - [+] test_toggle_refreshes_owning_service_cache

**tests.test_transport_control.TestDbusControlTimeout**

  - [+] test_dbus_send_timeout_returns_false

**tests.test_transport_control.TestControlMpdTruthfulness**

  - [+] test_ok_response_confirms
  - [+] test_refusal_is_reported_not_swallowed
  - [+] test_empty_response_is_not_success
  - [+] test_every_action_travels_as_a_command_list
  - [+] test_toggle_sends_bare_pause
  - [+] test_volume_is_clamped
  - [+] test_never_raises

**tests.test_transport_control.TestHqplayerSeek**

  - [+] test_seek_reaches_the_hqplayer_service

**tests.test_transport_seek**

  - [+] test_direct_seek_needs_no_fallback
  - [+] test_empty_response_is_not_success
  - [+] test_refused_tidal_seek_reopens_from_the_complete_cache
  - [+] test_seek_while_paused_restores_the_pause
  - [+] test_incomplete_remux_refuses_rather_than_restarting
  - [+] test_failed_reopen_compensates_position_and_pause
  - [+] test_non_tidal_stream_gets_no_reopen
  - [+] test_cache_rejected_id_refuses_without_replay
  - [+] test_tidal_module_absent_refuses_cleanly
  - [+] test_other_mpd_refusals_do_not_trigger_the_fallback
  - [+] test_never_raises_even_on_unexpected_errors
  - [+] test_control_mpd_routes_seek_through_the_new_path
  - [+] test_register_publishes_the_router_cache_in_the_container (0.01s)
  - [+] test_reopen_in_flight_refuses_instead_of_queueing

**tests.test_trial_override.TestEffectiveTrialDays**

  - [+] test_no_cache_returns_floor
  - [+] test_valid_signed_override_extends
  - [+] test_override_below_floor_is_ignored
  - [+] test_forged_value_fails_signature
  - [+] test_wrong_signer_is_rejected
  - [+] test_none_key_returns_floor
  - [+] test_days_remaining_honours_effective_duration

**tests.test_trial_override.TestRefreshTrialConfig**

  - [+] test_online_loop_fetches_and_caches_the_blob (0.01s)

**tests.test_trial_override.TestEffectiveTrialAnchor**

  - [+] test_no_cache_returns_none
  - [+] test_valid_signed_anchor_returned
  - [+] test_wrong_device_id_ignored
  - [+] test_forged_value_fails_signature
  - [+] test_wrong_signer_rejected
  - [+] test_none_key_returns_none

**tests.test_trial_override.TestPingAnchor**

  - [+] test_ping_caches_signed_anchor_from_response

**tests.test_trial_override.TestServiceAnchorWiring**

  - [+] test_trial_reconciles_to_cached_anchor

**tests.test_ttl_cache.TestTTLDictCacheGetStale**

  - [+] test_returns_an_expired_entry
  - [+] test_returns_a_live_entry_too
  - [+] test_returns_the_default_for_a_key_never_written
  - [+] test_a_stored_none_is_not_mistaken_for_an_absent_key
  - [+] test_an_invalidated_key_is_gone_not_stale
  - [+] test_the_freshest_write_is_the_one_kept (0.02s)

**tests.test_ttl_cache.TestTTLDictCacheStaleAgeBound**

  - [+] test_an_entry_older_than_max_age_is_refused (0.02s)
  - [+] test_an_entry_within_max_age_is_served
  - [+] test_no_bound_keeps_the_previous_behaviour (0.02s)

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

**tests.test_upmpdcli_parser.TestNamingScheme**

  - [+] test_serialize_derives_friendlyname_from_avfriendlyname
  - [+] test_serialize_realigns_a_dissociated_friendlyname
  - [+] test_serialize_strips_whitespace_around_the_name
  - [+] test_serialize_without_a_name_leaves_friendlyname_alone
  - [+] test_serialize_never_writes_a_blank_avfriendlyname
  - [+] test_parse_backfills_avfriendlyname_for_legacy_configs
  - [+] test_parse_backfill_strips_the_av_runtime_suffix_once
  - [+] test_parse_backfill_preserves_a_chosen_oh_ending
  - [+] test_parse_backfills_over_a_blank_avfriendlyname
  - [+] test_parse_never_overrides_an_explicit_avfriendlyname
  - [+] test_legacy_config_migrates_on_a_structured_roundtrip

**tests.test_upmpdcli_parser.TestBooleans**

  - [+] test_parse_coerces_schema_booleans
  - [+] test_parse_accepts_the_usual_truthy_spellings
  - [+] test_serialize_writes_booleans_as_0_1
  - [+] test_boolean_roundtrip_is_stable

**tests.test_upmpdcli_parser.TestSchema**

  - [+] test_single_name_field_is_avfriendlyname
  - [+] test_openhome_is_an_exposed_boolean

**tests.test_upmpdcli_parser.TestMarkerPreservation**

  - [+] test_marker_is_preserved_on_structured_save
  - [+] test_marker_is_never_added_to_an_unmarked_config
  - [+] test_raw_save_is_untouched

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
  - [+] test_stop_delegates (0.01s)
  - [+] test_pause_calls_avtransport_action_directly
  - [+] test_resume_calls_avtransport_play_directly
  - [+] test_pause_sends_action_without_stale_publish (0.01s)
  - [+] test_pause_noop_when_no_avtransport_action
  - [+] test_seek_abs_time (0.01s)
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
  - [+] test_publish_status_force_then_nonforce_dedup_works

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
  - [+] test_known_route_exists (0.04s)
  - [+] test_connection_route_exists (0.04s)
  - [+] test_status_route_exists (0.04s)
  - [+] test_notify_route_exists (0.04s)
  - [+] test_bypass_route_removed (0.05s)
  - [+] test_remove_renderer_route_exists (0.04s)

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
  - [+] test_check_queue_advance_uri_change_while_playing_schedules_task
  - [+] test_check_queue_advance_no_trigger_when_queue_empty
  - [+] test_check_queue_advance_deduplicates_when_task_pending
  - [+] test_check_queue_advance_creates_task_when_previous_done
  - [+] test_stop_clears_queue
  - [+] test_direct_play_clears_queue
  - [+] test_advance_queue_resolver_failure_rolls_back_queue_idx
  - [+] test_play_queue_entry_always_re_resolves_with_resolver
  - [+] test_advance_queue_uri_changed_re_resolves_for_on_play (0.01s)
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
  - [+] test_resubscribe_guard_prevents_concurrent_calls (0.06s)
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

**tests.test_upnp_renderer.TestManagerDiscoverBuildsNoService**

  - [+] test_discover_calls_the_stateless_helper_directly
  - [+] test_discovery_leaves_no_temporary_file_behind

**tests.test_utils_config_path.TestResolveConfigPath**

  - [+] test_declared_path_kept_when_it_exists
  - [+] test_falls_back_when_declared_missing
  - [+] test_subdirectory_below_the_prefix_is_preserved
  - [+] test_unchanged_when_nothing_found
  - [+] test_empty_path_passthrough
  - [+] test_etc_is_searched_before_usr_local

**tests.test_version**

  - [+] test_product_version_is_semver
  - [+] test_backend_version_matches_product_version (0.04s)

### ui

**js/anti-zoom.test.js**

  - [+] mobile anti-zoom contract > sets no font-size inline on a text field anywhere in js/ (0.02s)
  - [+] mobile anti-zoom contract > gates the anti-zoom rule on the pointer, not on a width breakpoint
  - [+] mobile anti-zoom contract > keeps the anti-zoom selector specific enough to win against component overrides
  - [+] field size tracks its label on touch > draws the field at the label step rather than leaving it at 16px
  - [+] field size tracks its label on touch > follows the label down when compact mode shrinks the scale
  - [+] field size tracks its label on touch > leaves dropdowns out of the anti-zoom rule entirely
  - [+] field size tracks its label on touch > never lets the drawn size reach the 16px the declaration claims

**js/api-docs.test.js**

  - [+] apiDocsUrl > offers nothing when the core does not serve the reference
  - [+] apiDocsUrl > points at the path the core reports, under this core's base
  - [+] apiDocsUrl > asks the entry point, not the reference itself, and does not retry
  - [+] apiDocsUrl > costs one request however many callers ask
  - [+] apiDocsUrl > reports no reference when the core cannot be reached
  - [+] apiDocsUrl > does not remember a failure
  - [+] docsUrlFrom > reads the reference out of an answer already in hand
  - [+] docsUrlFrom > answers null for a core that serves none
  - [+] docsUrlFrom > answers null rather than throwing on nothing at all
  - [+] openApiDocs > does nothing without a URL
  - [+] openApiDocs > uses the application modal when the page has one
  - [+] openApiDocs > falls back to a tab when it does not

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

**js/appearance.test.js**

  - [+] setDarkMode > stamps both elements, since the tokens and the theme rules read different ones
  - [+] setDarkMode > persists it the way theme-boot.js reads it back
  - [+] setDarkMode > goes through MemoryCache when the application provides one
  - [+] setDarkMode > leaves the chrome to the application when the application is there
  - [+] setDarkMode > paints it through theme-boot when nothing else can, with the theme in force
  - [+] setDarkMode > switches even with neither the event nor the hook
  - [+] setDarkMode > returns what it applied, so a caller can hold its own state

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
  - [+] login() — the shape of a failure, which every sign-in message depends on > refused password: 401 with the core's detail
  - [+] login() — the shape of a failure, which every sign-in message depends on > core stopped behind server.py: 502 with an HTML body, detail null
  - [+] login() — the shape of a failure, which every sign-in message depends on > core crashed: Starlette's plain-text 500, detail null, not a network error
  - [+] login() — the shape of a failure, which every sign-in message depends on > a field the core refused: 422 array joined into one line, kept raw underneath
  - [+] login() — the shape of a failure, which every sign-in message depends on > nothing answered: tagged, no status

**js/colors.test.js**

  - [+] colours — every text token clears the floor (règle 8) > minimal light
  - [+] colours — every text token clears the floor (règle 8) > minimal dark
  - [+] colours — every text token clears the floor (règle 8) > slate light
  - [+] colours — every text token clears the floor (règle 8) > slate dark
  - [+] colours — every text token clears the floor (règle 8) > gravity light
  - [+] colours — every text token clears the floor (règle 8) > gravity dark
  - [+] colours — every text token clears the floor (règle 8) > gives every semantic role a text-safe variant in every theme
  - [+] colours — text on a fill, not on the page > minimal light
  - [+] colours — text on a fill, not on the page > minimal dark
  - [+] colours — text on a fill, not on the page > slate light
  - [+] colours — text on a fill, not on the page > slate dark
  - [+] colours — text on a fill, not on the page > gravity light
  - [+] colours — text on a fill, not on the page > gravity dark
  - [+] colours — components read roles, never values (règle 6) > declares no colour literal as a var() fallback (0.05s)
  - [+] colours — components read roles, never values (règle 6) > keeps the base semantic tokens out of JavaScript, whatever route they take (0.12s)
  - [+] colours — components read roles, never values (règle 6) > explains every text colour still written as a value (0.01s)
  - [+] colours — components read roles, never values (règle 6) > paints text with a text-safe token, never a base semantic one (0.04s)

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

**js/fonts.test.js**

  - [+] fonts — served from disk, everywhere > is pulled in by the stylesheet manifest, so every surface gets it
  - [+] fonts — served from disk, everywhere > index.html reaches no font host
  - [+] fonts — served from disk, everywhere > login.html reaches no font host
  - [+] fonts — served from disk, everywhere > public/offline.html reaches no font host
  - [+] fonts — served from disk, everywhere > index.html declares a CSP that forbids remote fonts
  - [+] fonts — served from disk, everywhere > login.html declares a CSP that forbids remote fonts
  - [+] fonts — served from disk, everywhere > leaves no font host in the service worker
  - [+] fonts — served from disk, everywhere > declares every @font-face with a relative url, never a remote one
  - [+] fonts — served from disk, everywhere > ships every referenced font file, as real WOFF2
  - [+] fonts — served from disk, everywhere > covers the weights the UI actually asks of each family
  - [+] fonts — served from disk, everywhere > declares an interface face heavy enough for the heaviest rule in the tree (0.03s)
  - [+] fonts — served from disk, everywhere > declares latin last in each family, so the shared marks do not pull latin-ext
  - [+] fonts — served from disk, everywhere > redistributes the OFL text inside the deployed artifact
  - [+] typography — the theme layer owns the family, and always wins > defaults to Inter on :root
  - [+] typography — the theme layer owns the family, and always wins > names, in both tokens, families the stylesheet actually declares
  - [+] typography — the theme layer owns the family, and always wins > keeps the family out of the components, stylesheet or script (0.03s)
  - [+] typography — the theme layer owns the family, and always wins > never sets an uppercase label in the monospace face (0.01s)
  - [+] typography — the theme layer owns the family, and always wins > never lets waiting for a face swallow what arrived meanwhile
  - [+] typography — the theme layer owns the family, and always wins > resolves the token in one place for the consumers that cannot read CSS
  - [+] typography — the theme layer owns the family, and always wins > keeps the family out of every stylesheet but the theme layer
  - [+] typography — the theme layer owns the family, and always wins > loads the themes after the defaults, since specificity cannot separate them
  - [+] typography — the theme layer owns the family, and always wins > reaches every element a component may read the token from
  - [+] typography — the theme layer owns the family, and always wins > leaves the default theme on the reference typeface
  - [+] typography — the theme layer owns the family, and always wins > offers system names only as a fallback, never as the choice

**js/keyless-client.test.js**

  - [+] the probe: one request decides, instead of hundreds failing > locks after a single 403 and suppresses everything that follows (0.06s)
  - [+] the probe: one request decides, instead of hundreds failing > marks the local refusal as final so the retry layer does not spin (0.02s)
  - [+] the probe: one request decides, instead of hundreds failing > opens keyless traffic when the core proves it does not gate on a key
  - [+] the probe: one request decides, instead of hundreds failing > remembers the verdict across a reload of the same tab (0.01s)
  - [+] what stays open, and what never opens > lets the public endpoints through even when locked
  - [+] what stays open, and what never opens > gives a leftover JWT no URL: the middleware gates on the key alone
  - [+] what stays open, and what never opens > renders covers as empty while locked, and never serialises null
  - [+] what stays open, and what never opens > opens no player SSE from the store while locked (0.06s)
  - [+] what stays open, and what never opens > opens no dashboard worker, and keeps the caller sequence alive

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
  - [+] getSnapshot > serves the cached value on a second call
  - [+] getSnapshot > refetches when forced, and returns the new list
  - [+] getHraCategories > asks the core again after an empty answer
  - [+] getHraCategories > serves the cached list once it has one
  - [+] getHraCategories > refetches when forced
  - [+] getHraCategories > answers with an empty list rather than throwing when the core is unreachable
  - [+] hraHasSubscription > narrows only on an explicit false — absent, null and unknown all read as subscribed
  - [+] getHraConnection > reads /highresaudio/connection and hands the object through
  - [+] getHraConnection > serves the cached answer to the next pill switch
  - [+] getHraConnection > asks again once the sources card forgot it — a new account must not inherit the old answer
  - [+] getHraConnection > a request in flight when the account changes can neither stamp the cache nor answer for it
  - [+] getHraConnection > a sign-in seeds the cache from the POST body — no second round-trip for the browse
  - [+] getHraConnection > seeding with something unusable leaves the cache empty rather than poisoned
  - [+] getHraConnection > answers null rather than throwing when the core is unreachable, and does not keep it
  - [+] getHraConnection > answers null to a body that is not an object, and never caches it
  - [+] forgetHraAccount > drops every cache scoped to the account — favourites and genres too, not just the connection
  - [+] getHraLabels > asks the core for the labels route
  - [+] getHraLabels > serves the cached list once it has one
  - [+] getHraLabels > answers with an empty list rather than throwing
  - [+] getHraPlaylistGroups > asks for the grouping it was given
  - [+] getHraPlaylistGroups > keeps the two groupings in caches of their own
  - [+] getHraPlaylistGroups > answers an unknown grouping with an empty list, asking the core nothing
  - [+] forgetHraAccount — the two shelves added with the menu restructure > drops the labels and both playlist groupings too — they missed the purge (review)
  - [+] getHraSearchFilters > asks again after an answer missing one of HRA's two lists
  - [+] getHraSearchFilters > serves the cached answer once it has a whole one
  - [+] getHraSearchFilters > serves the cache in the same shape it serves a fetch
  - [+] getHraSearchFilters > answers with three empty lists rather than throwing when the core is unreachable
  - [+] getHraSearchFilters > is dropped on sign-out with everything else HRA
  - [+] getQobuzShelves > reads the list from the core rather than holding a copy
  - [+] getQobuzShelves > serves the cached list once it has one
  - [+] getQobuzShelves > asks the core again after an empty answer
  - [+] getQobuzShelves > answers with an empty list rather than throwing when the core is unreachable
  - [+] getQobuzGenres > fetches the tree from its own endpoint
  - [+] getQobuzGenres > keeps its own cache, separate from the HIGHRESAUDIO tree
  - [+] getQobuzGenres > answers with an empty list rather than throwing when the core is unreachable
  - [+] the three Tidal lists > each reads its own endpoint
  - [+] the three Tidal lists > keeps three separate caches, so one never serves under another
  - [+] the three Tidal lists > answer with an empty list rather than throwing when the core is unreachable
  - [+] the Tidal Explore tree > reads the entries from their own endpoint, and caches them
  - [+] the Tidal Explore tree > encodes the page path rather than pasting it into the query
  - [+] the Tidal Explore tree > normalises a page so the strips can read it without checking
  - [+] the Tidal Explore tree > normalises the shapes a malformed answer could take
  - [+] the Tidal Explore tree > answers an empty page rather than throwing at a caller that did not await
  - [+] the Tidal Explore tree > is not cached — there are dozens of pages and each is one small request

**js/license-tiers.test.js**

  - [+] isLicensed > unlocks the paid features for a live licence
  - [+] isLicensed > unlocks them during the trial
  - [+] isLicensed > locks them on the free tier
  - [+] isLicensed > locks them for a licence bought for an earlier major version
  - [+] isLicensed > locks them once a time-limited licence has ended
  - [+] isLicensed > leaves tampered and no_license ungated, as they have always been
  - [+] isLicensed > treats an unknown status as licensed rather than guessing
  - [+] isLicensed > cannot be widened by a caller
  - [+] shouldPromptForLicense > prompts a box on the free tier
  - [+] shouldPromptForLicense > prompts a customer whose term has ended
  - [+] shouldPromptForLicense > stays quiet for a version-locked licence
  - [+] shouldPromptForLicense > stays quiet for a licensed box

**js/login-guidelines.test.js**

  - [+] login page — no phantom tokens (règle 6) > every custom property it reads resolves under every theme
  - [+] login page — no phantom tokens (règle 6) > writes no colour literal of its own
  - [+] login page — no phantom tokens (règle 6) > declares no fallback value inside var()
  - [+] login page — contrast floor (règle 8) > never paints text with --text-tertiary
  - [+] login page — contrast floor (règle 8) > --text-secondary clears 4.5:1 in minimal clair
  - [+] login page — contrast floor (règle 8) > --text-secondary clears 4.5:1 in minimal sombre
  - [+] login page — contrast floor (règle 8) > states the error in --text-primary, not in the red
  - [+] login page — scale discipline (règles 15 et 16) > writes no arbitrary padding or margin
  - [+] login page — scale discipline (règles 15 et 16) > keeps the 11px step for uppercase labels only
  - [+] login page — a button handed back must still work > hands the auto-passkey trigger back to the user after a failure
  - [+] login page — a button handed back must still work > does not arm that trigger with { once: true }
  - [+] login page — a button handed back must still work > still guards against a double submit while the attempt runs

**js/module-imports.test.js**

  - [+] every module comes from this server > finds the sources
  - [+] every module comes from this server > imports nothing over http (0.03s)
  - [+] every module comes from this server > mocks the specifier the code actually imports
  - [+] every module comes from this server > keeps one copy of @lit/context, at the declared version (0.02s)

**js/net-errors.test.js**

  - [+] isNetworkError > recognises Chromium's transport failure once the fetch site has tagged it
  - [+] isNetworkError > recognises Gecko's transport failure once the fetch site has tagged it
  - [+] isNetworkError > recognises WebKit's transport failure once the fetch site has tagged it
  - [+] isNetworkError > recognises a transport failure whose wording nobody has seen yet
  - [+] isNetworkError > does not claim an untagged TypeError raised after a successful response
  - [+] isNetworkError > does not claim an untagged TypeError even when it is worded like a transport failure
  - [+] isNetworkError > does not claim an AbortError
  - [+] isNetworkError > does not claim a 401 as a network failure
  - [+] isNetworkError > does not claim a 403 as a network failure
  - [+] isNetworkError > does not claim a 404 as a network failure
  - [+] isNetworkError > does not claim a 500 as a network failure
  - [+] isNetworkError > does not claim a 502 as a network failure
  - [+] isNetworkError > lets a status override the tag, never the reverse
  - [+] isNetworkError > is not fooled by an ordinary error that merely mentions failure
  - [+] isNetworkError > survives null being thrown
  - [+] isNetworkError > survives undefined being thrown
  - [+] isNetworkError > survives Load failed being thrown
  - [+] isNetworkError > survives 42 being thrown
  - [+] asNetworkError > returns the same error, tagged
  - [+] asNetworkError > wraps a non-Error rejection rather than dropping it
  - [+] isGatewayError > recognises a 502, which only a proxy ever says
  - [+] isGatewayError > recognises a 504, which only a proxy ever says
  - [+] isGatewayError > recognises a 503 that carries no message of its own
  - [+] isGatewayError > never claims a 500, whatever its body
  - [+] isGatewayError > leaves a 400 alone
  - [+] isGatewayError > leaves a 401 alone
  - [+] isGatewayError > leaves a 403 alone
  - [+] isGatewayError > leaves a 404 alone
  - [+] isGatewayError > leaves a 422 alone
  - [+] isGatewayError > leaves a 429 alone
  - [+] isGatewayError > leaves a 500 alone
  - [+] isGatewayError > claims nothing when no status came back
  - [+] connectionMessage > names the address that was tried
  - [+] connectionMessage > still reads as a sentence when the host is unknown
  - [+] connectionMessage > tells the reader what to do, not what failed
  - [+] throwForStatus — one error shape for every caller > turns the service worker's synthetic offline 503 back into a transport failure
  - [+] throwForStatus — one error shape for every caller > keeps a core 503 as what the core said
  - [+] throwForStatus — one error shape for every caller > leaves detail null when the body is not JSON — never statusText
  - [+] throwForStatus — one error shape for every caller > reads slowapi's wording under `error` as something the server said
  - [+] throwForStatus — one error shape for every caller > marks the service worker's offline answer as final — not worth a retry
  - [+] throwForStatus — one error shape for every caller > uses the very literal the service worker writes
  - [+] throwForStatus — one error shape for every caller > joins a 422 field list into one line and keeps it raw underneath
  - [+] readJson > tags a body read the connection dropped, which a retry can fix
  - [+] readJson > leaves a body that is not JSON alone — no retry will change it
  - [+] validationField > drops the leading body/query and joins the rest
  - [+] fetchOrThrow > returns an ok response untouched
  - [+] fetchOrThrow > tags a rejection at the fetch site
  - [+] signInFailureMessage — checked against what the servers really send > server.py with the core stopped — 502, HTML body → names the box and asks for a re-probe
  - [+] signInFailureMessage — checked against what the servers really send > nothing answered → names the box and asks for a re-probe
  - [+] signInFailureMessage — checked against what the servers really send > a proxy 503 with no message → names the box and asks for a re-probe
  - [+] signInFailureMessage — checked against what the servers really send > a running core that crashed → an internal error, not a switched-off box
  - [+] signInFailureMessage — checked against what the servers really send > six wrong passwords in a minute → the wait, not `HTTP 429`
  - [+] signInFailureMessage — checked against what the servers really send > a refused field → a sentence, never the array
  - [+] signInFailureMessage — checked against what the servers really send > a wrong password keeps the form's own line over the core's "Invalid credentials"
  - [+] signInFailureMessage — checked against what the servers really send > a revoked passkey shows the core's sentence when the path asks for it
  - [+] signInFailureMessage — checked against what the servers really send > survives being handed nothing at all
  - [+] signInFailureMessage — checked against what the servers really send > never shows a bare status line for a status it has no sentence for
  - [+] signInFailureMessage — checked against what the servers really send > explains a WebAuthn SecurityError instead of quoting the engine
  - [+] signInFailureMessage — checked against what the servers really send > does not read a superseded WebAuthn ceremony as an unreachable box

**js/no-undef.test.js**

  - [+] no undeclared identifier anywhere in the tree > reports no error
  - [+] no undeclared identifier anywhere in the tree > reports no stale eslint-disable directive
  - [+] no undeclared identifier anywhere in the tree > actually looked at the application, rather than at nothing
  - [+] no undeclared identifier anywhere in the tree > does not lint generated output that git already refuses to track
  - [+] each file is checked against its own platform, not against every platform > gives the service worker its own globals and not the browser DOM
  - [+] each file is checked against its own platform, not against every platform > gives the build config Node and not the DOM
  - [+] each file is checked against its own platform, not against every platform > gives the application the DOM and not Node
  - [+] each file is checked against its own platform, not against every platform > knows the Storybook preview runs in a browser, unlike Storybook's own config (0.01s)
  - [+] each file is checked against its own platform, not against every platform > knows the Storybook setup file runs in Chromium, despite looking like a test helper
  - [+] each file is checked against its own platform, not against every platform > accepts the names the compatibility layer publishes, and still catches a typo
  - [+] each file is checked against its own platform, not against every platform > accepts the libraries index.html loads from a script tag

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
  - [+] activeOutput > picks the entry named by active_output_id
  - [+] activeOutput > falls back to the active flag when no id is given
  - [+] activeOutput > returns null when there are no outputs
  - [+] outputLabel > names the active output
  - [+] outputLabel > names a selected output that is stopped, instead of claiming none is selected
  - [+] outputLabel > falls back to the flat label, then to a placeholder
  - [+] isOutputStopped > is true for a selected output sitting idle
  - [+] isOutputStopped > is false while it plays or pauses
  - [+] isOutputStopped > is false when the state is unknown — never inferred from a missing item
  - [+] activeOutputError > reads the error of the output designated by active_output_id
  - [+] activeOutputError > returns the message when the active output is the failing one
  - [+] isOutputUnreachable > is true for a selected speaker that cannot be contacted
  - [+] isOutputUnreachable > is false when it answers
  - [+] isOutputUnreachable > is false when the backend does not send the flag
  - [+] seekRefusalRollback > restores the pre-seek position on a 503 for the same track
  - [+] seekRefusalRollback > does nothing on other statuses — the seek may in fact have landed
  - [+] seekRefusalRollback > does nothing once the track has changed — the anchor belongs to another song
  - [+] seekRefusalRollback > does nothing without a seek in flight or without an anchor
  - [+] toggleRefusalRollback > restores the pre-flip transport state on a 503 for the same track
  - [+] toggleRefusalRollback > does nothing on other statuses — the toggle may in fact have landed
  - [+] toggleRefusalRollback > does nothing once the track has changed
  - [+] toggleRefusalRollback > does nothing without an anchor
  - [+] applyVolumeGuard > passes the state through when no change is pending
  - [+] applyVolumeGuard > holds the target while a level the finger already left arrives
  - [+] applyVolumeGuard > releases on the exact target
  - [+] applyVolumeGuard > does not accept a neighbouring level as the destination
  - [+] applyVolumeGuard > expires so a refused level cannot freeze the slider
  - [+] applyVolumeGuard > releases when the source changes — the volume is someone else's now
  - [+] applyVolumeGuard > leaves the incoming object untouched while holding

**js/push-manager.test.js**

  - [+] push-manager unsubscribe (Fix P3) > calls apiDelete (not apiPost) on unsubscribe (0.02s)
  - [+] push-manager unsubscribe (Fix P3) > passes endpoint as query param in the URL
  - [+] push-manager unsubscribe (Fix P3) > URLSearchParams encodes the endpoint correctly

**js/sizes.test.js**

  - [+] the type scale is one closed scale > declares seven steps, in one place
  - [+] the type scale is one closed scale > gives every step a different value
  - [+] the type scale is one closed scale > orders the steps by their names
  - [+] the type scale is one closed scale > names no step it does not declare (0.02s)
  - [+] sizes come from the scale > finds the sources
  - [+] sizes come from the scale > writes no size as a value, unless it says why (0.03s)
  - [+] sizes come from the scale > is documented with the values it actually has
  - [+] sizes come from the scale > leaves the pipeline diagram off the scale
  - [+] sizes come from the scale > keeps the touch-field size a literal
  - [+] sizes come from the scale > reserves the smallest step for labels, not for read text

**js/sse.test.js**

  - [+] services_metrics routing > emits the whole event, envelope included
  - [+] services_metrics routing > still emits one event per service, unchanged
  - [+] services_metrics routing > emits the envelope before the per-service events
  - [+] services_metrics routing > carries a true memory_accounting through as well
  - [+] services_metrics routing > emits the envelope even when the event lists no service
  - [+] services_metrics routing > delivers one event per throttle window, not one per subscriber
  - [+] worker errors > routes nothing when the worker reports an error
  - [+] worker errors > names a dropped connection instead of logging undefined
  - [+] the worker sends errors in the shape the page reads > sees every error path in the file
  - [+] the worker sends errors in the shape the page reads > never posts an error without an error field
  - [+] the worker sends errors in the shape the page reads > does not route an error through the generic forward helper

**js/static-assets.test.js**

  - [+] the app shell lists files the box actually serves > finds the list
  - [+] the app shell lists files the box actually serves > ships every same-origin entry it promises to precache
  - [+] the app shell lists files the box actually serves > ships every image the service worker names elsewhere
  - [+] the marks the library shows exist too > finds the marks
  - [+] the marks the library shows exist too > ships every file they name, in both variants
  - [+] the marks the library shows exist too > gives each mark a light and a dark variant
  - [+] the app icon is declared once and reserved everywhere > declares one size
  - [+] the app icon is declared once and reserved everywhere > reserves that size at every call-site that renders it inline
  - [+] the manifest points at icons that exist > declares some
  - [+] the manifest points at icons that exist > ships every one of them
  - [+] the manifest points at icons that exist > offers a square icon for every purpose it declares

**js/text-selection.test.js**

  - [+] text selection is off by default > turns selection off on body rather than on a list of elements
  - [+] text selection is off by default > keeps the -webkit- prefix, since nothing prefixes for us
  - [+] text selection is off by default > also suppresses the iOS long-press callout, which is a separate mechanism
  - [+] text selection is off by default > re-enables selection everywhere the user has to copy or type
  - [+] text selection is off by default > never grants the exception to .xterm (0.13s)
  - [+] components in a shadow root carry the rule themselves > declares user-select in every component the body rule cannot reach (0.01s)

**js/theme-boot.test.js**

  - [+] theme boot — reaches the page before the first paint > index.html loads it synchronously, ahead of the stylesheet
  - [+] theme boot — reaches the page before the first paint > index.html allows it under its own CSP
  - [+] theme boot — reaches the page before the first paint > login.html loads it synchronously, ahead of the stylesheet
  - [+] theme boot — reaches the page before the first paint > login.html allows it under its own CSP
  - [+] theme boot — reaches the page before the first paint > is served at a stable path, not fingerprinted into assets/
  - [+] theme boot — reaches the page before the first paint > is precached, so a cold load offline still gets it
  - [+] theme boot — its copies match their source > knows the same themes as the registry
  - [+] theme boot — its copies match their source > falls back to the same theme as common.js
  - [+] theme boot — its copies match their source > reads the keys common.js and the config panel write
  - [+] theme boot — its copies match their source > paints the browser chrome the colours updateThemeColorMeta would
  - [+] theme boot — its copies match their source > stamps the root element, the only one that exists that early
  - [+] theme boot — its copies match their source > recreates the theme-color meta rather than updating it
  - [+] theme boot — its copies match their source > survives storage being unavailable
  - [+] theme boot — its copies match their source > carries the whole Safari remedy, not just the node swap
  - [+] theme boot — reachable from the interface, and safe there > exposes the routine the appearance switch calls (0.04s)
  - [+] theme boot — reachable from the interface, and safe there > paints the chrome of a theme it knows (0.01s)
  - [+] theme boot — reachable from the interface, and safe there > falls back rather than throwing on a theme it does not know

**js/themes.test.js**

  - [+] theme layer — every theme is scoped to itself > minimal.css writes only under its own selector
  - [+] theme layer — every theme is scoped to itself > slate.css writes only under its own selector
  - [+] theme layer — every theme is scoped to itself > gravity.css writes only under its own selector
  - [+] theme layer — a palette applies before any script runs > index.html stamps data-theme in the markup
  - [+] theme layer — a palette applies before any script runs > login.html stamps data-theme in the markup
  - [+] theme layer — a palette applies before any script runs > leaves no colour on :root for a page to fall back to
  - [+] theme layer — no theme depends on another > minimal resolves every token without help from a sibling theme
  - [+] theme layer — no theme depends on another > slate resolves every token without help from a sibling theme
  - [+] theme layer — no theme depends on another > gravity resolves every token without help from a sibling theme

**js/ui-helpers.test.js**

  - [+] getUserFriendlyError > reads a tagged transport failure, whatever the engine called it
  - [+] getUserFriendlyError > does not turn an untagged TypeError into a connection error
  - [+] getUserFriendlyError > reads a gateway answer the same way net-errors does
  - [+] getUserFriendlyError > survives being handed nothing
  - [+] getUserFriendlyError > maps HTTP 401
  - [+] getUserFriendlyError > maps HTTP 403
  - [+] getUserFriendlyError > maps HTTP 404
  - [+] getUserFriendlyError > maps HTTP 500
  - [+] getUserFriendlyError > returns error.detail when available
  - [+] getUserFriendlyError > returns error.message for unknown errors
  - [+] getUserFriendlyError > returns default for empty error
  - [+] showToast — the type comes first, and a wrong one is said aloud > coerces an unknown type and reports the call (0.02s)
  - [+] showPasswordConfirm — field styling contract > styles the field through .form-control, never an inline font-size (0.03s)
  - [+] showPasswordConfirm — field styling contract > keeps the password affordances the browser needs
  - [+] showPasswordConfirm — dialog contrast > carries the dialog variant so the field is not the colour of the modal
  - [+] downloadBlob — the two details that decide whether a file is written > clicks an anchor that is part of the document
  - [+] downloadBlob — the two details that decide whether a file is written > does not revoke the object URL before returning
  - [+] downloadBlob — the two details that decide whether a file is written > still frees the memory, one turn later
  - [+] downloadBlob — the two details that decide whether a file is written > leaves no anchor behind
  - [+] downloadBlob — the two details that decide whether a file is written > downloadTextFile goes through the same path, with the given type

**js/validation.test.js**

  - [+] validation.js > validateAudioConfig > posts the config to the audio-config validation route
  - [+] validation.js > validateTopologyConfig > posts the topology to the topology validation route
  - [+] validation.js > validateTopologyConfig > returns the validation response verbatim (errors + warnings)
  - [+] validation.js > validateTopologyConfig > rethrows when the API call fails

**js/version.test.js**

  - [+] version propagation (single source: audiogravity.ops/VERSION) > VERSION is a valid semver (0.9.51)
  - [+] version propagation (single source: audiogravity.ops/VERSION) > js/core/config.js UI_VERSION matches VERSION (UI display)
  - [+] version propagation (single source: audiogravity.ops/VERSION) > sw.js CACHE_NAME matches VERSION (PWA cache busting)

**js/webauthn.test.js**

  - [+] loginWithPasskey > short-circuits (NoPasskeyError) without prompting when the username has no passkey
  - [+] loginWithPasskey > prompts and completes when the user has passkeys
  - [+] loginWithPasskey > discoverable flow (no username) still prompts even with empty allowCredentials
  - [+] webauthnFetch — what a refusal and a dead network look like to the caller > carries the status and the core's own sentence on a 401
  - [+] webauthnFetch — what a refusal and a dead network look like to the caller > reads a slowapi rate limit, which is worded under `error`, not `detail`
  - [+] webauthnFetch — what a refusal and a dead network look like to the caller > leaves detail null on a proxy 502 whose body is HTML
  - [+] webauthnFetch — what a refusal and a dead network look like to the caller > tags a transport failure whatever the engine calls it

**js/wordmark.test.js**

  - [+] the wordmark is text, at every call-site > is imported by the stylesheet manifest, so login and the app both get it
  - [+] the wordmark is text, at every call-site > index.html writes the brand as markup, in the shared class
  - [+] the wordmark is text, at every call-site > login.html writes the brand as markup, in the shared class
  - [+] the wordmark is text, at every call-site > js/components/molecules/ag-tabs.js writes the brand as markup, in the shared class
  - [+] the wordmark is text, at every call-site > js/login.js sets the footer credit in the same treatment
  - [+] the wordmark is text, at every call-site > js/components/organisms/ag-footer.js sets the footer credit in the same treatment
  - [+] the wordmark is text, at every call-site > leaves the drawn logo behind everywhere, precache included
  - [+] the mark is styled in one place > sets the landing page treatment on the shared class
  - [+] the mark is styled in one place > inherits its colour rather than declaring one
  - [+] the mark is styled in one place > goes inline in running text, so a link underline reaches it
  - [+] the mark is styled in one place > keeps the mark an inline-block, so a flex parent cannot reach the <sup>
  - [+] the mark is styled in one place > sizes the superscript against the mark, not against the type scale
  - [+] the mark is styled in one place > leaves the call-sites nothing to declare but their size

**js/components/component-imports.test.js**

  - [+] component import graph > every <ag-*> tag used in a component template is imported by that component (0.15s)

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
  - [+] normalizeSearchSources > drops entries the backend marks as not selectable
  - [+] normalizeSearchSources > keeps sources from a backend that does not send the flag
  - [+] normalizeSearchSources > appends known UPnP servers with their location URL
  - [+] normalizeSearchSources > falls back to "UPnP" label and empty location when missing
  - [+] normalizeSearchSources > does not add the same UPnP server twice
  - [+] normalizeSearchSources > tolerates null/undefined inputs
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > gives HIGHRESAUDIO a mark, because its owner asked to be shown rather than named
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > gives Qobuz, Tidal and Roon one too — these logos ARE the name written out
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > marks every id Roon answers to, not just one of them
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > src_highresaudio carries both theme variants and the name for anyone the image cannot reach
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > src_qobuz carries both theme variants and the name for anyone the image cannot reach
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > src_tidal carries both theme variants and the name for anyone the image cannot reach
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > src_roon carries both theme variants and the name for anyone the image cannot reach
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > sizes the two wide marks apart from HIGHRESAUDIO
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > renders the source badge as a mask, so it survives the selected card
  - [+] SOURCE_MARKS — a source shown by its mark instead of its name > leaves every other source to be named

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
  - [+] catalogueErrorMessage > relays the core reason when an external catalogue refused the request
  - [+] catalogueErrorMessage > has its own wording when a 503 carries no reason
  - [+] catalogueErrorMessage > keeps the caller fallback for anything that is not a 503
  - [+] catalogueErrorMessage > does not throw on a null error
  - [+] fmtIsoDate > keeps the calendar day whatever the viewer timezone
  - [+] fmtIsoDate > formats the first of a month without slipping into the previous one
  - [+] fmtIsoDate > returns nothing for an absent date, so callers can fall back
  - [+] fmtIsoDate > shows an unrecognised value as authored rather than inventing a day
  - [+] isPast > is false on the expiry day itself — a licence is valid through it
  - [+] isPast > is true the day after
  - [+] isPast > compares in UTC, matching the core
  - [+] isPast > is false when there is no date at all
  - [+] planLabel > names a perpetual licence
  - [+] planLabel > does not call a paid term a trial
  - [+] planLabel > carries the end date, formatted without shifting the day
  - [+] planLabel > handles a term with no date rather than printing undefined
  - [+] planLabel > shows an unknown plan as given instead of inventing one

**js/core/FavoritesController.test.js**

  - [+] FavoritesController > registers with the host
  - [+] FavoritesController > load() subscribes, fills the id set, and requests an update
  - [+] FavoritesController > load() re-subscribes when the source changes (unsubscribing the previous one)
  - [+] FavoritesController > a favorites notification re-syncs from the cache
  - [+] FavoritesController > hostDisconnected unsubscribes
  - [+] FavoritesController > toggle(add) optimistically adds and persists
  - [+] FavoritesController > toggle(remove) optimistically removes and persists
  - [+] FavoritesController > reverts the optimistic change and toasts when persistence fails

**js/core/ScrollEdgesController.test.js**

  - [+] ScrollEdgesController > registers itself with the host
  - [+] ScrollEdgesController > marks the right edge only, at the start of an overflowing strip
  - [+] ScrollEdgesController > marks both edges in the middle
  - [+] ScrollEdgesController > drops the right marker at the end — within a pixel of slack
  - [+] ScrollEdgesController > marks neither edge when everything fits
  - [+] ScrollEdgesController > re-reads the edges as the strip is scrolled
  - [+] ScrollEdgesController > a drag costs no render: only overflowing-at-all asks for one
  - [+] ScrollEdgesController > asks for a render when the strip starts overflowing
  - [+] ScrollEdgesController > re-attaching the same pair keeps one listener, and reads no layout
  - [+] ScrollEdgesController > says nothing at all about a strip in a hidden view
  - [+] ScrollEdgesController > takes its markers off the element it stops watching
  - [+] ScrollEdgesController > lets go of the strip when the host disconnects, and re-reads on reconnect
  - [+] ScrollEdgesController > watches the strip for width changes, not just scrolls
  - [+] ScrollEdgesController > re-reads once the webfonts have landed — they widen the labels, not the box
  - [+] ScrollEdgesController > survives a browser without ResizeObserver
  - [+] ScrollEdgesController > does nothing at all when attached to nothing
  - [+] ScrollEdgesController > falls back to marking the strip itself when given no target

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
  - [+] SwipeToDismissController > interactive-target guard (row action buttons) > ignores a gesture that starts on an action button
  - [+] SwipeToDismissController > interactive-target guard (row action buttons) > still arms when the gesture starts on the row itself
  - [+] SwipeToDismissController > interactive-target guard (row action buttons) > ignores an interactive ancestor that sits OUTSIDE the swiped row
  - [+] SwipeToDismissController > interactive-target guard (row action buttons) > still ignores a control that IS inside the swiped row
  - [+] SwipeToDismissController > interactive-target guard (row action buttons) > arms when the event carries no DOM target (synthetic events must not throw)
  - [+] SwipeToDismissController > multi-touch / pointer isolation > ignores a second concurrent pointerdown and never mixes their state
  - [+] SwipeToDismissController > multi-touch / pointer isolation > ignores move/end from a foreign pointerId
  - [+] SwipeToDismissController > trailing-click suppression + timer cleanup > keeps `swiping` true through the trailing click, then clears it
  - [+] SwipeToDismissController > trailing-click suppression + timer cleanup > does not leave `swiping` set after a plain tap (never crossed the slop)
  - [+] SwipeToDismissController > trailing-click suppression + timer cleanup > hostDisconnected clears the pending timer
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > reveals the backdrop while dragging and hides it once the row is back (0.04s)
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > clears the inline transform once the snap-back has run
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > leaves no trace at all after a plain tap
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > does not strip a row a new gesture has already taken over
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > cleans up per row: a gesture on another row does not strand the first
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > hides the backdrop at once on a commit, before the wrap is reused
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > does not reveal the backdrop for a rightward drag
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > rests a row still animating when the host goes away
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > release() frees a row un-wired mid-gesture, and the controller with it
  - [+] SwipeToDismissController > resting state — nothing red under an untouched row > keeps `swiping` true for a fresh drag started during the trailing click
  - [+] swipeRow directive > stamps the coexistence contract and wires the four pointer listeners
  - [+] swipeRow directive > does not wire or stamp when enabled is false
  - [+] swipeRow directive > tears down listeners and the contract on disconnect
  - [+] swipeRow directive > throws when used outside an element binding

**js/core/config.test.js**

  - [+] API key resolution > prefers the key the installer injected over one kept in this browser
  - [+] API key resolution > drops the leftover override so it cannot come back later
  - [+] API key resolution > still uses a stored key when nothing is injected (development)
  - [+] API key resolution > reports a missing key instead of throwing
  - [+] API key resolution > no longer exposes a way to overwrite the key at runtime

**js/core/gesture-constants.test.js**

  - [+] edge band invariant > reserves more room than the panels actually claim
  - [+] edge band invariant > keeps a usable safety margin, not a token one
  - [+] edge band invariant > treats every panel-open touch as an edge start
  - [+] edge band invariant > leaves the middle of the screen alone
  - [+] edge band invariant > yields in the margin itself — where nothing should happen

**js/core/keep-in-view.test.js**

  - [+] keepInView > centres the item in its own strip (0.16s)
  - [+] keepInView > never touches an overflow-hidden ancestor — the page must not shift (0.01s)
  - [+] keepInView > scrolls vertically only when the item is actually out of view (0.01s)
  - [+] keepInView > animates by default, instantly on first or with animations off (0.01s)
  - [+] keepInView > is a no-op without an element or without a designed scroller

**js/core/license-docs.test.js**

  - [+] license-docs > exposes a title
  - [+] license-docs > numbers the EULA sections 1..n without a gap or a repeat
  - [+] license-docs > tells the owner what the box sends to the licence server
  - [+] license-docs > keeps Governing Law and General last, in that order
  - [+] parity with audiogravity.site/EULA.md > shows the same clauses, in the same order, under the same numbers
  - [+] parity with audiogravity.site/EULA.md > carries the licence-validation clause on both sides

**js/core/support-report-format.test.js**

  - [+] formatSupportReport > handles a missing or malformed report instead of throwing
  - [+] formatSupportReport > states when it was generated and which format it is
  - [+] formatSupportReport > says up front that secrets were removed
  - [+] formatSupportReport > gives the version and architecture
  - [+] formatSupportReport > gives each managed service its state and whether it starts at boot
  - [+] formatSupportReport > says whether each config is AG-managed or hand-written
  - [+] formatSupportReport > surfaces a failed unit outside the AG set
  - [+] formatSupportReport > reports a library path that exists but cannot be read
  - [+] formatSupportReport > says when MPD has never indexed
  - [+] formatSupportReport > includes the redacted config lines and what was removed
  - [+] formatSupportReport > prints a section the core could not collect rather than dropping it
  - [+] formatSupportReport > still renders every other section when one failed
  - [+] formatSupportReport > renders an empty report without throwing
  - [+] formatSupportReport > says a box has no local library rather than showing an empty list
  - [+] formatSupportReport > marks a config file that is missing
  - [+] formatSupportReport > rounds the load average
  - [+] formatSupportReport > keeps a space between a long label and its value
  - [+] formatSupportReport > marks a package unsupported on this architecture
  - [+] formatSupportReport — v2 sections > reports NTP not synchronizing — the silent killer
  - [+] formatSupportReport — v2 sections > reports an unreachable licence server with its error
  - [+] formatSupportReport — v2 sections > gives the UI its own version line
  - [+] formatSupportReport — v2 sections > flags a certificate that does not name the current address
  - [+] formatSupportReport — v2 sections > says the CA signs the served certificate
  - [+] formatSupportReport — v2 sections > treats an absent download token as the normal public-releases state
  - [+] formatSupportReport — v2 sections > reports MEASURED access to the releases repo, with the latest version
  - [+] formatSupportReport — v2 sections > says when the box is up to date
  - [+] formatSupportReport — v2 sections > reports refused access as what breaks updates
  - [+] formatSupportReport — v2 sections > never converts a GitHub rate limit into a verdict
  - [+] formatSupportReport — v2 sections > warns on a world-readable .env and lists missing keys by name
  - [+] formatSupportReport — v2 sections > shows storage in terabytes when it is terabytes
  - [+] formatSupportReport — v2 sections > shows the live stream — the bit-perfect proof
  - [+] formatSupportReport — v2 sections > renders MPD stats even on a streaming-only box
  - [+] formatSupportReport — v2 sections > renders journal lines, and silence as a real answer
  - [+] formatSupportReport — v2 sections > renders an idle stream list as a statement, not an absence
  - [+] formatSupportReport — v2 sections > states when the .env does not exist at all
  - [+] formatSupportReport — v2 sections > a failed v2 section prints its error and sinks nothing
  - [+] formatSupportReport — AV network > lists each renderer with its host and marks this box
  - [+] formatSupportReport — AV network > lists media servers such as MinimServer
  - [+] formatSupportReport — AV network > reports HQPlayer reachable with its engine state
  - [+] formatSupportReport — AV network > reports an unreachable Roon Core as the diagnosis it is
  - [+] formatSupportReport — AV network > says none found rather than showing an empty list
  - [+] formatSupportReport — AV network > marks the interface carrying the default route
  - [+] formatSupportReport — links, USB speed, audio tuning > gives each wired link its negotiated speed — the 100 Mb gigabit port
  - [+] formatSupportReport — links, USB speed, audio tuning > says WHY the wifi rate is unknown instead of pretending
  - [+] formatSupportReport — links, USB speed, audio tuning > gives a measured wifi link its bitrate, signal and ssid
  - [+] formatSupportReport — links, USB speed, audio tuning > shows the local time next to the timezone
  - [+] formatSupportReport — links, USB speed, audio tuning > names the USB link speed of the DAC
  - [+] formatSupportReport — links, USB speed, audio tuning > shows the current CPU frequency with the governor
  - [+] formatSupportReport — links, USB speed, audio tuning > renders live scheduling with accounting and drop-ins
  - [+] formatSupportReport — links, USB speed, audio tuning > flags a drop-in that did not apply — configured vs live
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > marks a read-only filesystem as the failure it is
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > unmasks a crash-looping unit hidden by Restart=always
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > reads what accounting counts — memory and cpu per unit
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > says an unconfigured HQPlayer was still FOUND on the network
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > says an unconfigured Roon Core announces itself
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > counts the backups behind each config
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > surfaces hardware kernel warnings — the DAC reset
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > shows the boot history that reframes a ticket
  - [+] formatSupportReport — kernel, boots, ro, restarts, backups, network finds > states kernel silence as an answer
  - [+] formatSupportReport — post-review corrections > a box without Roon says "not in use", never a false UNREACHABLE
  - [+] formatSupportReport — post-review corrections > keys on code defaults read as inventory, not as an alarm
  - [+] formatSupportReport — a failed measurement is never a negative diagnosis > a v1 core: absent v2 sections are stated as absent, not fabricated
  - [+] formatSupportReport — a failed measurement is never a negative diagnosis > a failed gateway or DNS read is shown as a failed read
  - [+] formatSupportReport — a failed measurement is never a negative diagnosis > a failed live scheduling probe falls back to configured values and says so
  - [+] formatSupportReport — a failed measurement is never a negative diagnosis > a failed unit query still shows kernel warnings and boot history
  - [+] formatSupportReport — a failed measurement is never a negative diagnosis > kernel and boot read failures are rendered, not swallowed
  - [+] formatSupportReport — a failed measurement is never a negative diagnosis > an unreadable /proc/asound/cards is not "no DAC"
  - [+] formatSupportReport — a failed measurement is never a negative diagnosis > backups are shown even for a config file that is missing
  - [+] formatSupportReport — a probe that could not run never reads as a negative > a streaming account whose probe failed is unknown, not "not signed in"
  - [+] formatSupportReport — a probe that could not run never reads as a negative > renders a streaming service the core added that the UI never heard of
  - [+] formatSupportReport — a probe that could not run never reads as a negative > probe_errors is never rendered as if it were a streaming service
  - [+] formatSupportReport — a probe that could not run never reads as a negative > a masked unit is not called missing
  - [+] formatSupportReport — a probe that could not run never reads as a negative > an unknown load state is reported neutrally, never as absence
  - [+] formatSupportReport — a probe that could not run never reads as a negative > a unit that is not installed is said to be missing, not tuned
  - [+] formatSupportReport — what the box does, not only what AG believes > tells two outputs of the same card apart
  - [+] formatSupportReport — what the box does, not only what AG believes > never prints the same USB id twice on one line
  - [+] formatSupportReport — what the box does, not only what AG believes > still names the USB id when the label does not carry it
  - [+] formatSupportReport — what the box does, not only what AG believes > says nothing about the config device when the core did not send one
  - [+] formatSupportReport — what the box does, not only what AG believes > reports an unreadable config device as such, distinctly from an absent field
  - [+] formatSupportReport — what the box does, not only what AG believes > shows the device each config actually names
  - [+] formatSupportReport — what the box does, not only what AG believes > flags a config that plays somewhere other than the pinned output
  - [+] formatSupportReport — what the box does, not only what AG believes > says nothing about agreement when there is no pin to compare against
  - [+] formatSupportReport — the facts a certificate incident turns on > dates the served certificate, not only its expiry
  - [+] formatSupportReport — the facts a certificate incident turns on > dates and fingerprints the authority, which an upgrade never reissues
  - [+] formatSupportReport — the facts a certificate incident turns on > says a leased address is leased
  - [+] formatSupportReport — the facts a certificate incident turns on > reports the name the box announces, as avahi gives it
  - [+] formatSupportReport — the facts a certificate incident turns on > still says something on a box where nothing announces the name
  - [+] formatSupportReport — the facts a certificate incident turns on > does not turn "could not ask" into "announces nothing"
  - [+] formatSupportReport — the facts a certificate incident turns on > omits the issue date rather than printing undefined
  - [+] formatSupportReport — the facts a certificate incident turns on > compares the announced name without case, as DNS does
  - [+] formatSupportReport — the facts a certificate incident turns on > flags an announced name the certificate does not carry
  - [+] formatSupportReport — the facts a certificate incident turns on > explains no_license instead of letting it read as a refusal
  - [+] formatSupportReport — the facts a certificate incident turns on > dates the self-update, so "done" says when
  - [+] formatSupportReport — the facts a certificate incident turns on > marks MPD's last error as undated, since MPD keeps it until cleared

**js/components/atoms/ag-library-cover.test.js**

  - [+] ag-library-cover — deferred image loading > marks the cover image as lazy so off-screen rows cost nothing (0.04s)
  - [+] ag-library-cover — deferred image loading > still points at the requested cover
  - [+] ag-library-cover — deferred image loading > renders no image at all when there is no cover, so nothing is requested
  - [+] ag-library-cover — deferred image loading > drops the image once it has failed, instead of retrying on every render
  - [+] ag-library-cover — banner artwork > is square by default: the height matches the width
  - [+] ag-library-cover — banner artwork > halves the height when the artwork is a banner
  - [+] ag-library-cover — banner artwork > recomputes the height when the size alone changes on a cell already wide
  - [+] ag-library-cover — banner artwork > restores a square cell when the artwork stops being a banner

**js/components/atoms/ag-license-badge.test.js**

  - [+] ag-license-badge > says Lifetime for a perpetual licence (0.02s)
  - [+] ag-license-badge > does not say Lifetime for a licence bought with an end date
  - [+] ag-license-badge > names an ended term instead of falling through to "No license"
  - [+] ag-license-badge > paints an ended term as a warning, never as critical (0.01s)
  - [+] ag-license-badge > still paints a tampered file as critical
  - [+] ag-license-badge > counts down the trial
  - [+] ag-license-badge > falls back to "No license" only for an unknown status

**js/components/atoms/ag-theme-toggle.test.js**

  - [+] ag-theme-toggle > takes its initial state from the document, not from a default (0.05s)
  - [+] ag-theme-toggle > offers the appearance you are not in
  - [+] ag-theme-toggle > hands the click to the shared switch (0.01s)
  - [+] ag-theme-toggle > announces the change to whoever is listening

**js/components/organisms/ag-audio-pipeline-render.test.js**

  - [+] the steering pop-up renders > with a service on this port — the branch that threw
  - [+] the steering pop-up renders > with a service on another port
  - [+] the steering pop-up renders > while a service is being steered
  - [+] the steering pop-up renders > with no service at all
  - [+] the steering pop-up renders > when the node has gone from the pipeline since the pop-up opened
  - [+] the node detail panel renders > for an active node — the branch that threw
  - [+] the node detail panel renders > for an inactive node
  - [+] the node detail panel renders > for a node with no manufacturer or model

**js/components/organisms/ag-audio-software-logs.test.js**

  - [+] live log events > advances the cursor so a later catch-up cannot duplicate the line
  - [+] live log events > ignores lines from a package the modal is not showing
  - [+] opening the modal > does not fetch the log before the operation has started
  - [+] catch-up after missed events > asks only for what is missing and appends it in order
  - [+] catch-up after missed events > recovers the closing burst when the stream comes back (0.05s)
  - [+] catch-up after missed events > does nothing while the stream is still down
  - [+] catch-up after missed events > skips the request when no operation is being watched
  - [+] catch-up after missed events > skips the request when the modal is closed
  - [+] catch-up after missed events > leaves the modal usable when the catch-up request fails
  - [+] catch-up after missed events > does not duplicate lines when two catch-ups overlap
  - [+] catch-up after missed events > never moves the cursor backwards when a live line overtook the fetch
  - [+] catch-up after missed events > leaves the cursor alone when the server has nothing new

**js/components/organisms/ag-audio-software-page.test.js**

  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > escapes a malicious package label
  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > escapes malicious version strings
  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > renders a normal package correctly after escaping
  - [+] Bulk-update confirm dialog — XSS prevention via escapeHtml > handles undefined version gracefully
  - [+] Update of a package that publishes no version > offers a reinstall for a vendor that publishes no version
  - [+] Update of a package that publishes no version > still refuses when a package that should have a version has none
  - [+] Update of a package that publishes no version > keeps the up-to-date shortcut for packages that do publish one
  - [+] Update of a package that publishes no version > goes ahead when the published version differs
  - [+] Playback warning in the confirmation > warns that an update restarts the service
  - [+] Playback warning in the confirmation > warns that an uninstall stops and removes it
  - [+] Playback warning in the confirmation > says nothing when installing something that is not running yet
  - [+] Playback warning in the confirmation > says nothing for a package AG does not start or stop
  - [+] Playback warning in the confirmation > escapes the label it interpolates
  - [+] Reading which services AG has configured > does not ask when the session is not an admin
  - [+] Reading which services AG has configured > reads it for an admin, and says nothing when the read fails (3.03s)

**js/components/organisms/ag-audio-stack-provisioning.test.js**

  - [+] _libraryPayload > manual path → music_directory
  - [+] _libraryPayload > manual with empty path → null
  - [+] _libraryPayload > usb source → library_usb_uuid + fstype
  - [+] _libraryPayload > mount source → music_directory
  - [+] _libraryPayload > no choice → null
  - [+] _canProvision > false without a library
  - [+] _canProvision > true with output + library
  - [+] _canProvision > false while provisioning
  - [+] a box with no local library > can initialize once "no library" is chosen
  - [+] a box with no local library > is still refused while nothing has been chosen
  - [+] a box with no local library > sends an explicit empty path, not an absent field
  - [+] a box with no local library > names the way out instead of only stating the requirement
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
  - [+] AgConfigEditor — guided/structured/expert mode switching > switching to another service returns to the default view
  - [+] AgConfigEditor — guided/structured/expert mode switching > a status refresh of the same service leaves the chosen view alone
  - [+] AgConfigEditor — guided/structured/expert mode switching > a status refresh does not disturb the structured view either
  - [+] AgConfigEditor — guided/structured/expert mode switching > repeated status refreshes never accumulate into a reset
  - [+] AgConfigEditor — originals capture on parent reload (guided-apply safety) > re-captures originals when the parent reloads the config (both props change)
  - [+] AgConfigEditor — originals capture on parent reload (guided-apply safety) > does not re-capture originals on a single-mode edit (only one prop changes)

**js/components/organisms/ag-config-page.test.js**

  - [+] the handlers given to the modal survive being called by it > stores the status even when invoked with the modal as `this`
  - [+] the handlers given to the modal survive being called by it > reloads the services grid even when invoked with the modal as `this`
  - [+] the handlers given to the modal survive being called by it > does not ask the box for the status a second time
  - [+] the handlers given to the modal survive being called by it > is what makes the banner go away without a reload
  - [+] the handlers given to the modal survive being called by it > throws nothing where the unbound methods did
  - [+] the modal template uses the bound handlers > hands over the bound handlers themselves, not the raw methods
  - [+] the modal template uses the bound handlers > hands over functions that keep working off the page

**js/components/organisms/ag-config-panel.test.js**

  - [+] Settings panel — the API key is not editable from here > renders no API key field
  - [+] Settings panel — the API key is not editable from here > holds no API key state and no way to overwrite it
  - [+] Settings panel — every toast names its type first > passes one of the four toast types as the first argument
  - [+] Settings panel — every toast names its type first > never starts a toast call with an expression instead of a type literal

**js/components/organisms/ag-guided-config.test.js**

  - [+] descriptor > mpd has output + library, airplay has output, upmpdcli none (0.02s)
  - [+] _initialOutputId > matches the pinned output
  - [+] _initialOutputId > falls back to the recommended output when no pin
  - [+] _outputChanged > false when selection equals the pin
  - [+] _outputChanged > true when selection differs from the pin
  - [+] _canApply > false with no changes
  - [+] _canApply > true when the output changed
  - [+] _canApply > true when a library is chosen
  - [+] _canApply > false while busy
  - [+] _apply > patches only the output when only the output changed (airplay) (0.02s)
  - [+] _apply > patches output AND library for mpd, and clears the library choice (0.03s)
  - [+] _apply > does nothing when there is no change
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
  - [+] removing the music library from the guided editor > asks before detaching
  - [+] removing the music library from the guided editor > does nothing when the question is declined
  - [+] removing the music library from the guided editor > does not ask when a library is being SET
  - [+] removing the music library from the guided editor > does not announce an indexing run that will not happen
  - [+] removing the music library from the guided editor > still announces one when a library IS set

**js/components/organisms/ag-json-config-modal.test.js**

  - [+] ag-json-config-modal file transfer > _handleDownload > downloads the live editor content under the configured filename
  - [+] ag-json-config-modal file transfer > _handleDownload > falls back to configText when there is no editor yet
  - [+] ag-json-config-modal file transfer > _handleDownload > falls back to a default name when none is configured
  - [+] ag-json-config-modal file transfer > _handleUploadClick > clicks the hidden file input
  - [+] ag-json-config-modal file transfer > _handleFileSelected > loads the file content into the editor and enters edit mode
  - [+] ag-json-config-modal file transfer > _handleFileSelected > does nothing when no file is picked
  - [+] ag-json-config-modal file transfer > _handleFileSelected > surfaces a read error without throwing

**js/components/organisms/ag-library-browse-pills.test.js**

  - [+] each pill asks the core for its own order > All requests the alphabetical sort
  - [+] each pill asks the core for its own order > A–Z requests the alphabetical sort
  - [+] each pill asks the core for its own order > Recent requests the library-add order — the fix
  - [+] each pill asks the core for its own order > an unknown pill falls back to alphabetical rather than to nothing
  - [+] changing pill reloads only when the order really changes > reloads when moving to Recent
  - [+] changing pill reloads only when the order really changes > does not refetch between All and A–Z — they are the same order today
  - [+] changing pill reloads only when the order really changes > ignores a click on the pill already active
  - [+] the client no longer reorders what the core sent > hands the pages through untouched
  - [+] the client no longer reorders what the core sent > does not truncate Recent to a fixed head
  - [+] Roon is not offered an order it cannot honour > sends no sort parameter
  - [+] Roon is not offered an order it cannot honour > renders no sort pills at all
  - [+] Roon is not offered an order it cannot honour > does not refetch when a filter value changes
  - [+] a page in flight cannot land in the wrong order > drops a load-more that resolves after a reload
  - [+] a page in flight cannot land in the wrong order > keeps a load-more that resolves within its own generation
  - [+] a page in flight cannot land in the wrong order > releases the load-more gate on reload so the next page can be fetched
  - [+] a pill bar that scrolls says so > offers no chevron at all while every pill fits
  - [+] a pill bar that scrolls says so > offers both chevrons as soon as pills are hidden
  - [+] a pill bar that scrolls says so > names the chevrons after what the bar holds on every source, not just HRA
  - [+] a pill bar that scrolls says so > names each strip's chevrons after the strip they move
  - [+] a pill bar that scrolls says so > names a strip added later after itself, not after the filters
  - [+] a pill bar that scrolls says so > keeps the chevrons out of the global tab swipe
  - [+] a pill bar that scrolls says so > leaves the wrapper class alone so the markers survive a render
  - [+] a pill bar that scrolls says so > keeps the bar up while a page loads
  - [+] the genre strip drills in place > shows no genre strip on any other pill
  - [+] the genre strip drills in place > shows the strip on the Genres pill, with its own data-strip name
  - [+] the genre strip drills in place > offers a way back to the list once a genre is chosen
  - [+] the genre strip drills in place > says to choose a genre rather than reporting no albums

**js/components/organisms/ag-library-browse.test.js**

  - [+] ag-library-browse — artist drill-down > _fetchPage hits /library/albums?artist_id=… when an artist is set
  - [+] ag-library-browse — artist drill-down > _fetchPage bypasses the streaming pill routing in artist mode (Tidal)
  - [+] ag-library-browse — artist drill-down > _fetchPage carries the name-as-id for HRA (name-based backend)
  - [+] ag-library-browse — artist drill-down > _sectionLabel shows "Albums by <name>" in artist mode
  - [+] ag-library-browse — artist drill-down > _sectionLabel falls back to "artist" when the name is missing
  - [+] ag-library-browse — HIGHRESAUDIO category pills > keeps the categories off the filter bar, which is the seven shelves and fixed
  - [+] ag-library-browse — HIGHRESAUDIO category pills > is the same bar before the categories have arrived
  - [+] ag-library-browse — HIGHRESAUDIO category pills > shows the label but keys the strip on the title HRA answers with
  - [+] ag-library-browse — HIGHRESAUDIO category pills > leads the strip with the entries HIGHRESAUDIO asked for, keeping the rest behind
  - [+] ag-library-browse — HIGHRESAUDIO category pills > _fetchPage asks for the category by title
  - [+] ag-library-browse — HIGHRESAUDIO category pills > _fetchPage asks for nothing while the categories are still in flight
  - [+] ag-library-browse — HIGHRESAUDIO category pills > _fetchPage still routes the Favorites pill to the generic album list
  - [+] ag-library-browse — HIGHRESAUDIO category pills > _sectionLabel titles the grid with the displayed label, not the German title
  - [+] ag-library-browse — HIGHRESAUDIO category pills > takes the list from the store, which owns the caching
  - [+] ag-library-browse — HIGHRESAUDIO category pills > a failed list leaves an empty strip, never a broken bar
  - [+] ag-library-browse — HIGHRESAUDIO category pills > asks again on every load while the list is missing — Refresh repairs the strip
  - [+] ag-library-browse — HIGHRESAUDIO category pills > does not fetch the categories on a browse that is not showing them
  - [+] ag-library-browse — HIGHRESAUDIO category pills > asks for the genre tree again on every load while it is missing
  - [+] ag-library-browse — HIGHRESAUDIO category pills > does not fetch the genre tree while another pill is chosen
  - [+] ag-library-browse — HIGHRESAUDIO category pills > stops asking once the list is there
  - [+] ag-library-browse — HIGHRESAUDIO Vault > _fetchPage asks the Vault route, paged like the others
  - [+] ag-library-browse — HIGHRESAUDIO Vault > a subscribed account sees the Vault beside Favorites, ahead of the shelves
  - [+] ag-library-browse — HIGHRESAUDIO Vault > an account without a subscription gets the Vault alone, and lands on it
  - [+] ag-library-browse — HIGHRESAUDIO Vault > never asks for the shelves on an account that cannot play them
  - [+] ag-library-browse — HIGHRESAUDIO Vault > reads the connection before fetching a page, so the first request is the right one
  - [+] ag-library-browse — HIGHRESAUDIO Vault > an answer it cannot read is "subscribed" — the state every account had before the field
  - [+] ag-library-browse — HIGHRESAUDIO Vault > a load superseded during the connection wait does not blank what its successor rendered
  - [+] ag-library-browse — HIGHRESAUDIO Vault > does not ask for the ★ Set of an account whose favourites are refused
  - [+] ag-library-browse — HIGHRESAUDIO Vault > offers no ★ on a purchase — a Vault id is not a catalogue id
  - [+] ag-library-browse — HIGHRESAUDIO Vault > keeps the ★ on the other streaming sources
  - [+] ag-library-browse — HIGHRESAUDIO Vault > titles the grid after the pill
  - [+] ag-library-browse — HIGHRESAUDIO Vault > queues a purchase as an album, with the prefixed id exactly as listed
  - [+] ag-library-browse — HIGHRESAUDIO genres > offers the genres while none is chosen
  - [+] ag-library-browse — HIGHRESAUDIO genres > offers the genre as "All", then its sub-genres
  - [+] ag-library-browse — HIGHRESAUDIO genres > never repeats a label when a sub-genre carries its genre's name
  - [+] ag-library-browse — HIGHRESAUDIO genres > stays on the genre of the chosen sub-genre
  - [+] ag-library-browse — HIGHRESAUDIO genres > asks for the album grid by path, not by title
  - [+] ag-library-browse — HIGHRESAUDIO genres > fetches nothing while no genre is chosen
  - [+] ag-library-browse — HIGHRESAUDIO genres > titles the grid with the whole path, so "All" still says which genre
  - [+] ag-library-browse — HIGHRESAUDIO genres > fetches the tree on the first visit only
  - [+] ag-library-browse — HIGHRESAUDIO genres > returns to the list of genres when the pill is chosen again
  - [+] ag-library-browse — HIGHRESAUDIO playlists > offers Playlists among the seven shelves
  - [+] ag-library-browse — HIGHRESAUDIO playlists > asks for the tree that is on screen
  - [+] ag-library-browse — HIGHRESAUDIO playlists > switching tree reloads with the other one
  - [+] ag-library-browse — HIGHRESAUDIO playlists > queues a playlist as a playlist, with the id exactly as listed
  - [+] ag-library-browse — HIGHRESAUDIO playlists > an album on any other pill is still an album
  - [+] ag-library-browse — HIGHRESAUDIO playlists > names the Tidal surface on screen, as the other two do
  - [+] ag-library-browse — HIGHRESAUDIO playlists > names the Qobuz tree on screen, as HRA does
  - [+] ag-library-browse — HIGHRESAUDIO playlists > forgets which tree was open, and which shelf, when the source changes
  - [+] ag-library-browse — HIGHRESAUDIO playlists > titles the grid with the tree on screen
  - [+] ag-library-browse — a playlist is told from an album > knows the playlist grids of all three services, and no other pill
  - [+] ag-library-browse — a playlist is told from an album > tags a playlist card, in the slot an album gives its year
  - [+] ag-library-browse — a playlist is told from an album > leaves an album card alone — its year, or nothing
  - [+] ag-library-browse — a playlist is told from an album > says it on a list row too, ahead of the byline
  - [+] ag-library-browse — a playlist is told from an album > queues from the same answer it renders from
  - [+] ag-library-browse — the ★ is offered only where the grid holds albums > is withheld on every playlist grid
  - [+] ag-library-browse — the ★ is offered only where the grid holds albums > is withheld on the Vault — a purchase id is not a catalogue id
  - [+] ag-library-browse — the ★ is offered only where the grid holds albums > stays on the album grids it was written for
  - [+] ag-library-browse — the ★ is offered only where the grid holds albums > shows one glyph for one coverless item, card and row alike
  - [+] ag-library-browse — banner covers > marks HRA editorial artwork as a banner, card and row alike
  - [+] ag-library-browse — banner covers > leaves the account's own HRA playlists square — their artwork has no measured shape
  - [+] ag-library-browse — banner covers > leaves Qobuz and Tidal playlists square — their covers are square
  - [+] ag-library-browse — banner covers > leaves the HRA album grids square — only the playlists are banners
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > offers All ahead of the four shelves — nothing can be hidden
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > asks HRA for the shelf rather than filtering 1762 here
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > sends no shelf on All, which is the only view holding the uncategorised
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > shows no shelf strip over the account's own tree, and asks for none
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > shows no shelf strip on any other pill
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > leaving the editorial tree drops its shelf — a narrowed tree with no strip is a dead end
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > picking a shelf reloads; picking the one already open does not
  - [+] ag-library-browse — HIGHRESAUDIO editorial shelves > the chosen shelf names the grid, and All gives the tree its name back
  - [+] ag-library-browse — the Labels and Charts shelves > leads the strip with the labels HIGHRESAUDIO asked for
  - [+] ag-library-browse — the Labels and Charts shelves > asks for one label by title
  - [+] ag-library-browse — the Labels and Charts shelves > asks for nothing while the labels are still in flight
  - [+] ag-library-browse — the Labels and Charts shelves > opens on the first label once the list lands, without waiting for a tap
  - [+] ag-library-browse — the Labels and Charts shelves > leaves the choice alone when the reader has already made one
  - [+] ag-library-browse — the Labels and Charts shelves > titles the grid with the label on screen
  - [+] ag-library-browse — the Labels and Charts shelves > Charts asks for the chart route and needs no second choice
  - [+] ag-library-browse — the Labels and Charts shelves > Charts is titled by its own shelf, having no strip to name it
  - [+] ag-library-browse — playlists by genre and by theme > browses the editorial tree, naming the grouping beside it
  - [+] ag-library-browse — playlists by genre and by theme > sends no shelf alongside a grouping — HRA serves them from different endpoints
  - [+] ag-library-browse — playlists by genre and by theme > asks for nothing until a group is chosen
  - [+] ag-library-browse — playlists by genre and by theme > shows the shelf strip over the editorial tree and the group strip over a grouping
  - [+] ag-library-browse — playlists by genre and by theme > treats a grouping as editorial artwork — those are the 2:1 teasers too
  - [+] ag-library-browse — playlists by genre and by theme > opens a grouping on its first entry when its list is already in memory
  - [+] ag-library-browse — playlists by genre and by theme > fetches a grouping the first time it is opened, then opens on its first entry
  - [+] ag-library-browse — playlists by genre and by theme > keeps the two groupings apart in state
  - [+] ag-library-browse — playlists by genre and by theme > titles the grid with the group, not with the grouping
  - [+] ag-library-browse — playlists by genre and by theme > leaving a grouping takes its choice with it
  - [+] ag-library-browse — review fixes on the shelves > a groups list landing after the reader left Playlists changes nothing on screen
  - [+] ag-library-browse — review fixes on the shelves > still opens the grouping when its shelf IS on screen
  - [+] ag-library-browse — review fixes on the shelves > re-measures the filter bar when the subscription state is learned
  - [+] ag-library-browse — review fixes on the shelves > keeps a category in its asked-for place even when the core re-words its label
  - [+] ag-library-browse — the two design calls settled with the user > a shelf reopened finds the entry its reader left it on
  - [+] ag-library-browse — the two design calls settled with the user > still opens on the first entry when nothing has been chosen yet
  - [+] ag-library-browse — the two design calls settled with the user > reads a grouping key that is not a word on its own
  - [+] ag-library-browse — Qobuz shelves > offers five shelves, each opening a strip of its own
  - [+] ag-library-browse — Qobuz shelves > is the same bar before the shelves have arrived
  - [+] ag-library-browse — Qobuz shelves > keys the strip on the shelf title and shows its label
  - [+] ag-library-browse — Qobuz shelves > does not reorder what the core listed
  - [+] ag-library-browse — Qobuz shelves > asks the shelf endpoint with the chosen shelf as the type
  - [+] ag-library-browse — Qobuz shelves > asks for nothing until a shelf is chosen
  - [+] ag-library-browse — Qobuz shelves > names the grid after the chosen shelf, not after the pill above it
  - [+] ag-library-browse — Qobuz shelves > opens on the first shelf when its list lands
  - [+] ag-library-browse — Qobuz shelves > does not fill the strip when the source changed while the list was in flight
  - [+] ag-library-browse — Qobuz purchases > asks the purchases endpoint
  - [+] ag-library-browse — Qobuz purchases > still offers the ★, unlike the HRA vault
  - [+] ag-library-browse — Qobuz purchases > holds albums, not playlists
  - [+] ag-library-browse — Qobuz playlists > carries the chosen tree to the core
  - [+] ag-library-browse — Qobuz playlists > offers exactly two trees — Qobuz has no third
  - [+] ag-library-browse — Qobuz playlists > queues a playlist as a playlist
  - [+] ag-library-browse — Qobuz playlists > has no shelf strip under its trees, unlike HRA
  - [+] ag-library-browse — Qobuz genres > offers the genres while none is chosen
  - [+] ag-library-browse — Qobuz genres > offers the genre as "All", then its sub-genres
  - [+] ag-library-browse — Qobuz genres > stays on the genre of the chosen sub-genre
  - [+] ag-library-browse — Qobuz genres > finds the genre of a name that carries a slash
  - [+] ag-library-browse — Qobuz genres > titles the grid with the genre and its sub-genre, never with the raw path
  - [+] ag-library-browse — Qobuz genres > keeps the list of genres when the chosen one has nothing under it
  - [+] ag-library-browse — Qobuz genres > asks the Qobuz genre endpoint with the opaque path
  - [+] ag-library-browse — Qobuz genres > asks for nothing until a genre is picked
  - [+] ag-library-browse — Qobuz genres > fetches the Qobuz tree, not the HRA one
  - [+] ag-library-browse — Qobuz genres > does not fill the strip when the source changed while the tree was in flight
  - [+] ag-library-browse — Tidal > offers six shelves, not five flat pills
  - [+] ag-library-browse — Tidal > has no Purchases pill — Tidal sells nothing
  - [+] ag-library-browse — Tidal > reads a shelf through the one list route, naming which list
  - [+] ag-library-browse — Tidal > reads a genre and a mood through that same route
  - [+] ag-library-browse — Tidal > asks for nothing until an entry is chosen
  - [+] ag-library-browse — Tidal > routes the three playlist surfaces to their own endpoints
  - [+] ag-library-browse — Tidal > puts the charts in the playlist strip, not on the bar
  - [+] ag-library-browse — Tidal > shares the shelf strip with Qobuz rather than growing one of its own
  - [+] ag-library-browse — Tidal > keeps the moods on their own state, not on the shelves
  - [+] ag-library-browse — Tidal > names the grid after the chosen entry on every strip
  - [+] ag-library-browse — Tidal > actually renders its genre strip
  - [+] ag-library-browse — Tidal > drills nowhere in the genres — Tidal publishes no sub-genre
  - [+] ag-library-browse — Tidal > fetches the Tidal tree, not another service’s
  - [+] ag-library-browse — Tidal > does not fill a strip when the source changed while it was in flight
  - [+] ag-library-browse — Tidal > opens on the first entry when a strip lands
  - [+] ag-library-browse — Tidal Explore > shows the entries while none is open
  - [+] ag-library-browse — Tidal Explore > drills a page of links in place, with a way back
  - [+] ag-library-browse — Tidal Explore > offers no way back from a strip that was never replaced
  - [+] ag-library-browse — Tidal Explore > shows a page of sections on the strip below, not in place
  - [+] ag-library-browse — Tidal Explore > has no section strip on a page that only leads on
  - [+] ag-library-browse — Tidal Explore > pages the grid through the section key
  - [+] ag-library-browse — Tidal Explore > asks for nothing until a section is chosen
  - [+] ag-library-browse — Tidal Explore > names the grid with the page and the section
  - [+] ag-library-browse — Tidal Explore > opens a page on its first section
  - [+] ag-library-browse — Tidal Explore > goes back to the entries without asking the core again
  - [+] ag-library-browse — Tidal Explore > drops a page that lands after the reader left the shelf
  - [+] ag-library-browse — Tidal Explore > keeps the level when a linked page is opened
  - [+] ag-library-browse — Tidal Explore > queues a shelf of playlists as playlists, because the core says so
  - [+] ag-library-browse — Tidal Explore > leaves a shelf of albums alone
  - [+] ag-library-browse — Tidal Explore > reads the same statement on an Explore section
  - [+] ag-library-browse — Tidal Explore > drops a page that lands after the reader moved on
  - [+] ag-library-browse — every source with a Genres pill renders its strip > src_highresaudio
  - [+] ag-library-browse — every source with a Genres pill renders its strip > src_qobuz
  - [+] ag-library-browse — every source with a Genres pill renders its strip > src_tidal
  - [+] ag-library-browse — every source with a Genres pill renders its strip > and a source without one renders nothing

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

**js/components/organisms/ag-library-page.test.js**

  - [+] ag-library-page — one home for the view mapping > the tab bar and _navigate agree on where "browse" goes for a UPnP source
  - [+] ag-library-page — one home for the view mapping > an unknown tab lands on the browse rather than nowhere
  - [+] ag-library-page — one home for the view mapping > a tab switch does not reload the browse — it keeps its grid and its scroll
  - [+] ag-library-page — one home for the view mapping > _navigate still reloads the browse — its callers arrive with a reason to
  - [+] ag-library-page — one home for the view mapping > a tab switch leaves artist mode
  - [+] ag-library-page — the sources-changed funnel > reloads the browse when the source list changes — the one signal an account change sends
  - [+] ag-library-page — the sources-changed funnel > after the source list is current, so the browse reads the new state, not the old

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
  - [+] ag-library-queue — truthful removal > _remove relays the refusal as a toast and re-syncs the list (0.02s)
  - [+] ag-library-queue — truthful removal > _remove stays silent on success
  - [+] ag-library-queue — truthful removal > _clear sweeps past failures and summarises them in ONE toast
  - [+] ag-library-queue — truthful removal > _clear stays silent when every removal succeeds

**js/components/organisms/ag-library-radio.test.js**

  - [+] AbortController — race condition guard > creates a new AbortController on each call
  - [+] AbortController — race condition guard > aborts the previous controller when called a second time
  - [+] AbortController — race condition guard > ignores results from a cancelled request (signal.aborted guard)
  - [+] AbortController — race condition guard > clears loading flag after a successful non-aborted search
  - [+] AbortController — race condition guard > does not clear loading flag when the request is aborted
  - [+] search debounce — outbound politeness > waits long enough that ordinary typing does not query per keystroke
  - [+] search debounce — outbound politeness > cancels the pending timer before arming a new one
  - [+] leaving the Search tab > drops a debounce timer armed just before the tab switch
  - [+] leaving the Search tab > discards a search already in flight when the tab changes
  - [+] leaving the Search tab > lowers the loading flag the aborted search can no longer lower itself
  - [+] leaving the Search tab > tears the pending search down in the component itself
  - [+] leaving the Search tab > guards the search result write by view, as the sibling loaders do
  - [+] catalogue failures on membership actions > surfaces the catalogue reason when an add fails
  - [+] catalogue failures on membership actions > does not blame MPD when a station will not start

**js/components/organisms/ag-library-search.test.js**

  - [+] ag-library-search — where a HIGHRESAUDIO search goes > uses the ordinary search while no filter is set
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > uses the filtered endpoint as soon as one is set
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > answers with albums only, and empties the other two sections
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > leaves the filters behind when the source does
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > keeps the filters when the source did not change
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > searches on a criterion alone, with the box left empty
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > sends every criterion the form applied, under the core's own names
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > searches a two-letter term, filtered or not
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > does not send an order with nothing to arrange, and says why
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > sends the order along once there is something to arrange
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > drops the results when the form is cleared with an empty box
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > keeps searching on the criteria when the box is emptied
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > drops an answer that arrives after a newer search
  - [+] ag-library-search — where a HIGHRESAUDIO search goes > a filter change disarms the pending keystroke search
  - [+] ag-library-search — an account without a subscription > says where the purchases are instead of running a search that cannot answer
  - [+] ag-library-search — an account without a subscription > does not ask for the ★ Set its account is refused
  - [+] ag-library-search — an account without a subscription > leaves every other source alone — the flag only means something on HRA
  - [+] ag-library-search — an account without a subscription > reads the connection through the store when arriving on HRA

**js/components/organisms/ag-logs-modal.test.js**

  - [+] closing the logs modal > closes itself even when the handler is invoked by the modal
  - [+] closing the logs modal > does not close the modal element instead of itself
  - [+] closing the logs modal > still asks its host to close, for hosts that drive it themselves

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
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > gives every table its own scroll container, keeping the <table> element (0.01s)
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > wraps each of several tables exactly once
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > is idempotent — re-enhancing does not nest a second wrapper
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > stamps GitHub-style slug ids (punctuation, duplicate dedup, unicode)
  - [+] ag-manual-modal > link rewriting (_rewriteLink / _enhanceHtml) > enhances at cache time: cached HTML already has ids, absolute lazy images

**js/components/organisms/ag-mobile-pipeline.test.js**

  - [+] ag-mobile-pipeline data acquisition > requests the pipeline exactly once, then listens
  - [+] ag-mobile-pipeline data acquisition > never polls the pipeline endpoint again, however long the tab stays open
  - [+] ag-mobile-pipeline data acquisition > takes its updates from the SSE event instead
  - [+] ag-mobile-pipeline data acquisition > still polls steering, which has no event on the dashboard channel
  - [+] ag-mobile-pipeline data acquisition > stops listening and polling once disconnected
  - [+] ag-mobile-pipeline data acquisition > survives a failing backend without leaving the tab on the loader
  - [+] an empty signal path explains itself > names the output it found when the described chain does not mention it
  - [+] an empty signal path explains itself > puts what is playing next to what is declared
  - [+] an empty signal path explains itself > names the box, not the whole chain, when its outputs are missing
  - [+] an empty signal path explains itself > says the route could not be traced when music plays and nothing is undeclared
  - [+] an empty signal path explains itself > says something plain when everything matches but nothing is playing
  - [+] an empty signal path explains itself > explains instead of drawing nothing when no device is active
  - [+] what the panel says is declared > names the box when only its own outputs are missing
  - [+] what the panel says is declared > lists the declared outputs when there are some

**js/components/organisms/ag-modal.test.js**

  - [+] the Escape listener > is installed while the modal is shown
  - [+] the Escape listener > is removed when the modal is hidden
  - [+] the Escape listener > is removed when the modal is torn out of the DOM while still shown
  - [+] the Escape listener > survives being disconnected without ever having been shown
  - [+] the Escape listener > is not installed at all when escape-close is refused

**js/components/organisms/ag-network-test.test.js**

  - [+] AgNetworkTest.disconnectedCallback — jitterChart destroy (Fix P2) > destroys _jitterChart when component is disconnected (0.06s)
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
  - [+] AgNowPlayingFullscreen — Up next from PlayerState.queue_next > a local item shown while a cast runs elsewhere keeps its own queue
  - [+] AgNowPlayingFullscreen — Up next from PlayerState.queue_next > a state without played_on falls back to the local path
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
  - [+] AgNowPlayingFullscreen — volume in flight (real _control) > shows the level asked for at once, and remembers what to hold
  - [+] AgNowPlayingFullscreen — volume in flight (real _control) > ignores a level the finger already left, then releases on the target
  - [+] AgNowPlayingFullscreen — volume in flight (real _control) > restores the previous level when the output REFUSES it
  - [+] AgNowPlayingFullscreen — volume in flight (real _control) > does NOT roll back on a network error — the level may well have taken (0.04s)
  - [+] AgNowPlayingFullscreen — volume in flight (real _control) > an older command failing does not undo a newer one (0.01s)

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
  - [+] AgNowPlaying — volume in flight (real _sendControl) > shows the level at once and arms the guard for that source
  - [+] AgNowPlaying — volume in flight (real _sendControl) > rolls back a REFUSED level on the item currently in the list
  - [+] AgNowPlaying — volume in flight (real _sendControl) > an older command refused does not undo a newer one
  - [+] AgNowPlaying — volume in flight (real _sendControl) > never holds a level on a source the user was not adjusting

**js/components/organisms/ag-orientation-gate.test.js**

  - [+] ag-orientation-gate > tags itself with the .orientation-gate CSS hook on connect (0.22s)
  - [+] ag-orientation-gate > renders the rotate prompt and a landscape escape hatch (0.01s)
  - [+] ag-orientation-gate > _dismiss turns the lock off (state + persisted) and applies it
  - [+] ag-orientation-gate > _setBackgroundInert inerts sibling top-level elements but never itself

**js/components/organisms/ag-pipeline-page.test.js**

  - [+] ag-pipeline-page topology save > persists directly when the topology is valid with no warnings
  - [+] ag-pipeline-page topology save > blocks the save and shows the modal on structural errors
  - [+] ag-pipeline-page topology save > asks for confirmation before persisting when there are warnings
  - [+] ag-pipeline-page topology save > persists once the warning confirmation callback runs
  - [+] ag-pipeline-page topology save > falls through to the save when validation is unreachable (0.01s)
  - [+] ag-pipeline-page topology save > reports a backend save failure without closing the modal
  - [+] the mobile view can reach the configuration > offers CONFIG on a phone, as the desktop view does
  - [+] the mobile view can reach the configuration > withholds it from a guest, exactly as the desktop view does
  - [+] the test stubs do not leak > leaves document.getElementById alone for other ids

**js/components/organisms/ag-pull-tab.test.js**

  - [+] ag-pull-tab — restore gesture > restores on a clean tap
  - [+] ag-pull-tab — restore gesture > restores on an upward swipe
  - [+] ag-pull-tab — restore gesture > restores on a -12 px travel — the band that used to do nothing
  - [+] ag-pull-tab — restore gesture > restores on a -15 px travel — the band that used to do nothing
  - [+] ag-pull-tab — restore gesture > restores on a -20 px travel — the band that used to do nothing
  - [+] ag-pull-tab — restore gesture > restores on a -29 px travel — the band that used to do nothing
  - [+] ag-pull-tab — restore gesture > restores on a sloppy tap that drifts downward within the slop
  - [+] ag-pull-tab — restore gesture > ignores a deliberate downward drag
  - [+] ag-pull-tab — restore gesture > suppresses the synthetic click it would otherwise duplicate
  - [+] ag-pull-tab — restore gesture > leaves the click path alone when it ignores the gesture

**js/components/organisms/ag-services-page.test.js**

  - [+] when the box counts no memory > says so once, and offers the way out
  - [+] when the box counts no memory > stays silent when the counter works
  - [+] when the box counts no memory > points at the Systemd tab when a service has its accounting off
  - [+] when the box counts no memory > says nothing at all when every figure is measured
  - [+] when the box counts no memory > stops saying it once the counter is turned on
  - [+] when the box counts no memory > reads a service with its accounting off from the event
  - [+] when the box counts no memory > says nothing when every service is measured
  - [+] when the box counts no memory > opens the manual at the chapter that explains it
  - [+] when the box counts no memory > survives a page without the manual modal in the DOM
  - [+] the two metrics subscriptions do not overlap > reads the envelope for what only it carries
  - [+] the two metrics subscriptions do not overlap > does not apply the figures a second time
  - [+] the two metrics subscriptions do not overlap > still applies them once, on the per-service event

**js/components/organisms/ag-support-report.test.js**

  - [+] the this binding through ag-modal > closes itself when the handler is invoked by the modal
  - [+] the this binding through ag-modal > does not close the modal element instead of itself
  - [+] the this binding through ag-modal > copies its own text when the handler is invoked by the modal
  - [+] the this binding through ag-modal > binds the handlers to the instance, not merely to some function
  - [+] collecting the report > asks the core only when the window opens
  - [+] collecting the report > does not collect a second time on reopen
  - [+] collecting the report > shows the failure instead of an empty window
  - [+] collecting the report > clears the loading flag on success
  - [+] copy > does nothing when there is no report yet
  - [+] copy > tells the owner when the browser blocked the clipboard
  - [+] download > does nothing when there is no report yet
  - [+] download > names the file after the day it was taken
  - [+] the template itself > renders while collecting
  - [+] the template itself > renders a loaded report
  - [+] the template itself > renders a failure
  - [+] the template itself > renders an untouched component
  - [+] the template itself > wires the footer buttons to its own bound handlers
  - [+] the template itself > refuses backdrop close, so selecting the text cannot dismiss the window
  - [+] reopening after a failure > does not show the previous error again
  - [+] collection state is unmistakable > shows a spinner and the warning tone while collecting
  - [+] collection state is unmistakable > switches to the success tone once the report is ready

**js/components/organisms/ag-user-modal.test.js**

  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (6 spaces) is rejected (0.02s)
  - [+] AgUserModal._handleSave — password trim (Fix P3) > whitespace-only password (tabs) is rejected
  - [+] AgUserModal._handleSave — password trim (Fix P3) > valid password passes validation
  - [+] AgUserModal._handleSave — password trim (Fix P3) > password with surrounding spaces is trimmed before sending
  - [+] AgUserModal._handleSave — password trim (Fix P3) > short username is rejected regardless of password

**js/components/molecules/ag-announcement-banner.test.js**

  - [+] ag-announcement-banner — localStorage helpers > getDismissed returns empty Set when storage is empty
  - [+] ag-announcement-banner — localStorage helpers > getDismissed survives malformed JSON without throwing
  - [+] ag-announcement-banner — localStorage helpers > saveDismissed + getDismissed round-trip
  - [+] ag-announcement-banner — _icon > returns the matching Lucide icon for each known type
  - [+] ag-announcement-banner — _icon > falls back to the info icon for unknown type
  - [+] ag-announcement-banner — _emitBadge > emits count=0 when all announcements are dismissed
  - [+] ag-announcement-banner — _emitBadge > emits correct count with partial dismissals
  - [+] ag-announcement-banner — _emitBadge > emits count=N when nothing is dismissed

**js/components/molecules/ag-config-card.test.js**

  - [+] handleEdit > dispatches a bubbling edit-config event with the service id
  - [+] handleEdit > stops propagation so the tile click does not also fire
  - [+] provisioning state defaults > defaults provisionable and configured to false
  - [+] missing package > greys the tile out, like the Services and Profiles tabs do
  - [+] missing package > says the package is absent rather than leaving the tile blank
  - [+] missing package > points at the tab where the package is installed
  - [+] missing package > keeps the explanation out of the faded part of the tile
  - [+] missing package > drops the badges that would describe a service that is not there
  - [+] missing package > disables editing and downloading a file that is not there
  - [+] missing package > keeps the tile usable when the backend did not say either way
  - [+] package removed but its configuration file left behind > still says the package is gone
  - [+] package removed but its configuration file left behind > does not claim the file does not exist
  - [+] package removed but its configuration file left behind > keeps the file downloadable — it is on the box, whatever became of the package
  - [+] package removed but its configuration file left behind > still refuses to configure software that is not there
  - [+] package removed but its configuration file left behind > does not fade the buttons it deliberately left working
  - [+] installed service whose configuration file is missing > does not mark the tile unavailable
  - [+] installed service whose configuration file is missing > still reports what systemd says about the service
  - [+] installed service whose configuration file is missing > leaves the editor open so the file can be created
  - [+] installed service whose configuration file is missing > treats an unknown file state as present rather than disabling anything
  - [+] systemd state > shows a stopped service as stopped instead of showing nothing
  - [+] systemd state > shows a failed service as failed

**js/components/molecules/ag-highresaudio-output.test.js**

  - [+] AgHighresaudioOutput render > shows the login form when disconnected
  - [+] AgHighresaudioOutput render > shows connected card with name and username when connected
  - [+] AgHighresaudioOutput render > says next to the account that it can play its purchases only
  - [+] AgHighresaudioOutput render > reads an absent flag as a subscription — a core that predates the field
  - [+] AgHighresaudioOutput keeps the store honest about the account > a sign-in seeds the store with the POST body — the GET the browse would pay is already answered
  - [+] AgHighresaudioOutput keeps the store honest about the account > not after a sign-in that failed — nothing changed
  - [+] AgHighresaudioOutput keeps the store honest about the account > a sign-out forgets the whole account, not just the connection
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
  - [+] AgHqplayerOutput._toggleOutput — server-side setting > reverts the switch when the call fails (0.01s)
  - [+] AgHqplayerOutput._toggleOutput — one write at a time > ignores a second flip while the first is still in flight
  - [+] AgHqplayerOutput._toggleOutput — one write at a time > accepts the next flip once the first has settled
  - [+] AgHqplayerOutput._toggleOutput — one write at a time > releases the lock even when the call fails
  - [+] AgHqplayerOutput._renderDsp — volume label > prints the volume rounded to the slider step, not the float32 artifact
  - [+] AgHqplayerOutput._renderDsp — volume label > shows 0.0 dB when the status has no volume yet

**js/components/molecules/ag-hra-search-filters.test.js**

  - [+] ag-hra-search-filters > carries the seven criteria HRA takes, under their own parameter names
  - [+] ag-hra-search-filters > reads as empty until something is set
  - [+] ag-hra-search-filters > does not count a field holding only spaces
  - [+] ag-hra-search-filters > says nothing while the form is being filled in
  - [+] ag-hra-search-filters > announces the whole form when it is applied
  - [+] ag-hra-search-filters > counts what was applied, not what is typed
  - [+] ag-hra-search-filters > clearing announces itself too, so the results stop being narrowed
  - [+] ag-hra-search-filters > keeps Clear reachable once fields are emptied by hand after a search
  - [+] ag-hra-search-filters > clearing an untouched form says nothing
  - [+] ag-hra-search-filters > clearing a form emptied by hand still announces, the search still being narrowed
  - [+] ag-hra-search-filters > fetches the option lists on the first opening, and only then
  - [+] ag-hra-search-filters > never asks at all for someone who does not open the form
  - [+] ag-hra-search-filters > asks again after an answer that came back empty
  - [+] ag-hra-search-filters > offers format, mood and order — the fields their own application offers
  - [+] ag-hra-search-filters > lists an option carrying no family alongside the ones that do
  - [+] ag-hra-search-filters > offers neither album nor genre
  - [+] ag-hra-search-filters > shows nothing but the toggle until it is opened

**js/components/molecules/ag-lib-tabbar.test.js**

  - [+] ag-lib-tabbar > renders one labelled tab per destination, radio included (0.07s)
  - [+] ag-lib-tabbar > marks only the active tab (0.02s)
  - [+] ag-lib-tabbar > announces every tap, including one on the tab already highlighted (0.01s)
  - [+] ag-lib-tabbar > keeps the newly active tab in view, animated after the first render (0.01s)
  - [+] ag-lib-tabbar > does not scroll when a re-render is not a tab change
  - [+] ag-lib-tabbar > syncScroll repositions instantly — for a bar that just became visible
  - [+] ag-lib-tabbar > is wired: the page resyncs the visible bar on every view switch
  - [+] ag-lib-tabbar > gives the custom element itself the flex properties, not just .lib-nav

**js/components/molecules/ag-library-list-row.test.js**

  - [+] ag-library-list-row — the cover cell > keeps the row height and doubles the width for a banner (0.05s)
  - [+] ag-library-list-row — the cover cell > is a square cell of the usual size otherwise
  - [+] ag-library-list-row — the cover cell > gives the cover column no width of its own, so the cell decides
  - [+] ag-library-list-row — the trailing controls > puts the star and the + in one cell, so the row stays on three items (0.03s)
  - [+] ag-library-list-row — the trailing controls > adds no empty cell to a row that carries neither
  - [+] ag-library-list-row — the trailing controls > keeps the grid at three columns

**js/components/molecules/ag-library-scan-indicator.test.js**

  - [+] ag-library-scan-indicator > renders nothing while idle (0.02s)
  - [+] ag-library-scan-indicator > shows the indexing row once a scan is observed (0.03s)
  - [+] ag-library-scan-indicator > flashes "indexed" then hides when the scan completes
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
  - [+] _priceDisplay — price formatting > formats a valid numeric price
  - [+] _priceDisplay — price formatting > hands back a non-numeric price verbatim — it does not sanitise
  - [+] _priceDisplay — price formatting > hands back null unchanged
  - [+] the purchase sentence — price as text node > embeds a valid price string correctly
  - [+] the purchase sentence when the licence server gives no price > keeps a whole sentence — no dangling comma (0.10s)
  - [+] the purchase sentence when the licence server gives no price > states the price when there is one (0.02s)
  - [+] the purchase sentence when the licence server gives no price > states the price once, not again in the steps (0.02s)
  - [+] the purchase sentence when the licence server gives no price > renders a hostile price as inert text (0.03s)
  - [+] the purchase sentence when the licence server gives no price > states the price in the steps once the trial has ended (0.01s)
  - [+] the trial tile says the day count once > keeps the badge and the bar caption, drops the relayed sentence (0.01s)
  - [+] the trial tile says the day count once > still relays the message for a state the tile does not otherwise explain (0.01s)

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

**js/components/molecules/ag-package-card.test.js**

  - [+] ag-package-card — availability > says nothing when the package is available (0.06s)
  - [+] ag-package-card — availability > stays silent for a core that does not send the field yet
  - [+] ag-package-card — availability > explains a package blocked by a conflicting one (0.01s)
  - [+] ag-package-card — availability > marks an unreachable source as unknown, not as incompatible
  - [+] ag-package-card — availability > marks a genuinely unsupported package as an error
  - [+] ag-package-card — availability > does not repeat itself: no bare "Not Supported" badge next to the banner (0.02s)
  - [+] ag-package-card — availability > keeps the plain badge when the architecture alone is the reason
  - [+] ag-package-card — availability > falls back to a generic sentence when the core sends no reason
  - [+] ag-package-card — availability > does not blame the vendor for a local conflict with no reason attached
  - [+] ag-package-card — availability > stays neutral for a state it does not know yet
  - [+] ag-package-card — availability > keeps a compact signal on an installed package the box cannot install (0.02s)
  - [+] ag-package-card — availability > says nothing on an installed package, whatever the verdict (0.02s)
  - [+] ag-package-card — actions > offers a disabled INSTALL for something unavailable and not installed
  - [+] ag-package-card — actions > offers no UNINSTALL on a package the box cannot work without
  - [+] ag-package-card — actions > offers REPAIR when a required package failed while installed (0.02s)
  - [+] ag-package-card — actions > offers no REPAIR on a required package that is simply installed
  - [+] ag-package-card — actions > still offers UNINSTALL on everything else
  - [+] ag-package-card — actions > keeps UPDATE and UNINSTALL on an installed package the core marks unavailable
  - [+] ag-package-card — actions > offers a retry after a failed install, not actions on absent software
  - [+] ag-package-card — actions > leaves a way out after a failed operation
  - [+] ag-package-card — actions > still offers INSTALL normally when everything is fine
  - [+] ag-package-card — configuration state > says so when AG has not written the configuration
  - [+] ag-package-card — configuration state > says nothing once it is configured
  - [+] ag-package-card — configuration state > says nothing when the state could not be read
  - [+] ag-package-card — configuration state > says nothing about a package that is not installed (0.01s)
  - [+] ag-package-card — configuration state > says nothing about a package AG does not drive

**js/components/molecules/ag-prov-library-picker.test.js**

  - [+] payloadFor > manual path → music_directory
  - [+] payloadFor > manual empty/whitespace → null
  - [+] payloadFor > usb source → library_usb_uuid + fstype
  - [+] payloadFor > mount source → music_directory
  - [+] payloadFor > no choice → null
  - [+] payloadFor > out-of-range source index → null
  - [+] the deliberate "no library" choice > sends an EMPTY path, not an absent field
  - [+] the deliberate "no library" choice > is usable, unlike "nothing chosen yet"
  - [+] the deliberate "no library" choice > reaches the request as an explicit empty path
  - [+] the deliberate "no library" choice > ignores a manual path left behind in the field
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

**js/components/molecules/ag-roon-status.test.js**

  - [+] what each state says > names the missing endpoint and where to install it
  - [+] what each state says > tells the owner to check their Core when nothing answers
  - [+] what each state says > says where to click, and under which name, while waiting
  - [+] what each state says > carries the name the box reports, not one written into the interface
  - [+] what each state says > counts the zones once connected, in the singular when there is one
  - [+] what it refuses to say > never leaves the panel blank on a state it does know
  - [+] what it refuses to say > says nothing about a state it does not recognise
  - [+] what it refuses to say > says nothing when the box could not be reached at all
  - [+] what it refuses to say > shows a checking line only while the first answer is pending
  - [+] refresh > keeps the last known state when a request fails
  - [+] refresh > tells the card when a session comes up, so it can load the zones
  - [+] refresh > bypasses the cache when the owner says they have just enabled it
  - [+] while the box is still trying > shows the checking state the box reports
  - [+] while the box is still trying > looks again by itself, once, rather than staying on "Checking" for good
  - [+] while the box is still trying > gives up looking on its own rather than polling the box for ever
  - [+] while the box is still trying > starts looking again when the owner asks
  - [+] while the box is still trying > arms nothing once the card has been collapsed mid-request
  - [+] while the box is still trying > stops looking when the card goes away

**js/components/molecules/ag-rt-monitor.test.js**

  - [+] ag-rt-monitor — _load array coercion > keeps an array response as-is
  - [+] ag-rt-monitor — _load array coercion > coerces an undefined response to [] (no .map crash)
  - [+] ag-rt-monitor — _load array coercion > coerces a non-array object response to []
  - [+] ag-rt-monitor — _load array coercion > leaves _processes an array and records the error when apiGet throws

**js/components/molecules/ag-service-card.test.js**

  - [+] a figure nobody measured > is a dash on the tile
  - [+] a figure nobody measured > is a dash in the tooltip too, where a zero used to creep back in
  - [+] a figure nobody measured > draws no sparkline for it — while CPU keeps its own
  - [+] a figure nobody measured > opens no expanded chart for it, even when everything is expanded
  - [+] a figure that was measured > is printed, with its sparkline
  - [+] a figure that was measured > still expands
  - [+] a figure that was measured > keeps a genuine zero as a zero — an idle service reads nothing

**js/components/molecules/ag-service-detail-modal.test.js**

  - [+] a figure nobody measured > is a dash for memory, not a zero
  - [+] a figure nobody measured > is a dash for the network rates too
  - [+] a figure that is genuinely zero > stays a zero — a stopped service reads nothing, and says so
  - [+] a figure that is genuinely zero > prints real figures unchanged

**js/components/molecules/ag-tabs.test.js**

  - [+] ag-tabs — drag transform cleanup > _clearDragTransform > removes the inline transform from the sidebar and the toggle button
  - [+] ag-tabs — drag transform cleanup > _clearDragTransform > also resets the config modal when present
  - [+] ag-tabs — drag transform cleanup > _clearDragTransform > is safe when the toggle button is not present
  - [+] ag-tabs — drag transform cleanup > _handleTouchMove — edge-swipe turned vertical > clears the inline transform instead of leaving it stuck
  - [+] ag-tabs — drag transform cleanup > _handleTouchEnd — ends with no active/opening drag > clears any orphaned transform before the early return
  - [+] ag-tabs — licence gating > blocks the licensed tabs on Starter
  - [+] ag-tabs — licence gating > leaves the config tab open on Starter
  - [+] ag-tabs — licence gating > blocks nothing once licensed

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

**js/components/molecules/ag-volume-popover.test.js**

  - [+] ag-volume-popover live-value release > shows the dragged value while the hold lasts (0.12s)
  - [+] ag-volume-popover live-value release > falls back to the prop after the hold — a refused volume snaps back (0.01s)
  - [+] ag-volume-popover live-value release > is invisible when the change was confirmed before the release
  - [+] ag-volume-popover live-value release > rearms on every interaction — no snap-back mid-drag
  - [+] ag-volume-popover live-value release > step buttons hold and release the same way
  - [+] ag-volume-popover live-value release > closing releases immediately and cancels the timer
