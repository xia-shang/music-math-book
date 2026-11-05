---
title: "Chapter 3 · Consonance and Dissonance: A Physical Account"
description: "Using beats, critical bands, and a roughness model to turn 'consonance' from an adjective into a computable function."
---

# Chapter 3 · Consonance and Dissonance: A Physical Account

<div class="chapter-meta">
  <span>Estimated 45 minutes</span>
  <span>Prerequisite: Chapters 1 and 2</span>
  <span>Code: code/ch03_consonance.py</span>
</div>

In traditional music theory, the teacher tells you that "a perfect fifth is consonant, an augmented fourth is dissonant." But you may ask: **on what grounds?** Is this merely cultural habit?

The answer: **it cannot be explained by cultural habit alone, and the sense of consonance cannot be reduced entirely to a single physical formula.** This chapter first separates out three layers that can be computed:

1. **Physical layer**: two notes vibrate at once, their waveforms superpose and produce beating; certain difference-frequency ranges make the auditory system perceive "roughness";
2. **Physiological layer**: the frequency resolution of the human basilar membrane is not linear. Whether a pair of components is likely to sound rough depends not on the Hz difference alone, but on the ratio of that difference to the critical bandwidth;
3. **Mathematical layer**: when the frequency ratio is a simple integer ratio, the two harmonic series coincide at low order, and the corresponding beat terms are 0; this does not mean every other harmonic pair is beat-free.

The task of this chapter is to write these three layers as one function:

$$
\text{Consonance}(f_1, f_2) \;=\; \frac{1}{1 + D(f_1,f_2)}
$$

where $D$ is the roughness computed from the first two layers. By the end of this chapter you will hold a formula that can score **any** interval (including microtonal ones), instead of a table of consonances to memorize.

## 3.1 Beats and Roughness: The Auditory Effect of Interference

### 3.1.1 Superposition of Two Sine Waves

Start with the simplest case: two pure tones at frequencies $f_1$ and $f_2$, both with amplitude $A$. The sum-to-product identity gives:

$$
A\sin(2\pi f_1 t) + A\sin(2\pi f_2 t)
= 2A \cos\!\left(2\pi \frac{f_1 - f_2}{2} t\right)
  \sin\!\left(2\pi \frac{f_1 + f_2}{2} t\right)
$$

The resulting physical picture is clean: a **high-frequency carrier** (at the average of the two frequencies) is modulated by a **low-frequency envelope**, whose frequency is

$$
f_{\text{beat}} = |f_1 - f_2|.
$$

<Box kind="definition" title="Beat frequency">

When two pure tones at $f_1, f_2$ superpose, the amplitude envelope of the combined wave varies at $f_{\text{beat}} = |f_1 - f_2|$, in Hz. $f_{\text{beat}}$ is independent of the average of the two frequencies; only the difference matters.

</Box>

Equal amplitudes make the envelope formula above especially simple; with unequal amplitudes the combined wave still fluctuates at the difference frequency, but the envelope no longer drops to 0. Real instruments contain many harmonics, and here the beats must be computed **pair by pair** between harmonics — which is exactly what Section 3.3 does.

### 3.1.2 From "Wobble" to "Roughness" to "Separation"

Beating itself is not a bad thing. For two pure tones that fall within the same auditory analysis channel, we can draw the following qualitative distinction:

| Relation between frequency difference and auditory bandwidth | Subjective impression | Typical situation |
| --- | --- | --- |
| Slow beating | Regular rises and falls in loudness | Slight detuning in unison singing, vibrato |
| Beating enters the roughness-sensitive region | **Roughness**, harsh, itchy | Dissonant intervals, an out-of-tune piano |
| Frequency separation far exceeds the auditory bandwidth | The two pitches separate; roughness fades | Two notes far apart |

Here there is **no 15 Hz or 400 Hz threshold that works across registers**: the boundary varies with center frequency, loudness, and timbre. This chapter does not use a fixed table of Hz ranges; it describes this variation continuously with the critical bandwidth and roughness kernel below. They are inputs to the model, not results derived from it.

<Box kind="pitfall" title="Common misconception: faster beats sound worse">

