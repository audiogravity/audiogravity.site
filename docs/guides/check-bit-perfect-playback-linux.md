# How to check bit-perfect playback on a Linux streamer

**Short answer:** playback is bit-perfect when every sample reaches the DAC exactly as it is in
the file. On a Linux streamer you can check most of it in two minutes, because the system
writes down the format the sound card receives. A matching format is necessary, not
sufficient: a digital volume control changes every sample and can leave the format as it was.

## What can change the samples

- **Resampling**: 44.1 kHz turned into 48 or 96 kHz.
- **Format conversion**: 24 bits cut to 16, or 16 bits widened to 24. Widening keeps each value
  and adds zeros below it: the DAC receives a longer word carrying the same music.
- **Digital volume** below 100 %: every sample is recalculated.
- **Mixing**: a sound server shared by several programs (PulseAudio, PipeWire, ALSA's `dmix`)
  brings everything to one common format.
- **Processing**: an equaliser, room correction, ReplayGain.
- **DSD turned into PCM**: if DSD cannot reach the DAC as DSD, a player may convert it to PCM
  rather than refuse it.

## Check 1: what the sound card receives

While a track plays, on the streamer:

```bash
cat /proc/asound/cards
cat /proc/asound/card1/pcm0p/sub0/hw_params
```

The first command lists the sound cards and their numbers: put your DAC's number in the second
(`card1` here). It answers with lines like these, or `closed` when nothing plays on that output:

```text nocopy
format: S32_LE
channels: 2
rate: 44100 (44100/1)
```

- **The rate must be the file's.** Any other rate means something resampled.
- **The format is the word the card receives**: `S16_LE` is 16 bits, `S24_3LE` and `S24_LE` are
  24, `S32_LE` is 32. A 16-bit file arriving as `S32_LE` has been widened: find out by what
  (check 2).
- **DSD sent as DSD shows a DSD format** (`DSD_U32_BE`, for instance). Sent as DoP, it shows
  PCM: DoP wraps DSD in 24-bit PCM words.

## Check 2: the player's settings

Many Raspberry Pi streamers play through MPD, Audiogravi<sup>ty</sup> among them, and MPD's own
manual keeps a check list for bit-perfect playback. In its configuration, the `audio_output` block that feeds your DAC:

- **`device "hw:1,0"`**, straight to the card. A `plughw:` or `default` device lets ALSA convert
  on the way.
- **No `mixer_type "software"`.** `none` leaves the samples alone, `hardware` hands the volume to
  the DAC. I measured what the software volume does on MPD 0.24.5 (2026-10-17): even at 100 %,
  it widens 16-bit audio to 24 bits in a 32-bit word. Every sample of a 20-second test file came
  out at exactly 256 times its value, the same music in a longer word; a 24-bit file came out
  byte for byte identical. Towards a DAC that accepts 16 bits only, MPD then brings that audio
  back to 16 bits with dither: at 100 % too, half the samples of a 3-second test came out
  changed, by up to 3 steps (2026-10-18). Below 100 %, MPD recalculates every sample.
- **No ReplayGain, no forced format** (`format`, `audio_output_format`).
- **For DSD**, MPD sends DSD natively when the sound card accepts it, uses DoP only if you set
  `dop "yes"`, and otherwise converts DSD to PCM. Check 1 shows which happened.

## Check 3: a file that only survives untouched

A matching format shows nothing was converted; it cannot show that the values were left alone.
Some audiophiles use a DTS-encoded CD track for that: played as ordinary PCM over a digital
link to an amplifier or processor that decodes DTS, it is recognised as DTS only if every bit
arrives unchanged. I have not run this test myself. If you try it, never play that file through
a DAC that does not decode DTS, and start with the volume low: undecoded, it is loud noise.

## What Audiogravi<sup>ty</sup> shows, and what it does not

- **The player shows the source**: codec, sample rate, bit depth. That is what the file is,
  not what the DAC receives.
- **The signal path shows the chain**, device by device, with the format on each link (Pipeline
  tab, Pro). A **FULL RES** badge marks a link where the formats match and the cable can carry
  them: on the link into the box's output, the source's rate and bit depth equal the sound
  card's; on the cable to your DAC, the connector can carry that format. It compares formats,
  not samples: it is not a proof of bit-perfect playback, and a volume at 90 % does not change it.
- **The configuration Audiogravi<sup>ty</sup>'s guided setup writes for MPD** sends each output
  straight to its card (`hw:`), with ALSA's conversions off (`auto_resample`, `auto_format`,
  `auto_channels` set to `no`), and a software volume. With it, 24-bit audio passes untouched at
  100 %, 16-bit audio is widened to 24 bits with its values unchanged — unless the DAC accepts
  16 bits only (check 2) — and below 100 % the samples are recalculated. For strict
  bit-perfect playback, leave the volume at 100 and set your listening level on the amplifier.
- **During DSD, the player's volume does nothing**: MPD leaves DSD untouched, whatever its
  volume. Audiogravi<sup>ty</sup> sets your DAC's own volume to maximum while the DAC receives
  DSD, then puts it back — some DACs play nothing, or noise, when that volume is lowered during
  DSD. A switch in MPD's **Guided** view turns this off for a DAC that lowers DSD properly.

The details are in the manual:
[Outputs & engines → The signal path](../manual/06-outputs-engines#the-signal-path-and-the-chain-you-describe),
and [Listening](../manual/04-listening).

## Sources

- MPD user manual, *Bit-perfect playback* and *Direct Stream Digital (DSD)*, version 0.24.5: [user.rst](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/user.rst).
- MPD's ALSA output settings, version 0.24.5: [plugins.rst](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/plugins.rst).
- MPD's software volume, version 0.24.5: [src/pcm/Volume.cxx](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/src/pcm/Volume.cxx).
