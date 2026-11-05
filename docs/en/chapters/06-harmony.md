---
title: "Chapter 6 · Harmony as Linear Algebra"
description: "Write chords as vectors, progressions as matrices."
---

# Chapter 6 · Harmony as Linear Algebra

<div class="chapter-meta">
  <span>Estimated 50 minutes</span>
  <span>Prerequisite: Chapters 3 and 5</span>
  <span>Code: code/ch06_harmony.py</span>
</div>

This chapter answers five questions:

1. What exactly is a chord? A set of three notes, or a point in some space?
2. Why does a major triad sound "stable" and a diminished triad "unstable"? Can that difference be computed?
3. Why can transposition and inversion be written as matrix multiplication? What kind of group do they form?
4. Can the cycle "tonic–subdominant–dominant–tonic" be written as a Markov chain?
5. Why does a cadence feel like "falling into a pit"? What does the potential function of that pit look like?

Chapter 5 selected 7 of the 12 pitch classes and obtained a scale. Now push the camera in: **what happens when you press three of them at once?** This chapter answers in three steps: first write a chord as a vector in $\mathbb{R}^{12}$, then write the consonance relations between chords as a matrix, and finally write a "chord progression" as a transition matrix acting on probability vectors. After the three steps, "function" and "resolution" become explicit matrix computations; at the same time we will see clearly which conclusions come from definitions and which are only physical analogies that aid intuition.

## 6.1 Chord Vectors: Pitch-Class Set Theory

### 6.1.1 From "Three Notes" to a "12-Dimensional Vector"

Traditional notation writes `C E G`, three letters. A programmer would rather write it as an array:

$$
\mathbf{v}_{C} = (1,0,0,0,1,0,0,1,0,0,0,0),
$$

Entries $0,4,7$ are 1 and the rest are 0. This is not for looks; it is to **let chords enter linear algebra**: once a chord is a vector, transposition is matrix multiplication, consonance is a quadratic form, and the distance between chords is a norm.

<Box kind="definition" title="Definition 6.1 (indicator vector of a chord)">

Let pitch classes be numbered by $\mathbb{Z}_{12}$. For a pitch-class set $S \subset \mathbb{Z}_{12}$, define its **indicator vector** $\mathbf{v}(S) \in \mathbb{R}^{12}$ by
$$
\mathbf{v}(S)_p = \begin{cases} 1, & p \in S,\\ 0, & p \notin S. \end{cases}
$$
If $\lvert S \rvert = k$, call $S$ a $k$-note chord. There are $\binom{12}{3} = 220$ trichords; $\mathbb{Z}_{12}$ has $2^{12} = 4096$ subsets in total.

</Box>

The advantage of the indicator vector is that "set operations = vector operations": union is componentwise maximum, intersection is componentwise product, and complement is $\mathbf{1} - \mathbf{v}$. This chapter uses only addition and multiplication, but you should remember this translation rule—it will return in Chapter 9 when we discuss topology.

The three most common chords, written as vectors, are:

$$
\mathbf{v}_{C} = \mathbf{e}_0 + \mathbf{e}_4 + \mathbf{e}_7,\qquad
\mathbf{v}_{Cm} = \mathbf{e}_0 + \mathbf{e}_3 + \mathbf{e}_7,\qquad
\mathbf{v}_{C\dim} = \mathbf{e}_0 + \mathbf{e}_3 + \mathbf{e}_6,
$$

where $\mathbf{e}_p$ is the $p$-th standard basis vector. The three pitch classes of the $C$ major triad are "root, major third, perfect fifth"; the $C$ minor triad swaps in a "minor third", and the diminished triad swaps in a "diminished fifth". **A chord's quality is just the relative spacing of its three nonzero coordinates.**

### 6.1.2 Transposition and Inversion Are Permutation Matrices

In music theory, transposition is "raise everything by $n$ semitones". In vector language it is a coordinate rotation: entry $p$ moves to entry $p+n$. Such an operation can be written as a $12\times12$ permutation matrix.

<Box kind="definition" title="Definition 6.2 (transposition and inversion operators)">

For $n \in \mathbb{Z}_{12}$, define **transposition** $T_n$ by
$$
(T_n \mathbf{v})_p = \mathbf{v}_{(p-n) \bmod 12},
$$
with matrix form $(P_n)_{p,q} = 1$ if and only if $q = (p-n) \bmod 12$. Define **inversion** $I$ by
$$
(I\mathbf{v})_p = \mathbf{v}_{(-p) \bmod 12},
$$
with matrix form $(J)_{p,q} = 1$ if and only if $q = (-p) \bmod 12$.

</Box>

Table 4 of Experiment 6.1 applies these four operators to the C major triad:

| Transformation | Result | Chord name |
| --- | --- | --- |
| Identity | `C E G` | C major |
| $T_4$ | `E G# B` | E major |
| $T_7$ | `G B D` | G major |
| $I$ | `C F G#` | F minor |

$T_n$ translates root, third, and fifth together, so of course it is still the same kind of chord. $I$ is more interesting: it flips the C major triad into an **F minor triad**—inversion turns "major third on top" into "minor third at the bottom", so major and minor triads are paired.

