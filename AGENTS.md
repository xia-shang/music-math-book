# AGENTS.md —— 写作 / 维护手册

> 你是这本书的**作者兼编辑**。任何接手本仓库的 agent 或人类，先读完本文件，再读 `PLAN.md`，最后看 `PROGRESS.md` 决定从哪继续。

## 一句话目标

把《音乐的数理逻辑》写成一个可以部署在 GitHub Pages 上的 VitePress 网页书：10 章正文、5 个附录、10 个可运行的 Python 脚本，风格统一、数学自洽、数字可验证。

## 仓库结构

```
docs/                     # 站点根目录（VitePress srcDir）
  index.md                # 首页（已完成，勿动）
  about.md                # 关于（已完成）
  guide/                  # 导读三页（已完成）
  chapters/               # 第 0~9 章（00 与 03 已完成；03 是风格基准）
  appendix/               # 附录 A~E（均为占位页，待写）
  .vitepress/config.mts   # 站点配置（导航/侧边栏/数学开关，尽量勿动）
  .vitepress/theme/       # 自定义主题与组件（勿动，除非修 bug）
  public/logo.svg
  public/figures/         # 脚本生成的 SVG 插图（勿手改）
  public/audio/           # 脚本生成的 WAV 对照音频（勿手改）
code/                     # Python 实验脚本（common.py 已完成）
  common.py               # 公共函数（音高、临界带宽、粗糙度、律制）
  ch03_consonance.py      # 已完成，可作脚本风格基准
  ch0X_*.py               # 待写
  make_figures.py         # 生成 docs/public/figures/*.svg
  make_audio.py           # 生成 docs/public/audio/*.wav
PLAN.md                   # 全书内容规格（写作合同）
PROGRESS.md               # 任务清单与进度（每完成一项就打勾）
```

## 环境与命令

工作目录：仓库根目录。Windows + PowerShell。

### 构建 / 校验站点（必须做）

```powershell
$env:PATH="C:\Users\Aanch\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin;$env:PATH"
node "C:\Users\Aanch\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\pnpm\bin\pnpm.mjs" build
```

成功标志：输出 `build complete in ...`，退出码 0。构建会检查死链，因此导航里出现不存在的页面会直接报错。

### 运行 Python 脚本

```powershell
$env:PYTHONUTF8='1'
& "C:\Users\Aanch\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" code\ch04_tuning.py
```

如果上述 Python 路径不存在，退回 `python code\ch04_tuning.py`。

### 本地预览（可选）

```powershell
node "...\pnpm.mjs" dev     # http://localhost:5173
```

## 硬性规则

1. **不许留占位页。** `::: warning 占位页` 必须被真实内容替换。
2. **正文数字必须来自真实运行结果。** 写 `ch0X` 脚本 → 运行 → 把输出粘进 `<Box kind="experiment">`。不许编造数值。
3. **不要重写第 3 章。** 它是风格基准；如发现笔误可小改，但保持结构。
4. **不要改** `docs/.vitepress/`、`package.json`、`pnpm-workspace.yaml`，除非构建确实因它们失败；改动要在 `PROGRESS.md` 记录原因。
5. **一次只推进一个任务**（`PROGRESS.md` 里第一个未完成项），完成后立刻构建校验并更新 `PROGRESS.md`。
6. **链接必须合法**：站内链接用 `/chapters/02-pitch` 这种 clean URL（不带 `.md`）；`pnpm build` 会校验。
7. **中文全角标点**，中英文/数字之间留空格；代码与公式内部不空格。
8. 不引入新依赖、不引入新图片、不改配色。
9. 每章结尾必须有「下一章预告」，链接指向真实文件；第 9 章用「全书回顾」。
10. 提交前自查：本文件末尾的「完稿检查清单」。
11. **插图与音频必须可复现**：由 `code/make_figures.py` / `code/make_audio.py` 生成；页面统一用 `<Figure>` / `<AudioDemo>` 组件引用。不要直接写 `<img src="/xx.svg">` 或把大段 base64/二进制塞进仓库 —— 部署到 `/<repo>/` 子路径时会 404。

