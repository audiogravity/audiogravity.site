# Your NAS music on a Raspberry Pi streamer: mount the share, or use a UPnP server

**Short answer:** there are two ways, and many setups use both. Mount the NAS share on the
streamer: its player reads the files directly and keeps its own index of them. Or run a UPnP
media server on the NAS, such as MinimServer: the server keeps the index, and the streamer plays
each track from it over the network. If you mount the share, have it mounted when the folder is
first opened rather than at startup: a NAS that is off then delays nothing, and your player's
index survives it.

Checked on 2026-10-21 on Debian 13, the base of today's Raspberry Pi OS (cifs-utils 7.4,
nfs-common 2.8.3, systemd 257, MPD 0.24.5), against a Samba file server over SMB 3.1.1 and an
NFS 4.2 server. DietPi and the UPnP servers: from their documentation and source code, read but
not run, at the versions named below.

## What to note on the NAS

- **Its address.** An IP address, such as `192.168.1.20`, works on any network; a name works only
  if your network resolves it. Reserve the address in your router, so that it never changes.
- **For SMB**, what Synology, QNAP, Windows and macOS shares speak: the share's name, and an
  account allowed to read it. Read-only access is enough. On a Synology, the SMB versions it
  accepts are under **Control Panel → File Services → SMB → Advanced Settings**.
- **For NFS**: the folder's path on the NAS, and a rule on the NAS that lets the streamer's
  address read it. As usually set up, NFS asks for no password: the NAS goes by address. On a
  Synology, tick **Enable NFS service** under **Control Panel → File Services → NFS**, then, for
  the shared folder, **Edit → NFS Permissions → Create**, with the streamer's address under
  **Hostname or IP**.

## Mount the share on Raspberry Pi OS or Debian

### SMB

Raspberry Pi OS comes with SMB's mount tool, `cifs-utils`. Elsewhere, install it:

```bash
sudo apt install cifs-utils
```

Keep the NAS account in a file only root can read: create it empty, then write two lines in it.

```bash
sudo install -m 600 /dev/null /root/.smbcredentials
sudo nano /root/.smbcredentials
```

```text nocopy
username=nasuser
password=naspassword
```

Then add one line to `/etc/fstab` (`sudo nano /etc/fstab`), with your NAS's address and share:

```text nocopy
//192.168.1.20/music  /mnt/music  cifs  credentials=/root/.smbcredentials,ro,nofail,x-systemd.automount  0  0
```

- **`x-systemd.automount`** mounts the share when the folder is first opened, and **`nofail`**
  lets the streamer start as usual when the NAS is off.
- **`ro`** mounts it read-only: a player writes nothing there.
- **No version.** The streamer and the NAS agree on the newest SMB version both speak, from 2.1
  up: 3.1.1 with the server above. A NAS too old for SMB 2.1 needs its version written, `vers=2.0`
  or `vers=1.0`; SMB1 is insecure, so update the NAS if you can.
- **A space in the share's name** is written `\040` in this file.

### NFS

NFS's mount tool, `nfs-common`, is missing from Raspberry Pi OS Lite. Install it if need be:

```bash
sudo apt install nfs-common
```

The line for `/etc/fstab`:

```text nocopy
192.168.1.20:/volume1/music  /mnt/music  nfs  ro,nofail,x-systemd.automount  0  0
```

To see which folders the NAS exports, and to which addresses:

```bash nocopy
showmount -e 192.168.1.20
```

```text nocopy
Export list for 192.168.1.20:
/volume1/music 192.168.1.0/24
```

### Start it, and check

```bash
sudo systemctl daemon-reload
sudo systemctl start mnt-music.automount
ls /mnt/music
```

The second command is named after the folder: `/mnt/music` gives `mnt-music`. After a restart,
there is nothing to start by hand. Your music's folders should be listed; then check that the
account your player runs as can read them — for MPD:

```bash
sudo -u mpd ls /mnt/music
```

With SMB and the options above, every file is readable by every account. With NFS, files keep the
permissions they have on the NAS.

### When it fails

If `ls` answers `No such device`, the share could not be mounted. The reason is in:

```bash
sudo systemctl status mnt-music.mount
```

| Message | What it means |
|---|---|
| `mount error(13): Permission denied` | Wrong username or password, or a share that refuses guests. |
| `mount error(2): No such file or directory` | No share by that name on the NAS. |
| `mount error(95): Operation not supported` | No SMB version in common, such as `vers=1.0` with a NAS that has SMB1 off. |
| `mount error: could not resolve address for mynas: Unknown error` | Your network does not know that name: use the address. |
| `mount error(113): could not connect to 192.168.1.20Unable to find suitable address.` | SMB: the NAS is off, or out of reach. It takes about six seconds. |
| `mount: /mnt/music: cannot mount //192.168.1.20/music read-only.` | `cifs-utils` is not installed. |
| `mount.nfs: access denied by server while mounting 192.168.1.20:/volume1/music` | The path is wrong, or the NAS does not let this address in. |
| `mount.nfs: Failed to resolve server mynas: Name or service not known` | Your network does not know that name. |
| `Mounting timed out. Terminating.` | NFS: the NAS is off, or out of reach. Opening the folder waits a minute and a half first. |
| `mount: /mnt/music: fsconfig() failed: NFS: mount program didn't pass remote address.` | `nfs-common` is not installed. |

For SMB, `sudo dmesg` adds the NAS's own answer: `STATUS_LOGON_FAILURE` for a wrong password,
`BAD_NETWORK_NAME` for a wrong share.

### On DietPi

`dietpi-drive_manager`, then **Add network drive**, then **Samba** or **NFS**, asks for the
address, the share, the account and where to mount it, installs the tools, and writes the
`/etc/fstab` line itself, with `x-systemd.automount` as above. For SMB, it tries the versions from
3.1.1 down, and keeps the first that mounts.