<Box kind="theorem" title="Theorem 6.1 (transposition and inversion form a dihedral group)">

Let $P_n$ be the permutation matrix of $T_n$ and $J$ the permutation matrix of $I$. Then
$$
P_n P_m = P_{n+m},\qquad J P_n J = P_{-n},\qquad J^2 = \mathbf{I}_{12}.
$$
Hence the set $\{P_n\}_{n=0}^{11} \cup \{J P_n\}_{n=0}^{11}$ forms a group of order 24 under matrix multiplication, isomorphic to the dihedral group $D_{12}$.

</Box>

<Box kind="proof" title="Proof">

For any vector $\mathbf{v}$, $(P_n P_m \mathbf{v})_p = (P_m \mathbf{v})_{p-n} = \mathbf{v}_{p-n-m} = (P_{n+m}\mathbf{v})_p$, hence $P_n P_m = P_{n+m}$. Next, $(J P_n J \mathbf{v})_p = (P_n J\mathbf{v})_{-p} = (J\mathbf{v})_{-p-n} = \mathbf{v}_{p+n} = (P_{-n}\mathbf{v})_p$; and $(J^2\mathbf{v})_p = (J\mathbf{v})_{-p} = \mathbf{v}_{p}$, so $J^2 = \mathbf{I}$. The $P_n$ are pairwise distinct and the $J P_n$ are pairwise distinct, and $J P_n$ cannot be written as some $P_m$ (because $J$ fixes position 0 and flips the others), giving $12 + 12 = 24$ elements. The relation $J P_n J = P_{-n}$ is exactly the defining relation of the dihedral group. $\blacksquare$

</Box>

This group-theoretic fact explains a notational phenomenon: **why equivalence classes of pitch-class sets are first quotiented by transposition and then by inversion**. The 220 trichords merge into 19 classes under transposition, then into 12 classes under inversion (line 69 of the experiment output). In other words, there are only 12 trichord "shapes"; the rest is transpositional and inversional disguise.

<Box kind="pitfall" title="Common misconception: inversion means 'playing the chord backwards'">

Inversion $I$ is not time reversal but a **mirror on the pitch axis**: $p \mapsto -p$. It turns a major triad into a minor triad and an ascending interval into a descending one. Time reversal is called "retrograde"; pitch mirroring is called "inversion". The former swaps temporal order, the latter reverses interval direction; do not mix up the terms or the operations.

</Box>

## 6.2 Tensor Products and Chord Space

### 6.2.1 The Consonance Matrix: 66 Interval Pairs in One Table

Chapter 3 gave the consonance $S(f_1,f_2)$ of any two notes. Compute it on all 12 pitch classes and you get a $12\times12$ matrix:

$$
M_{pq} = S\!\left(f(p), f(q)\right),\qquad f(p) = C_4 \cdot 2^{p/12}.
$$

<Box kind="definition" title="Definition 6.3 (consonance matrix and chord quadratic form)">

Call $M \in \mathbb{R}^{12\times12}$ the **consonance matrix**, where $M_{pq} = S(p,q)$. For the indicator vector $\mathbf{v}$ of a chord with $k \ge 2$ notes, define **chord consonance** as the average score over all unordered note pairs:
$$
C(\mathbf{v})
= \frac{2}{k(k-1)}\sum_{p\lt q}v_pv_qM_{pq}
= \frac{\mathbf{v}^{\mathsf{T}}M\mathbf{v}-\sum_p M_{pp}v_p}{k(k-1)}.
$$
The second equality uses $v_p^2=v_p$: first subtract the true diagonal contribution from the quadratic form, then divide by the number of ordered off-diagonal pairs $k(k-1)$. The script approximates the diagonal entries as 1, so $(\mathbf{v}^{\mathsf{T}}M\mathbf{v}-k)/(k(k-1))$ is a common approximation; here we keep $M_{pp}$ so that the definition agrees exactly with the pairwise-averaging script.

</Box>

Table 1 of Experiment 6.1 gives the first 12 rows of this matrix. A few numbers are worth remembering:

- The diagonal is $1.00$ to two decimals, but not exactly 1: at the same pitch, same-order harmonics align, while cross-order harmonic pairs still contribute a tiny positive roughness;
- The perfect fifth (e.g. $C$–$G$) also shows $1.00$, because a 12-TET fifth differs from $3:2$ by only $1.955\ \text{¢}$, very close to 1 in the current register and model;
- The smallest off-diagonal entry is $0.46$, at the adjacent pairs $A$–$A\sharp$ and $A\sharp$–$B$; it cannot be lumped under "minor second or tritone", because the score also depends on register and on the specific harmonic coincidences.

The matrix is symmetric: $M_{pq} = M_{qp}$. This is no coincidence: in the definition of $S$, $\Delta f$ is taken in absolute value and the critical bandwidth uses a $\min$, so the order of the two notes does not affect the result.

<Box kind="theorem" title="Proposition 6.2 (diagonal entries are row maxima in this numerical consonance submatrix)">

