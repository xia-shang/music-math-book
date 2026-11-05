---
title: "Chapter 9 · Tonality and Atonality: A Topology"
description: "A map of modulation and atonality drawn with the circle of fifths, a tonal graph, and random walks."
---

# Chapter 9 · Tonality and Atonality: A Topology

<div class="chapter-meta">
  <span>Estimated 45 minutes</span>
  <span>Prerequisites: Chapters 2, 5, 6</span>
  <span>Code: code/ch09_topology.py</span>
</div>

This chapter answers five questions:

1. Why is the circle of fifths a circle rather than a line?
2. What shape is the space of chords? Does the "Möbius strip" claim hold up?
3. From C major to F♯ minor, what is the minimum number of keys you must pass through?
4. Why does atonal music sound "without direction"?
5. Which of these topological metaphors are theorems, and which are mere rhetoric?

The first eight chapters dealt with the local: how intervals are computed, how scales are chosen, how chords are stacked, how rhythm is divided, how melodies connect. This chapter pulls the lens back and asks a different question: **when these local rules are assembled, what shape does the whole have?** The answer is three geometric objects: the circle of fifths is a circle, the space of dyads is a torus, and the 24 major and minor keys form a graph. Only with a shape can we talk about distance and paths: how far a modulation is, how to take the shortest route, and why atonality cannot find a direction.

Let us be blunt up front: topological vocabulary is easily abused in writing of this kind. A sentence like "chord space is a Klein bottle" sounds profound, but unless it says clearly **which equivalence relation was quotiented out and which discrete set was made continuous**, it is just rhetoric. This chapter gives several conclusions that can be written down rigorously, and devotes a section to explaining which metaphors must be discounted.

## 9.1 The Circle of Fifths and the Topology of Pitch Space

### 9.1.1 The Circle of Fifths Is a Circle

Chapter 4 used a chain of fifths to generate 12 notes, and computed that 12 fifths and 7 octaves differ by $23.46\ \text{¢}$. Now let us rephrase the chain: give each key a "position".

<Box kind="definition" title="Definition 9.1 (fifth coordinate)">

For a pitch class $p \in \mathbb{Z}_{12}$, define its **fifth coordinate**
$$
\nu(p) = 7p \bmod 12 ,
$$
meaning "how many perfect fifths up from C does it take to reach $p$". The major tonic pitch class at position $n$ is $7n \bmod 12$. Conversely, the pitch-class coordinate of position $n$ is also $7n$: the formulas for the two directions are identical. This is no coincidence; the theorem in the next paragraph explains why.

</Box>

<Box kind="theorem" title="Theorem 9.1 (the fifth coordinate is an involution on Z₁₂)">

The map $\nu:\mathbb{Z}_{12}\to\mathbb{Z}_{12}$, $\nu(p)=7p$, is a bijection, and $\nu^{-1}=\nu$.

</Box>

<Box kind="proof" title="Proof">

If $7p\equiv 7q \pmod{12}$, then $7(p-q)\equiv 0\pmod{12}$. Because $\gcd(7,12)=1$, we get $12\mid(p-q)$; and since $p,q\in\{0,\ldots,11\}$, necessarily $p=q$. Hence $\nu$ is injective, and an injection on a finite set is a bijection.

Next verify that $\nu$ is its own inverse: $7\cdot 7 = 49 \equiv 1 \pmod{12}$, so $\nu(\nu(p)) = 7(7p) = 49p \equiv p$. $\blacksquare$

</Box>

This theorem says something quite plain: **the circle of fifths returns to its starting point after exactly 12 steps, and never closes early**. Table 1 of Experiment 9.1 lists the tonics of the 12 positions:

$$
0,\ 7,\ 2,\ 9,\ 4,\ 11,\ 6,\ 1,\ 8,\ 3,\ 10,\ 5 ,
$$

After deduplication these are exactly all 12 pitch classes. This sequence is the circle of fifths: C → G → D → A → E → B → F♯ → D♭ → A♭ → E♭ → B♭ → F → C.

So why a circle and not a line? Because **pitch-class space is itself a circle**: in Chapter 2 the frequency axis was folded by octaves, $\mathbb{R}_{>0}/2^{\mathbb{Z}}$ is isomorphic to $S^1$, and the 12 pitch classes are 12 equally spaced points on that circle. The circle of fifths is not another line; it is the same circle under a different parameterization, with the step changed from a semitone to a fifth. Adding a fifth means rotating $7/12$ of a turn around the circle; because $7$ and $12$ are coprime, this rotation visits all 12 points before returning to the start.

