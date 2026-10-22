import hashlib
b = "https://raw.githubusercontent.com/MikeBrumson/ilustromania-semnatura/main"
v = hashlib.md5(open("out/poza.gif", "rb").read()).hexdigest()[:8]  # ?v= nou la fiecare GIF nou, ca să nu rămână în cache
card = open("card.html", encoding="utf8").read().replace("BAZA", b).replace('.gif"', '.gif?v=' + v + '"')
p = open("semnatura.html", encoding="utf8").read()
i = p.index('<div class="box" id="sig">') + len('<div class="box" id="sig">')
j = p.index('</div>\n<div class="pas">')
out = p[:i] + "\n" + card + p[j:]
for f in ("index.html", "semnatura.html"):
    open(f, "w", encoding="utf8").write(out)
print("ok", v)
