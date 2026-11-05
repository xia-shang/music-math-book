---
title: "Appendix E · Exercises and Answers"
description: "Approach, numerical answers, and common mistakes for two problems per chapter, Chapters 0–9."
---

# Appendix E · Exercises and Answers

<div class="chapter-meta">
  <span>Estimated 30 minutes</span>
  <span>Prerequisite: the end-of-chapter exercises attempted</span>
  <span>Use: check answers, diagnose mistakes</span>
</div>

Every chapter in the body ends with a set of exercises, more than forty in total. This page picks only **two** per chapter: one to practice computation, one to practice reasoning. The reason is not that the others are unimportant, but that these two represent the chapter's method — if you can do them, most of the rest are the same problem with different parameters.

Answers are written in three layers:

1. **Approach**: which definition or theorem to start from;
2. **Numbers**: results to 4 decimal places (angles in cents, information in bits);
3. **Limits**: the conditions under which the answer changes.

All numbers are computed by `code/common.py` or by the same functions used in the chapter scripts, consistent with the experiment output in the body. If your result disagrees from the third decimal place on, first check whether you have mixed up "ratio" and "cent".

<Box kind="note" title="Got It Wrong? Locate the Layer First">

Mistakes in exercises usually fall into three layers, and each is fixed differently:

- **Formula layer**: you misremembered $p=1200\log_2(f/f_0)$ or $H=-\sum p_i\log_2 p_i$. Go back to Appendix A, look up the formula, and copy it once more.
- **Parameter layer**: the formula is right, but you treated the unit of $f$ as kHz, the number of semitones as cents, or the natural logarithm as base 2. Go back to the body and check the units.
- **Interpretation layer**: the number is right, but the conclusion is stated backwards. For example, you compute that a pure fifth is $1.955$ ¢ wider than the 12-TET fifth, then say "the equal-tempered fifth is higher". Go back to the theorem and the pitfall in that chapter.

Locate the layer first, then redo; do not start the whole problem over — that usually just repeats the same mistake once more.

</Box>

## E.1 Chapter 0: Postulates and Cent Coordinates

**Problem 1**: The interval from 440 Hz to 660 Hz equals how many 12-TET semitones? How much wider than seven semitones is it?

- **Approach**: use the coordinate formula of Theorem 0.1 directly; the ratio is $660/440=3/2$; semitones equal the cent value divided by 100.
- **Answer**: $1200\log_2(3/2)=701.9550$ ¢, i.e. $7.0196$ semitones; that is $1.9550$ ¢ wider than 7 semitones (700 ¢).
- **Limits**: this "wider" is the difference of the just fifth relative to the 12-TET fifth, not an "intonation error"; Chapter 4 says the same thing the other way around: the 12-TET fifth is 1.955 ¢ narrower than the pure fifth.

**Problem 2**: Compute the cent values for 220 → 230 and 1760 → 1770. Why does the same $+10\ \text{Hz}$ roughly halve with each octave?

- **Approach**: use $1200\log_2(f_2/f_1)$ both times. For small differences, use the approximation $\Delta p\approx (1200/\ln 2)(\Delta f/f)$.
- **Answer**: 220 → 230 is $76.9564$ ¢; 1760 → 1770 is $9.8087$ ¢. The same $+10\ \text{Hz}$ at 220, 440, 880, 1760 gives $76.96$, $38.91$, $19.56$, $9.81$ ¢: each doubling of frequency halves $\Delta f/f$, and roughly halves the cent value.
- **Limits**: it is not exactly halved, because $\log_2(1+x)$ is nonlinear (only the first-order approximation gives a strict proportion); $+10$ Hz near 100 Hz is already on the order of $150$ ¢, where the small-quantity approximation fails.

## E.2 Chapter 1: Simple Harmonic Motion and Period

**Problem 1**: For a spring oscillator with $m=0.01$ kg and $k=4$ N/m, find $\omega$, $f$, $T$. Does doubling the amplitude change them?

