---
title: "附录 D · 延伸阅读"
description: "15 本（篇）文献的书目地图：每本解决本书的哪个问题。"
---

# 附录 D · 延伸阅读

<div class="chapter-meta">
  <span>预计 25 分钟</span>
  <span>前置：读完第 3、4、6、8、9 章之一</span>
  <span>用途：从科普走向文献</span>
</div>

这本书刻意把每一章写成「可闭环」的：定义、公设、定理、实验、边界，一套走完。但闭环的另一面是视野窄。真实的声学、心理声学与音乐理论文献要厚得多，也吵得多：同一张协和曲线，不同实验条件能给出不同的峰值位置；同一个「欧几里得节奏」，不同作者用不同的下标约定。这一页列出 15 本（篇）我们认为值得读的文献，并按「它能回答本书的哪个问题」来组织，而不是按出版年份排队。

三条选书标准：

1. **能回答一个具体问题**，而不是「这个领域很重要」；
2. **有可检验的数据、公式或代码**，读完能动手验证；
3. **在本书的模型边界之外**：它要么给出更精确的模型，要么给出反例。

不符合这三条的畅销书，这里一概不列。

## D.1 听知觉与协和：把「好听」拆成实验

### 1. Helmholtz，《论音的感觉》

Hermann von Helmholtz, *On the Sensations of Tone as a Physiological Basis for the Theory of Music*, 1885 年 A. J. Ellis 英译本（原书 1863 年）。[archive.org 全文](https://archive.org/details/onsensationofto00helm)

这是把「协和」从美学思辨拉进实验室的第一本书。它用谐波、拍频与耳蜗生理解释为什么简单整数比听起来稳定，第 3 章的「谐波重合」思路直接继承自它。读它要带着历史眼光：Helmholtz 的时代还没有临界频带的概念，他对「不协和」的很多判断是定性描述，不是今天的定量曲线。它的价值在于问题意识，不在于具体数字。

### 2. Plomp & Levelt（1965），《音调协和与临界带宽》

Reinier Plomp & Willem J. M. Levelt, "Tonal consonance and critical bandwidth", *Journal of the Acoustical Society of America* 38(4), 548–560。[DOI](https://doi.org/10.1121/1.1909741)

这篇论文是第 3 章粗糙度核的祖先。它用纯音对做听辨实验，画出「频率差—不协和度」曲线，发现曲线的峰值落在临界带宽的一个固定比例附近 —— 本书取 $0.25\,\mathrm{CB}$ 就是把这条曲线参数化。读它要弄清两件事：实验刺激是**纯音**，不是乐器音；曲线是**平均听感**，个体差异被平均掉了。第 3 章的 5 次谐波模型是在这两条之上做的推广，不是它的原样复刻。

### 3. Zwicker & Fastl，《心理声学：事实与模型》

Eberhard Zwicker & Hugo Fastl, *Psychoacoustics: Facts and Models*, 3rd ed., Springer, 2007。[DOI](https://doi.org/10.1007/978-3-540-68888-4)

如果只读一本心理声学教材，就是这本。它系统讲掩蔽、临界带、音高、响度与粗糙度，每一章都附实验数据。本书公设 3.1 的 $\mathrm{CB}(f)\approx 94+71.3(f/\text{kHz})^{0.69}$ 来自这一传统；教材会告诉你这个拟合式在 100 Hz 以下误差变大，在 5 kHz 以上也不能外推。读它的正确方式是对着第 3 章的公式查表：哪些参数是实验测的，哪些是我们为了写代码方便而取的。

### 4. Terhardt（1974），《音高、协和与和声》

Ernst Terhardt, "Pitch, consonance, and harmony", *JASA* 55(5), 1061–1069。[DOI](https://doi.org/10.1121/1.1914648)

这篇论文值得所有「协和 = 好听」的推论者读一遍。它区分了**心理声学的协和**（没有粗糙度）与**音乐上的音程感**（虚拟音高），并指出前者不能单独解释后者。第 2 章把音高写成对数坐标、第 3 章把协和写成粗糙度函数，这两件事在 Terhardt 看来是两层不同的机制。读它不会推翻本书的公式，但会提醒你：公式算的是「不刺耳」，不是「有意义」。

### 5. Sethares，《调律、音色、频谱与音阶》

William A. Sethares, *Tuning, Timbre, Spectrum, Scale*, 2nd ed., Springer, 2005。[DOI](https://doi.org/10.1007/978-1-4471-4177-8)

这本书的核心论点很锋利：**音阶的「自然」程度取决于音色**。同一个粗糙度模型，换一套谐波包络，就会推出不同的「最佳音阶」。第 3、4 章把音色固定成 $1/i$ 衰减，是为了让例子可算；Sethares 把音色当成变量，展示了模型的另一面。书里有可下载的代码与音频，适合想改参数、听结果的人。

## D.2 律制、音阶与节奏：数论进入音乐

### 6. Benson，《音乐：一种数学的奉献》

David J. Benson, *Music: A Mathematical Offering*, Cambridge University Press, 2006。[作者主页免费 PDF](https://homepages.abdn.ac.uk/d.j.benson/pages/html/music.pdf)

这是一本「数学系写给音乐系、也写给数学系」的书，覆盖面极大：傅里叶、律制、音阶、节奏、对称性、群论，甚至附带的音频文件。它的律制章节比本书第 4 章细得多，连分数与逼近的内容也更完整。优点是免费、例子多、代码可跑；缺点是想一口气读完会迷路，建议按本书的章节顺序挑对应章节读。

### 7. Toussaint，《音乐节奏的几何》

Godfried T. Toussaint, *The Geometry of Musical Rhythm: What Makes a "Good" Rhythm Good?*, CRC Press, 2013。[DOI](https://doi.org/10.1201/b13751)

第 7 章的欧几里得节奏、克拉普环与「均匀性」讨论，大半来自 Toussaint 的整理。这本书把世界各地的节奏 pattern 画成时钟图与多边形，用几何量（面积、周长、对称性）比较它们。读它最大的收获是**去中心化**：你会看到欧洲古典节奏只是众多「好节奏」里的一种，而不是标准答案。

### 8. Demaine 等（2009），《音乐的距离几何》

Erik D. Demaine, Francisco Gomez-Martin, Henk Meijer, et al., "The distance geometry of music", *Computational Geometry: Theory and Applications* 42(5), 429–454。[DOI](https://doi.org/10.1016/j.comgeo.2008.04.005)

这篇论文把欧几里得节奏放进计算几何的框架：它证明了这类节奏与「把 $n$ 个点尽量均匀放在圆上」的问题等价，并给出若干距离性质。第 7 章的定理 7.1 只证明了「间隔只差 1」，这篇论文会告诉你还有更强的结构。它也是「音乐问题可以反向喂给数学」的好例子：节奏的均匀性帮助理解了多边形里的距离计算。

### 9. Loy，《音乐数学》第一卷

Gareth Loy, *Musimathics: The Mathematical Foundations of Music*, Vol. 1, MIT Press, 2006。[MIT Press](https://mitpress.mit.edu/9780262122824/musimathics/)

这本书偏工程：采样、量化、卷积、滤波器、音色合成，一步步把信号处理搭起来。第 1 章讲傅里叶与谐波时，如果你想知道「真实合成器怎么算一个音」，Loy 是合适的下一站。它不追求极简，公式与代码并重；读的时候可以跳过与本书无关的滤波器设计章节。

## D.3 和声与几何：和弦是高维空间里的点

### 10. Tymoczko，《音乐的几何》

Dmitri Tymoczko, *A Geometry of Music: Harmony and Counterpoint in the Extended Common Practice*, Oxford University Press, 2011。[Oxford University Press](https://global.oup.com/academic/product/a-geometry-of-music-9780195335279)

这本书把「和弦进行」翻译成高维空间里的运动：和弦是点，声部进行是路径，转调是换坐标。第 6 章的指示向量与第 9 章的环面，都是它的离散化玩具版本。Tymoczko 的野心是把传统和声学、爵士与 20 世纪音乐放进同一个几何框架；读它会让你重新理解「平行五度为什么不好」这类规则 —— 它们不再是禁令，而是空间里的某些路径。

### 11. Callender、Quinn & Tymoczko（2008），《广义声部进行空间》

Clifton Callender, Ian Quinn & Dmitri Tymoczko, "Generalized voice-leading spaces", *Science* 320(5874), 346–348。[DOI](https://doi.org/10.1126/science.1153021)

这篇短论文为第 6 章的声部距离与第 9 章的路径视角提供了更一般的空间背景：它研究不同声部进行距离之间的关系，以及由这些距离构造的音乐空间。读它要注意模型差别：本书的调性图只有 24 个节点、边权是人定的，论文关注的是声部移动定义的距离与商空间，而不是这张调性图的最短路。两者能互相启发，但不能直接把论文的定理搬到 24 节点图上。

### 12. Huron，《甜蜜的期待》

David Huron, *Sweet Anticipation: Music and the Psychology of Expectation*, MIT Press, 2006。[MIT Press](https://mitpress.mit.edu/9780262582780/sweet-anticipation/)

第 8 章说「好听是意料之外、情理之中」，Huron 把这句话展开成一整套心理学：期待来自统计学习，惊喜带来情绪，违反期待要付出认知代价。他的框架比本书的马尔可夫链宽：还考虑旋律轮廓、节奏、文化训练与情绪。读它能把「熵」和「为什么人会在副歌前感到兴奋」连接起来，也能提醒你别把 $H$ 当成「好听度」。

## D.4 统计与信息论：从熵到生成

### 13. Shannon（1948），《通信的数学理论》

Claude E. Shannon, "A mathematical theory of communication", *Bell System Technical Journal* 27(3), 379–423。[DOI](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x)

第 8 章所有公式的源头。Shannon 定义了熵、联合熵、条件熵、冗余度与信道容量，并说明「平均信息量」为什么是对数。读原文的好处是看清定义之间的依赖顺序：先有概率分布，才有熵；先有联合分布，才有条件熵。原文的很多例子是电码与英语文本，不是音乐 —— 这恰好说明这套工具是通用的。

### 14. Temperley，《基本音乐结构的认知》

David Temperley, *The Cognition of Basic Musical Structures*, MIT Press, 2001。[MIT Press](https://mitpress.mit.edu/9780262700948/the-cognition-of-basic-musical-structures/)

Temperley 用「偏好规则」建模听者如何推断节拍、调性与和弦，方法与本书的统计模型互补：他更关心「听者用什么规则做判断」，本书更关心「数据里有多少可预测性」。第 6、8 章里「功能」「调性中心」这些词，在他的框架里是一组可计算的偏好分数。想从「统计描述」走向「认知解释」，这是自然的下一本。

### 15. Manning & Schütze，《统计自然语言处理基础》

Christopher D. Manning & Hinrich Schütze, *Foundations of Statistical Natural Language Processing*, MIT Press, 1999。[MIT Press](https://mitpress.mit.edu/9780262133609/foundations-of-statistical-natural-language-processing/)

别被书名骗了：第 6、8 章用到的马尔可夫链、最大似然估计、平滑、留出检验、交叉熵，这本书都有标准而清晰的讲法。它的例子是词序列，但数学结构与音序列完全同构。第 8 章的「二阶上下文只覆盖 17/49」这类稀疏性问题，在语言模型里叫 data sparsity，处理办法（回退、插值、平滑）可以直接借用。

## D.5 五条阅读路线

书单不必从头读到尾。按你手上的问题选路线：

| 你想解决的问题 | 建议顺序 | 预计投入 |
| --- | --- | --- |
| 协和到底怎么算，模型哪里会失效 | 1 → 2 → 3 → 4 → 5 | 2~3 周 |
| 为什么是 12 个音，其他律制怎么设计 | 6 → 5 → 8 | 2 周 |
| 和弦进行与转调能不能变成几何 | 10 → 11 → 6 | 3 周 |
| 旋律统计、熵与生成 | 13 → 15 → 12 → 14 | 3 周 |
| 节奏的数学结构与世界音乐 | 7 → 8 → 6 | 2 周 |

这张表的时间估计按「每天 1 小时、做笔记」计算。如果只是查一个问题，读摘要、图表与结论即可，不必从头推公式。

## D.6 怎么读一篇论文

文献不是用来「读完」的，是用来回答问题的。我们建议三遍读法：

- **第一遍（20 分钟）**：读标题、摘要、图、结论。只回答一个问题：它和我的问题有关吗？无关就停。
- **第二遍（1~2 小时）**：看方法与参数。实验刺激是什么？样本多大？临界带宽怎么估的？结论在什么条件下成立？
- **第三遍（半天以上）**：复现一个图或一个数。复现失败不是坏事 —— 它通常意味着你发现了原文没写清的参数。

以 Plomp & Levelt 为例，第二遍至少要问：

1. 刺激是纯音还是复合音？频率、声压级各是多少？
2. 「不协和度」是听者打分还是配对比较？量表怎么归一化？
3. 曲线的峰值在哪个频率差？这个差与临界带宽的比值是多少？
4. 结论对音区、响度、个体差异是否稳健？
5. 本书的 $0.25\,\mathrm{CB}$ 与论文的峰值位置差多少？这个差会影响第 3 章的排序吗？

<Box kind="checkpoint" title="读后练习：把一篇论文折成一张卡片">

选上面任意一篇，用 200 字回答五个问题：

1. 它解决什么问题？（一句）
2. 它用什么方法？（实验 / 证明 / 模拟）
3. 关键数字或定理是什么？（一个）
4. 它的结论在什么条件下失效？（一条）
5. 它和本书哪一章的哪个公式直接相关？（给出章号与符号）

写不出第 4 条，说明你只读了摘要；写不出第 5 条，说明还没把文献接回自己的知识结构。

</Box>

## D.7 引用伦理与模型的边界

<Box kind="pitfall" title="不要把参考文献当成「权威背书」">

引用一篇论文，只说明「这个说法有出处」，不说明「这个说法在本书的条件下也成立」。三个常见的误用：

- **条件漂移**：Plomp–Levelt 的曲线来自纯音，本书却拿它给带 5 次谐波的乐器音打分；参数可以借，结论不能直接搬。
- **数值崇拜**：Zwicker 的 $\mathrm{CB}$ 公式是拟合式，在 100 Hz 以下误差明显；把 $94+71.3(f/\text{kHz})^{0.69}$ 代到 50 Hz 得到的数，不该被当成实验事实。
- **时代错位**：Helmholtz 没有现代心理声学的实验工具，他的很多判断是洞见而非数据；引用时要标明这是历史文献。

正确姿势是：**先写清自己的模型与条件，再说明文献在哪些条件下支持它、在哪些条件下不支持它**。这比多列十篇参考文献更难，也更有用。

</Box>

## D.8 结语

这一页的 15 条文献，共同构成一张「离开本书之后」的地图：往左是更精确的物理与生理模型（Helmholtz、Plomp–Levelt、Zwicker、Terhardt、Sethares），往右是更抽象的结构（Tymoczko、Callender 等、Benson、Toussaint），往下是更工程化的实现（Loy、Manning–Schütze），往上是更心理学的解释（Huron、Temperley）。你不需要全部读完；你需要的是在遇到问题时知道该往哪个方向走。

最后给一个诚实的提醒：本书的所有数字都来自 `code/` 下的脚本，所有模型都在正文里标了边界。文献能扩展这些边界，但不会替你决定「哪个模型更适合你的问题」。那个决定，仍然要你自己做。

::: tip 下一章预告
读完文献，该动手做题了。附录 E 汇总第 0~9 章每章两道题的提示与数值答案，按章排列 —— [附录 E · 习题答案](/appendix/e-exercises)。
:::
