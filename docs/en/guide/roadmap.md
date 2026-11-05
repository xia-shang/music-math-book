# Study Roadmap

## Chapter Dependencies

```
                    ┌────────────────────────┐
                    │  Ch. 0  Introduction   │
                    └────────────┬───────────┘
                                 │ mathematical tools
                    ┌────────────┴──────────────────────────┐
                    ▼                                       ▼
       ┌────────────────────────┐              ┌────────────────────────┐
       │  Ch. 1  Vibration      │              │  Ch. 2  Pitch          │
       └────────────┬───────────┘              └────────────┬───────────┘
                    │ spectrum / overtones                  │ log coordinates
                    ▼                                       ▼
             ┌────────────────────────────────────────────────────┐
             │  Ch. 3  Consonance (the hinge of the book)         │
             └──────┬─────────────────────────────────────────────┘
                    │ roughness function
                    ▼
       ┌────────────────────────┐              ┌────────────────────────┐
       │  Ch. 4  Tuning         │──▶           │  Ch. 5  Scales         │
       └────────────┬───────────┘              └────────────┬───────────┘
                    │ pitch-class sets                      │ pitch-class sets
                    ▼                                       ▼
       ┌────────────────────────┐              ┌────────────────────────┐
       │  Ch. 6  Harmony        │              │  Ch. 9  Topology       │
       └────────────────────────┘              └────────────────────────┘

      Ch. 5, 6 ──▶ Ch. 7  Rhythm ──▶ Ch. 8  Melody
                      (Ch. 8 also needs Ch. 0 and 2)
```

The figure shows only the main dependencies; for exact prerequisites, see the start of each chapter. Chapter 7 builds on the discrete-set and probabilistic viewpoint of Chapters 5 and 6; Chapter 8 needs Chapters 0 and 2 in addition to Chapter 7, so it is not an independent branch that opens up from the introduction alone.

## Three Recommended Paths

### Path A: A 3-Day Fast Read (for engineers short on time)

| Slot | Content | Goal |
| --- | --- | --- |
| Day 1 | Ch. 0 + Ch. 1 + Ch. 2 | build the cent coordinate; compute intervals with `1200·log2` |
| Day 2 | Ch. 3 | write the roughness function and explain "why the fifth is consonant" |
| Day 3 | Ch. 4 + Ch. 5 | hand-compute the errors of three tuning systems; explain the victory of 12-TET |

### Path B: A Full Close Read (for those who want to rebuild their worldview)

Read in the order 0 → 9 and do the "runnable experiment" in every chapter. For Chapter 6, keep the linear-algebra quick reference in Appendix A.4 at hand; before Chapter 8, read the probability and information-theory intuition in Appendix A.6.

### Path C: Engineering Implementation (for hands-on people)

1. Run every script under `code/` once to build "number intuition";
2. Go back to Chapters 3 and 4 and modify `roughness_kernel` in `common.py` to try different kernel functions;
3. Use the basis-vector idea of Chapter 6 to write a chord recognizer;
4. Use the Markov chain of Chapter 8 to generate an 8-bar melody and check whether it falls into the short loops analyzed in the body; to listen to it, hook up your own synthesis tool.

## Self-Check List for Each Chapter

After finishing a chapter, close the book and ask yourself four questions:

1. What physical quantity defines the core object introduced in this chapter?
2. Which postulate does it depend on? If that postulate were overturned, how would the conclusions change?
3. Which line of code verifies the chapter's most important conclusion?
4. Can I explain it to a non-scientist in one sentence?

If you can answer all four, move on.
