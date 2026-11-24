#!/usr/bin/env python3
"""Haberler modülü · örnek veri üretici (yalnızca bu modülün sayfalarına yazar).

Kullanım:  python3 -I moduller/haberler/_uret.py

Kaynaklar (yalnızca okunur):
  - public sözlük: ../dadahaber-prototip/araclar/ornek_veri.json (yayındaki haberler, yazarlar)
  - public site menüsü: ../dadahaber-prototip/parcalar/ust.html (kategori ağacı)
  - public sayfalar: haber başlığı → sitede gösterilen görsel eşleşmesi
  - ek sözlük: veri/panel.json → haberler_ek (taslak, zamanlanmış, çöp)
Yazdığı işaretler (moduller/haberler/index.html):
  <!--P:hb-satirlar--> <!--P:hb-suz-kategori--> <!--P:hb-suz-yazar--> <!--P:hb-suz-tur--> <!--P:hb-agac-->
  ve sekme sayaçlarının taban değerleri (data-taban).
"""
import glob, html, json, os, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
PUB = KOK.parent / "dadahaber-prototip"
SAYFA = KOK / "moduller" / "haberler" / "index.html"
SITE = "https://gaviaworks-dev.github.io/dadahaber-prototip/"
LISTEDE = 25

soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
ek = json.loads((KOK / "veri" / "panel.json").read_text(encoding="utf-8"))["haberler_ek"]["kayitlar"]
kayit = json.loads((KOK / "moduller.json").read_text(encoding="utf-8"))
e = lambda s: html.escape(str(s), quote=True)

# ---- başlık → görsel (sitede kartta gösterilen) ----
basliklar = {h["baslik"] for h in soz["haberler"]}
gorsel = {}
for f in sorted(glob.glob(str(PUB / "*.html"))):
    t = open(f, encoding="utf-8").read()
    for m in re.finditer(r"url\(assets/gorsel/(p\d+\.jpg)\)", t):
        h = re.search(r"<h[23][^>]*>(?:<a[^>]*>)?([^<]+)<", t[m.end():m.end() + 1500])
        if h:
            b = html.unescape(h.group(1).strip())
            if b in basliklar and b not in gorsel:
                gorsel[b] = m.group(1)

TUR = {"video-detay.html": "Video", "haber-dinle-detay.html": "Sesli haber", "kose-yazisi.html": "Köşe yazısı",
       "foto-fokus-detay.html": "Galeri", "infografik-detay.html": "İnfografik", "podcast-detay.html": "Podcast",
       "dada-dogrula-inceleme.html": "Dada Doğrula", "dada-baglam-dosya.html": "Dosya", "resmi-ilan-detay.html": "Resmî ilan",
       "dakika-dakika.html": "Canlı anlatım", "dakika-dakika-butce.html": "Canlı anlatım"}
TUR_IKON = {"Haber": "fa-newspaper", "Video": "fa-video", "Sesli haber": "fa-headphones", "Köşe yazısı": "fa-pen-nib",
            "Galeri": "fa-images", "İnfografik": "fa-chart-simple", "Podcast": "fa-podcast", "Dada Doğrula": "fa-circle-check",
            "Dosya": "fa-folder-open", "Resmî ilan": "fa-bullhorn", "Canlı anlatım": "fa-tower-broadcast"}
DURUM = {"yayinda": ("ok", "Yayında"), "taslak": ("off", "Taslak"), "zamanli": ("info", "Zamanlanmış"), "cop": ("warm", "Çöpte")}

def sayi(s):
    s = s.replace(".", "").replace(",", ".")
    m = re.match(r"([\d.]+)\s*(B|Mn)?", s)
    return float(m.group(1)) * (1000 if m.group(2) == "B" else 1e6 if m.group(2) == "Mn" else 1) if m else 0

def tarih(t, s):
    y, a, g = t.split("-")
    return f"{g}.{a}.{y} {s}"

# ---- düzenleme ekranının adresi (kayıttan; hazır değilse yapım aşaması sayfası) ----
duz = next(s for m in kayit["moduller"] if m["id"] == "haberler" for s in m["sayfalar"] if s["id"] == "duzenle")
def duz_href(kimlik):
    if duz.get("hazir"):
        return os.path.relpath(KOK / duz["dosya"], SAYFA.parent) + "?id=" + kimlik
    return os.path.relpath(KOK / kayit["yakinda_sayfasi"], SAYFA.parent) + "?s=haberler.duzenle"

# ---- satırlar ----
yayinda = sorted(soz["haberler"], key=lambda h: (h["tarih"], h["saat"]), reverse=True)
kayitlar = [dict(h, durum="yayinda", tur=TUR.get(h["detay"], "Haber"), gorsel=gorsel.get(h["baslik"])) for h in yayinda[:LISTEDE]]
kayitlar = [dict(x) for x in ek if x["durum"] != "cop"] + kayitlar + [dict(x) for x in ek if x["durum"] == "cop"]

