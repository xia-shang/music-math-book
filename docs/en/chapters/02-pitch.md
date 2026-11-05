---
title: "Chapter 2 · The Physics and Geometry of Pitch"
description: "Swap the frequency axis for a logarithmic one: pitch is a coordinate, an interval is a group."
---

# Chapter 2 · The Physics and Geometry of Pitch

<div class="chapter-meta">
  <span>Estimated 45 minutes</span>
  <span>Prerequisite: Chapter 1</span>
  <span>Code: code/ch02_pitch.py</span>
</div>

The questions this chapter answers:

1. Why does the same 100 Hz difference sound like "a lot" in the low register and almost nothing in the high register?
2. Why does raising a melody by an octave usually not count as changing the notes, while raising it by a major second does?
3. Why can pitch be rolled up into a circle? Is that circle the same as the circle of fifths?
4. Why can "adding intervals" be computed as "multiplying frequency ratios"? Are the two really the same thing?
5. Among the 12 semitones, which intervals are the "simplest"? Does simple always mean consonant?

Chapter 1 reduced sound to frequency: a periodic signal has a fundamental, and its harmonics fall at integer multiples of it. But "frequency" is a physical quantity, not an auditory one. On an oscilloscope 440 Hz and 880 Hz differ only by a factor of two, yet to the ear that is "the same note an octave higher"; 220 Hz and 320 Hz differ by only 100 Hz, yet they sound far apart. What this chapter does is build a ruler for "pitch." The ruler has two unusual features: it is **logarithmic**, and its two ends are **glued together**.

## 2.1 Frequency and Pitch: The Weber–Fechner Law

### 2.1.1 Why Hearing Is a Logarithmic Scale

Start with a thought experiment. Against a background of 220 Hz, add 10 Hz, giving 230 Hz; against a background of 880 Hz, add the same 10 Hz, giving 890 Hz. The absolute change is identical both times, yet the first is usually far more noticeable and the second much less so.

In the nineteenth century, E. H. Weber and G. T. Fechner idealized phenomena of this kind into an empirical law:

$$
\Delta S = k\,\frac{\Delta I}{I},
$$

where $I$ is the stimulus magnitude (frequency in this chapter) and $S$ is the subjective coordinate. Weber's law says the just-noticeable change in stimulus $\Delta I$ is roughly proportional to $I$; Fechner went further and treated each such step as an equal subjective increment $\Delta S$. The meaning is: **in this approximate model, the ear detects relative change, not absolute change.** Write the relation in differential form and integrate over $I$:

$$
S = k \ln I + C = k \ln \frac{I}{I_0}.
$$

This is Fechner's law: the subjective magnitude is proportional to the logarithm of the stimulus. In terms of frequency, pitch is proportional to $\log f$.

<Box kind="axiom" title="Postulate 2.1 (Logarithmic perception of pitch)">

In the middle intensity range of hearing, pitch differences are proportional to the logarithm of frequency ratios:
$$
p = 1200 \log_2 \frac{f}{f_0}.
$$
Basis: an approximate fit of the Weber–Fechner law to pitch-discrimination experiments; under favorable loudness, mid-frequency pure tones and sufficient duration, trained listeners can reach frequency-difference thresholds on the order of a few cents. Failure boundary: the difference threshold is not constant — it changes at low and high frequencies, at low loudness, and with short durations; and the subjective "distance" of very large intervals (spanning several octaves) no longer grows strictly logarithmically.

</Box>

This postulate is not derived from physics; it is extracted from **auditory experiments**. That matters: every geometric structure that follows rests on this empirical law, not on the wave equation.

### 2.1.2 The Compound Interest Analogy: Multiplication and Addition Are the Same Thing

Suppose you deposit 1 unit of principal in an account with annual rate $r$, settled once a year. After $n$ years the balance is $(1+r)^n$. If each period the amount is **multiplied** by the same factor $q$, then after $n$ periods it is $q^n$. The logic of intervals is exactly the same:

- from A4 to A5 (one octave) is a frequency **multiplication** by 2;
- 12-TET cuts the octave into 12 equal parts, so each step's factor is
$$
q = 2^{1/12} \approx 1.059463,
$$
i.e. each semitone up multiplies the frequency by $1.059463$, roughly "a 5.946% rise";
- multiplying 12 times: $1.059463^{12} = 2.000000$, exactly back to one octave.

