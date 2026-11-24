#!/usr/bin/env python3
"""Panel denetimi: her sayfa için kural kural GEÇTİ / KALDI (docs/teslim-denetimi.md → "Otomatik denetim").

Kullanım:  python3 -I araclar/denetim.py [--hizli] [--genislik 1440,390] [klasör ya da sayfa …]
  - Bağımsız: kendi yerel sunucusunu açar (boş bir kapı), başsız Chrome'la araclar/denetim.html'i çalıştırır.
  - Yol verilmezse bütün sayfalar (moduller/, cekirdek/, ui-kit.html). Her dalga teslimden önce bu betikten geçer.
  - Çıkış kodu: ihlal varsa 1. "Karar bekliyor" (pano, uzun sayfa önerisi) ihlal sayılmaz, ayrı listelenir.

Statik kurallar (dosyadan): elle zorunlu/yıldız, tarayıcı tarih alanı, sayfada <style>, satır içi sabit renk
  (kulüp rengi gibi veri hariç: --kat/--renk), satır içi elle boşluk (margin/padding/gap), kayıtta olmayan data-sayfa.
Tarayıcı kuralları (araclar/denetim.html): JS hatası, yatay taşma, liste araç satırı (tek satır, taşmasız, listede bir tane),
  çift blok, uzun sayfa, kilitli düğme, satır eylemleri sırası, Çöp sekmesi, boşluk (yapışık ipucu/kutu),
  bildirimin düğmeyi kapatması, zorunlu alan (?yeni=1 formlarında pasif ana düğme).
"""
import json, os, re, socket, subprocess, sys, threading, functools, http.server, glob
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
arg = [a for a in sys.argv[1:]]
GEN = "1440,390"
if "--genislik" in arg:
    GEN = arg[arg.index("--genislik") + 1]; del arg[arg.index("--genislik"):arg.index("--genislik") + 2]
HIZLI = "--hizli" in arg
arg = [a for a in arg if not a.startswith("--")]

def sayfa_listesi():
    hedef = arg or ["moduller", "cekirdek", "ui-kit.html"]
    out = []
    for h in hedef:
        p = KOK / h
        if p.is_file(): out.append(h)
        else: out += sorted(str(x.relative_to(KOK)) for x in p.rglob("*.html"))
    return [s for s in out if "/screenshots/" not in s]

kayit = json.loads((KOK / "moduller.json").read_text(encoding="utf-8"))
ANAHTAR = {f"{m['id']}.{s['id']}" for m in kayit["moduller"] for s in m.get("sayfalar", [])}

def statik(s):
    t = (KOK / s).read_text(encoding="utf-8")
    g = re.sub(r"<!--P:(menu|ust|bas)-->.*?<!--/P:\1-->", "", t, flags=re.S)
    g = re.sub(r"<!--.*?-->", "", g, flags=re.S)
    v = []
    if s != "ui-kit.html" and (re.search(r'<span class="zorunlu">', g) or re.search(r"\sdata-zorunlu(?=[\s>])", g)): v.append("zorunlu: sayfada elle zorunlu/yıldız (kayıttan gelmeli)")
    if re.search(r'type="(date|datetime-local|time)"', g): v.append("form: tarayıcı tarih alanı")
    if s != "ui-kit.html" and "<style" in g: v.append("gorsel-dil: sayfada <style>")
    for st in re.findall(r'style="([^"]*)"', g):
        if re.search(r"(?<![-\w])(margin|padding|gap)\s*:", st): v.append("bosluk: satır içi elle boşluk (" + st[:40] + ")"); break
    for st in re.findall(r'style="([^"]*)"', g):
        if re.search(r"(^|;)\s*(color|background(-color)?|border(-color)?)\s*:\s*(#|rgb)", st): v.append("gorsel-dil: satır içi sabit renk (" + st[:40] + ")"); break
    m = re.search(r'<body[^>]*data-sayfa="([^"]+)"', t)
    if s.startswith(("moduller/", "cekirdek/")) and "yakinda" not in s and m and m.group(1) not in ANAHTAR: v.append("kayit: data-sayfa kayıtta yok")
    return v

def sunucu():
    sk = socket.socket(); sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]; sk.close()
    class Sessiz(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(Sessiz, directory=str(KOK)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, port

def tarayici(sayfalar, port):
    sonuc = []
    parca = 12  # bir Chrome çağrısında 12 sayfa
    for i in range(0, len(sayfalar), parca):
        grup = sayfalar[i:i + parca]
        url = f"http://127.0.0.1:{port}/araclar/denetim.html?w={GEN}&s=" + ",".join(grup)
        butce = str(len(grup) * len(GEN.split(",")) * 2500 + 5000)
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--virtual-time-budget={butce}", "--dump-dom", url], capture_output=True, text=True, timeout=600)
        m = re.search(r'<pre id="sonuc">(.*?)</pre>', r.stdout, re.S)
        try: sonuc += json.loads(html_unescape(m.group(1)))
        except Exception: sonuc += [{"sayfa": s, "w": 0, "ihlal": ["denetim: tarayıcı sonucu okunamadı"], "karar": []} for s in grup]
    return sonuc

def html_unescape(x):
    import html; return html.unescape(x)

sayfalar = sayfa_listesi()
srv, port = sunucu()
try:
    tar = [] if HIZLI else tarayici(sayfalar, port)
finally:
    srv.shutdown()

rapor, kural_say, karar_say = {}, {}, {}
for s in sayfalar:
    rapor[s] = {"ihlal": [f"{v} (dosya)" for v in statik(s)], "karar": []}
for x in tar:
    for v in x["ihlal"]: rapor[x["sayfa"]]["ihlal"].append(f"{v} @{x['w']}")
    for v in x["karar"]: rapor[x["sayfa"]]["karar"].append(f"{v} @{x['w']}")
for s, r in rapor.items():
    for v in r["ihlal"]: kural_say[v.split(":")[0]] = kural_say.get(v.split(":")[0], 0) + 1
    for v in r["karar"]: karar_say[v.split(":")[0]] = karar_say.get(v.split(":")[0], 0) + 1

kalan = [s for s, r in rapor.items() if r["ihlal"]]
print(f"Denetim: {len(sayfalar)} sayfa · genişlik {GEN if not HIZLI else '— (yalnız dosya)'} · geçti {len(sayfalar) - len(kalan)} · kaldı {len(kalan)}")
for s in sayfalar:
    r = rapor[s]
    if r["ihlal"] or r["karar"]:
        print(("KALDI  " if r["ihlal"] else "KARAR  ") + s)
        for v in r["ihlal"]: print("   ✗ " + v)
        for v in r["karar"]: print("   ? " + v)
print("Kural başına ihlal: " + (", ".join(f"{k} {n}" for k, n in sorted(kural_say.items())) or "yok"))
if karar_say: print("Karar bekleyen: " + ", ".join(f"{k} {n}" for k, n in sorted(karar_say.items())))
(KOK / "docs" / "screenshots").mkdir(parents=True, exist_ok=True)
(KOK / "docs" / "screenshots" / "denetim-son.json").write_text(json.dumps(rapor, ensure_ascii=False, indent=1), encoding="utf-8")
sys.exit(1 if kalan else 0)