def satir(h, i):
    kimlik = h.get("id") or f"ek-{i}"
    d_cls, d_ad = DURUM[h["durum"]]
    g = h.get("gorsel")
    alt = h.get("alt_konu") or ""
    kat = f'<span class="kb-kat"><b>{e(h["bolum"])}</b>' + (f'<i class="fa-solid fa-chevron-right" aria-hidden="true"></i>{e(alt)}' if alt and alt != h["bolum"] else "") + "</span>"
    thumb = (f'<span class="rcp-thumb" style="background-image:url(../../veri/gorsel/kucuk/{g})"></span>' if g
             else '<span class="rcp-thumb kb-yok" title="Görsel eksik"><i class="fa-solid fa-image" aria-hidden="true"></i></span>')
    tur = h.get("tur", "Haber")
    alt_satir = f'<i class="fa-solid {TUR_IKON.get(tur, "fa-newspaper")}" aria-hidden="true"></i>{e(tur)} · {e(h.get("yazar", ""))}'
    if h.get("sure"): alt_satir += f' · {e(h["sure"])}'
    if h.get("not"): alt_satir += f' · {e(h["not"])}'
    zaman = tarih(h["tarih"], h["saat"])
    if h["durum"] == "zamanli": zaman_hucre = f'<span class="kb-tarih">{zaman}</span>'
    elif h["durum"] in ("taslak", "cop"): zaman_hucre = f'<span class="kb-tarih muted">{zaman}</span>'
    else: zaman_hucre = f'<span class="kb-tarih">{zaman}</span>'
    gor = h.get("goruntulenme", "—") if h["durum"] == "yayinda" else "—"
    if h["durum"] == "yayinda":
        bak = f'<a class="ia-btn" href="{SITE}{e(h["detay"])}" target="_blank" rel="noopener" aria-label="Sitede görüntüle" title="Sitede görüntüle"><i class="fa-solid fa-eye" aria-hidden="true"></i></a>'
    else:
        bak = f'<a class="ia-btn" href="{e(duz_href(kimlik))}" aria-label="Önizle" title="Önizle"><i class="fa-solid fa-eye" aria-hidden="true"></i></a>'
    ara = f'{h["baslik"]} {h.get("yazar","")} {h["bolum"]} {alt}'
    nit = {
        "satir": kimlik, "durum": h["durum"], "kategori": h["bolum"], "yazar": h.get("yazar", ""), "tur": tur,
        "ara": ara, "baslik": h["baslik"], "href": duz_href(kimlik), "kat": f'{h["bolum"]}' + (f' › {alt}' if alt and alt != h["bolum"] else ""),
        "yayin": zaman, "goruntulenme": gor, "tur-ad": tur, "durum-ad": d_ad,
        "gorsel": f"../../veri/gorsel/{g}" if g else "",
    }
    nits = " ".join(f'data-{k}="{e(v)}"' for k, v in nit.items())
    return (f'<tr {nits}>'
            f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(h["baslik"])}"></td>'
            f'<td class="kb-ana"><div class="rcp-cell">{thumb}<div class="rcp-id"><div class="rcp-name" title="{e(h["baslik"])}">{e(h["baslik"])}</div><div class="rcp-by">{alt_satir}</div></div></div></td>'
            f'<td class="kb-gizle-m">{kat}</td>'
            f'<td><span class="pstat {d_cls}">{d_ad}</span></td>'
            f'<td class="kb-gizle-m">{zaman_hucre}</td>'
            f'<td class="say kb-gizle-t">{e(gor)}</td>'
            f'<td><div class="row-acts">{bak}'
            f'<a class="ia-btn" href="{e(duz_href(kimlik))}" aria-label="Düzenle" title="Düzenle"><i class="fa-solid fa-pen" aria-hidden="true"></i></a>'
            f'<button type="button" class="ia-btn danger" data-sil aria-label="Çöpe taşı" title="Çöpe taşı"><i class="fa-solid fa-trash" aria-hidden="true"></i></button>'
            f'<button type="button" class="ia-btn" data-diger aria-haspopup="true" aria-expanded="false" aria-label="Diğer işlemler" title="Diğer"><i class="fa-solid fa-ellipsis" aria-hidden="true"></i></button>'
            f'</div></td></tr>')

satirlar = "".join(satir(h, i) for i, h in enumerate(kayitlar))

# ---- kategori ağacı: sitenin menüsünden ----
ust = (PUB / "parcalar" / "ust.html").read_text(encoding="utf-8")
HIZMET = {"canli-skor", "puan-durumu", "fikstur", "takimlar", "piyasa-ekrani", "doviz", "altin", "borsa", "kripto-para",
          "akaryakit-fiyatlari", "faiz-oranlari", "ekonomik-takvim", "sinav-takvimi", "hamilelik", "astroloji", "81-il", "kadin-yazarlar"}