In compound interest, the growth factors of the periods are multiplied, and only after taking logarithms do they become additive; intervals are "**intervals add, frequency ratios multiply**." This is no coincidence: the logarithm translates multiplication into addition. Chapter 0 already used cents to compute this translation; here we write it as a theorem that can be proved.

### 2.1.3 Definitions and Basic Properties

<Box kind="definition" title="Definition 2.1 (Pitch coordinate and the cent)">

Take a reference frequency $f_0 > 0$ (this book defaults to $f_0 = \mathrm{A4} = 440\ \text{Hz}$). The **pitch coordinate** of a frequency $f$ is
$$
p(f) = 1200 \log_2 \frac{f}{f_0},
$$
in units of the **cent** (written ¢). One octave is 1200 ¢ and one semitone (12-TET) is 100 ¢. One cent corresponds to a frequency ratio of $2^{1/1200} \approx 1.000578$.

</Box>

The definition immediately yields three properties:

1. $p(f_0) = 0$;
2. $p(2f) = p(f) + 1200$, i.e. "an octave up = 1200 added to the coordinate";
3. $p$ is strictly increasing in $f$, so the pitch coordinate can be inverted to recover the frequency: $f = f_0 \cdot 2^{p/1200}$.

The third is especially important: it shows that the pitch coordinate is not a "description" but an **invertible coordinate transform**. Given a cent value, you can recover the frequency uniquely; given a frequency, you can compute the cents uniquely. Tables 1 and 4 of Experiment 2.1 are the two halves of this conversion table.

<Box kind="pitfall" title="Common misconception: a cent is a “smaller hertz”">

Wrong. A cent is a logarithmic unit of **ratio**, not a unit of frequency. Raising a frequency $f$ by 100 ¢ adds $\Delta f=f(2^{1/12}-1)$: about 13.1 Hz at 220 Hz, about 52.3 Hz at 880 Hz, and about 209.3 Hz at 3520 Hz. The same cent value corresponds to different hertz differences in different registers — that is exactly what "logarithmic scale" means. Adding or subtracting cents directly on a value in Hz is the most common dimensional error in code.

</Box>

### 2.1.4 Theorem: Cent Addition Is Isomorphic to Frequency-Ratio Multiplication

Now let us make the "translation" precise. Consider the multiplicative group of positive reals $(\mathbb{R}_{>0}, \cdot)$ and the additive group of reals $(\mathbb{R}, +)$.

<Box kind="theorem" title="Theorem 2.1 (Cent addition is isomorphic to frequency-ratio multiplication)">

Define
$$
\varphi(r) = 1200 \log_2 r, \qquad r > 0.
$$
Then $\varphi: (\mathbb{R}_{>0}, \cdot) \to (\mathbb{R}, +)$ is an **order-preserving group isomorphism**. That is:

1. $\varphi(rs) = \varphi(r) + \varphi(s)$ (multiplication becomes addition);
2. $\varphi(1) = 0$, $\varphi(1/r) = -\varphi(r)$;
3. $\varphi$ is a bijection, with inverse $\psi(p) = 2^{p/1200}$;
4. $r \lt s \iff \varphi(r) \lt \varphi(s)$ (order-preserving).

Hence the **interval** between two notes can equivalently be written as a "frequency ratio" or a "cent difference":
$$
\varphi\!\left(\frac{f_2}{f_1}\right) = p(f_2) - p(f_1).
$$

</Box>

<Box kind="proof" title="Proof">

**(1)** By the basic property of logarithms, $\log_2(rs) = \log_2 r + \log_2 s$; multiply both sides by 1200. In particular, taking $s = 1/r$ gives $\varphi(1) = \varphi(r) + \varphi(1/r)$, and since $\varphi(1) = 1200\log_2 1 = 0$, we get $\varphi(1/r) = -\varphi(r)$.

**(3)** For any $p \in \mathbb{R}$, set $r = 2^{p/1200}$; then
$$
\varphi(r) = 1200 \log_2 2^{p/1200} = p,
$$
so $\varphi$ is surjective. If $\varphi(r) = \varphi(s)$, then $r = s$, so $\varphi$ is injective. Hence $\varphi$ is invertible, with inverse $\psi$.

**(4)** $\log_2$ is strictly increasing on $(0, \infty)$, and multiplying by the positive constant 1200 preserves monotonicity, so order is preserved.

