---
title: "Appendix A · Mathematical Toolkit"
description: "Eight groups of formulas and one conversion table: a quick reference for the book's mathematics."
---

# Appendix A · Mathematical Toolkit

<div class="chapter-meta">
  <span>Estimated 25 minutes</span>
  <span>Prerequisites: Chapters 0–9</span>
  <span>Use: look things up as needed</span>
</div>

Each time the main text introduces a mathematical tool, we try to explain it on the spot. But some formulas deserve a page of their own: they recur, and each time they appear they wear a different coat. This appendix compresses the mathematics used throughout the book into eight sections. Each formula gets one sentence saying what it is talking about, and no proofs — the proofs are in the main text.

Reading advice: no need to read from start to finish. If you forget how cents convert, see A.1 and A.8; if matrix transposes confuse you, see A.4; if you want to understand the relation between "entropy" and "surprisal", see A.6. Each section notes the chapters it mainly serves.

## A.1 Logarithms and Exponentials: Turning Multiplication into Addition

The definition of a logarithm is one sentence: $\log_b x$ is "what power of $b$ equals $x$":

$$
y=\log_b x \quad\Longleftrightarrow\quad b^y=x.
$$

Three laws of operation support all the derivations that follow:

$$
\log_b(xy)=\log_b x+\log_b y,\qquad
\log_b\frac{x}{y}=\log_b x-\log_b y,\qquad
\log_b x^n=n\log_b x.
$$

**Intuition**: logarithms translate geometric sequences into arithmetic sequences. Each time the frequency is multiplied by a fixed ratio, the pitch rises by a fixed difference; that is why intervals can be computed by "addition".

The change-of-base formula says that the base only changes the unit, not the structure:

$$
\log_b x=\frac{\ln x}{\ln b},\qquad
\log_2 x=\frac{\ln x}{\ln 2}\approx 1.442695\ln x.
$$

The book uses $\log_2$ throughout, because the unit in information theory is the bit: heads or tails of a fair coin each carry $1$ bit of information, and $\log_2 2=1$.

Translating a "frequency ratio" into an "interval" gives the core formula of Chapter 2:

$$
p=1200\log_2\frac{f}{f_0}
\quad\Longleftrightarrow\quad
f=f_0\,2^{p/1200}.
$$

<Box kind="definition" title="Definition A.1 (cent coordinates of an interval)">

Let two frequencies be $f_1,f_2$; define the interval between them as
$$
p_{12}=1200\log_2\frac{f_2}{f_1}\ \text{¢}.
$$
If a reference frequency $f_0$ is also introduced, each note has an absolute pitch coordinate $p=1200\log_2(f/f_0)$. An interval is a difference of coordinates and is independent of the reference frequency: $p_{12}=p_2-p_1$.

</Box>

Three immediate corollaries of this definition are worth memorizing:

1. **An octave is 1200 ¢**: when $f_2/f_1=2$, $\log_2 2=1$, and multiplying by 1200 gives 1200;
2. **A semitone is 100 ¢**: 12-TET divides 1200 ¢ into 12 equal parts;
3. **Intervals add**: multiplication of ratios $f_3/f_1=(f_3/f_2)(f_2/f_1)$ corresponds to addition of cents $p_{13}=p_{23}+p_{12}$.

Common ratios converted to cents, rounded to 4 decimal places (computed by `cents_of_ratio` in `code/common.py`):

| Interval | Frequency ratio | cents |
| --- | --- | --- |
| Perfect octave | $2:1$ | 1200.0000 |
| Perfect fifth | $3:2$ | 701.9550 |
| Perfect fourth | $4:3$ | 498.0450 |
| Just major third | $5:4$ | 386.3137 |
| Just minor third | $6:5$ | 315.6413 |
| Major second | $9:8$ | 203.9100 |
| Minor second | $16:15$ | 111.7313 |
| Tritone | $45:32$ | 590.2237 |
| Harmonic seventh | $7:4$ | 968.8259 |

Note the last two rows: $45:32$ is only "one" tritone; the 12-TET tritone is 600.0000 ¢. And $7:4$ is the natural seventh, 31.1741 ¢ below the 12-TET minor seventh (1000 ¢). **The same name can correspond to different ratios**, so this book writes ratios where possible and interval names sparingly.

<Box kind="pitfall" title="Do not treat cents as a linear unit">

