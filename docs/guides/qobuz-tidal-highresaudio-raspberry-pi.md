# Qobuz, Tidal and HIGHRESAUDIO on a Raspberry Pi

**Short answer:** a Raspberry Pi can play all three, but few setups offer all three at once. They
differ in what they cost, in the quality they reach, and in where you choose the music: in the
service's own app, with Qobuz Connect or TIDAL Connect, or in the streamer's app or a UPnP control
app. Each service needs your own subscription, whichever way you choose.

Checked on 2026-10-21 against each product's official pages and source code, read but not run.
Prices are those shown that day, and they change: the sources are listed at the end.

## The ways, side by side

| | Qobuz | TIDAL | HIGHRESAUDIO | From the service's app | Cost |
|---|---|---|---|---|---|
| upmpdcli, on Raspberry Pi OS or Debian | Yes | Yes | Yes | No | Free |
| Volumio Premium | Yes | Yes | Yes | Qobuz Connect, TIDAL Connect | €7.49 a month, or €69.99 a year |
| moOde | Yes | No | No | Qobuz Connect | Free |
| piCorePlayer with Lyrion Music Server | Yes | Up to CD quality | No | No | Free |
| HQPlayer | Yes | No | Yes | No | €319 for HQPlayer 6 Embedded |
| Roon, with the Pi as a Roon Bridge | Yes | Yes | No | No | $14.99 a month |

## upmpdcli, on Raspberry Pi OS or Debian

upmpdcli makes MPD a UPnP renderer and, with one module per service, adds a UPnP media server for
Qobuz, TIDAL and HIGHRESAUDIO. You browse it from a UPnP control app, such as BubbleUPnP (Android)
or mconnect Player (iPhone, iPad, Android), and the Pi plays.

