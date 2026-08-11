# Audiogravi<sup>ty</sup> — Release Notes

Synthesized overview of each release. For the full line-by-line changelog, see
[CHANGELOG.md](CHANGELOG.md).

---

## Unreleased

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
computer — the installer prints the address to fetch it from and the exact steps for
iPhone, Android, macOS and Windows, and the manual now has a chapter on it. After that
the box is trusted like any other site: no warnings, and the app installs normally.

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
