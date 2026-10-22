# What your USB DAC accepts on Linux, and how to read it

**Short answer:** Linux writes down, for each USB DAC, every format and rate the DAC offers, in one
file per card. Read it before blaming a player: it says whether a 192 kHz or a DSD file can reach
your DAC as it is. The line above it says whether the DAC came up on a high-speed USB link: on a
full-speed link, 24-bit audio stops at 96 kHz.

Checked on 2026-10-22 on Debian 13 (Linux 6.12) with a USB DAC built on an XMOS interface, and
against the kernel's own sources.

## Find your DAC

```bash
lsusb
cat /proc/asound/cards
aplay -l
```

- **`lsusb`** lists what is plugged in, by name: `ID 20b1:30ab XMOS Ltd Heed Abacus`. The first
  four characters name the maker of the DAC's USB interface, here XMOS. If the DAC is missing,
  `sudo dmesg | tail` right after plugging it in says what Linux saw: a line such as
  `New USB device found, idVendor=20b1, idProduct=30ab` means it was seen. Nothing at all points
  to the cable, the port or the DAC's power.
- **`/proc/asound/cards`** lists the sound cards with their number, and a USB DAC with its link:
  `HEED Heed Abacus at usb-0000:00:14.0-8, high speed`.
- **`aplay -l`** lists the same cards, to an account allowed to use them. If it answers
  `aplay: device_list:279: no soundcards found...` while `/proc/asound/cards` lists your DAC, your
  account is not in the `audio` group: `sudo usermod -aG audio $USER`, then log in again.

## Read what it accepts

With your DAC's card number in place of `0`:

```bash nocopy
cat /proc/asound/card0/stream0
```

For the DAC above, shortened:

```text nocopy
HEED Heed Abacus at usb-0000:00:14.0-8, high speed : USB Audio

Playback:
  Status: Stop
  Interface 1
    Altset 1
    Format: S32_LE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ASYNC)
    Rates: 44100, 48000, 88200, 96000, 176400, 192000, 352800, 384000
    Bits: 32
  Interface 1
    Altset 2
    Format: SPECIAL DSD_U32_BE
    Channels: 2
    Endpoint: 0x01 (1 OUT) (ASYNC)
    Rates: 44100, 48000, 88200, 96000, 176400, 192000, 352800, 384000
    Bits: 32
```

- **One block per format.** `S32_LE` is PCM in 32-bit words; other DACs show `S24_3LE` (24 bits
  in three bytes) or `S16_LE`.
- **`Rates`** are the sample rates the DAC takes in that format. A file at a rate missing from the
  list cannot reach the DAC as it is: something has to resample it.
- **`SPECIAL DSD_U32_BE`** means Linux can send this DAC native DSD (see
  [DSD on a Linux streamer](dsd-native-dop-linux)).
- **`ASYNC`** means the DAC's own clock sets the pace. While it plays, the same file shows the
  clock as the computer sees it: `Momentary freq = 44101 Hz` for a 44.1 kHz stream, `192003 Hz`
  for 192 kHz, on the DAC above.

## When the list stops at 96 kHz

- **The link.** `lsusb -t` gives each device's speed: `480M` is high speed, as for the DAC above,
  `12M` is full speed. At full speed, the USB link carries at most 1,023 bytes of audio per
  millisecond: 24-bit stereo fits at 96 kHz, not at 176.4 kHz, which needs 1,058. A DAC shown at
  full speed in `/proc/asound/cards` is held back by its link, not by Linux.
- **The class.** `lsusb -v -d 20b1:30ab | grep bInterfaceProtocol`, with your DAC's two numbers:
  `32` on its audio interfaces means USB Audio Class 2, `0` means class 1. If your DAC's manual
  mentions a class 1 mode, for computers without a class 2 driver, make sure it is off.

## Settings copied from forums

Options for the USB audio driver sit in `/etc/modprobe.d/`, on `options snd_usb_audio …` lines.
To see which ones your kernel takes:

```bash
/sbin/modinfo -p snd_usb_audio
```

An option missing from that list does nothing, and the kernel log says so. On my test box, an old
`nrpacks=1` gives `snd_usb_audio: unknown parameter 'nrpacks' ignored`. The kernel's own
documentation still describes `nrpacks`: the list `modinfo` prints is the one that counts.

## With Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup> reads this same list to know whether your DAC takes DSD as DSD, and sets
MPD up accordingly. Its support report, **System › Actions › Support Report**, names each sound
card with the speed of its USB link.

The details are in the manual:
[Administration → Support report](../manual/07-administration#support-report).

## Sources

- Linux 6.12: the link speed in a card's name, in [sound/usb/card.c](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/sound/usb/card.c?h=v6.12); the USB Audio Class numbers in [include/uapi/linux/usb/audio.h](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/include/uapi/linux/usb/audio.h?h=v6.12); the full-speed limit of 1,023 bytes per isochronous packet in [drivers/usb/core/config.c](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/usb/core/config.c?h=v6.12); the USB audio driver's options in [Documentation/sound/alsa-configuration.rst](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/sound/alsa-configuration.rst?h=v6.12).
- The outputs shown: measured on 2026-10-22 on the test box, Linux 6.12.111, playing silence for the `Momentary freq` lines.
