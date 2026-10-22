# Your streamer on the network: how much bandwidth music takes, Wi-Fi or cable, and VLANs

**Short answer:** music takes little bandwidth: about 1.4 Mbit/s at CD quality and 9.2 Mbit/s at
24 bits and 192 kHz, before lossless compression shrinks it. Only HQPlayer feeding an NAA at DSD512
or 768 kHz needs around 50 Mbit/s. A steady Wi-Fi link carries the rest; a cable removes the
question. What breaks more setups is discovery: AirPlay, UPnP and the NAA find each other with
messages that stay on the local network, so a guest Wi-Fi or another VLAN hides devices unless the
router passes those messages on.

Checked on 2026-10-22: measured on a Raspberry Pi 4 under Raspberry Pi OS, wired and on Wi-Fi, on a
Debian 13 box on Wi-Fi, and on music files; the protocols from their standards, the routers from
their makers' documentation, the NAA from HQPlayer's author.

## How much bandwidth music takes

| Stream, stereo | Rate, uncompressed |
|---|---|
| 16 bits, 44.1 kHz (CD) | 1.41 Mbit/s |
| 24 bits, 96 kHz | 4.61 Mbit/s |
| 24 bits, 192 kHz | 9.22 Mbit/s |
| DSD64 | 5.64 Mbit/s |
| DSD128 | 11.29 Mbit/s |
| DSD256 | 22.58 Mbit/s |
| HQPlayer to an NAA, DSD512 | 45.16 Mbit/s |
| HQPlayer to an NAA, PCM 768 kHz, 32 bits | 49.15 Mbit/s |

- **Lossless compression takes less.** FLAC and ALAC carry the same music in fewer bits: in a
  sample of 147 CD-quality ALAC files, the median needed 861 kbit/s, 61 % of 1,411. Files that
  are not compressed, WAV and DSF, measured their full rate.
- **HQPlayer sends an NAA its finished output**, at the full rate of what it converts to, whatever
  the file's own rate. DoP or native DSD makes no difference: DoP is handled at the NAA, in
  HQPlayer's author's words.

## Wi-Fi or cable

The Raspberry Pi 4 and 5 have Gigabit Ethernet and dual-band 802.11ac Wi-Fi. To see your Wi-Fi
link, on the Pi:

```bash
/sbin/iw dev wlan0 link
/sbin/iw dev wlan0 get power_save
```

On the Pi 4 above, shortened:

```text nocopy
signal: -64 dBm
rx bitrate: 150.0 MBit/s
tx bitrate: 24.0 MBit/s
Power save: on
```

- **The bitrates are what the link is set at**, not what it delivers: test what it delivers with
  iperf3, below.
- **Power saving is on by default** on a Raspberry Pi, as above. Raspberry Pi's documentation
  offers to turn it off in `raspi-config`, an option "that we don't recommend setting unless
  instructed to by a Raspberry Pi engineer": it "might improve connection stability but increase
  power consumption".
- **How steady the link is**: with your router's address,

  ```bash nocopy
  ping -c 100 -i 0.2 192.168.1.1
  ```

  The last two lines give the losses and the slowest answer. The Pi 4 above, pinged from a computer on
  Wi-Fi, answered in 1.4 ms on average and 2.5 ms at worst through its cable, 5.3 and 7.5 ms on
  Wi-Fi, with no loss either way.
- **Whether it carries 50 Mbit/s**, for an NAA: install iperf3 on the Pi and on another computer
  (`sudo apt install iperf3`), run `iperf3 -s` on the computer, then on the Pi, with the computer's
  address:

  ```bash nocopy
  iperf3 -c 192.168.1.30 -u -b 50M -t 10 -R
  ```

  `-R` has the other computer send, as HQPlayer does. The `receiver` line gives the rate reached,
  the jitter and the datagrams lost: losses at 50M mean the link is short for DSD512.
- **For DSD512 and 768 kHz, a cable.** HQPlayer's author writes that "Ethernet provides practically
  unlimited reliable bandwidth with galvanic isolation (NAA works over WiFi as well)"; in one of
  his tests, DSD512 did not get through Wi-Fi to an NAA where DSD256 did (January 2025).

## Finding each other across the network

- **AirPlay** announces itself with mDNS: messages to 224.0.0.251, port 5353, an address routers
  do not pass on.
- **UPnP** media servers and renderers announce themselves with SSDP: messages to
  239.255.255.250, port 1900, which a router passes on only when set to. On my test network, a
  media server one router away answered when asked by its address, not to a discovery search
  (2026-10-21).