"Raising by 100 Hz" and "raising by 100 ¢" are two different things. Starting from A4 = 440 Hz, raising by 100 ¢ gives $440\times 2^{1/12}=466.16$ Hz, only 26.16 Hz more; raising by 100 Hz gives 540 Hz, which is $1200\log_2(540/440)=354.5$ ¢, close to a perfect fourth. Cents are a ratio unit, hertz a linear unit; the two cannot be added.

</Box>

There is also an engineering habit in computation: do not round intermediate steps early. Writing $701.9550$ as $702$ accumulates error; the reason the chain of fifths in Chapter 4 can reveal the 23.46 ¢ comma is that it keeps decimals throughout.

## A.2 Simple Harmonic Motion: The Standard Solution of a Second-Order Linear Equation

Chapter 1 starts from an ideal spring. Let the mass be $m$, the spring constant $k$, and the displacement $x(t)$; the linear restoring force gives

$$
m\ddot x+kx=0
\quad\Longleftrightarrow\quad
\ddot x+\omega_0^2x=0,\qquad \omega_0=\sqrt{\frac{k}{m}}.
$$

Its general solution is a linear combination of sine and cosine, or a single cosine:

$$
x(t)=A\cos(\omega_0 t+\varphi).
$$

Three quantities carry all the information: amplitude $A$, initial phase $\varphi$, angular frequency $\omega_0$. Period and frequency are

$$
T=\frac{2\pi}{\omega_0},\qquad f=\frac{\omega_0}{2\pi}=\frac{1}{T}.
$$

**Intuition**: this equation remembers only two things — inertia ($m\ddot x$) and restoring force ($kx$). The sine that comes out is the ceasefire these two forces negotiate.

Energy passes back and forth between kinetic and potential, with the total conserved:

$$
E=\frac12 m\omega_0^2A^2=\frac12 kA^2.
$$

For A4 = 440 Hz, $\omega_0=2\pi\times 440=2764.60\ \text{rad/s}$ and the period is $T=2.2727\ \text{ms}$. These numbers come up often when writing audio code.

Real systems also have damping. Add a damping term proportional to velocity and the equation becomes

$$
\ddot x+2\gamma\dot x+\omega_0^2x=0,
$$

and in the underdamped case ($\gamma\lt\omega_0$) the solution is

$$
x(t)=Ae^{-\gamma t}\cos(\omega t+\varphi),\qquad
\omega=\sqrt{\omega_0^2-\gamma^2}.
$$

**Intuition**: damping mainly changes the envelope $e^{-\gamma t}$, and corrects the frequency only at second order. So "the sound turns dull" is usually heard first as faster amplitude decay, not as an obvious drop in pitch. The quality factor $Q=\omega_0/(2\gamma)$ measures "how long it rings": high $Q$, slow decay, narrow spectrum.

<Box kind="note" title="Isochronism holds only for linear systems">

"Amplitude does not affect frequency" is a property of the linear equation, not a universal law. At large amplitudes the restoring force may no longer be a linear function of displacement, the effective spring constant changes with amplitude, and the frequency drifts with amplitude. All models in this book assume small amplitudes and the linear approximation.

</Box>

## A.3 Fourier Series: Decomposing a Waveform into Tuning Forks

A signal of period $T$ and angular frequency $\omega=2\pi/T$ can be written as a trigonometric series:

$$
f(t)=\frac{a_0}{2}+\sum_{n=1}^{\infty}\left(a_n\cos n\omega t+b_n\sin n\omega t\right),
$$

with coefficients given by integrals:

$$
a_n=\frac{2}{T}\int_0^T f(t)\cos(n\omega t)\,dt,\qquad
b_n=\frac{2}{T}\int_0^T f(t)\sin(n\omega t)\,dt.
$$

The complex form of the same thing is more compact:

$$
f(t)=\sum_{n=-\infty}^{\infty}c_ne^{in\omega t},\qquad
c_n=\frac{1}{T}\int_0^T f(t)e^{-in\omega t}\,dt.
$$

For $n\gt 0$, $c_n=(a_n-ib_n)/2$ and $c_{-n}=(a_n+ib_n)/2$. $2\lvert c_n\rvert=\sqrt{a_n^2+b_n^2}$ is the sine amplitude of the $n$-th harmonic, and $\arg c_n$ is its phase.

**Intuition**: the Fourier series answers "which tuning forks make up this waveform, how loud each one is, and at what phase it starts". Time domain and frequency domain are not two things but two layouts of the same information.

Coefficients of three common waveforms (sine terms only; suitable phases chosen for all three):

