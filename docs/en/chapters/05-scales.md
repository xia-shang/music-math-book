---
title: "Chapter 5 · Algorithms for Generating Scales"
description: "Enumerating the 792 seven-note subsets of the 12 pitch classes to see why the major scale wins."
---

# Chapter 5 · Algorithms for Generating Scales

<div class="chapter-meta">
  <span>Estimated 45 minutes</span>
  <span>Prerequisite: Chapters 3 and 4</span>
  <span>Code: code/ch05_scale_search.py</span>
</div>

This chapter answers the following questions:

1. Why exactly 7 notes in an octave? Why not 5, 6, or 12?
2. Is the major scale's semitone pattern `2-2-1-2-2-2-1` a cultural habit or a mathematical necessity?
3. Why must any 7 notes include a minor second, while a pentatonic scale can have none?
4. Try every 7-element subset of the 12 pitch classes: where does the major scale rank?
5. What exactly are the seven modes? Why does the same set of notes, starting from a different point, acquire a different "character"?

Chapter 4 accepted the 12-TET grid: an octave cut into 12 equally spaced pitch classes. Now switch to a purer combinatorial problem: **choose 7 of these 12 slots — how many ways are there, and which is best?** This chapter writes "best" as a computable objective function and then actually enumerates 792 possibilities. The conclusion is slightly counterintuitive: the major scale does not win on "highest consonance"; it wins on the balance of "consonance, evenness, and harmonic resources" — and on some individual measures it is not even first.

## 5.1 Scale as a Filter: From Continuous Frequency to Discrete Degrees

### 5.1.1 Quantization: Compressing Continuous Pitch into Finite Labels

Chapter 2 wrote pitch as a continuous coordinate $p = 1200\log_2(f/f_0)$. Real-world frequencies are continuous, but the piano keyboard is discrete: 88 keys, each corresponding to one pitch class. This "continuous → discrete" mapping is **quantization**.

Take 12-TET: number the pitch classes $\mathbb{Z}_{12} = \{0,1,\dots,11\}$, with C as $0$ and B as $11$. The quantization rule for an arbitrary frequency is

$$
q(p) = 100 \cdot \operatorname{round}\!\left(\frac{p}{100}\right) \pmod{1200},
$$

that is, snap it to the nearest whole-hundred-cent grid point. The cost of quantization is **error**: any note deviates from the grid by at most $50\ \text{¢}$. This number is not trivial — Chapter 4 computed that the just and 12-TET major thirds differ by $13.686\ \text{¢}$, less than a third of the half-grid error. In other words, **the grid itself already consumes a great deal of precision**; the scale's job is to pick out the slots "worth keeping" on top of this coarse grid.

<Box kind="definition" title="Definition 5.1 (scale and pitch-class set)">

A $k$-note **scale** is a $k$-element subset of $\mathbb{Z}_{12}$
$$
S = \{s_0,\ s_1,\ \dots,\ s_{k-1}\} \subset \mathbb{Z}_{12},
$$
where $s_0 \lt s_1 \lt \cdots \lt s_{k-1}$ is increasing order, $s_i$ is a pitch-class number, and $k$ is called the number of degrees of the scale. Arranging the elements in circular order, the number of semitones between adjacent degrees
$$
g_i = (s_{i+1} - s_i) \bmod 12,\qquad i = 0,\dots,k-1
$$
is called the **step pattern**, with the convention $s_k = s_0$. It is not the interval vector of pitch-class set theory, which counts how many intervals of each class occur. These $g_i$ are all positive integers, and
$$
\sum_{i=0}^{k-1} g_i = 12.
$$

</Box>

The word "scale" in everyday usage also carries connotations of tonality, performance, and history. This chapter takes only its mathematical skeleton: **a subset modulo 12, together with a cyclic step vector**. This abstraction is narrow enough to enumerate, yet wide enough to hold major, minor, pentatonic, blues, and whole-tone scales.

<Figure src="/figures/major-scale.svg" caption="The step structure of the major scale: 7 of the 12 slots, with adjacent spacings 2-2-1-2-2-2-1 (unit: semitones). The two '1's are the minor seconds E–F and B–C." />

<Box kind="definition" title="Definition 5.2 (degrees, tonic, and adjacent intervals)">

Let $S$ be a scale. Call $s_i$ the $i$-th **degree**. If some degree $s_r$ is chosen as the **tonic**, the interval of the $i$-th degree relative to the tonic is
$$
\delta_i = (s_{(r+i) \bmod k} - s_r) \bmod 12 \quad (\text{unit: semitones}),
$$
and the interval between adjacent degrees, $100\,g_i\ \text{¢}$, is called a **step**. The smallest $g_i$ determines where the scale is "densest," and the largest determines where it is "emptiest."

</Box>

### 5.1.2 A Scale Is a Lossy Compression

Think of a scale as a filter: the input is continuous frequency, the output is one of $k$ discrete labels. Two layers of operation must be distinguished first: the earlier $q(p)$ quantizes to 12-TET with a fixed maximum error of 50 ¢; then choosing the nearest label among the scale's $k$ notes has a maximum error determined by the scale's largest gap, $50\max_i g_i$ ¢. Therefore, **reducing the number of degrees does not automatically improve precision**; it reduces the number of labels, and usually makes the quantization grain coarser.