Combining (1)(3)(4): $\varphi$ is a bijection that preserves the operation and the order, i.e. an order-preserving group isomorphism. Then from $p(f) = \varphi(f/f_0)$,
$$
p(f_2) - p(f_1) = \varphi(f_2/f_0) - \varphi(f_1/f_0) = \varphi\!\left(\frac{f_2}{f_1}\right). \qquad \blacksquare
$$

</Box>

This theorem is the foundation of all of Chapter 2 and of every chapter that follows. It says three mutually equivalent things:

- **Geometrically**: pitch can be drawn on a logarithmic number line;
- **Algebraically**: composing intervals is adding cents;
- **Computationally**: computing an interval takes only a division and a logarithm, and requires no musical knowledge.

Plugging in numbers: $\varphi(3/2) = 701.955$ ¢, $\varphi(4/3) = 498.045$ ¢, and the two add up to $1200.000$ ¢ because $(3/2)(4/3) = 2$. Table 2 of Experiment 2.1 verifies this identity on six pairs of intervals.

## 2.2 Octave Equivalence and the Spiral Pitch Model

### 2.2.1 An Empirical Fact: An Octave Is Not "Another Note"

Raise a melody by an octave and you still recognize it as the same melody. A violinist writes the same note name on the score; a singer switching to the higher octave for the same phrase does not make the audience feel "this is a different song." This phenomenon is called **octave equivalence**.

Its physical basis is clear: if two notes have a frequency ratio of $2:1$, the $k$-th harmonic of the upper note falls exactly on the $2k$-th harmonic of the lower one. That is, **every harmonic of the upper note is a subset of the lower note's harmonics**; the auditory system sees the same harmonic skeleton, only from a different starting point.

<Box kind="axiom" title="Postulate 2.2 (Octave equivalence)">

At the level of pitch class, the frequencies $f$ and $2f$ are treated as the same pitch class. Basis: in many musical contexts octave transposition preserves melodic identity and note-name similarity; $2:1$ is also the simplest non-unison integer ratio in the overtone series, corresponding to a large amount of harmonic coincidence. Failure boundary: octave equivalence is an equivalence at the level of "pitch class," not at the level of "pitch" — listeners can still tell A3 from A4; its strength also depends on the stimulus, the listener and the cultural context, and it cannot be carried over directly to strongly inharmonic instruments or certain microtonal systems.

</Box>

Note the status of Postulate 2.2: it is a **modeling choice**, not a theorem. In principle you could choose another equivalence relation — for example "frequency multiplied by 3" equivalence (the Bohlen–Pierce system does exactly this) — or none at all. The octave occupies a central place in many musical traditions, closely tied to the harmonic coincidence of $2:1$ and to perceptual similarity; but mathematics does not force every music to adopt it, and an acoustic basis does not mean cultural influence is absent.

### 2.2.2 Quotient Space: Rolling the Line into a Circle

Once octave equivalence is fixed, the frequency axis repeats every octave. In group-theoretic language, we are taking a **quotient**:

$$
\mathbb{R}_{>0} \big/ 2^{\mathbb{Z}},
$$

where $2^{\mathbb{Z}} = \{\,2^k : k \in \mathbb{Z}\,\}$ is the subgroup generated by "integer powers of 2." An element of the quotient space is an equivalence class

$$
[f] = \{\, f \cdot 2^k : k \in \mathbb{Z}\,\}.
$$

Each class contains exactly one representative in $[1, 2)$: take $k = \lfloor \log_2 f \rfloor$, then $g = f / 2^k \in [1, 2)$. So as a set, the quotient space is the half-open interval $[1, 2)$, except that the two endpoints $1$ and $2$ represent the same class — glue the endpoints together and you have a circle.

<Box kind="theorem" title="Theorem 2.2 (The octave quotient space is homeomorphic to the circle)">

Treat the numerical value of frequency as a positive real (the unit Hz serves only as a ruler). Let $S^1 = \{\, z \in \mathbb{C} : \lvert z \rvert = 1 \,\}$. The map
$$
F([f]) = \exp\!\left(2\pi i \log_2 f\right)
$$
is a group isomorphism from the multiplicative quotient group $\mathbb{R}_{>0}/2^{\mathbb{Z}}$ to the multiplicative group $S^1$, and also a homeomorphism. Taking $f_0=\mathrm{A4}=440\ \text{Hz}$ as reference, the pitch-class coordinate can be written
$$
\theta(f) = \left\{\log_2 \frac{f}{f_0}\right\} \in [0, 1),
$$
where the braces denote the fractional part. The corresponding point on the circle is
$$
\Theta([f])=e^{2\pi i\theta(f)}
=F([f])e^{-2\pi i\log_2 f_0},
$$
that is, $F$ rotated by a fixed angle. $\theta$ should be understood as a coordinate modulo 1, not as an ordinary real-valued function that stays continuous at the seam.