- **Approach**: $\omega=\sqrt{k/m}$, $f=\omega/(2\pi)$, $T=1/f$.
- **Answer**: $\omega=20$ rad/s, $f=3.1831$ Hz, $T=0.3142$ s. Doubling the amplitude changes none of the three — this is the isochronism of a linear restoring force (Section 1.1.3).
- **Limits**: past its elastic limit a real spring no longer has a constant $k$, and isochronism fails; a pendulum at large angles also departs from simple harmonic motion.

**Problem 2**: What is the period of a 440 Hz pure tone in milliseconds? What is its angular frequency in rad/s?

- **Approach**: $T=1/f$, $\omega=2\pi f$; a millisecond is $10^{-3}$ s.
- **Answer**: $T=0.0022727$ s $=2.2727$ ms; $\omega=2764.6015$ rad/s.
- **Limits**: these two quantities describe a "steady-state pure tone". The attack transient of a real musical tone has no single period; $T$ is meaningful only in the steady-state segment.

## E.3 Chapter 2: Interval Addition and Frequency Conversion

**Problem 1**: Verify $\varphi(5/4)+\varphi(6/5)=\varphi(3/2)$, and find the cent value after stacking both twice and reducing modulo an octave.

- **Approach**: $\varphi$ turns multiplication of ratios into addition in cents; stacking twice means multiplying the ratio by itself twice.
- **Answer**: $386.3137+315.6413=701.9550$ ¢, consistent with $\varphi(3/2)$. Stacked twice: $2\times701.9550=1403.9100$ ¢, minus one octave $1200$ ¢ leaves $203.9100$ ¢, the major second $9:8$.
- **Limits**: "modulo octave" relies on the octave equivalence of Postulate 0.2; without treating the octave as equivalent, $1403.91$ ¢ and $203.91$ ¢ are two different pitch positions.

**Problem 2**: With A4 = 440 Hz, find the frequency at $+350$ ¢ and the pitch coordinate of 220 Hz.

- **Approach**: $f=f_0\,2^{p/1200}$, $p=1200\log_2(f/f_0)$.
- **Answer**: $f=440\times2^{350/1200}=538.5836$ Hz; $p(220)=1200\log_2(220/440)=-1200$ ¢.
- **Limits**: change the reference frequency and absolute coordinates shift as a whole, but interval differences stay the same; this is exactly the Chapter 2 exercise on "coordinate differences are reference-independent".

## E.4 Chapter 3: The Consonance Function

**Problem 1**: With $f_1=220$ Hz, compute $D$ for $2:1$, $3:2$, $5:4$. Can the $D$ of an octave be called exactly 0?

- **Approach**: $D$ sums over harmonic pairs with $i,j\le 5$, and $W(0)=0$; the octave has some partials that coincide exactly, but the truncated harmonic series still contains non-coincident cross-tone pairs.
- **Answer**: $D(2:1)=1.2168\times10^{-11}$, $D(3:2)=0.0020$, $D(5:4)=0.3680$; at four decimal places they display as $0.0000$, $0.0020$, $0.3680$. The octave's $D$ is only approximately 0: coincident terms contribute 0, non-coincident terms remain positive. Only at unison, $f_1=f_2$, do all harmonic pairs satisfy $\Delta f=0$, giving the ideal $D=0$.
- **Limits**: the fifth and the third have larger $D$ because non-coincident harmonic pairs contribute more. At 330 Hz, the fifth's $D$ becomes small enough to display as 0.000; "displays as 0" and "strictly equals 0" must be kept apart.

**Problem 2**: Change $N$ from 5 to 3. Does the ordering of the tritone and the perfect fourth by $S$ change?

- **Approach**: reducing the number of harmonics removes contributions from higher orders (amplitude $1/i$ is smaller), so $S$ rises overall, but the ordering depends on the low-order structure.
- **Answer**: it does not change. With $N=3$, $S(45:32)=0.9074$ and $S(4:3)=0.9981$; with $N=5$ they are $0.8720$ and $0.9939$. Under both values of $N$ the perfect fourth is more consonant.
- **Limits**: for very small $N$ the gap between tritone and perfect fourth is compressed; if $N=1$ only the fundamentals remain, the ordering is set by the rise-then-fall shape of $W$ as a function of frequency difference, and the valley produced by coincident higher harmonics disappears.