This is the same thing as "prediction-compression" in Chapter 0: **a scale can be seen as a codebook for organizing melodic labels**. The codebook size $k$ is inversely proportional to the average spacing $12/k$ semitones. Using all 12 pitch classes (chromatic) gives the finest codebook; using only 5 gives fewer labels and a larger average spacing. The major scale takes $k=7$, an intermediate value — and why intermediate is good is exactly what Section 5.2 computes.

First, a purely combinatorial fact that explains the phenomenon "7 notes necessarily include a minor second."

<Box kind="theorem" title="Theorem 5.1 (seven notes must contain a minor second)">

Let $S \subset \mathbb{Z}_{12}$ with $\lvert S \rvert = 7$. Then $S$ must contain two pitch classes one semitone apart (i.e. the step pattern must contain $g_i = 1$).

</Box>

<Box kind="proof" title="Proof">

Suppose all spacings are $\ge 2$. Then the sum of the seven spacings is at least $7 \times 2 = 14$, but by Definition 5.1 the sum of the spacings is always $12$. Contradiction. Hence at least one $g_i = 1$, i.e. there exist two adjacent degrees differing by exactly one semitone. $\blacksquare$

</Box>

This proof uses only "the sum of seven positive integers is 12." It also gives a boundary: for a $k$-note set to avoid a minor second, we need $2k \le 12$, i.e. $k \le 6$. At $k=6$ there is still room (e.g. the whole-tone scale $\{0,2,4,6,8,10\}$); at $k=7$ there is none. So "a seven-note scale must contain a minor second" is not a cultural choice but the pigeonhole principle.

<Box kind="pitfall" title="Common misconception: the minor second is a 'defect of the scale'">

The minor second is not only a roughness cost; it can also be a **functional resource**. B–C in major provides the semitone tendency of leading tone to tonic, while E–F shapes the interval relations of the subdominant region; but a semitone by itself does not automatically guarantee tonal clarity — rhythm, melody, and harmonic context also matter. A pentatonic scale has no semitone adjacency, yet it can still establish a tonic through repetition, rests, and the tonic chord; it cannot simply be dismissed as "floaty."

</Box>

### 5.1.3 Writing "Good Scale" as a Score

Now we need an objective function. Chapter 3 already has the consonance score $S(f_1,f_2) \in (0,1]$; Chapter 4 has the notion of "step spacing." Combine the two and add a harmonic-resource term:

<Box kind="definition" title="Definition 5.3 (scale scoring function)">

For a $k$-note scale $S$, first fold the distance between two degrees into an interval class
$$
\tilde d_{ij}=\min\!\left((s_j-s_i)\bmod 12,\,(s_i-s_j)\bmod 12\right),
$$
then fix $C_4=261.626\ \text{Hz}$ and define the lookup values
$$
\mathcal S_d=S\!\left(C_4,C_4\,2^{d/12}\right),\qquad d=1,\dots,6.
$$
The three components are
$$
\bar S(S) = \frac{1}{\binom{k}{2}} \sum_{i \lt j} \mathcal S_{\tilde d_{ij}},
\qquad
U(S) = \frac{1}{1 + \sigma(g)},
\qquad
T(S) = \#\{\text{major or minor triads fully contained in } S\},
$$
where $\sigma(g)$ is the standard deviation of the step pattern $g$ (unit: semitones). The total score is
$$
F(S) = 0.55\,\bar S(S) + 0.25\,U(S) + 0.20\,\frac{T(S)}{6}.
$$

</Box>

Each of the three components handles one thing:

- $\bar S$ measures the **folded two-degree relations between pitch classes**, not the roughness of two arbitrary pitches sounding together in some actual arrangement;
- $U$ measures "whether the spacings are even"; the smaller $\sigma$, the more even; this term penalizes "a cluster of notes plus one huge gap";
- $T$ measures "how many triads these notes can build." The denominator is 6 because the champion major scale happens to have 6; enumeration shows some "clustered" sets reach 7, so this is only a scaling constant, not an upper bound, and $T/6$ can exceed 1.

Reading a major seventh as a minor second and a major sixth as a minor third is an **octave-folding assumption** added specifically to study interval classes; it is not an identity automatically implied by the finite-harmonic model of Chapter 3. For example, at the same $C_4$ reference the model gives $S\approx0.9994$ for 700 ¢, whereas the folded lookup at 500 ¢ gives $0.9722$. Hence the ranking below applies to this explicitly specified combinatorial model and should not be read directly as a consonance ranking for actual registers and voice arrangements.

The weights $0.55/0.25/0.20$ are a **modeling choice**, not a theorem. Section 5.2 will show that with a different set of weights, the champion changes. This must be stated up front; otherwise the later "major scale wins" would be misread as a mathematical proof.

## 5.2 Enumerating 792: The Major Scale Wins

### 5.2.1 How Large Is the Search Space

The number of ways to choose 7 of the 12 pitch classes is

$$
\binom{12}{7} = \frac{12!}{7!\,5!} = 792.
$$

792 sets, each requiring only 21 consonance pairs, 7 spacings, and a few triads. This scale is small enough that a laptop can run it dozens of times per second, so this chapter uses no heuristics; it **enumerates** directly.