Let $K$ be the $k\times k$ submatrix of this chapter's fixed numerical matrix $M$ on some chord, $K_{ij}=M_{s_i s_j}$. A row-by-row check in the script gives
$$
K_{ii}\gt K_{ij}\qquad(i\ne j).
$$
That is, **the diagonal entry is the largest element in its row**. This is not the standard linear-algebra conclusion of "strict diagonal dominance"; the latter requires $K_{ii}\gt\sum_{j\ne i}\lvert K_{ij}\rvert$, which this chapter neither proves nor needs.

</Box>

<Box kind="proof" title="Basis of the check">

At the same pitch, only harmonic pairs with $a=b$ satisfy $W(0)=0$; pairs with $a\ne b$ are still summed and are not removed by the model. Hence $D(f,f)$ is generally a very small positive number, not exactly 0. For $C_4$, for example, the actual run gives $D\approx1.2249\times10^{-16}$, so $S=1/(1+D)$ is only extremely close to 1.

Different pitch classes have different fundamentals, so the $a=b=1$ term already has $W(x_{11})\gt0$, and the corresponding off-diagonal entry is less than 1. Comparing diagonal and off-diagonal magnitudes further depends on frequencies and parameters; this chapter only checks this $12\times12$ numerical matrix row by row, without generalizing it to a theorem for arbitrary frequencies. $\blacksquare$

</Box>

This numerical property says only one thing: in the current model, the same-pitch diagonal entry exceeds the other interval entries in the same row. It has no direct bearing on whether a chord is stable, or whether the matrix is positive definite or invertible. In Experiment 6.1 the $3\times3$ submatrix of the C major triad is, to three decimals,

$$
K_C = \begin{pmatrix}
1.000 & 0.858 & 0.999\\
0.858 & 1.000 & 0.803\\
0.999 & 0.803 & 1.000
\end{pmatrix},
$$

and within display precision each row's diagonal entry is the row maximum, consistent with Proposition 6.2; the $1.000$ here is a rounded value.

<div class="audio-row">

<AudioDemo src="/audio/chord-just.wav" title="Just-intonation C major triad C–E–G" hint="5:4 and 3:2 both hold: the harmonics of the three notes overlap heavily, so the sound fuses." />

<AudioDemo src="/audio/chord-tet.wav" title="12-TET C major triad C–E–G" hint="The third is off by 13.7 ¢ and the fifth by 2 ¢: you can hear a slight shimmer." />

</div>

### 6.2.2 The Quadratic Form Is a Contraction of the "Chord × Pitch Class" Tensor

$\mathbf{v}^{\mathsf{T}} M \mathbf{v}$ can also be written as a tensor contraction. The outer product $\mathbf{v} \otimes \mathbf{v}$ is a $12\times12$ matrix that is 1 exactly when $(p,q)$ satisfy $p,q \in S$; it records "all ordered note pairs in the chord". Hence

$$
\mathbf{v}^{\mathsf{T}} M \mathbf{v} = \sum_{p,q} (\mathbf{v}\otimes\mathbf{v})_{pq} M_{pq} = \langle \mathbf{v}\otimes\mathbf{v},\, M\rangle_F,
$$

where the right side is the Frobenius inner product, with the outer product as a second-order tensor. In plain language: **multiply the chord's ordered note pairs by the interval consonance table term by term and sum, and you get the unnormalized total score**. Definition 6.3 still subtracts the diagonal terms and divides by the number of note pairs to obtain the average consonance between distinct notes. The matrix $M$ is the fixed "world model"; the vector $\mathbf{v}$ is the variable "query". The tensor contraction adds no new physics; it is only another notation for the same computation.

Because $M$ is fixed, the scores of all $k$-note chords in chord space can be computed in one pass. Table 3 of Experiment 6.1 is the ranking of all 220 trichords:

- First place is the $G$ major triad (`D G B`), $0.9759$—it has a perfect fifth ($G$–$D$) and a major third ($G$–$B$), both falling in the valleys of the Chapter 3 roughness curve;
- Four of the top five are major triads and one is minor; the last three are non-triads squeezed within a semitone ($0.4949 \sim 0.4958$);
- Averaged by type, major and minor are both $0.9099$, augmented is $0.8959$, diminished is $0.8440$.

One easy misreading of this ranking: **the augmented triad does not rank low**. For C–E–G♯, its internal consonance is $0.8757$, even higher than C minor's $0.8562$. Its three interval pairs are two major thirds (C–E, E–G♯, $400\ \text{¢}$ each) and a minor sixth (C–G♯, $800\ \text{¢}$), not "three major thirds"; in this register all of them have high pairwise consonance scores. On the other hand, the augmented triad lacks a perfect fifth and divides the octave equally, so its root and function can only be judged from context. **Consonance is not stability, and still less is it function in a particular work.**

### 6.2.3 Model Boundaries: Register, Timbre, and "Function"

Table 2 has an "all-class average" column that includes all 12 roots. You will find that the same C major chord scores $0.8868$ with C as root but $0.9099$ on the all-class average—that is, **the same chord drifts in score when the register changes**. The reason is again the critical bandwidth from Chapter 3: near $C_4$, $E$–$G$ are only $63\ \text{Hz}$ apart, right on the roughness peak; raise the whole chord an octave and the gap doubles, so the roughness changes.