## E.5 Chapter 4: The Comma and Equal-Temperament Error

**Problem 1**: Compute the comma and verify the ratio $(3/2)^{12}/2^7$.

- **Approach**: the comma is 12 fifths minus 7 octaves; the ratio is $3^{12}/2^{19}$.
- **Answer**: $\text{comma}=1200(12\log_2(3/2)-7)=23.4600$ ¢; the ratio is $531441/524288=1.0136433$.
- **Limits**: this is the comma of Pythagorean tuning. Just intonation has other commas (e.g. the syntonic comma $81/80$, about $21.506$ ¢); same name, different value, do not mix them.

**Problem 2**: How many cents apart are $2^{7/12}\approx1.498307$ and $3/2$?

- **Approach**: first compute the difference of the two frequency ratios, then convert the ratio of the two into cents; watch the direction.
- **Answer**: $2^{7/12}=1.4983071$, which differs from $1.5$ by $0.0016929$; in cents, $1200\log_2(1.5/2^{7/12})=1.9550$ ¢. The 12-TET fifth is **narrower** than the pure fifth by $1.955$ ¢.
- **Limits**: this is the error of the fifth alone; the weighted RMS of Chapter 4 also includes major and minor thirds, and the winner need not be 12-TET.

## E.6 Chapter 5: Exhaustive Scale Search

**Problem 1**: Verify $\binom{12}{7}=\binom{12}{5}=792$, and explain why the two binomial coefficients are equal.

- **Approach**: use the identity $\binom{n}{k}=\binom{n}{n-k}$; replace "the 7 chosen" with "the 5 excluded".
- **Answer**: both equal 792. The seven-note and five-note searches have the same size because every 7-note set corresponds one-to-one with a 5-note complement; but the two searches have different **constraints** (seven notes require spacing, five notes require no semitone), so the results cannot be swapped directly.
- **Limits**: the identity only guarantees equal counts, not symmetric scores; the complement's consonance and triad count generally differ.

**Problem 2**: With $k=6$ and all gaps $\ge2$, prove the only gap pattern is $2\text{-}2\text{-}2\text{-}2\text{-}2\text{-}2$. What is the triad coverage of the whole-tone scale?

- **Approach**: six gaps sum to 12, and each is at least 2, so each is exactly 2. The whole-tone scale is $\{0,2,4,6,8,10\}$.
- **Answer**: the only gap pattern is $2\text{-}2\text{-}2\text{-}2\text{-}2\text{-}2$. Triad coverage $T=0$: a major or minor triad fully contained in the whole-tone scale would need a structure like $0,4,7$, but $7$ is odd and not in the set. Verify with `triads_in({0,2,4,6,8,10})` from `code/ch05_scale_search.py`, which returns 0.
- **Limits**: "triad coverage" as defined in this chapter counts only major and minor triads; the whole-tone scale contains augmented triads, but augmented triads are not counted in $T$. That is a definitional choice, not a mathematical fact.

## E.7 Chapter 6: Indicator Vectors and Quadratic Forms

**Problem 1**: Write the indicator vectors of F major and G major, verify that $\mathbf{f}_S,\mathbf{f}_D,\mathbf{f}_T$ are linearly independent. Which coordinates of the sum vector equal 2?

- **Approach**: $F=\{5,9,0\}$, $G=\{7,11,2\}$, $C=\{0,4,7\}$; take coordinates $0,4,7$ to form a $3\times3$ submatrix and check its determinant.
- **Answer**: on coordinates $(0,4,7)$ the three vectors are $(1,0,0)$, $(0,0,1)$, $(1,1,1)$; arranged in that order the determinant is $-1$ (swapping two rows gives $1$), and nonzero means linear independence. The sum vector equals 2 at coordinates 0 and 7: C belongs to both T and S, and G belongs to both T and D.
- **Limits**: linear independence is the algebraic fact that "the three function bases span a 3-dimensional subspace"; it does not guarantee that these three chords form T-S-D musically, which also needs the transition matrix and the potential.

