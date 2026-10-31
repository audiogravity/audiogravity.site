# A streamer into an amplifier with DIN inputs: the cable, the level, the volume

**Short answer:** many European amplifiers of the 1970s and 1980s, and Naim's up to its latest
integrated amplifiers, take their sources on round 5-pin DIN sockets rather than RCA. A DAC
connects to them with a cable that has RCA plugs at one end and a DIN plug wired for that
amplifier at the other. Which pin carries what is not the same everywhere, so read the
amplifier's manual first. These inputs often expect far less than a DAC sends: the volume knob
then does its work in the first part of its travel, which is expected, not a fault.

Checked on 2026-10-31 against Naim's manuals for the NAIT 2, its integrated amplifiers of 2019
and the NAIT 50, a DAC board's datasheet and the Linux driver of its chip, with `speaker-test`
from alsa-utils 1.2.14 on Debian 13.

## Which pin carries what

A 5-pin DIN socket has its five contacts on a half circle. In the scheme most often given for an
amplifier's socket, the amplifier receives the left and right channels on pins 3 and 5, sends a
signal out, to a tape recorder, on pins 1 and 4, and has its ground on pin 2. Makers departed from
it:

- some took a source's signal on pins 1 and 4;
- some fed power on pins 3 and 5, to an external phono stage or to a tuner;
- Philips and Uher tape recorders used every pin as an input while recording.

So a cable that plays on one amplifier may give a single channel, or nothing, on another. And a
socket that carries power must not see its pins joined by a cable wired for something else: on
Naim's SUPERNAIT 3 and NAIT XS 3, the **aux 2** socket "also carries a power supply output
intended to power a Naim StageLine or SuperLine phono preamplifier".

What to do:

1. **Read the amplifier's manual.** Naim's draw the sockets with what each contact carries: `ch1`
   for the left channel, `ch2` for the right, `-ve` for the ground, `nc` for nothing.
2. **Get a cable made for that make**, RCA at the DAC's end and DIN at the amplifier's. TNT-Audio
   advises such a cable over an RCA-to-DIN adapter.
3. **Or check the cable you have**, the amplifier off and the cable out: with a multimeter set to
   continuity, each RCA plug's centre pin must beep with the contact the manual gives for its
   channel, and each plug's outer ring with the ground.

## How much a DAC sends, and what the input expects

A line input's **sensitivity** is the level that drives the amplifier to full power with its
volume turned all the way up. A DAC's datasheet gives its own output at full scale. Two figures
from the makers:

| | Level |
|---|---|
| Naim NAIT 2, line inputs (Tuner, Aux, Tape) | 75 mV |
| Naim NAIT 50, line inputs, level at clipping | 88 mV |
| HiFiBerry DAC+ Pro, a DAC board for the Raspberry Pi, maximum output | 2.1 V |

The DAC board sends 28 times the NAIT 2's 75 mV, about 29 dB more. The amplifier reaches full power
with its knob far from the top, and the part of its travel you use is short. That is expected, not
a fault.

**Never connect a DAC to a phono input**, DIN or RCA. A phono stage is made for a cartridge: 2.5 mV
on the NAIT 2, 840 times less than the board above.

## Where to set the volume

- **On the amplifier, with the streamer at 100 %.** Your music reaches the DAC untouched, and the
  amplifier's knob sets the level (see
  [How to check bit-perfect playback](check-bit-perfect-playback-linux)).
- **On the DAC's own analogue control, if it has one.** Boards built on Texas Instruments' PCM512x
  chips have a control the Linux driver names `Analogue Playback Volume`, with two steps: 0 and
  −6 dB. It lowers the output without changing a sample. The HiFiBerry DAC+ is one: its Linux
  overlay declares a PCM5122.
- **In the player.** A software volume below 100 % recalculates every sample (see
  [Software or hardware volume on a Linux streamer](software-hardware-volume-linux)).

## Check both channels

Do this once the cable is in, before any music. Turn the amplifier's volume right down first: the
test is at a fixed level, and these inputs are sensitive. Stop the player that holds the DAC, MPD
for instance (see [“Device or resource busy”](device-or-resource-busy-dac)), then, with your DAC's
card number from `aplay -l` in place of `0`:

```bash
speaker-test -D plughw:0,0 -c 2 -t wav -l 1
```

A voice says "Front left", then "Front right", and the terminal shows which it is playing:

```text nocopy
 0 - Front Left
 1 - Front Right
```

Raise the volume slowly. Each voice must come from its own speaker. The two swapped: the cable's
channels are crossed. One of them silent: the cable does not reach the right contacts.

## With Audiogravi<sup>ty</sup>

Its guided setup gives MPD a software volume: leave the player's slider at 100 and set the level
with the amplifier's knob. The details are in the manual: [Listening](../manual/04-listening).

The NAIT 2, one of these amplifiers, has its own story in the blog:
[The Naim NAIT 2](../blog/naim-audio-nait-2).

## Sources

- The usual use of a 5-pin DIN socket on an amplifier, and the makers who departed from it: [DIN connector](https://en.wikipedia.org/wiki/DIN_connector), Wikipedia, section "Analog audio", read on 2026-10-31. Its table cites a Soviet handbook of 1983; the section itself is marked as lacking references.
- Naim: the NAIT 2's owner's manual, inputs and sensitivities on pages 8–9; [Integrated amplifiers manual, issue 3B](https://dam.focal-naim.com/m/6d2ba0ea6c735cd8/original/Integrated-Amps-English-Issue-3B_0-pdf.pdf), for the SUPERNAIT 3, NAIT XS 3 and NAIT 5si: socket drawings and the aux 2 power supply on pages E3 and E5; [NAIT 50 user guide](https://dam.focal-naim.com/m/600f931144c0c6c7/original/User_Guide_Nait_50_web-pdf.pdf), DIN inputs of 47 kΩ and 88 mV on its specifications page.
- HiFiBerry DAC+ Pro: ["Maximum output voltage 2.1Vrms"](https://www.hifiberry.com/docs/data-sheets/datasheet-dac-pro/), read on 2026-10-31; its chip, declared in the Raspberry Pi kernel's [hifiberry-dacplus overlay](https://github.com/raspberrypi/linux/blob/rpi-6.12.y/arch/arm/boot/dts/overlays/hifiberry-dacplus-overlay.dts).
- The PCM512x analogue control: Linux 6.12, [pcm512x.c](https://github.com/torvalds/linux/blob/v6.12/sound/soc/codecs/pcm512x.c), `Analogue Playback Volume` with a range of −6 to 0 dB in one step.
- TNT-Audio, March 2003: Lucio Cadeddu, ["Naim Nait 1 – A living legend"](https://www.tnt-audio.com/ampli/nait_e.html), on RCA-to-DIN cables and adapters.
- `speaker-test`: [speaker-test(1)](https://manpages.debian.org/trixie/alsa-utils/speaker-test.1.en.html), Debian 13; its output above was taken on 2026-10-31 by playing to ALSA's null device, with no sound card opened.
