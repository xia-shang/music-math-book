---
title: "Chapter 7 · Rhythm: Fractals and Chaos"
description: "Turn drum patterns into integers with Euclid's algorithm, and measure syncopation with moments and weights."
---

# Chapter 7 · Rhythm: Fractals and Chaos

<div class="chapter-meta">
  <span>Estimated 45 minutes</span>
  <span>Prerequisite: Chapters 5 and 6</span>
  <span>Code: code/ch07_rhythm.py</span>
</div>

This chapter answers five questions:

1. What makes a drum pattern feel "grouped" rather than a string of equal-length hits?
2. Given 3 onsets and 8 cells, how do you compute the most even placement?
3. Syncopation makes listeners feel "off balance". Can that imbalance be written as a number?
4. When 3:4 and 5:8 are overlaid, why is the period 12 and 40 rather than 7 and 13?
5. Are the "fractal" and "chaos" in the title mathematics or rhetoric?

Chapter 6 compressed harmony into 12-dimensional vectors. This chapter changes coordinates: time. Music's two basic dimensions—pitch and time—do the same thing mathematically: **discretize first, then look for patterns**. A scale cuts continuous frequency into 12 pitch classes; rhythm cuts continuous time into $n$ cells. The remaining question is identical: in these discrete cells, which patterns let the ear predict without becoming boring?

The answer comes in three layers: first a one-line formula that writes the "most even rhythm" as an integer set; then the moments of a probability distribution and metric weights to turn "syncopation" into a comparable number; finally the Chinese remainder theorem to explain why the periods of polymeters such as 3:4 and 5:8 are products. One thread runs through all three: **grouping**. Grouping is the first step of auditory compression, and its quality can be quantified by "how much the gaps differ", "how far the centroid shifts", and "how many coincidence points there are".

## 7.1 Grouping on the Time Axis: Beats, Bars, and the Euclidean Algorithm

### 7.1.1 From Continuous Time to n Cells

Suppose a bar lasts $L$ seconds: physical time is continuous, yet a player may count "four beats" and a drummer may subdivide into "eight eighth notes". Divide the bar evenly into $n$ cells, each of length $L/n$ seconds; a rhythm is then a choice of $k$ cells for onsets, with the rest left as rests. Write it in binary:

$$
b_i = \begin{cases} 1, & \text{cell } i \text{ has an onset},\\ 0, & \text{cell } i \text{ is a rest}, \end{cases}
\qquad i = 0,1,\ldots,n-1.
$$

So the rhythm becomes a binary word of length $n$ and weight $k$. For $n=8$, $k=3$ there are $\binom{8}{3}=56$ such words. If "overall translation" counts as the same rhythm (musicians would say "play the same pattern in a different position"), the 56 further merge into rotation equivalence classes. This chapter cares not about "how many kinds there are" but about "which one is most even".

Why is evenness worth pursuing? Because hearing is always predicting the next beat. Strong beats provide anchors and weak beats provide variation; all-equal (`x.x.x.x.`) is easiest to predict and easiest to bore; random scatter is unpredictable and sounds like noise. Composition is essentially the search for a position between predictability and surprise. To discuss "surprise", we first have to nail down the baseline of "evenness"—that is what Euclidean rhythms are for.

A side note: the $n$ cells need not be equal in length. In real music a beat can be stretched, shortened, or even given a "swing" offset. This chapter first fixes equal cells to obtain a computable skeleton; the stretching on top of that skeleton is the performer's second act of creation and is outside this chapter's model.

### 7.1.2 Euclidean Rhythms

<Box kind="definition" title="Definition 7.1 (Euclidean rhythm E(k,n))">

Let $1 \le k \le n$. Place $k$ onsets in $n$ cells at positions defined by
$$
p_j = \left\lfloor \frac{j\,n + k - 1}{k} \right\rfloor,
\qquad j = 0,1,\ldots,k-1.
$$
Call this onset set the **Euclidean rhythm** $E(k,n)$. Positions are numbered from $0$; when $k=n$ it degenerates to one hit per cell, and when $k=1$ the single onset falls in cell $0$.

</Box>

The $k-1$ in the numerator is not arbitrary: it pins the first onset to cell $0$ (the downbeat), that is, $p_0=\lfloor(k-1)/k\rfloor=0$. For integers $j,n,k$, the definition can also be written $p_j=\lceil jn/k\rceil$. More generally, $c\in[0,1)$ in $p_j=\lfloor jn/k+c\rfloor$ controls the phase; this chapter fixes $c=(k-1)/k$, which merely selects a representative aligned with the barline, not a claim that other rotations are less even.

In the literature, $E(k,n)$ sometimes denotes the whole rotation class and sometimes one representative, so the same name may be printed as different strings. Bjorklund's recursive bucketing algorithm, the closed form here, and the Bresenham criterion below all generate the corresponding maximally even patterns; the differences are usually rotation conventions. When comparing two sources, cyclically shift first, and do not mistake a phase difference for a mathematical contradiction.