Note that the "circle" closes on pitch classes, not on frequencies. The note to Table 1 gives the accounting: 12 fifths are $8423.46\ \text{¢}$, 7 octaves are $8400\ \text{¢}$, a difference of $23.46\ \text{¢}$. So the real chain of fifths is a **spiral** (each turn rises by one Pythagorean comma), and only after the octave is treated as an equivalence relation and folded does it project to a circle. The spiral of Chapter 2 and the circle here are two photographs of the same object.

<Figure src="/figures/circle-of-fifths.svg" caption="The circle of fifths: the outer ring is note names, the inner ring is pitch-class numbers (C = 0). Each step is +7 semitones; because gcd(7, 12) = 1, the rotation visits all 12 pitch classes before returning to the start." />

<Box kind="pitfall" title="Common misconception: the circle of fifths is “natural”">

The circle of fifths has 12 points because we chose 12-TET. Switch to 19-TET or 31-TET and the circle becomes a circle of 19 or 31 points, and the step is no longer 7 (it becomes a non-integer such as $19\times\log_2(1.5)\approx 11.1$). The number 12 is a historical and engineering choice, not a mathematical necessity. Theorem 9.1 holds for any $n$-TET, provided 7 is replaced by "the number of steps closest to a perfect fifth" and that number is coprime to $n$ — coprimality is the condition that really matters.

</Box>

### 9.1.2 Dyad Space Is a Torus

A dyad can be written with two coordinates: the root $r$ and the interval $q$.

<Box kind="definition" title="Definition 9.2 (dyad space)">

Write an ordered dyad as $(r,q)\in\mathbb{Z}_{12}\times\mathbb{Z}_{12}$, where $r$ is the root pitch class and $q$ is the interval from the root to the other note (in semitones, signed). This $12\times12$ discrete set is called **dyad space**. Its two basic operations are
$$
T_n:(r,q)\mapsto(r+n,\ q),
\qquad
I:(r,q)\mapsto(-r,\ -q).
$$
$T_n$ is a rotation along the root direction; $I$ is the reflection that negates both coordinates, sending interval $q$ to $-q$.

</Box>

Both coordinates of $(r,q)$ are angles mod 12, so this space is a **torus** $\mathbb{Z}_{12}\times\mathbb{Z}_{12}$: 12 steps horizontally return to the start, and 12 steps vertically do too. $T_n$ is a translation on the torus, $I$ a reflection on it. The transposition and inversion of Chapter 6 now have a geometric identity.

Now count the equivalence classes. Of the 144 ordered chords, how many classes remain if we regard "transposition does not change the essence of a chord" (that is, quotient out $T$)? $T$ moves only $r$, not $q$, so each class is determined by $q$: 12 classes. If we further regard "inversion does not change the essence" (quotient out $I$), $q$ and $-q$ are merged, and the 12 intervals collapse to just 7 classes: $0,1,\ldots,6$.

<Box kind="theorem" title="Theorem 9.2 (counting equivalence classes of dyads)">

Under $T$, the 144 ordered dyads fall into 12 equivalence classes (12 each); under $T$ and $I$ together, they fall into 7 classes, corresponding to the interval classes $0,1,\ldots,6$.

</Box>

<Box kind="proof" title="Proof">

$T$ acts freely and transitively on $r$: fix $q$, and the 12 roots are all reachable from one another, forming a single orbit. $q$ has 12 values, so $T$ has 12 orbits.

$I$ sends $q$ to $-q$, so orbits are determined by $\{q,-q\}$. $q=0$ and $q=6$ are each paired with themselves ($-0=0$, $-6\equiv 6$); the remaining 10 intervals pair into 5 groups, for $1+1+5=7$ classes. Within each class $T$ can still move the root freely, so the class representatives are the interval classes. $\blacksquare$

</Box>

Table 2 of Experiment 9.1 computes these numbers: 144 ordered chords, 78 unordered sets (66 distinct pairs plus 12 unison pairs), 12 $T$ classes, 7 $T/I$ classes. The number of unordered sets per interval class is also listed: 12 for every class except the tritone, which has 6.

There is a distinction that is easy to skip: **discrete counts and continuous shapes are not the same thing**. On a finite set, quotienting out $T$ and $I$ leaves only 7 points, and there is no "strip" to speak of. The Möbius strip appears only after $\mathbb{Z}_{12}$ is made continuous as $S^1$ and the discrete points on the torus are made continuous as a continuous torus: the space of unordered dyads is the torus with a diagonal gluing, and "gluing along the diagonal" is exactly taking a rectangular strip, flipping one end, and joining it — that is a Möbius strip. The output of Experiment 9.1 says this below Table 2, because it is a **conclusion of the continuous model**, not something integer counting can produce.

