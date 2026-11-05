---
title: "Chapter 1 · The Mathematics of Vibration: Where Sound Begins"
description: "From the spring oscillator to the Fourier series: taking sound apart into frequencies."
---

# Chapter 1 · The Mathematics of Vibration: Where Sound Begins

<div class="chapter-meta">
  <span>Estimated 45 minutes</span>
  <span>Prerequisite: Chapter 0</span>
  <span>Code: code/ch01_vibration.py</span>
</div>

The questions this chapter answers:

1. Why does a string vibrate at a fixed frequency instead of shaking about at random?
2. Why must a periodic signal have a discrete spectrum, while the power spectrum of ideal white noise is continuous?
3. Why do the Fourier coefficients of a square wave appear only at odd harmonics, and why do they decay as $1/n$?
4. Why does adding harmonics make the waveform look more like a square wave, without removing the overshoot near the jump?
5. When a piano and a violin play the same pitch, exactly which part of the spectrum accounts for the difference in timbre?

Chapter 0 said that pitch is the logarithm of a frequency ratio. But where does "frequency" itself come from? Why can an instrument produce one frequency steadily instead of a mess of random jitter? This chapter starts from the simplest mechanical model, reduces "sound" to a differential equation, and then decomposes its solution into a string of sine waves.

## 1.1 Simple Harmonic Motion and the Sine Wave: The Differential Equation of a Spring Oscillator

### 1.1.1 From Hooke's Law to a Second-Order Differential Equation

Consider an idealized system: a block of mass $m$ on a smooth horizontal surface, attached to a spring of stiffness $k$. Pull the block away from equilibrium by $x$ and the spring pulls it back, with restoring force

$$
F = -kx.
$$

The minus sign says the force always points opposite to the displacement. Ignoring friction and using Newton's second law $F = m\ddot{x}$, we obtain

$$
m\ddot{x} + kx = 0.
$$

This is the starting point of the chapter. It is a second-order linear homogeneous differential equation with constant coefficients; the unknown function is the position $x(t)$.

<Box kind="axiom" title="Postulate 1.1 (Linear restoring force)">

Near the equilibrium position the restoring force is proportional to the displacement: $F = -kx$. Basis: Hooke's law holds approximately in the **small-deformation** range of elastic elements; strings, membranes and air columns all satisfy it approximately when the amplitude is far smaller than the geometric scale. Failure boundary: at large amplitudes the material enters the nonlinear regime and the spring "stiffens" or "softens," and the period of vibration is no longer constant.

</Box>

This postulate matters: the entire conclusion "sine wave" is derived from "restoring force proportional to displacement." If the restoring force were $F = -kx^3$, the vibration would still be periodic, but no longer sinusoidal, and the period would depend on the amplitude.

### 1.1.2 The Form of the Solution

Guess a solution $x(t) = A\cos(\omega t + \varphi)$, where $A$ is the amplitude, $\varphi$ the initial phase, and $\omega$ the angular frequency to be determined. Differentiate twice:

$$
\dot{x} = -A\omega\sin(\omega t + \varphi), \qquad
\ddot{x} = -A\omega^2\cos(\omega t + \varphi) = -\omega^2 x.
$$

Substitute back into the equation:

$$
m(-\omega^2 x) + kx = (k - m\omega^2)x = 0.
$$

For this to hold for every $x$, we must have

$$
\omega = \sqrt{\frac{k}{m}}.
$$

So the solution really is sinusoidal, and the angular frequency is set by the system's "stiffness" and "mass." More mass means slower vibration; a stiffer spring means faster vibration.

<Box kind="definition" title="Definition 1.1 (Period, frequency, and angular frequency)">

For a periodic vibration $x(t)$, the smallest positive $T$ satisfying $x(t+T)=x(t)$ for all $t$ is the **period**, in seconds (s). The **frequency** is

$$
f = \frac{1}{T},
$$

in hertz (Hz), i.e. periods per second. The **angular frequency** is

$$
\omega = 2\pi f = \frac{2\pi}{T},
$$

in radians per second ($\text{rad/s}$). The three satisfy $\omega = 2\pi f$ and $T = 1/f$.

</Box>

<Box kind="theorem" title="Theorem 1.1 (General solution and uniqueness for simple harmonic motion)">

