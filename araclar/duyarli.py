#!/usr/bin/env python3
"""Duyarlı test: bütün sayfalar (ve yeni kayıt formları) 1440 · 1280 · 1024 · 768 · 390 genişlikte, başsız Chrome'la.

Kullanım:  python3 -I araclar/duyarli.py [--taban https://…/dadahaber-panel-prototip] [--genislik 1440,390] [sayfa …]
  --taban verilmezse yerel sunucu açılır. Canlı test için yayın adresini verin (araclar/duyarli.html yayında olmalı).
Ölçülenler araclar/duyarli.html başında. Sonuç: genişlik başına sorunlu sayfa ve ayrıntı; docs/screenshots/duyarli-son.json.
"""
import concurrent.futures, functools, html, http.server, json, os, re, socket, subprocess, sys, threading
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
a = sys.argv[1:]
def al(ad, vars_):
    if ad in a:
        i = a.index(ad); v = a[i + 1]; del a[i:i + 2]; return v
    return vars_
TABAN = al("--taban", None)
GEN = [int(x) for x in al("--genislik", "1440,1280,1024,768,390").split(",")]

def sayfalar():
    hedef = a or ["moduller", "cekirdek", "ui-kit.html"]
    out = []
    for h in hedef:
        p = KOK / h
        files = [p] if p.is_file() else sorted(p.rglob("*.html"))
        for f in files:
            rel = str(f.relative_to(KOK))
            if "/screenshots/" in rel: continue
            out.append(rel)
            if "data-yeni-baslik" in f.read_text(encoding="utf-8"): out.append(rel + "?yeni=1")
    return out

def sunucu():
    sk = socket.socket(); sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]; sk.close()
    class Sessiz(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x): pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(Sessiz, directory=str(KOK)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{port}"

def calistir(taban, w, grup):
    url = f"{taban}/araclar/duyarli.html?w={w}&s=" + ",".join(x.replace("?", "%3F").replace("=", "%3D") for x in grup)
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--virtual-time-budget={len(grup) * 6000 + 5000}", "--dump-dom", url], capture_output=True, text=True, timeout=900)
    m = re.search(r'<pre id="sonuc">(.*?)</pre>', r.stdout, re.S)
    try: return json.loads(html.unescape(m.group(1)))
    except Exception: return [{"sayfa": s, "w": w, "hata": ["test: sonuç okunamadı"]} for s in grup]

S = sayfalar()
srv = None
if not TABAN: srv, TABAN = sunucu()
isler = [(w, S[i:i + 10]) for w in GEN for i in range(0, len(S), 10)]
sonuc = []
with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('PARALEL', '2'))) as ex:
    for r in ex.map(lambda x: calistir(TABAN, x[0], x[1]), isler): sonuc += r
# yük altında sunucu bir dosyayı geç verebilir (kbKurucu yok): sorunlu sayfa/genişlik bir kez tek başına yeniden ölçülür
for x in [x for x in sonuc if x["hata"]]:
    y = calistir(TABAN, x["w"], [x["sayfa"]])
    if y and y[0].get("sayfa") == x["sayfa"]: sonuc[sonuc.index(x)] = y[0]
if srv: srv.shutdown()
print(f"Duyarlı test: {len(S)} sayfa/form × {len(GEN)} genişlik · taban {TABAN}")
for w in GEN:
    k = [x for x in sonuc if x["w"] == w and x["hata"]]
    print(f"  {w}px: sorunlu {len(k)}")
    for x in k:
        print(f"    ✗ {x['sayfa']}: " + " · ".join(x["hata"])[:300])
import collections
pen = sum((x.get("pencere") or {}).get("olculen", 0) for x in sonuc); penh = sum((x.get("pencere") or {}).get("hatali", 0) for x in sonuc)
bd = sum((x.get("bosluk") or {}).get("durum", 0) for x in sonuc); by = sum((x.get("bosluk") or {}).get("yapisik", 0) for x in sonuc); bb = sum((x.get("bosluk") or {}).get("binme", 0) for x in sonuc)
tek = {(x["sayfa"], b["ad"]) for x in sonuc for b in (x.get("pencere") or {}).get("bas", [])}
notlu = {(x["sayfa"].split("?")[0], i) for x in sonuc for i in (x.get("pencere") or {}).get("notlu", [])}
print(f"Çekmece/pencere: {len(tek)} ayrı çekmece/pencere · {pen} açılış ölçüldü (sayfa × genişlik) · sorunlu {penh} · uzun açıklaması gövdeye inen {len(notlu)}")
ac = sum(x.get("acilir", 0) or 0 for x in sonuc); print(f"Açılan kutu: {ac} açılış ölçüldü (sayfa × genişlik) · sorunlu sayfa/genişlik {sum(1 for x in sonuc if any(h.startswith('acilir') for h in x['hata']))}")
print(f"Blok boşluğu: {bd} durum · yapışık çift {by} · binme {bb}")
for w in GEN:  # başlık yüksekliği bütün çekmece ve pencerelerde aynı olmalı
    hs = collections.Counter(b["h"] for x in sonuc if x["w"] == w for b in (x.get("pencere") or {}).get("bas", []))
    if len(hs) > 1:
        cok = hs.most_common(1)[0][0]
        farkli = [(x["sayfa"], b["ad"], b["h"]) for x in sonuc if x["w"] == w for b in (x.get("pencere") or {}).get("bas", []) if b["h"] != cok]
        print(f"  ✗ {w}px başlık yüksekliği farklı (çoğu {cok}px): " + "; ".join(f"{s} {a} {h}px" for s, a, h in farkli[:5]))
        for s, a_, h in farkli: next(x for x in sonuc if x["w"] == w and x["sayfa"] == s)["hata"].append(f"pencere: {a_} başlık yüksekliği {h}px (çoğu {cok}px)")
(KOK / "docs" / "screenshots").mkdir(parents=True, exist_ok=True)
(KOK / "docs" / "screenshots" / "duyarli-son.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
sys.exit(1 if any(x["hata"] for x in sonuc) else 0)
