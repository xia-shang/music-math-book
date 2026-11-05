---
title: "Appendix D · Further Reading"
description: "A bibliographic map of 15 books and papers: which question of this book each one answers."
---

# Appendix D · Further Reading

<div class="chapter-meta">
  <span>Estimated 25 minutes</span>
  <span>Prerequisite: any of Chapters 3, 4, 6, 8, 9 read</span>
  <span>Use: from popular science to the literature</span>
</div>

This book deliberately writes every chapter as a closed loop: definitions, postulates, theorems, experiments, limits. But the other side of a closed loop is a narrow field of view. The real literature on acoustics, psychoacoustics, and music theory is much thicker and much noisier: the same consonance curve can peak in different places under different experimental conditions, and the same "Euclidean rhythm" comes with different index conventions from different authors. This page lists 15 books and papers we think are worth reading, organized by "which question of this book it can answer" rather than by publication year.

Three selection criteria:

1. **It answers a specific question**, not "this field is important";
2. **It has testable data, formulas, or code** — you can verify something after reading;
3. **It lies outside the model boundaries of this book**: it either gives a more precise model or a counterexample.

Bestsellers that fail these three tests are not listed here.

## D.1 Auditory Perception and Consonance: Turning "Pleasant" into an Experiment

### 1. Helmholtz, *On the Sensations of Tone*