The general solution of $m\ddot{x} + kx = 0$ ($m, k > 0$) is

$$
x(t) = A\cos(\omega t + \varphi), \qquad \omega = \sqrt{\frac{k}{m}},
$$

where $A \ge 0$ and $\varphi$ are determined by the initial conditions. Given $x(0) = x_0$ and $\dot{x}(0) = v_0$, the solution is unique, and

$$
A = \sqrt{x_0^2 + \left(\frac{v_0}{\omega}\right)^2},
\qquad
\varphi = \operatorname{atan2}\!\left(-\frac{v_0}{\omega},x_0\right)
\quad (A>0).
$$

When $A>0$, $\varphi$ is unique modulo $2\pi$; when $x_0\ne0$ it can also be written $\tan\varphi=-v_0/(\omega x_0)$, but the tangent value alone cannot fix the quadrant. If $A=0$, then $x_0=v_0=0$ and the phase may be chosen freely.

</Box>

<Box kind="proof" title="Proof">

**General solution**: set $x = e^{\lambda t}$; substitution gives the characteristic equation $m\lambda^2 + k = 0$, i.e. $\lambda = \pm i\omega$ with $\omega = \sqrt{k/m}$. Hence the real general solution is $C_1\cos(\omega t) + C_2\sin(\omega t)$, which can be rewritten in the form $A\cos(\omega t + \varphi)$.

**Initial conditions**: from $x(0) = A\cos\varphi = x_0$ and $\dot{x}(0) = -A\omega\sin\varphi = v_0$, squaring and adding gives

$$
A^2 = x_0^2 + \left(\frac{v_0}{\omega}\right)^2.
$$

When $A>0$, $\cos\varphi=x_0/A$ and $\sin\varphi=-v_0/(\omega A)$ together determine $\varphi$ (modulo $2\pi$); this is the $\operatorname{atan2}$ form above. Using the tangent formula instead requires a separate quadrant check and separate handling of $x_0=0$. The case $A=0$ is the zero solution, where the phase does not affect the function.

**Uniqueness**: the solution of a second-order linear equation is uniquely determined by $x(0)$ and $\dot{x}(0)$ (existence and uniqueness theorem). $\blacksquare$

</Box>

### 1.1.3 Energy and Isochronism

Add the kinetic and elastic potential energies:

$$
E = \frac{1}{2}m\dot{x}^2 + \frac{1}{2}kx^2.
$$

Differentiate with respect to time and use $m\ddot{x} = -kx$:

$$
\dot{E} = m\dot{x}\ddot{x} + kx\dot{x}
= \dot{x}(m\ddot{x} + kx) = 0.
$$

So $E$ is conserved. At the equilibrium position $x=0$ the velocity is maximal, and $E = \frac{1}{2}m(A\omega)^2 = \frac{1}{2}kA^2$, proportional to the square of the amplitude.

One counterintuitive but crucial conclusion: **the period does not depend on the amplitude**. Pull the block out by 1 cm or by 5 cm, and as long as Postulate 1.1 holds, the period is exactly the same. This is called isochronism. A pendulum clock keeps time precisely because this property holds approximately at small angles; once the swing is too large, isochronism breaks down and the clock runs slow.

<Box kind="pitfall" title="Common misconception: higher frequency means more energy">

Frequency and energy are two different things. For a fixed simple harmonic oscillator, the energy is set by the amplitude $A$ ($E = \frac{1}{2}kA^2$) and the frequency by $k/m$; comparing different oscillators also requires comparing $k$. A high-frequency, small-amplitude vibration can carry far less energy than a low-frequency, large-amplitude one. Equating "high pitch" with "high energy" confuses frequency with loudness.

</Box>

### 1.1.4 From a Spring to a String

The spring oscillator is the minimal model, but its conclusions carry over directly to a string. For an ideal string of length $L$, tension $F_T$ and linear density $\mu$, the transverse wave speed is $c = \sqrt{F_T/\mu}$; a string fixed at both ends can hold only whole numbers of half wavelengths, so the frequency of the $n$-th mode is

$$
f_n = \frac{n}{2L}\sqrt{\frac{F_T}{\mu}}, \qquad n = 1, 2, 3, \dots
$$