Wrong. As the frequency difference grows further and the auditory system separates the two components, roughness actually decreases. What needs to be compared is the size of $\Delta f$ relative to the critical bandwidth, not a single "fastest beat" threshold applied to every register.

</Box>

Before deriving further, run a unit test with your ears. The four audio clips below are all six-harmonic complexes on the root C4: the first two are perfect fifths, the last two major thirds; in each pair the first uses just intonation and the second 12-TET.

<div class="audio-row">

<AudioDemo src="/audio/fifth-just.wav" title="Just perfect fifth 3:2" hint="The harmonics coincide exactly; you can barely hear any fluctuation — this is where 'clean' comes from." />

<AudioDemo src="/audio/fifth-tet.wav" title="12-TET perfect fifth 700 ¢" hint="The 5th and 3rd harmonics are offset by about 2 ¢; listen closely for a slight wobble." />

</div>

<div class="audio-row">

<AudioDemo src="/audio/third-just.wav" title="Just major third 5:4" hint="5:4 aligns exactly; the timbres fuse." />

<AudioDemo src="/audio/third-tet.wav" title="12-TET major third 400 ¢" hint="Off by 13.7 ¢, a beat of about 3 Hz: clearly 'wobbling'." />

</div>

### 3.1.3 Why "Rough" Rather Than "Buzzy"

From a signal-processing perspective, the basilar membrane can be viewed roughly as a row of bandpass filters with different center frequencies. When the frequency difference between two tones is smaller than some bandwidth, they fall into the same filter and trigger a "competition" within the same cluster of hair cells; what the brain receives is not two pitches but a mixed signal whose amplitude fluctuates violently — that is the origin of roughness.

This bandwidth is the critical band of the next section.

## 3.2 The Critical Band: Why the Bass Register Is More "Picky"

### 3.2.1 A Counterintuitive Phenomenon

First fix the frequency difference at 100 Hz, and use the kernel below to compute the normalized distance of two pure-tone pairs (results first; the formulas are defined in 3.2.2 and 3.3.2):

- 440 Hz and 540 Hz: $x = 100/(0.25\,\mathrm{CB}(440)) \approx 2.975$, $W \approx 0.00345$;
- 2000 Hz and 2100 Hz: $x \approx 1.914$, $W \approx 0.2556$.

Under this set of model parameters, **the high-register case is actually rougher**, so "bass is nearly unbearable, treble is only mildly abrasive" cannot be taken as a general law. The critical bandwidth does widen with center frequency, which makes $x$ decrease as the register rises; but the roughness kernel first increases and then decreases, and a smaller $x$ does not always mean a smaller $W$. Bass is often considered harder to arrange in harmony; that should be discussed in terms of the specific interval, register, and spectrum, not reduced to "a fixed Hz difference is harsher in the bass."

### 3.2.2 Empirical Formula for the Critical Band

The approximate formula measured by Zwicker et al. in masking experiments is the postulate adopted in this book:

<Box kind="axiom" title="Postulate 3.1 (critical bandwidth)">

$$
\mathrm{CB}(f) \approx 94 + 71.3 \cdot \left(\frac{f}{1\ \text{kHz}}\right)^{0.69}\ \text{Hz}
$$
where $f$ is in Hz. The formula holds approximately over $100\ \text{Hz} \sim 5\ \text{kHz}$; the error is larger at the low end.

**Dimensional reminder**: the $f$ inside the parentheses must be inserted in kHz, or the numbers will be absurd. In code, the safest form is to divide by 1000 first.

</Box>

Inserting a few values immediately reveals the nonlinearity:

| $f$ (Hz) | 220 | 330 | 440 | 880 | 2000 | 4000 |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{CB}(f)$ (Hz) | 119.1 | 127.2 | 134.5 | 159.3 | 209.0 | 279.6 |

$f$ rises from 220 Hz to 2000 Hz (about 9×), while $\mathrm{CB}$ rises only from 119 Hz to 209 Hz (about 1.76×). In other words: **relative resolution is finer in the bass**. This is the mathematical expression of "bass is harder to manage."