### 9.1.3 The Möbius Strip and the Klein Bottle: Which Are Theorems, Which Are Metaphors

First let us list what can be stated rigorously:

- **Circle of fifths $\cong S^1$**: this is an isomorphism; the discrete circle of 12 points is isomorphic to the set of 12 equally spaced points on $S^1$. Rigorous.
- **Dyad space $\cong T^2$**: $\mathbb{Z}_{12}\times\mathbb{Z}_{12}$ is a discrete torus. Rigorous.
- **Unordered dyads $\cong$ Möbius strip**: this is a conclusion about the quotient space after continuization; it is a standard picture in Tymoczko's geometric music theory. It has conditions (continuization, quotienting out the order), but under those conditions it holds.
- **"Chord space is a Klein bottle"**: this sentence needs great care. A Klein bottle requires "flip-gluing" in one direction, and what equivalence relation that flip corresponds to in music is often unclear. In most writing the Klein bottle is just rhetoric about "more twisting", not a proven model.

The root of the problem is that **topological properties are properties of a quotient space, and what you quotient out is a modeling choice.** Quotient out order and you get a strip; quotient out octaves and you get a circle; quotient out inversion as well and you get half a strip. None of these steps is discovered by music; each is decided by you. Treating "Möbius" as an intrinsic property of music amounts to presenting "I chose to regard these things as equivalent" as "the world is really like this".

There is a more fundamental limitation: the real musical space is **discrete**. There are only 12 pitch classes, finitely many chords, 24 keys. The value of a continuous model is that it gives you a map you can draw and walk on; its danger is that it makes you forget those points are actually integers. The tonal graph later in this chapter is an honest discrete graph — 24 nodes, 108 edges, not one of them continuous.

<Box kind="pitfall" title="Common misconception: the more obscure the topological metaphor, the deeper the theory">

"Klein bottle", "Möbius strip", "higher-dimensional torus" appear often in popular science, but they usually carry little information. To judge whether a sentence deserves belief, ask three things: (1) Which equivalence relations were quotiented out? (2) How was the discrete set made continuous? (3) What testable prediction does the conclusion yield? A metaphor that cannot answer these three questions can serve as an intuition pump, but not as an argument.

</Box>

## 9.2 Path Planning for Modulation

### 9.2.1 The Tonal Graph: 24 Nodes

Modulation is the most common kind of "movement" in music: from C major to G major, from C major to A minor, and so on. To talk about "how far", we first need a coordinate for each of the 24 major and minor keys.

<Box kind="definition" title="Definition 9.3 (tonal graph)">

Each key is represented by "key-signature position $n\in\mathbb{Z}_{12}$ + mode $M$ or $m$": the major tonic at position $n$ is $7n\bmod 12$, and the minor tonic at position $n$ is $(7n+9)\bmod 12$ (a minor third below its relative major). Thus the 24 keys correspond to 24 nodes.

Two keys are joined by an edge if and only if their key-signature positions differ by $\lvert\Delta n\rvert\le 2$ (shortest distance mod 12); the edge weight is
$$
w = \lvert\Delta n\rvert + 3\cdot[\text{mode change}].
$$

</Box>

The $3$ in the edge weight is not arbitrary: it lets the weight be rewritten as a function of the **number of common tones**. For two keys at position difference $d\le 5$ with the same mode, the number of common tones is exactly $7-d$, so
$$
w = (7-\text{common tones}) + 3\cdot[\text{cross-mode}].
$$
In other words, the cost of one modulation = "how many notes must be replaced" + "whether the mode changes". Look at Table 3: C major and A minor share $7$ notes, at cost $3$ (same position, cross-mode); C major and C minor share $4$ notes, at cost $6=(7-4)+3$ (position difference 3, plus cross-mode). $d=6$ is the exception: two keys a tritone apart share 2 notes rather than 1, so the formula overcounts by 1.

That is, the edge weights of this graph encode two things at once: **notational closeness** (key-signature difference) and **perceptual closeness** (number of common tones). Table 3 of Experiment 9.1 lists the common-tone counts and shortest costs for all 24 keys; the two curves move largely in step.

<Box kind="theorem" title="Theorem 9.3 (the tonal graph is connected)">

