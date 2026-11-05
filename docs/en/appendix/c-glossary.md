---
title: "Appendix C · Glossary and Notation"
description: "77 terms and one symbol quick-reference table: the book's jargon translated into plain language."
---

# Appendix C · Glossary and Notation

<div class="chapter-meta">
  <span>Estimated 20 minutes</span>
  <span>Prerequisite: Chapters 0–9 read</span>
  <span>Use: look up terms, align symbols</span>
</div>

By this point you have met a large number of terms: pitch class, critical band, indicator vector, Euclidean rhythm, stationary distribution, circular centroid... They come from acoustics, number theory, linear algebra, probability and topology, and the same word often means different things in different disciplines. This page does three things:

1. Collect the **symbols** used throughout the book into a single table, so that you do not confuse $p$ (pitch) with $P$ (transition matrix);
2. Give the **77 terms** with their English and Chinese forms, symbols, and the chapter where each first appears;
3. Untangle the **10 most easily confused pairs**, explaining how they differ and when they may be interchanged.

## C.1 How to Use This Table

First, a convention for "first appearance": it means the chapter in which the concept is first **formally defined or systematically discussed**, not necessarily the place where the word first occurs. For example, "beat frequency" is mentioned in the end-of-chapter preview of Chapter 2, but its real definition is in Section 3.1 of Chapter 3; the table records Chapter 3. The reason is simple: if you need to go back and relearn something, you should return to the page where someone actually explains it.

Symbols are read according to three rules:

- **Italic Latin letters denote variables**; upright letters denote function names or units, e.g. $f$ is frequency, $\mathrm{CB}$ is a function, and $\text{Hz}$ is a unit;
- **Subscripts denote attachment**: $f_1$ is the frequency of the first tone, $T_n$ is translation by $n$ semitones, $P_{xy}$ is the transition probability from $x$ to $y$;
- **The same letter may change jobs between chapters.** $p$ is a pitch coordinate in Chapter 2 and a probability $p_i$ in the accent distribution of Chapter 7; $P$ is a transition matrix in Chapters 6 and 8, and may denote a pitch-class set around Chapter 5. When in doubt, read the subscripts and the context, not just the letter.

<Box kind="note" title="Three Kinds of Sentences, Three Ways to Read Them">

Three kinds of sentences are mixed together in the body, and they are read quite differently:

- A **definition** only names something and prescribes a construction; it has no truth value, only "does it work well". When you see "call ... a ...", a definition is being made.
- A **postulate** is input borrowed from experiment; this book does not prove it. When you see "Basis: ..." or "Limits: ...", remember that it is the foundation of the model, not a conclusion.
- A **theorem** is a proposition derived inside the definitions and postulates. It guarantees "if the model is right, then the conclusion is right"; it does not guarantee that the model itself is right.

The glossary gives only meanings, not these identities. To check whether a word is a definition or a theorem, go back to the Box title in the body.

</Box>

## C.2 Symbol Quick Reference