<Box kind="theorem" title="Theorem 3.1 (piecewise behavior of roughness under a fixed Hz difference)">

Let two pure tones have frequencies $f$ and $f + \Delta f$, with $\Delta f > 0$ fixed, and define
$$
x(f) = \frac{\Delta f}{0.25\,\mathrm{CB}(f)}.
$$
Then $x(f)$ decreases strictly with $f$, but $W(x)=x^2e^{1-x^2}$ is not monotone in $f$: for $x>1$, $W$ **increases** as $f$ increases; for $0<x<1$, $W$ **decreases** as $f$ increases; at $x=1$ roughness reaches its peak.

</Box>

<Box kind="proof" title="Proof">

By Postulate 3.1, $\mathrm{CB}(f)$ is strictly increasing, so $x(f)$ is strictly decreasing. On the other hand,
$$
W'(x)=2x(1-x^2)e^{1-x^2}.
$$
Hence $W(x)$ increases for $0<x<1$ and decreases for $x>1$. Increasing $f$ moves $x$ to the left: on the right side of the peak this moves toward the peak, so $W$ rises; on the left side this moves toward 0, so $W$ falls. What is always monotone is the normalized distance $x$; it cannot be equated directly with roughness. $\blacksquare$

</Box>

<Box kind="pitfall" title="This is not 'broken ears'">

The variation of the critical band with frequency is a feature of auditory filtering, not a fault. A wider absolute bandwidth and a narrower relative resolution $\mathrm{CB}(f)/f$ can hold at the same time; whether something sounds rougher still depends on which side of the kernel it falls.

</Box>

### 3.2.3 An Intuitive Conversion

It is more convenient to express the critical band in cents. At $f = 440$ Hz, $\mathrm{CB}(440) \approx 134.5$ Hz. Compute the interval between 440 Hz and $440 + 134.5 = 574.5$ Hz using the logarithmic definition:

$$
1200 \log_2 \frac{574.5}{440} \approx 462\ \text{cent},
$$

roughly the width of a perfect fourth (498 cents).

There is a trap here: since 1 cent near 440 Hz is about $0.254$ Hz, dividing directly, $134.5 / 0.254$, gives 529 cents. The two answers differ by 67 cents because cents are a geometric scale while Hz is a linear one; the linear approximation requires $\Delta f/f$ to be sufficiently small, not merely the interval to be less than an octave. At 100 Hz, this division turns a bandwidth of 108.6 Hz into 1879 cents, whereas the logarithmic definition gives only 1273 cents — a difference of about 606 cents.

This conversion provides only an intuition: near 440 Hz, one critical bandwidth already spans a fairly wide frequency range. Real auditory filters do not have neat brick-wall edges, and whether two components affect each other still depends on center frequency, loudness, and spectrum; therefore "460 cents" cannot be taken as a universal consonance threshold for all registers, nor can it be used to deduce how many degrees a scale can be subdivided into.

## 3.3 From Integer Ratios to a Consonance Function

### 3.3.1 Harmonic Coincidence: Why Integer Ratios Are Consonant

Let the fundamental be $F$, and let the two notes be $mF$ and $nF$, with $m,n$ integers.

<Box kind="definition" title="Harmonic coincidence">

The $i$-th harmonic means the component at frequency $iF$ ($i \ge 1$). If there exist positive integers $i,j$ such that $i \cdot (mF) = j \cdot (nF)$, the $i$-th and $j$-th harmonics of the two notes are said to **coincide**. Coincidence is equivalent to $\frac{i}{j} = \frac{n}{m}$, so as long as the ratio is rational, coincidence must occur at finite harmonic order; the "simpler" the ratio (the smaller $m,n$), the earlier coincidence occurs and the more harmonic pairs participate.

</Box>

For the perfect fifth $3:2$: $f_1 = 3F$, $f_2 = 2F$. The 2nd harmonic ($6F$) coincides exactly with the other note's 3rd harmonic ($6F$), and the beat frequency is 0. That is why the fifth sounds "clean."

<Box kind="theorem" title="Theorem 3.2 (rational ratio ⇒ common period and some zero beat frequencies)">

