# HQPlayer Embedded on a Raspberry Pi 5

**Short answer:** yes, HQPlayer Embedded runs on a Raspberry Pi 5, and Signalyst publishes it
for that board in two forms. The Pi 5 suits stereo, not multichannel, and its USB output has a
known problem at the highest rates. Whichever way you install it, HQPlayer Embedded needs a
licence from Signalyst; without one, it runs for half an hour at a time.

Checked on 2026-10-22 against Signalyst's download pages and packages. The package was
installed on a Raspberry Pi 4 under Raspberry Pi OS, built on Debian 13 (version 6.0.2,
2026-09-22); what it does once installed was measured on an x86 box under Debian 13 in
September 2026. The Pi 5's limits are Signalyst's, with their dates.

## Two ways to install it

- **A ready-made system image.** You write it to a microSD card and the Pi starts as an
  HQPlayer machine: the image replaces the Pi's whole system with one built for HQPlayer.
  Version 6 images exist for the Pi 5 only; the only Pi 4 image is a 5.17.2.
- **A Debian package**, `hqplayerd`, for Debian 13 on arm64, the same for a Pi 4 and a Pi 5. It
  installs like any other program, so HQPlayer sits beside your other players: MPD, Roon
  Bridge, AirPlay, a UPnP renderer.

The image is the simpler route if the Pi will do nothing else; the package, if the Pi is also
your streamer.

## Install the package on Raspberry Pi OS or Debian

The package needs Debian 13, or a Raspberry Pi OS built on it. To check:

```bash
grep VERSION_CODENAME /etc/os-release
```

It must answer `VERSION_CODENAME=trixie`. Then take the newest version in Signalyst's
[Debian 13 folder](https://signalyst.com/bins/hqplayerd/trixie/), 6.1.1 on 2026-10-22, a
127 MB download, and install it:

```bash
wget https://signalyst.com/bins/hqplayerd/trixie/hqplayerd_6.1.1-5_arm64.deb
sudo apt install ./hqplayerd_6.1.1-5_arm64.deb
```

Version 6 starts at once, and at every boot. Installed again after a removal, it stays off
until you turn it on:

```bash
sudo systemctl enable --now hqplayerd
```

DietPi on Debian 13 takes the same commands: its software list does not offer HQPlayer
Embedded (DietPi 9.20).

**Version 5 does not install on Debian 13.** It depends on `libgmpris`, which neither Debian
nor Signalyst's Debian 13 folder provides, and apt stops with:

```text nocopy
Unsatisfied dependencies:
 hqplayerd : Depends: libgmpris but it is not installable
```

A licence for version 5 calls for Signalyst's 5.17.2 image instead.

### Then, by hand

- **Give its web page a password.** The package installs it without one, so the settings
  pages turn everybody away, and each refused sign-in writes `OnAuthRequest(): digest not set`
  to its log. Set one with Signalyst's own command, then restart the service: HQPlayer reads
  it only when it starts.

  ```bash nocopy
  sudo hqplayerd -s hqplayer your-password
  sudo systemctl restart hqplayerd
  ```

  Its web page is then at `http://<the Pi's address>:8088`: sign in as `hqplayer`. The
  password stays in your shell's history, and in the system journal, where sudo records each
  command it runs: choose one you use nowhere else.
- **Give it an output.** It has none after installation, and plays nothing. On its web page,
  open **Configuration** and choose your DAC under **ALSA backend → Device**. A DAC another
  player is using is left off that list.
- **Keep an eye on its log.** It writes to `/tmp/hqplayerd.log`, which is memory on Debian 13,
  adds to it at every start, never empties it, and has no setting for its size. Most of the
  time that is a few lines. During one fault, I saw it write 600 MB a minute.
  `ls -lh /tmp/hqplayerd.log` shows the size; restarting the Pi empties it.
- **The trial counts from the start of the service, not from the first note.** Without a
  licence, HQPlayer stops taking commands about 32 minutes after it starts, whether or not it
  played meanwhile. It writes nothing about it in its log; it just stops answering.
  `sudo systemctl restart hqplayerd` gives you another half hour.

## What a Pi 5 can handle

Jussi Laako, who writes HQPlayer, has answered this on the Roon forum:

- **Stereo, yes; multichannel, no.** "It's only quad-core, so not great for multichannel
  (typically you'd have minimum one or two cores per channel)" (September 2023).
- **Its USB output fails at the highest rates.** "There are some hardware/OS issues with RPi5
  and 48k x512 and higher output rates" (March 2024). The issue "is specific to USB output":
  up to 44.1k × 512 or 705.6k PCM, "it should work" (May 2024). In February 2025, still:
  "native DSD256 output works on RPi5. On my testing issue appears on 768k PCM and 48k x512
  DSD, and up". His way around it is a Raspberry Pi 4 as the NAA between the Pi 5 and the DAC,
  "that way you avoid the USB issues of RPi5". Of the Pi as an NAA, in June 2025: "Only RPi4
  works properly, RPi3 and RPi5 don't (due to hardware bugs)."

I have not measured HQPlayer Embedded on a Pi 5 myself.

Two practical points:

- **Power it with a 5 A supply**, such as the official 27 W one. With any other, the Pi 5
  "restricts downstream USB devices to 600 mA of power", instead of 1.6 A: a DAC powered from
  USB may not get enough.
- **Set the DSD rate limit before the first play.** HQPlayer Embedded comes set to DSD256. If
  your DAC stops lower, lower it on the web page, under **Configuration → SDM settings → Rate
  limit**: 2822400 for DSD64, 5644800 for DSD128. Some DACs accept a rate they cannot convert
  and hiss instead of playing.

## With Audiogravi<sup>ty</sup>

In its Pro edition, and during its 30-day trial, Audiogravi<sup>ty</sup> installs Signalyst's
package from its **Audio Software** tab. You choose the line your licence covers; it sets the
password with Signalyst's command and restarts HQPlayer, keeps its log in 10 MB of memory of
its own, lets you choose its output in the **Config** tab, and never moves an update to
another major version.

The details are in the manual:
[Outputs & engines → HQPlayer Embedded](../manual/06-outputs-engines#hqplayer-embedded), and
[Troubleshooting → HQPlayer Embedded stops after half an hour](../manual/09-troubleshooting#hqplayer-embedded-stops-after-half-an-hour).

## Sources

- Signalyst: [system images](https://signalyst.com/bins/hqplayerd/images/) and [Debian 13 packages](https://signalyst.com/bins/hqplayerd/trixie/), read on 2026-10-22; the install scripts and settings file inside the 5.17.2-48 and 6.1.1-5 packages; the help on HQPlayer Embedded's own Configuration page, version 6.1.1.
- Jussi Laako, who writes HQPlayer, on the Roon forum: [multichannel](https://community.roonlabs.com/t/hqplayer-embedded-discussion/244327/488) (September 2023), [USB output](https://community.roonlabs.com/t/hqplayer-naa-on-raspberry-pi-5/269171) (March to November 2024), [HQPlayer Embedded on a Pi 5](https://community.roonlabs.com/t/hqplayer-embedded-discussion/244327/1470) (February 2025) and [the Pi as an NAA](https://community.roonlabs.com/t/new-pc-stuttering-config-issue/301078/17) (June 2025).
- Raspberry Pi documentation: [power supplies](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc), read on 2026-10-22.
