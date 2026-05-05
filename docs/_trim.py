"""Auto-trim white margins from each PNG in figures/."""
from PIL import Image, ImageChops
from pathlib import Path

PAD = 16
for f in sorted(Path("figures").glob("*.png")):
    im = Image.open(f).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if not bbox:
        continue
    L, T, R, B = bbox
    cropped = im.crop((max(0, L - PAD), max(0, T - PAD),
                       min(im.width, R + PAD), min(im.height, B + PAD)))
    cropped.save(f, optimize=True)
    print(f"{f.name}: {im.size} -> {cropped.size}")
