---
title: "Appendix B · Code and Experiment Environment"
description: "The ten scripts, the shared API, reproduction steps, and one-click deployment."
---

# Appendix B · Code and Experiment Environment

<div class="chapter-meta">
  <span>Estimated 20 minutes</span>
  <span>Prerequisites: able to use a command line</span>
  <span>Code: code/ directory</span>
</div>

This page is the manual for the experimental part and answers three questions:

1. What are these scripts written in, and how do you run them?
2. What exactly does each script output, and which table in the main text corresponds to which part?
3. If I want to add my own experiment, where do I start?

The numbers in the main-text experiments all come from the scripts under `code/`; there are no "illustrative values" and no "roughly like this". If you find a table that does not match the output, the script output wins — it is the only source of fact the experimental numbers recognize.

## B.1 Environment: One Interpreter, Zero Third-Party Dependencies

The experiments use only the Python standard library: `math`, `random`, `itertools`, `statistics`, `heapq`, `unicodedata`, `pathlib`. No numpy, no pandas, no matplotlib. The reason is not "back to basics" but three engineering constraints:

- **Reproducible**: any machine with Python can run them, with no binary wheels to deal with;
- **Pasteable**: the output is plain-text tables that go straight into Markdown, with no screenshots;
- **Auditable**: every number can be traced to a `print` in the source, with no black box in between.

The interpreter version measured in the environment where this book was written:

```text
Python 3.12.14
```

The code uses only syntax from before 3.10 (type annotations, f-strings, `pathlib`) and touches no new features of 3.11 or 3.12, so 3.10 and 3.11 also work. Run it from the **repository root**:

```bash
python code/ch03_consonance.py
```

On Windows, if the output is garbled, set UTF-8 first:

```powershell
$env:PYTHONUTF8='1'
python code\ch03_consonance.py
```

<Box kind="note" title="Why every script is run from the repository root">

The scripts use `sys.path.insert(0, Path(__file__).parent)` to find `common.py` in the same directory, so strictly speaking they can be imported from any directory. But the commands in the main text are uniformly written `python code/xxx.py`, and relative paths in the output are interpreted against the repository root — this is so readers do not have to guess the current directory when copy-pasting.

</Box>

Building the site requires Node.js 20 or later and pnpm 9 or later:

```bash
pnpm install
pnpm build
```

`pnpm build` does three things: render Markdown, check for dead internal links, and write the result to `docs/.vitepress/dist`. Success is the last line `build complete in ...` and exit code 0.

## B.2 Ten Experiment Scripts + Two Asset Generators

One script per chapter, named `chNN_topic.py`. The output line counts are those obtained from an actual run, excluding trailing blank lines; they change when the script is revised. The two `make_*.py` scripts generate the figures and audio used by the web pages and print no tables.

The console labels printed by these Python scripts are in Chinese, but the numbers and structure are unaffected by language: the tables and values are the same in any locale.

| Script | Output lines | Main content |
| --- | --- | --- |
| `ch00_intro.py` | 71 | note name–frequency–cent table, logarithmic perception, 12 pitch-class quantization, common ratios |
| `ch01_vibration.py` | 74 | square-wave Fourier coefficients, partial-sum error, ASCII waveform, autocorrelation |
| `ch02_pitch.py` | 90 | spiral coordinates, interval addition, ratio-complexity ranking, 12-TET coordinates |
| `ch03_consonance.py` | 24 | roughness and consonance of 13 intervals, minima of the 0–1200 ¢ curve |
| `ch04_tuning.py` | 94 | chain of fifths, deviations of three tuning systems, wolf fifth, n-TET error search |
| `ch05_scale_search.py` | 138 | exhaustive search over 792 seven-note sets, three scoring criteria, modes, pentatonic |
| `ch06_harmony.py` | 133 | 12×12 consonance matrix, 220 trichords, T/I, functional transitions |
| `ch07_rhythm.py` | 105 | E(k,n) patterns, 528-case exhaustive search, syncopation, polymeter, Klapp ring |
| `ch08_melody.py` | 194 | transition matrix, entropy and redundancy, held-out test, guessing game, melody generation |
| `ch09_topology.py` | 125 | circle of fifths, dyad counts, 24-key graph, shortest paths, random walk |
| `make_figures.py` | 13 | generate the 11 SVG figures under `docs/public/figures/` (including roughness curves, harmonic comb, rhythm timeline, transition heatmap) |
| `make_audio.py` | 26 | generate the 21 comparison WAVs under `docs/public/audio/` (intervals / chords / cadences / scales / timbre / rhythm / melody) |