| Waveform | Nonzero coefficients | Decay rate | Sound |
| --- | --- | --- | --- |
| Square wave | $b_n=\dfrac{4}{\pi n}$, $n$ odd | $1/n$ | sharp, with an "electric" edge |
| Sawtooth wave | $b_n=\dfrac{2}{\pi n}(-1)^{n+1}$ | $1/n$ | bright, with a buzz |
| Triangle wave | $b_n=\dfrac{8}{\pi^2n^2}(-1)^{(n-1)/2}$, $n$ odd | $1/n^2$ | soft, close to the human voice |

The faster the coefficients decay, the "smoother" the waveform. The $1/n$ decay of the square wave corresponds to a jump; the $1/n^2$ decay of the triangle wave corresponds to a continuous curve with corners — the same rule holds in image compression and audio coding.

The frequency-domain version of energy conservation is Parseval's theorem:

$$
\frac{1}{T}\int_0^T\lvert f(t)\rvert^2\,dt
=\frac{a_0^2}{4}+\frac12\sum_{n=1}^{\infty}\left(a_n^2+b_n^2\right)
=\sum_{n=-\infty}^{\infty}\lvert c_n\rvert^2.
$$

**Intuition**: as much energy as there is in the waveform, there is in the spectrum; only the bookkeeping changes.

Practical computation uses the discrete Fourier transform (DFT). For a sampled sequence $x_0,\dots,x_{N-1}$ of length $N$:

$$
X_k=\sum_{n=0}^{N-1}x_ne^{-2\pi ikn/N},\qquad
x_n=\frac{1}{N}\sum_{k=0}^{N-1}X_ke^{2\pi ikn/N}.
$$

The frequency resolution is $1/(NT_{\text{s}})$, where $T_{\text{s}}$ is the sampling interval; the highest representable frequency is the Nyquist frequency $1/(2T_{\text{s}})$.

<Box kind="pitfall" title="The Gibbs phenomenon does not “go away”">

Approximating a square wave with a finite Fourier sum always produces overshoot near the jump, about 9% of the jump amplitude. Adding terms only makes the overshoot narrower, not lower. So "compute a few more terms and it is perfect" is wrong; the correct statement is "compute a few more terms and the error concentrates in an ever narrower region".

</Box>

## A.4 Matrices, Inner Products, and Stochastic Matrices

The inner product of two $n$-dimensional real vectors is

$$
\langle \mathbf{u},\mathbf{v}\rangle=\sum_{i=1}^{n}u_iv_i,
$$

and the norm is $\lVert\mathbf{u}\rVert=\sqrt{\langle\mathbf{u},\mathbf{u}\rangle}$. The Cauchy–Schwarz inequality gives

$$
\lvert\langle\mathbf{u},\mathbf{v}\rangle\rvert\le\lVert\mathbf{u}\rVert\,\lVert\mathbf{v}\rVert.
$$

**Intuition**: the inner product measures "how aligned two vectors are". The cosine of the angle is $\langle\mathbf{u},\mathbf{v}\rangle/(\lVert\mathbf{u}\rVert\lVert\mathbf{v}\rVert)$.

A matrix is a tabulation of a linear transformation. The book uses three kinds repeatedly:

- **Transpose** $\mathbf{A}^{\mathsf{T}}$: rows and columns swap, $(A^{\mathsf{T}})_{ij}=A_{ji}$;
- **Permutation matrix**: exactly one 1 in each row and each column, all else 0; its job is to "move coordinates";
- **Stochastic matrix**: nonnegative entries, each row summing to 1; its job is to "move probability".

For $n\in\mathbb{Z}_{12}$, the transposition operator of Chapter 6 is written as the permutation matrix

$$
(P_n)_{p,q}=1 \quad\Longleftrightarrow\quad q=(p-n)\bmod 12,
$$

and the inversion operator as

$$
(J)_{p,q}=1 \quad\Longleftrightarrow\quad q=(-p)\bmod 12.
$$

**Intuition**: a permutation matrix does not stretch, only rearranges; so it preserves length, inner products, and anything that depends only on relative position, such as "consonance".

A symmetric matrix satisfies $M=M^{\mathsf{T}}$; its quadratic form is

$$
Q(\mathbf{v})=\mathbf{v}^{\mathsf{T}}M\mathbf{v}=\sum_{i,j}M_{ij}v_iv_j.
$$

A symmetric matrix can always be orthogonally diagonalized:

$$
M=U\Lambda U^{\mathsf{T}},\qquad U^{\mathsf{T}}U=\mathbf{I},
$$