**Problem 2**: Using the three off-diagonal entries of $K_C$, $0.858,0.803,0.999$, hand-compute the consonance of the C major triad and verify $0.8868$.

- **Approach**: the $3\times3$ submatrix has 1s on the diagonal and off-diagonal entries appearing in pairs; use $\big(\sum M_{ij}-k\big)/(k(k-1))$ from Definition 6.3.
- **Answer**: the submatrix sum is $=3+2(0.858+0.803+0.999)=8.320$; $(8.320-3)/(3\times2)=0.8867$, differing from the body's $0.8868$ only in the last rounding digit. Computing term by term with the definition gives the same number, because the quadratic form counts each off-diagonal pair twice, and dividing by $k(k-1)$ cancels exactly.
- **Limits**: this score depends on the values of $K_C$ and on the register; in a lower register the same chord's $S$ drops. Do not treat $0.8868$ as an absolute property of C major.

## E.8 Chapter 7: Euclidean Rhythms

**Problem 1**: Hand-compute the positions of $E(4,9)$ and verify the gaps $3,2,2,2$; then do it again with the Bresenham criterion.

- **Approach**: the position formula of Definition 7.1, $\lfloor(jn+k-1)/k\rfloor$, with $j=0,1,2,3$; the criterion is $(ik\bmod n)\lt k$.
- **Answer**: positions $\{0,3,5,7\}$; cyclic gaps $3,2,2,2$ (the last segment is $9-7=2$). Check the criterion position by position: for $i=0,3,5,7$, $4i\bmod9$ is $0,3,2,1$ respectively, all less than 4; no other position satisfies it.
- **Limits**: the definition of $E(k,n)$ assumes "as even as possible" and contains no cultural constraint beyond "must start at 0"; choosing another starting point is just a global shift.

**Problem 2**: If $k\mid n$, prove that all gaps of $E(k,n)$ equal $n/k$. Conversely, if all gaps are equal, must $k\mid n$?

- **Approach**: the $k$ gaps sum to $n$; each gap is an integer.
- **Answer**: if $k\mid n$, let $q=n/k$; the positions are $0,q,2q,\ldots,(k-1)q$ and all gaps are $q$. Conversely, if all $k$ gaps equal $q$, then $n=kq$, so $k\mid n$. Hence "all gaps equal" and "$k\mid n$" are equivalent.
- **Limits**: this is a result for a discrete uniform grid; if gaps may be real numbers (continuous time), "all equal" no longer forces $k\mid n$, because $n/k$ may be non-integer.

## E.9 Chapter 8: Entropy and Surprisal

**Problem 2**: If every row of a first-order chain is a uniform distribution, what are $H_1$ and the redundancy? What if every row degenerates to a point mass?

- **Approach**: a uniform distribution has $p_i=1/K$, so $H=\log_2 K$; a point mass has $H=0$.
- **Answer**: with $K=7$, a uniform row gives $H_1=\log_2 7=2.8074$ bit, redundancy $R=1-H_1/H_{\max}=0$, and any single-step guessing strategy hits with probability only $1/7$. A point-mass row gives $H_1=0$, $R=1$: given the current note, the next note is fully determined.
- **Limits**: $H_1=0$ only says "predictable given this corpus and alphabet", not that the music is "monotonous"; a fixed ostinato can still be expressive. Entropy measures uncertainty, not aesthetics.

**Problem 3**: Using the counts of the $D\to E$ row (C: 2, F: 4, G: 1), hand-compute the conditional entropy and check the inequality of Theorem 8.4.

- **Approach**: first normalize $p=(2/7,4/7,1/7)$, then compute $-\sum p\log_2 p$; rank by descending probability.
- **Answer**: $H=1.3788$ bit. Ranks: F first ($-\log_2(4/7)=0.807$), C second ($1.807$), G third ($2.807$). Check $-\log_2 p\ge\log_2 r$ one by one: F's $0.807\ge0$, C's $1.807\ge1$, G's $2.807\ge1.585$, all hold.
- **Limits**: the inequality depends on ranks assigned by descending probability; an arbitrary guessing order does not guarantee it. This order also minimizes the expected rank.

