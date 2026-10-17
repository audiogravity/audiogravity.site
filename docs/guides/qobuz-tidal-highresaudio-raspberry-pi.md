# Qobuz, Tidal and HIGHRESAUDIO on a Raspberry Pi

**Short answer:** a Raspberry Pi can play all three, but few setups offer all three at once, and
they differ in what they cost, how they connect to each service, and how they are driven: from
the service's own app (Qobuz Connect, TIDAL Connect) or from the streamer's own library. Each
service needs your own subscription, whichever way you choose.

Checked on 2026-10-17. These products change often: the sources are listed at the end of the
page, with their dates.

## The ways to do it

**Volumio Premium.** Qobuz, TIDAL and HIGHRESAUDIO are built into Volumio's library, and Premium
adds Qobuz Connect and TIDAL Connect. Premium costs €7.49 a month or €69.99 a year, with a
14-day trial, and needs a MyVolumio account. Qobuz
lists Volumio among its Qobuz Connect partners, and HIGHRESAUDIO names Volumio as a partner.
Volumio 4 runs on the Raspberry Pi 4 and 5.

**piCorePlayer, or Lyrion Music Server.** Free. Qobuz and TIDAL come as plugins from the
server's official plugin list, both updated in October 2026. There is no HIGHRESAUDIO plugin in
that list.

**moOde.** Free and open source. Qobuz goes through upmpdcli, which moOde sets up as a UPnP media
server: you browse it from a separate UPnP control app. Since September 2026, moOde can also
install Pibuz, for Qobuz Connect. For TIDAL, moOde's founder wrote in August 2024 that the UPnP
option "doesn't work anymore". HIGHRESAUDIO is not offered in moOde's interface.

**HQPlayer.** HQPlayer streams Qobuz and HIGHRESAUDIO itself: Signalyst lists both as streaming
partners. It runs on the Pi (see [HQPlayer Embedded on a Raspberry Pi 5](hqplayer-embedded-raspberry-pi-5)),
and is driven from its own interface or another controller.

## With Audiogravi<sup>ty</sup>

Audiogravi<sup>ty</sup> runs on a Raspberry Pi 4 or 5 with Debian 13 (Trixie), DietPi or
Raspberry Pi OS included. The three services come with the Pro edition; the 30-day trial
includes them.

**One library for the three.** Qobuz, Tidal and HIGHRESAUDIO sit side by side with your own
files and your UPnP media servers. **Search** looks through all of them at once, and an
artist's page gathers their albums across the services. Each service keeps its own shelves:
favourites, playlists, genres, Qobuz purchases, the HIGHRESAUDIO vault.

**Connecting each service**, from **Library → Sources**:

- **Qobuz**: tap **Connect**, sign in on Qobuz's page, and you are sent back connected.
- **Tidal**: tap **Connect** and sign in; Tidal then shows a page the app cannot read on its own,
  so you copy that page's address back into Audiogravi<sup>ty</sup>, once.
- **HIGHRESAUDIO**: your email and password, kept encrypted on the box. HIGHRESAUDIO allows one
  active device per account: connecting the box signs your other HIGHRESAUDIO players out.

**The best quality each service offers.** Audiogravi<sup>ty</sup> asks Qobuz and Tidal for their
highest quality, up to 24-bit / 192 kHz, and plays what HIGHRESAUDIO publishes, up to
24-bit / 352.8 kHz. The audio is not re-encoded: Qobuz and HIGHRESAUDIO send it as it is, and
Tidal's is repackaged without being changed. Keep Tidal on a lossless setting: its lower ones
produce no sound.

**Where it plays.** On the DAC attached to the box, on a UPnP renderer elsewhere on your network,
or through HQPlayer.

**What it does not do.** There is no Qobuz Connect and no TIDAL Connect: you choose the music in
Audiogravi<sup>ty</sup>, not in the Qobuz or TIDAL apps.

The details are in the manual:
[Library & streaming → Streaming services](../manual/05-library-streaming#streaming-services).

## Sources

- Volumio editions and prices: [volumio.com/en/get-started](https://volumio.com/en/get-started/), read on 2026-10-17. Volumio 4 and the Pi 5: [Volumio 4 OS](https://volumio.com/volumio-4-os/), November 2025; [supported devices](https://help.volumio.com/en/articles/10-what-3rd-party-devices-are-supported).
- Qobuz Connect partners: [Qobuz Connect celebrates over 100 partners](https://community.qobuz.com/press-en/qobuz-connect-celebrates-over-100-partners), Qobuz, December 2025.
- HIGHRESAUDIO's partners: [HIGHRESAUDIO streaming app](https://www.highresaudio.com/en/content/streaming-app), read on 2026-10-17.
- Lyrion Music Server plugins: [the official plugin list](https://github.com/LMS-Community/lms-plugin-repository/blob/master/extensions.xml), read on 2026-10-17 (Qobuz 3.7.2, TIDAL 1.8.2).
- moOde: [release notes](https://github.com/moode-player/moode/blob/master/www/relnotes.txt) (Pibuz in 10.3.4 and 10.3.5, September 2026); [Pibuz](https://github.com/PhilipVinc/pibuz); Tim Curtis on Tidal: [moOde forum](https://moodeaudio.org/forum/showthread.php?pid=57024), August 2024.
- HQPlayer's streaming partners: [signalyst.com](https://signalyst.com/?page_id=124), read on 2026-10-17.