One detail: in this chapter's pitch-class model, a global transposition changes neither the step pattern nor the interval-class distribution, so $U$, $T$, and the lookup-defined $\bar S$ are all unchanged. This is a **symmetry of the model**, not a guarantee that "roughness is unchanged when the register changes" in actual acoustics.

For a seven-note set, any nonzero transposition yields a different set: if a shift $t$ fixes a 7-element set, then $7t$ must be a multiple of 12, so $7t\equiv0\pmod{12}$; since $\gcd(7,12)=1$, $t\equiv0$. Each translation orbit contains exactly 12 sets, so the 792 sets collapse into

$$
\frac{792}{12} = 66
$$

**transposition equivalence classes**. The five-note case is analogous because $\gcd(5,12)=1$. The script first enumerates 792, then deduplicates by equivalence class, and checks that scores within a class agree exactly (actual deviation about $2\times10^{-16}$, pure floating-point error). This step matters: without folding, the top 5 would be flooded by the 12 transpositions of the same scale.

<Box kind="algorithm" title="Algorithm 5.1 (enumerating scales)">

```text
输入：k（音级数），S 表（12 个半音距离的协和度）
for 每个 C(12,k) 组合 S:
    计算间距型 g、σ(g)、S 均值、三和弦数 T
    计算 F(S)
按 F 降序排序；按「12 个平移取字典序最小」去重
返回前 5 名与各分项
```
Complexity $O\!\left(\binom{12}{k}\right)$; at $k=7$ that is 792 scorings, on the order of milliseconds.

</Box>

<Box kind="experiment" title="Experiment 5.1: Enumerating 792 seven-note sets and 792 five-note sets">

```bash
python code/ch05_scale_search.py
```

Actual output (reference $C_4 = 261.626\ \text{Hz}$, $N=5$ harmonics):

The script prints its labels in Chinese; the numbers are unchanged.

::: details Expand the full script output (138 lines, unedited)

