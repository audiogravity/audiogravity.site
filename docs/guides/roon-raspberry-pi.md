# Roon on a Raspberry Pi: Roon Bridge, and Roon through HQPlayer

**Short answer:** a Raspberry Pi makes a Roon endpoint, not a Roon Core. Roon Bridge, the part
that plays, runs on a 64-bit Pi; Roon Server, the Core that holds your library, does not: on Linux
it runs on x64 machines only. So the Pi plays what a Core elsewhere sends it: a PC, a Mac, a NAS. And to listen
through HQPlayer, the Pi needs HQPlayer's NAA rather than Roon Bridge.

Checked on 2026-10-17 against Roon's own help pages, and on 2026-10-22 against Roon's installer
for the 64-bit Pi; the sources are at the end.

## Roon Bridge, Roon Server and Roon Ready

- **Roon Server** is the Core: library, browsing, processing. Roon: "Roon Server for Linux runs on
  x64 platforms", and "ARM builds only support Output functions". Its recommended hardware is an
  Intel Core i3 or better, 4 GB of memory and an SSD.
- **Roon Bridge** is "a lightweight software package designed to do exactly one thing: add audio
  outputs to your Roon setup over the network". It runs on Linux x64, armv7hf and armv8 — armv8
  being a 64-bit Raspberry Pi.
- **Roon Ready** is not software you install: it is Roon's certification of devices that carry
  Roon's streaming technology, RAAT, in their own firmware. A Pi with Roon Bridge receives the same
  RAAT stream, without the certification.
- **Roon itself** costs $14.99 a month, $149.88 a year or $829.99 for life (US dollars, Roon's
  pricing page).

## Ways to turn a Pi into a Roon endpoint

- **Verox, formerly RoPieee.** A free system image dedicated to the job, for the Pi 3, 4 and 5:
  a Roon Bridge endpoint, plus AirPlay 2, Spotify Connect, an HQPlayer NAA and a UPnP renderer
  among others. RoPieee took the name Verox in September 2026; existing installations moved over
  with their settings.
- **Roon's own installer**, on Raspberry Pi OS or Debian, below.
- **A general-purpose streamer**: Volumio has a Roon Bridge plugin, and moOde manages Roon Bridge
  once you have installed it.

### With Roon's installer

On a 64-bit system, where `uname -m` answers `aarch64`. The installer needs `bzip2` to unpack
Roon Bridge:

```bash
sudo apt install bzip2
curl -O https://download.roonlabs.net/builds/roonbridge-installer-linuxarmv8.sh
chmod +x roonbridge-installer-linuxarmv8.sh
sudo ./roonbridge-installer-linuxarmv8.sh
```

It asks for a confirmation, then installs Roon Bridge in `/opt/RoonBridge`, keeps its data in
`/var/roon/RoonBridge`, and runs it as root, as the `roonbridge` service, started at every boot.
On a 32-bit system (`armv7l`), the same steps take `roonbridge-installer-linuxarmv7hf.sh`.

On DietPi, Roon Bridge is in its software list: `dietpi-software install 121` (DietPi 9.20).

## Roon through HQPlayer

Roon can send to HQPlayer, which then does the processing and plays to its own output: on a
Raspberry Pi next to the DAC, that output is HQPlayer's NAA (see
[HQPlayer NAA on a Raspberry Pi](hqplayer-naa-raspberry-pi)).

- **The Pi needs the NAA, not Roon Bridge.** Tested on 2026-09-26: Roon played through HQPlayer
  to the NAA with Roon Bridge stopped.
- **The two should not fight over the DAC.** Roon's help: "Both Roon and HQPlayer expect to have
  exclusive access to the device" — if HQPlayer uses a device, disable it in Roon's audio settings.
  HQPlayer's developer, Jussi Laako, said the same of a Roon Bridge left running beside an NAA on
  one machine: Roon takes the DAC unless that output is disabled in Roon.
- **In HQPlayer**, turn on "Allow control from network" so that Roon can drive it.

## DSD from Roon to a Linux endpoint

Roon's *DSD Playback Strategy* setting decides what reaches the endpoint. Its default is
*Convert to PCM*. Native DSD works on Linux when the system's driver exposes native DSD for your
DAC; otherwise Roon's help suggests trying *DSD over PCM (DoP)*.

## With Audiogravi<sup>ty</sup>

In its Pro edition, and during its 30-day trial, Audiogravi<sup>ty</sup> installs Roon Bridge
with Roon's own installer, from its **Audio Software** tab, and runs it through profiles that
say what they play, such as *Roon Bridge + HQPlayer NAA*: "Roon directly, or through HQPlayer
— one at a time". It also registers as a Roon extension: once you enable it in Roon, under
**Settings → Extensions**, your Roon zones and library appear beside your other sources.

The details are in the manual:
[Outputs & engines → Roon](../manual/06-outputs-engines#roon), and
[Library & streaming → Roon](../manual/05-library-streaming#roon).

## Sources

- Roon on Linux: [Linux install](https://help.roonlabs.com/portal/en/kb/articles/linux-install) (September 2026), and the installer itself, [roonbridge-installer-linuxarmv8.sh](https://download.roonlabs.net/builds/roonbridge-installer-linuxarmv8.sh), read on 2026-10-22; hardware recommendations: [Roon hardware specification recommendations](https://help.roonlabs.com/portal/en/kb/articles/faq-what-are-the-minimum-requirements) (September 2026); [software packages](https://help.roonlabs.com/portal/en/kb/articles/software-packages) (June 2026); [Roon Ready](https://help.roonlabs.com/portal/en/kb/articles/roon-ready); prices: [roon.app/en/pricing](https://roon.app/en/pricing), read on 2026-10-17.
- Roon and HQPlayer: [HQPlayer](https://help.roonlabs.com/portal/en/kb/articles/hqplayer) (June 2026). Jussi Laako on Roon Bridge beside an NAA: [Roon Community](https://community.roonlabs.com/t/176288/80), August 2022.
- Roon and DSD: [audio setup basics](https://help.roonlabs.com/portal/en/kb/articles/audio-setup-basics) (March 2026), [audio on Linux](https://help.roonlabs.com/portal/en/kb/articles/audio-on-linux).
- Verox: [verox.audio](https://verox.audio/), [release 2026.09](https://ropieee.org/stable/release/2026/09/26/release-2026.09.html), [installation](https://docs.verox.audio/installation/), read on 2026-10-17.