## Have the player index it

MPD, on Raspberry Pi OS or Debian: set the folder in `/etc/mpd.conf`,

```text nocopy
music_directory "/mnt/music"
```

then restart MPD and have it index the share (`mpc` comes with `sudo apt install mpc`):

```bash
sudo systemctl restart mpd
mpc update --wait
mpc stats
```

`mpc stats` counts the songs MPD found.

- **Music added later is not seen on its own.** MPD's `auto_update` relies on the kernel's file
  notifications, inotify, and inotify "does not catch remote events that occur on network
  filesystems". Run `mpc update` after adding music.
- **Update with the share there.** On my test box (2026-10-21), an update run while the share was
  not mounted found an empty folder, and removed every song from MPD's index without a word.
  With `x-systemd.automount` and the NAS off, MPD logged `Failed to open /mnt/music: No such
  device` instead, and kept them all.

## Use a UPnP server instead

A media server on the NAS indexes the music there and publishes it on your network. A control app
browses that index and has the streamer play each track, fetched from the server over HTTP:
nothing is mounted on the streamer.

- **On the NAS.** MinimServer has packages for Synology and QNAP, among others; MiniDLNA (also
  called ReadyMedia) and Asset UPnP are other servers. Point the server at your music folder: it
  reads the tags, and arranges the library its own way.
- **The original file, or not.** MiniDLNA never converts. MinimServer converts only once you add
  its MinimStreamer package and fill in its `stream.transcode` setting, which takes a full licence.
  Asset UPnP lets you choose, format by format, between sending the file as it is and converting
  it.
- **On the streamer, a renderer.** On Raspberry Pi OS or Debian, upmpdcli makes MPD one; it is not
  in Debian's archive, and its author distributes it from
  [lesbonscomptes.com/upmpdcli](https://www.lesbonscomptes.com/upmpdcli/). Control apps list it
  under a name that starts with `UpMpd-`.
- **To choose the music, a control app**, such as BubbleUPnP (Android) or mconnect Player (iPhone,
  iPad, Android).
- **Same network.** UPnP devices find each other through announcements sent to the whole local
  network. The NAS, the streamer and the phone must be on the same network: a guest Wi-Fi or
  another VLAN hides them from each other, unless your router passes those announcements on.

## Which one

- **Mount the share** if you want the streamer's own search and index, and no server to run.
- **Use a UPnP server** if one already serves your other players, or if you like the way it
  arranges the library.
- **Both work side by side.** A NAS can share a folder and serve it through its UPnP server at the
  same time; the two paths reach the same files.

## With Audiogravi<sup>ty</sup>

**Add network share (NAS)**, at the bottom of the **Music library** picker of the guided setup,
mounts an SMB share as above — read-only, when first opened, the password in a file only the
system reads — and tests it on the spot: you see the share appear, or the error. Once you confirm
it as the library, MPD indexes it. An NFS share, or any share you mount yourself under `/mnt`, is
offered in the same picker. With Pro, **Library → Sources** lists the UPnP servers of your
network, and takes the address of one on another part of it; you browse and search them, and
play on the box's DAC, on a UPnP renderer, or through HQPlayer.

The details are in the manual:
[First run → Music on a NAS](../manual/03-first-run#music-on-a-nas-add-the-share-from-the-picker),
[Troubleshooting → Manual NAS mount](../manual/09-troubleshooting#manual-nas-mount-terminal),
and [Library & streaming → UPnP / DLNA media servers](../manual/05-library-streaming#upnp--dlna-media-servers).

## Sources

- Mount options: [mount.cifs(8)](https://manpages.debian.org/trixie/cifs-utils/mount.cifs.8.en.html), cifs-utils 7.4; [nfs(5)](https://manpages.debian.org/trixie/nfs-common/nfs.5.en.html), nfs-common 2.8.3; [systemd.mount(5)](https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html), systemd 257 — Debian 13, read on 2026-10-21.
- What Raspberry Pi OS installs: the [Lite image's package list](https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2026-10-06/2026-10-06-raspios-trixie-arm64-lite.info), release of 2026-10-06.
- File notifications on network shares: [inotify(7)](https://man7.org/linux/man-pages/man7/inotify.7.html), *Limitations and caveats*. MPD's `auto_update`: [mpd.conf(5)](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/mpd.conf.5.rst), and the code that watches the folder, [InotifyUpdate.cxx](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/src/db/update/InotifyUpdate.cxx), version 0.24.5.
- Synology: [SMB protocols](https://kb.synology.com/en-global/DSM/tutorial/Why_cant_access_shared_folder) and [NFS permissions](https://kb.synology.com/en-global/DSM/help/DSM/AdminCenter/file_share_privilege_nfs?version=7), DSM 7, read on 2026-10-21.
- DietPi 9.20: [dietpi-drive_manager](https://github.com/MichaIng/DietPi/blob/v9.20/dietpi/dietpi-drive_manager).
- MinimServer 2.2: [transcoding](https://minimserver.com/ug-other.html) and [downloads](https://minimserver.com/downloads.html). MiniDLNA 1.3.3: its [to-do list](https://sourceforge.net/p/minidlna/git/ci/v1_3_3/tree/TODO), where transcoding is a wish. Asset UPnP: [audio streaming options](https://doc.dbpoweramp.com/asset/en/custom.htm).
- upmpdcli 1.9.17: its default name, in the `/etc/upmpdcli.conf` of its package.
- UPnP discovery: [UPnP Device Architecture 2.0](https://openconnectivity.org/upnp-specs/UPnP-arch-DeviceArchitecture-v2.0-20200417.pdf), section 1.
