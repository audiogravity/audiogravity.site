# Real-time priority and reserved CPU cores for audio on Linux

**Short answer:** three tools, often mixed up. *Real-time priority* lets the player's threads go
first. *Pinning* keeps the player on chosen cores. *Reserving* keeps everything else off those
cores; pinning alone does not do that. What they buy is shorter, rarer delays when the player has
to wake up, and they matter most when the box is busy. MPD's own manual is plain about it:
real-time scheduling does not improve audio quality, it reduces the risk of skipping under heavy
load.

Checked on 2026-10-22 on an x86 box under Debian 13 and on a Raspberry Pi 4 under Raspberry Pi
OS (kernel 6.18); the latency figures were measured on 2026-10-17, on the x86 box.

## The three tools

- **Real-time priority.** A thread with the `SCHED_FIFO` policy takes the processor from any
  ordinary thread as soon as it is ready, at a priority from 1 to 99. With systemd:
  `CPUSchedulingPolicy=fifo` and `CPUSchedulingPriority=`. MPD already asks for it for its output
  thread, at priority 40, and Debian's MPD service grants it (`LimitRTPRIO=40`).
- **Pinning.** `CPUAffinity=` in a service's systemd settings keeps it on the cores you list.
  Other programs can still run there.
- **Reserving.** Keeping everything else off a core takes one of two things. The kernel parameter
  `isolcpus=`, set at boot (Linux 6.12's documentation marks it as deprecated in favour of
  cpusets). Or a *cpuset*, which systemd sets with `AllowedCPUs=` and which can change while the box
  runs. Two more boot parameters, `nohz_full=` and `rcu_nocbs=`, take the timer tick and some
  kernel housekeeping off those cores — on kernels built for it: Debian 13's are, Raspberry Pi OS's
  are not, so on a Pi `isolcpus=` works and those two have no effect.

Holding the player's memory in RAM, so that none of it is ever swapped out, is a fourth setting:
`LimitMEMLOCK=`.

## See what your player runs with

For MPD, one line per thread:

```bash
ps -L -o tid,cls,rtprio,comm -p "$(pidof mpd)"
```

`CLS` is the policy: `TS` ordinary, `FF` and `RR` real time (`SCHED_FIFO`, and `SCHED_RR`, which
takes turns at equal priority); `RTPRIO` is the priority. On my x86 box, shortened:

```text nocopy
    TID CLS RTPRIO COMMAND
 290953  FF     40 rtio
 290956  FF     40 output:Heed Aba
```

The thread named `output:` and the output's name, cut to 15 characters, is the one that feeds the
DAC, at the priority MPD asks for. The cores MPD may run on, and the cores reserved at boot (none
when the answer is empty):

```bash
taskset -cp "$(pidof mpd)"
cat /sys/devices/system/cpu/isolated
```

## Pin a player, reserve a core

To pin MPD to core 3, give its service a drop-in file: systemd's way of adding settings to a
service without changing the service's own file.

```bash
sudo systemctl edit mpd
```

Between the two comment lines at the top, write:

```text
[Service]
CPUAffinity=3
```

Save, then run `sudo systemctl restart mpd`: `taskset` now answers `current affinity list: 3`.
`CPUSchedulingPolicy=`, `CPUSchedulingPriority=` and `LimitMEMLOCK=` go in the same file.

To reserve that core on a Raspberry Pi, add ` isolcpus=3` at the end of the single line of
`/boot/firmware/cmdline.txt`, then restart the Pi:

```bash
sudo nano /boot/firmware/cmdline.txt
```

`cat /sys/devices/system/cpu/isolated` then answers `3`. On Debian with GRUB, the parameter goes
in `GRUB_CMDLINE_LINUX_DEFAULT`, in `/etc/default/grub`, followed by `sudo update-grub`. A reserved
core runs only what is pinned to it: reserve it without pinning anything, and it sits idle.

## What it changes, measured

