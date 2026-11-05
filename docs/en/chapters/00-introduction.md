---
title: "Chapter 0 · Introduction: Music as the Interface of Physics and Psychology"
description: "Set the axioms and coordinates first, then talk about music theory."
---

# Chapter 0 · Introduction: Music as the Interface of Physics and Psychology

<div class="chapter-meta">
  <span>Estimated 40 minutes</span>
  <span>Prerequisite: none</span>
  <span>Code: code/ch00_intro.py</span>
</div>

The questions this chapter answers:

1. Why does a random string of frequencies sound like noise, while a scale sounds like music?
2. On what grounds can music theory be written as "definition—postulate—theorem," rather than a pile of rules to memorize?
3. Why does doubling the frequency still sound like "the same note"?
4. Why does adding the same 10 Hz land near a semitone in the low register but become nearly inaudible in the high register?
5. How do the ten chapters of this book chain into a single logical line?

In traditional textbooks, Chapter 0 is usually a lyrical passage about "what music is." This book does not intend to be lyrical. Instead it does three things first: explain why hearing can be modeled, state the book's assumptions once and for all, and put two tools (logarithms and Fourier) into your toolbox. Once those three things are done, the remaining nine chapters have a common language.

## 0.1 Why Music Can Be Understood by the Brain: Pattern Recognition and Prediction

Start with a thought experiment. Draw a random number between 20 Hz and 20 kHz, draw 100 of them per second, and play the result to yourself continuously. You will not say "this piece is terrible"; you will say: "this is noise."

Why? Because the brain is not a passive tape recorder. At every instant it predicts, from the sounds already heard, what will happen in the next moment: roughly what register the next note will be in, how long the gap will be, how loud. When the prediction succeeds, the neural activity is "cheap"; when it fails, there is surprise. Music works because it makes surprise happen at a controlled rate: predictable most of the time, with an occasional surprise.

In the language of information theory, let the $t$-th auditory event be $x_t$; by the time the listener hears it, the listener already holds a conditional probability distribution $p(x_t \mid x_{1:t-1})$. Then the surprise of this event is

$$
e_t = -\log_2 p(x_t \mid x_{1:t-1}) \quad \text{bit}.
$$

If the predictive distribution matches the event's true conditional distribution, the expectation of the surprise over $x_t$ is the conditional entropy $H(X_t\mid X_{1:t-1})$; the average surprise over a finite sample is an estimate of it. Chapter 8 will use this to quantify melody. For now you only need one intuition: **the less likely an event, the more information it carries; music plays with the size of that information.**

<Box kind="definition" title="Definition 0.1 (Surprise)">

Let the listener's predictive distribution for the next event be $p(x_t \mid x_{1:t-1})$. Then the surprise carried by the occurrence of event $x_t$ is
$$
e_t = -\log_2 p(x_t \mid x_{1:t-1}) \quad \text{bit}.
$$
Properties:

1. $e_t \ge 0$, and $e_t = 0$ when $p = 1$ (fully expected);
2. The smaller the probability, the larger the surprise;
3. If the predictive distribution equals the true conditional distribution, the expectation of the surprise is the conditional entropy $H(X_t\mid X_{1:t-1})$; the sample mean over many events estimates it.

Boundary: this is only a descriptive model. It does not claim the brain actually computes logarithms; it characterizes the "degree of unexpectedness," not emotion itself.

</Box>

Within this framework the role of the scale is very clear: it cuts the continuous frequency axis into a finite set of labels. With 12 equiprobable pitch classes in an octave, the uncertainty of the choice is only $\log_2 12$; if instead frequency could take any value from 20 Hz to 20 kHz at 1 Hz resolution, the uncertainty is close to $\log_2 19981$. The two differ by about a factor of 4 (see Table 4 of Experiment 0.1). In other words, the scale compresses a vast range of choices into "a dozen or so predictable labels."

What is being compared here is only the **alphabet size of a single choice**, not the actual bit rate of music: pitch classes can also appear in different octaves, and real events are not necessarily equiprobable. It illustrates the intuition behind discretization, not a law about music's compression ratio.