<Box kind="pitfall" title="Common misconception: chord consonance is an 'intrinsic property of the chord'">

It is not. $C(\mathbf{v})$ depends on three modeling choices: (1) register (we use $C_4$ as the reference); (2) timbre ($N=5$, $1/k$ harmonic decay); (3) weighting (equal weight per pair). Change the register and the G major triad may no longer rank first; change to a timbre with richer harmonics or distortion, and the whole ranking must be recomputed—you cannot predict in advance which type will rise.

The conclusions this chapter can support are limited to: **at these 12 specific pitches, under this harmonic parameter set**, major and minor have the highest all-class averages and diminished is lower. This is a numerical result, not a register-independent law of types, and it certainly cannot by itself explain every textbook use of "consonant/dissonant". Traditional harmony also uses roots, modes, voice leading, and context, none of which is contained in $C(\mathbf{v})$.

</Box>

## 6.3 Harmonic Function (T-S-D-T): Dynamics in a State Space

### 6.3.1 Three Function Basis Vectors

Traditional harmony divides chords into three functions: **tonic** (T), **subdominant** (S), and **dominant** (D). Using the C major scale from Chapter 5, each corresponds to a triad:

<Box kind="definition" title="Definition 6.4 (function basis vectors)">

In C major, define
$$
\mathbf{f}_T = \mathbf{e}_0 + \mathbf{e}_4 + \mathbf{e}_7,\quad
\mathbf{f}_S = \mathbf{e}_5 + \mathbf{e}_9 + \mathbf{e}_0,\quad
\mathbf{f}_D = \mathbf{e}_7 + \mathbf{e}_{11} + \mathbf{e}_2.
$$
These are the indicator vectors of $C$ major, $F$ major, and $G$ major. The three vectors are linearly independent and span a 3-dimensional subspace of $\mathbb{R}^{12}$, called the **function subspace**.

</Box>

Verifying linear independence is easy: $\mathbf{f}_T$ is nonzero at coordinate 4 while the other two are zero there; $\mathbf{f}_S$ is nonzero at 5 while the other two are zero; $\mathbf{f}_D$ is nonzero at 11 while the other two are zero. The three coordinates do not overlap, so the rank is 3.

A chord progression is then a polyline in the function subspace. The traditional notation $T \to S \to D \to T$ corresponds to the vector sequence

$$
\mathbf{f}_T \to \mathbf{f}_S \to \mathbf{f}_D \to \mathbf{f}_T.
$$

### 6.3.2 Voice-Leading Distance: How Far Apart Two Chords Are

To turn a "progression" into dynamics, we first need a distance between chords. The most natural definition is **voice-leading distance**: pair up the notes of the two chords one-to-one so that the sum of semitone motions is minimized.

<Box kind="definition" title="Definition 6.5 (voice-leading distance)">

Let $A, B$ be two $k$-note chords, each viewed as a pitch-class set. Define
$$
d(A,B) = \min_{\sigma \in \mathrm{Bij}(A,B)} \sum_{a \in A} \delta\big(a, \sigma(a)\big),
\qquad
\delta(a,b) = \min\big(\lvert a-b \rvert,\ 12 - \lvert a-b \rvert\big),
$$
where $\mathrm{Bij}(A,B)$ is the set of all bijections from $A$ to $B$. $\delta$ is the shortest arc length on the pitch-class circle. This definition looks only at pitch-class sets and does not record actual octaves, voicing, or doublings, so it is a "minimum pitch-class motion", not the minimum voice motion over all possible orchestrations.

</Box>

Table 5 of Experiment 6.1 gives the six distances among the three functions. Most noteworthy:

- $T \to S$: `C→C`, `E→F`, `G→A`, total distance $3$;
- $T \to D$: `C→B`, `E→D`, `G→G`, total distance $3$;
- $S \to D$: `F→G`, `A→B`, `C→D`, total distance $6$;
- $D \to T$: `G→G`, `B→C`, `D→E`, total distance $3$.

$S \to D$ takes $6$ semitones with this choice of pitch-class representatives, twice the other three steps. However, this **does not** imply that "subdominant to dominant must take a detour": $IV\to V$ is a common progression, and other inversions and actual registers can change the voice motion. The $3,3,6,3$ here is only the result for the chosen pitch-class sets under a simplified metric, not a ranking of real orchestration.

With a distance in hand, we can define transition probabilities. This chapter adopts a minimal Boltzmann-style rule:

$$
P_{ij} = \frac{w_j \, e^{-d_{ij}/2}}{\sum_{k} w_k \, e^{-d_{ik}/2}},
$$

where $w_T = 1.00$, $w_S = 0.85$, $w_D = 0.75$ are the "gravity weights" of the three functions. Both $w$ and $d$ are **modeling choices**: $d$ comes from the pitch-class distance above, while $w$ comes from the artificial prior that "the tonic should have a higher long-run share". Because $d_{ij}=d_{ji}$, setting all $w$ to 1 makes $P$ symmetric, so the uniform distribution is stationary; "symmetric" here means $P_{ij}=P_{ji}$, not that every state moves to all neighbors with equal probability.

