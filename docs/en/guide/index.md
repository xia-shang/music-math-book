# How to Use This Book

> This book does not require you to be a musician first. It only asks that you be willing to translate "how it sounds" into "how it computes".

## Three Reading Paths

| Path | Who it suits | Order | Duration |
| --- | --- | --- | --- |
| **Fast read** (3 days) | programmers who only want to understand "consonance and tuning" | 0 → 1 → 2 → 3 → 4 → 5 | 1–2 hours per day |
| **Close read** (6 weeks) | science students who want to build the full axiomatic intuition | Chapters 0–9 plus Appendices A/B | 1 hour per day |
| **Engineering** (learn by doing) | people who want to turn the conclusions into tools | do every "runnable experiment", then reread the body | open-ended |

All three paths must pass through Chapter 2. Without logarithmic coordinates, everything that follows turns into new rote memorization.

## The Structure of Each Chapter

Every chapter follows the same template, so that you can jump around:

1. **Opening questions** — 3 to 5 "whys" that the chapter must be able to answer by its end;
2. **Definitions / postulates** — introduce the new objects, state which quantities define them and where their limits lie;
3. **Theorems and derivations** — start from the postulates, give verifiable conclusions, with proof sketches where needed;
4. **Runnable experiment** — a Python script that turns formulas into numbers in the terminal;
5. **Summary and exercises** — close with one paragraph, and check with a set of exercises whether you really understood it.

<Box kind="note" title="An Honest Note on Theorems">

The "theorems" in this book are conclusions derived from our own models, not laws of nature. Models can be falsified, and that is exactly what makes them more useful than "my music theory teacher said so". Any assumption that rests on psychoacoustic experimental data is marked as a **postulate** (for example, the approximation formula for critical bandwidth).

</Box>

## How to Run the Code

The repository root contains a `code/` folder, and every experiment script depends only on the Python standard library. After cloning the book's repository or your own fork, run from the repository root:

```bash
python code/ch03_consonance.py      # 协和度曲线
python code/ch04_tuning.py          # 三种律制偏差表
python code/ch05_scale_search.py    # 从泛音列搜索最优音阶
```

Every script prints in the same "table + one-line conclusion" format, which you can paste straight into your notes. To plot the curves, read the data with the template in Appendix B.4 and draw it with whatever plotting tool you have at hand; the book's own scripts do not depend on any plotting library.

## The Book's Tech Stack

This book is itself a reproducible piece of experimental equipment:

- **VitePress** static site (Markdown + Vue 3), with formulas rendered by MathJax;
- **GitHub Actions** for automated builds, **GitHub Pages** for hosting;
- **Python 3.12** to verify every numerical conclusion;
- interactive demos are pure Vue components, with no third-party chart library.

In other words: every curve and every number you see can be traced to code in the repository.

<Box kind="checkpoint" title="After Reading">

You should be able to answer on your own: why 12-TET is not the smallest-error system yet is still convenient for transposition; why the same interval has different roughness in different registers; and why a second-order Markov model can actually perform worse on small samples.

</Box>
