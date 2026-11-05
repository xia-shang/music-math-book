# 理科生的乐理书 · 程序员版

> 《音乐的数理逻辑：从振动到结构的公理化乐理》
>
> 不背五线谱，先写微分方程。用物理、数学和代码把「听起来对」变成「算得出来」。

[![Deploy](https://github.com/xia-shang/music-math-book/actions/workflows/deploy.yml/badge.svg)](https://github.com/xia-shang/music-math-book/actions/workflows/deploy.yml)
![Version](https://img.shields.io/badge/version-1.1.0-0f766e)
![Languages](https://img.shields.io/badge/languages-中文%20%7C%20English-blue)
![VitePress](https://img.shields.io/badge/VitePress-1.6-646cff)
![Python](https://img.shields.io/badge/Python-3.12-3776ab)
![License](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey)

**在线阅读：<https://xia-shang.github.io/music-math-book/>**
**English edition: <https://xia-shang.github.io/music-math-book/en/>**

> v1.1.0 新增英文版（中文/English 可切换）、版本页、21 段程序生成音频与 4 张新图。更新日志见 [`docs/releases.md`](docs/releases.md)。

## 中英双语

- 中文版：<https://xia-shang.github.io/music-math-book/>
- English edition：<https://xia-shang.github.io/music-math-book/en/>

页面右上角的语言菜单可以在「简体中文 / English」之间切换；版本号在导航栏 `v1.1.0` 与页脚，详见 [`docs/releases.md`](docs/releases.md)。

## 这是什么

一本开源网络书。它按 **物理现象 → 数学建模 → 感知规律 → 系统推演** 的顺序重写乐理：

- 每个概念都从可测量的量出发：频率、周期、振幅、频谱；
- 每条结论都写成定义、公设与定理，可以顺着推、也可以顺着查；
- 每章配一个可运行的 Python 脚本，书里的数字你都能自己重算一遍；
- 关键概念有可交互组件（协和度曲线、律制偏差尺、欧几里得节奏实验），不用靠想象；
- 关键图表是脚本生成的 SVG；音程、音阶、终止式、节奏与马尔可夫旋律都配了 21 段可试听的 WAV 对照。

## 目录

| 部 | 章 | 主题 | 代码 |
| --- | --- | --- | --- |
| 一 · 声与音 | 0 | 导论：音乐作为物理与心理的接口 | `code/ch00_intro.py` |
| | 1 | 振动的数学 —— 声音的起源 | `code/ch01_vibration.py` |
| | 2 | 音高的物理与几何学 | `code/ch02_pitch.py` |
| 二 · 协和与律制 | 3 | 协和与不协和的物理学本质 | `code/ch03_consonance.py` |
| | 4 | 律制的数学优化问题 | `code/ch04_tuning.py` |
| | 5 | 音阶的生成算法 | `code/ch05_scale_search.py` |
| 三 · 结构与时间 | 6 | 和声的线性代数模型 | `code/ch06_harmony.py` |
| | 7 | 节奏的分形与混沌 | `code/ch07_rhythm.py` |
| | 8 | 旋律的统计学与信息论 | `code/ch08_melody.py` |
| | 9 | 调性与离调的拓扑学 | `code/ch09_topology.py` |

附录：数学工具速查 / 代码与实验环境 / 术语表 / 延伸阅读 / 习题答案。

## 本地运行

需要 Node.js ≥ 20 与 pnpm ≥ 9。

```bash
pnpm install
pnpm dev       # http://localhost:5173
pnpm build     # 构建到 docs/.vitepress/dist
pnpm preview   # 预览构建结果
```

跑代码实验只需要 Python ≥ 3.10（无第三方依赖）：

```bash
python code/ch03_consonance.py
python code/ch05_scale_search.py
```

## 部署到 GitHub Pages（3 分钟）

1. **Fork 或新建仓库**，把本项目推到 `main` 分支：

   ```bash
   git init
   git add .
   git commit -m "feat: 初始化《理科生的乐理书》"
   git branch -M main
   git remote add origin git@github.com:<你的用户名>/music-math-book.git
   git push -u origin main
   ```

2. 打开仓库 **Settings → Pages**，把 **Source** 设为 **GitHub Actions**。

3. 推送即部署。`.github/workflows/deploy.yml` 会自动：
   - 安装依赖、构建静态站点；
   - 依据仓库名计算 `BASE_PATH`：项目站点用 `/<仓库名>/`，仓库名以 `.github.io` 结尾时自动改用 `/`；
   - 上传 artifact 并用 `actions/deploy-pages` 发布。

4. 首次部署完成后，站点地址是：

   ```
   https://<你的用户名>.github.io/<仓库名>/
   ```

> 使用自定义域名时，站点根路径是 `/`，需要把 workflow 里的 `BASE_PATH` 改为 `/`；项目站点与用户主页站点的判断不需要手动改。

## 项目结构

```
docs/                       # VitePress 站点（中文根路径 /）
  .vitepress/config.mts     # 双语 locale、导航、侧边栏、MathJax、搜索、版本号
  .vitepress/theme/         # 自定义主题 + 交互组件 + i18n 文案
  chapters/                 # 中文版 10 章正文
  appendix/                 # 中文版 5 个附录
  guide/                    # 中文版导读、符号表、路线图
  index.md                  # 中文首页
  releases.md               # 版本与更新日志
  en/                       # 英文版（相同结构，路径 /en/）
  public/figures/           # 脚本生成的 SVG 插图
  public/audio/             # 脚本生成的对照音频（WAV）
code/                       # 全书 Python 实验（仅标准库）
TRANSLATION.md              # 英文版翻译规范与术语表
AGENTS.md                   # 写作/维护手册（给未来的作者与 agent）
PLAN.md                     # 全书内容规格
PROGRESS.md                 # 进度看板
.github/workflows/deploy.yml
```

## 技术栈

| 层 | 选择 | 为什么 |
| --- | --- | --- |
| 站点 | **VitePress 1.6** | Markdown 写作 + Vue 交互，构建即静态，天然适合 GitHub Pages |
| 公式 | **MathJax（服务端渲染 SVG）** | 构建期成图，不依赖客户端 JS，首屏就正确 |
| 交互 | **Vue 3 单文件组件** | 手写 SVG，零图表库依赖，体积小 |
| 插图 / 音频 | **Python 生成** | 7 张 SVG + 8 个 WAV，全部来自 `code/make_*.py`，可复现 |
| 实验 | **Python 标准库** | 读者无需配置环境，`python xxx.py` 即可复现 |
| 部署 | **GitHub Actions + Pages** | push 即发布，无额外服务器 |

## 关于书名

「程序员版」不是噱头：全书用公理化（定义/公设/定理）组织内容，用可运行代码验证结论，用版本化的仓库承载知识——这三件事，恰好是写一份好技术文档的同一套方法论。

## 许可

- 正文与插图：**CC BY-NC-SA 4.0**（署名 · 非商业性使用 · 相同方式共享）
- 代码示例：**MIT**

详见 [LICENSE](./LICENSE)。

## 贡献

欢迎 Issue / PR：修公式、补实验、改善解释。贡献前请读 [AGENTS.md](./AGENTS.md) 与 [PLAN.md](./PLAN.md)。