<Box kind="experiment" title="Experiment B.1: all ten scripts run">

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

Real output (one measured run; times include interpreter startup):

```text
ch00_intro.py        exit=0  lines= 71   0.08s
ch01_vibration.py    exit=0  lines= 74   0.11s
ch02_pitch.py        exit=0  lines= 90   0.07s
ch03_consonance.py   exit=0  lines= 24   0.08s
ch04_tuning.py       exit=0  lines= 94   0.07s
ch05_scale_search.py exit=0  lines=138   0.12s
ch06_harmony.py      exit=0  lines=133   0.11s
ch07_rhythm.py       exit=0  lines=105   0.07s
ch08_melody.py       exit=0  lines=194   0.06s
ch09_topology.py     exit=0  lines=125   0.07s
```

All ten lines are `exit=0`, totaling 1048 lines of output in under 1 second. The slowest is `ch05_scale_search.py` (0.12 s), because it really does enumerate $2\times\binom{12}{7}=1584$ sets; `ch08_melody.py` is fast because a 48-note corpus only needs matrix statistics.

</Box>

This "lightweight" approach has a price: without numpy, the enumeration in `ch05` needs hand-written loops with `itertools.combinations`; without matplotlib, every "curve" can only be printed as a table or ASCII plot. If you want heavier experiments (say, sweeping 100,000 intervals), copy `common.py` into your own project and add numpy — but that leaves the reproducible scope of this book.

## B.3 `common.py`: The Shared Function API

All scripts share the same physical and perceptual parameters. The shared functions live only in `code/common.py`, and scripts import them through `sys.path`, ensuring that "the same interval gets the same consonance in every chapter".

| Function / constant | Returns | Description | Main chapters |
| --- | --- | --- | --- |
| `cents_of_ratio(ratio)` | float | $1200\log_2(\text{ratio})$ | 0, 2, 4, 5, 8, 9 |
| `ratio_of_cents(cents)` | float | $2^{\text{cents}/1200}$ | 2, 4, 5, 6 |
| `pitch_of_freq(f, f_ref=A4)` | float | frequency → pitch coordinate relative to the reference | 0, 2 |
| `freq_of_pitch(p, f_ref=A4)` | float | pitch coordinate → frequency | 0, 2, 9 |
| `hz_to_cents(f1, f2)` | float | interval between two frequencies | 1, 3 |
| `critical_band(f)` | float | critical bandwidth $\mathrm{CB}(f)$, in Hz | 3, 6 |
| `roughness_kernel(df, bw)` | float | roughness kernel $W$ for a single pair of partials | 3 |
| `dissonance(f1, f2, partials=5)` | float | total roughness $D$ of two tones | 3, 5, 6 |
| `consonance(f1, f2, partials=5)` | float | consonance $S=1/(1+D)$ | 3, 5, 6 |
| `interval_ratios()` | list | just ratio / 12-TET ratio / semitone count for 13 intervals | 2, 4 |
| `tet_ratios(n=12)` | list | frequency ratios of the degrees of n-TET | 2, 4 |
| `pythagorean_major_ratios()` | list | ratios of the 7 degrees of the Pythagorean major scale | 4 |
| `just_major_ratios()` | list | ratios of the 7 degrees of the just major scale | 4 |
| `deviations(ratios)` | list | deviations (in cents) of a set of scale ratios from 12-TET | 4 |
| `A4 = 440.0` | float | reference frequency | whole book |
| `KERNEL_PEAK = 0.25` | float | peak position of the roughness kernel (in CB units) | 3, 6 |
| `PARTIALS = 5` | int | number of harmonics included in the computation | 3, 5, 6 |

Two parameters need special explanation, because they are **not derived** but fitted to listening experiments:

- `KERNEL_PEAK = 0.25`: roughest when the frequency difference is $0.25\,\mathrm{CB}$;
- `PARTIALS = 5`: only the first 5 harmonics are computed. Harmonic amplitudes in the model decay as $1/n$; real instruments may have dozens of partials. This truncation is a deliberate model simplification, not a universally valid sufficient approximation.

<Box kind="pitfall" title="Do not tweak common.py to make the numbers look nice">

These two parameters are **inputs** of the model, effectively postulates. Change them and the consonance, chord rankings, and scale scores in every chapter change, and all the numbers in the main text become invalid. If you really want to study parameter sensitivity, the right move is to copy `common.py` into a new directory and state clearly in an appendix or a new chapter that "this is another model", not to quietly edit the shared file.

</Box>

## B.4 Adding Your Own Experiment

Suppose you want to compute the consonance of a just major third and a perfect fifth, and then observe how it changes with register. The template below fixes the fundamental at 440 Hz first; later you can change the fundamental to compare registers, without modifying any existing script:

1. Create `my_experiment.py` under `code/` (any name, but do not overwrite `ch*.py`);
2. Import the needed functions from `common`;
3. Fix the random seed (if there is randomness);
4. Organize the logic in `main()` and add `if __name__ == "__main__":` at the end;
5. Keep output within 80 columns and avoid ANSI colors;
6. Run it, confirm exit code 0, then paste the **real output** into the main text.

Template (copy as-is; just change the `rows` in the middle):

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

Running `python code/my_experiment.py` gives the real output:

```text
纯律大三度: 386.314 ¢, 协和度 S = 0.9924
纯五度: 701.955 ¢, 协和度 S = 1.0000
```

Note that the fifth shows 1.0000 — what is computed here is the perfect fifth $3:2$, not the 12-TET fifth; $S=0.999999928\ldots$ is only displayed as 1.0000 after rounding, and is not strictly equal to 1. Change the format to `.6f` to see more digits, but 4 decimals is enough in the main text: **precision should match the strength of the claim**.

<Box kind="checkpoint" title="Four questions before submitting a new experiment">

1. Does it depend only on the standard library, and does it run in one command from the repository root?
2. Is the random part seeded? Do two runs produce output identical line by line?
3. Can every number cited in the main text be found on the same line in the output?
4. Does it state the failure boundaries of the model, rather than only reporting good news?

</Box>

## B.5 Reproducibility: Seeds, Floating Point, and Rounding

Of the ten scripts, only four use random numbers, and all of them fix a seed:

| Script | Random source | Seed |
| --- | --- | --- |
| `ch01_vibration.py` | `random.seed(7)` | 7 |
| `ch06_harmony.py` | `random.seed(2024)` | 2024 |
| `ch08_melody.py` | `random.Random(8)` | 8 |
| `ch09_topology.py` | `random.Random(9)` | 9 |

The other six scripts are purely deterministic: given the input, the output is bit-for-bit identical. `ch01` and `ch06` use the global `random` and reset the seed explicitly, while `ch08` and `ch09` use independent `Random` instances; each is reproducible when run separately from the command line, but if you call the first two repeatedly in the same process, mind the global random state.

Three rules of thumb for floating point:

- On the same machine and the same Python version, the output is bit-for-bit identical;
- Across platforms (Windows / Linux) the last digit may differ, but `.3f` and `.4f` formatting hides the difference;
- To compare two floats, do not use `==`; use `abs(a-b) < 1e-9`. Chapter 2 does exactly this when verifying interval addition, with an error bound of $1.14\times10^{-13}$.

Chinese alignment relies on `unicodedata.east_asian_width`: full-width characters count as 2 columns, half-width as 1. That is why the scripts have a small `pad()` or `width()` function instead of plain `f"{name:<10}"` — the latter would misalign Chinese headers.

<Box kind="pitfall" title="Output line count is not “information content”">

`ch08_melody.py` produces 193 lines of output, `ch03_consonance.py` only 24; this does not mean the former is more important. The line count only reflects how many tables were printed; the real information content is in the conclusion each line carries. When reading a script, look at the headers first, then the numbers, and finally the "key numbers" summary at the end of the script.