This is the principle behind tuning a string instrument: tighten the string (increase $F_T$) and the frequency rises; press the string down (decrease $L$) and the frequency also rises. The $n$-th mode is exactly the $n$-th harmonic, which sets up the Fourier analysis of the next section. A real string has stiffness, so its harmonics deviate slightly from integer multiples; this is the piano's "inharmonicity," mentioned again in Section 1.3.

## 1.2 Spectrum and Timbre: The Fourier Series Expansion

### 1.2.1 Fourier Series of a Periodic Signal

A signal $x(t)$ with period $T$ can, under rather mild conditions, be written as

$$
x(t) = \frac{a_0}{2} + \sum_{n=1}^{\infty}\left(a_n\cos(2\pi nFt) + b_n\sin(2\pi nFt)\right),
\qquad F = \frac{1}{T}.
$$

The coefficients are given by inner products:

$$
a_n = \frac{2}{T}\int_0^T x(t)\cos(2\pi nFt)\,\mathrm{d}t, \qquad
b_n = \frac{2}{T}\int_0^T x(t)\sin(2\pi nFt)\,\mathrm{d}t.
$$

The $n=1$ component is the fundamental, and its frequency $F$ is the fundamental frequency; components with $n \ge 2$ are higher harmonics. Apart from the DC term $a_0/2$, every component is determined jointly by an amplitude and a phase. What the Fourier series says is: **a periodic signal can be decomposed completely into these discrete frequency components.**

### 1.2.2 The Square Wave: Odd Harmonics and 1/n Decay

Take the "hardest" periodic waveform: the square wave

$$
x(t) = \operatorname{sgn}\!\left(\sin(2\pi Ft)\right),
$$

which is $+1$ for half a period and $-1$ for the other half. This function is odd, so all cosine terms vanish and only sine terms remain.

<Box kind="theorem" title="Theorem 1.2 (Fourier coefficients of a square wave)">

For the square wave above,

$$
b_n =
\begin{cases}
\dfrac{4}{\pi n}, & n \text{ odd},\\[4pt]
0, & n \text{ even}.
\end{cases}
$$

That is, the square wave contains only odd harmonics, with amplitudes decaying as $1/n$.

</Box>

<Box kind="proof" title="Proof">

From the coefficient formula,
$$
b_n = \frac{2}{T}\left(\int_0^{T/2}\sin(2\pi nFt)\,\mathrm{d}t
- \int_{T/2}^{T}\sin(2\pi nFt)\,\mathrm{d}t\right).
$$
The first integral equals $\dfrac{1-\cos(\pi n)}{2\pi nF}$ and the second equals $\dfrac{\cos(\pi n)-1}{2\pi nF}$; their difference leaves $\dfrac{1-\cos(\pi n)}{\pi nF}$ in the bracket. Multiplying by $2/T = 2F$ gives

$$
b_n = \frac{2(1-\cos(\pi n))}{\pi n}.
$$

When $n$ is even, $\cos(\pi n)=1$ and $b_n=0$; when $n$ is odd, $\cos(\pi n)=-1$ and $b_n=4/(\pi n)$. $\blacksquare$

</Box>

This result has two testable corollaries: the even harmonics of a square wave are exactly zero; and for odd harmonic number $n$, the amplitude is $1/n$ of the fundamental's amplitude. Table 1 of Experiment 1.1 prints these numbers.

<Figure src="/figures/harmonics.svg" caption="Time domain and frequency domain are two faces of the same thing: the more odd harmonics are superposed, the closer the waveform comes to an ideal square wave; the spectrum on the right shows only odd components, with amplitudes decaying as 1/k." />

### 1.2.3 Sawtooth, Triangle, and Timbre

Different waveforms correspond to different harmonic structures:

- **Sawtooth**: all harmonics are present, with amplitudes decaying as $1/n$;
- **Triangle**: only odd harmonics, with amplitudes decaying as $1/n^2$, so it sounds "cleaner" than the square wave;
- **Square**: only odd harmonics, with amplitudes decaying as $1/n$, and the hardest edges.