## E.10 Chapter 9: Fifth Coordinates and Two-Note Chords

**Problem 1**: Hand-compute $\nu(p)=7p$ for $p=0,1,2,3$, verify $\nu(\nu(p))=p$. Why is 7 the integer step closest to a pure fifth among the 12 notes?

- **Approach**: multiplication modulo 12; $\nu^{-1}=\nu$ is equivalent to $7^2\equiv1\pmod{12}$.
- **Answer**: $\nu(0)=0$, $\nu(1)=7$, $\nu(2)=14\equiv2$, $\nu(3)=21\equiv9$. Since $7^2=49\equiv1$, $\nu(\nu(p))=49p\equiv p$. A pure fifth is $\log_2(3/2)=0.58496$ octaves, and $12\times0.58496=7.0196$, whose nearest integer is 7.
- **Limits**: 7 is "nearest", not "exact"; each fifth misses by about $0.0196$ semitones, i.e. $1.955$ ¢, and only after 12 accumulations does it become the Pythagorean comma of about $23.46$ ¢, already computed in Chapter 4.

**Problem 2**: Prove that under $T$ each equivalence class contains 12 ordered two-note chords, and under $T/I$ contains 12 or 24. Which classes have 12?

- **Approach**: $T_n$ acts on an ordered pair $(p,q)$ as a global shift, and only $n=0$ fixes it; $I$ maps $(p,q)$ to $(-p,-q)$ and may merge two $T$ orbits.
- **Answer**: under $T$ each orbit has exactly 12 elements ($n=0,\ldots,11$ give 12 distinct results). Under $T/I$, the "unison pairs" with interval $d=q-p=0$ and the "tritone pairs" with $d=6$ have 12 each — because $I$ maps $d$ to $-d$, and $0$ and $6$ are self-inverse; the other 5 interval classes have 24 each ($d$ merges with $12-d$). The total is $12+12+5\times24=144$, consistent with the 7 $T/I$ classes.
- **Limits**: this counts **ordered** two-note pairs; if $(p,q)$ and $(q,p)$ are treated as the same unordered chord, the count drops from 144 to 78 and the class structure must be recomputed.

## E.11 How to Use These Answers

After checking your answers, do three things rather than closing the page:

1. **Classify your mistakes**: go back to the "three layers" box above and write down whether you went wrong in the formula, the parameters, or the interpretation. Only the first layer can be fixed by memorizing a formula.
2. **Change one parameter and redo**: change $f_1$ from 220 to 330, $N$ from 5 to 3, $k$ from 7 to 5, and see whether the conclusion is robust. This is the method demonstrated repeatedly in Chapters 3 and 5.
3. **Write one sentence about limits**: for each problem, write at least one sentence on "under what conditions this answer fails". If you cannot, you have remembered the number but not the model.

<Box kind="checkpoint" title="Five Questions: Can You Really Do These Problems?">

1. Without looking at the answers, can you explain why the octave's $D$ in Chapter 3 is only approximately 0 at finite display precision, while only unison $D$ can be exactly 0?
2. Why is the triad coverage of the whole-tone scale in Chapter 5 equal to 0? Is this a definitional issue or a theorem?
3. In Chapter 8, why are $H=1.3788$ and "surprisal $2.807$" not the same quantity?
4. In the $T/I$ class count of Chapter 9, why do unison pairs and tritone pairs have 12 rather than 24?
5. Pick any problem you got wrong and say whether it belongs to the formula layer, the parameter layer, or the interpretation layer.

If you can answer all five, this page can be closed; if one of them stumps you, go back to the Box in the corresponding section and reread it.

</Box>

::: tip Back to the Book
With the exercises done, you can return to the [home page](/en/) and reread the three reading routes, or go back to [Chapter 9](/en/chapters/09-topology) and walk through the topology chapter once more. The book has no standard answers, only reproducible models and clearly written limits.
:::
