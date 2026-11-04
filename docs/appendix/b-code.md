---
title: "附录 B · 代码与实验环境"
description: "十个脚本的清单、公共 API、复现步骤与一键部署说明。"
---

# 附录 B · 代码与实验环境

<div class="chapter-meta">
  <span>预计 20 分钟</span>
  <span>前置：会运行命令行</span>
  <span>代码：code/ 目录</span>
</div>

这一页是实验部分的说明书，回答三个问题：

1. 这些脚本用什么写的、怎么跑？
2. 每个脚本具体输出什么、正文里的哪张表对应哪一段？
3. 我想加一个自己的实验，应该从哪儿下手？

书里的每一个数字都来自 `code/` 下的脚本；没有「示意值」，也没有「大概是这样」。如果你发现正文与输出对不上，以脚本输出为准 —— 那是我们唯一承认的事实来源。

## B.1 环境：一个解释器，零第三方依赖

实验只用 Python 标准库：`math`、`random`、`itertools`、`statistics`、`heapq`、`unicodedata`、`pathlib`。没有 numpy，没有 pandas，也没有 matplotlib。原因不是「返璞归真」，而是三条工程约束：

- **可复现**：任何一台装了 Python 的机器都能跑，不用处理二进制轮子；
- **可粘贴**：输出是纯文本表格，直接进 Markdown，不需要截图；
- **可审计**：每个数字都能在源码里找到对应的 `print`，中间没有黑箱。

本书写作环境实测的解释器版本：

```text
Python 3.12.14
```

代码只用到 3.10 以前的语法（类型标注、f-string、`pathlib`），没有碰 3.11 或 3.12 的新特性，所以 3.10 与 3.11 也能跑。运行方式是在**仓库根目录**执行：

```bash
python code/ch03_consonance.py
```

Windows 上如果输出出现乱码，先设置 UTF-8：

```powershell
$env:PYTHONUTF8='1'
python code\ch03_consonance.py
```

<Box kind="note" title="为什么所有脚本都从仓库根目录运行">

脚本用 `sys.path.insert(0, Path(__file__).parent)` 找到同目录的 `common.py`，所以严格来说在哪个目录运行都能导入。但正文里的命令统一写成 `python code/xxx.py`，输出里的相对路径也按仓库根目录解释 —— 这是为了让读者复制粘贴时不需要猜当前目录。

</Box>

构建站点需要 Node.js 20 以上与 pnpm 9 以上：

```bash
pnpm install
pnpm build
```

`pnpm build` 会做三件事：渲染 Markdown、检查站内死链、把结果写到 `docs/.vitepress/dist`。成功标志是最后一行出现 `build complete in ...`，退出码 0。

## B.2 十个实验脚本 + 两个资产生成脚本

每章一个脚本，命名规则是 `chNN_主题.py`。行数统计包含文档字符串与空行；输出行数是实际运行一次得到的行数，不包括末尾空行。两个 `make_*.py` 负责生成网页用的插图与音频，不打印表格。

| 脚本 | 行数 | 输出行数 | 主要内容 |
| --- | --- | --- | --- |
| `ch00_intro.py` | 120 | 71 | 音名—频率—cent 对照、对数感知、12 音级量化、常用比值 |
| `ch01_vibration.py` | 176 | 74 | 方波傅里叶系数、部分和误差、ASCII 波形、自相关 |
| `ch02_pitch.py` | 180 | 90 | 螺旋坐标、音程加法、比值复杂度排序、12-TET 坐标 |
| `ch03_consonance.py` | 52 | 24 | 13 个音程的粗糙度与协和度、0~1200 ¢ 曲线谷底 |
| `ch04_tuning.py` | 190 | 94 | 五度链、三种律制偏差、狼五度、n-TET 误差搜索 |
| `ch05_scale_search.py` | 350 | 138 | 792 个七音集合穷举、三种打分口径、调式、五声 |
| `ch06_harmony.py` | 378 | 133 | 12×12 协和矩阵、220 个三音集合、T/I、功能转移 |
| `ch07_rhythm.py` | 267 | 105 | E(k,n) 模式、528 组穷举、切分度、复合节奏、克拉普环 |
| `ch08_melody.py` | 444 | 193 | 转移矩阵、熵与冗余、留出检验、猜谜、生成旋律 |
| `ch09_topology.py` | 379 | 125 | 五度圈、二音和弦计数、24 调图、最短路、随机游走 |
| `make_figures.py` | 357 | 9 | 生成 `docs/public/figures/` 下 7 张 SVG 插图 |
| `make_audio.py` | 135 | 18 | 生成 `docs/public/audio/` 下 8 个对照 WAV |

