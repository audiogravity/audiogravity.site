# DSD on a Linux streamer: native, DoP, or converted to PCM

**Short answer:** DSD reaches a DAC in one of three ways. *Native*, as DSD itself. *DoP*, DSD
wrapped in PCM words that the DAC unwraps. Or *converted to PCM*, which any DAC plays but which is
no longer DSD. Native needs a USB DAC whose Linux driver exposes DSD. DoP needs a DAC that decodes
it: one that does not receives PCM full of markers. And a DAC board on the Raspberry Pi's pins
cannot take native DSD at all.

## The three ways, as the DAC sees them

Measured on my test box (2026-10-17) with a DSD128 file and a USB DAC that accepts native DSD:

| Sent as | What the DAC receives (`hw_params`) |
|---|---|
| Native DSD | `format: DSD_U32_BE`, `rate: 176400` |
| DoP | `format: S32_LE`, `rate: 352800` |

- **Native** carries 32 bits of DSD per sample, so DSD128 needs 176.4 kHz and DSD256 352.8 kHz.
- **DoP** carries 16 bits of DSD in each 24-bit word, the other 8 being the marker. So it needs
  twice the rate: 176.4 kHz for DSD64 and 352.8 kHz for DSD128 (the DoP standard), and 705.6 kHz
  for DSD256. On a card that stops at 384 kHz, like the one measured above, DSD256 fits natively
  (352.8 kHz) but not as DoP (705.6 kHz).
- **Converted to PCM** works with any DAC, at the cost of what DSD was chosen for.

## What decides it on Linux

**A USB DAC.** The USB audio standard has no flag for "this device accepts DSD", so Linux keeps a
list of the DACs known to, plus a generic detection that catches many others. The list grows with
each kernel version: a recent DAC may need a newer kernel for native DSD. What your DAC accepts
is one command away, with the DAC free and its card number in place of `0`:

```bash
aplay -D hw:0,0 --dump-hw-params -d 1 -f S32_LE -r 44100 -c 2 /dev/zero
```

It plays one second of silence and lists what the card takes. The DAC measured above answers
`FORMAT: S32_LE SPECIAL DSD_U32_BE` and `RATE: [44100 384000]`: native DSD, PCM up to 384 kHz.
A `DSD_…` format in that list means native DSD is possible.

**A DAC board on the Pi's pins.** The Pi's I2S drivers, on the Pi 4 and the Pi 5 alike, offer PCM
only: 16, 24 or 32 bits, up to 384 kHz. Native DSD cannot pass. DoP can, if the board's chip
decodes it, up to DSD128: 352.8 kHz fits under 384 kHz, the 705.6 kHz of DSD256 does not. Boards
built on a chip that does not decode DSD, such as the PCM5122 of the HiFiBerry DAC+ Pro, play
DSD only once converted to PCM.

**MPD**, which many Linux streamers play through, decides in this order: native when the card
accepts it, DoP only if its `dop` option says `yes` (it has no way of knowing whether the DAC
decodes DoP), and otherwise a conversion to PCM. One trap: `dsd_usb` is the name `dop` had until
MPD 0.18, and MPD still reads it as the same option. With `dsd_usb "yes"`, DSD leaves as DoP even
beside `dop "no"`: that is the pair behind the second row of the table above.

**Roon** decides with its own *DSD Playback Strategy* setting, *Convert to PCM* by default (see
[Roon on a Raspberry Pi](roon-raspberry-pi)).

## Volume and DSD

A DSD stream cannot be turned down in software without converting it. On DoP, a digital volume
would also alter the markers, and the DAC would no longer recognise DSD. Play DSD at full digital
level and set your level on the amplifier, or on the DAC if it has its own volume.

## With Audiogravi<sup>ty</sup>

From version 0.9.74, the configuration Audiogravi<sup>ty</sup>'s guided setup writes for MPD
leaves DoP off: DSD goes out natively to a DAC that accepts it, and MPD converts it to PCM for one
that does not. Nothing reaches a DAC in a form it may not decode.

- **Boxes set up by an earlier version** had DoP on, through the old `dsd_usb` line. The update
  removes that line where it sits beside `dop "no"`, keeps the previous file among the
  configuration editor's saved copies, and restarts MPD.
- **A DAC that decodes DoP but not native DSD under Linux** can still have DoP: turn on **Send DSD
  as DoP** in MPD's **Guided** view, under **Config**. It is set on the DAC MPD plays on, and MPD
  takes it without a restart.
- **The player says how DSD reaches the DAC**: nothing more when it arrives as DSD, a **DoP** tag,
  or a warning when MPD converted it to PCM.
- **The player's volume does nothing to DSD.** I measured it on MPD 0.24.5: its volume at 30, then
  at 5, changed neither the level nor the DoP of a DSD128 track, and a DSD it converted to PCM came
  out byte for byte the same at 100 and at 30. The volume control gives way to a padlock while DSD
  plays: set your level on the amplifier.
- **Your DAC's own volume goes to full while it receives DSD.** On the USB DAC of my test box, that
  volume lowered by 10 dB silenced DoP and turned native DSD to noise. So while a DSD track reaches
  the DAC as DSD or as DoP, from any player, Audiogravi<sup>ty</sup> sets the DAC's volume to
  maximum, then puts it back. For a DAC that lowers DSD properly, turn off **Full DAC volume during
  DSD** in MPD's **Guided** view.
- **Through HQPlayer, DSD is never converted behind your back.** A file HQPlayer cannot read in
  DSD, a DST-compressed DFF, is refused with the reason.

The details are in the manual:
[Listening](../manual/04-listening), and
[Outputs & engines → What can and cannot go through HQPlayer](../manual/06-outputs-engines#what-can-and-cannot-go-through-hqplayer).

## Sources

- The DoP standard, version 1.1: [DoP open standard](https://dsd-guide.com/sites/default/files/white-papers/DoP_openStandard_1v1.pdf), 2012.
- Linux and native DSD over USB: [sound/usb/quirks.c](https://github.com/torvalds/linux/blob/master/sound/usb/quirks.c), [sound/usb/format.c](https://github.com/torvalds/linux/blob/master/sound/usb/format.c).
- The Pi's I2S drivers: [bcm2835-i2s.c](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/sound/soc/bcm/bcm2835-i2s.c), [dwc-i2s.c](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/sound/soc/dwc/dwc-i2s.c).
- MPD and DSD, version 0.24.5: [user manual](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/user.rst), and `dsd_usb` read as `dop`: [AlsaOutputPlugin.cxx](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/src/output/plugins/AlsaOutputPlugin.cxx).
- Roon's DSD setting: [audio setup basics](https://help.roonlabs.com/portal/en/kb/articles/audio-setup-basics).
