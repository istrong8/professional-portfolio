# Reframing Nuclear Licensing: The FSAR as a Tool, Not a Barrier

White paper by Irais Strong, written for NE 5599-003, Idaho State University (May 2025).

**Read it:** [PDF](../../docs/papers/reframing-nuclear-licensing-fsar.pdf) · [on the portfolio site](https://istrong8.github.io/professional-portfolio/#standards)

Argues that the Final Safety Analysis Report is a strategic tool for advanced reactor licensing rather than a bureaucratic barrier. Draws on the Production Part Approval Process from manufacturing; case studies of NuScale, Oklo, and Kairos Power; NRC mandatory hearing and NEPA reforms; and 10 CFR Part 53.

The Oklo case study covers the NRC's January 2022 denial of the first Aurora application. A footnote notes Oklo's later NRC pre-application readiness assessment (2025).

## Files

| File | What it is |
|---|---|
| `main.tex` | Paper source |
| `bibliographie.bib` | References |
| `elsarticle.cls` | Elsevier article class (LaTeX Project Public License) |

## Build

Requires a TeX distribution with `elsarticle-num.bst` (TeX Live: `texlive-publishers`) and the `cm-super` fonts.

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

The document class is loaded with the `authoryear` option while using a numeric bibliography style, so natbib reports a compatibility error; run in nonstop mode (Overleaf does this automatically). The output is unaffected.