Plot the harmonic amplitudes as a curve against $n$ and you get the **spectral envelope**. Most of the secret of timbre lies in the shape of this envelope: the faster the envelope falls, the fewer the high frequencies and the "rounder" the sound; a flat envelope means rich high frequencies and a "brighter" or "harsher" sound.

The difference between a piano and a violin is not only the slope of the envelope. A piano string's vibration has a time-varying envelope (a strong attack followed by decay), and because of string stiffness its harmonics deviate slightly from integer multiples; a violin body forms several resonances that boost certain bands. Neither is a "standard $1/n$ spectrum," but both can be described in the same Fourier language: **timbre = the distribution of harmonic amplitudes and phases as they change over time.**

<Figure src="/figures/timbre.svg" caption="A schematic of artificial envelopes: the blue curve's higher harmonics decay quickly, the orange curve keeps more high frequencies, illustrating how the spectrum relates to a “dark / bright” impression. The piano and violin labels in the figure are intuitive tags, not measured spectra; a real instrument cannot be distinguished by a single power-law envelope." />

<div class="audio-row">

<AudioDemo src="/audio/timbre-piano.wav" title="A harmonic envelope that decays quickly" hint="The higher harmonics fall off fast, so the sound leans “dark” — like the steady portion of a piano tone." />

<AudioDemo src="/audio/timbre-violin.wav" title="An envelope that keeps the higher harmonics" hint="With slight vibrato added and richer high frequencies, the sound leans “bright” — like a sustained string tone." />

</div>

<Box kind="pitfall" title="Common misconception: the Fourier coefficients are the timbre">

The Fourier coefficients describe the steady-state spectrum. A real note also has an attack, a decay, vibrato and noise components; these "transient" aspects matter just as much — sometimes more — for identifying timbre. A single steady-state spectrum cannot distinguish "a short piano strike" from "a long violin note," even if their harmonic envelopes look alike. Timbre is the joint distribution of spectrum and time structure.

</Box>

### 1.2.4 Machine Verification: The First Six Terms of a Square Wave

<Box kind="experiment" title="Experiment 1.1: Fourier coefficients, approximation error, and the waveform of a square wave">

```bash
python code/ch01_vibration.py
```

Real output (fundamental $F = 100\ \text{Hz}$, period $T = 10.0\ \text{ms}$):

The script prints its labels in Chinese; the numbers are unchanged.

::: details Expand full script output (74 lines, content unedited)

```text:no-line-numbers
ch01_vibration.py —— 第 1 章配套实验（基频 F = 100 Hz，周期 T = 10.0 ms）

表 1：方波的前 6 个非零傅里叶系数（n 为奇数）

     n      系数 c_n  相对基波振幅
----------------------------------
     1      1.273240         1.000
     3      0.424413         0.333
     5      0.254648         0.200
     7      0.181891         0.143
     9      0.141471         0.111
    11      0.115749         0.091

只出现奇次谐波；系数按 1/n 衰减，第 11 次谐波只剩基波振幅的 9.1%。

表 2：用部分和逼近方波（4096 个采样点，t 覆盖两个周期）

最高谐波 N        非零项数      RMS 误差  部分和峰值
----------------------------------------------------
1                        1        0.4352      1.2732
3                        2        0.3152      1.2004
5                        3        0.2587      1.1884
7                        4        0.2245      1.1842
9                        5        0.2010      1.1823
11                       6        0.1836      1.1813

项数越多，RMS 误差越小；但部分和峰值仍比理想振幅 1 高约 18%，
也就是过冲约 0.18 并不消失。这就是吉布斯现象：有限项和消不掉间断点附近的过冲。

图 1：一个周期内的波形（# 理想方波，. N=5 部分和，* 重合）

  1.4 |                                                        |
      |    ..                ..                                |
      |###*##**###******###**##*###                            |
      |  .     ...      ...     .                              |
      |                                                        |
      | .                        .                             |
      |                                                        |
      |.                          .                            |
  0.0 |                                                        |
      |                            .                          .|
      |                                                        |
      |                             .                        . |
      |                                                        |
      |                              .     ...      ...     .  |
      |                            ###*##**###******###**##*###|
      |                                ..                ..    |
 -1.4 |                                                        |

表 3：三种波形的谐波结构（系数绝对值）

    n        方波      锯齿波      三角波
-----------------------------------------
    1      1.2732      0.6366      0.8106
    2      0.0000      0.3183      0.0000
    3      0.4244      0.2122      0.0901
    4      0.0000      0.1592      0.0000
    5      0.2546      0.1273      0.0324
    6      0.0000      0.1061      0.0000

方波与三角波只有奇次谐波；锯齿波有全部谐波。
衰减速度：方波 1/n，锯齿波 1/n，三角波 1/n² —— 三角波最「干净」。

表 4：自相关——周期性的数值判据

  周期信号（T = 64 个采样点）：
    r(0)   = +1.000    r(T/2) = -0.600
    r(T)   = +1.000    r(2T)  = +1.000

  白噪声（512 个采样点，随机种子 7）：
    r(0)   = +1.000    r(128) = -0.024

理想周期信号在整数周期处应有 r(T) ≈ 1；这是重要线索，不是单独成立的充分判据。
实际判断还要结合多个滞后、信号长度与噪声；白噪声只在 lag = 0 处强相关，其他滞后接近 0。
```

