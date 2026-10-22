"""Scoate autocolantul „ilustromania” (literele albastre + conturul alb) de pe fundalul graffiti -> logo-sursa.png transparent."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

im = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
alb = (r > 215) & (g > 215) & (b > 215)
alb = ndimage.binary_closing(alb, iterations=2)
# tot ce e închis de conturul alb (literele) intră în autocolant
plin = ndimage.binary_fill_holes(alb)
lab, n = ndimage.label(plin)
marimi = ndimage.sum(plin, lab, range(1, n + 1))
pastrat = np.isin(lab, [i + 1 for i, s in enumerate(marimi) if s > marimi.max() * 0.02])
ys, xs = np.where(pastrat)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
rgba = np.dstack([a, pastrat * 255]).astype(np.uint8)[y0:y1, x0:x1]
out = Image.fromarray(rgba, "RGBA")
out.save("logo-sursa.png")
print("logo", out.size, "componente pastrate", len([s for s in marimi if s > marimi.max() * 0.02]))