where $\Lambda$ is the diagonal matrix of real eigenvalues. This property guarantees that the quadratic form can be written as a weighted sum of eigenvalues in orthogonal coordinates; Chapter 6 actually uses only symmetry and the quadratic-form notation, and does not need to diagonalize first in order to rank.

A stochastic matrix $P$ satisfies $P_{ij}\ge0$ and $\sum_jP_{ij}=1$. If a probability row vector $\boldsymbol{\pi}$ satisfies

$$
\boldsymbol{\pi}P=\boldsymbol{\pi},
$$

it is called a **stationary distribution**. The Perron–Frobenius theorem guarantees that an irreducible, aperiodic stochastic matrix has a unique stationary distribution, all of whose components are strictly positive. The functional transition matrix of Chapter 6 falls in this range.

<Box kind="pitfall" title="Row-stochastic or column-stochastic: pick one">

Some textbooks make columns sum to 1, others rows. The two conventions differ by a transpose, but mixing them makes the two sides of $\boldsymbol{\pi}P=\boldsymbol{\pi}$ disagree. This book uses **row-stochastic** throughout: $P_{ij}$ is the probability of moving from $i$ to $j$, states are row vectors, and the update is written $\boldsymbol{\pi}_{t+1}=\boldsymbol{\pi}_tP$.

</Box>

If every row and every column of a matrix sums to 1 (doubly stochastic), then the uniform distribution is its stationary distribution. Chapter 9 uses exactly this property to prove that "a translation-invariant random walk has no directional preference", with circular centroid $R=0$.

## A.5 Tensor Products and Outer Products: A Chord as a Table

The outer product of two vectors is a matrix:

$$
(\mathbf{u}\otimes\mathbf{v})_{ij}=u_iv_j,
\qquad
\mathbf{u}\otimes\mathbf{v}=\mathbf{u}\mathbf{v}^{\mathsf{T}}.
$$

**Intuition**: the inner product compresses two vectors into a number; the outer product spreads them into a table. Cell $(i,j)$ records "component $i$ of $u$ times component $j$ of $v$".

The Frobenius inner product of matrices is the elementwise inner product:

$$
\langle A,B\rangle_F=\sum_{i,j}A_{ij}B_{ij}=\operatorname{tr}(A^{\mathsf{T}}B).
$$

Thus the chord consonance of Chapter 6 can be written as

$$
\mathbf{v}^{\mathsf{T}}M\mathbf{v}
=\langle \mathbf{v}\otimes\mathbf{v},M\rangle_F.
$$

**Intuition**: $\mathbf{v}\otimes\mathbf{v}$ records all **ordered note pairs** in the chord (a C major triad has 9 pairs, including 3 notes paired with themselves), and $M$ records the consonance of every pair; multiplying cell by cell and summing is "looking up and adding the consonances of all internal intervals of this chord".

The tensor product (Kronecker product) assembles two tables into one large table. If $A$ is $m\times n$ and $B$ is $p\times q$, then $A\otimes B$ is $mp\times nq$, written in blocks as

$$
A\otimes B=
\begin{pmatrix}
a_{11}B & \cdots & a_{1n}B\\
\vdots & \ddots & \vdots\\
a_{m1}B & \cdots & a_{mn}B
\end{pmatrix}.
$$

**Intuition**: the outer product handles "two vectors", the tensor product handles "two matrices"; the latter suits multi-layer structures such as "pitch class × pitch class × chord type". Chapter 6 uses only the outer product, but knowing that the tensor product exists makes Chapter 9's chord space easier to read.

<Box kind="pitfall" title="The outer product is not the dot product">

$\mathbf{u}\otimes\mathbf{v}$ is a matrix, $\mathbf{u}\cdot\mathbf{v}$ is a scalar. In $\mathbf{v}^{\mathsf{T}}M\mathbf{v}$, $\mathbf{v}$ is a column vector and $\mathbf{v}^{\mathsf{T}}$ a row vector; the order of multiplication cannot be reversed. Reverse it and you get a $12\times12$ matrix instead of a score.

</Box>

## A.6 Probability, Entropy, and Markov Chains

A probability distribution is a set of nonnegative numbers summing to 1:

$$
p_i\ge0,\qquad \sum_{i=1}^{K}p_i=1.
$$

The entropy of a random variable $X$ is defined as

$$
H(X)=-\sum_{i=1}^{K}p_i\log_2p_i.
$$