```text:no-line-numbers
ch05_scale_search.py —— 第 5 章配套实验：在 12 个音级里穷举音阶

表 1：12-TET 各级音程的协和度（基准 C4 = 261.626 Hz）

   距离 d     音程 ¢      S(C4,·)         备注
----------------------------------------------
        1        100        0.514       小二度
        2        200        0.481       大二度
        3        300        0.643       小三度
        4        400        0.858       大三度
        5        500        0.972       纯四度
        6        600        0.827       三全音

d > 6 用 12−d 折回：大七度读作小二度、大六度读作小三度。
最粗糙的是 200 ¢ （S = 0.481），不是最近的 100 ¢。
协和度不是距离的单调函数：200 ¢ 落在粗糙峰附近，100 ¢ 反而略好。

七音集合：
  穷举 792 个集合，折叠为 66 个平移等价类；类内得分最大偏差 2.22e-16。

表 2：七音集合混合得分前 5 名

 名次  代表（含 C）                  半音间距              混合     S 均值    均匀度   三和弦     σ 间距
--------------------------------------------------------------------------------------------
    1  C C# D# F F# G# A#            1-2-2-1-2-2-2       0.7713     0.7257    0.6888        6      0.452
    2  C C# D E F G# A               1-1-2-1-3-1-3       0.7710     0.7359    0.5317        7      0.881
    3  C C# D F F# A A#              1-1-3-1-3-1-2       0.7710     0.7359    0.5317        7      0.881
    4  C C# D F F# G# A              1-1-3-1-2-1-3       0.7369     0.7344    0.5317        6      0.881
    5  C C# D E F F# A               1-1-2-1-1-3-3       0.7278     0.7180    0.5317        6      0.881

代表取 12 个平移里字典序最小的写法：平移不改任何音程，得分因此完全相同。

冠军核对：
  代表写法   C C# D# F F# G# A#（间距 1-2-2-1-2-2-2）
  平移到 C 大调写法：C D E F G A B（每个音 +11 个半音），间距 2-2-1-2-2-2-1。
  得分 0.7713 = 0.55×0.7257 + 0.25×0.6888 + 0.20×6/6。

表 3：三种打分口径的比较（同一批平移等价类）

打分口径                            冠军代表                    间距                 S 均值     三和弦
--------------------------------------------------------------------------------------
只问协和（S 均值最高）              C C# D E F G# A             1-1-2-1-3-1-3        0.7359          7
只问均匀（σ 最小）                  C C# D E F# G# A#           1-1-2-2-2-2-2        0.7036          2
协和 + 均匀 + 三和弦（本章口径）    C C# D# F F# G# A#          1-2-2-1-2-2-2        0.7257          6

只问协和的冠军间距型 1-1-2-1-3-1-3：靠「扎堆 + 大跳」堆协和度，三和弦反而有 7 个。
只问均匀的冠军 S 均值比混合冠军低 0.0221，三和弦只有 2 个。
混合口径把两者折中：S 均值排第 6、均匀度排第 1、三和弦 6 个。

表 3b：权重灵敏度（换一组系数，冠军是否变化）

权重 S/U/T       冠军代表                      间距                   得分         S    三和弦
--------------------------------------------------------------------------------
0.55/0.25/0.20   C C# D# F F# G# A#            1-2-2-1-2-2-2        0.7713    0.7257         6
0.80/0.10/0.10   C C# D E F G# A               1-1-2-1-3-1-3        0.7586    0.7359         7
0.70/0.20/0.10   C C# D# F F# G# A#            1-2-2-1-2-2-2        0.7458    0.7257         6
0.30/0.50/0.20   C C# D# F F# G# A#            1-2-2-1-2-2-2        0.7621    0.7257         6
0.30/0.10/0.60   C C# D E F G# A               1-1-2-1-3-1-3        0.9739    0.7359         7

协和权重 0.80 或三和弦权重 0.60 时，冠军换成 1-1-2-1-3-1-3 型；
均匀权重 0.50 时，冠军仍是 2-2-1-2-2-2-1。结论对权重敏感，但不脆弱。

表 4：冠军（C 大调）的 7 种调式：同一集合的循环移位

调式          音级（主音起）                半音间距             主音→第 6 音
------------------------------------------------------------------------
伊奥尼亚      C D E F G A B                 2-2-1-2-2-2-1               900 ¢
多利亚        D E F G A B C                 2-1-2-2-2-1-2               900 ¢
弗里几亚      E F G A B C D                 1-2-2-2-1-2-2               800 ¢
利底亚        F G A B C D E                 2-2-2-1-2-2-1               900 ¢
混合利底亚    G A B C D E F                 2-2-1-2-2-1-2               900 ¢
爱奥利亚      A B C D E F G                 2-1-2-2-1-2-2               800 ¢
洛克里亚      B C D E F G A                 1-2-2-1-2-2-2               800 ¢

7 个调式的音级集合完全相同，只是起点不同。特征音程是第 6 音：
800 ¢（= 8 个半音，小六度）给弗里几亚 / 爱奥利亚 / 洛克里亚，
900 ¢（= 9 个半音，大六度）给伊奥尼亚 / 多利亚 / 利底亚 / 混合利底亚。
注意：同一集合的 7 个旋转不是 7 个新的音阶，而是一个对象的 7 种读法。

校验：三和弦覆盖率在 66 个七音等价类上的分布

  7 个三和弦：2 类
  6 个三和弦：4 类
  5 个三和弦：16 类
  4 个三和弦：20 类
  3 个三和弦：10 类
  2 个三和弦：11 类
  1 个三和弦：2 类
  0 个三和弦：1 类

最多 7 个（含大三和弦与小三和弦），共 2 类。
  三和弦最多的一类：C C# D E F G# A，间距 1-1-2-1-3-1-3，混合得分 0.7710。
  三和弦最多的一类：C C# D F F# A A#，间距 1-1-3-1-3-1-2，混合得分 0.7710。

三和弦 6 个的类有 4 个；它们的间距型与最大间隙：
  C C# D E F F# A：1-1-2-1-1-3-3（最大间隙 3）
  C C# D E F A A#：1-1-2-1-4-1-2（最大间隙 4）
  C C# D F F# G# A：1-1-3-1-2-1-3（最大间隙 3）
  C C# D# F F# G# A#：1-2-2-1-2-2-2（最大间隙 2）

最大间隙 ≤ 2 的类有 3 个（这是最均匀的一族），三和弦覆盖：
  C C# D E F# G# A#：2 个三和弦，间距 1-1-2-2-2-2-2
  C C# D# E F# G# A#：4 个三和弦，间距 1-2-1-2-2-2-2
  C C# D# F F# G# A#：6 个三和弦，间距 1-2-2-1-2-2-2
最均匀一族里，只有 2-2-1-2-2-2-1 拿到 6 个三和弦；其余两类只有 4 个和 2 个。

五音集合：
  穷举 792 个集合，折叠为 66 个平移等价类；类内得分最大偏差 2.22e-16。

表 5：五音集合（C(12,5)=792，折叠后 66 类）混合得分前 5 名

 名次  代表（含 C）              半音间距              混合     S 均值    均匀度   最小间距
--------------------------------------------------------------------------
    1  C C# E F# A               1-3-2-3-3           0.6465     0.7412    0.5556      100 ¢
    2  C C# E G A                1-3-3-2-3           0.6465     0.7412    0.5556      100 ¢
    3  C D E G A                 2-2-3-2-3           0.6457     0.7476    0.6712      200 ¢
    4  C C# E F G#               1-3-1-3-4           0.6366     0.7691    0.4545      100 ¢
    5  C C# E F A                1-3-1-4-3           0.6366     0.7691    0.4545      100 ¢

如果把「不含小二度」当硬约束（3.3 节：小二度最粗糙），只剩 3 类：

代表（含 C）              半音间距              混合     S 均值    三和弦
----------------------------------------------------------------
C D E G A                 2-2-3-2-3           0.6457     0.7476         2
C D E F# A                2-2-2-3-3           0.6314     0.7218         2
C D E F# G#               2-2-2-2-4           0.5246     0.7013         0

黑键 C# D# F# G# A# 与上表的 C D E G A 属于同一个平移等价类（整体下移 6 个半音）。
它的间距是 2-3-2-2-3，最小间距 200 ¢ —— 这就是「黑键天然是五声音阶」的数学原因。
无约束冠军靠一个小二度换协和度，但只比 C D E G A 高 0.0009：
差距小到可以忽略，于是「不含小二度」这个硬约束几乎不花成本。
七音集合则做不到：7 个点塞进 12 格，鸽笼原理保证必然出现相邻半音。

关键数字：
  S(纯五度 700 ¢)  = 0.9722
  S(小二度 100 ¢)  = 0.5135
  S(大二度 200 ¢)  = 0.4812
  冠军混合得分     = 0.7713（S 0.7257 + 均匀 0.6888 + 三和弦 6）
```