<Box kind="experiment" title="实验 B.1：十个脚本全部跑通">

```powershell
$env:PYTHONUTF8='1'
Get-ChildItem code -Filter 'ch*.py' | Sort-Object Name | ForEach-Object {
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $out = & python $_.FullName
  $sw.Stop()
  $code = $LASTEXITCODE
  "{0,-20} exit={1}  lines={2,3}  {3,5:N2}s" -f $_.Name, $code, @($out).Count, $sw.Elapsed.TotalSeconds
}
```

真实输出（一次实测，用时含解释器启动）：

```text
ch00_intro.py        exit=0  lines= 71   0.08s
ch01_vibration.py    exit=0  lines= 74   0.11s
ch02_pitch.py        exit=0  lines= 90   0.07s
ch03_consonance.py   exit=0  lines= 24   0.08s
ch04_tuning.py       exit=0  lines= 94   0.07s
ch05_scale_search.py exit=0  lines=138   0.12s
ch06_harmony.py      exit=0  lines=133   0.11s
ch07_rhythm.py       exit=0  lines=105   0.07s
ch08_melody.py       exit=0  lines=193   0.06s
ch09_topology.py     exit=0  lines=125   0.07s
```

十行全是 `exit=0`，合计 1047 行输出，总用时不到 1 秒。最慢的是 `ch05_scale_search.py`（0.12 s），因为它真的穷举了 $2\times\binom{12}{7}=1584$ 个集合；`ch08_melody.py` 反而快，因为 48 个音的语料只做矩阵统计。

</Box>

这套「轻量」是有代价的：没有 numpy，`ch05` 的穷举只能用 `itertools.combinations` 手写循环；没有 matplotlib，所有「曲线」只能打印成表格或 ASCII 图。如果你要做更重的实验（比如扫 10 万个音程），建议把 `common.py` 拷进自己的项目，再引入 numpy —— 但那就离开了本书的复现范围。

## B.3 `common.py`：公共函数的 API

所有脚本共享同一套物理与感知参数。公共函数只放在 `code/common.py`，脚本通过 `sys.path` 导入，保证「同一个音程在不同章节得到同一个协和度」。

| 函数 / 常量 | 返回 | 说明 | 主要使用章节 |
| --- | --- | --- | --- |
| `cents_of_ratio(ratio)` | float | $1200\log_2(\text{ratio})$ | 0、2、4、5、8、9 |
| `ratio_of_cents(cents)` | float | $2^{\text{cents}/1200}$ | 2、4、5、6 |
| `pitch_of_freq(f, f_ref=A4)` | float | 频率 → 相对参考的音高坐标 | 0、2 |
| `freq_of_pitch(p, f_ref=A4)` | float | 音高坐标 → 频率 | 0、2、9 |
| `hz_to_cents(f1, f2)` | float | 两个频率的音程 | 1、3 |
| `critical_band(f)` | float | 临界带宽 $\mathrm{CB}(f)$，Hz | 3、6 |
| `roughness_kernel(df, bw)` | float | 单对谐波的粗糙度核 $W$ | 3 |
| `dissonance(f1, f2, partials=5)` | float | 两音总粗糙度 $D$ | 3、5、6 |
| `consonance(f1, f2, partials=5)` | float | 协和度 $S=1/(1+D)$ | 3、5、6 |
| `interval_ratios()` | list | 13 个音程的纯律比 / 12-TET 比 / 半音数 | 2、4 |
| `tet_ratios(n=12)` | list | n 平均律各级频率比 | 2、4 |
| `pythagorean_major_ratios()` | list | 五度相生律大调 7 级比值 | 4 |
| `just_major_ratios()` | list | 纯律大调 7 级比值 | 4 |
| `deviations(ratios)` | list | 一组音阶相对 12-TET 的偏差（cent） | 4 |
| `A4 = 440.0` | float | 参考频率 | 全书 |
| `KERNEL_PEAK = 0.25` | float | 粗糙度核峰值位置（以 CB 为单位） | 3、6 |
| `PARTIALS = 5` | int | 参与计算的谐波个数 | 3、5、6 |