The convention is $0\log_2 0=0$ (in the limiting sense). The range of entropy is

$$
0\le H(X)\le\log_2K,
$$

with equality on the right at the uniform distribution. **Intuition**: entropy is "average surprise" — how many bits, on average, you need to encode the outcome. The more uniform the distribution, the harder it is to guess, and the larger the entropy.

Joint and conditional entropy of two variables:

$$
H(X,Y)=-\sum_{x,y}p(x,y)\log_2p(x,y),
\qquad
H(X\mid Y)=H(X,Y)-H(Y).
$$

The chain rule:

$$
H(X,Y)=H(X)+H(Y\mid X)=H(Y)+H(X\mid Y).
$$

**Intuition**: the conditional entropy $H(X\mid Y)$ is "how much uncertainty about $X$ remains once $Y$ is known". The more you know, the smaller the remaining entropy; this is "conditioning does not increase entropy":

$$
H(X\mid Y)\le H(X).
$$

Mutual information measures "how much $Y$ actually tells you about $X$":

$$
I(X;Y)=H(X)-H(X\mid Y)=H(X)+H(Y)-H(X,Y)\ge0.
$$

KL divergence measures the difference between two distributions:

$$
D_{\mathrm{KL}}(p\Vert q)=\sum_ip_i\log_2\frac{p_i}{q_i}\ge0.
$$

Cross-entropy is the average length of "encoding data from $p$ with $q$":

$$
H(p,q)=-\sum_ip_i\log_2q_i=H(p)+D_{\mathrm{KL}}(p\Vert q).
$$

The surprisal of a single outcome is

$$
s_i=-\log_2p_i,
$$

and its expectation is exactly the entropy: $\mathbb{E}[s]=H(X)$. Chapter 8's "unexpected yet inevitable" works on this identity: there must be nonzero $s_i$, but the average $s_i$ must not be too large.

A Markov chain uses a transition matrix to describe "the next step depends only on the current state":

$$
\Pr(X_{t+1}=j\mid X_t=i)=P_{ij},\qquad \sum_jP_{ij}=1.
$$

The stationary distribution satisfies $\boldsymbol{\pi}=\boldsymbol{\pi}P$. The first-order and second-order chains of Chapter 8, and the pitch-class walk of Chapter 9, all have this form.

Substituting the measured values of Chapter 8 into the formulas checks your understanding:

| Quantity | Formula | Measured in Chapter 8 |
| --- | --- | --- |
| Maximum entropy | $\log_2 7$ | 2.8074 bit |
| Marginal entropy | $H(X)$ | 2.6046 bit |
| First-order conditional entropy | $H(X_t\mid X_{t-1})$ | 1.2167 bit |
| Redundancy | $1-H_1/H_{\max}$ | 0.5666 |

After knowing the previous note, the first-order conditional entropy is still $1.2167/2.8074\approx43.3\%$ of the maximum entropy; that is the remaining normalized uncertainty. Relative to the uniform seven-note baseline, uncertainty is reduced by $56.7\%$, which is the redundancy $R$ defined in this book. If the question is "how much uncertainty does the context remove relative to the marginal distribution", the right figure is $(2.6046-1.2167)/2.6046\approx53.3\%$; the two denominators must not be mixed.

<Box kind="pitfall" title="Entropy is a property of a distribution, not of a sequence">

The same sequence, evaluated with different models, yields different entropies. To say "the entropy of this melody is 2.6 bit" you must also say "with which distribution, of what order, over what alphabet". Outside a model, the number is meaningless.

</Box>

When samples are few, plug-in estimation systematically underestimates entropy (many symbols occur only once and are treated as "very certain"). Chapter 8 applies the Miller–Madow correction to the first-order conditional entropy grouped by predecessor: 18 nonzero joint cells, 7 nonempty rows, 47 transitions, giving an increment of $(18-7)/(2\times47\ln2)=0.1688$ bit, which raises the estimate from 1.2167 to 1.3855 bit. The correction is a reminder that **the numbers in the table are estimates, not truth**.

## A.7 Graphs and Shortest Paths

A graph $G=(V,E)$ consists of a vertex set and an edge set. A weighted graph assigns a nonnegative weight $w(u,v)$ to each edge. The length of a path is the sum of edge weights, and the shortest-path length between two vertices is written $d(u,v)$. If the graph is disconnected, a distance may be infinite.

The adjacency matrix $A$ is defined as

$$
A_{ij}=\begin{cases}w(i,j),& (i,j)\in E,\\ 0,& \text{otherwise}.\end{cases}
$$