:::

</Box>

Verify five things:

1. **792 collapses to 66**: because transposition does not change intervals. The representative notation in Table 2, `C C# D# F F# G# A#`, does not look like a major scale, but shifting it up 11 semitones (i.e. down 1) gives `C D E F G A B`.
2. **The champion's step pattern is `2-2-1-2-2-2-1`**, exactly the textbook major scale; its $\sigma = 0.452$ is in the smallest tier of the whole field (evenness $0.6888$, rank 1 among the 66 classes).
3. **The champion leads the tied runner-up by only $0.0003$ points** ($0.7713$ vs. $0.7710$). In other words, the model's "preference" is very weak; Section 5.2.3 explains why.
4. **The maximum triad count is 7**, achieved by two "clustered" sets scoring $0.7710$, a little below the champion. So "most triads" does not equal "best."
5. **The five-note part**: the unconstrained champion `C C# E F# A` contains a minor second and is only $0.0009$ above `C D E G A`; with "no minor second" as a hard constraint, `C D E G A` ranks first.

### 5.2.2 Reading the Table: Where the Major Scale Actually Wins

Break the three components apart and the champion's profile is clear:

- **Consonance $\bar S = 0.7257$**, ranked 6th among the 66 classes. The consonance-only champion `1-1-2-1-3-1-3` scores $0.7359$; it contains 4 minor seconds and 2 major seconds, yet has 6 major-third interval classes, showing that this lookup target is not "fewer semitones is better," nor is it the perceived ranking of actual arrangements.
- **Evenness $0.6888$**, **tied for 1st** with two other classes. The step pattern `2-2-1-2-2-2-1` has standard deviation $0.452$ semitones and is the only one among the three classes with "maximum gap no more than 2 semitones" that also gets 6 triads.
- **Triads $T = 6$**: the three major triads $C$–$E$–$G$, $F$–$A$–$C$, $G$–$B$–$D$, plus the three minor triads $D$–$F$–$A$, $E$–$G$–$B$, $A$–$C$–$E$. The global maximum is 7 (achieved by two "clustered" sets), but within the even family with "maximum gap $\le 2$," 6 is the ceiling.

So the major scale's victory can be written as the intersection of three properties:

<Box kind="theorem" title="Theorem 5.2 (the most even seven-note step pattern)">

Let $S \subset \mathbb{Z}_{12}$, $\lvert S \rvert = 7$, and suppose all spacings satisfy $g_i \le 2$. Then the multiset of the step pattern must be
$$
\{1,1,2,2,2,2,2\},
$$
i.e. five whole tones plus two semitones. Conversely, any step pattern with this multiset satisfies $g_i \le 2$. It not only minimizes the maximum gap but also makes the variance $\sigma^2$ the smallest among all seven-note step patterns.

</Box>

<Box kind="proof" title="Proof">

If all $g_i \le 2$, let $d_i = 2 - g_i \ge 0$. From $\sum g_i = 12$ we get
$$
\sum_{i=0}^{6} d_i = 7 \times 2 - 12 = 2.
$$
Seven nonnegative integers summing to 2 can only be "two 1s and five 0s," i.e. exactly two spacings equal 1 and five equal 2.

Now the variance. With the mean of the seven spacings fixed at $12/7$, minimizing $\sigma^2$ is equivalent to minimizing $\sum g_i^2$. If two spacings satisfy $g_j\ge g_i+2$, replace them with $g_j-1$ and $g_i+1$; the sum is unchanged, while the change in the sum of squares is
$$
(g_j-1)^2+(g_i+1)^2-g_j^2-g_i^2=2(g_i-g_j+1)<0.
$$
Hence in the minimum any two spacings differ by at most 1; under the conditions of positive integers summing to 12, this still forces two 1s and five 2s. $\blacksquare$

</Box>

Theorem 5.2 explains where the multiset of `2-2-1-2-2-2-1` comes from, but it does not determine the relative positions of the two semitones. Placing the two 1s into 7 positions gives $\binom72=21$ linear arrangements; viewed by cyclic position, the short distance between the two semitones has only three possibilities — 1, 2, or 3 steps — so the arrangements fall into 3 rotation classes, with 2, 4, and 6 triads respectively. The major scale belongs to the class with 6.

<Box kind="theorem" title="Theorem 5.3 (triad count of the major scale)">

The scale $S = \{0,2,4,5,7,9,11\}$ (C major) contains exactly 3 major triads and 3 minor triads, 6 in total; it is the one with the most triads among the equivalence classes with "maximum gap $\le 2$."

</Box>

<Box kind="proof" title="Proof">

