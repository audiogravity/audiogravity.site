# Audiogravi<sup>ty</sup> — Release Notes

Synthesized overview of each release. For the full line-by-line changelog, see
[CHANGELOG.md](CHANGELOG.md).

---

## Unreleased

### Services and profiles come from Audiogravi<sup>ty</sup>

The audio services the box drives, and the profiles that start and stop them, are now
defined by Audiogravi<sup>ty</sup> itself.

**No more export or import.** The Settings panel no longer offers *Export Configuration*
and *Import Configuration*: an import would overwrite what Audiogravi<sup>ty</sup> defines,
and the export only existed to be imported again.

---

## 0.9.61 — 2026-09-25

### Your Qobuz playlists, managed from the box

Everything the box does with your HIGHRESAUDIO playlists, it now does with your Qobuz ones:
you fill them, open them, play them from any track and tidy them up, without Qobuz's own
applications.

**Adding.** In the full-screen player, the button beside the title adds the Qobuz track
playing now; on Qobuz's album covers and in the album rows of a search, the same button
sits next to the star. It opens your playlists with **New playlist** at the top: tap one,
or name a new one and the track or the album goes straight into it.

**Nothing goes in twice.** Qobuz keeps a track added twice, and its own protection refuses
a whole album as soon as one of its tracks is already there. So the box looks at the
playlist first and sends only what it lacks; the message says what went in and what was
already there.

**A new playlist is private.** Qobuz makes a playlist public unless told otherwise, which
shows it on your public profile. The box creates yours private; making one public is done
from a Qobuz app.

**A playlist opens on a page of its own.** The **open** button, at the bottom left of the
cover, shows its tracks, and a tap on a track plays the playlist from there. The selections
Qobuz publishes open the same way, and each of their tracks can be copied into one of your
playlists.

**Your own playlists, edited in place.** On one of yours, a track comes out with one tap —
every copy of it, if it was there twice; the pencil renames the playlist and edits its
description; the bin deletes it, once you confirm. **New playlist**, the first tile of
*Mine*, creates an empty one. A playlist you follow without owning it stays read-only: only
its owner can change it.

**Long playlists are read to the end.** Qobuz hands a playlist out 500 tracks at a time,
and the box used to stop there; it now reads every track, however long the playlist.

Tidal is not written yet.

### Installing software survives a restart

Some installations take a minute: HQPlayer Embedded downloads 120 MB, then sets itself
up. Until now, restarting Audiogravi<sup>ty</sup> during that minute — or updating it,
or restarting the box — killed the installation halfway, and left the system's package
manager in a state where nothing more could be installed until a command had been typed
on the box.

**Restarting waits for the installation.** While something is being installed,
**Restart Core**, **Reboot OS** and the update of Audiogravi<sup>ty</sup> say what is
being installed and ask you to try again once it has finished. Stopping or restarting
the core from **Services** gets the same answer. A reboot and an update wait for any
installation on the box, including one started from the Terminal tab or over SSH.

**A stop that comes anyway lets the installation finish.** If the core is stopped all
the same — the box shutting down, a command typed on it — it first lets an installation
already under way finish, for up to four minutes, and then stops. One that had not
started yet — still downloading, or waiting its turn — is called off and says so,
rather than starting in the middle of the stop.

**A restart is quicker when nothing is installing**: about five seconds, where a page
left open on the box used to hold it until it was forced to stop.

### When the package manager needs repairing, you are told how

If an earlier installation was cut short all the same — by a power cut, say — the
system's package manager refuses every change until it is repaired.
Audiogravi<sup>ty</sup> found that out only after downloading the package, and then
reported a bare *Installation failed*. It now checks first and tells you, before
anything is downloaded, with the command that repairs the box:
`sudo dpkg --configure -a`. The **Terminal** tab (System, admin) is now allowed to run
it, and the manual's troubleshooting chapter walks you through it. If another
installation is simply still running, you are told that instead.

### The version offered is the right one

Right after installing HQPlayer Embedded, its card could offer a version older than the
one just installed — *Older version offered*. For software Audiogravi<sup>ty</sup>
downloads from its vendor, the page now asks the vendor only, and asks again as soon as
an installation, an update or a removal ends.

### A service setting that goes wrong no longer takes the box with it

The **Systemd** tab lets you tune how each audio program runs: its priority, the
processor cores it uses, its memory and file limits. A setting the system refuses used
to be saved all the same: the program then failed at every start, and the system kept
restarting it every two seconds, for as long as nobody noticed. On a lab box, HQPlayer
Embedded did so for two hours, and every profile tile naming it stayed on PENDING.

**Settings a program cannot start with are refused before they are saved**, with the
reason: a real-time priority without a real-time policy and the reverse, a processor
core the box does not have, a memory limit under 16 MB, an open-file limit under 1024.
The memory limit matters most: at 1 KB, it is not the program that stops, it is the
whole box's service manager that freezes. **Validate** says the same.

**A change that stops the program is undone.** Audiogravi<sup>ty</sup> restarts the
program on its new settings and watches it for a few seconds; if it does not stay up,
the previous settings are put back and the program started again, and you are told.
A program that is not running is no longer started by a save: its new settings apply
when it next starts.

**A failure reads as one.** A program the system keeps restarting now shows as
failed, never as starting. The profile you are using reads **FAILED** in red, and
**Activate** on it starts again what failed; the other profiles are left as they are,
with a small count of what failed among their programs. **Stop all** stops a program
caught in such a loop, which it could not before.

**Restore Backup works on the box.** It never did outside a development machine: the
system refused the command it used. It now brings back the settings the last change
replaced.

### Your licence after reinstalling the system: one address to write to

Reinstalling the operating system, or moving Audiogravi<sup>ty</sup> to another machine,
gives the box a new Device ID, and a licence belongs to the Device ID it was activated
on. The licence portal cannot hand it back to the new one, the old licence file is
refused, and the key answers that no licence exists for this device. The manual, the
licence panel and the emails that deliver a key or a licence said the opposite — the
portal was presented as the way back after a reinstall since 0.9.31.

They now tell it as it is. Reinstalling Audiogravi<sup>ty</sup> itself, on the same
system, changes nothing: the key and the portal still bring your licence back. After a
new system or a new machine, write to support@audiogravity.app with your Order ID and the
new Device ID, and your licence is reset. The manual's troubleshooting chapter lists the
messages you would see, and its backup instructions no longer restore the old licence
file, which would have kept even the free trial from starting.

---

## 0.9.60 — 2026-09-23

### Your HIGHRESAUDIO playlists, managed from the box

Your HIGHRESAUDIO playlists no longer need HIGHRESAUDIO's own applications: from
Audiogravi<sup>ty</sup> you fill them, open them, play them from any track, and tidy
them up.

**Adding.** The track you are listening to, or a whole album, goes into one of your
playlists without leaving the player. In the full-screen player, a button beside the
title adds the track playing now; on HIGHRESAUDIO's album covers and in the album rows
of a search, the same button sits next to the star. It opens a window with your
playlists and **New playlist** at the top: tap one, or name a new one and the track or
the album goes straight into it.

**Nothing goes in twice.** HIGHRESAUDIO accepts a track a playlist already holds and
keeps both copies — and a later removal takes out every copy at once. So the box looks
at the playlist first and sends only what it lacks. The message says what happened: the
track was added, it was already there, or, for an album, how many tracks went in and how
many were already there.

**An album arrives whole, and once.** HIGHRESAUDIO's own way of adding an album puts its
last track in twice. The box sends the album's tracks as a list instead, in the album's
order.

**A playlist opens on a page of its own.** Tapping a playlist still plays it; its new
**open** button, at the bottom left of the cover, shows what it holds — its name, its
description, how many tracks and how long, then the tracks. **Play** and **Queue** take
the whole of it, and a tap on a track plays the playlist from there. The selections
HIGHRESAUDIO publishes open the same way, and each of their tracks can be copied into one
of your playlists.

**Your own playlists, edited in place.** On one of yours, a track comes out with one tap;
the pencil renames the playlist and edits its description; the bin deletes it, once you
confirm. **New playlist**, the first tile of your playlists, creates an empty one to fill
later.

**What you see is what your account holds.** HIGHRESAUDIO's own list lags a few seconds
behind every change; the box shows a playlist just created, renamed or deleted as it now
is, everywhere, meanwhile. A playlist deleted elsewhere is said to be gone rather than
shown empty, and a track tapped in a playlist that changed in the meantime still starts
the right track.

Purchases (the Vault) have playlists of their own and are not offered these buttons, and
Qobuz and Tidal are not written yet.

### Nothing hides under the mini-player any more

On a phone, the last lines of a list — the library, and the other tabs too — could stay
under the mini-player at the bottom of the screen, whatever the scroll. They now always
clear it, and clear its small pull tab when the player is folded away. With the phone on
its side, the top of the library no longer sits under the top bar either, and in a low
window on a computer, with the tabs shown as a bar, the tabs can be reached again.

---

## 0.9.59 — 2026-09-23

### HQPlayer Embedded, installed from Audiogravi<sup>ty</sup>

Until now Audiogravi<sup>ty</sup> could install the adapter that carries HQPlayer's sound
to your DAC, but not HQPlayer itself. It can now: HQPlayer Embedded appears on the Audio
Software page beside the rest of the stack, for Debian 13 on Intel and on 64-bit ARM.

**You choose the version — among those this machine can actually run.** Signalyst keeps
two major lines published side by side, and only you know which one your licence covers.
So Audiogravi<sup>ty</sup> does not take the newest by default: it shows the newest build
of each line. But before offering one, it checks with the system that everything the
package needs can be installed. On Debian 13 today that rules out the 5 line — it depends
on a library called `libgmpris` that neither Debian nor Signalyst publishes — so you will
see it named, with that reason, rather than offered as a choice that would leave a
half-installed package behind. Once installed, your line is held: updates stay on it, and
moving to another major stays a decision you make. Signalyst's licence provides for a
time-limited trial.

**And you read the licence first.** Signalyst puts its end-user licence agreement on a
screen its own installer shows. Audiogravi<sup>ty</sup> installs without that screen, so
until now the agreement was accepted on your behalf, by nobody — and that was already
true of the adapter, on every box. Both licences are now read straight out of the package
and shown before anything is downloaded, and the install waits until you accept. That
wait is enforced by Audiogravi<sup>ty</sup> itself, not just by the screen. If the licence
cannot be fetched, you are told so and asked to accept all the same, instead of seeing
nothing.

**A password for its web interface, set for you.** HQPlayer Embedded has its own web
interface, and its package installs it with no password at all: nobody can open the
settings, and every attempt fills a log. The install dialog proposes a random password,
shown in clear so you can note it down; Audiogravi<sup>ty</sup> sets it right after the
install and restarts HQPlayer once, when it has finished starting, so that it takes it. If
it could not be set, the card of the installed package offers *Set web password* — no need
to uninstall and start again. The password is written in no log, the system's included.

**A log that cannot fill the box's memory.** HQPlayer writes its log to memory, with no
limit and never emptied, and a loop in it once wrote 600 MB a minute there. The log now
gets 10 MB of memory of its own, which the system does not let it exceed; HQPlayer keeps
playing when it is full, and nothing is ever written to disk.

**Part of your profiles.** HQPlayer Embedded is started, stopped and switched to like the
rest of the stack, and it takes the DAC from the adapter and gives it back. Two profiles
run it: *MPD HQPlayer Embedded* keeps MPD running beside it, so your own library plays
through it too; *HQPlayer Embedded* stops MPD as well. If you remove it from your
configuration, it stays removed. A stop it would ignore right after starting now ends
within 15 seconds instead of 90.

**Your music plays through it.** While HQPlayer Embedded runs, what you start from the
Library goes to it, and from it straight to your DAC — there is no adapter in between, and
nothing asks for one. The HQPlayer card says *This box*, with *Use as output* on and locked
for as long as it runs. If you had chosen an HQPlayer on your network, it is kept, with its
own settings and its DSP choices; the card goes back to it when HQPlayer Embedded stops.
The player shows what is playing, and the signal path starts from HQPlayer Embedded. A
format HQPlayer cannot decode is converted to FLAC on the way out (see below); what stays
refused is refused before anything is sent, with advice you can follow: a profile that
stops it.

**Its output is chosen here; everything else on its own page.** HQPlayer Embedded has no
output after installation. You choose it in **Config**, on its tile, exactly as for MPD or
AirPlay — and only that setting changes: its filters, its modulators and its DSD rate stay
what you set in its web interface. It is restarted to take the new output only if it is
running; a save never starts it, since it takes your DAC as soon as it starts.

**Its DSD rate, before the first play.** HQPlayer Embedded comes set to DSD256, and a DAC
that does not go that high does not refuse it: it hisses, and keeps hissing after the music
stops. Audiogravi<sup>ty</sup> cannot tell — a DAC does not say which DSD rates it
converts. So the manual shows where to set the limit on HQPlayer's own page before you play
anything, and what to do if you hear the hiss.

**When a step after the install cannot be done**, the card says the package is installed
and what is left to do — *Incomplete*, not *Failed* — and *Update all* now says so too.
And a restart Audiogravi<sup>ty</sup> has just done itself is no longer asked of you.

Several things were fixed on the way, and they matter for every piece of software in the
stack. A package used to be downloaded into `/tmp`, which on these boxes is memory rather
than disk: a 144 MB download would have been 144 MB of RAM held while your music played.
The space a package unpacks to — 257 MB for this one — was never checked, so a full disk
broke an installation halfway instead of refusing it at the start. A package from its
vendor was installed in a way that always stopped on missing libraries and let apt repair
afterwards — so even a successful install showed a string of red errors, and an install
that apt "repaired" by removing the package was announced as a success. It now installs
with its libraries in one step, and success is confirmed with the system. And when an
install is turned down, you now read why.

Removing a package also changed: it now keeps your settings, and erasing them is a
separate, explicit choice. For HQPlayer that distinction is every filter and modulator
you chose.

The manual has a section on HQPlayer Embedded, in *Outputs & engines*: installing it,
choosing its output, setting its DSD rate, switching to it, playing through it. It needs a
licence from Signalyst. What to do when its password is lost, or when the DAC hisses, is in
*Troubleshooting*.

Two fixes concern an HQPlayer on your network as well. The support report now describes
the HQPlayer you actually use — the one chosen in the card, which it used to miss, saying
*not configured* — and which one plays when the box runs its own. And with HQPlayer as the
output, a start-up where the adapter started at the same moment no longer leaves every play
refused until the adapter restarts.

**The 30-minute trial says its name.** Signalyst lets you run HQPlayer Embedded without a
licence key, but only 30 minutes at a time — and the half hour counts from the moment
HQPlayer Embedded **starts**, not from the moment you press play. Spend it setting your
output and your DSD rate, and there is none of it left for music; the vendor's own wording,
"plays for 30 minutes at a time", does not suggest that, and measuring it is how we know.
What happens at the end looks exactly like a breakdown: HQPlayer keeps running and keeps
your DAC, its own web page still answers, but it stops taking commands — so the music stops
and Audiogravi<sup>ty</sup> shows it as unavailable, with nothing to explain it. It cannot
explain it: HQPlayer writes that limit in no log, so all the box ever reads is a player gone
quiet. The limit is now told where you can still do something about it — in the install
window before anything is downloaded, on the package's card once it is installed, and in the
manual, which says to restart it from **Services** and to start your music again, since the
restart leaves HQPlayer with an empty queue. A licence from Signalyst removes the limit.
Audiogravi<sup>ty</sup> will not restart it for you: that would work around a limit its
maker set, and cut your music without warning.

**And its settings page is one click away.** HQPlayer's filters, its modulators, its DSD
rate and its licence key live on a web page of its own — the one the manual keeps sending
you to, and which you had to reach by typing your box's address followed by `:8088`. The
HQPlayer card, in **Library → Sources**, now has a **Web interface** button beside its DSP
controls. It shows up only for the HQPlayer running on your box, since one on your network
has no such page — and it stays there when the card says HQPlayer is offline, which is when
you need it most: that page answers even when the rest of HQPlayer has stopped, and it is
where you enter the licence key.

**Five rough edges on the way to HQPlayer.** They are small, and you meet them daily.
Adding tracks to an album already playing used to blank its title, its artist and its cover
a few seconds later, and for good: HQPlayer takes about five seconds to acknowledge a
longer playlist, and Audiogravi<sup>ty</sup> read that delay as a playlist that was no
longer its own. A command — next, previous, pause, a jump within the track — was reported
as failed whenever HQPlayer took more than three seconds to answer, although it had
carried it out; measured, an HQPlayer on the network takes up to 4.5 seconds to answer the
first command of a connection, even when it is stopped. Starting an album now says it is on
its way, instead of leaving the screen still for the seconds the tracks take to go over.
The tracks HQPlayer accepts and then quietly drops — a file it cannot open, an address it
cannot reach — are named on screen, where the album simply played short. And an HQPlayer
designated by its name rather than its address is now told the right address to fetch your
files from, instead of the box's default route, which is the wrong one on exactly the
networks where this matters: two networks, a VPN, an audio LAN with no gateway.

### Your whole library plays through HQPlayer, whatever it is encoded in

HQPlayer reads a short list of formats, and an Apple-encoded library is not on it. Hand it
an ALAC file and it answers with an error without so much as opening it — served over the
network or given by its path, it makes no difference. That mattered more than it sounds:
a library ripped with iTunes or Apple Music is almost entirely M4A, and the media server
on our own network answers with 185 M4A files out of 200. Choosing HQPlayer as your output
meant losing nearly all of your music, and the only advice we could give was to convert the
lot yourself, with something else, and keep two copies.

**You no longer have to.** Audiogravi<sup>ty</sup> converts each track to FLAC as it hands
it over. Losslessly — nothing is lost that was not already lost — and your files are never
touched: what is converted is the copy going out, and it is thrown away afterwards. A
CD-rate track takes about two seconds and comes out the same size as the original.

**And you can still move inside a track.** That is the part worth insisting on, because it
is what a simple relay would have cost you. The conversion is a complete file rather than
a stream, so it is served with its length and can be read from any point: ask for three
minutes in and HQPlayer goes there. A converted album behaves like any other.

This covers three paths at once. A file in your own library. **A track a media server
publishes** — until now the same album was accepted from the box and refused from the NAS,
which took some explaining. And **an internet radio station**: many of the best-sounding
ones broadcast in AAC only, with no equivalent anywhere else, and HQPlayer refused them
outright. Audiogravi<sup>ty</sup> now relays those as they arrive, for well under one per
cent of a processor core.

**DSD is never converted.** Turning it into PCM behind your back is not a decision a music
player should make on its own, so those formats stay refused, with the reason — as does an
address Audiogravi<sup>ty</sup> merely passes on without holding the audio itself.

One thing you may notice: an album whose tracks have to be converted starts on its first
track and fills in behind it. HQPlayer inspects every entry before accepting it, and that
inspection is what sets the conversion going, so a sixteen-track album queued in one go
would have been half a minute of silence before the first note. The conversions are kept
on disk in a space sized from what your box actually has free, emptied every time it
starts, and remade when needed.

### Fixes that concern every box

**Updates on a box set to another language.** On a box set to French or German, no update
was ever offered for the software installed from the system: Audiogravi<sup>ty</sup> read
the system's answers in English only. It now always asks in English.

**System files handed back to the system.** Files Audiogravi<sup>ty</sup> writes into the
system — the mount of a USB library or of a network share, a service setting — are
prepared under its own account and then handed to the administrator. For mounts, that
last step never worked, and nothing said so. Every step is now checked, and the update
hands the files already written back to the administrator.

**Restarting a service** from the Services tab no longer reports a failure when the
service simply takes more than a few seconds to stop.

**Restoring your own configuration** works on a box that does not have every optional
package installed: a service that is not installed is now a warning, not a reason to
refuse the file.

**A network share with an accent in its name** is recognised as mounted. And when
installing a package makes the system remove other software, you are now told what went.

---

## 0.9.58 — 2026-09-20

### Audiogravi<sup>ty</sup> knows which HQPlayer you have, and keeps the adapter in step with it

HQPlayer and the network audio adapter that carries its sound to your DAC have to be on
the same major line. A 6 adapter does not work with HQPlayer 5 — nothing plays, and
nothing says why.

Audiogravi<sup>ty</sup> now asks the instance who it is when you connect it. The card
shows the engine version beside the name, a network scan says which address holds a
Desktop and which an Embedded, and the version of your adapter is read from the box. If
the two lines do not match, the card tells you so and names both, and *Use as output* is
refused instead of sending your music into silence. If either version cannot be read,
nothing is claimed and nothing is blocked.

From that, the adapter offered to you follows the HQPlayer in front of it rather than
whatever is already installed. So a box that ended up on the wrong line is offered the
right one — which means an **older** version than the one it holds, deliberately. The
Audio Software page says exactly that: an older version is offered, and it asks to
switch rather than to update.

None of it is polled. The version is read once when the instance answers and forgotten
when it goes away, so upgrading HQPlayer on your other machine is picked up on its own.

### The NAA update stops offering a version your HQPlayer cannot use

Signalyst publishes two lines of its Network Audio Adapter side by side in the same folder —
the one that pairs with HQPlayer 5 and the one that pairs with HQPlayer 6 — and
Audiogravi<sup>ty</sup> offered whichever file came last on the page. On a machine running the
5 line that meant proposing a 6, which does not work with HQPlayer 5.

The update now compares versions instead of reading the listing in order, and it stays on the
line your machine already runs. A machine that is current is told so. One that was a release
behind is finally offered the update it had been denied — the real one was buried under a
version it could not use. A machine with nothing installed still gets the newest published.

### One less switch in the settings

Audiogravi<sup>ty</sup> shipped with a **Compact Mode** switch that was already on the first
time you opened the interface. Turning it off made everything larger — a second layout that
existed only to be left behind, and that every screen had to carry. It is gone, and what you
have been looking at all along is now simply what the interface is.

Nothing moves on screen, with two exceptions:

- **The settings drawer** gives each switch a line of its own. Light/dark mode, notifications,
  animations, portrait lock and Face ID / Touch ID used to sit two to a row, each label
  squeezed into half the width beside its switch.
- **A service that starts, or a profile you activate**, no longer nudges its tile's contents
  by a pixel while its border thickens.

The sign-in screen is the one place that kept its own layout. It never loaded the setting, so
it had been drawing the larger one on its own, and simply following the interface would have
shrunk it while nothing around it changed. It now holds those steps itself and looks exactly
as it did.

### A calmer playback bar

**Repeat** and **shuffle** have left the bar above the footer. They sat on a second line under
the track title, in a strip whose job is to tell you what is playing and give you the transport
— play/pause, previous, next, volume. Both controls are in the **fullscreen player**, alongside
the rest of what you set while listening.

The bar keeps exactly the height it had, so nothing above it shifts; the space is simply given
back to what remains.

And because the fullscreen player now holds two controls that used to be one tap away, the
manual finally says how to open it: the small tab at the top-right corner of the bar on a
computer, a swipe up from the track title on a phone, or nothing at all — it opens by itself
when you start something playing from the Library. It used to say "tap the bar", which never
worked; tapping the cover art opens the album's details and its tracklist.

---

## 0.9.57 — 2026-09-19

### Your own library plays through HQPlayer — on every box

With HQPlayer as your output, playing an album from your own library could not work
anywhere but in our lab. To play a file, HQPlayer is handed an address on your network to
fetch it from, and that address had been written into the code as the one of our development
machine. Every box gave it out. In the lab the development machine was always running, with
the same music on it, so HQPlayer fetched the files from there and everything seemed fine;
on your network that machine does not exist, and nothing played.

The address is now your box's own, the one on the route toward HQPlayer — the right one even
on a box with two network connections. Your files are fetched from the same signed address
network speakers use, closing on the way a route that let any device on your network download
any file of your library without a signature.

Three things that followed from it:

- **MP3 files play.** HQPlayer refuses an MP3 it is given with its size, and one sent without
  it never started when the file opened with its cover. They now go to HQPlayer the way a radio
  does, from their first note.
- **The progress bar works on every MP3.** HQPlayer cannot measure the length of an MP3 without
  a particular header, so the bar had no scale and could not be dragged. The length your library
  knows is shown instead — HQPlayer's own measurement still wins when it has one. For such files
  it can run a couple of seconds long, so the bar may stop just short of the end.
- **The cover is your library's.** The picture inside the file, as the library shows it, with the
  search on the internet behind it when a file has none.

### HQPlayer now says what it actually kept

HQPlayer accepts whatever it is given and may then drop it without a word — a file it cannot
open, an address it cannot reach. Audiogravi<sup>ty</sup> used to take that silence for a yes.
It now reads HQPlayer's playlist back as it sends. An album plays with the tracks that were
kept, and the titles and covers follow the tracks HQPlayer really holds. A play HQPlayer keeps
nothing of — or an addition to the queue that loses a track — is refused at once, naming the
tracks, instead of blaming your sound card 45 seconds later.

Starting an album while a radio plays through HQPlayer also works reliably now. Stopping the
radio takes HQPlayer about four seconds to acknowledge — more than Audiogravi<sup>ty</sup> used
to wait — and that late reply could stop the album from starting, silently. Every reply is now
matched to the command it answers.

### The Systemd tab shows the real-time settings your audio services run with