两个参数需要特别说明，因为它们**不是推导出来的**，而是对听知觉实验的拟合：

- `KERNEL_PEAK = 0.25`：两音频率差为 $0.25\,\mathrm{CB}$ 时最粗糙；
- `PARTIALS = 5`：只算前 5 次谐波。真实乐器有几十次，但 5 次之后的能量按 $1/n$ 衰减，贡献已经很小。

<Box kind="pitfall" title="不要为了让数字好看而改 common.py">

这两个参数是模型的**输入**，相当于公设。改了它们，全书所有章节的协和度、和弦排名、音阶得分都会跟着变，而且正文里的数字会全部失效。如果确实要研究参数敏感性，正确做法是复制一份 `common.py` 到新目录，在附录或新章节里明确标注「这是另一个模型」，而不是偷偷改公共文件。

</Box>

## B.4 加一个自己的实验

假设你想验证「大三度在低音区比高音区更协和」。不必改动任何现有脚本，新建一个文件即可：

1. 在 `code/` 下新建 `my_experiment.py`（名字随意，不要覆盖 `ch*.py`）；
2. 从 `common` 导入需要的函数；
3. 固定随机种子（如果有随机）；
4. 用 `main()` 组织逻辑，末尾加 `if __name__ == "__main__":`；
5. 输出宽度控制在 80 列内，不要 ANSI 颜色；
6. 运行并确认退出码 0，再把**真实输出**粘进正文。

模板（可以原样复制，改中间的 `rows` 即可）：

```python
"""my_experiment.py —— 自定义实验模板（只依赖标准库）。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import cents_of_ratio, consonance  # noqa: E402


def main() -> None:
    rows = [("纯律大三度", 5 / 4), ("纯五度", 3 / 2)]
    for name, ratio in rows:
        c = cents_of_ratio(ratio)
        s = consonance(440.0, 440.0 * ratio)
        print(f"{name}: {c:.3f} ¢, 协和度 S = {s:.4f}")


if __name__ == "__main__":
    main()
```

运行 `python code/my_experiment.py`，真实输出是：

```text
纯律大三度: 386.314 ¢, 协和度 S = 0.9924
纯五度: 701.955 ¢, 协和度 S = 1.0000
```

注意五度显示 1.0000 —— 这不是「精确等于 1」，而是 12-TET 的五度与 $3:2$ 只差 1.955 ¢，粗糙度小到四位小数看不见。想看更多位数就把格式改成 `.6f`，但正文里保留 4 位就够了：**精度要匹配论点的强度**。

<Box kind="checkpoint" title="提交一个新实验前的四问">

1. 它是否只依赖标准库，且能在仓库根目录一条命令跑通？
2. 随机部分是否固定了种子？两次运行输出是否逐行一致？
3. 正文引用的每个数字，是否都能在输出里找到同一行？
4. 是否交代了模型的失效边界，而不是只报喜？

</Box>

## B.5 复现性：种子、浮点与舍入

十个脚本中，只有四个用到随机数，而且全部固定了种子：

| 脚本 | 随机源 | 种子 |
| --- | --- | --- |
| `ch01_vibration.py` | `random.seed(7)` | 7 |
| `ch06_harmony.py` | `random.seed(2024)` | 2024 |
| `ch08_melody.py` | `random.Random(8)` | 8 |
| `ch09_topology.py` | `random.Random(9)` | 9 |

其余六个脚本是纯确定性计算：给定输入，输出逐位相同。带随机的四个脚本也不依赖全局状态，`ch08`、`ch09` 用独立的 `Random` 实例，所以即使在同一进程里连续调用也不会互相污染。

浮点方面有三条经验：

- 同一台机器、同一个 Python 版本，输出逐位相同；
- 不同平台（Windows / Linux）在最后一位上可能不同，但 `.3f`、`.4f` 的格式化会把差异藏掉；
- 比较两个浮点数不要用 `==`，用 `abs(a-b) < 1e-9`。第 2 章验证音程加法时就是这么做的，误差上限 $1.14\times10^{-13}$。

