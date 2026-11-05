# TRANSLATION.md — English edition brief

## Identity

- Book title: **Music as Mathematical Logic**
- Subtitle: *An Axiomatic Theory of Music from Vibration to Structure*
- Site name: **Music as Math**
- Tagline: "Don't memorize the staff. Write the differential equation first."
- Edition: Programmer's Edition · v1.1.0

## Rules

1. **Full translation, not a summary.** Preserve every section, subsection, list, table, theorem/proof, experiment, exercise and tip.
2. **Keep all math and code exactly as in the Chinese source** — `$...$`, `$$...$$`, code fences, command names, file names, numbers and identifiers.
3. Keep Vue components and HTML wrappers; translate only their visible text:
   - `<Box kind="..." title="...">`: translate `title`; body prose translated. Do not change `kind`.
   - `<Figure src="..." caption="...">`: keep `src`, translate `caption`.
   - `<AudioDemo src="..." title="..." hint="...">`: keep `src`, translate `title` and `hint`.
   - Keep `<div class="chapter-meta">` and translate the three pills.
4. **Internal links must point to the English edition**: `/en/chapters/…`, `/en/appendix/…`, `/en/guide/…`, `/en/releases`. Asset links `/figures/...` and `/audio/...` stay unchanged.
5. Frontmatter: translate `title` and `description`; keep the `---` block.
6. Code blocks and their printed output stay unchanged. Add no apology inside every exercise; a single note in Appendix B (already planned) explains that console labels are Chinese while numbers are language-independent. If an experiment's raw output is visibly Chinese, add one short English sentence before the details block: “The script prints its labels in Chinese; the numbers are unchanged.” Do not translate inside the code fence.
7. Tone: precise, dry, engineer-to-engineer; avoid marketing language. Use American spelling.
8. Do **not** edit Chinese files, config, components, scripts or assets. Do not run the site build or push.
9. Markdown style: keep tables, blank lines around components, and `::: tip` blocks. Translate the tip text.
10. Write files under `docs/en/` exactly at the target paths given by the Lead.

## Terminology

| 中文 | English |
| --- | --- |
| 音高 | pitch |
| 音级 | pitch class |
| 音程 | interval |
| 频率比 | frequency ratio |
| 纯律 | just intonation |
| 五度相生律 | Pythagorean tuning |
| 十二平均律 / 12-TET | 12-tone equal temperament (12-TET) |
| 律制 | tuning system |
| 毕达哥拉斯音差 | Pythagorean comma |
| 狼五度 | wolf fifth |
| 临界带宽 | critical bandwidth |
| 粗糙度 | roughness |
| 协和 / 不协和 | consonance / dissonance |
| 拍频 | beat frequency |
| 基频 / 基波 | fundamental frequency / fundamental |
| 谐波 | harmonic |
| 分音 / 泛音 | partial / overtone |
| 频谱 | spectrum |
| 包络 | envelope |
| 音色 | timbre |
| 八度等价 | octave equivalence |
| 音阶 | scale |
| 主音 | tonic |
| 下属 / 属 | subdominant / dominant |
| 终止式 | cadence |
| 声部进行 | voice leading |
| 音级集合 | pitch-class set |
| 五度圈 | circle of fifths |
| 马尔可夫链 | Markov chain |
| 熵 / 冗余度 / 惊讶度 | entropy / redundancy / surprise |
| 欧几里得节奏 | Euclidean rhythm |
| 复合节奏 | polymeter |
| 克拉普环 | Klapp ring |
| 莫比乌斯带 / 克莱因瓶 | Möbius strip / Klein bottle |
| 商空间 / 环面 | quotient space / torus |
| 公设 / 定理 / 证明 | postulate / theorem / proof |
| 可运行实验 | runnable experiment |
| 自检 | self-check |
| 常见误解 | common misconception |

## Chapter titles

| No. | English title |
| --- | --- |
| 0 | Introduction: Music as the Interface of Physics and Psychology |
| 1 | The Mathematics of Vibration: Where Sound Begins |
| 2 | The Physics and Geometry of Pitch |
| 3 | Consonance and Dissonance: A Physical Account |
| 4 | Tuning Systems as an Optimization Problem |
| 5 | Algorithms for Generating Scales |
| 6 | Harmony as Linear Algebra |
| 7 | Rhythm: Fractals and Chaos |
| 8 | Melody: Statistics and Information Theory |
| 9 | Tonality and Atonality: A Topology |

Appendices: A Mathematical Toolkit · B Code and Experiment Environment · C Glossary and Notation · D Further Reading · E Exercises and Answers.