The 24-node graph constructed by Definition 9.3 is connected.

</Box>

<Box kind="proof" title="Proof">

Two keys of the same mode at adjacent positions ($\lvert\Delta n\rvert=1$) have an edge, so the 12 major keys form a cycle along the position circle, and likewise the 12 minor keys. The major and minor keys at the same position have the same key-signature position ($\Delta n=0$), edge weight $3$, so they are also joined. Therefore, starting from any key, walk along the same-mode cycle to any position, cross the mode once, and you reach the other key at that position; the reverse works too. Hence any two keys are reachable. $\blacksquare$

</Box>

### 9.2.2 Dijkstra: The Shortest Modulation Path

To find shortest paths on a graph, use Dijkstra. It requires nonnegative edge weights — this graph satisfies that, since $\lvert\Delta n\rvert\ge 0$ and the penalty is $3$ or $0$.

<Box kind="algorithm" title="Algorithm 9.1 (Dijkstra for the shortest modulation path)">

```text
输入：邻接表 adj，起点 s
1.  dist[v] ← ∞，prev[v] ← 空，dist[s] ← 0
2.  把 (0, s) 压入优先队列
3.  当队列非空:
        (d, u) ← 弹出最小值
        若 d > dist[u]: 跳过
        对每条边 (u, v, w):
            nd ← d + w
            若 nd < dist[v]: dist[v] ← nd; prev[v] ← u; 压入 (nd, v)
4.  从 dst 沿 prev 回溯，得到路径
输出：dist 与路径
```
Complexity $O((V+E)\log V)$; here $V=24$, $E=108$, so it finishes instantly.

</Box>

Table 4 of Experiment 9.1 gives two paths, both worth reading:

**C major → F♯ minor, total cost 6.** A direct edge is forbidden: the key-signature positions differ by 3, beyond the limit of at most 2 fifths per step. The route Dijkstra chooses is

$$
\text{C major}\ \xrightarrow{1}\ \text{G major}\ \xrightarrow{5}\ \text{F♯ minor},
$$

The first step is same-mode with position difference 1 (cost 1); the second crosses mode with position difference 2 (cost $2+3=5$). Common tones drop from 7 to 6 to 5, smoothly, with no cliff. This path makes auditory sense: first move to the dominant, then cross along the key-signature direction to F♯ minor (note that F♯ minor is not the relative minor of G; the relative minor of G is E minor).

**C major → B♭ minor, total cost 8.** The route is C → F → E♭ → B♭ minor, three steps, with common tones $6\to5\to5$. This goes half-way around in the flat direction: the sharp direction would require crossing more fifths, so it is actually better to go through F.

Note that "shortest" here means shortest **in this graph**, not the unique musical answer. Change the edge weights (say, make the mode penalty 2 or 4) and the paths change. The value of the model is not that it delivers truth, but that it turns "does this feel far?" into a number you can recompute.

<Box kind="pitfall" title="Common misconception: the shortest path is the “best modulation”">

Dijkstra only optimizes the cost function you give it. Real modulation also involves melodic position, harmonic preparation, bass motion, and performance difficulty, none of which are in the edge weights. Taking "shortest on the graph" for "most natural musically" mistakes the model for reality. The graph in this chapter is only a coarse skeleton; its use is to show you which keys lie close together, not to make arranging decisions for you.

</Box>

### 9.2.3 The Diameter of the Graph and What the Cost Means

Table 5 of Experiment 9.1 gives statistics for the whole graph: 24 nodes, 108 undirected edges, connected, **diameter 9.0** (C major → D♯ minor), average shortest path $4.6957$.

A diameter of 9.0 means that even the two hardest keys to connect are 9 cost units apart. Starting from C major, the most distant key is D♯ minor (position 6, 6 sharps), with cost exactly a combination of $3+3+3$ — cross the mode first, then move step by step along edges of position difference 2, paying at every step.

The number 108 can be checked: position differences $d=1$ and $d=2$ each give 12 pairs of positions, each pair of positions has 2 modes, and there are 4 mode combinations, so $12\times4 + 12\times4 = 96$ edges; adding the 12 same-position, different-mode edges (parallel major and minor) gives $108$. This count shows the graph is not sparse: each node is connected to 9 edges on average.

<Box kind="note" title="How to read Table 5 correctly">

