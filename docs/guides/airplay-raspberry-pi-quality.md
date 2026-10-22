# AirPlay to a Raspberry Pi: what quality actually arrives

**Short answer:** on Linux, AirPlay is received by shairport-sync. In classic AirPlay, it always
gets CD quality: ALAC, 16 bits, 44.1 kHz, lossless, whatever the music's own resolution. In AirPlay
2, an iPhone, iPad or Mac sends most apps' music as lossy AAC at 48 kHz, according to
shairport-sync's author; only a HomePod mini or an Apple TV 4K sends lossless, at 24 bits and
48 kHz. Nothing above 48 kHz arrives. Raspberry Pi OS and Debian 13 ship the classic version.

Checked on 2026-10-22 against shairport-sync's documentation and source code — version 5.6.1, and
4.3.7 as Debian 13 ships it —, Debian's packages and Apple's pages, which do not say what AirPlay
carries; measured on two test boxes.

## What arrives

| AirPlay | Sent by | What arrives |
|---|---|---|
| Classic | any Apple device or app | ALAC, 16 bits, 44.1 kHz: lossless, CD quality |
| AirPlay 2, real time | Spotify's free tier, or a Mac's whole sound | ALAC, 16 bits, 44.1 kHz |
| AirPlay 2, buffered | most apps on an iPhone, iPad or Mac | AAC at 48 kHz, 44.1 on older systems: lossy |
| AirPlay 2, lossless | a HomePod mini or an Apple TV 4K playing the music itself | ALAC, 24 bits, 48 kHz |

- **Apple does not publish this.** The table comes from shairport-sync's documentation and from its
  author, Mike Brady, who reads what reaches his receiver (2026). Of higher resolutions he writes:
  "We don't know how to decipher higher resolutions"; 96 and 192 kHz are not received.
- **The Apple device chooses**, among the formats the receiver says it takes, and can switch from
  lossy to lossless during a stream.
- **When a HomePod mini or an Apple TV plays to several speakers**, all of them receive what the
  weakest takes.

## On Raspberry Pi OS or Debian

```bash
sudo apt install shairport-sync
shairport-sync -V
```

The second command says what you have. Debian 13's package, as installed on Raspberry Pi OS,
answers `4.3.7-libdaemon-OpenSSL-Avahi-ALSA-…`: classic AirPlay. A version built for AirPlay 2
carries `-AirPlay2` in that line.

Its settings are in `/etc/shairport-sync.conf`. The name Apple devices show, and the DAC it plays
on, with your card's number from `aplay -l`:

```text nocopy
general = {
    name = "Living room";
};
alsa = {
    output_device = "hw:0,0";
};
```

Then `sudo systemctl restart shairport-sync`.

- **Classic AirPlay** shows in the AirPlay list of iPhones, iPads and Macs, but cannot join other
  speakers for several rooms at once, and does not appear in the Home app.
- **AirPlay 2** needs shairport-sync built with `--with-airplay-2`, and its companion NQPTP, which
  Debian 13 does not have and which must have ports 319 and 320 to itself: shairport-sync's
  build guide gives the steps.

## What shairport-sync does to the sound

- **It keeps time.** To stay in step with the sender, it now and then adds or removes a frame.
  Its author: this "inevitably must degrade the audio fidelity, even if it is very hard to hear";
  the `All Sync PPM` figure of its statistics can stay at 0.0 for long periods on a well sorted
  system.
- **Its volume.** By default, shairport-sync lowers the level itself, and adds dither when it
  does. With `mixer_control_name` in its `alsa` section, the DAC's own volume does it instead. With
  `ignore_volume_control = "yes"`, the level stays at full: in its author's words, "a clean,
  unmodified stream of audio".
- **The rate sent to the DAC.** Version 4.3.7 picks the lowest rate the DAC takes, and the
  greatest bit depth; version 5 matches what arrives when it can. Measured on my test box, with
  shairport-sync 5.5 in classic AirPlay and its volume in software (2026-10-22): the output received
  44,100 Hz in 32-bit words, `S32_LE` in its `hw_params` (see
  [How to check bit-perfect playback](check-bit-perfect-playback-linux)).

## When it fails

- **`fatal error: could not establish a service on port 5000 -- program terminating. Is another
  instance of Shairport Sync running on this device?`** — a second shairport-sync on the same box.
  Measured with one already running.
- **`warning: The output device "hw:0,0" is busy and can't be used by Shairport Sync at
  present.`** —
  another player holds the DAC (see ["Device or resource busy"](device-or-resource-busy-dac)).
- **The Pi is not in the AirPlay list.** The Apple device and the Pi must be on the same network,
  not on a guest Wi-Fi or another VLAN.

## With Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup> installs the box system's shairport-sync, names the receiver after the box,
and sends it to the output you choose for it in the guided setup — another one than MPD's if you
like, the box's optical output for instance.

The details are in the manual:
[First run → Per-service outputs](../manual/03-first-run#per-service-outputs).

## Sources

- shairport-sync 5.6.1: [AIRPLAY2.md](https://github.com/mikebrady/shairport-sync/blob/5.6.1/AIRPLAY2.md), [CONFIGURATION FLAGS.md](https://github.com/mikebrady/shairport-sync/blob/5.6.1/CONFIGURATION%20FLAGS.md), [BUILD.md](https://github.com/mikebrady/shairport-sync/blob/5.6.1/BUILD.md), [GetTheBest.md](https://github.com/mikebrady/shairport-sync/blob/5.6.1/ADVANCED%20TOPICS/GetTheBest.md), the [sample settings](https://github.com/mikebrady/shairport-sync/blob/5.6.1/scripts/shairport-sync.conf), and its version line in [common.c](https://github.com/mikebrady/shairport-sync/blob/5.6.1/common.c); version 4.3.7's choice of rate in [audio_alsa.c](https://github.com/mikebrady/shairport-sync/blob/4.3.7/audio_alsa.c). Read on 2026-10-22.
- Mike Brady, shairport-sync's author, on what arrives: [March 2026](https://github.com/mikebrady/shairport-sync/discussions/2007#discussioncomment-16123386), [May 2026](https://github.com/mikebrady/shairport-sync/discussions/2208#discussioncomment-17063287); on volume and bit-perfect classic AirPlay: [May 2026](https://github.com/mikebrady/shairport-sync/discussions/2202#discussioncomment-16951175).
- Debian 13: the `shairport-sync` 4.3.7-1 package's [build options](https://sources.debian.org/data/main/s/shairport-sync/4.3.7-1/debian/rules), without AirPlay 2; `nqptp` [not in trixie](https://packages.debian.org/trixie/nqptp).
- Apple: [lossless audio in Apple Music](https://support.apple.com/en-us/118295), September 2026, which does not mention AirPlay.
