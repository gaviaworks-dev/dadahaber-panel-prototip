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
import importlib.util as _iu
_skp = _iu.spec_from_file_location("_kategori", Path(__file__).resolve().parent / "_kategori.py"); _kat = _iu.module_from_spec(_skp); _skp.loader.exec_module(_kat)  # kategori ağacı (tek kaynak)
_sp = _iu.spec_from_file_location("_yazim", Path(__file__).resolve().parent / "_yazim.py"); _yazim = _iu.module_from_spec(_sp); _sp.loader.exec_module(_yazim)  # yazım kuralı (Beyar)

KOK = Path(__file__).resolve().parents[2]
PUB = KOK.parent / "dadahaber-prototip"
SAYFA = KOK / "moduller" / "haberler" / "index.html"
SITE = "https://gaviaworks-dev.github.io/dadahaber-prototip/"
LISTEDE = 72

soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
_pv = json.loads((KOK / "veri" / "panel.json").read_text(encoding="utf-8"))
ek = _pv["haberler_ek"]["kayitlar"]
AI = _pv["ai_kaynakli"]["kayitlar"]
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

TUR = {"video-detay.html": "Video", "haber-dinle-detay.html": "Sesli Haber", "kose-yazisi.html": "Köşe Yazısı",
       "foto-fokus-detay.html": "Galeri", "infografik-detay.html": "İnfografik", "podcast-detay.html": "Podcast",
       "dada-dogrula-inceleme.html": "Dada Doğrula", "dada-baglam-dosya.html": "Dosya", "resmi-ilan-detay.html": "Resmî İlan",
       "dakika-dakika.html": "Canlı Anlatım", "dakika-dakika-butce.html": "Canlı Anlatım"}
TUR_IKON = {"Haber": "fa-newspaper", "Video": "fa-video", "Sesli Haber": "fa-headphones", "Köşe Yazısı": "fa-pen-nib",
            "Galeri": "fa-images", "İnfografik": "fa-chart-simple", "Podcast": "fa-podcast", "Dada Doğrula": "fa-circle-check",
            "Dosya": "fa-folder-open", "Resmî İlan": "fa-bullhorn", "Canlı Anlatım": "fa-tower-broadcast"}
