#!/usr/bin/env python3
"""Kalıp OKUNURLUK ölçümü (Beyar, 26.11.2026: "hiçbir yazı katman altında kalmaz").

Her yazının GERÇEK zeminine karşı karşıtlığı ölçülür: sayfa gerçek tarayıcıda açılır (kalip/_oku.mjs, CDP), kartlardaki her yazı
satırının kutusu, rengi ve etkin saydamlığı toplanır, sayfanın ekran görüntüsü alınır. Aynı görünümün yazılı ve YAZISIZ iki ekran görüntüsü alınır (yazılar saydam, yerleşim aynı); harflerin gerçekten çizildiği
pikseller (iki görüntünün farkı) altındaki zemin
(fotoğraf, geçiş, karartma, kutu — ne varsa) ile yazının etkin rengi karşılaştırılır; zeminin en kötü %10'u ile yazı rengi arasındaki karşıtlık
WCAG ≥ 3:1 olmalı (büyük ve kalın yazı; panelde bütün kart yazıları bu sınıfta sayılır).
Görünümler: Seçilen + 14 iskelet × bütün sekmeler (Gündem) ve Seçilen × beş kategori × bütün sekmeler; Instagram 4:5.
Kullanım: python3 -I kalip/_oku.py [--canli] [--hepsi]   Çıkış: 0 = hepsi okunur · 1 = okunmayan var. kalip/_olc.py sonunda çalıştırır.
"""
import functools, http.server, json, os, re, shutil, socket, subprocess, sys, tempfile, threading, urllib.request
from pathlib import Path
from PIL import Image

KOK = Path(__file__).resolve().parent.parent
CANLI = "https://gaviaworks-dev.github.io/dadahaber-panel-prototip/"
ESIK = 3.0
SEKME = ["akis", "haber", "sd", "kaydir", "dikey", "alinti", "durum"]


def lum(c):
    def k(v):
        v /= 255
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    return .2126 * k(c[0]) + .7152 * k(c[1]) + .0722 * k(c[2])


def oran(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + .05) / (min(x, y) + .05)


def renk(s):
    return list(s[:3]) if isinstance(s, list) else [float(x) for x in re.findall(r"[\d.]+", s)[:3]]


def sunucu():
    sk = socket.socket(); sk.bind(("127.0.0.1", 0)); port = sk.getsockname()[1]; sk.close()

    class S(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
        def do_GET(self):
            if self.path.startswith("/canli/"):
                try:
                    with urllib.request.urlopen(urllib.request.Request(CANLI + self.path[7:], headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
                        b, tur = r.read(), r.headers.get("Content-Type", "application/octet-stream")
                    self.send_response(200); self.send_header("Content-Type", tur); self.end_headers(); self.wfile.write(b)
                except Exception:
                    self.send_response(404); self.end_headers()
                return
            return super().do_GET()
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(S, directory=str(KOK)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, port


def main():
    canli = "--canli" in sys.argv
    veri = json.loads(re.search(r'<script type="application/json" id="kpVeri">(.*?)</script>', (KOK / "kalip" / "index.html").read_text(encoding="utf-8"), re.S).group(1))
    altlar = [a["id"] for a in veri["alt"]]
    gorunum = [f"alt={a}&sekme={s}&kat=gundem" for a in altlar for s in SEKME]
    gorunum += [f"alt={veri['varsayilan']}&sekme={s}&kat={k}" for k in ("spor", "kadin", "finans", "savunma") for s in SEKME if s != "durum"]
    srv, port = sunucu()
    dz = Path(tempfile.mkdtemp(prefix="kp-oku-"))
    (dz / "g.json").write_text(json.dumps(gorunum))
    taban = f"http://127.0.0.1:{port}/" + ("canli/" if canli else "")
    subprocess.run(["node", str(KOK / "kalip" / "_oku.mjs"), taban, str(dz), str(dz / "g.json")], timeout=3600, capture_output=True)
    srv.shutdown()
    kalan, satir, hata = [], 0, []
    for i, g in enumerate(gorunum):
        jp = dz / f"{i}.json"
        if not jp.exists():
            hata.append(g); continue
        o = json.loads(jp.read_text())
        if "hata" in o or not o.get("parca"):
            hata.append(g); continue
        def birlestir(ek):
            pc = [Image.open(dz / f"{i}_{k}{ek}.png").convert("RGB") for k in range(len(o["parca"]))]
            W_, H_ = pc[0].size[0], o["parca"][-1] + pc[-1].size[1]
            im_ = Image.new("RGB", (W_, H_))
            for k, p_ in enumerate(pc): im_.paste(p_, (0, o["parca"][k]))
            return im_
        im = birlestir(""); W, H = im.size; px = im.load(); py = birlestir("y").load()  # px: yazısız zemin · py: yazılı
        for m in o["m"]:
            x, y, w, h = m["r"]; y -= o["y"]
            x0, y0, x1, y1 = max(0, int(x)), max(0, int(y)), min(W, int(x + w)), min(H, int(y + h))
            if x1 - x0 < 3 or y1 - y0 < 3:
                continue
            satir += 1
            tc, op = renk(m["c"]), m["op"]
            # yalnız harfin gerçekten çizildiği pikseller (yazılı ile yazısız görüntü farklı): harfin altındaki zemin
            ornek = []
            for yy in range(y0, y1):
                for xx in range(x0, x1, 1 if x1 - x0 < 200 else 2):
                    a_, b_ = py[xx, yy], px[xx, yy]
                    if abs(a_[0] - b_[0]) + abs(a_[1] - b_[1]) + abs(a_[2] - b_[2]) > 60:
                        ornek.append(b_)
            if len(ornek) < 6:
                continue
            # her zemin pikselinde yazının etkin rengi (saydamlık zeminle karışır) ile zeminin karşıtlığı; en kötü %10'un ortancası
            oranlar = sorted(oran([op * tc[j] + (1 - op) * p[j] for j in range(3)], p) for p in ornek)
            kotu = oranlar[: max(1, len(oranlar) // 10)]
            o_ = kotu[len(kotu) // 2]
            if o_ < ESIK:
                kalan.append((o_, f"{g} · {m['ad']} · {m.get('s', '')} \"{m['m']}\" karşıtlık {o_:.2f}"))
    shutil.rmtree(dz, ignore_errors=True)
    kalan.sort()
    print(f"Okunurluk{' (canlı)' if canli else ''}: {len(gorunum)} görünüm · {satir} yazı satırı · okunmayan {len(kalan)}" + (f" · açılamayan görünüm {len(hata)}" if hata else ""))
    for _, x in kalan[: (10 ** 6 if "--hepsi" in sys.argv else 40)]:
        print("   " + x)
    sys.exit(1 if kalan or hata else 0)


if __name__ == "__main__":
    main()