BOLUMLER = ["Gündem", "Spor", "Finans", "Kadın", "Savunma", "Dünya", "Kampüs", "Keşfet"]
KESFET = ["Teknoloji", "Yapay Zekâ", "Bilim", "Uzay", "Siber Güvenlik", "Oyun", "Gelecek", "İklim", "Sağlık", "Halk Sağlığı",
          "Otomobil", "Seyahat", "Gastronomi", "Kültür ve Yaşam", "Sinema", "Dizi", "Müzik", "Kitap", "Tiyatro", "Sergi"]  # sayfa-envanteri §3
linkler = re.findall(r'<a [^>]*href="([a-z0-9-]+)\.html"[^>]*>([^<]+)<', ust)
agac, sim = {}, None
for slug, ad in linkler:
    ad = html.unescape(ad.strip())
    if ad in BOLUMLER and ad not in agac:
        sim = ad; agac[sim] = []; continue
    if sim and ad not in ("Tümünü Gör", "Son Dakika") and slug not in HIZMET and ad not in agac[sim]:
        agac[sim].append(ad)
agac["Keşfet"] = KESFET
agac["Köşe"] = []
say_b = {}; say_a = {}
for h in soz["haberler"]:
    say_b[h["bolum"]] = say_b.get(h["bolum"], 0) + 1
    k = (h["bolum"], (h.get("alt_konu") or "").lower())
    say_a[k] = say_a.get(k, 0) + 1
RENK = {"Gündem": "gundem", "Spor": "spor", "Finans": "finans", "Kadın": "kadin", "Savunma": "savunma", "Dünya": "dunya", "Kampüs": "kampus", "Keşfet": "kesfet", "Köşe": "kose"}
fmt = lambda n: f"{n:,}".replace(",", ".")
parca = []
for b, altlar in agac.items():
    lis = "".join(f'<li>{e(a)}<span class="ka-say">{fmt(say_a.get((b, a.lower()), 0))}</span></li>' for a in altlar)
    parca.append(f'<details class="kat-{RENK[b]}"{" open" if b == "Gündem" else ""}><summary><i class="fa-solid fa-chevron-right" aria-hidden="true"></i><span class="ka-renk"></span>{e(b)}'
                 f'<span class="ka-say">{len(altlar)} alt konu · {fmt(say_b.get(b, 0))} haber</span></summary>'
                 + (f"<ul>{lis}</ul>" if lis else "") + "</details>")
agac_html = "".join(parca)

# ---- süzgeç seçenekleri ----
def secenek(deger, ad, alt=""):
    return f'<button type="button" data-deger="{e(deger)}" data-ad="{e(ad)}">{e(ad)}' + (f'<span class="ks-alt">{e(alt)}</span>' if alt else "") + "</button>"
suz_kat = secenek("", "Bütün kategoriler") + "".join(secenek(b, b, fmt(say_b.get(b, 0))) for b in agac)
yazarlar = {}
for y in soz["yazarlar"]:
    yazarlar.setdefault(y["alan"], []).append(y["ad"])
suz_yaz = secenek("", "Bütün yazarlar") + "".join(f'<div class="ks-grup">{e(b)}</div>' + "".join(secenek(a, a) for a in ads) for b, ads in yazarlar.items())
turler = ["Haber", "Köşe yazısı", "Video", "Sesli haber", "Galeri", "İnfografik", "Podcast", "Canlı anlatım", "Dosya", "Dada Doğrula", "Resmî ilan"]
suz_tur = secenek("", "Bütün türler") + "".join(secenek(t, t) for t in turler)

# ---- yaz ----
t = SAYFA.read_text(encoding="utf-8")
def yaz(t, ad, ic):
    d = re.compile(rf"(<!--P:{ad}-->).*?(<!--/P:{ad}-->)", re.S)
    if not d.search(t): raise SystemExit(f"işaret yok: {ad}")
    return d.sub(lambda m: m.group(1) + ic + m.group(2), t)
t = yaz(t, "hb-satirlar", satirlar)
t = yaz(t, "hb-suz-kategori", suz_kat)
t = yaz(t, "hb-suz-yazar", suz_yaz)
t = yaz(t, "hb-suz-tur", suz_tur)
t = yaz(t, "hb-agac", agac_html)
toplam = len(soz["haberler"])
t = re.sub(r'(data-sekme="hepsi"[^>]*data-taban=")\d*(")', rf"\g<1>{toplam - LISTEDE}\2", t)
t = re.sub(r'(data-sekme="yayinda"[^>]*data-taban=")\d*(")', rf"\g<1>{toplam - LISTEDE}\2", t)
SAYFA.write_text(t, encoding="utf-8")
print(f"satır {len(kayitlar)} · görselli {sum(1 for h in kayitlar if h.get('gorsel'))} · kategori {len(agac)} · yayında toplam {toplam}")