_hb = next(m for m in kayit["moduller"] if m["id"] == "haberler")
BICIM = {b["id"]: b["ad"] for b in _hb["ayarlar"]["bicim"]["secenekler"]}  # Haber, Analiz, Görüş, Uzman Görüşü, Röportaj, Video
BICIM_VARS = _hb["ayarlar"]["bicim"].get("varsayilan", "haber")
BICIM_IKON = {k: v["ikon"] for k, v in _kat.TURLER.items()}; BICIM_IKON.setdefault("video", "fa-video")
def bicim_id(h):
    """Örnekte biçim sitenin `tur` alanından (analiz, uzman-gorusu, video); köşe yazısı Görüş; yoksa Haber."""
    if h.get("bicim") in BICIM: return h["bicim"]
    if h.get("detay") == "kose-yazisi.html" or h.get("bolum") == "Köşe" or (h.get("tur") or "").lower() == "köşe yazısı": return "gorus"
    t_ = (h.get("tur") or "").lower()
    return t_ if t_ in BICIM else BICIM_VARS
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
# köşe yazısı kendi düzenleme sayfasında açılır (Köşe Yazıları bölümü, t-kose); kayıtta yoksa haber düzenlemeye düşer
kose_duz = next((s for m in kayit["moduller"] if m["id"] == "haberler" for s in m["sayfalar"] if s["id"] == "kose-duzenle"), None)
def duz_href(kimlik, tur=None):
    d_ = kose_duz if (tur == "Köşe Yazısı" and kose_duz and kose_duz.get("hazir")) else duz
    if d_.get("hazir"):
        return os.path.relpath(KOK / d_["dosya"], SAYFA.parent) + "?id=" + kimlik
    return os.path.relpath(KOK / kayit["yakinda_sayfasi"], SAYFA.parent) + "?s=haberler." + d_["id"]

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
    tur = {x.lower(): x for x in TUR_IKON}.get((h.get("tur") or "Haber").lower(), h.get("tur") or "Haber")
    bc = bicim_id(h)
    bicim_etk = (f' <span class="etk"><i class="fa-solid {BICIM_IKON.get(bc, "fa-tag")}" aria-hidden="true"></i>{e(BICIM[bc])}</span>' if bc != "haber" else "")
    ai = AI.get(h.get("id", ""))
    ai_etk = (f'<span class="kb-ai-etk" title="AI haber havuzundan · {e(ai["kaynak"])} ({ai["grup"]}) · güven %{ai["skor"]} · {e(ai["onay"])} onayladı"><i class="fa-solid fa-robot" aria-hidden="true"></i>AI · %{ai["skor"]}</span>' if ai else "")
    alt_satir = ai_etk + f'<i class="fa-solid {TUR_IKON.get(tur, "fa-newspaper")}" aria-hidden="true"></i>{e(tur)} · {e(h.get("yazar", ""))}'
    if h.get("sure"): alt_satir += f' · {e(h["sure"])}'
    if h.get("not"): alt_satir += f' · {e(h["not"])}'
    zaman = tarih(h["tarih"], h["saat"])
    if h["durum"] == "zamanli": zaman_hucre = f'<span class="kb-tarih">{zaman}</span>'
    elif h["durum"] in ("taslak", "cop"): zaman_hucre = f'<span class="kb-tarih muted">{zaman}</span>'
    else: zaman_hucre = f'<span class="kb-tarih">{zaman}</span>'
    gor = h.get("goruntulenme", "—") if h["durum"] == "yayinda" else "—"
    if h["durum"] == "yayinda":
        bak = f'<a class="ia-btn" href="{SITE}{e(h["detay"])}" target="_blank" rel="noopener" aria-label="Sitede Görüntüle" title="Sitede Görüntüle"><i class="fa-solid fa-eye" aria-hidden="true"></i></a>'
    else:
        bak = f'<a class="ia-btn" href="{e(duz_href(kimlik, tur))}" aria-label="Önizle" title="Önizle"><i class="fa-solid fa-eye" aria-hidden="true"></i></a>'
    ara = f'{h["baslik"]} {h.get("yazar","")} {h["bolum"]} {alt}'
    nit = {
        "satir": kimlik, "durum": h["durum"], "kategori": h["bolum"], "yazar": h.get("yazar", ""), "tur": tur,
        "ara": ara, "baslik": h["baslik"], "href": duz_href(kimlik, tur), "kat": f'{h["bolum"]}' + (f' › {alt}' if alt and alt != h["bolum"] else ""),
        "yayin": zaman, "goruntulenme": gor, "tur-ad": tur, "durum-ad": d_ad, "bicim": bc, "bicim-ad": BICIM[bc],
        # B4/B6: haberin kullanıldığı yerler (örnek): manşet, Günün 5'i, bülten
        "yerler": ("manset gunun5" if h["durum"] == "yayinda" and i % 6 == 0 else "bulten" if h["durum"] == "yayinda" and i % 6 == 3 else ""),
        "gorsel": f"../../veri/gorsel/{g}" if g else "",
        "kaynak": "ai" if ai else "editor",
        "kaynak-ad": (f'AI haber havuzu · {ai["kaynak"]} ({ai["grup"]}) · güven %{ai["skor"]} · {ai["onay"]} onayladı' if ai else "Editör girişi"),
    }
    nits = " ".join(f'data-{k}="{e(v)}"' for k, v in nit.items())
    return (f'<tr {nits}>'
            f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(h["baslik"])}"></td>'
            f'<td class="kb-ana"><div class="rcp-cell">{thumb}<div class="rcp-id"><div class="rcp-name" title="{e(h["baslik"])}">{e(h["baslik"])}</div><div class="rcp-by">{alt_satir}</div></div></div></td>'
            f'<td class="kb-gizle-m">{kat}</td>'
            f'<td><span class="pstat {d_cls}">{d_ad}</span>{bicim_etk}</td>'
            f'<td class="kb-gizle-m">{zaman_hucre}</td>'
            f'<td class="say kb-gizle-t">{e(gor)}</td>'
            f'<td><div class="row-acts">{bak}'
            f'<a class="ia-btn" href="{e(duz_href(kimlik, tur))}" aria-label="Düzenle" title="Düzenle"><i class="fa-solid fa-pen" aria-hidden="true"></i></a>'
            f'<button type="button" class="ia-btn danger" data-sil aria-label="Çöpe Taşı" title="Çöpe Taşı"><i class="fa-solid fa-trash" aria-hidden="true"></i></button>'
            f'<button type="button" class="ia-btn" data-diger aria-haspopup="true" aria-expanded="false" aria-label="Diğer işlemler" title="Diğer"><i class="fa-solid fa-ellipsis" aria-hidden="true"></i></button>'
            f'</div></td></tr>')

