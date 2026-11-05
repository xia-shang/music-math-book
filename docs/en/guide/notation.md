# Notation and Conventions

This book tries to give each symbol exactly one meaning. Definitions appear at first use; this page collects them in one table.

## Frequency and Pitch

| Symbol | Meaning | Unit | First appearance |
| --- | --- | --- | --- |
| $f$ | frequency | Hz | Ch. 0 |
| $T$ | period, $T = 1/f$ | s | Ch. 1 |
| $\omega$ | angular frequency, $\omega = 2\pi f$ | rad/s | Ch. 1 |
| $a_n,b_n$ | cosine and sine coefficients of the $n$-th harmonic | — | Ch. 1 |
| $\varphi$ | initial phase of simple harmonic motion | rad | Ch. 1 |
| $f_0$ | reference frequency (440 Hz by default in this book) | Hz | Ch. 0 |
| $p$ | pitch coordinate, $p = 1200\log_2(f/f_0)$ | cent (¢) | Ch. 0 |
| $\Delta p$ | interval, the difference of two pitch coordinates | cent | Ch. 0 |
| $r$ | frequency ratio, $r = f_2/f_1$ | — | Ch. 0 |

## Consonance and Tuning Systems

| Symbol | Meaning | Unit | First appearance |
| --- | --- | --- | --- |
| $\mathrm{CB}(f)$ | critical bandwidth | Hz | Ch. 3 |
| $W(x)$ | roughness kernel, $x=\Delta f/(0.25\,\mathrm{CB})$ | — | Ch. 3 |
| $D(f_1,f_2)$ | dissonance (roughness) | — | Ch. 3 |
| $S$ | consonance score, $S = 1/(1+D)$ | $(0,1]$ | Ch. 3 |
| $f_k$ | frequency of the $k$-th degree of $n$-TET, $f_k=f_0 2^{k/n}$ | Hz | Ch. 4 |
| $e_i(n)$ | deviation of $n$-TET from the $i$-th target interval | cent | Ch. 4 |

## Sets and Matrices

| Symbol | Meaning | First appearance |
| --- | --- | --- |
| $\mathbb{Z}_{12}$ | cyclic group of the twelve pitch classes | Ch. 2 |
| $S$ | pitch-class set, $S \subseteq \mathbb{Z}_{12}$ | Ch. 5 |
| $\mathbf{v}_C$ | 12-dimensional indicator vector of chord $C$ | Ch. 6 |
| $\langle \mathbf{u}, \mathbf{v}\rangle$ | inner product, $\sum_i u_i v_i$ | Ch. 6 |
| $\mathbf{f}_T,\mathbf{f}_S,\mathbf{f}_D$ | basis vectors of the tonic, subdominant, and dominant functions | Ch. 6 |
| $P_{ij}$ | Markov transition probability, from state $i$ to $j$ | Ch. 6 |
| $H(X)$ | entropy, $-\sum_i p_i \log_2 p_i$ | Ch. 8 |

## Writing Conventions

- **Definition**: introduces a new term and gives its mathematical expression and conditions of use.
- **Postulate**: a hypothesis that cannot be proved inside this book and depends on physical or physiological facts.
- **Theorem**: a conclusion derived from the definitions and postulates, with a proof or proof sketch.
- **Runnable experiment**: code that finishes in under 3 seconds and produces a checkable number.
- All intervals are in **cents** (1 octave = 1200 ¢) unless another unit is stated explicitly.
- Frequency ratios are written $m:n$; when both are integers they are called an **integer ratio**.