| Symbol | Read as | Meaning | Unit / range | First appearance |
| --- | --- | --- | --- | --- |
| $p$ | pitch coordinate | logarithmic pitch relative to a reference frequency | ¢, $p=1200\log_2(f/f_0)$ | Ch. 0 |
| $f$ | frequency | cycles per unit time | Hz | Ch. 0 |
| $T$ | period | time for one complete waveform | s, $T=1/f$ | Ch. 1 |
| $F$ | fundamental frequency | common spacing of the harmonic series | Hz | Ch. 1 |
| $f_i$ | $i$-th harmonic | $f_i=iF$ | Hz | Ch. 1 |
| $f_{\text{beat}}$ | beat frequency | frequency difference of two tones | Hz, $\lvert f_1-f_2\rvert$ | Ch. 3 |
| $\mathrm{CB}(f)$ | critical bandwidth | equivalent width of an auditory filter | Hz | Ch. 3 |
| $D$ | dissonance | sum of roughness over all harmonic pairs | dimensionless, $\ge 0$ | Ch. 3 |
| $S$ | consonance | $S=1/(1+D)$ | $(0,1]$ | Ch. 3 |
| $\Delta p$ | interval | difference of two pitch coordinates | ¢ | Ch. 0 |
| $p\in\mathbb{Z}_{12}$ | pitch class | pitch class modulo 12 | $0,\ldots,11$ | Ch. 0 |
| $\nu(p)$ | fifth coordinate | $\nu(p)=7p \bmod 12$ | $\mathbb{Z}_{12}$ | Ch. 9 |
| $\mathbf{v}(S)$ | indicator vector | 0–1 encoding of the set $S$ | $\mathbb{R}^{12}$ | Ch. 6 |
| $T_n$ | transposition | add $n$ to every pitch class | mod 12 | Ch. 6 |
| $I$ | inversion | reflect pitch classes about 0 | mod 12 | Ch. 6 |
| $D_{12}$ | dihedral group | 12 rotations plus 12 reflections | 24 elements | Ch. 6 |
| $M$ | consonance matrix | $M_{pq}=S(p,q)$ | $12\times12$ | Ch. 6 |
| $E(k,n)$ | Euclidean rhythm | $k$ onsets in $n$ slots | $0\le k\le n$ | Ch. 7 |
| $h(i)$ | metric weight | strong–weak level of position $i$ | $(0,1]$ | Ch. 7 |
| $\operatorname{sync}(S)$ | syncopation | mean weakness of the onsets | $[0,1)$ | Ch. 7 |
| $R$ | circular centroid | length of the resultant accent vector on the circle | $[0,1]$ | Ch. 7 |
| $X_t$ | state | pitch class or function at step $t$ | discrete state | Ch. 6 |
| $P$ | transition matrix | $P_{xy}=p(X_{t+1}=y\mid X_t=x)$ | rows sum to 1 | Ch. 6 |
| $\boldsymbol{\pi}$ | stationary distribution | distribution satisfying $\boldsymbol{\pi}P=\boldsymbol{\pi}$ | probability vector | Ch. 6 |
| $H$ | entropy | average information | bit | Ch. 8 |
| $H(Y\mid X)$ | conditional entropy | remaining uncertainty of $Y$ given $X$ | bit | Ch. 8 |
| $-\log_2 p$ | surprisal | information of an event with probability $p$ | bit | Ch. 8 |
| $\tau$ | temperature | sharpening / smoothing parameter of a sampling distribution | $>0$ | Ch. 8 |
| $G=(V,E,w)$ | tonal graph | 24 keys, weighted edges | 24 nodes / 108 edges | Ch. 9 |

This table lists only the 29 most common symbols; finer ones (e.g. $\sigma^2$, $v_2(i)$, $\operatorname{lcm}$) appear in the corresponding glossary entries.

## C.3 Glossary

The six groups are ordered "from sound to structure". The English term is the rendering this book adopts; it is not the only possible translation. A dash in the symbol column means the concept has no dedicated symbol in this book.

### C.3.1 Acoustics, Vibration, and Hearing

| English | Chinese | Symbol | First appearance |
| --- | --- | --- | --- |
| pitch | 音高 | $p$ | Ch. 0 |
| frequency | 频率 | $f$ | Ch. 0 |
| period | 周期 | $T$ | Ch. 1 |
| simple harmonic motion | 简谐振动 | $x(t)=A\cos(\omega t+\varphi)$ | Ch. 1 |
| fundamental frequency | 基频 | $F$ | Ch. 1 |
| harmonic / partial | 谐波 | $f_i=iF$ | Ch. 1 |
| spectrum | 频谱 | — | Ch. 1 |
| timbre | 音色 | — | Ch. 1 |
| beat frequency | 拍频 | $f_{\text{beat}}$ | Ch. 3 |
| roughness | 粗糙度 | $D$ | Ch. 3 |
| consonance | 协和度 | $S$ | Ch. 3 |
| critical band | 临界频带 | $\mathrm{CB}(f)$ | Ch. 3 |
| autocorrelation | 自相关 | $r(\tau)$ | Ch. 1 |
| noise | 噪声 | — | Ch. 1 |
| Weber–Fechner law | 韦伯–费希纳定律 | — | Ch. 2 |
| masking | 掩蔽 | — | Ch. 3 |

### C.3.2 Pitch, Intervals, and Tuning Systems