Enumerate the seven notes of $S$ one by one as roots. A major triad requires the root, $+4$, and $+7$ all in $S$: $C(0)$ gives $\{0,4,7\}$, $F(5)$ gives $\{5,9,0\}$, $G(7)$ gives $\{7,11,2\}$, 3 in total; the remaining roots ($D,E,A,B$) each lack at least one note. A minor triad requires the root, $+3$, and $+7$: $D(2)$ gives $\{2,5,9\}$, $E(4)$ gives $\{4,7,11\}$, $A(9)$ gives $\{9,0,4\}$, 3 in total. The total is 6. The enumeration in Table 2 shows that the other two classes also having "maximum gap $\le 2$" contain only 4 and 2 triads, so 6 is the maximum in this family. $\blacksquare$

</Box>

### 5.2.3 Weights Decide the Champion: An Honest Boundary

Table 3 is the table in this chapter most worth rereading. Same search space, same components, only the objective changes, and the champion changes:

| Objective | Champion step pattern | $\bar S$ | Triads | Problem |
| --- | --- | --- | --- | --- |
| Consonance only | `1-1-2-1-3-1-3` | 0.7359 | 7 | spacing $\sigma = 0.881$; the melody must leap 3 semitones |
| Evenness only | `1-1-2-2-2-2-2` | 0.7036 | 2 | harmonic resources reduced to 2 triads |
| Three-way compromise | `1-2-2-1-2-2-2` | 0.7257 | 6 | not first on any single measure, but first overall |

This reminds us: **the sentence "the major scale is the mathematical optimum" must carry a qualifier.** The accurate statement is: under the objective "consonance 55% + evenness 25% + triads 20%," it ranks first among the 66 equivalence classes, and leads by only $0.0003$. Table 3b tries several other weight sets: with consonance $0.80$ / evenness $0.10$ / triads $0.10$, the champion becomes `1-1-2-1-3-1-3` (score $0.7586$); with a triad weight of $0.60$ it also becomes that one ($0.9739$). But under $0.70/0.20/0.10$ and $0.30/0.50/0.20$, the champion is still `2-2-1-2-2-2-1`. These five sample points show that the conclusion **does change with the weights**, but they do not imply "as long as the evenness weight is nonzero, the major scale necessarily wins"; the latter would require a full analysis of the parameter region.

<Box kind="pitfall" title="Common misconception: the model can 'prove' the major scale is the unique solution">

It cannot. What the model proves is a conditional statement: **given this objective function, the major scale ranks first**. The three weights in the objective are the modeler's priors about "sounding good," not derived from physical laws. Chapter 3 already explained that the roughness model itself depends on postulates such as critical bandwidth and harmonic count; change those parameters and the ranking moves.

Within these 66 classes and these three metrics, one can also verify that the major scale is a **Pareto nondominated point**: no other class is at least as good on all three of $\bar S$, $U$, and $T$ while being better on at least one. Its evenness ties for first with two classes, and its triad count is the highest in its family; but its $\bar S$ ranks only 6th. This structural fact deserves explanation, yet it is still not a proof of the major scale's historical origin or cross-cultural universality.

</Box>

## 5.3 The Modal Cycle: Seven Readings of the Same Set

### 5.3.1 A Mode Is a Rotation, Not a New Scale

Definition 5.2 already planted the seed: the tonic is selectable. For the same seven-element set, choosing a different degree as tonic yields a different **mode**.

<Box kind="definition" title="Definition 5.4 (mode)">

Let the scale be $S = \{s_0,\dots,s_{k-1}\}$ and choose the $r$-th degree as tonic. Rearrange the degrees as
$$
M_r = \left\{(s_{(r+i)\bmod k} - s_r) \bmod 12 \;\middle|\; i = 0,\dots,k-1\right\},
$$
then $M_r$ is called the $r$-th **mode** of $S$. As sets, $M_r$ and $S$ differ only by a translation $s_r$, so $\lvert M_r \rvert = k$, and the step pattern is just a cyclic shift of $g$.

</Box>

For C major, the seven modes are the seven rows of Table 4. Two ways of writing them must be distinguished: without tonic normalization, the seven rows use **exactly the same absolute pitch-class set**, only starting at a different point; written as $M_r$, each row subtracts its own tonic, so what you get is a different transposition of the same set, not a set that is equal term by term. Under both views, the interval-class distribution, the step multiset, and the triad count are unchanged, so this chapter's $\bar S$, $U$, and $T$ do not change when the tonic changes.

Then why does it sound different? Because the tonic fixes the frame of reference. The same pitch class has different intervals relative to different tonics:

- Ionian (C tonic): major third is $C$–$E$ (400 ¢), major sixth is $C$–$A$ (900 ¢), major seventh is $C$–$B$ (1100 ¢);
- Dorian (D tonic): minor third is $D$–$F$ (300 ¢), but the major sixth is still $D$–$B$ (900 ¢);
- Phrygian (E tonic): minor second is $E$–$F$ (100 ¢), minor third is $E$–$G$ (300 ¢), minor sixth is $E$–$C$ (800 ¢);
- Lydian (F tonic): major third is $F$–$A$ (400 ¢), but the fourth becomes $F$–$B$ (600 ¢), an augmented fourth;
- Locrian (B tonic): minor second $B$–$C$ (100 ¢), diminished fifth $B$–$F$ (600 ¢).

