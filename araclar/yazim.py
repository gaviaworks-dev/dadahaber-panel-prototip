#!/usr/bin/env python3
"""Yazım kuralı dönüştürücüsü (Beyar, 25.11.2026): etiket, bölüm/kart başlığı, sekme, düğme, menü öğesi, pencere başlığı ve seçenek
adlarında her kelimenin baş harfi büyük; bağlaç ve edatlar küçük; Türkçe büyük harf (i → İ, ı → I); kısaltma ve özel adlar olduğu gibi.

Kaynak: denetim betiğinin tarayıcıda bulduğu metinler (docs/screenshots/denetim-ham.json → "yazim"). Betik bu metinleri kaynakta
yalnız metin olarak geçtikleri yerlerde değiştirir: >Metin<, kullanıcıya görünen nitelikler (data-baslik, data-onay-evet …),
çekirdek JS'teki tırnaklı dizgiler, modül kaydındaki "baslik" adları ve modül üreticileri (_uret*.py).
Kullanım:  python3 -I araclar/yazim.py [--uygula]   (--uygula yoksa yalnız ne değişeceğini sayar)
"""
import json, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
BAGLAC = {"ve", "ya", "da", "de", "ile", "için", "veya", "ki", "mi", "mı", "mu", "mü", "gibi", "kadar", "göre", "ama", "yoksa"}  # bağlaç ve edat
NITELIK = ["data-baslik", "data-onay-evet", "data-isaret-on", "data-isaret-off", "data-yeni-metin", "data-bos", "data-ad-tekil", "data-yok", "data-etiket"]

def buyuk(c):
    return {"i": "İ", "ı": "I"}.get(c, c.upper())

def kelime(w, ilk):
    m = re.match(r'^([("“\'«]*)(.*)$', w); on, govde = m.group(1), m.group(2)
    if not govde: return w
    h = govde[0]
    if not re.match(r"[a-zçğıöşü]", h): return w
    if re.search(r"[A-ZÇĞİÖŞÜ]", govde[1:]): return w  # iOS, eBay gibi karışık yazılan özel adlar olduğu gibi
    if re.match(r"^(https?:|@|#|www\.)", govde) or re.search(r"[a-z]\.[a-z]", govde, re.I): return w
    if not ilk and re.sub(r"[),.:;!?\"”']+$", "", govde).lower() in BAGLAC: return w
    return on + buyuk(h) + govde[1:]

def donustur(s):
    k = s.split(" "); out = []
    for i, w in enumerate(k):
        if i > 0 and out and re.fullmatch(r"[·•\-–—|/]", k[i - 1] or ""): out.append(w); continue
        out.append(kelime(w, i == 0) if w else w)
    return " ".join(out)

ham = json.loads((KOK / "docs" / "screenshots" / "denetim-ham.json").read_text(encoding="utf-8"))
esle = {}
for x in ham:
    for s in x.get("yazim", []) or []:
        y = donustur(s)
        if y != s: esle[s] = y
dosyalar = sorted(set(list(KOK.glob("moduller/**/*.html")) + list(KOK.glob("cekirdek/**/*.html")) + [KOK / "ui-kit.html"]
               + list(KOK.glob("cekirdek/js/*.js")) + list(KOK.glob("moduller/*/_uret*.py")) + list(KOK.glob("moduller/*/_veri*.py")) + [KOK / "moduller.json"]))
dosyalar = [f for f in dosyalar if "screenshots" not in str(f) and f.name != "kayit.js"]
uygula = "--uygula" in sys.argv
toplam, bulunan = 0, set()
for f in dosyalar:
    t = f.read_text(encoding="utf-8"); y = t
    for eski, yeni in sorted(esle.items(), key=lambda kv: -len(kv[0])):
        es_ = eski.replace("'", "&#x27;").replace('"', "&quot;")  # HTML'de kesme işareti varlık olarak yazılmış olabilir
        if eski not in y and es_ not in y: continue  # hızlı ön kontrol
        if eski not in y: eski, yeni = es_, yeni.replace("'", "&#x27;").replace('"', "&quot;")
        e = re.escape(eski)
        desen = [r"(?<=>)(\s*)" + e + r"(\s*)(?=<)"]                      # >Metin<
        desen += [r'(?<=\b' + n + r'=")' + e + r'(?=")' for n in NITELIK]  # nitelik
        if f.suffix in (".js", ".py"):
            # veri anahtarı korunur: dosyada ["x"], "x": ya da 'x': biçiminde geçen tek kelime anahtar sayılır, hiç değiştirilmez
            # (saat → Saat üreticileri bozmuştu: h["saat"] KeyError)
            if " " not in eski and re.search(r"""\[\s*['"]""" + e + r"""['"]\s*\]|['"]""" + e + r"""['"]\s*:""", y): continue
            desen += [r"(?<=')" + e + r"(?=')", r'(?<=")' + e + r'(?=")']  # tırnaklı dizgi
            desen += [r"(?<=\})" + e + r"(?=<)", r"(?<=>)" + e + r"(?=\{)", r"(?<=\})" + e + r"(?=\{)"]  # f-string içinde {…}Metin< ya da >Metin{…}
        if f.name == "moduller.json": desen = [r'(?<="baslik": ")' + e + r'(?=")', r'(?<="ad": ")' + e + r'(?=")']
        for d_ in desen:
            y2, n = re.subn(d_, lambda m: (m.group(1) if m.groups() else "") + yeni + (m.group(2) if m.groups() and len(m.groups()) > 1 else ""), y)
            if n: bulunan.add(eski.replace('&#x27;', "'").replace('&quot;', '"')); toplam += n; y = y2
    if y != t and uygula: f.write_text(y, encoding="utf-8")
kalan = sorted(set(esle) - bulunan)
print(f"Yazım: {len(esle)} farklı metin · {toplam} yerde {'değiştirildi' if uygula else 'değişecek'} · kaynakta düz bulunamayan {len(kalan)}")
for s in kalan[:60]: print("   ? " + s + "  →  " + esle[s])
