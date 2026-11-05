---
layout: home

hero:
  name: Music as Math
  text: An Axiomatic Theory of Music
  tagline: Don't memorize the staff. Write the differential equation first. Physics, mathematics and code turn "it sounds right" into "it can be computed".
  image:
    src: /logo.svg
    alt: Music as Math
  actions:
    - theme: brand
      text: Start reading
      link: /en/guide/
    - theme: alt
      text: Chapters
      link: /en/chapters/00-introduction
    - theme: alt
      text: About
      link: /en/about

features:
  - icon: 🌊
    title: Physics first
    details: Every concept starts from a measurable quantity — frequency, period, amplitude, spectrum — not from "the teacher says play it this way".
  - icon: ∑
    title: Mathematical modelling
    details: Pitch is a logarithmic coordinate, chord consonance is a quadratic form, tuning is a constrained optimization problem.
  - icon: 🐍
    title: Runnable code
    details: Each chapter ships a Python script. Every key number can be recomputed in your terminal, including "which interval is most consonant".
  - icon: 🧱
    title: Axiomatic structure
    details: "Definition → postulate → theorem → corollary. Read music theory the way you read an RFC: every claim has antecedents."
  - icon: 🎛
    title: Interactive
    details: Drag a slider to watch roughness, beating and tuning deviations change; generate Euclidean rhythms from k and n and hear them.
  - icon: 🎧
    title: Listenable
    details: 21 programmatically generated WAV files — intervals, scales, cadences, rhythms and a Markov melody. Verify conclusions with your ears.
  - icon: 🚀
    title: One-click deploy
    details: VitePress + GitHub Actions + Pages. Once Pages is enabled, every push to main rebuilds and deploys.
---

<ClientOnly>

<div class="mm-banner">pitch   f  ──▶  p = 1200·log₂(f/f₀)      [cents]
roughness D(f₁,f₂) = Σᵢ Σⱼ (aᵢaⱼ) · W(Δf / (0.25·CB))    [model]
tuning    min Σ |1200·log₂(2^(k/n)) − 1200·log₂(qₖ)|²  [optimization]
harmony   𝕍 = span{ v_T, v_S, v_D }                [state space]</div>

</ClientOnly>

<div class="mm-version">v1.1.0 · English / 中文 (switch in the top-right) · <a href="./releases">Release notes</a></div>

## What this book does

Traditional theory starts with symbols: learn the clef, memorise chord tables, then judge consonance by feel. That works for some musicians; for anyone who prefers derivations, it is torture.

This book reverses the order: **phenomenon → model → perception → system**. First ask what happens when two tones sound together (Chapter 3), then why the ear judges some combinations consonant (critical bands), and finally how 12-TET trades audible error for freedom of transposition (Chapter 4). Every conclusion is written as a definition, postulate or theorem, and every key number can be reproduced with the bundled Python scripts.

## Chapter map

<div class="mm-grid">
  <a href="./chapters/00-introduction">
    <span class="no">CH.00</span>
    <span class="title">Introduction: Music as Interface</span>
    <span class="desc">Pattern recognition, axiomatic method, intuitions for logs and Fourier.</span>
  </a>
  <a href="./chapters/01-vibration">
    <span class="no">CH.01</span>
    <span class="title">The Mathematics of Vibration</span>
    <span class="desc">Simple harmonic motion, Fourier series, where timbre comes from.</span>
  </a>
  <a href="./chapters/02-pitch">
    <span class="no">CH.02</span>
    <span class="title">The Physics and Geometry of Pitch</span>
    <span class="desc">Weber–Fechner, octave equivalence, the pitch spiral.</span>
  </a>
  <a href="./chapters/03-consonance">
    <span class="no">CH.03</span>
    <span class="title">Consonance and Dissonance</span>
    <span class="desc">Beating, critical bands, and a computable consonance function.</span>
  </a>
  <a href="./chapters/04-tuning">
    <span class="no">CH.04</span>
    <span class="title">Tuning as Optimization</span>
    <span class="desc">The Pythagorean predicament, just intonation, the engineering win of 12-TET.</span>
  </a>
  <a href="./chapters/05-scales">
    <span class="no">CH.05</span>
    <span class="title">Algorithms for Scales</span>
    <span class="desc">Brute-force 7-note subsets of 12, and the privilege of the pentatonic.</span>
  </a>
  <a href="./chapters/06-harmony">
    <span class="no">CH.06</span>
    <span class="title">Harmony as Linear Algebra</span>
    <span class="desc">Pitch-class sets, basis vectors, T–S–D–T dynamics in a state space.</span>
  </a>
  <a href="./chapters/07-rhythm">
    <span class="no">CH.07</span>
    <span class="title">Rhythm: Fractals and Chaos</span>
    <span class="desc">Euclidean algorithms, syncopation statistics, coprime polymeter.</span>
  </a>
  <a href="./chapters/08-melody">
    <span class="no">CH.08</span>
    <span class="title">Melody: Statistics and Information</span>
    <span class="desc">Markov chains, entropy, and "surprising yet inevitable".</span>
  </a>
  <a href="./chapters/09-topology">
    <span class="no">CH.09</span>
    <span class="title">Tonality and Atonality: A Topology</span>
    <span class="desc">Circle-of-fifths geometry, modulation paths, atonal random walks.</span>
  </a>
</div>

## Who it is for

- Science students who know a little calculus and linear algebra but close the page at the sight of a staff;
- Programmers who want to know what actually happens behind `f = 440 × 2^(n/12)`;
- Theory teachers who want an explanation they can compute in front of a class;
- Anyone who believes "it sounds good" should not be a reason-free statement.

## How to read

Each chapter opens with **questions**, develops formal **definitions / postulates / theorems**, and ends with **runnable experiments** and **exercises**. If a formula looks opaque, run the code first: `python code/ch03_consonance.py`. The numbers will tell you what the formula is doing.

<Box kind="note" title="Prerequisites">

You do not need to play an instrument, but you should be comfortable with derivatives and compound interest. Chapters 0–1 use a little integration (for Fourier coefficients), Chapter 6 uses a little linear algebra (bases and inner products). Appendix A is a quick reference.

</Box>