The **Systemd** tab said "default" for the scheduling policy and the nice level of every audio
service — including services running in real time. systemd reports the policy as a number,
Audiogravi<sup>ty</sup> only understood names, and the nice level was asked for under a name
systemd does not have. The tab now shows what systemd actually applies: `rr` for the audio
engines tuned for real time, −10 for an HQPlayer NAA set that way.

It mattered beyond the display. The editor starts from what the tab shows, so saving any
setting wrote the service's file back without its policy — a service put in real time with
*Audio Optimized* would have lost it at its next edit. It keeps it now. A service you never
tuned still reads "default", and saving leaves systemd's defaults alone rather than freezing
them into your settings.

### A softer default theme, and charts that show what was measured

The default theme, *Minimal*, keeps its black and white but loses its hard edges: every
corner now has the same slight 2 px radius, from the cards and buttons to the badges and the
notifications. Status dots no longer glow — green or orange, they are flat discs that still
blink. In the mini player, the badge naming where the music comes from (Qobuz, Tidal…) now
matches the output badge beside it exactly.

The small charts of the **Services** and **System** tabs were redrawn, and made honest:

- **They start empty and fill from the right.** A Services box used to open on a flat line
  at zero followed by a cliff — thirty invented zeros that took five to fifteen minutes to
  scroll out. It now shows the few measurements it has, on the right, and grows.
- **A gap is a gap.** A missing reading, or a pause while the app was in the background,
  leaves a break in the line instead of a dive to zero or two moments glued together.
- **Services** boxes draw a thin line over a light area, with a dot on the latest value.
  **System** tiles draw one bar per measurement, with the highest value of the window and
  the time it covers written above it.
- **They move.** The Services charts were only redrawn when something else refreshed the
  page; they now follow every measurement.

---

## 0.9.56 — 2026-09-17

### Offline, the app now shows what it promised it was showing

Take the box off the network — or walk out of range of it — and the interface raises a
banner across the top: **OFFLINE MODE — VIEWING CACHED DATA**. Underneath it, the panel you
were reading said *"Unable to connect to server. Please check your connection."*

Both were true, and that is what made it bad. The strip of figures along the top really was
restored from the last thing the box said. Nothing else was. Every panel fetches its own
data, and none of them had ever been handed back what it last saw — they simply asked the
box again, got no answer, and reported it, directly beneath a banner announcing the
opposite.

Six panels now keep their last reading and show it when the box cannot be reached: your
profiles, your services, the system dashboard, the audio software list, the accounts, and
the description of the processor. The banner means what it says on those screens.

It is deliberately not everywhere. A reading is only served when **nothing answered at
all** — a box that replies and refuses still says so, rather than showing you state from
hours ago as though it were current. And three screens keep the error on purpose: the
configuration editor, the systemd override editor, and the log viewer. The first two have
a Save button, and offering a stale copy there is offering to overwrite the live file with
it. Frozen logs shown as live mislead on precisely the subject you opened them for.

On a phone the banner also stopped covering the page. It is fixed below the top bar, so the
content underneath has to leave room for it — and the rule that did so had been shut inside
a block that only applies to wide screens. On the screen where the banner is seen most, the
first section title was cut in half.

### An installed app that starts offline, after an update

The app keeps its own copy of everything it needs, and rebuilds that copy at every release.
Two files it cannot start without were missing from it: the one carrying the address and
key of your box, and the one holding the connection for live updates.

So the first launch after an update, made away from the network, opened an interface with
no credentials — unable to ask the box for anything, and staying that way until it was
reloaded with the network back. The live updates were gone too, without a word, because
that particular failure is not one the app can notice. Both are kept now, and the app opens
with your data.

### Less work for nothing, on a machine that has music to play

Three things the interface did on every page load, for no benefit:

It re-fetched parts of itself. The rule deciding which files never change spelled out the
shape of the fingerprint in their names, and the tool that produces them sometimes puts a
dash in it — so whichever files happened to draw one that day were treated as changeable,
re-requested and rewritten on each load. Which ones were affected was redrawn at every
build, so the cost kept moving instead of being noticed. The pictures, icons and launch
screens had their own version of this: re-checked against the box on every request, cache
hit included, for files that cannot change until the next release replaces them all.

It wrote the box's state to storage on every measurement that arrived — several times a
minute, blocking the interface each time, when only the last value is ever read back.

And it loaded nine of its heaviest screens in the background so they would be available
offline. They already were.

---

## 0.9.55 — 2026-09-16

### The Library stops offering you what you are already listening to

Play a station, stand on the Radio screen, and a banner appeared across the top:
*"Radio Choco HD is now playing"*, with a button offering to switch you to the radio. You
were on the radio. The same banner turned up for a Qobuz album, and its Dismiss button was
decoration — the box republishes what is playing about every three seconds, and the banner
came straight back each time, so there was no way to make it stop.

Underneath it, the two halves of that screen were not answering the same question. A
station, a Qobuz album and a stream from a media server all travel over the same engine, so
the field naming the engine says *the local library* for all three; only a second field
names where the music actually comes from. The Library was reading the engine on one side
and the real source on the other, and then telling you they disagreed. They always did.

Both sides now read the real source. The radio has a quirk of its own on top of that — its
screen is reached from the tab bar without changing the source you are browsing — so the
banner also takes account of what the screen is showing, and starting a station now makes
the radio the source you are browsing, exactly as picking it from the sources screen does.
That last step waits until the station has actually started, so a station that fails to play
no longer rearranges the tab bar underneath the error message.

Dismiss now holds. The refusal lasts as long as that source is the one playing and lifts by
itself once something else starts, so you are still told about the next thing — and glancing
at the Radio screen is no longer read as changing your mind.

Two smaller things came out of the same work. Signing in to a streaming account refreshes
the list of sources, and that refresh had started adopting whatever was playing: it could
drop you onto the radio screen, or swap the media server you were browsing for the local
library. It refreshes the list now, and leaves you where you were. And the banner no longer
names things that are not sources: with HQPlayer driven from its own remote, it offered
*"HQPlayer is now playing"* and its Switch button sent the Library off to browse a routing
handle, which holds no music to show you.

---

### The manual shows the interface you are running

The pictures in the manual were taken between eight and ten weeks ago, and the interface
moved underneath them. They offered you MPD 0.23 where your box installs 0.24, an engine
that is no longer listed and neither of the two that now are, three outputs where a plain
box has six, a user card missing the passkeys button that sits beside it today, and an
update banner announcing a version from last spring.

Every one of them has been retaken against a running box, at the size of a phone screen
and at three times its resolution, so they stay sharp on the device most people read them
on. Where a caption had come to describe something the screen no longer says — the button
is **Restart Core**, not "Restart Backend" — it was corrected along with the picture above it.

Seven parts of the manual described something and showed nothing. The stream-origin badge
that arrived in 0.9.54 was one of them: explained in a paragraph, never pictured. It is now
shown carrying the name of a station beside the engine playing it, which is the whole point
of it — the engine alone tells you nothing, since everything you play travels over the same
one. The bar at the bottom of every screen, the list of sources the Library chapter is built
around, the radio collection, the signal chain as a phone draws it, and the tiles of the
configuration editor have joined it.

The licence panel is shown twice, on trial and once activated, because it holds different
things in each. The device identifier and the order number are blurred in both: an order
number is the licence key itself.

### When the app says your box is offline and your box is fine

A phone that was asleep, or an app that was closed while the box updated itself, can keep
serving the copy of the interface it already had. That copy asks the box for things the
newer version moved, gets nothing back, and reports the only thing it can honestly see —
no answer — as **CORE · OFFLINE**.

So the screen tells you to go and look at your box, and your box is working: the same
address opens normally in any other browser. The troubleshooting chapter now says this in
as many words and gives the way out, including inside the installed app, which has no
reload button to press.

### Sending music to a network speaker hands the room over

Casting an album to a UPnP speaker used to leave the box playing whatever it already
had on its own DAC. Two different pieces of music, two outputs, at the same time — and
the screen followed the wrong one: it showed the station you had been listening to,
with its cover and its format, while the speaker played the album you had just chosen.
The signal path read *Radio → your speaker*, which describes nothing that exists.

Nothing was wrong with what the box knew. It had the speaker's track, artist and album
the whole time. The local player simply never stopped, and Audiogravi<sup>ty</sup> shows
you the source that is actually playing — so it went on showing that one, correctly,
from a situation that should never have arisen. HQPlayer hid it by accident: its network
adaptor holds the sound card for itself, so the local player is stopped by being refused
it. A speaker on the network takes nothing away from your DAC.

Casting now hands the room over: what was playing stops as the speaker starts. It stops
at the last moment, so a speaker that has left the network, or a streaming link that
expires while it is being fetched, leaves your music playing instead of stopping it for
nothing — and once per album, not once per track.

### A stray line in the interface installer

Installing the interface printed `install.sh: line 347: -: command not found` in the middle
of its success report, on every install. Nothing was broken by it — the service it writes
was always correct — but it is the kind of line that makes you stop and wonder what you have
just done to your box. It is gone, along with the truncated comment it left behind in one of
the files on your machine.

---

## 0.9.54 — 2026-09-12

### You can see where the music is coming from

Everything you play travels over the same engine — a Qobuz album, a Tidal track, a station,
a file on the box, a record served by a machine down the hall. So the card at the top of the
**Audio Pipeline** tab could only ever tell you about the engine. It said **MPD**, and it
said it for all of them.

It now tells you the source as well, beside the engine rather than instead of it: the tab is
about the path your music takes, and the engine is part of that path. When naming both would
just say one thing twice — AirPlay carried by AirPlay — only one is shown.

The same information reaches the player at the bottom of the screen and the full-screen
player, where it was already shown but only in the general: a record served by your media
server reads **MinimServer** instead of "UPnP", a station you are listening to reads its own
name instead of "Radio", and music playing on HQPlayer from HQPlayer's own remote reads
**HQPlayer** instead of "External" — which told you it was not us without telling you what
it was.

None of this asks your box for anything new. All of it was in the answer it was already
giving, and no screen had ever read it.

### The Admin tab stops counting who is connected

A small figure sat beside **Admin** in the list of tabs — people connected, over accounts on
the box. On a phone the tabs always run down the side of the screen, which is where that
figure shows, so it was in the way of the one place it had no reason to be.

A box at home is not a server with users to watch. The count is gone, and with it a question
the interface asked the box every time it loaded.

Who is online is still there where it says something: open **Admin** and each account carries
a green mark for as long as that person has the interface open.

### Reordering your library is instant

The three buttons above your local collection — **All**, **Recent**, **A–Z** — are answered
by the box across the whole collection, not by the screen across the page it happens to
hold. That is what makes *Recent* mean recent. The cost was that each of them started the
collection over: the box listed every album again, then went back once per album for the
file its cover is read from. On a 475-album library that is a fifth of a second of work,
every time, for a list the box already had in front of it.

It keeps that list now and simply turns it around, which takes about a thousandth of the
time. Only the **↻ Refresh** button asks it to go and read the collection again — which is
what that button is for.

And the list is no longer kept "for a minute, then thrown away just in case". The box asks
its own music index whether anything has changed — a question that costs 0.17 ms, against
the fifth of a second the reading costs — and keeps its list for as long as the answer is
no. So music you add appears **straight away**, whether you added it yourself or AG
re-indexed after you pointed it at a new folder; and a collection that has not changed in a
fortnight is not re-read every minute for nothing.

### The support report tells you where to reach the interface

Everything needed to open your box was already in the report — the port the interface is
served on, the address of the box on your network, the name it announces — in three
different places, and never as something you could read off and type. The name on its own
lands on port 80, where nothing listens, so a box answering perfectly looks unreachable.

It now writes the address out whole, and puts the one that always works first:
`http://10.0.4.254:8080 · also http://musics.local:8080`. The `.local` name is the one
worth keeping — it still finds your box after your router hands it a different address —
and it comes second because it is also the half that can fail on its own.

---

## 0.9.53 — 2026-09-07

### The radio is a source, and the screen finally says what is playing

The sources screen used to name the engine rather than the music. Play a webradio and it
announced **Local Library** as the active source — because a station, a Qobuz album and a
file on your disk all travel through the same engine, and the badge was reading that
engine. The radio was worse off still: it had no card at all, only a tab, so there was
nothing for the badge to land on even if it had been right.

Sources are now named by what they are, and the radio is one of them, on the same footing
as Qobuz, Tidal, HIGHRESAUDIO, your local library and a UPnP server. Its stations keep
their own screen with their own filters — country, genre, codec — so the shared search bar
does not offer it, and its tab bar drops the two tabs that would answer an empty grid and
an error. Its queue is the shared queue it actually plays through, not an empty one.

**AirPlay and the UPnP bridge are listed too.** They do put out sound, so they are sources.
But an input hides the source behind it: what a phone sends over AirPlay has an identity
the box cannot see, so there is no catalogue on this side of the door. They appear in their
own section, they light up while they play, and touching one raises the player.

**Several things can play at once, and now they all show it.** Casting AirPlay to one
output while Qobuz plays on another lit a single card — whichever had started first. And a
card no longer waits for a page reload: a second stream pausing, changing album or moving
to the next track reaches the screen straight away.

### The Tidal subscription notice from 0.9.52, made to actually work

0.9.52 added a line under each streaming account saying what it will really play. It
worked for Qobuz and HIGHRESAUDIO. It did not work for Tidal, and the reason is worth
saying plainly: reading the plan needs a valid access key, that key lasts a week, and
nothing renews it unless you play something from Tidal. On a box used for anything else,
the question could not be asked — and an unanswered question is read as "subscribed", so
the card went on announcing Hi-Res on an account that had none.

It renews the key now, like every other part of the box that talks to Tidal.

### The box says which shelf, and which server

The music on your disk answered to **MPD** — the name of the engine that plays the files,
not of the shelf they sit on. The interface patched the word on its way to the screen,
from a table of its own, so the box and the screen disagreed about the same thing. It is
called **Local Library** now, from the box, and the screen shows what it is given: the
same words on the source card, on the now-playing badge and above the queue.

A UPnP server used to be known by its **name** alone. Two servers named alike lit both
cards, with nothing to say which one was playing. Each now travels with its own identity,
from the moment a track is queued — including tracks cast to a network renderer or pushed
to HQPlayer, where a local file used to be filed under the name of the processor playing
it.

**What renderers fetch audio from is a door without a key** — it has to be, since a
renderer sends no headers. When a track could not be resolved, that door used to hand back
the streaming service's own error, verbatim, to anything on the network. It now says only
that the track is unavailable, and writes the reason in the box's journal, where it was
missing.

---

## 0.9.52 — 2026-09-06

### When HIGHRESAUDIO is slow, the box stops taking the blame

Their catalogue sometimes takes its time — a filtered search computed cold can run for tens of
seconds, then answer the same one instantly. Audiogravi<sup>ty</sup> knew how to say that, and
said it well. On one screen. Everywhere else the same wait produced a flat *"HIGHRESAUDIO
unavailable"*, which reads as a fault on the box.

That was never a decision. The sentence had been copied by hand onto forty routes and finished
on one. It is now written once and shared, so every shelf says the same honest thing.

### When a subscription ends, the box says so

Until now it did not. A Tidal or Qobuz subscription that lapses does not lock you out —
both services keep you signed in, keep the catalogue browsable, and keep handing out
music. Thirty seconds of it, per track. The screen meanwhile still read *Hi-Res* and
*Studio · Hi-Res 24/192*, because that is the quality Audiogravi<sup>ty</sup> **asks**
for, and no part of the playback path can tell a thirty-second excerpt from a short
song. So the music stopped early and nothing, anywhere, explained why.

Each streaming card now says what will actually be heard. And it keeps saying it: the
state is read again from the service rather than remembered from the day you signed in,
which is the difference between being right once and being right the day it matters.

### A Qobuz account without a subscription can finally connect

It could not before — and it was told the wrong reason. Qobuz was asked to sign the
account in, did so, and Audiogravi<sup>ty</sup> refused the result because the account
had no streaming rights. What the browser showed was *"Failed to exchange the
authorization code. Please try again."*: a good code blamed, a retry invited that could
never work, and the real cause left in the journal. The account was shut out of Qobuz
altogether — **including the albums it had paid for**.

It now connects like any other. The catalogue browses, the purchases are there, and what
Qobuz gives is played — with the card saying plainly why the tracks are short.

---

## 0.9.51 — 2026-09-01

### Tidal opens the same way — and two of its shelves were simply not working

Two of Tidal's five buttons were empty. *Charts* showed nothing at all, and *Editorial*
showed the charts mixed in with its own selections. Same cause for both: the box was
recognising those lists by the words Tidal writes above them on its home page, and Tidal
renamed one. Nothing recognises a heading any more.

Tidal now has the same five shelves as the other two services: your favourites, the
**shelves** of the catalogue, the **playlists** — the editors' selections, your own and
the charts, all three on one strip — the **genres**, twenty of them and out of reach
until now, and the **moods**, a shelf HIGHRESAUDIO has and Qobuz has nothing for.

A shelf that holds nothing is left out, and we check rather than believe: one Tidal shelf
announces that it has albums and answers an error, another announces the same and holds
281 playlists. Taking Tidal at its word would have given you one dead button and hidden a
real shelf.

Two things you will not find, because Tidal does not have them: purchases, since it sells
nothing, and sub-genres — its genres are one level deep.

A sixth shelf, **Explore**, opens Tidal's own navigation, and it is where the depth is:
**HiRes**, seven **decades** from the fifties to the two-thousand-tens, **52 record
labels**, and genre pages far richer than a single grid — jazz alone opens on a dozen
lists. Some of those pages lead to others rather than holding albums, so the strip goes
down into them and offers a way back, exactly as the genres do.

### Qobuz opens the way HIGHRESAUDIO does, and most of its catalogue is reachable at last

Qobuz had four buttons above the album grid, and two of them were a single shelf each out
of the many the catalogue holds — the rest simply had no way in. It now has the same five
shelves HIGHRESAUDIO got in the previous release, each opening a strip below it: your
favourites, **your purchases**, the **shelves** of the catalogue, the **playlists**, and
the **genres**.

Nine shelves are on that strip — new releases, all new releases, the Qobuz selection,
Qobuzissims, press awards, best sellers, most streamed, the ideal discography and Harmonia
Mundi. Qobuz names fifteen; six were left out after checking each one, because they are
empty, or the same shelf twice under two names, or — for four of them — one undifferentiated
list whose contents match none of the four names it is published under. A button that cannot
be labelled honestly is worse than no button.

**Your purchases** are new, and **your own playlists** appear beside the ones Qobuz
publishes: they were never listed, although everything needed to play them already worked.
And the **genres** — thirteen of them, seventy-eight sub-genres — were entirely out of
reach until now.

One thing to know about the genres: on Qobuz a genre is not a shelf of its own, it only
narrows one. Choosing *Jazz* therefore shows the Qobuz selection within jazz. That is not a
shortcut on our side — it is the only shelf where sub-genres return anything at all, which
we measured before choosing it. Two genres publish one sub-genre or none: that is their
catalogue, not a fault.

Search stays a single box, deliberately. There is no advanced search for Qobuz the way there
is for HIGHRESAUDIO, because their current interface has nothing to build one on: every
filter it accepts on a search is accepted and then ignored, which we checked rather than
assumed. It did get faster — the same search used to be sent three times over, and is now
sent once.

### Your box answers to its name, so its address can change without taking the app with it

Until now the way to reach your box was its address on the network — and that address
belongs to your router, which is free to hand out a different one. The day it does, every
bookmark stops working, and so does the icon on your phone's home screen: an app added to
the home screen remembers the address it was added from, for ever, and a full-screen app
has no address bar and no error page. It simply opens on nothing.

Every box has always had a second address — its own name, `<box>.local` — and its
certificate has always promised it. What was missing was the small service that answers to
that name. It came along by accident if you had installed AirPlay, and not at all
otherwise. It is now installed with the rest, and two things were corrected on the way: the
name is built the way that service actually publishes it, and a box whose certificate names
something else now reissues it — the authority your phones were told to trust is left
alone, so nothing has to be set up again.

Point your browser and your home-screen icon at `https://<your box>.local` rather than at
its address, and a change of address stops mattering.

### The report you send us now carries the facts we ask you for

When something goes wrong with the certificate — a phone that will not open the interface
any more — the questions are always the same, and the report did not answer them: when the
certificate was issued, when the box's own authority was created, whether its address is
leased or fixed, and what name it announces. Five such facts were added, and the report now
also points out when the name a box announces is not the one its certificate carries.

Two lines were also saying something they did not mean, and both cost time. One of them
read like a refusal from our licence server when it only meant "this box is on a trial and
holds no licence file".

---

## 0.9.50 — 2026-08-31

### HIGHRESAUDIO, arranged the way HIGHRESAUDIO asked

Browsing HIGHRESAUDIO meant reading a single row of eighteen buttons, in whatever order
their catalogue happened to publish them, with most of the shop categories off the edge of
the screen. Their own team said so, and then described the menu they wanted.

That menu is now there: seven shelves — Favorites, Vault, Categories, Charts, Playlists,
Labels, Genres — each opening its own row underneath. Three of them are new. **Charts** is
the ranking their front page shows. **Labels** is the seven imprints they name, 2L and
audite among them. And **Playlists** now offers *Genre* and *Theme* beside the editorial
selections and your own, which is how they file those selections themselves.

Nothing was hidden along the way. Their catalogue publishes fourteen categories and all
fourteen are there — the six they listed first, in their order, the rest behind. Three of
them appear nowhere in their plan, and each one turned out to hold real albums, so taking
them out would have made part of the shop unreachable. One shelf they asked for is
missing: two of its four entries duplicate categories you already have, and the other two
point at data their API does not serve. That question is with them.

The genres and themes of their playlists are now listed alphabetically, as their catalogue
genres already were at their request. The order they arrive in follows no rule that can be
read — not the identifier, not the alphabet, not the size of each group — and a row nobody
can predict is harder to use than one that reads left to right.

### Searching HIGHRESAUDIO, with the form they built

Typing *Queen* into the search box returned a list with little to do with Queen, and
filling in a filter while the box was empty did nothing at all — no result, and no message
saying why. Both of those were ours, not theirs.

Their advanced search needs no words at all: asking for the label *ECM* on its own answers
with twenty albums. The box refused to ask below three characters, a rule that belongs to
their *quick* search and had been carried onto this one by mistake — and the screen only
ran a search when the box held something, so filling in a filter beside an empty box was
answered by silence.

There is now an **Advanced search** panel, folded away until you want it, holding the eight
criteria their own application offers: the words you type, plus artist, composer, label,
year, format, mood, and the order results come back in. It is applied by its **Search**
button rather than as you type — a filtered search can take HIGHRESAUDIO the better part of
a minute the first time it is asked, and seconds thereafter, so asking once is the point.

Two things are worth knowing, because they are theirs and we chose not to paper over them.
**Year** is the year an album was put online, not the year it was recorded: *Innuendo* is a
1991 record and answers to 2026 — their application calls that field Year, and so does
this one. And choosing a **format** makes their catalogue ignore the words you typed: ask
for *queen* in FLAC 192 and you get the same fifty albums as any other word. Their own
application behaves that way; a search here that quietly behaved differently would be the
larger surprise. They have been told.

### A star and a plus sign, side by side again

In the search results, an album from a streaming service carries two controls at the end of
its line: the star that adds it to your favourites, and the `+` that puts it in the queue.
There was room for one. The `+` fell to a second line and came back at the far left, under
the sleeve, with the star left alone on the right.

It had been like that since mid-July, on Qobuz, Tidal and HIGHRESAUDIO alike — the search
results are the only place in the application where a line carries both. They now sit
together, where they belong.

### Playlist covers are no longer cut in half

HIGHRESAUDIO's playlists carry a banner, twice as wide as it is tall — measured on
thirty-two of them, from the oldest in their catalogue to the newest, and every one the
same shape. They were being shown in a square frame, which kept the middle and discarded
the rest: on artwork composed across its width, what disappeared was the title and the
label's mark.

The frame now takes the shape of the picture. In the grid the card is simply shorter; in
the lists below it the rows keep the height they have always had and the thumbnail widens
instead, so a list holding both shapes never changes rhythm from one line to the next.

### The services you browse are shown, not spelled

Above the album grid, the line that tells you which source you are browsing named it in
capitals: QOBUZ, TIDAL, ROON. HIGHRESAUDIO was already an exception — it appeared as its
own logo, because that logo is simply its name drawn. The other three now do the same,
each with the artwork its owner publishes, in a version for the light theme and one for
the dark. They are set at a size that matches the weight of the words around them rather
than the size of the file, which is why a very wide mark like Tidal's does not tower over
the rest.

The small green dot that used to pulse in front of that line has gone. It could only ever
be green: it announced that the source was live at the exact moment when that cannot be
in doubt — you have just picked it, and its covers are already on screen. A light that
never changes is one you stop believing, and this one would have been in the way the day
something genuinely needed reporting. It was also animating continuously on a machine
whose spare capacity belongs to the music.

---

## 0.9.49 — 2026-08-29

### The API reference is no longer served to the whole network

Audiogravi<sup>ty</sup>'s core carries an interactive reference of its API — the page
developers use to explore what a box can do. It was reachable by anyone who could reach
the box: no password, no key, nothing. What it hands over is not an access — every
operation still checks who is asking — but it is the complete map of the machine, down to
the routes that handle sign-in, licences and updates. Read on a running box: 188 routes.