## 章节模板（直接复制）

```md
---
title: "第 N 章 · 标题"
description: "一句话描述（30 字内）"
---

# 第 N 章 · 标题

<div class="chapter-meta">
  <span>预计 40 分钟</span>
  <span>前置：第 N-1 章</span>
  <span>代码：code/chNx_xxx.py</span>
</div>

本章要回答的问题：

1. ……
2. ……
3. ……

## N.1 小节标题

正文……

<Box kind="definition" title="定义 N.1（……）">
……
</Box>

## N.2 ……

## N.x 小结

……

<Box kind="exercise" title="习题">
1. ……
</Box>

::: tip 下一章预告
一句话 + [第 N+1 章](/chapters/xx-xxx)。
:::
```

## 组件 API

| 标签 | 用途 | 注意 |
| --- | --- | --- |
| `<Box kind="..." title="...">` | 各种盒子 | kind 只能取：definition / axiom / theorem / proof / experiment / exercise / algorithm / pitfall / checkpoint / note；盒子内部可以放公式、列表、代码块 |
| `<ConsonanceExplorer />` | 粗糙度交互演示 | 只在第 3 章（已用）或第 4 章引用；不要再改组件本身 |
| `<CentsRuler />` | 三种律制偏差对比 | 用在第 4 章 |
| `<Figure src="/figures/…" caption="…" />` | 脚本生成的 SVG 插图 | 先跑 `make_figures.py`；caption 写清「图在说明什么」，不要只写「如图」 |
| `<AudioDemo src="/audio/…" title="…" hint="…" />` | 试听卡片 | 先跑 `make_audio.py`；hint 说明「该听哪个差异」；成对出现时用 `<div class="audio-row">` 包一层 |

VitePress 内置容器：`::: tip` / `::: warning` / `::: danger` / `::: info` 可用。不要自己发明 `::: theorem`。

## 数学排版

- 行内 `$f = 440$`；独立公式：

```md
$$
p = 1200 \log_2 \frac{f}{f_0}
$$
```

- 绝对值用 `\lvert x \rvert`，不要在表格里写 `|x|`。
- 中文不要塞进 `$...$` 里；需要单位写 `\text{Hz}`。
- MathJax 会把 `$` 当数学定界符，正文不要出现单独的 `$` 符号（例如价格）。

## 写作质量检查（每章自问）

1. 开场问题有没有在正文里被真正回答？
2. 每个「定理」是否都能由本章定义/公设推出？推导里有没有跳步？
3. 有没有至少一个「可运行实验」，它的输出与正文数字一致？
4. 有没有交代模型的**失效边界**（至少一个 pitfall 或说明）？
5. 公式是否有直觉解释（一句话说明它在讲什么）？
6. 字数是否 ≥ 2000 汉字，且没有灌水段落？

## 每章的推荐结构（平衡「推导」与「可读」）

- 40% 现象与直觉（物理图像、例子、反例）
- 35% 定义/定理/推导（形式化）
- 15% 代码与数据（可验证）
- 10% 边界、盲点与习题

## 常见坑

- `pnpm build` 报 dead link：通常是链接写了 `.md` 后缀或层级错了。站内链接以 `/` 开头。
- 构建报 `spawn git ENOENT`：正常现象，配置里 `lastUpdated` 已按 `CI` 环境变量关闭。
- 表格里有 `|` 会被当成列分隔符：用 `\lvert`/`\rvert` 或 `\vert`。
- 组件标签与 markdown 之间要空行，否则可能被当成段落文本。
- 脚本输出中文时务必设置 `PYTHONUTF8=1`，否则 Windows 控制台会乱码。

## 完稿检查清单

- [ ] 该章所有小节与 PLAN.md 一致，编号连续
- [ ] 至少 2 个 Box（definition/theorem 类）+ 1 个 experiment + 1 个 exercise
- [ ] `python code/ch0X_*.py` 运行通过，输出与正文一致
- [ ] `pnpm build` 通过
- [ ] 章末链接可达
- [ ] `PROGRESS.md` 已更新