</Box>

<Box kind="proof" title="Proof">

**Well-defined**: if $g = f \cdot 2^k$, then $\log_2 g = \log_2 f + k$; the two differ by an integer, the exponentials differ by $e^{2\pi i k} = 1$, so $F([g]) = F([f])$.

**Group isomorphism**: $F([f][g]) = e^{2\pi i (\log_2 f + \log_2 g)} = F([f])F([g])$; the identity $[1]$ maps to $1$; the inverse $[1/f]$ maps to the conjugate $F([f])^{-1}$.

**Bijection**: the image of $F$ lies on the unit circle; given any $e^{2\pi i \theta}$, take $f = 2^{\theta}$ to hit it. If two classes give the same point, their $\log_2$ values differ by an integer, i.e. the frequency ratio is an integer power of $2$, so they belong to the same class.

**Homeomorphism**: the quotient space is homeomorphic to $[1,2]$ with the two endpoints glued, hence compact; $F$ is continuous, and a continuous bijection from a compact space to a Hausdorff space is a homeomorphism. $\theta(f)$ is just $F$ composed with a fixed rotation $e^{-2\pi i \log_2 \mathrm{A4}}$, so it is also a continuous bijection. $\blacksquare$

</Box>

The meaning of this theorem: **the pitch-class space has no endpoints and no "high or low."** You can keep walking clockwise around the circle, and after 12 steps (if each step is a semitone) you are back where you started; you can also walk counterclockwise. There is no "first note" on the circle, only relative positions.

### 2.2.3 The Spiral: Pulling the Circle Open Again

The circle has thrown away the information "which octave this is." Add that information back and you get a **spiral**:

$$
(r, \theta) = \left(\log_2 \frac{f}{\mathrm{A4}},\ \left\{\log_2 \frac{f}{\mathrm{A4}}\right\}\right) \in \mathbb{R} \times S^1.
$$

$r$ is the height (the octave number, which may be any real number) and $\theta$ is the angle (the position of the pitch class). Fixing $\theta$ and moving along $r$ gives the same pitch class in different octaves; fixing $r$ and going once around $\theta$ gives the 12 pitch classes within one octave.

- **Transposition**: all notes' angles rotate by $\Delta\theta = c/1200$, and all heights shift by $c/1200$;
- **Octave duplication**: the height shifts by 1 and the angle is unchanged;
- **Chords**: finite point sets on the spiral. A major triad is three points whose angular separations in just intonation are $386.3$ ¢ and $315.6$ ¢.

<Figure src="/figures/spiral.svg" caption="The pitch spiral: one turn is 12 semitones, and one turn up is one octave. C4, C5 and C6 stack vertically, and notes at the same angle belong to the same pitch class." />

Table 1 of Experiment 2.1 marks the 15 notes from A3 to A5 on the spiral: A3, A4 and A5 all have $\theta = 0.0000$, while their heights are $-1$, $+0$ and $+1$ respectively, forming a vertical column; G4 has $\theta = 0.8333$, meaning it is close to A on the circle (only $-200$ ¢ away) but one octave lower in height.

<Box kind="pitfall" title="Common misconception: the pitch-class circle is the circle of fifths">

It is not. The circle given by the octave quotient space is called the **chromatic circle**, and its coordinate $\theta$ is proportional to the logarithm of frequency; the circle of fifths is a different circle, which takes a perfect fifth as one step, comes back only after $12$ steps (about $8423.5$ ¢), and does not close exactly (off by about $23.5$ ¢, computed in Chapter 4). Both circles are homeomorphic to $S^1$, but the **metrics** on them are completely different: adjacent points on the chromatic circle differ by 100 ¢, adjacent points on the circle of fifths by 700 ¢. Chapter 9 puts both circles in the same picture.

</Box>

## 2.3 The Mathematical Definition of Intervals: Simplification and Ordering