If $f_2 / f_1 = m/n$ is rational (in lowest terms), then the combined signal has period $T = 1/(f_1/n)$; the harmonics of both notes fall on integer multiples of the common fundamental $f_1/n$, and there are infinitely many coinciding harmonic pairs. The beat frequency of each coinciding pair is 0; this does not mean every harmonic pair coincides, nor does it by itself guarantee that the total roughness is low.

</Box>

<Box kind="proof" title="Proof">

Since $f_1 = n \cdot (f_1/n)$ and $f_2 = m \cdot (f_1/n)$, both are integer multiples of $g = f_1/n$. Hence for every positive integer $a$, the $an$-th harmonic of $f_1$ and the $am$-th harmonic of $f_2$ both have frequency $amn \cdot g$: exact coincidence, zero beat. All frequency components of the combined signal are integer multiples of $g$, so $1/g$ is a period. $\blacksquare$

</Box>

Low-order coincidence is an important reason why simple integer ratios tend to be more consonant, but the model in this chapter also computes **the distances between non-coinciding harmonics**. Few coincidences do not necessarily mean a low total score, and many do not necessarily mean a high one; you have to add up every term with its amplitude weight to know.

<Figure src="/figures/harmonic-comb.svg" caption="Two harmonic series on the same frequency axis. The cyan vertical bands mark spectrum lines that coincide exactly; the distances between the remaining lines determine roughness. 3:2 coincides near 660 Hz and 5:4 near 1100 Hz — the earlier the coincidence, the cleaner the low harmonics." />

### 3.3.2 Writing Roughness as a Summable Formula

Now assemble the physical and physiological facts above into a function. For each harmonic pair $(i,j)$:

$$
\Delta f_{ij} = |i f_1 - j f_2|, \qquad
x_{ij} = \frac{\Delta f_{ij}}{0.25 \cdot \mathrm{CB}(\min(i f_1, j f_2))}
$$

<Box kind="definition" title="The roughness kernel W">

$$W(x) = x^2 e^{1 - x^2}$$
Properties:
1. $W(0) = 0$ — exact unison only changes loudness, producing no roughness;
2. $W$ attains its maximum 1 at $x = 1$, i.e. roughness is greatest when $\Delta f = 0.25\,\mathrm{CB}$;
3. $W \to 0$ as $x \to \infty$ — the auditory system has separated the two tones.

The coefficient $0.25$ is our modeling choice (based on the peak location of the Plomp–Levelt curve); it is a postulate, not a theorem.

</Box>

<Box kind="definition" title="Dissonance D and consonance S">

$$
D(f_1,f_2) = \sum_{i=1}^{N}\sum_{j=1}^{N} \frac{1}{i}\cdot\frac{1}{j}\; W\!\left(x_{ij}\right),
\qquad
S(f_1,f_2) = \frac{1}{1 + D}
$$

where $N = 5$ is the number of harmonics included, and $1/i$ is the amplitude of the $i$-th harmonic (a simplified $1/i$ decay replaces the spectrum of a real instrument). $D$ is not normalized: with $N$, the amplitude rule, and the reference register fixed, intervals can be compared; changing $N$ adds or removes summands, and changing the overall amplitude scale also changes $D$, so absolute scores under different parameters are not directly comparable. $S \in (0,1]$; the closer to 1, the lower the roughness computed by this model.

</Box>

<Box kind="algorithm" title="Algorithm 3.1 (computing the consonance of any two notes)">

```text
输入：f1, f2, N
D ← 0
for i in 1..N:
  for j in 1..N:
    Δf ← |i·f1 − j·f2|
    CB ← 94 + 71.3·(min(i·f1, j·f2)/1000)^0.69
    x  ← Δf / (0.25·CB)
    D  ← D + (1/i)(1/j) · x²·e^(1−x²)
返回 S = 1/(1+D)
```
Complexity $O(N^2)$; at $N=5$ there are only 25 harmonic pairs to process, but each pair also involves a critical bandwidth and an exponential, so it is not just 25 multiplications in total.

</Box>

### 3.3.3 Checking on the Machine