It is now off unless you ask for it, on new installations and on existing ones alike, and
"off" means the address answers *not found* rather than *not allowed*. The interface
follows on its own: where the box does not serve the reference, the buttons that opened it
are simply not there. If you want it — on a box you administer, on a network you trust —
a single setting in the core's configuration brings it back, and the interface offers it
again the next time it asks. One thing to know if you do: that page fetches its own code
from the internet, so it stays blank on a box that has none.

### The name, set in type

The interface showed its own name as a picture. That picture asked for a typeface —
Helvetica — that the machines Audiogravi<sup>ty</sup> runs on do not have, and it had never
been converted into a drawing, so every box rendered the name in whatever its system
offered instead. It looked right on the machine where the file was made, and only there.
Dark mode had to repaint it with a filter, the way one inverts a photograph, because a
picture cannot simply take a colour.

The name is now written, in the typeface the interface already carries, exactly as the
landing page writes it — the same weight, the same tight fit, the same small *ty*. It
appears that way on the screen shown while the app starts, on the title bar, in the
sidebar, on the sign-in card and in the credit line at the bottom of both screens. Sizes
were matched to what the old picture occupied, so nothing on any screen has moved.

Retiring the picture turned up a small pile of files the interface believed it had.
Several icons were listed under names nothing in the project has ever carried, so they
were never really kept for offline use; notifications asked for an icon that does not
exist and were drawn with the browser's own instead; and the picture itself was offered
to phones as the application icon — a name five times wider than tall, where an icon is
square. All of them are now checked automatically against what the box actually ships.

### Light or dark, before you sign in

The choice between the light and the dark palette was inside the configuration panel,
which is behind the sign-in form. Someone starting the box at night therefore got the
light one full in the face, and had to sign in before they could do anything about it.

A small button now sits in the corner of the sign-in card: a moon when the page is light,
a sun when it is dark — always showing where pressing it takes you. It changes the
appearance only; which theme you use is still yours to pick in the panel, and the button
merely flips that theme's palette. The choice is remembered, and applied before the page
is drawn the next time, so a box you left in dark opens dark, with no white flash. On a
phone where the interface is installed to the home screen, the status bar follows in the
same instant.

The badge above the form also stopped calling the box "API". It says **CORE**, which is
what it is checking.

### A blank sleeve, with the picture already in hand

An album bought from HIGHRESAUDIO played with no cover in the player — while the same
artwork sat, perfectly visible, on the *Up next* row just below it. One record, one
image, two answers.

The two rows do not ask the same way. The queue asks with the picture's address alone;
the player asks with the address *and* the artist and album, as a fallback for when
there is no picture. That fallback turned out to be the problem. Covers are remembered
twice — once for the track, once for the album, so one download serves a whole record —
and the album entry was consulted before the address the service had provided. Once it
was marked "nothing found", it answered on behalf of the album and the picture was
never fetched at all.

"Nothing found" only ever meant that the public cover catalogues had never heard of the
album — which is simply true of a promotional sampler, and of plenty of fine obscure
records on any source. It was never a reason to ignore artwork the service itself
handed over. The album memory now answers only when it actually holds a cover, and the
first track that finds its own repairs the album for all the others.

---

## 0.9.48 — 2026-08-29

### The albums you bought from HIGHRESAUDIO, next to the ones you stream

HIGHRESAUDIO sells albums as well as streaming them, and an album you bought is yours to
play whether or not you keep a subscription. Audiogravi<sup>ty</sup> now shows them: a
**Vault** button on the HIGHRESAUDIO source, beside Favorites, lists every purchase on the
account and plays it like any other album — on the box, on a network renderer, through
HQPlayer.

Under the surface the purchases are a different place from the catalogue, with their own
addresses, and the two do not answer for each other. So each purchase carries a small mark
in its address that says which place it lives in, and playback follows the mark rather than
guessing from the shape of the address. It is the same mechanism playlists already use, and
it is what keeps a purchase playable on an account the catalogue would refuse.

### Seventeen hundred playlists, and now a way through them

HIGHRESAUDIO publishes 1762 editorial playlists. They reached the interface as a single
list in no particular order, which is another way of saying they were unreachable. They
sort them into four shelves — *New Releases*, *Recommended*, *Popular*, *Moods* — and a
strip now picks one, with the sorting done on their side rather than by pulling the whole
catalogue over to sift it here.

It opens on **All**, deliberately. Going through the whole tree turned up fourteen
playlists filed under no shelf — *Mr. Slowhand — Eric Clapton*, *In the Spirit of Jazz*,
*The Sky is Crying* — old ones, from before the shelves existed, and among the best in the
set. Offering only the four would have buried them for good, so the shelves narrow the
list instead of carving it up.

### HIGHRESAUDIO looked at the integration, and three things moved

Their first feedback arrived within a day. Four of their shop shelves reach the interface
with German names, and the English put on them here was invented — two of the four
wrongly. They now read as HIGHRESAUDIO writes them: *Listening Tips*, *Top Albums*, *New
Release*, *Recently Added*. Their genres and sub-genres arrived in the order their system
happens to hold them, which is no order at all; both levels are now alphabetical, and so
are the artists a search brings back. And a playlist finally looks like one: on every
streaming source, a playlist card and a playlist row say the word, where before only the
heading above the shelf did — *"It is very important that you differentiate between
albums and playlists"*, they wrote, and they were right.

### An account with purchases and no subscription can sign in

It was believed that HIGHRESAUDIO turned such an account away at the door, and the
integration was written on that belief. Tried on one, it does not: HIGHRESAUDIO answers the
sign-in with a refusal *and hands over a working session in the same breath* — one that
lists the purchases and streams them all the way to the file. It was
Audiogravi<sup>ty</sup> that read the refusal and threw the session away.

It no longer does. Such an account signs in, the sources card says next to its name that it
can play its purchases only, and the library offers it the Vault and nothing else — the
favourites, the playlists, every shelf of the shop and the search would all refuse it, and a
row of buttons that fail is worse than one button that works. Switch accounts on the sources
card and the library follows at once, shelves and stars included — never the account that
was signed in a moment ago. Whether HIGHRESAUDIO meant to label a
working session as a failure is a question for them; the music plays either way.

### A box that was off told you the password was wrong

It happened on iPhones and iPads, and nowhere else. Someone opened
Audiogravi<sup>ty</sup>, typed the password they have typed a hundred times, and read
*Invalid username or password*. So they typed it again, more carefully. Then again. The
box, meanwhile, had simply stopped — and two centimetres above that message, the screen
was already saying **API · OFFLINE**.

The cause is worth telling, because it is a small thing that produced a large lie. When a
request cannot reach a machine at all, the browser reports it in its own words, and those
words are different in every browser: Chrome says *Failed to fetch*, Firefox says
*NetworkError*, Safari says *Load failed*. The screen recognised a failure by reading that
sentence, and its list knew Chrome's and Firefox's. Safari's slipped through a rule meant
for something else and came out as a rejected password — so the one device most people use
to control their box was the one device that accused them.

It no longer reads sentences. The only part of the software that can know a request never
left is the part that sent it, so that is where the fact is now recorded, and every screen
asks rather than guesses. Nothing depends on which browser is in front.

### And when something is wrong, the screen says which thing

Once the sign-in screen stopped guessing, it turned out to be answering with status codes
for everything else too. Each of those has been replaced with a sentence, and each sentence
was checked against what the box actually sends rather than what it was assumed to send.

A box that cannot be reached now **names the address it tried** — the difference between
writing to us and walking over to look at the machine. A box that is running and has just
crashed says so instead, and points at the support report: that is a different event from a
machine that is off, and it needs a different action. Six wrong passwords in a minute — what
anyone does when they believe they are mistyping — answered *HTTP 429*, a number naming a
rule it never mentioned; it now says how long to wait. And a field the box refuses to accept
answered *[object Object]*.

One more thing on the same screen: the panel a phone with a passkey meets first offered a
retry button after a failure that had already been disconnected, so pressing it did nothing
at all until the page was reloaded. It works.

### The same honesty, on the other screens — and in the app on your phone

The sign-in screen was the first to stop guessing. It was not the only one guessing:
uploading a licence file, adding a passkey from Settings, and every request the
installed app makes on a phone all recognised a dead network in their own way, and
each way had a hole. The licence upload still printed Safari's raw *Load failed*; the
app on your home screen, which cannot let the browser report a failed request on
iOS, turned one into *Service temporarily unavailable* — a sentence that never once
mentioned the network, in front of a box that was simply off.

Every request now leaves through one door, and that door records what happened.
Whatever the screen, a box that cannot be reached is reported as a box that cannot be
reached; a box that refused says why, in its own words; and nothing is retried unless
nothing answered.

---

## 0.9.47 — 2026-08-25

### A trial that, once given, stays given

The length of the trial every box starts with is set on the licence server
and served to the fleet each day, so it can change without a release. What it
could not do was change safely in one direction: a box recomputes its days
remaining from whatever length it is served, so lowering the setting ended
trials that were already running, overnight and without a word.

The server now serves each box the longest length it has ever told it.
Raising the setting reaches every box, trials already running included — a
box at day forty of a thirty-day trial is back in trial with twenty days
left. Lowering it reaches only boxes the server has never seen. What was
given is not taken back. The administration console shows the length granted
to each installation and can forget one, which is how a figure typed by
mistake is undone. Nothing changes on the boxes themselves.

### The support report tells the truth, or says it does not know

The report a box produces for support was built to end the exchange of
screenshots. It could only do that if every line of it were true, and five of
its sections were not. It reported no streaming account signed in on every box
ever, whatever the truth — a broken probe whose error was written down as a
"no". It described the realtime tuning of software that is not installed,
because asking systemd about a unit that does not exist gets you an answer
anyway. It printed five outputs as *PCH*, *PCH*, *HDMI*, *HDMI*, *HDMI*, which
is where an AirPlay receiver quietly ends up on the wrong socket. It showed the
output Audiogravi<sup>ty</sup> believes it selected and never the one each
service is actually playing on — so the one fault most worth reporting was the
one it could not show. And it repeated a single failure twenty-one times, out
of order.

Each of those now answers correctly, and where an answer cannot be had, the
report says *unknown* and names the reason rather than inventing a negative
one. Repeated failures fold into one line with their count and their last
occurrence, in chronological order. The report is a tenth smaller for it.

The rule this came from is worth stating: a measurement that failed must never
be printed as a finding. It applies to the whole report, and the sections that
already followed it were the ones that never misled anyone.

### The licence server keeps its own backups

Everything the licence server knows — who bought what, the licence files it
can re-send, every revocation — lives in one file, and until now the only
copy of it was the one taken around an upgrade. A nightly job now copies it
consistently, checks that the copy opens, compresses it and keeps the newest
thirty. Existing servers get it at their next update, which also takes a
snapshot before it restarts into the new code.

### HIGHRESAUDIO's mark, as they drew it

The HIGHRESAUDIO artwork shipped since 0.9.44 was cut out by hand from a flat
image, and the cut had washed out the **RES** at the centre of the mark — the
one word the whole logo is built around sat at half contrast, close to
disappearing into its own white plate. HIGHRESAUDIO supplied their official
file on 25 August; the three images the interface uses are regenerated from it,
at the source's own proportions, and the wordmark reads as it was drawn.

The small badge beside Qobuz and Tidal is redrawn from the same source and
joins the treatment those two already use: at that size no lettering is legible
either way, so what a reader gets is a silhouette — and a silhouette that
follows the text colour stays visible on a selected card, whose background
inverts, where a fixed dark image would not. Checked in all four combinations
of theme and selection.

---

## 0.9.46 — 2026-08-24

### A box that can be diagnosed at a distance

The support report already answered "what is this box": version, licence, which
services run, what the configuration files say. What it could not answer was
everything around the box — and that is where the other half of every support
conversation went.

It now measures, when you ask for it. How the interface is really served, asked
of the running server rather than read from a file: plain HTTP or TLS, which
port, which version of the interface is actually deployed, whether the
certificate has expired, whether it still names the address the box answers on,
and whether the authority you asked phones to trust is the one signing it. The
network the music crosses: the gateway, the DNS, which interface actually
carries the traffic, the negotiated speed of a wired link — a gigabit port
running at a hundred is a thing that happens — the WiFi rate and signal, whether
the clock is synchronised at all, and whether the internet and the licence
server answer, with the time they took.

The audio path as it is at that instant, not as it was configured: which DAC the
system can see and at what USB speed, and the format and sample rate genuinely
crossing ALSA — the bit-perfect claim, measured. How the audio services are
scheduled, with what systemd was told to apply set beside what the running
process actually carries, because a tuning file that failed to apply is exactly
the difference between those two columns.

What else is on the network: UPnP renderers and servers, an HQPlayer, a Roon
Core — whether or not this box was configured to use them, since "not
configured" and "nowhere to be found" are different answers and only one of them
is a fault. Free space, and any filesystem the kernel has quietly remounted
read-only, which is the failure where a box keeps working and nothing it does
persists. Whether the deployed settings carry what the code expects, by name and
never by value. Whether an update could actually download, asked of the release
repository itself rather than inferred from anything else.

And the last seven days of failures — the services' own, and the kernel's, which
is where a DAC dropping off the bus, a dying memory card, an undervolted supply
or thermal throttling speak, and where nothing else in the report would ever
show them. The boot history comes with it, because five boots in two days is a
hardware conversation, not a software one.

Two rules hold throughout. Secrets are still removed before the report is built.
And a measurement that fails says it failed: a probe that could not run is never
printed as a negative finding — "we could not read this" and "there is nothing
here" are not the same sentence, and only one of them is honest.

The window itself now shows a turning indicator and names what it is probing
while it works, then says "Report ready." when it is done.

### The name on the network is yours

For someone who drives their streamer from JPLAY, BubbleUPnP or mconnect, the
name in that list is the whole product — they may never open the interface at
all. And that name was wrong twice over: a hostname nobody picked, wearing a
`-UPnP/AV` protocol suffix nobody asked for. The configuration form compounded
it — its one name field promised to be "the name displayed to UPnP clients"
and wasn't, so typing `Salon` produced `Salon-UPnP/AV`, and whoever came
hunting for the suffix found nothing to fix.

The form's **Friendly Name** now is what control points display. Exactly. A
fresh box calls itself `audiogravity-XXXX`, with a short token unique to that
box, because two boxes in one home must not announce the same name and UPnP has
no way of telling them apart. An existing box sheds its suffix the first time
its form is saved. And **Reset to default** warns that the name goes back to
the default — a reset is a reset, and it says so.

OpenHome, promised on the landing "once OpenHome is switched on", is now an
actual switch: an **OpenHome Renderer** checkbox in the same form. Ticked, a
second renderer appears for Linn Kazoo, named with an `-OH` tail so the two
never collide in an app that lists both — and toggling it never renames the
renderer your other apps already know. Both positions of the switch were
measured on the real network, not inferred.

Along the way, saving from the form stopped quietly stripping the *Managed by
Audiogravi<sup>ty</sup>* line — the one that keeps the CONFIGURED badge honest and tells
the support report whether a file was written by hand — and checkboxes learned
to read `0` as off and to write settings in the file's own language.

---

## 0.9.45 — 2026-08-23

### One button that says what your box actually looks like

Helping someone at a distance used to work by deduction. The version was inferred
from a timestamp on the licence server. A service was assumed to be off because it
looked that way in a screenshot. A configuration file edited by hand was guessed at
from a description of it. Each guess took a day to confirm, and some of them were
wrong — which meant looking for a fault in the audio chain where there wasn't one.

**System › Actions › Support Report** answers all of it at once. The version and the
architecture. The licence, and when the box last reached the licence server. Uptime,
load, temperature. Which audio packages are installed, at which versions. Every
service: running or not, and whether it comes back at the next boot. The outputs the
box can see, and the one each service is pointed at. Whether each configuration file
was written by Audiogravi<sup>ty</sup> or by hand. The declared music folder, whether it exists,
whether MPD can read it, and whether MPD ever finished indexing it.

And the configuration files themselves — the thing nobody could see, and the thing
that most often explains the rest. They are reduced to what is actually in effect:
comments dropped, which takes upmpdcli's file from three hundred and eighty-five lines
to thirteen and turns it into something a person can read. Whatever gets cut is
counted, so a shortened file never passes for a complete one.

Anything else on the box that has failed is listed too. A NAS mount that never came
up explains an empty library perfectly, and it never shows up anywhere in the audio
stack.

**Passwords, API keys, streaming tokens and share credentials are taken out before
the report is assembled.** A setting's name stays, so you can still see it is
configured; its value is replaced. Your music never appears — no titles, no albums,
no file names.

And nothing is sent anywhere. The report is displayed for you to read. **Copy** puts
it on your clipboard, **Download** saves it as a text file, and it reaches anyone
else only if you decide to attach it to a message.


### What the box tells the licence server, in writing

Once a day, and whenever a key is activated, your box contacts the licence server.
That is what keeps a Pro licence bound to one machine, and it is also how revocations,
announcements and update offers reach you.

Until now that exchange was described nowhere — not in the licence agreement, which
had seven clauses and not one about data, not on the site, not in the interface. It
is a short thing to say, and it was missing.

It now appears in the manual, under Licence in the Administration chapter, and as a
clause of the licence agreement. What travels: the Device ID, the primary MAC address,
the operating system and architecture, the Audiogravi<sup>ty</sup> version, the current licence
status and, during the trial, the date it started. The licence file itself goes when it
is being verified, and the hostname you type when activating a key. The server records
the address the request comes from.

What does not travel: your music, the paths it lives at, the credentials of any service
you have signed into, and anything about what you listen to.

Worth saying plainly, because it is the part most likely to be misread: whether Pro is
unlocked is decided **on the box**, from the signature of its licence file. No
round-trip to the server decides it.


### The setup screen now shows what it just did

You run the first-time setup, it reports success, the three services come back
configured — and the tab behind the window is the one from before. The banner
inviting you to configure is still there, the tiles still say the services are
not configured. Reloading the page by hand shows the truth. It is the worst
possible moment for a screen to freeze: the one where you are looking for
confirmation that something happened, and where the natural conclusion is that
it did not.

The refresh was there all along. It never ran: the setup panel sits inside a
dialog, and the code meant to update the tab was being called on the dialog
instead of on the tab, failing silently every time. The box had been reporting
itself correctly configured throughout.

Fixed, and one more thing with it: the installation-log window used to close by
luck. Its own close button was writing to the wrong place, and the window only
shut because something else happened to be listening. It closes on its own
account now.


### A box that plays no local files is a box like any other

Setting up Audiogravi<sup>ty</sup> asked for a music folder, and would not finish without one.
But plenty of boxes hold no music at all: everything comes from HIGHRESAUDIO, Qobuz or
Tidal, or the box is there to receive AirPlay, or to bridge UPnP. None of that needs a
single file on disk.

Those owners had one way past the button — invent a path — and the box took it. Nobody
checked that the folder existed. What came out looked like a complete success: the
configuration written, MPD running, the tile marked as configured, the indexing announcing
it had finished, because there was nothing to walk through. And a library with nothing in
it, with no explanation anywhere.

The setup now offers **No music library — online listening only** as a choice in its own
right. It is not an empty field: it is an answer, and the box records it as one.

It works in both directions. A box that started without a library can be pointed at one
later. A box that has one can be released from it — that asks first, since it takes
something away; nothing on disk is touched, and you can point it back whenever you like.

And a path you *do* give is now checked before anything happens: it must be absolute, it
must exist, it must be a folder, and MPD must be able to read it. That last one matters
more than it sounds — MPD runs under its own account, so a folder you can open is not
necessarily one it can, and until now that ended as an empty library with no clue as to
why. Each refusal names what was wrong, and arrives before a single thing on the box has
been changed.

### An empty library and a missing one no longer look alike

MPD turns down every question about a collection it does not have, and that refusal
carried none of the information Audiogravi<sup>ty</sup> was reading — so it arrived as "no
albums", and as "no results" when searching. On a box whose library had never been set up,
the interface was announcing that your collection was empty.

Both now say what is actually going on: *No music library is configured on this box. Add
one from the Config tab, or keep listening to your streaming services.* A collection that
really is empty is still reported as empty.


### A configuration tile that admits the software is not there

The Services and Profiles tabs have always been able to say *this software is not
installed*. The Configuration tab could not. It showed a tile like any other for a package
that was not on the box — the path of a file that did not exist, a button offering to edit
it, a download button with nothing to fetch, and no date, no state, no badge. Nothing said
why the tile was half empty, so it read either as something broken or as software that was
there.

Such a tile is now dashed and greyed, carries an **UNAVAILABLE** badge, says the package is
not installed, and links straight to **Audio Software**, where it is installed. Come back
after installing it and the tile has caught up on its own.

What still works, still works. Removing a package without purging it leaves its
configuration file on the box, and that file stays downloadable — a file that is there can
always be taken away, and its backups are not lost, they return with the package. What
cannot work is refused instead of being offered: editing is closed, because saving a
configuration also restarts the service, and no restart succeeds for software that is
absent. The opposite case is untouched — an installed service whose file has gone keeps its
editor, since that is what creates the file.

### Every service's state, including the ones sitting still

The same tab showed no state at all for some services. It was asking systemd for its list
of loaded units, and that list quietly leaves out anything installed but idle — the UPnP
bridge, on an ordinary box, was simply missing from it. Those tiles had no badge, and
nothing separated *stopped* from *not installed*.

Each service is now asked about directly, so **RUNNING**, **STOPPED** and **FAILED** show
up wherever they belong. The tab also asks the box one question instead of two, and asks it
over the system bus rather than by running commands — which matters more than it sounds:
the same answer feeds the audio pipeline, and that path now creates no processes at all
where the first attempt created six every time the pipeline refreshed.

### Silence, explained

Everything Audiogravi<sup>ty</sup> plays goes through MPD — your files, the queue, radio,
and all three streaming services. The box stops it itself when you pick the Roon or the
HQPlayer profile, and the Services tab lets you stop it by hand, so a stopped MPD is a
state you reach on purpose. It was also the one failure the box could not name: pressing
play answered *Playback failed — Queue operation failed*, and the library showed no albums
at all, as if your collection had vanished.

Now every one of those moments says the same thing: **MPD is not running. Start it from
the Services tab.** Playing, queueing, removing a track, searching, casting to a network
renderer, starting a station.

Two details worth knowing. Audiogravi<sup>ty</sup> restarts MPD itself when you change
output, and during that second the port refuses exactly like a stopped daemon — so a
refusal is confirmed a second later before anything is claimed, rather than sending you
after a daemon that is already coming back. And a daemon that is listening but not
answering is a different fault; it is not reported as this one.

### A box that can play, after an install and after an update

Installing the MPD package is not the same as having its daemon running. A box that
already carried MPD, with the service stopped or simply not set to start with the machine,
went through the whole installation without anything noticing — and came out with an
interface in front of something silent. Every installation and every update now starts MPD
and sets it to start with the box.

If you run yours as a Roon endpoint or an HQPlayer NAA only, MPD is still yours to turn
off — but stopping it is not enough: it comes back at the next boot unless you also turn
its **ENABLED** switch off. And an update turns both back on, deliberately: a box that
cannot play is a broken box, and turning MPD off again is two clicks.

### The whole HIGHRESAUDIO shop, not three shelves of it

HIGHRESAUDIO arranges its catalogue in fourteen shop categories. Audiogravi<sup>ty</sup> showed
three, and had renamed two of the three: what they call *High-Res Essentials* appeared as
*Discover*, and *Editors Choice* as *Editor's Picks*. The three were written into the interface by
hand, which is why the other eleven were not merely hidden but unreachable — the label highlights
that speak to a collector (ECM, Pentatone, Sony, Universal, Warner), the bestsellers, the editorial
tips, the albums just added.

The box now asks HIGHRESAUDIO for the list and builds one button per category, in their order and
under their names. A shelf they add tomorrow shows up on its own, without an update from us. Four
of their titles arrive in German whatever language is requested — a quirk of their interface that
their own application works around the same way — so those four are relabelled on screen
(*Hörtipps* becomes *Tips*) while the box keeps asking for them by their real name.

### Two more ways into the same catalogue

HIGHRESAUDIO arranges its music a second way, by genre: twenty-six of them, a hundred and
eighty-six subdivisions underneath. None of it was reachable. A **Genres** button now opens a second
row under the shelves — the genres, then the one you pick with its own subdivisions, and a way back.
The whole genre is offered as **All**, because two of their genres contain a sub-genre of the same
name and two identical buttons side by side read as a mistake; the heading above the albums tells
you where you stand, *Soundtrack · Original Score*.

And a search can now be narrowed by **composer** or by **record label** — the two questions the
words alone cannot answer: the composer of a classical recording appears on no other field, and a
collector browses by ECM or Pentatone. Both narrow what you typed rather than replacing it, and an
empty pair of fields changes nothing.

Two filters HIGHRESAUDIO offers are deliberately missing, and it is worth saying why. Choosing an
audio **format** makes their search discard the words you typed: we measured three different
searches, one of them deliberate nonsense, returning the same fifty albums. And a **mood** takes
about a minute to answer the first time. A control that quietly searches for something else, or that
hangs for a minute, is worse than no control at all. Both are reported to them, and both come back
the day their answer changes.