### 2.3.1 An Interval Is a Cent Difference

With the pitch coordinate in hand, the definition of an interval is one sentence.

<Box kind="definition" title="Definition 2.2 (Interval, pitch-class interval, and frequency ratio)">

Given two frequencies $f_1, f_2 > 0$:

- The **directed interval** is $\Delta p = p(f_2) - p(f_1) = \varphi(f_2/f_1) \in \mathbb{R}$, in cents; downward is negative.
- The **pitch-class interval** (modulo the octave) is $\Delta p \bmod 1200 \in \mathbb{R}/1200\mathbb{Z}$, by convention taking values in $[0, 1200)$.
- If $f_2/f_1 = m/n$ is rational ($m, n$ coprime), the interval's frequency ratio is $m:n$, and $m+n$ is called its **ratio complexity**.

Example: the interval of $3:2$ is $701.955$ ¢; $-701.955$ ¢ is its inversion; modulo the octave it is still $701.955$ ¢ (because it is less than 1200); the interval of $9:4$ is $1403.910$ ¢, which is $203.910$ ¢ modulo the octave.

</Box>

### 2.3.2 Intervals Form a Group

<Box kind="theorem" title="Theorem 2.3 (The group of pitch-class intervals)">

Modulo the octave, all pitch-class intervals form the additive group $\mathbb{R}/1200\mathbb{Z}$, which is isomorphic to the octave quotient space $\mathbb{R}_{>0}/2^{\mathbb{Z}}$. Specifically:

1. **Composition**: going first by interval $a$, then by interval $b$, gives the total interval $(a+b) \bmod 1200$, corresponding to multiplying frequency ratios;
2. **Identity**: $0$ ¢, corresponding to the frequency ratio $1:1$ (perfect unison);
3. **Inverse**: $(-a) \bmod 1200$, corresponding to taking the reciprocal of the frequency ratio;
4. **Commutativity**: $a + b = b + a$, so going up a fifth then a fourth reaches the same pitch class as going up a fourth then a fifth.

In addition, 12-TET takes the subgroup $\mathbb{Z}_{12}$ ($100$ ¢ per step), the most important discrete subgroup used in this book.

</Box>

<Box kind="proof" title="Proof">

By Theorem 2.1, $\varphi$ is an isomorphism from the multiplicative group to the additive group $(\mathbb{R}, +)$. The octave subgroup $2^{\mathbb{Z}}$ maps under this isomorphism to $1200\mathbb{Z}$. The quotient group isomorphism theorem gives
$$
(\mathbb{R}_{>0}/2^{\mathbb{Z}}) \;\cong\; \mathbb{R}/1200\mathbb{Z}.
$$
The quotient group inherits commutativity from the additive group; its identity is $0 + 1200\mathbb{Z}$ and the inverse of $a$ is $-a + 1200\mathbb{Z}$. Composition corresponds to adding cosets, i.e. $(a+b) \bmod 1200$. Finally, $\mathbb{Z}_{12}$ is generated by integer multiples of $100$ ¢ and is a finite subgroup of $\mathbb{R}/1200\mathbb{Z}$. $\blacksquare$

</Box>

The structure of this group explains a fact often treated as a mnemonic in music theory: **intervals can be stacked arbitrarily, the order of stacking does not matter, and the number of stackings can be arbitrarily large.** But it also warns us: the group records only "which pitch class you arrived at," not "how many turns you made." On the spiral, $701.955$ ¢ and $1901.955$ ¢ correspond to the same pitch class but different heights.

Corollary: a chain of fifths does not close automatically. $12$ perfect fifths are $12 \times 701.955 = 8423.46$ ¢, while $7$ octaves are $8400$ ¢; on the pitch-class circle both come back near the starting point, but in height they differ by about $23.46$ ¢. Chapter 4 calls this difference the **Pythagorean comma** and takes it as the starting point of the tuning optimization problem.

### 2.3.3 Ordering Intervals by "Complexity"

With the cent ruler, every interval can be compared in "size"; but music has another, more important comparison: **simplicity**. $3:2$ is "simpler" than $17:16$ because we prefer to describe it with smaller integers. Two common measures of complexity are:

- **$p+q$**: the sum of numerator and denominator. $3:2$ gives 5, $5:4$ gives 9, $17:16$ gives 33;
- **Stern-Brocot depth**: place the fraction $p/q$ in the Stern-Brocot tree and count the steps from the root $1/1$. The shallower the depth, the "earlier" the fraction appears, and the simpler it is.

