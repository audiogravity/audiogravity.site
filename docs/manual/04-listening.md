# 4. Listening

Once your box is set up, playing music is the same whatever the source — local files,
Qobuz, Tidal, HIGHRESAUDIO, internet radio or a UPnP server all flow through one set
of controls.

## The Now Playing screen

The Now Playing bar is always at hand; tap it for the fullscreen player:

- **Cover art**, a **seekable progress bar**, and full **transport** controls
  (play/pause, next, previous, seek, volume).
- The **album tracklist**, and **swipe** between sources.
- A dynamic background derived from the cover.

## The live hi-fi readout

On every track change, AudioGravity shows exactly what's reaching your DAC:

- **Format** (PCM / DSD), **sample rate**, **bit depth**, and instantaneous **bitrate**.

This is your at-a-glance confirmation that a Hi-Res track really is playing at its
native resolution.

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