Fifteen buttons no longer fit across a screen, so the row scrolls. Where it continues, it now fades
into the page rather than cutting a word in half, and on a computer a small chevron in each margin
moves it one shelf at a time. On a touch screen the fade alone marks the way, since the strip is
already yours to drag. Neither appears on a row that fits, and each goes out as soon as its end is
reached.

### Their playlists, and yours

HIGHRESAUDIO keeps two separate collections of playlists: the two hundred selections its editors
publish, and the ones belonging to your own account. Neither could be reached, on a box where Qobuz
and Tidal have had their Playlists shelf from the first day.

A **Playlists** button now opens both. A playlist behaves like an album from there on — open it to
read its tracks, or send the whole thing to the queue in one gesture, whether you listen on the
box's own DAC, on a network renderer or through HQPlayer. An account with no playlist of its own
says so plainly instead of looking broken.

What this does not do is write. Creating a playlist, renaming one, adding or removing a track:
what HIGHRESAUDIO has made is readable, what you make stays where you made it. That is a
deliberate first step, not an oversight.

One repair travelled with it, and it reaches further than playlists. HIGHRESAUDIO allows a single
signed-in device per account, so any other phone or computer signing in ends the box's session —
an ordinary event the box is built to recover from by signing back in on its own. It recovered
from two of the three ways the service announces a finished session, and not from the third, which
happens to be the one used by everything tied to your account: playlists, favourites, purchases,
downloads. The box did not notice, did not sign back in, and answered with an empty list — telling
you the account owned no favourites, on an account that owns some. All three are now recognised,
verified against a session genuinely ended from another device rather than a simulated one.

---

## 0.9.44 — 2026-08-21

### A box that can play, out of the box

Installing Audiogravi<sup>ty</sup> set up Audiogravi<sup>ty</sup> — and nothing else. The engines it
conducts were left for you to add, which is defensible in a manual and indefensible on screen: you
reached the interface of a brand-new box, found no output to select and no music anywhere, and
nothing told you that a single button under **Audio Software** was the missing piece.

MPD now comes with the box. Calling it one engine among several was the mistake: your local files,
the queue, internet radio and Qobuz, Tidal and HIGHRESAUDIO all reach your DAC through it, and the
UPnP bridge is a front-end that drives it. Without it there is an interface and no sound.

So it is no longer presented as a choice. Its card keeps **UPDATE** and loses **UNINSTALL**, and a
box asked to remove it says why rather than obeying. If you run yours purely as a Roon endpoint or
an HQPlayer NAA, stop the service from the **Systemd** tab — a stopped daemon costs nothing, and
your setup stays exactly as you want it.

The other engines are untouched, and remain yours to install or remove: AirPlay, the UPnP bridge,
Roon Bridge, Roon Server, HQPlayer NAA.

### One line, no token

Until now, installing Audiogravi<sup>ty</sup> meant owning a credential. Early access ran from a
private repository, so the install command carried a 90-character access token that had to be
sent by e-mail, pasted without a typo, and kept — the box stores it, because one-click
self-update reaches for the same repository later.

It never fit what the product promises. Owners retyped it by hand, asked how to move it from a
laptop to the box, or ran the example from this page as if it were the real thing. And because
the same token served everyone, its life was collective: it expired on a set date, and one copy
left in the open ended it for every owner at the same moment.

The repository is public now and the token is gone from the entire path. Installing is one short
line, typed straight into the box:

```bash
curl -fsSL https://audiogravity.app/install.sh | sudo bash
```

There is nothing to request, nothing to carry across machines, and nothing to renew.

Boxes installed during early access still hold the old token, and it would have stopped them
updating — a credential that is no longer valid is refused even by a public repository, where
asking for nothing at all is accepted. They now clear it themselves. Your box fetches the
installer afresh every time it updates, so it collects the fix on its first attempt: it tests the
credential it is holding, drops it when the answer is a refusal, and removes it from its
configuration. Nothing to do, and nobody has to open a terminal on a box.

---

## 0.9.43 — 2026-08-19

### The explanation behind the dash, delivered at last

0.9.42 stopped a service card from claiming **0** where nothing had been measured, and put
a line under the **Services** title explaining what a dash means and how to get the number
back. The dashes appeared. The line did not — on any box.

Your machine sends one measurement report per cycle. One fact on it belongs to the machine
rather than to any single service: *this kernel counts no memory at all*. The interface was
breaking that report into one message per service before handing it on, and that fact, having
no service to belong to, fell out. The **Services** tab was listening for the whole report,
which nothing had sent since v0.9.4 — so it never had the one thing it needed to speak.

It is sent now. On a Raspberry Pi, whose kernel starts with the memory counter switched off,
every card shows a dash for memory and the line finally says why, with a link to the one-line
boot change in the manual.

The same missing report also left the **Profiles** tab showing service states frozen at the
moment you opened it. That tab had been waiting on it just as long, and it too is live again.

---

## 0.9.42 — 2026-08-19

### A dash where there was never a measurement

Three of the figures on a service card come from counters that can be switched off:
memory, disk and network. When they are off, nothing on the machine knows the answer — not
systemd, not us. We were publishing that silence as **0**, under a flat graph, which is
precisely how an idle service looks. A box measuring nothing looked like a box doing
nothing.

Those figures now show a dash, and no graph is drawn. The Services tab explains once, above
the cards, what a dash means and how to get the number back — because the two cases have
different answers:

**Disk and network** are counted service by service, and only when *IO Accounting* and *IP
Accounting* are enabled for that service in the **Systemd** tab. Two switches, effective
straight away, no reboot.

**Memory** is not up to the app at all: a Raspberry Pi kernel starts with that counter
switched off, and turning it on means one line on the kernel command line and a restart.
The note links to the manual, which walks through it.

CPU and tasks are always measured, and nothing about them changes.

_Nothing yet._

---

## 0.9.41 — 2026-08-18

### Roon keeps looking, without keeping your box busy

The check we added last time was right to exist and wrong in its pacing. If your Roon
Core is switched off — overnight, or while you are away — your box went looking for it
every single minute, for as long as it stayed on. Nothing came of it, and it is exactly
the kind of small, endless work an audiophile machine should not be doing in the
background.

It now eases off: every minute at first, stretching to a quarter of an hour while nothing
answers, and straight back to the quick pace the moment you open the Roon card. So the
Enable click you make inside Roon is still picked up within a minute, and an idle box is
left alone.

The box's log changed with it, in the other direction. It was meant to report an
unchanged situation once instead of once per attempt, and it did — but it also managed to
swallow the single event worth recording: a Roon Core that stops answering in the middle
of a session. That one is now always written down, and a Core that has moved to another
address is named again rather than muted by an older report.

One more thing you would only have noticed as a general slowness: a connection attempt
that hangs — a Core that answers and then never finishes introducing itself — used to
consume, once a minute, one of the workers the whole box shares. Left long enough,
nothing else could run and the Pipeline tab stopped answering at all. Such an attempt is
now confined to a thread of its own, and there is never more than one.

### An empty signal path tells you what it is waiting for

Open the Pipeline tab on a phone and you could find the track playing above a blank
space — no box, no converter, no speakers, no explanation. It looked broken. It was not:
the view draws each device only when music actually flows through one of the connections
**you have described**, and every new box arrives with an example description — a
converter reached over USB and optical — meant to be replaced by your own gear.

If your converter is a HAT board sitting on a Raspberry Pi's connector, it matches
neither of those, so nothing in the chain lights up and the drawing empties itself. We
found this on two of our own boxes, both blank for exactly that reason, with nothing on
screen to say so.

Now the panel speaks, and it puts the two facts next to each other: what your box is
playing through, and what your description declares. Seeing *HiFiBerry DAC+ Pro* on one
line and *USB Audio Output, Optical Output* on the next is usually all it takes to know
which of the two has to change.

Where to change it was itself a dead end on a phone: the **CONFIG** button existed only
in the desktop layout, while the phone is exactly what you have in hand when you notice
something is wrong. The Pipeline tab now carries the same bar on both, so the panel can
point at a button that is really there. And when the
description does match your gear and simply nothing is playing, it says that instead of
leaving you guessing between the two. The manual carries the same explanation, both where
outputs are described and in the troubleshooting chapter.

_Nothing yet._

---

## 0.9.40 — 2026-08-17

### Roon, without the terminal

Connecting Audiogravi<sup>ty</sup> to Roon used to take a route no owner should have to
walk: open an SSH session on the box, edit a configuration file, type in your Roon
Core's IP address, restart the backend — and only then click **Enable** in Roon. Four of
those five steps are gone.

What remains is what you would expect. Install **Roon Bridge** from the Audio Software
page. Open Roon → **Settings → Extensions**, and enable **Audiogravity**. That's it.
Your box looks for your Core on the network by itself and finds it in about five
seconds, so its address is something you never need to know. And the click inside Roon
was always the permission that mattered — nothing is read from your Core, or sent to it,
until you give it. Asking for the same consent a second time, in a file, only made the
feature hard to reach.

Three settings disappeared along the way, and not one of them did what its name
suggested. The port was never read at all: Roon fixes it, and the value the file
carried pointed at a different port, closed on the Core. The on/off switch duplicated
Roon's own authorization. And the extension's name only made it harder to find — one
box announced itself in Roon's list as “Aty” while its owner scrolled past looking for
“Audiogravity”. Boxes running Roon Server instead of Roon Bridge are covered by the same
rule; the Roon section of the manual is rewritten around the two steps above.

The card itself now tells you where you are. That matters more than it sounds: the step
above happens inside Roon, on another screen, and your box has no way of seeing you take
it. Expand the Roon card and it says what is true — no Roon Bridge running here, no Core
answering, waiting for your authorization (naming the extension to look for), or
connected with the number of zones. While it waits, **I have enabled it** checks again
straight away rather than leaving you wondering whether the click registered, and the
list of zones fills itself in as soon as the connection comes up.

One more thing, less visible but worth knowing: your box used to try to reach your Core
exactly once, when it started. Switch the Core on afterwards and Roon simply stayed
absent until someone restarted the backend. It now keeps an eye out, quietly, and never
makes the interface wait while it looks.

---

## 0.9.39 — 2026-08-17

### A service you stop stays stopped

Stop MPD from its card, or switch to a profile that leaves it out, and on a recently
installed box it came straight back — under two seconds later, before the page had
finished refreshing. On one box: stopped at 07:40:32, running again at 07:40:34. There
was no way to keep it off, and nothing on screen to explain why.

The cause is in how Debian ships MPD: as two pieces rather than one. There is the
daemon, and there is a second piece whose only job is to hold MPD's port open and start
the daemon the instant anything connects to it. Your box connects to that port
constantly — that is how it knows what is playing — so it woke up the very thing it had
just been told to stop. Audiogravi<sup>ty</sup> writes MPD's own configuration with the
address and port it should listen on, so that second piece was never doing anything the
daemon does not already do for itself. It is now locked out when Audiogravi<sup>ty</sup>
is installed, and MPD runs when, and only when, Audiogravi<sup>ty</sup> says so.

If your box never showed this, it is because that second piece happened to be switched
off already — recent installations arrive with it on. It gets the same treatment at its
next update either way, and uninstalling Audiogravi<sup>ty</sup> puts the piece back.

One consequence is worth spelling out, because it is a change you could notice. That
second piece also decided *where* MPD could be reached, and it answered the whole
network. MPD now answers only on the box itself — which is what
Audiogravi<sup>ty</sup>'s own configuration has always asked for; the wider opening came
from the packaging, not from a decision. Nothing you use through Audiogravi<sup>ty</sup>
is affected: the interface, the UPnP renderer your phone sends music to, and playback
itself all reach MPD from inside the box. We checked this on a box that has been
local-only all along — its renderer is visible on the network and works normally. The
one thing that stops working is a third-party MPD application, on a phone or another
computer, connecting straight to the box. If that is part of how you listen, tell us:
opening that door again is reasonable, but it should be a switch you turn on knowingly
— the port in question asks for no password, so anything on your network can control
the music through it.

---

### The configuration editor stays where you put it

Open a service's configuration and it lands on **Guided**, which is the right place to
start. Choose **Structured** or **Expert** and, about a second later, it slid back to
Guided on its own — and if you had started typing, that went too, without the question
you normally get before changes are discarded. Anyone who wanted the raw file had to
race the interface for it.

The click was never the problem. Your box streams the state of each service
continuously, so the little status dots on the tiles stay true without you refreshing
anything. The editor was reading one of those heartbeats as "a different service has
been opened" — the one situation where returning to the default view is exactly right.
It now tells a heartbeat from a service apart. Opening another service still starts you
on Guided, as before.

---

## 0.9.38 — 2026-08-16

### Installing something no longer surprises you

Three things could go wrong around an installation, and all three were silent.

An install began by refreshing the system's package lists, and that step reports
failure if **any** configured source is unreachable — including repositories
that have nothing to do with audio, which a box accumulates over time. The
install stopped there, on a package that was very often already available
locally. It now carries on and lets the package manager say whether it can
actually find what was asked for; and the refresh waits its turn rather than
failing when another operation is already using the package system, which is
what happened when a version check and an install overlapped.

Nothing measured the free disk space. A disk filling up mid-download left a
truncated file, and on an update that is worse than a plain failure: the old
version has already been replaced by the time the tool complains. The room
needed is now checked first — the download plus as much again for unpacking —
and a filesystem that cannot be measured is never treated as full.

And installing something still does not configure it — deliberately, because
writing an audio configuration on your behalf is not a side effect an install
should have. What changed is that the card now says so. A freshly installed
service runs on the settings its own package ships: it will start, it will look
perfectly ready, and it may well play to the wrong output. The card says "not
configured" until Audiogravi<sup>ty</sup> has written that service's
configuration itself — which is judged on a marker it puts in the file, not on
the file existing, since every package ships one. It also means the label
reappears if a package upgrade ever replaces the file. When the box cannot
answer the question at all, the card says nothing rather than accusing
everything.

The last one is the most ordinary. Updating a package restarts the service it
drives, because the package's own installation script does that; uninstalling
stops it. Neither was said anywhere, so choosing *Update* in the middle of an
album simply cut the music. The confirmation now tells you which service is
about to be restarted or stopped. Deliberately said rather than prevented:
knowing whether that service is *currently* playing would mean rebuilding the
entire audio pipeline before every operation, which is a lot to pay for a
question the person pressing the button can answer better than the box.

### And keeps telling you, instead of answering with the day it booted

Reading the right source is worth little if it is read once. The check ran a
couple of seconds after the box started and never again: a machine left on for
three weeks — which is what an audio box is for — answered with what had been
true on the day it was switched on, and the notification could only ever fire
in that same moment. It now repeats once a day.

The subtler half is where the answer comes from. For software that lives in a
package repository, the version on offer is read from a list held locally, and
that list is only as current as the last time something refreshed it.
Audiogravi<sup>ty</sup> only refreshed it as the first step of an installation,
so on a box where nothing had been installed for months the answer was months
old — and whether anything else refreshes it depends on the distribution:
DietPi switches those automatic refreshes off, Raspberry Pi OS leaves them on.
The same box running the same code gave two different answers depending on
which one it was. Measured on a DietPi machine: the main Debian index dated
from five weeks earlier, so a security update to MPD would have been invisible
for five weeks.

The box now refreshes before it answers, and so does the **Check updates**
button, which is what everyone assumed it did. The cost is deliberately
bounded — the refresh is skipped when the lists are already recent, it takes
about five seconds when it does run, and an update you have already been told
about is not re-announced every day.

One thing was removed rather than added: the browser used to keep its own copy
of the last versions it had seen, with no expiry, and lay it over a fresh
answer from the box. A version that had stopped being offered could therefore
keep an update badge lit on that browser indefinitely. The box remembers now,
so the copy is gone.

### The audio software page starts telling you what is actually out there

Knowing what is installed is half the question. The other half — is there
something newer — was answered by the system's package manager, which works well
for software that comes from a package repository and not at all for software
that does not. HQPlayer NAA does not: it is downloaded straight from its
publisher. Asked about it, the package manager replied with the version already
installed, so Audiogravi<sup>ty</sup> compared a version with itself and said
"up to date" every time. Measured on a box: 5.1.5-67 installed, 6.1.4-71
published — two major versions, invisible. The code that reads the publisher's
page existed and had simply never been called. It is now, and while looking at
what pressing *Update* would do, one more thing changed: the newer package is
installed over the old one instead of the old one being removed first, so the
audio output no longer vanishes for the length of a download.

Roon is the opposite problem: it publishes no version number at all, anywhere.
Its download has a fixed name and carries no version file, so there is nothing
to compare — and because the interface insisted on a number, it refused the
action outright, leaving no way to update Roon from Audiogravi<sup>ty</sup> at
all. Updating Roon simply means re-running its own installer, which always
fetches the current build. That is what the button now offers, and it says so:
no version to compare, here is the one you have, shall we fetch the latest.

The last one is invisible until you know it is there. The UPnP bridge has no
official build for 64-bit ARM, so Audiogravi<sup>ty</sup> builds and hosts it.
Those packages carry their version in their file name, and those names were
written into the release — so rebuilding and publishing changed nothing on any
box until the next release edited them. The list of files now comes from the
checksum manifest already published beside the packages, which is the same file
already downloaded to verify them: no new mechanism, one fewer thing to keep in
step, and the version to display comes with it. Since that manifest now decides
what gets installed rather than merely confirming it, it is checked against the
packages the release expects — an unexpected, missing or repeated entry stops
the install before anything is downloaded.

### The audio software page stops guessing about your box

Audiogravi<sup>ty</sup> builds itself a small reference file describing what your
particular machine can install and where the software on it lives. Everything the
Audio Software page shows or does reads that file. It turned out to contain several
things that were not true, and each of them was visible.

The clearest was Roon. On a box where Roon Bridge had been installed by DietPi rather
than by Audiogravi<sup>ty</sup>, the card showed no version at all, and uninstalling
announced a success while removing nothing — the program stayed on disk, whole, and
only its service entry disappeared. Behind it was one assumption written down as a
fact: that Roon lives in `/opt/RoonBridge`. It does, when Roon's own installer puts it
there; DietPi's puts it in `/opt/roonbridge`, with its data somewhere else again. The
tempting fix is to test the operating system and branch — and it would be wrong, since
a DietPi box where Audiogravi<sup>ty</sup> installs Roon itself lands back on the first
layout. What decides is not the machine but who installed it, and the running service
knows. Both paths are now read from it, and re-read after every install and uninstall
so the file cannot go on describing a state that has moved on.

Removing them is its own small problem. Deleting a folder that is not there succeeds
without a word, so the step that removed nothing had no way of knowing it, and the
service entry — the only thing that could still have located the files — was deleted
immediately afterwards. That is how the original fault stayed invisible. The removal is
now checked rather than announced, and it fails loudly when there was nothing where
there should have been something. If an earlier attempt already took the service entry
away, it looks for both layouts by name instead of giving up on the very one it exists
for, and it says outright that the data folder can no longer be worked out — better an
admission than the impression of a clean sweep.

The second was quieter and would only have bitten a 32-bit ARM owner. The list of
architectures a package supports was read from the *names of the folders* on the
publisher's server; upstream `upmpdcli` has a 32-bit ARM folder that holds only its
add-ons, and its repository declares two architectures, neither of them that one. Every
box therefore carried "32-bit ARM supported" for a package that apt would have refused.
The repository's own manifest is now read — the same thing apt obeys — and the package
is confirmed present for your architecture before it is offered.

The third is about honesty rather than correctness. If a publisher's site could not be
reached while that file was being worked out, the software was recorded as
unsupported — the same word used for software that genuinely has no build for your
machine, and just as permanent. A box installed without an internet connection came up
with HQPlayer NAA, the UPnP bridge and Roon all marked unsupported, with nothing to say
why. Those are now two different answers, and the card says which one it is: something
unreachable is worth trying again, something incompatible is not.

Two smaller things came out of the same pass. Installing the UPnP bridge on a fresh box
now works — adding a publisher's repository writes two system-owned files, and the box
had permission for neither, so the install stopped at its first privileged step.
And Roon Server is no longer offered next to Roon Bridge: the Server already contains
the Bridge, so having both means two Roon endpoints on one machine fighting over one
audio output, and Roon's own installer neither notices nor warns. The card now names
which of the two is in the way. A box that already has both still shows both — the rule
decides what can be installed, it does not hide what is there.

### The interface stops behaving like a document

Press and hold a button on a phone and, instead of the button responding, a blue
highlight would spread over its label and the *Copy / Look Up* bubble would rise over
it. Drag a mouse across the screen on a computer and it left a trail of highlighted
words behind it. Neither was doing anything useful: a browser treats every page as
prose to be read and copied, and Audiogravi<sup>ty</sup> is a console you operate, not
a text you read.

Selection is now off across the interface. What matters is where it deliberately
stays on, because that list is the whole point of the change: anything you type into,
the details of an event, the differences shown before a service change is applied, and
the short technical values you may need to send us — an order number, a media server's
address. Where a copy button already existed, as on the logs and the Device ID, it is
still the quickest way and it has not moved.

The terminal is the interesting exception. It looks like the one place that most needs
selecting and copying, and it is — but it has always drawn its own selection rather
than relying on the browser's, precisely so that a selection follows the grid of
characters instead of the page underneath. Handing the browser's selection back to it
would have set the two against each other. So the terminal is left exactly as it was,
which is what keeps its copying working.

---

## 0.9.37 — 2026-08-13

### Two ways the volume was not telling the truth

Both were found the same way — by watching what the box actually publishes while
someone moves a slider, rather than by reasoning about the code — and both turned out
to be different from what they looked like.

**A DSD album could leave every volume at maximum.** DSD is a 1-bit stream, and any
attenuation degrades it, so Audiogravi<sup>ty</sup> raises the volumes to 100 while one
plays and puts them back when it ends. That is why the slider is replaced by a padlock
during DSD: the level is deliberately out of your hands for the duration.

The putting-back only happened if something was still playing at that precise moment.
When a DSD album simply reached its end — or was stopped before choosing what came next
— the restore was skipped, and the levels being held were thrown away in the same
breath. Nothing later could recover them. Whatever you played next played at 100, and
the only way back was to set the volume by hand. It looked intermittent because it
depended on something else happening to be paused at the right instant.

Restoring now happens whether or not the music is still running. One subtlety shaped
the fix: a player that fails to answer is indistinguishable, from the outside, from a
player that has stopped — and writing a level on the first case would attenuate a
stream still in flight, the exact harm the whole mechanism exists to prevent. So the
end of a DSD stream is now established by asking, once, instead of inferred from
silence. When the answer does not come, nothing is written and nothing is forgotten.

**And the slider could jump backwards after a drag.** A moment after letting go, it
would flick to somewhere in the middle of your own gesture before landing on the value
you chose. The previous release fixed one cause of this, and that fix does hold —
verified, nothing arrives out of order any more. What remained is simpler: a drag sends
one command per movement, so for about a second after you let go, the box is still
publishing the levels your finger passed through on the way.

The slider was covering that with a fixed pause of a second and a half. Measured
against a running box, the correct value arrived after 1.26 s — a quarter of a second
of margin. Enough on an idle machine; not enough on a busy one, a slower one, or after
a longer drag. It now keeps the level you asked for until the box confirms that exact
level, so no margin decides whether the display is right. The same gap existed in the
player at the bottom of the screen, where nothing had gone wrong yet; it is closed
there too.

---

## 0.9.36 — 2026-08-13

### Your streaming subscriptions reach HQPlayer

Until now, choosing HQPlayer as your output meant giving up Qobuz, Tidal and HIGHRESAUDIO.
The refusal was immediate and explicit — turn HQPlayer off to play this — which at least
told the truth, but the choice it forced was an odd one: your DSP engine or your
subscriptions, never both.

Nothing had to be invented to lift it, and that is the interesting part. Your local
library, internet radio and media servers all reach HQPlayer the same way: Audiogravi<sup>ty</sup>
hands it a web address on your own network, and HQPlayer fetches the music itself. The three
streaming services already publish exactly such an address — network speakers have been
pulling Qobuz and Tidal through it for months, for the same reason a speaker cannot hold a
password. The route existed; it had simply never been pointed at HQPlayer.

**Where the music actually travels** differs by service, and it is worth knowing because it
decides what your box spends its evening doing. For **Qobuz** and **HIGHRESAUDIO**, the
address redirects straight to the service's own servers: your box hands over an address and
steps aside. It carries nothing. Measured during playback, the core sits at four percent of
one processor core — the cost of watching, not of relaying. **Tidal** is the exception: it
delivers its audio in a form that has to be converted before anything can play it, so that
one stream does pass through the box. Measured on a genuine first listen — nothing cached —
HQPlayer plays the conversion while it is still being written, knows the full length of the
track, and never runs its buffer dry.

Nothing is re-encoded on any of the three paths. What reaches your DAC is bit-for-bit what
the service sent, then whatever HQPlayer's own filters make of it.

### The screen follows the track again, through a whole album

The previous release noted one limit: with HQPlayer as your output, an album showed the
first track's title, artist and cover from beginning to end, while the progress bar moved on
correctly at every change. Two sources, two behaviours, and only one of them right.

