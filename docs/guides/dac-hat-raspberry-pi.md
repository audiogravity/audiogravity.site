# A DAC HAT on a Raspberry Pi: why it is not detected, and the line that fixes it

**Short answer:** a DAC board stacked on the Pi's pins (HiFiBerry, Raspberry Pi DAC+, Allo…) is
not found on its own the way a USB DAC is. Linux creates its sound card once the Pi's boot
configuration names the board's *overlay*: one line in `/boot/firmware/config.txt`, then a reboot.
Some boards carry a memory chip that names it for you; many audio boards do not, or name one that
no longer works.

Checked on 2026-10-17 against Raspberry Pi's and HiFiBerry's documentation, and on my own
Raspberry Pi 4 with a HiFiBerry DAC+ Pro under Raspberry Pi OS (Debian 13).

## Why it is not automatic

At boot, the Pi's firmware looks for a memory chip on the board (an EEPROM) and loads the overlay
it names, "without any user intervention", in Raspberry Pi's words. That works when the chip is
there and up to date. With audio boards, it often is not:

- **No chip.** A board may have none: it can then not be called a HAT, but it works once declared.
- **An outdated chip.** HiFiBerry: on some of its cards, such as the DAC+ Pro, the configuration
  stored on the board "might not load correctly" with today's systems. Declare the board, and add
  `force_eeprom_read=0` so the firmware stops reading the chip.
- **Two versions of one board.** Raspberry Pi's own audio boards exist in green (Raspberry Pi) and
  black (IQaudIO): "electrically equivalent, but have different EEPROM contents".

My own Pi shows the result: the firmware reports no HAT at all (`/proc/device-tree/hat` is
absent), and the DAC+ Pro works because of one line in `config.txt`.

## The line for your board

On Raspberry Pi OS, the file is `/boot/firmware/config.txt`. On older images it was
`/boot/config.txt`, which now holds only a note saying the file has moved. Put the lines at the top
of the file, before any line in brackets such as `[pi4]`: what follows such a line applies to that
model only.

| Board | Line |
|---|---|
| HiFiBerry DAC+ Pro, DAC2 Pro | `dtoverlay=hifiberry-dacplus-pro` |
| HiFiBerry DAC+ Standard, Amp2, Amp4 | `dtoverlay=hifiberry-dacplus-std` |
| HiFiBerry DAC2 HD | `dtoverlay=hifiberry-dacplushd` |
| HiFiBerry DAC+ Light, DAC Zero, MiniAmp | `dtoverlay=hifiberry-dac` |
| HiFiBerry Digi+, Digi2 Standard | `dtoverlay=hifiberry-digi` |
| HiFiBerry Digi+ Pro, Digi2 Pro | `dtoverlay=hifiberry-digi-pro` |
| HiFiBerry DAC8x (Raspberry Pi 5 only) | `dtoverlay=hifiberry-dac8x` |
| Raspberry Pi DAC+, DAC Pro, DigiAMP+, Codec Zero (green boards) | `dtoverlay=rpi-dacplus`, `rpi-dacpro`, `rpi-digiampplus`, `rpi-codeczero` |
| IQaudIO DAC+ (black board) | `dtoverlay=iqaudio-dacplus` |
| Allo Boss | `dtoverlay=allo-boss-dac-pcm512x-audio` |
| Allo DigiOne | `dtoverlay=allo-digione` |

Check the name against your board maker's own documentation. The Pi holds the full catalogue, with
a description of each overlay, in `/boot/firmware/overlays/README`.

- **Pro and Standard are not interchangeable.** A HiFiBerry "Pro" board has its own clocks; its
  `-pro` line uses them. The Standard line on a Pro board still plays, but with the Pi driving the
  clock. The two names date from Linux 6.1.77; before that, both boards used `hifiberry-dacplus`.
- **Nothing else to switch on.** The overlay does all of it: no `dtparam=i2s=on` or
  `dtparam=i2c_arm=on` needed, as the Raspberry Pi kernel's maintainer put it.

## Turn the Pi's own audio off

With the Pi's own outputs still on, your DAC is one sound card among several. My Pi 4 has these two
lines beside the DAC's:

```text nocopy
dtparam=audio=off
dtoverlay=vc4-kms-v3d,noaudio
```

The first turns off the Pi's headphone jack and its basic HDMI audio; the second, the HDMI audio of
its display driver. The Raspberry Pi 5 has no headphone jack: there, `noaudio` is what keeps HDMI
from appearing as a sound card.

Changes take effect after a reboot.

## Check it

```bash
aplay -l
```

The board should appear under its own name. On my Pi:

```text nocopy
card 0: sndrpihifiberry [snd_rpi_hifiberry_dacplus], device 0: HiFiBerry DAC+ Pro HiFi pcm512x-hifi-0 [HiFiBerry DAC+ Pro HiFi pcm512x-hifi-0]
```

If it does not, check that the board is fully seated on the pins, then try `force_eeprom_read=0`.
To list sound cards, your account must belong to the `audio` group.

## Debian 13 without Raspberry Pi OS

Everything above is for Raspberry Pi OS. Debian's own image for the Raspberry Pi works
differently: `config.txt` is rewritten at every kernel or firmware update ("Do not modify this
file!"), lasting additions go in `/etc/default/raspi-firmware-custom`, and Debian ships only a
couple of overlays, `hifiberry-dac` among them. For most DAC boards, Raspberry Pi OS is the simpler
base.

## DSD on a DAC HAT

The Pi's I2S connection, the one these boards use, carries PCM only: up to 384 kHz in 16, 24 or 32
bits, in the drivers of the Pi 4 and the Pi 5 alike. Native DSD does not pass. A board whose chip
decodes DoP can still play DSD wrapped in PCM; the others, such as the PCM5122 of the HiFiBerry
DAC+ Pro, play PCM only.

## With Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup> lists the sound cards Linux exposes, so a DAC board appears once it is
declared. Then, in **Config → Guided**, choose it as the output: that writes it into each audio
service's configuration. Audiogravi<sup>ty</sup> does not edit `config.txt` for you; the manual
walks through it, with a backup first and what to do if the Pi does not come back:
[Troubleshooting → My DAC is not in the output list](../manual/09-troubleshooting#my-dac-is-not-in-the-output-list-raspberry-pi-hat).

## Sources

- Raspberry Pi documentation (GitHub copy, read on 2026-10-17): [config.txt location](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/config_txt/what_is_config_txt.adoc), [device trees and HATs](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/configuration/reference.adoc), [audio boards](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/accessories/audio/configuration.adoc), [HDMI audio](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/config_txt/audio.adoc).
- The overlays: [overlays README](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/overlays/README), Raspberry Pi kernel. Phil Elwell on `i2s` and `i2c_arm`: [raspberrypi/linux #5843](https://github.com/raspberrypi/linux/issues/5843), January 2024.
- HiFiBerry: [configuration](https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/) (February 2025), [changes in HiFiBerry drivers](https://www.hifiberry.com/blog/changes-in-hifiberry-drivers/) (March 2024).
- Debian's own image: the `raspi-firmware` package, [Debian archive](https://deb.debian.org/debian/pool/non-free-firmware/r/raspi-firmware/).
- The Pi's I2S drivers: [bcm2835-i2s.c](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/sound/soc/bcm/bcm2835-i2s.c) (Pi 4 and earlier), [dwc-i2s.c](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/sound/soc/dwc/dwc-i2s.c) (Pi 5).
