---
layout: home

hero:
  name: 理科生的乐理书
  text: 从振动到结构的公理化乐理
  tagline: 不背五线谱，先写微分方程。用物理、数学和代码把「听起来对」变成「算得出来」。
  image:
    src: /logo.svg
    alt: 理科生的乐理书
  actions:
    - theme: brand
      text: 开始阅读
      link: /guide/
    - theme: alt
      text: 章节目录
      link: /chapters/00-introduction
    - theme: alt
      text: 关于本书
      link: /about

features:
  - icon: 🌊
    title: 物理先行
    details: 每个概念都从可测量的量出发 —— 频率、周期、振幅、频谱，而不是从「老师说要这样弹」出发。
  - icon: ∑
    title: 数学建模
    details: 音高是对数坐标，协和度是内积，律制是一个带约束的优化问题。乐理被翻译成一串可以推导的式子。
  - icon: 🐍
    title: 代码可跑
    details: 每章配 Python 脚本，书里的每个结论你都能在终端里重算一遍 —— 包括「哪个音程最协和」。
  - icon: 🧱
    title: 公理化组织
    details: 定义 → 公设 → 定理 → 推论。像读一份 RFC 一样读乐理，每一句结论都有前因。
  - icon: 🎛
    title: 可交互
    details: 拖动滑块，协和度曲线、拍频、律制偏差当场变化。看见的东西比记住的东西可靠。
  - icon: 🎧
    title: 可试听
    details: 纯律 vs 12-TET 的五度、三度、三和弦，配了真实合成的 WAV 对照 —— 结论也能用耳朵验收。
  - icon: 🚀
    title: 一键上线
    details: VitePress + GitHub Actions + Pages。push 到 main，网站自动重新构建并部署。
---

<ClientOnly>

<div class="mm-banner">音高   f  ──▶  p = 1200·log₂(f/f₀)      [cents]
协和度 D(f₁,f₂) = Σᵢ Σⱼ (aᵢaⱼ) · W(Δf / CB)    [粗糙度模型]
律制    min Σ |1200·log₂(2^(k/n)) − 1200·log₂(qₖ)|²  [优化问题]
和声   𝕍 = span{ v_T, v_S, v_D }                [状态空间]</div>

</ClientOnly>

## 这本书想干什么

传统乐理教材从符号开始：先认谱号，再背和弦表，最后凭手感判断「协和」。这套流程对有天分的人有效，对习惯推导的人则是折磨。

本书换一个顺序：**现象 → 建模 → 感知 → 系统**。先问「两个音同时响会发生什么」（第三章），再问「为什么人耳会把某些组合判为协和」（临界频带），最后问「世界各地的律制为什么收敛到十二平均律」（第四章）。所有结论都写成定义、公设和定理，所有计算都能用附带的 Python 脚本复现。

## 章节地图

<div class="mm-grid">
  <a href="./chapters/00-introduction">
    <span class="no">CH.00</span>
    <span class="title">导论：音乐作为接口</span>
    <span class="desc">模式识别、公理化体系、对数与傅里叶的直觉。</span>
  </a>
  <a href="./chapters/01-vibration">
    <span class="no">CH.01</span>
    <span class="title">振动的数学</span>
    <span class="desc">简谐振动、傅里叶级数、音色从哪来。</span>
  </a>
  <a href="./chapters/02-pitch">
    <span class="no">CH.02</span>
    <span class="title">音高的物理与几何</span>
    <span class="desc">韦伯-费希纳定律、八度等价、螺旋模型。</span>
  </a>
  <a href="./chapters/03-consonance">
    <span class="no">CH.03</span>
    <span class="title">协和与不协和</span>
    <span class="desc">拍频、临界频带，以及一个可计算的协和度函数。</span>
  </a>
  <a href="./chapters/04-tuning">
    <span class="no">CH.04</span>
    <span class="title">律制的数学优化</span>
    <span class="desc">毕达哥拉斯困境、纯律的局部最优、十二平均律的工程胜利。</span>
  </a>
  <a href="./chapters/05-scales">
    <span class="no">CH.05</span>
    <span class="title">音阶的生成算法</span>
    <span class="desc">从泛音列里提取 7 个最优音级，以及五声音阶的特权。</span>
  </a>
  <a href="./chapters/06-harmony">
    <span class="no">CH.06</span>
    <span class="title">和声的线性代数</span>
    <span class="desc">音级集合、基向量、T-S-D-T 的状态空间动力学。</span>
  </a>
  <a href="./chapters/07-rhythm">
    <span class="no">CH.07</span>
    <span class="title">节奏的分形与混沌</span>
    <span class="desc">欧几里得算法、切分音的统计、互质复节奏。</span>
  </a>
  <a href="./chapters/08-melody">
    <span class="no">CH.08</span>
    <span class="title">旋律的统计学</span>
    <span class="desc">马尔可夫链、信息熵，以及「意料之外、情理之中」。</span>
  </a>
  <a href="./chapters/09-topology">
    <span class="no">CH.09</span>
    <span class="title">调性的拓扑学</span>
    <span class="desc">五度圈的几何、转调的路径规划、无调性随机游走。</span>
  </a>
</div>

## 适合谁

- 学过一点微积分和线性代数、但一看到五线谱就想关页面的理科生；
- 写代码的人，想搞清楚 `f = 440 × 2^(n/12)` 背后到底发生了什么；
- 教乐理的老师，想要一套可以「算给别人看」的解释；
- 任何相信「好听」不该是无理由的人。

## 怎么读

每章开头是**问题清单**，中间是**定义 / 公设 / 定理**的正式推导，末尾是**可运行实验**和**习题**。
看不懂公式时先跑代码：`python code/ch03_consonance.py`，数值会告诉你公式在做什么。

<Box kind="note" title="前置知识">

你不需要会弹琴，但需要知道导数和复利。第三章会用到一点积分（求谐波能量），第六章会用到一点线性代数（基与内积）。附录 A 有速查表。

</Box>
