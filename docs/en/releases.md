# Releases and changelog

Current version: **v1.1.0** (2026-11-05)

The project follows semantic versioning: `major.minor.patch`. Major changes when the structure becomes incompatible, minor for new chapters/languages/features, patch for typo and numerical fixes.

| Version | Date | What changed |
| --- | --- | --- |
| **v1.1.0** | 2026-11-05 | English edition with a language switch; version page; full factual/editorial review; 4 new figures, 3 interactive demos, 21 generated audio clips; collapsed long outputs; mobile fixes |
| v1.0.0 | 2026-11-03 | First release: 10 chapters + 5 appendices + 10 runnable scripts; VitePress site and GitHub Pages deployment |

## v1.1.0 in detail

- **Bilingual**: `docs/en/` plus a navbar language switcher; component strings follow the active locale.
- **Review**: corrected the non-monotonicity of roughness with pitch, the "exactly zero" claim about $D$, the intervals of the augmented triad, Perron–Frobenius conditions, the Miller–Madow conditional-entropy correction, and several topological statements about discrete spaces.
- **Interactive**: `ConsonanceExplorer` now has Web Audio playback and a harmonic comb; `EuclideanRhythmLab` adds k/n/BPM controls and a click track.
- **Charts**: roughness curve, harmonic comb, rhythm timeline, transition heatmap.
- **Audio**: expanded from 8 to 21 clips covering intervals, chords, cadences, scales, timbre, rhythms and a Markov melody.
- **Reading experience**: long script outputs collapsed; fixed mobile formula clipping, wide tables and the rhythm grid overflow.

## Where the version appears

- Navbar: `v1.1.0` links here;
- Footer: `… · v1.1.0`;
- `package.json` `version` field.