It could not be fixed by asking HQPlayer. It reads no tags at all from a stream it fetches
over the network — asked what it is playing, it answers "HTTP stream" even for a perfectly
tagged Hi-Res file, with no artist and no album. That closed the obvious door and opened a
better one: Audiogravi<sup>ty</sup> already knows every title, artist and cover of what it
sent, and HQPlayer does say which entry of its list is playing. Keeping the list and reading
the number is enough. Nothing is asked of anyone, and no extra request is made.

It follows on everything Audiogravi<sup>ty</sup> pushes — your own library included, which
had the same problem for the same reason.

Two situations still show no title, and both are the honest answer rather than a gap. A
playback you started from **HQPlayer's own remote** was never sent by Audiogravi<sup>ty</sup>,
so there is no list to read and nothing truthful to display. And if you **rearrange
HQPlayer's playlist from HQPlayer itself** while it is playing, that is noticed too: the
list no longer matches, so the labels stop rather than caption someone else's music with
your album's titles.

**Internet radio is a separate matter.** A station announces each song inside the audio
stream, and through HQPlayer it is HQPlayer that receives that stream — and it keeps only
the station's name. So a radio played through HQPlayer shows the station and its logo where
the same station on your local output shows the song. That one is a real gap, and it is
written down as work to do.

### Three things that were quietly wrong, with HQPlayer as your output

**Starting an album did not replace what was playing.** It queued behind it. The first album
kept playing, the new one waited its turn — and the screen showed the new one's title and
cover the whole time. You were looking at one record and listening to another. The command
that empties HQPlayer's queue turns out to leave the track that is loaded and playing
exactly where it is; it is now stopped first, which empties it properly.

**A track found by searching a media server refused to play.** Playing the same track from
the server's folders always worked, so the failure looked like a fault in the server. It was
not: the request was being handed to the local library index, which was asked to find a file
named after a web address.

**Tidal in a quality that cannot play now says why.** Tidal's lossy qualities deliver AAC,
which cannot be converted losslessly — so nothing came out, on any output, with nothing said.
Audiogravi<sup>ty</sup> now looks at what Tidal *actually serves* rather than at what your
account asked for, which matters more than it sounds: an album unavailable in lossless comes
back as AAC even when your setting is right, and no setting can warn you about that.

### The certificate you were told to install could not be fetched

The previous release gave boxes installed with HTTPS a certificate authority of their
own, and told you to collect it from `https://<box>/ca.crt`. That address cannot work,
and the reason is circular: fetching a file over HTTPS means trusting the certificate
protecting the connection — which is the very certificate you are coming to collect.
Safari on iOS does not offer a way through. Not a warning to accept, not a button to
tap: it refuses. The procedure was impossible on the device it was written for, and so
was the app install that depends on it.

It went out because the feature was tested where it was built. On a computer the
authority is already trusted, or the browser lets you push past the warning, so the
address answers and everything looks correct. The one device that cannot is a phone
that has never seen the box before — which is every phone, the first time.

The authority is now handed out over **plain HTTP**, on a port that serves that one
file and nothing else: every other address on it is redirected to the HTTPS interface.
Being unencrypted is deliberate and costs nothing. A certificate authority is public by
design — handing it out is its entire purpose — and it contains no key. What would be
serious is serving the *private* key in the clear, which is a different file, in a
different place, and which the previous release stopped serving at all.

The written steps were wrong too, and for a worse reason: they had been composed from
memory rather than performed. The iPhone ones are now what a phone actually does,
checked end to end — including the step that everything hinges on, which is easy to
miss because it looks redundant. Installing the profile does **not** trust it; a
separate switch, in a different part of Settings, does. Miss it and nothing changes,
with no error to explain why.

For Android we now give no menu path at all. It differs between versions and between
manufacturers, so a single path would be wrong for most phones. The manual describes
what has to be achieved instead, along with the two things that genuinely block
people — a screen lock is required before Android will store an authority, and since
Android 11 only the Settings app may begin the install, so tapping the downloaded file
does nothing. And it says outright that, unlike the iPhone route, nobody has run the
Android one on a device. That is the honest state of it, and better written down than
implied.

---

## 0.9.35 — 2026-08-12

### HQPlayer: the progress bar works, and you can move around in a track

The bar was there and it was inert. The elapsed time counted up, the bar never moved, and
dragging it did nothing at all. Two assumptions inside Audiogravi<sup>ty</sup> explained
it: that HQPlayer cannot jump to a position, and that it has nothing to say about how long
a track is. Both were written down years ago, one of them in a specification, and neither
had been checked against the thing itself.

Asking HQPlayer directly took a few minutes and contradicted both. It accepts a jump to any
position — sent one on a playing track, it moved from 1:16 to 2:20 without a hiccup. And it
works out a track's length by itself: for a stream nobody had described to it, it answered
seven minutes twenty, which was exactly right.

So both are now used. The bar has a scale, it advances, and you can drag it. The length
HQPlayer measures is preferred over the one the source supplied, because it is right more
often — and it is the *only* one available when you start playback from HQPlayer's own
remote rather than from Audiogravi<sup>ty</sup>, a case that used to show nothing at all.
A live stream still shows no length, which is the honest answer for something with no end.

One limit stood at the time of this release: push a whole album and the screen stayed on the
first track, because HQPlayer plays straight through without announcing that it has moved
on. It was written down as work to do rather than a wall, and the next release lifted it.

### The box can now prove who it is, so your phone will treat it as an app

Install Audiogravi<sup>ty</sup> with HTTPS and the box signs its own certificate —
nobody else can, because no public authority certifies a private address on your own
network. Your browser therefore warns you on the first visit, you accept, and you get
on with listening. That is where it looked finished, and where it wasn't.

Accepting a warning gets you a *page*. It does not get you an *app*. A phone only
grants a site a home-screen icon that opens fullscreen, starts without the network and
receives notifications once it genuinely **trusts** the certificate — and this one
could not be trusted, no matter how patient you were. It identified itself only in a
field that Chrome, Safari and Firefox stopped reading in 2017, so every one of them
refused it outright, and installing it by hand as a trusted certificate did not repair
that. On Android, the *Install app* prompt simply never appeared, and nothing on screen
explained why.

The box now creates a small **certificate authority of its own**, and signs the
interface's certificate with it. You install that authority once on each phone or
computer — the installer prints the address to fetch it from and the steps for iPhone,
Android, macOS and Windows, and the manual now has a chapter on it. After that the box
is trusted like any other site: no warnings, and the app installs normally.

> **Read this with 0.9.36.** The address printed here could not be opened on a phone,
> and the printed steps were wrong. Both are fixed in the following release; on 0.9.35
> alone this feature cannot be completed on an iPhone.

The reason it is an authority rather than a single certificate is what happens later.
Certificates expire, and addresses change. With one certificate, each of those events
means going back around every device in the house. With an authority, only the
certificate it signs is reissued — quietly, before every start and once a day — while
the authority your devices trust stays untouched. You do it once, and it holds for
years.

Reviewing that work turned up something older and more serious, unrelated to the
authority itself: **the interface was handing out its own private key**. The certificate
and its key sat in the same folder the interface serves its pages from, and the server
drew no distinction — asking it for `/ssl/key.pem` returned the key in full, to any
device on the network, with no password and no login. That key is what proves the box is
the box. The store now lives outside anything the interface serves; upgrading moves it
and deletes the exposed copy, and the server refuses that path outright as a second lock.
Only the public certificate, the one your devices are meant to install, is published.

Two smaller things came with it. A box that changes address no longer serves a
certificate for the old one, which it did indefinitely because the file was written at
the first install and never re-examined. And the QR code the installer prints at the
end takes a third less room on screen: same symbol, drawn exactly as precisely as
before, with the oversized margin trimmed.

---

## 0.9.34 — 2026-08-11

### Controls that tell the truth

Every transport control in Audiogravi<sup>ty</sup> — play/pause, next, previous, volume,
repeat, shuffle — used to work on trust. The command was sent to the player, the interface
flipped at once, and the player's answer was never read. Almost always that trust was
well placed, which is why it went unnoticed for so long. The exceptions were quietly
corrosive: a DAC with no volume control of its own refuses every volume change, and the
slider moved anyway; a player mid-restart drops commands on the floor, and the pause
button toggled over music that never stopped.

The seek was converted first — it is described below, and it forced the question of what
the other six controls should do when the player says no. The answer, chosen deliberately:
say nothing, and be right. On a refusal the button or slider simply returns to the true
state. No toast, no error banner — a control that visibly does not act is the honest
message, and a notification would be noise for something as rare as an output without a
mixer. The volume panel was the last holdout: it kept showing the level you dragged to
until you closed it. It now glides back to the real level a moment after you let go —
invisible when the change took, honest when it did not.

Two things stand behind this, worth a sentence each. After every command, refused or not,
the player broadcasts its actual state, and that broadcast — not the interface's optimism
— is the reference every screen converges on. And switching between audio outputs was
found capable of something worse than lying: it could disable every output and report
success. The new output is now switched on before the old ones are touched, so a refusal
leaves the music playing where it was, and the refusal reaches you with the player's own
reason.

The same treatment then went to everything that *adds* music rather than steers it:
queueing a track or an album, starting a radio station, removing a row from the queue.
All of them answered "done" without reading the player's reply, and the failures they hid
are the ordinary kind — a station whose address the player rejects, an album that left the
library index since the page was drawn, a queue row someone already removed. You would
click, see the interface agree, and hear nothing. Now each says what happened, in the
player's own words.

Two refusals are deliberately *not* passed on, because failing the whole request would lie
in the other direction. When you queue an album and the player stops partway through the
list, the tracks that made it in are yours — they are kept, and counted honestly. And the
titles Audiogravi<sup>ty</sup> attaches to queued streams are decoration: if writing them
fails, your music is still queued, and that is what you are told.

### Seeking a Tidal track on the very first listen

Tidal delivers its lossless tracks in pieces rather than as a file, so
Audiogravi<sup>ty</sup> reassembles each one on the fly and hands it to the player as it is
being written — which is why playback starts about a second after you press play instead of
after a full download. The cost was a small, oddly specific annoyance: on that first listen the
progress bar did nothing. The player decides whether it can jump around inside a stream at the
moment it opens it, and at that moment the file is still being written, so the answer was no —
for the whole track. Play it again later and seeking worked, because by then the finished copy
was on the box.

That finished copy is the thing this release makes use of. It is ready a few seconds into the
track, and it was simply never offered to the listen already in progress. Now, when you drag the
bar, the track is reopened from it and your jump lands. You do not see the reopen: a seek always
goes quiet for an instant, and it hides in there.

Two honest limits, both improvements in their own right. Dragging the bar during the first few
seconds, before the copy is ready, is still declined — but it now says so, where before it looked
like the app had simply frozen the bar at the position you chose. Same for a live radio stream:
a live broadcast has no end to jump to, and being told so plainly is better than a control that
appears to work and does not.

One more limit, added after testing the impatient case: if you drag the bar again while a reopen
is already under way, that second jump is declined rather than queued behind the first. Each
queued jump would have reopened the track in its turn, so three quick drags meant hearing the
track restart three times.

### The queue knew how long every track was, and threw it away

A track from your own library shows its length in the queue. A track from Qobuz, Tidal,
HIGHRESAUDIO or your UPnP server showed `--:--`, and the reason is a fair one: those tracks
reach the player as a stream, and MPD — which does the playing — only learns how long a
stream is by decoding it. A track waiting its turn in the queue has not been decoded, so it
has no length to report.

But the length was never actually unknown. Qobuz says it. Tidal says it. HIGHRESAUDIO says
it, and a UPnP server puts it in the very listing Audiogravi<sup>ty</sup> reads to show you
the album. Every one of those values was in hand at the moment the track was queued, and
every one of them was being dropped one line later, because the little record kept
alongside each queued stream had room for the title, the artist, the album and the cover —
and no room for the duration.

It has room now, and that record is written to disk, so the durations survive restarting
the box rather than vanishing with the first reboot. Internet radio still shows `--:--`:
a live stream genuinely has no end, and pretending otherwise would be worse than admitting
it. Tracks already sitting in your queue from before the update keep showing `--:--` until
you queue them again — their length was never written down, so there is nothing to recover.

One thing came out of the tidying. The player's remaining-time display reads the same
record now, which it did not before. Had it been left alone, you could have seen the queue
give a track's length while the progress bar just above it showed none, for the same track,
at the same moment.

### Forms on a phone were paying for a protection they only half needed

Tap a text field on an iPhone and Safari zooms the page in. It does that whenever the field's text
is declared below a certain size, it does not zoom back out afterwards, and the button you were
reaching for ends up off the screen. It is a real problem and Audiogravi<sup>ty</sup> guarded
against it the obvious way: every field on a touch screen was raised to that size.

The guard worked. What nobody had weighed was its price. Every form in the interface — settings,
licence, profiles, configuration, the test panels — was drawn on a phone with its fields visibly
larger than the labels above them. A form reads as a sequence of pairs, a name and a value, and
the pairs no longer looked like pairs.

It turns out the two goals were never in conflict. What Safari inspects is the size a field
*declares*, not the size it is finally drawn at. Fields still declare exactly what Safari wants,
and are now drawn at the size the form was designed with. Confirmed on an actual iPhone rather
than reasoned about: a field declared large and drawn small takes focus without moving the page,
while the same field declared small zooms it a quarter larger.

The fallback is the part worth stating. On an iPhone older than iOS 16.4 the second half of that
is ignored and the field keeps its former, larger size — inelegant, and still perfectly safe. The
protection never rests on the new behaviour, only the appearance does.

### Five symbols and no words

The library is the part of Audiogravi<sup>ty</sup> people spend their time in, and on a phone its
five tabs had no names. Browse, Search, Queue, Library and Radio were five bare symbols, because
the rule that drew their names simply switched them off below a certain screen width — the very
screen the library is used from most.

The names are back, under the icons, everywhere. The interesting part is what it took to fit them,
because the bar had no room to give: the source you are browsing sat in it, and "LOCAL LIBRARY" in
bold capitals is a third of a phone's width. It has moved to the head of the content it describes,
which is where it belonged all along — it tells you what you are *looking at*, not where you can
go. The bar also stopped spending a sixth of the screen on margins inherited from a desktop
layout. Between the two, the five names fit with room to spare.

When they do not — a long source name, a smaller phone — the bar can be dragged sideways, and it
brings the selected tab back into view by itself whenever the tab changes, including when you
change it by swiping the page rather than by tapping.

One thing found on the way: on four screens, the tab shown as selected is not quite the screen you
are on — the outputs list shows Library, the artist and Roon and UPnP browsers all show Browse.
Tapping that tab is the obvious way back out, and it did nothing whatsoever. Nobody noticed while
the tab had no name on it.

### The last thing the installer prints is now a QR code

Audiogravi<sup>ty</sup> runs on a box on your own network, and the interface lives at a private
address on that network. That address cannot be shortened, published or looked up — it is
yours — which left one clumsy step at the very end of an otherwise unattended install: reading
an address off a screen and typing it, digit by digit, into the phone you are going to use the
interface from.

The installer now prints a QR code of that exact address, and under it the three steps that turn
the page into a proper app — fullscreen, its own icon on the home screen — on Android, on iPhone
and on the desktop. The certificate warning is explained at the point you actually meet it, right
under the code with the phone in your hand, rather than several screens earlier.

Two details decide whether something like this is a courtesy or a nuisance. It is drawn only when
a person is present: an upgrade, or the one-click update which runs detached with no terminal at
all, prints nothing and installs nothing extra on your box. And it gets out of the way rather than
misbehave — a narrower terminal gets a compact rendering, a very narrow one gets the address on its
own. What is printed can always be scanned, or nothing is printed.

### The address the installer prints is now one your phone can reach

The installer used to name the first of every address the machine holds, which sounds reasonable
until you look at what that list contains on a box running Docker, a VPN, a bridge, or simply
holding two network interfaces. The first entry can easily be an address that exists only inside
the machine. It was printed as the place to go, and the certificate was issued in its name.

It now asks the routing table which address a packet leaving the box would carry — the question
that was being asked all along. This mattered little when it produced a line of text somebody
would sanity-check; it matters entirely when it produces a QR code, where a wrong address is worse
than no address at all.

### Dropdown lists were never at risk in the first place

They had been held at that same enlarged size since the beginning, on the assumption that every
form control behaves like a text field. It was never checked, and it is not true: a dropdown opens
a picker wheel rather than a keyboard, and measured on an iPhone it does not zoom the page at any
size.

So the rule was buying nothing, and it was costing the lists their proportions. The clearest case
was the HQPlayer DSP card, where *Filter*, *Shaper* and *Mode* sit under labels deliberately set
small — the lists there were being drawn a third larger than the words naming them, which is what
made the card look wrong without it being obvious why.

Lists now keep the size their own screen gives them, on a phone exactly as on a desktop.

---

## 0.9.33 — 2026-08-09

### Nothing was telling the box that the music comes first

Audiogravi<sup>ty</sup> runs two things on the same machine: the player, and the core that
controls it. Until now the operating system had no reason to treat them differently. If the core
did something demanding — installing a package, or simply going wrong — it asked for processor,
memory and disk on exactly the same terms as the software decoding your music.

That is the wrong default for a listening machine, and it is invisible until the day it is not.

The core now runs with a declared, lower claim on the machine. Three things follow. Under
contention the player gets two thirds of the processor and the core one third — still several
times what the core needs, since at rest it uses about a tenth of one percent of a single core,
measured across three days of normal use. A burst of memory from the core is slowed down at a
threshold rather than being allowed to evict the player's own working data. And a runaway is
capped and restarted within seconds, which on a machine you are listening to is far better than
watching it grind itself into swap.

On an idle box none of this does anything at all — that is the point. These are not
optimisations, they are a statement of priority, and they only speak when something is competing
for the machine.

### Seven screens that needed the internet to appear

Configuration, Profiles, Performance, Systemd, Services, Audio software and the dashboard all rest
on one small library — a few hundred lines that let a screen read the application's shared state.
The interface fetched it from a public code distributor on the internet, every time it loaded.

There is a difference between a typeface that fails to arrive and code that fails to arrive. The
first is a matter of appearance. The second stops the page: a module the browser cannot fetch stops
the chain that depends on it, and those seven screens rendered nothing at all — no message, no
partial page. On a machine sitting on a network with no route out, or behind one that blocks that
distributor, that is what you got.

The library now ships with Audiogravi<sup>ty</sup>, folded into a file the interface already
downloads, so it costs not one extra request. It turned out to have been installed all along and
simply unused, and one screen was already loading it that way — which means the interface had been
carrying two copies of the same library, at two different versions, exchanging messages with each
other.

Three other libraries are still fetched that way: the code editor, the chart on the latency test,
and the terminal. Those three are asked for by name and checked before use, so when they do not
arrive the screen still appears — the editor becomes a plain text box, the chart does not draw.
They will follow, and they need more care: folding them in naively would make every start pay for
two screens most people never open.

### Not every screen wants to be dense

The licence administration and the page a customer uses to re-download a licence were sharing one
set of text sizes, and that was a mistake of category rather than of taste.

The administration is a working surface: rows of orders read against each other, consulted at
length by someone who knows it. Density is what makes that possible, and enlarging it would only
push content off the screen and separate the things being compared. The customer page is the
opposite — opened once, usually on a phone, by someone who has just reinstalled a machine and wants
a file. Nothing there is being compared, and nothing rewards density.

So the customer page now starts one step higher, and the administration keeps the size it was
designed at. Underneath both, the sizes those pages had accumulated — twenty-two of them, eight
falling within two pixels of each other, differences no eye can resolve — have become six
deliberate steps. That kind of drift has a mechanical cause worth naming: the page declared its
text at one size while the unit everything else was written in resolved against another, so every
value tuned by eye landed slightly beside the one before it.

The same treatment was given to the space between things, which had grown to twenty-one different
values — several of them a pixel apart, differences nobody decided and nobody sees one at a time,
but which together make a page read as restless. Seven remain. Where a value had to move it moved
outward, never inward: a layout should not quietly tighten because someone tidied it.

Two faults were found in the doing, both of the sort that are invisible until someone is affected.
Tapping a field on the customer page zoomed an iPhone in and never back out — the stylesheet had
guarded against exactly that, but six fields carried their size on the element itself, which
overrides a stylesheet, so the guard was present and inert. And the preview of an email campaign
showed its unsubscribe footer larger than the message that actually goes out, because the preview
is drawn in a frame that does not load the interface's stylesheet. A preview exists to decide
whether to send.

### The page that fetches your licence had a dependency you never agreed to

If you reinstall your machine, you come to a page on the licence server to download your licence
file again. That page was built on code — and set in a typeface — fetched from a public code
distributor elsewhere on the internet, every time it opened.

That arrangement is invisible while it works. When it does not — an outage at that distributor, a
corporate network that blocks it, a connection that simply cannot reach it — a missing typeface
would have been a cosmetic matter. Missing code is not: the page renders nothing at all. Blank,
with no message, precisely when someone needs it most.

Everything that page needs now comes from the licence server itself. It is sixteen kilobytes; the
argument for keeping it elsewhere was never strong, and the cost of the arrangement fell entirely
on whoever happened to open the page on a bad day. The administration console gained the same
independence, and rather more from it: code fetched from a third party there was running with full
access to a page that holds licence keys and customer addresses.

While in those pages, two things that had been true since they were written were put right. Their
light theme had never been given colours of its own, so it borrowed those drawn for a black
background — a green status, an amber warning, a red refusal, all barely distinguishable from white
paper. And they were set in whatever typeface the machine happened to provide, so the page a
customer sees looked like a different product on every computer. They now use Inter and JetBrains
Mono, like the rest of Audiogravi<sup>ty</sup>, served from the same place as everything else.

### The message you most need to read was the hardest one to read

When a password is refused, the sentence explaining it was set in red on a pale red ground.
That is the conventional way to write an error and one of the least legible: on the sign-in
screen it fell below the contrast the text of an interface owes its reader — fine on a good
monitor, gone on a laptop outdoors. The alert keeps its red border and tinted ground, because
that is what makes it read as an alarm at a glance; the sentence inside it is now plain dark
text. The icon beside it carries the same meaning for anyone who does not see the colour.

The same was true, more quietly, of the greys around it — the line under the logo, the version
at the foot of the page, the placeholder in each field. They are darker now. A failed passkey
attempt is shown in the same alert as any other failure, instead of a line of small red text
that resembled nothing else on the page.

Two faults behind this were of a kind that cannot be seen by looking. Several colours and
sizes were asking for values defined nowhere in the interface, so a stylesheet that read
correctly did not behave correctly — and one of them left the spinner on the sign-in button
drawn in white, on a white button, in dark mode: the button simply appeared to do nothing
while it worked.

The panel shown when a list of albums or stations fails to load is the same component, so it
is fixed with it: readable text on the same red-bordered ground, and a red each theme now
states for itself instead of inheriting another theme's.

### The white flash before the dark screen

Opening Audiogravi<sup>ty</sup> on the dark theme began with a full-brightness white screen. Not
long — the time it takes to fetch and parse the interface's code — but long enough to be the first
thing you saw, and on a device most people use in a dimly lit room it is the worst possible first
thing.

The cause was ordinary: the theme and the dark mode were applied by that code, so until it ran
there was nothing to apply them. The browser's own bar had the same problem in a simpler form — it
had been given one fixed colour, belonging to one theme, shown to everyone. And the sign-in screen
always appeared in the default theme before switching to yours a moment later.

The appearance is now read and applied before anything is drawn at all, so the first thing on
screen is already the one you chose. It survives a reload with no network, too.

### Audiogravi<sup>ty</sup> was wearing someone else's typeface

The interface was set in whatever font the device happened to ship — one typeface on a Mac,
another on a PC, another again on an Android phone. Nobody had chosen that, and it was not for
want of a typeface: Inter was being downloaded from Google's servers on every single page load,
and then thrown away. The default theme substituted the operating system's font for it, so the
only people who ever saw Inter were those who had gone into the settings and picked another
theme.

That download was not free. It is a request to a third party on the critical path of the first
screen, a visitor's address handed to that third party, and a wait before anything can be drawn.
On a device sitting on a network with no route to the internet — which is where a music streamer
often sits — it is simply a typeface that never arrives.

Inter now ships with Audiogravi<sup>ty</sup> and is served by the installation itself, on every
screen including sign-in. Nothing is requested from the internet to draw the interface, no address
goes to anyone, and a box with no connection shows exactly what a connected one shows. It is
stored with the rest of the interface, so it is there from the first visit, offline included. The
default theme wears it like the others.

The second typeface changed too. Everything read digit by digit — frequencies, temperatures,
identifiers, addresses, the terminal — was set in Courier New, a typewriter face from the 1950s
and the one thing on the interface that looked its age. It is now JetBrains Mono, drawn for
screens and for exactly this job: its figures share a width, so a value refreshing in place no
longer shifts the layout under the eye.

Both licences are served alongside the fonts, as those licences require.

### A theme can carry its own typeface

Themes are the part of Audiogravi<sup>ty</sup> open to contribution, and this is the first release
where a theme is genuinely self-contained. One of the three was quietly acting as the palette every
other theme inherited from, so changing a colour in it changed screens under the other two; and a
theme that declared a typeface was obeyed everywhere except the sign-in screen, which pinned its
own regardless.