Table 3 of Experiment 2.1 lists every reduced ratio with $p, q \le 9$ within one octave in ascending order of $p+q$. You can see that $1:1$, $2:1$, $3:2$, $4:3$, $5:3$, $5:4$, $6:5$… the ordering largely matches the intuition "smaller is simpler," but clear disagreements appear too: $7:4$ has $p+q = 11$, tied with $6:5$, yet its Stern-Brocot depth is only $4$, shallower than the $5$ of $6:5$; conversely, $9:8$ has $p+q$ as high as $17$ and depth $8$, making it one of the "most complex" intervals in the table — and yet it is exactly the "major second" of the natural major scale.

<Box kind="pitfall" title="Common misconception: simple means consonant">

"Simple" is a **property of numbers**; "consonant" is a **property of hearing**. The two are related but not identical. The roughness table of Chapter 3 gives a counterexample: $7:4$ ($969$ ¢) has $D = 0.0642$, more consonant than the minor third $6:5$ with $D = 0.197$, even though their $p+q$ are the same. The reason is that roughness also depends on register, number of harmonics and critical bandwidth; a ratio with a slightly larger numerator whose harmonics line up neatly can easily beat a ratio with a smaller numerator whose harmonics do not. Complexity is only a first approximation.

</Box>

### 2.3.4 Machine Experiment: Printing Coordinates, Groups, and Orderings

<Box kind="experiment" title="Experiment 2.1: Pitch coordinates, the spiral, and interval addition">

```bash
python code/ch02_pitch.py
```

Real output (reference A4 = 440 Hz, p = 0 ¢):

The script prints its labels in Chinese; the numbers are unchanged.

::: details Expand full script output (90 lines, content unedited)

```text:no-line-numbers
ch02_pitch.py —— 第 2 章配套实验（参考音 A4 = 440 Hz，p = 0 ¢）

表 1：A3–A5 的音名、频率与螺旋坐标

音名        半音     频率 (Hz)         cent          θ    圈数
--------------------------------------------------------------
A3           -12       220.000      -1200.0     0.0000      -1
B3           -10       246.942      -1000.0     0.1667      -1
C4            -9       261.626       -900.0     0.2500      -1
D4            -7       293.665       -700.0     0.4167      -1
E4            -5       329.628       -500.0     0.5833      -1
F4            -4       349.228       -400.0     0.6667      -1
G4            -2       391.995       -200.0     0.8333      -1
A4            +0       440.000         +0.0     0.0000      +0
B4            +2       493.883       +200.0     0.1667      +0
C5            +3       523.251       +300.0     0.2500      +0
D5            +5       587.330       +500.0     0.4167      +0
E5            +7       659.255       +700.0     0.5833      +0
F5            +8       698.456       +800.0     0.6667      +0
G5           +10       783.991      +1000.0     0.8333      +0
A5           +12       880.000      +1200.0     0.0000      +1

θ 是「音级」坐标（0~1 表示一个八度内的位置），圈数是八度的编号；
两者合起来就是螺旋坐标：r = log₂(f/A4) 给出高度，θ = r mod 1 给出角度。

表 2：音程加法的两种算法（cent 相加 vs 频率比相乘）

运算                  左 ¢      右 ¢       和 ¢       积 ¢   模 1200      误差
------------------------------------------------------------------------------
纯五度 × 纯四度    701.955   498.045   1200.000   1200.000     0.000  0.00e+00
大三度 × 纯四度    386.314   498.045    884.359    884.359   884.359  1.14e-13
大三度 × 小三度    386.314   315.641    701.955    701.955   701.955  1.14e-13
小三度 × 大六度    315.641   884.359   1200.000   1200.000     0.000  0.00e+00
纯五度 × 纯五度    701.955   701.955   1403.910   1403.910   203.910  0.00e+00
纯八度 × 纯五度   1200.000   701.955   1901.955   1901.955   701.955  0.00e+00

每一行的「和 ¢」与「积 ¢」在浮点精度内相等：
φ(r₁r₂) = φ(r₁) + φ(r₂)，这就是定理 2.1 的数值版本。
「模 1200」列把音程折回一个八度：5:4 与 6:5 相加得到 3:2，折回仍是 702 ¢；
3:2 自乘得到 9:4，折回后是 204 ¢ —— 音级空间里只剩「方向」，不再有圈数。

表 3：一个八度内 p:q 音程的复杂度排序（p+q 升序，并列按音高升序）

比值            cent     p+q   SB 深度  名称        
----------------------------------------------------
1:1             0.00       2         0  纯一度      
2:1          1200.00       3         1  纯八度      
3:2           701.96       5         2  纯五度      
4:3           498.04       7         3  纯四度      
5:3           884.36       8         3  大六度      
5:4           386.31       9         4  大三度      
6:5           315.64      11         5  小三度      
7:4           968.83      11         4  和声小七度  
7:5           582.51      12         4  —           
7:6           266.87      13         6  —           
8:5           813.69      13         4  小六度      
9:5          1017.60      14         5  —           
8:7           231.17      15         7  —           
9:7           435.08      16         5  —           
9:8           203.91      17         8  大二度      

p+q 越小，频率比越「简单」；SB 深度是同一个直觉的树版本：
1:1 在树根（深度 0），3:2 是「右-左」两步（深度 2）。
两种排序大体一致，但在 7:4 这类「分子大而分母适中」的比上会出现分歧。

表 4：12-TET 的 12 个音级在螺旋上的坐标

   k      cent         θ  名称         频率 (Hz)
------------------------------------------------
   0       0.0    0.0000  纯一度         440.000
   1     100.0    0.0833  小二度         466.164
   2     200.0    0.1667  大二度         493.883
   3     300.0    0.2500  小三度         523.251
   4     400.0    0.3333  大三度         554.365
   5     500.0    0.4167  纯四度         587.330
   6     600.0    0.5000  三全音         622.254
   7     700.0    0.5833  纯五度         659.255
   8     800.0    0.6667  小六度         698.456
   9     900.0    0.7500  大六度         739.989
  10    1000.0    0.8333  小七度         783.991
  11    1100.0    0.9167  大七度         830.609

θ = k/12 严格等距：平均律把单位圆切成 12 等份，
每一步的比值都是 2^(1/12) ≈ 1.059463，即每半音 +100 ¢。

一致性检查：
  cents(2:1)      = 1200.000 ¢（应等于 1200）
  2^(1200/1200)   = 2.000000（应等于 2）
  pitch(440 Hz)   = 0.000 ¢（应等于 0）
  freq(0 ¢)       = 440.000 Hz（应等于 440）
```