This is one structural source of modal color: **the absolute pitch-class set is unchanged, but the interval sequence obtained from the tonic changes**. The minor second above the tonic in Phrygian, the augmented fourth in Lydian, and the diminished fifth in Locrian are all features describable in cents; as for "gloomy," "floating," or "unstable," those also depend on melody, texture, and cultural context and cannot be deduced necessarily from a single interval.

<Box kind="pitfall" title="Common misconception: the seven modes are seven different scales">

If you compare only the unnormalized absolute pitch-class sets, they are indeed the same set with a different starting point; if you rewrite each mode with C as tonic, you get different sets of note names, but they are still transpositions of the same pitch-class set. Nor is modal music necessarily "tonally ambiguous": repeating the tonic, emphasizing the tonic chord, and using cadences can all establish a clear center.

The real difference appears at the level of **frame of reference and harmony**: once the tonic changes, which triads are "tonic" and which are "dominant" all change. Chapter 6 will write this layer of structure as a matrix.

</Box>

### 5.3.2 The Modal Cyclic Group

The seven modes can be seen as the action of a cyclic group. Let $S$ be a seven-element set and define the shift operator

$$
\rho\big((s_0,\dots,s_6)\big) = (s_1, s_2, \dots, s_6, s_0 + 12),
$$

that is, shift the sequence left by one and add an octave to the last note. Applying it seven times returns to the original sequence, because each of the seven notes has moved once. Thus the set of modes is the orbit of $\mathbb{Z}_7$ acting on the scale:

$$
\{\rho^r(S) : r = 0,\dots,6\}, \qquad \rho^7 = \mathrm{id}.
$$

Note that $\rho$ is not the same as "global transposition": transposition changes absolute pitch, while $\rho$ changes the **reading** (which note counts as degree 0). The former does not change the identity of the scale; the latter changes the identity of the mode. The two operations commute, so "66 transposition classes × 7 modes" are not $66 \times 7$ new objects — the modes remain within the same set.

This also explains an easily overlooked fact in Table 4: the step patterns of the seven rows are just the seven cyclic shifts of `2-2-1-2-2-2-1`, e.g. Ionian `2-2-1-2-2-2-1`, Dorian `2-1-2-2-2-1-2`, Locrian `1-2-2-1-2-2-2`. They describe the same ring of steps, just counted from a different step.

## 5.4 The Pentatonic Scale: The Mathematical Privilege of the Black Keys

### 5.4.1 The Five-Note Search: Only 3 Classes Out of 792

The search space for five notes is as large as for seven: $\binom{12}{5} = 792$, also 66 transposition equivalence classes after folding. But the constraint is completely different — a five-note set can have **no adjacent semitone at all**.

From the boundary in Theorem 5.1, only $k \le 6$ has a chance to avoid the minor second. If all spacings of a five-note set are $\ge 2$, their sum is 12, so the only possibilities are

$$
2+2+2+3+3 = 12 \quad\text{or}\quad 2+2+2+2+4 = 12.
$$

The "hard constraint" subtable of Experiment Table 5 gives the only 3 equivalence classes, with combined scores from high to low:

| Representative | Step pattern | Combined score | $\bar S$ | Triads |
| --- | --- | --- | --- | --- |
| `C D E G A` | `2-2-3-2-3` | 0.6457 | 0.7476 | 2 |
| `C D E F# A` | `2-2-2-3-3` | 0.6314 | 0.7218 | 2 |
| `C D E F# G#` | `2-2-2-2-4` | 0.5246 | 0.7013 | 0 |

`C D E G A` is the **major pentatonic scale**. Its smallest spacing is 200 ¢ and largest 300 ¢, with no adjacent semitone. The third candidate is a whole-tone fragment `C D E F# G#`, with a maximum spacing of 400 ¢; the leaps are too large, and its score is pushed down to $0.5246$.

<Box kind="theorem" title="Theorem 5.4 (semitone-free structure of the pentatonic scale)">

Let $S \subset \mathbb{Z}_{12}$, $\lvert S \rvert = 5$, and suppose all spacings satisfy $g_i \ge 2$. Then $g_i \in \{2,3,4\}$, and the step multiset can only be $\{2,2,2,3,3\}$ or $\{2,2,2,2,4\}$. Among them, the unique multiset with the smallest maximum gap is $\{2,2,2,3,3\}$, corresponding to a maximum gap of 3 semitones.

</Box>

<Box kind="proof" title="Proof">

All five spacings are $\ge 2$ and sum to 12; let $h_i = g_i - 2 \ge 0$, then $\sum h_i = 12 - 10 = 2$. The five nonnegative integers summing to 2 can only be distributed as $(2,0,0,0,0)$, $(1,1,0,0,0)$, or the same with the 2 placed in any other position; after merging, this is "one 4" or "two 3s." Hence the multiset is $\{2,2,2,2,4\}$ or $\{2,2,2,3,3\}$. The latter has maximum gap 3 and the former 4, so the latter is more even. $\blacksquare$

</Box>

This proof is more permissive than the seven-note case: five notes have "slack," so they can avoid semitones entirely; seven notes have no slack, so semitones are forced to appear. **The mathematical explanation for "pentatonic is older and more widespread than heptatonic" is exactly these 2 semitones of slack.**

### 5.4.2 Why the Black Keys Are Exactly Pentatonic

