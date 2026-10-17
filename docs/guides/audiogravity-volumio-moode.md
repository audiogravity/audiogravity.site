# Audiogravi<sup>ty</sup>, Volumio or moOde: which to choose?

**Short answer:** moOde if you want a free, open-source player and do not need Tidal or
HIGHRESAUDIO in its library. Volumio if you want to pick music in the Qobuz and TIDAL apps
(Qobuz Connect, TIDAL Connect) and accept a subscription and an account. Audiogravi<sup>ty</sup>
if you use HQPlayer, or want Qobuz, Tidal and HIGHRESAUDIO in one library without a
subscription to the player itself.

I make Audiogravi<sup>ty</sup>: read this page with that in mind. Everything said here about
Volumio and moOde comes from their own sites, documentation and release notes, read on
2026-10-17 and listed at the end. A row appears in the table only where I could check all three.

## Side by side

| | Audiogravi<sup>ty</sup> | Volumio | moOde |
|---|---|---|---|
| Price | Starter free; Pro is a one-off licence, no subscription ([price](https://audiogravity.app/#pricing)) | Free; Premium €7.49 a month or €69.99 a year | Free, open source (GPL 3) |
| Online account | None | MyVolumio, for Premium | None |
| Qobuz, Tidal, HIGHRESAUDIO in the library | All three (Pro) | All three (Premium) | Qobuz, through upmpdcli and a separate UPnP control app |
| Qobuz Connect, TIDAL Connect | No | Both (Premium) | Qobuz Connect through Pibuz, installed by the user |
| HQPlayer | HQPlayer Embedded on the box, NAA, HQPlayer as the output, its filters from the app | Not offered | Not offered |
| Roon | Roon Bridge or Roon Server on the box, Roon zones as a source | Roon Bridge plugin | Roon Bridge, installed by the user |
| AirPlay | Yes | Yes | AirPlay 1 and 2 |
| Browsing UPnP media servers | Yes (Pro) | Yes | Removed in 2022 (version 8.1.0) |
| DSD | Native to a USB DAC that accepts it | DoP; native since Volumio 4 | Native and DoP |
| Apps | Installable web app (iPhone, Android), browser | Browser, native apps | Browser |
| System | Debian 13 (Trixie): Raspberry Pi 4 and 5, x86-64 PCs | Debian 12 (Bookworm): Raspberry Pi 4 and 5, PCs | Raspberry Pi OS (Trixie), 64-bit Raspberry Pi |

## moOde

A free, open-source player built on MPD, actively developed: version 10.3.6 came out on
10 October 2026. Besides MPD it manages AirPlay, Spotify Connect, Squeezelite, Plexamp and Roon
Bridge as renderers, and plays multichannel. Qobuz goes through upmpdcli, which moOde sets up as
a UPnP media server for a separate control app. Since September 2026, Pibuz brings Qobuz
Connect. Tidal and HIGHRESAUDIO are not in its interface.

## Volumio

Volumio 4 is built on Debian 12 and runs on the Raspberry Pi 4 and 5 and on PCs, with apps in
the app stores. The free edition plays your files, AirPlay and UPnP; Premium adds Qobuz, TIDAL
and HIGHRESAUDIO in the library, Qobuz Connect and TIDAL Connect, and needs a MyVolumio account.
Qobuz lists Volumio among its Qobuz Connect partners, and HIGHRESAUDIO names it as a partner.
Volumio's own devices are Roon Ready.

## Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup> installs and drives the audio software on the box — MPD, AirPlay, Roon
Bridge or Roon Server, HQPlayer Embedded or HQPlayer's NAA, a UPnP renderer — and switches
between them by profile. It also drives UPnP renderers elsewhere on your network. The free
Starter edition plays your own library and internet radio; Pro adds the streaming services, UPnP
media servers, Roon, HQPlayer, the signal path view and the tuning of the box. Pro is a one-off
licence for one machine; the 30-day trial opens everything. Each streaming service needs your
own subscription.

What it does not have: Qobuz Connect, TIDAL Connect, Spotify Connect, Squeezelite, Plexamp.

The guides go further on two of its subjects:
[HQPlayer Embedded on a Raspberry Pi 5](hqplayer-embedded-raspberry-pi-5) and
[Qobuz, Tidal and HIGHRESAUDIO on a Raspberry Pi](qobuz-tidal-highresaudio-raspberry-pi).

## Sources

- Volumio: [editions and prices](https://volumio.com/en/get-started/) (version 4.119, 24 March 2026), [Volumio 4 OS](https://volumio.com/volumio-4-os/) (November 2025), [supported devices](https://help.volumio.com/en/articles/10-what-3rd-party-devices-are-supported), [MyVolumio account](https://help.volumio.com/en/articles/5-what-is-myvolumio-account), [plugins for Volumio 4](https://github.com/volumio/volumio-plugins-sources-bookworm), [Rivo](https://shop.volumio.com/product/rivo); all read on 2026-10-17.
- Qobuz Connect partners: [Qobuz](https://community.qobuz.com/press-en/qobuz-connect-celebrates-over-100-partners), December 2025. HIGHRESAUDIO's partners: [highresaudio.com](https://www.highresaudio.com/en/content/streaming-app), read on 2026-10-17.
- moOde: [moodeaudio.org](https://moodeaudio.org/) and [release notes](https://github.com/moode-player/moode/blob/master/www/relnotes.txt), read on 2026-10-17; [setup guide](https://github.com/moode-player/docs/blob/main/setup_guide.md); [Pibuz](https://github.com/PhilipVinc/pibuz).
