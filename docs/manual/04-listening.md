# 4. Listening

Once your box is set up, playing music is the same whatever the source — local files,
Qobuz, Tidal, HIGHRESAUDIO, internet radio or a UPnP server all flow through one set
of controls.

## The Now Playing bar

A sticky **Now Playing** bar sits above the footer and shows **all active audio
sources** at once, with quick transport — play/pause, next, and volume. Tap it (or
swipe up on mobile / the expand button on desktop) to open the **fullscreen player**.

## The fullscreen player

- **Cover art** with a dynamic background derived from it, a **seekable progress
  bar**, and full **transport**: repeat · previous · play/pause · next · shuffle.
- **Album details** — Album, Artist, Format, Genre, Year, Position, Source and the
  full **Tracklist**.
- A **Queue** view for what's coming up.
- **Swipe** between active sources; close with the back button or swipe-down.
- When playing to a network renderer, a **"Routed to UPnP renderer"** indicator makes
  the destination clear.

## The live hi-fi readout

On every track change, Audiogravi<sup>ty</sup> shows exactly what's reaching your DAC:

- **Format** (PCM / DSD), **sample rate**, **bit depth**, and instantaneous **bitrate**.

This is your at-a-glance confirmation that a Hi-Res track really is playing at its
native resolution. A DSD lock indicator appears for DSD streams.

## The stream-origin badge

A badge in the Now Playing bar always tells you **where the audio is coming from** —
Tidal, Qobuz, HIGHRESAUDIO, your UPnP server (by name), a radio station, a local file,
or AirPlay. No guessing which source is live.

## Profiles — switch whole chains in one tap

A **profile** is a saved scenario for your audio system. Switching one automatically
**starts the services it needs and stops the conflicting ones**, so the chain is
always coherent and bit-perfect. Typical profiles: *Roon + HQPlayer* for serious
listening, *MPD + upmpdcli* to expose the box as a UPnP renderer, *AirPlay only* for
background music.

Each profile tile shows the services it starts/stops, the resolved output port (e.g.
`usb`, `toslink`), a live **health bar** (active / failed / idle), and when it was
last activated. Activation is atomic, with a detailed toast on failure.

## Sleep timer

A built-in sleep timer pauses playback after a set duration — for falling asleep to
music without leaving the system running all night.

## Where the audio goes

Choosing **where** music plays — your local DAC, a network renderer, HQPlayer or
AirPlay — is covered in **[6. Outputs & engines](06-outputs-engines.md)**. Connecting
streaming services and browsing your library is in
**[5. Library & streaming](05-library-streaming.md)**.
