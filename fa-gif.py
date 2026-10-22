from PIL import Image, ImageDraw, ImageFont

W, H = 640, 170
INK = (20, 32, 74)
f = ImageFont.truetype("C:/Windows/Fonts/BRUSHSCI.TTF", 112)
txt = "Mihai Onea"

base = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(base)
bb = d.textbbox((0, 0), txt, font=f)
tw = bb[2] - bb[0]
x = (W - tw) // 2 - bb[0]
y = (H - (bb[3] - bb[1])) // 2 - bb[1] - 8
d.text((x, y), txt, font=f, fill=255)
# subliniere, ca la autograf
d.line([(x + 40, H - 26), (x + tw - 10, H - 34)], fill=255, width=4)

L, R = x - 10, x + tw + 20
frames, N = [], 34
for i in range(N + 1):
    t = 1 - (1 - i / N) ** 2  # încetinește spre final
    edge = int(L + (R - L) * t)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(0, 0), (edge + 30, 0), (edge - 10, H), (0, H)], fill=255)
    a = Image.composite(base, Image.new("L", (W, H), 0), m)
    fr = Image.new("RGB", (W, H), (255, 255, 255))
    fr.paste(Image.new("RGB", (W, H), INK), mask=a)
    frames.append(fr.convert("P", palette=Image.ADAPTIVE, colors=32))

frames[0].save("semnatura-mihai-onea.gif", save_all=True, append_images=frames[1:],
               duration=[55] * N + [3500], loop=0, optimize=True)
print("ok", len(frames))