Three examples:

- $E(3,8)$: $j=0,1,2$ gives $0,3,6$, pattern `x..x..x.`, gaps $3,3,2$;
- $E(5,8)$: $j=0,\ldots,4$ gives $0,2,4,5,7$, pattern `x.x.xx.x`, gaps $2,2,1,2,1$;
- $E(7,16)$: $j=0,\ldots,6$ gives $0,3,5,7,10,12,14$, pattern `x..x.x.x..x.x.x.`, gaps $3,2,2,3,2,2,2$.

The first is the Cuban tresillo (three-stroke pattern), the second is a five-stroke pattern (of the cinquillo family), and the third packs seven hits into sixteen cells. What they share: **the gaps differ by at most one cell**. This is the maximal evenness proved in the next subsection.

The same sets have a one-line equivalent algorithm that is easier to use in code:

<Box kind="algorithm" title="Algorithm 7.1 (one-line generation of E(k,n))">

```text
输入：k, n（1 ≤ k ≤ n）
for i = 0 .. n−1:
    b_i ← 1   若 (i·k) mod n < k
    b_i ← 0   否则
输出：b_0, b_1, …, b_{n−1}
```
Time complexity $O(n)$; it needs only integer modulo, no division, recursion, or floating point.

</Box>

Why do the one-line criterion and the closed form give the same set? Picture the $n$ cells as a line of slope $k/n$: cell $i$ corresponds to the remainder $i k \bmod n$, and a point is placed when the remainder falls among the first $k$ values. This is exactly Bresenham's line-drawing algorithm from computer graphics. Table 3 of Experiment 7.1 runs all 528 cases with $1 \le k \le n \le 32$; the closed form and the criterion agree bit for bit, with no exception.

<Figure src="/figures/euclidean.svg" caption="Three Euclidean rhythms on a ring: E(3,8), E(5,8), and E(5,13). Filled dots are onsets; every pattern's gaps differ by at most one cell, which is the geometric meaning of 'maximally even'." />

<Figure src="/figures/euclidean-timeline.svg" caption="The same rhythms flattened onto a timeline. The first three rows are E(3,8), E(5,8), and E(5,13); the last row overlays 3 beats and 4 beats, which realign after 12 steps." />

The experiment below puts $k$, $n$, and tempo on sliders; the ring, the timeline, and the click track change together:

<EuclideanRhythmLab />

<div class="audio-row">

<AudioDemo src="/audio/euclid-3-8.wav" title="E(3,8): tresillo" hint="A two-bar loop; the first beat is louder—listen for the gaps 3-3-2." />

<AudioDemo src="/audio/euclid-5-8.wav" title="E(5,8): five-stroke pattern" hint="Same loop length, denser onsets; gaps 2-2-1-2-1." />

<AudioDemo src="/audio/euclid-5-13.wav" title="E(5,13): five onsets in thirteen cells" hint="The displacement is more pronounced and the rolling feel is stronger." />

</div>

<div class="audio-row">

<AudioDemo src="/audio/polymeter-3-4.wav" title="3:4 polymeter" hint="The high voice lands every 4 steps, the low voice every 3; they coincide again after 12 steps." />

</div>

### 7.1.3 Maximal Evenness: Gaps Can Differ Only by 1

<Box kind="theorem" title="Theorem 7.1 (the gaps of E(k,n) take only two adjacent integers)">

Let $q=\lfloor n/k \rfloor$ and $r=n-qk$. The $k$ cyclic gaps of $E(k,n)$ (including the segment from the last onset back to the first) all equal $q$ or $q+1$; exactly $r$ of them equal $q+1$ and $k-r$ equal $q$.

</Box>

<Box kind="proof" title="Proof">

Write $c=(k-1)/k$ and $x_j=jn/k+c$, so $p_j=\lfloor x_j\rfloor$. The gap between adjacent onsets is
$$
p_{j+1}-p_j=\lfloor x_j+n/k\rfloor-\lfloor x_j\rfloor .
$$
For any real $x$ and $\alpha>0$, $\lfloor x+\alpha\rfloor-\lfloor x\rfloor \in \{\lfloor\alpha\rfloor,\lceil\alpha\rceil\}$: the difference equals $\lfloor \operatorname{frac}(x)+\alpha\rfloor$, and $\operatorname{frac}(x)\in[0,1)$. Taking $\alpha=n/k=q+\theta$ ($0\le\theta\lt 1$) gives $p_{j+1}-p_j\in\{q,q+1\}$.