:::

</Box>

Check four things:

1. In **Table 1** the $\theta$ values of A3, A4 and A5 are all $0.0000$, and the turn counts are $-1, 0, +1$ — they line up vertically on the spiral, exactly one octave apart; B3 and B4 also share the same $\theta = 0.1667$.
2. In **Table 2** the "sum ¢" and "product ¢" agree on every row, and the largest error $1.14 \times 10^{-13}$ is just double-precision rounding; $3:2$ squared gives $1403.910$ ¢, which is $203.910$ ¢ modulo $1200$, showing exactly that the pitch-class group "remembers direction and forgets turns."
3. In **Table 3** the Stern-Brocot depth of $4:3$ is $3$ (the path "right-left-right"), and $5:3$ has the same depth; while $9:8$ needs $8$ steps, the deepest interval in the table.
4. In **Table 4** $\theta = k/12$ is strictly equidistant, and $k=7$ gives $659.255\ \text{Hz}$, the 700 ¢ "equal-tempered fifth"; it is $1.955$ ¢ shorter than the just $701.955$ ¢ — this discrepancy is the first account Chapter 4 must settle.

<Box kind="checkpoint" title="Self-check">

Close the book and write down three things: (1) prove from $p = 1200\log_2(f/f_0)$ that "an octave up means adding 1200"; (2) explain why the octave quotient space is homeomorphic to the circle, and draw A3, A4 and A5 on the spiral; (3) use $5:4$ and $6:5$ to verify "intervals add = frequency ratios multiply," then argue that the identity still holds modulo the octave.

</Box>

## 2.4 The Boundaries of the Model

An honest coordinate system must state where it stops working. There are at least three such places.

<Box kind="pitfall" title="Blind spot 1: octave equivalence is not a universal truth">

