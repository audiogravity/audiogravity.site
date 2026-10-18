# Your NAS music on a Raspberry Pi streamer: mount the share, or use a UPnP server

**Short answer:** there are two ways, and many setups use both. Mount the NAS share on the
streamer: its player reads the files directly and keeps its own index of them. Or run a UPnP
media server on the NAS, such as MinimServer: the server keeps the index, and the streamer asks
it for each track over the network.

## Mounting the share

The NAS shares a folder over SMB (what Synology, QNAP and most NAS speak) or NFS, and the
streamer mounts it like a local disk. The player then reads the files as if they were on the box
and builds its own index from their tags: search, the album list and the order by date added
are the player's own.

What makes a mount reliable:

- **Read-only.** A music library does not need to be written to from the streamer.
- **No pinned SMB version.** Left alone, the system agrees with the NAS on the highest version
  both support. Avoid `vers=1.0` (SMB1), which is obsolete and insecure.
- **Waiting for the network, or mounting on access.** Mounted at boot, the share must wait for the
  network (`_netdev`). Mounted on first access instead, a NAS that is switched off when the
  streamer starts causes no trouble.
- **Indexing.** The player has to index the share before its music shows, and again to find what
  you add later. MPD, which many Raspberry Pi streamers use, does not watch for new files unless
  its `auto_update` option is turned on.

## Using a UPnP media server

A media server runs on the NAS (MinimServer, Plex and others), indexes the music there, and
publishes it on the network. A control app browses the server's index, and the player fetches
each track from the server over HTTP: nothing is mounted on the streamer.

- **One index for every player.** Any UPnP player in the house sees the same library, browsed
  the way the server arranges it.
- **Same network only.** UPnP devices find each other by announcing themselves on the local
  network: a server on another network segment or VLAN does not show up.
- **The original file, or not.** Some servers can convert formats on the fly. If you want the
  file as it is stored, check that yours sends it unchanged.

## Which one

- **Mount the share** if you want the streamer's own search and index, and no server to run.
- **Use a UPnP server** if one already serves your other players, or if you like the way it
  arranges the library.
- **Both work side by side.** A NAS can share a folder and serve it through its UPnP server at the
  same time; the two paths reach the same files.

## With Audiogravi<sup>ty</sup>

**Mounting from the app.** In the **Music library** picker of the guided setup, **Add network
share (NAS)** asks for a name, the NAS address, the share, and a username and password unless the
share is open to guests. Audiogravi<sup>ty</sup> mounts the share and tests it on the spot: you
see it appear, or the actual error, such as a wrong password or an unreachable NAS. The share is
mounted read-only, on first access, so a NAS that is off when the box starts causes no trouble;
the password is kept in a file only the system can read. Once you confirm it as the library,
MPD points at it and starts indexing, with an indicator until it is done.

**NFS from the terminal.** The app mounts SMB only, so as not to add NFS's own services to every
box. A share you mount yourself under `/mnt`, NFS or SMB, is offered as a library just the same.

**UPnP servers** (Pro). **Library → Sources** lists the servers Audiogravi<sup>ty</sup> already
knows, and **Re-scan** looks for more. You browse a server's tree, search it when the server
supports search, and play what you find: on the DAC attached to the box, on a UPnP renderer, or
through HQPlayer. A track in a format HQPlayer cannot read reaches it converted to FLAC, without
loss; the file on your NAS is never touched.

The details are in the manual:
[First run → Music on a NAS](../manual/03-first-run#music-on-a-nas-add-the-share-from-the-picker),
[Troubleshooting → Manual NAS mount](../manual/09-troubleshooting#manual-nas-mount-terminal),
and [Library & streaming → UPnP / DLNA media servers](../manual/05-library-streaming#upnp--dlna-media-servers).

## Sources

- MPD's `auto_update`, off by default: [mpd.conf(5)](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/mpd.conf.5.rst), version 0.24.5.