"Average shortest path $4.6957$" averages the $24\times23$ directed distances. It has no musical meaning; it is just a graph-theoretic statistic showing that the graph has a small radius. The real information is in the **distribution** — many keys at cost 1 or 2 (nearby keys), few at cost 8 or 9 (remote keys). The last column of Table 3 is that distribution; reading it is more useful than looking at the mean.

</Box>

## 9.3 Atonal Music: A Random Walk That Breaks the Gravitational Field

### 9.3.1 Two Kinds of Walk

The previous two sections were static: where the space is, how large the distances are. This section sets a point moving in the space. The smallest model of motion is a random walk.

<Box kind="definition" title="Definition 9.4 (random walk on pitch classes)">

Let $X_t\in\mathbb{Z}_{12}$ be the pitch class at step $t$. The **atonal walk** has transition probabilities $P_{xy}=p(X_{t+1}=y\mid X_t=x)$ that depend only on $y-x$, with step sizes uniform on $\{\pm1,\ldots,\pm5\}$, each $0.1$. Its **stationary distribution** $\pi$ satisfies $\pi P=\pi$ and $\sum_i\pi_i=1$; define the circular centroid
$$
R=\Bigl\lvert\sum_{k=0}^{11}\pi_k\,e^{2\pi \mathrm{i} k/12}\Bigr\rvert,
$$
which measures "whether the distribution has a direction" (Chapter 7 used the same quantity).

</Box>

The second walk is "tonal": it moves only by steps of $\pm1$ and $\pm2$, and every step carries a gravity well centered on C,
$$
P_{xy}\ \propto\ \exp\!\Bigl(-\frac{d(y,0)}{T}\Bigr),\qquad y\in\{x\pm1,x\pm2\},
$$
where $d(y,0)=\min(y,12-y)$ is the semitone distance to the tonic C, and $T=1.5$ is the temperature. The farther from C, the lower the probability of being chosen — this is the minimal model of "tonal gravity".

### 9.3.2 The Stationary Distribution of Atonality Is Uniform

<Box kind="theorem" title="Theorem 9.4 (the stationary distribution of a translation-invariant walk is uniform)">

Suppose the transition probabilities depend only on the step, $P_{xy}=g(y-x)$, with $g(s)=g(-s)$, and the support of $g$ generates all of $\mathbb{Z}_{12}$. Then $P$ is doubly stochastic, the stationary distribution is uniform, $\pi_k=1/12$, and it is the unique stationary distribution.

</Box>

<Box kind="proof" title="Proof">

Row sums equal 1 by definition. Column sums: fix $y$; then $\sum_x P_{xy}=\sum_x g(y-x)=\sum_s g(s)=1$ (substitute $s=y-x$; as $x$ runs over $\mathbb{Z}_{12}$, so does $s$). Thus $P$ is doubly stochastic, and the all-ones vector (the uniform distribution) satisfies $\pi P=\pi$.

Uniqueness: the support $\{\pm1,\ldots,\pm5\}$ generates $\mathbb{Z}_{12}$, so the chain is irreducible; and since $g(1)>0$ and $g$ is symmetric, the chain is aperiodic. By the Perron–Frobenius theorem from Chapter 6, an irreducible aperiodic finite chain has a unique stationary distribution.

Hence $\pi_k=1/12$, $R=\lvert\frac{1}{12}\sum_k e^{2\pi \mathrm{i}k/12}\rvert=0$, and the entropy is $\log_2 12$. $\blacksquare$

</Box>

This proof is only three lines, but it answers a question that sounds mystical: **why is atonality "without direction"?** Because its stationary distribution is uniform: every pitch class is visited with the same probability, the circular centroid is $R=0$, the distribution is rotationally symmetric, and no note is "home". It is not "no pitches", but "no pitch is favored".

Table 6 of Experiment 9.1 gives numerical verification: after 10000 steps of the atonal walk, the stationary entropy is $3.5850$ bit (exactly $\log_2 12$), the simulated entropy is $3.5842$, the circular centroid is $R=0.0046$ (numerically zero), and the visit rate of the tonic C is $0.0881$ (theoretical value $1/12=0.0833$).

### 9.3.3 The Quantitative Meaning of “No Direction”

Putting the two walks side by side, the difference is obvious:

| Model | Stationary entropy (bit) | Circular centroid $R$ | $P(C)$ | Mean row entropy (bit) | Row-entropy range |
| --- | --- | --- | --- | --- | --- |
| Atonal | 3.5850 | 0.0046 | 0.0881 | 3.3219 | 3.322–3.322 |
| Tonal | 2.5211 | 0.7650 | 0.3266 | 1.6948 | 1.451–1.924 |

