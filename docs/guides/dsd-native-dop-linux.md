# DSD on a Linux streamer: native, DoP, or converted to PCM

**Short answer:** DSD reaches a DAC in one of three ways. *Native*, as DSD itself. *DoP*, DSD
wrapped in PCM words that the DAC unwraps. Or *converted to PCM*, which any DAC plays but which is
no longer DSD. Native needs a USB DAC whose Linux driver exposes DSD. DoP needs a DAC that decodes
it: one that does not receives PCM full of markers, heard as noise. And a DAC board on the
Raspberry Pi's pins cannot take native DSD at all.

Checked on 2026-10-17 and 18 on Debian 13 with a USB DAC that takes native DSD, and on a Raspberry
Pi 4 with a HiFiBerry DAC+ Pro, with MPD 0.24.5 and 0.24.4; the Linux and MPD source code, read on
2026-10-21.

## The three ways, as the DAC sees them

Measured with a DSD128 file and a USB DAC that accepts native DSD:

| Sent as | What the DAC receives |
|---|---|
| Native DSD | `format: DSD_U32_BE`, `rate: 176400` |
| DoP | `format: S32_LE`, `rate: 352800` |

- **Native** packs 32 bits of DSD into each sample: DSD64, DSD128 and DSD256 need 88.2, 176.4 and
  352.8 kHz.
- **DoP** carries 16 bits of DSD in each 24-bit word, the other 8 being the marker, so it needs
  twice the rate: 176.4, 352.8 and 705.6 kHz. On a card that stops at 384 kHz, like the one above,
  DSD256 fits natively but not as DoP.
- **Converted to PCM** works with any DAC, at the cost of what DSD was chosen for.

## Check your DAC

What it accepts, with nothing playing on it, and its card number, from `aplay -l`, in place of
`0`:

```bash nocopy
aplay -D hw:0,0 --dump-hw-params -d 1 -f S32_LE -r 44100 -c 2 /dev/zero
```

It plays one second of silence and lists what the card takes. A `DSD_…` format in the list means
native DSD is possible: the DAC above answers `FORMAT: S32_LE SPECIAL DSD_U32_BE` and
`RATE: [44100 384000]`.

What it receives, while a DSD track plays:

```bash nocopy
cat /proc/asound/card0/pcm0p/sub0/hw_params
```

A `DSD_…` format means native DSD. A PCM format can be DoP or a conversion: DSD128 reached the USB
DAC above as DoP, and the HiFiBerry board as converted PCM, both as `S32_LE` at 352.8 kHz. The
DAC's own display, which says DSD or PCM, or the player's log, tells them apart.

## What decides it on Linux

**A USB DAC.** A DAC cannot say plainly that it takes DSD: the USB audio standard only lets it
declare "raw data". So Linux recognises native DSD on a list of DACs by model, and on the
raw-data devices of a list of makers, the XMOS- and Thesycon-based interfaces among them. Both
lists grow with each kernel version: a recent DAC may need a newer kernel for native DSD.

**A DAC board on the Pi's pins.** The Pi's I2S drivers, on the Pi 4 and the Pi 5 alike, offer PCM
only: 16, 24 or 32 bits, up to 384 kHz. Native DSD cannot pass. DoP can, if the board's chip
decodes it, up to DSD128: 352.8 kHz fits under 384 kHz, the 705.6 kHz of DSD256 does not. Boards
built on a chip that does not decode DSD, such as the PCM5122 of the HiFiBerry DAC+ Pro, play DSD
only once converted to PCM.

## The setting in MPD

MPD, the player of many Linux streamers, decides in this order: native when the card accepts it,
DoP only if the `dop` setting of its output says `yes`, and otherwise a conversion to PCM. MPD
cannot know whether a DAC decodes DoP, so it never chooses DoP by itself:

```text nocopy
audio_output {
    type    "alsa"
    name    "USB DAC"
    device  "hw:0,0"
    dop     "yes"
}
```

If DoP fails on the card, MPD falls back to native, or to a conversion. One trap: `dsd_usb` is the
name `dop` had until MPD 0.18, and MPD still reads it as the same setting. With `dsd_usb "yes"`,
DSD leaves as DoP even beside `dop "no"`.

## Volume and DSD

DSD cannot be turned down in software without becoming PCM, and on DoP a digital volume would
damage the markers. Set your level on the amplifier, or on the DAC if its own volume works on DSD.

- **MPD's software volume does nothing to DSD**, even when MPD converts it to PCM for a DAC that
  takes no DSD: with MPD 0.24.5, a DSD track came out the same at volume 100 and at 30.
- **To have MPD's volume act on DSD on a DAC that takes none**, a DAC board for instance, add
  `audio_output_format "*:32:*"` to `mpd.conf`: MPD then converts DSD as it decodes it, before the
  volume. It also widens all PCM to 32 bits, its values unchanged at full volume, and would turn
  native DSD into PCM too, so keep it for a box where no output takes DSD. On the Raspberry Pi 4 above, DSD64,
  DSD128 and DSD256 then reached the HiFiBerry board as 32-bit PCM at 352.8 kHz; the conversion took
  about 4, 37 and 69 % of one processor core.
- **A DAC's own volume may not work on DSD.** The USB DAC above, its volume lowered by 10 dB,
  played DoP as silence and native DSD as noise.

## With Audiogravi<sup>ty</sup>

- **The guided setup configures MPD native first**: DSD goes out natively to a DAC that takes it,
  and is converted for one that does not. For a DAC that decodes DoP but not native DSD under Linux,
  turn on **Send DSD as DoP (DSD over PCM)** in MPD's **Guided** view.
- **The player says how DSD reaches the DAC**: a **DoP** tag, or **Converted to PCM**.
- **Volume.** While the DAC receives DSD, the volume control gives way to a padlock, and the DAC's
  own volume goes to maximum, then back; **Full DAC volume during DSD** turns that off. On a box
  whose outputs take no DSD, MPD converts it before its volume, and the volume stays.

The details are in the manual: [Listening](../manual/04-listening).

## Sources

- The DoP standard, version 1.1: [DoP open standard](https://dsd-guide.com/sites/default/files/white-papers/DoP_openStandard_1v1.pdf), 2012.
- Linux 6.12 and native DSD over USB: [sound/usb/quirks.c](https://github.com/torvalds/linux/blob/v6.12/sound/usb/quirks.c) (the DACs by model, and the makers, in `snd_usb_interface_dsd_format_quirks`), [sound/usb/format.c](https://github.com/torvalds/linux/blob/v6.12/sound/usb/format.c) (the raw-data format).
- The Pi's I2S drivers: [bcm2835-i2s.c](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/sound/soc/bcm/bcm2835-i2s.c), [dwc-i2s.c](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/sound/soc/dwc/dwc-i2s.c). The PCM5122's formats: [Texas Instruments](https://www.ti.com/product/PCM5122), read on 2026-10-21.
- MPD 0.24.5: DSD in its [user manual](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/user.rst); `dop`, `dsd_usb` and the fallback in [AlsaOutputPlugin.cxx](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/src/output/plugins/AlsaOutputPlugin.cxx); the rename in its [NEWS](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/NEWS), version 0.19.
