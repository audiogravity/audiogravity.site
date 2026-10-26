# Lossless internet radio: which stations stream FLAC, and how to check what a station sends

**Short answer:** most internet radio is MP3 or AAC, which drop part of the music on the way, whatever
a station calls itself. Some stations stream FLAC, which drops nothing: of the 88 found here, three in
four sent CD quality, 16 bits at 44.1 or 48 kHz, and five went above 48 kHz. Station directories are a
poor guide: the largest lists five stations as FLAC, while 82 more of those found sit under "OGG", next
to lossy streams. Ask the stream itself: `ffprobe` names its format in a second.

Checked on 2026-10-26: 333 streams read with ffprobe 7.1 on Debian 13, chosen in the Radio Browser
directory (every station listed as FLAC or carrying FLAC, lossless or hi-res in its name or tags, the
150 most-voted stations listed as Ogg, the 150 most-voted listed at 256 kbit/s or more), and eight of
them played in MPD 0.24.5 without a sound card. The formats and the directory's workings come from
their specifications and source code.

## Lossy, lossless, and what names say

- **MP3, AAC, Opus and Vorbis are lossy.** Their bitrate, 128, 192 or 320 kbit/s, says how much of the
  music is kept, not a resolution. A name does not change it: France Inter's "hifi" stream is AAC at
  192 kbit/s, BBC Radio 3's "HD Sound" is AAC at 320 kbit/s, and "Classic Vinyl HD" is MP3.
- **FLAC is lossless.** Its bits and its rate are the stream's real resolution.
- **Ogg is a wrapper**, not a format: it carries FLAC, Vorbis or Opus, and a server sends all three as
  `audio/ogg`. Of the 125 most-voted stations listed as Ogg that answered, 56 sent FLAC, 35 Vorbis
  and 34 Opus.
- **HLS**, an address ending in `.m3u8`, sends the stream in short files. Its specification allows
  AAC, MP3 and AC-3 on their own, and Apple's adds FLAC and Apple Lossless in MP4 files: SomaFM's
  Groove Salad sends FLAC that way.

The 88 FLAC streams found:

| Format | Streams |
|---|---|
| 16 bits, 44.1 kHz | 47 |
| 16 bits, 48 kHz | 21 |
| 24 bits, 48 kHz | 12 |
| 24 bits, 44.1 kHz | 3 |
| 24 bits, 96 kHz | 2 |
| 24 bits, 192 kHz | 2 |
| 16 bits, 192 kHz | 1 |

## Check what a station sends

ffprobe comes with ffmpeg: `sudo apt install ffmpeg`. Then, with the station's address:

```bash nocopy
ffprobe -v error -show_entries stream=codec_name,sample_rate,bits_per_raw_sample,bit_rate:format_tags=icy-br -of compact "http://stream.radioparadise.com/mellow-flac"
```

```text nocopy
stream|codec_name=flac|sample_rate=44100|bit_rate=N/A|bits_per_raw_sample=16
format|tag:icy-br=1441
```

- **`codec_name`** is the format: `flac` is lossless; `mp3`, `aac`, `opus` and `vorbis` are not.
- **`bits_per_raw_sample`** and **`sample_rate`** are the resolution of a FLAC stream. A lossy stream has
  no bit depth, `N/A`: its `bit_rate`, in bits per second, stands in its place.
- **`icy-br`** is the bitrate the station announces about itself: an Icecast server passes on the
  figure the station's software gives it, and nothing checks it. Naim Jazz announces `128` for the
  same format as above, 16-bit FLAC.

ffprobe reads a second or two of the stream, follows redirections and reads HLS addresses as they are.

## What station directories say

Radio Browser, a free directory to which anyone can add a station, listed nearly 70,000 stations on
the day: two in three as MP3, five as FLAC. Its code explains why. A station's codec is what the
server's `Content-Type` names, so every `audio/ogg` stream is listed as Ogg; its bitrate is the
station's own `icy-br`. Read against the streams themselves:

- **"OGG" hides most FLAC stations.** 82 of the 88 FLAC streams found were listed as Ogg, one as MP4
  (SomaFM's HLS), five as FLAC.
- **Bitrates are what stations announce.** The FLAC streams were listed at anything from 0 to
  6,144 kbit/s.
- **Names are not formats.** Of the 97 stations that answered and that call themselves FLAC or
  lossless in their name or tags, or are listed as FLAC, 17 sent MP3, AAC or Vorbis: often a lossy
  version of a FLAC station, under the same name.
- **"High bitrate" means lossy.** Of the 141 most-voted stations listed at 256 kbit/s or more that
  answered, 113 sent MP3, 23 AAC and one Vorbis; two sent FLAC, and two could not be identified.

So search a directory for "flac" in names and tags, then check each candidate with ffprobe.

## Stations found streaming FLAC

Read on 2026-10-26. Stations change their addresses: if one no longer answers, its own website gives
the current one.

- **Radio Club 80 Trance**, Chile, 24 bits, 192 kHz: `https://stream.radioclub80.cl:8052/trance80.flac`
- **SECTOR Jazz**, Russia, 24 bits, 96 kHz: `http://89.223.45.5:8000/jazz-flac`
- **Sveriges Radio P2**, Sweden, 24 bits, 48 kHz, a stream its broadcaster calls experimental:
  `https://live1.sr.se/p2-flac`
- **Radio Calico**, United States, 24 bits, 48 kHz: `http://roon.radio-calico.com:8000/roon`
- **Fréquence 3 Gold**, France, 24 bits, 48 kHz: `https://frequence3.net-radio.fr/frequence3gold.flac`
- **PureClassix**, Netherlands, 24 bits, 44.1 kHz: `http://mscp4.live-streams.nl:8140/flac.ogg`
- **Český rozhlas D-dur**, Czechia, 16 bits, 48 kHz: `http://amp.cesnet.cz:8000/cro-d-dur.flac`
- **Český rozhlas Jazz**, Czechia, 16 bits, 48 kHz: `http://amp.cesnet.cz:8000/cro-jazz.flac`
- **SomaFM Groove Salad**, United States, 16 bits, 48 kHz:
  `https://hls.somafm.com/hls/groovesalad/FLAC/program.m3u8`
- **Radio Paradise, Main Mix**, United States, 16 bits, 44.1 kHz: `https://stream.radioparadise.com/flac`
- **Naim Radio**, United Kingdom, 16 bits, 44.1 kHz: `http://mscp3.live-streams.nl:8360/flac.flac`
- **Naim Jazz**, United Kingdom, 16 bits, 44.1 kHz: `http://mscp3.live-streams.nl:8340/jazz-flac.flac`
- **Rondo Classic Klasu**, Finland, 16 bits, 44.1 kHz: `https://iradio.fi/klasu.flac`

Some stations stream FLAC to one country only, for licensing reasons. Munich Vinyl Radio announces
FLAC at 192 kHz for listeners in Germany: from France, its streams answered `401 Unauthorized`.

## Playing them with MPD

```bash nocopy
mpc add http://stream.radioparadise.com/mellow-flac
mpc play
mpc status '%audioformat%, %kbitrate% kbit/s'
```

- **An HLS address goes in as it is.** MPD 0.24 played SomaFM's and France Inter's `.m3u8` from their
  `https://` addresses, 45 seconds each, across several of their files. Written `hls+https://`, a form
  MPD's code accepts and some guides give, it failed on SomaFM and played France Inter with decoding
  errors, and ffmpeg's own log advises the plain address.
- **What MPD shows is "the format emitted by the decoder plugin"**, in its documentation's words, not
  what the station sent:

  | Station | Sends | `%audioformat%` |
  |---|---|---|
  | Radio Club 80 Trance | FLAC, 24 bits, 192 kHz | `192000:24:2` |
  | Sveriges Radio P2 | FLAC, 24 bits, 48 kHz | `48000:24:2` |
  | Radio Paradise, Mellow Mix | FLAC, 16 bits, 44.1 kHz | `44100:16:2` |
  | Classic Vinyl HD | MP3, 320 kbit/s announced | `48000:24:2` |
  | France Inter, hifi | AAC, 192 kbit/s | `48000:16:2` |
  | France Inter, HLS | AAC | `48000:f:2` |

  For a lossy stream, the bits are the decoder's working resolution: an app that shows "24 bit,
  48 kHz" for an MP3 says nothing of its quality.
- **To reach the DAC untouched**, a FLAC stream needs what a file needs: no resampling and no software
  volume. See [How to check bit-perfect playback](check-bit-perfect-playback-linux).

## Through HQPlayer

HQPlayer's list of formats has FLAC and MP3, not AAC: "AAC is not supported as it requires additional
patent licenses", its author wrote in April 2025. An AAC station reaches it only decoded beforehand,
by a player such as Roon, which "always sends just raw decoded PCM or DSD to HQPlayer".

## With Audiogravi<sup>ty</sup>

Its Radio tab searches the Radio Browser directory, and a station missing from it can be added by its
address. A station plays like the music on the box, to the same outputs. For HQPlayer, the box relays
each station, and converts to FLAC what HQPlayer does not read: the conversion keeps the sound as it
arrived, it does not bring back what a lossy stream left out.

The details are in the manual:
[Library & streaming → Internet radio](../manual/05-library-streaming#internet-radio).

## Sources

- Measurements, 2026-10-26: 333 streams read with ffprobe 7.1.5 (Debian 13), from Radio Browser's answers to its station search; eight played in MPD 0.24.5 with its `null` output, the two HLS ones for 45 seconds; the directory's figures from its `/json/codecs` and `/json/stats` answers.
- Radio Browser: its [API documentation](https://api.radio-browser.info/) and its server's source, [radiobrowser-api-rust](https://gitlab.com/radiobrowser/radiobrowser-api-rust), which writes a station's codec and bitrate only from its stream check; the check, [av-stream-info-rust 0.13.2](https://docs.rs/crate/av-stream-info-rust/0.13.2), reads them from the `Content-Type` and `icy-br` headers. Read on 2026-10-26.
- Formats: [RFC 9639](https://www.rfc-editor.org/rfc/rfc9639) (FLAC in Ogg sent as `audio/ogg`), [RFC 8216](https://www.rfc-editor.org/rfc/rfc8216) (HLS), Apple's [HLS Authoring Specification](https://developer.apple.com/streaming/hls-authoring-specification-for-apple-devices.html) (FLAC and Apple Lossless, revision of June 2025); Icecast's [configuration reference](https://icecast.org/docs/icecast-latest/config_file/) (an announced bitrate); FFmpeg's [ffprobe](https://ffmpeg.org/ffprobe.html) documentation.
- MPD: its [plugins](https://mpd.readthedocs.io/en/stable/plugins.html) and [protocol](https://mpd.readthedocs.io/en/stable/protocol.html) documentation (the `audio` field).
- Stations, read on 2026-10-26: [BBC Sounds](https://www.bbc.co.uk/sounds/help/questions/features/hd-sound) on Radio 3's HD Sound; Sveriges Radio's [technical support](https://teknisk-support.sverigesradio.se/org/teknisk-support/d/flac-streams-for-radio/) on P2's FLAC stream (January 2024); [Munich Vinyl Radio](https://munichvinylradio.de/).
- Jussi Laako, who writes HQPlayer, on the Roon forum: [AAC](https://community.roonlabs.com/t/244327/1598) (April 2025) and [Roon](https://community.roonlabs.com/t/166652/13) (July 2021); HQPlayer's [source formats](https://signalyst.com/hqplayer-desktop/).