On my x86 test box: Debian 13 with its standard kernel (6.12, not a real-time one), two of its four
cores reserved at boot (`isolcpus=2-3 nohz_full=2-3 rcu_nocbs=2-3 irqaffinity=0-1`). The other two
run everything else, device interrupts included, so the *Ordinary core* column describes this box,
not one that reserves no core; I have not measured one. Each run is one minute of `cyclictest` at
priority 99, waking every 100 µs; the figure is the worst delay seen (2026-10-17).

| Situation | Reserved core | Ordinary core |
|---|---|---|
| Box idle | 43 µs | 2,547 µs |
| The two ordinary cores fully loaded | 288 µs | 3,861 µs |
| Box idle, deep sleep allowed (`--default-system`) | 211 µs | 2,520 µs |

- **The ordinary core was late by more than 0.4 ms about once a second**, even with nothing to do
  (59 times in the minute); the reserved core, never.
- **Under load on the other cores**, the reserved core stayed under 0.3 ms.
- **What that means for sound: nothing audible.** MPD keeps a buffer of audio ahead of the DAC:
  half a second with its default settings (its own log, MPD 0.24.5). A delay of a few
  milliseconds leaves it far from empty. These figures matter when buffers are short, or when the box is busy with something
  heavy.

## Measuring your own box

`cyclictest` comes in the `rt-tests` package:

```bash
sudo apt install rt-tests
sudo cyclictest -p99 -t1 -i100 -l600000 -m -q -a3
```

That is one thread at priority 99 on core 3, for a minute. Read `Max`: the worst delay, in
microseconds. Two things to know about it:

- **cyclictest flatters the box by default.** It keeps the processor out of its deep sleep states
  while it measures (it writes 0 to `/dev/cpu_dma_latency`). Add `--default-system` to measure the
  box as it normally runs: on my test box, the worst delay of the reserved core went from 43 to
  211 µs.
- **Compare like with like**: the same core, the same length, the same load, before and after a
  change.

A real-time kernel (`PREEMPT_RT`) goes further still. It has been part of Linux since 6.12; Debian 13
offers one (`linux-image-rt-amd64`, `linux-image-rt-arm64`), and Raspberry Pi's repository has one
for the Pi 4. I have not measured them.

## With Audiogravi<sup>ty</sup>

Its **Systemd tuning** page (Pro) sets each audio service's cores, real-time policy and
priority, and memory lock, in drop-in files as above; its *Audio Optimized* preset fills in
`SCHED_FIFO` at 80. Its **Performance** page (Pro) shows what runs in real time and runs
`cyclictest` with cyclictest's default, deep sleep held off. It pins services to cores; it does
not reserve cores.

The details are in the manual:
[Administration → Performance tuning](../manual/07-administration#performance-tuning-pro), and
[Administration → Systemd tuning](../manual/07-administration#systemd-tuning-pro).

## Sources

- MPD and real-time scheduling, version 0.24: [user manual](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/user.rst) ("There is a rumor that real-time scheduling improves audio quality. That is not true."); Debian 13's `mpd.service` (`LimitRTPRIO=40`).
- `SCHED_FIFO`: [sched(7)](https://manpages.debian.org/trixie/manpages/sched.7.en.html). systemd: [systemd.exec(5)](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html), [systemd.resource-control(5)](https://manpages.debian.org/trixie/systemd/systemd.resource-control.5.en.html).
- Kernel parameters, Linux 6.12: [kernel-parameters](https://www.kernel.org/doc/html/v6.12/admin-guide/kernel-parameters.html); CPU isolation: [cpu-isolation](https://www.kernel.org/doc/html/v7.2/admin-guide/cpu-isolation.html).
- cyclictest: [cyclictest(8)](https://manpages.debian.org/trixie/rt-tests/cyclictest.8.en.html), and its `--help` (rt-tests 2.6).
- PREEMPT_RT: [Linux 6.12](https://kernelnewbies.org/Linux_6.12); Raspberry Pi's [real-time kernel notes](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/linux_kernel/patching.adoc).