The last gap is computed separately:
$$
n-p_{k-1}=n-\left\lfloor n-\frac{n-k+1}{k}\right\rfloor
=\left\lceil \frac{n-k+1}{k}\right\rceil
=\left\lceil \frac{n}{k}-\frac{k-1}{k}\right\rceil \in \{q,q+1\}.
$$
Let $c'$ be the number of gaps equal to $q+1$. All gaps sum to $n$, so $n=kq+c'$; comparing with $n=kq+r$ gives $c'=r$. $\blacksquare$

</Box>

The corollary is clean: if $k$ divides $n$ (that is, $r=0$), all gaps equal $n/k$ and the rhythm degenerates to a uniform grid. The "equal division" of quarter notes and eighth notes is this special case.

This theorem gives a combinatorial explanation of the balance of $E(3,8)$: there are only two gap sizes, $3$ and $2$, differing by exactly one cell, with no strong density contrast from longer versus shorter gaps. However, a larger gap difference does not necessarily mean "ugly" or that the pattern will be heard as two rhythms; that is a perceptual question depending on tempo, timbre, and accents, outside the theorem's conclusion.

So where does the word "Euclidean" come from? $q$ and $r$ are exactly the quotient and remainder of $n$ divided by $k$, the first step of the Euclidean algorithm (repeated division). More beautiful is the recursive structure: take the positions of the long ($q+1$) gaps; they themselves form a rotation of $E(r,k)$. The long-gap positions of $E(5,8)$ are $\{0,1,3\}$, while $E(3,5)=\{0,2,4\}$; shifting the latter by one gives the former. The long-gap positions of $E(3,8)$, $\{0,1\}$, are $E(2,3)=\{0,2\}$ shifted by one. Thus repeated division with remainder on $(k,n)$ until $r=0$ terminates in lockstep with computing $\gcd(n,k)$.

This "rhythm inside a rhythm" structure is what the title's "fractal" concretely refers to: the same rule repeating at several finite scales. It is **recursive self-similarity in a combinatorial sense**, not a geometric fractal with infinite detail; running more rounds of division will not produce a fractal dimension. So "fractal" here is a metaphor with a definite referent and should not be read as a strict classification of dynamical systems.

<Box kind="pitfall" title="Common misconception: gaps differing by 1 imply maximal evenness">

Counterexample: for $n=8$, $k=5$ the pattern `x.x.x.xx` (onsets at $0,2,4,6,7$) has cyclic gaps $2,2,2,1,1$. All gaps lie in $\{1,2\}$ and look "only one cell apart", but the two short gaps are adjacent at the end, leaving the first half loose and the second half tight; it sounds rushed, not even.

It is not even a rotation of $E(5,8)$: $E(5,8)$ is `x.x.xx.x` (onsets $0,2,4,5,7$), where the short gaps are separated by long ones. The strict condition for maximal evenness is "there exists a phase $c$ such that every onset can be written as $\lfloor j n/k+c\rfloor$"; checking the number of gap types is not enough, because the **order** of the gaps also matters to the ear.

</Box>

## 7.2 Syncopation and Accent Shift: Mean and Variance of a Probability Distribution

### 7.2.1 Reading a Rhythm as a Probability Distribution

The $k$ onsets of a rhythm can be seen as spreading total mass $1$ evenly over $k$ positions. Then "where the onsets fall" has a probability distribution, and we can compute its mean and variance. An onset is not necessarily played as an accent; here the position distribution is only the basis for later weighting of accent strength.

<Box kind="definition" title="Definition 7.2 (onset position distribution and its moments)">

Let $S\subset\mathbb{Z}_n$ be the onset set with $\lvert S\rvert=k$. Define the **onset position distribution**
$$
p_i=\begin{cases} 1/k, & i\in S,\\ 0, & i\notin S. \end{cases}
$$
Its first moment (centroid) and second central moment (variance) are
$$
\mu=\sum_{i=0}^{n-1} i\,p_i,
\qquad
\sigma^2=\sum_{i=0}^{n-1}(i-\mu)^2 p_i .
$$
$\mu$ is measured in cells (steps), $\sigma^2$ in steps$^2$.

</Box>

Table 4 of Experiment 7.1 gives a set of numbers for $n=8$: $E(3,8)$ has $\mu=3.000$, $\sigma^2=6.000$; $E(4,8)$ has $\mu=3.000$, $\sigma^2=5.000$; $E(5,8)$ has $\mu=3.600$, $\sigma^2=5.840$; $E(1,8)$ has $\mu=0$, $\sigma^2=0$; $E(8,8)$ has $\mu=3.500$, $\sigma^2=5.250$.

How to read these numbers? $\mu$ says "around which cell the onset centroid lies": $E(5,8)$'s $3.600$ is later than $E(3,8)$'s $3.000$, because three of its five onsets sit at cell $4$ or later ($4,5,7$), not because "all three are after cell 4". $\sigma^2$ says "how spread out the onsets are around the centroid": $E(3,8)$'s three hits fall at $0,3,6$, symmetric about $3$, with variance $6.000$; $E(4,8)$'s four hits fall at $0,2,4,6$, more clustered about $3$, with variance $5.000$.