Three numbers deserve elaboration:

- **Stationary entropy**: for atonality it is $3.5850=\log_2 12$, spreading the 12 pitch classes as flat as possible; tonality is only $2.5211$, $1.06$ bit less. The missing part is the information content of "tonality" — knowing where the tonic is removes some uncertainty.
- **Circular centroid $R$**: atonality $0.0046$, tonality $0.7650$ (analytic value $0.7701$). $R$ near 1 means the distribution is concentrated on one side of the circle (has direction); near 0 means rotational symmetry (no direction).
- **Tonic visit rate**: atonality $0.0881$ (about $1/12$), tonality $0.3266$. The latter is $3.9$ times the former: the tonal walk spends nearly a third of its time on C.

What is most telling is the **row entropy**. Every row of the atonal walk looks the same: from any pitch class, the next step has 10 equally likely candidates, and the row entropy is always $\log_2 10=3.3219$ bit. **Position provides no information** — whether you are on C or on F♯, the prediction of the next step is exactly the same. The tonal walk is the opposite: row entropy varies between $1.451$ and $1.924$ bit; rows near C are more certain, rows far from C are freer. Position itself carries information, and that is the mathematical definition of a "gravitational field".

<Box kind="pitfall" title="Common misconception: atonality = no structure">

"Atonality" in this chapter is only a model of **pitch-class distribution**: a uniform stationary distribution with no preferred center. Real free atonal music certainly has structure — intervallic cells, rhythmic motives, registral layout, timbral change — none of which is in this chapter's model. To sum up an entire work with "no direction" respects neither the work nor the model: the model speaks about one dimension only; do not let it speak for the others.

</Box>

<Box kind="experiment" title="Experiment 9.1: the circle of fifths, the tonal graph, and random walks">

```bash
python code/ch09_topology.py
```

Real output (standard library only; fixed seed 9):

The script prints its labels in Chinese; the numbers are unchanged.

::: details Expand the full script output (125 lines, unmodified)