satirlar = "".join(satir(h, i) for i, h in enumerate(kayitlar))

# ---- kategori ağacı: tek kaynak (site araclar/kategori.json → _kategori.py), sütunlara göre ----
def tr_slug(s):
    m = str.maketrans("çğıöşüâîûÇĞİÖŞÜ", "cgiosuaiuCGIOSU")
    return re.sub(r"[^a-z0-9]+", "-", s.translate(m).lower()).strip("-")
agac = _kat.ALTLAR            # haber atanabilen alt kategoriler (formların alt konu havuzu)
say_b = {}; say_a = {}
for h in soz["haberler"]:
    say_b[h["bolum"]] = say_b.get(h["bolum"], 0) + 1
    k = (h["bolum"], (h.get("alt_konu") or "").lower())
    say_a[k] = say_a.get(k, 0) + 1
RENK = _kat.RENK
fmt = lambda n: f"{n:,}".replace(",", ".")
def duzenle_btn(ad, ust, sl, baslik, sutun=""):
    seo_b = f"{ad} Haberleri" + (f" · {ust}" if ust else "") + " | Dada Haber"
    seo_a = f"{ad} ile ilgili son dakika gelişmeleri, analizler ve özel haberler Dada Haber'de."
    return (f'<button type="button" class="ka-btn" data-sablon-ac="hbKategoriForm" data-baslik-yaz="{e(ad)} · düzenle" '
            f'data-deger-ad="{e(ad)}" data-deger-ust-tur="{"alt" if ust else "ana"}" data-deger-ust="{e(ust)}" data-deger-sutun="{e(sutun)}" data-deger-slug="{e(sl)}" data-deger-seo-baslik="{e(seo_b)}" data-deger-seo-aciklama="{e(seo_a)}" '
            f'aria-label="{e(ad)} düzenle" title="Düzenle"><i class="fa-solid fa-pen" aria-hidden="true"></i></button>')
def sil_btn(ad, ust, haber, alt):
    return (f'<button type="button" class="ka-btn danger" data-kat-sil data-ad="{e(ad)}" data-ust="{e(ust)}" data-haber="{haber}" data-alt="{alt}" '
            f'aria-label="{e(ad)} sil" title="Sil"><i class="fa-solid fa-trash" aria-hidden="true"></i></button>')
SERVIS = '<span class="etk" title="Sitede servis sayfasıdır; içeriği kendiliğinden gelir, habere alt kategori olarak atanmaz">Servis Sayfası · Haber Atanmaz</span>'
def ekle_btn(b_, sutun=""):
    return (f'<button type="button" class="ka-btn" data-sablon-ac="hbKategoriForm" data-baslik-yaz="{e(b_)}' + (f' › {e(sutun)}' if sutun else "") + ' · yeni alt konu" data-deger-ad="" data-deger-ust-tur="alt" '
            f'data-deger-ust="{e(b_)}" data-deger-sutun="{e(sutun)}" data-deger-slug="" data-deger-seo-baslik="" data-deger-seo-aciklama="" '
            f'aria-label="{e(b_)}' + (f' › {e(sutun)}' if sutun else "") + ' altına alt konu ekle" title="Alt konu ekle"><i class="fa-solid fa-plus" aria-hidden="true"></i></button>')
