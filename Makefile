.PHONY: demo viz pdf figures clean

# Run the offline meta-harness optimization loop end-to-end.
demo:
	bin/meta-harness demo

# Serve the live dashboard.
viz:
	bin/meta-harness viz

# Rebuild the typeset PDF (post.pdf) and the per-figure PNGs.
pdf: docs/post.pdf
figures: docs/figures/architecture.png

docs/post.pdf: docs/post.tex
	cd docs && pdflatex -interaction=nonstopmode post.tex
	cd docs && pdflatex -interaction=nonstopmode post.tex
	cd docs && rm -f *.aux *.log *.out *.toc

docs/figures/architecture.png: docs/figures.tex
	cd docs && pdflatex -interaction=nonstopmode figures.tex
	cd docs && pdftoppm -r 250 -png figures.pdf figures/figure
	cd docs && mv figures/figure-1.png figures/architecture.png
	cd docs && mv figures/figure-2.png figures/bar-chart.png
	cd docs && mv figures/figure-3.png figures/heatmap.png
	cd docs && mv figures/figure-4.png figures/dashboard-sketch.png
	cd docs && python3 -c "from PIL import Image, ImageChops; from pathlib import Path;\
	  [_save(f) for f in sorted(Path('figures').glob('*.png'))]" 2>/dev/null || \
	  python3 docs/_trim.py
	cd docs && rm -f *.aux *.log *.out *.toc

clean:
	rm -rf runs/
	cd docs && rm -f *.aux *.log *.out *.toc figures.pdf
