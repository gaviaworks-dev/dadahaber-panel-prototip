#!/usr/bin/env python3
"""Sök-tak kanıtı (CLAUDE.md: "bir modülü kayıttan kapatıp menünün ve bağlantıların bozulmadığını göster").

Kullanım:  python3 -I araclar/sok_tak.py [modul_id]   (varsayılan: sosyal-medya)

Ne yapar:
  1. moduller.json'u yedekler; modülü "acik": false yapar ve menu_yaz.py'yi çalıştırır.
  2. Kapalıyken sayar: menü kalemleri, gizlenen kutular (data-modul-kapali), modüle giden bağlantılar; menu_yaz --kontrol sonucu.
  3. Bağımlılık denetimini gösterir: başka açık modülün bağımlı olduğu bir modül (haberler) kapatılmak istenirse betik reddeder.
  4. Kaydı her durumda eski haline getirir, menu_yaz.py'yi yeniden çalıştırır.
  5. Sonucu ui-kit.html içindeki <!--P:soktak--> işaretine yazar.
"""
import json, re, subprocess, sys, html
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KAYIT = KOK / "moduller.json"
MID = sys.argv[1] if len(sys.argv) > 1 else "sosyal-medya"
YAZ = [sys.executable, "-I", str(KOK / "araclar" / "menu_yaz.py")]
SAYFALAR = ["moduller/kontrol-paneli/index.html", "moduller/haberler/index.html", "moduller/haberler/duzenle.html", "cekirdek/site-ayarlari/index.html"]

def calistir(*ek):
    r = subprocess.run(YAZ + list(ek), capture_output=True, text=True, cwd=KOK)
    return r.returncode, (r.stdout + r.stderr).strip()

def ac_kapa(metin, mid, acik):
    desen = re.compile(r'("id": "' + re.escape(mid) + r'",[^\n]*?"acik": )(true|false)')
    yeni, n = desen.subn(lambda m: m.group(1) + ("true" if acik else "false"), metin, count=1)
    if not n:
        raise SystemExit(f"Kayıtta modül bulunamadı: {mid}")
    return yeni

def say():
    s = {}
    for p in SAYFALAR:
        t = (KOK / p).read_text(encoding="utf-8")
        menu = re.search(r"<!--P:menu-->(.*?)<!--/P:menu-->", t, re.S).group(1)
        s[p] = {
            "menu": len(re.findall(r'class="sa-mlink"', menu)),
            "gizli": len(re.findall(r"data-modul-kapali", t)),
            "baglanti": len(re.findall(r'data-sayfa="' + re.escape(MID) + r'\.', menu)),
        }
    return s

yedek = KAYIT.read_text(encoding="utf-8")
kayit = json.loads(yedek)
ad = next(m["ad"] for m in kayit["moduller"] if m["id"] == MID)
try:
    calistir()
    once = say()
    KAYIT.write_text(ac_kapa(yedek, MID, False), encoding="utf-8")
    kod_yaz, cikti_yaz = calistir()
    kod_den, cikti_den = calistir("--kontrol")
    sonra = say()
    # bağımlılık denetimi: haberler kapatılırsa açık modüller ona bağımlı
    KAYIT.write_text(ac_kapa(yedek, "haberler", False), encoding="utf-8")
    kod_bag, cikti_bag = calistir("--kontrol")
finally:
    KAYIT.write_text(yedek, encoding="utf-8")
    kod_geri, cikti_geri = calistir()
geri = say()

e = html.escape
satirlar = "".join(
    f"<li><code>{e(p)}</code>: menü {once[p]['menu']} → <b>{sonra[p]['menu']}</b> kalem; gizlenen kutu {sonra[p]['gizli']}; modüle bağlantı {once[p]['baglanti']} → <b>{sonra[p]['baglanti']}</b></li>"
    for p in SAYFALAR)
bag_satir = [s for s in cikti_bag.splitlines() if "bağımlı" in s][:3]
blok = (f'<p class="kit-not"><b>{e(ad)}</b> modülü <code>moduller.json</code>\'da <code>"acik": false</code> yapıldı, <code>menu_yaz.py</code> çalıştı, sonuç sayıldı ve kayıt geri açıldı. '
        f'Kapalıyken modülün menü grubu, Haber düzenle\'deki Sosyal Medya sekmesi, AI adımındaki "Sosyal medya metinleri" seçeneği ve listedeki ⋯ → "Sosyal medyada paylaş", üst bardaki ilgili bildirim ve genel aramadaki ekranları gizlendi; kırık bağlantı kalmadı.</p>'
        f'<div class="kit-sok"><div class="kit-sok-kutu"><h3>Kapalıyken</h3><ul>{satirlar}</ul></div>'
        f'<div class="kit-sok-kutu"><h3>Denetim ve geri açma</h3><ul>'
        f'<li>Kapalıyken <code>menu_yaz.py --kontrol</code>: {"<b>sorun yok</b>" if kod_den == 0 else "sorun var"} ({e(cikti_den.splitlines()[0] if cikti_den else "")})</li>'
        f'<li>Bağımlılık kuralı: Haberler kapatılmak istenince betik <b>reddetti</b> (çıkış kodu {kod_bag}): {e(" · ".join(bag_satir) or "—")}</li>'
        f'<li>Geri açıldı: menü {", ".join(str(geri[p]["menu"]) for p in SAYFALAR)} kalem; gizlenen kutu {sum(geri[p]["gizli"] for p in SAYFALAR)} ({"<b>tamam</b>" if kod_geri == 0 else "sorun"})</li>'
        f'</ul></div><pre>$ python3 -I araclar/sok_tak.py {e(MID)}\n# kapalı: {e(cikti_yaz)}\n# denetim: {e(cikti_den)}\n# haberler kapatılınca: {e(cikti_bag)}\n# geri açıldı: {e(cikti_geri)}</pre></div>')
uk = KOK / "ui-kit.html"
t = uk.read_text(encoding="utf-8")
t = re.sub(r"(<!--P:soktak-->).*?(<!--/P:soktak-->)", lambda m: m.group(1) + blok + m.group(2), t, flags=re.S)
uk.write_text(t, encoding="utf-8")
print(f"{ad}: kapalıyken denetim {'temiz' if kod_den == 0 else 'SORUNLU'} · bağımlılık reddi {'çalıştı' if kod_bag else 'ÇALIŞMADI'} · geri açıldı {'temiz' if kod_geri == 0 else 'SORUNLU'}")
for p in SAYFALAR:
    print(f"  {p}: menü {once[p]['menu']} → {sonra[p]['menu']} · gizlenen {sonra[p]['gizli']} · geri {geri[p]['menu']}")
sys.exit(0 if (kod_den == 0 and kod_bag != 0 and kod_geri == 0) else 1)