Both are gone. A theme now states what it wants — colours, typeface — and the whole interface
follows it, with nothing outside the theme able to overrule it on one screen and not the next.
Nothing changes in what any of the three existing themes looks like; what changes is that the next
one will behave.

### A red frame around a station nobody was deleting

On an iPhone, swiping one of the radio screens sideways left a red outline drawn around the
station under the finger — and it stayed drawn, including while another station was being
chosen. Red, on a screen where red means "remove", is not a detail: it reads as though
something is about to be deleted.

Two things caused it, and both are gone. The red panel that a swipe uncovers to offer
**Remove** was in fact painted beneath every row all the time, simply covered up; and a row
that had been touched once kept the small displacement the gesture gave it, forever. On iOS
that combination is enough for a sliver of the red to show around the row's edges. The panel
now exists only while a row is really being dragged left, and a row goes back to being an
ordinary row the moment the finger lifts.

The gesture is shared by four lists — radio stations, UPnP servers, renderers and the
playback queue — so all four are fixed at once, along with three faults found in the same
place: dragging one row and then merely tapping another used to leave the first one stuck,
a drag to the right (or the sideways drift of a normal scroll) uncovered the red under a row
that had not moved, and a removed row handed its red panel to whichever row slid up to take
its place.

### The licence panel says things once

A trial announced how many days were left three times over — on the badge, in a sentence and
under the progress bar — and one of those was assembled from a template, so it read
"27 day(s) remaining". The price was given twice on the way to paying. The badge and the bar
keep the count, the offer keeps the price, and the panel is two lines shorter.

One correction travels with it. Last release removed the repeated price, and removed it from a
piece of text used in two places rather than one: a box whose trial had ended was then asked
to buy a licence without ever being shown what it costs, and the help screen lost its only
figure too. Both state the price again.

### The System tab shows the core's logs again

The log panel on the System tab had been empty for some time, and nothing said why. It was
asking the system journal for a service under a name that no longer exists. A journal asked
for a service it does not know does not report an error — it answers with an empty log — so
the panel looked as though there was simply nothing to show. It now asks for the service that
is running, and the logs are back.

Alongside it, the interface has stopped calling the core "the backend". The System tab's
button now reads **Restart Core**, and so do the confirmation, the notice that follows it, the
title above the logs and the connection indicator. The site, the manual and the documentation
have said "core" all along; the interface was the last place using a second word for the same
thing.

---

## 0.9.32 — 2026-08-06

### Licences bought for a period now say so

Audiogravi<sup>ty</sup> can issue a licence that runs for a fixed period rather than for ever.
None had been issued yet, and it is as well: the whole path told the customer the wrong
thing, twice.

While the licence ran, the panel announced *"Lifetime license active"* and showed the end
date nowhere at all — so someone who had bought a year believed he had bought the software
outright. On the day it ended, that same panel told him his licence file was *"invalid or
bound to a different device"*. Read plainly, that says corrupted or stolen. It is the sort of
message that costs a support exchange, and an apology.

The panel now names the end date for as long as the licence runs. On the day it ends it says
what happened — the licence ended on that date, and Audiogravi<sup>ty</sup> keeps running in
Starter Edition — and offers to renew, with the order number still on screen where it is
needed. A licence bought for a period is also no longer called a trial, which is the word
three different screens were using, one of them right after payment.

Two things behind the scenes go with it. A mistyped end date is refused the moment it is
entered, instead of being discovered months later by the customer whose box stops accepting
his licence. And both ends now settle expiry in UTC: a box in New Zealand and the server in
Europe used to disagree, for about thirteen hours a day, on whether a licence had run out.

### The manual is now part of the site

Until now, every link to the documentation left audiogravity.app for GitHub. That is a fine
place for source code and a poor one for a manual: raw files, a developer's interface, and our
own documentation earning its search results for someone else.

The twelve chapters are now pages of this site, with the chapters listed alongside, working
links between them, and the same typography and light or dark theme as the rest. There is a
**Manual** entry in the top bar.

Nothing was rewritten: the pages are built from the same text the manual inside
Audiogravi<sup>ty</sup> displays, and rebuilt automatically whenever a chapter is edited — so
what you read on the site and what you read in the app cannot drift apart.

### The manual reads on a phone

The user manual opens inside Audiogravi<sup>ty</sup> itself, and any chapter with a
screenshot used to push the reader off to one side — you had to drag it back to carry on
reading. The screenshots are phone captures at their own size, and nothing was stopping
them from being wider than the screen you were reading on. An iPhone 13 happened to be
wide enough; anything narrower was not.

Screenshots now fit whatever they are read on. Wide tables scroll on their own instead of
taking the page with them, and a long command written in the middle of a sentence no longer
holds the text open. Checked chapter by chapter, from the smallest iPhone up.

### This page works on a phone

Most people meet Audiogravi<sup>ty</sup> here first, and until now that page had to be
dragged sideways on every iPhone made: it wanted 470 pixels and the narrowest current
model offers 375. Several things held it open at once — a button kept beside the logo long
after the menu had been hidden, a comparison table with a fixed label column that left the
text beside it under a hundred pixels to wrap in, and the title itself, one unbreakable
word set wider than the smallest screen.

All of it now fits, on six screen sizes in both light and dark, portrait and landscape. The
comparison table gained about a fifth more room for its content, keeps the capability name
pinned on the left while you swipe through the products, and stops each swipe on a whole
column instead of halfway through one. Added to a home screen the page runs full-screen and
keeps clear of the notch and the home indicator.

Every icon on the page is now a drawn shape from the same set the interface uses. The ticks
in the comparison table were plain text characters, which meant each visitor's own machine
chose how to draw them — a different shape and weight on a Mac, an iPhone, a PC or an
Android device, in the column where we invite you to compare.

---

## 0.9.31 — 2026-08-04

### Getting your licence back after a reinstall

Audiogravi<sup>ty</sup> offers two buttons that open the licence portal: "Download .lic",
to fetch your licence file again, and the v1 → v2 upgrade. Neither had ever actually
opened — the page they point to was not published, so both ended on a redirect to an
unrelated site. Reinstalling a box meant asking us for the file by hand.

The portal now opens as intended. Only that page and what it needs is public; the
administration side remains closed.

The same fix repairs the unsubscribe link at the bottom of our emails, which arrived
without the values identifying your order and reported them as missing.

### The licence pages work on a phone

Now that the portal opens, it had to be usable where you are most likely to open it — from
the link in an email, on a phone. The pages were laid out for a desktop window: fields
rendered as white rectangles on a black page, tapping one zoomed the page in and never back
out, and nothing was reserved for the notch or the home indicator.

Both the portal and the administration side were rebuilt to fit, and checked across screen
sizes from the smallest iPhone to a tablet.

---

## 0.9.30 — 2026-08-03

### The free trial is kept in one place

The trial start date used to be mirrored to a second, system-level file. That copy never
worked on an installed box — nothing ever created it with the right ownership — and where
an old one happened to linger, the two dates disagreed and the app logged a licence error
every few seconds.

There is now a single record, and the licence server remains the authority: it remembers
the date a box genuinely started its trial and restores it, so a trial reflects real first
use. Upgrading removes the obsolete file; nothing is asked of you.

---

## 0.9.29 — 2026-08-03

### Announcements and updates now reach every box

In-app announcements and "a new version is available" notices are broadcast from the
licence server. Until now they only reached a box with a currently-valid licence: a box
on its free trial — which never presents a licence — and a box whose licence has expired
were both left out, so they could stay on an old version without ever being told a newer
one exists.

Both now travel over the public channel every box already checks, so a trial or expired
box is notified just like a licensed one. The update notice is bounded to the box's own
major version, so it is only ever offered a newer release it can run — moving to a new
major stays a deliberate upgrade, never an automatic one.

---

## 0.9.28 — 2026-08-03

### A longer trial is now a switch, not a release

The free trial was fixed at 30 days, baked into the app — changing it meant building and
shipping a new version. It is now a length the licence server can raise on its own: set a
number in the admin, and every box picks it up at its next check-in and runs the longer
trial, with the licence panel counting down against the real total.

It stays tamper-proof. The server signs the value with the same key it uses for licence
files, and the box refuses anything not genuinely signed by the server, or that tries to
shorten the trial below the built-in floor — so a box owner cannot lengthen their own
trial, and a box that never reaches the server simply keeps the built-in length.

---

## 0.9.27 — 2026-08-02

### A network blip no longer looks like a licence problem

The box checks in with the licence service now and then to confirm everything is in
order. When that check could not get through — a brief network drop, the service busy
for a moment — the box treated the silence as a verdict and showed the licence as
*invalid*, greyed out and alarming, until the next check hours later. Nothing was
actually wrong.

It now tells the two apart: a reply it can read is honoured, and anything else reads as
"could not reach the service right now" — the last known-good state stays and the box
keeps playing. Behind the scenes the licence service also moved to its own address and
had its plumbing tightened; none of it asks anything of you.

---

## 0.9.26 — 2026-08-01

### The button you could not reach

Installing an update from a phone asks for your password. On an iPhone, tapping that
field zoomed the page in, and the dialog's Confirm button ended up somewhere off the
right edge of the screen. The update could not be validated at all — the only way
through was to pinch the page back out, if you thought of it.

Safari zooms in on any field whose text is smaller than 16 pixels. Audiogravi<sup>ty</sup>
has carried a rule against exactly this since 0.9.20, but that one field described its own
size directly on the element, where no rule can reach it. The same protection turned out
to be tied to narrow screens rather than to touch ones, so it also stopped applying on
every iPad, and on any iPhone held sideways. Both are fixed.

### Editing a radio station without fighting for it

The pencil that opens a station's settings was, in the reporter's words, practically
impossible to click — and there were two separate reasons, not one. It was drawn smaller
than the two icons beside it and, with compact mode on, its target measured 24 pixels
across. And the gesture that removes a station armed after 8 pixels of sideways travel
anywhere on the row, buttons included, so a thumb that drifted while aiming started
removing the station instead.

The three icons are now the same size, the buttons are half again as tall as they are
wide — height costs nothing on a row that is already 60 pixels deep, while width would
have pushed the icons visibly apart — and a gesture that begins on a button belongs to
that button. That last part applies to every list you can swipe: stations, the queue,
UPnP servers and renderers.

### Radio search, and being a good neighbour

Radio search stopped working twice in one day. Neither time was a fault in
Audiogravi<sup>ty</sup>: the catalogue it queries, the community-run Radio Browser, was
answering that it had no server available. What the episode exposed was how badly
Audiogravi<sup>ty</sup> behaved around it.

It believed it had five mirror servers. It has one — three of those names no longer
resolve, the other two point at the same machine, and the catalogue itself advertises a
single server. So every failed search fired four requests at the one machine that had just
refused, in a third of a second, while the interface sent a fresh search for almost every
letter typed. Audiogravi<sup>ty</sup> now sends one request, asks again only when the first
got no answer at all, waits longer before searching as you type, and goes silent for as
long as the catalogue asks if it ever says it is being queried too often.

Two things also changed for you rather than for the catalogue. A search you have already
run keeps showing its results while the catalogue is unreachable, instead of an error —
and those stations still play, which took a second fix: they were listed, but starting one
asked the catalogue again and came back with "station not found" for a station right there
on screen. And when something does fail, the message says whether the problem is at the
provider or on your box — the previous "Search failed" was the same three words for both,
which sent people hunting through their own settings for an outage happening elsewhere.
That now holds wherever the catalogue is involved, not only in search: starring a station
and adding one to My Live Radio used to answer "Could not update" for every cause alike,
and a station that would not start pointed at the local player by name — while the local
player was working, and the catalogue was the thing that had not answered.

Waiting longer before searching had one consequence worth naming, because it was found in
review rather than in use. A search still on its way could arrive after you had left the
Search tab and replace what the tab you had opened was showing — your saved stations
swapped for hits on what you had typed, under the wrong heading, and swipeable, so a swipe
asked the box to remove a station that list never held. Leaving Search now abandons the
search with it.

Finally, Audiogravi<sup>ty</sup> now does what the catalogue asks of the software that uses
it: report which stations get played. That count is what makes the popularity ranking —
the ranking Audiogravi<sup>ty</sup> sorts your search results by, and had been taking
without giving anything back. Only catalogue stations are reported, never the ones you
enter yourself, and never a play that failed to start. It does mean a station identifier
leaves your box, so it can be switched off: `RADIO_REPORT_PLAYS=false`.

### The self-update safety net, made real

Audiogravi<sup>ty</sup> can update itself, and an update that fails is supposed to undo
itself and leave the box exactly as it was. Tested on real hardware — by deliberately
breaking an update — it did not. The undo restored the core program and nothing else,
then wrote *previous version restored* in its log. Everything else an update rewrites was
left as the failed version: the service definition, the package registry, the privileged
helpers — and the update mechanism itself. A bad update could leave a box that could no
longer update, while its own log said all was well.

The undo now restores everything the update overwrote — measured, nine files — reloads
the service definition, and tells the truth: if any part cannot be put back, it says so
rather than claiming success. And after undoing a failed update, the box can update again,
which is the whole point.

Fixing this surfaced a second, sharper problem in the same machinery. The privileged
helper that carries out an update runs with administrator rights, and it used to take the
address it downloaded-and-ran, and the path it wrote, from whoever asked. Anything already
running under Audiogravi<sup>ty</sup>'s own limited account could hand it a malicious
address and have it run as administrator — a local escalation to full control of the box.
The helper now owns those values and refuses to take them from its caller; it accepts only
a checked list of the rest. Proven on real hardware: an injected address is dropped and
never runs.

Neither is reachable from the network, and neither changes anything you see. They are the
kind of thing that has to be right before a box is trusted to update itself unattended.

### The API key leaves the Settings panel

The Settings panel offered your box's API key in a field, behind a reveal button, to
anyone logged in. It looked like a secret being guarded. It was not: the key is already
inside the page your browser downloads — the installer writes it there, because the
interface needs it to talk to your box at all. Hiding it behind a padlock protected
nothing that was not already in plain view.

What the field could do was break things. It was the only thing on a running box able to
store a key in your browser, and a browser that had stored a wrong one stayed cut off from
your music for good: the value kept locally outranked the one your box publishes, so every
upgrade republished the right key and lost, silently. The field was, in other words, the
sole cause of the problem it existed to repair.

It is gone, and the key your box publishes is now the one that wins. A leftover copy from
before is discarded on the way. Nothing replaces the field — there was nothing left to type
into it.

### Removing it means removing it

Uninstalling is meant to give you your machine back. It nearly did.

Performance tuning installs a small service that re-applies your chosen CPU governor at
every boot. The uninstaller removed the programs, the services, the privileged rules and
the system account — but not that one. So a machine you had removed
Audiogravi<sup>ty</sup> from kept having its processor scheduling changed at every start,
by a service that no longer had anything on the machine to explain it. It is now removed
with the rest.

`--purge`, which is meant to leave nothing at all, also kept the backups of your audio
services' configuration files — copies that can hold your MPD password or your Shairport
authentication keys. Those go too now.

And the manual has been rewritten on this point, because it was the real problem: it gave
two commands and stopped there. Following it to the letter, you would believe the machine
was clean while your entire configuration was still sitting in `/etc/audiogravity`. It now
says what each form removes, what it keeps and why, how to remove everything — and what is
deliberately never touched: the audio software you installed from the Audio Software page
is made of ordinary system packages that go on working without Audiogravi<sup>ty</sup>, so
removing them stays your decision.

---

## 0.9.25 — 2026-07-28

### A window that stops lying to you

Installing or removing an audio service opens a window that shows the work as it happens.
It had a habit of freezing: the progress bar stayed where it was, the last line stayed on
screen, and nothing else ever came. People waited, then cancelled, then tried again — on a
box where the work had in fact finished long before.

On a real machine the numbers were plain: the package was installed in **six seconds**, and
six minutes later the window was still announcing an installation in progress.

The cause was that those log lines only existed in flight. Audiogravi<sup>ty</sup> sent each
one to the browser at the moment it appeared, and kept nothing for a browser that was not
listening. A reconnection, a phone that had put the page to sleep, a second of poor Wi-Fi —
and the missing lines were gone for good. The window had no way of finding out, and no way of
asking. So it stayed on the last thing it had heard.

Two things changed. Audiogravi<sup>ty</sup> now keeps the log of the operation under way, and
the interface claims what it missed — when the connection comes back, and each time the
operation moves on. And the log no longer arrives all at once at the very end: lines appear as
the package manager produces them. That second part matters more than it sounds, because until
now a perfectly healthy installation and a dead one looked **identical** for as long as they
lasted.

### Red means something again

Removing AirPlay used to finish on a red error: `rmdir: failed to remove
'/var/lib/shairport-sync'`. The removal had worked. That line comes from the shairport-sync
package itself, which prints it on purpose and ignores it — the directory is an old leftover
and is usually not there at all.

Audiogravi<sup>ty</sup> was deciding how serious a line was by looking at its wording, so
anything containing the word "failed" was shown as an error, whoever had written it and
whatever they meant by it. What the package manager prints is now shown as plain information.
Whether an operation succeeded is decided by its result, not by the vocabulary of a third
party — so a red line is once again worth reading.

---

## 0.9.24 — 2026-07-28

### One less thing to get right

Every audio service keeps its settings in a file, and Audiogravi<sup>ty</sup> lets you edit
it from the Config tab. Where that file sits is not up to us: `/etc` when the service came
from the distribution's packages, `/usr/local/etc` when it was compiled from source. The same
service, two places, depending on the machine.

That location used to be written down in the box's own configuration file — which can only
name one of the two. So the value shipped with Audiogravi<sup>ty</sup> was, by construction,
wrong on the other kind of machine. Every ARM box had the wrong path for AirPlay, and always
had.

Nothing appeared broken, because the Config tab was tolerant: it looked in both places and
opened the right file anyway. But the configuration check was not, and reported the file as
missing — on the very machine that was editing it a moment earlier. Two parts of the software
looking at the same line and disagreeing about it.

Audiogravi<sup>ty</sup> now works it out on its own, and both parts ask the same question of
the same source. The line in your configuration file is ignored; new installations no longer
carry one at all. If yours has one, it does nothing and can stay.

The same reasoning settled a second question. How a settings file is read — its format — was
being guessed from its name, which worked until a file was named unexpectedly. It now follows
from which service the file belongs to, which is something the software knows rather than
infers.

---

## 0.9.23 — 2026-07-28

### A first install that no longer depends on what the machine already had

Setting up a new box is meant to be one command. Three things quietly undermined that,
and each of them reported success or said nothing at all.

The command checked that Python was installed and stopped if it was not — even though
the installer it was about to download would have installed Python itself. That
installer never got the chance: the check came first. So the one thing that could have
repaired the machine sat inside a package the command refused to fetch.

The second was subtler, because nothing appeared to go wrong. Every box generates its
own keys for push notifications when it is first set up, and that needs one cryptography
library. Audiogravi<sup>ty</sup> fetched it with `pip` — a tool that is simply not
installed on a stock ARM machine. There, the step failed and moved on, and notifications
worked only on boxes that happened to already carry the library for some other reason.

The third was the one that would have been hardest to diagnose. The interface is served
over HTTPS, which needs a certificate, which the installer creates with a tool Debian
does not promise is installed. When it was absent, the installation stopped the instant
it tried — and the error was thrown away, so the screen showed the line announcing the
certificate and then nothing. No message, no reason, no obvious next step.

Underneath all three sat the same habit: the installer decided whether a step had worked
by asking the package manager, rather than by looking at the machine. When it could not
even refresh its package lists, it skipped the installation and announced "System
dependencies installed" anyway — a box could finish setup, with a clean-looking log,
missing every one of those tools.

All three are now handled the same way as everything else the box needs: through the
system's own package manager, on both architectures, and only when the box will actually
use them — an installation behind a reverse proxy is never made to fetch a certificate
tool it will never run. And success is now judged by what is on the machine at the end,
not by what a command reported along the way. Anything still missing is named, with the
feature it takes with it. Where a step cannot complete, it says so.

On machines where `pip` did exist, this also stops Audiogravi<sup>ty</sup> from writing
into the system's Python installation and hiding the version the operating system had
put there — something Debian goes out of its way to prevent, and which had no business
happening on a machine whose job is to play music without interference.

Nothing changes on a box that is already running.

---

## 0.9.22 — 2026-07-27

### A start that no longer waits on your queue

The list of tracks waiting to play shows a small cover beside each one. That list sits in
the Library tab, which is built into the page from the very first moment — even when you
are looking at something else entirely. A hidden image is still fetched, so every cover in
that list was downloaded before you had touched anything.

With sixty-seven tracks queued, that meant sixty-seven requests to the box for the same
album cover, sixty-seven times over — half of everything the app asked for while starting.
And the cost grew with the queue: a few hundred tracks waiting meant a few hundred
requests, on a phone, over Wi-Fi, at the exact moment the app was trying to become usable.

Covers are now fetched only when they are about to come into view. The screen is
identical; the app simply asks for half as much in order to show it.

### A screen you can leave open

The Pipeline tab on a phone shows what is playing and the whole chain the sound travels
through. Watching it was not free: every five seconds it asked the box to work out the
entire pipeline again and send it back. That calculation takes around half a second of
the machine's attention, so a tab left open on a phone on the side quietly consumed close
to seven minutes of processor time every hour — on the machine whose only job is to play
your music without a hitch.

None of that work was needed. Audiogravi<sup>ty</sup> already notices when the pipeline
changes and says so. The tab now listens for that instead of asking again and again: it
reads the state once when you open it, and is told the moment anything moves. Left open,
it costs nothing.

The screen itself is unchanged. The one visible difference is the small dot beside each
active source, which now pulses by fading rather than by shrinking — the same signal,
drawn in a way that does not tie up a phone's graphics for as long as the tab is open.

### Fewer tracks that fail halfway

When HQPlayer is your output and a track is in a format it cannot read,
Audiogravi<sup>ty</sup> refuses it straight away and names the format. That has been true
for a while — but only for the formats it had been told about, one at a time. Anything
else went through, HQPlayer took it, and playback failed a moment later with an error
pointing at your sound card instead of your file.

The refusal list has been checked against Signalyst's own list of what HQPlayer accepts.
Twelve more formats are now caught before anything is sent: concert rips in AC3 or DTS,
older lossless collections in Musepack, TAK, TTA or Shorten, Matroska files, and the
compressed flavour of AIFF.

Nothing you can actually play was added to that list. The ten formats HQPlayer accepts —
and the M3U, M3U8 and PLS playlists it reads — are held in place by tests, because
refusing a track that would have played is worse than letting one fail late.

---

## 0.9.21 — 2026-07-26

### A track that cannot play says so before trying

If you browse your music through a media server and send it to HQPlayer, you may have met
a puzzling failure: nothing plays, and Audiogravi<sup>ty</sup> blames the sound card.

The cause was a naming difference between servers. M4A files — most lossless libraries are
full of them — are refused up front, because HQPlayer cannot decode them: you get an
immediate message telling you to switch HQPlayer off for this track. But Plex publishes
those very same files under another name, `.mp4`, and that spelling was missing from the
list. So the track went through, HQPlayer took it, and failed a moment later — with an
error pointing at the wrong culprit.

The same file, refused from one server and pushed from the other. Both now give the same
answer, immediately and for the right reason. Those tracks also used to show a blank
format in the player; they now name their codec.

### The player comes back on the first try

The small tab at the bottom of the screen — the one that brings the Now Playing bar
back once you have pushed it away — ignored about one touch in two. You pressed, and
nothing happened, so you pressed again.

Two causes, both now fixed. The tab reacted to a short tap or to a long upward swipe,
but to nothing in between — and "in between" is precisely what a finger does when it
slides a couple of millimetres on the way down. And the tab was smaller than any touch
target should be: barely a third of the height Apple and Google both recommend.

It looks exactly the same. What changed is invisible: the area that listens for your
finger now extends above the visible tab, where touches actually land, and anything
that is not a deliberate downward drag brings the player back.

---

## 0.9.20 — 2026-07-25

### Setting your machine up is no longer a paid feature

Editing a service's configuration file, and the guided setup that generates the
whole audio stack in a few clicks, were both reserved for Trial and Pro. A
Starter user could run the box, monitor it, switch profiles — but not configure
it. That line was in the wrong place: configuring the machine is part of owning
it, not part of paying for it.

Both are now open, and the **Config** tab is no longer greyed out in Starter.
The guided setup stays **administrator-only** — it rewrites every service's
configuration and mounts network shares, so it is gated on who you are, not on
what you paid.

What Pro still unlocks is unchanged: the player controls, the library, internet
radio, the HQPlayer DSP remote, the pipeline view, systemd tuning, performance
optimisation, DSD protection and the sleep timer.

### A play that makes no sound now tells you — without making you wait for it

Sending music to HQPlayer and getting silence is the failure this release keeps
chasing. Audiogravi<sup>ty</sup> already checked that playback had really started; the
problem was **when** it checked, and **what it accepted as proof**.

It checked while your click waited — up to twelve seconds before you got an
answer — and it gave up too early. Measured here: a DSD128 track upsampled to DSD
starts **twenty-eight seconds** after being sent, and HQPlayer stops answering
altogether while it warms up. A perfectly good album was announced as failed
fifteen seconds before the first note.