On the piano keyboard there are 5 black keys and 7 white keys. Adjacent black keys are 2 or 3 semitones apart, step pattern `2-3-2-2-3`, minimum spacing 200 ¢. The last row of Experiment Table 5 gives the key fact: the black-key set $\{1,3,6,8,10\}$ belongs to the **same transposition equivalence class** as `C D E G A` — shifting all the black keys down 6 semitones gives exactly `C D E G A`.

So "the black keys are naturally a pentatonic scale" is neither a coincidence nor an aesthetic choice by piano makers, but the same combinatorial structure in a different key. Conversely, the 7 white keys form a seven-note scale, so minor seconds necessarily exist among the white keys ($E$–$F$, $B$–$C$) — guaranteed by Theorem 5.1.

<Box kind="pitfall" title="Why 'larger minimum spacing' in the pentatonic scale does not mean 'more consonant'">

Table 1 shows that in the $C_4$ register, $200\ \text{¢}$ has $S = 0.481$, actually the lowest in the whole table; $100\ \text{¢}$ has $S = 0.514$, slightly higher. This is the opposite of the conclusion in Chapter 3 ($330\ \text{Hz}$), where the minor second was the roughest. The reason is that the critical bandwidth varies with frequency, so the roughness peak moves.

So the accurate reason "the pentatonic scale avoids the minor second" is not "avoid the roughest interval" but three more down-to-earth facts: (1) fewer degrees, a smaller codebook, melodies easier to remember; (2) larger spacing between adjacent degrees, wider tolerance for quantization and performance error; (3) no semitone adjacency, so tonal boundaries are not "nailed down" by a semitone, and it sounds more open. The roughness model is supporting evidence, not the sole reason.

</Box>

## 5.5 Summary

This chapter turned the scale into a combinatorial optimization problem:

$$
\underbrace{\binom{12}{7} = 792}_{\text{search space}}
\;\xrightarrow{\text{transposition dedup}}\;
\underbrace{66\ \text{equivalence classes}}_{\text{candidates}}
\;\xrightarrow{\ 0.55\bar S + 0.25U + 0.20T/6\ }\;
\underbrace{\text{major scale}}_{\text{champion}}
$$

Three main conclusions:

- **Seven notes must contain a minor second** (Theorem 5.1): seven positive integers summing to 12 must include a 1. Put 7 notes in an octave, and you must accept one semitone adjacency.
- **The major scale's step pattern `2-2-1-2-2-2-1` is the unique multiset with the smallest maximum gap** (Theorem 5.2): five 2s plus two 1s, $\sigma = 0.452$ semitones, the most even tier among the 66 classes.
- **The major scale wins on a three-way compromise, not on any single measure**: $\bar S$ ranks 6th, evenness 1st, triads 6; total score $0.7713$, leading the runner-up by only $0.0003$. Raise the consonance weight to 80%, and the champion becomes a "clustered + big leap" set like `1-1-2-1-3-1-3`.

The pentatonic scale is the solution of the same search under looser constraints: of $\binom{12}{5}=792$, only 3 classes avoid the minor second, and `C D E G A` scores highest among them; the black-key pentatonic is just its transposition by 6 semitones. **The "antiquity" and "universality" of the pentatonic correspond to those 2 semitones of slack in the 12 slots.**

The next chapter accepts the major scale as a "pitch-class set" and turns to another question: press these pitch classes together — what is a chord? And what is a progression between chords? The answer will use 12-dimensional indicator vectors and transition matrices — and the "6 triads" computed in this chapter are exactly that chapter's state space.

<Box kind="exercise" title="Exercises">

1. Verify $\binom{12}{7} = \binom{12}{5} = 792$ and explain why the two binomial coefficients are equal. Use this identity to explain the coincidence in size between the "seven-note search" and the "five-note search."
2. Prove: if $k=6$ and all spacings are $\ge 2$, the step pattern can only be `2-2-2-2-2-2`, corresponding to the whole-tone scale. What is this scale's triad coverage? Verify with the script.
3. Change the triad weight in Definition 5.3 from $0.20$ to $0$, and rerun the search. Does the champion change? If so, to which one? What does this experiment say about the relation between weights and conclusions?
4. The black-key pentatonic $\{1,3,6,8,10\}$ differs from `C D E G A` by a transposition of how many semitones? Write down the transposition amount, and explain why the piano arranges the 5 black keys as `2-3-2-2-3` rather than equally spaced.
5. (Open) Replace the hard constraint "no minor second" with "no tritone": how many equivalence classes satisfy it for five notes and for seven notes? What are their scores? Can this explain which musical tradition prefers which scale?

</Box>

<Box kind="checkpoint" title="Self-check">

Close the book and write down three things: (1) why the proof of Theorem 5.1 uses only "the sum is 12"; (2) why `2-2-1-2-2-2-1` is the most even seven-note step pattern, and why its 21 arrangements select only 3 classes; (3) why the statement "the major scale is the unique optimum" must carry a qualifier.

</Box>

::: tip Next Chapter
Chapter 6 upgrades the pitch-class set to chords: represent a chord with a 12-dimensional indicator vector, score it with a consonance matrix, and then write the "tonic–dominant–subdominant" progression as a state transition. You will see that the 6 triads computed in this chapter are exactly enough to support the harmonic skeleton of a key.
:::