For most tonal music, octave equivalence holds very well; but for inharmonic instruments such as bells and xylophones, $2:1$ does not correspond to "the same note," because their spectra do not fall on integer multiples at all. The Bohlen–Pierce system even chooses $3:1$ as its equivalence relation. Postulate 2.2 is a convention that holds "within the range of music discussed in this book," not a law of nature.

</Box>

<Box kind="pitfall" title="Blind spot 2: equal cents are not equal perceptual distance">

The pitch coordinate draws 100 ¢ as the same-width cell, but the ear's resolution is not constant: in the low register the discriminable difference is about 5–10 ¢, it worsens in the high register, and it deteriorates sharply near the threshold of hearing. Moreover, a minor second of 100 ¢ and a major seventh of 100 ¢ have entirely different "abruptness" in a melody — perception also depends on context and expectation, not only on a coordinate difference.

</Box>

<Box kind="pitfall" title="Blind spot 3: pitch is not a function of frequency alone">

The same frequency, played as a sine wave, on a piano or on a distorted guitar, can be heard as having a different "sense of pitch," especially when the fundamental is missing while the harmonics remain (the missing-fundamental phenomenon). The pitch coordinate is an idealized description of **steady-state, harmonic, single-fundamental** signals; for noise, chords and fast glissandi it can only be an approximation.

</Box>

## 2.5 Summary

This chapter replaced the frequency axis with a pitch axis, and along the way built three structures:

$$
\underbrace{p = 1200\log_2 \frac{f}{f_0}}_{\text{logarithmic coordinate}}
\;\longrightarrow\;
\underbrace{\mathbb{R}_{>0}/2^{\mathbb{Z}} \cong S^1}_{\text{octave quotient space}}
\;\longrightarrow\;
\underbrace{\mathbb{R}/1200\mathbb{Z}}_{\text{interval group}}
\;\longrightarrow\;
\underbrace{p+q \text{ and SB depth}}_{\text{complexity ordering}}
$$

First, **pitch is a logarithmic coordinate**: an interval is the logarithm of a frequency ratio, so "adding intervals" is equivalent to "multiplying frequencies" (Theorem 2.1). Second, **octave equivalence rolls the line into a circle**: factoring the frequency axis by $2^{\mathbb{Z}}$ gives the pitch-class circle (Theorem 2.2), and adding the turn count back gives the spiral. Third, **pitch-class intervals form a group** $\mathbb{R}/1200\mathbb{Z}$ (Theorem 2.3): they can be stacked arbitrarily, inverted, and reordered, but group elements do not record how many turns were made. Fourth, **complexity is only a first approximation to consonance**: $p+q$ and Stern-Brocot depth can order intervals by "simplicity," but they cannot explain why $7:4$ may be more consonant than $6:5$.

The next chapter turns "consonance" from an adjective into a function. You will see that the simplicity of an interval is only half the story; the other half hides in critical bandwidth and harmonic overlap — exactly what the roughness model of Chapter 3 handles.

<Box kind="exercise" title="Exercises">

1. Use Theorem 2.1 to verify $\varphi(5/4) + \varphi(6/5) = \varphi(3/2)$, and compute the three cent values. If $5:4$ and $6:5$ are stacked twice in succession, how many cents is the result modulo the octave?
2. Given A4 = 440 Hz, find the frequency corresponding to $+350$ ¢ and the pitch coordinate corresponding to $220$ Hz. Compute by hand with $f = f_0 \cdot 2^{p/1200}$, then check against the experiment script.
3. The semitone ratio of 12-TET is $q = 2^{1/12}$. Prove that $q^{12} = 2$, and explain why "+100 ¢ per step" and "multiply by $q$ per step" are the same thing.
4. Order $7:5$, $8:5$ and $9:7$ by $p+q$, then by Stern-Brocot depth. Do the two orders agree? If not, which one better matches the intuition of "sounding simple"? Give your reasons.
5. (Open) If humans chose $3:1$ instead of $2:1$ as the equivalence relation, how long should the pitch-class circle be? Compute it with $1200\log_2 3$; then explain: if each pitch class must still be 100 ¢ apart, $19$ steps cover only $1900$ ¢ — how far is that from closing the circle? How would this discrepancy change the design of scales?

</Box>

::: tip Next chapter
Chapter 3 turns the interval coordinate into an auditory model: beat frequency, critical bandwidth, the roughness kernel, and finally a consonance function that can score any interval. You will see why the "simple" intervals of Chapter 2 are usually more consonant, and where that rule breaks down.
:::