Hermann von Helmholtz, *On the Sensations of Tone as a Physiological Basis for the Theory of Music*, English translation by A. J. Ellis, 1885 (original 1863). [Full text at archive.org](https://archive.org/details/onsensationofto00helm)

This is the first book to drag consonance out of aesthetic speculation and into the laboratory. It uses harmonics, beats, and cochlear physiology to explain why simple integer ratios sound stable; the "harmonic coincidence" line of thought in Chapter 3 descends directly from it. Read it with a historical eye: Helmholtz's era had no concept of the critical band, and many of his judgments about dissonance are qualitative descriptions rather than today's quantitative curves. Its value lies in the questions it raises, not in specific numbers.

### 2. Plomp & Levelt (1965), "Tonal Consonance and Critical Bandwidth"

Reinier Plomp & Willem J. M. Levelt, "Tonal consonance and critical bandwidth", *Journal of the Acoustical Society of America* 38(4), 548–560. [DOI](https://doi.org/10.1121/1.1909741)

This paper is the ancestor of the roughness kernel in Chapter 3. It ran listening experiments with pure-tone pairs, plotted a "frequency difference–dissonance" curve, and found that the curve's peak falls near a fixed fraction of the critical bandwidth — the book's $0.25\,\mathrm{CB}$ is a parameterization of that curve. Two things to get straight when reading it: the stimuli were **pure tones**, not instrument tones; and the curve is **average perception**, with individual differences averaged out. The five-harmonic model of Chapter 3 is a generalization built on top of these two facts, not a reproduction of the paper.

### 3. Zwicker & Fastl, *Psychoacoustics: Facts and Models*

Eberhard Zwicker & Hugo Fastl, *Psychoacoustics: Facts and Models*, 3rd ed., Springer, 2007. [DOI](https://doi.org/10.1007/978-3-540-68888-4)

If you read only one psychoacoustics textbook, make it this one. It systematically covers masking, critical bands, pitch, loudness, and roughness, with experimental data in every chapter. Postulate 3.1 of this book, $\mathrm{CB}(f)\approx 94+71.3(f/\text{kHz})^{0.69}$, comes from this tradition; the textbook will tell you that this fit degrades below 100 Hz and cannot be extrapolated above 5 kHz either. Read it with the formulas of Chapter 3 at hand: which parameters are measured, and which we chose for coding convenience.

### 4. Terhardt (1974), "Pitch, Consonance, and Harmony"

Ernst Terhardt, "Pitch, consonance, and harmony", *JASA* 55(5), 1061–1069. [DOI](https://doi.org/10.1121/1.1914648)

This paper deserves a read by anyone who infers "consonance = pleasant". It separates **psychoacoustic consonance** (absence of roughness) from the **musical sense of an interval** (virtual pitch), and argues that the former cannot explain the latter on its own. Chapter 2 writes pitch as a log coordinate and Chapter 3 writes consonance as a roughness function; to Terhardt these are two different mechanisms. Reading it will not overturn the book's formulas, but it will remind you: the formula computes "not harsh", not "meaningful".

### 5. Sethares, *Tuning, Timbre, Spectrum, Scale*

William A. Sethares, *Tuning, Timbre, Spectrum, Scale*, 2nd ed., Springer, 2005. [DOI](https://doi.org/10.1007/978-1-4471-4177-8)

The book's central claim is sharp: **how "natural" a scale sounds depends on timbre**. The same roughness model, given a different harmonic envelope, yields a different "best scale". Chapters 3 and 4 fix timbre at a $1/i$ decay so that the examples stay computable; Sethares treats timbre as a variable and shows the other side of the model. The book ships downloadable code and audio, suited to readers who want to change parameters and listen to the result.

## D.2 Tuning, Scales, and Rhythm: Number Theory Enters Music

### 6. Benson, *Music: A Mathematical Offering*

David J. Benson, *Music: A Mathematical Offering*, Cambridge University Press, 2006. [Free PDF on the author's homepage](https://homepages.abdn.ac.uk/d.j.benson/pages/html/music.pdf)

This is a book written by a mathematics department for music departments and for mathematics departments, and its coverage is enormous: Fourier, tuning, scales, rhythm, symmetry, group theory, and even accompanying audio files. Its tuning chapter is far more detailed than Chapter 4 of this book, and its treatment of continued fractions and approximation is more complete. The advantages: free, many examples, runnable code. The drawback: reading it cover to cover will get you lost, so pick the chapters that match this book's order.

### 7. Toussaint, *The Geometry of Musical Rhythm*

Godfried T. Toussaint, *The Geometry of Musical Rhythm: What Makes a "Good" Rhythm Good?*, CRC Press, 2013. [DOI](https://doi.org/10.1201/b13751)

Much of the Euclidean rhythm, Klapp ring, and "evenness" discussion in Chapter 7 comes from Toussaint's survey. The book draws rhythms from around the world as clock diagrams and polygons and compares them with geometric quantities (area, perimeter, symmetry). The biggest takeaway is **decentering**: you will see that European classical rhythm is just one of many "good rhythms", not the standard answer.

### 8. Demaine et al. (2009), "The Distance Geometry of Music"

Erik D. Demaine, Francisco Gomez-Martin, Henk Meijer, et al., "The distance geometry of music", *Computational Geometry: Theory and Applications* 42(5), 429–454. [DOI](https://doi.org/10.1016/j.comgeo.2008.04.005)

This paper puts Euclidean rhythms into the framework of computational geometry: it proves that such rhythms are equivalent to "placing $n$ points as evenly as possible on a circle", and gives several distance properties. Theorem 7.1 in Chapter 7 proves only that "the gaps differ by 1"; this paper shows that there is stronger structure. It is also a good example of music problems feeding back into mathematics: the evenness of rhythms helped understand distance computations in polygons.

### 9. Loy, *Musimathics*, Vol. 1

Gareth Loy, *Musimathics: The Mathematical Foundations of Music*, Vol. 1, MIT Press, 2006. [MIT Press](https://mitpress.mit.edu/9780262122824/musimathics/)

This book leans engineering: sampling, quantization, convolution, filters, timbre synthesis — signal processing built up step by step. When Chapter 1 discusses Fourier and harmonics, if you want to know "how a real synthesizer computes a note", Loy is the right next stop. It does not aim for minimalism; formulas and code carry equal weight. You can skip the filter-design chapters unrelated to this book.

## D.3 Harmony and Geometry: Chords Are Points in a High-Dimensional Space

### 10. Tymoczko, *A Geometry of Music*

Dmitri Tymoczko, *A Geometry of Music: Harmony and Counterpoint in the Extended Common Practice*, Oxford University Press, 2011. [Oxford University Press](https://global.oup.com/academic/product/a-geometry-of-music-9780195335279)

This book translates "chord progression" into motion in a high-dimensional space: chords are points, voice leading is a path, modulation is a change of coordinates. The indicator vectors of Chapter 6 and the torus of Chapter 9 are its discrete toy versions. Tymoczko's ambition is to put traditional harmony, jazz, and 20th-century music into one geometric framework; reading it will change how you understand rules such as "why parallel fifths are bad" — they stop being prohibitions and become certain paths in a space.

### 11. Callender, Quinn & Tymoczko (2008), "Generalized Voice-Leading Spaces"

Clifton Callender, Ian Quinn & Dmitri Tymoczko, "Generalized voice-leading spaces", *Science* 320(5874), 346–348. [DOI](https://doi.org/10.1126/science.1153021)

This short paper provides a more general spatial background for the voice-leading distance of Chapter 6 and the path perspective of Chapter 9: it studies relations among different voice-leading distances and the musical spaces built from them. Note the difference in models: the tonal graph in this book has only 24 nodes and hand-set edge weights, while the paper focuses on distances defined by voice movement and on quotient spaces, not shortest paths on this graph. The two can inspire each other, but the paper's theorems cannot be carried over to the 24-node graph directly.

### 12. Huron, *Sweet Anticipation*

David Huron, *Sweet Anticipation: Music and the Psychology of Expectation*, MIT Press, 2006. [MIT Press](https://mitpress.mit.edu/9780262582780/sweet-anticipation/)

Chapter 8 says "good melody is unexpected yet reasonable"; Huron expands that sentence into a whole psychology: expectation comes from statistical learning, surprise produces emotion, and violating expectation has a cognitive cost. His framework is broader than the book's Markov chains: it also considers melodic contour, rhythm, cultural training, and emotion. Reading it connects "entropy" to "why people feel excited before a chorus", and warns you not to treat $H$ as a "pleasantness" score.

## D.4 Statistics and Information Theory: From Entropy to Generation

### 13. Shannon (1948), "A Mathematical Theory of Communication"

Claude E. Shannon, "A mathematical theory of communication", *Bell System Technical Journal* 27(3), 379–423. [DOI](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x)

The source of every formula in Chapter 8. Shannon defined entropy, joint entropy, conditional entropy, redundancy, and channel capacity, and explained why "average information" is logarithmic. The benefit of reading the original is seeing the dependency order among definitions: a probability distribution comes first, then entropy; a joint distribution comes first, then conditional entropy. Many examples in the original are codes and English text, not music — which is exactly why the tool is general.

### 14. Temperley, *The Cognition of Basic Musical Structures*

David Temperley, *The Cognition of Basic Musical Structures*, MIT Press, 2001. [MIT Press](https://mitpress.mit.edu/9780262700948/the-cognition-of-basic-musical-structures/)

Temperley models how listeners infer meter, key, and chords with "preference rules"; his method complements the book's statistical models: he cares more about "which rules listeners use to make judgments", while the book cares more about "how much predictability the data contains". The words "function" and "tonal center" in Chapters 6 and 8 are, in his framework, a set of computable preference scores. To move from "statistical description" to "cognitive explanation", this is the natural next book.

### 15. Manning & Schütze, *Foundations of Statistical Natural Language Processing*

Christopher D. Manning & Hinrich Schütze, *Foundations of Statistical Natural Language Processing*, MIT Press, 1999. [MIT Press](https://mitpress.mit.edu/9780262133609/foundations-of-statistical-natural-language-processing/)

Don't be fooled by the title: Markov chains, maximum likelihood estimation, smoothing, held-out testing, and cross-entropy — everything used in Chapters 6 and 8 is explained here in a standard, clear way. Its examples are word sequences, but the mathematical structure is isomorphic to note sequences. The sparsity problem mentioned in Chapter 8 — "a second-order context covers only 17/49" — is called data sparsity in language modeling, and its remedies (backoff, interpolation, smoothing) can be borrowed directly.

## D.5 Five Reading Routes

You do not have to read the list from cover to cover. Pick a route by the problem in front of you:

| The problem you want to solve | Suggested order | Time budget |
| --- | --- | --- |
| How consonance is actually computed, and where the model fails | 1 → 2 → 3 → 4 → 5 | 2–3 weeks |
| Why 12 notes, and how other tuning systems are designed | 6 → 5 → 8 | 2 weeks |
| Can chord progressions and modulation become geometry? | 10 → 11 → 6 | 3 weeks |
| Melodic statistics, entropy, and generation | 13 → 15 → 12 → 14 | 3 weeks |
| The mathematical structure of rhythm and world music | 7 → 8 → 6 | 2 weeks |

The time estimates assume 1 hour per day with notes. If you are only looking up one question, read the abstract, figures, and conclusion; there is no need to derive the formulas from scratch.

## D.6 How to Read a Paper

The literature is not meant to be "finished"; it is meant to answer questions. We suggest a three-pass method:

- **First pass (20 minutes)**: read the title, abstract, figures, and conclusion. Answer only one question: is it relevant to my problem? If not, stop.
- **Second pass (1–2 hours)**: look at the methods and parameters. What were the stimuli? How large was the sample? How was the critical bandwidth estimated? Under what conditions does the conclusion hold?
- **Third pass (half a day or more)**: reproduce one figure or one number. Failing to reproduce is not a disaster — it usually means you have found a parameter the original did not state clearly.

Taking Plomp & Levelt as an example, the second pass should at least ask:

1. Were the stimuli pure tones or complex tones? What were the frequencies and sound pressure levels?
2. Was "dissonance" a listener rating or a paired comparison? How was the scale normalized?
3. Where is the curve's peak in frequency difference? What is the ratio of that difference to the critical bandwidth?
4. Is the conclusion robust across register, loudness, and individual differences?
5. How far is the book's $0.25\,\mathrm{CB}$ from the paper's peak position? Would that difference change the rankings in Chapter 3?

<Box kind="checkpoint" title="Post-Reading Exercise: Fold a Paper into One Card">

Pick any paper above and answer five questions in 200 words:

1. What problem does it solve? (one sentence)
2. What method does it use? (experiment / proof / simulation)
3. What is the key number or theorem? (one)
4. Under what conditions does its conclusion fail? (one)
5. Which formula in which chapter of this book does it connect to directly? (give the chapter number and symbol)

If you cannot write item 4, you have read only the abstract; if you cannot write item 5, you have not yet connected the literature back to your own knowledge structure.

</Box>

## D.7 Citation Ethics and the Limits of Models

<Box kind="pitfall" title="Do Not Treat a Reference as an Endorsement">

Citing a paper only says "this claim has a source"; it does not say "this claim also holds under the conditions of this book". Three common misuses:

- **Condition drift**: the Plomp–Levelt curve comes from pure tones, but this book uses it to score instrument tones with five harmonics; the parameters can be borrowed, the conclusions cannot be transplanted directly.
- **Number worship**: Zwicker's $\mathrm{CB}$ formula is a fit, and its error is obvious below 100 Hz; the number you get by substituting into $94+71.3(f/\text{kHz})^{0.69}$ at 50 Hz should not be treated as experimental fact.
- **Anachronism**: Helmholtz had none of the experimental tools of modern psychoacoustics, and many of his judgments are insights rather than data; when citing him, mark that this is a historical source.

The correct posture is: **state your own model and conditions first, then say under which conditions the literature supports it and under which it does not**. That is harder than listing ten more references, and more useful.

</Box>

## D.8 Closing

The 15 references on this page form a map of "life after this book": to the left are more precise physical and physiological models (Helmholtz, Plomp–Levelt, Zwicker, Terhardt, Sethares); to the right are more abstract structures (Tymoczko, Callender et al., Benson, Toussaint); downward are more engineered implementations (Loy, Manning–Schütze); upward are more psychological explanations (Huron, Temperley). You do not need to read them all; you need to know which direction to walk when a problem appears.

One honest reminder at the end: every number in this book comes from the scripts under `code/`, and every model has its limits marked in the body. The literature can extend those limits, but it will not decide for you "which model fits your problem better". That decision is still yours.

::: tip Next chapter
With the literature read, it is time to do the problems. Appendix E collects hints and numerical answers for two problems per chapter, Chapters 0–9, arranged by chapter — [Appendix E · Exercises and Answers](/en/appendix/e-exercises).
:::