</Box>

There is also a statistical reproducibility issue: with few samples, entropy is underestimated. The 48 notes of `ch08` cover only 17 second-order contexts (out of 49), so the second-order model looks "very low entropy" when in fact too many situations are unseen. The main text uses a held-out test (train on the first 6 bars, predict the last 6) to expose this problem, rather than treating training-set entropy as a conclusion.

## B.6 From Script to Web Page: Build and Deployment

Local build:

```bash
pnpm build
```

On success the last line is similar to:

```text
build complete in 21.03s
```

The build checks all internal links. There is only one link rule: **use clean URLs, no `.md`**. For example, at the end of Chapter 6 the English page writes `/en/chapters/07-rhythm`, not `/en/chapters/07-rhythm.md`. A mistake fails the build immediately instead of producing a 404 after launch.

Deployment to GitHub Pages is "configure once, automatic afterwards":

- `.github/workflows/deploy.yml` in the repository triggers on a push to `main`;
- The workflow derives `BASE_PATH` from the repository name (a project site looks like `/<repo>/`), then runs `pnpm build`;
- The build artifact `docs/.vitepress/dist` is uploaded by `actions/upload-pages-artifact` and published by `actions/deploy-pages`;
- For the first deployment, just set Source to **GitHub Actions** under the repository's **Settings → Pages**.

For local preview use `pnpm dev`, default address `http://localhost:5173`. The only difference between preview and production is `base`: production carries the `/<repo>/` prefix, so internal links must be absolute paths starting with `/`, never relative paths.

<Box kind="pitfall" title="The three most common build failures">

1. **Dead link**: the link has a `.md` suffix, or is one level short. The build log gives the source file and the target path.
2. **Angle brackets in math**: $x \lt 1$ must be written `\lt`. Writing `<` directly may be parsed by Vue as the start of an HTML tag.
3. **Vertical bars in tables**: absolute values in cells must be written `\lvert x \rvert`; a bare `|` is treated as a column separator.

</Box>

## B.7 Figures and Listening Examples: The Two Asset Generators

The figures and audio in the book are not binary files placed in the repository by hand; they are script outputs — change one parameter, rerun once, and all the figures and audio in the book update together:

```bash
python code/make_figures.py   # docs/public/figures/*.svg（11 张）
python code/make_audio.py     # docs/public/audio/*.wav（21 个）
```

Design constraints:

- **Figures are SVG**: vector, diffable, versionable, assembled from string templates, with no matplotlib;
- **Audio is WAV**: 22050 Hz / 16 bit / mono, total duration from 1.8 s to 10 s, about 2.5 MB in total;
- **Pages reference them through components**: `<Figure src="/figures/…" />` and `<AudioDemo src="/audio/…" />` call VitePress's `withBase()` internally, so they load correctly under the `/<repo>/` subpath;
- **Every audio clip corresponds to a checkable conclusion**:
  - intervals: fifth, major third, and tritone, each just vs 12-TET;
  - chords and cadences: C major triad, just and equal-tempered versions of C–F–G–C;
  - scales: C major in just intonation and in equal temperament;
  - timbre: two harmonic envelopes with fast and slow decay;
  - rhythm: E(3,8), E(5,8), E(5,13) and 3:4 polymeter;
  - melody: generated by the Markov chain of Chapter 8 with a fixed seed.
- **Interactive listening**: `<ConsonanceExplorer />` in Chapter 3 synthesizes the current interval directly with Web Audio; `<EuclideanRhythmLab />` in Chapter 7 lets you drag k, n, and tempo and listen to two bars, with no extra audio files.

<Box kind="note" title="Want your own figures?">

Copy any `fig_*` function in `make_figures.py`, change the coordinates and data, and register the file name in the dictionary in `main()`. All figures share the same "light card" style, so they stay legible in both light and dark themes.

</Box>

::: tip Next Stop
The code runs, but the terminology may not be unified yet. Appendix C is the glossary and notation reference, with each term given in English and Chinese and a note of the chapter where it first appears, so you can go back to the main text for context.
:::