This does not mean that simpler music is better. A metronome is perfectly predictable and therefore boring; white noise is wholly unpredictable and therefore incomprehensible. Music stands between the two: it offers an alphabet small enough for patterns to form, and leaves enough ways of combining them that patterns can keep being broken.

<Box kind="definition" title="Definition 0.2 (Pitch class and scale)">

Two frequencies $f$ and $f'$ are **octave-equivalent** if there is an integer $k$ with $f' = 2^k f$. Under this equivalence relation, an equivalence class is called a **pitch class**. Written in the pitch coordinate $p = 1200\log_2(f/f_0) \bmod 1200$, a pitch class takes values in the half-open interval $[0, 1200)$.

A **scale** is a finite set of pitch classes arranged in pitch order within one octave,
$$
S = \{s_1, s_2, \dots, s_n\} \subset [0, 1200),
\qquad 0 \le s_1 < s_2 < \cdots < s_n < 1200,
$$
with one of its elements designated as the tonic. When $n = 7$ and the successive gaps from the tonic (including the final step back to the starting point) are 2-2-1-2-2-2-1 semitones, the result is what is usually called the natural major scale.

</Box>

Note that "octave equivalence" in Definition 0.2 is not a mathematical theorem but Postulate 0.2 — we choose to treat $f$ and $2f$ as the same pitch class because a strong octave similarity exists in auditory perception, not because mathematics requires it, and not because the two are indistinguishable in height. Under a different equivalence relation the definition of a scale still holds; it simply no longer yields the music familiar to this book.

<Box kind="pitfall" title="Common misconception: the more predictable the better">

If predictability equaled beauty, the metronome would be the world's most popular music. The opposite is true: a perfectly predictable signal carries no information, and after enough listening you "fall asleep"; a perfectly unpredictable signal admits no patterns, and sounds like noise. Good music usually stays in a middle band — Chapter 8 will draw that band with entropy and redundancy.

</Box>

## 0.2 The Axiomatic System of Music Theory: Definitions, Postulates, and Theorems

Music theory is often treated as a pile of rules to memorize: perfect fifths are consonant, parallel fifths are bad, the leading tone must resolve to the tonic. The trouble with rules is that they admit exceptions, and the exceptions usually go unexplained. A theorem admits no exceptions: as long as the model's definitions and postulates hold, the conclusion must hold. This book takes the second approach.

While reading, keep four kinds of sentence apart:

- **Definition**: names an object and specifies which quantities constitute it. A definition is neither true nor false, only useful or not.
- **Postulate**: an input borrowed from physics or from auditory-physiology experiments. It is not proved, only declared; if an experiment refutes it, the whole model must change.
- **Theorem**: a proposition derived from definitions and postulates. A theorem is true inside the model, but the model itself may still be wrong.
- **Proof**: the chain of derivation from premises to conclusion. The proofs in this book are kept as short as possible without skipping steps.

The virtue of this style is honesty: you can see at a glance which sentence is "what we assume" and which is "what we derive." The cost is that it makes music theory look more like an engineering spec than a book of poems. We accept the cost.

<Box kind="axiom" title="Postulates 0.1–0.5 (the five modeling assumptions of this book)">

**Postulate 0.1 (Logarithmic perception)**: the subjective difference of pitch is determined by the frequency ratio. If the pitch coordinates of two frequencies $f_1, f_2$ differ by $\Delta p$, then
$$
\Delta p = 1200 \log_2 \frac{f_2}{f_1}.
$$
Basis: the Weber–Fechner law and discrimination experiments — within the frequency range used by music, the just-noticeable frequency difference is roughly proportional to frequency. Failure boundary: very low and very high frequencies, and situations with large loudness differences.

**Postulate 0.2 (Octave equivalence)**: $f$ and $2f$ are treated as the same pitch class. Basis: octave similarity is very strong in auditory perception and is treated as an equivalence relation in nearly all known musical cultures. Failure boundary: not every culture uses octave identity in melodic design; Shepard-scale experiments also show that octave circularity becomes ambiguous under specific stimuli.

