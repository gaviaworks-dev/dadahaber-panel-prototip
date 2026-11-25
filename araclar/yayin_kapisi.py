#!/usr/bin/env python3
"""Yayın kapısı (Beyar, 25.11.2026): denetimden geçmeyen ya da yarım kalan sayfa canlıya çıkmaz.

Her yayından (commit + push) önce çalışır. Bütün sayfaları denetler (araclar/denetim.py, 5 genişlik, ?yeni=1 halleri dahil);
KALDI olan her sayfanın kayıttaki (moduller.json) "hazir" değerini false yapar, menüleri yeniden üretir (araclar/menu_yaz.py):
sayfa menüde görünmez, ona giden bağlantılar pasif olur. Kayıtta bulunmayan bir sayfa kalırsa yayın durur.

Kullanım:  python3 -I araclar/yayin_kapisi.py            (denetim + kapı)
           python3 -I araclar/yayin_kapisi.py --kuru     (yalnız rapor; kayda dokunmaz)
Çıkış kodu: 0 = bütün sayfalar geçti · 2 = kalan sayfalar hazir:false yapıldı (yayın onlarsız sürebilir) · 1 = yayın durmalı.
"""
import re, subprocess, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KURU = "--kuru" in sys.argv

d = subprocess.run([sys.executable, "-I", str(KOK / "araclar" / "denetim.py")], cwd=KOK, capture_output=True, text=True)
print("\n".join(l for l in d.stdout.splitlines() if l.startswith(("Denetim:", "Kural başına", "Çekirdek JS"))))
kalan = sorted({l.split()[1].split("?")[0] for l in d.stdout.splitlines() if l.startswith("KALDI")})
# ayrı sunum sayfası (kalip/): kendi denetimi ve kalıp ölçümü (çakışma, taşma) — kalan varsa yayın durur
kalip_hata = False
if (KOK / "kalip" / "index.html").exists():
    dk = subprocess.run([sys.executable, "-I", str(KOK / "araclar" / "denetim.py"), "kalip/index.html"], cwd=KOK, capture_output=True, text=True)
    print("Sunum (kalip/): " + next((l for l in dk.stdout.splitlines() if l.startswith("Denetim:")), "denetim çıktısı yok"))
    if any(l.startswith("KALDI") for l in dk.stdout.splitlines()): kalip_hata = True
    if (KOK / "kalip" / "_olc.py").exists():
        ko = subprocess.run([sys.executable, "-I", str(KOK / "kalip" / "_olc.py")], cwd=KOK, capture_output=True, text=True)
        print(next((l for l in ko.stdout.splitlines() if l.startswith("Kalıp ölçümü")), "Kalıp ölçümü: çıktı yok")); kalip_hata = kalip_hata or ko.returncode != 0
cekirdek_hata = "Çekirdek JS tarayıcı kutusu: yok" not in d.stdout
if not kalan and not cekirdek_hata and not kalip_hata:
    print("Yayın kapısı: bütün sayfalar geçti.")
    sys.exit(0)

kayit = (KOK / "moduller.json").read_text(encoding="utf-8")
inen, kayitsiz = [], []
for s in kalan:
    desen = re.compile(r'("dosya":\s*"' + re.escape(s) + r'",\s*"hazir":\s*)(true|false)')
    m = desen.search(kayit)
    if not m: kayitsiz.append(s); continue
    if m.group(2) == "true":
        inen.append(s)
        if not KURU: kayit = desen.sub(r"\1false", kayit, count=1)
if inen and not KURU:
    (KOK / "moduller.json").write_text(kayit, encoding="utf-8")
    subprocess.run([sys.executable, "-I", str(KOK / "araclar" / "menu_yaz.py"), "--kayit-js"], cwd=KOK, check=True, capture_output=True)

print("Yayın kapısı: denetimden geçmeyen " + str(len(kalan)) + " sayfa")
for s in kalan:
    print("   " + s + ("  → hazir: false (menüden çıktı)" if s in inen else "  → kayıtta yok" if s in kayitsiz else "  → zaten hazir: false"))
if KURU and inen: print("   (--kuru: kayda dokunulmadı)")
if cekirdek_hata: print("   Çekirdek JS'te tarayıcı kutusu var: yayın durmalı")
if kalip_hata: print("   Sunum sayfası (kalip/) denetimden ya da kalıp ölçümünden geçmedi: yayın durmalı")
sys.exit(1 if kayitsiz or cekirdek_hata or kalip_hata else 2)