Plugging in the experimental data gives the transition matrix

$$
P = \begin{pmatrix}
0.737 & 0.140 & 0.123\\
0.201 & 0.765 & 0.034\\
0.220 & 0.042 & 0.739
\end{pmatrix}.
$$

Each row sums to 1, and **the diagonal entry exceeds any off-diagonal entry in the same row**: functions have inertia and do not change on every beat. Note that $P_{SD} = 0.034$ is pitifully small and $P_{DS} = 0.042$ is also small—this corresponds directly to the distance $6$ for $S \to D$ and $D \to S$. The "shape" of the matrix is a shadow of the distance structure.

### 6.3.3 A Markov Chain and Its Stationary Distribution

Treat a function as a state; the next beat's function depends only on the current function. This is a three-state Markov chain:

$$
\boldsymbol{\pi}_{t+1} = \boldsymbol{\pi}_t P,
\qquad
\boldsymbol{\pi}_t \in \Delta^2 = \left\{ (p_T,p_S,p_D) : p_i \ge 0,\ \textstyle\sum p_i = 1 \right\}.
$$

Table 6 of Experiment 6.1 runs 24 steps from $T$ and yields the sequence

$$
T\,T\,T\,T\,D\,D\,D\,D\,S\,S\,S\,S\,S\,S\,S\,S\,S\,S\,D\,T\,S\,S\,S\,S.
$$

24 steps is too short; the empirical frequencies ($0.208/0.583/0.208$) are far from the stationary distribution. Power iteration over 4000 steps gives

$$
\boldsymbol{\pi} = (0.443,\ 0.308,\ 0.249).
$$

<Box kind="theorem" title="Theorem 6.3 (the stationary distribution exists and is unique)">

If $P$ is a row-stochastic matrix with all entries strictly positive, then there is a unique probability vector $\boldsymbol{\pi}$ satisfying $\boldsymbol{\pi} P = \boldsymbol{\pi}$, with $\pi_i \gt 0$ for all $i$. It equals $\lim_{t\to\infty} \boldsymbol{\pi}_0 P^t$ and is independent of the initial distribution.

</Box>

<Box kind="proof" title="Proof">

This is the Perron–Frobenius theorem specialized to positive matrices. All entries of $P$ are positive, so its spectral radius is 1 and is a simple eigenvalue, corresponding to a unique (normalized) positive left eigenvector $\boldsymbol{\pi}$; all other eigenvalues have modulus strictly less than 1. By our convention $\boldsymbol{\pi}$ is a row vector and $\mathbf{1}$ is the all-ones column vector, so $P^t$ converges to the rank-1 matrix $\mathbf{1}\boldsymbol{\pi}$, not $\mathbf{1}\boldsymbol{\pi}^{\mathsf{T}}$. Hence every initial distribution $\boldsymbol{\pi}_0$ satisfies $\boldsymbol{\pi}_0P^t\to\boldsymbol{\pi}$. $\blacksquare$

</Box>

$\pi(T)=0.443$ is largest and $\pi(D)=0.249$ smallest, meaning that in this chain the tonic has the highest **long-run visit share** and the dominant the lowest. The true attractor of the distribution dynamics is the stationary distribution $\boldsymbol{\pi}$, not the single state $T$: the chain still moves among the three states, and $T$ is not absorbing.

In particular, do not translate a lower $\pi(D)$ as "$D$ cannot stay". In the matrix, $P_{DD}\approx0.739$, even slightly above $P_{TT}\approx0.737$; the one-step self-loop probability and the long-run share are not the same quantity. $\boldsymbol{\pi}$ is determined jointly by all state weights, distances, and row normalization; it cannot be explained from one diagonal alone.

<Box kind="pitfall" title="Common misconception: this chain can predict real harmonic progressions">

It cannot. It encodes only two pieces of information: voice-leading distances, and prior weights for the three functions. Real harmonic progressions are also shaped by melody, rhythm, lyrics, form, and even the performer's breathing. More fatally, it assumes "the next beat depends only on the current chord"—whereas in real music, the chord two beats ago and the melody note in progress both change the next choice.

The point of this chain is not prediction but **a computable baseline**: any real progression can be compared against it to see how far it deviates. Where the deviation is large is often where the music gets interesting.

</Box>

## 6.4 Cadences: Attractors and Potential Wells

### 6.4.1 Writing the Tonal Center as a Pit

The stationary distribution $\boldsymbol{\pi}$ gives each function's long-run visit share. To draw "higher share, lower position" as a potential-well diagram, borrow the logarithmic relation between probability and energy in the Boltzmann distribution and define:

$$
E(i) = -\log \pi_i.
$$

The last column of Table 6 in Experiment 6.1 is exactly this: $E(T) = 0.814$, $E(S) = 1.177$, $E(D) = 1.392$. $T$ has the lowest potential and $D$ the highest. That is, **the tonic is the bottom of the well and the dominant is a ledge on its wall**.

<Box kind="definition" title="Definition 6.6 (function potential)">