parca = []
for b in _kat.AGAC:
    b_ = b["ad"]; lis = []
    for s in b["sutunlar"]:
        tum_servis = all(o["servis"] for o in s["ogeler"])
        # sayaç yeri her satırda aynı (sağa yaslı); servis sayfasında sayaç yerine işaret
        lis.append(f'<li class="ka-sutun"><b>{e(s["ad"])}</b><span class="ka-say">' + (SERVIS if tum_servis else f'{len(s["ogeler"])} alt konu') + f'</span>{ekle_btn(b_, s["ad"])}</li>')
        for o in s["ogeler"]:
            n = say_a.get((b_, o["ad"].lower()), 0)
            lis.append(f'<li>{e(o["ad"])}<span class="ka-say">' + (("—" if tum_servis else SERVIS) if o["servis"] else fmt(n)) + '</span>'
                       + f'{duzenle_btn(o["ad"], b_, o["slug"], b_, s["ad"])}{sil_btn(o["ad"], b_, 0 if o["servis"] else n, 0)}</li>')
    nt = len(_kat.TUM_ALTLAR[b_])
    parca.append(f'<details class="kat-{RENK[b_]}"{" open" if b_ == "Gündem" else ""}><summary><i class="fa-solid fa-chevron-right" aria-hidden="true"></i><span class="ka-renk"></span>{e(b_)}'
                 f'<span class="ka-say">{len(b["sutunlar"])} sütun · {nt} alt konu · {fmt(say_b.get(b_, 0))} haber</span>{ekle_btn(b_)}{duzenle_btn(b_, "", b["slug"], b_)}{sil_btn(b_, "", say_b.get(b_, 0), nt)}</summary>'
                 f'<ul>{"".join(lis)}</ul></details>')
agac_html = "".join(parca)
ust_secenek = "".join(
    f'<button type="button" data-deger="{e(b_)}" data-ad="{e(b_)}">{e(b_)}<span class="ks-alt">{len(_kat.SUTUNLAR[b_])} sütun · {len(_kat.TUM_ALTLAR[b_])} alt konu</span></button>' for b_ in _kat.ANALAR)

# ---- süzgeç seçenekleri ----
def secenek(deger, ad, alt=""):
    return f'<button type="button" data-deger="{e(deger)}" data-ad="{e(ad)}">{e(ad)}' + (f'<span class="ks-alt">{e(alt)}</span>' if alt else "") + "</button>"
suz_kat = secenek("", "Bütün Kategoriler") + "".join(secenek(b, b, fmt(say_b.get(b, 0))) for b in agac)
yazarlar = {}
for y in soz["yazarlar"]:
    yazarlar.setdefault(y["alan"], []).append(y["ad"])
suz_yaz = secenek("", "Bütün yazarlar") + "".join(f'<div class="ks-grup">{e(b)}</div>' + "".join(secenek(a, a) for a in ads) for b, ads in yazarlar.items())
turler = ["Haber", "Köşe Yazısı", "Video", "Sesli Haber", "Galeri", "İnfografik", "Podcast", "Canlı Anlatım", "Dosya", "Dada Doğrula", "Resmî İlan"]
suz_bicim = secenek("", "Bütün Biçimler") + "".join(secenek(k, v) for k, v in BICIM.items())

# ---- yaz ----
t = SAYFA.read_text(encoding="utf-8")
def yaz(t, ad, ic):
    d = re.compile(rf"(<!--P:{ad}-->).*?(<!--/P:{ad}-->)", re.S)
    if not d.search(t): raise SystemExit(f"işaret yok: {ad}")
    return d.sub(lambda m: m.group(1) + ic + m.group(2), t)
t = yaz(t, "hb-satirlar", satirlar)
t = yaz(t, "hb-suz-kategori", suz_kat)
t = yaz(t, "hb-suz-yazar", suz_yaz)
t = yaz(t, "hb-suz-bicim", suz_bicim)
t = yaz(t, "hb-agac", agac_html)
t = yaz(t, "hb-kat-ust", ust_secenek)
# Sütun: üst kategori seçilince o kategorinin sütunları; yoksa aynı yerden eklenir (havuz kuralı); alt konu için zorunlu
t = yaz(t, "hb-kat-sutun", (f'<div class="kb-cip-girdi" data-alan="sutun" data-alan-id="sutun" data-tek data-havuz-yonet data-kullanim-birim="alt konuda" data-ana-kaynak="#kfUstSecim" '
    f'data-alt-harita="{e(json.dumps(_kat.SUTUNLAR, ensure_ascii=False))}" data-havuz="[]" data-zorunlu-metin="Alt konunun açılır menüde duracağı sütunu seçin">'
    '<input type="text" placeholder="Sütun ara ya da yazıp ekleyin" aria-label="Sütun ara"><div class="pnl-menu kb-cip-oneri"></div></div>'))