The check now runs behind you. Playback starts immediately, and if nothing comes
out, the reason appears under the output — the same line that already tells you
the sound card is held by another player. The message lifts on its own as soon as
the music really plays, whichever way you restarted it.

And the proof changed. Audiogravi<sup>ty</sup> no longer takes HQPlayer's word for it: it
watches the **position advance**. With the sound card held elsewhere, HQPlayer
reports "playing" with its position frozen at zero for as long as you leave it —
nine seconds of that were being read as a success. A position that moves is sound
coming out; nothing else is.

The trade is deliberate: a play that genuinely never starts now takes longer to be
declared failed, because "stopped" is also what a heavy chain reports while it
warms up. Only time tells the two apart, and crying wolf on working music is the
worse mistake.

### A format HQPlayer can't play is now refused up front — from every source

HQPlayer does not decode ALAC, AAC, OGG/Opus, WMA or APE. Until now only internet
radio checked, because that is where the problem was first met. But the limit has
nothing to do with radio: an ALAC album sitting in your own library failed exactly
the same way — HQPlayer accepted the request, then never started, and several
seconds later Audiogravi<sup>ty</sup> blamed the sound card. The wrong culprit, after a wait.

The check now sits on the single path every source goes through, so it holds for
your library, your media server and radio alike. The answer is immediate and names
the format, and an album is checked before anything is sent — one unplayable track
is caught up front rather than stopping the music halfway through. Formats
Audiogravi<sup>ty</sup> cannot identify are still attempted: only what HQPlayer is documented
not to handle is refused.

An album is treated as a whole, deliberately. A record where a single bonus track is
ALAC is refused entirely rather than played without it: an album missing a track you
never noticed was dropped is a worse answer than a clear refusal naming the track.

One case remains unguarded, deliberately: some media servers publish tracks at
addresses that reveal nothing about the format. There, Audiogravi<sup>ty</sup> has nothing to
go on and lets the attempt through rather than refusing on a guess.

---

## 0.9.19 — 2026-07-20

### HQPlayer takes its true place: a processor in your chain

HQPlayer no longer masquerades as a music source. When Audiogravi<sup>ty</sup> streams
your library through it, the player shows **Library** as the source and the
signal path tells the real story — Library → HQPlayer → NAA streamer → your
DAC. If you drive HQPlayer from its own remote instead, Audiogravi<sup>ty</sup> shows an
**External** playback with the live sample rate and DSD/PCM mode (HQPlayer's
API doesn't reveal the track title in that case). Play/pause, volume and the
DSD safeguards all keep working exactly as before.

### Silence now comes with an explanation

Your sound card is exclusive on purpose — that is what makes bit-perfect
playback possible — so only one player can hold it at a time. Until now, if you
pressed play while another player still had it, nothing happened and nothing
said why. Audiogravi<sup>ty</sup> now tells you on the spot with a notification: *"Output
in use by another player — stop it to play here"*. The fullscreen player shows
the same message under the output, with the engine's exact wording available as
a tooltip if you want the technical detail. The message always describes what
you are trying to play right now, and appears once when the problem starts
rather than repeating while it lasts.

The same goes for a refused playback. Audiogravi<sup>ty</sup> always knew why a track
would not start — an unreachable server, an expired stream, a source that
cannot reach the output you selected — but the places you start playback from
kept that reason to themselves, so the tap simply appeared to do nothing. They
now tell you, in plain words. Playback that works stays quiet: the music is the
confirmation.

### The renderer is now an output — casts show their true source

Sending music to a network renderer used to make the renderer itself appear as
the "source" in the player. That never matched reality: the music comes *from*
Qobuz or your library and *plays on* the renderer. The player now says exactly
that — the now-playing card is badged with the real origin (**Qobuz**,
**Library**, your UPnP server's name, or **External** when another app drives
the renderer), and the renderer appears where it belongs: as the **output**
("→ renderer name" badge and the output bar). Play/pause, next, seek and volume
keep working exactly as before — commands are always routed to the device that
actually plays the music. When the renderer is your selected output but nothing
is playing, it still stays on screen as the selected output. (This refines the
0.9.18 "renderer as a source" presentation into the final model.)

---

## 0.9.18 — 2026-07-19

### Casting to a network renderer, done right

Sending audio to a network renderer — a Marantz or Linn streamer, another
Audiogravi<sup>ty</sup> box, any UPnP device — now feels like playing to any local output.
The renderer shows up as a full **now-playing** entry in both the mini-player and
the fullscreen player: cover art, track info, the source badge, the signal path,
and transport controls that actually work. When the renderer is your selected
output but nothing is playing, it stays on screen as **Stopped** (named after the
renderer) instead of the player going blank.

Under the hood this fixed two long-standing problems with renderer playback.
**Play/pause now works**: it was silently doing nothing on many renderers because
of an unreliable internal check — Audiogravi<sup>ty</sup> now sends the pause/play command
straight to the device. And **the renderer's state now updates live** (play,
pause, track, position) within about a second, instead of lagging up to a minute:
the device's own status events were being rejected before they ever reached
Audiogravi<sup>ty</sup>, so it had been falling back on slow polling. The player's output
name and signal path now correctly show the renderer, and casting a DSD file to a
network amplifier no longer forces its volume to full.

### Streaming reliability pass

A round of fixes makes the streaming services steadier without changing how they
look. **Tidal** stops showing a misleading "client credentials rotated" message
(and quietly hammering the login endpoint) when a session simply expires — it
now recognises the expired session and asks you to reconnect cleanly. **Qobuz**
sign-in no longer ends up "half-connected" — reported as connected while playback
silently fails — when the last step can't complete, and if the sign-in can't
reach Qobuz you get a clear error page instead of a raw *Internal Server Error*
in the pop-up. **Hi-Res only** radio search returns a full page of stations again
instead of collapsing to a handful, and adding radio favourites no longer stalls
behind a slow catalogue lookup.

A second review pass covered the playback engines: **Qobuz** browsing now
recovers on its own when your session has simply expired (it re-signs in and
retries) instead of telling you the app credentials rotated; **HQPlayer** keeps
the album on the now-playing card for a single track and no longer chokes on an
odd status value; and network-renderer control is a touch more robust around
reconnects.

A third pass covered playback and notifications: DSD tracks can no longer get
stuck at full volume if a volume adjustment hiccups at the start of playback
(your level is restored when DSD ends), and push notifications are more reliable
— a valid device is no longer dropped over a transient error, and the stored
subscriptions file is written privately.

Finally, a system-internals pass: changing the CPU governor no longer briefly
stalls the audio pipeline, a self-update that can't start is reported as failed
right away instead of appearing to hang, and the critical-temperature alert is
guaranteed to be sent.

Security hardening: installing an audio engine now only ever downloads over
HTTPS, with a size cap and timeouts, so the install step can't be tampered with
in transit or made to hang or fill the disk. The album-art proxy can no longer
be pointed at internal addresses, passkey sign-in no longer reveals which
usernames exist, and the config backups it keeps are capped instead of growing
forever. The service-tuning panel now strictly validates every value it writes
to systemd (closing a way to run code as root) and only ever touches
Audiogravi<sup>ty</sup>'s own services, never system units like SSH or networking.

---

## 0.9.17 — 2026-07-18

### Add a NAS to your library without touching a terminal

Pointing Audiogravi<sup>ty</sup> at music on a network drive used to mean an SSH
session and an `/etc/fstab` line. Now there's an **Add network share (NAS)** panel
right in the music-library picker: type the NAS address, the share name and your
credentials, and Audiogravi<sup>ty</sup> mounts it, **tests it on the spot**, and
selects it as your library — read-only by default, and if anything is wrong (wrong
password, unreachable box) it tells you exactly what and leaves nothing behind. The
same panel lists the shares you've added and lets you remove them, warning you
before it pulls the one your music is currently playing from. It survives reboots
(the share mounts on first access, even if the NAS was off at boot). CIFS/SMB —
what Synology, QNAP and every mainstream NAS speak, and it now negotiates whatever
SMB dialect your NAS does, so a share that refused a strict SMB3 handshake mounts
cleanly; for NFS or a hand-managed mount, the manual's NAS section still has you
covered.

Once a share — or any library change — is applied, Audiogravi<sup>ty</sup> re-scans
its music database for you and shows a live **"Indexing library…"** indicator until
it's done, so you're never left wondering whether the new library has been picked
up. Leave and come back to the Config tab mid-scan and the indicator is still there;
it disappears on its own the moment indexing finishes.

### The manual grows up — quick start, glossary, and real screenshots

The user manual now covers the whole journey, illustrated. A one-page **Quick
start** takes you from a bare box to music — and it's the first thing the in-app
reader shows — while a new **Glossary** decodes the audiophile and UPnP vocabulary
in two lines per term. Eleven **real screenshots** (phone rendering, light theme)
show the screens the chapters describe: the fullscreen player, the mixed queue with
its source badges, the output selector, first-run setup, Services, Settings and the
update banner.

The guides you were missing are there too: **mounting a NAS share** step by step,
**installing Audiogravi<sup>ty</sup> as an app** on your phone (required for push
notifications on iPhone), **getting HTTPS** at home so passkeys and notifications
light up, **backing up and restoring** your box, recovering a **lost admin
password**, and fixing the classic network traps that hide AirPlay and UPnP
devices. First-run now tells the whole truth as well — including the audio-engine
installation step and the default `admin` account you sign in with (change that
password!).

---

## 0.9.16 — 2026-07-13

### Favorite your streaming albums

You can now star a Qobuz, Tidal or HIGHRESAUDIO album to add it to your favorites
on that service — straight from the browse grid or search, with one tap. The star
shows whether an album is already a favorite and updates instantly.

### Swipe to remove

You can now swipe a queued track to the left to remove it — the same familiar gesture
already used for radio stations and UPnP devices, now on the Queue too (the Remove
button stays if you prefer it). It always removes the track you swiped, even if the
queue has since reordered.

### See your streaming queue — and where each track comes from