**Postulate 0.3 (Roughness is determined by pairs of harmonics)**: the roughness of two sustained tones is a function of the frequency differences of each pair of their harmonics, and each difference must be compared against the critical bandwidth. Basis: the auditory-physiology experiments of Plomp–Levelt and Zwicker. Failure boundary: ignores loudness, masking, phase, attention and transients; applies only to steady dyads. Chapter 3 turns it into a computable formula.

**Postulate 0.4 (Harmonicity of musical tones)**: a sustained musical tone is approximately a periodic signal whose spectrum consists of harmonics at integer multiples of a fundamental $F$. Basis: strings, pipes and vocal folds are all approximately periodic oscillators. Failure boundary: piano strings have pronounced inharmonicity; percussion and noise are not periodic signals; attack transients do not satisfy it either. Chapter 1 discusses these exceptions.

**Postulate 0.5 (Cultural priors stay out of the base model)**: the base model of this book uses only acoustic and auditory-physiological facts, and takes no "does this style sound right" as a premise; cultural conventions enter as boundary conditions in the discussion of specific chapters, not hidden inside formulas. Basis: this is a methodological choice, not an experimental result. Failure boundary: it is strong, and necessarily misses style, training and context; Chapter 9 discusses the model's range of applicability explicitly.

</Box>

Of these five postulates, the first four are modeling assumptions about the world and perception; the fifth is "how we look at the world." The theorems in every later chapter may use only these postulates, that chapter's definitions, and explicitly introduced mathematical premises.

Now for the single formal theorem of this chapter. It looks almost like a truism, but it is the reason a great many formulas in this book can be added together.

<Box kind="theorem" title="Theorem 0.1 (The additive structure of intervals)">

Let $f_1, f_2, f_3 > 0$ and define the map from ratios to intervals $\varphi(r) = 1200\log_2 r$ ($r>0$). Then
$$
\varphi\!\left(\frac{f_3}{f_1}\right)
= \varphi\!\left(\frac{f_3}{f_2}\right)
+ \varphi\!\left(\frac{f_2}{f_1}\right).
$$
Equivalently: multiplication of frequency ratios corresponds to addition of cent coordinates. If intervals are regarded as "ratios," all intervals form an abelian group, and $\varphi$ maps this group isomorphically onto the additive group of the reals.

</Box>

<Box kind="proof" title="Proof">

By the definition of $\varphi$,
$$
\varphi\!\left(\frac{f_3}{f_1}\right)
= 1200\log_2\frac{f_3}{f_1}
= 1200\left(\log_2\frac{f_3}{f_2} + \log_2\frac{f_2}{f_1}\right)
= \varphi\!\left(\frac{f_3}{f_2}\right)
+ \varphi\!\left(\frac{f_2}{f_1}\right).
$$
The second step uses the multiplicative property of logarithms $\log(xy) = \log x + \log y$. For the group isomorphism: the positive reals under multiplication form an abelian group, and $\varphi(r)=1200\log_2 r$ is a bijective homomorphism onto the additive group $(\mathbb{R}, +)$, hence an isomorphism. $\blacksquare$

</Box>

One immediate corollary: an octave is exactly 1200 cents, each semitone of 12-tone equal temperament is exactly 100 cents, and any interval can be split into a sum of smaller intervals. Chapter 2 upgrades this theorem to a formal group-theoretic statement; the tuning errors of Chapter 4 and the harmonic distances of Chapter 6 are also computed in this additive coordinate.

With postulates and coordinates in hand, the route through the book can be summarized in one diagram:

```text
Ch. 0 (postulates + cent coordinate + tools)
├─ Physics line:   Ch. 1 Vibration ─▶ Ch. 3 Consonance ─▶ Ch. 4 Tuning ─▶ Ch. 5 Scales ─▶ Ch. 6 Harmony
├─ Perception line: Ch. 2 Pitch ─▶ Ch. 3 Consonance
├─ Time line:      Ch. 7 Rhythm ─▶ Ch. 8 Melody
└─ Structure line: Ch. 6 Harmony ─▶ Ch. 9 Topology of tonality
Appendices A–E: math reference / code environment / glossary / further reading / exercise answers
```

The same diagram reads as three paths:

| Path | Order | Best for |
| --- | --- | --- |
| Quick read | 0 → 2 → 3 → 4 → 5 | Programmers who only want consonance and tuning |
| Close read | 0 → 9, with Appendices A and B | Science students who want the full axiomatic intuition |
| Engineering | Run each chapter's experiment first, then reread the text | People who want to turn the conclusions into tools |

All three paths must pass through Chapter 2. Without the logarithmic coordinate, everything that follows degenerates into a new round of rote memorization.

## 0.3 Toolkit: An Intuitive Grasp of Logarithms, Exponents, and Fourier

### 0.3.1 Logarithms: Compound Interest on Intervals

Suppose you deposit $P$ dollars in a bank at annual rate $r$, compounded once a year; after $n$ years the balance is

$$
P(1+r)^n.
$$

Intervals work in exactly the same way. Let the frequency ratio of one semitone be $q$; starting from $f_0$ and walking $n$ semitones gives the frequency $f_0 q^n$. Taking logarithms of both sides:

$$
\log f = \log f_0 + n\log q.
$$

**Multiplication has become addition.** That is why intervals can be described as "how many steps," and why cents can be added. With compound interest you care about how many doublings have happened; with intervals you care about how many octaves — both are logarithms.

Fix a doubling at 1200 cents and you get the coordinate of this book:

$$
p = 1200\log_2\frac{f}{f_0}.
$$

Here $f_0$ is the reference frequency. This book defaults to $f_0 = 440\ \text{Hz}$ (A4), so A4 has coordinate 0 cents, A5 is 1200 cents, and A3 is $-1200$ cents.

### 0.3.2 Fourier: Decomposing a Waveform into Sines

The second tool is the Fourier series. Its claim fits in one sentence: **any "sufficiently well-behaved" periodic signal can be decomposed into a sum of sine waves.**

For a sustained tone with fundamental $F$ and period $T = 1/F$, we can write it as a sum of cosine and sine components:

$$
x(t) = \frac{a_0}{2} + \sum_{k=1}^{\infty}
\left(a_k\cos(2\pi kFt) + b_k\sin(2\pi kFt)\right).
$$

For $k\ge 1$ the coefficients are obtained by inner products:

$$
a_k = \frac{2}{T}\int_0^T x(t)\cos(2\pi kFt)\,\mathrm{d}t,
\qquad
b_k = \frac{2}{T}\int_0^T x(t)\sin(2\pi kFt)\,\mathrm{d}t.
$$

The amplitude of the $k$-th harmonic is $A_k=\sqrt{a_k^2+b_k^2}$, and the phase is determined jointly by $a_k$ and $b_k$; a single sine inner product cannot represent the amplitude at an arbitrary phase.

Intuitively, Fourier analysis is a prism: a beam of white light goes in, a spectrum comes out. For sound, that "spectrum" is the **frequency spectrum**. The fundamental $F$ sets the pitch, and the distribution of harmonic amplitudes $A_k$ is a major source of timbre — which is why a piano and a violin can play the same pitch and sound completely different. Chapter 1 expands on this.

<Box kind="pitfall" title="Common misconception: the Fourier transform is musical analysis">

The Fourier series describes periodic signals directly, or the periodic extension of a signal on a finite interval. Real instrument tones have attacks, decays, vibrato, and noise components; strictly speaking none of them are infinitely long periodic signals. We therefore commonly use the **short-time Fourier analysis**: assume the signal is approximately stationary inside a window of a few tens of milliseconds. The shorter the window, the better the time resolution and the worse the frequency resolution — the basic trade-off between time and frequency resolution. Treating Fourier as a universal microscope is the most common over-promise of beginners.

</Box>

### 0.3.3 Three Calculations by Hand

Before running any code, compute three numbers by hand from the formulas, to get a feel for magnitudes.

1. **A4 → A5**: $f_2/f_1 = 2$, so $p = 1200\log_2 2 = 1200$ cents.
2. **Perfect fifth $3:2$**: $p = 1200\log_2 1.5 = 701.955$ cents.
3. **Just major third $5:4$**: $p = 1200\log_2 1.25 = 386.314$ cents.

