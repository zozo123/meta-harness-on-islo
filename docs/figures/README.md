# Figures

PNGs of each TikZ figure used in the writeup. Drop them straight into Substack or any other Markdown-based publishing tool.

| File | Used in | What it shows |
|---|---|---|
| `architecture.png` | post.pdf p.1 | The optimization loop: harness → snapshot → eval → runs → proposer → harness. Maps each step to an `islo` primitive. |
| `bar-chart.png` | post.pdf p.2 | Pass rate per iteration. Goes 0/5 → 2/5 → 3/5 → 4/5 → 5/5 in 4 proposer steps; "✓ converged at v4" annotation points at the final bar. |
| `heatmap.png` | post.pdf p.3 | Task × iteration grid showing which task was fixed at which step. The shape of the green wave shows progression and any regressions. |
| `dashboard-sketch.png` | post.pdf p.4 | Layout sketch of the live HTML dashboard at `viz/index.html`. Three panels: pass-rate timeline, task×iter heatmap, trace inspector. |

## Rebuilding

From repo root:

```bash
make figures
```

This compiles `docs/figures.tex` (one TikZ figure per page, via the `article` document class with thin-margin `\newpage` separation), rasterizes each page to PNG with `pdftoppm` at 250 DPI, then auto-trims white margins via `docs/_trim.py` (PIL).

The same TikZ source lives in `docs/post.tex` and is kept in lockstep with this file.