Let $\boldsymbol{\pi}$ be the stationary distribution of the transition matrix $P$. Define the **potential** of function $i$ as $E(i) = -\log \pi_i$. For any two functions $i \to j$, the potential difference is
$$
\Delta E_{ij} = E(j) - E(i) = \log\frac{\pi_i}{\pi_j}.
$$
If $\Delta E_{ij} \lt 0$, call the transition **downhill**; otherwise it is uphill.

</Box>

### 6.4.2 Cadences: Describing "Resolution" by Potential Difference

The "dominant resolves to tonic" in a cadence can be compared to a downhill transition. But three discrete functions have no continuous gradient, and $E=-\log\pi$ is not a physical potential derived from voice-leading distance; so what we have here is a **potential difference**, not gradient descent in the strict sense. Table 7 of Experiment 6.1 splits $D\to T$ into three voices:

| D note | T note | Motion (semitones) |
| --- | --- | --- |
| $G$ | $G$ | $0$ |
| $B$ | $C$ | $+1$ |
| $D$ | $E$ | $+2$ |

$G$ stays put, $B$ rises a semitone to $C$, and $D$ rises two semitones to $E$, for a total motion of $3$ semitones. Under the pitch-class sets and bijection rule of Definition 6.5, this is the minimum total distance. At the same time $E(D)-E(T)\approx0.578\gt0$, so $D\to T$ is also downhill on the artificial potential map. **Voice-leading distance and potential difference point to the same progression here, but they are two independent definitions; this agreement is a useful analogy, not a general mathematical theorem of "resolution".**

<AudioDemo src="/audio/cadence-just.wav" title="Just-intonation cadence C–F–G–C" hint="Each chord uses 5:4 and 3:2 internally: from dominant to tonic all three voices take the shortest path." />

<AudioDemo src="/audio/cadence-tet.wav" title="12-TET cadence C–F–G–C" hint="Same voice leading, but the thirds and fifths no longer align exactly; the sound shimmers slightly." />

This perspective explains two things:

1. **Why the dominant often carries a leading tone**: $B$ is the seventh degree of C major and is only one semitone from the tonic $C$, providing a short melodic resolution path. The one step here is $B\to C$, not the distance from the whole $D$ chord to $T$; the latter's minimum total pitch-class motion is still $3$.
2. **Why a cadence sounds like an ending**: in this chapter's potential map, $T$ is the lowest position, and after landing on $T$ there is no lower discrete state. One can stay on $T$ (self-loop probability $0.737$) or move on to $S$ or $D$; so the "sense of ending" is analogized by the lowest potential, not implemented by the chain stopping.

<Box kind="pitfall" title="Common misconception: the dominant must resolve to the tonic">

Not necessarily. Real music has the **deceptive cadence**: $V \to vi$, where the dominant goes to the submediant and sounds like "you expected an ending, but it turned a corner". In this chapter's matrix that corresponds to a transition from $D$ to a non-$T$ state. Our three-state chain has no $vi$, so it cannot simulate a deceptive cadence—which shows precisely that the model is too coarse.

Nor must a phrase land on $T$ every time: stopping on an incomplete tonic, or closing on $V$ to form a half cadence, leaves varying degrees of openness. This chapter has only three coarse states $T,S,D$ and cannot distinguish these orchestration and cadence types. The potential map can describe the common route "back to the tonic function", but it cannot serve as a theory of cadence classification.

</Box>

<Box kind="checkpoint" title="Self-check">

Close the book and write down three things: (1) why a chord can be written as a vector in $\mathbb{R}^{12}$, and why transposition is a permutation matrix; (2) why $D(f,f)$ at the same pitch is not exactly zero, and why Proposition 6.2 cannot be called standard "diagonal dominance"; (3) how many semitones each of the three voices moves in the cadence D→T, and why this distance and the $-\log\pi$ potential difference are two independent definitions.

</Box>

<Box kind="experiment" title="Experiment 6.1: Consonance matrix, chord ranking, and function transitions">

```bash
python code/ch06_harmony.py
```

The script prints its labels in Chinese; the numbers are unchanged.

Actual output (reference $C_4 = 261.626\ \text{Hz}$):

::: details Expand full script output (133 lines, content unedited)