For comparison, a semitone of 12-TET is $2^{1/12}$, exactly 100 cents. So the perfect fifth is about 2 cents wider than seven semitones (700 cents), and the just major third is about 14 cents narrower than four semitones (400 cents). These two discrepancies become the core trade-off of tuning systems in Chapter 4.

### 0.3.4 On the Machine: The First Experiment

<Box kind="experiment" title="Experiment 0.1: Note names, frequencies, cents, and the “logarithmic ear”">

```bash
python code/ch00_intro.py
```

Real output:

The script prints its labels in Chinese; the numbers are unchanged.

::: details Expand full script output (71 lines, content unedited)

```text:no-line-numbers
ch00_intro.py —— 导论配套实验（A4 = 440 Hz）

表 1：A3 ~ A5 的音名、频率与音高坐标（A4 = 440 Hz，12-TET）

音名         频率 (Hz)      相对 A4 (cent)
------------------------------------------
A3             220.000             -1200.0
A#3            233.082             -1100.0
B3             246.942             -1000.0
C4             261.626              -900.0
C#4            277.183              -800.0
D4             293.665              -700.0
D#4            311.127              -600.0
E4             329.628              -500.0
F4             349.228              -400.0
F#4            369.994              -300.0
G4             391.995              -200.0
G#4            415.305              -100.0
A4             440.000                 0.0
A#4            466.164               100.0
B4             493.883               200.0
C5             523.251               300.0
C#5            554.365               400.0
D5             587.330               500.0
D#5            622.254               600.0
E5             659.255               700.0
F5             698.456               800.0
F#5            739.989               900.0
G5             783.991              1000.0
G#5            830.609              1100.0
A5             880.000              1200.0

注意首尾两行：A3 与 A5 都叫 A，坐标恰好相差 2400 cent（两个八度）。

表 2：同样 +10 Hz，听起来差多少？

频率变化                 音程 (cent)
------------------------------------
    220 → 230                   77.0
    440 → 450                   38.9
    880 → 890                   19.6

同样 +10 Hz，低音区接近一个半音，高音区只剩五分之一。
听觉比较的是「比值」，不是「差值」。

表 3：220 Hz 与 880 Hz 的「中点」在哪里？

  算术中点 (220+880)/2       = 550.000 Hz   相对 220 Hz =  1586.3 cent
  几何中点 sqrt(220×880)     = 440.000 Hz   相对 220 Hz =  1200.0 cent
  两段音程应该相等：几何中点把 2400.0 cent 平分成两个 1200 cent。
  算术中点偏出的 386.3 cent，就是「线性频率轴」的谎言。

表 4：把连续频率离散成音级，省掉多少信息？

  连续频率（20~20000 Hz，1 Hz 分辨率）       14.29 bit
  12 个音级（等概率）                         3.58 bit
  压缩比                                       3.99 倍

音阶把「无限种可能」压成「12 个可预测的标签」，这就是它好用的原因。

表 5：三个常用比值与毕达哥拉斯音差

  3:2（纯五度）                     701.955 cent
  5:4（纯律大三度）                 386.314 cent
  2^(1/12)（12-TET 半音）           100.000 cent

  12 个纯五度 =  8423.460 cent
  7 个纯八度  =  8400.000 cent
  差值（毕达哥拉斯音差）= 23.460 cent

纯五度链走 12 步回不到原点：第 4 章要解决的就是这 23.4 cent；12-TET 的五度圈则闭合。
```

:::

</Box>

Check five things:

1. In Table 1 the first and last entries, A3 and A5, have coordinates $-1200$ and $+1200$, a difference of 2400 cents — two octaves, exactly as Postulate 0.2 says;
2. In Table 2 the change is the same $+10\ \text{Hz}$ in both cases, yet it is 77.0 cents in the low register and only 19.6 cents in the high register (about one fifth of a semitone); each doubling of the reference frequency roughly halves the cent change — exactly as Postulate 0.1 says;
3. In Table 3 the geometric midpoint 440 Hz splits 2400 cents into two equal pieces, while the arithmetic midpoint 550 Hz is off by 386.3 cents — the frequency axis is not the pitch axis;
4. In Table 4, 14.29 bit versus 3.58 bit shows that a discrete scale compresses the space of choices by about a factor of 4 — a scale is a compression dictionary;
5. In Table 5, 23.460 cents is the difference between twelve perfect fifths and seven octaves; the circle of fifths does not return to its starting point after 12 steps — the main conflict of Chapter 4.