:::

</Box>

Check four things:

1. In Table 1 the even harmonics are entirely absent; the coefficient at $n=3$ is $1/3$ of the fundamental's, and at $n=11$ it is $1/11 \approx 0.091$;
2. In Table 2 the RMS error falls monotonically from 0.4352 to 0.1836, yet the partial-sum peak falls only from 1.2732 to 1.1813, close to the theoretical limit $\approx 1.179$; only the part above the ideal amplitude 1 counts as overshoot;
3. In Figure 1 the edges of the ideal square wave are vertical jumps, while the $N=5$ partial sum oscillates and overshoots near the jumps — that is the Gibbs phenomenon;
4. In Table 4 the periodic signal has $r(T)=r(2T)=1$ and the white noise has $r(128)=-0.024$; the two give useful numerical clues, but a single $r(T)\approx1$ is not a sufficient criterion — with finite samples you must check several lags and the data length.

<Box kind="pitfall" title="Common misconception: a few more terms give a perfect square wave">

The RMS error does tend to zero, but the partial-sum peak does not return to the ideal amplitude 1, and the overshoot ratio does not tend to zero either. The Gibbs phenomenon says: when a jump is approximated by continuous sine waves, the maximum overshoot near the jump is about 9% of the whole jump amplitude (relative to the one-sided ideal amplitude 1, the peak is about 1.179). The location of the overshoot moves closer to the jump as more terms are added, which is why this does not contradict the RMS error going to zero. This is not badly written code; it is a mathematical property of the Fourier series. Real amplifiers also have bandwidth limits, so a "perfect square wave" does not exist physically.

</Box>

## 1.3 Noise and Musical Tone: Periodic vs. Non-Periodic

### 1.3.1 Autocorrelation: How to Decide Whether a Signal "Has a Period"

Judging periodicity from a waveform plot is not always reliable, especially when noise is mixed in. The more robust approach is autocorrelation. For a signal $x(t)$, define

$$
R_x(\tau) = \lim_{T \to \infty}\frac{1}{T}\int_0^T x(t)x(t+\tau)\,\mathrm{d}t,
\qquad
r_x(\tau) = \frac{R_x(\tau)}{R_x(0)}.
$$

$r_x(\tau)$ measures "how much the signal resembles itself after being shifted by $\tau$." For a signal with period $T$, $r_x(kT)=1$ (each period lines up exactly); for white noise, the correlation at every lag except $\tau=0$ is close to 0.

<Box kind="definition" title="Definition 1.2 (Periodicity and harmonicity)">

If there is a smallest $T > 0$ such that $x(t+T)=x(t)$ for all $t$, then $x$ is a **periodic signal** and $T$ is its minimal period. If the spectrum of $x$ has energy only at integer multiples of some common fundamental $F$, then $x$ is **harmonic**, and these frequency components are called harmonics.

In steady-state models satisfying the Fourier convergence conditions, strict periodicity ⇒ harmonicity; conversely, if the spectral coefficients are absolutely summable, harmonicity also ⇒ period $1/F$, though the minimal period may be shorter. Phase affects the waveform but does not break this periodicity. If amplitude, frequency or phase change over time, one should switch to a short-time spectrum and cannot apply this equivalence directly. Real musical tones are usually only "approximately periodic and approximately harmonic."