```text:no-line-numbers
ch06_harmony.py —— 第 6 章配套实验：和弦的线性代数

表 1：12 音级协和度矩阵 M（行 = 第一个音，列 = 第二个音）

        C   C#    D   D#    E    F   F#    G   G#    A   A#    B
----------------------------------------------------------------
  C  1.00 0.51 0.48 0.64 0.86 0.97 0.83 1.00 0.83 0.97 0.80 0.64
 C#  0.51 1.00 0.51 0.49 0.68 0.89 0.98 0.84 1.00 0.84 0.97 0.83
  D  0.48 0.51 1.00 0.50 0.50 0.72 0.91 0.99 0.84 1.00 0.84 0.98
 D#  0.64 0.49 0.50 1.00 0.49 0.51 0.76 0.93 0.99 0.85 1.00 0.85
  E  0.86 0.68 0.50 0.49 1.00 0.48 0.53 0.80 0.94 0.99 0.86 1.00
  F  0.97 0.89 0.72 0.51 0.48 1.00 0.48 0.54 0.84 0.95 1.00 0.88
 F#  0.83 0.98 0.91 0.76 0.53 0.48 1.00 0.47 0.57 0.88 0.96 1.00
  G  1.00 0.84 0.99 0.93 0.80 0.54 0.47 1.00 0.47 0.59 0.91 0.96
 G#  0.83 1.00 0.84 0.99 0.94 0.84 0.57 0.47 1.00 0.47 0.62 0.94
  A  0.97 0.84 1.00 0.85 0.99 0.95 0.88 0.59 0.47 1.00 0.46 0.65
 A#  0.80 0.97 0.84 1.00 0.86 1.00 0.96 0.91 0.62 0.46 1.00 0.46
  B  0.64 0.83 0.98 0.85 1.00 0.88 1.00 0.96 0.94 0.65 0.46 1.00

对角线在两位小数下全为 1.00，但并非严格等于 1：跨阶谐波对仍有微小正贡献。
非对角元范围 0.46 ~ 1.00；纯五度也四舍五入为 1.00。
最小值出现在 A–A♯、A♯–B 这两个相邻音对，不应笼统归给三全音。M 对称：S(i,j) = S(j,i)。

表 2：四类三和弦的内部协和度

性质      C 为根                均值 S        最小 S      全类平均  三个音程                
----------------------------------------------------------------------------------------
大三      C 大三                0.8868        0.8026        0.9099  300 ¢ / 400 ¢ / 700 ¢   
小三      C 小三                0.8562        0.6428        0.9099  300 ¢ / 400 ¢ / 700 ¢   
增三      C 增三                0.8757        0.8291        0.8959  400 ¢ / 400 ¢ / 800 ¢   
减三      C 减三                0.7437        0.6428        0.8440  300 ¢ / 300 ¢ / 600 ¢   

以 C 为根时：大三 0.8868 > 增三 0.8757 > 小三 0.8562 > 减三 0.7437。
把 12 个根音平均后，大三与小三都约为 0.9099（相差不到 0.0001）：
它们的音程多重集相同（3、4、7 个半音），只是排列顺序不同。
增三 0.8959，减三 0.8440。

C 大三和弦的 3×3 协和子矩阵 K：

           C      E      G
    C   1.000  0.858  0.999
    E   0.858  1.000  0.803
    G   0.999  0.803  1.000

在三位小数下，对角元为行内最大；这不是线性代数中「严格对角占优」的标准结论（命题 6.2）。

表 3：C(12,3)=220 个三音集合的协和度排序

 名次  音级                            均值 S  识别          
------------------------------------------------------------
    1  D G B                           0.9759  G 大三        
    2  C# F# A#                        0.9703  F# 大三       
    3  C F A                           0.9623  F 大三        
    4  D F# B                          0.9613  B 小三        
    5  E G# B                          0.9584  E 大三        
  ...
  218  E F F#                          0.4958  （非三和弦）  
  219  D D# E                          0.4953  （非三和弦）  
  220  D# E F                          0.4949  （非三和弦）  

按类型平均（12 个根音的集合都算）：
  大三：12 个集合，平均 0.9099，最高 0.9759
  小三：12 个集合，平均 0.9099，最高 0.9613
  增三：4 个集合，平均 0.8959，最高 0.9141
  减三：12 个集合，平均 0.8440，最高 0.9194
排在最前的是大三和弦与小三和弦（G、F#、F、Bm、E 等）：
一个纯五度加一个三度，正好落在 3.3 节粗糙度曲线的谷底上。

220 个三音集合按平移去重剩 19 类，再按平移+倒置去重剩 12 类。

表 4：移位与倒置作为置换矩阵（以 C 大三和弦为例）

变换        作用后的向量（音级）            和弦名                        
--------------------------------------------------------------------------
恒等        C E G                           C 大三                        
T_4         E G# B                          E 大三                        
T_7         D G B                           G 大三                        
I           C F G#                          F 小三                        

T_n 把 {0,4,7} 送到 {n,n+4,n+7}；I 把它送到 {0,5,8}，即 F 小三和弦。
T_n ∘ T_m = T_{n+m}，且 I ∘ T_n ∘ I = T_{-n}，所以 {T_n, I} 生成 24 阶二面体群。
表 4 只展示了 4 个代表；完整群有 24 个元素（12 个平移 + 12 个倒置平移）。

表 5：T / S / D 的声部进行距离与转移矩阵

方向        最优配对（起点→终点）               总距离（半音）
------------------------------------------------------------
T→S         C→C，E→F，G→A                                  3
T→D         C→B，E→D，G→G                                  3
S→T         F→E，A→G，C→C                                  3
S→D         F→G，A→B，C→D                                  6
D→T         G→G，B→C，D→E                                  3
D→S         G→F，B→A，D→C                                  6

转移矩阵 P（行 = 当前功能，列 = 下一功能）：
          T       S       D
  T   0.737   0.140   0.123
  S   0.201   0.765   0.034
  D   0.220   0.042   0.739

P_ij ∝ w_j · exp(−d_ij/2)，w 表示三个功能的「引力」权重（T 最大）。
对角线元都大于同行的任一非对角元：功能有惯性，不会每拍都换。

表 6：从 T 出发的功能序列（固定随机种子）

  T T T T D D D D S S S S S S S S S S D T S S S S

  功能   经验频率   平稳分布 π   势能 −log π
   T     0.208      0.443       +0.814
   S     0.583      0.308       +1.177
   D     0.208      0.249       +1.392

24 步只是短样本，经验频率与 π 有偏差；4000 次幂迭代使分布收敛到 π。
π 是分布动力学的吸引子；π(D) 较低来自权重与连通结构，不等于 D 的自环率低。

表 7：终止式 D→T 的声部移动

D 的音      T 的音      移动（半音）  方向      
--------------------------------------------
G           G                     +0  保持      
B           C                     +1  升        
D           E                     +2  升        

势能差：E(D) − E(T) = −log π(D) − (−log π(T)) = 0.578。
三个声部的总移动 = 3 个半音；G 保持不动、B 上行半音、D 上行两个半音。
E(T) 最低，所以 D→T 是沿势能下降方向的一步 —— 这就是「属和弦解决到主和弦」。

关键数字：
  12 音级对数            = C(12,2) = 66
  三音集合数            = C(12,3) = 220
  C 大三和弦内部 S 均值 = 0.8868
  增三和弦内部 S 均值   = 0.8757
  T→S / S→D / D→T 距离  = 3 / 6 / 3
```

