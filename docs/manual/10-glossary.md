# 10. Glossary

The terms this manual (and the audiophile world) takes for granted — two lines each.

**AirPlay** — Apple's streaming protocol. The box *receives* AirPlay (via
shairport-sync): your iPhone or Mac streams to it like to any AirPlay speaker.

**ALSA** — the Linux kernel's audio layer. "ALSA device" = a sound card output as
the OS sees it; Audiogravi<sup>ty</sup> resolves your DAC to one automatically.

**Bit-perfect** — the audio samples reach the DAC exactly as stored in the file: no
resampling, no software volume, no mixing. The guided setup generates bit-perfect
configs by default.

**Control point** — the UPnP role that *drives* playback on another device.
Audiogravi<sup>ty</sup> is a control point when it casts to a network renderer.

**DAC** — Digital-to-Analog Converter, the component that turns the digital stream
into the analog signal your amplifier plays. USB, HAT, HDMI or S/PDIF-attached.

**DSD** — Direct Stream Digital, the 1-bit high-rate format of SACD lineage
(DSD64/128/256…). The player shows a **DSD lock** when a DSD stream plays natively.

**Engine** — the software that actually renders audio on the box: MPD, shairport-sync
(AirPlay), Roon Bridge, HQPlayer NAA. Audiogravi<sup>ty</sup> conducts engines; it
doesn't replace them.

**FLAC** — the lossless compressed audio format most hi-res catalogues use. Lossless
= decodes to the exact original samples.

**Gapless** — playback (or an output switch) with no silence inserted between
tracks — essential for live albums and continuous mixes.

**Hi-Res** — better-than-CD resolution: more than 16-bit / 44.1 kHz, typically
24-bit at 96 or 192 kHz. The **HI·RES** badge in the player flags it live.

**MPD** — Music Player Daemon, the core playback engine: it plays your local
library and carries Qobuz, Tidal, HIGHRESAUDIO and internet radio.

**mDNS / Bonjour** — the LAN protocol devices use to announce themselves (AirPlay,
`.local` hostnames). Needs multicast to work — see
[9. Troubleshooting](09-troubleshooting.md#the-box-doesnt-appear-as-an-airplay-speaker).

**NAA** — HQPlayer's Network Audio Adapter: the box receives HQPlayer's processed
stream and hands it to the DAC, keeping the heavy DSP on another machine.

**Passkey** — password-less login credential bound to a device (Face ID, Touch ID,
hardware key) via the WebAuthn standard. Requires HTTPS on a real domain.

**PCM** — Pulse-Code Modulation, the "normal" digital audio representation (CD,
FLAC, streaming). Contrast with DSD.

**PWA** — Progressive Web App: the Audiogravi<sup>ty</sup> interface installed from
the browser onto your home screen, running fullscreen like a native app.

**Renderer** — the UPnP role that *plays* audio. Network amplifiers and streamers
are renderers; the box itself is one too (via upmpdcli) so other apps can cast to it.

**Sample rate / bit depth** — how often the signal is measured (44.1–384 kHz) and
how finely each measurement is stored (16/24/32-bit). Shown live in the hi-fi
readout.

**S/PDIF · TOSLINK** — the coaxial (electrical) and optical variants of the same
consumer digital-audio link between box and DAC.

**UPnP / DLNA** — the LAN protocol family for media discovery and playback:
media **servers** expose libraries (e.g. MinimServer), **renderers** play, control
points conduct.

**upmpdcli** — the bridge that presents MPD as a UPnP renderer, letting other apps
cast to the box.