toplam = len(soz["haberler"])
t = re.sub(r'(data-sekme="hepsi"[^>]*data-taban=")\d*(")', rf"\g<1>{toplam - LISTEDE}\2", t)
t = re.sub(r'(data-sekme="yayinda"[^>]*data-taban=")\d*(")', rf"\g<1>{toplam - LISTEDE}\2", t)
SAYFA.write_text(_yazim.duzelt(t), encoding="utf-8")

# ---- düzenleme sayfası: ana kategori, alt konu, yazar, tür seçenekleri ----
DUZ = KOK / "moduller" / "haberler" / "duzenle.html"
d = DUZ.read_text(encoding="utf-8")
def sec_isaretli(deger, ad, alt, secili):
    return f'<button type="button" data-deger="{e(deger)}" data-ad="{e(ad)}"{" class=\"is-sec\"" if secili else ""}>{e(ad)}' + (f'<span class="ks-alt">{e(alt)}</span>' if alt else "") + "</button>"
d = yaz(d, "hb-df-kat", "".join(sec_isaretli(b_, b_, f"{len(a_)} alt konu", b_ == "Gündem") for b_, a_ in agac.items()))
# alt konular: çoklu seçim (Beyar 24.11.2026); ilk seçilen ana alt konu. Ana kategori değişince havuz değişir.
alt_harita = {b_: a_ for b_, a_ in agac.items()}
cip = lambda v: f'<span class="kb-cip" data-deger="{e(v)}"><span>{e(v)}</span><button type="button" aria-label="Kaldır"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></span>'
d = yaz(d, "hb-df-alt", (f'<div class="kb-cip-girdi" data-alan-id="alt-konu" data-birincil data-havuz-kapali data-ana-kaynak="#dfKatSecim" '
    f'data-havuz="{e(json.dumps(agac["Gündem"], ensure_ascii=False))}" data-alt-harita="{e(json.dumps(alt_harita, ensure_ascii=False))}">'
    + cip("Toplum") + '<input type="text" placeholder="Alt konu ara" aria-label="Alt konu ara"><div class="pnl-menu kb-cip-oneri"></div></div>'))
d = yaz(d, "hb-df-yazar", "".join(f'<div class="ks-grup">{e(b_)}</div>' + "".join(sec_isaretli(a_, a_, "", a_ == "Hakan Uysal") for a_ in ads) for b_, ads in yazarlar.items()))
d = yaz(d, "hb-df-bicim", "".join(sec_isaretli(k, v, "", k == BICIM_VARS) for k, v in BICIM.items()))
# yeni kayıt boş açılır (Beyar): örnek kaynak satırları gizlenir, zamanlama tarihleri boşalır; bildirim önizlemesini çekirdek doldurur
d = d.replace('<div class="km-satir" data-sira>', '<div class="km-satir" data-sira data-yeni-gizle>')
d = re.sub(r'(<div class="kb-tarih-sec" id="(?:bTarih|soTarih)" data-deger="[^"]*")(?! data-yeni-bos)', r'\1 data-yeni-bos', d)
d = re.sub(r'(data-alan="push-(?:baslik|metin)">)[^<]*(<)', r'\1\2', d)
d = re.sub(r'<span class="kp-resim" style="[^"]*"></span>', '<span class="kp-resim"></span>', d)
d = re.sub(r'(<div class="ksk-kart-alt">dadahaber\.com · )([^<]+)(</div>)', r'\1<span data-alan="baslik" data-yeni-metin="">\2</span>\3', d)
DUZ.write_text(_yazim.duzelt(d), encoding="utf-8")
print(f"satır {len(kayitlar)} · görselli {sum(1 for h in kayitlar if h.get('gorsel'))} · kategori {len(agac)} · yayında toplam {toplam}")