<Box kind="pitfall" title="Common misconception: larger variance means a messier rhythm">

Variance only measures the squared distance of onsets from the mean position; it is not the same thing as "messy". $E(7,16)$ has variance $21.633$, which looks large only because the span of 16-cell coordinates is twice that of 8 cells, and squaring makes it four times as large; comparing it directly with $n=8$ numbers is meaningless.

The more fundamental flaw: these are **linear moments on a ring**. Positions $0$ and $n-1$ are neighbors to the ear but $n-1$ apart in linear coordinates. Hence both the linear centroid and the variance drift with rotation and with $n$; to compare across rhythms you need the circular statistics of the next subsection.

</Box>

### 7.2.2 Metric Weight and Syncopation Degree

Rhythm cells are not flat. In 4/4 time, cell $0$ (the barline) and cell $4$ (the third beat) are strong, cells $2$ and $6$ are secondary, and odd cells are weakest. This "strength" can be written exactly using binary subdivision: the more times a position is divisible by $2$, the closer it is to a strong beat at some level.

<Box kind="definition" title="Definition 7.3 (metric weight and syncopation)">

Let $n=2^L$. Define the **metric weight** of position $i$ as
$$
h(0)=1,\qquad h(i)=\frac{2^{v_2(i)}}{n}\quad(1\le i\lt n),
$$
where $v_2(i)=\max\{v:2^v\mid i\}$ is the exponent of $2$ in $i$ (with $v_2(1)=0$). For an onset set $S$, define the **syncopation degree**
$$
\operatorname{sync}(S)=1-\frac{1}{k}\sum_{i\in S} h(i).
$$
It measures "how low the average metric weight of the onsets is": $0$ when all onsets lie on barlines, approaching $1-1/n$ when all lie on the weakest odd cells.

</Box>

The weight table for $n=8$ looks like this:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $h(i)$ | 1 | 1/8 | 1/4 | 1/8 | 1/2 | 1/8 | 1/4 | 1/8 |

Each level down halves the weight: cell $0$ is the whole bar, cell $4$ the second half, cells $2$ and $6$ the quarter points, and odd cells the eighth points. This hierarchy is not a natural constant but a cultural convention of 4/4; switch to 3/4 and the table must be rewritten. This chapter uses it only within binary subdivision.

Substituting the definition into the experimental data, the syncopation degrees for $n=8$ are:

- $E(1,8)$: $0.0000$—only the strong beat, no syncopation at all;
- $E(4,8)$: $0.5000$—half the onsets fall on the secondary weak positions $2,6$;
- $E(3,8)$: $0.5417$—the tresillo has three onsets, two of them weak;
- $E(5,8)$: $0.6000$—the five-stroke pattern is more "fragmented";
- $E(8,8)$: $0.6875$—every cell has an onset, so the average weight is lowest.

$E(3,8)$ is $0.0417$ above $E(4,8)$, and $E(5,8)$ is $0.0583$ above $E(3,8)$. This ordering matches auditory intuition: the tresillo is "a bit unstable" and the five-stroke pattern is "more unstable". But remember that this is only the **share of weak positions**, not a degree of ugliness.

<Box kind="pitfall" title="Common misconception: higher syncopation degree means more syncopated">

$E(8,8)$ has the highest syncopation degree, $0.6875$, of all $n=8$ rhythms, but every cell has an onset, so there is no strong-weak contrast at all; it sounds flat, not syncopated. Real syncopation needs **rests** to create a gap in expectation: a weak onset is followed by an empty strong position, and the ear falls through.

This chapter's metric can only answer "how weak is the average grid position of the accents"; it cannot answer "where is expectation broken". The latter requires the information theory (surprise) of Chapter 8. Confusing the two is like using a thermometer to measure blood pressure.

</Box>

### 7.2.3 Circular Centroid: Also Computing "Which Way It Leans"

Linear moments are unsafe on a ring; the standard remedy is circular statistics: view each position as an angle on the unit circle and take their mean vector.

$$
z=\frac{1}{k}\sum_{i\in S} e^{2\pi \mathrm{i}\, i/n},
\qquad R=\lvert z\rvert,\qquad \theta=\arg z .
$$

$R\in[0,1]$ is called the resultant length: $R$ near $1$ means the onset directions are highly concentrated; $R=0$ only means the first circular moment vectors cancel and no mean direction is defined, **not** that the distribution has a nontrivial rotational symmetry. $\theta$ is meaningful only when $R\gt0$; after converting to "steps" and taking the representative in $[-n/2,n/2)$, a negative sign means the mean direction falls toward the end of the bar.

Table 4 of Experiment 7.1 gives:

- $E(3,8)$: $R=0.138$, direction $-1.0$ steps—the centroid is one cell later than the barline, a small shift;
- $E(4,8)$: $R=0.000$—four onsets quarter the circle, rotational symmetry, no bias;
- $E(5,8)$: $R=0.083$, direction $-2.0$ steps—the centroid is later, but the resultant vector is short;
- $E(7,8)$: $R=0.143$, direction $-3.0$ steps;
- $E(7,16)$: $R=0.028$, direction $-3.0$ steps—almost flat over sixteen cells, so the direction is nearly meaningless.

Read $R$ and the direction together: small $R$ means weak first-order directionality, and the direction says "which way it leans". The four points of $E(4,8)$ indeed form a rotationally symmetric figure, so its $R=0$; but this is not "no syncopation", only no first-order mean direction. This also shows the danger of a single metric: with the same data, changing the statistic changes the question being answered.

## 7.3 African Polymeter: Superimposing Coprime Numbers on a Timeline

### 7.3.1 Two Periods, One Least Common Multiple

Everything so far has been a single timeline. Real percussion often runs two or three at once: one hand strikes every 3 beats, the other every 4. Overlay the two lines on one schedule and you get a polymeter.

<Box kind="definition" title="Definition 7.4 (m:n polymeter and its period)">

Let $m,n$ be positive integers and $L=\operatorname{lcm}(m,n)$. On a cyclic timeline of length $L$, define
$$
A=\{t\in\mathbb{Z}_L: t\equiv 0 \pmod m\},\qquad
B=\{t\in\mathbb{Z}_L: t\equiv 0 \pmod n\},
$$
and call $A\cup B$ the **$m:n$ polymeter**. $A$ strikes every $m$ beats and $B$ every $n$ beats; only when $m\lt n$ can they be called "fast" and "slow" respectively. In one period the two lines have $L/m$ and $L/n$ onsets, and the only zero-phase common onset is $t=0$, so the number of distinct onsets is
$$
\frac{L}{m}+\frac{L}{n}-1=\frac{m+n}{\gcd(m,n)}-1.
$$
The table in this section takes only coprime $m,n$, where this reduces to $m+n-1$.

</Box>

Write the 12 beats of 3:4 as one line (`O` = both lines coincide, `x` = 3-beat line only, `y` = 4-beat line only, `.` = rest):

```text
t:  0 1 2 3 4 5 6 7 8 9 10 11
    O . . x y . x . y x .  .
```

$x$ appears $3$ times ($t=3,6,9$), $y$ appears $2$ times ($t=4,8$), and with the coincidence at $t=0$ there are $6$ distinct onsets; the two lines individually have $4+3=7$ onsets, and the difference is exactly the coincidence. Table 5 of Experiment 7.1 computes five common combinations:

| Overlay | Period $L$ | Onsets | After dedup | Density | Coincidences |
| --- | --- | --- | --- | --- | --- |
| 3:4 | 12 | 7 | 6 | 0.500 | 1 |
| 4:5 | 20 | 9 | 8 | 0.400 | 1 |
| 3:5 | 15 | 8 | 7 | 0.467 | 1 |
| 5:8 | 40 | 13 | 12 | 0.300 | 1 |
| 4:7 | 28 | 11 | 10 | 0.357 | 1 |

Density = distinct onsets / period. The density of $5:8$ is only $0.300$, meaning $28$ of $40$ cells are empty—lots of white space, hence it sounds "spacious"; $3:4$ has density $0.500$, half the cells sounding, hence denser. Density is not "complexity"; it only describes "how many beats are empty".

Why is the period the product? Because of the least common multiple of the two periods. When coprime, $\operatorname{lcm}(m,n)=mn$, so 3:4 has period $12$ and 5:8 has period $40$. This is no coincidence but a direct corollary of the Chinese remainder theorem.

<Box kind="theorem" title="Theorem 7.2 (unique decomposition of a coprime overlay)">

Let $\gcd(m,n)=1$ and $L=mn$. The map
$$
t \mapsto (t \bmod m,\ t \bmod n)
$$
is a bijection from $\mathbb{Z}_L$ to $\mathbb{Z}_m\times\mathbb{Z}_n$. Hence the period of the $m:n$ overlay is exactly $mn$, and within one period the two lines coincide only at $t=0$. More generally, for any relative phase $s$, the system $t\equiv 0\pmod m$, $t\equiv s\pmod n$ has exactly one solution in $\mathbb{Z}_{mn}$.

</Box>

<Box kind="proof" title="Proof">

If $t,t'$ give the same pair of residues, then $m\mid(t-t')$ and $n\mid(t-t')$; since $\gcd(m,n)=1$, $mn\mid(t-t')$. Within a period of length $mn$ this can only mean $t=t'$, so the map is injective. Both $\mathbb{Z}_L$ and $\mathbb{Z}_m\times\mathbb{Z}_n$ have $mn$ elements, so injective implies bijective.