</Box>

### 1.3.2 Why a Periodic Signal Must Have a Discrete Spectrum

<Box kind="theorem" title="Theorem 1.3 (Periodic signals and discrete spectra)">

Let $x(t)$ be a signal with period $T$ that is absolutely integrable over one period and has only finitely many extrema and discontinuities (the Dirichlet conditions). Then the spectrum of $x$ consists only of components at the discrete frequencies

$$
f_n = nF = \frac{n}{T}, \qquad n \in \mathbb{Z}
$$

and the energy at all other frequencies is zero.

Conversely, if the spectrum of a steady-state signal falls **only** on integer multiples of some common fundamental $F$, and these coefficients are absolutely summable, then the signal has period $1/F$ (the minimal period may be shorter). What is discussed here is periodic power signals, not signals with finite energy on the infinite time axis.

</Box>

<Box kind="proof" title="Proof sketch">

**Forward**: by the Fourier series expansion,
$$
x(t) = \sum_{n \in \mathbb{Z}} c_n e^{i 2\pi n Ft},
$$
where $F=1/T$. Only the discrete frequencies $nF$ appear in this sum, so the spectrum is discrete.

**Converse**: if $x(t) = \sum_n c_n e^{i2\pi nFt}$ and $\sum_n \lvert c_n \rvert$ converges, then
$$
x(t+T) = \sum_n c_n e^{i2\pi nF(t+T)}
= \sum_n c_n e^{i2\pi nFt}e^{i2\pi n}
= x(t),
$$
because $e^{i2\pi n}=1$. Hence $x$ has period $1/F$. $\blacksquare$

</Box>

Note the two conditions in the theorem. The forward direction needs the Dirichlet conditions, or the Fourier series may fail to converge to the original signal; the absolute summability in the converse guarantees uniform convergence, making the sum continuous and allowing the time shift to be applied term by term. More importantly, the theorem concerns the ideal case of an "infinitely long, strictly periodic" signal. In reality we can observe only a finite duration, and windowing broadens an ideal spectral line into a peak of finite width; a rectangular window gives a sinc-shaped spectrum, and other windows have different main lobes and side lobes — the phenomenon is called **spectral leakage**. So "discrete" is a limiting concept, not pixels you can read off an oscilloscope.

Noise sits precisely on the other side of the theorem: the autocorrelation of ideal white noise is zero for $\tau \ne 0$, its **power spectral density** is continuous and flat, and no single frequency is "selected." Pink noise has a power spectral density decaying as $1/f$, still a continuous spectrum. Ideal white noise has no common fundamental and usually produces no stable, definite musical pitch; but noise processed by narrow-band filtering can still give a vague sense of pitch, so "continuous spectrum" must not be equated with "completely pitchless."

### 1.3.3 Harmonicity, Inharmonicity, and "Sounds Like an Instrument"

Real instruments mostly emit quasi-periodic signals, but the degree of "quasi" varies:

- **Strings and pipes**: in the ideal model the harmonics fall exactly at $nF$; a real piano string, because of stiffness, puts the $n$-th component above $nF$, with the deviation growing with $n$ — this is inharmonicity;
- **Percussion**: the partials of instruments such as the xylophone and the bell need not fall on a single integer-multiple series, which is also inharmonicity; inharmonicity changes timbre and pitch perception but does not mean the absence of pitch — a xylophone usually has a definite pitch, and a bell can be heard as having pitch too;
- **White noise**: has a continuous power spectrum and no stable harmonic structure, and is usually not heard as a definite musical tone; exceptions such as narrow-band noise can still produce a sense of pitch.

This also explains why "pitch" is not a purely objective quantity. The fundamental of a periodic signal is mathematically well defined, but whether a listener hears it as a note also depends on whether the harmonics fall inside the resolution units of the auditory system and whether they are strong enough. Chapter 2 translates "frequency" into "pitch coordinate," and Chapter 3 explains how overlapping harmonics affect the sense of consonance.

<div class="audio-row">

<AudioDemo src="/audio/tone-440.wav" title="A 440 Hz musical tone (6 harmonics)" hint="Discrete spectrum, definite fundamental → you hear one pitch." />

