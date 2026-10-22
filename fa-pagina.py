b = "https://raw.githubusercontent.com/MikeBrumson/ilustromania-semnatura/main"
card = open("card.html", encoding="utf8").read().replace("BAZA", b)
p = open("semnatura.html", encoding="utf8").read()
i = p.index('<div class="box" id="sig">') + len('<div class="box" id="sig">')
j = p.index('</div>\n<div class="pas">')
out = p[:i] + "\n" + card + p[j:]
for f in ("index.html", "semnatura.html"):
    open(f, "w", encoding="utf8").write(out)
print("ok")