A coincidence point satisfies $t\equiv0\pmod m$ and $t\equiv0\pmod n$, hence $t\equiv0\pmod{mn}$, which within $\mathbb{Z}_{mn}$ means only $t=0$. The statement with phase $s$ is the inhomogeneous form of the Chinese remainder theorem: two congruences have exactly one solution modulo $mn$. $\blacksquare$

</Box>

Theorem 7.2 settles something easy to get wrong: **the complexity of an overlay is not additive but multiplicative**. The two lines have periods $m$ and $n$, but after overlaying you must wait $mn$ beats to return to the initial state. "3 plus 4 equals 7" for 3:4 is only the onset count, not the period; the period is $12$.

### 7.3.2 The Klapp Ring Matrix

Draw $\mathbb{Z}_m\times\mathbb{Z}_n$ as a table with $m$ rows and $n$ columns and you get the matrix representation of a polymeter. Define $K\in\{0,1\}^{m\times n}$:
$$
K_{ij}=1 \iff \exists\, t\in A\cup B,\ t\equiv i\pmod m,\ t\equiv j\pmod n .
$$
By Theorem 7.2, when $m,n$ are coprime there is at most one such $t$, so $K$ is well defined. This $0$-$1$ matrix is called the **Klapp ring matrix** in this book: it rolls the two periods onto one torus, with rows as the fast period's phase and columns as the slow period's phase.

The Klapp ring matrix for 3:4 is $3\times4$:

```text
        j=0  j=1  j=2  j=3
  i=0   O    x    x    x
  i=1   y    .    .    .
  i=2   y    .    .    .
```

Row $i=0$ is filled by the fast rhythm (4 cells), column $j=0$ by the slow rhythm (3 cells), and the two coincide at $(0,0)$, so the union is $4+3-1=6$ cells. Gluing the rows and columns end to end turns this discrete grid into a grid on a torus; walking $12$ steps along $(i,j)\mapsto(i+1,j+1)$ visits all $12$ cells because $3$ and $4$ are coprime. If $\gcd(m,n)=g\gt1$, the torus itself does not "split"; rather, this synchronous time orbit splits into $g$ disjoint cycles on the grid, each of length $\operatorname{lcm}(m,n)$; different orbits correspond to different relative phases.

This matrix also explains an auditory phenomenon: the "locked-in" feel of a polymeter comes from the coincidence point. The two lines each turn their own circle and land together at only one phase; once you hear that coincidence, the whole loop has a "beginning". Table 5 of Experiment 7.1 shows that all five combinations have exactly $1$ coincidence—the phased version of Theorem 7.2 tells us that no matter how you shift one line, there is still only one coincidence, only its location changes.

<Box kind="experiment" title="Experiment 7.1: Euclidean rhythms, syncopation metrics, and polymeter">

```bash
python code/ch07_rhythm.py
```

The script prints its labels in Chinese; the numbers are unchanged.

Actual output (standard library only; positions numbered $0..n-1$):

::: details Expand full script output (105 lines, content unedited)

