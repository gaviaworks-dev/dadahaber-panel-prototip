#!/usr/bin/env python3
"""Haberler modülü · Dalga 2 sayfaları (d2-haberler) üretici.

Kullanım:
  python3 -I moduller/haberler/_uret_d2.py
  python3 -I araclar/menu_yaz.py --yalniz moduller/haberler

Yalnız bu klasöre YENİ sayfa yazar: vitrin, son-dakika, canli, canli-masa, dosyalar, dosya, gunun-5, inceleme,
yazarlar, yazar, surumler, kose-yazilari, kose-duzenle (t-kose). Lead'in pilot dosyalarına (index.html, duzenle.html, _uret.py) dokunmaz.
Sayfalar yalnız ortak bileşenlerle kurulur (ui-kit.html); sayfaya stil ya da betik yazılmaz.
Kaynaklar (yalnız okunur): public sözlük (yazarlar, haberler, son dakika), public sayfalar (Dada Bağlam, Dada Doğrula,
Günün 5'i, Dakika Dakika metinleri), veri/panel.json (personalar).
"""
import html, json, re
from pathlib import Path
import importlib.util as _iu
_sp = _iu.spec_from_file_location("_yazim", Path(__file__).resolve().parent / "_yazim.py"); _yazim = _iu.module_from_spec(_sp); _sp.loader.exec_module(_yazim)  # yazım kuralı (Beyar)

KOK = Path(__file__).resolve().parents[2]
PUB = KOK.parent / "dadahaber-prototip"
KLASOR = KOK / "moduller" / "haberler"
SITE = "https://gaviaworks-dev.github.io/dadahaber-prototip/"
soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))

def e(s): return html.escape(str(s), quote=True)
def I(ad, ek=""): return f'<i class="fa-solid {ad}{(" " + ek) if ek else ""}" aria-hidden="true"></i>'
def IB(ad): return f'<i class="fa-brands {ad}" aria-hidden="true"></i>'
def tr_slug(s):
    m = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiuCGIOSUAIU")
    return re.sub(r"[^a-z0-9]+", "-", s.translate(m).lower()).strip("-")
def bas_harf(ad): p = ad.split(); return (p[0][0] + (p[-1][0] if len(p) > 1 else "")).upper()
def g(p): return f"../../veri/gorsel/{p}.jpg"
def gk(p): return f"../../veri/gorsel/kucuk/{p}.jpg"

# ======================================================================= iskelet
def sayfa(dosya, baslik, anahtar, govde, sablonlar="", editor=False, body_ek=""):
    sc = ["kabuk", "bilesen", "form", "alan", "kirp"]
    js = "".join(f'<script src="../../cekirdek/js/{s}.js"></script>\n' for s in sc)
    if editor:
        js += '<script src="../../assets/vendor/tiptap-2.27.3/tiptap.min.js"></script>\n<script src="../../cekirdek/js/editor.js"></script>\n'
    t = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(baslik)} · Dada Haber Yönetim Paneli</title>
<link rel="stylesheet" href="../../assets/vendor/fontawesome-6.5.2/css/all.min.css">
<link rel="stylesheet" href="../../tema/dadahaber.css" data-tema>
<link rel="stylesheet" href="../../cekirdek/css/kabuk.css">
<link rel="stylesheet" href="../../cekirdek/css/bilesen.css">
<!--P:bas--><!--/P:bas-->
</head>
<body data-sayfa="{anahtar}"{body_ek}>
<div class="sa-app">
<!--P:menu--><!--/P:menu-->
<div class="pnl-overlay" id="pnlOverlay"></div>
<!--P:ust--><!--/P:ust-->

