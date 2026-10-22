# HQPlayer NAA on a Raspberry Pi

**Short answer:** a Raspberry Pi makes a good NAA. HQPlayer does the heavy processing on a
computer elsewhere in the house and sends the result over the network; the Pi passes it to your
DAC, at almost no cost. It needs a licensed HQPlayer, and two things right: an NAA your HQPlayer
accepts — NAA 6 needs HQPlayer 5.16 or later — and, for a USB DAC at the highest rates, a Pi 4
rather than a Pi 5, as HQPlayer's author recommends.

Checked on 2026-10-21 against Signalyst's download pages, its NAA 6.1.4 package and image (read,
not run) and the statements of HQPlayer's author; measured on a Raspberry Pi 4 running NAA 5.1.8
(2026-10-21) and on a test box with a USB DAC (2026-09-26).

## What an NAA does

HQPlayer's filters and modulators need a powerful processor, and a powerful processor is hot
and noisy: not something to put beside a DAC. NAA, Signalyst's Network Audio Adapter, splits
the work in two. HQPlayer runs on a computer anywhere on your network. The NAA runs next to the
DAC, receives what HQPlayer has already processed, and plays it. The NAA's licence allows its use
"provided that you have a valid license for the Signalyst HQPlayer".

## Three ways to install it

### Signalyst's NAA OS image

Signalyst publishes one image per version, `naa-518`, `naa-612` and `naa-614`, each for the
Raspberry Pi 4 and 5 alike. Extract the `.img` file from the `.7z` archive and write it to a
microSD card of 4 GB or more, with balenaEtcher or `dd`. There is nothing to set up: the Pi takes
its address from your router on the Ethernet port — the image turns Wi-Fi and Bluetooth off — and
names itself. To update it, write the newer image.

### The package, on Raspberry Pi OS or Debian

Signalyst publishes the NAA as a Debian package, `networkaudiod`, beside your other players:

```bash nocopy
wget https://signalyst.com/bins/naa/linux/trixie/networkaudiod_6.1.4-71_arm64.deb
sudo apt install ./networkaudiod_6.1.4-71_arm64.deb
sudo systemctl start networkaudiod
systemctl status networkaudiod
```

- **For an HQPlayer older than 5.16**, take `networkaudiod_5.1.8-68_arm64.deb` instead: both lines
  sit in the same folder, the newest last.
- **The install shows Signalyst's licence**, and sets the NAA to start with the Pi, but does not
  start it: hence the third command. `active (running)` means it is up.
- **To choose the name HQPlayer shows**, remove the `#` before `NETWORKAUDIOD_NAME` in
  `/etc/default/networkaudiod`, put a one-word name between the quotes, then
  `sudo systemctl restart networkaudiod`.

### On DietPi

In `dietpi-software`, **NAA Daemon** installs the newest package on Signalyst's page — 6.1.4
today, which needs HQPlayer 5.16 or later.

## In HQPlayer

Open **File → Settings** (on macOS, **Preferences**) and choose **NetworkAudioAdapter IPv6**, or
**NetworkAudioAdapter**, as the backend; HQPlayer's author finds that discovery usually works better
over IPv6. The **Device** list then
shows each NAA with its DAC, "always combination of the NAA device plus the hardware device ID".
If the list stays empty, check that the NAA is running, that it is on the same network, and that
it is not too new for your HQPlayer.

## What to get right

- **An NAA your HQPlayer accepts.** In HQPlayer's author's words: "NAA 6.x is not compatible with
  HQPlayer versions prior to 5.16. While HQPlayer works with NAA versions up at least from NAA 3.x."
  (February 2026). My own test agrees: an NAA 6 did not work with HQPlayer Desktop 5.13
  (2026-09-20). With HQPlayer 6, an NAA 5 still plays; DAC corrections need it at 5.1.5 or
  later, and the newest ones need NAA 6.
- **A Pi 4 for a USB DAC at the highest rates.** HQPlayer's author found that a Pi 5's USB output
  fails from 768 kHz PCM and 48 kHz × 512 DSD up (February 2025), and still recommended the Pi 4 in
  January 2026: "Only RPi4 works properly" (June 2025). I have not measured it.
- **It holds the DAC only while HQPlayer plays.** Measured on my x86 test box with a USB DAC
  (2026-09-26): with the NAA running and HQPlayer idle, the DAC stays free and another player can
  use it; when HQPlayer plays, the NAA takes it; when HQPlayer stops, the DAC is free again within
  three seconds. An NAA can live beside your other players.
- **It costs almost nothing at rest.** On a Raspberry Pi 4 left idle for 30 hours, NAA 5.1.8 used
  3.8 MB of memory and 20 seconds of processor time in all (2026-10-21).

## With Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup> installs Signalyst's package itself, from **Audio Software**, on the major
version of the HQPlayer it is connected to, and has profiles that run the NAA alone or beside MPD
and Roon Bridge. HQPlayer, the NAA included, comes with the Pro edition. With **Use as output** on
the HQPlayer card, what you play in Audiogravi<sup>ty</sup> goes through HQPlayer and back to your
DAC through the NAA; if the two major versions differ, it says so instead of playing. Formats
HQPlayer cannot read reach it as FLAC, without loss.

The details are in the manual:
[Outputs & engines → HQPlayer](../manual/06-outputs-engines#hqplayer), and
[Administration → Audio Software](../manual/07-administration#audio-software).

## Sources

- Signalyst: [NAA images](https://www.signalyst.com/bins/naa/images/) and [Debian 13 packages](https://www.signalyst.com/bins/naa/linux/trixie/), read on 2026-10-21; [HQPlayer Desktop](https://signalyst.com/hqplayer-desktop/) (Raspberry Pi 4 or 5 as an NAA); [DAC corrections](https://signalyst.com/dac-corrections-updated-4/), June 2026. The licence and the service: in the `networkaudiod` 6.1.4-71 package. HQPlayer 6.1.1's manual: in the `hqplayer6desktop` package.
- Jussi Laako, who writes HQPlayer, on the Roon forum: [NAA and HQPlayer versions](https://community.roonlabs.com/t/hqplayer-naa-thread/176288/764), February 2026, and [NAA for DAC corrections](https://community.roonlabs.com/t/is-there-a-compelling-v6-upgrade-argument-now-that-ahmxec4b-modulators-are-available/325365/4), September 2026; the Raspberry Pi 5, [February 2025](https://community.roonlabs.com/t/hqplayer-embedded-discussion/244327/1470) and [June 2025](https://community.roonlabs.com/t/new-pc-stuttering-config-issue/301078/17); writing the image, [January 2025](https://community.roonlabs.com/t/roon-disconnects-from-hqplayer/290465/4), and updating it, [May 2026](https://community.roonlabs.com/t/hqplayer-naa-thread/176288/801); the NAA's name, [November 2025](https://community.roonlabs.com/t/hqplayer-naa-thread/176288/742); IPv6, [March 2025](https://community.roonlabs.com/t/hqplayer-desktop-thread/166213/1707); the Pi 4 with NAA OS, [January 2026](https://community.roonlabs.com/t/which-hqp-filter-are-you-using-2024/261032/1272).
- DietPi 10.7: [dietpi-software](https://github.com/MichaIng/DietPi/blob/v10.7/dietpi/dietpi-software).