Selecting a Qobuz, Tidal or HIGHRESAUDIO album now fills the Queue with its tracks,
titles and all — where before it looked empty (those services play through the same
engine as your local library, and the queue simply wasn't reading them back). Titles
stick around across a restart, too.

When a queue mixes sources — say a radio station followed by a Qobuz album — each
upcoming track shows a small badge telling you where it comes from, and a filter lets
you show just one source at a time. Filtering only changes what you see; nothing moves
or stops playing, and the current track always stays in view.

### Keep the app in portrait

Audiogravi<sup>ty</sup> now stays in portrait by default on phones and tablets. A new
**Portrait Lock** switch in Settings turns it off if you prefer landscape, and on a
device you can't rotate a *Continue in landscape* button on the rotate screen lets
you carry on. Desktop installs are unaffected.

---

## 0.9.15 — 2026-07-13

### Read the user manual without leaving Audiogravi<sup>ty</sup>

A new **Manual** button in the tab bar opens the full user manual right inside the
app — a chapter list on the side, the page on the right. It always shows the latest
published manual, and links between chapters work in place without losing your spot.

### The queue shows what you are actually playing

Playing internet radio while browsing your library used to label the queue "Queue of
Local Library" with no artwork, because radio (like Qobuz or Tidal) rides the same
playback engine as your local files. The queue now reads by the real source —
"Radio" — and shows the station's logo.

---

## 0.9.14 — 2026-07-12

---

## 0.9.13 — 2026-07-12

### Spot a waiting update from the tab bar

The Admin tab now carries a small download marker whenever a newer Audiogravi<sup>ty</sup>
release is available for your box — the same at-a-glance cue the tab already gives
for new announcements. A **required** update stands out in the warning colour. Open
the Admin page to install it in one click, as before.

### Tap an artist in search to see their albums

Searching your library and tapping an **artist** now opens that artist's albums —
across your local library, **Qobuz**, **Tidal** and **HIGHRESAUDIO** — with a back
control to return to browsing. Previously an artist row tried (and failed) to queue,
since an artist isn't something you can play directly; now it's a proper way in to
their discography.

### Qobuz search works again

Qobuz library search had begun returning an error for **every** query — an empty
image field coming back from Qobuz was enough to break the whole search. Fixed:
searches with missing artwork, compilation credits or other absent fields now come
back cleanly.

---

## 0.9.12 — 2026-07-10

### Describe your hi-fi chain with confidence

Audiogravi<sup>ty</sup> draws the **Audio Pipeline** signal-path view from a file you own, `audio-topology.json` — your description of the hi-fi chain (which DAC, amplifier, speakers, and how they're wired). That file is now **checked when you edit it**: open the pipeline's **CONFIG** editor, and saving first validates your changes. A genuinely broken file (bad structure, an unknown device type) is refused with a clear reason; softer issues — an output pointing at a device that no longer exists, or a connector that matches none of the box's real outputs — are shown as warnings you can review and accept. The same check also runs quietly at startup.

You can now also **Download** the topology to your computer and **Upload** it back — handy for editing it offline or keeping a copy — with the same validation applied when you save. A fully-commented example file ships with the box to start from, and the user manual gains a dedicated section explaining what the topology is, how physical outputs are detected live from your hardware, and how to keep the map up to date.

---

## 0.9.11 — 2026-07-10

### License emails from your own domain, with the right sender

Audiogravi<sup>ty</sup>'s license server now sends its mail through a proper delivery provider with domain authentication (DKIM/SPF), so license keys and license files land reliably in customers' inboxes instead of spam. License deliveries and broadcast communications carry **distinct sender addresses** (for example `license@` for deliveries and `news@` for announcements), and every message can set a **Reply-To** (such as `support@`) so replies reach the right place. Everything is configurable from the admin SMTP panel.

### Large mailing campaigns send themselves, safely, over several days

Broadcast campaigns to your licence holders are no longer fired all at once. The licence server now paces them under your email provider's daily limit, always keeping room for the essential licence-delivery emails that must go out. A big campaign is queued and delivered automatically over the following days — you can close the page and it keeps going. Recipients already emailed are never contacted twice, anyone who unsubscribes before their turn is skipped, and the mailing panel shows each campaign's progress (sent / pending).

### More reliable physical output switching (USB / optical / HDMI)

Switching the physical audio output no longer relies on a hand-written device map that could silently point at the wrong sound card after a reboot or a USB re-plug. Audiogravi<sup>ty</sup> now detects the real audio hardware and works out the correct output on the fly, so switching between USB, optical and — now also — HDMI outputs stays correct across reboots. The signal-path view's active-output indicator is corrected the same way. Your hi-fi chain description (which amplifier, speakers, cabling) remains yours to declare and edit — Audiogravi<sup>ty</sup> reads it, never overwrites it. And when a switch does not take, the Outputs panel now tells you instead of pretending it worked — it shows the reason and rolls back to the real state.

Better still, switching **MPD's** output is now **gapless**: Audiogravi<sup>ty</sup> flips the output over MPD's control socket instead of restarting the player, so there is no silence and a cast already playing keeps going on the new output. AirPlay can't be switched without restarting its receiver, so there the Outputs panel warns you first that it will interrupt any AirPlay playback in progress. (After updating an existing box, run "reset to minimal" once on the audio services so MPD picks up the new gapless switching; until then it keeps working the old way.)

### Tidier library search on small screens

The row of source-filter chips beneath the library search box now stays on one line and scrolls sideways on narrow screens, instead of wrapping onto several rows — a cleaner, more compact search header.

---

## 0.9.10 — 2026-07-06

### Update Audiogravi<sup>ty</sup> in one click — no terminal needed

When a newer Audiogravi<sup>ty</sup> release is available, the **Admin** page now shows an update banner with the new version, a release-notes link, and a **required** badge when the update is critical. One click — a short confirmation (playback briefly stops) and your admin password — installs it: the box downloads the new version, swaps it in, checks it comes back up healthy on the **right version**, and shows live progress the whole way (downloading → installing → verifying), even across the restart. On a single-box setup, the same click also updates the web interface, so everything lands on the new version together.

Safety first: if anything goes wrong, the box **automatically rolls back** to the previous version and tells you — you're never left on a broken update. The update runs on its own, detached from the app, so it survives the restart it triggers. There's no operating-system reboot; only a brief pause while the audio service restarts.

Under the hood the updater runs with tightly-scoped privileges (a locked-down, root-owned launcher rather than a blanket permission), an interrupted update can't leave the box stuck "updating" forever, and a mistyped version on the licence-server side is refused rather than silently offered to your fleet.

### HIGHRESAUDIO (HRA) — a new hi-res streaming source

Audiogravi<sup>ty</sup> now streams from **HIGHRESAUDIO** (HRA-Streaming) through its official API, alongside Qobuz and Tidal. Connect from **Sources** with your HRA email and password; the app keeps the session alive on its own and re-logs in transparently when it expires. Your password is stored encrypted on the device.

Once connected, Highresaudio appears as a library source with several curated views — **Favorites** (your saved albums), **Discover**, **Editor's Picks** and **Bestsellers** — plus full catalog **search**. Albums play on the local MPD output or on a connected UPnP renderer, and the now-playing screen shows an **HRA** source badge.

HRA always delivers each album at its **native master resolution** (up to 24-bit / 352.8 kHz FLAC) — bit-perfect, with no quality downgrade. Note: HRA allows a single active device per account, so connecting Audiogravi<sup>ty</sup> signs you out of your other HRA players.

### More reliable transport controls when casting to a network player

When you cast a streaming source (Qobuz, Tidal or HIGHRESAUDIO) to a UPnP renderer, the transport buttons (**next / previous / play-pause**) now talk to the player that actually holds the playlist. This fixes occasional failures on a manual *next* — an error, or the screen dropping to "Nothing playing" — even though tracks kept advancing on their own. Playback of your local library is unchanged.

A related fix: a Qobuz or HIGHRESAUDIO track played to your **local output** used to fail after about an hour — the streaming link it queued expired. Queued tracks now carry a stable link that Audiogravi<sup>ty</sup> refreshes the moment the track actually plays, so a paused track, a long queue or a resumed session plays without a hitch (and without routing the audio through Audiogravi<sup>ty</sup> — it streams straight from the source).

### Your box's own renderer is shown, but not selectable

Audiogravi<sup>ty</sup> advertises itself on the network as a UPnP renderer so other apps — a phone, a control point — can cast music *to* it. That self-entry now appears in the renderer list as a greyed-out **"This device · receives external casts"** row you can't select: playing on the box is exactly what the **Local DAC** output already does, so choosing the box's own renderer would be a pointless duplicate. Real network renderers (Marantz, Linn…) are unaffected. If a box had somehow been set to its own renderer, it falls back to the Local DAC on update — same sound, cleaner state.

### Cast your local library to a network player

Your **local music library** (NAS / USB files) can now be sent to a UPnP network player, just like Qobuz, Tidal or HIGHRESAUDIO. When a network player is your active output, playing a local album streams it to that player over your LAN — seekable, bit-perfect, no re-encoding. Playback on Audiogravi<sup>ty</sup>'s own local output is untouched and stays direct. And the now-playing screen now shows the real source badge on a network player (**LIBRARY / QOBUZ / TIDAL / HRA**) instead of a generic **UPNP**.

### Set up and tune your audio services, guided

Configuring the audio services (MPD, AirPlay, UPnP) is now guided end-to-end. On a **new box**, a single **Configure audio stack** button detects your DAC and music library and generates a minimal, bit-perfect working configuration for all three services — it asks for your admin password, then gets out of the way (the button disappears once the box is set up).

Afterwards, each service opens in a **Guided** editor where you change its **audio output** or **music library** in a couple of clicks — only the setting you touch is rewritten, so any manual tweaks you made are preserved. Every service can target its **own output**: MPD on your USB hi-res DAC, AirPlay on the optical out, and so on. A **Reset to default** action regenerates a clean working config whenever you need it (your current file is backed up first), and each service tile shows a **CONFIGURED** badge once Audiogravi<sup>ty</sup> has set it up.

Under the hood, when you configure a USB DAC the box pins its sound-card number at the system level, so Linux always gives that DAC the same number even after a reboot or a USB re-plug. The audio services therefore always open the right output — nothing to re-check at startup, no restart, and nothing to go stale. (Your own hand-made audio tweaks are left untouched.)

---

## 0.9.9 — 2026-06-30

### Deployment renamed: `core` and `ui` (was `backend` / `frontend`)

The two installable components are now called **core** and **ui** everywhere — packages, systemd services, install scripts and data directories. New installs use `install-core.sh` / `install-ui.sh`, the services are `ag-core-server` / `ag-ui-server`, and data lives under `/opt/audiogravity/core` and `/var/www/audiogravity-ui`.

Existing systems are not touched automatically. To move an already-installed host to the new layout, run the new `migrate-deploy-layout.sh` once (as root) before reinstalling: it backs everything up first, then renames the layout while preserving your configuration, secrets and user accounts. It works whether core and ui share a host or run on separate machines.

### Fullscreen player — source badge on the cover art

The origin badge (❖ QOBUZ, ❖ TIDAL, ❖ UPNP) is now displayed directly on the cover art, top-left. The track badge (A1 · TRACK 01) appears bottom-left. The duplicate source badge that appeared below the cover has been removed.

### Track number badge now shown for all sources

The A1 · TRACK 01 badge was missing for Qobuz, Tidal and MinimServer streams. It now appears correctly for all sources, via both the direct MPD path and the UPnP renderer path.

---

## 0.9.8 — 2026-06-29

### Signal path — the real audio chain, in real time

The fullscreen player now shows the full audio chain as it actually exists at any moment, not a static topology.

**With a UPnP renderer active** (e.g. upmpdcli / music.#1):
`• Qobuz → • music.#1 → • MPD → • USB → • Heed Abacus`

**In bypass mode or without renderer:**
`• Qobuz → • MPD → • USB → • Heed Abacus`

**With a native network renderer** (Marantz, Linn…) that has its own internal DAC:
`• Qobuz → • Marantz PM7000N`

The connector (USB / TOSLINK) is inserted automatically based on the active ALSA output and updates live when you switch. The source (Qobuz, Tidal, Radio, Library…) is always the first step.

The separate `→ music.#1` overlay in the fullscreen player has been removed — the renderer is now one step among others in the chain. The mini player source row gains a compact `→ renderer_name` badge when a renderer is active.

### Output selector — switch between physical outputs and network renderers

The Sources panel now shows a unified **output selector** with every available audio destination in one place:

- **Physical outputs** — one row per MPD audio output block (USB DAC, TOSLINK…), named exactly as configured in `mpd.conf`. Tapping one enables it exclusively and disconnects any active renderer.
- **Network renderers** — all known UPnP renderers (upmpdcli, Marantz, Linn…) listed below. Tap to connect; the active renderer shows a Disconnect button and a volume slider.

The active output is highlighted in green. An unreachable renderer shows orange. Switching between a physical output and a renderer requires no page refresh and fires no extra commands — one tap routes audio.

**Radio cast to renderer** — playing an internet radio station while a UPnP renderer is selected now sends the stream to the renderer via AVTransport, just like Qobuz or library tracks. If no renderer is active, playback falls back to the local MPD output.

**Remove a renderer** — swipe a renderer row to the left to permanently remove it from the list. No need to reconnect or scan again to add it back — use the Scan button.

### UPnP renderer — full album playback, NEXT / PREV and "Up next"

When you play an album from Qobuz, Tidal or a MinimServer library to a UPnP renderer, AG now queues all tracks and chains them automatically — gapless where the renderer supports it, seamless in any case. Qobuz tracks are served through AG's internal proxy so URLs never expire, enabling both uninterrupted album play and manual navigation.

The **NEXT** and **PREV** transport buttons in the fullscreen player now skip between tracks in the renderer queue. Buttons are disabled at boundaries (first / last track). Pressing both rapidly is safe — a 409 is returned if a transition is already in progress.

The fullscreen player shows an **Up next** strip at the bottom with the next track's title, artist and cover art, updated in real time as the album progresses.

### UPnP renderer — seeking within a Qobuz track

UPnP renderers can now seek mid-track within a Qobuz stream. The AG proxy forwards HTTP `Range` requests from the renderer to the Qobuz CDN and relays the `206 Partial Content` response, so transport position scrubbing in the renderer's own UI (or any control point) works without restarting the stream from the beginning.

### UPnP renderer — live status indicator

The renderer card in the Sources panel now reflects the true state of the device in real time:

- **Connected** (green) — renderer is reachable and responding
- **Unreachable** (orange) — the connection object is active but the device stopped responding (powered off, network loss). The card shows "unreachable — check device" and recovers automatically within 30 s when the device comes back — no page refresh, no manual reconnect.
- **Offline** (red) — no renderer configured

After a backend restart, the auto-reconnect now retries with exponential backoff (30 s → 60 s → … → 5 min cap) instead of giving up after one attempt. If upmpdcli or the renderer starts later than the AG core, the badge goes green as soon as the device responds.

### Install on your home screen (Android / Chrome)

On Android, Chrome will now offer a compact **Install** banner at the bottom of the screen when Audiogravi<sup>ty</sup> is eligible for installation as a standalone app. Tap **Install** to add it to your home screen — the app then opens full-screen without the browser chrome, exactly like a native app. Dismissing the banner suppresses it for 30 days.

On iPhone, use Safari's Share sheet → "Add to Home Screen" as before (iOS does not expose an install event to web apps).

### Player stays visible when offline

If you lose your network connection while Audiogravi<sup>ty</sup> is open, the player now keeps showing the last known track and source instead of going blank. A small **Offline** label appears in the source row to make the stale state explicit.

On a cold reload (opening the app while offline), the last known player state is restored from local cache — so you can still see what was playing last, even without a live connection to the streamer.

### Reliability & fixes

- **Native renderer — "Nothing playing" fixed** — with a network renderer (Marantz, Linn…) whose audio stack is self-contained, the fullscreen player was showing "Nothing playing" even when a track was actively playing. AG now reads the renderer's internal state directly: title, artist, album, cover art and transport position all appear correctly without requiring the local MPD to be in the chain.
- **Native renderer — output bar "No output selected" fixed** — same root cause: when no local source was active the output bar could not determine the routing. The output label and signal path (e.g. `• Marantz PM7000N`) now reflect the renderer correctly.
- **Disconnect stops playback** — clicking Disconnect in the Sources panel now immediately stops the renderer. Previously the renderer kept playing its stream independently until it finished.
- **Renderer snaps back after restart** — after an AG backend restart, the renderer badge now reflects the correct state (PLAYING / STOPPED) within seconds instead of waiting up to 30 s. The backend detects the stale subscription ID, re-subscribes immediately, and refreshes the display.
- **Signal path during reconnect window** — the renderer step is no longer shown in the signal path while the connection is being re-established after a restart.
- **Qobuz single track to renderer** — playing a single Qobuz track (not a full album) to an active renderer was silently broken since the queue refactor. Now correctly routes via `play_queue()` with cover art forwarded.
- **Renderer card stale on new session** — if a renderer status event arrived before the renderer list finished loading, the card was left stale. It now triggers a reload and applies the event on completion.
- **Cover art on consecutive album tracks** — if a track returned a 404 cover, subsequent tracks on the same album were permanently blocked. The error is now cleared on every track change.
- **"Up next" strip cleared on disconnect** — the next-track strip now disappears when the renderer disconnects or is bypassed, instead of lingering indefinitely.
- **Idle renderer badge** — when the renderer is connected but nothing is playing, the fullscreen player now shows the renderer name in the source row so you can confirm the routing without starting playback.
- **Connector badge for upmpdcli** — the USB/TOSLINK badge was incorrectly hidden when upmpdcli was active; it is now always visible since the physical connector is in the chain.
- **MPD output — invalid ID now returns 404** — selecting an MPD output with an unknown `output_id` would previously silently disable all outputs. Now correctly returns 404 before issuing any MPD command.

---

## 0.9.7 — 2026-06-26

### UPnP Control Point — send audio to network renderers

AG can now control any UPnP/DLNA MediaRenderer on the local network (network amplifiers, DLNA speakers, upmpdcli…). Select a renderer in the Sources panel, connect it, then play from the MinimServer library, Qobuz or Tidal — the stream goes directly to the renderer.

**What's new:**
- New "UPnP Renderer" section in the Sources panel: network discovery, connection persisted across restarts, Play/Pause/Stop/Volume controls from the interface.
- `→ renderer` badge in the mini player and fullscreen player to indicate active routing.
- MinimServer → renderer: URI handoff (zero AG proxy, zero extra CPU load).
- Qobuz → renderer: self-authenticated CDN URL (HMAC, no proxy).
- Tidal → renderer: existing DASH→FLAC proxy with LAN-reachable IP (same quality as MPD).
- Renderer state updated in real time via SSE (SUBSCRIBE/NOTIFY + 30 s heartbeat fallback).

---

## 0.9.6 — 2026-06-25

### Cover art when playing via upmpdcli

When an external UPnP control point (BubbleUPnP, Kazoo, Linn app…) pushes music or radio to your streamer via upmpdcli, Audiogravi<sup>ty</sup> now displays the correct cover art — including radio station logos — by querying upmpdcli's AVTransport directly to retrieve the artwork the controller originally sent.

### HQPlayer — accurate connection status

The HQPlayer card in the Sources view now reflects the true state of the full audio chain:

- **Connected** — HQPlayer reachable and `networkaudiod` active (audio can reach the DAC).
- **NAA offline** — HQPlayer reachable but `networkaudiod` inactive (no audio output possible).
- **Offline** — HQPlayer unreachable.

The "Use as output" toggle is only shown when the full chain is operational. It is cleared automatically if `networkaudiod` stops during a session.

Several core polling regressions fixed: logs no longer flood with WARNING messages at startup or during DSD stream loading.

### Player auto-follows the active source

The mini-player and fullscreen player now automatically display the currently playing source — no manual dot navigation required when switching between sources (MPD, Roon, AirPlay, TIDAL…).

Tapping a dot or swiping to another source suspends auto-follow so you can browse at your own pace. Auto-follow resumes automatically when the source you selected stops playing.

### Format strip — bitrate now shown for all sources

The fullscreen player's format strip now displays a bitrate for every source and format — ALAC, FLAC, WAV local files, TIDAL, Qobuz, radio, Roon and AirPlay.

- **MPD sources (ALAC, FLAC, WAV, radio, Qobuz)** — instantaneous decode bitrate as reported by MPD.
- **TIDAL** — exact bitrate read from the DASH manifest, available from the very first second of playback (no more `—` during stream warm-up).
- **Roon / AirPlay** — PCM-equivalent computed from bit depth × sample rate × 2 ch (e.g. 24bit/96kHz → 4608 kbps).

### Communications from Audiogravi<sup>ty</sup>

Two new channels so you never miss important news about the product.

**In-app announcements** — When Audiogravi<sup>ty</sup> publishes a notice (new version, maintenance window, special offer), a 🔔 bell appears on your Admin tab. Open it to see the message as a dismissable banner. Dismissal is stored locally — the banner won't come back. Notices are fetched passively during the regular 24 h licence check-in; no additional data is collected.

**Email** — Important communications (release announcements, early-access offers) are sent to the email address associated with your licence. Every message includes a one-click unsubscribe link — no account required.

---

## 0.9.5 — 2026-06-22

### Core — Audio reliability & under-the-hood fixes

Two core modules (`audio_pipeline` and `audio_hw`) went through a thorough code review. The fixes are transparent to the end user but protect audio quality under load:

- **Event loop no longer blocked** — all filesystem access in `audio_hw` and `audio_pipeline` is now off the event loop (`asyncio.to_thread`). On the Pi, a scan could stall for 50–200 ms, delaying SSE heartbeats and potentially causing audio glitches.
- **Accurate ALSA subdevice availability** — `GET /audio-hw/devices` now reflects the real occupation state of ALSA devices (read from `/proc/asound`). Previously `subdevices_available` was always `1` even when MPD or HQPlayer held the device exclusively.
- **`?force_refresh=true`** — new query parameter on `GET /audio-hw/devices` to force an immediate rescan after a USB hotplug event, without waiting for the 60 s cache to expire.
- **Cache not corrupted on I/O error** — a transient error during a scan (hotplug race, permission) no longer caches an empty or partial list; the next call retries cleanly.
- **Pipeline metrics corrected** — HQPlayer volume clamped to `[0, 100]`, `cpu_percent()` initialised correctly, ALSA latency accurate on ARM64 (64-bit wraparound).
- **HQPlayer "ghost track" in mini player fixed** — after stopping HQPlayer completely (no track loaded), the mini player kept displaying the last played track indefinitely. The now-playing cache is now explicitly cleared when HQPlayer confirms it has nothing to play, while transient stops (DSP transitions, buffering) still show the last known state.
- **Config backup restore now works** — `restore_backup` was silently rejected by sudoers in production (missing `cp` rule); backups can now be restored from the UI.
- **Backup files are now private** — backup files (which may contain service passwords) are now correctly set to mode 600; previously the `chmod` silently failed and files were world-readable.
- **Config editor save/reload no longer stalls** — all blocking I/O in the config service (file reads, sudo commands) now runs off the event loop, preventing audio glitches during a config save or package install.
- **Config validation no longer freezes the server** — `POST /config_validation/validate` previously ran a `systemctl` subprocess per service synchronously on the event loop (up to N×5 s); checks are now parallel and non-blocking.
- **Login timing hardened** — disabled accounts and nonexistent accounts now take the same response time, preventing username enumeration by measuring login latency.
- **Passkey registration and login no longer interfere** — starting a passkey registration and a passkey login simultaneously for the same account no longer causes both flows to fail.
- **HQPlayer playback now works** — every `play_uri` and `play_library_item` call was silently failing after loading the queue because the `<Play/>` command closes the connection without responding; the batch transport now handles this correctly.
- **Trial period survives a power loss** — the trial file is now written atomically; a crash mid-write no longer produces corrupted JSON that is misdiagnosed as tampering and locks the user out of their trial.
- **License gate no longer bypassed at startup** — if the license service fails to initialise, protected endpoints now return HTTP 503 instead of silently allowing all access.
- **Radio custom stations now actually work** — a missing `await` made `POST /radio/library/custom` always fail with a serialisation error since the feature was introduced.
- **Tidal login errors are now reported correctly** — previously the callback endpoint returned HTTP 200 even when the token exchange failed; it now returns HTTP 400 with a clear error message.
- **Server shutdown no longer hangs** — SSE monitoring loops were never cancelled on shutdown due to a type mismatch (`List[Task]` iterated as a single `Task`); fixed so graceful restart is reliable.
- **Reduced CPU/memory pressure on Pi under load** — several long-running blocking operations (audio ALSA scan, thermal zone reads, governor writes, stddev histogram expansion, `os.fsync`) are now off the event loop, reducing audio dropout risk and RAM pressure under sustained load.
- **License server XSS fixed** — a crafted license key or server-controlled filename could inject HTML into the portal activation pages; the admin session token could be exfiltrated if the admin panel was open in the same browser session.
- **License resend and transfer now preserve version scope** — resending or transferring a v1-scoped license was silently upgrading it to an all-versions license; upgrade paywall is now enforced correctly.
- **All-versions lifetime licenses no longer falsely rejected on AG v2** — licenses issued before version scoping was introduced are now correctly accepted on all AG versions.
- **UI XSS vulnerabilities fixed** — three injection points in the license status and package update UI now HTML-escape or validate server-controlled values before rendering. A crafted core response could previously exfiltrate the admin JWT token.
- **UI no longer crashes on corrupted browser storage** — auth initialisation handles a malformed `jwt_user` in localStorage gracefully instead of throwing an uncaught `SyntaxError` that left the app blank.
- **Config editor no longer accumulates memory** — opening and closing the config editor multiple times no longer leaks CodeMirror instances; a `disconnectedCallback` now properly cleans up.

---

## 0.9.4 — 2026-06-20

### UI — Security, reliability & code quality

A targeted UI review produced the following improvements:

- **XSS hardening** — `escapeHtml` now imported as an ES6 module in the admin panel (no more `window.escapeHtml` fallback that could silently skip escaping); metric chart labels use Lit's built-in auto-escaping instead of `unsafeHTML`.
- **Push notifications fixed** — unsubscribing from push notifications now uses the correct `DELETE` HTTP method with the endpoint as a query parameter, matching the backend router. Previously the call was a `POST` with a JSON body that was silently ignored.
- **Password validation** — whitespace-only passwords (e.g. 6 spaces) are now rejected in the user modal before reaching the backend.
- **Memory leak fixed** — the jitter latency Chart.js instance in the network test page is now destroyed when the component is removed from the DOM.

### Reliability & Security — Core hardening

An extensive review of all 20 core modules produced 40+ targeted fixes. None break existing functionality; the most impactful for daily use:

- **Radio station editing now works** — `PUT /radio/{uuid}` was silently returning a coroutine instead of the result; station edits are now persisted correctly.
- **DSD streams detected in the pipeline** — `audio_str="dsd64:2"` was silently discarded; DSD sample rate and bit depth now appear correctly in the pipeline graph and metrics.
- **UPnP queue routes to the right output** — when multiple MPD outputs are configured, UPnP queue operations now honour the requested `output_id` instead of always using the first output.
- **Profile activation resilient to slow services** — stop and start phases are now bounded to 30 s each; a hung service can no longer freeze a profile switch indefinitely.
- **Player poll loop no longer crashes silently** — a network error during `get_now_playing()` now degrades gracefully instead of causing a `NameError` that killed the SSE stream.
- **Package installer hardened against injection** — `install_script_args`, `check_command` and `uninstall_commands` now use `shlex.split` + `subprocess_exec` instead of `shell=True`; GPG key and sources-list destination paths are validated before any `sudo cp`.
- **Steering output switch validated** — ALSA device strings are checked against `hw:<card>,<device>` before being written into any config file, preventing malformed values from corrupting MPD or shairport-sync config.
- **Auth & JWT tightened** — `POST /auth/users` correctly returns 201; whitespace-only passwords rejected; JWT tokens now carry a `jti` (unique ID) for future revocation; token decode errors no longer expose fragments in logs.

### HQPlayer — Stop playback

`POST /hqplayer/stop` is now implemented (it was documented but missing). The button in the HQPlayer output card can reliably stop playback and clear the current track metadata.

### Stream Origin Badge

The Now Playing players (mini bar and fullscreen) now show **where the current
track is streaming from** — a small logo + label such as Tidal, Qobuz, your
UPnP/DLNA server (by name, e.g. *MinimServer*), a radio station, a local file,
Roon or AirPlay. Previously every source that played through MPD looked
identical ("MPD"), so you couldn't tell a Tidal track from a Qobuz one or from a
file on your NAS. The badge is derived server-side from the active stream, so it
stays accurate as you switch sources.

### Reliability — Tidal & Qobuz

When Tidal or Qobuz reverse-engineered client credentials rotate (which happens
periodically without notice), AG now detects the 401/403 response and logs a
clear ERROR with a remediation hint instead of returning an opaque failure. The
Tidal stream endpoint returns HTTP 503 so MPD gets a clean error rather than a
broken stream.

### Library & Settings refinements

- **UPnP/DLNA search fully playable** — media servers such as MinimServer now
  appear as search sources next to MPD, Roon, Qobuz and Tidal. Selecting one while
  in the Search tab runs a text query against that server; clicking "+" or play on
  a result adds it to MPD with correct title, cover art and server badge.
- **Config editor — blank file hint** — when a service config has all sections
  empty (package defaults, e.g. a fresh Debian shairport-sync install), the form
  view now shows a clear banner instead of a series of empty `{}` boxes, with a
  direct link to Expert Mode to view and uncomment the full file.
- **Settings panel** — a single unified product version (front and back share it)
  next to the Swagger API link, and the **Logout** button moved from the top bar
  into the Settings footer for a cleaner top bar.
- **Polish** — the settings button uses a gear icon (mobile nav uses a hamburger),
  and Qobuz/Tidal/HQPlayer now share the same connection status indicator as the
  other sources.

---

## 0.9.3 — 2026-06-14

### Tidal HiFi Streaming

Tidal joins Qobuz as a streaming source. Connect a Tidal HiFi account via PKCE
login (open the link, sign in, paste the redirect URL back — Tidal's fixed
redirect cannot be intercepted in a browser), then browse Favorites, New Releases,
Charts (TIDAL's Top Hits, Viral / Rap / R&B / Pop Hits…), Editorial playlists
(Popular, Trending, TIDAL Rising…) and your own Playlists, or search the full
catalogue. Playback is **lossless FLAC**:
unlike Qobuz's direct URL, Tidal delivers FLAC as a segmented DASH manifest, so a
local proxy remuxes it on the fly with ffmpeg (`-c:a copy`, no re-encoding) and
streams it to MPD as it is produced — playback starts in about a second. The
remux is written to a seekable FLAC file and kept in a small, disk-backed cache
(the current track plus a couple of recent ones, wiped at startup), so replaying
or reopening a track serves it with HTTP Range and **in-track seek works**. The
first play of a given track was not seekable in this release; it is since
0.9.34, which reopens the track from that cached copy when you seek. Requires
`ffmpeg` (installed by the backend installer).

### Top Bar — Mobile Navigation & Library Shortcut

The top bar gains two buttons. On the left, a navigation toggle opens the
vertical tab menu on mobile — symmetric to the settings burger on the right. A
new Library shortcut (left of Logout) jumps straight to the Library tab from
anywhere; licence gating is preserved, so a locked tab opens the licence modal
instead. The obsolete documentation and admin "Components" buttons were removed.

### Roon Source Logo

The Roon source dropped its "RN" text placeholder for a proper logo, sized like
the other source icons (MinimServer, Qobuz, HQPlayer). Because the mark is
monochrome, it is rendered as a `currentColor` mask, so it stays visible across
light, dark and the active (selected) card state.

### DRY-RUN Restricted to Admins

The Audio Software DRY-RUN toggle is scoped to administrators. It now performs
real validation: a HEAD request is sent to the download URL before reporting
success, so a dead URL or unreachable server surfaces as a failure instead of a
fake `Success`. For APT repository packages, `apt-get install --simulate` is
also run when possible to surface dependency conflicts.

### Login Page

The version label now reads `v0.9.2` (lowercase prefix, no space).

### Bug Fixes

- **AirPlay now-playing on ARM** — shairport-sync track metadata is read from an
  `a{sv}` D-Bus dict whose values arrived wrapped as Variants on ARM/Debian, leaking
  the raw `<dbus_fast…Variant…>` repr into the pipeline now-playing. The values are now
  unwrapped (recursively; no-op on x86 where they are already native).
- **Fullscreen player volume swipe** — adjusting the volume slider no longer triggers
  the player's multi-source switch swipe; the volume popover now isolates its own touch
  gestures.
- **Library horizontal scroll vs tab switch** — scrolling a horizontal row (browse pills,
  album shelves) no longer flips to the next tab; the swipe-to-switch handler now defers
  to any horizontally-scrollable element under the finger.
- **Fullscreen player pull-down vs scroll** — in a long tracklist, swiping down to scroll
  back up no longer closes the player; pull-to-dismiss only engages when the content is
  already scrolled to the top.

---

## 0.9.2 — 2026-06-09

### Qobuz Hi-Res Streaming (full stack)

Qobuz authentication migrated from deprecated username/password to **OAuth2**.
New backend module handles the full lifecycle: bundle credential extraction,
OAuth URL generation, browser login, token exchange, secret discovery, and
persistent config. The library service uses header-based auth and correct API
signature format. Search runs 3 parallel single-type calls; album and track
queueing registers external stream metadata (title, artist, album, cover art)
keyed by stable `eid`, so now-playing displays are correct despite ephemeral
signed URLs. Qobuz appears as a virtual source in the player when connected.

**Catalog browsing** — browse pills switch to Favorites / New Releases /
Selection / Playlists when Qobuz is selected. Each category fetches from a
dedicated Qobuz API endpoint. Editorial playlists are playable — clicking one
queues all tracks to MPD with full metadata.

### DSD Volume Protection — 6 Bug Fixes

Fixed intermittent regression where volume snapped to 100% during non-DSD
playback. Root causes: stale HQPlayer cache items triggering false DSD
detection, race conditions corrupting saved volume state. 10 unit tests added.

---

## 0.9.1 — 2026-06-07

**Focus: ARM/Debian (aarch64) portability + production hardening.**

### ARM64 as First-Class Target

Audiogravi<sup>ty</sup> now installs and runs on aarch64 (Raspberry Pi 4 / Debian)
alongside x86/DietPi. Backend, frontend, license server, and audio-software
installs validated end-to-end on both architectures.

- Deterministic dependencies: `requirements.lock` (68 packages, wheels verified
  for x86_64 and aarch64, Python 3.13.5)
- upmpdcli on ARM64: native build script for the libnpupnp → libupnpp →
  upmpdcli chain, published as a checksum-verified `.deb` bundle
- Roon per-arch URLs, download allowlist, complete uninstall support

### HQPlayer Integration

Discovery panel with manual IP entry for cross-subnet setups. Volume protection
for DSD streams (DSD playback forces 100% hardware volume, restored on
non-DSD). Auto-cleared stale track state after 30s stopped.

### Qobuz OAuth2 Foundation

Full OAuth2 flow replacing deprecated username/password login. Bundle credential
extraction from the Qobuz web player JS, browser-based login, code-to-token
exchange. Frontend connect/disconnect card in the Sources view.

### Library Player — Fullscreen Music Browser

Bottom-sheet overlay hosting six views: Browse, Search, Queue, Sources, Outputs,
Now Playing. Artist → album → track drill-down for MPD, Roon, and Qobuz. Album
card grid with infinite-scroll pagination (IntersectionObserver, 50 albums per
page). Queue management (MPD: remove/clear; Roon: read-only).

### Now Playing — Complete Playback Control

Fullscreen panel driven by SSE: cover art, title, artist, album, format strip
(sample rate, bitrate, codec, hi-res highlight), signal path, seekable progress
bar, transport controls (prev/play/next/repeat/shuffle), volume slider. Dynamic
background tint extracted via canvas color sampling. Horizontal swipe between
active sources. Album detail popover with tracklist. Mini player bar with swipe
gestures.

### Audio Pipeline

Interactive SVG graph: pan, zoom, minimap, draggable nodes with persisted
positions. Live status on nodes (playback state, now-playing info). Output
steering: click any link to switch a service's ALSA output on the fly. Roon zone
display and transfer. Network connectivity view (WiFi signal quality). Mobile
responsive layout.

### License System

- **Trial**: 30-day auto-activated, HMAC-signed with device fingerprint
- **Lifetime**: single-device `.lic` file, Ed25519-signed, uploaded via UI
- **License Server**: admin panel (orders, audit log, email templates, bulk ops,
  device transfer), customer self-service portal, PayPal IPN automation, online
  verification (24h refresh)
- **Feature gating**: `require_full_license` dependency on premium endpoints;
  `version_expired` handling for v1→v2 upgrades
- **Self-service activation**: 3-step stepper (key → hostname → activate) with
  `.lic` download

### Passkeys — Face ID / Touch ID (WebAuthn / FIDO2)

Passwordless authentication via discoverable credentials. One-time setup offer
after password login. Burger menu toggle to register/remove passkeys. Backend:
6 endpoints, replay-attack prevention via sign-count tracking.

### Services & Profiles Management

- **Services tab**: quick filter (All/Running/Stopped/Failed), global health
  bar, inline metrics (CPU/Memory/Disk/NET), uptime display, restart button,
  boot icon, detail modal with session history, dual-line sparklines
- **Profiles tab**: health bar per tile, quick filter (All/Active/Idle), detail
  modal, instant activation (async, SSE-driven status updates)

### Audio Software Management

Quick filter (All/Installed/Updates), restart-required badge, documentation
links per package, per-arch support badges.

### Configuration Editor

Service status badges (Running/Stopped/Failed), diff preview before save,
restart-after-save toggle, backup management. Generic JSON/INI/XML/Libconfig
editor via CodeMirror.

### Systemd Overrides

RT presets (Audio Optimized / Reset to Defaults), OOM Score Adjust, CPU Weight,
diff preview before save.

### Performance Monitoring

CPU governor management, throttle detection badge, latency and network stability
tests with 10-result history, RT process monitor (SCHED_FIFO/RR detection).

### System Administration

Terminal (full interactive PTY shell in browser via WebSocket), backend restart,
OS reboot (with password confirmation), role-based access (admin/user/guest).

### Mobile & PWA

- Touch-first gesture navigation: edge swipes for sidebar/panel, vertical
  "molette" for fast tab cycling, gallery content swipe
- View Transitions API between tabs (direction-aware)
- GPU-accelerated gestures (will-change, RAF batching, passive listeners)
- In-app splash screen, offline indicator, intelligent cache warming
- iOS: safe-area insets, notch handling, rubber-band prevention, PWA splash
  screens (40 device-specific tags)

### Security

- mTLS / PKI: optional nginx mutual TLS client certificate authentication
- Guest role enforcement across all tabs and API endpoints
- CSP hardening, hidden source maps
- Security lock: blocks UI rendering without valid session

### Performance & Architecture

- Event-driven pipeline monitoring (inotify + D-Bus signals, replacing 2s
  polling — CPU drops to near zero at idle)
- Lazy loading, IntersectionObserver pause, Lit chunk splitting
- Backend: `orjson` (5× JSON), `uvloop`, Pydantic v2 `__slots__`, unified
  TTL cache, parallel pipeline construction
- Frontend: `content-visibility: auto` on inactive tabs, concurrent queue
  operations, MPD `command_list` batching, MPD `window` server-side limits
- 3 themes: Slate, Minimal, Gravity

### Codebase Quality

- 54 Lit 3.0 Web Components (Atomic Design: atoms/molecules/organisms/pages)
- Stylelint Phase 3: all CSS files lint-clean, Husky pre-commit hook
- Unified TTL cache replacing 15 ad-hoc implementations
- Dead code audit (frontend + backend), formatter consolidation
- Full CSS custom properties architecture with design tokens

---

## 0.9.0 — 2026-03-06

Full-stack rewrite. Frontend migrated from vanilla JS to **Lit 3.0 Web
Components** (54 components, Light DOM, Storybook 10, Vite 7). Backend moved to
**native D-Bus** (`dbus-fast`) with JWT authentication, adaptive monitoring
(2s→30s intervals, 40-60% CPU reduction at idle), and 9 modular FastAPI
services. Dual-layer security (API key + JWT RBAC), BCrypt hashing, role-based
access (Admin/User/Guest). WCAG 2.1 Level AA accessibility.
