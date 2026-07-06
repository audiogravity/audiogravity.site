# 3. First run — guided audio setup

The first time you open Audiogravi<sup>ty</sup>, a few guided steps take you from a bare box to
music playing — without touching a config file.

## 1. Your trial activates automatically

A **30-day trial** — full access to every Pro feature — is activated on first run.
No action required, no card. When it ends you can keep using the free **Starter**
features or buy a **lifetime** licence (see [7. Administration → Licence](07-administration.md)).

## 2. Create your admin account

Set up your administrator account and sign in. After a first password login you can
register a **passkey** on the device — Face ID, Touch ID, a fingerprint or a hardware
key — and every later login becomes a tap. (Passkeys require Audiogravi<sup>ty</sup> to be
reachable over a real HTTPS **domain** — see the `--public-url` flag in
[2. Installation](02-installation.md).)

## 3. Configure the audio stack (guided)

On a new box, the **Config** tab shows an **Initialize audio stack** panel
(administrators only). It:

1. **Auto-detects** your DAC and your music library.
2. **Generates a minimal, bit-perfect configuration** for the three audio services —
   **MPD** (local library), **AirPlay** (shairport-sync) and **UPnP** (upmpdcli) —
   all wired to the output you choose.
3. Asks for your **admin password** before applying.

Once at least one service is set up, the panel disappears and each MPD / AirPlay /
UPnP tile shows a **CONFIGURED** badge.

> **Why "bit-perfect"?** The generated configs send audio to your DAC untouched — no
> resampling, no volume math in the digital domain — so what your DAC receives is
> exactly what the file contains.

### The DAC stays put

When you configure a USB DAC, Audiogravi<sup>ty</sup> **pins its sound-card index** at the OS
level. Linux then always gives that DAC the same number, even after a reboot or a
USB re-plug — so the output your services target never drifts and nothing needs
re-checking at startup.

### Per-service outputs

Each service can target its **own** output. For example: MPD on your USB hi-res DAC,
AirPlay on the optical out. Change any service's output later from the **Guided**
editor (see below) in a couple of clicks.

## 4. Change output or library later (Guided mode)

For MPD, AirPlay and UPnP, the Config editor opens in a **Guided** view where you
change the **audio output** or **music library** in a couple of clicks. Only the
setting you touch is rewritten — the rest of your config is preserved. A **Reset to
default** action regenerates a clean minimal config (admin password required; your
current file is backed up first).

## Next

Your box now plays. Head to **[4. Listening](04-listening.md)** to start playing
music, or **[5. Library & streaming](05-library-streaming.md)** to connect Qobuz,
Tidal, HIGHRESAUDIO and internet radio.