```text:no-line-numbers
ch07_rhythm.py —— 第 7 章配套实验：节奏的数学

表 1：若干欧几里得节奏 E(k,n) 的模式与循环间隔

节奏           k     n  模式（x = 起音）        循环间隔              间隔取值   
------------------------------------------------------------------------------
E(2,5)         2     5  x..x.                   3 2                   2 / 3      
E(3,7)         3     7  x..x.x.                 3 2 2                 2 / 3      
E(3,8)         3     8  x..x..x.                3 3 2                 2 / 3      
E(4,9)         4     9  x..x.x.x.               3 2 2 2               2 / 3      
E(5,8)         5     8  x.x.xx.x                2 2 1 2 1             1 / 2      
E(5,12)        5    12  x..x.x..x.x.            3 2 3 2 2             2 / 3      
E(7,12)        7    12  x.x.x.xx.x.x            2 2 2 1 2 2 1         1 / 2      
E(7,16)        7    16  x..x.x.x..x.x.x.        3 2 2 3 2 2 2         2 / 3      

E(3,8) 的间隔 3-3-2 就是古巴 tresillo（三击型）的骨架；
E(5,8) 的间隔 2-2-1-2-1 是五击型节奏（cinquillo 一类）。
所有间隔只相差不超过 1：这就是「最大均匀」的含义。

表 2：带余除法 n = q·k + r 与长短间隔的个数

节奏           q     r     k     n  长间隔(q+1) 个数    短间隔(q) 个数
------------------------------------------------------------------
E(3,8)         2     2     3     8                 2                 1
E(5,8)         1     3     5     8                 3                 2
E(4,9)         2     1     4     9                 1                 3
E(7,16)        2     2     7    16                 2                 5

由 r = n − q·k 可直接推出：长间隔恰好 r 个、短间隔恰好 k − r 个。
当 r = 0（k 整除 n）时所有间隔都等于 q，节奏退化为均匀网格。
下一步的「多出来的 r 个格子」该放在哪，正是欧几里得算法递归下去的理由。

表 3：穷举验证 1 ≤ k ≤ n ≤ 32

  测试组合数                    = 528
  闭式位置集与 Bresenham 判据一致 = 528 / 528
  所有间隔 ∈ {⌊n/k⌋, ⌈n/k⌉}      = 528 / 528
  间隔取值的最大种类数          = 2（≤ 2 即最大均匀）

也就是说，一行判据就能生成 E(k,n)，不必模拟递归分组。
闭式解 p_j = ⌊(j·n + k − 1)/k⌋ 与判据给出同一集合，误差为 0。

表 4：n = 8 的切分度量（期望 μ、方差 σ²、平均节拍权重 h、切分度 1 − h）

节奏       模式        μ（步）  σ²（步²）   平均 h   切分度       R  方位（步）
--------------------------------------------------------------------------------
E(1,8)     x.......      0.000    0.000   1.0000   0.0000   1.000        +0.0
E(2,8)     x...x...      2.000    4.000   0.7500   0.2500   0.000           —
E(3,8)     x..x..x.      3.000    6.000   0.4583   0.5417   0.138        -1.0
E(4,8)     x.x.x.x.      3.000    5.000   0.5000   0.5000   0.000           —
E(5,8)     x.x.xx.x      3.600    5.840   0.4000   0.6000   0.083        -2.0
E(6,8)     x.xxx.xx      3.667    5.556   0.3750   0.6250   0.000           —
E(7,8)     x.xxxxxx      3.857    4.980   0.3393   0.6607   0.143        -3.0
E(8,8)     xxxxxxxx      3.500    5.250   0.3125   0.6875   0.000           —

  E(7,16)  x..x.x.x..x.x.x.
    μ = 7.286 步，σ² = 21.633 步²，平均 h = 0.2411，切分度 = 0.7589，R = 0.028，方位 = -3.0 步

E(1,8) 只有一个强拍，切分度 0；E(4,8) 把重音均匀铺在 0、2、4、6，
平均节拍权重 0.5，切分度 0.5，圆重心 R = 0（旋转对称，无偏向）。
E(3,8) 的切分度 0.5417 略高于 E(4,8)；E(5,8) 的 0.6000 更高。
E(3,8) 的圆重心合成向量 R = 0.138，方位 −1 步：重音整体略偏晚。
注意：切分度随 n 变化（n = 16 的弱位更「弱」），只在同一 n 下比较才有意义。
E(7,16) 的圆重心方位 -3.0 步：向小节末尾方向偏移，但合成向量很短。

表 5：互质复合节奏的叠加（t 时刻：x = 快周期，y = 慢周期，O = 重合）

叠加        LCM  起音数  去重后   密度   重合点  周期（拍）
------------------------------------------------------
3:4          12      7      6  0.500        1       12
4:5          20      9      8  0.400        1       20
3:5          15      8      7  0.467        1       15
5:8          40     13     12  0.300        1       40
4:7          28     11     10  0.357        1       28

时间线（每格一拍，共 LCM 拍）：
  3:4  O..xy.x.yx..
  4:5  O...xy..x.y.x..yx...
  3:5  O..x.yx..xy.x..
  5:8  O....x..y.x....xy...x...yx....x.y..x....
  4:7  O...x..yx...x.y.x...xy..x...

两个互质周期只在 t = 0（以及 t = LCM）处重合，恰好 1 个重合点。
去重后的起音数 = m + n − 1：这就是「叠加不是简单相加」的定量版本。

表 6：克拉普环矩阵（3:4）—— Z_3 × Z_4 环面上的 12 个格子

        j=0  j=1  j=2  j=3
  i=0   O    x    x    x
  i=1   y    .    .    .
  i=2   y    .    .    .

行 i = t mod 3 对应快周期（每 3 拍一击），列 j = t mod 4 对应慢周期。
3:4 的 12 个时刻被中国剩余定理一一映射到 3×4 = 12 个格子。
快节奏占满一整行（4 格），慢节奏占满一整列（3 格），
并在 (0,0) 重合，所以并集只有 4 + 3 − 1 = 6 个格子被点亮。

关键数字：
  E(3,8) 的间隔            = [3, 3, 2]
  E(5,8) 的间隔            = [2, 2, 1, 2, 1]
  E(7,16) 的间隔           = [3, 2, 2, 3, 2, 2, 2]
  3:4 的周期               = lcm(3,4) = 12
  5:8 的周期               = lcm(5,8) = 40
  3:4 去重后的起音数       = 3 + 4 − 1 = 6
  5:8 去重后的起音数       = 5 + 8 − 1 = 12
```

:::

</Box>

## 7.4 Summary

This chapter broke rhythm into three layers:

$$
\underbrace{E(k,n)=\left\{\left\lfloor \frac{jn+k-1}{k}\right\rfloor\right\}}_{\text{discrete skeleton}}
\;\longrightarrow\;
\underbrace{(\mu,\sigma^2,h,\operatorname{sync})}_{\text{accent distribution}}
\;\longrightarrow\;
\underbrace{\mathbb{Z}_m\times\mathbb{Z}_n}_{\text{composite period}}
$$

Three main conclusions:

- **Evenness can be written as a one-line formula**. The positions of $E(k,n)$ are given by $\lfloor(jn+k-1)/k\rfloor$, equivalent to the Bresenham criterion $(ik\bmod n)\lt k$. Its $k$ gaps take only $\lfloor n/k\rfloor$ or $\lceil n/k\rceil$, with exactly $r=n-qk$ long gaps; when $k\mid n$ it degenerates to a uniform grid. Having at most two gap sizes is only a necessary feature—the order of the gaps also takes part in the definition. Repeated division with remainder on $(k,n)$ gives the finite recursive self-similarity that the title's "fractal" borrows.
- **Syncopation can be measured, but which ruler matters**. The syncopation degree $1-\frac1k\sum h(i)$ on $n=8$ gives $E(5,8)=0.6000 > E(3,8)=0.5417 > E(4,8)=0.5000 > E(1,8)=0$; the circular centroid's $R$ and direction add "which way it leans". Neither metric equals "ugly" or "sophisticated"; they only describe the shape of the accent distribution.
- **The period of a polymeter is the product**. For coprime $m,n$ the overlaid period is $mn$, the distinct onset count is $m+n-1$, and the density is $(m+n-1)/(mn)$: 3:4 gives $6/12=0.5$, 5:8 gives $12/40=0.3$. The Klapp ring matrix rolls the two lines into a $0$-$1$ matrix on $\mathbb{Z}_m\times\mathbb{Z}_n$, with exactly one coincidence point.

Back to the title: **"fractal" is a metaphor with a definite referent, and "chaos" is only rhetoric.** Euclidean rhythms do have finite recursive self-similarity, but no geometric fractal structure at infinite scale. The systems in this chapter are all finite-state and strictly periodic: $n$ cells admit only $2^n$ binary patterns, and a full period necessarily returns to the start. Chaos does not require "looking complex"; it has specific dynamical-systems criteria. Discrete systems can be chaotic, but one cannot use the word merely because "multi-layered periods sound complex". The polymeters here come from periods and phases, not from sensitive dependence on initial conditions.

Finally, the five opening questions: grouping comes from discretizing into $n$ cells and $k$ onsets; $E(k,n)$ gives a maximally even representative using adjacent integer gaps and their constrained ordering; syncopation can be described by metric weights and circular statistics, but it does not equal ugliness; 3:4 and 5:8 have periods $12$ and $40$ because the overlay of coprime numbers has a product period; "fractal" means finite recursive self-similarity, and "chaos" here is only a metaphor.

The next chapter leaves "beat-by-beat" discrete time and turns to melody: treat a pitch-class sequence as a Markov chain, estimate style from transition probabilities, and use entropy and surprise to explain "unexpected yet inevitable".

<Box kind="checkpoint" title="Self-check">

Close the book and write down three things: (1) the three onset positions and two gap values of $E(3,8)$; (2) why $E(8,8)$ has the highest syncopation degree yet is not really syncopated; (3) the period of the 3:4 overlay, its distinct onset count, and the dimensions of its Klapp ring matrix.

</Box>

<Box kind="exercise" title="Exercises">

1. Use Definition 7.1 to hand-compute the four positions of $E(4,9)$ and verify that the gaps are $3,2,2,2$. Then compute them again with the criterion of Algorithm 7.1; the two methods should agree.
2. Prove that if $k\mid n$, then all gaps of $E(k,n)$ equal $n/k$; conversely, if all gaps are equal, must $k\mid n$?
3. For $n=8$, compute $\mu$, $\sigma^2$, the syncopation degree, and the circular centroid $R$ of $E(2,8)$ and $E(6,8)$, and explain why $E(2,8)$ has $R=0$.
4. Write down the dimensions of the Klapp ring matrix for 5:8 and the number of lit cells; then use Theorem 7.2 to explain why there is only one coincidence no matter how the slow rhythm is shifted.
5. (Open) If the metric weights are changed to a triple-meter hierarchy ($n=12$, strong beats at $0,4,8$), how does the syncopation degree of $E(3,8)$ change? Which boundary of the model does this change illustrate?

</Box>

::: tip Next chapter
Chapter 8 treats a melody as a Markov chain: estimate a transition matrix from a 12-bar corpus, compute first-order entropy and second-order conditional entropy, and then let a program generate a melody that is "unexpected yet inevitable". [Chapter 8](/en/chapters/08-melody)
:::
