# “Undervoltage detected!” on a Raspberry Pi: what it does to a streamer, and how to check the supply

**Short answer:** when its supply sags below about 4.63 V, a Raspberry Pi slows its processor down
and the kernel writes `Undervoltage detected!` in its log. On the Pi 4 below, the processor fell from
1.8 GHz to 600 MHz while Linux still showed 1.8 GHz, and it happened 68 times a day, often within
seconds of a login. Playing a file kept up even then; heavier work has less room, and USB devices,
a DAC among them, share the low voltage. `vcgencmd get_throttled` tells whether it has happened. The
cure is the supply and its cable, not a setting.

Checked on 2026-10-26 on a Raspberry Pi 4 Model B under Raspberry Pi OS (Debian 13, Linux 6.18)
whose supply falls short: six days of its log, and a two-minute load test. The rest comes from
Raspberry Pi's documentation, its engineers and the kernel's sources.

## Has it happened on yours?

```bash
vcgencmd get_throttled
```

`throttled=0x0` means none of these has happened. Any other value adds them up, from Raspberry Pi's
documentation:

| Now | Has occurred | What |
|---|---|---|
| `0x1` | `0x10000` | Undervoltage |
| `0x2` | `0x20000` | Arm frequency capped |
| `0x4` | `0x40000` | Throttled |
| `0x8` | `0x80000` | Soft temperature limit |

On the Pi above, `0x50000` at rest: undervoltage and throttling have occurred, none is going on. It
still read so five minutes after the last drop. During a drop, `0x50005`: both are going on too.

The kernel's log gives the time of each drop:

```bash
journalctl -k --no-hostname | grep -i voltage
```

```text nocopy
Oct 26 09:43:29 kernel: hwmon hwmon1: Undervoltage detected!
Oct 26 09:43:50 kernel: hwmon hwmon1: Voltage normalised
```

- **One pair of lines per drop.** The kernel asks the firmware every two seconds and writes a line
  each time the state changes. To count the drops since the Pi started:
  `journalctl -k -b | grep -c "Undervoltage detected"`.
- **The same alarm, without `vcgencmd`:** `grep -H . /sys/class/hwmon/hwmon*/in0_lcrit_alarm` reads
  `1` while a drop lasts, `0` otherwise.
- **On the desktop**, Raspberry Pi OS shows a notification, "Low voltage warning", over "Please check
  your power supply".
- **Where none of this exists.** `vcgencmd` comes with Raspberry Pi OS and DietPi, in the
  `raspi-utils-core` package. Debian's own packages have neither it nor the kernel's driver, which
  Debian 13 leaves out of its arm64 kernel: there, what is left is the red power LED of a Pi 1 to 4,
  "off or flickering when there is undervoltage", and a multimeter (below). The Zero range has no
  detection circuit at all.

## What it does

In Raspberry Pi's documentation: "If the voltage drops below 4.63 V (±5%), the Arm cores and the GPU
are throttled back, and a message indicating the low voltage state is added to the kernel log."
To watch it happen:

```bash
watch -n 1 'vcgencmd measure_clock arm; vcgencmd get_throttled'
```

What the Pi above did, with three of its four cores kept busy:

- **The processor ran at a third of its speed.** `measure_clock arm` read `frequency(48)=600117184`,
  600 MHz, within a tenth of a second of the load starting, while Linux's own figure,
  `/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`, still read `1800000`. The documentation
  explains it: that figure "is the kernel requested frequency", and `measure_clock` gives the actual
  one. Tools that show Linux's figure do not see the slowdown.
- **It came back at once.** 1.8 GHz again within 0.2 s of the load stopping; the kernel wrote
  `Voltage normalised` about four seconds later.
- **Playing a file kept up.** One core decoded a 24-bit, 192 kHz FLAC file of noise, the hardest
  kind for FLAC, 64 times faster than it plays at 1.8 GHz, and still 25 times faster at 600 MHz with
  the other cores busy. Work that needs far more of the processor, heavy resampling or HQPlayer's
  filters, gets a third of it while a drop lasts.
- **Storage and USB devices share the low voltage.** Raspberry Pi's documentation: "Low quality power
  supplies can corrupt storage or cause unpredictable behaviour", and "often problems with USB
  devices are caused by power issues". One of its engineers adds that below 4.75 V, the edge of the
  USB specification, "USB devices are likely to malfunction".

How often, on that Pi, over six days of log: 404 drops, 68 a day, from 4 seconds to over 5 minutes
(half of them 6 seconds or less, nine over a minute). They followed activity: 16 between midnight and
7 a.m., and nearly one login in two was followed by one within ten seconds (162 of 347).

## The supply, and what it feeds

Raspberry Pi's requirements:

| Model | Supply | Shared by the USB ports |
|---|---|---|
| Pi 3 B+ | 5.1 V, 2.5 A, micro USB | 1.2 A |
| Pi 4, Pi 400 | 5.1 V, 3 A, USB-C | 1.2 A |
| Pi 5 | 5.1 V, 5 A, USB-C | 1.6 A, or 600 mA from a 3 A supply |