- **Install** upmpdcli and the module of each service, `upmpdcli-qobuz`, `upmpdcli-tidal` and
  `upmpdcli-hra`, from [upmpdcli's site](https://www.lesbonscomptes.com/upmpdcli/): none is in
  Debian's archive. The TIDAL module also needs the Python package `tidalapi`, version 0.8.11,
  which upmpdcli's manual has you install with `pip`.
- **Turn each service on** in `/etc/upmpdcli.conf`:

  ```text nocopy
  qobuzuser = me
  qobuzformatid = 27
  tidaluser = me
  tidalaudioquality = HI_RES_LOSSLESS
  hrauser = you@example.com
  hrapass = your-password
  ```

  `qobuzuser` and `tidaluser` only switch the service on, whatever their value. `27` asks Qobuz
  for its highest quality, `HI_RES_LOSSLESS` asks TIDAL for its. The HIGHRESAUDIO password sits in
  this file in clear: upmpdcli's manual advises making it readable by its owner only
  (`sudo chmod 600 /etc/upmpdcli.conf`). Then restart upmpdcli: `sudo systemctl restart upmpdcli`.
- **Sign in once** to Qobuz and TIDAL. Each module comes with a script that prints a web address:
  open it, sign in, and the module keeps the authorisation. upmpdcli's manual names the scripts and
  their options.
- **TIDAL's highest quality reaches MPD only.** TIDAL sends it as MPEG-DASH, which MPD plays; other
  renderers are served CD quality, says upmpdcli's manual.

## Volumio 4.231

The three services, Qobuz Connect and TIDAL Connect come with Volumio Premium: €7.49 a month or
€69.99 a year, for up to 6 devices, with a MyVolumio account and a 14-day trial. Connect each
service under **Settings → Sources**, with **Connect**. For TIDAL's highest quality, Volumio's help
says to set its quality to **Hi-Res**. Qobuz lists Volumio among its Qobuz Connect brands.

## moOde 10.3.6

- **Qobuz Connect.** In **Configure → Renderers**, under **Qobuz Connect**, **Install** builds
  Pibuz on the Pi itself: about 10 minutes on a Pi 5 with 4 GB, 20 to 40 on a Pi 4, by moOde's own
  timings. The Qobuz app then plays on moOde; its quality starts at *Hi-Res 24/192K*.
- **Qobuz as a UPnP media server**, through upmpdcli: in **Configure → Renderers**, **Edit** on the
  UPnP renderer, then **Qobuz Music Service**, with a userid, a password and a quality. You browse
  it from a UPnP control app. moOde ships upmpdcli 1.9.17, whose manual says that Qobuz now signs in
  once through a web page, with a script run on the box.
- **No TIDAL and no HIGHRESAUDIO.** moOde removed TIDAL from its settings in 2021.

## piCorePlayer 11.1 with Lyrion Music Server 9.1

Qobuz and TIDAL come as free plugins from Lyrion's official list: install them under **Settings →
Manage Plugins**, then set each one up in its page under **Settings → Advanced**.

- **Qobuz 3.7.3**: your username and password. Its **Preferred format** starts at *FLAC 16 bits /
  44.1 kHz*: choose *FLAC Hi-Res 24 bits / >96 kHz* for its highest.
- **TIDAL 1.8.2**: **Add Account** takes you to TIDAL to sign in. Its **Quality** starts at *AAC
  320Kbps* and stops at *CD (FLAC)*: no hi-res in this version.
- No HIGHRESAUDIO plugin in the official list.

## HQPlayer and Roon

- **HQPlayer** streams Qobuz and HIGHRESAUDIO itself: Signalyst lists both as streaming partners,
  and you sign in from HQPlayer Client. HQPlayer Embedded runs on a Pi (see
  [HQPlayer Embedded on a Raspberry Pi 5](hqplayer-embedded-raspberry-pi-5)): HQPlayer 6 Embedded
  costs €319, and plays 30 minutes at a time without a licence.
- **Roon** streams Qobuz and TIDAL, as well as KKBOX and nugs, not HIGHRESAUDIO. Its server does
  not run on a Pi: the Pi plays as a Roon Bridge, and the server runs on a computer (see
  [Roon on a Raspberry Pi](roon-raspberry-pi)). Roon costs $14.99 a month or $149.88 a year.

## Check what you get

- **Your subscription sets the ceiling.** Qobuz's highest quality, FLAC 24-bit up to 192 kHz,
  needs its Studio plan: €14.99 a month in France. TIDAL's goes up to 24-bit / 192 kHz.
- **The DAC shows what reaches it.** While a track plays,
  `cat /proc/asound/card0/pcm0p/sub0/hw_params` gives the rate it receives, `rate: 192000` for a
  24/192 album played untouched (see
  [How to check bit-perfect playback](check-bit-perfect-playback-linux)).

## With Audiogravi<sup>ty</sup>

The three services come with the Pro edition. They sit beside your own files and your UPnP media
servers, in one library and one search. Connect each one from **Library → Sources**: Qobuz and
Tidal through their own sign-in page, HIGHRESAUDIO with your email and password.
Audiogravi<sup>ty</sup> asks Qobuz and Tidal for their highest quality, and plays on the box's DAC,
on a UPnP renderer, or through HQPlayer. There is no Qobuz Connect and no TIDAL Connect: you choose
the music in Audiogravi<sup>ty</sup>.

The details are in the manual:
[Library & streaming → Streaming services](../manual/05-library-streaming#streaming-services).

## Sources

- upmpdcli 1.9.17: its [manual](https://framagit.org/medoc92/upmpdcli/-/blob/master/doc/upmpdcli-manual.txt) and [configuration reference](https://framagit.org/medoc92/upmpdcli/-/blob/master/doc/upmpdcli-config.txt), read on 2026-10-21; the modules, in its Debian 13 package list.
- Volumio: [editions and prices](https://volumio.com/get-started/), help on [streaming services](https://help.volumio.com/en/articles/8-what-audio-sources-can-i-add-to-volumio) and [TIDAL quality](https://help.volumio.com/en/articles/56-tidal-tracks-showing-as-16-bit-instead-of-24-bit-in-volumio), read on 2026-10-21. Qobuz Connect brands: [Qobuz help](https://help.qobuz.com/en/articles/314578-list-of-brands-integrated-into-qobuz-connect), updated on 2026-04-03.
- moOde 10.3.6: [Renderers](https://github.com/moode-player/moode/blob/r1036/www/templates/ren-config.html), [UPnP settings](https://github.com/moode-player/moode/blob/r1036/www/templates/upp-config.html), [build times](https://github.com/moode-player/moode/blob/r1036/www/install_renderers.txt) and [release notes](https://github.com/moode-player/moode/blob/r1036/www/relnotes.txt); [Pibuz](https://github.com/PhilipVinc/pibuz), 2.7.1.
- Lyrion plugins: [the official list](https://github.com/LMS-Community/lms-plugin-repository/blob/9d7afc19f5a3ed40a3cfd84d17c02d3af4269c03/extensions.xml), [Qobuz](https://github.com/LMS-Community/plugin-Qobuz) 3.7.3, [TIDAL](https://github.com/michaelherger/lms-plugin-tidal) 1.8.2, read on 2026-10-21.
- HQPlayer: [Signalyst](https://signalyst.com/), its [quick start guide](https://signalyst.com/quickstart-guide/) and shop, read on 2026-10-21.
- Roon: [compatibility](https://roon.app/en/compatibility) and [Linux install](https://help.roonlabs.com/portal/en/kb/articles/linux-install), read on 2026-10-21.
- Qobuz Studio: [plans](https://www.qobuz.com/fr-fr/music/streaming/offers/studio), France, read on 2026-10-21. TIDAL's quality: [HiRes FLAC](https://support.tidal.com/hc/en-us/articles/17412130162961-HiRes-FLAC-audio), updated on 2026-01-09.