<Box kind="pitfall" title="Common misconception: Hz is a linear pitch scale">

On the frequency axis, 220 → 230 and 880 → 890 are both $+10\ \text{Hz}$ and look like "the same increase"; on the pitch coordinate the first is 77.0 cents and the second only 19.6 cents. Any comparison of whether intervals are "fair" must be made on the cent axis. Taking "equal spacing in frequency" for "equal spacing in pitch" is the most common coordinate error of beginners, and it is why 12-TET must use $2^{1/12}$ rather than "a fixed number of Hz per step."

</Box>

<Box kind="checkpoint" title="Self-check">

Close the book and try three things: (1) restate the five postulates in your own words, and give one failure scenario for each; (2) without looking anything up, write $p = 1200\log_2(f/f_0)$ and compute the cent value of $3:2$; (3) explain why "a scale is a compression dictionary" does not mean "the simpler the scale, the better."

</Box>

## 0.4 Summary

This chapter has not defined a single chord, yet it has already laid the foundation for the nine chapters that follow. The three main lines are:

$$
\underbrace{\text{Vibration}}_{\text{Ch. 1}}
\;\longrightarrow\;
\underbrace{\text{Spectrum}}_{\text{Ch. 1}}
\;\longrightarrow\;
\underbrace{\text{Pitch coordinate}}_{\text{Ch. 2}}
\;\longrightarrow\;
\underbrace{\text{Consonance}}_{\text{Ch. 3}}
\;\longrightarrow\;
\underbrace{\text{Tuning} \to \text{Scale}}_{\text{Ch. 4, 5}}
\;\longrightarrow\;
\underbrace{\text{Harmony and structure}}_{\text{Ch. 6–9}}
$$

First, hearing is a prediction system: it guesses the next event from past patterns, and music controls the rate of failed predictions. Second, music theory can be written as an axiom system: the five postulates come from physics and physiology, and the remaining conclusions are derived from them. Third, the cent coordinate turns multiplication of frequency ratios into addition, making "interval = number of steps" a computable object.

If you remember only one sentence from this chapter, remember this one: **pitch is the logarithm of a ratio, an interval is a difference of pitch coordinates; the rest of music theory is geometry done in this additive coordinate.**

The next chapter begins with a single string: we write "vibration" as a differential equation, see why a periodic signal must have a discrete spectrum, and find out exactly where in the spectrum timbre hides.

<Box kind="exercise" title="Exercises">

1. Use the cent formula to compute the interval from 440 Hz to 660 Hz, then answer: how many 12-TET semitones is it? How much wider than seven semitones?
2. Verify the trend of Table 2 with code: compute the cent values for 220 → 230 and 1760 → 1770. Why does each octave up roughly halve the effect of the same $+10\ \text{Hz}$?
3. The arithmetic midpoint of 220 Hz and 880 Hz is 550 Hz; the geometric midpoint is 440 Hz. Use the cent coordinate to explain why the "auditory midpoint" must be the geometric midpoint. If you insisted on the arithmetic midpoint, what coordinate would you implicitly be using?
4. Twelve perfect fifths add up to 8423.460 cents; seven octaves are 8400 cents. Starting from one note and going up 12 perfect fifths, will you end up higher or lower than the target note, and by how much? This is exactly the conflict Chapter 4 resolves; guess a solution first.

</Box>

::: tip Next chapter
[Chapter 1](/en/chapters/01-vibration) reduces "sound" to a spring oscillator and a differential equation: why the solution of $m\ddot{x} + kx = 0$ is a sine wave, why the Fourier coefficients of a square wave are $4/(\pi n)$, and why the condition "periodic" forces the spectrum to be discrete. After reading it you will be able to explain why a piano and a violin playing the same note sound like two different things.
:::