| English | Chinese | Symbol | First appearance |
| --- | --- | --- | --- |
| cent | cent | ¢ | Ch. 0 |
| interval | 音程 | $\Delta p$ | Ch. 0 |
| octave | 八度 | $2:1$ | Ch. 0 |
| semitone | 半音 | $100\ \text{¢}$ | Ch. 0 |
| pitch class | 音级 | $p\in\mathbb{Z}_{12}$ | Ch. 0 |
| quotient space | 商空间 | $\mathbb{R}/1200\mathbb{Z}\cong S^1$ | Ch. 2 |
| pitch helix | 螺旋音高模型 | $(p,\theta)$ | Ch. 2 |
| interval group | 音程群 | $(\mathbb{R}_{>0},\times)$ | Ch. 2 |
| complexity | 复杂度 | $p+q$ | Ch. 2 |
| Pythagorean tuning | 五度相生律 | $3:2$ chain | Ch. 4 |
| just intonation | 纯律 | 5-limit ratios | Ch. 4 |
| 12-TET | 十二平均律 | $2^{k/12}$ | Ch. 4 |
| comma | 音差 | $23.460\ \text{¢}$ | Ch. 4 |
| wolf fifth | 狼五度 | $678.495\ \text{¢}$ | Ch. 4 |
| continued fraction | 连分数 | $[a_0;a_1,\ldots]$ | Ch. 4 |
| microtone | 微分音 | — | Ch. 4 |
| scale | 音阶 | $S\subset[0,1200)$ | Ch. 5 |
| mode | 调式 | rotation equivalence class | Ch. 5 |
| pentatonic scale | 五声音阶 | 5-note set | Ch. 5 |
| triad | 三和弦 | 3-note set | Ch. 5 |

### C.3.3 Harmony and Transformations

| English | Chinese | Symbol | First appearance |
| --- | --- | --- | --- |
| pitch-class set | 音级集合 | $S\subset\mathbb{Z}_{12}$ | Ch. 6 |
| indicator vector | 指示向量 | $\mathbf{v}(S)$ | Ch. 6 |
| transposition | 移位 | $T_n$ | Ch. 6 |
| inversion | 倒置 | $I$ | Ch. 6 |
| dihedral group | 二面体群 | $D_{12}$ | Ch. 6 |
| permutation matrix | 置换矩阵 | $P_n$ | Ch. 6 |
| consonance matrix | 协和矩阵 | $M$ | Ch. 6 |
| quadratic form | 二次型 | $\mathbf{v}^{\mathsf{T}}M\mathbf{v}$ | Ch. 6 |
| tensor product | 张量积 | $\otimes$ | Ch. 6 |
| harmonic function | 和声功能 | $T,S,D$ | Ch. 6 |
| voice leading | 声部进行 | $\delta$ | Ch. 6 |
| Markov chain | 马尔可夫链 | $X_t$ | Ch. 6 |
| transition matrix | 转移矩阵 | $P$ | Ch. 6 |
| stationary distribution | 平稳分布 | $\boldsymbol{\pi}$ | Ch. 6 |
| potential | 势能 | $E(i)=-\log\pi_i$ | Ch. 6 |
| cadence | 终止式 | — | Ch. 6 |

### C.3.4 Rhythm and Time

| English | Chinese | Symbol | First appearance |
| --- | --- | --- | --- |
| Euclidean rhythm | 欧几里得节奏 | $E(k,n)$ | Ch. 7 |
| accent distribution | 重音分布 | $p_i$ | Ch. 7 |
| metric weight | 节拍权重 | $h(i)$ | Ch. 7 |
| syncopation | 切分度 | $\operatorname{sync}(S)$ | Ch. 7 |
| circular centroid | 圆重心 | $R$ | Ch. 7 |
| polyrhythm | 复合节奏 | $m:n$ | Ch. 7 |
| least common multiple | 最小公倍数 | $\operatorname{lcm}(m,n)$ | Ch. 7 |
| Klapp ring matrix | 克拉普环矩阵 | $K$ | Ch. 7 |

### C.3.5 Melody, Statistics, and Information

| English | Chinese | Symbol | First appearance |
| --- | --- | --- | --- |
| entropy | 熵 | $H$ | Ch. 8 |
| conditional entropy | 条件熵 | $H(Y\mid X)$ | Ch. 8 |
| redundancy | 冗余度 | $R=1-H_1/H_{\max}$ | Ch. 8 |
| surprisal | 惊讶度 | $-\log_2 p$ | Ch. 8 |
| Shannon guessing game | 香农猜谜 | rank $r$ | Ch. 8 |
| temperature | 温度 | $\tau$ | Ch. 8 |
| held-out test | 留出检验 | — | Ch. 8 |
| second-order context | 二阶上下文 | $(x_{t-2},x_{t-1})$ | Ch. 8 |
| maximum likelihood estimation | 最大似然估计 | MLE | Ch. 8 |

