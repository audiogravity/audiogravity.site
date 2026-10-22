# Software or hardware volume on a Linux streamer: what each does to your music

**Short answer:** you can turn the music down in three places. In the player, a software volume
recalculates every sample, except at 100 %. In the DAC, a hardware volume leaves the samples as the
player sent them, and the DAC lowers the level itself. On the amplifier, nothing digital is touched.
For bit-perfect playback, keep the player's volume at 100 or off. With DSD, a player's software
volume does nothing, and some DACs' own volume breaks it.

Measured on 2026-10-22 on Debian 13 with MPD 0.24.5 and a USB DAC built on an XMOS interface; the
16-bit and DSD cases on 2026-10-17 and 18.

## The three places

- **The player's software volume** multiplies every sample by a factor below one. The result is a
  new set of numbers: below 100 %, nothing reaches the DAC as it is in the file.
- **The DAC's hardware volume** is a control the DAC offers to the computer. The player sends the
  samples untouched and asks the DAC to lower the level; how the DAC does it, inside its chip or in
  its analogue stage, is up to the DAC.
- **The amplifier** comes after the DAC: the whole digital chain stays as it is.

## Does your DAC have a volume of its own

```bash nocopy
amixer -c 0 scontrols
amixer -c 0 sget 'Heed Abacus ',0
```

With your DAC's card number, from `aplay -l`, in place of `0`, and the name the first command
prints in the second. For the DAC above:

```text nocopy
Simple mixer control 'Heed Abacus ',0
Simple mixer control 'Heed Abacus ',1
  Limits: Playback 0 - 127
  Front Left: Playback 127 [100%] [0.00dB] [on]
```

It has two, from −127 dB to 0 dB in steps of 1 dB. A DAC that lists no control has no volume of
its own that Linux can set.

## In MPD

Each output of `/etc/mpd.conf` chooses its volume with `mixer_type`:

```text nocopy
audio_output {
    type           "alsa"
    name           "USB DAC"
    device         "hw:0,0"
    mixer_type     "hardware"
    mixer_device   "hw:0"
    mixer_control  "Heed Abacus "
    mixer_index    "0"
}
```

- **`hardware`** sets the DAC's own control. MPD looks for one named `PCM` unless told otherwise:
  copy the name `amixer` prints, between the quotes, spaces included, and its index when two share
  a name. A name MPD cannot find leaves the volume at `n/a`, and MPD's log says why:
  `Failed to read mixer for "USB DAC": no such mixer control: PCM` with no name given, `…: Heed
  Abacus` without the final space of the name above.
- **`software`** computes the volume in MPD.
- **`none`** leaves the level at full: set it on the amplifier.

By default, MPD uses the hardware volume of a device that has one, and none for the others.

## What MPD's software volume does

- **The slider is not in decibels.** Measured with a 1 kHz tone: 90 is −3.6 dB, 75 is −9.0 dB,
  50 is −18.5 dB, 25 is −29.8 dB, 10 is −41.1 dB and 1 is −60.2 dB, against 100.
- **At 100, 24-bit audio passes untouched.** 16-bit audio is widened to 24 bits, every value
  multiplied by 256: the same music in a longer word (see
  [How to check bit-perfect playback](check-bit-perfect-playback-linux)).
- **Below 100, every sample is recalculated.**

## DSD and volume

- **MPD's software volume does nothing to DSD**, even when MPD converts it to PCM for a DAC that
  takes no DSD: a DSD track came out the same at volume 100 and at 30.
- **A DAC's own volume may break DSD.** The DAC above, its volume lowered by 10 dB, played DoP as
  silence and native DSD as noise. With such a DAC, leave its volume at maximum while it receives
  DSD, and set the level on the amplifier (see [DSD on a Linux streamer](dsd-native-dop-linux)).

## With Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup>'s guided setup gives MPD its software volume: the player's slider is MPD's,
and at 100 your music reaches the DAC as described above. While the DAC receives DSD, the slider
gives way to a padlock, and the DAC's own volume goes to its maximum, then back; **Full DAC volume
during DSD**, in MPD's **Guided** view, turns that off for a DAC that lowers DSD properly.

The details are in the manual: [Listening](../manual/04-listening).

## Sources

- MPD 0.24.5: `mixer_type` in its [user manual](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/user.rst), `mixer_device`, `mixer_control` and `mixer_index` in its [plugins reference](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/plugins.rst).
- `amixer`: [amixer(1)](https://manpages.debian.org/trixie/alsa-utils/amixer.1.en.html), Debian 13.
- The slider's decibels: measured on 2026-10-22 with a private MPD 0.24.5 playing a 1 kHz tone to a pipe output, in floating point, with no sound card opened. The hardware volume's names and messages: a private MPD 0.24.5 reading the DAC's volume without setting it, the DAC's level the same before and after.