<AudioDemo src="/audio/noise.wav" title="White noise" hint="Continuous power spectrum, no stable period → usually no definite musical pitch, just a “hiss.”" />

</div>

<Box kind="pitfall" title="Common misconception: a discrete spectrum guarantees a pitch">

A strictly periodic click train repeating twice a second has, mathematically, discrete spectral lines spaced 2 Hz apart, yet no one hears a "2 Hz musical tone"; a discrete spectrum is only a condition on the signal, and a pitch must also fall inside the time and frequency ranges the auditory system can process effectively. Conversely, some narrow-band-filtered noise can give listeners a vague pitch. Pitch is a joint product of "signal structure + auditory system," and you cannot conclude from the spectrum alone.

</Box>

<Box kind="checkpoint" title="Self-check">

Close the book and do three things: (1) derive $\omega=\sqrt{k/m}$ and $T=2\pi\sqrt{m/k}$ from $m\ddot{x}+kx=0$; (2) without looking anything up, write the first three nonzero coefficients of a square wave and explain why the even terms vanish; (3) explain the difference between "periodic signal" and "white noise" in the language of autocorrelation.

</Box>

## 1.4 Summary

This chapter took sound apart on three levels:

$$
\underbrace{m\ddot{x}+kx=0}_{\text{mechanics}}
\;\longrightarrow\;
\underbrace{x(t)=A\cos(\omega t+\varphi)}_{\text{time domain}}
\;\longrightarrow\;
\underbrace{x(t)=\sum_n c_n e^{i2\pi nFt}}_{\text{frequency domain}}
\;\longrightarrow\;
\underbrace{\text{timbre} = \text{harmonic distribution}}_{\text{perception}}
$$

First, simple harmonic motion comes from a linear restoring force; its solution is sinusoidal, and the period is set by $k/m$, independent of amplitude. Second, the Fourier series of a periodic signal contains only discrete frequencies; a square wave contains only odd harmonics with coefficients decaying as $1/n$, and a triangle wave as $1/n^2$. Third, periodicity and harmonicity are the important mathematical foundation of "musical tone," while ideal white noise stands on the side of the continuous power spectrum; but a discrete spectrum alone does not guarantee a pitch, and a continuous spectrum does not absolutely exclude one.

The chapter also leaves two threads hanging: **the shape of the spectrum determines whether harmonics will interfere with one another**, which is the input to the roughness model of Chapter 3; and **the fact that harmonics fall near integer multiples** becomes, in Chapter 5, the harmonic template and consonance score used by the scale search.

Next chapter we replace the frequency axis with a logarithmic axis. You will see why "doubling" is an interval, why pitch can be arranged on a circle, and why the addition of intervals is really a group operation.

<Box kind="exercise" title="Exercises">

1. A spring oscillator has mass $m = 0.01\ \text{kg}$ and stiffness $k = 4\ \text{N/m}$. Find the angular frequency $\omega$, the frequency $f$ and the period $T$. If the amplitude doubles, do these three quantities change?
2. For a pure tone at 440 Hz, what is the period in milliseconds? What is the angular frequency in $\text{rad/s}$? Compute them separately with $T=1/f$ and $\omega=2\pi f$.
3. Using Theorem 1.2, compute the partial sum of the first three nonzero terms of a square wave at $t=T/4$ and compare it with the true value $+1$. What does the sign of the error tell you?
4. In Table 2 the RMS error keeps falling, but the partial-sum peak settles near 1.18 (relative to the ideal amplitude 1, an overshoot of about 0.18). Explain this difference with the Gibbs phenomenon. Would the overshoot survive if you used a triangle wave instead?
5. The normalized autocorrelation of an ideal steady-state signal satisfies $r(T)=0$ and $r(2T)=1$. Can you conclude that $T$ is not its period and that $2T$ is one? Must $2T$ be the minimal period? Explain.

</Box>

::: tip Next chapter
[Chapter 2](/en/chapters/02-pitch) replaces the frequency axis with a logarithmic one: $p = 1200\log_2(f/f_0)$. We will prove that "adding intervals" and "multiplying frequency ratios" are isomorphic, roll pitch up into a circle, and explain why the octave is the most stubborn equivalence relation in music.
:::
