# 1. Introduction

## What Audiogravi<sup>ty</sup> is

Audiogravi<sup>ty</sup> is a **control app for your music streamer**. It runs on the small
Linux computer next to your hi-fi (a DietPi box, a Raspberry Pi, a NUC…) and gives
you a single, beautiful interface — in any browser, on your phone, tablet or
laptop — to run every part of your listening chain.

It plays your local library, streams Qobuz, Tidal and HIGHRESAUDIO, tunes internet
radio, drives HQPlayer, casts to network renderers, and even tunes the Linux kernel
underneath for bit-perfect, glitch-free playback — all from the same screen.

## What Audiogravi<sup>ty</sup> is *not*

Audiogravi<sup>ty</sup> does **not replace** the audio engines audiophiles already trust. It
**orchestrates** them. MPD, Roon Bridge, HQPlayer, AirPlay (shairport-sync), the
UPnP stack — Audiogravi<sup>ty</sup> installs, configures and drives these proven engines
rather than reinventing them. Your signal path stays exactly as pure as the tools
you already rely on; Audiogravi<sup>ty</sup> just gives you one place to conduct them.

## How it fits together

Think of your streaming setup as five layers. Audiogravi<sup>ty</sup> sits across all of them:

| Layer | What lives here | Audiogravi<sup>ty</sup>'s role |
|-------|-----------------|---------------------|
| **Interface** | The screens you touch — browser, phone, tablet, installable app (PWA) | **It is the interface** |
| **Orchestration** | Switching sources, transport, volume, casting, monitoring | **It orchestrates** |
| **Content sources** | Your NAS, Qobuz, Tidal, HIGHRESAUDIO, internet radio, UPnP media servers | **It connects to them** |
| **Audio engine** | MPD, Roon Bridge, HQPlayer, AirPlay, UPnP renderers | **It installs, configures & drives them** |
| **OS / kernel** | Real-time scheduling, CPU pinning, ALSA | **It tunes it** |

You never have to touch a config file or a terminal to get any of this working —
though everything remains open and inspectable if you want to.

## What you can do with it

- **Play everything from one place** — local files, Qobuz / Tidal / HIGHRESAUDIO,
  internet radio, and your UPnP/DLNA media servers, with unified transport,
  cover art and a live hi-fi readout (format, sample rate, bit depth, bitrate).
- **Send music where you want** — your local DAC, a network UPnP renderer
  (Marantz, Linn, DLNA speakers), HQPlayer's DSP engine, or an AirPlay receiver.
- **Set up your audio stack in a few clicks** — a guided setup detects your DAC
  and music library and generates minimal, bit-perfect configurations for you.
- **Tune for sound quality** — real-time kernel scheduling, per-core CPU pinning,
  latency benchmarks, and a live view of your entire signal path (Pro).
- **Manage the box** — services, users with passkeys, config editing with backups,
  and one-click updates — no SSH required.

## Editions

| Edition | Price | What you get |
|---------|-------|--------------|
| **Trial** | Free · 30 days | Everything, including all Pro features |
| **Starter** | Free · forever | Profiles, Services, Audio Software, System, Users |
| **Pro** | €49 · lifetime, one machine | Audio Pipeline, Player, Library, Config editor, Performance tuning |

Pro is a **lifetime licence** — no subscription, no renewal. You can start on the
free 30-day trial; it activates automatically on first run.

> **Note:** streaming from Qobuz, Tidal or HIGHRESAUDIO requires your own active
> subscription to each service. Audiogravi<sup>ty</sup> does not provide access to them.

## What you need

- A **Linux box** (DietPi or Debian/Ubuntu, x86-64 or ARM/Raspberry Pi) next to your hi-fi
- A **DAC or audio output** the box can see (USB, HAT, HDMI, S/PDIF…)
- Your **home network**, and any device with a browser to control it

Ready? Head to **[2. Installation](02-installation.md)**.