中文对齐依赖 `unicodedata.east_asian_width`：全角字符按 2 列算，半角按 1 列算。这也是为什么脚本里有一个 `pad()` 或 `width()` 小函数，而不是直接 `f"{name:<10}"` —— 后者会把中文表头排歪。

<Box kind="pitfall" title="输出行数不是「信息量」">

`ch08_melody.py` 有 193 行输出，`ch03_consonance.py` 只有 24 行；这不代表前者更重要。行数只反映「打印了多少张表」，真正的信息量要看每行承载的结论。读脚本时先看表头，再看数字，最后看脚本末尾的「关键数字」汇总。

</Box>

还有一条与统计有关的复现性问题：样本少时熵会被低估。`ch08` 的 48 个音只覆盖 17 个二阶上下文（总共 49 个），所以二阶模型看着「熵很低」，其实是没见过的情况太多。正文用留出检验（前 6 小节训练、后 6 小节预测）来暴露这个问题，而不是拿训练集熵当结论。

## B.6 从脚本到网页：构建与部署

本地构建：

```bash
pnpm build
```

成功时最后一行类似：

```text
build complete in 21.03s
```

构建过程会检查所有站内链接。链接规则只有一条：**用 clean URL，不带 `.md`**。例如第 6 章末尾写 `/chapters/07-rhythm`，不要写 `/chapters/07-rhythm.md`。写错会直接让构建失败，而不是等上线后才发现 404。

部署到 GitHub Pages 是「一次配置、之后自动」：

- 仓库里的 `.github/workflows/deploy.yml` 在推送到 `main` 时触发；
- 工作流自动从仓库名推导 `BASE_PATH`（项目站点形如 `/<repo>/`），再执行 `pnpm build`；
- 构建产物 `docs/.vitepress/dist` 由 `actions/upload-pages-artifact` 上传，`actions/deploy-pages` 发布；
- 首次部署只需在仓库 **Settings → Pages** 里把 Source 选为 **GitHub Actions**。

本地预览用 `pnpm dev`，默认地址 `http://localhost:5173`。预览环境和线上环境的差别只有 `base`：线上带 `/<repo>/` 前缀，所以站内链接必须写成以 `/` 开头的绝对路径，不能写相对路径。

<Box kind="pitfall" title="三个最常见的构建失败">

1. **死链**：链接写了 `.md` 后缀，或层级少了一级。构建日志会直接给出源文件与目标路径。
2. **数学里的尖括号**：$x \lt 1$ 要写成 `\lt`。直接写 `<` 可能被 Vue 当成 HTML 标签的开头。
3. **表格里的竖线**：单元格里的绝对值要写 `\lvert x \rvert`，直接写 `|` 会被当成列分隔符。

</Box>

## B.7 插图与试听：两个资产生成脚本

书里的图和音频都不是手工放进仓库的二进制文件，而是脚本产物 —— 改一个参数，重跑一次，全书的图和音频一起更新：

```bash
python code/make_figures.py   # docs/public/figures/*.svg（7 张）
python code/make_audio.py     # docs/public/audio/*.wav（8 个）
```

设计约束：

- **图是 SVG**：矢量、可 diff、可版本化，由字符串模板拼出，不引入 matplotlib；
- **音频是 WAV**：22050 Hz / 16 bit / 单声道，6 个谐波、1.8 s，合计约 620 KB；
- **页面用组件引用**：`<Figure src="/figures/…" />` 与 `<AudioDemo src="/audio/…" />` 内部调用 VitePress 的 `withBase()`，因此部署到 `/<repo>/` 子路径时也能正确加载；
- **每个音频都对应一个可验证的结论**：纯律 vs 12-TET 的五度/三度/三和弦，以及乐音 vs 噪声。

<Box kind="tip" title="想换自己的图？">

复制 `make_figures.py` 里的任一 `fig_*` 函数，改坐标与数据，再在 `main()` 的字典里注册文件名即可。所有图共用同一套「浅色卡片」样式，浅色和深色主题下都不会糊。

</Box>

::: tip 下一站
代码跑通了，术语可能还没统一。附录 C 是一张中英术语对照表，每条都标注了首次出现的章节，方便你回正文查上下文。
:::
