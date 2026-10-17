# HQPlayer NAA on a Raspberry Pi

**Short answer:** a Raspberry Pi makes a good NAA. HQPlayer does the heavy processing on a
computer elsewhere in the house and sends the result over the network; the Pi passes it to
your DAC, at almost no cost. Two things decide whether it works: the NAA must be on the same
major version as your HQPlayer, and with a USB DAC at the highest DSD rates, Signalyst
recommends a Pi 4 over a Pi 5.

## What an NAA does

HQPlayer's filters and modulators need a powerful processor, and a powerful processor is hot
and noisy: not something to put beside a DAC. NAA, Signalyst's Network Audio Adapter, splits
the work in two. HQPlayer runs on a computer anywhere on your network. The NAA runs next to the
DAC, receives what HQPlayer has already processed, and plays it. In HQPlayer's settings, you
choose the NAA as its output.

## Two ways to install it

Signalyst offers both on its download pages (checked on 2026-10-17):

- **A ready-made system image** for the Raspberry Pi, in versions 5.1.8, 6.1.2 and 6.1.4.
  Written to a microSD card, it turns the Pi into an NAA and nothing else.
- **A Debian package** (`networkaudiod`, for Debian 13 on arm64, from 5.1.5 to 6.1.4). It
  installs on Raspberry Pi OS or Debian 13 like any other program, beside your other players.

## What to get right

- **The same major version as HQPlayer.** HQPlayer 5 plays to an NAA 5, HQPlayer 6 to an NAA 6.
  I measured it: an NAA 6 does not work with HQPlayer 5. Signalyst publishes both lines side by
  side, so the newest file on the page is not always the one you need.
- **A Pi 4 or a Pi 5 for a USB DAC.** Jussi Laako, who writes HQPlayer, on the Roon forum:
  "There are some hardware/OS issues with RPi5 and 48k x512 and higher output rates" (March
  2024). The problem is specific to USB output; up to 44.1 kHz × 512 or 705.6 kHz PCM, it
  should work (May 2024). In November 2024 he still saw a problem with 48k × 512 DSD, and found
  the Pi 4 more reliable. I have not measured it.
- **It holds the DAC only while HQPlayer plays.** Measured on my x86 test box with a USB DAC
  (2026-09-26): with the NAA running and HQPlayer idle, the DAC stays free and another player
  can use it; when HQPlayer plays, the NAA takes it; when HQPlayer stops, the DAC is free again
  within three seconds. An NAA can live beside your other players.
- **It costs almost nothing at rest.** On a Raspberry Pi 4, idle: 4 MB of memory and no
  measurable processor time (measured 2026-09-26, over 30 seconds).

## With Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup> installs Signalyst's own package on a Raspberry Pi running Debian 13
(Trixie), DietPi or Raspberry Pi OS included, and keeps it on the right line. HQPlayer, the NAA
included, comes with the Pro edition; the 30-day trial includes it.

1. In **Library → Sources**, connect your HQPlayer: its card finds it on the network. The box
   then knows which major version it runs.
2. In **Audio Software**, click **INSTALL** on the **HQPlayer NAA** card. The version offered
   is the one that matches the HQPlayer you are connected to, not simply the newest.
3. Switch to a profile that runs it. Each says what it starts: **HQPlayer NAA** alone, or
   **MPD + HQPlayer NAA**, **Roon Bridge + HQPlayer NAA**, **Roon Bridge + MPD + HQPlayer NAA**
   to keep other players beside it.
4. In HQPlayer, choose this NAA as the output.

From then on:

- **HQPlayer can be your output.** The **Use as output** switch on the HQPlayer card sends what
  you play from Audiogravi<sup>ty</sup> — your library, Qobuz, Tidal, HIGHRESAUDIO, internet
  radio, UPnP media servers — through HQPlayer and back to your DAC through the NAA. The signal
  path shows *Library → HQPlayer → NAA → your DAC*.
- **A pair that cannot work is refused, with the reason.** No HQPlayer configured, the NAA not
  running, or a major version that does not match: the switch and playback say which, naming the
  two versions, instead of playing silence.
- **Formats HQPlayer cannot read are converted on the way.** ALAC, AAC, OGG and others reach
  HQPlayer as FLAC, without loss; your own files are never touched. DSD is never converted.
- **Updates follow your HQPlayer.** The NAA stays on the line of the HQPlayer you are connected
  to; with no HQPlayer answering, the line already installed is kept.

The details are in the manual:
[Outputs & engines → HQPlayer](../manual/06-outputs-engines#hqplayer), and
[Administration → Audio Software](../manual/07-administration#audio-software).

## Sources

- Signalyst downloads, [signalyst.com](https://signalyst.com/), checked on 2026-10-17.
- Jussi Laako on the Raspberry Pi 5 as an NAA: [HQPlayer NAA on Raspberry Pi 5](https://community.roonlabs.com/t/hqplayer-naa-on-raspberry-pi-5/269171), Roon Community, March to November 2024.