- **The cable counts.** The documentation's figures are "measured at the plug, not the supply":
  "Allow for voltage loss in the cable", it says, and it names wires "that are too thin" among the
  causes. Raspberry Pi's own supplies come with 1.2 to 1.5 m of
  17 or 18 AWG cable. It adds that "the voltage from some USB chargers/power supplies can fall as low
  as 4.2 V", where 4.8 V is the floor "for reliable performance".
- **Count what the Pi feeds.** A DAC, a disk or a hub powered through its USB cable draws on the
  column above, from the same supply. `lsusb -v` shows what each device declares: the DAC of my x86
  test box reads `(Bus Powered)` and `MaxPower 500mA`, so its USB side may take up to 500 mA from the
  port. To rule power out, Raspberry Pi's documentation advises connecting USB devices "using a
  powered hub".
- **A Pi 5 needs 5 A to feed its USB ports fully.** Without a supply that offers 5 A, its desktop
  warns "This power supply is not capable of supplying 5A", over "Power to peripherals will be
  restricted".
  `usb_max_current_enable=1` in `config.txt` lifts the limit, under the documentation's warning that
  it "can cause system instability, crashes, or data loss": for a USB-powered DAC, the 5 A supply is
  the better fix.
- **Reading the voltage.** A Pi 5 reads its own: `vcgencmd pmic_read_adc EXT5V_V` answers, in the
  documentation's example, `EXT5V_V volt(24)=5.06520000V`. On older models, `vcgencmd measure_volts`
  gives the processor's voltage, not the supply's, and the documentation sends you to a multimeter
  between the 5 V and ground pins. A multimeter shows the average: "it won't pick up momentary
  dropouts", in the words of the same engineer, and the Pi's own detection does.

## Settings that hide it

- **`avoid_warnings=2`** "allows turbo mode even when low-voltage is present". Raspberry Pi files it
  among the `config.txt` options that "don't work with Raspberry Pi OS Bookworm and later", and it
  never mended the supply.
- **DietPi's `cpu` command** prints a "Throttle up" line: that is the frequency governor's threshold,
  not the slowdown above.

## With Audiogravi<sup>ty</sup>

On a Raspberry Pi, its Performance tab marks every core THROTTLED when the supply could not keep up,
and, with notifications on, the box sends "Power Supply Too Weak" as the voltage drops, at most once a
day.

The details are in the manual:
[Administration → Performance tuning](../manual/07-administration#performance-tuning-pro) and
[Push notifications](../manual/07-administration#push-notifications).

## Sources

- Raspberry Pi's documentation, read on 2026-10-26 from [its repository](https://github.com/raspberrypi/documentation), which mirrors the website: [power supplies](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/power-supplies.adoc) (the 4.63 V threshold, the requirements, the causes and consequences), [setting up](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/getting-started/setting-up.adoc) (voltage measured at the plug), [vcgencmd](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/os/graphics-utilities.adoc) (`get_throttled`, `measure_clock`, `measure_volts`, `pmic_read_adc`), [overclocking](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/config_txt/overclocking.adoc) (throttling, 4.8 V, the requested frequency), [USB](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/raspberry-pi/usb-bus-on-raspberry-pi.adoc) (current per port), [performance](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/configuration/performance.adoc) (`usb_max_current_enable`), [LED warnings](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/configuration/led_blink_warnings.adoc), [legacy options](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/legacy_config_txt/misc.adoc) (`avoid_warnings`); the product briefs of the [27 W](https://datasheets.raspberrypi.com/power-supply/27w-usb-c-power-supply-product-brief.pdf) and [15 W](https://datasheets.raspberrypi.com/power-supply/15w-usb-c-power-supply-product-brief.pdf) supplies (cables).
- Raspberry Pi engineers on GitHub: Phil Elwell on [`0x50000`](https://github.com/raspberrypi/linux/issues/2459#issuecomment-375332847) (2018); Dave Stevenson on [brief drops, multimeters and USB](https://github.com/raspberrypi/linux/issues/5584) (August 2023).
- The desktop's messages: [pplug-power](https://github.com/raspberrypi-ui/pplug-power/blob/master/src/power.c), Raspberry Pi OS's power plugin.
- Linux 6.12: the messages and the two-second polling in [drivers/hwmon/raspberrypi-hwmon.c](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/drivers/hwmon/raspberrypi-hwmon.c?h=v6.12) and [its documentation](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation/hwmon/raspberrypi-hwmon.rst?h=v6.12). Debian 13: `CONFIG_SENSORS_RASPBERRYPI_HWMON` not set in its arm64 kernel 6.12.113, and no `vcgencmd` in [its packages](https://packages.debian.org/search?searchon=contents&keywords=vcgencmd&mode=filename&suite=trixie&arch=any). DietPi: [dietpi-cpuinfo](https://github.com/MichaIng/DietPi/blob/master/dietpi/dietpi-cpuinfo).
- Measurements, 2026-10-26: a Raspberry Pi 4 Model B Rev 1.5, Raspberry Pi OS (image of 2026-04-21) on Debian 13, Linux 6.18.50, firmware of 2026-09-14, nothing on its USB ports; its kernel log from 2026-10-20 to 26; the load test with busy loops and ffmpeg 7.1. The USB DAC's declaration read with `lsusb` (usbutils 018) on the x86 test box, Debian 13. Nothing was measured on a Pi 5.