:::

</Box>

## 6.5 Summary

This chapter broke harmony into three layers of linear structure:

$$
\underbrace{\mathbf{v} \in \{0,1\}^{12}}_{\text{chord = vector}}
\;\longrightarrow\;
\underbrace{M_{pq} = S(p,q)}_{\text{consonance = matrix}}
\;\longrightarrow\;
\underbrace{\boldsymbol{\pi}_{t+1} = \boldsymbol{\pi}_t P}_{\text{progression = Markov chain}}
$$

Three main conclusions:

- **A chord is an indicator vector, and transformations are permutation matrices**: $T_n$ and $I$ generate a dihedral group of order 24; the 220 trichords leave 19 classes under $T$ and 12 under $T/I$. A chord has only 12 "shapes".
- **Chord consonance comes from a quadratic form, but the true diagonal terms must be subtracted**: $C(\mathbf{v})=(\mathbf{v}^{\mathsf{T}}M\mathbf{v}-\sum_pM_{pp}v_p)/(k(k-1))$. Under the current register and timbre parameters, major and minor have the highest all-class averages, and diminished is the lowest of the four triad types; the augmented score is not low, though its root and function still require context.
- **Harmonic progressions can be coarse-grained into a Markov chain**: build $P$ from voice-leading distance ($T\to S$, $T\to D$, and $D\to T$ are all 3 semitones; $S\to D$ is 6), with stationary distribution $\boldsymbol{\pi}=(0.443,0.308,0.249)$. It describes long-run visit shares rather than turning some state into an absorbing one; using $E=-\log\pi$, the potential drop of $D\to T$ is $0.578$.

In one sentence: **functions can be encoded as states, and "resolution" can be illustrated by potential difference; matrices make the computation clear, but they do not supply the model with all the causal structure of real music.**

The next chapter leaves the "vertical" structure of harmony for the "horizontal" structure: rhythm on the time axis. You will see that the Euclidean algorithm can generate African drum patterns, and that syncopation can be measured by the mean and variance of a probability distribution.

<Box kind="exercise" title="Exercises">

1. Write the indicator vectors of the $F$ major and $G$ major triads and verify that $\mathbf{f}_S, \mathbf{f}_D$ are linearly independent of $\mathbf{f}_T$. Which coordinates of the sum vector $\mathbf{f}_T + \mathbf{f}_S + \mathbf{f}_D$ equal 2? Which "common tones" do these correspond to?
2. Use the three off-diagonal entries of $K_C$ ($0.858,0.803,0.999$) to hand-compute the consonance of the C major triad. The three-decimal rounded values give about $0.8867$, slightly different from the script's $0.8868$ obtained from the unrounded matrix; then write it again with the quadratic form of Definition 6.3 and explain why the numerator subtracts $\sum_pM_{pp}v_p$ rather than subtracting $k$ without comment.
3. Change the gravity weights of $P$ to $w_T = w_S = w_D = 1$ and recompute $P$ and its stationary distribution. Does $\boldsymbol{\pi}$ become uniform? Why?
4. Verify that the total voice-leading distance $3$ for $D \to T$ is minimal: enumerate all $3! = 6$ pairings and list the total distance for each.
5. (Open) If we add a "submediant" ($vi$, the A minor triad) to the three-state chain, the transition matrix becomes $4\times4$. Construct a $P$ that can produce the deceptive cadence $V \to vi$, and explain how its stationary distribution changes.

</Box>

::: tip Next chapter
Chapter 7 treats the time axis as a number line and uses the Euclidean algorithm to generate rhythms: $E(3,8)$, $E(5,8)$, $E(7,16)$. You will see that the "asymmetry" of African drums is in fact maximal evenness, and that syncopation can be measured by the shift of the centroid.
:::