### C.3.6 Topology and Tonal Space

| English | Chinese | Symbol | First appearance |
| --- | --- | --- | --- |
| circle of fifths | 五度圈 | $\nu(p)=7p$ | Ch. 9 |
| torus | 环面 | $T^2=S^1\times S^1$; discrete grid $\mathbb{Z}_{12}\times\mathbb{Z}_{12}$ | Ch. 9 |
| tonal graph | 调性图 | $G=(V,E,w)$ | Ch. 9 |
| random walk | 随机游走 | $X_t$ | Ch. 9 |
| atonality | 无调性 | — | Ch. 9 |
| graph diameter | 图的直径 | $9.0$ | Ch. 9 |
| Möbius strip | 莫比乌斯带 | — | Ch. 9 |
| Klein bottle | 克莱因瓶 | — | Ch. 9 |

The six tables add up to **77 entries**. If you want to memorize only ten, take: pitch class, cent, critical band, consonance, indicator vector, quadratic form, Euclidean rhythm, entropy, stationary distribution, fifth coordinate — they are the load-bearing walls of the next eight chapters.

## C.4 Ten Most Confused Pairs

The glossary settles "what it is called" but not "how it differs from the word next to it". The ten pairs below are the confusions readers ask about most; each gets a one-line test.

**1. Pitch vs. pitch class.** Pitch is continuous ($p$ can take any real value); the 12-TET pitch class used in this book first folds by octave equivalence, then quantizes onto 12 slots. 440 Hz and 880 Hz differ in pitch but share a pitch class. Test: ask whether it survives transposition by an octave unchanged; if yes, it is a pitch class.

**2. Cent vs. Hz.** Cent is a ratio unit; Hz is a linear unit. Raising by 100 ¢ multiplies the frequency by $2^{1/12}$; raising by 100 Hz adds a fixed amount; the former corresponds to a larger Hz difference in the high register. Test: ask whether the two quantities can be added directly. Cents add; Hz cannot be added to cents.

**3. Frequency ratio vs. interval name.** The same interval name can map to different ratios: the tritone can be $45:32$ ($590.2$ ¢) or the 12-TET $600.0$ ¢; the minor seventh can be $16:9$ or $7:4$. Test: write the ratio in a paper, the name on a score; do not substitute one for the other.

**4. Consonance vs. simplicity.** "Simple" is a property of numbers ($p+q$ small, continued fraction short); "consonant" is a property of hearing (low roughness). The counterexample in Chapter 3 shows that the two do not always agree: $7:4$ is not simple, yet its roughness is lower than that of $6:5$. Test: ask whether the judgment needs ears; if yes, it is consonance.

**5. Roughness $D$ vs. consonance $S$.** The two are monotone transforms: $S=1/(1+D)$. $D$ can be compared across registers directly; $S$ is squeezed into $(0,1]$ and is better suited to scoring. Test: to rank, use $D$; to show a user a score, use $S$; do not treat differences in $S$ as a linear scale.

**6. Pythagorean tuning vs. just intonation vs. 12-TET.** Pythagorean tuning generates everything from $3:2$; the 5-limit just intonation of this book introduces extra ratios such as $5:4$; 12-TET divides the octave into 12 irrational ratios. Test: look at the prime factors of the ratios. Only 2 and 3 means the Pythagorean system; allowing a factor of 5 means the book's 5-limit just intonation; check whether every semitone has the same width — equal width means equal temperament.

**7. Scale vs. mode.** A scale is a set of notes; a mode is a reading of "which note is the tonic". The C major scale and the D Dorian mode have exactly the same pitch-class set; they differ only in tonic and functional relations. Test: ask whether it is still the same object when another note becomes the tonic; if yes, it is a modal rotation.

**8. Transposition $T_n$ vs. inversion $I$.** Transposition preserves the direction of intervals (a major second stays a major second); inversion flips direction (an ascending major third becomes a descending major third). Together they generate the 24-element dihedral group. Test: ask whether the chord's left and right hands have been swapped; if so, it is inversion.

**9. Entropy vs. surprisal.** Entropy is the average information of a distribution, $H=-\sum p_i\log_2 p_i$; surprisal is that of a single event, $-\log_2 p$. Entropy is an expectation, surprisal a sample value; one high-surprisal event does not imply high entropy, and high entropy does not require every event to be highly surprising. Test: ask whether it describes one event or a whole distribution; the former is surprisal, the latter entropy.