```text:no-line-numbers
ch09_topology.py —— 第 9 章配套实验：拓扑、转调与随机游走

表 1：五度圈的 12 个位置（位置 n 的大调主音 pc = 7n mod 12）

 位置 n   主音 pc  调名    调号       
----------------------------------------
      0         0  C       0 个升号   
      1         7  G       1 个升号   
      2         2  D       2 个升号   
      3         9  A       3 个升号   
      4         4  E       4 个升号   
      5        11  B       5 个升号   
      6         6  F♯      6 个升号   
      7         1  D♭      5 个降号   
      8         8  A♭      4 个降号   
      9         3  E♭      3 个降号   
     10        10  B♭      2 个降号   
     11         5  F       1 个降号   

  12 个位置的主音序列 = [0, 7, 2, 9, 4, 11, 6, 1, 8, 3, 10, 5]
  去重后 12 个：恰好覆盖 Z_12 的全部音级。
  因为 gcd(7,12) = 1，映射 n ↦ 7n 是 Z_12 上的置换，
  所以五度圈走 12 步就回到原点，不会提前闭合。
  12 个五度 = 8423.46 ¢，7 个八度 = 8400 ¢，差 23.46 ¢（第 4 章的毕达哥拉斯音差）。

表 2：二音和弦空间 —— 音程类、无序集合数与有序和弦数

音程类 d            音程名    无序集合数    有序和弦数
------------------------------------------------------
       0            纯一度            12            12
       1   小二度 / 大七度            12            24
       2   大二度 / 小七度            12            24
       3   小三度 / 大六度            12            24
       4   大三度 / 小六度            12            24
       5   纯四度 / 纯五度            12            24
       6            三全音             6            12

  无序二音集合共 78 个（= C(12,2) + 12 个同度对 = 66 + 12）。
  有序二音和弦共 144 个（= 12 × 12，含 (x,x) 的 12 个）。
  把顺序商掉（无序），144 个有序和弦折成 78 个集合；
  再把倒置 q ↦ −q 商掉，音程类只剩 0..6 这 7 类。
  连续化之后，无序二音对的空间是环面沿对角线粘合的结果 —— 一张莫比乌斯带；
  但离散计数只告诉你 7 个类，带子的「扭转」属于连续模型，不属于整数。

表 3：24 个大小调 —— 调号位置、与 C 大调的共同音数、最短转调代价

调             位置  调号          共同音数  到 C 大调代价
----------------------------------------------------------
C 大调            0  0 个升号             7              —
G 大调            1  1 个升号             6            1.0
D 大调            2  2 个升号             5            2.0
A 大调            3  3 个升号             4            3.0
E 大调            4  4 个升号             3            4.0
B 大调            5  5 个升号             2            5.0
F♯ 大调           6  6 个升号             2            6.0
D♭ 大调           7  5 个降号             2            5.0
A♭ 大调           8  4 个降号             3            4.0
E♭ 大调           9  3 个降号             4            3.0
B♭ 大调          10  2 个降号             5            2.0
F 大调           11  1 个降号             6            1.0
A 小调            0  0 个升号             7            3.0
E 小调            1  1 个升号             6            4.0
B 小调            2  2 个升号             5            5.0
F♯ 小调           3  3 个升号             4            6.0
C♯ 小调           4  4 个升号             3            7.0
G♯ 小调           5  5 个升号             2            8.0
D♯ 小调           6  6 个升号             2            9.0
B♭ 小调           7  5 个降号             2            8.0
F 小调            8  4 个降号             3            7.0
C 小调            9  3 个降号             4            6.0
G 小调           10  2 个降号             5            5.0
D 小调           11  1 个降号             6            4.0

  从 C 大调出发，其余 23 个调的平均最短代价 = 4.6957；
  最远的调是 D♯ 小调（位置 6），代价 9.0。

表 4：两条最短转调路径

  C 大调 → F♯ 小调：最短代价 6.0（直连代价 不可一步到达）
    C 大调 → G 大调   调号差 1 + 模式罚分 0 = 1   （共同音 6，累计 1）
    G 大调 → F♯ 小调   调号差 2 + 模式罚分 3 = 5   （共同音 5，累计 6）
  路径经过 3 个调，2 次转调。

  C 大调 → B♭ 小调：最短代价 8.0（直连代价 不可一步到达）
    C 大调 → F 大调   调号差 1 + 模式罚分 0 = 1   （共同音 6，累计 1）
    F 大调 → E♭ 大调   调号差 2 + 模式罚分 0 = 2   （共同音 5，累计 3）
    E♭ 大调 → B♭ 小调   调号差 2 + 模式罚分 3 = 5   （共同音 5，累计 8）
  路径经过 4 个调，3 次转调。

表 5：调性图的统计

  节点数（24 个大小调）     = 24
  无向边数                  = 108
  图是否连通                = 是
  直径（最长最短路径）      = 9.0（C 大调 → D♯ 小调）
  平均最短路（有向平均）    = 4.6957

  边权 = |调号位置差| + 3 × [模式不同]，且只保留 |Δn| ≤ 2 的边。
  邻接限制让绕路成为常态：直连往往更便宜，但一步最多跨两个五度。

表 6：无调性与有调性随机游走（各 10000 步，种子 9）

模型         平稳熵     模拟熵        R      P(C)    平均行熵      行熵范围
---------------------------------------------------------------------------
无调性       3.5850     3.5842   0.0046    0.0881      3.3219   3.322–3.322
有调性       2.5211     2.5372   0.7650    0.3266      1.6948   1.451–1.924

  无调性：步长在 ±1..±5 上均匀，每步一次；
  有调性：只走 ±1/±2，并带一个以 C 为中心、温度 T = 1.5 的重力井。

  无调性：平稳分布 π = 均匀（1/12 = 0.0833），熵 = log2 12 = 3.5850 bit；
  每个状态的行熵都等于 log2 10 = 3.3219 bit，与位置无关。
  有调性的 π（按音级 0..11） =
    0.327  0.207  0.095  0.025  0.007  0.002
    0.001  0.002  0.007  0.025  0.095  0.207
  圆重心 R（解析值）= 0.7701，方向指向 C：分布不再旋转对称。
  模拟 10000 步的圆重心：无调性 0.0046，有调性 0.7650。
  R 是「有没有中心」的度量：无调性 R ≈ 0，有调性 R > 0。

关键数字：
  12 个五度 = 7 个八度 + 23.46 ¢（毕达哥拉斯音差）
  24 个大小调、108 条无向边、图的直径 9.0
  无调性平稳熵 = log2 12 = 3.5850 bit，圆重心 R ≈ 0
  有调性平稳熵 = 2.5211 bit，圆重心 R = 0.7701
  种子 = 9，模拟步数 = 10000
```

:::

</Box>

## 9.4 Summary

This chapter divides "space" into three layers:

$$
\underbrace{\mathbb{Z}_{12}\cong S^1}_{\text{circle of fifths}}
\;\longrightarrow\;
\underbrace{\mathbb{Z}_{12}\times\mathbb{Z}_{12}\cong T^2}_{\text{dyads}}
\;\longrightarrow\;
\underbrace{G=(V,E,w),\ \lvert V\rvert=24}_{\text{tonal graph}}
$$

Main conclusions:

- **The circle of fifths is a circle, and an involution.** $\nu(p)=7p$ is a bijection on $\mathbb{Z}_{12}$ with $\nu^{-1}=\nu$ (because $7^2\equiv1$); 12 fifths traverse every pitch class and return to C. This "circle" is a product of octave equivalence: the real chain of fifths is a spiral, and 12 fifths exceed 7 octaves by $23.46\ \text{¢}$.
- **Dyad space is a torus; after quotienting out order it is a Möbius strip.** The 144 ordered chords have 12 classes under $T$ and 7 under $T/I$; the "strip" belongs to the quotient space after continuization, not to the integer 144.
- **The tonal graph makes "how far a modulation is" computable.** 24 nodes, 108 edges, edge weight $=\lvert\Delta n\rvert+3[\text{mode change}]$, diameter $9.0$, average shortest path $4.6957$. The shortest path C → F♯ minor is C → G → F♯ minor, cost $1+5=6$; C → B♭ minor is C → F → E♭ → B♭ minor, cost $8$.
- **The stationary distribution of atonality is uniform.** A translation-invariant walk satisfies $\pi_k=1/12$, circular centroid $R=0$, and row entropy constant at $\log_2 10$; the tonal gravity well pushes entropy down to $2.5211$ bit, raises $R$ to $0.7650$, and raises $P(C)$ to $0.3266$. "No direction" is computable, not an adjective.

Failure boundaries: the tonal graph in this chapter simplifies "modulation cost" into key-signature difference plus a fixed penalty, ignoring harmonic preparation, melodic position, and performance difficulty; the random walk models only pitch-class distribution, ignoring rhythm, register, and harmony; the topological metaphors hold only under the conventions of continuization and quotient spaces, and outside those conventions they are rhetoric.

Back to the five questions at the opening: the circle of fifths is a circle because pitch-class space is itself a circle and the fifth is only another step size; chord space is a torus, which becomes a Möbius strip in the continuous model after quotienting out order, but "Klein bottle" is mostly metaphor; C major to F♯ minor takes at least two modulations (cost 6); atonality is "without direction" because its stationary distribution is uniform and row entropy is independent of position; the first three are rigorous, and the Klein bottle must be discounted.

<Box kind="checkpoint" title="Self-check">

Close the book and answer three things: (1) Why do exactly $12$ fifths traverse all $12$ pitch classes, while $7$ octaves fail to return to the same frequency? (2) How many classes remain from the 144 ordered dyads under $T$ and under $T/I$, and which coordinate is quotiented out in each case? (3) Why is the row entropy of the atonal walk always $\log_2 10$, while the row entropy of the tonal walk varies with position?

</Box>

<Box kind="exercise" title="Exercises">

1. Compute $\nu(p)=7p$ by hand for $p=0,1,2,3$ and verify $\nu(\nu(p))=p$; then explain why for $n=12$ the integer step closest to a perfect fifth is $7$ (hint: $7/12\approx0.583$, closest to $\log_2 1.5\approx0.585$).
2. Prove: under $T$, each equivalence class contains exactly 12 ordered dyads; under $T/I$, it contains 12 or 24. Which classes contain 12?
3. Use the data in Table 3 to verify "two major keys of the same mode at position difference $d$ share about $7-d$ notes", find the counterexample at $d=6$, and explain it (hint: the tritone is its own inverse).
4. Change the mode penalty from 3 to 2 and re-derive the shortest path and total cost from C → F♯ minor; does the path still hold? (No need to run the program; compute by hand from the edge weights in Table 3.)
5. (Open) If the random walk is constrained to return to the tonic once per bar, what shape does the stationary distribution take? Which musical concept does this constraint correspond to?

</Box>



::: tip Review of the Whole Book
Ten chapters done: vibration → pitch → consonance → tuning → scales → harmony → rhythm → melody → tonality. Appendix A turns the mathematical tools used throughout the book into a quick-reference sheet, Appendix B gives the code environment and the script list, and Appendix C is the glossary and notation reference. [Appendix A](/en/appendix/a-math) · [Appendix B](/en/appendix/b-code) · [Appendix C](/en/appendix/c-glossary)
:::