<main class="pnl-main" id="icerik">
{govde}
</main>
</div>
{sablonlar}
{js}</body>
</html>
'''
    (KLASOR / dosya).write_text(_yazim.duzelt(t), encoding="utf-8")
    return dosya

def bas(h1, alt, eylemler, h1_yeni=None, alt_yeni=None):
    y1 = f' data-yeni-metin="{e(h1_yeni)}"' if h1_yeni else ""
    y2 = f' data-yeni-metin="{e(alt_yeni)}"' if alt_yeni else ""
    return (f'  <div class="pnl-page-head">\n    <div>\n      <h1{y1}>{e(h1)}</h1>\n      <div class="ph-sub"{y2}>{alt}</div>\n    </div>\n'
            f'    <div class="ph-actions">\n      ' + "\n      ".join(eylemler) + '\n    </div>\n  </div>\n')

def a_hedef(metin, ikon, hedef, ek="", cls="btn-ghost", attr=""):
    ekk = f' data-hedef-ek="{e(ek)}"' if ek else ""
    return f'<a class="btn {cls} btn-sm" data-hedef="{hedef}"{ekk}{attr} href="#">{I(ikon)}{e(metin)}</a>'
def a_dis(metin, ikon, href, attr=""):
    return f'<a class="btn btn-ghost btn-sm"{attr} href="{e(href)}" target="_blank" rel="noopener">{I(ikon)}{e(metin)}</a>'
def btn(metin, ikon, cls="btn-ghost", attr=""):
    return f'<button type="button" class="btn {cls} btn-sm"{attr}>{I(ikon)}{e(metin)}</button>'

DIL_BTN = ('<div class="kb-dil" role="group" aria-label="İçerik dili">'
           '<button type="button" class="is-on" aria-pressed="true">TR · Türkçe</button>'
           + "".join(f'<button type="button" disabled title="Çeviri ekranları sonraki aşamada">{d}<span class="kd-etk">Sonraki aşama</span></button>' for d in ("EN", "AR", "DE"))
           + '</div>')
def dil(not_, kap=False):
    return (f'<div class="kb-form-bas{" kb-kap-dil" if kap else ""}">{DIL_BTN}'
            + (f'<span class="kfb-not">{I("fa-language")}{e(not_)}</span>' if not_ else "") + '</div>')

# ======================================================================= form parçaları
def cm(ipucu, n): return f'<div class="char-meter"><span>{e(ipucu)}</span><b>0 / {n}</b></div>'
def ferr(m): return f'<div class="ferr">{I("fa-circle-exclamation")}{e(m)}</div>' if m else ""
def girdi(id_, etiket, deger="", alan_id=None, sayac=None, ipucu="", ph="", hata=None, cls="finput", ek="", ipucu_alt=""):
    aid = f' data-alan-id="{alan_id}"' if alan_id else ""
    say = f' data-sayac="{sayac}"' if sayac else ""
    p = f' placeholder="{e(ph)}"' if ph else ""
    m = cm(ipucu, sayac.split("|")[0]) if sayac else (f'<span class="fhint">{ipucu_alt or e(ipucu)}</span>' if (ipucu or ipucu_alt) else "")
    return f'<div class="frow"><label for="{id_}">{e(etiket)}</label><input class="{cls}" id="{id_}"{aid}{say}{p}{ek} value="{e(deger)}">{m}{ferr(hata)}</div>'
def alan(id_, etiket, deger="", alan_id=None, sayac=None, ipucu="", ph="", hata=None, rows=3, ek=""):
    aid = f' data-alan-id="{alan_id}"' if alan_id else ""
    say = f' data-sayac="{sayac}"' if sayac else ""
    p = f' placeholder="{e(ph)}"' if ph else ""
    m = cm(ipucu, sayac.split("|")[0]) if sayac else (f'<span class="fhint">{e(ipucu)}</span>' if ipucu else "")
    return f'<div class="frow"><label for="{id_}">{e(etiket)}</label><textarea class="ftext" id="{id_}"{aid}{say}{p} rows="{rows}"{ek}>{e(deger)}</textarea>{m}{ferr(hata)}</div>'

def secim(id_, secenekler, deger=None, bos="Seçin", ara=None, alan_id=None, etk=None, suz=None, ek="", bos_metin=None, yeni_deger=None):
    """secenekler: (deger, ad, alt) | ('#grup', ad)"""
    ops = []
    for s in secenekler:
        if s[0] == "#grup": ops.append(f'<div class="ks-grup">{e(s[1])}</div>'); continue
        d, ad = s[0], s[1]; alt = s[2] if len(s) > 2 else ""
        sec = ' class="is-sec"' if deger is not None and d == deger and d != "" else ""
        ops.append(f'<button type="button" data-deger="{e(d)}" data-ad="{e(ad)}"{sec}>{e(ad)}' + (f'<span class="ks-alt">{e(alt)}</span>' if alt else "") + '</button>')
    goster = next((s[1] for s in secenekler if s[0] == deger and s[0] != "#grup"), None) if deger is not None else None
    dolu = " is-dolu" if goster and deger != "" else ""
    ad_ = ' data-alan-id="%s"' % alan_id if alan_id else ""
    sz = f' data-suz="{suz}"' if suz else ""
    dg = f' data-deger="{e(deger)}"' if goster and deger != "" else ""
    yd = f' data-yeni-deger="{e(yeni_deger)}"' if yeni_deger is not None else ""
    etiket = f'<span class="ks-etk">{e(etk)}</span>' if etk else ""
    ym = f' data-yeni-metin="{e(bos)}"' if yeni_deger == "" and goster and deger != "" else ""  # yeni kayıtta yer tutucu
    arab = (f'<div class="kb-secim-ara">{I("fa-magnifying-glass")}<input type="search" placeholder="{e(ara)}" aria-label="{e(ara)}"></div>' if ara else "")
    bosm = f'<div class="kb-secim-bos" hidden>{e(bos_metin or "Sonuç yok.")}</div>' if ara else ""
    return (f'<div class="kb-secim{dolu}"{sz}{ad_}{dg}{yd} data-bos="{e(bos)}"{ek}>'
            f'<button type="button" class="kb-secim-btn" data-acilir="{id_}" aria-expanded="false" aria-haspopup="listbox">{etiket}<span class="ks-deger"{ym}>{e(goster or bos)}</span>{I("fa-chevron-down")}</button>'
            f'<div class="pnl-menu kb-secim-menu" id="{id_}">{arab}<div class="kb-secim-liste" role="listbox">{"".join(ops)}</div>{bosm}</div></div>')

def tarih(id_, deger="", saatsiz=False, ek="", etiket="Tarih ve saat seç"):
    sz = " data-saatsiz" if saatsiz else ""
    dg = f' data-deger="{deger}"' if deger else ""
    if deger and "data-yeni-bos" not in ek: ek += " data-yeni-bos"  # yeni kayıt boş açılır (Beyar)
    return (f'<div class="kb-tarih-sec" id="{id_}"{dg}{sz}{ek}><button type="button" class="kb-tarih-btn" data-acilir="{id_}M" aria-expanded="false" aria-haspopup="dialog" aria-label="{e(etiket)}">{I("fa-calendar-days")}<span class="kt-deger"></span></button>'
            f'<div class="pnl-menu kb-tarih-menu" id="{id_}M" role="dialog" aria-label="{e(etiket)}"></div></div>')

def anahtar(baslik, alt, acik=True, ek="", kap_ek="", yeni=None):
    if yeni is not None: ek += f' data-yeni-isaret="{1 if yeni else 0}"'  # yeni kayıttaki hali (çekirdek isteği)
    return (f'<div class="toggle-row"{kap_ek}><span>{e(baslik)}<small>{e(alt)}</small></span><label class="toggle"><input type="checkbox"{" checked" if acik else ""}{ek} aria-label="{e(baslik)}"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>')

def editor(ad, icerik, alan_id=None, kisa=False, medya=False, zm=None, alt=None):
    a = (f' data-alan-id="{alan_id}"' if alan_id else "") + (f' data-zorunlu-metin="{e(zm)}"' if zm else "")
    return (f'<div class="kb-editor" data-editor-ad="{e(ad)}"{" data-editor-kisa" if kisa else ""}{" data-editor-medya" if medya else ""}>'
            f'<div class="kz-alan ke-alan"{a}>{icerik}</div>' + (f'<div class="kz-alt"><span data-kz-say></span><span>{e(alt)}</span></div>' if alt else "") + '</div>')

def km_satir(b, a, ad, ekler="", duzenle=True, tutamac=True):
    t = f'<button type="button" class="kb-tutamac" aria-label="Sırayı değiştir (sürükleyin ya da ok tuşları)">{I("fa-grip-vertical")}</button>' if tutamac else ""
    d = f'<button type="button" class="ia-btn" data-satir-duzenle aria-label="{e(ad)} düzenle" title="Düzenle">{I("fa-pen")}</button>' if duzenle else ""
    return (f'<div class="km-satir" data-sira data-yeni-gizle>{t}{ekler}<span class="km-yazi">{e(b)}' + (f'<small>{e(a)}</small>' if a else "") + '</span>'
            f'{d}<button type="button" class="ia-btn danger" data-satir-sil aria-label="{e(ad)} kaldır" title="Kaldır">{I("fa-trash")}</button></div>')
def satir_liste(ad, alan1, alan2, satirlar, ekle=None, siralanir=True, ek=""):
    s = " data-siralanir" if siralanir else ""
    return (f'<div class="kb-madde" data-satir-liste{s} data-satir-ad="{e(ad)}" data-satir-alan1="{e(alan1)}" data-satir-alan2="{e(alan2)}"{ek}>'
            + "".join(km_satir(b, a, ad, tutamac=siralanir) for b, a in satirlar)
            + (f'<button type="button" class="kb-ekle-btn" data-satir-ekle>{I("fa-plus")}{e(ekle)}</button>' if ekle else "") + '</div>')

def fs(baslik, ikon, ic, ek_bas="", attr=""):
    eb = f'<span class="fs-ek">{ek_bas}</span>' if ek_bas else ""
    return f'<div class="form-sec"{attr}><div class="form-sec-tt">{I(ikon)}{e(baslik)}{eb}</div>{ic}</div>'
def grid(*parcalar, cls=""): return f'<div class="form-grid{(" " + cls) if cls else ""}">' + "".join(parcalar) + '</div>'
def frow(etiket, ic, ipucu="", hata=None, attr=""):
    return f'<div class="frow"{attr}><span class="flabel">{e(etiket)}</span>{ic}' + (f'<span class="fhint">{ipucu}</span>' if ipucu else "") + ferr(hata) + '</div>'
def cip(v): return f'<span class="kb-cip" data-deger="{e(v)}"><span>{e(v)}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>'
def cip_girdi(degerler, havuz, ph, ek="", serbest=False):
    hv = "" if serbest else f" data-havuz='{e(json.dumps(havuz, ensure_ascii=False))}'"
    sb = " data-serbest" if serbest else ""
    return (f'<div class="kb-cip-girdi"{sb}{hv}{ek}>' + "".join(cip(v) for v in degerler)
            + f'<input type="text" placeholder="{e(ph)}" aria-label="{e(ph)}">' + ('' if serbest else '<div class="pnl-menu kb-cip-oneri"></div>') + '</div>')

def ai_adim(kaynak, secenekler, durum="Başlığı ve spotu yazın; işaretli bölümler bunlardan üretilir. Üretilen her bölüm “AI önerisi” etiketiyle gelir, gözden geçirip düzeltirsiniz.", neden="Önce başlık ve spot"):
    ops = "".join(f'<label class="kb-secenek"{(" data-modul=" + chr(34) + m + chr(34)) if m else ""}><input type="checkbox" value="{v}"{" checked" if c else ""}>{e(l)}</label>' for v, l, c, m in secenekler)
    return (f'<div class="kb-ai-adim" data-ai-adim data-ai-kaynak="{kaynak}" data-yeni-goster hidden><div class="kaa-bas"><span class="kaa-ikon">{I("fa-wand-magic-sparkles")}</span>'
            f'<div><b>Gerisini AI ile üret</b><span data-ai-durum>{e(durum)}</span></div></div>'
            f'<div class="kaa-secim" role="group" aria-label="Üretilecek bölümler">{ops}</div>'
            f'<div class="kaa-alt"><button type="button" class="btn btn-acc btn-sm" data-ai-uret disabled>{I("fa-wand-magic-sparkles")}Gerisini Üret</button><span class="fhint" data-ai-neden>{e(neden)}</span></div></div>')

BOLUMLER = ["Gündem", "Spor", "Finans", "Kadın", "Savunma", "Dünya", "Kampüs", "Keşfet", "Köşe"]
ALTLAR = {"Gündem": ["Siyaset", "Türkiye", "Toplum", "Hukuk", "Güvenlik", "Eğitim", "Çevre", "Afet", "Yerel Haberler", "İstanbul", "Ankara", "İzmir"],
          "Finans": ["Türkiye Ekonomisi", "Bankacılık", "Kişisel Finans", "Enflasyon", "Çalışma Hayatı", "Enerji", "Gayrimenkul", "Faiz Oranları"],
          "Savunma": ["Savunma Sanayii", "Millî Projeler", "Hava Platformları", "Deniz Platformları"],
          "Dünya": ["Avrupa", "Orta Doğu", "Diplomasi", "Göç", "Küresel Siyaset"],
          "Kampüs": ["Eğitim ve Sınavlar", "YKS", "KPSS", "Üniversiteler"],
          "Keşfet": ["İklim", "Teknoloji", "Yapay Zekâ", "Bilim", "Sağlık", "Otomobil", "Dada Bağlam", "Dada Doğrula", "Günün 5'i"],
          "Spor": ["Futbol", "Basketbol", "Millî Takım", "Süper Lig"], "Kadın": ["Kadın Gündemi", "Kadın ve Çalışma Hayatı"], "Köşe": []}
def kat_secenek(): return [(b, b, f"{len(ALTLAR.get(b, []))} alt konu") for b in BOLUMLER]
def kategori_alanlari(id_, ana, altlar):
    return (f'<div class="frow two"><div class="frow"><span class="flabel">Ana Kategori</span>'
            + secim(id_ + "Kat", kat_secenek(), ana, "Kategori seçin", "Kategori ara", alan_id="kategori", ek=f' id="{id_}KatSecim"', bos_metin="Bu adla kategori yok.")
            + '<span class="fhint">Adres ve SEO ana kategoriye göre kurulur.</span>' + ferr("Ana kategori zorunlu.") + '</div>'
            + '<div class="frow"><span class="flabel">Alt Konular</span>'
            + cip_girdi(altlar, ALTLAR.get(ana, []), "Alt konu ara", ek=f' data-alan-id="alt-konu" data-birincil data-havuz-kapali data-ana-kaynak="#{id_}KatSecim" data-alt-harita="{e(json.dumps(ALTLAR, ensure_ascii=False))}"')
            + '<span class="fhint">İlk seçilen ana alt konudur; yeni alt konu Kategoriler’den eklenir.</span></div></div>')

YAZARLAR = soz["yazarlar"]
def yazar_secenek():
    o, son = [], None
    for y in YAZARLAR:
        if y["alan"] != son: o.append(("#grup", y["alan"])); son = y["alan"]
        o.append((y["ad"], y["ad"]))
    return o
def yazar_alani(id_, ad):
    return frow("Yazar", secim(id_, yazar_secenek(), ad, "Yazar seçin", "Yazar ara", alan_id="yazar", ek=" data-oturum-yazar", bos_metin="Bu adla yazar yok."),
                ipucu="Boş bırakılırsa oturumdaki kişi yazılır.")

def kapak(id_, gorsel, odak, kaynak, altyazi, yukle_not="Web görseli yüklenince mobil görsel ondan otomatik kırpılır · önerilen en az 1280×533"):
    ox, oy = odak
    st = f"background-image:url({g(gorsel)});background-position:{ox}% {oy}%"
    return (f'<div class="form-sec" id="{id_}" data-alan-id="kapak" data-zorunlu-metin="Kapak görseli yükleyin ya da havuzdan seçin" data-gorsel-alan="haberler.kapak" data-gorsel-ad="Kapak Görseli" data-kirp-sonra>'
            f'<div class="form-sec-tt">{I("fa-image")}Kapak Görseli<span class="fs-ek" data-yeni-gizle>{e(kaynak)}</span></div>'
            f'<div class="kb-yukle" data-yeni-goster data-gorsel-bos hidden>{I("fa-cloud-arrow-up")}<b>Kapak görselini sürükleyin ya da seçin</b><span>{e(yukle_not)}</span><span class="kg-acts">'
            f'<button type="button" class="btn btn-acc btn-sm" data-gorsel-yukle>{I("fa-upload")}Bilgisayardan yükle</button><button type="button" class="btn btn-ghost btn-sm" data-medya-sec>{I("fa-photo-film")}Havuzdan Seç</button></span></div>'
            f'<div class="kb-gorsel" data-yeni-gizle data-gorsel-dolu><div class="kg-bolum"><div class="kg-bas">{I("fa-desktop")}Web</div><div class="kg-ikili">'
            f'<div class="kg-resim r-detay" data-gorsel-hedef="web" data-kirp-oran="web.detay" style="{st}"><span class="kg-odak" style="left:{ox}%;top:{oy}%"></span><span class="kg-etk">Detay · 2.4:1</span></div>'
            f'<div class="kg-resim r-kart" data-gorsel-hedef="web" data-kirp-oran="web.kart" style="{st}"><span class="kg-etk">Kart · 16:10</span></div></div>'
            f'<div class="kg-olcu">Önerilen: detay <b>1280×533</b>, kart <b>308×193</b> (sitenin görünen genişliği). <span data-gorsel-bilgi>Yüklenen: 1200×800 JPG.</span></div>'
            f'<div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{I("fa-crop-simple")}Kırp ve Odak</button><button type="button" class="btn btn-ghost btn-sm" data-medya-sec>{I("fa-photo-film")}Havuzdan Seç</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{I("fa-upload")}Yükle</button><button type="button" class="btn btn-ghost btn-sm danger" data-gorsel-kaldir>{I("fa-trash")}Kaldır</button></div></div>'
            f'<div class="kg-bolum"><div class="kg-bas">{I("fa-mobile-screen")}Mobil<span class="kg-oto">{I("fa-wand-magic-sparkles")} Webden kırpıldı</span></div>'
            f'<div class="kg-resim r-kart" data-gorsel-hedef="mobil" data-kirp-oran="mobil.kart" style="{st}"><span class="kg-odak" style="left:{ox}%;top:{oy}%"></span><span class="kg-etk">Mobil kart · 16:10</span></div>'
            f'<div class="kg-olcu">Önerilen: <b>358×224</b> (sitenin telefon görünümü). Aynı odak noktası kullanılır.</div>'
            f'<div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac="mobil.kart">{I("fa-crop-simple")}Kırp</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle data-gorsel-kapsam="mobil">{I("fa-upload")}Ayrı Görsel Yükle</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-webe-don hidden>{I("fa-rotate-left")}Webden kırpılana dön</button></div></div></div>'
            + f'<div class="frow kb-ust-bosluk"><label for="{id_}Alt">Görsel Altyazısı ve Kaynağı</label><input class="finput" id="{id_}Alt" data-sayac="120|160" value="{e(altyazi)}">{cm("Görselin altında ve erişilebilirlik metninde", 120)}</div></div>')

def sekmeler(liste, aria="Düzenleme sekmeleri"):
    o = []
    for i, (pid, ad, ikon, mod) in enumerate(liste):
        m = f' data-modul="{mod}"' if mod else ""
        o.append(f'<button type="button" class="sa-form-tab{" is-on" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-panel="{pid}"{m}>{I(ikon)}{e(ad)}</button>')
    return f'<div class="sa-form-tabs" role="tablist" aria-label="{e(aria)}">' + "".join(o) + '</div>'
def panel(pid, ic, ilk=False, attr=""):
    return f'<div class="sa-form-panel" id="{pid}" role="tabpanel"{attr}{"" if ilk else " hidden"}>{ic}</div>'

def seo_panel(seo_b, seo_a, pre, slug, kelimeler, onek=""):
    return panel(f"{onek}pSeo", fs("Otomatik Üretildi", "fa-wand-magic-sparkles", grid(
        girdi(f"{onek}sBaslik", "SEO Başlığı", seo_b, sayac="60|70", ipucu="Arama sonucunda görünen başlık · 50–60 karakter önerilir", ek=' data-alan="seo-baslik"'),
        alan(f"{onek}sAciklama", "SEO Açıklaması", seo_a, sayac="155|170", ipucu="Arama sonucunda başlığın altında · 120–155 karakter önerilir", ek=' data-alan="seo-aciklama"', rows=3),
        f'<div class="frow"><label for="{onek}sSlug">Adres</label><div class="slug-wrap"><span class="slug-pre">{e(pre)}</span><input class="finput" id="{onek}sSlug" data-alan="slug" value="{e(slug)}"></div><span class="fhint">Yayımlandıktan sonra değiştirilirse eski adres yeniye yönlendirilir.</span></div>',
        frow("Anahtar Kelimeler", cip_girdi(kelimeler, [], "Yazın; Enter ya da virgülle ekleyin", serbest=True)),
        frow("Arama Sonucu Önizlemesi", f'<div class="serp"><div class="serp-url"><span class="serp-fav kb-logo-isaret"></span><span>{e(pre.replace("/", " › ").rstrip(" › "))} › <span data-alan="slug">{e(slug)}</span></span></div><div class="serp-title" data-alan="seo-baslik">{e(seo_b)}</div><div class="serp-desc" data-alan="seo-aciklama">{e(seo_a)}</div></div>'),
        anahtar("Google Haberler ve Discover'a Uygun", "NewsArticle şeması ve büyük görsel önizlemesi açık")),
        ek_bas=f'<button type="button" class="btn btn-ghost btn-sm" data-seo-uret>{I("fa-rotate")}Başlıktan Yeniden Üret</button>'), attr=' data-ai-grup="seo"')

def bildirim_panel(onek, baslik, metin, ek_secim=""):
    return panel(f"{onek}pBildirim", f'<div class="form-sec"><div>' + grid(
        frow("Kanallar", '<div class="kb-secenek-grup"><label class="kb-secenek"><input type="checkbox" checked>Telefon Bildirimi</label><label class="kb-secenek"><input type="checkbox" checked>Web Bildirimi</label></div>', ipucu="Mobil uygulama gelene kadar telefon bildirimi web üzerinden gider. Bildirim bütün abonelere gider."),
        ek_secim,
        f'<div class="frow"><label for="{onek}bBaslik">Bildirim Başlığı</label><input class="finput" id="{onek}bBaslik" data-alan="push-baslik" data-sayac="60|65" value="{e(baslik)}"><div class="kb-cubuk"><span></span></div>{cm("Telefonda kalın satır · 60 karaktere kadar tam görünür", 60)}</div>',
        f'<div class="frow"><label for="{onek}bIcerik">Bildirim Metni</label><textarea class="ftext" id="{onek}bIcerik" data-alan="push-metin" data-sayac="150|178">{e(metin)}</textarea><div class="kb-cubuk"><span></span></div>{cm("Kilit ekranında 3 satıra kadar · 150 karakter önerilir", 150)}</div>',
        anahtar("Bildirim Görseli", "Kapak görselinin mobil kırpımı kullanılır (2:1)"),
        frow("Ne Zaman", f'<div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="{onek}bZaman" checked>Kaydedince Hemen</label><label class="kb-secenek"><input type="radio" name="{onek}bZaman" data-ac="{onek}bZamanSec">Zamanla</label></div><div id="{onek}bZamanSec" hidden>' + tarih(f"{onek}bTarih", "2026-11-23 18.30", ek=' data-enaz="bugun"') + '</div>')) + '</div></div>', attr=' data-ai-grup="bildirim"')

def sosyal_panel(onek, kapak_id, gorsel, odak, metinler, link):
    P = [("x", "X", IB("fa-x-twitter"), "Dada Haber", "@dadahaber", "280", ' data-link-uzunluk="23"', "ok", "16:9=1200×675,1:1=1080×1080,serbest"),
         ("facebook", "Facebook", IB("fa-facebook"), "Dada Haber", "Facebook sayfası", "2000", "", "ok", "1.91:1=1200×630,1:1=1080×1080,serbest"),
         ("linkedin", "LinkedIn", IB("fa-linkedin"), "Dada Haber", "Medya · 12.400 takipçi", "3000", "", "ok", "1.91:1=1200×627,1:1=1200×1200,serbest"),
         ("instagram", "Instagram", IB("fa-instagram"), "dadahaber", "İstanbul", "2200", "", "hata", "1:1=1080×1080,4:5=1080×1350,serbest"),
         ("telegram", "Telegram", IB("fa-telegram"), "Dada Haber", "kanal · 48.200 abone", "4096", "", "ok", "16:9=1280×720,1:1=1080×1080,serbest")]
    pb = "".join(f'<button type="button" class="kb-platform{" is-on" if i == 0 else ""}" role="tab" data-platform="{p}" data-ad="{e(a)}" data-tutamac="{e(t)}" data-sinir="{s}"{l} data-hesap-durum="{d}" data-oranlar="{o}" data-metin="{e(metinler[p])}">{ik}{n}<span class="kp-durum{" hata" if d == "hata" else ""}"></span></button>'
                 for i, (p, n, ik, a, t, s, l, d, o) in enumerate(P))
    ox, oy = odak
    return panel(f"{onek}pSosyal", f'<div class="form-sec kb-sosyal"><div class="kb-platformlar" role="tablist" aria-label="Platformlar">{pb}</div><div class="kb-ust-bosluk">' + grid(
        '<div class="kb-hesap-kutu"><span class="kh-ava kb-logo-isaret"></span><div><b data-sosyal-ad>Dada Haber</b><span data-sosyal-tutamac>@dadahaber</span></div><span class="pstat ok" data-sosyal-hesap>Bağlı</span></div>',
        f'<div class="frow" data-sosyal-uyari hidden><div class="kb-hata-not">{I("fa-triangle-exclamation")}Instagram bağlantısının süresi doldu. Gönderi hazırlanabilir ama hesap yeniden bağlanana kadar yayımlanmaz.<a data-hedef="sosyal-medya.hesaplar" href="#">Hesabı Bağla</a></div></div>',
        f'<div class="frow"><label for="{onek}soMetin">Gönderi Metni<button type="button" class="btn btn-ghost btn-sm kb-sag" data-sosyal-uret>{I("fa-wand-magic-sparkles")}Yeniden üret</button></label><div class="kb-sosyal-kutu"><div class="kb-sosyal-arac" role="toolbar" aria-label="Gönderi metni biçimi" data-sosyal-arac></div><textarea class="ftext" id="{onek}soMetin" data-sosyal-metin data-oneri rows="7"></textarea></div><div class="kb-cubuk"><span></span></div><div class="char-meter kb-sosyal-say"><span class="kb-sayaclar"></span><b>0 / 280</b></div><p class="fhint kb-sa-not" data-sosyal-not></p></div>',
        f'<div class="kb-sosyal-ek" data-sosyal-ek hidden><div class="frow" data-sosyal-ek-alan="konum"><label for="{onek}soKonum">Konum</label><input class="finput" id="{onek}soKonum" data-oneri="konum" placeholder="Konum ara: İstanbul, Ankara…" autocomplete="off"><span class="fhint">Platformun kendi konum etiketi; gönderinin üstünde görünür</span></div><div class="frow" data-sosyal-ek-alan="gorselde-etiket"><label for="{onek}soGorselEt">Görselde Etiketlenecek Hesaplar</label><input class="finput" id="{onek}soGorselEt" data-oneri placeholder="@ yazın: hesap ara" autocomplete="off"><span class="fhint">Instagram\'ın "kişileri etiketle" özelliği</span></div></div>',
        f'<div class="frow"><span class="flabel">Görsel Oranı<span class="fhint kb-sag" data-oran-not></span></span><div class="kb-oranlar"></div><div class="kb-kirp-alan"><span class="kk-resim" style="background-image:url({g(gorsel)})"></span><span class="kk-cerceve" data-kirp-izle="sosyal.16:9" style="background-image:url({g(gorsel)});background-position:{ox}% {oy}%"></span></div><span class="fhint">Kapak görselinin odak noktasına göre otomatik kırpıldı. <button type="button" class="kb-bag" data-kirp-ac="sosyal.16:9" data-kirp-alan="#{kapak_id}">Kırpmayı düzenle</button></span></div>',
        frow("Yayın", f'<div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="{onek}soZaman" checked>Kaydedince Hemen</label><label class="kb-secenek"><input type="radio" name="{onek}soZaman" data-ac="{onek}soZamanSec">Zamanla</label><label class="kb-secenek"><input type="radio" name="{onek}soZaman">Bu Platformda Paylaşma</label></div><div id="{onek}soZamanSec" hidden>' + tarih(f"{onek}soTarih", "2026-11-23 17.00", ek=' data-enaz="bugun"') + '</div>')) + '</div></div>', attr=' data-ai-grup="sosyal"')

def yan_onizleme(onek, push_b, push_m, gorsel, ox, oy, kart_alt):
    return (f'<div class="kb-yan-onizle" data-panel-icin="{onek}pBildirim" hidden><section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{I("fa-mobile-screen")}Bildirim önizlemesi</h2></div><div class="pc-body"><div class="kb-onizle-kap">'
            f'<div class="kb-onizle-sec" data-segment><button type="button" class="is-on" data-hedef="{onek}onzTel" aria-pressed="true">Telefon</button><button type="button" data-hedef="{onek}onzWeb" aria-pressed="false">Web</button></div>'
            f'<div id="{onek}onzTel"><div class="kb-telefon"><div class="kb-telefon-ekran"><div class="kt-zaman">16.05</div><div class="kt-tarih">23 Kasım Pazartesi</div><div class="kb-push"><span class="kp-ikon kb-logo-isaret"></span><div class="kp-ic"><div class="kp-ust"><span>DADA HABER</span><span>şimdi</span></div><b data-alan="push-baslik"></b><p data-alan="push-metin"></p></div><span class="kp-resim"></span></div></div></div></div>'
            f'<div id="{onek}onzWeb" hidden><div class="kb-web-push"><span class="kp-ikon kb-logo-isaret"></span><div><b data-alan="push-baslik"></b><p data-alan="push-metin"></p><small>dadahaber.com · Chrome</small></div></div></div>'
            f'<p class="kb-onizle-not">Önizleme yaklaşıktır; telefonun ve tarayıcının görünümüne göre değişir.</p></div></div></section></div>'
            f'<div class="kb-yan-onizle" data-panel-icin="{onek}pSosyal" hidden><section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{I("fa-eye")}Canlı önizleme</h2><span class="kb-kap-alt" data-sosyal-ad-platform></span></div><div class="pc-body"><div class="kb-onizle-kap"><div class="kb-sosyal-kart p-x" data-sosyal-onizle><div class="ksk-tg">'
            f'<div class="ksk-bas"><span class="kh-ava kb-logo-isaret"></span><div><b><span data-sosyal-ad>Dada Haber</span>{I("fa-circle-check")}</b><span data-sosyal-tutamac>@dadahaber</span> · 1 dk</div>{I("fa-ellipsis", "ksk-noktalar")}</div>'
            f'<div class="ksk-metin"></div><div class="ksk-gorsel" style="background-image:url({g(gorsel)});background-position:{ox}% {oy}%"></div><div class="ksk-kart-alt">dadahaber.com · <span data-alan="baslik" data-yeni-metin="">{e(kart_alt)}</span></div>'
            f'<div class="ksk-eylem"><i class="fa-regular fa-comment" aria-hidden="true"></i>{I("fa-retweet")}<i class="fa-regular fa-heart" aria-hidden="true"></i>{I("fa-chart-simple")}<i class="fa-regular fa-bookmark" aria-hidden="true"></i></div></div></div><p class="kb-onizle-not">Platformun gerçek görünümüne yakındır</p></div></div></section></div>')

def yayin_karti(id_, durumlar, durum, tarih_deger, ekler="", surum=None, baslik="Yayın", yeni_durum="taslak", tarih_bos="Yayımlanınca o anın saati", tarih_etk="Yayın Zamanı"):
    st = {"yayinda": "Yayında", "taslak": "Taslak", "zamanli": "Zamanlanmış", "canli": "Canlı", "bitti": "Sona Erdi"}
    sr = (f'<div class="kb-surum" data-yeni-gizle><span><b>{surum[0]}</b> · {e(surum[1])}</span><a class="kb-bag" data-hedef="haberler.surumler"{(" data-hedef-ek=" + chr(34) + e(surum[2]) + chr(34)) if len(surum) > 2 else ""} href="#">Sürüm geçmişi ve düzeltmeler</a></div>' if surum else "")
    return (f'<section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{I("fa-paper-plane")}{e(baslik)}</h2><span class="status-dot" data-state="{durum}" data-yeni-durum="{yeni_durum}" title="{e(st.get(durum, durum))}"></span></div>'
            f'<div class="pc-body sc-stack"><div class="sc-field"><span class="flabel">Durum</span>' + secim(id_ + "Durum", durumlar, durum, "Taslak", yeni_deger=yeni_durum) + '</div>'
            f'<div class="sc-field"><span class="flabel">{e(tarih_etk)}</span>' + tarih(id_ + "Tarih", tarih_deger, ek=f' data-yeni-bos data-bos="{e(tarih_bos)}" data-temizlenir="1"') + '</div>'
            + ekler + sr + '</div></section>')

def seo_skor(puan, kontroller, onek=""):
    ch = "".join(f'<div class="seo-chk {"pass" if ok else "fail"}">{I("fa-circle-check") if ok else chr(60) + "i class=" + chr(34) + "fa-regular fa-circle" + chr(34) + " aria-hidden=" + chr(34) + "true" + chr(34) + "></i>"}{e(m)}</div>' for ok, m in kontroller)
    ad = "İyi" if puan >= 80 else "Orta" if puan >= 60 else "Zayıf"
    return (f'<section class="pnl-card" data-one-cik="{onek}pSeo"><div class="pc-head"><h2 class="pc-title">{I("fa-gauge")}SEO Skoru</h2></div><div class="pc-body">'
            f'<p class="fhint" data-yeni-goster hidden>Skor, başlık, spot ve görsel girilince hesaplanır.</p>'
            f'<div class="seo-score" data-yeni-gizle><div class="score-ring" style="--p:{puan}"><span class="score-num">{puan}</span></div><div class="score-meta"><b>{ad}</b><span>Eksikler giderilince yükselir</span></div></div>'
            f'<div class="seo-checks" data-yeni-gizle>{ch}</div></div></section>')

def kaydet(form_id, durum, ana, bildir, yeni_ana=None, yeni_bildir=None, taslak=True, yeni_durum="Henüz kaydedilmedi", taslak_bildir="Taslak kaydedildi; yayındaki hal değişmedi", ek_ana=""):
    ya = f' data-yeni-bildir="{e(yeni_bildir)}"' if yeni_bildir else ""
    ym = f'<span data-yeni-metin="{e(yeni_ana)}">{e(ana)}</span>' if yeni_ana else e(ana)
    t = (f'<button type="button" class="btn btn-ghost btn-sm" data-kaydet data-kaydet-tur="taslak" data-kaydet-metin="Taslak olarak kaydedildi" data-bildir="{e(taslak_bildir)}">{I("fa-floppy-disk")}Taslak Kaydet</button>' if taslak else "")
    return (f'  <div class="kb-kaydet" data-form-icin="{form_id}"><div class="kk-durum">{I("fa-circle-check")}<span data-yeni-metin="{e(yeni_durum)}">{e(durum)}</span></div>'
            f'<div class="kk-sag">{t}<button type="button" class="btn btn-acc btn-sm" data-kaydet data-kaydet-metin="Kaydedildi" data-bildir="{e(bildir)}"{ya}{ek_ana}>{I("fa-check")}{ym}</button></div></div>\n')

def sablon(id_, baslik, alt, ic, zorunlu=None):
    z = f' data-zorunlu-kayit="{zorunlu}"' if zorunlu else ""
    return f'<template id="{id_}"{z} data-baslik="{e(baslik)}" data-alt="{e(alt)}">\n{ic}\n</template>\n'
def kfs(baslik, ic): return f'<div class="kb-fs"><div class="kb-fs-tt">{e(baslik)}</div>{ic}</div>'
def alt_cubuk(*b): return '<div class="kb-kap-alt-cubuk">' + "".join(b) + '</div>'

# ======================================================================= liste
def liste(ad, aria, sekme_list, ara_ph, suzler, toplu, basliklar, satirlar, menu, bos, bilgi, cop=True, sayfa_boy=25, attr="", liste_cop_not=None, bant="", kap=True):
    ch = []
    for i, (s, n, taban) in enumerate(sekme_list):
        ch.append(f'<button type="button" class="chip{" is-on" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-sekme="{s}" data-taban="{taban}">{e(n)}<span class="ch-cnt">0</span></button>')
    copb = f'<button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop" data-taban="0">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>' if cop else ""
    sz = "".join(secim(i, ops, None, "Tümü", ara, etk=etk + ":", suz=k, bos_metin="Sonuç yok.") for k, etk, i, ops, ara in suzler)
    tp = (f'<div class="kb-toplu" hidden><b data-secili-say>0 {e(ad)} seçildi</b><span class="kb-toplu-ayir"></span>' + "".join(toplu)
          + '<button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button></div>') if toplu else ""
    hd = "".join(f'<th{(" class=" + chr(34) + c + chr(34)) if c else ""}>{h}</th>' for h, c in basliklar)
    n = len(basliklar)
    isk = "".join('<tr class="kb-iskelet">' + "".join('<td></td>' if j in (0, n - 1) and toplu else ('<td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td>' if j == (1 if toplu else 0) else '<td><span></span></td>') for j in range(n)) + '</tr>' for _ in range(4))
    cn = f' data-liste-cop-not="{e(liste_cop_not)}"' if liste_cop_not else ""
    etk_ = "section" if kap else "div"
    return (f'<{etk_}{" class=" + chr(34) + "pnl-card" + chr(34) if kap else ""} data-liste data-liste-ad="{e(ad)}" data-sayfa-boy="{sayfa_boy}"{cn} aria-label="{e(aria)}"{attr}>\n'
            f'<h2 class="sr-only">{e(aria)}</h2>'
            f'<div class="kb-liste-ust"><div class="chips" role="tablist" aria-label="Duruma göre">{"".join(ch)}</div>{copb}</div>\n'
            + (f'<div class="form-sec">{bant}</div>' if bant else "") +
            f'<div class="filter-bar"><div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="{e(tr_slug(aria))}Ara">{e(ara_ph)}</label><input id="{e(tr_slug(aria))}Ara" type="search" data-liste-ara placeholder="{e(ara_ph)}" autocomplete="off"></div>{sz}'
            f'<button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button></div>\n{tp}\n'
            f'<div class="ptable-wrap"><table class="ptable"><thead><tr>{hd}</tr></thead>\n<tbody data-satirlar>{"".join(satirlar)}</tbody>\n'
            f'<tbody><tr class="kb-bos-satir" hidden><td colspan="{n}"><div class="pnl-empty"><div class="pe-ico">{I("fa-magnifying-glass")}</div><h2>Bu süzgeçlerle sonuç yok</h2><p>Arama metnini kısaltmayı ya da süzgeçleri kaldırmayı deneyin.</p><button type="button" class="pe-tag" data-suz-temizle>{I("fa-filter-circle-xmark")}Süzgeçleri temizle</button></div></td></tr></tbody>\n'
            f'<tbody data-durum-goster="yukleniyor" hidden>{isk}</tbody>\n'
            f'<tbody data-durum-goster="hata" hidden><tr><td colspan="{n}"><div class="pnl-empty kb-hata"><div class="pe-ico">{I("fa-triangle-exclamation")}</div><h2>{e(bos["hata"])}</h2><p>Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin; sorun sürerse sistem yöneticisine haber verin.</p><a class="pe-tag" href="{bos["dosya"]}">{I("fa-rotate-right")}Yeniden dene</a></div></td></tr></tbody>\n'
            f'<tbody data-durum-goster="bos" hidden><tr><td colspan="{n}"><div class="pnl-empty"><div class="pe-ico">{I(bos["ikon"])}</div><h2>{e(bos["baslik"])}</h2><p>{e(bos["metin"])}</p>{bos["eylem"]}</div></td></tr></tbody>\n'
            f'</table></div>\n'
            f'<div class="pnl-menu kb-diger-menu" role="menu">{menu}</div>\n</{etk_}>\n')

def tr(kimlik, durum, ara, baslik, hucreler, eylemler, href=None, secim_kutu=True, **data):
    d = {"satir": kimlik, "durum": durum, "ara": ara, "baslik": baslik}
    if href: d["href"] = href
    d.update({k.replace("_", "-"): v for k, v in data.items()})
    nit = " ".join(f'data-{k}="{e(v)}"' for k, v in d.items())
    sk = f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(baslik)}"></td>' if secim_kutu else ""
    hc = "".join(f'<td{(" class=" + chr(34) + c + chr(34)) if c else ""}>{h}</td>' for h, c in hucreler)
    return f'<tr {nit}>{sk}{hc}<td><div class="row-acts">{eylemler}</div></td></tr>'
def ana_hucre(baslik, alt, thumb=None, ava=None, alt_ham=False):
    if ava is not None: t = ava
    elif thumb: t = f'<span class="rcp-thumb" style="background-image:url({gk(thumb)})"></span>'
    elif thumb is False: t = f'<span class="rcp-thumb kb-yok" title="Görsel eksik">{I("fa-image")}</span>'
    else: t = ""
    return (f'<div class="rcp-cell">{t}<div class="rcp-id"><div class="rcp-name" title="{e(baslik)}">{e(baslik)}</div><div class="rcp-by">{alt if alt_ham else e(alt)}</div></div></div>', "kb-ana")
def kat_hucre(b, a=None):
    return (f'<span class="kb-kat"><b>{e(b)}</b>' + (f'{I("fa-chevron-right")}{e(a)}' if a else "") + '</span>', "kb-gizle-m")
def rozet(cls, m): return f'<span class="pstat {cls}">{e(m)}</span>'
def isaret_sabit(bildir_on, bildir_off, secili=False):  # KURAL: tek tıkla işaretleme aynı yerden geri alınır (çekirdek kb-isaret)
    return (f'<button type="button" class="kb-isaret" data-isaret="sabit" data-isaret-on="Sabit" data-isaret-off="Sabitle" data-isaret-ikon="fa-thumbtack" '
            f'data-isaret-bildir-on="{e(bildir_on)}" data-isaret-bildir-off="{e(bildir_off)}" aria-pressed="{"true" if secili else "false"}"></button>')
def ia_a(href, etk, ikon, dis=False):
    t = ' target="_blank" rel="noopener"' if dis else ""
    return f'<a class="ia-btn" href="{e(href)}"{t} aria-label="{e(etk)}" title="{e(etk)}">{I(ikon)}</a>'
def ia_tanim(tid, etk, ikon): return f'<button type="button" class="ia-btn" data-tanim="{tid}" aria-label="{e(etk)}" title="{e(etk)}">{I(ikon)}</button>'
SIL = f'<button type="button" class="ia-btn danger" data-sil aria-label="Çöpe Taşı" title="Çöpe Taşı">{I("fa-trash")}</button>'
DIGER = f'<button type="button" class="ia-btn" data-diger aria-haspopup="true" aria-expanded="false" aria-label="Diğer işlemler" title="Diğer">{I("fa-ellipsis")}</button>'
def kilit(neden): return f'<button type="button" class="ia-btn kb-kilit" disabled aria-label="{e(neden)}" title="{e(neden)}">{I("fa-lock")}</button>'
def m_grup(ad, durum=None): return f'<div class="kb-dm-grup"{(" data-durum-icin=" + chr(34) + durum + chr(34)) if durum else ""}>{e(ad)}</div>'
def m_ayir(durum=None): return f'<div class="pmenu-div"{(" data-durum-icin=" + chr(34) + durum + chr(34)) if durum else ""}></div>'
def m_btn(metin, ikon, durum=None, attr="", cls=""):
    d = f' data-durum-icin="{durum}"' if durum else ""
    c = f' class="{cls}"' if cls else ""
    return f'<button type="button"{c}{d}{attr}>{I(ikon)}{e(metin)}</button>'
def m_a(metin, ikon, hedef, ek="", attr=""):
    ekk = f' data-hedef-ek="{e(ek)}"' if ek else ""
    return f'<a data-hedef="{hedef}"{ekk}{attr} href="#">{I(ikon)}{e(metin)}</a>'
def onay(baslik, metin, evet, tehlike=False, ikon=None, kod=False, sonra=None, bildir=None):
    a = f' data-onay-baslik="{e(baslik)}" data-onay-metin="{e(metin)}" data-onay-evet="{e(evet)}"'
    if tehlike: a += " data-onay-tehlike"
    if ikon: a += f' data-onay-ikon="{ikon}"'
    if kod: a += " data-kod"
    if sonra: a += f' data-sonra-durum="{sonra[0]}" data-sonra-durum-ad="{e(sonra[1])}" data-sonra-durum-sinif="{sonra[2]}"'
    if bildir: a += f' data-bildir-sonra="{e(bildir)}"'
    return a
COP_MENU = (m_ayir("cop") + m_btn("Çöpten geri al", "fa-rotate-left", "cop", " data-geri-al")
            + m_btn("Kalıcı Olarak Sil", "fa-trash-can", "cop", " data-kalici-sil", cls="danger"))
DENETIM = f'<a data-hedef="denetim-izi.liste" data-roller="super gyy" href="#">{I("fa-clipboard-list")}Denetim izinde gör</a>'
def bos_durum(dosya, hata, ikon, baslik, metin, eylem): return {"dosya": dosya, "hata": hata, "ikon": ikon, "baslik": baslik, "metin": metin, "eylem": eylem}
def yan(*kartlar): return '<aside class="side-card" aria-label="Yan panel">' + "".join(kartlar) + '</aside>'
def kart(baslik, ikon, ic, sag="", govde_cls="pc-body"):
    govde = ic if govde_cls is None else f'<div class="{govde_cls}">{ic}</div>'
    return f'<section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{I(ikon)}{e(baslik)}</h2>{sag}</div>{govde}</section>'
def gecmis(satirlar, bag=True):
    return ('<div class="pc-body sa-gecmis">' + "".join(f'<div><b>{e(b)}</b><span>{e(a)}</span></div>' for b, a in satirlar)
            + (f'<a class="kb-bag" data-hedef="denetim-izi.liste" data-roller="super gyy" href="#">Denetim izinde bütün kayıtlar</a>' if bag else "") + '</div>')
def durum_dl(satirlar): return '<div class="pc-body sa-durum">' + "".join(f'<div><span>{e(a)}</span><b>{e(b)}</b></div>' for a, b in satirlar) + '</div>'

YAZILDI = []

# ======================================================================= 1 · VİTRİN (manşet; K16)
HABERLER_SEC = [  # yayındaki haberler (public sözlük) · manşet ve Günün 5'i adayları
    ("Asgari ücret görüşmelerinde ilk toplantı 4 Aralık'ta yapılacak", "Gündem", "Türkiye", "Hakan Uysal", "23.11 14.05", "24,6 B", "p188", "asgari-ucret-gorusmelerinde-ilk-toplanti-4-aralikta-yapilacak"),
    ("İstanbul Valiliği: okullar 24 Kasım'da da tatil", "Gündem", "İstanbul", "Sibel Arslan", "23.11 16.05", "52,1 B", "p183", "istanbul-valiligi-okullar-24-kasimda-da-tatil"),
    ("Merkez Bankası politika faizini yüzde 42,5'te sabit tuttu", "Finans", "Faiz Oranları", "Elif Aras", "23.11 14.00", "27,5 B", "p192", "merkez-bankasi-politika-faizini-yuzde-42-5te-sabit-tuttu"),
    ("KAAN'ın ikinci prototipi ilk test uçuşunu gerçekleştirdi", "Savunma", "Hava Platformları", "Mert Yalın", "23.11 13.20", "1,4 B", "p195", "kaanin-ikinci-prototipi-ilk-test-ucusunu-gerceklestirdi"),
    ("Marmara'da yoğun kar yağışı: gelişmeler dakika dakika", "Gündem", "Canlı Anlatım", "Mehmet Koçak", "23.11 16.05", "64,3 B", "p180", "marmarada-yogun-kar-yagisi"),
    ("Millî takımın aday kadrosu açıklandı", "Spor", "Millî Takım", "Burak Tan", "23.11 13.48", "18,2 B", "p203", "milli-takimin-aday-kadrosu-aciklandi"),
    ("Rüzgâr enerjisinde yeni yatırım ihalesi", "Finans", "Enerji", "Can Demir", "23.11 12.00", "19,6 B", "p117", "ruzgar-enerjisinde-yeni-yatirim-ihalesi"),
    ("AB dışişleri bakanları göç paketini görüştü", "Dünya", "Avrupa", "Zeynep Ak", "23.11 13.25", "23,1 B", "p133", "ab-disisleri-bakanlari-goc-paketini-gorustu"),
    ("Doğuda kar yağışı: 214 köy yolu kapalı", "Gündem", "Afet", "Ayşe Yıldız", "23.11 15.35", "4,4 B", "p182", "doguda-kar-yagisi-214-koy-yolu-kapali"),
    ("YKS 2027 tarihleri tek ekranda", "Kampüs", "YKS", "Aslı Gür", "23.11 14.50", "3,8 B", "p163", "yks-2027-tarihleri-tek-ekranda"),
    ("Asgari ücret desteği 2027 bütçesinde yer aldı", "Gündem", "Finans", "Sibel Arslan", "23.11 15.50", "12,5 B", "p178", "asgari-ucret-destegi-2027-butcesinde-yer-aldi"),
    ("Dolar/TL güne yatay başladı, gözler enflasyon verisinde", "Finans", "Döviz", "Elif Aras", "23.11 15.00", "18,4 B", "p164", "dolar-tl-gune-yatay-basladi"),
]
def haber_sec_secenek(haric=()):
    return [(h[7], h[0], f"{h[1]} · {h[4]}") for h in HABERLER_SEC if h[7] not in haric]

def sirali_secenek(haberler):
    return "".join(f'<button type="button" data-deger="{h[7]}" data-ad="{e(h[0])}" data-alt="{e(h[1])} › {e(h[2])} · {e(h[3])}" data-gorsel="{g(h[6])}">{e(h[0])}<span class="ks-alt">{e(h[1])} · {e(h[4])}</span></button>' for h in haberler)
def sirali(id_, satirlar, havuz, sinir, ad, yer, alan_id=None):
    rows = "".join(f'<div class="km-satir" data-sira data-deger="{h[7]}" data-ad="{e(h[0])}" data-alt="{e(h[1])} › {e(h[2])} · {e(h[3])}" data-gorsel="{g(h[6])}"></div>' for h in satirlar)
    aid = f' data-alan-id="{alan_id}"' if alan_id else ""
    return (f'<div class="kb-sirali" data-sirali-havuz data-sinir="{sinir}" data-sirali-ad="{e(ad)}"{aid}><div class="kb-madde" data-siralanir id="{id_}">{rows}</div>'
            f'<div class="kb-secim" data-yer="{e(yer)}"><button type="button" class="kb-secim-btn" data-acilir="{id_}Sec" aria-expanded="false" aria-haspopup="listbox">{I("fa-plus", "ks-ikon")}<span class="ks-deger">{e(yer)}</span>{I("fa-chevron-down")}</button>'
            f'<div class="pnl-menu kb-secim-menu" id="{id_}Sec"><div class="kb-secim-ara">{I("fa-magnifying-glass")}<input type="search" placeholder="Yayındaki haberlerde ara" aria-label="Yayındaki haberlerde ara"></div>'
            f'<div class="kb-secim-liste" role="listbox">{sirali_secenek(havuz)}</div><div class="kb-secim-bos" hidden>Bu adla yayında haber yok.</div></div></div></div>')
def vitrin_oniz(telefon=False, id_=None):
    yer = '<span class="kvo-g" data-oniz-gorsel></span><b data-oniz-baslik></b>'
    return (f'<div class="kb-vitrin-oniz{" is-telefon" if telefon else ""}"{(" id=" + chr(34) + id_ + chr(34)) if id_ else ""}{" hidden" if telefon else ""}>'
            f'<div data-sira-onizleme="#vtSlayt"><div class="kvo-ana" data-oniz-yer>{yer}</div></div>'
            f'<div class="kvo-yan" data-sira-onizleme="#vtKart">' + "".join(f'<div class="kvo-kart" data-oniz-yer>{yer}</div>' for _ in range(3)) + '</div></div>')

def vitrin():
    secili = HABERLER_SEC[:8]
    sl, kr = secili[:5], secili[5:8]
    govde = bas("Vitrin", "Ana sayfa manşeti · 5 slayt ve yanındaki 3 kart · ana sayfanın geri kalanı kendiliğinden dolar (K16) · son değişiklik 23.11.2026 15.48 · Ayşe Yıldız",
                [a_hedef("Son Dakika", "fa-bolt", "haberler.son-dakika"), a_dis("Sitede Görüntüle", "fa-arrow-up-right-from-square", SITE + "index.html")])
    ilk = secili[0]
    form = (f'<section class="pnl-card" id="vtForm" data-form aria-label="Manşet">'
            f'<div class="pc-head"><h2 class="pc-title">{I("fa-star")}Manşet</h2>{rozet("ok", "Yayında")}</div>'
            f'<div class="form-sec"><div class="kb-bant bilgi">{I("fa-circle-info")}<span><b>Kaydedilince hemen ana sayfaya yansır.</b> Önceki dizilim sürüm geçmişinde kalır; manşetten çıkan haber yayından kalkmaz.</span></div></div>'
            + fs("Önizleme", "fa-eye", f'<div class="kb-onizle-sec" data-segment><button type="button" class="is-on" data-hedef="vtOnWeb" aria-pressed="true">Web</button><button type="button" data-hedef="vtOnTel" aria-pressed="false">Telefon</button></div>'
                 + f'<div class="kb-ust-bosluk">{vitrin_oniz(id_="vtOnWeb")}{vitrin_oniz(True, "vtOnTel")}</div><p class="fhint kb-ust-bosluk">Sıra değişince önizleme hemen güncellenir. Web: büyük slayt (948×490) ve yanında 3 kart; telefonda slayt 358×420, kartlar altında.</p>', ek_bas="Sıraya bağlı")
            + fs("Manşet slaytları", "fa-images", sirali("vtSlayt", sl, HABERLER_SEC, 5, "Haber", "Slayta haber ekle", alan_id="slaytlar")
                 + '<p class="fhint kb-ust-bosluk">İlk slayt açılışta görünür. Sürükleyerek ya da tutamaç seçiliyken ↑/↓ ile sıralayın; × onaysız çıkarır, “Geri al” ile döner. Haberler listesindeki ⋯ → “Manşete ekle” de buraya ekler.</p>', ek_bas="5 slayt · sitede 948×490 (1.93:1)")
            + fs("Yanındaki kartlar", "fa-table-cells-large", sirali("vtKart", kr, HABERLER_SEC, 3, "Haber", "Karta haber ekle", alan_id="kartlar"), ek_bas="3 kart · sitede 316×155 (2:1)")
            + fs("Kurallar", "fa-sliders", grid(
                anahtar("Yayından kalkan haber manşetten de çıkar", "Boşalan yere sıradaki haber geçer; yer boş kalırsa en çok okunan haber gelir"),
                anahtar("Son dakika varken manşetin üstünde şerit", "Son Dakika listesindeki “Şeritte” girişler manşetin üstünde kayar"),
                anahtar("Canlı anlatım rozeti", "Canlı anlatım manşetteyse slaytta “Canlı” rozeti ve son giriş saati görünür")))
            + '</section>')
    kirp = kart("İlk slayt görseli", "fa-crop-simple",
        f'<div class="kb-gorsel-kucuk" data-gorsel-alan="haberler.manset" data-gorsel-ad="Manşet görseli">'
        f'<span class="kg-resim r-manset" data-gorsel-hedef="web" data-kirp-oran="web.detay" data-gorsel-kucuk style="background-image:url({gk(ilk[6])})"></span>'
        f'<div><b>1.93:1 · 948×490</b><span data-gorsel-bilgi>Haberin kapağından odak noktasına göre kendiliğinden kırpılır; yan kart 2:1, telefon 6:7.</span>'
        f'<div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{I("fa-crop-simple")}Kırp</button></div></div></div>')
    son = kart("Son Değişiklikler", "fa-clock-rotate-left", govde_cls=None, ic=gecmis([
        ("Manşete eklendi: Marmara'da yoğun kar yağışı", "Ayşe Yıldız · 23.11.2026 15.48"),
        ("Sıra değişti: faiz kararı 3. slayta indi", "Ayşe Yıldız · 23.11.2026 14.10"),
        ("Manşetten çıkarıldı: Dolar/TL güne yatay başladı", "Mehmet Koçak · 23.11.2026 12.02")]))
    govde += f'  <div class="form-layout">\n  {form}\n  {yan(kirp, son)}\n  </div>\n'
    govde += kaydet("vtForm", "Yayında · 23.11.2026 15.48 · Ayşe Yıldız", "Yayına Al", "Manşet güncellendi; ana sayfada hemen görünür, önceki dizilim sürüm geçmişinde", taslak=False)
    YAZILDI.append(sayfa("vitrin.html", "Vitrin", "haberler.vitrin", govde))

# ======================================================================= 2 · SON DAKİKA
SD_KAT = {"Siyaset": ("Gündem", "Siyaset"), "Türkiye": ("Gündem", "Türkiye")}
SD_BAGLI = {"İstanbul Valiliği: okullar 24 Kasım'da da tatil": "istanbul-valiligi-okullar-24-kasimda-da-tatil",
            "Asgari ücret görüşmelerinde ilk toplantı 4 Aralık'ta yapılacak": "asgari-ucret-gorusmelerinde-ilk-toplanti-4-aralikta-yapilacak",
            "Merkez Bankası politika faizini yüzde 42,5'te sabit tuttu": "merkez-bankasi-politika-faizini-yuzde-42-5te-sabit-tuttu",
            "Millî takımın aday kadrosu açıklandı": "milli-takimin-aday-kadrosu-aciklandi",
            "KAAN'ın ikinci prototipi test uçuşunda": "kaanin-ikinci-prototipi-ilk-test-ucusunu-gerceklestirdi",
            "Havalimanlarında kar nedeniyle 46 iç hat seferi iptal edildi": "marmarada-yogun-kar-yagisi"}
def sd_kat_secenek():
    o = []
    for b in ["Gündem", "Finans", "Spor", "Savunma", "Dünya", "Kampüs", "Kadın", "Keşfet"]:
        o.append((b, b)); o += [(f"{b} › {a}", f"{b} › {a}") for a in ALTLAR.get(b, [])[:3]]
    return o
def sd_form(onek, kayit=None):
    b = kayit["baslik"] if kayit else ""
    kat = kayit["katad"] if kayit else None
    bag = kayit.get("bagli") if kayit else None
    zaman = kayit["deger"] if kayit else ""
    ic = (dil("Dil seçici başlığı birlikte değiştirir; kategori ve bağlı haber bütün dillerde ortaktır.", kap=True)
          + kfs("Son Dakika", girdi(f"{onek}B", "Başlık", b, "baslik", "90|110", "Şeritte tek satır · 90 karaktere kadar tam görünür", ph="ör. İstanbul Valiliği: okullar 24 Kasım'da da tatil", hata="Başlık zorunlu.")
                + frow("Kategori", secim(f"{onek}K", sd_kat_secenek(), kat, "Kategori seçin", "Kategori ara", alan_id="kategori", bos_metin="Bu adla kategori yok."), ipucu="Şeritte başlığın önündeki etiket.", hata="Kategori zorunlu.")
                + frow("Bağlı haber", secim(f"{onek}H", [("", "Bağlı haber yok")] + haber_sec_secenek(), bag, "Bağlı haber yok", "Başlık ara", bos_metin="Bu adla yayında haber yok."), ipucu="İsteğe bağlı. Bağlıysa şeritteki başlık habere gider; değilse Son Dakika sayfasında kalır.")
                + frow("Saat", tarih(f"{onek}T", zaman, ek=' data-alan-id="saat" data-bos="Yayımlanınca o anın saati" data-temizlenir="1"'), ipucu="Boş bırakılırsa yayımlandığı an yazılır."))
          + kfs("Dağıtım", anahtar("Şeritte göster", "Ana sayfa ve bütün sayfaların üstündeki kayan şerit", kayit.get("serit", True) if kayit else True)
                + (anahtar("Bildirim gönderildi", kayit["deger"][8:10] + "." + kayit["deger"][5:7] + "." + kayit["deger"][:4] + " " + kayit["deger"][11:] + "'te bütün abonelere gitti; düzenleme yeniden göndermez", True, ek=" disabled", kap_ek=' data-modul="etkilesim"')
                   if kayit and kayit.get("bildirim") else anahtar("Bildirim gönder", "Bütün abonelere telefon ve web bildirimi gider", False, kap_ek=' data-modul="etkilesim"'))))
    return ic
def son_dakika():
    L = soz["son_dakika"]["liste"]
    satir, sab = [], []
    for i, s in enumerate(L):
        kb, ka = SD_KAT.get(s["kat"], (s["kat"], None))
        katad = f"{kb} › {ka}" if ka else kb
        y, a, gn = s["tarih"].split("-")
        zaman = f"{gn}.{a}.{y} {s['saat']}"
        durum = "serit" if i < 4 else "bitti"
        bagli = SD_BAGLI.get(s["baslik"])
        bag_ad = next((h[0] for h in HABERLER_SEC if h[7] == bagli), None)
        bildirim = i < 3 or s["kat"] == "Savunma"
        kayit = {"baslik": s["baslik"], "katad": katad, "bagli": bagli or "", "deger": f"{s['tarih']} {s['saat']}", "serit": durum == "serit", "bildirim": bildirim}
        tid = f"sdD{i}"
        sab.append(sablon(tid, "Son dakika · düzenle", f"{zaman} · {katad}", sd_form(tid, kayit) + alt_cubuk(
            f'<button type="button" class="btn btn-ghost btn-sm danger kb-sol"{onay("Son dakika çöpe taşınsın mı?", "“" + s["baslik"] + "” şeritten ve Son Dakika sayfasından kalkar; Çöp sekmesinden geri alınabilir. İşlem denetim izine yazılır.", "Çöpe Taşı", True, sonra=("cop", "Çöpte", "warm"), bildir="Son dakika çöpe taşındı; Çöp sekmesinden geri alınabilir")}>{I("fa-trash")}Sil</button>',
            f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="sdTamam" data-baslik-yaz="Son dakika güncellendi" data-bildir-sonra="Son dakika güncellendi; şeritte ve sayfada hemen görünür">{I("fa-check")}Güncelle</button>'), "haberler.son-dakika"))
        alt = ("Habere bağlı" if bag_ad == s["baslik"] else "Bağlı haber: " + bag_ad) if bag_ad else "Bağlı haber yok · yalnız Son Dakika sayfasında"
        satir.append(tr(f"sd-{i}", durum, f"{s['baslik']} {katad}", s["baslik"],
            [(f'<span class="kb-tarih">{zaman}</span>', ""), ana_hucre(s["baslik"], alt), kat_hucre(kb, ka),
             ((rozet("ok", "Şeritte") + " " + isaret_sabit("Şeridin başına sabitlendi", "Şeritteki sabitleme kaldırıldı; giriş saatine göre sıralanır")) if durum == "serit" else rozet("off", "Bitti"), ""),
             ((f'<span class="kb-kat">{I("fa-bell")}Gönderildi</span>' if bildirim else '<span class="muted">—</span>'), "kb-gizle-t")],
            ia_tanim(tid, "Görüntüle", "fa-eye") + ia_tanim(tid, "Düzenle", "fa-pen") + SIL + DIGER, kategori=kb))
    # çöpteki örnek
    satir.append(tr("sd-cop", "cop", "Dolar/TL güne 34,50 seviyesinde başladı Finans", "Dolar/TL güne 34,50 seviyesinde başladı",
        [('<span class="kb-tarih muted">23.11.2026 09.58</span>', ""), ana_hucre("Dolar/TL güne 34,50 seviyesinde başladı", "Yanlış rakamla girildi · Mehmet Koçak çöpe taşıdı"), kat_hucre("Finans"), (rozet("warm", "Çöpte"), ""), ('<span class="muted">—</span>', "kb-gizle-t")],
        ia_tanim("sdYeni", "Görüntüle", "fa-eye") + ia_tanim("sdYeni", "Düzenle", "fa-pen") + SIL + DIGER, kategori="Finans", onceki="bitti"))
    menu = (m_grup("Şerit", "serit bitti")
            + m_btn("Bitir (şeritten kaldır)", "fa-flag-checkered", "serit", onay("Son dakika bitirilsin mi?", "Giriş şeritten kalkar; Son Dakika sayfasında saatiyle kalır. Geri almak için ⋯ → Yeniden şeride al.", "Bitir", ikon="fa-flag-checkered", sonra=("bitti", "Bitti", "off"), bildir="Şeritten kaldırıldı; Son Dakika sayfasında kalıyor"))
            + m_btn("Yeniden şeride al", "fa-rotate-left", "bitti", onay("Yeniden şeride alınsın mı?", "Giriş şeritte saatine göre yerini alır.", "Şeride al", ikon="fa-bolt", sonra=("serit", "Şeritte", "ok"), bildir="Yeniden şeritte"))
            + m_ayir("serit bitti") + m_grup("Dağıtım", "serit bitti")
            + m_btn("Bildirim gönder", "fa-bell", "serit bitti", ' data-modul="etkilesim"' + onay("Bildirim gönderilsin mi?", "Başlık bütün abonelere telefon ve web bildirimi olarak gider; geri alınamaz. İşlem denetim izine yazılır.", "Gönder", ikon="fa-bell", bildir="Bildirim gönderildi"))
            + m_a("Habere dönüştür", "fa-file-circle-plus", "haberler.duzenle", "?yeni=1", ' data-durum-icin="serit bitti"')
            + f'<a data-durum-icin="serit bitti" href="{SITE}son-dakika.html" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Sitede Görüntüle</a>'
            + m_ayir("serit bitti") + m_grup("Kayıt") + DENETIM + COP_MENU)
    govde = bas("Son Dakika", "Şerit ve Son Dakika sayfası tek listeden beslenir · bugün 13 giriş · 4'ü şeritte",
                [a_hedef("Vitrin", "fa-star", "haberler.vitrin"), f'<button type="button" class="btn btn-acc btn-sm" data-tanim="sdYeni" data-roller="super gyy editor">{I("fa-plus")}Yeni son dakika</button>'])
    govde += liste("son dakika", "Son dakika listesi", [("hepsi", "Tümü", 0), ("serit", "Şeritte", 0), ("bitti", "Bitti", 0)], "Başlık ya da Kategori Ara",
        [("kategori", "Kategori", "sdSuzKat", [("", "Bütün Kategoriler")] + [(b, b) for b in ["Gündem", "Finans", "Spor", "Savunma", "Dünya", "Kampüs"]], None)],
        [btn("Bitir", "fa-flag-checkered", attr=' data-toplu="bitti" data-bildir="Seçilen girişler şeritten kaldırıldı; Son Dakika sayfasında kalıyor"'), btn("Çöpe Taşı", "fa-trash", "btn-ghost danger", ' data-toplu="cop"')],
        [('<input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün girişleri seç">', "kb-sec-hucre"), ("Saat", ""), ("Başlık", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Bildirim", "kb-gizle-t"), ('<span class="sr-only">İşlemler</span>', "")],
        satir, menu, bos_durum("son-dakika.html", "Son dakika listesi yüklenemedi", "fa-bolt", "Henüz son dakika yok", "Şeride düşecek ilk girişi ekleyin; giriş hemen sitede görünür.", f'<button type="button" class="pe-tag" data-tanim="sdYeni">{I("fa-plus")}Yeni son dakika</button>'),
        "20 sonuçtan 1–20 gösteriliyor", liste_cop_not="Şeritten ve Son Dakika sayfasından kalkar ve Çöp sekmesine taşınır")
    sab.insert(0, sablon("sdYeni", "Yeni son dakika", "Kaydedilince hemen şeritte ve Son Dakika sayfasında", sd_form("sdY") + alt_cubuk(
        f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="sdTamam" data-bildir-sonra="Son dakika yayımlandı; şeritte ve Son Dakika sayfasında">{I("fa-bolt")}Yayımla</button>'), "haberler.son-dakika"))
    sab.append(sablon("sdTamam", "Son dakika yayında", "Şerit ve Son Dakika sayfası güncellendi",
        f'<div class="kb-bant tamam">{I("fa-circle-check")}<span><b>Yayında.</b> Giriş şeritte ve Son Dakika sayfasında görünüyor; işlem denetim izine yazıldı.</span></div>'
        + alt_cubuk(f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="sdYeni">{I("fa-plus")}Yeni son dakika</button>')))
    YAZILDI.append(sayfa("son-dakika.html", "Son Dakika", "haberler.son-dakika", govde, "".join(sab)))

# ======================================================================= 3 · CANLI ANLATIM LİSTESİ
CANLI = [
    ("marmara", "Marmara'da yoğun kar yağışı: gelişmeler dakika dakika", "Gündem", "Afet", "Mehmet Koçak", "canli", "23.11.2026 16.05", "10 giriş · 06.10'dan beri", "64,3 B", "p180", "dakika-dakika.html"),
    ("butce", "TBMM'de 2027 bütçesi görüşmeleri: gelişmeler dakika dakika", "Gündem", "Siyaset", "Ayşe Yıldız", "canli", "23.11.2026 15.42", "14 giriş · 10.00'dan beri", "21,7 B", "p178", "dakika-dakika-butce.html"),
    ("ab", "Türkiye–AB yüksek düzeyli diyalog toplantısı: dakika dakika", "Dünya", "Diplomasi", "Kaan Yücel", "bitti", "22.11.2026 17.40", "18 giriş · 17.40'ta kapandı", "15,3 B", "p133", "dakika-dakika-zirve.html"),
    ("komisyon", "Plan ve Bütçe Komisyonu'nda son gün oturumu", "Gündem", "Siyaset", "Ozan Er", "bitti", "22.11.2026 19.20", "22 giriş · 19.20'de kapandı", "7,1 B", "p193", "canli-gundem.html"),
    ("iklim", "BM İklim Konferansı kapanış oturumu", "Dünya", "Küresel Siyaset", "Ozan Er", "bitti", "21.11.2026 22.05", "31 giriş · 22.05'te kapandı", "41,5 B", "p155", "canli-gundem.html"),
    ("derbi", "Derbi günü: Galatasaray–Fenerbahçe maçı öncesi son gelişmeler", "Spor", "Futbol", "Burak Tan", "taslak", "29.11.2026 16.00", "Başlamadı · 29.11.2026 16.00'da açılacak", "—", "p203", None),
]
def canli():
    satir = []
    for k, b, kb, ka, yz, d, son, ozet, gor, gs, site in CANLI:
        rz = {"canli": ("warm", "Canlı"), "bitti": ("off", "Sona Erdi"), "taslak": ("info", "Zamanlanmış")}[d]
        href = f"canli-masa.html?id={k}" + ("&sekme=pAkis" if d == "canli" else "")
        gorl = ia_a(SITE + site, "Sitede Görüntüle", "fa-eye", True) if site else ia_a(f"canli-masa.html?id={k}", "Önizle", "fa-eye")
        satir.append(tr(k, d, f"{b} {yz} {kb} {ka}", b, [ana_hucre(b, f"{yz} · {ozet}", gs), kat_hucre(kb, ka), (rozet(*rz), ""),
            (f'<span class="kb-tarih{"" if d != "taslak" else " muted"}">{son}</span>', "kb-gizle-m"), (gor, "say kb-gizle-t")],
            gorl + ia_a(href, "Düzenle", "fa-pen") + SIL + DIGER, href=href, kategori=kb, yerler="manset" if k == "marmara" else ""))
    satir.append(tr("eski", "cop", "Deprem tatbikatı: gelişmeler dakika dakika Kerem Aksoy", "Deprem tatbikatı: gelişmeler dakika dakika",
        [ana_hucre("Deprem tatbikatı: gelişmeler dakika dakika", "Kerem Aksoy · 4 giriş · yanlışlıkla açıldı", "p192"), kat_hucre("Gündem", "Afet"), (rozet("warm", "Çöpte"), ""), ('<span class="kb-tarih muted">18.11.2026 10.20</span>', "kb-gizle-m"), ("—", "say kb-gizle-t")],
        ia_a("canli-masa.html?id=eski", "Görüntüle", "fa-eye") + ia_a("canli-masa.html?id=eski", "Düzenle", "fa-pen") + SIL + DIGER, href="canli-masa.html?id=eski", kategori="Gündem", onceki="bitti"))
    menu = (m_grup("Anlatım", "canli bitti taslak")
            + m_a("Masayı aç (yeni giriş)", "fa-pen-to-square", "haberler.canli-masa", "?sekme=pAkis", ' data-durum-icin="canli"')
            + m_btn("Anlatımı kapat", "fa-circle-stop", "canli", onay("Canlı anlatım kapatılsın mı?", "Önce: canlı, okurlar yeni girişleri anında görüyor → Sonra: “Sona erdi”; sayfa ve girişler arşivde kalır, yeni giriş eklenemez. Gerekirse ⋯ → Yeniden aç. İşlem denetim izine yazılır.", "Anlatımı kapat", True, "fa-circle-stop", sonra=("bitti", "Sona Erdi", "off"), bildir="Canlı anlatım kapatıldı; sayfa arşivde"))
            + m_btn("Yeniden aç", "fa-tower-broadcast", "bitti", onay("Anlatım yeniden açılsın mı?", "Sayfa yeniden “Canlı” olur; yeni girişler en üstte görünür.", "Yeniden aç", ikon="fa-tower-broadcast", sonra=("canli", "Canlı", "warm"), bildir="Anlatım yeniden canlı"))
            + m_btn("Şimdi başlat", "fa-play", "taslak", onay("Anlatım şimdi başlasın mı?", "Sayfa yayına girer ve “Canlı” olur; zamanlanan açılış iptal edilir.", "Başlat", ikon="fa-play", sonra=("canli", "Canlı", "warm"), bildir="Canlı anlatım başladı"))
            + f'<button type="button" data-durum-icin="canli bitti" data-roller="super gyy editor" data-yer="manset" data-yer-ad="Manşet">{I("fa-star")}<span>Manşete ekle</span></button>'
            + m_ayir("canli bitti") + m_grup("Dağıtım", "canli bitti")
            + m_btn("Bildirim gönder", "fa-bell", "canli", ' data-modul="etkilesim"' + onay("Bildirim gönderilsin mi?", "Anlatımın son girişi bütün abonelere telefon ve web bildirimi olarak gider; geri alınamaz.", "Gönder", ikon="fa-bell", bildir="Bildirim gönderildi"))
            + m_btn("Bağlantıyı kopyala", "fa-link", "canli bitti", " data-kopyala")
            + m_ayir("canli bitti taslak") + m_grup("Kayıt") + m_a("Sürüm Geçmişi", "fa-clock-rotate-left", "haberler.surumler") + DENETIM + COP_MENU)
    govde = bas("Canlı Anlatım", "Dakika Dakika anlatımları · 2 canlı · 3 sona erdi · 1 zamanlanmış",
                [a_dis("Canlı Gündem sayfası", "fa-arrow-up-right-from-square", SITE + "canli-gundem.html"), a_hedef("Yeni anlatım", "fa-plus", "haberler.canli-masa", "?yeni=1", "btn-acc", ' data-roller="super gyy editor kat-ed"')])
    govde += liste("anlatım", "Canlı anlatım listesi", [("hepsi", "Tümü", 0), ("canli", "Canlı", 0), ("bitti", "Sona Erdi", 0), ("taslak", "Zamanlanmış", 0)], "Başlık, Yazar ya da Kategori Ara",
        [("kategori", "Kategori", "caSuzKat", [("", "Bütün Kategoriler")] + [(b, b) for b in ["Gündem", "Dünya", "Spor", "Finans"]], None)],
        [btn("Çöpe Taşı", "fa-trash", "btn-ghost danger", ' data-toplu="cop"')],
        [('<input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün anlatımları seç">', "kb-sec-hucre"), ("Anlatım", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Son giriş", "kb-gizle-m"), ("Okunma", "say kb-gizle-t"), ('<span class="sr-only">İşlemler</span>', "")],
        satir, menu, bos_durum("canli.html", "Canlı anlatımlar yüklenemedi", "fa-tower-broadcast", "Henüz canlı anlatım yok", "Gelişen bir olayı dakika dakika anlatmak için yeni anlatım açın.", f'<a class="pe-tag" data-hedef="haberler.canli-masa" data-hedef-ek="?yeni=1" href="#">{I("fa-plus")}Yeni anlatım</a>'),
        "6 sonuçtan 1–6 gösteriliyor", liste_cop_not="Anlatım ve girişleri yayından kalkar ve Çöp sekmesine taşınır")
    YAZILDI.append(sayfa("canli.html", "Canlı Anlatım", "haberler.canli", govde))

# ======================================================================= 4 · CANLI ANLATIM MASASI
GIRISLER = [
    ("16.05", "İstanbul Valiliği: okullar yarın da tatil", "İstanbul Valiliği, kar yağışının yarın öğle saatlerine kadar sürmesinin beklenmesi nedeniyle okul öncesi, ilk ve ortaöğretim kurumlarında eğitime 24 Kasım'da da ara verildiğini açıkladı.", "İstanbul Valiliği", "kilit", True, None, "Mehmet Koçak"),
    ("15.20", "Havalimanlarında 46 sefer iptal edildi", "Valilik koordinasyon merkezinin açıklamasına göre gün içinde 46 iç hat seferi iptal edildi. Yolculara uçuş durumunu havayolu şirketlerinden kontrol etmeleri öneriliyor.", "İstanbul Valiliği", "kilit", False, None, "Sibel Arslan"),
    ("14.40", "Kuzey Marmara Otoyolu'nda tır geçişlerine kısıtlama", "Karayolları Genel Müdürlüğü, ağır tonajlı araçların otoyola girişine yağış süresince izin verilmeyeceğini duyurdu.", "Karayolları Genel Müdürlüğü", "yayinda", False, None, "Sibel Arslan"),
    ("13.55", "Meteoroloji: yağış gece saatlerinde kuvvetlenecek", "Meteoroloji Genel Müdürlüğü, yağışın gece saatlerinde kuvvetlenmesi, kar kalınlığının yüksek kesimlerde 30 santimetreye ulaşması beklendiğini bildirdi.", "Meteoroloji Genel Müdürlüğü", "kilit", False, None, "Mehmet Koçak"),
    ("13.10", "Toplu taşımada ek seferler", "İstanbul'da metro ve Marmaray hatlarında sefer sıklığı artırıldı; vapur seferlerinde ise rüzgâr nedeniyle bazı iptaller yaşanıyor.", "İstanbul Valiliği", "yayinda", False, ("video", "marmaray-ek-sefer.mp4", "48"), "Sibel Arslan"),
    ("12.25", "Kocaeli ve Sakarya'da da okullar tatil edildi", "Kocaeli ve Sakarya valilikleri, kar yağışı nedeniyle eğitime bir gün ara verildiğini açıkladı. Tatil kararı verilen il sayısı 14'e yükseldi.", "Kocaeli Valiliği", "kilit", False, None, "Mehmet Koçak"),
    ("11.30", "AFAD: vatandaşlar zorunlu olmadıkça yola çıkmamalı", "Afet ve Acil Durum Yönetimi Başkanlığı, sürücülerin kış lastiği ve zincir bulundurmasını, zorunlu olmadıkça seyahat edilmemesini istedi.", "AFAD", "yayinda", False, ("gorsel", "p182", None), "Mehmet Koçak"),
    ("10.15", "Edirne-İstanbul yolunda ulaşım kontrollü sağlanıyor", "Karayolları ekipleri, Edirne-İstanbul kara yolunda tuzlama çalışmalarını sürdürüyor. Ulaşım kontrollü olarak sağlanıyor.", "Karayolları Genel Müdürlüğü", "yayinda", False, None, "Sibel Arslan"),
    ("08.40", "Belediye 1.200 araçla sahada", "İstanbul Büyükşehir Belediyesi, kar mücadelesi için 1.200 araç ve 7 bin personelin sahada olduğunu açıkladı.", "İstanbul Büyükşehir Belediyesi", "yayinda", False, ("gorsel", "p180", None), "Mehmet Koçak"),
    ("06.10", "Turuncu kodlu uyarı yürürlükte", "Meteoroloji Genel Müdürlüğü, Marmara Bölgesi için yayımladığı turuncu kodlu uyarının 24 Kasım öğle saatlerine kadar geçerli olduğunu bildirdi.", "Meteoroloji Genel Müdürlüğü", "kilit", False, None, "Mehmet Koçak"),
]
KURUMLAR = ["İstanbul Valiliği", "Meteoroloji Genel Müdürlüğü", "Karayolları Genel Müdürlüğü", "AFAD", "Kocaeli Valiliği", "İstanbul Büyükşehir Belediyesi", "Sakarya Valiliği", "Türkiye Büyük Millet Meclisi"]
def giris_form(onek, gz=None):
    saat, bsl, mtn, kyn, dr, sabit, medya, yz = gz if gz else ("", "", "", None, "yayinda", False, None, "")
    m_g = medya and medya[0] == "gorsel"
    m_v = medya and medya[0] == "video"
    gorsel = (f'<div class="kb-gorsel-kucuk" data-gorsel-alan="haberler.canli_giris" data-gorsel-ad="Giriş görseli" data-kirp-oranlar="giris=Giriş görseli=16:9=800×450" data-kirp-sonra>'
              f'<span class="kg-resim r-kart" data-gorsel-hedef="web" data-kirp-oran="giris" data-gorsel-kucuk{(" style=" + chr(34) + "background-image:url(" + gk(medya[1]) + ")" + chr(34)) if m_g else ""}></span>'
              f'<div><b>16:9 · önerilen 800×450</b><span data-gorsel-bilgi>{"Akışta girişin altında tam genişlikte görünür." if m_g else "Görsel yok; isteğe bağlı."}</span><div class="kg-acts">'
              f'<button type="button" class="btn btn-ghost btn-sm" data-medya-sec>{I("fa-photo-film")}Havuzdan Seç</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{I("fa-upload")}Yükle</button><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{I("fa-crop-simple")}Kırp</button><button type="button" class="btn btn-ghost btn-sm danger" data-gorsel-kaldir>{I("fa-trash")}Kaldır</button></div></div></div>')
    video = f'<div class="kb-dosya" data-tur="video" data-ad="Giriş videosu" data-sinir="200">' + (f'<div class="kb-dosya-oge" data-ad="{medya[1]}" data-boyut="18874368" data-sure="{medya[2]}"></div>' if m_v else "") + '</div>'
    return (dil("Dil seçici başlığı ve metni birlikte değiştirir; saat, görsel ve kaynak bütün dillerde ortaktır.", kap=True)
            + kfs("Giriş", frow("Saat", tarih(f"{onek}T", f"2026-11-23 {saat}" if saat else "", ek=' data-alan-id="saat" data-bos="Yayımlanınca o anın saati" data-temizlenir="1"'), ipucu="Boş bırakılırsa yayımlandığı an yazılır; akış saate göre sıralanır.")
                  + girdi(f"{onek}B", "Başlık", bsl, "baslik", "70|90", "Akışta kalın satır; isteğe bağlı", ph="ör. Havalimanlarında 46 sefer iptal edildi")
                  + f'<div class="frow"><span class="flabel">Metin</span>' + editor("Giriş metni", f"<p>{e(mtn)}</p>" if mtn else "<p></p>", "metin", kisa=True, zm="Giriş metnini yazın") + ferr("Giriş metni zorunlu.") + '</div>'
                  + frow("Kaynak", cip_girdi([kyn] if kyn else [], KURUMLAR, "Kurum ara", ek=' data-havuz-yonet data-kullanim-birim="girişte"'), ipucu="Akışta “Kaynak: …” satırı. Havuzda yoksa yazıp ekleyin."))
            + kfs("Medya", frow("Görsel", gorsel) + frow("Video", video, ipucu="İsteğe bağlı · MP4, en fazla 200 MB; sitede girişin altında oynatılır."))
            + kfs("Akıştaki yeri", anahtar("Kilit an", "Sayfanın başındaki “Kilit anlar” kutusunda saatiyle listelenir", dr == "kilit")
                  + anahtar("En üste sabitle", "Yeni girişler gelse de akışın başında kalır; önceki sabit giriş çözülür", sabit)
                  + anahtar("Bu giriş için bildirim gönder", "Bütün abonelere telefon ve web bildirimi", False, kap_ek=' data-modul="etkilesim"')))

def canli_masa():
    sab, satir = [], []
    for i, gz in enumerate(GIRISLER):
        saat, bsl, mtn, kyn, dr, sabit, medya, yz = gz
        tid = f"cmG{i}"
        sab.append(sablon(tid, "Giriş · " + saat, f"23.11.2026 {saat} · {yz}", giris_form(tid, gz) + alt_cubuk(
            f'<button type="button" class="btn btn-ghost btn-sm danger kb-sol"{onay("Giriş çöpe taşınsın mı?", "“" + bsl + "” akıştan kalkar; okurlar artık görmez. Çöp sekmesinden geri alınabilir; işlem denetim izine yazılır.", "Çöpe Taşı", True, sonra=("cop", "Çöpte", "warm"), bildir="Giriş çöpe taşındı; Çöp sekmesinden geri alınabilir")}>{I("fa-trash")}Sil</button>',
            f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="cmTamam" data-baslik-yaz="Giriş güncellendi" data-bildir-sonra="Giriş güncellendi; sitede hemen görünür, önceki hal sürüm geçmişinde">{I("fa-check")}Güncelle</button>'), "haberler.canli-giris"))
        mi = (f' · {I("fa-film")}Video 0:48' if medya and medya[0] == "video" else f' · {I("fa-image")}Görsel' if medya else "")
        rz = rozet("info", "Kilit an") if dr == "kilit" else rozet("ok", "Yayında")
        rz += " " + isaret_sabit("Giriş akışın başına sabitlendi", "Sabitleme kaldırıldı; giriş saatine göre sıralanır", sabit)
        satir.append(tr(f"g{i}", dr, f"{bsl} {mtn} {kyn}", bsl,
            [(f'<span class="kb-tarih">{saat}</span>', ""), ana_hucre(bsl, e(yz) + mi + f" · {e(kyn)} · " + e(mtn[:70]) + "…", alt_ham=True), (rz, "")],
            ia_tanim(tid, "Görüntüle", "fa-eye") + ia_tanim(tid, "Düzenle", "fa-pen") + SIL + DIGER, secim_kutu=False))
    menu = (m_grup("Akış", "yayinda kilit")
            + m_btn("Kilit an yap", "fa-key", "yayinda", onay("Kilit an olarak işaretlensin mi?", "Giriş sayfanın başındaki “Kilit anlar” kutusunda saatiyle listelenir.", "Kilit an yap", ikon="fa-key", sonra=("kilit", "Kilit an", "info"), bildir="Kilit anlara eklendi"))
            + m_btn("Kilit anlardan çıkar", "fa-key", "kilit", onay("Kilit anlardan çıkarılsın mı?", "Giriş akışta kalır; yalnız “Kilit anlar” kutusundan çıkar.", "Çıkar", ikon="fa-key", sonra=("yayinda", "Yayında", "ok"), bildir="Kilit anlardan çıkarıldı"))
            + m_btn("Bildirim gönder", "fa-bell", "yayinda kilit", ' data-modul="etkilesim"' + onay("Bu giriş için bildirim gönderilsin mi?", "Giriş başlığı bütün abonelere telefon ve web bildirimi olarak gider; geri alınamaz.", "Gönder", ikon="fa-bell", bildir="Bildirim gönderildi"))
            + m_btn("Bağlantıyı kopyala", "fa-link", "yayinda kilit", " data-kopyala")
            + m_ayir("yayinda kilit") + m_grup("Kayıt") + DENETIM + COP_MENU)
    akis = (f'<div class="form-sec" data-yeni-gizle><div class="kb-bant bilgi">{I("fa-tower-broadcast")}<span><b>Canlı · 10 giriş.</b> Kaydedilen giriş hemen sitede, en üstte görünür.</span>'
            f'<button type="button" class="btn btn-acc btn-sm kb-bant-eylem" data-tanim="cmYeni">{I("fa-plus")}Yeni giriş</button></div></div>'
            + f'<div class="pnl-empty" data-yeni-goster hidden><div class="pe-ico">{I("fa-tower-broadcast")}</div><h2>Henüz giriş yok</h2><p>Anlatımı kaydedince ilk girişi buradan eklersiniz; anlatım okurlara bu girişle açılır.</p></div>'
            + liste("giriş", "Canlı akış girişleri", [("hepsi", "Tümü", 0), ("kilit", "Kilit anlar", 0)], "Girişlerde ara", [], [],
                [("Saat", ""), ("Giriş", "kb-ana"), ("Durum", ""), ('<span class="sr-only">İşlemler</span>', "")], satir, menu,
                bos_durum("canli-masa.html?sekme=pAkis", "Girişler yüklenemedi", "fa-tower-broadcast", "Henüz giriş yok", "İlk girişi ekleyin; anlatım okurlara bu girişle açılır.", f'<button type="button" class="pe-tag" data-tanim="cmYeni">{I("fa-plus")}Yeni giriş</button>'),
                "10 sonuçtan 1–10 gösteriliyor", liste_cop_not="Akıştan kalkar ve Çöp sekmesine taşınır", kap=False, attr=" data-yeni-gizle"))
    kp = "cmKapak"
    detay = (fs("Anlatım", "fa-file-lines", grid(
                girdi("cmBaslik", "Başlık", "Marmara'da yoğun kar yağışı: gelişmeler dakika dakika", "baslik", "70|90", "Sitede başlık; SEO başlığı buradan üretilir", cls="finput kb-buyuk", ek=' data-alan="baslik"', hata="Başlık zorunlu."),
                alan("cmSpot", "Spot", "Meteoroloji'nin turuncu kodlu uyarısının ardından Marmara Bölgesi'nde etkili olan kar yağışı ulaşımı ve eğitimi etkiliyor. Valilik ve kurum açıklamalarını geldikçe bu sayfada topluyoruz.", "spot", "220|280", "Başlığın altındaki giriş cümlesi", ek=' data-alan="spot"', hata="Spot zorunlu.")))
             + ai_adim("#cmBaslik,#cmSpot", [("ozet", "Dada Özet", True, None), ("sinif", "Kategori ve Alt Konular", True, None), ("seo", "SEO", True, None), ("bildirim", "Bildirim Metni", True, "etkilesim"), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")])
             + fs("Sınıflandırma", "fa-sitemap", grid(kategori_alanlari("cm", "Gündem", ["Afet", "İstanbul"]), yazar_alani("cmYazar", "Mehmet Koçak")), attr=' data-ai-grup="sinif"')
             + kapak(kp, "p180", (50, 45), "Kaynak: Dada Haber arşivi", "Kar yağışı sabah saatlerinde İstanbul'da etkili oldu · Dada Haber arşivi")
             + fs("Dada Özet", "fa-bolt", '<div class="kb-madde">' + "".join(f'<div class="km-satir"><span class="km-no">{n}</span><input value="{e(v)}" aria-label="Özet maddesi {n}"></div>' for n, v in enumerate([
                 "Marmara'da 14 ilde okullar tatil; İstanbul'da tatil yarın da sürecek.", "Havalimanlarında 46 iç hat seferi iptal edildi, otoyolda tır geçişi kısıtlandı.", "Yağışın gece kuvvetlenmesi, 24 Kasım öğle saatlerinde zayıflaması bekleniyor."], 1)) + '</div><p class="fhint">Sitede akışın üstünde 15 sn özet olarak görünür; gelişme oldukça güncelleyin.</p>', ek_bas="İsteğe bağlı", attr=' data-ai-grup="ozet"')
             + fs("Kaynaklar", "fa-link", satir_liste("Kaynak", "Kaynak adı (kurum, belge)", "Açıklama, tarih ya da bağlantı", [
                 ("Meteoroloji Genel Müdürlüğü", "Marmara Bölgesi turuncu kodlu meteorolojik uyarı · 23 Kasım 2026"), ("İstanbul Valiliği", "Eğitime ara verilmesine ilişkin duyuru · 23 Kasım 2026"), ("Karayolları Genel Müdürlüğü", "Yol durumu ve ağır tonajlı araç kısıtlaması bildirimi")], "Kaynak ekle"), ek_bas="Sitede akışın sonunda")
             + fs("Anlatım ayarları", "fa-sliders", grid(
                 anahtar("Yeni girişler en üstte", "Kapalıysa akış eskiden yeniye sıralanır"),
                 anahtar("Okur sayfasında kendiliğinden yenile", "Okur sayfayı yenilemeden yeni girişleri görür (30 sn)"),
                 anahtar("Yorumlar Açık", "Yorumları editörler yönetir"))))
    form = (f'<section class="pnl-card" id="cmForm" data-form data-sekmeli data-zorunlu-kayit="haberler.canli" aria-label="Canlı anlatım formu">'
            + dil("Dil seçici bütün sekmelerdeki metin alanlarını birlikte değiştirir; girişlerin saati, görseli ve kaynağı bütün dillerde ortaktır.")
            + sekmeler([("pDetay", "Detay", "fa-file-lines", None), ("pAkis", "Akış", "fa-tower-broadcast", None), ("pSeo", "SEO", "fa-magnifying-glass-chart", None), ("pBildirim", "Bildirim", "fa-bell", "etkilesim"), ("pSosyal", "Sosyal Medya", "fa-share-nodes", "sosyal-medya")])
            + panel("pDetay", detay, ilk=True) + panel("pAkis", akis)
            + seo_panel("Marmara'da kar: gelişmeler dakika dakika | Dada Haber", "Marmara'da yoğun kar yağışı ulaşımı ve eğitimi etkiliyor. Okul tatilleri, sefer iptalleri ve yol durumu dakika dakika Dada Haber'de.", "dadahaber.com/dakika-dakika/", "marmarada-yogun-kar-yagisi", ["kar yağışı", "okullar tatil mi", "marmara kar"])
            + bildirim_panel("", "Marmara'da kar: İstanbul'da okullar yarın da tatil", "Valilik, eğitime 24 Kasım'da da ara verildiğini açıkladı. Gelişmeleri canlı takip edin.",
                frow("Hangi girişlerde", '<div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="cmBTur" checked>Yalnız kilit anlarda</label><label class="kb-secenek"><input type="radio" name="cmBTur">Her girişte</label><label class="kb-secenek"><input type="radio" name="cmBTur">Elle (girişte seçilir)</label></div>', ipucu="Bildirim yorgunluğunu önlemek için varsayılan: yalnız kilit anlar."))
            + sosyal_panel("", kp, "p180", (50, 45), {
                "x": "🔴 CANLI | Marmara'da yoğun kar: İstanbul'da okullar yarın da tatil, 46 sefer iptal. Gelişmeler dakika dakika:\n\nhttps://dadahaber.com/dakika-dakika/marmarada-yogun-kar-yagisi\n\n#kar #İstanbul",
                "facebook": "Marmara'da yoğun kar yağışı: İstanbul'da okullar yarın da tatil, havalimanlarında 46 sefer iptal edildi. Valilik ve kurum açıklamalarını geldikçe topluyoruz.\n\nhttps://dadahaber.com/dakika-dakika/marmarada-yogun-kar-yagisi",
                "linkedin": "Marmara'da kar yağışı iş ve ulaşım hayatını etkiliyor: okullar tatil, otoyolda tır kısıtlaması, sefer iptalleri. Gelişmeleri tek sayfada izleyin.\n\nhttps://dadahaber.com/dakika-dakika/marmarada-yogun-kar-yagisi",
                "instagram": "Marmara'da kar ❄️ İstanbul'da okullar yarın da tatil; 46 iç hat seferi iptal. Canlı akış profildeki bağlantıda.\n\n#kar #istanbul #dadahaber",
                "telegram": "🔴 CANLI · Marmara'da yoğun kar\n\nİstanbul'da okullar yarın da tatil; havalimanlarında 46 sefer iptal.\n\nhttps://dadahaber.com/dakika-dakika/marmarada-yogun-kar-yagisi"}, "dakika-dakika")
            + '</section>')
    yk = yayin_karti("cmY", [("canli", "Canlı"), ("bitti", "Sona Erdi", "yeni giriş eklenemez"), ("taslak", "Taslak", "yayından kalkar"), ("zamanli", "Zamanlanmış")], "canli", "2026-11-23 06.10",
        anahtar("Manşette", "Vitrinden sıralanır; slaytta “Canlı” rozeti", True, yeni=False) + anahtar("Son dakika şeridinde", "Kilit anlar şeride düşer", True, yeni=False),
        ("Sürüm 12", "son giriş 23.11.2026 16.05 · Mehmet Koçak", "?id=marmarada-yogun-kar-yagisi"), tarih_etk="Başlangıç", tarih_bos="Başlatılınca o anın saati")
    govde = bas("Canlı anlatım masası", "Marmara'da yoğun kar yağışı · <b>Canlı</b> · 06.10'dan beri · 10 giriş · 64,3 B okunma",
                [a_hedef("Canlı anlatımlara dön", "fa-arrow-left", "haberler.canli"), a_dis("Sitede Görüntüle", "fa-arrow-up-right-from-square", SITE + "dakika-dakika.html", " data-yeni-gizle"),
                 f'<button type="button" class="btn btn-ghost btn-sm danger" data-yeni-gizle{onay("Canlı anlatım kapatılsın mı?", "Önce: canlı, okurlar yeni girişleri anında görüyor → Sonra: “Sona erdi”; sayfa ve 10 giriş arşivde kalır, yeni giriş eklenemez. Gerekirse listeden yeniden açılır. İşlem denetim izine yazılır.", "Anlatımı kapat", True, "fa-circle-stop", bildir="Canlı anlatım kapatıldı; sayfa arşivde ve “Sona erdi” olarak görünüyor")}>{I("fa-circle-stop")}Anlatımı kapat</button>'],
                h1_yeni="Yeni canlı anlatım", alt_yeni="Taslak · henüz kaydedilmedi · yazar: oturumdaki kullanıcı")
    govde += f'  <div class="form-layout">\n  {form}\n  {yan(yan_onizleme("", "Marmara\'da kar: İstanbul\'da okullar yarın da tatil", "Valilik, eğitime 24 Kasım\'da da ara verildiğini açıkladı. Gelişmeleri canlı takip edin.", "p180", 50, 45, "Marmara\'da yoğun kar yağışı: gelişmeler dakika dakika"), yk, seo_skor(84, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Kapak görseli 1200 px üstü"), (False, "LiveBlogPosting şemasında bitiş saati yok")]))}\n  </div>\n'
    govde += kaydet("cmForm", "Kaydedildi · 23.11.2026 16.05 · Mehmet Koçak", "Güncelle", "Anlatım bilgileri güncellendi; sitede hemen görünür", "Yayına Al", "Canlı anlatım yayında; ilk girişi Akış sekmesinden ekleyin")
    sab.insert(0, sablon("cmYeni", "Yeni giriş", "Kaydedilince hemen akışın en üstünde görünür", giris_form("cmY0") + alt_cubuk(
        f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="cmTamam" data-bildir-sonra="Giriş yayımlandı; akışın en üstünde">{I("fa-paper-plane")}Yayımla</button>'), "haberler.canli-giris"))
    sab.append(sablon("cmTamam", "Giriş yayında", "Akış güncellendi; okurlar sayfayı yenilemeden görür",
        f'<div class="kb-bant tamam">{I("fa-circle-check")}<span><b>Yayında.</b> Giriş akışta saatine göre yerini aldı; işlem denetim izine yazıldı.</span></div>'
        + alt_cubuk(f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="cmYeni">{I("fa-plus")}Yeni giriş</button>')))
    YAZILDI.append(sayfa("canli-masa.html", "Canlı anlatım masası", "haberler.canli-masa", govde, "".join(sab), editor=True, body_ek=' data-yeni-baslik="Yeni canlı anlatım"'))

# ======================================================================= 5 · DOSYALAR VE FORMATLAR
DOSYALAR = [
    ("su", "İstanbul’un su sorunu: barajlardan musluğa bir yıl", "Keşfet", "İklim", "İrem Su", "yayinda", "23.11.2026 09.20", "8 olay · 3 taraf · 5 terim · 6 haber", "12,4 B", "p158", True),
    ("asgari", "Asgari ücret: kim, ne istiyor?", "Finans", "Çalışma Hayatı", "Nazlı Öztürk", "yayinda", "23.11.2026 14.20", "6 olay · 3 taraf · 4 terim · 9 haber", "6,9 B", "p188", True),
    ("faiz", "Faiz kararı cebine nasıl yansır?", "Finans", "Faiz Oranları", "İrem Su", "yayinda", "23.11.2026 14.45", "5 olay · 2 taraf · 6 terim · 4 haber", "12,2 B", "p192", False),
    ("kaan", "KAAN programı: prototipten seri üretime takvim", "Savunma", "Millî Projeler", "Mert Yalın", "yayinda", "22.11.2026 18.10", "9 olay · 2 taraf · 4 terim · 7 haber", "5,5 B", "p195", True),
    ("goc", "AB göç paketi: Türkiye için ne değişir?", "Dünya", "Göç", "Hande Polat", "yayinda", "22.11.2026 16.40", "7 olay · 4 taraf · 3 terim · 5 haber", "10,8 B", "p133", True),
    ("yks", "YKS 2027 rehberi: başvurudan tercihe", "Kampüs", "YKS", "Ozan Er", "yayinda", "22.11.2026 11.00", "6 olay · 2 taraf · 7 terim · 3 haber", "4,1 B", "p163", False),
    ("deprem", "Deprem bölgesinde konut: rakamlarla iki yıl", "Gündem", "Afet", "Kerem Aksoy", "yayinda", "21.11.2026 17.30", "10 olay · 3 taraf · 2 terim · 8 haber", "9,4 B", "p193", False),
    ("emisyon", "Emisyon ticaret sistemi nedir, kimleri kapsar?", "Keşfet", "İklim", "İrem Su", "taslak", "23.11.2026 15.10", "3 olay · 2 taraf · 6 terim · 2 haber", "—", "p155", False),
]
INCELEMELER = [
    ("asgari60", "Asgari ücrete ocakta yüzde 60 zam yapılacağı iddiası yanıltıcı", "Yanıltıcı", "Kerem Aksoy", "yayinda", "23.11.2026 11.40", "3 kaynak · 3 kanıt", "21,3 B", "p122"),
    ("kopru", "Kar altındaki köprü görüntüsü 2022 yılına ait", "Bağlam dışı", "İrem Su", "yayinda", "23.11.2026 10.05", "2 kaynak · 2 kanıt", "14,3 B", "p180"),
    ("lastik", "Kış lastiği zorunluluğu kaldırılmadı", "Yanlış", "İrem Su", "yayinda", "23.11.2026 15.50", "2 kaynak · 1 kanıt", "7,6 B", "p182"),
    ("organ", "Organ bağışı kayıtları bu yıl yüzde 12 arttı", "Doğru", "Ozan Er", "yayinda", "22.11.2026 13.15", "3 kaynak · 2 kanıt", "12,9 B", "p164"),
    ("kira", "Kira artışlarının yavaşladığına dair paylaşılan grafik eksik", "Eksik", "Ozan Er", "yayinda", "22.11.2026 10.40", "2 kaynak · 2 kanıt", "6,2 B", "p178"),
    ("yksoru", "YKS’de soru sayısının azaltılacağı iddiası doğrulanamadı", "Doğrulanamadı", "Nilay Ersoy", "yayinda", "22.11.2026 09.25", "1 kaynak · 0 kanıt", "11,5 B", "p163"),
    ("banka", "Bankaların hesaplara el koyacağı iddiası", "Yanlış", "Kerem Aksoy", "taslak", "23.11.2026 15.55", "Taslak · 1 kaynak", "—", "p192"),
]
KARAR = {"Doğru": ("ok", "Kaynaklarla uyumlu"), "Yanlış": ("warm", "Kanıtlar çürütüyor"), "Yanıltıcı": ("warm", "Doğru veri, yanlış sonuç"), "Eksik": ("wait", "Önemli bağlam atlanmış"),
         "Doğrulanamadı": ("off", "Yeterli kanıt yok"), "Bağlam dışı": ("wait", "Başka zamandan, başka yerden")}
def dosyalar():
    ds, dg = [], []
    for k, b, kb, ka, yz, d, gun, oz, gor, gs, gelis in DOSYALAR:
        href = f"dosya.html?id={k}"
        rz = rozet("ok", "Yayında") if d == "yayinda" else rozet("off", "Taslak")
        oz2 = " · ".join(x for x in oz.split(" · ") if "taraf" not in x and "terim" not in x)
        ds.append(tr(k, d, f"{b} {yz} {kb} {ka}", b, [ana_hucre(b, e(yz) + " · " + e(oz2) + (f' · {I("fa-arrows-rotate")}gelişiyor' if gelis else ""), gs, alt_ham=True), kat_hucre(kb, ka), (rz, ""), (f'<span class="kb-tarih{" muted" if d == "taslak" else ""}">{gun}</span>', "kb-gizle-m"), (gor, "say kb-gizle-t")],
            (ia_a(SITE + "dada-baglam-dosya.html", "Sitede Görüntüle", "fa-eye", True) if d == "yayinda" else ia_a(href, "Önizle", "fa-eye")) + ia_a(href, "Düzenle", "fa-pen") + SIL + DIGER, href=href, kategori=kb, yerler="manset" if k == "su" else ""))
    ds.append(tr("eski-dosya", "cop", "Kurban Bayramı tatili: kim, ne kadar izin kullanır?", "Kurban Bayramı tatili: kim, ne kadar izin kullanır?", [ana_hucre("Kurban Bayramı tatili: kim, ne kadar izin kullanır?", "Nazlı Öztürk · süresi geçti, çöpe taşındı", "p117"), kat_hucre("Finans", "Çalışma Hayatı"), (rozet("warm", "Çöpte"), ""), ('<span class="kb-tarih muted">12.06.2026 10.00</span>', "kb-gizle-m"), ("8,1 B", "say kb-gizle-t")],
        ia_a("dosya.html?id=eski-dosya", "Görüntüle", "fa-eye") + ia_a("dosya.html?id=eski-dosya", "Düzenle", "fa-pen") + SIL + DIGER, href="dosya.html?id=eski-dosya", kategori="Finans", onceki="yayinda"))
    for k, b, kr, yz, d, gun, oz, gor, gs in INCELEMELER:
        href = f"inceleme.html?id={k}"
        dg.append(tr(k, d, f"{b} {kr} {yz}", b, [ana_hucre(b, f"{yz} · {oz}", gs), (rozet(KARAR[kr][0], kr), "kb-gizle-m"), (rozet("ok", "Yayında") if d == "yayinda" else rozet("off", "Taslak"), ""),
            (f'<span class="kb-tarih{" muted" if d == "taslak" else ""}">{gun}</span>', "kb-gizle-m"), (gor, "say kb-gizle-t")],
            (ia_a(SITE + "dada-dogrula-inceleme.html", "Sitede Görüntüle", "fa-eye", True) if d == "yayinda" else ia_a(href, "Önizle", "fa-eye")) + ia_a(href, "Düzenle", "fa-pen") + SIL + DIGER, href=href, karar=kr))
    dg.append(tr("eski-inceleme", "cop", "Market raflarında ekmeğin 25 lira olacağı iddiası", "Market raflarında ekmeğin 25 lira olacağı iddiası", [ana_hucre("Market raflarında ekmeğin 25 lira olacağı iddiası", "Kerem Aksoy · mükerrer kayıt, çöpe taşındı", "p183"), (rozet("off", "Doğrulanamadı"), "kb-gizle-m"), (rozet("warm", "Çöpte"), ""), ('<span class="kb-tarih muted">19.11.2026 12.10</span>', "kb-gizle-m"), ("—", "say kb-gizle-t")],
        ia_a("inceleme.html?id=eski-inceleme", "Görüntüle", "fa-eye") + ia_a("inceleme.html?id=eski-inceleme", "Düzenle", "fa-pen") + SIL + DIGER, href="inceleme.html?id=eski-inceleme", karar="Doğrulanamadı", onceki="taslak"))
    def menu(tur):
        return (m_grup("Yayın", "yayinda taslak")
                + m_btn("Şimdi yayımla", "fa-paper-plane", "taslak", onay(f"{tur} yayımlansın mı?", "Hemen sitede görünür; işlem denetim izine yazılır.", "Yayımla", ikon="fa-paper-plane", sonra=("yayinda", "Yayında", "ok"), bildir=f"{tur} yayımlandı"))
                + f'<button type="button" data-durum-icin="yayinda" data-roller="super gyy editor" data-yer="manset" data-yer-ad="Manşet">{I("fa-star")}<span>Manşete ekle</span></button>'
                + m_btn("Yayından kaldır", "fa-eye-slash", "yayinda", onay(f"{tur} yayından kaldırılsın mı?", "Sitedeki sayfa kapanır, kayıt taslak olarak kalır; bağlı haberlerdeki kutu gizlenir.", "Yayından kaldır", True, "fa-eye-slash", sonra=("taslak", "Taslak", "off"), bildir="Yayından kaldırıldı; taslakta"))
                + m_ayir("yayinda taslak") + m_grup("İçerik", "yayinda taslak")
                + (m_a("Kronolojiye olay ekle", "fa-timeline", "haberler.dosya", "?sekme=pKronoloji", ' data-durum-icin="yayinda taslak"') if tur == "Olay dosyası" else m_a("Karar değişikliği notu ekle", "fa-pen-to-square", "haberler.surumler", "?sekme=pNotlar", ' data-durum-icin="yayinda"'))
                + m_btn("Bağlantıyı kopyala", "fa-link", "yayinda", " data-kopyala")
                + m_ayir("yayinda taslak") + m_grup("Kayıt") + m_a("Sürüm Geçmişi", "fa-clock-rotate-left", "haberler.surumler") + DENETIM + COP_MENU)
    bs = lambda ad: [('<input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünenlerin hepsini seç">', "kb-sec-hucre"), (ad, "kb-ana")]
    L1 = liste("dosya", "Dada Bağlam olay dosyaları", [("hepsi", "Tümü", 16), ("yayinda", "Yayında", 16), ("taslak", "Taslak", 0)], "Dosya Adı, Yazar ya da Kategori Ara",
        [("kategori", "Kategori", "dsSuzKat", [("", "Bütün Kategoriler")] + [(b, b) for b in ["Gündem", "Finans", "Savunma", "Dünya", "Kampüs", "Keşfet"]], None)],
        [btn("Yayından kaldır", "fa-eye-slash", attr=' data-toplu="taslak" data-bildir="Seçilen dosyalar yayından kaldırılıp taslağa alındı"'), btn("Çöpe Taşı", "fa-trash", "btn-ghost danger", ' data-toplu="cop"')],
        bs("Olay dosyası") + [("Kategori", "kb-gizle-m"), ("Durum", ""), ("Güncellendi", "kb-gizle-m"), ("Okunma", "say kb-gizle-t"), ('<span class="sr-only">İşlemler</span>', "")],
        ds, menu("Olay dosyası"), bos_durum("dosyalar.html", "Olay dosyaları yüklenemedi", "fa-folder-open", "Henüz olay dosyası yok", "Uzun süren bir konuyu zaman çizgisi, taraflar ve sözlükle anlatmak için dosya açın.", f'<a class="pe-tag" data-hedef="haberler.dosya" data-hedef-ek="?yeni=1" href="#">{I("fa-plus")}Yeni olay dosyası</a>'),
        "24 sonuçtan 1–8 gösteriliyor", liste_cop_not="Sitedeki dosya sayfası kapanır ve Çöp sekmesine taşınır; bağlı haberler etkilenmez")
    L2 = liste("inceleme", "Dada Doğrula incelemeleri", [("hepsi", "Tümü", 179), ("yayinda", "Yayında", 179), ("taslak", "Taslak", 0)], "İddia, yazar ya da karar ara",
        [("karar", "Karar", "dgSuzKarar", [("", "Bütün kararlar")] + [(k, k, v[1]) for k, v in KARAR.items()], None)],
        [btn("Yayından kaldır", "fa-eye-slash", attr=' data-toplu="taslak" data-bildir="Seçilen incelemeler yayından kaldırılıp taslağa alındı"'), btn("Çöpe Taşı", "fa-trash", "btn-ghost danger", ' data-toplu="cop"')],
        bs("İnceleme") + [("Karar", "kb-gizle-m"), ("Durum", ""), ("Güncellendi", "kb-gizle-m"), ("Okunma", "say kb-gizle-t"), ('<span class="sr-only">İşlemler</span>', "")],
        dg, menu("İnceleme"), bos_durum("dosyalar.html?sekme=pDogrula", "İncelemeler yüklenemedi", "fa-scale-balanced", "Henüz inceleme yok", "Gündemdeki bir iddiayı kaynağıyla incelemek için yeni inceleme açın.", f'<a class="pe-tag" data-hedef="haberler.inceleme" data-hedef-ek="?yeni=1" href="#">{I("fa-plus")}Yeni inceleme</a>'),
        "186 sonuçtan 1–7 gösteriliyor", liste_cop_not="Sitedeki inceleme sayfası kapanır ve Çöp sekmesine taşınır")
    govde = bas("Dosyalar ve Formatlar", "Dada Bağlam olay dosyaları ve Dada Doğrula incelemeleri · Günün 5'i: sabah baskısı 24.11.2026 07.00'de çıkacak",
                [a_hedef("Günün 5'i", "fa-list-ol", "haberler.gunun-5"), a_hedef("Yeni inceleme", "fa-scale-balanced", "haberler.inceleme", "?yeni=1"), a_hedef("Yeni olay dosyası", "fa-plus", "haberler.dosya", "?yeni=1", "btn-acc")])
    govde += ('  <div data-sekmeli>' + sekmeler([("pBaglam", "Dada Bağlam · olay dosyaları", "fa-folder-open", None), ("pDogrula", "Dada Doğrula · incelemeler", "fa-scale-balanced", None)], "Format sekmeleri")
              + panel("pBaglam", L1, ilk=True) + panel("pDogrula", L2) + '</div>\n')
    YAZILDI.append(sayfa("dosyalar.html", "Dosyalar ve Formatlar", "haberler.dosyalar", govde))

# ======================================================================= 6 · OLAY DOSYASI DÜZENLE
OLAYLAR = [("Yağış ortalamanın altında kaldı", "2025-03-01", "Mart 2025", "Kış yağışları uzun yıllar ortalamasının yüzde 30 altında ölçüldü; barajlara giriş azaldı.", "Meteoroloji Genel Müdürlüğü"),
           ("Tasarruf çağrısı yapıldı", "2025-06-01", "Haziran 2025", "Su idaresi, yaz aylarında bahçe sulaması ve araç yıkamasında kısıtlamaya gitti.", "İstanbul su idaresi"),
           ("Doluluk yüzde 40’ın altına indi", "2025-09-01", "Eylül 2025", "Barajlardaki aktif doluluk son on yılın en düşük eylül değerine geriledi.", "İstanbul su idaresi"),
           ("Kuraklık eylem planı açıklandı", "2025-12-01", "Aralık 2025", "Plan; kayıp-kaçak oranını düşürme, gri su kullanımı ve yeni iletim hatlarını içeriyor.", "Su idaresi meclis kararı"),
           ("İletim hattı ihalesi yapıldı", "2026-03-01", "Mart 2026", "Komşu havzadan su taşıyacak 62 kilometrelik hattın ihalesi tamamlandı.", "İstanbul su idaresi"),
           ("Kademeli tarife başladı", "2026-07-01", "Temmuz 2026", "Yüksek tüketimli konutlar için kademeli su tarifesi yürürlüğe girdi.", "İstanbul su idaresi"),
           ("Tüketim yüzde 7 azaldı", "2026-10-01", "Ekim 2026", "Su idaresi, kişi başı günlük tüketimin bir yılda yüzde 7 azaldığını açıkladı.", "İstanbul su idaresi"),
           ("Doluluk yüzde 38’de", "2026-11-22", "22 Kasım 2026", "Kasım yağışlarına rağmen aktif doluluk yüzde 38 ile geçen yılın gerisinde.", "İstanbul su idaresi")]
def olay_form(onek, o=None):
    b, t, gos, ac, kyn = o if o else ("", "", "", "", None)
    ay = bool(o) and not gos[0].isdigit()
    return (dil("Dil seçici başlığı ve açıklamayı birlikte değiştirir; tarih ve kaynak bütün dillerde ortaktır.", kap=True)
            + kfs("Olay", frow("Tarih", tarih(f"{onek}T", t, saatsiz=True, ek=' data-alan-id="tarih"'), ipucu="Kronoloji tarihe göre kendiliğinden sıralanır.")
                  + anahtar("Yalnız ay ve yıl göster", "Sitede “Mart 2025” gibi; gün belli değilse açın", ay)
                  + girdi(f"{onek}B", "Olay başlığı", b, "baslik", "60|80", "Zaman çizgisinde kalın satır", hata="Olay başlığı zorunlu.")
                  + alan(f"{onek}A", "Açıklama", ac, "aciklama", "200|260", "Zaman çizgisinde başlığın altında", rows=3)
                  + frow("Kaynak", cip_girdi([kyn] if kyn else [], ["İstanbul su idaresi", "Meteoroloji Genel Müdürlüğü", "Su idaresi meclis kararı", "Üniversite raporu"], "Kaynak ara", ek=' data-havuz-yonet data-kullanim-birim="olayda"'))))
def dosya():
    sab = []
    satirlar = []
    for i, o in enumerate(OLAYLAR):
        tid = f"dsO{i}"
        sab.append(sablon(tid, "Olay · düzenle", o[2], olay_form(tid, o) + alt_cubuk(
            f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="dsTamam" data-baslik-yaz="Olay güncellendi" data-bildir-sonra="Olay güncellendi; kaydedince dosyada görünür">{I("fa-check")}Tamam</button>')))
        satirlar.append(f'<div class="km-satir" data-yeni-gizle><span class="kb-tarih">{e(o[2])}</span><span class="km-yazi">{e(o[0])}<small>{e(o[3])}</small></span>'
                        f'<button type="button" class="ia-btn" data-tanim="{tid}" aria-label="Olayı düzenle" title="Düzenle">{I("fa-pen")}</button>'
                        f'<button type="button" class="ia-btn danger" data-satir-sil aria-label="Olayı kaldır" title="Kaldır">{I("fa-trash")}</button></div>')
    sab.insert(0, sablon("dsOlayYeni", "Kronolojiye olay ekle", "Tarihe göre yerini alır; dosya kaydedilince sitede görünür", olay_form("dsOY") + alt_cubuk(
        f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="dsTamam" data-bildir-sonra="Olay eklendi; kaydedince dosyada görünür">{I("fa-plus")}Ekle</button>')))
    sab.append(sablon("dsTamam", "Kronoloji güncellendi", "Değişiklik dosya kaydedilince yayına yansır",
        f'<div class="kb-bant tamam">{I("fa-circle-check")}<span><b>Hazır.</b> Olay kronolojide tarihine göre yerini aldı. Yayına yansıması için sayfanın altındaki “Güncelle” ile kaydedin.</span></div>'
        + alt_cubuk(f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="dsOlayYeni">{I("fa-plus")}Yeni olay</button>')))
    kp = "dsKapak"
    detay = (fs("Dosya", "fa-folder-open", grid(
                girdi("dsBaslik", "Başlık", "İstanbul’un su sorunu: barajlardan musluğa bir yıl", "baslik", "70|90", "Sitede dosya başlığı; SEO başlığı buradan üretilir", cls="finput kb-buyuk", ek=' data-alan="baslik"', hata="Başlık zorunlu."),
                alan("dsSpot", "Spot", "Barajlarda doluluk iki yıldır normalin altında. Kuraklığın nasıl başladığını, alınan önlemleri ve tarafların görüşlerini zaman çizgisi ve sözlükle anlatıyoruz.", "spot", "220|280", "Başlığın altındaki giriş cümlesi", ek=' data-alan="spot"', hata="Spot zorunlu.")))
             + ai_adim("#dsBaslik,#dsSpot", [("ozet", "Özet metni taslağı", True, None), ("sinif", "Kategori ve Alt Konular", True, None), ("sozluk", "Sözlük önerileri", True, None), ("seo", "SEO", True, None), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")])
             + fs("Sınıflandırma", "fa-sitemap", grid(kategori_alanlari("ds", "Keşfet", ["İklim", "Dada Bağlam"]), yazar_alani("dsYazar", "İrem Su")), attr=' data-ai-grup="sinif"')
             + kapak(kp, "p158", (50, 50), "Kaynak: Dada Haber arşivi", "Ömerli Barajı, kasım 2026 · Dada Haber arşivi")
             + fs("Özet", "fa-align-left", editor("Dosya özeti", "<p>İstanbul’un içme suyunu sağlayan barajlarda doluluk iki yıldır mevsim normallerinin altında seyrediyor. Bu dosya, sorunun nasıl başladığını, hangi adımların atıldığını ve önümüzdeki dönemde neyin değişeceğini tek yerde topluyor.</p>", "ozet", zm="Dosyanın özet metnini yazın", alt="Sitede başlığın altında; “Dinle” bu metinden okunur"), ek_bas="Dosyanın asıl metni", attr=' data-ai-grup="ozet"')
             + fs("Kaynaklar", "fa-link", satir_liste("Kaynak", "Kaynak adı (kurum, belge)", "Açıklama, tarih ya da bağlantı", [
                 ("İstanbul su idaresi", "Baraj doluluk oranları, günlük veri · 22 Kasım 2026"), ("Meteoroloji Genel Müdürlüğü", "Bölgesel yağış raporu, Ekim 2026"), ("Kuraklık eylem planı", "Su idaresi meclis kararı, Aralık 2025")], "Kaynak ekle"), ek_bas="Sitede dosyanın sonunda")
             + fs("Dosya ayarları", "fa-sliders", grid(anahtar("Gelişen olay", "Listede “Gelişiyor” rozeti; bağlı haberlerin sonunda “Dosyanın devamı” kutusu görünür"), anahtar("Yorumlar Açık", "Yorumları editörler yönetir"))))
    kron = (f'<div class="form-sec"><div class="form-sec-tt">{I("fa-timeline")}Zaman çizgisi<span class="fs-ek"><button type="button" class="btn btn-ghost btn-sm" data-tanim="dsOlayYeni">{I("fa-plus")}Olay ekle</button></span></div>'
            f'<div class="kb-madde" data-satir-liste data-satir-ad="Olay">{"".join(satirlar)}</div><p class="fhint">Olaylar tarihe göre kendiliğinden sıralanır; en yenisi sitede altta, “Güncellendi” saatiyle görünür. Kalem olayı düzenler, çöp onaysız kaldırır (Geri al).</p></div>')
    taraf = (fs("Taraflar ne diyor?", "fa-people-arrows", alan("dsTarafGiris", "Giriş cümlesi", "Konunun üç ana tarafı aynı hedefte buluşuyor: tüketimi azaltmak ve kaynakları çeşitlendirmek. Öncelik sırası ise farklı.", sayac="200|260", ipucu="Taraflar bölümünün başında", rows=2)
                + satir_liste("Taraf", "Taraf (kurum ya da kişi)", "Görüşü ve kaynağı", [
                    ("Su idaresi", "Kayıp-kaçak oranını yüzde 18’e indirmeyi ve yeni iletim hattını 2027’de devreye almayı hedefliyor. Kuraklık eylem planı · Aralık 2025"),
                    ("Merkezî yönetim", "Havzalar arası su aktarımını ve tarımda damla sulamayı destekleyen bütçeyi artırdı. Bütçe gerekçesi · Ekim 2026"),
                    ("Uzmanlar", "Talep yönetimi olmadan yeni kaynakların yetmeyeceğini, gri su kullanımının yaygınlaşması gerektiğini söylüyor. Üniversite raporu · Eylül 2026")], "Taraf ekle"), ek_bas="Sürükleyerek sıralayın")
             + fs("Dosya sözlüğü", "fa-book", satir_liste("Terim", "Terim", "Tanım", [
                    ("Aktif doluluk", "Barajda kullanılabilir durumdaki suyun toplam kapasiteye oranı. Ölü hacim bu hesaba girmez."),
                    ("Ölü hacim", "Baraj gövdesinin altında kalan ve pompalanamayan su miktarı."),
                    ("Kayıp-kaçak oranı", "Şebekeye verilen su ile aboneye ulaşan su arasındaki farkın yüzdesi."),
                    ("Gri su", "Lavabo ve duştan gelen, arıtılarak sulama ya da rezervuarda yeniden kullanılabilen su."),
                    ("Kademeli tarife", "Tüketim arttıkça metreküp fiyatının yükseldiği fiyatlandırma.")], "Terim ekle"), ek_bas="Sitede alfabetik; terim metinde altı çizili görünür", attr=' data-ai-grup="sozluk"'))
    bagli_h = [("Barajlardaki doluluk oranı İstanbul’da yüzde 38’e geriledi", "Keşfet", "İklim", "Ayşe Yıldız", "23.11 11.40", "", "p158", "barajlarda-doluluk-yuzde-38"),
               ("Konya Ovası’nda yeraltı suyu seviyesi bir yılda 3 metre düştü", "Keşfet", "İklim", "Ozan Er", "23.11 10.15", "", "p164", "konya-ovasi-yeralti-suyu"),
               ("Büyükşehirlerde su tüketimi tek tabloda", "Keşfet", "Veri ve Harita", "Ozan Er", "22.11 16.20", "", "p155", "buyuksehirlerde-su-tuketimi"),
               ("İstanbul’da kademeli su tarifesi yürürlüğe girdi", "Gündem", "İstanbul", "Sibel Arslan", "01.07 09.30", "", "p183", "kademeli-su-tarifesi")]
    bagli = (fs("Bağlı haberler", "fa-newspaper", sirali("dsBagli", bagli_h, bagli_h + HABERLER_SEC, 20, "Haber", "Yayındaki haberlerde ara", alan_id="bagli")
                 + '<p class="fhint kb-ust-bosluk">Yalnız yayındaki haberler seçilir; sıra dosyadaki “İlgili içerikler” sırasıdır. Bağlı haberin sonunda “Dosyanın devamı” kutusu görünür. Haberler listesindeki ⋯ → “Olay dosyasına bağla” da buraya ekler.</p>'
                 + grid(anahtar("Yeni haberleri öner", "Aynı alt konu ve anahtar kelimeyle yayımlanan haber, editöre “bu dosyaya bağla” önerisi olarak gelir"), cls="kb-ust-bosluk"), ek_bas="4 haber · en çok 20"))
    form = (f'<section class="pnl-card" id="dsForm" data-form data-sekmeli data-zorunlu-kayit="haberler.dosya" aria-label="Olay dosyası formu">'
            + dil("Dil seçici bütün sekmelerdeki metin alanlarını birlikte değiştirir; tarih, görsel, kategori ve bağlı haberler bütün dillerde ortaktır.")
            + sekmeler([("pDetay", "Detay", "fa-file-lines", None), ("pKronoloji", "Kronoloji", "fa-timeline", None), ("pTaraf", "Taraflar ve sözlük", "fa-people-arrows", None), ("pBagli", "Bağlı haberler", "fa-newspaper", None),
                        ("pSeo", "SEO", "fa-magnifying-glass-chart", None), ("pBildirim", "Bildirim", "fa-bell", "etkilesim"), ("pSosyal", "Sosyal Medya", "fa-share-nodes", "sosyal-medya")])
            + panel("pDetay", detay, ilk=True) + panel("pKronoloji", kron) + panel("pTaraf", taraf) + panel("pBagli", bagli)
            + seo_panel("İstanbul’un su sorunu: barajlardan musluğa | Dada Haber", "İstanbul barajlarında doluluk neden düşük? Kuraklığın başlangıcı, alınan önlemler, taraflar ve sözlükle bir yılın zaman çizgisi.", "dadahaber.com/dada-baglam/", "istanbulun-su-sorunu", ["istanbul baraj doluluk", "kuraklık", "su tasarrufu"])
            + bildirim_panel("", "Su dosyası güncellendi: doluluk yüzde 38", "Kasım yağışlarına rağmen barajlar geçen yılın gerisinde. Bir yılın zaman çizgisi Dada Bağlam'da.")
            + sosyal_panel("", kp, "p158", (50, 50), {
                "x": "İstanbul’un su sorunu tek dosyada: barajlarda doluluk %38. Kuraklık nasıl başladı, neler yapıldı, sırada ne var?\n\nhttps://dadahaber.com/dada-baglam/istanbulun-su-sorunu\n\n#İstanbul #kuraklık",
                "facebook": "Barajlardan musluğa bir yıl: İstanbul’un su sorununu zaman çizgisi, taraflar ve sözlükle anlattık.\n\nhttps://dadahaber.com/dada-baglam/istanbulun-su-sorunu",
                "linkedin": "Su yönetiminde bir yıl: kayıp-kaçak hedefi, kademeli tarife ve yeni iletim hattı. Dada Bağlam dosyası.\n\nhttps://dadahaber.com/dada-baglam/istanbulun-su-sorunu",
                "instagram": "Barajlarda doluluk %38 💧 Kuraklığın bir yılı tek dosyada; bağlantı profilde.\n\n#istanbul #kuraklık #dadahaber",
                "telegram": "📁 Dada Bağlam · İstanbul’un su sorunu\n\nDoluluk %38; bir yılın zaman çizgisi ve sözlük.\n\nhttps://dadahaber.com/dada-baglam/istanbulun-su-sorunu"}, "dada-baglam")
            + '</section>')
    yk = yayin_karti("dsY", [("yayinda", "Yayında"), ("taslak", "Taslak", "yayından kalkar"), ("zamanli", "Zamanlanmış")], "yayinda", "2026-11-22 10.30",
        anahtar("Manşette", "Vitrinden sıralanır", True, yeni=False) + anahtar("Keşfet › Dada Bağlam'da öne çıkan", "Dosya listesinin başında büyük kartla", True, yeni=False),
        ("Sürüm 9", "son değişiklik 23.11.2026 09.20 · İrem Su", "?id=istanbulun-su-sorunu"))
    govde = bas("Olay dosyası düzenle", "Dada Bağlam · Keşfet › İklim · İrem Su · 22.11.2026 10.30'da yayımlandı · 23.11.2026 09.20'de güncellendi · 12,4 B okunma",
                [a_hedef("Dosyalara dön", "fa-arrow-left", "haberler.dosyalar"), a_dis("Sitede Görüntüle", "fa-arrow-up-right-from-square", SITE + "dada-baglam-dosya.html", " data-yeni-gizle")],
                h1_yeni="Yeni olay dosyası", alt_yeni="Dada Bağlam · taslak · henüz kaydedilmedi · yazar: oturumdaki kullanıcı")
    govde += f'  <div class="form-layout">\n  {form}\n  {yan(yan_onizleme("", "Su dosyası güncellendi: doluluk yüzde 38", "Kasım yağışlarına rağmen barajlar geçen yılın gerisinde. Bir yılın zaman çizgisi Dada Bağlam\'da.", "p158", 50, 50, "İstanbul’un su sorunu: barajlardan musluğa bir yıl"), yk, seo_skor(88, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Kapak görseli 1200 px üstü"), (True, "6 bağlı haber ile iç bağlantı")]))}\n  </div>\n'
    govde += kaydet("dsForm", "Kaydedildi · 23.11.2026 09.20 · İrem Su", "Güncelle", "Dosya güncellendi; sitede yayında, önceki hal sürüm geçmişinde", "Yayımla", "Olay dosyası yayımlandı; Keşfet › Dada Bağlam'da görünür")
    YAZILDI.append(sayfa("dosya.html", "Olay dosyası düzenle", "haberler.dosya", govde, "".join(sab), editor=True, body_ek=' data-yeni-baslik="Yeni olay dosyası"'))

# ======================================================================= 7 · GÜNÜN 5'İ
G5 = [("Asgari ücret komisyonu 4 Aralık’ta toplanıyor", "İşçi ve işveren tarafı ilk kez masaya oturuyor; karar yıl sonuna kadar bekleniyor.", "Gündem · 3 dk", "p188"),
      ("Politika faizi yüzde 42,5’te sabit kaldı", "Merkez Bankası beklentilere uygun karar verdi; kredi faizlerinde hızlı düşüş beklenmiyor.", "Finans · 2 dk", "p192"),
      ("Doğuda kar yağışı: 214 köy yolu kapalı", "Erzurum, Kars ve Ağrı'da ekipler kapalı yolları açmak için çalışıyor.", "Gündem · 2 dk", "p182"),
      ("AB göç paketinde oylama ocağa kaldı", "Dışişleri bakanları uzlaşamadı; Türkiye ile geri kabul maddesi yeniden yazılacak.", "Dünya · 3 dk", "p133"),
      ("YKS 2027 başvuru tarihleri belli oldu", "Başvurular 6 Şubat'ta başlıyor; sınav 20-21 Haziran'da yapılacak.", "Kampüs · 2 dk", "p163")]
def gunun_5():
    G5H = [("Asgari ücret komisyonu 4 Aralık’ta toplanıyor", "Gündem", "Türkiye", "Hakan Uysal", "23.11 14.05", "", "p188", "asgari-ucret-gorusmelerinde-ilk-toplanti-4-aralikta-yapilacak"),
           ("Politika faizi yüzde 42,5’te sabit kaldı", "Finans", "Faiz Oranları", "Elif Aras", "23.11 14.00", "", "p192", "merkez-bankasi-politika-faizini-yuzde-42-5te-sabit-tuttu"),
           ("Doğuda kar yağışı: 214 köy yolu kapalı", "Gündem", "Afet", "Ayşe Yıldız", "23.11 15.35", "", "p182", "doguda-kar-yagisi-214-koy-yolu-kapali"),
           ("AB göç paketinde oylama ocağa kaldı", "Dünya", "Avrupa", "Zeynep Ak", "23.11 13.25", "", "p133", "ab-disisleri-bakanlari-goc-paketini-gorustu"),
           ("YKS 2027 başvuru tarihleri belli oldu", "Kampüs", "YKS", "Aslı Gür", "23.11 14.50", "", "p163", "yks-2027-tarihleri-tek-ekranda")]
    kp = "g5Kapak"
    detay = (fs("Baskı", "fa-calendar-day", grid(
                f'<div class="frow two"><div class="frow"><span class="flabel">Tarih</span>{tarih("g5Tarih", "2026-11-24", saatsiz=True, ek=chr(32) + "data-alan-id=" + chr(34) + "tarih" + chr(34))}</div>'
                f'<div class="frow"><span class="flabel">Baskı</span><div class="kb-kart-sec"><label class="kb-secenek kb-secenek-kart"><input type="radio" name="g5Baski" checked><span><b>Sabah · 07.00</b><small>Güne başlarken</small></span></label><label class="kb-secenek kb-secenek-kart"><input type="radio" name="g5Baski"><span><b>Akşam · 18.00</b><small>Günün özeti</small></span></label></div></div></div>',
                girdi("g5Baslik", "Başlık", "Bugünü anlamak için beş haber: komisyon, faiz, kar, göç, sınav", "baslik", "70|90", "Sitede baskının başlığı; SEO ve bildirim buradan üretilir", cls="finput kb-buyuk", ek=' data-alan="baslik"', hata="Başlık zorunlu."),
                alan("g5Spot", "Kısa giriş", "Komisyon masaya oturuyor, faiz sabit, doğuda kar etkili. Beş haberi okuyarak 12, dinleyerek 9 dakikada bitirin.", None, "160|200", "İsteğe bağlı · sitede başlığın altında", ek=' data-alan="spot"', rows=2)))
             + ai_adim("#g5Baslik", [("sec", "Beş haber önerisi (en çok okunan + editör seçkisi)", False, None), ("seo", "SEO", True, None), ("bildirim", "Bildirim Metni", True, "etkilesim"), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")], durum="Başlığı yazın; işaretli bölümler başlıktan ve seçilen beş haberden üretilir.", neden="Önce başlık")
             + fs("Beş haber", "fa-list-ol", sirali("g5Sira", G5H, HABERLER_SEC, 5, "Haber", "Haber ekle", alan_id="haberler")
                  + '<p class="fhint kb-ust-bosluk">Sürükleyerek ya da tutamaç seçiliyken ↑/↓ ile sıralayın; × onaysız çıkarır, “Geri al” ile döner. Beş dolunca ekleme kapanır. Haberler listesindeki ⋯ → “Günün 5\'ine ekle” de buraya ekler. Sitede her haberin spotu görünür.</p>', ek_bas="5 / 5 · sıraya bağlı önizleme")
             + kapak(kp, "p188", (50, 40), "1. haberin kapağı · değiştirilebilir", "Günün 5'i · 24 Kasım 2026 sabah baskısı")
             + fs("Dinleme", "fa-headphones", grid(anahtar("Sesli özet", "Beş haber art arda okunur (Haber Dinle · yaklaşık 9 dk)"), anahtar("E-bülten olarak da gönder", "Günün 5'i bültenine abone olanlara baskı saatinde gider", True, kap_ek=' data-modul="etkilesim"'))))
    form = (f'<section class="pnl-card" id="g5Form" data-form data-sekmeli data-zorunlu-kayit="haberler.gunun-5" aria-label="Günün 5\'i formu">'
            + dil("Dil seçici başlığı, girişi ve tek cümleleri birlikte değiştirir; seçilen haberler ve görsel bütün dillerde ortaktır.")
            + sekmeler([("pDetay", "Detay", "fa-list-ol", None), ("pSeo", "SEO", "fa-magnifying-glass-chart", None), ("pBildirim", "Bildirim", "fa-bell", "etkilesim"), ("pSosyal", "Sosyal Medya", "fa-share-nodes", "sosyal-medya")])
            + panel("pDetay", detay, ilk=True)
            + seo_panel("Günün 5'i · 24 Kasım 2026 | Dada Haber", "Bugünü anlamak için beş haber: asgari ücret komisyonu, faiz kararı, doğuda kar, AB göç paketi ve YKS 2027 tarihleri.", "dadahaber.com/gunun-5-i/", "24-kasim-2026-sabah", ["günün haberleri", "24 kasım 2026", "gündem özeti"])
            + bildirim_panel("", "Günün 5'i: komisyon, faiz, kar, göç, sınav", "Bugünü anlamak için beş haber; okuyarak 12, dinleyerek 9 dakika.")
            + sosyal_panel("", kp, "p188", (50, 40), {
                "x": "☕ Günün 5'i\n\n1. Asgari ücret komisyonu 4 Aralık’ta toplanıyor\n2. Faiz %42,5’te sabit\n3. Doğuda 214 köy yolu kapalı\n4. AB göç paketi ocağa kaldı\n5. YKS 2027 tarihleri belli\n\nhttps://dadahaber.com/gunun-5-i",
                "facebook": "Bugünü anlamak için beş haber: komisyon, faiz, kar, göç ve sınav. Okuyarak 12, dinleyerek 9 dakika.\n\nhttps://dadahaber.com/gunun-5-i",
                "linkedin": "Güne başlarken beş başlık: asgari ücret takvimi, faiz kararı, AB göç paketi ve YKS 2027.\n\nhttps://dadahaber.com/gunun-5-i",
                "instagram": "Günün 5'i ☕ Kaydır, beş haberi 1 dakikada öğren. Tamamı profildeki bağlantıda.\n\n#günün5i #dadahaber",
                "telegram": "☕ Günün 5'i · 24 Kasım\n\n1. Asgari ücret komisyonu 4 Aralık’ta\n2. Faiz %42,5’te sabit\n3. Doğuda kar: 214 köy yolu kapalı\n4. AB göç paketi ocağa kaldı\n5. YKS 2027 tarihleri belli\n\nhttps://dadahaber.com/gunun-5-i"}, "gunun-5-i")
            + '</section>')
    onizle = kart("Önizleme", "fa-eye", f'<div class="kb-onizle-kap"><p class="kb-ozet-baslik">Bugünün 5 Haberi</p><p class="fhint">24 Kasım 2026 · 07.00 · Okuyarak 12 dk · Dinleyerek 9 dk</p><div class="kb-madde" data-sira-onizleme="#g5Sira">'
        + "".join(f'<div class="km-satir" data-oniz-yer><span class="km-no">{n}</span><span class="km-yazi" data-oniz-baslik></span></div>' for n in range(1, 6))
        + '</div><p class="kb-onizle-not">Sıra değişince güncellenir; sitede Günün 5\'i sayfası ve ana sayfa bandı.</p></div>', sag=rozet("info", "Zamanlanmış"))
    yk = yayin_karti("g5Y", [("zamanli", "Zamanlanmış"), ("yayinda", "Yayında"), ("taslak", "Taslak", "yayından kalkar")], "zamanli", "2026-11-24 07.00",
        anahtar("Ana sayfa bandında", "Ana sayfadaki Günün 5'i bandında gösterilir", True), ("Sürüm 3", "son değişiklik 23.11.2026 15.40 · İrem Su", "?id=gunun-5-24-kasim-2026-sabah"),
        tarih_bos="Baskı saatinde (07.00 / 18.00)")
    once = kart("Önceki baskılar", "fa-clock-rotate-left", govde_cls=None, ic='<div class="pc-body sa-gecmis">' + "".join(f'<div><b>{e(b)}</b><span>{e(a)}</span></div>' for b, a in [
        ("23 Kasım · sabah: komisyon, faiz, kar, göç, sınav", "İrem Su · 18,2 B okunma"), ("22 Kasım · akşam: bütçe görüşmeleri, kira verisi, enerji hattı", "İrem Su · 9,9 B okunma"),
        ("21 Kasım · akşam: enflasyon beklentisi, kitap fuarı, millî takım", "İrem Su · 3,2 B okunma")]) + f'<a class="kb-bag" href="{SITE}gunun-5-i.html" target="_blank" rel="noopener">Sitede bütün arşiv (365 baskı)</a></div>')
    govde = bas("Günün 5'i", "Sabah baskısı · 24.11.2026 Salı 07.00'de yayımlanacak · akşam baskısı 18.00 · İrem Su",
                [a_hedef("Dosyalar ve Formatlar", "fa-arrow-left", "haberler.dosyalar"), a_dis("Sitede Görüntüle", "fa-arrow-up-right-from-square", SITE + "gunun-5-i.html")])
    govde += f'  <div class="form-layout">\n  {form}\n  {yan(yan_onizleme("", "Günün 5\'i: komisyon, faiz, kar, göç, sınav", "Bugünü anlamak için beş haber; okuyarak 12, dinleyerek 9 dakika.", "p188", 50, 40, "Günün 5\'i · 24 Kasım 2026"), onizle, yk, seo_skor(81, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "5 haberle iç bağlantı"), (False, "Kısa giriş 120 karakterin altında")]), once)}\n  </div>\n'
    govde += kaydet("g5Form", "Kaydedildi · 23.11.2026 15.40 · İrem Su", "Zamanla", "Günün 5'i 24.11.2026 07.00 için zamanlandı; önceki hal sürüm geçmişinde")
    YAZILDI.append(sayfa("gunun-5.html", "Günün 5'i", "haberler.gunun-5", govde, editor=False))

# ======================================================================= 8 · DOĞRULAMA İNCELEMESİ
def inceleme():
    kp = "icKapak"
    kr = "".join(f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="icKarar" value="{e(k)}"{" checked" if k == "Yanıltıcı" else ""}{' data-yeni-isaret="0"' if k == "Yanıltıcı" else ""}><span><b>{e(k)}</b><small>{e(v[1])}</small></span></label>' for k, v in KARAR.items())
    detay = (fs("İnceleme", "fa-scale-balanced", grid(
                girdi("icBaslik", "Başlık", "Asgari ücrete ocakta yüzde 60 zam yapılacağı iddiası yanıltıcı", "baslik", "70|90", "Sitede başlık; karar etiketi başlığın üstünde ayrıca görünür", cls="finput kb-buyuk", ek=' data-alan="baslik"', hata="Başlık zorunlu."),
                alan("icSpot", "Spot", "Sosyal medyada paylaşılan görseldeki oran, geçen yılın talep metninden alınmış. Bu yılın komisyon süreci henüz başlamadı ve resmî bir oran açıklanmadı.", "spot", "220|280", "Başlığın altındaki giriş cümlesi", ek=' data-alan="spot"', hata="Spot zorunlu."),
                frow("Karar", f'<div class="kb-kart-sec" data-alan-id="karar" data-zorunlu-metin="Karar etiketini seçin">{kr}</div>', ipucu="Sitede inceleme kartında ve başlığın üstünde renkli etiket. Karar değişirse sürüm geçmişine “karar değişikliği” notu eklenir.")))
             + ai_adim("#icBaslik,#icSpot", [("ozet", "Karar özeti (3 madde)", True, None), ("seo", "SEO", True, None), ("bildirim", "Bildirim Metni", True, "etkilesim"), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")])
             + fs("Karar özeti", "fa-list-check", '<div class="kb-madde">' + "".join(f'<div class="km-satir"><span class="km-no">{n}</span><input value="{e(v)}" aria-label="Karar özeti maddesi {n}"></div>' for n, v in enumerate([
                 "Paylaşılan yüzde 60 oranı, işçi konfederasyonlarından birinin geçen yılki talebine ait.", "Bu yılın komisyon süreci henüz başlamadı; ilk toplantı 4 Aralık’ta yapılacak.", "Resmî bir oran açıklanmadı; karar yıl sonunda komisyonda verilecek."], 1)) + '</div>', ek_bas="Sitede “Dada Doğrula kararı” kutusunda · isteğe bağlı", attr=' data-ai-grup="ozet"')
             + fs("İddia", "fa-quote-left", grid(
                 f'<div class="frow"><span class="flabel">İddianın metni</span>' + editor("İddia", "<p>Sosyal medyada 20 Kasım’dan bu yana paylaşılan bir görselde, “Asgari ücrete ocakta yüzde 60 zam yapılacak, rakam kesinleşti” ifadesi yer alıyor. Görsel, bir haber sitesinin tasarımını taklit eden bir şablonla hazırlanmış ve 48 saatte 30 binden fazla kez paylaşılmış.</p>", "iddia", kisa=True, zm="İddianın metnini yazın") + '<span class="fhint">Sitede “İddia” bölümü</span>' + ferr("İddianın metnini yazın.") + '</div>',
                 f'<div class="frow two">' + frow("Nerede görüldü", secim("icPlatform", [("x", "X (Twitter)"), ("whatsapp", "WhatsApp grupları"), ("facebook", "Facebook"), ("instagram", "Instagram"), ("tiktok", "TikTok"), ("haber", "Haber Sitesi")], "x", "Platform seçin", yeni_deger="")) + frow("İlk görülme", tarih("icIlk", "2026-11-20 09.40")) + '</div>',
                 girdi("icYayilma", "Yayılma", "48 saatte 30 binden fazla paylaşım", ipucu="İsteğe bağlı · sitede iddianın altında"),
                 frow("İddianın bağlantısı", cip_girdi(["x.com/…/status/18620…"], [], "Bağlantıyı yapıştırın; Enter", serbest=True), ipucu="Bağlantılar sitede gösterilmez; yalnız ekip içi kayıt.")))
             + fs("Bulgular", "fa-magnifying-glass", editor("Bulgular", "<p>Görseldeki yüzde 60 oranının kaynağını aradık. Bu oran, bir işçi konfederasyonunun geçen yıl aralık ayında açıkladığı talep metninde geçiyor. Aynı konfederasyonun bu yıl için henüz bir talep açıklamadığını, kurumun basın biriminden yazılı olarak teyit ettik.</p><p>Çalışma ve Sosyal Güvenlik Bakanlığının 22 Kasım tarihli duyurusuna göre Asgari Ücret Tespit Komisyonu ilk toplantısını 4 Aralık’ta yapacak. Duyuruda herhangi bir artış oranından söz edilmiyor.</p><p>Bu nedenle iddiayı, gerçek bir talep oranının bağlamından koparılıp kesinleşmiş karar gibi sunulması gerekçesiyle <b>yanıltıcı</b> olarak değerlendirdik.</p>", "bulgular", medya=True, zm="Bulguları yazın", alt="İncelemenin asıl metni; “Dinle” bu metinden okunur"))
             + fs("Neden bu karar?", "fa-circle-question", grid(
                 girdi("icNedenB", "Soru", "Neden “yanlış” değil de “yanıltıcı”?", sayac="60|80", ipucu="Sitede açılır kutu başlığı · isteğe bağlı"),
                 alan("icNedenM", "Yanıt", "Yüzde 60 oranı uydurma değil; gerçek bir talep metninde geçiyor. Yanıltıcı olan, bu oranın kesinleşmiş bir karar gibi sunulması.", sayac="240|320", ipucu="Açılır kutunun içi", rows=2)), ek_bas="İsteğe bağlı")
             + fs("Kanıtlar", "fa-paperclip", satir_liste("Kanıt", "Kanıt (belge, kayıt, görsel)", "Ne gösteriyor", [
                 ("Konfederasyonun 2025 talep metni", "Yüzde 60 oranı geçen yılın aralık ayında açıklanan talepte geçiyor"),
                 ("Bakanlık duyurusu · 22 Kasım 2026", "İlk toplantı 4 Aralık’ta; duyuruda oran yok"),
                 ("Taklit şablonun arşiv karşılaştırması", "Taklit edilen sitenin arşivinde bu başlıkla haber yok")], "Kanıt ekle"), ek_bas="Sitede bulguların altında")
             + fs("Kaynaklar", "fa-link", satir_liste("Kaynak", "Kaynak adı (kurum, belge)", "Açıklama, tarih ya da bağlantı", [
                 ("Çalışma ve Sosyal Güvenlik Bakanlığı", "Asgari Ücret Tespit Komisyonu toplantı duyurusu · 22 Kasım 2026"), ("İşçi konfederasyonu basın birimi", "Yazılı yanıt · 22 Kasım 2026"), ("Resmî Gazete", "Asgari Ücret Yönetmeliği, komisyonun çalışma usulü")], "Kaynak ekle"), ek_bas="Sitede “İncelendi · 3 kaynak”")
             + kapak(kp, "p122", (50, 50), "Temsilî fotoğraf · Dada Haber arşivi", "Sosyal medyada paylaşılan görselin ekran görüntüsü yerine temsilî fotoğraf · Dada Haber arşivi", "İddianın görseli yerine temsilî fotoğraf önerilir (yanlış bilgiyi yaymamak için) · önerilen en az 1280×533")
             + fs("Ekip", "fa-user-check", grid(f'<div class="frow two">' + yazar_alani("icYazar", "Kerem Aksoy") + frow("İkinci okuyan editör", secim("icIkinci", yazar_secenek(), "Ayşe Yıldız", "Editör seçin", "Editör ara", yeni_deger="", bos_metin="Bu adla editör yok."), ipucu="Kayıt içindir; yayın onaya bağlı değildir (çok adımlı onay yok).") + '</div>',
                                                  anahtar("Okurdan geldi", "İddia “İddia gönder” formundan geldiyse gönderene sonuç e-postası gider", True, kap_ek=' data-modul="etkilesim"'))))
    form = (f'<section class="pnl-card" id="icForm" data-form data-sekmeli data-zorunlu-kayit="haberler.inceleme" aria-label="İnceleme formu">'
            + dil("Dil seçici bütün sekmelerdeki metin alanlarını birlikte değiştirir; karar etiketi, görsel ve kaynaklar bütün dillerde ortaktır.")
            + sekmeler([("pDetay", "Detay", "fa-file-lines", None), ("pSeo", "SEO", "fa-magnifying-glass-chart", None), ("pBildirim", "Bildirim", "fa-bell", "etkilesim"), ("pSosyal", "Sosyal Medya", "fa-share-nodes", "sosyal-medya")])
            + panel("pDetay", detay, ilk=True)
            + seo_panel("Yüzde 60 asgari ücret zammı iddiası yanıltıcı | Dada Doğrula", "Asgari ücrete ocakta yüzde 60 zam yapılacağı iddiası yanıltıcı: oran geçen yılın talep metninden; komisyon henüz toplanmadı.", "dadahaber.com/dada-dogrula/", "asgari-ucrete-yuzde-60-zam-iddiasi", ["asgari ücret yüzde 60", "asgari ücret zam iddiası", "dada doğrula"])
            + bildirim_panel("", "Dada Doğrula: yüzde 60 zam iddiası yanıltıcı", "Oran geçen yılın talep metninden; komisyon ilk kez 4 Aralık’ta toplanacak.")
            + sosyal_panel("", kp, "p122", (50, 50), {
                "x": "🔎 Dada Doğrula | YANILTICI\n\n“Asgari ücrete ocakta %60 zam kesinleşti” görseli geçen yılın talep metninden. Komisyon henüz toplanmadı.\n\nhttps://dadahaber.com/dada-dogrula/asgari-ucrete-yuzde-60-zam-iddiasi",
                "facebook": "Aile gruplarında dolaşan “%60 zam kesinleşti” görseli yanıltıcı. Oranın kaynağını ve resmî takvimi inceledik.\n\nhttps://dadahaber.com/dada-dogrula/asgari-ucrete-yuzde-60-zam-iddiasi",
                "linkedin": "Asgari ücret tartışmasında yanlış bilgi: %60 oranı geçen yılın talebi. Komisyonun ilk toplantısı 4 Aralık’ta.\n\nhttps://dadahaber.com/dada-dogrula/asgari-ucrete-yuzde-60-zam-iddiasi",
                "instagram": "YANILTICI ⚠️ “%60 zam kesinleşti” görseli geçen yılın talep metninden. Ayrıntı profildeki bağlantıda.\n\n#dadadoğrula #asgariücret",
                "telegram": "🔎 Dada Doğrula · Yanıltıcı\n\n%60 zam iddiası geçen yılın talep metninden; resmî oran açıklanmadı.\n\nhttps://dadahaber.com/dada-dogrula/asgari-ucrete-yuzde-60-zam-iddiasi"}, "dada-dogrula")
            + '</section>')
    yk = yayin_karti("icY", [("yayinda", "Yayında"), ("taslak", "Taslak", "yayından kalkar"), ("zamanli", "Zamanlanmış")], "yayinda", "2026-11-23 11.10",
        anahtar("Manşette", "Vitrinden sıralanır", False) + anahtar("Dada Doğrula'da öne çıkan", "İnceleme listesinin başında büyük kartla", True, yeni=False),
        ("Sürüm 3", "son değişiklik 23.11.2026 11.40 · Kerem Aksoy", "?id=asgari-ucrete-yuzde-60-zam-iddiasi"))
    govde = bas("İnceleme düzenle", "Dada Doğrula · <b>Yanıltıcı</b> · Kerem Aksoy · 23.11.2026 11.10'da yayımlandı · 11.40'ta güncellendi · 21,3 B okunma",
                [a_hedef("İncelemelere dön", "fa-arrow-left", "haberler.dosyalar", "?sekme=pDogrula"), a_dis("Sitede Görüntüle", "fa-arrow-up-right-from-square", SITE + "dada-dogrula-inceleme.html", " data-yeni-gizle")],
                h1_yeni="Yeni doğrulama incelemesi", alt_yeni="Dada Doğrula · taslak · henüz kaydedilmedi · yazar: oturumdaki kullanıcı")
    govde += f'  <div class="form-layout">\n  {form}\n  {yan(yan_onizleme("", "Dada Doğrula: yüzde 60 zam iddiası yanıltıcı", "Oran geçen yılın talep metninden; komisyon ilk kez 4 Aralık’ta toplanacak.", "p122", 50, 50, "Asgari ücrete ocakta yüzde 60 zam yapılacağı iddiası yanıltıcı"), yk, seo_skor(90, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "ClaimReview şeması: karar etiketi var"), (True, "3 kaynak bağlantısı")]))}\n  </div>\n'
    govde += kaydet("icForm", "Kaydedildi · 23.11.2026 11.40 · Kerem Aksoy", "Güncelle", "İnceleme güncellendi; sitede yayında, önceki hal sürüm geçmişinde", "Yayımla", "İnceleme yayımlandı; Dada Doğrula'da görünür")
    YAZILDI.append(sayfa("inceleme.html", "İnceleme düzenle", "haberler.inceleme", govde, editor=True, body_ek=' data-yeni-baslik="Yeni doğrulama incelemesi"'))

# ======================================================================= 9 · YAZARLAR
SAYI = {}
for h in soz["haberler"]:
    if h.get("yazar"): SAYI[h["yazar"]] = SAYI.get(h["yazar"], 0) + 1
SON = {}
for h in sorted(soz["haberler"], key=lambda h: (h["tarih"], h["saat"])):
    if h.get("yazar"): SON[h["yazar"]] = h
def yazarlar():
    satir = []
    adlar = [y["ad"] for y in YAZARLAR]
    for y in YAZARLAR:
        ad, unvan, alan_ = y["ad"], y["unvan"], y["alan"]
        sl = tr_slug(ad); n = SAYI.get(ad, 0); son = SON.get(ad)
        d = "pasif" if ad == "Pınar Okyay" else "aktif"
        kose = alan_ == "Köşe"
        st = f'{son["tarih"][8:]}.{son["tarih"][5:7]}.{son["tarih"][:4]} {son["saat"]}' if son else "—"
        hed = "|".join(x for x in adlar if x != ad)
        sil = (f'<button type="button" class="ia-btn danger" data-tasi-sil data-sonra-kaldir data-tasi-ad="{e(ad)}" data-tasi-sayi="{n}" data-tasi-birim="haber" data-tasi-birim-cogul="haberler" data-tasi-ikon="fa-newspaper" '
               f'data-tasi-soru="Haberler hangi yazara taşınsın?" data-tasi-hedefler="{e(hed)}" data-tasi-not="Haberlerin imzası seçilen yazara geçer; yazar sayfası kapanır, eski adres yeni yazara yönlendirilir. “{e(ad)}” çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır." '
               f'data-bildir-sonra="“{e(ad)}” çöpe taşındı; {n} haber seçilen yazara taşındı" aria-label="Çöpe Taşı" title="Çöpe Taşı">{I("fa-trash")}</button>')
        satir.append(tr(sl, d, f"{ad} {unvan} {alan_}", ad,
            [ana_hucre(ad, (f'{e(unvan)} · Köşesi: {e(", ".join(kose_konulari(ad, 2)))} · <a class="kb-bag" data-hedef="haberler.kose" data-hedef-ek="{kose_suz(ad)}" href="#">{KOSE_SAYI.get(ad, 0)} köşe yazısı</a>' if kose else e(unvan)), ava=f'<span class="kb-ava{" is-pasif" if d == "pasif" else ""}">{bas_harf(ad)}</span>', alt_ham=True), (f'<span class="kb-kat"><b>{e(alan_)}</b></span>', "kb-gizle-m"),
             (f"{n:,}".replace(",", "."), "say"), (f'<span class="kb-tarih">{st}</span>', "kb-gizle-t"), (rozet("ok", "Etkin") if d == "aktif" else rozet("off", "Pasif"), "")],
            ia_a(SITE + "yazar.html", "Sitede Görüntüle", "fa-eye", True) + ia_a(f"yazar.html?id={sl}", "Düzenle", "fa-pen") + sil + DIGER, href=f"yazar.html?id={sl}", bolum=alan_, tur="kose" if kose else "kadro"))
    satir.append(tr("onur-sevim", "cop", "Onur Sevim Keşfet Muhabiri Keşfet", "Onur Sevim", [ana_hucre("Onur Sevim", "Keşfet Muhabiri · 41 haberi Nilay Ersoy'a taşındı", ava='<span class="kb-ava is-pasif">OS</span>'), ('<span class="kb-kat"><b>Keşfet</b></span>', "kb-gizle-m"), ("0", "say"), ('<span class="kb-tarih muted">02.11.2026 17.20</span>', "kb-gizle-t"), (rozet("warm", "Çöpte"), "")],
        ia_a("yazar.html?id=onur-sevim", "Görüntüle", "fa-eye") + ia_a("yazar.html?id=onur-sevim", "Düzenle", "fa-pen") + SIL + DIGER, href="yazar.html?id=onur-sevim", bolum="Keşfet", tur="kadro", onceki="pasif"))
    menu = (m_grup("Yazar", "aktif pasif")
            + m_btn("Pasife al", "fa-user-slash", "aktif", onay("Yazar pasife alınsın mı?", "Yazar sayfası ve eski yazıları yayında kalır; haber formunda yazar olarak seçilemez. Gerekirse ⋯ → Etkinleştir.", "Pasife al", ikon="fa-user-slash", sonra=("pasif", "Pasif", "off"), bildir="Yazar pasife alındı"))
            + m_btn("Etkinleştir", "fa-user-check", "pasif", onay("Yazar etkinleştirilsin mi?", "Haber formunda yeniden yazar olarak seçilebilir.", "Etkinleştir", ikon="fa-user-check", sonra=("aktif", "Etkin", "ok"), bildir="Yazar etkinleştirildi"))
            + m_a("Yazılarını gör", "fa-newspaper", "haberler.liste", "", ' data-durum-icin="aktif pasif"')
            + m_a("Köşe yazıları", "fa-feather-pointed", "haberler.kose", "", ' data-durum-icin="aktif pasif" data-kosul-icin="tur:kose"')
            + m_btn("Bağlantıyı kopyala", "fa-link", "aktif pasif", " data-kopyala")
            + m_ayir("aktif pasif") + m_grup("Kayıt") + DENETIM + COP_MENU)
    bolum_ops = [("", "Bütün bölümler")] + [(b, b) for b in BOLUMLER]
    govde = bas("Yazarlar", "36 yazar · 8 bölüm ve köşe · 4 köşe yazarı · imza bilgisi sitedeki yazar sayfası ve haber kartlarında",
                [a_dis("Yazarlar sayfası", "fa-arrow-up-right-from-square", SITE + "yazarlar.html"), a_hedef("Yeni yazar", "fa-plus", "haberler.yazar", "?yeni=1", "btn-acc")])
    govde += liste("yazar", "Yazar listesi", [("hepsi", "Tümü", 0), ("aktif", "Etkin", 0), ("pasif", "Pasif", 0)], "Ad, Unvan ya da Bölüm Ara",
        [("bolum", "Bölüm", "yzSuzBolum", bolum_ops, "Bölüm ara"), ("tur", "Tür", "yzSuzTur", [("", "Bütün Türler"), ("kadro", "Kadro (editör, muhabir)"), ("kose", "Köşe yazarı")], None)],
        [btn("Pasife al", "fa-user-slash", attr=' data-toplu="pasif" data-bildir="Seçilen yazarlar pasife alındı; yazıları yayında kalıyor"')],
        [('<input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün yazarları seç">', "kb-sec-hucre"), ("Yazar", "kb-ana"), ("Bölüm", "kb-gizle-m"), ("Yazı", "say"), ("Son yazı", "kb-gizle-t"), ("Durum", ""), ('<span class="sr-only">İşlemler</span>', "")],
        satir, menu, bos_durum("yazarlar.html", "Yazarlar yüklenemedi", "fa-pen-nib", "Henüz yazar yok", "Haberlerde imza olarak görünecek ilk yazarı ekleyin.", f'<a class="pe-tag" data-hedef="haberler.yazar" data-hedef-ek="?yeni=1" href="#">{I("fa-plus")}Yeni yazar</a>'),
        "36 sonuçtan 1–36 gösteriliyor", sayfa_boy=40, liste_cop_not="Yazar sayfası kapanır ve Çöp sekmesine taşınır",
        bant=f'<div class="kb-bant bilgi">{I("fa-circle-info")}<span>Yazısı olan yazar doğrudan silinmez: silmede haberlerinin taşınacağı yazar seçilir, sonra çöpe gider (B1). Yazısı kalsın ama imza olarak seçilmesin diyorsanız ⋯ → Pasife al.</span></div>')
    YAZILDI.append(sayfa("yazarlar.html", "Yazarlar", "haberler.yazarlar", govde))

# ======================================================================= 10 · YAZAR DÜZENLE
def yazar():
    ad, unvan, bolum = "Aylin Sezer", "Köşe Yazarı", "Köşe"
    n = SAYI.get(ad, 0)
    foto = (f'<div class="form-sec" data-alan-id="foto" data-gorsel-alan="haberler.yazar" data-gorsel-ad="Yazar fotoğrafı" data-kirp-sonra data-etiketsiz>'
            f'<div class="form-sec-tt">{I("fa-circle-user")}Fotoğraf<span class="fs-ek">İsteğe bağlı · yoksa baş harfler görünür</span></div>'
            f'<div class="kb-yukle" data-gorsel-bos><span class="kb-ava k-lg" data-yeni-gizle>{bas_harf(ad)}</span><b>Fotoğrafı sürükleyin ya da seçin</b><span>1:1 · web kartı 88×88, profil 96×96, mobil 72×72 (sitede daire) · kişisel fotoğraf, medya havuzuna girmez</span><span class="kg-acts">'
            f'<button type="button" class="btn btn-acc btn-sm" data-gorsel-yukle>{I("fa-upload")}Bilgisayardan yükle</button></span></div>'
            f'<div class="kb-gorsel" data-gorsel-dolu hidden><div class="kg-bolum"><div class="kg-bas">{I("fa-desktop")}Web</div><div class="kg-ikili">'
            f'<div class="kg-resim r-1x1" data-gorsel-hedef="web" data-kirp-oran="web.detay"><span class="kg-etk">Profil · 1:1</span></div><div class="kg-resim r-1x1" data-gorsel-hedef="web" data-kirp-oran="web.kart"><span class="kg-etk">Kart · 1:1</span></div></div>'
            f'<div class="kg-olcu">Önerilen: profil <b>96×96</b>, yazar kartı <b>88×88</b> (sitenin görünen genişliği).</div>'
            f'<div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{I("fa-crop-simple")}Kırp ve Odak</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{I("fa-upload")}Yükle</button><button type="button" class="btn btn-ghost btn-sm danger" data-gorsel-kaldir>{I("fa-trash")}Kaldır</button></div></div>'
            f'<div class="kg-bolum"><div class="kg-bas">{I("fa-mobile-screen")}Mobil<span class="kg-oto">{I("fa-wand-magic-sparkles")} Webden kırpıldı</span></div><div class="kg-resim r-1x1" data-gorsel-hedef="mobil" data-kirp-oran="mobil.kart"><span class="kg-etk">Mobil · 1:1</span></div>'
            f'<div class="kg-olcu">Önerilen: <b>72×72</b> (sitenin telefon görünümü).</div><div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac="mobil.kart">{I("fa-crop-simple")}Kırp</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle data-gorsel-kapsam="mobil">{I("fa-upload")}Ayrı Görsel Yükle</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-webe-don hidden>{I("fa-rotate-left")}Webden kırpılana dön</button></div></div></div></div>')
    # sosyal bağlantılar: çekirdek "sosyal bağlantı listesi" (Beyar K2); okur e-postası ayrı alan
    sosyal = ('<div class="kb-sbag" data-sosyal-baglanti data-ad="yzSosyal" data-degerler=\'[{"p":"x","k":"aylinsezer_dh"},{"p":"linkedin","k":"in/aylin-sezer"}]\'></div>'
              + grid(f'<div class="frow"><label for="yzEp">Okur e-postası</label><div class="kb-eposta"><input class="finput" id="yzEp" type="email" data-eposta value="aylin.sezer@dadahaber.ornek">{I("fa-circle-check")}</div><span class="fhint">Yazar sayfasında “Yazara yaz” bağlantısı · isteğe bağlı</span>{ferr("Geçerli bir e-posta yazın.")}</div>'))
    tur = ''.join(f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="yzTur" value="{v}"{" checked" if v == "kose" else ""}{' data-ac="yzKosesi"' if v == "kose" else ""} data-yeni-isaret="{1 if v == "kadro" else 0}"><span><b>{b}</b><small>{s}</small></span></label>' for v, b, s in [
        ("kadro", "Kadro", "Editör ya da muhabir; haber imzası"), ("kose", "Köşe yazarı", "Köşe yazıları, Yazarlar sayfasında öne çıkar"), ("konuk", "Konuk yazar", "Farklı Bakışlar ve uzman görüşü")])
    detay = (fs("Kimlik", "fa-id-card", grid(
                f'<div class="frow two">' + girdi("yzAd", "Ad Soyad", ad, "ad", "40|60", "İmza olarak haberlerde ve yazar sayfasında", ek=' data-alan="baslik" data-slug-hedef="sSlug"', hata="Ad soyad zorunlu.")
                + girdi("yzUnvan", "Unvan", unvan, "unvan", "40|60", "Adın altında; yazar kartında", hata="Unvan zorunlu.") + '</div>',
                f'<div class="frow two">' + frow("Bölüm", secim("yzBolum", [(b, b) for b in BOLUMLER], bolum, "Bölüm seçin", "Bölüm ara", alan_id="bolum", yeni_deger="", bos_metin="Bu adla bölüm yok."), ipucu="Yazarlar sayfasında bu bölümün altında listelenir.")
                + frow("Panel hesabı", secim("yzHesap", [("", "Bağlı hesap yok"), ("aylin.sezer", "Aylin Sezer", "Editör · aylin.sezer@dadahaber.ornek"), ("ayse.yildiz", "Ayşe Yıldız", "Genel Yayın Yönetmeni"), ("mehmet.kocak", "Mehmet Koçak", "Editör")], "aylin.sezer", "Bağlı hesap yok", "Kullanıcı ara", yeni_deger="", bos_metin="Bu adla kullanıcı yok."), ipucu="Bağlıysa bu kullanıcının yazdıkları kendiliğinden bu imzayla çıkar.") + '</div>',
                frow("Tür", f'<div class="kb-kart-sec">{tur}</div>')))
             + foto
             + fs("Biyografi", "fa-align-left", editor("Biyografi", "<p>Aylin Sezer, 2014'ten bu yana kişisel finans ve çalışma hayatı üzerine yazıyor. Kredi, kira, emeklilik ve vergi gibi gündelik ekonomi konularını okurun cebine etkisi üzerinden anlatıyor.</p>", None, kisa=True, alt="Yazar sayfasının başında · 400 karakter önerilir"), ek_bas="İsteğe bağlı")
             + fs("Sosyal bağlantılar", "fa-share-nodes", sosyal, ek_bas="Yazar sayfasında ikonlarla")
             + fs("Yayın", "fa-sliders", grid(anahtar("Yazar sayfası yayında", "dadahaber.com/yazar/aylin-sezer · kapalıysa imza bağlantısız görünür"), anahtar("Okurlar takip edebilir", "Hesabım > Takip Ettiklerim'de yazar olarak eklenir"), anahtar("Yazarlar sayfasında öne çıkar", "Köşe yazarları bandında son yazısıyla", True))))
    form = (f'<section class="pnl-card" id="yzForm" data-form data-sekmeli data-zorunlu-kayit="haberler.yazar" aria-label="Yazar formu">'
            + dil("Dil seçici unvanı, biyografiyi ve SEO metinlerini birlikte değiştirir; ad, fotoğraf ve bağlantılar bütün dillerde ortaktır.")
            + sekmeler([("pDetay", "Detay", "fa-id-card", None), ("pSeo", "SEO", "fa-magnifying-glass-chart", None)])
            + panel("pDetay", detay, ilk=True)
            + seo_panel("Aylin Sezer · Köşe Yazarı | Dada Haber", "Aylin Sezer'in kişisel finans, kira, kredi ve emeklilik üzerine köşe yazıları Dada Haber'de.", "dadahaber.com/yazar/", "aylin-sezer", ["aylin sezer", "aylin sezer köşe yazısı"])
            + '</section>')
    onz = kart("Yazar kartı", "fa-eye", f'<div class="kb-onizle-kap"><p class="fhint" data-yeni-goster hidden>Ad Soyad girilince görünür.</p><div class="rcp-cell" data-yeni-gizle><span class="kb-ava k-lg">{bas_harf(ad)}</span><div class="rcp-id"><div class="rcp-name" data-alan="baslik">{e(ad)}</div><div class="rcp-by">{e(unvan)} · {n} yazı</div></div></div><p class="kb-onizle-not" data-yeni-gizle>Sitede Yazarlar sayfası ve haber imzasında böyle görünür.</p></div>')
    kk = KOSE_SAYI.get(ad, 0); son_k = next((x for x in KOSE_YAYINDA if x["yazar"] == ad), None)
    kosesi = (f'<section class="pnl-card" id="yzKosesi"><div class="pc-head"><h2 class="pc-title">{I("fa-feather-pointed")}Köşesi</h2></div>'
              f'<div class="pc-body sa-durum"><div data-yeni-gizle><span>Köşe Yazısı</span><b>{kk}</b></div><div data-yeni-gizle><span>Son yazı</span><b>{tarih_tr(son_k["tarih"], son_k["saat"]) if son_k else "—"}</b></div><div data-yeni-gizle><span>Konuları</span><b>{e(", ".join(kose_konulari(ad)))}</b></div>'
              f'<p class="fhint" data-yeni-goster hidden>Kaydedince köşe yazarları listesinde görünür; köşe yazısı formunda yazar olarak seçilir.</p>'
              f'<div><a class="kb-bag" data-hedef="haberler.kose" data-hedef-ek="{kose_suz(ad)}" href="#" data-yeni-gizle>Köşe yazıları</a><a class="kb-bag" data-hedef="haberler.kose-duzenle" data-hedef-ek="?yeni=1" href="#">Yeni köşe yazısı</a></div></div></section>')
    ist = kart("Özet", "fa-chart-simple", govde_cls=None, ic=durum_dl([("Yazı", f"{n}"), ("Son yazı", "23.11.2026 15.30"), ("Takipçi", "48,2 B"), ("Yazmaya başladı", "2014"), ("Son değişiklik", "18.11.2026 · Selin Aydemir")]))
    ist = ist.replace('<section class="pnl-card">', '<section class="pnl-card" data-yeni-gizle>', 1)
    govde = bas("Yazar düzenle", f"Köşe · {unvan} · {n} yazı · 48,2 B takipçi", [a_hedef("Yazarlara dön", "fa-arrow-left", "haberler.yazarlar"), a_dis("Sitede Görüntüle", "fa-arrow-up-right-from-square", SITE + "yazar.html", " data-yeni-gizle")],
                h1_yeni="Yeni yazar", alt_yeni="Henüz kaydedilmedi · ad ve unvan girilince yazar sayfası açılır")
    govde += f'  <div class="form-layout">\n  {form}\n  {yan(onz, kosesi, ist, seo_skor(78, [(True, "Başlık 50–60 karakter"), (False, "Açıklama 120 karakterin altında"), (False, "Fotoğraf yok (yazar şeması için önerilir)"), (True, "Biyografi var")]))}\n  </div>\n'
    govde += kaydet("yzForm", "Kaydedildi · 18.11.2026 10.40 · Selin Aydemir", "Kaydet", "Yazar kaydedildi; sitedeki yazar sayfası ve imzalar güncellendi", "Kaydet", "Yazar eklendi; haber formunda seçilebilir", taslak=False)
    YAZILDI.append(sayfa("yazar.html", "Yazar düzenle", "haberler.yazar", govde, editor=True, body_ek=' data-yeni-baslik="Yeni yazar"'))

# ======================================================================= 11 · SÜRÜM GEÇMİŞİ (B9)
SURUMLER = [
    ("4", "Yayında", "ok", "Ayşe Yıldız", "23.11.2026 15.20", "Spot ve “Takvim” bölümü güncellendi; kaynak eklendi", "güncelleme"),
    ("3", "Önceki", "off", "Hakan Uysal", "23.11.2026 14.40", "Toplantı günü düzeltildi (5 → 4 Aralık) · düzeltme notu", "düzeltme"),
    ("2", "Önceki", "off", "Hakan Uysal", "23.11.2026 14.12", "Başlık kısaltıldı, Dada Özet eklendi", "güncelleme"),
    ("1", "İlk yayın", "off", "Hakan Uysal", "23.11.2026 14.05", "Haber yayımlandı", "ilk yayın")]
NOTLAR = [
    ("n1", "guncelleme", "Güncelleme", "23.11.2026 15.20", "Ayşe Yıldız", "Komisyonun geçen yılki karar takvimi ve 7 milyon çalışan bilgisi eklendi."),
    ("n2", "duzeltme", "Düzeltme notu", "23.11.2026 14.40", "Hakan Uysal", "Haberin ilk halinde toplantı tarihi 5 Aralık olarak yazılmıştı; doğrusu 4 Aralık'tır."),
    ("n3", "guncelleme", "Güncelleme", "23.11.2026 14.12", "Hakan Uysal", "İşçi ve işveren tarafının talepleri ayrı başlık altında toplandı.")]
def not_form(onek, tur, n=None):
    metin = n[5] if n else ""
    zaman = n[3] if n else ""
    z = f"{zaman[6:10]}-{zaman[3:5]}-{zaman[:2]} {zaman[11:]}" if zaman else ""
    ac = ("Okura haberin altında “Güncellendi” satırıyla görünür; Güncellenen Haberler sayfasında listelenir. Düzenlenebilir ve silinebilir."
          if tur == "guncelleme" else "Okura haberin altında “Düzeltme” kutusuyla görünür ve Düzeltme Politikası sayfasına yazılır. <b>Yayımlandıktan sonra değiştirilemez ve silinemez</b> (B9).")
    return (dil("Dil seçici not metnini birlikte değiştirir; zaman ve tür bütün dillerde ortaktır.", kap=True)
            + f'<div class="kb-bant {"bilgi" if tur == "guncelleme" else "uyari"}">{I("fa-circle-info" if tur == "guncelleme" else "fa-triangle-exclamation")}<span>{ac}</span></div>'
            + kfs("Güncelleme" if tur == "guncelleme" else "Düzeltme notu",
                  frow("Zaman", tarih(f"{onek}T", z, ek=' data-alan-id="zaman" data-bos="Kaydedilince o anın saati" data-temizlenir="1"'), ipucu="Boş bırakılırsa kaydedildiği an yazılır.")
                  + f'<div class="frow"><span class="flabel">{"Ne değişti?" if tur == "guncelleme" else "Neyi düzelttik?"}</span>' + editor("Not metni", f"<p>{e(metin)}</p>" if metin else "<p></p>", "metin", kisa=True, zm="Not metnini yazın") + ferr("Not metni zorunlu.") + '</div>'
                  + (anahtar("Güncellenen Haberler sayfasında listele", "Okur “ne değişti” akışında görür", True) if tur == "guncelleme" else anahtar("Düzeltme Politikası sayfasına yaz", "Kurumsal düzeltme kaydı; kapatılamaz", True, ek=" disabled"))))
def surumler():
    sab, s_satir, n_satir = [], [], []
    ICERIK = {"4": "<p>Asgari Ücret Tespit Komisyonu, 2027 yılı için ilk toplantısını 4 Aralık'ta yapacak. İşçi ve işveren tarafı taleplerini bu toplantıda masaya koyacak; komisyonun yıl sonuna kadar karar vermesi bekleniyor.</p><h2>Takvim</h2><p>Geçen yıl komisyon dört toplantının ardından kararını aralık ayının son haftasında açıklamıştı. Belirlenecek asgari ücret yaklaşık 7 milyon çalışanı doğrudan ilgilendiriyor.</p>",
              "3": "<p>Asgari Ücret Tespit Komisyonu, 2027 yılı için ilk toplantısını 4 Aralık'ta yapacak. İşçi ve işveren tarafı taleplerini bu toplantıda masaya koyacak.</p><h2>Takvim</h2><p>Geçen yıl komisyon dört toplantının ardından kararını aralık ayının son haftasında açıklamıştı.</p>",
              "2": "<p>Asgari Ücret Tespit Komisyonu, 2027 yılı için ilk toplantısını 5 Aralık'ta yapacak. İşçi ve işveren tarafı taleplerini bu toplantıda masaya koyacak.</p>",
              "1": "<p>Asgari Ücret Tespit Komisyonu, 2027 yılında uygulanacak asgari ücreti belirlemek için ilk toplantısını 5 Aralık Cuma günü Ankara'da yapacak.</p>"}
    BASLIK = {"4": "Asgari ücret görüşmelerinde ilk toplantı 4 Aralık'ta yapılacak", "3": "Asgari ücret görüşmelerinde ilk toplantı 4 Aralık'ta yapılacak", "2": "Asgari ücret görüşmelerinde ilk toplantı 5 Aralık'ta yapılacak", "1": "Asgari Ücret Tespit Komisyonu 2027 için ilk kez 5 Aralık'ta toplanıyor"}
    for no, dur, cls, kim, zaman, ozet, islem in SURUMLER:
        tid = f"srS{no}"
        sab.append(sablon(tid, f"Sürüm {no}", f"{zaman} · {kim} · {ozet}",
            f'<div class="kb-bant bilgi">{I("fa-lock")}<span><b>Sürüm kaydı değiştirilemez ve silinemez.</b> Her kayıtta kendiliğinden oluşur; denetim izinin parçasıdır. Bu hale dönmek için “Bu sürüme dön” yeni bir sürüm oluşturur.</span></div>'
            + kfs("Sürüm bilgisi", f'<dl class="kb-ozet-dl"><dt>Sürüm</dt><dd>{no} · {e(dur)}</dd><dt>Kaydeden</dt><dd>{e(kim)}</dd><dt>Zaman</dt><dd>{zaman}</dd><dt>İşlem</dt><dd>{e(islem)}</dd><dt>Değişiklik</dt><dd title="{e(ozet)}">{e(ozet)}</dd></dl>')
            + kfs("Başlık", f'<p class="kb-ozet-baslik">{e(BASLIK[no])}</p>')
            + kfs("Metin (salt okunur)", f'<div class="kb-editor" aria-label="Sürüm {no} metni (salt okunur)"><div class="ke-icerik">{ICERIK[no]}</div></div>')
            + (alt_cubuk(f'<button type="button" class="btn btn-acc btn-sm"{onay("Sürüm " + no + "’e dönülsün mü?", "Haberin şimdiki hali (Sürüm 4) korunur; Sürüm " + no + " içeriğiyle yeni bir Sürüm 5 oluşur ve hemen yayına yansır. İşlem denetim izine yazılır.", "Bu sürüme dön", ikon="fa-clock-rotate-left", bildir="Sürüm " + no + " içeriğiyle Sürüm 5 oluşturuldu; sitede yayında")}>{I("fa-clock-rotate-left")}Bu sürüme dön</button>') if no != "4" else "")))
        s_satir.append(tr(f"s{no}", "yayinda" if no == "4" else "eski", f"Sürüm {no} {ozet} {kim}", f"Sürüm {no}",
            [(f'<b>Sürüm {no}</b>', ""), ana_hucre(ozet, f"{kim} · {islem}"), (rozet(cls, dur), ""), (f'<span class="kb-tarih">{zaman}</span>', "kb-gizle-m")],
            ia_tanim(tid, "Görüntüle", "fa-eye") + DIGER, secim_kutu=False))
    s_menu = (m_btn("Bu sürüme dön", "fa-clock-rotate-left", "eski", onay("Bu sürüme dönülsün mü?", "Şimdiki hal korunur; seçilen sürümün içeriğiyle yeni bir sürüm oluşur ve hemen yayına yansır. İşlem denetim izine yazılır.", "Bu sürüme dön", ikon="fa-clock-rotate-left", bildir="Seçilen sürümün içeriğiyle Sürüm 5 oluşturuldu"))
              + m_a("Karşılaştır", "fa-code-compare", "haberler.surumler", "?sekme=pFark") + DENETIM)
    for k, d, ad, zaman, kim, metin in NOTLAR:
        tid = f"srN{k}"
        if d == "guncelleme":
            sab.append(sablon(tid, "Güncelleme · düzenle", f"{zaman} · {kim}", not_form(tid, d, (k, d, ad, zaman, kim, metin)) + alt_cubuk(
                f'<button type="button" class="btn btn-ghost btn-sm danger kb-sol"{onay("Güncelleme notu çöpe taşınsın mı?", "Not haberin altından ve Güncellenen Haberler sayfasından kalkar; Çöp sekmesinden geri alınabilir.", "Çöpe Taşı", True, sonra=("cop", "Çöpte", "warm"), bildir="Güncelleme notu çöpe taşındı")}>{I("fa-trash")}Sil</button>',
                f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="srTamam" data-baslik-yaz="Güncelleme notu kaydedildi" data-bildir-sonra="Güncelleme notu kaydedildi; sitede haberin altında">{I("fa-check")}Kaydet</button>'), "haberler.surum-notu"))
            eyl = ia_tanim(tid, "Görüntüle", "fa-eye") + ia_tanim(tid, "Düzenle", "fa-pen") + SIL + DIGER
            rz = rozet("info", "Güncelleme")
        else:
            sab.append(sablon(tid, "Düzeltme notu", f"{zaman} · {kim} · yayımlandı",
                f'<div class="kb-bant bilgi">{I("fa-lock")}<span><b>Yayımlanan düzeltme kaydı değiştirilemez; yeni bir düzeltme notu ekleyin.</b> Düzeltme Politikası gereği okura açık bir kayıttır (B9).</span></div>'
                + kfs("Düzeltme notu", f'<dl class="kb-ozet-dl"><dt>Zaman</dt><dd>{zaman}</dd><dt>Yazan</dt><dd>{e(kim)}</dd><dt>Sürüm</dt><dd>3</dd></dl><div class="kb-editor kb-ust-bosluk" aria-label="Düzeltme notu (salt okunur)"><div class="ke-icerik"><p>{e(metin)}</p></div></div>')
                + alt_cubuk(f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="srYeniDuzeltme">{I("fa-plus")}Yeni düzeltme notu</button>')))
            neden = "Yayımlanan düzeltme kaydı değiştirilemez; yeni bir düzeltme notu ekleyin"
            eyl = ia_tanim(tid, "Görüntüle", "fa-eye") + kilit(neden) + kilit(neden) + DIGER
            rz = rozet("warm", "Düzeltme")
        n_satir.append(tr(k, d, f"{ad} {metin} {kim}", metin, [(f'<span class="kb-tarih">{zaman}</span>', ""), ana_hucre(metin, f"{kim} · {ad}"), (rz, "")], eyl, secim_kutu=False))
    n_menu = (m_btn("Bağlantıyı kopyala", "fa-link", "guncelleme duzeltme", " data-kopyala") + m_ayir("guncelleme duzeltme") + DENETIM + COP_MENU)
    sab.append(sablon("srYeniGuncelleme", "Güncelleme ekle", "Okura haberin altında “Güncellendi” satırıyla görünür", not_form("srYG", "guncelleme") + alt_cubuk(
        f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="srTamam" data-bildir-sonra="Güncelleme notu yayımlandı; haberin altında görünür">{I("fa-check")}Yayımla</button>'), "haberler.surum-notu"))
    sab.append(sablon("srYeniDuzeltme", "Düzeltme notu ekle", "Yayımlandıktan sonra değiştirilemez ve silinemez", not_form("srYD", "duzeltme") + alt_cubuk(
        f'<button type="button" class="btn btn-acc btn-sm"{onay("Düzeltme notu yayımlansın mı?", "Not haberin altında “Düzeltme” kutusuyla görünür ve Düzeltme Politikası sayfasına yazılır. Yayımlandıktan sonra değiştirilemez ve silinemez; yanlışlık olursa yeni bir düzeltme notu eklenir.", "Yayımla", ikon="fa-pen-to-square", bildir="Düzeltme notu yayımlandı; Düzeltme Politikası sayfasına yazıldı")}>{I("fa-check")}Yayımla</button>'), "haberler.surum-notu"))
    sab.append(sablon("srTamam", "Not kaydedildi", "Haberin altında görünür",
        f'<div class="kb-bant tamam">{I("fa-circle-check")}<span><b>Kaydedildi.</b> Not sitede haberin altında görünüyor; işlem denetim izine yazıldı.</span></div>'
        + alt_cubuk(f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="srYeniGuncelleme">{I("fa-plus")}Yeni güncelleme</button>')))
    s_liste = liste("sürüm", "Sürümler", [("hepsi", "Tümü", 0), ("yayinda", "Yayında", 0), ("eski", "Önceki", 0)], "Sürümlerde Ara", [], [],
        [("Sürüm", ""), ("Değişiklik", "kb-ana"), ("Durum", ""), ("Zaman", "kb-gizle-m"), ('<span class="sr-only">İşlemler</span>', "")], s_satir, s_menu,
        bos_durum("surumler.html", "Sürümler yüklenemedi", "fa-clock-rotate-left", "Henüz sürüm yok", "Haber ilk kez kaydedilince Sürüm 1 oluşur.", ""), "4 sonuçtan 1–4 gösteriliyor", cop=False, kap=False,
        bant=f'<div class="kb-bant bilgi">{I("fa-lock")}<span><b>Sürümler silinemez ve değiştirilemez.</b> Her kayıtta kendiliğinden oluşur ve denetim izinin parçasıdır; eski bir hale dönmek yeni bir sürüm oluşturur.</span></div>')
    n_liste = liste("not", "Güncelleme ve düzeltme notları", [("hepsi", "Tümü", 0), ("guncelleme", "Güncellemeler", 0), ("duzeltme", "Düzeltme notları", 0)], "Notlarda ara", [], [],
        [("Zaman", ""), ("Not", "kb-ana"), ("Tür", ""), ('<span class="sr-only">İşlemler</span>', "")], n_satir, n_menu,
        bos_durum("surumler.html?sekme=pNotlar", "Notlar yüklenemedi", "fa-pen-to-square", "Henüz not yok", "Haber güncellenince ya da düzeltilince okura açık bir not ekleyin.", f'<button type="button" class="pe-tag" data-tanim="srYeniGuncelleme">{I("fa-plus")}Güncelleme ekle</button>'),
        "3 sonuçtan 1–3 gösteriliyor", liste_cop_not="Haberin altından kalkar ve Çöp sekmesine taşınır", kap=False,
        bant=f'<div class="kb-bant bilgi">{I("fa-lock")}<span><b>Yayımlanan düzeltme kaydı değiştirilemez; yeni bir düzeltme notu ekleyin.</b> Güncelleme notları düzenlenir ve silinir (B9).</span></div>')
    def fark(ad, s1, s2, satirlar):
        return (f'<div id="{ad}"' + ("" if ad == "fk34" else " hidden") + f'><div class="kb-fark"><div class="kb-fark-satir kb-fark-bas"><span>Alan</span><span>Sürüm {s1}</span><span>Sürüm {s2}</span></div>'
                + "".join(f'<div class="kb-fark-satir"><b>{e(a)}</b><span class="kb-fark-once">{o}</span><span class="kb-fark-sonra">{s}</span></div>' for a, o, s in satirlar) + '</div></div>')
    fk = (f'<div class="form-sec"><div class="kb-onizle-sec" data-segment role="group" aria-label="Karşılaştırılan sürümler"><button type="button" class="is-on" data-hedef="fk34" aria-pressed="true">3 → 4</button><button type="button" data-hedef="fk23" aria-pressed="false">2 → 3</button><button type="button" data-hedef="fk12" aria-pressed="false">1 → 2</button></div><div class="kb-ust-bosluk">'
          + fark("fk34", 3, 4, [("Spot", "…masaya koyacak.", "…masaya koyacak<ins>; komisyonun yıl sonuna kadar karar vermesi bekleniyor</ins>."), ("Metin · Takvim", "…son haftasında açıklamıştı.", "…son haftasında açıklamıştı. <ins>Belirlenecek asgari ücret yaklaşık 7 milyon çalışanı doğrudan ilgilendiriyor.</ins>"), ("Kaynaklar", "2 kaynak", "<ins>Resmî Gazete · Asgari Ücret Yönetmeliği</ins> eklendi")])
          + fark("fk23", 2, 3, [("Başlık", "…ilk toplantı <del>5</del> Aralık'ta yapılacak", "…ilk toplantı <ins>4</ins> Aralık'ta yapılacak"), ("Spot", "…ilk toplantısını <del>5</del> Aralık'ta yapacak.", "…ilk toplantısını <ins>4</ins> Aralık'ta yapacak."), ("Düzeltme notu", "—", "<ins>Toplantı tarihi düzeltildi</ins>")])
          + fark("fk12", 1, 2, [("Başlık", "<del>Asgari Ücret Tespit Komisyonu 2027 için ilk kez 5 Aralık'ta toplanıyor</del>", "<ins>Asgari ücret görüşmelerinde ilk toplantı 5 Aralık'ta yapılacak</ins>"), ("Dada Özet", "—", "<ins>3 madde eklendi</ins>")])
          + '</div><p class="fhint">Silinen metin çizili, eklenen metin vurgulu. Karşılaştırma yalnız değişen alanları gösterir.</p></div>')
    kartlar = ('<section class="pnl-card" data-sekmeli aria-label="Sürüm Geçmişi">'
               + sekmeler([("pSurum", "Sürümler", "fa-clock-rotate-left", None), ("pFark", "Karşılaştır", "fa-code-compare", None), ("pNotlar", "Güncelleme ve düzeltme notları", "fa-pen-to-square", None)], "Sürüm geçmişi sekmeleri")
               + panel("pSurum", s_liste, ilk=True) + panel("pFark", fk) + panel("pNotlar", n_liste) + '</section>')
    ozet = kart("Haber", "fa-newspaper", govde_cls=None, ic=durum_dl([("Durum", "Yayında"), ("Sürüm", "4"), ("İlk yayın", "23.11.2026 14.05"), ("Son değişiklik", "23.11.2026 15.20"), ("Güncelleme", "2"), ("Düzeltme", "1")]))
    kural = kart("Kural", "fa-scale-balanced", f'<p class="fhint">Güncelleme: haberde yeni bilgi; düzenlenir ve silinir. Düzeltme: yanlış bir bilginin düzeltilmesi; yayımlandıktan sonra değiştirilemez ve silinemez, Düzeltme Politikası sayfasına yazılır (B9).</p><a class="kb-bag" href="{SITE}duzeltme-politikasi.html" target="_blank" rel="noopener">Düzeltme Politikası sayfası</a>')
    govde = bas("Sürüm Geçmişi", "Asgari ücret görüşmelerinde ilk toplantı 4 Aralık'ta yapılacak · Sürüm 4 yayında · 2 güncelleme, 1 düzeltme notu",
                [a_hedef("Habere dön", "fa-arrow-left", "haberler.duzenle"), btn("Düzeltme notu ekle", "fa-pen-to-square", attr=' data-tanim="srYeniDuzeltme"'), btn("Güncelleme ekle", "fa-plus", "btn-acc", ' data-tanim="srYeniGuncelleme"')])
    govde += f'  <div class="form-layout">\n  {kartlar}\n  {yan(ozet, kural)}\n  </div>\n'
    YAZILDI.append(sayfa("surumler.html", "Sürüm Geçmişi", "haberler.surumler", govde, "".join(sab), editor=True))

# ======================================================================= 12 · KÖŞE YAZILARI (t-kose; Beyar onayı: Haberler altında ayrı bölüm)
# Site karşılığı: kose-yazisi.html (detay), yazar.html (yazarın köşe yazıları), yazarlar.html (bant). Sitede "köşe adı" yok:
# köşe yazısı yazarın adıyla ve konusuyla görünür; panel de yalnız bunları sorar.
KOSE_YAZARLAR = [y for y in YAZARLAR if y["alan"] == "Köşe"]
KOSE_ADLAR = {y["ad"] for y in KOSE_YAZARLAR}
KOSE_PASIF = {"Pınar Okyay"}  # yazarlar listesiyle aynı örnek (pasif yazar formda seçilemez)
_TUM_ADLAR = {y["ad"] for y in YAZARLAR}
def kose_konu(h):
    a = h.get("alt_konu") or ""
    return "Görüş" if (not a or a in _TUM_ADLAR) else a  # sözlükte 4 yazıda alt_konu bir yazar adı: sitede konu etiketi "Görüş"
KOSE_YAYINDA = sorted([h for h in soz["haberler"] if h.get("detay") == "kose-yazisi.html"], key=lambda h: (h["tarih"], h["saat"]), reverse=True)
KOSE_EK = [  # panele özgü örnek kayıtlar (taslak, zamanlanmış, çöp); sitede henüz yok
    {"id": "esnek-calisma-kadinlar-icin-gercekten-esnek-mi", "baslik": "Esnek çalışma kadınlar için gerçekten esnek mi?", "yazar": "Füsun Erdem", "alt_konu": "Kadın Yazarlar", "tarih": "2026-11-23", "saat": "15.50", "durum": "taslak", "not": "taslak"},
    {"id": "yeni-yilda-kira-artisi-hesabi", "baslik": "Yeni yılda kira artışı hesabı: sözleşmeden önce bakılacak üç kalem", "yazar": "Aylin Sezer", "alt_konu": "Enflasyon", "tarih": "2026-11-24", "saat": "07.00", "durum": "zamanli"},
    {"id": "goc-pazarliginin-ikinci-perdesi", "baslik": "Göç pazarlığının ikinci perdesi", "yazar": "Leyla Sarıgül", "alt_konu": "Görüş", "tarih": "2026-11-20", "saat": "18.40", "durum": "cop", "onceki": "taslak"}]
KOSE_SAYI = {}
for h in KOSE_YAYINDA: KOSE_SAYI[h["yazar"]] = KOSE_SAYI.get(h["yazar"], 0) + 1
KOSE_KONULAR = []
for h in KOSE_YAYINDA:
    k = kose_konu(h)
    if k not in KOSE_KONULAR: KOSE_KONULAR.append(k)
def yazar_unvan(ad): return next((y["unvan"] for y in YAZARLAR if y["ad"] == ad), "")
def kose_konulari(ad, n=3):
    say = {}
    for h in KOSE_YAYINDA:
        if h["yazar"] == ad: k = kose_konu(h); say[k] = say.get(k, 0) + 1
    return [k for k, _ in sorted(say.items(), key=lambda x: -x[1])[:n]]
def kose_suz(ad):  # yazara süzülü köşe listesi (çekirdek: ?suz-<anahtar>=<değer>, lead'e bildirildi)
    return "?suz-yazar=" + ad.replace(" ", "%20")
def tarih_tr(t_, s_): return f"{t_[8:]}.{t_[5:7]}.{t_[:4]} {s_}"

KOSE_DURUM = {"yayinda": ("ok", "Yayında"), "taslak": ("off", "Taslak"), "zamanli": ("info", "Zamanlanmış"), "cop": ("warm", "Çöpte")}
def kose_yazilari():
    kayitlar = [dict(x) for x in KOSE_EK if x["durum"] != "cop"] + [dict(h, durum="yayinda") for h in KOSE_YAYINDA] + [dict(x) for x in KOSE_EK if x["durum"] == "cop"]
    satir = []
    for i, h in enumerate(kayitlar):
        sl, ad, d = h["id"], h["yazar"], h["durum"]
        konu = kose_konu(h)
        cls, dad = KOSE_DURUM[d]
        zaman = tarih_tr(h["tarih"], h["saat"])
        href = f"kose-duzenle.html?id={sl}"
        alt = f'<b>{e(ad)}</b> · {e(konu)}' + (f' · {e(h["sure"])}' if h.get("sure") else "")
        ava = f'<span class="kb-ava{" is-pasif" if ad in KOSE_PASIF else ""}" title="{e(ad)} · kapak yoksa kartta bu fotoğraf görünür">{bas_harf(ad)}</span>'
        gor = h.get("goruntulenme", "—") if d == "yayinda" else "—"
        bak = ia_a(SITE + "kose-yazisi.html", "Sitede Görüntüle", "fa-eye", True) if d == "yayinda" else ia_a(href, "Önizle", "fa-eye")
        satir.append(tr(sl, d, f'{h["baslik"]} {ad} {konu}', h["baslik"],
            [ana_hucre(h["baslik"], alt, ava=ava, alt_ham=True), (rozet(cls, dad), ""),
             (f'<span class="kb-tarih{" muted" if d in ("taslak", "cop") else ""}">{zaman}</span>', "kb-gizle-m"), (e(gor), "say kb-gizle-t")],
            bak + ia_a(href, "Düzenle", "fa-pen") + SIL + DIGER, href=href, yazar=ad, konu=konu,
            yerler=("bulten" if d == "yayinda" and i % 7 == 3 else ""), **({"onceki": h["onceki"]} if h.get("onceki") else {})))
    menu = (m_grup("Yayın", "yayinda taslak zamanli")
            + m_btn("Şimdi yayımla", "fa-paper-plane", "taslak zamanli", ' data-bildir="Köşe yazısı yayımlandı (prototip)"')
            + m_btn("Yayın zamanını değiştir", "fa-calendar-days", "yayinda taslak zamanli", ' data-bildir="Yayın zamanı düzenleme ekranında (prototip)"')
            + m_btn("Yayından kaldır", "fa-eye-slash", "yayinda", ' data-bildir="Köşe yazısı yayından kaldırılıp taslağa alındı (prototip)"')
            + m_ayir("yayinda") + m_grup("Dağıtım", "yayinda")
            + m_btn("Bildirim gönder", "fa-bell", "yayinda", ' data-modul="etkilesim" data-bildir="Bildirim sekmesi düzenleme ekranında (prototip)"')
            + m_btn("Sosyal medyada paylaş", "fa-share-nodes", "yayinda", ' data-modul="sosyal-medya" data-bildir="Sosyal Medya sekmesi düzenleme ekranında (prototip)"')
            + f'<button type="button" data-modul="etkilesim" data-durum-icin="yayinda" data-yer="bulten" data-yer-ad="Akşam Bülteni">{I("fa-envelope-open-text")}<span>Bültene ekle</span></button>'
            + m_btn("Bağlantıyı kopyala", "fa-link", "yayinda", " data-kopyala")
            + m_ayir("yayinda taslak zamanli") + m_grup("İçerik", "yayinda taslak zamanli")
            + m_a("Güncelleme ekle", "fa-arrows-rotate", "haberler.surumler", "?sekme=pNotlar", ' data-durum-icin="yayinda"')
            + m_a("Düzeltme notu ekle", "fa-pen-to-square", "haberler.surumler", "?sekme=pNotlar", ' data-durum-icin="yayinda"')
            + m_btn("Kopyasını oluştur", "fa-copy", "yayinda taslak zamanli", ' data-bildir="Kopyası taslak olarak oluşturuldu (prototip)"')
            + f'<button type="button" data-durum-icin="yayinda" disabled title="Çeviri ekranları sonraki aşamada">{I("fa-language")}Çeviri iste<span class="pm-ek">Sonraki aşama</span></button>'
            + m_ayir("yayinda taslak zamanli") + m_grup("Kayıt")
            + m_a("Sürüm Geçmişi", "fa-clock-rotate-left", "haberler.surumler") + DENETIM + COP_MENU)
    yazar_ops = [("", "Bütün köşe yazarları")] + [(y["ad"], y["ad"], "Pasif" if y["ad"] in KOSE_PASIF else f'{KOSE_SAYI.get(y["ad"], 0)}') for y in KOSE_YAZARLAR]
    konu_ops = [("", "Bütün konular")] + [(k, k) for k in KOSE_KONULAR]
    n = len(kayitlar); n_acik = sum(1 for k in kayitlar if k["durum"] != "cop")
    govde = bas("Köşe Yazıları", f'{len(KOSE_YAYINDA)} köşe yazısı yayında · {len(KOSE_YAZARLAR)} köşe yazarı · 1 taslak, 1 zamanlanmış · sitede yazar sayfasında ve Yazarlar bandında',
                [a_hedef("Köşe yazarları", "fa-pen-nib", "haberler.yazarlar", "?suz-tur=kose"),
                 a_hedef("Yeni köşe yazısı", "fa-plus", "haberler.kose-duzenle", "?yeni=1", "btn-acc")])
    L = liste("köşe yazısı", "Köşe yazısı listesi", [("hepsi", "Tümü", 0), ("yayinda", "Yayında", 0), ("taslak", "Taslak", 0), ("zamanli", "Zamanlanmış", 0)], "Başlık, Yazar ya da Konu Ara",
        [("yazar", "Yazar", "kySuzYazar", yazar_ops, "Yazar ara"), ("konu", "Konu", "kySuzKonu", konu_ops, "Konu ara")],
        [btn("Yayından kaldır", "fa-eye-slash", attr=' data-toplu="taslak" data-bildir="Seçilen köşe yazıları yayından kaldırılıp taslağa alındı"'), btn("Çöpe Taşı", "fa-trash", "btn-ghost danger", ' data-toplu="cop"')],
        [('<input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün köşe yazılarını seç">', "kb-sec-hucre"), ("Köşe Yazısı", "kb-ana"), ("Durum", ""), ("Yayın", "kb-gizle-m"), ("Okunma", "say kb-gizle-t"), ('<span class="sr-only">İşlemler</span>', "")],
        satir, menu, bos_durum("kose-yazilari.html", "Köşe yazıları yüklenemedi", "fa-feather-pointed", "Henüz köşe yazısı yok", "Köşe yazarlarından birinin ilk yazısını ekleyin; yazı yazar sayfasında ve Yazarlar bandında görünür.", f'<a class="pe-tag" data-hedef="haberler.kose-duzenle" data-hedef-ek="?yeni=1" href="#">{I("fa-plus")}Yeni köşe yazısı</a>'),
        f"{n} sonuçtan 1–{n} gösteriliyor", sayfa_boy=40, liste_cop_not="Yazar sayfasından ve Yazarlar bandından kalkar ve Çöp sekmesine taşınır")
    gez = ('<nav class="kb-medya-gez kb-gez-sayfa" aria-label="Köşe yazarına göre gez">'
           + f'<button type="button" data-gez-suz="yazar" data-v="">Bütün köşe yazıları<span>{n_acik}</span></button><div class="kmg-tt">Köşe yazarları</div>'
           + "".join(f'<button type="button" data-gez-suz="yazar" data-v="{e(y["ad"])}" aria-pressed="false" title="{e(y["ad"])} · {e(y["unvan"])}">{e(y["ad"])}{"<small>Pasif</small>" if y["ad"] in KOSE_PASIF else ""}<span>{sum(1 for k in kayitlar if k["yazar"] == y["ad"] and k["durum"] != "cop")}</span></button>' for y in KOSE_YAZARLAR)
           + '</nav>')
    L = L.replace('<div class="ptable-wrap">', f'<div class="kb-medya-gov">{gez}<div><div class="ptable-wrap">', 1).replace('\n<div class="pnl-menu kb-diger-menu"', '</div></div>\n<div class="pnl-menu kb-diger-menu"', 1)
    govde += L
    YAZILDI.append(sayfa("kose-yazilari.html", "Köşe Yazıları", "haberler.kose", govde))

# ======================================================================= 13 · KÖŞE YAZISI DÜZENLE (haber düzenleme ekranının köşe varyantı)
KY_METIN = ("<p>Geçen hafta gece yarısına doğru bir üniversite kütüphanesinin önünden geçtim. Kapıda, içeride yer açılmasını bekleyen otuz kadar öğrenci vardı. Kimi ayakta not okuyor, kimi telefonundan ders videosu izliyordu. O kuyruğu görünce, sınav haftalarında açılan gece salonlarını hâlâ bir istisna gibi konuşmamızın ne kadar yanlış olduğunu düşündüm.</p>"
            "<p>Bu öğrencilerin çoğu evde çalışabilecek bir oda bulamadığı için orada. Kalabalık bir evde, paylaşılan bir yurt odasında ya da kirası ancak bölünerek ödenebilen bir dairede sessiz bir köşe bulmak sanıldığı kadar kolay değil. Kütüphane, onlar için bir masa ve bir prizden fazlası; dikkatin dağılmadığı tek yer.</p>"
            "<h2>Kuyruk bize ne anlatıyor?</h2>"
            "<p>Kütüphane istatistiklerine baktığımda, salonların doluluk oranının sınav dönemlerinde yüzde yüzü aştığını, yani kapasitenin üzerinde öğrencinin sırayla yer kullandığını görüyorum. Bu tablo bir yoğunluk anından değil, yapısal bir eksiklikten söz ediyor. Talep yalnızca birkaç hafta artmıyor; o haftalarda görünür hale geliyor.</p>"
            "<p>Bana göre sorun yalnızca üniversitelerin değil. Belediye kütüphaneleri çoğu zaman akşam erken saatte kapanıyor, hafta sonu kısa çalışıyor. Oysa üniversiteye hazırlanan liseli de, işten sonra sınava çalışan genç de akşam saatlerinde yer arıyor.</p>"
            "<h2>Kalıcı bir düzen mümkün</h2>"
            "<p>Gece çalışmanın maliyetli olduğunu biliyorum: personel, güvenlik, ısınma. Ama bazı şehirlerde denenen modeller bu maliyetin yönetilebildiğini gösteriyor. Gece saatlerinde salonların yalnızca bir bölümünü açık tutmak, giriş için öğrenci kartı ya da kütüphane kartı istemek ve aydınlatmayı kullanılan alanla sınırlamak, giderleri ciddi biçimde azaltabiliyor.</p>"
            "<p>Kütüphaneleri hâlâ kitap ödünç alınan yerler olarak görmeye devam edersek bu kuyrukları her dönem yeniden konuşacağız. Gece de açık kalmaları bir lütuf değil; bu ihtiyacı görmemizin en somut yolu.</p>")
def kose_duzenle():
    h = next(x for x in KOSE_YAYINDA if x["id"] == "kutuphanelerin-gece-de-acik-kalmasi-bir-lutuf-degil-ihtiyac")
    ad = h["yazar"]; kp = "kyKapak"; n = KOSE_SAYI.get(ad, 0)
    baslik = h["baslik"]
    spot = "Sınav haftalarında gece boyunca açık kalan kütüphanelerin önündeki kuyruk, gençlerin çalışacak sakin bir yer bulmakta ne kadar zorlandığını gösteriyor. Bu uygulamanın kalıcı olması gerekiyor."
    yazar_ops = [(y["ad"], y["ad"], y["unvan"]) for y in KOSE_YAZARLAR if y["ad"] not in KOSE_PASIF]
    detay = (fs("Yazı", "fa-feather-pointed", grid(
                girdi("kyBaslik", "Başlık", baslik, "baslik", "70|90", "Sitede yazının başlığı; SEO başlığı buradan üretilir", cls="finput kb-buyuk", ek=' data-alan="baslik"', hata="Başlık zorunlu."),
                alan("kySpot", "Spot", spot, "spot", "220|280", "Başlığın altındaki giriş cümlesi; Yazarlar bandında da görünür", ek=' data-alan="spot"', hata="Spot zorunlu.")))
             + ai_adim("#kyBaslik,#kySpot", [("sinif", "Konu önerisi", True, None), ("seo", "SEO", True, None), ("bildirim", "Bildirim Metni", True, "etkilesim"), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")],
                       durum="Başlığı ve spotu yazın; işaretli bölümler bunlardan üretilir. Yazının metni yazarındır, AI taslak yazmaz. Üretilen her bölüm “AI önerisi” etiketiyle gelir.")
             + fs("Köşe", "fa-pen-nib", grid(
                 '<div class="frow two">'
                 + frow("Köşe yazarı", secim("kyYazar", yazar_ops, ad, "Köşe yazarı seçin", "Köşe yazarı ara", alan_id="yazar", bos_metin="Bu adla köşe yazarı yok."),
                        ipucu=f'Yalnız etkin köşe yazarları listelenir. Yeni köşe yazarı <a class="kb-bag" data-hedef="haberler.yazar" data-hedef-ek="?yeni=1" href="#">Yazarlar’dan</a> eklenir (Tür: Köşe yazarı).', hata="Köşe yazarı seçin.")
                 + frow("Ana Kategori", '<span class="kb-kat"><b>Köşe</b></span>', ipucu="Köşe yazılarında sabittir; adres yazarın adıyla kurulur.")
                 + '</div>',
                 frow("Konular", cip_girdi([kose_konu(h)], KOSE_KONULAR, "Konu ara ya da yazıp ekleyin", ek=' data-alan-id="konu" data-birincil data-havuz-yonet data-kullanim-birim="yazıda"'),
                      ipucu="İlk seçilen ana konudur; sitede başlığın üstündeki etikette görünür. Havuzda yoksa yazıp Enter’la eklenir."),
                 frow("Ek kategori ve alt konular", cip_girdi(["Kampüs › Üniversiteler"], ["Kadın › Kadın Yazarlar", "Kampüs › Üniversiteler", "Finans › Kişisel Finans", "Gündem › Toplum", "Gündem › Eğitim"], "Kategori ara"),
                      ipucu="İsteğe bağlı; yazı bu sayfalarda da listelenir (ör. kadın yazarların yazıları Kadın › Kadın Yazarlar’da).")), attr=' data-ai-grup="sinif"')
             + kapak(kp, "p163", (50, 45), "İsteğe bağlı · yoksa yazar fotoğrafı", "Sınav haftasında gece de açık kalan bir üniversite kütüphanesi · Dada Haber arşivi")
             + fs("Kartta görünen görsel", "fa-id-badge", grid(anahtar("Kapak yerine yazar fotoğrafı", "Açıksa sitede köşe kartında ve Yazarlar bandında yazarın fotoğrafı görünür; kapak yalnız yazının sayfasında kalır. Kapak boşsa kendiliğinden açıktır.", False)))
             + fs("Yazı metni", "fa-align-left", editor("Yazı metni", KY_METIN, "metin", medya=True, zm="Yazının metnini yazın", alt="Sitede “Yazıyı dinle” bu metinden okunur"), ek_bas="Ara başlık, bağlantı, alıntı ve görsel")
             + fs("Kaynaklar", "fa-link", satir_liste("Kaynak", "Kaynak adı (kurum, belge)", "Açıklama, tarih ya da bağlantı", [
                 ("Türkiye İstatistik Kurumu", "Kütüphane İstatistikleri, 2025"), ("Yükseköğretim Kurulu", "Üniversite kütüphaneleri kullanım verileri, 2025-2026 akademik yılı"),
                 ("Kütüphaneler ve Yayımlar Genel Müdürlüğü", "Halk kütüphaneleri çalışma saatleri ve hizmet standartları")], "Kaynak ekle"), ek_bas="İsteğe bağlı · sitede yazının sonunda")
             + fs("Okur ve yayın ayarları", "fa-sliders", grid(
                 anahtar("Görüş notu", "Yazının sonunda: “Bu yazı yazarın görüşüdür; Dada Haber'in yayın çizgisini bağlamaz.”", True),
                 anahtar("Yorumlar Açık", "Yorumları editörler yönetir", True),
                 anahtar("Yazıyı dinle", "Yapay zekâ ile seslendirilir; sitede “Yazıyı dinle” oynatıcısı", True),
                 anahtar("Okur düzeltme bildirimi", "Okur “düzeltme bildir” bağlantısını görür", True))))
    form = (f'<section class="pnl-card" id="kyForm" data-form data-sekmeli data-zorunlu-kayit="haberler.kose" aria-label="Köşe yazısı formu">'
            + dil("Dil seçici bütün sekmelerdeki metin alanlarını birlikte değiştirir; yazar, görsel ve konu bütün dillerde ortaktır.")
            + sekmeler([("pDetay", "Detay", "fa-file-lines", None), ("pSeo", "SEO", "fa-magnifying-glass-chart", None), ("pBildirim", "Bildirim", "fa-bell", "etkilesim"), ("pSosyal", "Sosyal Medya", "fa-share-nodes", "sosyal-medya")])
            + panel("pDetay", detay, ilk=True)
            + seo_panel("Kütüphaneler gece de açık kalmalı | Aylin Sezer", "Sınav haftalarındaki kütüphane kuyrukları geçici bir yoğunluk değil, yapısal bir eksiklik. Aylin Sezer'in köşe yazısı Dada Haber'de.", "dadahaber.com/yazar/aylin-sezer/", "kutuphanelerin-gece-de-acik-kalmasi", ["kütüphane", "üniversite", "gençlik", "kent yaşamı"])
            + bildirim_panel("", "Aylin Sezer yazdı: Kütüphaneler gece de açık kalmalı", "Sınav haftalarındaki kuyruklar geçici bir yoğunluk değil, yapısal bir eksiklik. Yeni köşe yazısı Dada Haber'de.")
            + sosyal_panel("", kp, "p163", (50, 45), {
                "x": "Kütüphanelerin gece de açık kalması bir lütuf değil, ihtiyaç. Aylin Sezer yazdı.\n\nhttps://dadahaber.com/yazar/aylin-sezer/kutuphanelerin-gece-de-acik-kalmasi\n\n#kütüphane #gençlik",
                "facebook": "Sınav haftalarındaki kütüphane kuyrukları ne anlatıyor? Aylin Sezer'in yeni köşe yazısı.\n\nhttps://dadahaber.com/yazar/aylin-sezer/kutuphanelerin-gece-de-acik-kalmasi",
                "linkedin": "Gençlerin çalışacak sakin bir yere ihtiyacı var: üniversite ve belediye kütüphaneleri saatlerini birlikte planlayabilir. Aylin Sezer yazdı.\n\nhttps://dadahaber.com/yazar/aylin-sezer/kutuphanelerin-gece-de-acik-kalmasi",
                "instagram": "Kütüphaneler gece de açık kalmalı 📚 Aylin Sezer'in yeni yazısı; bağlantı profilde.\n\n#kütüphane #üniversite #dadahaber",
                "telegram": "✍️ Aylin Sezer · Köşe yazısı\n\nKütüphanelerin gece de açık kalması bir lütuf değil, ihtiyaç.\n\nhttps://dadahaber.com/yazar/aylin-sezer/kutuphanelerin-gece-de-acik-kalmasi"}, "yazar/aylin-sezer")
            + '</section>')
    yk = yayin_karti("kyY", [("yayinda", "Yayında"), ("taslak", "Taslak", "yayından kalkar"), ("zamanli", "Zamanlanmış")], "yayinda", "2026-11-23 07.00",
        anahtar("Yazarlar bandında", "Ana sayfadaki Yazarlar · Köşe Yazıları rayında ve Yazarlar sayfasında son yazı olarak", True),
        ("Sürüm 2", "son değişiklik 23.11.2026 09.30 · Aylin Sezer", f'?id={h["id"]}'))
    yazar_kart = kart("Köşe yazarı", "fa-pen-nib",
        f'<div class="rcp-cell"><span class="kb-ava k-lg">{bas_harf(ad)}</span><div class="rcp-id"><div class="rcp-name">{e(ad)}</div><div class="rcp-by">{e(yazar_unvan(ad))} · {n} köşe yazısı</div></div></div>'
        f'<p class="fhint"><a class="kb-bag" data-hedef="haberler.kose" data-hedef-ek="{kose_suz(ad)}" href="#">Bütün köşe yazıları</a> · <a class="kb-bag" data-hedef="haberler.yazar" data-hedef-ek="?id={tr_slug(ad)}" href="#">Yazar bilgileri</a></p>')
    yazar_kart = yazar_kart.replace('<section class="pnl-card">', '<section class="pnl-card" data-yeni-gizle>', 1)
    govde = bas("Köşe yazısı düzenle", f'Köşe · {e(ad)} · {tarih_tr(h["tarih"], h["saat"])}’de yayımlandı · 09.30’da güncellendi · {h["goruntulenme"]} okunma',
                [a_hedef("Köşe yazılarına dön", "fa-arrow-left", "haberler.kose"), a_dis("Sitede Görüntüle", "fa-arrow-up-right-from-square", SITE + "kose-yazisi.html", " data-yeni-gizle")],
                h1_yeni="Yeni köşe yazısı", alt_yeni="Köşe · taslak · henüz kaydedilmedi · köşe yazarını seçin")
    govde += f'  <div class="form-layout">\n  {form}\n  {yan(yan_onizleme("", "Aylin Sezer yazdı: Kütüphaneler gece de açık kalmalı", "Sınav haftalarındaki kuyruklar geçici bir yoğunluk değil, yapısal bir eksiklik. Yeni köşe yazısı Dada Haber\'de.", "p163", 50, 45, baslik), yk, seo_skor(84, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Kapak görseli 1200 px üstü"), (False, "Yazının içinde başka yazıya bağlantı yok")]), yazar_kart)}\n  </div>\n'
    govde += kaydet("kyForm", "Kaydedildi · 23.11.2026 09.30 · Aylin Sezer", "Güncelle", "Köşe yazısı güncellendi; sitede yayında, önceki hal sürüm geçmişinde", "Yayımla", "Köşe yazısı yayımlandı; yazar sayfasında ve Yazarlar bandında görünür")
    YAZILDI.append(sayfa("kose-duzenle.html", "Köşe yazısı düzenle", "haberler.kose-duzenle", govde, editor=True, body_ek=' data-yeni-baslik="Yeni köşe yazısı"'))

for f in (vitrin, son_dakika, canli, canli_masa, dosyalar, dosya, gunun_5, inceleme, yazarlar, yazar, surumler, kose_yazilari, kose_duzenle):
    f()
print("yazıldı:", ", ".join(YAZILDI))
