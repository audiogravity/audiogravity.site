# “Device or resource busy”: two players, one DAC

**Short answer:** a player that opens a DAC directly has it to itself until it lets go. Any other
player that tries in the meantime gets "Device or resource busy" and plays nothing. That
exclusivity is what lets a player send your music untouched, so the fix is not to share the DAC:
it is to find which program holds it, and to have your players take turns.

Checked on 2026-10-22 on an x86 box under Debian 13, with MPD 0.24.5 and ALSA 1.2.14; the
measurements are dated where they appear.

## What it looks like

The words vary with the program; the cause does not. Two of them:

```text nocopy
aplay: main:850: audio open error: Device or resource busy
ERROR: Failed to open "USB DAC" (alsa); Failed to open ALSA device "hw:0,0": Device or resource busy
```

The first is what `aplay`, ALSA's own player, printed on my test box when another program held
the DAC (2026-10-17). The second is what `mpc status` showed when MPD met a DAC already in use
(2026-10-22), with the output's name and device from MPD's configuration. MPD's log has the same
line, and then `player: problems opening audio device while playing` with the track's name.

## Find who holds the DAC

On the streamer, list the sound cards, then read the state of yours (`card0` here; use your DAC's
number):

```bash
cat /proc/asound/cards
cat /proc/asound/card0/pcm0p/sub0/status
```

`closed` means nobody holds it. Otherwise the first lines say who does:

```text nocopy
state: RUNNING
owner_pid   : 1603814
```

That number is a process. Its name, and the service it belongs to:

```bash nocopy
cat /proc/1603814/comm
cat /proc/1603814/cgroup
```

For a player started as a service, the second answer ends with the service's name, such as
`/system.slice/mpd.service`.

## When each player lets go

Players do not all release the DAC at the same moment. Measured on my test boxes:

- **MPD 0.24.5** holds it while it plays and releases it less than a second after a pause or a
  stop (2026-10-17). Its `always_on` option changes that: the output is then paused instead of
  closed, and the DAC stays taken.
- **HQPlayer's NAA** takes it only while HQPlayer plays to it, and releases it within three
  seconds of a stop (2026-09-26).
- **HQPlayer Embedded**, without a licence, stops taking commands after half an hour but keeps
  running, and keeps the DAC (2026-09-22).

## The fixes

- **One player at a time.** Stop the one that holds the DAC, with `sudo systemctl stop` and the
  service's name found above, or stop running the players you do not use.
- **One output each.** A box with several outputs, a USB DAC and HDMI for instance, can give each
  player its own.
- **Not a mixer, on a hi-fi DAC.** ALSA's `dmix`, or a sound server such as PipeWire, lets several
  programs play at once, and the error goes away. But mixing brings every stream to one format:
  `dmix` runs at a single rate, 48 kHz unless you set another, so a 44.1 kHz or 96 kHz file is
  resampled on the way. Fine on a desktop; not what a streamer is for.

## With Audiogravi<sup>ty</sup>

Its profiles decide which players run, each named after what it starts: *MPD*, *Roon Bridge +
MPD*, *HQPlayer Embedded*… When MPD cannot open the DAC because another player holds it, the
player says so: *Output in use by another player — stop it to play here*.

The details are in the manual:
[Troubleshooting → No sound / wrong output](../manual/09-troubleshooting#no-sound--wrong-output),
and [Administration → Audio configuration](../manual/07-administration#audio-configuration-services--profiles).

## Sources

- MPD user manual, version 0.24.5, audio output setting `always_on`: [user.rst](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/user.rst); the message, in its ALSA output: [AlsaOutputPlugin.cxx](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/src/output/plugins/AlsaOutputPlugin.cxx).
- ALSA's `dmix` and its default rate: [Asoundrc](https://www.alsa-project.org/wiki/Asoundrc), ALSA project wiki, read on 2026-10-17, and `defaults.pcm.dmix.rate 48000` in `/usr/share/alsa/alsa.conf`, ALSA 1.2.14.