**10. Syncopation vs. circular centroid.** Syncopation measures how weak the grid positions of the onsets are on average; the circular centroid measures which side of the circle the accents lean toward. For $E(3,8)$, syncopation is $0.5417$ and the centroid length is $0.138$ with a late orientation; the former is a strength, the latter a direction. Test: ask whether you want a score or an arrow; a score is syncopation, an arrow is the circular centroid.

## C.5 Index by Chapter

| Chapter | Core concepts | Key symbols | In one sentence |
| --- | --- | --- | --- |
| [Chapter 0](/en/chapters/00-introduction) | postulates, cent coordinates, interval addition | $p$, $1200\log_2$ | Build the ruler first, then talk about music |
| [Chapter 1](/en/chapters/01-vibration) | simple harmonic motion, Fourier, period and noise | $T$, $f_i$, $r(\tau)$ | A musical tone is a periodic signal; noise is not |
| [Chapter 2](/en/chapters/02-pitch) | logarithmic perception, octave quotient space, interval group | $p$, $\mathbb{Z}_{12}$ | Pitch is a circle, and also a helix |
| [Chapter 3](/en/chapters/03-consonance) | beat frequency, critical band, roughness kernel | $\mathrm{CB}$, $D$, $S$ | Consonance can be computed as a function |
| [Chapter 4](/en/chapters/04-tuning) | fifth chain, just intonation, equal temperament, continued fractions | $23.460\ \text{¢}$ | Twelve fifths do not return to seven octaves |
| [Chapter 5](/en/chapters/05-scales) | scale search, modal rotation, pentatonic | 792 candidates | The major scale is the winner of an exhaustive search |
| [Chapter 6](/en/chapters/06-harmony) | indicator vectors, quadratic forms, function chains | $M$, $\boldsymbol{\pi}$ | A chord is a vector; a progression is a Markov chain |
| [Chapter 7](/en/chapters/07-rhythm) | Euclidean rhythms, syncopation, polyrhythm | $E(k,n)$, $R$ | Rhythm is division on the time axis |
| [Chapter 8](/en/chapters/08-melody) | transition matrices, entropy, surprisal, temperature | $H$, $\tau$ | Good melody is a balance between surprise and predictability |
| [Chapter 9](/en/chapters/09-topology) | circle of fifths, torus, tonal graph, random walk | $\nu(p)$, $G$ | Modulation is a shortest path on a graph |

This index is not a copy of the table of contents but a concept map: if you remember only a symbol and forget which chapter it belongs to, read from right to left.

## C.6 Self-Check

<Box kind="checkpoint" title="Ten Questions: Can You Really Tell These Words Apart?">

1. Convert $p=700$ ¢ and $p=1900$ ¢ into frequency ratios (relative to A4); how many octaves apart are they?
2. Why is "raise by 100 Hz" closer to a large interval in the low register than in the high register?
3. Why does the $D$ of a perfect octave show as 0 at the table's finite precision? Why can it not be called exactly 0?
4. The wolf fifth of Pythagorean tuning is $678.495$ ¢. How many cents short of a pure fifth is it? What is that difference called?
5. A major scale has the same pitch-class set as one of its modes. After changing the tonic, which quantities change and which do not?
6. How many 1s does the indicator vector of a three-note set have? Why does the quadratic form subtract $k$ and then divide by $k(k-1)$?
7. What are the three gaps of $E(3,8)$? Why can they take only two adjacent integers?
8. A piece has a melodic entropy of $2.6$ bit, and one note has a surprisal of $4$ bit. Do these two facts contradict each other?
9. Why is the theoretical stationary distribution of an atonal walk uniform? What is the theoretical circular centroid $R$? How does it differ from a finite simulation?
10. In the tonal-graph edge weight $\lvert\Delta n\rvert+3[\text{mode change}]$, is that 3 a theorem or a modeling choice?

The answers are not on this page — they are scattered through Chapters 0–9. If you can answer 8 of them, the terms have become your tools; if only 5, go back to the index in C.5 and fill in the gaps chapter by chapter.

</Box>

::: tip Next chapter
The glossary settles "what it is called"; the reading list settles "whom to read next". Appendix D gives 15 books and papers genuinely worth reading and says which question of this book each one can answer — [Appendix D · Further Reading](/en/appendix/d-reading).
:::