- **HQPlayer and its NAA** have a discovery of their own, which is not mDNS. Keep them on the same
  network, and the computer running HQPlayer without a second network connection, such as a VPN:
  its discovery could go out the wrong way, in its author's words.

So the Apple device, the control app, the server and the streamer must be on the same network: a
guest Wi-Fi or another VLAN hides them from each other. To cross VLANs anyway, the router must pass
the messages on, and its firewall must let the devices talk:

- **For mDNS (AirPlay)**, a reflector: Avahi's `enable-reflector=yes` on a Linux router, the
  *mDNS Proxy* of a UniFi gateway, the *mDNS Repeater* plugin of OPNsense, *Enable reflection* in
  pfSense's Avahi package.
- **For SSDP (UPnP)**, a separate relay: the *UDP Broadcast Relay* of pfSense and OPNsense, set to
  239.255.255.250 and port 1900. pfSense's documentation: "Firewall rules are not automatically
  created".
- **IGMP snooping**, on managed switches, filters multicast: mDNS's addresses always get through,
  SSDP's may not. Ubiquiti's advice, for audio and video on its switches: "enable IGMP Snooping
  and define a specific switch as the querier". HQPlayer's author: with such equipment, "the network infrastructure must be up before
  NAA and HQPlayer are started".

## With Audiogravi<sup>ty</sup>

Its **Network test**, in the Performance tab (Pro), runs the same ping, or an iperf3 test at the
rate you set, and gives a verdict. In **Library → Sources**, a UPnP server on another network can
be added by its address, which discovery cannot cross.

The details are in the manual:
[Administration → Network test](../manual/07-administration#network-test), and
[Troubleshooting → A UPnP renderer or media server isn't discovered](../manual/09-troubleshooting#a-upnp-renderer-or-media-server-isnt-discovered).

## Sources

- Raspberry Pi: [Pi 4](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-product-brief.pdf) and [Pi 5](https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-product-brief.pdf) product briefs, October 2026; WLAN power saving in its [networking documentation](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/configuration/configuring-networking.adoc). Read on 2026-10-22.
- mDNS: [RFC 6762](https://www.rfc-editor.org/rfc/rfc6762), and [RFC 5771](https://www.rfc-editor.org/rfc/rfc5771) for the addresses not forwarded off the link. SSDP: [UPnP Device Architecture 2.0](https://openconnectivity.org/upnp-specs/UPnP-arch-DeviceArchitecture-v2.0-20200417.pdf), section 1. IGMP snooping: [RFC 4541](https://www.rfc-editor.org/rfc/rfc4541).
- Avahi: [avahi-daemon.conf(5)](https://manpages.debian.org/trixie/avahi-daemon/avahi-daemon.conf.5.en.html). UniFi: [mDNS Proxy](https://help.ui.com/hc/en-us/articles/12648701398807-UniFi-Gateway-Multicast-DNS-mDNS-Proxy) and [Pro AV traffic](https://help.ui.com/hc/en-us/articles/18125733726615-Pro-AV-Traffic-Optimization-on-UniFi-Switches). OPNsense: [multicast DNS](https://docs.opnsense.org/manual/how-tos/multicast-dns.html). pfSense: [UDP Broadcast Relay](https://docs.netgate.com/pfsense/en/latest/packages/udpbroadcastrelay.html). Read on 2026-10-22.
- iperf3 3.18: [iperf3(1)](https://manpages.debian.org/trixie/iperf3/iperf3.1.en.html), Debian 13.
- Jussi Laako, who writes HQPlayer, on the Roon forum: [bandwidth](https://community.roonlabs.com/t/ifi-zen-stream/163860/1883) (April 2022), [DoP at the NAA](https://community.roonlabs.com/t/hqp-naa-raspberry-pi/6140/209) (February 2018), [Ethernet and Wi-Fi](https://community.roonlabs.com/t/usbridge-signature-at-dsd256-works-raat-but-fails-naa-audio-dropouts/226931/19) (December 2022), [DSD512 over Wi-Fi](https://community.roonlabs.com/t/m4-pro-mac-mini/284772/81) (January 2025), [discovery](https://community.roonlabs.com/t/hqplayer-client-setup-add-host-for-later-use/247384/9) (July 2023) and [IGMP](https://community.roonlabs.com/t/hqplayer-naa-thread/176288/571) (November 2024).