<Box kind="experiment" title="Experiment 3.1: Computing the consonance table">

```bash
python code/ch03_consonance.py
```
Output ($f_1 = 330$ Hz, $N = 5$):

| Interval | Just ratio | Just $D$ | Just $S$ | 12-TET $S$ |
| --- | --- | --- | --- | --- |
| Unison | 1.0000 | 0.000 | 1.000 | 1.000 |
| Minor second | 1.0667 | 1.117 | 0.472 | 0.484 |
| Major second | 1.1250 | 0.873 | 0.534 | 0.526 |
| Minor third | 1.2000 | 0.197 | 0.836 | 0.803 |
| Major third | 1.2500 | 0.046 | 0.956 | 0.940 |
| Perfect fourth | 1.3333 | 0.006 | 0.994 | 0.994 |
| Tritone | 1.4062 | 0.147 | 0.872 | 0.865 |
| Perfect fifth | 1.5000 | 0.000 | 1.000 | 1.000 |
| Minor sixth | 1.6000 | 0.141 | 0.876 | 0.863 |
| Major sixth | 1.6667 | 0.003 | 0.997 | 0.982 |
| Minor seventh | 1.7778 | 0.092 | 0.916 | 0.908 |
| Major seventh | 1.8750 | 0.519 | 0.659 | 0.642 |
| Octave | 2.0000 | 0.000 | 1.000 | 1.000 |

</Box>

Check three things:

1. **The $D$ values for unison, perfect fifth, and octave all display as 0.000; this is rounding, not an exact zero.** Only coinciding harmonic pairs have $W(0)$ exactly 0; the remaining separated pairs still contribute tiny positive amounts. With the same function at higher display precision, the perfect fifth at 330 Hz is about $D=1.4166\times10^{-5}$. The upper note's harmonic series in an octave is contained in the lower note's series, but the pairwise sum still includes non-coinciding combinations;
2. **Under this set of parameters, the just minor third, major third, and major sixth all beat 12-TET** — simple ratios bring low-order harmonic coincidence; equal-tempered intervals other than the octave have irrational ratios and can only coincide approximately;
3. **The minor second has the highest roughness in this table ($D = 1.117$)** — its fundamental difference is only about 22 Hz, which lands right in the rough region. This ranking depends on the 330 Hz reference and the harmonic setup; it is not a universal ordering for all registers.

### 3.3.4 The Valleys in the Curve

Sweep the interval from 0 to 1200 cents and $D$ shows a series of local minima. They are the low-roughness candidates of this model in this register; the sweep step is 2 ¢, so positions are grid readings, and $D=0.0000$ is still zero within display precision:

```text
  384.0 ¢  D = 0.0455   → 5:4 大三度
  500.0 ¢  D = 0.0060   → 4:3 纯四度
  702.0 ¢  D = 0.0000   → 3:2 纯五度
  886.0 ¢  D = 0.0034   → 5:3 大六度
  970.0 ¢  D = 0.0642   → 7:4 「和声小七度」
```

The last value, $970$ ¢, is worth noting: it corresponds to $7:4$, an interval that genuinely exists in the natural harmonic series, but it has no counterpart pitch class in 12-TET (the nearest is 10 semitones = 1000 ¢, still 30 ¢ away). This is the setup for Chapter 4's "tuning systems must make trade-offs": **the model has more valleys than there are 12 pitch classes.**

<Figure src="/figures/roughness-curve.svg" caption="The same model drawn as a curve: the valleys are 5:4, 4:3, 3:2, 5:3, 7:4, and the peak is near 600 ¢. The interactive component below lets you drag the fundamental and the interval to see how the curve moves." />

<ConsonanceExplorer />

## 3.4 Three Blind Spots of the Model

An honest model must state where it fails. Below are three known blind spots — they are not bugs, but doorways to the next chapter, or even the next book.

<Box kind="pitfall" title="Blind spot 1: the tritone is not always the 'most dissonant'">

In the table above, the just tritone $45:32$ has $S = 0.872$, actually higher than the minor third's $0.836$. This conflicts with the common sense that "the augmented fourth is the harshest."

