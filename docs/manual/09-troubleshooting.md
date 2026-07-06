# 9. Troubleshooting

Most issues come down to a service that isn't running, an output that points at the
wrong device, or a network hop that's flaky. Audiogravi<sup>ty</sup> surfaces all three in the
interface.

## No sound / wrong output

- Check the **output selector** — is the right destination (Local DAC vs a network
  renderer) selected?
- In **Config**, confirm the service's **audio output** badge points at your DAC. If
  the card index drifted after a hardware change, re-run **Guided → output** (the DAC
  index is normally pinned automatically — see [3. First run](03-first-run.md)).
- In **Services**, confirm the relevant service (mpd, shairport-sync…) is **RUNNING**.

## A service won't start

- Open **Services** → click the service name for its detail modal (live metrics + the
  session action history), then **restart** it.
- If a **Systemd** tuning override made it unstable, use **Restore Backup** or **Remove
  Override** on the Systemd tab to roll it back to factory behaviour instantly.
- For deeper output, use the browser **Terminal** (System tab, admin) — e.g.
  `systemctl status mpd` / `journalctl -u mpd -e`.

## Streaming fails or a track won't play

- Confirm the service is **Connected** in Library → Sources, and that your
  **subscription** covers Hi-Res (see [5. Library & streaming](05-library-streaming.md)).
- A track that played before but fails later is usually an **expired streaming link** —
  Audiogravi<sup>ty</sup> refreshes these automatically; retry the track.
- **HIGHRESAUDIO** allows a single active device — if it signed out, reconnect.

## Casting to a renderer stalls

- Check the renderer is reachable on the LAN and appears in the output selector.
- Network renderers depend on your local network — run the **Network Test**
  (Performance tab) to check jitter/loss.

## Audio glitches / dropouts

- Watch for a **THROTTLED** badge on a CPU core (Performance tab) — sustained thermal
  throttling causes glitches; improve cooling or ease the CPU governor.
- In the **RT process monitor**, audio processes should show **SCHED_FIFO / SCHED_RR**
  (green), not NON-RT (red). Apply the *Audio Optimized* preset on the Systemd tab.
- Run the **Latency test** (`cyclictest`) — a high max latency points at scheduling
  contention.

## Passkeys or push notifications unavailable

Passkeys (WebAuthn) and Web Push need Audiogravi<sup>ty</sup> reachable over a real HTTPS
**domain** — they do **not** work over a bare IP. Re-install the core with
`--public-url https://your.domain` (see [2. Installation](02-installation.md)).

## Version-mismatch banner

The interface and core are on different versions — update the other component. See
[8. Updating](08-updating.md).

## Getting help

- **Bug reports & questions** — [open an issue](https://github.com/audiogravity/audiogravity.site/issues).
- **Logs** — the System event log (in-app) and `journalctl -u ag-core-server` /
  `journalctl -u <service>` from the Terminal.
- More answers on the [website FAQ](https://audiogravity.app/#faq).
