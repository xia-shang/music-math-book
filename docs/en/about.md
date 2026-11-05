# About this book

## What it is

**Music as Mathematical Logic: An Axiomatic Theory of Music from Vibration to Structure** is an open-source web book. It rewrites music theory the way a computer-science textbook is organised:

- **Axiomatic**: definitions, postulates and theorems instead of "memorise this rule";
- **Computable**: every key numerical claim has a Python implementation;
- **Interactive**: key concepts come with draggable demos;
- **Deployable**: VitePress + GitHub Actions; fork the repo, enable Pages as described in Appendix B, and it deploys itself.

## What it is not

This is not a book about how to play an instrument, and it is not a music history. It will not tell you "press the chord like this"; it will tell you why pressing it like that is acoustically cheap.

## Authors and acknowledgements

The book is a collaborative project by people who believe that aesthetics can be partly explained. The chapter structure draws on Helmholtz's *On the Sensations of Tone*, Sethares's *Tuning, Timbre, Spectrum, Scale*, and the classic 1965 paper by Plomp and Levelt. The mathematics is kept hand-checkable wherever possible.

## Licence

| Content | Licence |
| --- | --- |
| Text and figures | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
| Code examples | [MIT](https://opensource.org/licenses/MIT) |

You may copy, distribute and adapt the text and figures for non-commercial purposes, provided you keep attribution and share under the same licence. Code examples are under MIT.

## Stack

```text
VitePress 1.6  →  Markdown + Vue 3 + MathJax
GitHub Actions →  build + deploy to Pages
Python 3.12    →  all numerical checks
```

## Contributing

Found a wrong formula, a broken script, or an unclear explanation? Open an issue or a PR:

1. Fork the repository;
2. Create a branch such as `fix/ch03-typo`;
3. Edit the Markdown under `docs/`;
4. Preview with `pnpm dev`, then open the PR.

> Text and figure contributions are licensed CC BY-NC-SA 4.0; code contributions are MIT. See `LICENSE`.
