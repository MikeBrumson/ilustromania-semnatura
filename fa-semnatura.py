"""Semnătura ILUSTROMANIA după designul din reel (card: bara de iconițe, text, poză în benzi oblice animate).
Rulare: python fa-semnatura.py [poza.jpg]  -> out/*.png, out/poza.gif
Totul la 2x (afișat la jumătate în HTML), ca să fie clar pe telefon."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2
NAVY = (20, 24, 38)
GRAY = (110, 116, 128)
LINE = (205, 209, 216)
BLUE = (0, 73, 255)
os.makedirs("out", exist_ok=True)


def font(name, px):
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", px * S)


# ---------- iconițe (24px afișat) ----------
def icon(kind):
    n = 24 * S
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = max(2, int(1.6 * S))
    c = (60, 66, 80, 255)
    if kind == "web":
        d.ellipse([5 * S, 5 * S, 19 * S, 19 * S], outline=c, width=w)
        d.ellipse([9 * S, 5 * S, 15 * S, 19 * S], outline=c, width=w)
        d.line([5 * S, 12 * S, 19 * S, 12 * S], fill=c, width=w)
    elif kind == "instagram":
        d.rounded_rectangle([5 * S, 5 * S, 19 * S, 19 * S], radius=4 * S, outline=c, width=w)
        d.ellipse([9 * S, 9 * S, 15 * S, 15 * S], outline=c, width=w)
        d.ellipse([15.5 * S, 7 * S, 17 * S, 8.5 * S], fill=c)
    elif kind == "facebook":
        f = font("arialbd.ttf", 15)
        d.text((12 * S, 12.5 * S), "f", font=f, fill=c, anchor="mm")
    im.save(f"out/{kind}.png")


for k in ("web", "instagram", "facebook"):
    icon(k)

# ---------- bifa albastră (16px) ----------
n = 16 * S
b = Image.new("RGBA", (n * 4, n * 4), (0, 0, 0, 0))
d = ImageDraw.Draw(b)
import math
pts = []
for i in range(24):  # rozetă ca la badge-ul „verified”
    r = (n * 2 - 2) if i % 2 == 0 else (n * 2 - 2) * 0.86
    a = math.pi * 2 * i / 24
    pts.append((n * 2 + r * math.cos(a), n * 2 + r * math.sin(a)))
d.polygon(pts, fill=(29, 155, 240, 255))
d.line([(n * 1.3, n * 2.05), (n * 1.8, n * 2.55), (n * 2.75, n * 1.5)], fill="white", width=int(n * 0.28), joint="curve")
b.resize((n, n), Image.LANCZOS).save("out/bifa.png")

# ---------- logo: varianta pentru fundal deschis (alb -> navy, albastrul rămâne) ----------
lg = Image.open("logo.webp").convert("RGBA")
px = lg.load()
for y in range(lg.height):
    for x in range(lg.width):
        r, g, bl, a = px[x, y]
        if a > 0 and r > 200 and g > 200 and bl > 200:
            px[x, y] = (*NAVY, a)
h = 22 * S
lg = lg.resize((int(lg.width * h / lg.height), h), Image.LANCZOS)
lg.save("out/logo.png")
print("logo", lg.size[0] // S, "x", lg.size[1] // S)

# ---------- poza în benzi oblice, animată ----------
W, H = 120 * S, 98 * S
if len(sys.argv) > 1:
    src = Image.open(sys.argv[1]).convert("RGB")
    sc = max(W / src.width, H / src.height)
    src = src.resize((int(src.width * sc) + 1, int(src.height * sc) + 1), Image.LANCZOS)
    src = src.crop(((src.width - W) // 2, 0, (src.width - W) // 2 + W, H))
else:  # fără poză: placeholder cu inițialele
    src = Image.new("RGB", (W, H), NAVY)
    ImageDraw.Draw(src).text((W // 2, H // 2), "MO", font=font("arialbd.ttf", 40), fill=(255, 255, 255), anchor="mm")
if os.environ.get("ALB_NEGRU") == "1":  # poza de om: alb-negru, ca în reel
    src = src.convert("L").convert("RGB")

N = 4                 # benzi
slant = 27 * S        # cât se înclină o bandă
bw = (W + slant) / N
gap = 5 * S


def band(i, dy):
    x0 = i * bw - slant
    return [(x0 + slant + gap / 2, dy), (x0 + bw + slant - gap / 2, dy), (x0 + bw - gap / 2, H + dy), (x0 + gap / 2, H + dy)]


frames, dur = [], []
STEPS = 16
for f in range(STEPS + 1):
    im = Image.new("RGB", (W, H), (255, 255, 255))
    dd = ImageDraw.Draw(im)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for i in range(N):
        t = max(0.0, min(1.0, (f - i * 2.2) / (STEPS - 3 * 2.2)))
        e = 1 - (1 - t) ** 3
        sign = -1 if i % 2 == 0 else 1
        dy = int(sign * H * (1 - e))
        # umbra gri a benzii (rămâne fixă, ca în reel)
        dd.polygon([(x + 6 * S, y) for x, y in band(i, 0)], fill=(232, 234, 238))
        md.polygon(band(i, dy), fill=255)
    im.paste(src, mask=mask)
    frames.append(im.convert("P", palette=Image.ADAPTIVE, colors=128))
    dur.append(45)
dur[-1] = 3800
frames[0].save("out/poza.gif", save_all=True, append_images=frames[1:], duration=dur, loop=0, optimize=True)
print("gif", os.path.getsize("out/poza.gif") // 1024, "KB", len(frames), "cadre")
