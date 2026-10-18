# Real-time priority and reserved CPU cores for audio on Linux

**Short answer:** three tools, often mixed up. *Real-time priority* lets the player's threads go
first. *Pinning* keeps the player on chosen cores. *Reserving* keeps everything else off those
cores; pinning alone does not do that. What they buy is shorter, rarer delays when the player has
to wake up, and they matter most when the box is busy. MPD's own manual is plain about it:
real-time scheduling does not improve audio quality, it reduces the risk of skipping under heavy
load.

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
  half a second with its default settings (its own log, MPD 0.24.5), which the configuration
  Audiogravi<sup>ty</sup> writes leaves as they are. A delay of a few milliseconds leaves it far
  from empty. These figures matter when buffers are short, or when the box is busy with something
  heavy.

## Measuring your own box

```bash
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

- **Real-time priority and pinning, per service** (Systemd tuning, Pro). For each audio service:
  its cores, a real-time policy and priority, its CPU weight, I/O priority and memory lock. The
  *Audio Optimized* preset fills in `SCHED_FIFO` at 80, memory locked, I/O in real time, and a lower
  risk of being stopped when memory runs short. Everything is written as systemd drop-in files, the
  service's own file is never changed, and a setting a service cannot start with is refused or
  undone.
- **What runs in real time, at a glance** (Performance, Pro): the policy of the audio programs,
  the processor governor of each core, and a mark on a core the processor had to slow down.
- **The latency test**, from the interface: `cyclictest`, with its threads, priority, length and
  cores to choose. It runs with cyclictest's default, deep sleep held off, so its figures are on
  the good side of how the box runs.
- **What it does not do: reserve cores.** Audiogravi<sup>ty</sup> pins a service to its cores but
  does not keep other programs off them.

The details are in the manual:
[Administration → Performance tuning](../manual/07-administration#performance-tuning-pro), and
[Administration → Systemd tuning](../manual/07-administration#systemd-tuning-pro).

## Sources

- MPD and real-time scheduling, version 0.24: [user manual](https://github.com/MusicPlayerDaemon/MPD/blob/v0.24.5/doc/user.rst) ("There is a rumor that real-time scheduling improves audio quality. That is not true."); Debian 13's `mpd.service` (`LimitRTPRIO=40`).
- `SCHED_FIFO`: [sched(7)](https://manpages.debian.org/trixie/manpages/sched.7.en.html). systemd: [systemd.exec(5)](https://manpages.debian.org/trixie/systemd/systemd.exec.5.en.html), [systemd.resource-control(5)](https://manpages.debian.org/trixie/systemd/systemd.resource-control.5.en.html).
- Kernel parameters, Linux 6.12: [kernel-parameters](https://www.kernel.org/doc/html/v6.12/admin-guide/kernel-parameters.html); CPU isolation: [cpu-isolation](https://www.kernel.org/doc/html/v7.2/admin-guide/cpu-isolation.html).
- cyclictest: [cyclictest(8)](https://manpages.debian.org/trixie/rt-tests/cyclictest.8.en.html), and its `--help` (rt-tests 2.6).
- PREEMPT_RT: [Linux 6.12](https://kernelnewbies.org/Linux_6.12); Raspberry Pi's [real-time kernel notes](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/linux_kernel/patching.adoc).