There are two reasons: although $45:32$ has a large numerator and denominator, it is a **simple integer ratio**, and its harmonics coincide more than one might think; while the minor third in the low register (330 Hz) has fundamentals 66 Hz apart, right near the roughness peak, and is therefore "dirtier."

In real music, the tritone's bad reputation comes largely from **tonal context** (it belongs to no diatonic scale) and **equal-temperament deviation** (12-TET's 600 ¢ is not any simple ratio), not from pure roughness. The lesson: a physical model can explain "sounds rough"; it cannot explain "sounds wrong."

</Box>

<AudioDemo src="/audio/tritone-just.wav" title="Just tritone 45:32 (590 ¢)" hint="Large numerator and denominator, but still an integer ratio: the harmonics can coincide at high order, so it sounds less harsh than you would expect." />

<AudioDemo src="/audio/tritone-tet.wav" title="12-TET tritone 600 ¢" hint="2^0.5 is not a simple integer ratio; the harmonics never line up: this is the usual source of the 'harsh augmented fourth.'" />

<Box kind="pitfall" title="Blind spot 2: all timbres are treated alike">

The model assumes every instrument has $1/k$ harmonics and $N=5$. Real pianos, clarinets, and synthesizers have wildly different spectra: change $N$ to 2 (fundamental plus second harmonic) and you get a completely different consonance table; conversely, push $N$ to 20 and the ranking of some intervals may even reverse.

This is not model instability; **consonance is bound to timbre in the first place**. The same interval sounds "pure" on a sine-wave synthesizer and "muddy" on a distorted guitar.

</Box>

<Box kind="pitfall" title="Blind spot 3: loudness and masking are ignored">

$W$ considers only frequency difference, not the loudness balance between the two notes, their temporal order, or the brain's expectations. A very soft minor second may be less "intrusive" than a very loud perfect fifth. Such effects require psychoacoustic models and are beyond the scope of this book.

</Box>

<Box kind="checkpoint" title="Self-check">

Close the book and write down three things: (1) the beat formula and its limits of applicability; (2) why the critical bandwidth makes the bass register pickier; (3) in your consonance function, which parameter is a postulate and which is free to tune.

</Box>

## 3.5 Summary

This chapter separated "consonance" into three layers:

$$
\underbrace{\text{Wave superposition}}_{\text{physics}}
\;\longrightarrow\;
\underbrace{\text{Critical band}}_{\text{physiology}}
\;\longrightarrow\;
\underbrace{W(x)=x^2e^{1-x^2}}_{\text{modeling}}
\;\longrightarrow\;
\underbrace{S=\frac{1}{1+D}}_{\text{scoring}}
$$

The conclusion: **consonance is a function of how much the harmonics coincide, and harmonic coincidence is determined by how simply the frequency ratio can be approximated by rationals.** The simpler the ratio (the smaller the numerator and denominator), the earlier and more numerous the coincidences, the smaller the physical interference, and the more consonant it sounds.

The next chapter treats this scoring function as an objective and solves an optimization problem: given the constraint "put $n$ notes in an octave," which set of frequency ratios minimizes total roughness? The answer will simultaneously locate Pythagorean tuning, just intonation, and 12-TET — and show where each of them loses.

<Box kind="exercise" title="Exercises">

1. Take $f_1 = 220$ Hz and compute $D$ for $2:1$, $3:2$, and $5:4$. Why is $D$ exactly 0 for the octave?
2. Change $N$ from 5 to 3 in the code. Does the $S$ ordering of the tritone and the perfect fourth change? Run it and check your prediction.
3. Use the critical bandwidth formula to compute CB at $f = 100$ Hz and $f = 4000$ Hz. How many cents is each? What does this show?
4. (Open) If you were to design a set of microtonal ratios "more consonant than just intonation" for electronic music, which ratios would you choose? Verify them with this chapter's function.

</Box>

::: tip Next Chapter
Chapter 4 treats consonance as an objective function and tuning as a constrained optimization problem. Spoiler: 12-TET is not the optimum, but it is **the least bad solution under the constraint of 12**.
:::