**Intuition**: the adjacency matrix writes "who can reach whom, at what cost" as a table; graph algorithms propagate on that table.

<Box kind="algorithm" title="Algorithm A.1 (Dijkstra shortest path)">

```text
Dijkstra(G, s):
  for each v in V: d[v] = ∞, prev[v] = None
  d[s] = 0
  Q = 以 d 为键的最小优先队列，初始只含 s
  while Q 非空:
    u = extract_min(Q)
    for each (u, v, w) in E:
      if d[u] + w < d[v]:
        d[v] = d[u] + w
        prev[v] = u
        insert_or_decrease(Q, v, d[v])
  return d, prev
```

</Box>

Implemented with a binary heap, the complexity is $O((V+E)\log V)$. **Intuition**: each time, start from "the cheapest outstanding promise currently known" and relax its neighbors — because all edge weights are nonnegative, the cheapest promise cannot be overturned by a later path.

The tonal graph of Chapter 9 has 24 nodes and 108 undirected edges, with diameter (the shortest cost between the two most distant keys) 9.0. The shortest path from C major to F♯ minor costs 6, and from C major to B♭ minor 8; Dijkstra gives not just the numbers but the whole modulation route.

<Box kind="pitfall" title="Negative edge weights break Dijkstra">

The correctness of Dijkstra depends on "nonnegative edge weights". With a negative edge, a vertex already "settled" could still be overwritten by a cheaper path, and the greedy choice is wrong; use Bellman–Ford instead. The tonal-graph weights in this book are all positive (key-signature difference plus cross-mode penalty), so Dijkstra is safe.

</Box>

## A.8 Conversion Table and Common Constants

Finally, the high-frequency numbers on one page. They are all computed by `code/common.py` and the scripts of Chapters 1–9, and can be checked directly in Python.

| Quantity | Value | Note |
| --- | --- | --- |
| A4 | 440.0000 Hz | reference frequency of this book |
| C4 | 261.6256 Hz | $440\times 2^{-9/12}$ |
| Semitone ratio | 1.059463 | $2^{1/12}$ |
| 1 ¢ at A4 | 0.2542 Hz | $440(2^{1/1200}-1)$ |
| $\ln 2$ | 0.693147 | for change of base |
| $\log_2 e$ | 1.442695 | for change of base |
| Pythagorean comma | 23.4600 ¢ | interval of $(3/2)^{12}/2^7$ |
| 12 perfect fifths | 8423.4600 ¢ | 23.46 ¢ more than 7 octaves |
| 7 octaves | 8400.0000 ¢ | the "target" for closing the fifth chain |

Common destinations starting from 440 Hz:

| Interval | cents | Frequency |
| --- | --- | --- |
| Up a semitone | +100.0000 | 466.16 Hz |
| Up a just major third | +386.3137 | 550.00 Hz |
| Up a perfect fourth | +498.0450 | 586.67 Hz |
| Up a perfect fifth | +701.9550 | 660.00 Hz |
| Up an octave | +1200.0000 | 880.00 Hz |

Three mental arithmetic rules:

1. **Add intervals = multiply ratios.** See two cents, add them; see two ratios, multiply them. Do not mix.
2. **One semitone ≈ 5.95% frequency increase** ($2^{1/12}-1=0.05946$); 1 ¢ is only about 0.058%.
3. **An octave is 1200 ¢, a fifth about 702 ¢, a fourth about 498 ¢, a major third about 386 ¢.** Memorize these four anchors and the rest can be estimated.

<Box kind="checkpoint" title="Self-check: four questions you can answer at once">

1. Starting from 440 Hz, go up a 3:2 — what is the frequency? What is the interval in cents?
2. First-order entropy 1.2167 bit, maximum entropy 2.8074 bit — what is the redundancy?
3. A tonal graph with 24 keys and 108 edges — what is its diameter?
4. Why is $H(X\mid Y)\le H(X)$ not contradicted by $I(X;Y)\ge0$?

</Box>

All the answers can be found in the main text: 660 Hz and 701.9550 ¢ (Chapters 2 and 4); $1-1.2167/2.8074=0.5666$ (Chapter 8); 9.0 (Chapter 9); the part by which conditional entropy decreases is exactly the mutual information, two sides of the same thing (A.6).

::: tip Next Stop
Better to run formulas than to memorize them. Appendix B gives the list of ten scripts, the complete API of `common.py`, and "how to add your own experiment".
:::
