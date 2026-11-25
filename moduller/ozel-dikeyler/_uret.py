#!/usr/bin/env python3
"""Özel Widgetlar modülü · sayfa üretici (yalnızca moduller/ozel-dikeyler/ altına yazar).

Kullanım:  python3 -I moduller/ozel-dikeyler/_uret.py && python3 -I araclar/menu_yaz.py --yalniz moduller/ozel-dikeyler

Kaynaklar (yalnızca okunur): public sözlük (ornek_veri.json: puan_tablosu, piyasa, hava, haberler), public sayfa metinleri
(fikstür, canlı skor, takvimler, resmî ilanlar), moduller.json, public araclar/kategori.json (kategori ağacı, DADAHABER-10).
Sayfalar: spor, kulup, takvimler, veri, burclar, burc, ilanlar, ilan. Anket, Sözlük, Firma Rehberi kapalı (K1), üretilmez.
"""
import html, json, re
from pathlib import Path

BURA = Path(__file__).resolve().parent
KOK = BURA.parents[1]
PUB = KOK.parent / "dadahaber-prototip"
SITE = "https://gaviaworks-dev.github.io/dadahaber-prototip/"
e = lambda s: html.escape(str(s), quote=True)
soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
kayit = json.loads((KOK / "moduller.json").read_text(encoding="utf-8"))
KAT = json.loads((PUB / "araclar" / "kategori.json").read_text(encoding="utf-8"))  # kategori ağacı · tek kaynak (DADAHABER-10)
I = lambda c, ek="": f'<i class="fa-solid {c}"{ek} aria-hidden="true"></i>'


# Haber alt konusu olmayan servis sayfaları: tek liste moduller.json → haberler.ayarlar.servis_sayfalari (yalnız okunur)
_SV = [m for m in kayit["moduller"] if m["id"] == "haberler"][0]["ayarlar"]["servis_sayfalari"]
SERVIS_SUTUN, SERVIS_OGE = set(_SV["sutunlar"]), set(_SV["ogeler"])


def alt_konular():
    """{ana kategori: [alt konular]} · kategori.json sütun sırasıyla"""
    return {b["ad"]: [o["ad"] for s in b["sutunlar"] if s["ad"] not in SERVIS_SUTUN for o in s["ogeler"] if o["ad"] not in SERVIS_OGE] for b in KAT["basliklar"]}


def sayi(n):
    return f"{n:,}".replace(",", ".")


def para(x, d=2):
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tarih_kisa(t):  # "23.11.2026 15.58" → bugünse "15.58"
    return t[11:] if t.startswith("23.11.2026") else t[:5] + " " + t[11:]


I = lambda c, ek="": f'<i class="fa-solid {c}"{ek} aria-hidden="true"></i>'


# ------------------------------------------------------------------ iskelet
def bas(baslik, sayfa, ek=""):
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{baslik} · Dada Haber Yönetim Paneli</title>
<link rel="stylesheet" href="../../assets/vendor/fontawesome-6.5.2/css/all.min.css?v=c84e8169">
<link rel="stylesheet" href="../../tema/dadahaber.css?v=64b109bb" data-tema>
<link rel="stylesheet" href="../../cekirdek/css/kabuk.css?v=9a2ad8c2">
<link rel="stylesheet" href="../../cekirdek/css/bilesen.css?v=6ab2ea5c">
<!--P:bas--><!--/P:bas-->
</head>
<body data-sayfa="ozel-dikeyler.{sayfa}"{ek}>
<div class="sa-app">
<!--P:menu--><!--/P:menu-->
<div class="pnl-overlay" id="pnlOverlay"></div>
<!--P:ust--><!--/P:ust-->
"""


def son(editor=False):
    s = """<script src="../../cekirdek/js/kabuk.js?v=4a1fba0b"></script>
<script src="../../cekirdek/js/bilesen.js?v=c2de94e7"></script>
<script src="../../cekirdek/js/form.js?v=dc6c8c08"></script>
<script src="../../cekirdek/js/alan.js?v=e0730eae"></script>
<script src="../../cekirdek/js/kirp.js?v=7e601950"></script>
"""
    if editor:
        s += """<script src="../../assets/vendor/tiptap-2.27.3/tiptap.min.js?v=cfbc905d"></script>
<script src="../../cekirdek/js/editor.js?v=d7e6c511"></script>
"""
    return s + "</body>\n</html>\n"


def secim(id_, secenekler, deger="", bos="Seçin", etk="", ara=None, ek="", suz=None, kaynak=None):
    """kb-secim: secenekler [(deger, ad, alt)]; kaynak="tplId" → liste sayfadaki ortak <template>'ten dolar (çekirdek liste havuzu)"""
    sec = [s for s in secenekler if s[0] == deger]
    gor = sec[0][1] if sec else bos
    ops = "".join(f'<button type="button" data-deger="{e(d)}" data-ad="{e(a)}"{" class=\"is-sec\"" if d == deger and d else ""}>{e(a)}{f"<span class=\"ks-alt\">{e(al)}</span>" if al else ""}</button>' for d, a, al in secenekler)
    arak = f'<div class="kb-secim-ara">{I("fa-magnifying-glass")}<input type="search" placeholder="{e(ara)}" aria-label="{e(ara)}"></div>' if ara else ""
    bosk = '<div class="kb-secim-bos" hidden>Bu adla sonuç yok.</div>' if ara else ""
    sz = f' data-suz="{suz}"' if suz else ""
    dg = f' data-deger="{e(deger)}"' if deger else ""
    et = f'<span class="ks-etk">{e(etk)}</span>' if etk else ""
    return (f'<div class="kb-secim{" is-dolu" if deger else ""}"{sz}{dg} data-bos="{e(bos)}"{ek}>'
            f'<button type="button" class="kb-secim-btn" data-acilir="{id_}" aria-expanded="false" aria-haspopup="listbox">{et}<span class="ks-deger">{e(gor)}</span>{I("fa-chevron-down")}</button>'
            f'<div class="pnl-menu kb-secim-menu" id="{id_}">{arak}<div class="kb-secim-liste" role="listbox"{f" data-liste-kaynak=\"{kaynak}\"" if kaynak else ""}>{"" if kaynak else ops}</div>{bosk}</div></div>')


def row_acts(gor, duz, sil, gor_ad="Görüntüle", duz_ad="Düzenle", sil_ad="Çöpe Taşı", diger=True):
    """gor/duz: ('href', url) | ('tanim', id) | ('kilit', neden); sil: 'sil' | ('tasi', attrs) | ('kilit', neden)"""
    def b(x, ikon, ad):
        if x[0] == "href":
            hed = f' data-hedef="{x[2]}"' if len(x) > 2 else ""
            tgt = ' target="_blank" rel="noopener"' if x[1].startswith("http") else ""
            return f'<a class="ia-btn" href="{e(x[1])}"{hed}{tgt} aria-label="{e(ad)}" title="{e(ad)}">{I(ikon)}</a>'
        if x[0] == "tanim":
            return f'<button type="button" class="ia-btn" data-tanim="{x[1]}" aria-label="{e(ad)}" title="{e(ad)}">{I(ikon)}</button>'
        return f'<button type="button" class="ia-btn kb-kilit" disabled aria-label="{e(ad)}: kilitli" title="{e(x[1])}">{I("fa-lock")}</button>'
    s = b(gor, "fa-eye", gor_ad) + (b(duz, "fa-pen", duz_ad) if duz else "")  # yapılamayan eylemin düğmesi çizilmez (Beyar)
    if sil is None:
        pass
    elif sil == "sil":
        s += f'<button type="button" class="ia-btn danger" data-sil aria-label="{e(sil_ad)}" title="{e(sil_ad)}">{I("fa-trash")}</button>'
    elif sil[0] == "tasi":
        s += f'<button type="button" class="ia-btn danger" {sil[1]} aria-label="{e(sil_ad)}" title="{e(sil_ad)}">{I("fa-trash")}</button>'
    else:
        s += f'<button type="button" class="ia-btn kb-kilit" disabled aria-label="Silinemez" title="{e(sil[1])}">{I("fa-lock")}</button>'
    if diger:
        s += f'<button type="button" class="ia-btn" data-diger aria-haspopup="true" aria-expanded="false" aria-label="Diğer işlemler" title="Diğer">{I("fa-ellipsis")}</button>'
    return f'<div class="row-acts">{s}</div>'


def durum_govdeleri(n, ikon, bos_bas, bos_metin, hata_bas, hata_metin, bos_eylem="", iskelet=None, yeniden="index.html"):
    isk = iskelet or ("<td></td>" * n)
    return f"""        <tbody>
          <tr class="kb-bos-satir" hidden><td colspan="{n}"><div class="pnl-empty">
            <div class="pe-ico">{I("fa-magnifying-glass")}</div>
            <h2>Bu süzgeçlerle sonuç yok</h2>
            <p>Arama metnini kısaltmayı ya da süzgeçleri kaldırmayı deneyin.</p>
            <button type="button" class="pe-tag" data-suz-temizle>{I("fa-filter-circle-xmark")}Süzgeçleri Temizle</button>
          </div></td></tr>
        </tbody>
        <tbody data-durum-goster="yukleniyor" hidden>
          {('<tr class="kb-iskelet">' + isk + '</tr>') * 4}
        </tbody>
        <tbody data-durum-goster="hata" hidden>
          <tr><td colspan="{n}"><div class="pnl-empty kb-hata">
            <div class="pe-ico">{I("fa-triangle-exclamation")}</div>
            <h2>{hata_bas}</h2>
            <p>{hata_metin}</p>
            <a class="pe-tag" href="{yeniden}">{I("fa-rotate-right")}Yeniden Dene</a>
          </div></td></tr>
        </tbody>
        <tbody data-durum-goster="bos" hidden>
          <tr><td colspan="{n}"><div class="pnl-empty">
            <div class="pe-ico">{I(ikon)}</div>
            <h2>{bos_bas}</h2>
            <p>{bos_metin}</p>{bos_eylem}
          </div></td></tr>
        </tbody>
"""


def pager(n_toplam_metin=True, sayfalar=True, son_=58):
    if not sayfalar:
        return '    <div class="pager"><div class="pager-info">—</div></div>\n'
    return f"""    <div class="pager">
      <div class="pager-info">—</div>
      <div class="pager-btns">
        <button type="button" class="pg-btn" disabled aria-label="Önceki sayfa">{I("fa-chevron-left")}</button>
        <button type="button" class="pg-btn is-on" aria-current="page">1</button>
        <button type="button" class="pg-btn pg-sayi" data-bildir-pg>2</button>
        <span class="pg-dots pg-sayi">…</span>
        <button type="button" class="pg-btn pg-sayi" data-bildir-pg>{son_}</button>
        <button type="button" class="pg-btn" data-bildir-pg aria-label="Sonraki sayfa">{I("fa-chevron-right")}</button>
      </div>
    </div>
"""


def gorsel_alani(anahtar, ad, baslik, ek, bos_yer, bos, web, mobil, olcu_web, olcu_mobil, ikon="fa-image", havuz=False, dolu=None, cekmece=False, nit=""):
    """Görsel alanı (çekirdek bileşen; emsal Kulüp Düzenle › Arma, Yazar Düzenle › Fotoğraf): web ve mobil ayrı bölüm, önerilen ölçü yazılı.
    web/mobil: [(kayıttaki oran anahtarı "web.detay", etiket, sınıf "r-1x1" ya da oran "2.9/1")]; ölçüler moduller.json → gorsel_alanlari.
    havuz: fotoğraf (medya havuzundan seçilir, yüklemede etiketlenir); değilse kurumsal işaret (etiketsiz, havuza girmez).
    bos: (boş kutu başlığı "Armayı sürükleyin ya da seçin", ölçü satırı) · bos_yer: yer tutucunun kendisi (rozet, ikon)
    dolu: (görsel adresi, odak "50% 40%", yüklenen bilgisi) · cekmece: çekmecede frow kabı, sayfada form-sec kabı."""
    def kutu(hedef, k, etk, r, ilk):
        sinif, stil = (r, []) if r.startswith("r-") else ("", [f"aspect-ratio:{r}"])
        if dolu: stil += [f"background-image:url({dolu[0]})", f"background-position:{dolu[1]}"]
        st = f' style="{";".join(stil)}"' if stil else ""
        od = f'<span class="kg-odak" style="left:{dolu[1].split()[0]};top:{dolu[1].split()[1]}"></span>' if dolu and ilk else ""
        return f'<div class="kg-resim{" " + sinif if sinif else ""}" data-gorsel-hedef="{hedef}" data-kirp-oran="{k}"{st}>{od}<span class="kg-etk">{e(etk)}</span></div>'
    wk = "".join(kutu("web", k, etk, r, i == 0) for i, (k, etk, r) in enumerate(web))
    wk = f'<div class="kg-ikili">{wk}</div>' if len(web) > 1 else wk
    mk = "".join(kutu("mobil", k, etk, r, i == 0) for i, (k, etk, r) in enumerate(mobil))
    mk = f'<div class="kg-ikili">{mk}</div>' if len(mobil) > 1 else mk
    hv = hv_acc = f'<button type="button" class="btn btn-ghost btn-sm" data-medya-sec>{I("fa-photo-film")}Havuzdan Seç</button>' if havuz else ""
    bilgi = f' <span data-gorsel-bilgi>{e(dolu[2])}</span>' if dolu else ""
    govde = (f'<div class="kb-yukle" data-gorsel-bos{" hidden" if dolu else ""}>{bos_yer}<b>{e(bos[0])}</b><span>{bos[1]}</span>'
             f'<span class="kg-acts"><button type="button" class="btn btn-acc btn-sm" data-gorsel-yukle>{I("fa-upload")}Bilgisayardan Yükle</button>{hv_acc}</span></div>'
             f'<div class="kb-gorsel" data-gorsel-dolu{"" if dolu else " hidden"}>'
             f'<div class="kg-bolum"><div class="kg-bas">{I("fa-desktop")}Web</div>{wk}<div class="kg-olcu">{olcu_web}{bilgi}</div>'
             f'<div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{I("fa-crop-simple")}Kırp ve Odak</button>{hv}'
             f'<button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{I("fa-upload")}Yükle</button><button type="button" class="btn btn-ghost btn-sm danger" data-gorsel-kaldir>{I("fa-trash")}Kaldır</button></div></div>'
             f'<div class="kg-bolum"><div class="kg-bas">{I("fa-mobile-screen")}Mobil<span class="kg-oto">{I("fa-wand-magic-sparkles")} Webden kırpıldı</span></div>{mk}<div class="kg-olcu">{olcu_mobil}</div>'
             f'<div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac="{"mobil.kart" if any(k == "mobil.kart" for k, _, _ in mobil) else mobil[0][0]}">{I("fa-crop-simple")}Kırp</button>'
             f'<button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle data-gorsel-kapsam="mobil">{I("fa-upload")}Ayrı Görsel Yükle</button>'
             f'<button type="button" class="btn btn-ghost btn-sm" data-gorsel-webe-don hidden>{I("fa-rotate-left")}Webden Kırpılana Dön</button></div></div></div>')
    at = f' data-gorsel-alan="ozel-dikeyler.{anahtar}" data-gorsel-ad="{e(ad)}" data-kirp-sonra{"" if havuz else " data-etiketsiz"}{nit}'
    if cekmece:
        return f'<div class="frow"{at}><span class="flabel">{e(baslik)}<span class="fhint kb-sag">{ek}</span></span>{govde}</div>'
    return f'<div class="form-sec"{at}><div class="form-sec-tt">{I(ikon)}{e(baslik)}<span class="fs-ek">{ek}</span></div>{govde}</div>'


def dil_secici(not_metni):
    return f"""    <div class="kb-form-bas">
      <div class="kb-dil" role="group" aria-label="İçerik dili">
        <button type="button" class="is-on" aria-pressed="true">TR · Türkçe</button>
        <button type="button" disabled title="Çeviri ekranları sonraki aşamada">EN<span class="kd-etk">Sonraki aşama</span></button>
        <button type="button" disabled title="Çeviri ekranları sonraki aşamada">AR<span class="kd-etk">Sonraki aşama</span></button>
        <button type="button" disabled title="Çeviri ekranları sonraki aşamada">DE<span class="kd-etk">Sonraki aşama</span></button>
      </div>
      <span class="kfb-not">{I("fa-language")}{not_metni}</span>
    </div>
"""



# ================================================================== SPOR
# Branş yapısı (Beyar, 25.11.2026): solda branş listesi (Gez kalıbı, medya havuzundaki gibi) üç sekmeyi birlikte süzer;
# branşlar sağ üstteki "Branşlar" çekmecesinde eklenir, düzenlenir, silinir (kayıt varsa taşıyarak, B1).
# Veri: public sitenin branş sayfaları (futbol, basketbol, voleybol, motor-sporlari, bisiklet, tenis, atletizm, olimpiyatlar, e-spor).
PT = soz["puan_tablosu"]
SEHIR = {"GS": "İstanbul", "FB": "İstanbul", "BJK": "İstanbul", "TS": "Trabzon", "BAŞ": "İstanbul", "SAM": "Samsun", "GÖZ": "İzmir", "KAS": "İstanbul",
         "EYP": "İstanbul", "ANT": "Antalya", "KON": "Konya", "ALN": "Antalya", "RİZ": "Rize", "GFK": "Gaziantep", "KOC": "Kocaeli", "AMD": "Diyarbakır",
         "KAY": "Kayseri", "GB": "Ankara"}
ALT = {"Galatasaray": "Galatasaray", "Fenerbahçe": "Fenerbahçe", "Beşiktaş": "Beşiktaş", "Trabzonspor": "Trabzonspor"}
SLUG = {"Galatasaray": "galatasaray.html", "Fenerbahçe": "fenerbahce.html", "Beşiktaş": "besiktas.html", "Trabzonspor": "trabzonspor.html"}
TR_SLUG = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower().translate(str.maketrans("çğıöşüâîé", "cgiosuaie"))).strip("-")

# ad, ikon, site sayfası, puan tablosu biçimi, spor veri API eşleşmesi (sitedeki spor menüsü sırası)
BRANSLAR = [("Futbol", "fa-futbol", "futbol.html", "lig", "football"), ("Basketbol", "fa-basketball", "basketbol.html", "lig2", "basketball"),
            ("Voleybol", "fa-volleyball", "voleybol.html", "set", "volleyball"), ("Motor Sporları", "fa-flag-checkered", "motor-sporlari.html", "sampiyona", "motorsport"),
            ("Bisiklet", "fa-person-biking", "bisiklet.html", "klasman", "cycling"), ("Tenis", "fa-baseball", "tenis.html", "siralama", "tennis"),
            ("Atletizm", "fa-person-running", "atletizm.html", "kulup", "athletics"), ("Olimpiyatlar", "fa-medal", "olimpiyatlar.html", "madalya", "olympics"),
            ("E-Spor", "fa-gamepad", "e-spor.html", "harita", "esports")]
B_SAYFA = {b[0]: b[2] for b in BRANSLAR}
B_IKON = {b[0]: b[1] for b in BRANSLAR}

# puan tablosu biçimi: ad, ad sütunu başlığı, API'den gelen ham sütunlar, görünen sütunlar (başlık, anahtar, sınıf), düzeltme alanları
BICIM = {
    "lig": ("Lig Puanı · Beraberlikli", "Takım", "o g b m a y av p", [("O", "o", ""), ("G-B-M", "g-b-m", "kb-gizle-m"), ("AV", "av", ""), ("P", "p", "")],
            [("Galibiyet", "g"), ("Beraberlik", "b"), ("Mağlubiyet", "m"), ("Attığı Gol", "a"), ("Yediği Gol", "y"), ("Puan Düzeltmesi (Ceza, Hükmen)", "pd")]),
    "lig2": ("Lig Puanı · Beraberliksiz", "Takım", "o g m a y av p", [("O", "o", ""), ("G-M", "g-m", "kb-gizle-m"), ("AV", "av", ""), ("P", "p", "")],
             [("Galibiyet", "g"), ("Mağlubiyet", "m"), ("Attığı Sayı", "a"), ("Yediği Sayı", "y"), ("Puan Düzeltmesi (Ceza, Hükmen)", "pd")]),
    "set": ("Lig Puanı · Set Averajı", "Takım", "o g m as vs av p", [("O", "o", ""), ("G-M", "g-m", "kb-gizle-m"), ("Set AV", "av", ""), ("P", "p", "")],
            [("Galibiyet", "g"), ("Mağlubiyet", "m"), ("Aldığı Set", "as"), ("Verdiği Set", "vs"), ("Puan Düzeltmesi (Ceza, Hükmen)", "pd")]),
    "harita": ("Lig Puanı · Harita Averajı", "Takım", "o g m hk hv av p", [("O", "o", ""), ("G-M", "g-m", "kb-gizle-m"), ("Harita AV", "av", ""), ("P", "p", "")],
               [("Galibiyet", "g"), ("Mağlubiyet", "m"), ("Kazandığı Harita", "hk"), ("Kaybettiği Harita", "hv"), ("Puan Düzeltmesi (Ceza, Hükmen)", "pd")]),
    "sampiyona": ("Şampiyona · Galibiyet, Podyum, Pole", "Sürücü ya da Takım", "g pod pole p", [("G", "g", "kb-gizle-m"), ("Pod", "pod", ""), ("Pole", "pole", "kb-gizle-m"), ("P", "p", "")],
                  [("Galibiyet", "g"), ("Podyum", "pod"), ("Pole", "pole"), ("Puan", "p")]),
    "klasman": ("Genel Klasman · Yarış, Podyum", "Bisikletçi ya da Takım", "yr g pod p", [("Yarış", "yr", "kb-gizle-m"), ("G", "g", ""), ("Pod", "pod", "kb-gizle-m"), ("P", "p", "")],
                [("Yarış", "yr"), ("Galibiyet", "g"), ("Podyum", "pod"), ("Puan", "p")]),
    "siralama": ("Dünya Sıralaması · Puan", "Oyuncu", "yas tur deg p", [("Turnuva", "tur", "kb-gizle-m"), ("±", "deg", ""), ("Puan", "p", "")],
                 [("Turnuva", "tur"), ("Puan", "p")]),
    "kulup": ("Kulüpler Klasmanı · Erkek, Kadın", "Kulüp", "e k t", [("Erkek", "e", "kb-gizle-m"), ("Kadın", "k", "kb-gizle-m"), ("Toplam", "t", "")],
              [("Erkek Puanı", "e"), ("Kadın Puanı", "k")]),
    "madalya": ("Madalya Tablosu", "Ülke", "al gu br t", [("Al-Gü-Br", "al-gu-br", "kb-gizle-m"), ("Toplam", "t", "")],
                [("Altın", "al"), ("Gümüş", "gu"), ("Bronz", "br")]),
}
SAYI_RE = re.compile(r"^[+\-−–]?\d[\d.,]*$|^–$")


def tablo_coz(ham, k):
    """public sayfadaki puan tablosu metni: "sıra KOD Ad ... değer×k" art arda → [(sıra, kod, ad, [değerler])]"""
    t, out, i = ham.split(), [], 0
    while i < len(t):
        sira, kod, i, ad = t[i], t[i + 1], i + 2, []
        while not SAYI_RE.match(t[i]):
            ad.append(t[i]); i += 1
        out.append((sira, kod, " ".join(ad), t[i:i + k])); i += k
    return out


def tablo():
    ts = []
    for t in PT["takimlar"]:
        o = t["G"] + t["B"] + t["M"]
        ts.append(dict(t, O=o, AV=t["A"] - t["Y"], P=3 * t["G"] + t["B"]))
    ts.sort(key=lambda x: (-x["P"], -x["AV"], -x["A"]))
    return ts


# id, branş, ad, aşama, katılımcı, API'nin verdiği tablo (public sayfadan)
LIG_HAM = [
    ("tff1", "Futbol", "1. Lig", "2026-27 · 13. hafta", "20 takım", "1 BOD Bodrum FK 13 8 3 2 22 11 +11 27 2 ERZ Erzurumspor 13 8 2 3 24 13 +11 26 3 SAK Sakaryaspor 13 7 4 2 20 12 +8 25 4 BAN Bandırmaspor 13 7 3 3 19 14 +5 24 5 PEN Pendikspor 13 6 4 3 18 14 +4 22 6 IĞD Iğdır FK 13 6 3 4 17 15 +2 21"),
    ("premier", "Futbol", "Premier Lig", "2026-27 · 13. hafta", "20 takım", "1 ARS Arsenal 13 9 3 1 27 9 +18 30 2 MCI Manchester City 13 9 0 4 28 15 +13 27 3 LIV Liverpool 13 8 2 3 25 15 +10 26 4 CHE Chelsea 13 7 4 2 24 13 +11 25 5 AVL Aston Villa 13 7 2 4 19 16 +3 23 6 NEW Newcastle 13 6 4 3 21 14 +7 22 7 TOT Tottenham 13 6 3 4 22 18 +4 21 8 MUN Manchester United 13 6 2 5 20 19 +1 20 9 BHA Brighton 13 5 4 4 19 18 +1 19 10 NFO Nottingham Forest 13 5 3 5 16 17 -1 18 11 FUL Fulham 13 4 5 4 17 18 -1 17 12 BRE Brentford 13 4 4 5 18 20 -2 16"),
    ("bsl", "Basketbol", "Basketbol Süper Ligi", "2026-27 · 9. hafta", "16 takım", "1 FBB Fenerbahçe Beko 9 8 1 812 701 +111 17 2 AEF Anadolu Efes 9 7 2 798 712 +86 16 3 BJK Beşiktaş 9 6 3 765 718 +47 15 4 TTK Türk Telekom 9 6 3 741 709 +32 15 5 BAH Bahçeşehir Koleji 9 5 4 735 724 +11 14 6 GS Galatasaray 9 5 4 720 717 +3 14 7 TOF Tofaş 9 5 4 728 730 -2 14 8 KSK Karşıyaka 9 4 5 702 711 -9 13 9 MAN Manisa Basket 9 4 5 698 715 -17 13 10 TS Trabzonspor 9 3 6 690 728 -38 12 11 MRS Mersinspor 9 3 6 684 731 -47 12 12 BÜY Büyükçekmece 9 2 7 671 744 -73 11"),
    ("euroleague", "Basketbol", "EuroLeague", "2026-27 · 13. hafta", "20 takım", "1 FBB Fenerbahçe Beko 13 10 3 1087 1045 +42 23 2 RMD Real Madrid 13 10 3 1087 1045 +42 23 3 OLY Olympiakos 13 9 4 1081 1051 +30 22 4 AEF Anadolu Efes 13 8 5 1075 1057 +18 21 5 PAO Panathinaikos 13 8 5 1075 1057 +18 21 6 ASM Monaco 13 7 6 1069 1063 +6 20"),
    ("kbsl", "Basketbol", "Kadınlar Basketbol Süper Ligi", "2026-27 · 8. hafta", "14 takım", "1 FBO Fenerbahçe Opet 8 8 0 680 632 +48 16 2 MER ÇBK Mersin 8 7 1 674 638 +36 15 3 GS Galatasaray 8 6 2 668 644 +24 14 4 BJK Beşiktaş 8 5 3 662 650 +12 13 5 EML Emlak Konut 8 4 4 656 656 +0 12 6 NES Nesibe Aydın 8 3 5 650 662 -12 11"),
    ("sultanlar", "Voleybol", "Sultanlar Ligi", "2026-27 · 8. hafta sürüyor", "14 takım", "1 VKF VakıfBank 7 7 0 21 4 +17 20 2 ECZ Eczacıbaşı 7 6 1 19 6 +13 18 3 FEN Fenerbahçe Medicana 7 6 1 18 7 +11 17 4 THY Türk Hava Yolları 7 5 2 16 9 +7 15 5 GS Galatasaray Daikin 7 4 3 14 12 +2 12 6 ARS Aras Kargo 7 4 3 13 12 +1 11 7 NİL Nilüfer Belediyespor 7 3 4 12 14 -2 9 8 BJK Beşiktaş 7 3 4 11 14 -3 9 9 KZB Kuzeyboru 7 2 5 10 16 -6 7 10 GÖZ Göztepe 7 2 5 9 17 -8 6 11 BHÇ Bahçelievler 7 1 6 7 19 -12 4 12 İLB İlbank 7 1 6 6 19 -13 3"),
    ("efeler", "Voleybol", "Efeler Ligi", "2026-27 · 8. hafta", "14 takım", "1 HAL Halkbank 7 6 1 19 6 +13 18 2 ZRT Ziraat Bankkart 7 6 1 18 7 +11 17 3 ARK Arkas Spor 7 5 2 16 9 +7 15 4 FB Fenerbahçe 7 4 3 14 11 +3 12 5 GS Galatasaray 7 4 3 13 12 +1 11 6 TOT Spor Toto 7 3 4 12 13 -1 9"),
    ("cev", "Voleybol", "CEV Kadınlar Şampiyonlar Ligi", "Grup aşaması · 2. maç", "6 takım", "1 VKF VakıfBank 2 2 0 6 1 +5 6 2 CON Conegliano 2 2 0 6 2 +4 6 3 FEN Fenerbahçe Medicana 2 2 0 6 2 +4 5 4 ECZ Eczacıbaşı 2 1 1 4 3 +1 3 5 MIL Milano 2 1 1 3 4 -1 3 6 LOD Łódź 2 0 2 1 6 -5 0"),
    ("f1", "Motor Sporları", "Formula 1 · Sürücüler", "2026 · 22/24 yarış", "20 sürücü", "1 MCL Lando Norris 7 15 6 382 2 MCL Oscar Piastri 6 14 5 364 3 RBR Max Verstappen 5 13 7 349 4 FER Charles Leclerc 2 9 3 251 5 MER George Russell 2 8 1 236 6 FER Lewis Hamilton 0 5 0 174 7 MER Kimi Antonelli 0 3 0 128 8 WIL Carlos Sainz 0 2 0 86 9 AMR Fernando Alonso 0 1 0 64 10 RBR Isack Hadjar 0 0 0 52 11 WIL Alexander Albon 0 0 0 47 12 ALP Pierre Gasly 0 0 0 38"),
    ("f1t", "Motor Sporları", "Formula 1 · Takımlar", "2026 · 22/24 yarış", "10 takım", "1 MCL McLaren 13 29 11 746 2 FER Ferrari 2 14 3 425 3 RBR Red Bull 5 13 7 401 4 MER Mercedes 2 11 1 364 5 WIL Williams 0 2 0 133 6 AMR Aston Martin 0 1 0 98"),
    ("motogp", "Motor Sporları", "MotoGP · Sürücüler", "2026 · sezon tamamlandı", "22 sürücü", "1 DUC Marc Márquez 11 18 9 545 2 GRE Álex Márquez 2 12 1 467 3 APR Marco Bezzecchi 2 7 3 312 4 DUC Francesco Bagnaia 2 8 2 288 5 KTM Pedro Acosta 0 5 0 265 6 VR4 Fabio Di Giannantonio 0 3 0 221"),
    ("uci", "Bisiklet", "UCI Dünya Turu · Bireysel", "2026 · sezon tamamlandı", "İlk 12 bisikletçi", "1 UAE Tadej Pogačar 62 19 31 11.680 2 TVL Jonas Vingegaard 58 8 19 6.845 3 RBH Remco Evenepoel 55 9 18 6.410 4 ADC Mathieu van der Poel 48 7 15 4.920 5 LTK Mads Pedersen 64 9 21 4.655 6 UAE João Almeida 50 5 14 4.380 7 RBH Primož Roglič 41 3 10 3.810 8 LTK Juan Ayuso 46 4 12 3.540 9 Q36 Tom Pidcock 52 3 11 3.215 10 EFE Ben Healy 57 2 8 2.960 11 RBH Florian Lipowitz 44 1 7 2.705 12 UAE Isaac del Toro 60 3 13 2.590"),
    ("ucit", "Bisiklet", "UCI Dünya Turu · Takımlar", "2026 · sezon tamamlandı", "18 takım", "1 UAE UAE Team Emirates 236 74 121 29.840 2 TVL Visma 228 31 88 18.910 3 RBH Red Bull-Bora 231 28 79 17.560 4 LTK Lidl-Trek 240 26 82 15.220 5 ADC Alpecin 219 22 61 12.300 6 SQS Soudal Quick-Step 225 19 57 11.050"),
    ("ucik", "Bisiklet", "UCI Kadınlar Dünya Turu", "2026 · sezon tamamlandı", "İlk 6 bisikletçi", "1 FDJ Demi Vollering 48 11 22 4.210 2 SDW Lotte Kopecky 52 9 20 3.880 3 TVL Pauline Ferrand-Prévot 36 7 12 3.150 4 UAE Elisa Longo Borghini 45 6 14 2.960 5 TVL Marianne Vos 41 5 13 2.540 6 CSR Katarzyna Niewiadoma 47 2 11 2.210"),
    ("atp", "Tenis", "ATP Dünya Sıralaması", "23.11.2026 · haftalık", "İlk 12 oyuncu", "1 ITA Jannik Sinner 25 18 – 11.250 2 ESP Carlos Alcaraz 23 19 – 10.870 3 GER Alexander Zverev 29 22 – 6.430 4 USA Taylor Fritz 29 21 +1 5.120 5 GBR Jack Draper 24 20 -1 4.880 6 SRB Novak Djokovic 39 14 – 4.630 7 USA Ben Shelton 24 22 +2 4.310 8 AUS Alex de Minaur 27 24 – 4.120 9 ITA Lorenzo Musetti 24 23 -2 3.980 10 CZE Jakub Menšík 21 22 +3 3.640 11 DEN Holger Rune 23 21 – 3.350 12 BRA João Fonseca 20 23 +4 3.120"),
    ("wta", "Tenis", "WTA Dünya Sıralaması", "23.11.2026 · haftalık", "İlk 6 oyuncu", "1 BLR Aryna Sabalenka 28 19 – 10.420 2 POL Iga Świątek 25 20 – 8.395 3 USA Coco Gauff 22 21 +1 6.880 4 USA Amanda Anisimova 25 20 -1 6.210 5 KAZ Elena Rybakina 27 19 +2 5.640 6 USA Jessica Pegula 32 22 – 5.120"),
    ("atptr", "Tenis", "ATP · Türk oyuncular", "23.11.2026 · haftalık", "6 oyuncu", "146 TÜR Kaan Yurtsever 24 26 +12 612 183 TÜR Berk Aydoğan 27 28 -8 498 239 TÜR Emre Çınar 22 24 +5 356 311 TÜR Mert Kaya 25 25 +21 271 398 TÜR Onur Saraç 29 27 -3 214 452 TÜR Ali Doğru 20 22 +34 168"),
    ("asl", "Atletizm", "Atletizm Süper Ligi · Kulüpler", "2026 · sezon tamamlandı", "12 kulüp", "1 FB Fenerbahçe 238 226 464 2 ENK Enkaspor 231 232 463 3 GS Galatasaray 205 198 403 4 BJK Beşiktaş 188 176 364 5 İBB İstanbul BB 172 180 352 6 BBS Bursa Büyükşehir 160 151 311 7 KĞT Kocaeli Kağıtspor 148 139 287 8 ASK Ankara ASKİ 141 130 271 9 ALK ALKAŞ 133 122 255 10 MBB Mersin BB 120 114 234 11 SBB Sakarya BB 112 101 213 12 GBB Gaziantep BB 98 92 190"),
    ("paris", "Olimpiyatlar", "Paris 2024 · Madalya tablosu", "Tamamlandı", "İlk 11 ülke ve Türkiye", "1 USA ABD 40 44 42 126 2 CHN Çin 40 27 24 91 3 JPN Japonya 20 12 13 45 4 AUS Avustralya 18 19 16 53 5 FRA Fransa 16 26 22 64 6 NED Hollanda 15 7 12 34 7 GBR Büyük Britanya 14 22 29 65 8 KOR Güney Kore 13 9 10 32 9 ITA İtalya 12 13 15 40 10 GER Almanya 12 13 8 33 11 NZL Yeni Zelanda 10 7 3 20 64 TÜR Türkiye 0 3 5 8"),
    ("milano", "Olimpiyatlar", "Milano Cortina 2026 · Madalya tablosu", "Tamamlandı", "İlk 6 ülke", "1 NOR Norveç 16 8 13 37 2 GER Almanya 11 9 8 28 3 USA ABD 10 11 9 30 4 ITA İtalya 9 8 11 28 5 NED Hollanda 8 6 4 18 6 SWE İsveç 7 6 5 18"),
    ("dakar", "Olimpiyatlar", "Dakar 2026 Gençlik Olimpiyatları", "Tamamlandı", "İlk 6 ülke", "1 CHN Çin 14 9 7 30 2 JPN Japonya 10 8 9 27 3 ITA İtalya 8 7 10 25 4 FRA Fransa 7 9 6 22 5 TÜR Türkiye 5 4 8 17 6 EGY Mısır 4 6 5 15"),
    ("valorant", "E-Spor", "Valorant Türkiye Ligi", "2026 · final oynanıyor", "12 takım", "1 FUT FUT Esports 11 10 1 21 5 +16 30 2 BBL BBL Esports 11 9 2 19 7 +12 27 3 GAL Galakticos 11 8 3 17 9 +8 24 4 BJK Beşiktaş Esports 11 7 4 15 10 +5 21 5 SUP Papara SuperMassive 11 6 5 14 12 +2 18 6 FFX Fire Flux 11 6 5 13 12 +1 18 7 AUR Aurora 11 5 6 12 13 -1 15 8 DP Dark Passage 11 5 6 11 14 -3 15 9 MIS Misa Esports 11 4 7 10 15 -5 12 10 RGC Regnum Carya 11 3 8 8 17 -9 9 11 SNG Sangal 11 2 9 7 19 -12 6 12 IW Istanbul Wildcats 11 1 10 4 21 -17 3"),
    ("lol", "E-Spor", "LoL Şampiyonluk Ligi", "2026 · kış sezonu", "6 takım", "1 SUP Papara SuperMassive 12 10 2 21 7 +14 30 2 DP Dark Passage 12 9 3 19 9 +10 27 3 BJK Beşiktaş Esports 12 8 4 17 11 +6 24 4 GAL Galakticos 12 6 6 14 14 +0 18 5 FUT FUT Esports 12 5 7 12 15 -3 15 6 MIS Misa Esports 12 3 9 8 19 -11 9"),
    ("cs2", "E-Spor", "CS2 Türkiye Ligi", "2026 · 10. hafta", "6 takım", "1 EF Eternal Fire 10 9 1 19 5 +14 27 2 FUT FUT Esports 10 7 3 15 9 +6 21 3 BBL BBL Esports 10 6 4 13 10 +3 18 4 GAL Galakticos 10 5 5 11 11 +0 15 5 SNG Sangal 10 3 7 8 15 -7 9 6 IW Istanbul Wildcats 10 0 10 2 20 -18 0"),
]


def ligler():
    """[{id, brans, ad, asama, katilim, bicim, satirlar:[(sıra, kod, ad, {anahtar: değer}, not)]}]; Süper Lig sözlükten hesaplanır"""
    bic = {b[0]: b[3] for b in BRANSLAR}
    sl = []
    for n, t in enumerate(tablo(), 1):
        d = {"o": t["O"], "g": t["G"], "b": t["B"], "m": t["M"], "a": t["A"], "y": t["Y"], "av": ("+" if t["AV"] > 0 else "") + str(t["AV"]), "p": t["P"]}
        sl.append((str(n), t["kod"], t["ad"], {k: str(v) for k, v in d.items()}, "Elle düzeltildi · 22.11.2026 18.40 · Burak Tan" if t["kod"] == "GFK" else ""))
    out = [dict(id="superlig", brans="Futbol", ad=PT["lig"], asama=f"2026-27 · {PT['oynanan_hafta'] + 1}. hafta sürüyor", katilim=f"{len(sl)} takım", bicim="lig", satirlar=sl, elle=1)]
    for lid, br, ad, asama, kat, ham in LIG_HAM:
        anah = BICIM[bic[br]][2].split()
        rows = [(s, k, a, dict(zip(anah, v)), "") for s, k, a, v in tablo_coz(ham, len(anah))]
        out.append(dict(id=lid, brans=br, ad=ad, asama=asama, katilim=kat, bicim=bic[br], satirlar=rows, elle=0))
    return out


# kulüpler: (ad, kod, renk, şehir, lig, branş); Süper Lig sözlükten
KULUP_EK = [
    ("Atlético Madrid", "ATM", "#CB3524", "Madrid", "UEFA Şampiyonlar Ligi", "Futbol"), ("Liverpool", "LIV", "#C8102E", "Liverpool", "Premier Lig", "Futbol"),
    ("Chelsea", "CHE", "#034694", "Londra", "Premier Lig", "Futbol"),
    ("Fenerbahçe Beko", "FBB", "#0B1F4B", "İstanbul", "Basketbol Süper Ligi", "Basketbol"), ("Anadolu Efes", "AEF", "#002F6C", "İstanbul", "Basketbol Süper Ligi", "Basketbol"),
    ("Türk Telekom", "TTK", "#00A3E0", "Ankara", "Basketbol Süper Ligi", "Basketbol"), ("Bahçeşehir Koleji", "BAH", "#1D3E8F", "İstanbul", "Basketbol Süper Ligi", "Basketbol"),
    ("Tofaş", "TOF", "#005DAA", "Bursa", "Basketbol Süper Ligi", "Basketbol"), ("Fenerbahçe Opet", "FBO", "#0B1F4B", "İstanbul", "Kadınlar Basketbol Süper Ligi", "Basketbol"),
    ("ÇBK Mersin", "MER", "#E30613", "Mersin", "Kadınlar Basketbol Süper Ligi", "Basketbol"),
    ("Fenerbahçe Medicana", "FEN", "#0B1F4B", "İstanbul", "Sultanlar Ligi", "Voleybol"), ("VakıfBank", "VKF", "#B8860B", "İstanbul", "Sultanlar Ligi", "Voleybol"),
    ("Eczacıbaşı Dynavit", "ECZ", "#E30613", "İstanbul", "Sultanlar Ligi", "Voleybol"), ("Türk Hava Yolları", "THY", "#C8102E", "İstanbul", "Sultanlar Ligi", "Voleybol"),
    ("Halkbank", "HAL", "#0C8C4C", "Ankara", "Efeler Ligi", "Voleybol"), ("Ziraat Bankkart", "ZRT", "#00843D", "Ankara", "Efeler Ligi", "Voleybol"),
    ("Arkas Spor", "ARK", "#1C3F94", "İzmir", "Efeler Ligi", "Voleybol"),
    ("McLaren", "MCL", "#FF8000", "Woking", "Formula 1", "Motor Sporları"), ("Ferrari", "FER", "#DC0000", "Maranello", "Formula 1", "Motor Sporları"),
    ("Red Bull Racing", "RBR", "#1E41FF", "Milton Keynes", "Formula 1", "Motor Sporları"), ("Mercedes", "MER", "#00A19C", "Brackley", "Formula 1", "Motor Sporları"),
    ("Ducati Lenovo", "DUC", "#C8102E", "Bologna", "MotoGP", "Motor Sporları"),
    ("UAE Team Emirates", "UAE", "#1C1C1C", "BAE", "UCI Dünya Turu", "Bisiklet"), ("Visma", "TVL", "#E5B700", "Hollanda", "UCI Dünya Turu", "Bisiklet"),
    ("Red Bull-Bora", "RBH", "#1E1E50", "Almanya", "UCI Dünya Turu", "Bisiklet"), ("Lidl-Trek", "LTK", "#E2001A", "ABD", "UCI Dünya Turu", "Bisiklet"),
    ("Enkaspor", "ENK", "#E30A17", "İstanbul", "Atletizm Süper Ligi", "Atletizm"), ("İstanbul BB", "İBB", "#0055A5", "İstanbul", "Atletizm Süper Ligi", "Atletizm"),
    ("Bursa Büyükşehir", "BBS", "#00843D", "Bursa", "Atletizm Süper Ligi", "Atletizm"), ("Kocaeli Kağıtspor", "KĞT", "#1F7A3D", "Kocaeli", "Atletizm Süper Ligi", "Atletizm"),
    ("FUT Esports", "FUT", "#E4002B", "İstanbul", "Valorant Türkiye Ligi", "E-Spor"), ("BBL Esports", "BBL", "#5B2C8F", "İstanbul", "Valorant Türkiye Ligi", "E-Spor"),
    ("Galakticos", "GAL", "#00A3E0", "İstanbul", "Valorant Türkiye Ligi", "E-Spor"), ("Beşiktaş Esports", "BJK", "#1A1A1A", "İstanbul", "Valorant Türkiye Ligi", "E-Spor"),
    ("Eternal Fire", "EF", "#F05A28", "İstanbul", "CS2 Türkiye Ligi", "E-Spor"), ("Papara SuperMassive", "SUP", "#0D3B66", "İstanbul", "LoL Şampiyonluk Ligi", "E-Spor"),
]


def kulupler():
    k = [(t["ad"], t["kod"], t["renk"], SEHIR.get(t["kod"], ""), "Süper Lig", "Futbol") for t in PT["takimlar"]]
    return k + KULUP_EK


def haber_say(ad):
    return sum(1 for h in soz["haberler"] if ad in h["baslik"])


def kulup_satir(ad, kod, renk, sehir, lig, brans, cop=False):
    kid = TR_SLUG(ad)
    hs = haber_say(ad) if brans == "Futbol" else 0
    alt = ALT.get(ad) or ("Süper Lig" if lig == "Süper Lig" else "Avrupa Ligleri" if brans == "Futbol" and lig != "1. Lig" else brans)
    etiket = f'<span class="kb-kat"><b>Spor</b>{I("fa-chevron-right")}{e(alt)}</span>'
    durum = ("elle", "info", "Elle düzeltildi") if kod == "GFK" else ("genel", "wait", "Etiket genel") if alt in ("Süper Lig", "Futbol") else ("eslesti", "ok", "API eşleşti")
    kul = f"Spor › {alt} konusuyla eşleşik; {hs} haberde geçiyor. Kulüp silinince haberler etkilenmez, puan tablosunda API adı görünür" if hs else ""
    dur = 'cop" data-onceki="' + durum[0] if cop else durum[0]
    site = SLUG.get(ad) or (B_SAYFA[brans] if brans != "Futbol" else "takimlar.html")
    return (f'<tr data-satir="kl-{kid}-{TR_SLUG(brans)}" data-durum="{dur}" data-brans="{e(brans)}" data-lig="{e(lig)}" data-ara="{e(ad + " " + kod + " " + sehir + " " + lig + " " + brans)}" data-baslik="{e(ad)}" data-href="kulup.html?id={kid}"{f" data-kullanim=\"{e(kul)}\"" if kul else ""}>'
            f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(ad)}"></td>'
            f'<td class="kb-ana"><div class="rcp-cell"><span class="kb-ava">{e(kod)}</span><div class="rcp-id"><div class="rcp-name">{e(ad)}</div><div class="rcp-by">{e(lig)} · {e(sehir)}</div></div></div></td>'
            f'<td class="kb-gizle-m"><span class="kb-renk is-ozel" title="Kurumsal renk {renk}"><span style="--kat:{renk}"></span><span class="sr-only">Kurumsal renk {renk}</span></span></td>'
            f'<td class="kb-gizle-t">{etiket}</td>'
            f'<td class="say kb-gizle-t">{sayi(hs)}</td>'
            f'<td><span class="pstat {durum[1]}">{durum[2]}</span></td>'
            f'<td>{row_acts(("href", SITE + site), ("href", f"kulup.html?id={kid}", "ozel-dikeyler.kulup"), "sil", gor_ad="Sitede Görüntüle")}</td></tr>')


def lig_satir(L):
    bas, _, _, kol, _ = BICIM[L["bicim"]]
    lider = L["satirlar"][0]
    pk = kol[-1][1]
    kaynak = ("info", f'{L["elle"]} elle düzeltme') if L["elle"] else ("ok", "API")
    return (f'<tr data-satir="lg-{L["id"]}" data-durum="{"elle" if L["elle"] else "api"}" data-brans="{e(L["brans"])}" data-ara="{e(L["ad"] + " " + L["brans"] + " " + lider[2])}" data-baslik="{e(L["ad"])}">'
            f'<td class="kb-ana"><div class="rcp-cell">{lig_isaret(L)}<div class="rcp-id"><div class="rcp-name">{e(L["ad"])}</div><div class="rcp-by">{e(L["brans"])} · {e(L["asama"])}</div></div></div></td>'
            f'<td class="kb-gizle-t">{e(L["katilim"])}</td>'
            f'<td class="kb-gizle-m">{e(lider[2])} · <b>{e(lider[3][pk])}</b></td>'
            f'<td><span class="pstat {kaynak[0]}" title="Spor veri API · son güncelleme 15.57">{kaynak[1]}</span></td>'
            f'<td>{row_acts(("tanim", "lgGor-" + L["id"]), ("tanim", "lgDuz-" + L["id"]), None, gor_ad="Puan Durumu", duz_ad="Logoyu Düzenle")}</td></tr>')


def lig_isaret(L, buyuk=False):
    """lig logosu yüklenmişse o, yoksa branş ikonu (yedek)"""
    k = "k-lg" if buyuk else "k-sm"
    if L.get("logo"):
        return f'<span class="kb-ava {k}" style="background-image:url({L["logo"]})" role="img" aria-label="{e(L["ad"])} logosu"></span>'
    return f'<span class="kb-ava {k}" title="Lig logosu yok; branş ikonu gösteriliyor">{I(B_IKON[L["brans"]])}</span>'


def lig_sablonlar(L):
    _, ad_bas, _, kol, dz = BICIM[L["bicim"]]
    bas = "".join(f'<th class="say {c}">{h}</th>' for h, _, c in kol)
    sat = []
    for sira, kod, ad, d, not_ in L["satirlar"]:
        d = dict(d, **{k: "-".join(d[x] for x in k.split("-")) for _, k, _ in kol if "-" in k})
        api = " · ".join(f"{h} {d[k]}" for h, k, _ in kol)
        deg = "".join(f' data-deger-{k}="{e(d.get(k, "0"))}"' for _, k in dz)
        duz = (f'<button type="button" class="ia-btn" data-sablon-ac="lgDz-{L["id"]}" data-baslik-yaz="{e(ad)} · Düzelt" data-deger-api="{e(sira + ". sıra · " + api)}"{deg} aria-label="{e(ad)}: Düzelt" title="Düzelt">{I("fa-pen")}</button>')
        hc = "".join(f'<td class="say {c}">{"<b>" + e(d[k]) + "</b>" if k == kol[-1][1] else e(d[k])}</td>' for _, k, c in kol)
        alt = f'<div class="rcp-by">{e(kod)}{" · " + e(not_) if not_ else ""}</div>'
        sat.append(f'<tr><td class="say">{e(sira)}</td><td class="kb-ana"><div class="rcp-id"><div class="rcp-name">{e(ad)}</div>{alt}</div></td>{hc}<td><div class="row-acts">{duz}</div></td></tr>')
    eksik = f' API bu tablo için {e(L["katilim"][0].lower() + L["katilim"][1:])} veriyor; tam tablo sitede.' if L["katilim"].startswith("İlk") else ""
    alanlar = "".join(f'<div class="frow"><label for="lgDz{L["id"]}-{k}">{h}</label><input class="finput" id="lgDz{L["id"]}-{k}" data-alan="{k}" inputmode="numeric"></div>' for h, k in dz)
    return f"""<template id="lgGor-{L['id']}" data-baslik="{e(L['ad'])} · Puan Durumu" data-alt="{e(L['brans'])} · {e(L['asama'])}">
  <div class="kb-fs">
    <div class="kb-bant bilgi">{I("fa-lock")}<span><b>Spor veri API · son güncelleme 15.57; silinmez.</b> Yanlış değer “Düzelt” ile elle düzeltilir; gerekçe zorunlu, düzeltme denetim izine önceki ve sonraki haliyle yazılır.{eksik}</span></div>
    <div class="ptable-wrap"><table class="ptable">
      <thead><tr><th class="say">#</th><th class="kb-ana">{ad_bas}</th>{bas}<th aria-label="İşlemler"></th></tr></thead>
      <tbody>{"".join(sat)}</tbody>
    </table></div>
  </div>
  <div class="kb-kap-alt-cubuk"><a class="btn btn-ghost btn-sm" href="{SITE}{B_SAYFA[L['brans']]}" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Sitede Görüntüle</a></div>
</template>
<template id="lgDz-{L['id']}" data-baslik="{e(L['ad'])} · Düzelt" data-alt="Elle düzeltme · gerekçe zorunlu" data-zorunlu-kayit="ozel-dikeyler.duzeltme">
  <div class="kb-fs">
    <div class="kb-bant bilgi">{I("fa-circle-info")}<span><b>API'deki değer:</b> <span data-alan="api"></span>. Düzeltme denetim izine önceki ve sonraki haliyle yazılır.</span></div>
    <div class="form-grid kb-iki-sutun">{alanlar}</div>
    <div class="frow"><label for="lgDz{L['id']}-ger">Gerekçe</label>
      <textarea class="ftext" id="lgDz{L['id']}-ger" rows="3" data-alan-id="gerekce" data-sayac="200|280" data-zorunlu-metin="Düzeltmenin gerekçesini yazın" placeholder="ör. API son hafta maçının sonucunu yanlış işledi; federasyonun resmî maç raporu esas alındı"></textarea>
      <div class="char-meter"><span>Denetim izinde ve düzeltme geçmişinde görünür</span><b>0 / 200</b></div>
      <div class="ferr">{I("fa-circle-exclamation")}Düzeltmenin gerekçesini yazın.</div></div>
    <div class="toggle-row"><span>Düzeltmeyi Koru<small>Açıkken API güncellemesi bu düzeltmenin üstüne yazmaz; kapalıysa sonraki güncelleme siler</small></span><label class="toggle"><input type="checkbox" checked aria-label="Düzeltmeyi koru"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
  <div class="kb-kap-alt-cubuk">
    <button type="button" class="btn btn-ghost btn-sm kb-sol" data-sablon-ac="lgGor-{L['id']}">{I("fa-arrow-left")}Puan Durumuna Dön</button>
    <button type="button" class="btn btn-acc btn-sm" data-onay-baslik="Puan tablosu düzeltmesi yayımlansın mı?" data-onay-metin="Değişiklik sitede puan durumunda, branş sayfasında ve skor bandında hemen görünür; önceki ve sonraki hal denetim izine yazılır." data-onay-evet="Düzeltmeyi Yayımla" data-onay-ikon="fa-pen-to-square" data-sonra-durum="elle" data-sonra-durum-ad="Elle düzeltme" data-sonra-durum-sinif="info" data-sonra-kapat data-bildir-sonra="Puan tablosu düzeltildi; sitede güncellendi">{I("fa-check")}Düzeltmeyi Kaydet</button>
  </div>
</template>
<template id="lgDuz-{L['id']}" data-baslik="{e(L['ad'])} · Logo" data-alt="{e(L['brans'])} · lig kimliği">
  <div class="kb-fs">
    <div class="kb-bant bilgi">{I("fa-lock")}<span><b>Ad, aşama ve puan tablosu spor veri API'sinden gelir.</b> Burada yalnız lig logosu yönetilir; logo yoksa listede ve sitede {e(L['brans'].lower())} ikonu görünür.</span></div>
    {gorsel_alani("lig_logo", "Lig logosu", "Lig Logosu", "İsteğe bağlı · yoksa branş ikonu", lig_isaret(L, True),
                  ("Lig logosunu sürükleyin ya da seçin", "1:1 · şeffaf PNG ya da SVG, en az 96×96 · medya havuzuna girmez"),
                  [("web.detay", "Lig sayfası · 1:1", "r-1x1"), ("web.kart", "Puan durumu · 1:1", "r-1x1")], [("mobil.kart", "Mobil · 1:1", "r-1x1")],
                  "Önerilen: lig sayfası <b>96×96</b>, puan durumu ve maç satırı <b>28×28</b>.", "Önerilen: <b>24×24</b>.", cekmece=True)}
  </div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="lgGor-{L['id']}" data-bildir-sonra="Lig logosu kaydedildi; listede, puan durumunda ve sitede görünür">{I("fa-floppy-disk")}Kaydet</button></div>
</template>
"""


def M(mid, br, lig, ev, dep, skor, zaman, dur, not_, baslik=None):
    """maç ya da yarış; yarışta ev/dep yok, başlık ve sonuç (1. sıra) yazılır"""
    return dict(id=mid, br=br, lig=lig, ev=ev, dep=dep, skor=skor, zaman=zaman, dur=dur, not_=not_, baslik=baslik or f"{ev[0]} – {dep[0]}")


MACLAR = [
    M("gs-fb", "Futbol", "Süper Lig · 14. hafta", ("Galatasaray", "GS"), ("Fenerbahçe", "FB"), "2-1", "23.11.2026 14.30", "canli", "67'"),
    M("bod-sak", "Futbol", "1. Lig · 13. hafta", ("Bodrum FK", "BOD"), ("Sakaryaspor", "SAK"), "0-0", "23.11.2026 15.00", "canli", "54'"),
    M("aef-fbb", "Basketbol", "Basketbol Süper Ligi · 9. hafta", ("Anadolu Efes", "AEF"), ("Fenerbahçe Beko", "FBB"), "78-71", "23.11.2026 14.00", "canli", "4. çeyrek 6.12"),
    M("fen-thy", "Voleybol", "Sultanlar Ligi · 8. hafta", ("Fenerbahçe Medicana", "FEN"), ("Türk Hava Yolları", "THY"), "2-0", "23.11.2026 15.00", "canli", "3. set"),
    M("ralli", "Motor Sporları", "Türkiye Ralli Şampiyonası · Bodrum", None, None, "1. Kerem Yıldız", "23.11.2026 09.00", "canli", "ÖE 7/12", "Bodrum Rallisi · özel etaplar"),
    M("kalkan-er", "Bisiklet", "Pist · Türkiye Şampiyonası · erkekler sprint finali", ("Emre Kalkan", "KNY"), ("Batuhan Er", "BUR"), "1-0", "23.11.2026 15.40", "canli", "2. seri"),
    M("sin-cer", "Tenis", "Davis Kupası Finalleri · Çeyrek final", ("Jannik Sinner", "ITA"), ("Francisco Cerúndolo", "ARG"), "1-1", "23.11.2026 14.00", "canli", "3. set"),
    M("ates-pop", "Tenis", "ITF W35 · Antalya", ("Deniz Ateş", "TÜR"), ("Elena Popescu", "ROU"), "1-0", "23.11.2026 15.00", "canli", "2. set"),
    M("ayd-park", "Olimpiyatlar", "Taekwondo Grand Prix Finali · −67 kg", ("Elif Aydın", "TÜR"), ("Park Seo-yeon", "KOR"), "2-1", "23.11.2026 15.30", "canli", "2. raunt"),
    M("fut-bbl", "E-Spor", "Valorant Türkiye Ligi · Final", ("FUT Esports", "FUT"), ("BBL Esports", "BBL"), "1-1", "23.11.2026 14.00", "canli", "3. harita"),
    M("ts-bas", "Futbol", "Süper Lig · 14. hafta", ("Trabzonspor", "TS"), ("Başakşehir", "BAŞ"), "1-1", "23.11.2026 11.30", "bitti", "MS"),
    M("sam-goz", "Futbol", "Süper Lig · 14. hafta", ("Samsunspor", "SAM"), ("Göztepe", "GÖZ"), "2-0", "23.11.2026 11.30", "bitti", "MS"),
    M("bjk-ttk", "Basketbol", "Basketbol Süper Ligi · 9. hafta", ("Beşiktaş", "BJK"), ("Türk Telekom", "TTK"), "84-80", "23.11.2026 12.00", "elle", "MS"),
    M("fbo-mer", "Basketbol", "Kadınlar Basketbol Süper Ligi · 8. hafta", ("Fenerbahçe Opet", "FBO"), ("ÇBK Mersin", "MER"), "76-69", "23.11.2026 13.00", "bitti", "MS"),
    M("zrt-hal", "Voleybol", "Efeler Ligi · 8. hafta", ("Ziraat Bankkart", "ZRT"), ("Halkbank", "HAL"), "1-3", "23.11.2026 12.00", "bitti", "MS"),
    M("ark-gs", "Voleybol", "Efeler Ligi · 8. hafta", ("Arkas Spor", "ARK"), ("Galatasaray", "GS"), "3-2", "23.11.2026 13.30", "bitti", "MS"),
    M("f1-lv", "Motor Sporları", "Formula 1 · Las Vegas GP", None, None, "1. Lando Norris", "23.11.2026 07.00", "bitti", "MS", "Las Vegas GP · yarış"),
    M("motogp-val", "Motor Sporları", "MotoGP · Valensiya GP", None, None, "1. Marc Márquez", "16.11.2026 16.00", "bitti", "MS", "Valensiya GP · yarış"),
    M("dogan-aksoy", "Bisiklet", "Pist · Türkiye Şampiyonası · kadınlar sprint finali", ("Ece Doğan", "ANK"), ("Nehir Aksoy", "İZM"), "2-1", "23.11.2026 14.30", "bitti", "MS"),
    M("cx-elit", "Bisiklet", "Siklokros Dünya Kupası · 4. ayak", None, None, "1. Mathieu van der Poel", "22.11.2026 15.00", "bitti", "MS", "Siklokros · elit erkekler"),
    M("zve-dem", "Tenis", "Davis Kupası Finalleri · Çeyrek final", ("Alexander Zverev", "GER"), ("Alex de Minaur", "AUS"), "2-1", "23.11.2026 11.00", "bitti", "MS"),
    M("kros-koc", "Atletizm", "Türkiye Kros Ligi · 2. kademe", None, None, "1. Emre Yavuz", "22.11.2026 10.00", "bitti", "MS", "Kros Ligi Kocaeli · erkekler"),
    M("ant-yari", "Atletizm", "Antalya Yarı Maratonu", None, None, "1. Faith Chepkoech", "22.11.2026 09.00", "bitti", "MS", "Antalya Yarı Maratonu · kadınlar"),
    M("wang-mor", "Olimpiyatlar", "Masa Tenisi · WTT Finalleri", ("Wang Chuqin", "CHN"), ("Truls Möregårdh", "SWE"), "4-2", "23.11.2026 12.30", "bitti", "MS"),
    M("gal-bjk", "E-Spor", "Valorant Türkiye Ligi · Üçüncülük maçı", ("Galakticos", "GAL"), ("Beşiktaş Esports", "BJK"), "2-0", "23.11.2026 11.00", "bitti", "MS"),
    M("ef-mon", "E-Spor", "CS2 · Avrupa elemeleri", ("Eternal Fire", "EF"), ("Monte", "MON"), "2-1", "22.11.2026 19.00", "bitti", "MS"),
    M("vkf-ecz", "Voleybol", "Sultanlar Ligi · 8. hafta", ("VakıfBank", "VKF"), ("Eczacıbaşı Dynavit", "ECZ"), "–", "23.11.2026 20.00", "bekliyor", "Başlamadı"),
    M("sup-dp", "E-Spor", "LoL Şampiyonluk Ligi", ("Papara SuperMassive", "SUP"), ("Dark Passage", "DP"), "–", "23.11.2026 20.00", "bekliyor", "Başlamadı"),
    M("liv-che", "Futbol", "Premier Lig · 13. hafta", ("Liverpool", "LIV"), ("Chelsea", "CHE"), "–", "23.11.2026 23.00", "bekliyor", "Başlamadı"),
    M("yildiz-lee", "Olimpiyatlar", "Okçuluk · Salon Dünya Serisi", ("Ece Yıldız", "TÜR"), ("Lee Ji-won", "KOR"), "–", "23.11.2026 18.30", "bekliyor", "Başlamadı"),
    M("gs-atm", "Futbol", "UEFA Şampiyonlar Ligi · 5. hafta", ("Galatasaray", "GS"), ("Atlético Madrid", "ATM"), "–", "24.11.2026 20.45", "bekliyor", "Başlamadı"),
    M("ttk-ulm", "Basketbol", "EuroCup · 10. hafta", ("Türk Telekom", "TTK"), ("Ulm", "ULM"), "–", "24.11.2026 20.00", "bekliyor", "Başlamadı"),
    M("rmd-aef", "Basketbol", "EuroLeague · 14. hafta", ("Real Madrid", "RMD"), ("Anadolu Efes", "AEF"), "–", "26.11.2026 21.45", "bekliyor", "Başlamadı"),
    M("kay-goz", "Futbol", "Süper Lig · 15. hafta", ("Kayserispor", "KAY"), ("Göztepe", "GÖZ"), "–", "27.11.2026 20.00", "bekliyor", "Başlamadı"),
    M("f1-qat-s", "Motor Sporları", "Formula 1 · Katar GP", None, None, "–", "28.11.2026 20.00", "bekliyor", "Başlamadı", "Katar GP · sprint"),
    M("cx-hulst", "Bisiklet", "Siklokros Dünya Kupası · Hulst", None, None, "–", "28.11.2026 13.00", "bekliyor", "Başlamadı", "Hulst etabı · elit"),
    M("fb-ts", "Futbol", "Süper Lig · 15. hafta", ("Fenerbahçe", "FB"), ("Trabzonspor", "TS"), "–", "28.11.2026 20.00", "bekliyor", "Başlamadı"),
    M("kros-edi", "Atletizm", "Türkiye Kros Ligi · 3. kademe", None, None, "–", "29.11.2026 10.00", "bekliyor", "Başlamadı", "Kros Ligi Edirne"),
]
MAC_DURUM = {"canli": ("warm", "Canlı"), "bitti": ("off", "Bitti"), "bekliyor": ("wait", "Başlamadı"), "elle": ("info", "Elle düzeltildi")}


def mac_satir(m):
    sinif, dad = MAC_DURUM[m["dur"]]
    return (f'<tr data-satir="mc-{m["id"]}" data-durum="{m["dur"]}" data-brans="{e(m["br"])}" data-ara="{e(m["baslik"] + " " + m["lig"] + " " + m["br"] + " " + m["skor"])}" data-baslik="{e(m["baslik"])}">'
            f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name">{e(m["baslik"])}</div><div class="rcp-by">{e(m["br"])} · {e(m["lig"])}</div></div></td>'
            f'<td class="say"><b>{e(m["skor"])}</b></td><td class="kb-gizle-m">{e(m["not_"])}</td>'
            f'<td class="kb-gizle-t"><span class="kb-tarih">{e(tarih_kisa(m["zaman"]))}</span></td>'
            f'<td><span class="pstat {sinif}">{dad}</span></td>'
            f'<td>{row_acts(("tanim", "mcGor-" + m["id"]), ("tanim", "mcDz-" + m["id"]), None, duz_ad="Sonucu Düzelt" if not m["ev"] else "Skoru Düzelt")}</td></tr>')


def mac_sablonlar(m):
    mid, sinif, dad = m["id"], *MAC_DURUM[m["dur"]]
    yaris = not m["ev"]
    durumlar = [("bekliyor", "Başlamadı", ""), ("canli", "Canlı", ""), ("devre", "Devre Arası", ""), ("bitti", "Bitti", ""), ("ertelendi", "Ertelendi", ""), ("iptal", "İptal", "")]
    if yaris:
        s1, s2 = (m["skor"][3:] if m["skor"].startswith("1. ") else ""), ""
        a1, a2, im = "1. Sıra", "2. Sıra", ""
    else:
        s1, s2 = (m["skor"].split("-") + ["", ""])[:2] if "-" in m["skor"] else ("", "")
        a1, a2, im = m["ev"][0], m["dep"][0], ' inputmode="numeric"'
    sk_ad = "Sonuç" if yaris else "Skor"
    return f"""<template id="mcGor-{mid}" data-baslik="{e(m['baslik'])}" data-alt="{e(m['br'])} · {e(m['lig'])}">
  <div class="kb-fs"><div class="kb-fs-tt">{"Yarış" if yaris else "Maç"}</div><div class="sa-durum">
    <div><span>Durum</span><b><span class="pstat {sinif}">{dad}</span></b></div>
    <div><span>{sk_ad}</span><b>{e(m['skor'])}</b></div>
    <div><span>{"Aşama" if yaris else "Dakika / Periyot"}</span><b>{e(m['not_'])}</b></div>
    <div><span>Başlama</span><b>{e(m['zaman'])}</b></div>
    <div><span>Veri</span><b>Spor veri API · son güncelleme 15.57</b></div>
  </div></div>
  <div class="kb-fs"><div class="kb-fs-tt">Bağlantılar</div><p class="fhint">Sitede {e(m['br'])} sayfasında, maç merkezinde ve skor bandında görünür. Canlı anlatım ve haberler Haberler modülünden bağlanır.</p>
    <a class="kb-bag" href="{SITE}{"mac-detay.html" if m['br'] == "Futbol" else B_SAYFA[m['br']]}" target="_blank" rel="noopener">{"Maç detayını" if m['br'] == "Futbol" else e(m['br']) + " sayfasını"} sitede aç</a></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="mcDz-{mid}">{I("fa-pen-to-square")}{sk_ad}u Düzelt</button></div>
</template>
<template id="mcDz-{mid}" data-baslik="{e(m['baslik'])} · {sk_ad}u Düzelt" data-alt="Elle düzeltme · gerekçe zorunlu" data-zorunlu-kayit="ozel-dikeyler.duzeltme">
  <div class="kb-fs">
    <div class="form-grid kb-iki-sutun">
      <div class="frow"><label for="mcS1-{mid}">{e(a1)}</label><input class="finput" id="mcS1-{mid}"{im} value="{e(s1)}" placeholder="–"></div>
      <div class="frow"><label for="mcS2-{mid}">{e(a2)}</label><input class="finput" id="mcS2-{mid}"{im} value="{e(s2)}" placeholder="–"></div>
      <div class="frow"><span class="flabel">Durum</span>{secim("mcDur-" + mid, durumlar, deger="bitti" if m['dur'] == "elle" else m['dur'], bos="Durum seçin")}</div>
      <div class="frow"><label for="mcDk-{mid}">{"Aşama" if yaris else "Dakika ya da Periyot"}</label><input class="finput" id="mcDk-{mid}" value="{e(m['not_'])}"></div>
    </div>
    <div class="frow"><label for="mcGer-{mid}">Gerekçe</label>
      <textarea class="ftext" id="mcGer-{mid}" rows="3" data-alan-id="gerekce" data-sayac="200|280" data-zorunlu-metin="Düzeltmenin gerekçesini yazın" placeholder="ör. API son dakikadaki sayıyı işlemedi; yayın görüntüsü esas alındı">{"API son 3 dakikada skoru güncellemedi; maç sonu skoru resmî kaynaktan işlendi." if m['dur'] == "elle" else ""}</textarea>
      <div class="char-meter"><span>Denetim izinde ve düzeltme geçmişinde görünür</span><b>0 / 200</b></div>
      <div class="ferr">{I("fa-circle-exclamation")}Düzeltmenin gerekçesini yazın.</div></div>
    <div class="toggle-row"><span>Düzeltmeyi Koru<small>Açıkken API güncellemesi bu düzeltmenin üstüne yazmaz; karşılaşma bitene kadar açık kalması önerilmez</small></span><label class="toggle"><input type="checkbox"{" checked" if m['dur'] in ("bitti", "elle") else ""} aria-label="Düzeltmeyi koru"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-onay-baslik="{sk_ad} düzeltmesi yayımlansın mı?" data-onay-metin="{sk_ad} sitede maç merkezinde, skor bandında ve canlı anlatımda hemen değişir; önceki ve sonraki hal denetim izine yazılır." data-onay-evet="Düzeltmeyi Yayımla" data-onay-ikon="fa-pen-to-square" data-sonra-durum="elle" data-sonra-durum-ad="Elle düzeltildi" data-sonra-durum-sinif="info" data-sonra-kapat data-bildir-sonra="{sk_ad} düzeltildi; sitede güncellendi">{I("fa-check")}Düzeltmeyi Kaydet</button></div>
</template>
"""


IKONLAR = [("fa-futbol", "Futbol Topu"), ("fa-basketball", "Basketbol Topu"), ("fa-volleyball", "Voleybol Topu"), ("fa-flag-checkered", "Damalı Bayrak"),
           ("fa-person-biking", "Bisikletçi"), ("fa-baseball", "Tenis Topu"), ("fa-person-running", "Koşucu"), ("fa-medal", "Madalya"), ("fa-gamepad", "Oyun Kolu"),
           ("fa-person-swimming", "Yüzücü"), ("fa-hand-fist", "Yumruk"), ("fa-chess", "Satranç"), ("fa-trophy", "Kupa")]


def brans_sablonlar(say, alt_spor):
    satir = []
    for ad, ikon, sayfa, bic, api in BRANSLAR:
        k, l, m = say[ad]
        n = k + l + m
        dig = "|".join(b[0] for b in BRANSLAR if b[0] != ad)
        meta = f"{k} kulüp · {l} lig · {m} maç" if n else "Kayıt yok"
        deg = f'data-deger-ad="{e(ad)}" data-deger-alt-konu="{e(ad)}" data-deger-ikon="{ikon}" data-deger-bicim="{bic}" data-deger-api="{api}"'
        satir.append(
            f'<div class="kb-ozk-satir"><span class="kb-ozk-ikon">{I(ikon)}</span><div class="kb-ozk-yazi"><b>{e(ad)}</b><span>{meta}</span></div><div class="row-acts">'
            f'<a class="ia-btn" href="{SITE}{sayfa}" target="_blank" rel="noopener" aria-label="{e(ad)}: Sitede Görüntüle" title="Sitede Görüntüle">{I("fa-eye")}</a>'
            f'<button type="button" class="ia-btn" data-sablon-ac="spBransForm" data-baslik-yaz="{e(ad)} · Düzenle" {deg} aria-label="{e(ad)} düzenle" title="Düzenle">{I("fa-pen")}</button>'
            f'<button type="button" class="ia-btn danger" data-tasi-sil data-sonra-kaldir data-tasi-ad="{e(ad)}" data-tasi-sayi="{n}" data-tasi-birim="kayıt" data-tasi-birim-cogul="kayıtlar" data-tasi-ikon="fa-layer-group" '
            f'data-tasi-soru="{k} kulüp, {l} lig ve {m} maç hangi branşa taşınsın?" data-tasi-hedefler="{e(dig)}" '
            f'data-tasi-not="“{e(ad)}” çöpe gider ve oradan geri alınabilir; kulüp, lig ve maçlar seçilen branşa taşınır. Sitedeki Spor › {e(ad)} alt konusu ve haberleri silinmez; Haberler › Kategoriler’den yönetilir. İşlem denetim izine yazılır." '
            f'aria-label="{e(ad)} sil" title="Sil">{I("fa-trash")}</button></div></div>')
    ikon_ops = "".join(f'<button type="button" data-deger="{c}" data-ad="{a}">{I(c)}{a}<span class="ks-alt">{c[3:]}</span></button>' for c, a in IKONLAR)
    bic_ops = [(k, v[0], "") for k, v in BICIM.items()]
    api_ops = [(b[4], b[4], b[0]) for b in BRANSLAR]
    alt_ops = [(a, f"Spor › {a}", "") for a in alt_spor]
    return f"""<template id="spBranslar" data-baslik="Branşlar" data-alt="{len(BRANSLAR)} branş · sıra sitedeki spor menüsüyle aynı">
  <div class="kb-ozk">{"".join(satir)}</div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="spBransForm" data-baslik-yaz="Yeni Branş" data-deger-ad="" data-deger-alt-konu="" data-deger-ikon="" data-deger-bicim="" data-deger-api="">{I("fa-plus")}Yeni Branş</button></div>
</template>
<template id="spBransForm" data-baslik="Branş" data-alt="Spor · branş" data-zorunlu-kayit="ozel-dikeyler.brans">
  <div class="kb-form-bas kb-kap-dil">
    <div class="kb-dil" role="group" aria-label="İçerik dili">
      <button type="button" class="is-on" aria-pressed="true">TR · Türkçe</button>
      <button type="button" disabled title="Çeviri ekranları sonraki aşamada">EN<span class="kd-etk">Sonraki aşama</span></button>
      <button type="button" disabled title="Çeviri ekranları sonraki aşamada">AR<span class="kd-etk">Sonraki aşama</span></button>
      <button type="button" disabled title="Çeviri ekranları sonraki aşamada">DE<span class="kd-etk">Sonraki aşama</span></button>
    </div>
    <span class="kfb-not">{I("fa-language")}Dil seçici branş adını değiştirir; ikon, tablo biçimi ve API eşleşmesi bütün dillerde ortaktır.</span>
  </div>
  <div class="kb-fs"><div class="kb-fs-tt">Temel Bilgiler</div>
    <div class="frow"><label for="brAd">Ad</label><input class="finput" id="brAd" data-alan="ad" data-alan-id="ad" data-zorunlu-metin="Branşa ad verin" data-sayac="20|30" placeholder="ör. Hentbol"><div class="char-meter"><span>Spor sayfasında, süzgeçlerde ve sitedeki spor menüsünde</span><b>0 / 20</b></div></div>
    <div class="frow"><span class="flabel">Spor Alt Konusu</span>{secim("brAlt", alt_ops, bos="Alt konu seçin", ara="Alt konu ara", ek=' data-alan="alt-konu"')}<span class="fhint">Sitedeki branş sayfası, adresi ve SEO'su bu alt konudan gelir; yeni alt konu Haberler › Kategoriler'den eklenir.</span></div>
    <div class="frow"><span class="flabel">İkon</span><div class="kb-secim" data-alan="ikon" data-bos="İkon seçin"><button type="button" class="kb-secim-btn" data-acilir="brIkon" aria-expanded="false" aria-haspopup="listbox"><span class="ks-deger">İkon seçin</span>{I("fa-chevron-down")}</button><div class="pnl-menu kb-secim-menu" id="brIkon"><div class="kb-secim-ara">{I("fa-magnifying-glass")}<input type="search" placeholder="İkon ara" aria-label="İkon ara"></div><div class="kb-secim-liste" role="listbox">{ikon_ops}</div><div class="kb-secim-bos" hidden>Bu adla ikon yok.</div></div></div><span class="fhint">Görsel yüklenmemişse branş listesinde, maç satırlarında ve sitede çipte bu ikon görünür.</span></div>
    {gorsel_alani("brans_gorsel", "Branş görseli", "Branş Görseli", "İsteğe bağlı · yüklenirse ikonun yerine geçer", '<span class="kb-ava k-lg">' + I("fa-layer-group") + '</span>',
                  ("Branş görselini sürükleyin ya da seçin", "1:1 · şeffaf PNG ya da SVG, en az 64×64 · medya havuzuna girmez"),
                  [("web.kart", "Branş ikonu · 1:1", "r-1x1")], [("mobil.kart", "Mobil · 1:1", "r-1x1")],
                  "Önerilen: <b>24×24</b> (branş listesi, maç satırı, sitede çip).", "Önerilen: <b>24×24</b>.", cekmece=True)}
  </div>
  <div class="kb-fs"><div class="kb-fs-tt">Veri</div>
    <div class="frow"><span class="flabel">Puan Tablosu Biçimi</span>{secim("brBicim", bic_ops, bos="Biçim seçin", ek=' data-alan="bicim"')}<span class="fhint">Ligler sekmesinde ve sitede puan tablosunun sütunlarını belirler.</span></div>
    <div class="frow"><span class="flabel">Spor Veri API Eşleşmesi</span>{secim("brApi", api_ops, bos="API branşı seçin", ara="API branşı ara", ek=' data-alan="api"')}<span class="fhint">Kulüp, lig ve maç verisi bu eşleşmeyle çekilir; eşleşmesiz branşta veri elle girilir.</span></div>
    <div class="toggle-row"><span>Sitedeki Spor Menüsünde Göster<small>Kapalıysa branş sayfası açık kalır, yalnızca menüden çıkar</small></span><label class="toggle"><input type="checkbox" checked aria-label="Spor menüsünde göster"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
  <div class="kb-kap-alt-cubuk">
    <button type="button" class="btn btn-ghost btn-sm kb-sol" data-sablon-ac="spBranslar">{I("fa-arrow-left")}Branşlara Dön</button>
    <button type="button" class="btn btn-acc btn-sm" data-sablon-ac="spBranslar" data-bildir-sonra="Branş kaydedildi; değişiklik denetim izine yazıldı">{I("fa-floppy-disk")}Kaydet</button>
  </div>
</template>
"""


def sayfa_spor():
    LG = ligler()
    KL = kulupler()
    kl = [kulup_satir(*k) for k in KL]
    kl.append(kulup_satir("Pendikspor", "PEN", "#8B1E3F", "İstanbul", "1. Lig", "Futbol", cop=True))
    say = {b[0]: [sum(1 for k in KL if k[5] == b[0]), sum(1 for L in LG if L["brans"] == b[0]), sum(1 for m in MACLAR if m["br"] == b[0])] for b in BRANSLAR}
    toplam = sum(sum(v) for v in say.values())
    canli = sum(1 for m in MACLAR if m["dur"] == "canli")
    nav = (f'<button type="button" data-gez-suz="brans" data-v="">Bütün Branşlar<span>{toplam}</span></button><div class="kmg-tt">Branş</div>'
           + "".join(f'<button type="button" data-gez-suz="brans" data-v="{e(b[0])}" aria-pressed="false">{I(b[1])}{e(b[0])}<span>{sum(say[b[0]])}</span></button>' for b in BRANSLAR))
    kl_lig = []
    for k in KL:
        if (k[4], k[4], k[5]) not in kl_lig: kl_lig.append((k[4], k[4], k[5]))
    kl_ligler = [("", "Bütün Ligler", "")] + kl_lig
    alt = alt_konular()
    s = bas("Spor", "spor")
    s += f"""
<!-- SPOR (D4): soldaki branş listesi (Gez kalıbı) Kulüpler · Ligler ve puan durumu · Maç merkezi sekmelerini birlikte süzer.
     Branşlar sağ üstteki çekmecede yönetilir (ekle, düzenle, taşıyarak sil). Puan tabloları ve maçlar spor veri API'sinden gelir;
     silinmez, elle düzeltilir (çekmece, gerekçe zorunlu, denetim izi). Kulüp düzenle ayrı sayfa (kulup.html).
     Maç Merkezi'nin başında tek ortak "Maç Kapağı" (ozel-dikeyler.mac_kapak; Beyar 25.11.2026): bütün maç sayfalarının bannerı; maç başına alan yok. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Spor</h1>
      <div class="ph-sub">{len(BRANSLAR)} branş · {len(KL)} kulüp · {len(LG)} lig ve sıralama · {canli} canlı karşılaşma</div>
    </div>
    <div class="ph-actions">
      <button type="button" class="btn btn-ghost btn-sm" data-tanim="spBranslar" data-roller="super gyy">{I("fa-layer-group")}Branşlar</button>
      <a class="btn btn-ghost btn-sm" data-hedef="entegrasyonlar.ayar" data-hedef-ek="?id=spor" data-roller="super" href="../../cekirdek/entegrasyonlar/ayar.html?id=spor">{I("fa-plug")}Spor Veri API</a>
      <a class="btn btn-acc btn-sm" data-hedef="ozel-dikeyler.kulup" data-hedef-ek="?yeni=1" href="kulup.html?yeni=1">{I("fa-plus")}Yeni Kulüp</a>
    </div>
  </div>

  <div class="kb-bant tehlike dash-row">{I("fa-triangle-exclamation")}<span><b>Spor veri API 15.58'den beri yanıt vermiyor.</b> Sitedeki skor bandı ve maç merkezi son veriyi (15.57) gösteriyor. Canlı karşılaşmalarda sonucu gerekirse elle düzeltin; API dönünce düzeltilmemiş veriler kendiliğinden güncellenir.</span><a class="btn btn-ghost btn-sm kb-bant-eylem" data-hedef="entegrasyonlar.ayar" data-hedef-ek="?id=spor" data-roller="super" href="../../cekirdek/entegrasyonlar/ayar.html?id=spor">{I("fa-plug")}Bağlantı</a></div>

  <section class="pnl-card" id="spVeri" data-sekmeli aria-label="Spor verisi">
    <div class="kb-medya-gov">
      <nav class="kb-medya-gez kb-gez-sayfa" data-gez-kapsam="#spVeri" aria-label="Branşlar">{nav}</nav>
      <div>
    <div class="sa-form-tabs" role="tablist" aria-label="Spor sekmeleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="spKulup">{I("fa-shield-halved")}Kulüpler</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="spLig">{I("fa-list-ol")}Ligler ve Puan Durumu</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="spMac">{I("fa-stopwatch")}Maç Merkezi</button>
    </div>

    <!-- ===== KULÜPLER ===== -->
    <div class="sa-form-panel" id="spKulup" role="tabpanel">
      <div data-liste data-liste-ad="kulüp" data-sayfa-boy="50" data-liste-cop-not="Kulüp listelerden kalkar ve Çöp sekmesine taşınır">
        <div class="kb-liste-ust">
          <div class="chips" role="tablist" aria-label="Eşleşme durumu">
            <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="eslesti">API Eşleşti<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="genel">Etiket Genel<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="elle">Elle Düzeltilen<span class="ch-cnt">0</span></button>
          </div>
          <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
        </div>
        <div class="filter-bar">
          <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="klAra">Kulüplerde Ara</label><input id="klAra" type="search" data-liste-ara placeholder="Kulüp adı, kısa kod ya da şehir ara" autocomplete="off"></div>
          {secim("klSuzLig", kl_ligler, etk="Lig:", bos="Tümü", ara="Lig ara", suz="lig")}
          <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
        </div>
        <div class="kb-toplu" hidden>
          <b data-secili-say>0 kulüp seçildi</b><span class="kb-toplu-ayir"></span>
          <button type="button" class="btn btn-ghost btn-sm" data-toplu="api" data-bildir="Seçilen kulüplerin verisi API'den yeniden çekilecek (prototip)">{I("fa-rotate")}<span>API'den Yenile</span></button>
          <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe Taşı</span></button>
          <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi Temizle</button>
        </div>
        <div class="ptable-wrap"><table class="ptable">
          <thead><tr><th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün kulüpleri seç"></th><th class="kb-ana">Kulüp</th><th class="kb-gizle-m">Renk</th><th class="kb-gizle-t">Etiket Eşleşmesi</th><th class="say kb-gizle-t">Haber</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
          <tbody data-satirlar>{"".join(kl)}</tbody>
{durum_govdeleri(7, "fa-shield-halved", "Henüz kulüp yok", "Kulüpler spor veri API'sinden gelir; listede olmayanı “Yeni kulüp” ile ekleyin.", "Kulüpler yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", iskelet='<td></td><td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="spor.html")}        </table></div>
{pager(sayfalar=False)}
        <div class="pnl-menu kb-diger-menu" role="menu">
          <div class="kb-dm-grup" data-durum-icin="eslesti genel elle">Veri</div>
          <button type="button" data-durum-icin="eslesti genel elle" data-onay-baslik="Kulüp verisi API'den yenilensin mi?" data-onay-metin="Ad, kadro ve istatistikler API'den yeniden çekilir; elle girilen renk, kısa kod ve etiket eşleşmesi korunur." data-onay-evet="Yenile" data-onay-ikon="fa-rotate" data-bildir-sonra="Kulüp verisi kuyruğa alındı">{I("fa-rotate")}API'den Yenile</button>
          <button type="button" data-durum-icin="eslesti genel elle" data-bildir="Haberler bu kulübün etiketine süzülerek açılır (prototip)">{I("fa-newspaper")}Kulübün Haberleri</button>
          <button type="button" data-durum-icin="eslesti genel elle" data-roller="super gyy" data-bildir="Denetim izi bu kayda süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim İzinde Gör</button>
          <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten Geri Al</button>
          <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı Olarak Sil</button>
        </div>
      </div>
    </div>

    <!-- ===== LİGLER VE PUAN DURUMU ===== -->
    <div class="sa-form-panel" id="spLig" role="tabpanel" hidden>
      <div data-liste data-liste-ad="lig" data-sayfa-boy="50">
        <div class="filter-bar">
          <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="lgAra">Liglerde Ara</label><input id="lgAra" type="search" data-liste-ara placeholder="Lig, sıralama ya da lider ara" autocomplete="off"></div>
          <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
        </div>
        <div class="pc-body"><div class="kb-bant bilgi">{I("fa-lock")}<span><b>Ligler ve puan tabloları API verisidir; silinmez.</b> Satıra tıklayınca puan durumu açılır; yanlış değer oradan “Düzelt” ile elle düzeltilir (gerekçe zorunlu, denetim izine yazılır). Lig logosu kalem düğmesinden yüklenir; yoksa branş ikonu görünür. Son güncelleme 15.57.</span></div></div>
        <div class="ptable-wrap"><table class="ptable">
          <thead><tr><th class="kb-ana">Lig ya da Sıralama</th><th class="kb-gizle-t">Katılımcı</th><th class="kb-gizle-m">Lider</th><th>Kaynak</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
          <tbody data-satirlar>{"".join(lig_satir(L) for L in LG)}</tbody>
{durum_govdeleri(5, "fa-list-ol", "Henüz lig yok", "Ligler ve sıralamalar spor veri API'sinden gelir; sezon başlamadıysa liste boş görünür.", "Ligler yüklenemedi", "Spor veri API yanıt vermiyor. Entegrasyonlar ekranından bağlantıyı kontrol edin.", yeniden="spor.html")}        </table></div>
{pager(sayfalar=False)}
        <div class="pnl-menu kb-diger-menu" role="menu">
          <div class="kb-dm-grup">Veri</div>
          <button type="button" data-onay-baslik="Puan tablosu API'den yenilensin mi?" data-onay-metin="Tablo API'den yeniden çekilir; korunan elle düzeltmeler yerinde kalır." data-onay-evet="Yenile" data-onay-ikon="fa-rotate" data-bildir-sonra="Puan tablosu kuyruğa alındı">{I("fa-rotate")}API'den Yenile</button>
          <button type="button" data-durum-icin="elle" data-onay-baslik="Elle düzeltmeler kaldırılsın mı?" data-onay-metin="Tablo yeniden yalnız API'den gelir; düzeltme kayıtları denetim izinde kalır." data-onay-evet="API'ye Dön" data-onay-ikon="fa-rotate-left" data-sonra-durum="api" data-sonra-durum-ad="API" data-sonra-durum-sinif="ok" data-bildir-sonra="Puan tablosu yeniden API'den geliyor">{I("fa-rotate-left")}API Değerine Dön</button>
          <button type="button" data-roller="super gyy" data-bildir="Denetim izi bu lige süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim İzinde Gör</button>
        </div>
      </div>
    </div>

    <!-- ===== MAÇ MERKEZİ ===== -->
    <div class="sa-form-panel" id="spMac" role="tabpanel" hidden>
{gorsel_alani("mac_kapak", "Maç kapağı", "Maç Kapağı (Ortak)", "Bütün maç sayfalarında aynı · yoksa varsayılan görsel görünür", I("fa-panorama"),
              ("Maç kapağını sürükleyin ya da seçin", "Bütün maç sayfalarının başında tam genişlik · web 1440×496 (2.9:1), mobil 390×390 · değişiklik hemen sitede uygulanır"),
              [("web.detay", "Maç sayfası · 2.9:1", "2.9/1")], [("mobil.kart", "Telefon · 1:1", "r-1x1")],
              "Önerilen: <b>1440×496</b> (maç sayfasının başı, tam genişlik). Solda skor ve künye durur; odağı sağa koyun.", "Önerilen: <b>390×390</b> (sitenin telefon görünümü).",
              ikon="fa-panorama", havuz=True, dolu=("../../veri/gorsel/p155.jpg", "60% 45%", "Yüklenen: 1200×800 JPG."))}
      <div data-liste data-liste-ad="karşılaşma" data-sayfa-boy="50">
        <div class="kb-liste-ust">
          <div class="chips" role="tablist" aria-label="Karşılaşma durumu">
            <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="canli">Canlı<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="bekliyor">Fikstür<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="bitti">Bitti<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="elle">Elle Düzeltilen<span class="ch-cnt">0</span></button>
          </div>
        </div>
        <div class="filter-bar">
          <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="mcAra">Karşılaşmalarda Ara</label><input id="mcAra" type="search" data-liste-ara placeholder="Takım, sporcu, lig ya da yarış ara" autocomplete="off"></div>
          <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
        </div>
        <div class="pc-body"><div class="kb-bant bilgi">{I("fa-lock")}<span><b>Maçlar ve yarışlar spor veri API'sinden gelir; silinmez.</b> Skor, sonuç ve durum “Düzelt” ile elle düzeltilir (gerekçe zorunlu, denetim izine yazılır).</span></div></div>
        <div class="ptable-wrap"><table class="ptable">
          <thead><tr><th class="kb-ana">Karşılaşma</th><th class="say">Skor / Sonuç</th><th class="kb-gizle-m">Dakika / Aşama</th><th class="kb-gizle-t">Başlama</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
          <tbody data-satirlar>{"".join(mac_satir(m) for m in MACLAR)}</tbody>
{durum_govdeleri(6, "fa-stopwatch", "Bu süzgeçle karşılaşma yok", "Fikstür API'den gelir; sezon arasında liste boş olabilir.", "Karşılaşmalar yüklenemedi", "Spor veri API yanıt vermiyor. Entegrasyonlar ekranından bağlantıyı kontrol edin.", yeniden="spor.html")}        </table></div>
{pager(sayfalar=False)}
        <div class="pnl-menu kb-diger-menu" role="menu">
          <div class="kb-dm-grup">Karşılaşma</div>
          <button type="button" data-modul="haberler" data-bildir="Canlı anlatım Haberler › Canlı anlatım ekranında bu karşılaşmayla açılır (prototip)">{I("fa-tower-broadcast")}Canlı Anlatım Aç</button>
          <button type="button" data-bildir="Karşılaşmanın haberleri süzülerek açılır (prototip)">{I("fa-newspaper")}Karşılaşma Haberleri</button>
          <button type="button" data-durum-icin="elle" data-onay-baslik="Elle düzeltme kaldırılsın mı?" data-onay-metin="Sonuç yeniden API'den gelir; düzeltme kaydı denetim izinde kalır." data-onay-evet="API'ye Dön" data-onay-ikon="fa-rotate-left" data-sonra-durum="bitti" data-sonra-durum-ad="Bitti" data-sonra-durum-sinif="off" data-bildir-sonra="Sonuç yeniden API'den geliyor">{I("fa-rotate-left")}API Değerine Dön</button>
          <button type="button" data-roller="super gyy" data-bildir="Denetim izi bu karşılaşmaya süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim İzinde Gör</button>
        </div>
      </div>
    </div>
      </div>
    </div>
  </section>
</main>
</div>
{brans_sablonlar(say, alt["Spor"])}{"".join(lig_sablonlar(L) for L in LG)}{"".join(mac_sablonlar(m) for m in MACLAR)}"""
    s += son()
    return s


# ================================================================== KULÜP DÜZENLE
# Arma ölçüsü (lead kararı 25.11.2026, kayıtta): sitede takım sayfası .pf-av 96 (telefonda 72), takımlar .tc-a .arma 56, maç 28, puan durumu 24
ARMA_OLCU = ("takım sayfası 96×96, takımlar 56×56, mobil 72×72", "Önerilen: takım sayfası <b>96×96</b>, takımlar listesi <b>56×56</b>; puan durumunda 24, maç satırında 28 küçültülür.", "Önerilen: <b>72×72</b> (telefonda takım sayfası).", "Takımlar")
def seo_bolum(pid, baslik, aciklama, onek, slug, kw, uret=True):
    cip = "".join(f'<span class="kb-cip" data-deger="{e(k)}"><span>{e(k)}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for k in kw)
    return f"""    <div class="sa-form-panel" id="{pid}" role="tabpanel" data-ai-grup="seo" hidden>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-wand-magic-sparkles")}Otomatik Üretildi<span class="fs-ek"><button type="button" class="btn btn-ghost btn-sm" data-seo-uret>{I("fa-rotate")}Başlıktan Yeniden Üret</button></span></div>
        <div class="form-grid">
          <div class="frow"><label for="{pid}B">SEO Başlığı</label>
            <input class="finput" id="{pid}B" data-alan="seo-baslik" data-sayac="60|70" value="{e(baslik)}">
            <div class="char-meter"><span>Arama sonucunda görünen başlık · 50–60 karakter önerilir</span><b>0 / 60</b></div></div>
          <div class="frow"><label for="{pid}A">SEO Açıklaması</label>
            <textarea class="ftext" id="{pid}A" data-alan="seo-aciklama" data-sayac="155|170">{e(aciklama)}</textarea>
            <div class="char-meter"><span>Arama sonucunda başlığın altında · 120–155 karakter önerilir</span><b>0 / 155</b></div></div>
          <div class="frow"><label for="{pid}S">Adres</label>
            <div class="slug-wrap"><span class="slug-pre">{e(onek)}</span><input class="finput" id="{pid}S" data-alan="slug" value="{e(slug)}"></div>
            <span class="fhint">Yayımlandıktan sonra değiştirilirse eski adres yeniye yönlendirilir.</span></div>
          <div class="frow"><span class="flabel">Anahtar Kelimeler</span>
            <div class="kb-cip-girdi" data-serbest>{cip}<input type="text" placeholder="Yazın; Enter ya da virgülle ekleyin" aria-label="Anahtar kelime ekle"><div class="pnl-menu kb-cip-oneri"></div></div></div>
          <div class="frow"><span class="flabel">Arama Sonucu Önizlemesi</span>
            <div class="serp"><div class="serp-url"><span class="serp-fav kb-logo-isaret"></span><span>{e(onek.replace("/", " › ").rstrip(" › "))} › <span data-alan="slug">{e(slug)}</span></span></div>
              <div class="serp-title" data-alan="seo-baslik">{e(baslik)}</div>
              <div class="serp-desc" data-alan="seo-aciklama">{e(aciklama)}</div></div></div>
        </div>
      </div>
    </div>
"""


def seo_skor(n=82, kontroller=None):
    k = kontroller or [("pass", "Başlık 50–60 karakter"), ("pass", "Açıklama 120–155 karakter"), ("fail", "Sayfada iç bağlantı az")]
    bos_ = '<i class="fa-regular fa-circle" aria-hidden="true"></i>'
    ch = "".join(f'<div class="seo-chk {c}">{I("fa-circle-check") if c == "pass" else bos_}{e(t)}</div>' for c, t in k)
    return f"""    <section class="pnl-card" data-one-cik="pSeo">
      <div class="pc-head"><h2 class="pc-title">{I("fa-gauge")}SEO Skoru</h2></div>
      <div class="pc-body">
        <p class="fhint" data-yeni-goster hidden>Skor, ad ve açıklama girilince hesaplanır.</p>
        <div class="seo-score" data-yeni-gizle><div class="score-ring" style="--p:{n}"><span class="score-num">{n}</span></div><div class="score-meta"><b>İyi</b><span>Eksikler giderilince yükselir</span></div></div>
        <div class="seo-checks" data-yeni-gizle>{ch}</div>
      </div>
    </section>
"""


def sayfa_kulup():
    t = [x for x in tablo() if x["kod"] == "GS"][0]
    sira = [x["kod"] for x in tablo()].index("GS") + 1
    ligler = [("Süper Lig", "Süper Lig", "Futbol"), ("1. Lig", "1. Lig", "Futbol"), ("UEFA Şampiyonlar Ligi", "UEFA Şampiyonlar Ligi", "Futbol · Avrupa"), ("Premier Lig", "Premier Lig", "Futbol · Avrupa"),
              ("Basketbol Süper Ligi", "Basketbol Süper Ligi", "Basketbol"), ("Sultanlar Ligi", "Sultanlar Ligi", "Voleybol")]
    alt = alt_konular()
    spor_alt = [(a, f"Spor › {a}", "") for a in alt["Spor"]]
    sehirler = json.dumps(["İstanbul", "Ankara", "İzmir", "Trabzon", "Samsun", "Antalya", "Konya", "Rize", "Gaziantep", "Kocaeli", "Diyarbakır", "Kayseri"], ensure_ascii=False)
    renkler = "".join(f'<label class="kb-renk kat-{k}" title="{a}"><input type="radio" name="klRenk" value="{k}"><span></span><span class="sr-only">{a}</span></label>' for k, a in [("gundem", "Gündem"), ("spor", "Spor"), ("finans", "Finans"), ("savunma", "Savunma"), ("dunya", "Dünya"), ("kose", "Köşe")])
    renkler += f'<label class="kb-renk is-ozel" title="Özel renk {t["renk"]}"><input type="radio" name="klRenk" value="{t["renk"]}" checked><span style="--kat:{t["renk"]}"></span><span class="sr-only">Özel renk {t["renk"]}</span></label>'
    s = bas("Kulüp Düzenle", "kulup", ' data-yeni-baslik="Yeni Kulüp"')
    s += f"""
<!-- KULÜP DÜZENLE (D4): Detay · SEO (kulüp sayfası sitede var, 8b). Arma 1:1 (ozel-dikeyler.arma; kurumsal işaret,
     medya havuzuna girmez, data-etiketsiz). Takım kapağı (ozel-dikeyler.takim_kapak; fotoğraf: havuzdan seçilir, yüklemede etiketlenir):
     takım sayfasının başı, yoksa kurumsal renkle kapak. Kurumsal renk hazır + özel (kb-renkler[data-renk-ozel]). Sitede arma yoksa renkli kısa kod rozeti. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1 data-yeni-metin="Yeni Kulüp">Kulüp Düzenle</h1>
      <div class="ph-sub" data-yeni-metin="Henüz kaydedilmedi · spor veri API'sinde eşleşme aranır">Galatasaray · Süper Lig · {sira}. sıra, {t['P']} puan · API ile eşleşik</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ozel-dikeyler.spor" href="spor.html">{I("fa-arrow-left")}Spora Dön</a>
      <a class="btn btn-ghost btn-sm" data-yeni-gizle href="{SITE}galatasaray.html" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Sitede Görüntüle</a>
    </div>
  </div>

  <div class="form-layout">
  <section class="pnl-card" id="klForm" data-form data-sekmeli data-zorunlu-kayit="ozel-dikeyler.kulup" aria-label="Kulüp formu">
{dil_secici("Dil seçici kulüp hakkında metnini ve SEO alanlarını birlikte değiştirir; ad, kısa kod, renk ve arma bütün dillerde ortaktır.")}
    <div class="sa-form-tabs" role="tablist" aria-label="Düzenleme sekmeleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="pDetay">{I("fa-file-lines")}Detay</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="pSeo">{I("fa-magnifying-glass-chart")}SEO</button>
    </div>

    <div class="sa-form-panel" id="pDetay" role="tabpanel">
      <div class="form-sec">
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><label for="klAd">Kulüp Adı</label>
            <input class="finput kb-buyuk" id="klAd" data-alan-id="ad" data-sayac="30|40" value="Galatasaray">
            <div class="char-meter"><span>Puan durumunda, skor bandında ve takım sayfasında</span><b>0 / 30</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Kulüp adı zorunlu.</div></div>
          <div class="frow"><label for="klKod">Kısa Kod</label>
            <input class="finput" id="klKod" data-alan-id="kod" data-sayac="3|4" value="GS">
            <div class="char-meter"><span>Skor bandında ve arma yoksa rozette</span><b>0 / 3</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Kısa kod zorunlu.</div></div>
          <div class="frow"><span class="flabel">Lig</span>
            {secim("klLig", ligler, deger="Süper Lig", bos="Lig seçin", ara="Lig ara", ek=' data-alan-id="lig" data-zorunlu-metin="Kulübün ligini seçin"')}
            <div class="ferr">{I("fa-circle-exclamation")}Kulübün ligini seçin.</div></div>
          <div class="frow"><span class="flabel">Şehir</span>
            <div class="kb-cip-girdi" data-havuz-yonet data-kullanim-birim="kulüpte" data-havuz='{e(sehirler)}'><span class="kb-cip" data-deger="İstanbul"><span>İstanbul</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><input type="text" placeholder="Şehir ara" aria-label="Şehir"><div class="pnl-menu kb-cip-oneri"></div></div></div>
          <div class="frow"><label for="klStat">Stadyum ya da Salon</label><input class="finput" id="klStat" value="Ali Sami Yen Spor Kompleksi"></div>
          <div class="frow"><label for="klTd">Teknik Direktör</label><input class="finput" id="klTd" value="" placeholder="Spor veri API'sinden gelir"><span class="fhint">Boş bırakılırsa API'deki ad gösterilir.</span></div>
        </div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-palette")}Kurumsal Renk<span class="fs-ek">Puan durumunda rozet, skor bandında çizgi</span></div>
        <div class="kb-renkler" role="radiogroup" aria-label="Kurumsal Renk" data-renk-ozel>{renkler}</div>
        <span class="fhint">Hazır renkler temadan; damlalık ile kulübün kendi rengi seçilir (okunurluk denetlenir).</span>
      </div>
{gorsel_alani("arma", "Arma", "Arma", "İsteğe bağlı · yoksa renkli kısa kod rozeti görünür", '<span class="kb-ava k-lg">GS</span>',
              ("Armayı sürükleyin ya da seçin", "1:1 · " + ARMA_OLCU[0] + " · şeffaf PNG ya da SVG önerilir; medya havuzuna girmez"),
              [("web.detay", "Takım sayfası · 1:1", "r-1x1"), ("web.kart", ARMA_OLCU[3] + " · 1:1", "r-1x1")], [("mobil.kart", "Mobil · 1:1", "r-1x1")],
              ARMA_OLCU[1], ARMA_OLCU[2], ikon="fa-shield-halved")}
{gorsel_alani("takim_kapak", "Takım kapağı", "Takım Kapağı", "İsteğe bağlı · yoksa kurumsal renkle kapak görünür", I("fa-panorama"),
              ("Takım kapağını sürükleyin ya da seçin", "Takım sayfasının başında tam genişlik · web 1440×496 (2.9:1), mobil 390×390 · görselin solu yazı için koyu perdeyle örtülür"),
              [("web.detay", "Takım sayfası · 2.9:1", "2.9/1")], [("mobil.kart", "Telefon · 1:1", "r-1x1")],
              "Önerilen: <b>1440×496</b> (takım sayfasının başı, tam genişlik). Solda ad ve künye durur; odağı sağa koyun.", "Önerilen: <b>390×390</b> (sitenin telefon görünümü).",
              ikon="fa-panorama", havuz=True, dolu=("../../veri/gorsel/p158.jpg", "62% 45%", "Yüklenen: 1200×800 JPG, 86 KB."))}
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-tags")}Etiket Eşleştirme<span class="fs-ek">Haberler, skor ve kulüp sayfası bu eşleşmeyle bağlanır</span></div>
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><span class="flabel">Spor Alt Konusu</span>{secim("klAlt", spor_alt, deger="Galatasaray", bos="Alt konu seçin", ara="Alt konu ara")}<span class="fhint">Yeni alt konu Haberler › Kategoriler'den eklenir.</span></div>
          <div class="frow"><label for="klApi">Spor Veri API Kimliği</label><input class="finput" id="klApi" value="takim/645" readonly><span class="fhint">API eşleşmesi kendiliğinden yapılır; değişmez.</span></div>
        </div>
        <div class="frow kb-ust-bosluk"><span class="flabel">Haberlerde Geçen Diğer Adlar</span>
          <div class="kb-cip-girdi" data-serbest><span class="kb-cip" data-deger="GS"><span>GS</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><span class="kb-cip" data-deger="Cimbom"><span>Cimbom</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><span class="kb-cip" data-deger="Sarı-Kırmızılılar"><span>Sarı-Kırmızılılar</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><input type="text" placeholder="Yazın; Enter ya da virgülle ekleyin" aria-label="Diğer ad ekle"></div>
          <span class="fhint">AI havuzu ve arama bu adlarla da kulübü tanır.</span></div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-align-left")}Kulüp Hakkında<span class="fs-ek">Takım sayfasının başında</span></div>
        <div class="kb-editor" data-editor-ad="Kulüp Hakkında" data-editor-kisa><div class="kz-alan ke-alan"><p>1905'te kurulan Galatasaray, Süper Lig'in en çok şampiyonluk kazanan kulübü. Maçlarını İstanbul'da Ali Sami Yen Spor Kompleksi'nde oynuyor.</p></div></div>
      </div>
    </div>

{seo_bolum("pSeo", "Galatasaray haberleri, maç sonuçları ve puan durumu | Dada Haber", "Galatasaray'ın son haberleri, maç sonuçları, fikstürü ve Süper Lig puan durumu Dada Haber'de.", "dadahaber.com/", "galatasaray", ["galatasaray", "galatasaray haberleri", "galatasaray maç sonucu"])}
  </section>

  <aside class="side-card" aria-label="Kulüp durumu">
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-futbol")}Durum</h2><span class="pstat ok" data-yeni-gizle>API ile eşleşik</span></div>
      <div class="pc-body sa-durum" data-yeni-gizle>
        <div><span>Sıra</span><b>{sira}. · {t['P']} puan</b></div>
        <div><span>Maç</span><b>{t['O']} · {t['G']}G {t['B']}B {t['M']}M</b></div>
        <div><span>Gol</span><b>{t['A']}:{t['Y']}</b></div>
        <div><span>Haber · 30 gün</span><b>{sayi(haber_say("Galatasaray"))}</b></div>
        <div><span>Son API güncellemesi</span><b>15.57</b></div>
      </div>
      <div class="pc-body" data-yeni-goster hidden><p class="fhint">Kaydedince spor veri API'sinde aynı adla takım aranır; bulunamazsa kulüp elle veriyle görünür.</p></div>
    </section>
{seo_skor(84)}  </aside>
  </div>

  <div class="kb-kaydet" data-form-icin="klForm">
    <div class="kk-durum">{I("fa-circle-check")}<span data-yeni-metin="Henüz kaydedilmedi">Kaydedildi · 21.11.2026 11.20 · Burak Tan</span></div>
    <div class="kk-sag">
      <button type="button" class="btn btn-acc btn-sm" data-kaydet data-kaydet-metin="Kaydedildi" data-bildir="Kulüp kaydedildi; sitede puan durumu ve takım sayfası güncellendi" data-yeni-bildir="Kulüp eklendi; spor veri API'sinde eşleşme aranıyor">{I("fa-floppy-disk")}Kaydet</button>
    </div>
  </div>
</main>
</div>
"""
    s += son(editor=True)
    return s


# ================================================================== TAKVİMLER
TK_TUR = {"gundem": ("Gündem", "bilgi", "fa-landmark"), "ekonomik": ("Ekonomik", "ok", "fa-chart-line"), "sinav": ("Sınav", "uyari", "fa-graduation-cap"), "etkinlik": ("Etkinlik", "marka", "fa-calendar-check")}
# takvim kaydının kategorisi "Ana › Alt konu" (kategori.json); liste süzgeci ana kategoriyle çalışır
TK_ALT = [f"{a} › {k}" for a, ks in alt_konular().items() for k in ks]
TK_ANA = [b["ad"] for b in KAT["basliklar"]]
ONEM = {"yuksek": ("warm", "Yüksek"), "orta": ("wait", "Orta"), "dusuk": ("off", "Düşük")}
TAKVIM = [
    # id, tür, başlık, tarih, kategori, kurum, not, önem, durum, ekonomik (önceki, beklenti, açıklanan), sınav aşaması
    ("tk-tuketici", "ekonomik", "Tüketici Güven Endeksi · Kasım", "23.11.2026 10.00", "Finans › Türkiye Ekonomisi", "TÜİK", "Önceki 84,1 · Beklenti 85,0", "yuksek", "yayinda", ("84,1", "85,0", "85,4"), ""),
    ("tk-ppk", "ekonomik", "TCMB Para Politikası Kurulu · Faiz kararı", "23.11.2026 14.00", "Finans › Faiz Oranları", "TCMB", "Açıklandı %42,50 · Beklenti %42,50", "yuksek", "yayinda", ("%42,50", "%42,50", "%42,50"), ""),
    ("tk-butce", "gundem", "Genel Kurul'da bütçe görüşmeleri", "23.11.2026 14.00", "Gündem › Siyaset", "TBMM", "Bakanlık bütçeleri", "yuksek", "yayinda", None, ""),
    ("tk-abd-issizlik", "ekonomik", "ABD Haftalık İşsizlik Başvuruları", "23.11.2026 15.30", "Finans › Dünya Ekonomisi", "ABD Çalışma Bakanlığı", "Önceki 231 bin · Beklenti 228 bin", "orta", "yayinda", ("231 bin", "228 bin", ""), ""),
    ("tk-eyds-basvuru", "sinav", "2026-e-YDS/12 İngilizce Başvuruları Son Gün", "23.11.2026 23.59", "Kampüs › ALES ve YDS", "ÖSYM", "Sınav 6 Aralık", "yuksek", "yayinda", None, "basvuru"),
    ("tk-kko", "ekonomik", "Kapasite Kullanım Oranı · Kasım", "24.11.2026 10.00", "Finans › Sanayi", "TCMB", "Önceki %74,2 · Beklenti %74,5", "orta", "yayinda", ("%74,2", "%74,5", ""), ""),
    ("tk-gs-atm", "etkinlik", "Şampiyonlar Ligi: Galatasaray – Atlético Madrid", "24.11.2026 20.45", "Spor › Galatasaray", "UEFA", "5. hafta", "orta", "yayinda", None, ""),
    ("tk-siddet", "gundem", "Kadına Yönelik Şiddete Karşı Uluslararası Mücadele Günü", "25.11.2026 10.00", "Kadın › Kadın Hakları", "", "Etkinlikler 81 ilde", "yuksek", "yayinda", None, ""),
    ("tk-ab-konsey", "gundem", "AB Dışişleri Konseyi Toplantısı", "26.11.2026 10.00", "Dünya › Diplomasi", "AB Konseyi", "Brüksel", "orta", "yayinda", None, ""),
    ("tk-pce", "ekonomik", "ABD Çekirdek PCE fiyat endeksi · Ekim", "26.11.2026 16.30", "Finans › Dünya Ekonomisi", "ABD Ticaret Bakanlığı", "Önceki %2,7 · Beklenti %2,8", "yuksek", "yayinda", ("%2,7", "%2,8", ""), ""),
    ("tk-basket", "etkinlik", "Basketbol: Türkiye – Macaristan", "26.11.2026 20.00", "Spor › Basketbol", "FIBA", "Dünya Kupası elemeleri", "orta", "yayinda", None, ""),
    ("tk-pmi", "ekonomik", "Euro Bölgesi Öncü İmalat PMI", "27.11.2026 12.00", "Finans › Dünya Ekonomisi", "S&P Global", "Önceki 49,8 · Beklenti 50,1", "orta", "yayinda", ("49,8", "50,1", ""), ""),
    ("tk-dis-ticaret", "ekonomik", "Dış ticaret dengesi · Ekim", "28.11.2026 10.00", "Finans › Türkiye Ekonomisi", "TÜİK", "Önceki -6,9 milyar $ · Beklenti -6,4 milyar $", "orta", "yayinda", ("-6,9 milyar $", "-6,4 milyar $", ""), ""),
    ("tk-kis-lastigi", "gundem", "Kış lastiği uygulaması başlıyor", "01.12.2026 00.00", "Gündem › Toplum", "Emniyet Genel Müdürlüğü", "Ticari araçlar için 1 Nisan'a kadar", "yuksek", "yayinda", None, ""),
    ("tk-gsyh", "ekonomik", "GSYH · 3. çeyrek (yıllık)", "01.12.2026 10.00", "Finans › Türkiye Ekonomisi", "TÜİK", "Önceki %4,8 · Beklenti %3,9", "yuksek", "yayinda", ("%4,8", "%3,9", ""), ""),
    ("tk-kpss-tercih", "sinav", "KPSS-2026/7 tercih dönemi", "01.12.2026 10.00", "Kampüs › KPSS", "ÖSYM", "Tercih 1–8 Aralık · Sonuç 18 Aralık", "orta", "yayinda", None, "tercih"),
    ("tk-aids", "gundem", "Dünya AIDS Günü", "01.12.2026 09.00", "Keşfet › Halk Sağlığı", "Sağlık Bakanlığı", "Ücretsiz test noktaları açılıyor", "dusuk", "yayinda", None, ""),
    ("tk-kulup-haftasi", "etkinlik", "Kış dönemi kulüp tanıtım haftası", "01.12.2026 10.00", "Kampüs › Öğrenci Toplulukları", "Üniversiteler", "Kampüslerde bir hafta", "dusuk", "taslak", None, ""),
    ("tk-tufe", "ekonomik", "TÜFE · Kasım (yıllık)", "03.12.2026 10.00", "Finans › Enflasyon", "TÜİK", "Önceki %32,9 · Beklenti %31,8", "yuksek", "yayinda", ("%32,9", "%31,8", ""), ""),
    ("tk-eyds-sinav", "sinav", "2026-e-YDS/12 İngilizce sınavı", "06.12.2026 10.15", "Kampüs › ALES ve YDS", "ÖSYM", "Sonuç 10 Aralık", "orta", "yayinda", None, "sinav"),
    ("tk-yokdil", "sinav", "2026-YÖKDİL/2 sonuçları", "18.12.2026 14.00", "Kampüs › ALES ve YDS", "ÖSYM", "Sonuçlar aday işlemleri sisteminde", "orta", "yayinda", None, "sonuc"),
    ("tk-eski", "gundem", "Bütçe görüşmeleri Plan ve Bütçe Komisyonu'nda", "02.11.2026 10.00", "Gündem › Siyaset", "TBMM", "Komisyon görüşmeleri", "orta", "cop", None, ""),
]
ASAMA = [("basvuru", "Başvuru", ""), ("sinav", "Sınav", ""), ("sonuc", "Sonuç", ""), ("tercih", "Tercih", "")]


def tk_tarih_iso(t):
    return f"{t[6:10]}-{t[3:5]}-{t[0:2]} {t[11:]}"


def tk_form(sid, r=None):
    tid, tur, bas_, tarih, kat, kurum, not_, onem, dur, eko, asama = r if r else ("", "", "", "", "", "", "", "orta", "taslak", None, "")
    turler = "".join(f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="tkTur-{sid}" value="{k}"{" checked" if k == tur else ""}{f" data-ac=\"tkEko-{sid}\"" if k == "ekonomik" else f" data-ac=\"tkSnv-{sid}\"" if k == "sinav" else ""}><span><b>{I(v[2])} {v[0]}</b><small>{ {"gundem": "Gündem Takvimi", "ekonomik": "Ekonomik Takvim", "sinav": "Sınav Takvimi", "etkinlik": "Gündem Takvimi · etkinlik"}[k] }</small></span></label>' for k, v in TK_TUR.items())
    katlar = [(k, k, "") for k in TK_ALT]
    onemler = "".join(f'<label class="kb-secenek"><input type="radio" name="tkOnem-{sid}" value="{k}"{" checked" if k == onem else ""}>{v[1]}</label>' for k, v in ONEM.items())
    e1, e2, e3 = eko if eko else ("", "", "")
    return f"""  <div class="kb-fs">
    <div class="frow"><label for="tkB-{sid}">Başlık</label>
      <input class="finput" id="tkB-{sid}" data-alan-id="baslik" data-sayac="70|90" value="{e(bas_)}" placeholder="ör. TÜFE · Kasım (yıllık)">
      <div class="char-meter"><span>Takvim sayfasında ve ana sayfa takvim kutusunda</span><b>0 / 70</b></div>
      <div class="ferr">{I("fa-circle-exclamation")}Başlık zorunlu.</div></div>
    <div class="frow"><span class="flabel">Tür</span><div class="kb-kart-sec" data-alan-id="tur" data-zorunlu-metin="Kaydın hangi takvimde görüneceğini seçin">{turler}</div>
      <div class="ferr">{I("fa-circle-exclamation")}Kaydın hangi takvimde görüneceğini seçin.</div></div>
    <div class="form-grid kb-iki-sutun">
      <div class="frow"><span class="flabel">Tarih ve Saat</span>
        <div class="kb-tarih-sec" id="tkT-{sid}" data-alan-id="tarih" data-deger="{tk_tarih_iso(tarih) if tarih else ""}" data-zorunlu-metin="Tarih ve saati seçin">
          <button type="button" class="kb-tarih-btn" data-acilir="tkTM-{sid}" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
          <div class="pnl-menu kb-tarih-menu" id="tkTM-{sid}" role="dialog" aria-label="Tarih ve saat seç"></div></div>
        <div class="ferr">{I("fa-circle-exclamation")}Tarih ve saati seçin.</div></div>
      <div class="frow"><span class="flabel">Kategori</span>
        {secim("tkK-" + sid, katlar, deger=kat, bos="Kategori seçin", ara="Kategori ara", ek=' data-alan-id="kategori" data-zorunlu-metin="Kategoriyi seçin"', kaynak="tkKatListe")}
        <div class="ferr">{I("fa-circle-exclamation")}Kategoriyi seçin.</div></div>
      <div class="frow"><label for="tkKu-{sid}">Kurum</label><input class="finput" id="tkKu-{sid}" value="{e(kurum)}" placeholder="ör. TÜİK, ÖSYM, TBMM"></div>
      <div class="frow"><label for="tkN-{sid}">Kısa Not</label><input class="finput" id="tkN-{sid}" data-sayac="60|80" value="{e(not_)}" placeholder="ör. Etkinlikler 81 ilde"><div class="char-meter"><span>Başlığın altında</span><b>0 / 60</b></div></div>
    </div>
    <div class="form-grid kb-iki-sutun" id="tkEko-{sid}" hidden>
      <div class="frow"><label for="tkO-{sid}">Önceki</label><input class="finput" id="tkO-{sid}" value="{e(e1)}"></div>
      <div class="frow"><label for="tkBk-{sid}">Beklenti</label><input class="finput" id="tkBk-{sid}" value="{e(e2)}"></div>
      <div class="frow"><label for="tkA-{sid}">Açıklanan</label><input class="finput" id="tkA-{sid}" value="{e(e3)}" placeholder="Açıklanınca girilir"></div>
    </div>
    <div class="frow" id="tkSnv-{sid}" hidden><span class="flabel">Aşama</span>{secim("tkAs-" + sid, ASAMA, deger=asama, bos="Aşama seçin")}</div>
    <div class="frow"><span class="flabel">Önem</span><div class="kb-secenek-grup">{onemler}</div><span class="fhint">Yüksek önemli kayıtlar ana sayfa takvim kutusunda öne çıkar.</span></div>
    <div class="frow"><label for="tkL-{sid}">Bağlantı</label><input class="finput" id="tkL-{sid}" inputmode="url" value="" placeholder="İlgili haber ya da resmî duyuru adresi (isteğe bağlı)"></div>
  </div>
"""


def tk_sablonlar(r):
    tid, tur, bas_, tarih, kat, kurum, not_, onem, dur, eko, asama = r
    ad, ton, ik = TK_TUR[tur]
    return f"""<template id="tkGor-{tid}" data-baslik="{e(bas_)}" data-alt="{ad} takvimi · {e(tarih)}">
  <div class="kb-fs"><div class="sa-durum">
    <div><span>Tarih</span><b>{e(tarih)}</b></div><div><span>Tür</span><b>{ad}</b></div><div><span>Kategori</span><b>{e(kat)}</b></div>
    <div><span>Kurum</span><b>{e(kurum or "—")}</b></div><div><span>Not</span><b>{e(not_)}</b></div>
    <div><span>Önem</span><b><span class="pstat {ONEM[onem][0]}">{ONEM[onem][1]}</span></b></div>
    <div><span>Durum</span><b>{"Yayında" if dur == "yayinda" else "Taslak" if dur == "taslak" else "Çöpte"}</b></div>
  </div></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="tkDz-{tid}">{I("fa-pen")}Düzenle</button></div>
</template>
<template id="tkDz-{tid}" data-baslik="{e(bas_)} · Düzenle" data-alt="Takvim kaydı · hemen yayında" data-zorunlu-kayit="ozel-dikeyler.takvim">
{tk_form(tid, r)}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm" data-kaydet-tur="taslak" data-sablon-ac="tkGor-{tid}" data-bildir-sonra="Taslak olarak kaydedildi; sitede görünmez">{I("fa-floppy-disk")}Taslak Kaydet</button><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="tkGor-{tid}" data-bildir-sonra="Takvim kaydı güncellendi; önceki hal denetim izinde">{I("fa-check")}Kaydet ve Yayımla</button></div>
</template>
"""


def sayfa_takvimler():
    canli = [r for r in TAKVIM if r[8] != "cop"]
    rows = []
    for r in TAKVIM:
        tid, tur, bas_, tarih, kat, kurum, not_, onem, dur, eko, asama = r
        ad, ton, ik = TK_TUR[tur]
        durum = "cop" if dur == "cop" else tur
        olay = f' data-tarih="{tarih}" data-ad="{e(bas_)}" data-ton="{ton}" data-ikon="fa-solid {ik}" data-not="{e(ad + " · " + kat + (" · " + kurum if kurum else ""))}"'
        rows.append(f'<tr data-satir="{tid}" data-durum="{durum}" data-kategori="{e(kat.split(" › ")[0])}" data-onem="{onem}" data-yayin="{dur}"{olay} data-ara="{e(bas_ + " " + kat + " " + kurum + " " + ad)}" data-baslik="{e(bas_)}"{" data-onceki=\"gundem\"" if dur == "cop" else ""}>'
                    f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(bas_)}"></td>'
                    f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name" title="{e(bas_)}">{e(bas_)}</div><div class="rcp-by">{I(ik)}{ad} · {e(kat)}{" · " + e(kurum) if kurum else ""}</div></div></td>'
                    f'<td><span class="kb-tarih">{e(tarih)}</span></td>'
                    f'<td class="kb-gizle-m">{e(not_)}</td>'
                    f'<td class="kb-gizle-t"><span class="pstat {ONEM[onem][0]}">{ONEM[onem][1]}</span></td>'
                    f'<td><span class="pstat {"ok" if dur == "yayinda" else "off"}">{"Yayında" if dur == "yayinda" else "Taslak" if dur == "taslak" else "Çöpte"}</span></td>'
                    f'<td>{row_acts(("tanim", "tkGor-" + tid), ("tanim", "tkDz-" + tid), "sil")}</td></tr>')
    sab = "".join(tk_sablonlar(r) for r in TAKVIM)
    katlar = [("", "Bütün Kategoriler", "")] + [(k, k, str(sum(1 for r in canli if r[4].split(" › ")[0] == k))) for k in TK_ANA if any(r[4].split(" › ")[0] == k for r in canli)]
    onemler = [("", "Bütün önemler", "")] + [(k, v[1], "") for k, v in ONEM.items()]
    yuksek = sum(1 for r in canli if r[7] == "yuksek")
    s = bas("Takvimler", "takvimler")
    s += f"""
<!-- TAKVİMLER (D4; KURAL · tek veri görünümü): gündem, ekonomik, sınav ve etkinlik takvimi tek kartta. Tür sekmeleri, arama ve süzgeç
     bir kez; takvim listeye bağlı (olaylar satırlardan, tr[data-tarih]); Ay · Hafta takvimi, "Liste" tabloyu gösterir (Çöp, toplu seçim,
     satır eylemleri orada). Kayıt çekmecede (görüntüle → düzenle); boş güne tıklayınca yeni kayıt (data-gun-ac). -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Takvimler</h1>
      <div class="ph-sub">{len(canli)} kayıt · {yuksek} yüksek önemli · takvimde boş bir güne tıklayarak o güne kayıt ekleyin</div>
    </div>
    <div class="ph-actions">
      <button type="button" class="btn btn-acc btn-sm" data-tanim="tkYeni">{I("fa-plus")}Yeni Kayıt</button>
    </div>
  </div>

  <section class="pnl-card" data-liste data-liste-ad="kayıt" data-sayfa-boy="25" data-liste-cop-not="Kayıt takvimlerden kalkar ve Çöp sekmesine taşınır" aria-labelledby="tkListeBas">
    <h2 class="sr-only" id="tkListeBas">Takvim kayıtları</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Takvim türü">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
        {"".join(f'<button type="button" class="chip" role="tab" aria-selected="false" data-sekme="{k}">{I(v[2])}{v[0]}<span class="ch-cnt">0</span></button>' for k, v in TK_TUR.items())}
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="tkAra">Kayıtlarda Ara</label><input id="tkAra" type="search" data-liste-ara placeholder="Başlık, kurum ya da kategori ara" autocomplete="off"></div>
      {secim("tkSuzKat", katlar, etk="Kategori:", bos="Tümü", ara="Kategori ara", suz="kategori")}
      {secim("tkSuzOnem", onemler, etk="Önem:", bos="Tümü", suz="onem")}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>
    <div class="kb-toplu" hidden>
      <b data-secili-say>0 kayıt seçildi</b><span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="yayin" data-bildir="Seçilen kayıtlar yayımlandı">{I("fa-paper-plane")}<span>Yayımla</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe Taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button>
    </div>
    <div class="kb-takvim" data-baslangic="23.11.2026" data-gorunum="ay" data-gun-ac="tkYeni"></div>
    <div class="ptable-wrap"><table class="ptable">
      <thead><tr><th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün kayıtları seç"></th><th class="kb-ana">Kayıt</th><th>Tarih</th><th class="kb-gizle-m">Not</th><th class="kb-gizle-t">Önem</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
      <tbody data-satirlar>{"".join(rows)}</tbody>
{durum_govdeleri(7, "fa-calendar-days", "Henüz takvim kaydı yok", "İlk kaydı ekleyin ya da takvimde boş bir güne tıklayın.", "Takvim kayıtları yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", bos_eylem=chr(10) + '            <button type="button" class="pe-tag" data-tanim="tkYeni">' + I("fa-plus") + 'Yeni kayıt</button>', iskelet='<td></td><td><div class="rcp-id"><span></span></div></td><td><span></span></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="takvimler.html")}    </table></div>
{pager(sayfalar=False)}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup" data-durum-icin="gundem ekonomik sinav etkinlik">Kayıt</div>
      <button type="button" data-durum-icin="gundem ekonomik sinav etkinlik" data-bildir="Kopyası taslak olarak oluşturuldu (prototip)">{I("fa-copy")}Kopyasını oluştur</button>
      <button type="button" data-durum-icin="gundem ekonomik sinav etkinlik" data-bildir="Kayıt sitede ilgili takvim sayfasında açılır (prototip)">{I("fa-arrow-up-right-from-square")}Sitede Görüntüle</button>
      <button type="button" data-durum-icin="gundem ekonomik sinav etkinlik" data-roller="super gyy" data-bildir="Denetim izi bu kayda süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
      <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten geri al</button>
      <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı olarak sil</button>
    </div>
  </section>
</main>
</div>

<template id="tkKatListe">{"".join(f'<button type="button" data-deger="{e(k)}" data-ad="{e(k)}">{e(k)}</button>' for k in TK_ALT)}</template>
<template id="tkYeni" data-baslik="Yeni Takvim Kaydı" data-alt="Takvim kaydı · seçilen türün sayfasında" data-zorunlu-kayit="ozel-dikeyler.takvim">
{tk_form("yeni")}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm" data-kaydet-tur="taslak" data-sablon-ac="tkEklendi" data-bildir-sonra="Taslak olarak kaydedildi; sitede görünmez">{I("fa-floppy-disk")}Taslak Kaydet</button><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="tkEklendi" data-bildir-sonra="Takvim kaydı eklendi; denetim izine yazıldı">{I("fa-plus")}Ekle ve Yayımla</button></div>
</template>
<template id="tkEklendi" data-baslik="Kayıt eklendi" data-alt="Takvimde ve listede görünür">
  <div class="pnl-empty"><div class="pe-ico">{I("fa-circle-check")}</div><h2>Takvim kaydı eklendi</h2><p>Kayıt seçilen türün takvim sayfasında görünür; listeden düzenleyip silebilirsiniz.</p></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-kapat>{I("fa-check")}Tamam</button></div>
</template>
{sab}"""
    s += son()
    return s


# ================================================================== VERİ BANTLARI (ayar ekranı kalıbı)
def saglayicilar(sid, liste):
    sat = "".join(f'<div class="km-satir" data-sira><button type="button" class="kb-tutamac" aria-label="Sırayı değiştir (sürükleyin ya da ok tuşları)">{I("fa-grip-vertical")}</button><span class="km-no">{n + 1}</span><span class="km-yazi">{e(ad)}<small>{e(acik)}</small></span><span class="pstat {s}">{d}</span>'
                  + (f'<a class="ia-btn" data-hedef="entegrasyonlar.ayar" data-hedef-ek="?id={ent}" data-roller="super" href="../../cekirdek/entegrasyonlar/ayar.html?id={ent}" aria-label="{e(ad)} bağlantı ayarı" title="Bağlantı ayarı (Entegrasyonlar)">{I("fa-plug")}</a>' if ent else f'<button type="button" class="ia-btn kb-kilit" disabled aria-label="Anahtar gerekmez" title="Açık veri; API anahtarı gerekmez">{I("fa-lock-open")}</button>')
                  + '</div>' for n, (ad, acik, s, d, ent) in enumerate(liste))
    return f"""        <div class="frow"><span class="flabel">Kaynak Önceliği<span class="fhint kb-sag">Sürükleyerek sıralayın; birincil düşerse sıradaki devreye girer</span></span>
          <div class="kb-madde" data-siralanir aria-label="Kaynak Önceliği">{sat}</div>
          <span class="fhint">Kaynak ekleme ve API anahtarı Entegrasyonlar ekranındadır; burada yalnız öncelik ve kullanım ayarlanır.</span></div>
"""


def periyot(sid, gun, gb, onb, ob, gecikme=None):
    birim = [("Saniye", "Saniye", ""), ("Dakika", "Dakika", ""), ("Saat", "Saat", ""), ("Gün", "Gün", "")]
    return f"""        <div class="form-grid kb-iki-sutun">
          <div class="frow"><label for="{sid}Per">Güncelleme Periyodu</label><div class="frow two"><input class="finput" id="{sid}Per" inputmode="numeric" value="{gun}">{secim(sid + "PerB", birim, deger=gb, bos="Birim")}</div><span class="fhint">Kaynaktan bu sıklıkla yeni veri çekilir.</span></div>
          <div class="frow"><label for="{sid}Onb">Önbellek Süresi</label><div class="frow two"><input class="finput" id="{sid}Onb" inputmode="numeric" value="{onb}">{secim(sid + "OnbB", birim, deger=ob, bos="Birim")}</div><span class="fhint">Okur bu süre boyunca aynı veriyi görür; kaynak yükü azalır.</span></div>
        </div>
""" + (f'        <div class="frow kb-ust-bosluk"><span class="flabel">Gecikme</span><div class="kb-birim"><input class="finput" inputmode="numeric" value="{gecikme}" aria-label="Gecikme süresi"><span>Dakika</span></div><span class="fhint">Sitede değerlerin yanında “{gecikme} dk gecikmeli” yazar (lisans koşulu).</span></div>\n' if gecikme else "")


def hata_davranis(sid, sec="son"):
    return f"""        <div class="frow kb-ust-bosluk"><span class="flabel">Kaynak Yanıt Vermezse</span>
          <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="{sid}Hata"{" checked" if sec == "son" else ""}>Son Veriyi Saatiyle Göster</label><label class="kb-secenek"><input type="radio" name="{sid}Hata"{" checked" if sec == "gizle" else ""}>Bandı Gizle</label></div></div>
"""


# ---------------- Piyasa enstrümanları (kimlik görselleri işi, Beyar 25.11.2026)
# Liste Piyasa sekmesinde (emsal: Canlı Masa › Akış sekmesindeki liste); kayıt çekmecede (küçük tanım → çekmece). Değerler sözlükten
# (ornek_veri.json piyasa.araclar: şerit ve vitrin sırası) ve sitenin piyasa sayfalarından (piyasa-ekrani, doviz, altin, borsa, kripto-para).
# Logolar sitenin assets/gorsel/piyasa/ dosyalarının kopyası (gorsel/piyasa/); logo yoksa kısa kod rozeti.
EN_TUR = {"doviz": ("Döviz", "fa-dollar-sign"), "altin": ("Altın ve Gümüş", "fa-coins"), "endeks": ("Borsa Endeksi", "fa-chart-line"),
          "hisse": ("Hisse", "fa-building"), "kripto": ("Kripto", "fa-coins"), "emtia": ("Emtia", "fa-oil-well")}
ENST = [
    # id, ad (şerit ve kutu), kısa kod (tablo ve rozet), açıklama satırı, kaynak sembolü, tür, logo, son değer, şerit sırası, widget sırası, sayfa açıklaması
    ("xu100", "BIST 100", "X100", "Endeks", "XU100", "endeks", None, "10.248,62", 1, None, "Borsa İstanbul'un 100 hisseden oluşan ana endeksi"),
    ("xu030", "BIST 30", "X30", "Endeks", "XU030", "endeks", None, "11.204,35", None, None, "Borsa İstanbul'un en büyük 30 hissesinden oluşan endeks"),
    ("xbank", "BIST Banka", "XBNK", "Endeks", "XBANK", "endeks", None, "14.876,90", None, None, ""),
    ("xusin", "BIST Sınai", "XSIN", "Endeks", "XUSIN", "endeks", None, "12.038,47", None, None, ""),
    ("usd", "Dolar", "USD", "ABD Doları", "USDTRY", "doviz", "doviz/USD.svg", "34,5448", 2, 1, "ABD Doları'nın Türk lirası karşısındaki satış kuru"),
    ("eur", "Euro", "EUR", "Euro", "EURTRY", "doviz", "doviz/EUR.svg", "36,2180", 3, 2, "Euro'nun Türk lirası karşısındaki satış kuru"),
    ("gbp", "Sterlin", "GBP", "İngiliz Sterlini", "GBPTRY", "doviz", "doviz/GBP.svg", "43,1150", None, 3, ""),
    ("chf", "İsviçre Frangı", "CHF", "İsviçre Frangı", "CHFTRY", "doviz", "doviz/CHF.svg", "39,0040", None, None, ""),
    ("jpy", "Japon Yeni", "JPY", "Japon Yeni (100)", "JPYTRY", "doviz", "doviz/JPY.svg", "22,5320", None, None, ""),
    ("sar", "Suudi Riyali", "SAR", "Suudi Arabistan Riyali", "SARTRY", "doviz", "doviz/SAR.svg", "9,2105", None, None, ""),
    ("gram", "Gram Altın", "GA", "TL", "XAUTRYG", "altin", None, "2.968,40", 4, 4, "Bir gram 24 ayar altının Türk lirası satış fiyatı"),
    ("ceyrek", "Çeyrek Altın", "ÇA", "TL", "CEYREK", "altin", None, "4.905,00", None, None, ""),
    ("cumhuriyet", "Cumhuriyet Altını", "CA", "TL", "CUMHUR", "altin", None, "20.150,00", None, None, ""),
    ("bilezik", "22 Ayar Bilezik", "22A", "TL · gram", "BILEZIK22", "altin", None, "2.745,10", None, None, ""),
    ("ons", "Ons Altın", "ONS", "Dolar", "XAUUSD", "altin", None, "2.674,15", 5, None, ""),
    ("gumus", "Gümüş", "AG", "TL · gram", "XAGTRYG", "altin", None, "34,12", 6, None, ""),
    ("brent", "Brent", "BRT", "Petrol · dolar/varil", "BRENT", "emtia", None, "74,82", 7, None, "Kuzey Denizi Brent petrolünün varil fiyatı"),
    ("wti", "WTI", "WTI", "Petrol · dolar/varil", "WTI", "emtia", None, "71,24", None, None, ""),
    ("ttf", "Doğal Gaz", "TTF", "TTF · euro/MWh", "TTF", "emtia", None, "42,18", None, None, ""),
    ("thyao", "Türk Hava Yolları", "THYAO", "Türk Hava Yolları", "THYAO", "hisse", "borsa/THYAO.png", "312,75", None, None, ""),
    ("asels", "Aselsan", "ASELS", "Aselsan", "ASELS", "hisse", "borsa/ASELS.png", "87,90", None, None, ""),
    ("garan", "Garanti BBVA", "GARAN", "Garanti BBVA", "GARAN", "hisse", "borsa/GARAN.png", "128,40", None, None, ""),
    ("akbnk", "Akbank", "AKBNK", "Akbank", "AKBNK", "hisse", "borsa/AKBNK.png", "62,15", None, None, ""),
    ("kchol", "Koç Holding", "KCHOL", "Koç Holding", "KCHOL", "hisse", "borsa/KCHOL.png", "178,20", None, None, ""),
    ("tuprs", "Tüpraş", "TUPRS", "Tüpraş", "TUPRS", "hisse", "borsa/TUPRS.png", "154,60", None, None, ""),
    ("bimas", "BİM Mağazalar", "BIMAS", "BİM Mağazalar", "BIMAS", "hisse", "borsa/BIMAS.png", "521,50", None, None, ""),
    ("sise", "Şişecam", "SISE", "Şişecam", "SISE", "hisse", "borsa/SISE.png", "42,36", None, None, ""),
    ("btc", "Bitcoin", "BTC", "Bitcoin · dolar", "BTCUSD", "kripto", "kripto/BTC.svg", "98.412", 8, None, "Bitcoin'in dolar cinsinden fiyatı"),
    ("eth", "Ethereum", "ETH", "Ethereum · dolar", "ETHUSD", "kripto", "kripto/ETH.svg", "3.412,50", None, None, ""),
    ("bnb", "BNB", "BNB", "BNB · dolar", "BNBUSD", "kripto", "kripto/BNB.svg", "642,30", None, None, ""),
    ("sol", "Solana", "SOL", "Solana · dolar", "SOLUSD", "kripto", "kripto/SOL.svg", "238,15", None, None, ""),
    ("xrp", "XRP", "XRP", "XRP · dolar", "XRPUSD", "kripto", "kripto/XRP.svg", "1,4120", None, None, ""),
    ("bugday", "Buğday", "BGD", "Dolar/buşel", "WHEAT", "emtia", None, "5,62", None, None, ""),  # çöpte
]
EN_COP = {"bugday"}
EN_SERIT = sum(1 for x in ENST if x[8])
EN_WIDGET = sum(1 for x in ENST if x[9])
EN_LOGO = "gorsel/piyasa/"


def en_isaret(x, buyuk=False):
    """enstrüman logosu yüklenmişse o, yoksa kısa kod rozeti"""
    k = " k-lg" if buyuk else ""
    if x[6] and not buyuk:
        return f'<span class="kb-ava" style="background-image:url({EN_LOGO}{x[6]})" role="img" aria-label="{e(x[2])} logosu"></span>'
    return f'<span class="kb-ava{k}" title="Logo yok; kısa kod rozeti gösteriliyor">{e(x[2])}</span>'


def en_kullanim(x):
    yer = ([f"şeritte {x[8]}. sırada"] if x[8] else []) + ([f"ana sayfa piyasa kutusunda {x[9]}. sırada"] if x[9] else [])
    return ("Sitede " + " ve ".join(yer) + "; silinince oradan da kalkar, piyasa sayfalarında görünmez") if yer else ""


def en_satir(x):
    eid, ad, kisa, alt, sem, tur, logo, deg, ser, wid, _ = x
    gor = "|".join((["serit"] if ser else []) + (["widget"] if wid else [])) or "sayfa"
    kul = en_kullanim(x)
    cop = eid in EN_COP
    return (f'<tr data-satir="en-{eid}" data-durum="{"cop" if cop else tur}"{f" data-onceki=\"{tur}\"" if cop else ""} data-gorunum="{gor}" data-ara="{e(ad + " " + kisa + " " + alt + " " + sem + " " + EN_TUR[tur][0])}" data-baslik="{e(ad)}"{f" data-kullanim=\"{e(kul)}\"" if kul else ""}>'
            f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(ad)}"></td>'
            f'<td class="kb-ana"><div class="rcp-cell">{en_isaret(x)}<div class="rcp-id"><div class="rcp-name">{e(ad)}</div><div class="rcp-by">{e(kisa)} · {e(alt)}</div></div></div></td>'
            f'<td class="say kb-gizle-m">{e(deg)}</td>'
            f'<td class="say">{f"{ser}." if ser else "—"}</td>'
            f'<td class="say kb-gizle-m">{f"{wid}." if wid else "—"}</td>'
            f'<td>{row_acts(("tanim", "enGor-" + eid), ("tanim", "enDz-" + eid), "sil")}</td></tr>')


def en_form(sid, x=None):
    eid, ad, kisa, alt, sem, tur, logo, deg, ser, wid, acik = x if x else ("", "", "", "", "", "", None, "", None, None, "")
    turler = [(k, v[0], "") for k, v in EN_TUR.items()]
    dolu = (EN_LOGO + logo, "50% 50%", "Yüklenen: " + ("SVG" if logo.endswith(".svg") else "PNG") + " · şeffaf zemin.") if logo else None
    bos_yer = f'<span class="kb-ava k-lg">{e(kisa) if kisa else I("fa-chart-line")}</span>'
    slug = TR_SLUG(ad) if ad else ""
    seo_b = f"{ad} ne kadar? Canlı {ad} fiyatı ve grafiği | Dada Haber" if ad else ""
    seo_a = f"{ad} ({kisa}) son değeri, günlük değişimi, gün içi en düşük ve en yüksek değerleri; 15 dakika gecikmeli piyasa verisi." if ad else ""
    sira = lambda n, ad_, v: (f'<div class="frow"><label for="en{sid}-{n}">{ad_} Sırası</label><div class="kb-birim"><input class="finput" id="en{sid}-{n}" inputmode="numeric" value="{v or ""}" placeholder="—"><span>sıra</span></div>'
                              f'<span class="fhint">Aynı sıradaki enstrüman bir sonrakine kayar.</span></div>')
    return f"""  <div data-sekmeli>
    <div class="kb-form-bas kb-kap-dil">
      <div class="kb-dil" role="group" aria-label="İçerik dili">
        <button type="button" class="is-on" aria-pressed="true">TR · Türkçe</button>
        <button type="button" disabled title="Çeviri ekranları sonraki aşamada">EN<span class="kd-etk">Sonraki aşama</span></button>
        <button type="button" disabled title="Çeviri ekranları sonraki aşamada">AR<span class="kd-etk">Sonraki aşama</span></button>
        <button type="button" disabled title="Çeviri ekranları sonraki aşamada">DE<span class="kd-etk">Sonraki aşama</span></button>
      </div>
      <span class="kfb-not">{I("fa-language")}Dil seçici ad, açıklama satırı, sayfa açıklaması ve SEO alanlarını değiştirir; kod, logo ve sıralar ortaktır.</span>
    </div>
    <div class="sa-form-tabs kb-kap-sekme" role="tablist">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="en{sid}Detay">{I("fa-circle-info")}Detay</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="en{sid}Seo">{I("fa-magnifying-glass-chart")}SEO</button>
    </div>
    <div class="sa-form-panel" id="en{sid}Detay">
      <div class="kb-fs">
        <div class="kb-fs-tt">Temel Bilgiler</div>
        <div class="frow"><label for="en{sid}-ad">Ad</label><input class="finput" id="en{sid}-ad" data-alan-id="ad" data-alan="baslik" data-sayac="20|28" value="{e(ad)}" placeholder="ör. Dolar">
          <div class="char-meter"><span>Şeritte ve ana sayfa piyasa kutusunda</span><b>0 / 20</b></div>
          <div class="ferr">{I("fa-circle-exclamation")}Ad zorunlu.</div></div>
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><label for="en{sid}-kod">Kısa Kod</label><input class="finput" id="en{sid}-kod" data-alan-id="kod" data-sayac="4|5" value="{e(kisa)}" placeholder="ör. USD">
            <div class="char-meter"><span>Tabloda ve logo yoksa rozette</span><b>0 / 4</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Kısa kod zorunlu.</div></div>
          <div class="frow"><span class="flabel">Tür</span>{secim("en" + sid + "Tur", turler, deger=tur, bos="Tür seçin", ek=' data-alan-id="tur" data-zorunlu-metin="Enstrümanın türünü seçin"')}
            <span class="fhint">Sitede hangi piyasa sayfasında listeleneceğini belirler.</span>
            <div class="ferr">{I("fa-circle-exclamation")}Enstrümanın türünü seçin.</div></div>
        </div>
        <div class="frow"><label for="en{sid}-alt">Açıklama Satırı</label><input class="finput" id="en{sid}-alt" data-sayac="28|36" value="{e(alt)}" placeholder="ör. ABD Doları, TL · gram">
          <div class="char-meter"><span>Tabloda kodun altında</span><b>0 / 28</b></div></div>
        <div class="frow"><label for="en{sid}-sem">Veri Kaynağı Sembolü</label><input class="finput" id="en{sid}-sem" value="{e(sem)}"{" readonly" if x else ' placeholder="ör. USDTRY"'}>
          <span class="fhint">{"Piyasa veri API'sindeki eşleşme; değişmez." if x else "Piyasa veri API'sindeki sembol; kaydedince değer çekilir."}</span></div>
      </div>
      <div class="kb-fs">
        <div class="kb-fs-tt">Logo</div>
        {gorsel_alani("enstruman_logo", "Enstrüman logosu", "Logo", "İsteğe bağlı · yoksa kısa kod rozeti", bos_yer,
                      ("Logoyu sürükleyin ya da seçin", "1:1 · şeffaf PNG ya da SVG, en az 64×64 · döviz ve kriptoda daire, hissede kare · medya havuzuna girmez"),
                      [("web.kart", "Tablo · 1:1", "r-1x1")], [("mobil.kart", "Mobil · 1:1", "r-1x1")],
                      "Önerilen: <b>32×32</b> (piyasa tabloları), ana sayfa kutusunda 30×30.", "Önerilen: <b>32×32</b>.", dolu=dolu, cekmece=True)}
      </div>
      <div class="kb-fs">
        <div class="kb-fs-tt">Görünüm</div>
        <div class="toggle-row"><span>Şeritte Göster<small>Sitenin üst şeridinde; kur ve altında satış fiyatı</small></span><label class="toggle"><input type="checkbox"{" checked" if ser else ""} aria-label="Şeritte göster"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        {sira("ser", "Şerit", ser)}
        <div class="toggle-row"><span>Widget'ta Göster<small>Ana sayfa piyasa kutusunda</small></span><label class="toggle"><input type="checkbox"{" checked" if wid else ""} aria-label="Widget'ta göster"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        {sira("wid", "Widget", wid)}
      </div>
      <div class="kb-fs">
        <div class="kb-fs-tt">Enstrüman Sayfası</div>
        <div class="frow"><label for="en{sid}-acik">Sayfa Açıklaması</label><textarea class="ftext" id="en{sid}-acik" rows="2" data-sayac="90|120" placeholder="ör. Borsa İstanbul'un 100 hisseden oluşan ana endeksi">{e(acik)}</textarea>
          <div class="char-meter"><span>Enstrüman sayfasının başında, adın üstünde</span><b>0 / 90</b></div></div>
        {gorsel_alani("enstruman_kapak", "Sayfa kapağı", "Sayfa Kapağı", "İsteğe bağlı · yoksa koyu zemin", I("fa-panorama"),
                      ("Sayfa kapağını sürükleyin ya da seçin", "Enstrüman sayfasının başında tam genişlik · web 1440×496, mobil 390×467"),
                      [("web.detay", "Enstrüman sayfası · 2.9:1", "2.9/1")], [("mobil.kart", "Telefon · 5:6", "5/6")],
                      "Önerilen: <b>1440×496</b>; solda ad durur, odağı sağa koyun.", "Önerilen: <b>390×467</b>.", havuz=True, cekmece=True,
                      dolu=("../../veri/gorsel/p133.jpg", "60% 50%", "Yüklenen: 1200×800 JPG.") if eid == "xu100" else None)}
      </div>
    </div>
    <div class="sa-form-panel" id="en{sid}Seo" hidden>
      <div class="kb-fs">
        <div class="kb-fs-tt">Arama Motoru</div>
        <div class="frow"><label for="en{sid}-seob">SEO Başlığı</label>
          <input class="finput" id="en{sid}-seob" data-alan="seo-baslik" data-sayac="60|70" value="{e(seo_b)}">
          <div class="char-meter"><span>Arama sonucunda görünen başlık · addan üretildi</span><b>0 / 60</b></div></div>
        <div class="frow"><label for="en{sid}-seoa">SEO Açıklaması</label>
          <textarea class="ftext" id="en{sid}-seoa" data-alan="seo-aciklama" data-sayac="155|170">{e(seo_a)}</textarea>
          <div class="char-meter"><span>Arama sonucunda başlığın altında</span><b>0 / 155</b></div></div>
        <div class="frow"><label for="en{sid}-slug">Adres</label>
          <div class="slug-wrap"><span class="slug-pre">dadahaber.com/piyasa/</span><input class="finput" id="en{sid}-slug" data-alan="slug" value="{e(slug)}"></div>
          <span class="fhint">Değiştirilirse eski adres yeniye yönlendirilir.</span></div>
        <div class="frow"><span class="flabel">Arama Sonucu Önizlemesi</span>
          <div class="serp"><div class="serp-url"><span class="serp-fav kb-logo-isaret"></span><span>dadahaber.com › piyasa › <span data-alan="slug">{e(slug)}</span></span></div>
          <div class="serp-title" data-alan="seo-baslik">{e(seo_b)}</div><div class="serp-desc" data-alan="seo-aciklama">{e(seo_a)}</div></div></div>
      </div>
    </div>
  </div>
"""


def en_sablonlar(x):
    eid, ad, kisa, alt, sem, tur, logo, deg, ser, wid, acik = x
    return f"""<template id="enGor-{eid}" data-baslik="{e(ad)}" data-alt="{EN_TUR[tur][0]} · {e(kisa)} · 15 dk gecikmeli">
  <div class="kb-fs"><div class="rcp-cell">{en_isaret(x)}<div class="rcp-id"><div class="rcp-name">{e(ad)}</div><div class="rcp-by">{e(kisa)} · {e(alt)}</div></div></div>
    <div class="sa-durum">
      <div><span>Son Değer</span><b>{e(deg)}</b></div><div><span>Tür</span><b>{EN_TUR[tur][0]}</b></div>
      <div><span>Şerit</span><b>{f"{ser}. sıra" if ser else "Gösterilmiyor"}</b></div><div><span>Widget</span><b>{f"{wid}. sıra" if wid else "Gösterilmiyor"}</b></div>
      <div><span>Logo</span><b>{"Yüklü" if logo else "Yok · kısa kod rozeti"}</b></div><div><span>Veri Kaynağı</span><b>Piyasa veri API · {e(sem)}</b></div>
    </div></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="enDz-{eid}">{I("fa-pen")}Düzenle</button></div>
</template>
<template id="enDz-{eid}" data-baslik="{e(ad)} · Düzenle" data-alt="Enstrüman · sonraki güncellemede sitede" data-zorunlu-kayit="ozel-dikeyler.enstruman">
{en_form(eid, x)}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="enGor-{eid}" data-bildir-sonra="Enstrüman kaydedildi; şeritte ve piyasa sayfalarında sonraki güncellemede görünür, önceki hal denetim izinde">{I("fa-floppy-disk")}Kaydet</button></div>
</template>
"""


def en_liste():
    canli = [x for x in ENST if x[0] not in EN_COP]
    gorunum = [("", "Bütün Görünümler", ""), ("serit", "Şeritte", str(EN_SERIT)), ("widget", "Widget'ta", str(EN_WIDGET)), ("sayfa", "Yalnız Sayfada", str(sum(1 for x in canli if not x[8] and not x[9])))]
    bos_eylem = chr(10) + '            <button type="button" class="pe-tag" data-tanim="enYeni">' + I("fa-plus") + 'Yeni Enstrüman</button>'
    durumlar = " ".join(EN_TUR)
    return f"""      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-coins")}Enstrümanlar<span class="fs-ek">Değer kaynaktan gelir; ad, logo, görünüm ve sıra buradan</span></div>
        <div class="kb-bant bilgi">{I("fa-circle-info")}<span><b>{len(canli)} enstrüman · {EN_SERIT} şeritte · {EN_WIDGET} widget'ta.</b> Değişiklik bir sonraki güncellemede sitede görünür; logo yoksa kısa kod rozeti çıkar.</span><button type="button" class="btn btn-acc btn-sm kb-bant-eylem" data-tanim="enYeni">{I("fa-plus")}Yeni Enstrüman</button></div>
        <div data-liste data-liste-ad="enstrüman" data-sayfa-boy="25" data-liste-cop-not="Enstrüman şeritten, widget'tan ve piyasa sayfalarından kalkar; Çöp sekmesine taşınır" aria-label="Piyasa enstrümanları">
          <h2 class="sr-only">Piyasa enstrümanları</h2>
          <div class="kb-liste-ust">
            <div class="chips" role="tablist" aria-label="Türe göre">
              <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
              {"".join(f'<button type="button" class="chip" role="tab" aria-selected="false" data-sekme="{k}">{v[0]}<span class="ch-cnt">0</span></button>' for k, v in EN_TUR.items())}
            </div>
            <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
          </div>
          <div class="filter-bar">
            <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="enAra">Enstrümanlarda Ara</label><input id="enAra" type="search" data-liste-ara placeholder="Ad, kod ya da sembol ara" autocomplete="off"></div>
            {secim("enSuzGor", gorunum, etk="Görünüm:", bos="Tümü", suz="gorunum")}
            <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
          </div>
          <div class="kb-toplu" hidden>
            <b data-secili-say>0 enstrüman seçildi</b><span class="kb-toplu-ayir"></span>
            <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe Taşı</span></button>
            <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi Temizle</button>
          </div>
          <div class="ptable-wrap"><table class="ptable">
            <thead><tr><th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün enstrümanları seç"></th><th class="kb-ana">Enstrüman</th><th class="say kb-gizle-m">Son Değer</th><th class="say">Şerit</th><th class="say kb-gizle-m">Widget</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
            <tbody data-satirlar>{"".join(en_satir(x) for x in ENST)}</tbody>
{durum_govdeleri(6, "fa-coins", "Henüz enstrüman yok", "Piyasa veri API'sinden enstrüman ekleyin; şeritte ve piyasa sayfalarında görünür.", "Enstrümanlar yüklenemedi", "Piyasa veri API yanıt vermiyor. Entegrasyonlar ekranından bağlantıyı kontrol edin.", bos_eylem=bos_eylem, iskelet='<td></td><td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td><td class="kb-gizle-m"><span></span></td><td><span></span></td><td class="kb-gizle-m"><span></span></td><td></td>', yeniden="veri.html")}          </table></div>
{pager()}
          <div class="pnl-menu kb-diger-menu" role="menu">
            <div class="kb-dm-grup" data-durum-icin="{durumlar}">Enstrüman</div>
            <button type="button" data-durum-icin="{durumlar}" data-bildir="Enstrüman sayfası sitede açılır (prototip)">{I("fa-arrow-up-right-from-square")}Sitede Görüntüle</button>
            <button type="button" data-durum-icin="{durumlar}" data-onay-baslik="Değer kaynaktan yenilensin mi?" data-onay-metin="Son değer piyasa veri API'sinden yeniden çekilir; ad, logo ve sıralar korunur." data-onay-evet="Yenile" data-onay-ikon="fa-rotate" data-bildir-sonra="Enstrüman verisi kuyruğa alındı">{I("fa-rotate")}API'den Yenile</button>
            <button type="button" data-durum-icin="{durumlar}" data-roller="super gyy" data-bildir="Denetim izi bu enstrümana süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim İzinde Gör</button>
            <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten Geri Al</button>
            <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı Olarak Sil</button>
          </div>
        </div>
      </div>
"""


def en_yeni():
    return f"""<template id="enYeni" data-baslik="Yeni Enstrüman" data-alt="Piyasa veri API'sinden · şeritte ve sayfalarda" data-zorunlu-kayit="ozel-dikeyler.enstruman">
{en_form("yeni")}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="enEklendi" data-bildir-sonra="Enstrüman eklendi; değer kaynaktan çekiliyor, denetim izine yazıldı">{I("fa-plus")}Ekle</button></div>
</template>
<template id="enEklendi" data-baslik="Enstrüman eklendi" data-alt="Listede ve piyasa sayfalarında">
  <div class="pnl-empty"><div class="pe-ico">{I("fa-circle-check")}</div><h2>Enstrüman eklendi</h2><p>Değeri bir sonraki güncellemede kaynaktan gelir; listeden düzenleyip silebilirsiniz.</p></div>
</template>
{"".join(en_sablonlar(x) for x in ENST)}"""


def sayfa_veri():
    pyasa = soz["piyasa"]["araclar"]
    serit = [a["ad"] for a in pyasa if a.get("serit")]
    havuz = json.dumps([a["ad"] for a in pyasa], ensure_ascii=False)
    cip = "".join(f'<span class="kb-cip" data-deger="{e(a)}"><span>{e(a)}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for a in serit)
    sehirler = [(s, s, "") for s in ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Trabzon", "Konya", "Gaziantep"]]
    h = soz["hava"]["simdi"]
    s = bas("Veri Bantları", "veri")
    s += f"""
<!-- VERİ BANTLARI (D4, ayar ekranı kalıbı): piyasa, hava, namaz vakitleri, deprem. Her birinde kaynak önceliği, güncelleme periyodu,
     önbellek süresi, hata davranışı; durumlar kb-saglik dilinde. Bağlantı ve API anahtarı Entegrasyonlar'da (gizli değer burada yok).
     Piyasa sekmesinde enstrüman listesi (sayfadaki tek liste; emsal Canlı Masa › Akış): kayıt çekmecede (Detay · SEO), logo
     (ozel-dikeyler.enstruman_logo; yoksa kısa kod rozeti), şerit ve widget görünürlüğü ile sırası, sayfa kapağı (enstruman_kapak).
     Liste işlemleri anında uygulanır, kaydet çubuğuna girmez; şeritte görünenler "Şerit" sütunundan gelir (eski çip girişi kalktı). -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Veri Bantları</h1>
      <div class="ph-sub">Sitenin üst şeridi, ana sayfa kutuları ve servis sayfaları · son kontrol 16.04</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="entegrasyonlar.liste" data-roller="super" href="../../cekirdek/entegrasyonlar/index.html">{I("fa-plug")}Entegrasyonlar</a>
    </div>
  </div>

  <section class="pnl-card dash-row" aria-labelledby="vbDurum">
    <div class="pc-head"><h2 class="pc-title" id="vbDurum">{I("fa-signal")}Bant Durumu</h2><span class="kb-kap-alt">Son kontrol 16.04</span></div>
    <div class="pc-body"><div class="kb-saglik-izgara">
      <a class="kb-saglik" href="veri.html?sekme=vbPiyasa"><span class="kb-saglik-bas"><span class="status-nokta"></span>Piyasa</span><span class="kb-saglik-deger">{soz["piyasa"]["guncelleme"]}</span><span class="kb-saglik-meta">{len(ENST) - len(EN_COP)} enstrüman · 15 dk gecikmeli · Dolar {next(a["deger"] for a in pyasa if a["ad"] == "Dolar")}</span></a>
      <a class="kb-saglik uyari" href="veri.html?sekme=vbHava"><span class="kb-saglik-bas"><span class="status-nokta"></span>Hava</span><span class="kb-saglik-deger">16.00</span><span class="kb-saglik-meta">81 il · İstanbul {h["sicaklik"]}°, {h["durum"].lower()} · turuncu kod uyarısı şeritte</span></a>
      <a class="kb-saglik" href="veri.html?sekme=vbNamaz"><span class="kb-saglik-bas"><span class="status-nokta"></span>Namaz Vakitleri</span><span class="kb-saglik-deger">00.10</span><span class="kb-saglik-meta">81 il ve 40 yurt dışı şehri · günde bir</span></a>
      <a class="kb-saglik" href="veri.html?sekme=vbDeprem"><span class="kb-saglik-bas"><span class="status-nokta"></span>Deprem</span><span class="kb-saglik-deger">13.58</span><span class="kb-saglik-meta">Son: Sındırgı (Balıkesir) 2,8 · en büyük 4,1 · AFAD</span></a>
    </div></div>
  </section>

  <div class="form-layout">
  <section class="pnl-card" id="vbForm" data-form data-sekmeli aria-label="Veri bantları ayarları">
    <div class="sa-form-tabs" role="tablist" aria-label="Bantlar">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="vbPiyasa">{I("fa-chart-line")}Piyasa</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="vbHava">{I("fa-cloud-sun")}Hava</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="vbNamaz">{I("fa-mosque")}Namaz Vakitleri</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="vbDeprem">{I("fa-house-crack")}Deprem</button>
    </div>

    <div class="sa-form-panel" id="vbPiyasa" role="tabpanel">
      <div class="form-sec">
{saglayicilar("vbP", [("Piyasa veri API", "Döviz, altın, borsa, emtia · 15 dk gecikmeli lisans", "ok", "Bağlı", "piyasa"), ("TCMB EVDS", "Gösterge kurlar ve politika faizi · yedek", "ok", "Hazır", ""), ("Borsa İstanbul gecikmeli veri", "Endeksler · yedek", "ok", "Hazır", ""), ("EPDK akaryakıt fiyatları", "Akaryakıt · günde bir", "ok", "Bağlı", "")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbP", 1, "Dakika", 60, "Saniye", gecikme=15)}        <div class="toggle-row kb-ust-bosluk"><span>Piyasa Kapalıyken Çekme<small>Hafta sonu ve resmî tatilde son kapanış gösterilir; kaynak kotası harcanmaz</small></span><label class="toggle"><input type="checkbox" checked aria-label="Piyasa Kapalıyken Çekme"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
{hata_davranis("vbP")}      </div>
{en_liste()}    </div>

    <div class="sa-form-panel" id="vbHava" role="tabpanel" hidden>
      <div class="form-sec">
{saglayicilar("vbH", [("Hava durumu API", "81 il · 6 günlük ve saatlik tahmin", "ok", "Bağlı", "hava"), ("Meteoroloji Genel Müdürlüğü", "Resmî uyarılar (sarı, turuncu, kırmızı kod)", "ok", "Hazır", "")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbH", 30, "Dakika", 15, "Dakika")}        <div class="frow kb-ust-bosluk"><span class="flabel">Varsayılan Şehir</span>{secim("vbHSehir", sehirler, deger="İstanbul", bos="Şehir seçin", ara="Şehir ara")}<span class="fhint">Konum izni vermeyen ya da şehir seçmemiş okura gösterilir.</span></div>
        <div class="toggle-row kb-ust-bosluk"><span>Turuncu ve Kırmızı Kod Uyarısını Şeritte Göster<small>Meteoroloji uyarısı süresince sitenin üstünde uyarı şeridi çıkar</small></span><label class="toggle"><input type="checkbox" checked aria-label="Hava uyarısını şeritte göster"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
{hata_davranis("vbH")}      </div>
    </div>

    <div class="sa-form-panel" id="vbNamaz" role="tabpanel" hidden>
      <div class="form-sec">
{saglayicilar("vbN", [("Diyanet İşleri Başkanlığı", "81 il ve yurt dışı şehirleri · resmî vakitler", "ok", "Bağlı", "namaz")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbN", 1, "Gün", 24, "Saat")}        <div class="frow kb-ust-bosluk"><span class="flabel">Varsayılan Şehir</span>{secim("vbNSehir", sehirler, deger="İstanbul", bos="Şehir seçin", ara="Şehir ara")}</div>
        <div class="toggle-row kb-ust-bosluk"><span>Yurt Dışı Şehirleri<small>Namaz vakitleri sayfasında 40 yurt dışı şehri listelenir</small></span><label class="toggle"><input type="checkbox" checked aria-label="Yurt Dışı Şehirleri"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
{hata_davranis("vbN")}      </div>
    </div>

    <div class="sa-form-panel" id="vbDeprem" role="tabpanel" hidden>
      <div class="form-sec">
{saglayicilar("vbD", [("AFAD", "Son depremler · resmî kaynak", "ok", "Hazır", ""), ("Kandilli Rasathanesi", "Son depremler · yedek", "ok", "Hazır", "")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbD", 1, "Dakika", 30, "Saniye")}        <div class="form-grid kb-iki-sutun kb-ust-bosluk">
          <div class="frow"><label for="vbDMin">Listede En Küçük Büyüklük</label><div class="kb-birim"><input class="finput" id="vbDMin" inputmode="decimal" value="2,0"><span>büyüklük</span></div><span class="fhint">Afet ve Acil Durum sayfasındaki “Son depremler” listesi.</span></div>
          <div class="frow"><label for="vbDSerit">Şeritte Gösterme Eşiği</label><div class="kb-birim"><input class="finput" id="vbDSerit" inputmode="decimal" value="4,0"><span>ve üstü</span></div><span class="fhint">Bu büyüklük ve üstündeki deprem 6 saat şeritte kalır.</span></div>
        </div>
        <div class="toggle-row kb-ust-bosluk"><span>5,0 ve Üstünde Editörlere Haber Ver<small>Panelde bildirim; son dakika ve push kararı editörde kalır</small></span><label class="toggle"><input type="checkbox" checked aria-label="Büyük depremde editörlere haber ver"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
{hata_davranis("vbD", "gizle")}      </div>
    </div>
  </section>

  <aside class="side-card" aria-label="Son Değişiklikler">
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-clock-rotate-left")}Son Değişiklikler</h2></div>
      <div class="pc-body sa-gecmis">
        <div><b>Hava uyarısı şeritte açıldı</b><span>Ayşe Yıldız · 23.11.2026 08.10</span></div>
        <div><b>Şeride Gümüş eklendi</b><span>Selin Aydemir · 20.11.2026 11.45</span></div>
        <div><b>Deprem periyodu 5 dk → 1 dk</b><span>Selin Aydemir · 12.11.2026 09.30</span></div>
        <a class="kb-bag" data-hedef="denetim-izi.liste" href="../../cekirdek/denetim-izi/index.html">Denetim izinde bütün kayıtlar</a>
      </div>
    </section>
  </aside>
  </div>

  <div class="kb-kaydet" data-form-icin="vbForm">
    <div class="kk-durum">{I("fa-circle-check")}<span>Kaydedildi · 23.11.2026 08.10 · Ayşe Yıldız</span></div>
    <div class="kk-sag"><button type="button" class="btn btn-acc btn-sm" data-kaydet data-kaydet-metin="Kaydedildi" data-bildir="Bant ayarları kaydedildi; sonraki güncellemede geçerli, önceki hal denetim izinde">{I("fa-floppy-disk")}Kaydet</button></div>
  </div>
</main>
</div>
{en_yeni()}"""
    s += son()
    return s


# ================================================================== BURÇLAR (kimlik görselleri işi, Beyar 25.11.2026)
# Alanlar public sitenin astroloji.html (12'li ızgara: ikon, ad, tarih aralığı; günlük yorum dört başlık) ve burc.html (kapak, başlık, spot,
# yazar, element, nitelik, yönetici gezegen, sembol, günlük yorum, rehber metni) sayfalarından. 12 burç sabittir: eklenmez, silinmez.
ELEMENT = {"Ateş": "fa-fire", "Toprak": "fa-mountain", "Hava": "fa-wind", "Su": "fa-droplet"}  # sitedeki ızgara ikonları (astroloji.html .bz-izg)
NITELIK = ["Öncü", "Sabit", "Değişken"]
GEZEGEN = ["Güneş", "Ay", "Merkür", "Venüs", "Mars", "Jüpiter", "Satürn", "Uranüs", "Neptün", "Plüton"]
AY_KISA = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
AY_UZUN = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
BURCLAR = [
    # id, ad, başlangıç (gün, ay), bitiş, element, nitelik, yönetici gezegen, günlük yorum (bugün yayımlandı mı)
    ("koc", "Koç", (21, 3), (19, 4), "Ateş", "Öncü", "Mars", True), ("boga", "Boğa", (20, 4), (20, 5), "Toprak", "Sabit", "Venüs", True),
    ("ikizler", "İkizler", (21, 5), (20, 6), "Hava", "Değişken", "Merkür", True), ("yengec", "Yengeç", (21, 6), (22, 7), "Su", "Öncü", "Ay", True),
    ("aslan", "Aslan", (23, 7), (22, 8), "Ateş", "Sabit", "Güneş", True), ("basak", "Başak", (23, 8), (22, 9), "Toprak", "Değişken", "Merkür", True),
    ("terazi", "Terazi", (23, 9), (22, 10), "Hava", "Öncü", "Venüs", True), ("akrep", "Akrep", (23, 10), (21, 11), "Su", "Sabit", "Plüton", False),
    ("yay", "Yay", (22, 11), (21, 12), "Ateş", "Değişken", "Jüpiter", True), ("oglak", "Oğlak", (22, 12), (19, 1), "Toprak", "Öncü", "Satürn", True),
    ("kova", "Kova", (20, 1), (18, 2), "Hava", "Sabit", "Uranüs", False), ("balik", "Balık", (19, 2), (20, 3), "Su", "Değişken", "Neptün", False),
]
BURC_GORSEL = {"koc": "../../veri/gorsel/kucuk/p188.jpg"}  # yalnız Koç'un görseli yüklü (sitede burc.html kapağı p188); diğerlerinde element ikonu
BURC_YORUM = [  # public burc.html · Koç · 23.11.2026 08.00 · Seda Uslu
    ("genel", "Genel", "fa-sun", "Gün, yarım kalan işleri toparlamak için uygun. Planladığın bir konuşmayı ertelemek yerine sakin bir dille başlatabilirsin."),
    ("ask", "Aşk ve İlişkiler", "fa-heart", "Yakın çevrende biriyle aranızdaki küçük bir yanlış anlaşılma netleşebilir. Dinlemeye ayırdığın zaman ilişkiyi rahatlatır."),
    ("is", "İş ve Para", "fa-briefcase", "Ekip içinde sorumluluk paylaşımı gündeme gelebilir. Harcamalarda acele etmemek bu hafta için iyi bir tercih."),
    ("saglik", "Sağlık ve Enerji", "fa-heart-pulse", "Enerjin yüksek ama dağınık. Kısa yürüyüşler ve düzenli uyku günü dengelemene yardımcı olur."),
]
BURC_METIN = ("<p>Koç, zodyak kuşağının ilk burcudur ve 21 Mart ile 19 Nisan arasında doğanları kapsar. Geleneksel astrolojide ateş elementiyle ve Mars gezegeniyle ilişkilendirilir.</p>"
              "<h2>Koç burcunun genel özellikleri</h2><p>Astroloji geleneğinde Koç burcu girişkenlik, cesaret ve yeni bir işe ilk adımı atma isteğiyle tanımlanır. Aynı gelenek, sabırsızlığı ve acele karar vermeyi bu burcun zorlandığı yönler olarak sayar.</p>"
              "<h2>Aşkta ve ilişkilerde</h2><p>Burç yorumlarında Koç, ilişkilerde açık sözlü ve doğrudan olarak anlatılır. Ateş grubundaki Aslan ve Yay burçlarıyla uyumlu kabul edilir.</p>"
              "<h2>İş hayatında</h2><p>Liderlik gerektiren, hızlı karar verilen ve rekabetin yüksek olduğu alanlar Koç burcuyla ilişkilendirilen çalışma ortamları arasında sayılır.</p>")


def aralik(b):
    (g1, a1), (g2, a2) = b[2], b[3]
    return f"{g1} {AY_KISA[a1 - 1]} – {g2} {AY_KISA[a2 - 1]}"


def burc_isaret(bid, ad, el, buyuk=False):
    """burç görseli yüklenmişse o, yoksa element ikonu (sitedeki ızgara yer tutucusu)"""
    k = " k-lg" if buyuk else ""
    if bid in BURC_GORSEL and not buyuk:
        return f'<span class="kb-ava" style="background-image:url({BURC_GORSEL[bid]})" role="img" aria-label="{e(ad)} burcu görseli"></span>'
    return f'<span class="kb-ava{k}" title="Burç görseli yok; {el.lower()} elementinin ikonu gösteriliyor">{I(ELEMENT[el])}</span>'


def sayfa_burclar():
    rows = []
    for b in BURCLAR:
        bid, ad, _, _, el, nit, gez, yorum = b
        site = SITE + ("burc.html" if bid == "koc" else f"burc.html?secim={bid}")
        rows.append(f'<tr data-satir="bz-{bid}" data-durum="{"yayinda" if yorum else "eksik"}" data-element="{el}" data-ara="{e(ad + " " + el + " " + nit + " " + gez)}" data-baslik="{e(ad)}" data-href="burc.html?id={bid}">'
                    f'<td class="kb-ana"><div class="rcp-cell">{burc_isaret(bid, ad, el)}<div class="rcp-id"><div class="rcp-name">{e(ad)}</div><div class="rcp-by">{aralik(b)}</div></div></div></td>'
                    f'<td class="kb-gizle-m">{I(ELEMENT[el])} {el}</td>'
                    f'<td class="kb-gizle-t">{nit}</td>'
                    f'<td class="kb-gizle-t">{gez}</td>'
                    f'<td>{"<span class=\"pstat ok\">Bugün 08.00</span>" if yorum else "<span class=\"pstat wait\">Bugün girilmedi</span>"}</td>'
                    f'<td>{row_acts(("href", site), ("href", f"burc.html?id={bid}", "ozel-dikeyler.burc"), None, gor_ad="Sitede Görüntüle")}</td></tr>')
    elemanlar = [("", "Bütün Elementler", "")] + [(k, k, str(sum(1 for b in BURCLAR if b[4] == k))) for k in ELEMENT]
    eksik = sum(1 for b in BURCLAR if not b[7])
    s = bas("Burçlar", "burclar")
    s += f"""
<!-- BURÇLAR (kimlik görselleri işi): 12 burç sabittir (eklenmez, silinmez); satır → Burç Düzenle sayfası (satır → sayfa).
     Burç görseli yoksa sitedeki ızgarada ve listede element ikonu görünür. Günlük yorum her gün burç sayfasından girilir. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Burçlar</h1>
      <div class="ph-sub">12 burç · bugünün yorumu {12 - eksik} burçta yayında, {eksik} burçta girilmedi · sitede Kadın › Astroloji</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" href="{SITE}astroloji.html" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Astroloji Sayfası</a>
    </div>
  </div>

  <div class="kb-bant bilgi dash-row">{I("fa-lock")}<span><b>12 burç sabittir; eklenmez ve silinmez.</b> Ad, tarih aralığı, element, görsel ve rehber metni burç sayfasından düzenlenir; günlük yorum her sabah aynı sayfadan girilir ve sitede astroloji sayfasında, burç sayfasında görünür.</span></div>

  <section class="pnl-card" data-liste data-liste-ad="burç" data-sayfa-boy="25" aria-labelledby="bzListeBas">
    <h2 class="sr-only" id="bzListeBas">Burç listesi</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Günlük yoruma göre">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="yayinda">Yorum Yayında<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="eksik">Yorum Girilmedi<span class="ch-cnt">0</span></button>
      </div>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="bzAra">Burçlarda Ara</label><input id="bzAra" type="search" data-liste-ara placeholder="Burç, element ya da gezegen ara" autocomplete="off"></div>
      {secim("bzSuzEl", elemanlar, etk="Element:", bos="Tümü", suz="element")}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
    </div>
    <div class="ptable-wrap"><table class="ptable">
      <thead><tr><th class="kb-ana">Burç</th><th class="kb-gizle-m">Element</th><th class="kb-gizle-t">Nitelik</th><th class="kb-gizle-t">Yönetici Gezegen</th><th>Günlük Yorum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
      <tbody data-satirlar>{"".join(rows)}</tbody>
{durum_govdeleri(6, "fa-star", "Burç bulunamadı", "12 burç kurulumda gelir; liste boşsa sayfayı yenileyin.", "Burçlar yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", iskelet='<td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="burclar.html")}    </table></div>
{pager(sayfalar=False)}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup">Burç</div>
      <button type="button" data-durum-icin="eksik" data-bildir="Dünkü yorum bugünün tarihiyle taslak olarak kopyalandı (prototip)">{I("fa-copy")}Dünkü Yorumu Kopyala</button>
      <button type="button" data-kopyala>{I("fa-link")}Bağlantıyı Kopyala</button>
      <button type="button" data-roller="super gyy" data-bildir="Denetim izi bu burca süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim İzinde Gör</button>
    </div>
  </section>
</main>
</div>
"""
    s += son()
    return s


def sayfa_burc():
    b = BURCLAR[0]
    bid, ad, (g1, a1), (g2, a2), el, nit, gez, _ = b
    elem = "".join(f'<label class="kb-secenek"><input type="radio" name="bzEl" value="{k}"{" checked" if k == el else ""}>{I(v)}{k}</label>' for k, v in ELEMENT.items())
    nite = "".join(f'<label class="kb-secenek"><input type="radio" name="bzNit" value="{k}"{" checked" if k == nit else ""}>{k}</label>' for k in NITELIK)
    gezo = [(g, g, "") for g in GEZEGEN]
    yazar = [(y["ad"], y["ad"], y.get("unvan", "")) for y in soz["yazarlar"]]
    yorum = "".join(f'<div class="frow"><label for="bzY-{k}">{I(ik)} {a}</label><textarea class="ftext" id="bzY-{k}" rows="3" data-sayac="200|260">{e(t)}</textarea>'
                    f'<div class="char-meter"><span>Akordeonda “{a}” başlığı altında</span><b>0 / 200</b></div></div>' for k, a, ik, t in BURC_YORUM)
    s = bas("Burç Düzenle", "burc")
    s += f"""
<!-- BURÇ DÜZENLE (kimlik görselleri işi): Detay · SEO (burç sayfası sitede var). Alanlar public burc.html ve astroloji.html'den.
     Burç görseli (ozel-dikeyler.burc; fotoğraf: havuzdan seçilir, yüklemede etiketlenir): burç sayfasının başı + ızgara; yoksa element ikonu.
     Tarih aralığı iki saatsiz özel tarih seçici (yıl dikkate alınmaz); element ve nitelik bölmeli seçici (KURAL · seçenek grubu), gezegen
     aranabilir liste; rehber metni zengin metin editörü. Zorunlular kayıtta: ozel-dikeyler.burc. Burç eklenmez ve silinmez (?yeni yok). -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Burç Düzenle</h1>
      <div class="ph-sub">{ad} · {g1} {AY_UZUN[a1 - 1]} – {g2} {AY_UZUN[a2 - 1]} · bugünün yorumu 08.00'de yayımlandı · 3,3 B görüntülenme</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ozel-dikeyler.burclar" href="burclar.html">{I("fa-arrow-left")}Burçlara Dön</a>
      <a class="btn btn-ghost btn-sm" href="{SITE}burc.html" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Sitede Görüntüle</a>
    </div>
  </div>

  <div class="form-layout">
  <section class="pnl-card" id="bzForm" data-form data-sekmeli data-zorunlu-kayit="ozel-dikeyler.burc" aria-label="Burç formu">
{dil_secici("Dil seçici ad, başlık, açıklama, günlük yorum, rehber metni ve SEO alanlarını birlikte değiştirir; tarih aralığı, element, gezegen ve görsel bütün dillerde ortaktır.")}
    <div class="sa-form-tabs" role="tablist" aria-label="Düzenleme sekmeleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="pDetay">{I("fa-file-lines")}Detay</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="pSeo">{I("fa-magnifying-glass-chart")}SEO</button>
    </div>

    <div class="sa-form-panel" id="pDetay" role="tabpanel">
      <div class="form-sec">
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><label for="bzAd">Ad</label>
            <input class="finput kb-buyuk" id="bzAd" data-alan-id="ad" data-alan="baslik" data-sayac="12|16" value="{ad}">
            <div class="char-meter"><span>Izgarada, listede ve burç sayfasında</span><b>0 / 12</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Ad zorunlu.</div></div>
          <div class="frow"><label for="bzSembol">Sembol</label>
            <input class="finput" id="bzSembol" data-sayac="16|24" value="{ad}">
            <div class="char-meter"><span>Burç sayfasının başındaki dört kutudan biri</span><b>0 / 16</b></div></div>
        </div>
        <div class="frow kb-ust-bosluk"><label for="bzBaslik">Sayfa Başlığı</label>
          <input class="finput" id="bzBaslik" data-sayac="60|80" value="{ad} burcu rehberi">
          <div class="char-meter"><span>Addan üretilir · burç sayfasının başlığı</span><b>0 / 60</b></div></div>
        <div class="frow kb-ust-bosluk"><label for="bzSpot">Kısa Açıklama</label>
          <textarea class="ftext" id="bzSpot" rows="2" data-sayac="160|200">{g1} {AY_UZUN[a1 - 1]} – {g2} {AY_UZUN[a2 - 1]} arasında doğanların burcu {ad}; günlük yorum, genel özellikler ve uyumlu burçlar.</textarea>
          <div class="char-meter"><span>Burç sayfasında başlığın altında; paylaşımda açıklama</span><b>0 / 160</b></div></div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-calendar-days")}Tarih Aralığı<span class="fs-ek">Her yıl tekrar eder; yıl dikkate alınmaz</span></div>
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><span class="flabel">Başlangıç</span>
            <div class="kb-tarih-sec" id="bzBas" data-saatsiz data-alan-id="baslangic" data-deger="2026-{a1:02d}-{g1:02d}" data-bos="Gün seçin" data-zorunlu-metin="Burcun başladığı günü seçin">
              <button type="button" class="kb-tarih-btn" data-acilir="bzBasMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
              <div class="pnl-menu kb-tarih-menu" id="bzBasMenu" role="dialog" aria-label="Başlangıç günü seç"></div></div>
            <div class="ferr">{I("fa-circle-exclamation")}Burcun başladığı günü seçin.</div></div>
          <div class="frow"><span class="flabel">Bitiş</span>
            <div class="kb-tarih-sec" id="bzBit" data-saatsiz data-alan-id="bitis" data-deger="2026-{a2:02d}-{g2:02d}" data-bos="Gün seçin" data-zorunlu-metin="Burcun bittiği günü seçin">
              <button type="button" class="kb-tarih-btn" data-acilir="bzBitMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
              <div class="pnl-menu kb-tarih-menu" id="bzBitMenu" role="dialog" aria-label="Bitiş günü seç"></div></div>
            <div class="ferr">{I("fa-circle-exclamation")}Burcun bittiği günü seçin.</div></div>
        </div>
        <span class="fhint">Sitede ızgarada “{aralik(b)}”, burç sayfasında “{g1} {AY_UZUN[a1 - 1]} – {g2} {AY_UZUN[a2 - 1]}” yazar.</span>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-star")}Burç Özellikleri<span class="fs-ek">Burç sayfasının başındaki dört kutu</span></div>
        <div class="frow"><span class="flabel">Element</span><div class="kb-secenek-grup" role="radiogroup" aria-label="Element" data-alan-id="element" data-zorunlu-metin="Elementi seçin">{elem}</div>
          <span class="fhint">Burç görseli yoksa ızgarada ve listede elementin ikonu görünür.</span>
          <div class="ferr">{I("fa-circle-exclamation")}Elementi seçin.</div></div>
        <div class="form-grid kb-iki-sutun kb-ust-bosluk">
          <div class="frow"><span class="flabel">Nitelik</span><div class="kb-secenek-grup" role="radiogroup" aria-label="Nitelik">{nite}</div></div>
          <div class="frow"><span class="flabel">Yönetici Gezegen</span>{secim("bzGez", gezo, deger=gez, bos="Gezegen seçin", ara="Gezegen ara")}</div>
        </div>
      </div>
{gorsel_alani("burc", "Burç görseli", "Burç Görseli", "İsteğe bağlı · yoksa element ikonu görünür", burc_isaret(bid, ad, el, True),
              ("Burç görselini sürükleyin ya da seçin", "Burç sayfasının başı ve astroloji ızgarası · web 1248×520 (2.4:1) ve 48×48, mobil 390×652 (3:5) ve 48×48"),
              [("web.detay", "Burç sayfası · 2.4:1", "r-detay"), ("web.kart", "Izgara · 1:1", "r-1x1")], [("mobil.detay", "Burç sayfası · 3:5", "3/5"), ("mobil.kart", "Izgara · 1:1", "r-1x1")],
              "Önerilen: burç sayfası <b>1248×520</b>, ızgara <b>48×48</b> (daire).", "Önerilen: burç sayfası <b>390×652</b> (telefonda tam ekran), ızgara <b>48×48</b>.",
              ikon="fa-image", havuz=True, dolu=("../../veri/gorsel/p188.jpg", "50% 45%", "Yüklenen: 1200×800 JPG, 179 KB."))}
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-calendar-day")}Günlük Yorum<span class="fs-ek">Astroloji sayfasında “Bugün” kutusunda ve burç sayfasında</span></div>
        <div class="frow"><span class="flabel">Yayın Zamanı</span>
          <div class="kb-tarih-sec" id="bzYayin" data-deger="2026-11-23 08.00" data-bos="Kaydedince o anın saati">
            <button type="button" class="kb-tarih-btn" data-acilir="bzYayinMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
            <div class="pnl-menu kb-tarih-menu" id="bzYayinMenu" role="dialog" aria-label="Tarih ve saat seç"></div></div>
          <span class="fhint">Yorum bu saatte yayına girer ve ertesi günün yorumu gelene kadar kalır.</span></div>
        <div class="form-grid kb-iki-sutun kb-ust-bosluk">{yorum}</div>
        <span class="fhint">Sitede yorumların altında “Burç yorumları eğlence ve kültür içeriğidir” uyarısı sabit durur; burada girilmez.</span>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-align-left")}Rehber Metni<span class="fs-ek">Burç sayfasında günlük yorumun altında</span></div>
        <div class="kb-editor" data-editor-ad="Rehber Metni">
          <div class="kz-alan ke-alan" data-alan-id="metin" data-zorunlu-metin="Rehber metnini yazın">{BURC_METIN}</div>
          <div class="kz-alt"><span data-kz-say></span><span>Sitede burç sayfasında</span></div>
        </div>
      </div>
    </div>

{seo_bolum("pSeo", "Koç burcu: özellikleri, günlük yorum ve uyumlu burçlar | Dada Haber", "21 Mart – 19 Nisan arasında doğanların burcu Koç; günlük burç yorumu, genel özellikler, aşk ve iş hayatı.", "dadahaber.com/astroloji/", "koc-burcu", ["koç burcu", "koç burcu günlük yorum", "koç burcu özellikleri"])}
  </section>

  <aside class="side-card" aria-label="Yayın">
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-paper-plane")}Yayın</h2><span class="status-dot" data-state="yayinda" title="Yayında"></span></div>
      <div class="pc-body sc-stack">
        <div class="sc-field"><span class="flabel">Yazar</span>{secim("bzYazar", yazar, deger="Seda Uslu", bos="Yazar seçin", ara="Yazar ara")}<span class="fhint">Boş bırakılırsa kaydeden editör yazılır.</span></div>
        <div class="sa-durum">
          <div><span>Durum</span><b><span class="pstat ok">Yayında</span></b></div>
          <div><span>Bugünün yorumu</span><b>23.11.2026 08.00</b></div>
          <div><span>Görüntülenme · bugün</span><b>3,3 B</b></div>
        </div>
      </div>
    </section>
{seo_skor(86)}  </aside>
  </div>

  <div class="kb-kaydet" data-form-icin="bzForm">
    <div class="kk-durum">{I("fa-circle-check")}<span>Kaydedildi · 23.11.2026 08.00 · Seda Uslu</span></div>
    <div class="kk-sag">
      <button type="button" class="btn btn-acc btn-sm" data-kaydet data-kaydet-metin="Kaydedildi" data-bildir="Burç kaydedildi; sitede burç sayfası ve astroloji ızgarası güncellendi, önceki hal denetim izinde">{I("fa-floppy-disk")}Kaydet</button>
    </div>
  </div>
</main>
</div>
"""
    s += son(editor=True)
    return s


# ================================================================== RESMÎ İLANLAR
IL_TUR = ["İhale", "Satış", "Kiralama", "Personel"]
ILANLAR = [
    # id, başlık, tür, kurum, yayın, son gün, görüntülenme, durum
    ("kmo-bakim", "Kuzey Marmara Otoyolu bağlantı yollarında bakım ve onarım işi ihale edilecek", "İhale", "Karayolları Genel Müdürlüğü (KGM)", "23.11.2026 09.00", "09.12.2026", "1,8 B", "yayinda"),
    ("dsi-personel", "Devlet Su İşleri 120 sözleşmeli personel alacak", "Personel", "Devlet Su İşleri (DSİ)", "23.11.2026 08.30", "05.12.2026", "6,4 B", "yayinda"),
    ("cankaya-arsa", "Çankaya'da üç parsel arsa açık artırmayla satılacak", "Satış", "Millî Emlak Genel Müdürlüğü", "22.11.2026 16.10", "11.12.2026", "2,2 B", "yayinda"),
    ("alsancak-isyeri", "Alsancak'ta kamuya ait işyeri kiraya verilecek", "Kiralama", "Millî Emlak Genel Müdürlüğü", "22.11.2026 14.40", "03.12.2026", "1,1 B", "yayinda"),
    ("tcdd-peron", "Hızlı tren hattında yolcu peronu yenileme işi ihale edilecek", "İhale", "TCDD", "22.11.2026 11.20", "08.12.2026", "940", "yayinda"),
    ("toki-kayseri", "Kayseri'de konut projesinde kalan daireler satışa çıkarıldı", "Satış", "TOKİ", "21.11.2026 15.00", "15.12.2026", "3,7 B", "yayinda"),
    ("sgk-bilisim", "SGK 60 sözleşmeli bilişim personeli alacak", "Personel", "Sosyal Güvenlik Kurumu (SGK)", "21.11.2026 10.30", "12.12.2026", "5,2 B", "yayinda"),
    ("meb-okul", "Ankara'da 24 derslikli okul binası yapım işi ihale edilecek", "İhale", "Millî Eğitim Bakanlığı (MEB)", "20.11.2026 13.00", "10.12.2026", "1,4 B", "yayinda"),
    ("ogm-tomruk", "2.400 metreküp tomruk açık artırmayla satılacak", "Satış", "Orman Genel Müdürlüğü (OGM)", "20.11.2026 09.40", "02.12.2026", "620", "yayinda"),
    ("dhmi-antalya", "Antalya Havalimanı'nda ticari alan kiralama ihalesi", "Kiralama", "DHMİ", "19.11.2026 16.00", "07.12.2026", "1,9 B", "yayinda"),
    ("iskur-danisman", "İŞKUR 400 iş ve meslek danışmanı alımı için başvuru açtı", "Personel", "İŞKUR", "19.11.2026 11.00", "06.12.2026", "8,1 B", "yayinda"),
    ("dmo-kirtasiye", "Kamu kurumları için toplu kırtasiye alımı ihalesi", "İhale", "Devlet Malzeme Ofisi (DMO)", "23.11.2026 15.45", "04.12.2026", "1,2 B", "yayinda"),
    ("ptt-arac", "PTT 35 hizmet aracını açık artırmayla satacak", "Satış", "PTT", "", "18.12.2026", "—", "taslak"),
    ("kgm-tuz", "Kış bakımı için 12 bin ton yol tuzu alım ihalesi", "İhale", "Karayolları Genel Müdürlüğü (KGM)", "02.11.2026 10.00", "20.11.2026", "2,6 B", "suresi"),
    ("tcdd-vagon", "Hurda vagon satışı ihalesi", "Satış", "TCDD", "28.10.2026 09.00", "15.11.2026", "880", "cop"),
]
IL_DURUM = {"yayinda": ("ok", "Yayında"), "taslak": ("off", "Taslak"), "suresi": ("wait", "Süresi Doldu"), "cop": ("off", "Çöpte")}


def sayfa_ilanlar():
    rows = []
    for iid, b, tur, kur, yay, son_, gor, dur in ILANLAR:
        sinif, dad = IL_DURUM[dur]
        kisa = re.search(r"\(([^)]+)\)", kur)
        kisa = kisa.group(1) if kisa else kur
        rows.append(f'<tr data-satir="il-{iid}" data-durum="{dur}" data-tur="{tur}" data-kurum="{e(kur)}" data-ara="{e(b + " " + tur + " " + kur)}" data-baslik="{e(b)}" data-href="ilan.html?id={iid}"{" data-onceki=\"suresi\"" if dur == "cop" else ""}>'
                    f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(b)}"></td>'
                    f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name" title="{e(b)}">{e(b)}</div><div class="rcp-by">{e(tur)} · {e(kisa)}</div></div></td>'
                    f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if not yay else ""}">{e(yay or "—")}</span></td>'
                    f'<td><span class="kb-tarih">{e(son_)}</span></td>'
                    f'<td class="say kb-gizle-t">{e(gor)}</td>'
                    f'<td><span class="pstat {sinif}">{dad}</span></td>'
                    f'<td>{row_acts(("href", SITE + "resmi-ilan-detay.html") if dur == "yayinda" else ("href", f"ilan.html?id={iid}", "ozel-dikeyler.ilan"), ("href", f"ilan.html?id={iid}", "ozel-dikeyler.ilan"), "sil", gor_ad="Sitede Görüntüle" if dur == "yayinda" else "Önizle")}</td></tr>')
    turler = [("", "Bütün Türler", "")] + [(t, t, str(sum(1 for x in ILANLAR if x[2] == t and x[7] != "cop"))) for t in IL_TUR]
    kurumlar = [("", "Bütün kurumlar", "")] + [(k, k, "") for k in sorted({x[3] for x in ILANLAR})]
    s = bas("Resmî İlanlar", "ilanlar")
    s += f"""
<!-- RESMÎ İLANLAR (D4; B-26 bekliyor, alanlar varsayım): liste + ilan düzenle sayfası (satır → sayfa). Türler sitedeki sekmelerle aynı. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Resmî İlanlar</h1>
      <div class="ph-sub">1.284 ilan yayında · bugün 2 yeni · 1 taslak · son başvurusu geçenler kendiliğinden “Süresi doldu”ya geçer</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-acc btn-sm" data-hedef="ozel-dikeyler.ilan" data-hedef-ek="?yeni=1" href="ilan.html?yeni=1">{I("fa-plus")}Yeni İlan</a>
    </div>
  </div>

  <section class="pnl-card" data-liste data-liste-ad="ilan" data-sayfa-boy="25" data-liste-cop-not="İlan yayından kalkar ve Çöp sekmesine taşınır" aria-labelledby="ilListeBas">
    <h2 class="sr-only" id="ilListeBas">İlan listesi</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Duruma göre">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi" data-taban="1305">Tümü<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="yayinda" data-taban="1272">Yayında<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="taslak" data-taban="0">Taslak<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="suresi" data-taban="33">Süresi Doldu<span class="ch-cnt">0</span></button>
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop" data-taban="0">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="ilAra">İlanlarda Ara</label><input id="ilAra" type="search" data-liste-ara placeholder="Başlık, kurum ya da tür ara" autocomplete="off"></div>
      {secim("ilSuzTur", turler, etk="Tür:", bos="Tümü", suz="tur")}
      {secim("ilSuzKurum", kurumlar, etk="Kurum:", bos="Tümü", ara="Kurum ara", suz="kurum")}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>
    <div class="kb-toplu" hidden>
      <b data-secili-say>0 ilan seçildi</b><span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen ilanlar yayından kaldırılıp taslağa alındı">{I("fa-eye-slash")}<span>Yayından kaldır</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe Taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button>
    </div>
    <div class="ptable-wrap"><table class="ptable">
      <thead><tr><th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün ilanları seç"></th><th class="kb-ana">İlan</th><th class="kb-gizle-m">Yayın</th><th>Son gün</th><th class="say kb-gizle-t">Görüntülenme</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
      <tbody data-satirlar>{"".join(rows)}</tbody>
{durum_govdeleri(7, "fa-bullhorn", "Henüz ilan yok", "İlk resmî ilanı ekleyin; yayımlanan ilanlar sitede Resmî İlanlar sayfasında listelenir.", "İlanlar yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", bos_eylem=chr(10) + '            <a class="pe-tag" data-hedef="ozel-dikeyler.ilan" data-hedef-ek="?yeni=1" href="ilan.html?yeni=1">' + I("fa-plus") + 'Yeni ilan</a>', iskelet='<td></td><td><div class="rcp-id"><span></span></div></td><td class="kb-gizle-m"><span></span></td><td><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="ilanlar.html")}    </table></div>
{pager(son_=52)}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup" data-durum-icin="yayinda taslak suresi">Yayın</div>
      <button type="button" data-durum-icin="taslak" data-onay-baslik="İlan yayımlansın mı?" data-onay-metin="İlan sitede Resmî İlanlar sayfasında hemen görünür. Zorunlu alanları eksikse düzenleme ekranında işaretlenir." data-onay-evet="Yayımla" data-onay-ikon="fa-paper-plane" data-sonra-durum="yayinda" data-sonra-durum-ad="Yayında" data-sonra-durum-sinif="ok" data-bildir-sonra="İlan yayımlandı">{I("fa-paper-plane")}Şimdi yayımla</button>
      <button type="button" data-durum-icin="yayinda" data-onay-baslik="İlan yayından kaldırılsın mı?" data-onay-metin="Önce: yayında → Sonra: taslak. İlan sitede görünmez olur; denetim izine yazılır." data-onay-evet="Yayından kaldır" data-onay-tehlike data-onay-ikon="fa-eye-slash" data-sonra-durum="taslak" data-sonra-durum-ad="Taslak" data-sonra-durum-sinif="off" data-bildir-sonra="İlan yayından kaldırıldı">{I("fa-eye-slash")}Yayından kaldır</button>
      <button type="button" data-durum-icin="suresi" data-bildir="Son başvuru tarihi düzenleme ekranında uzatılır (prototip)">{I("fa-calendar-plus")}Süreyi uzat</button>
      <div class="pmenu-div" data-durum-icin="yayinda taslak suresi"></div>
      <button type="button" data-durum-icin="yayinda taslak suresi" data-bildir="Kopyası taslak olarak oluşturuldu (prototip)">{I("fa-copy")}Kopyasını oluştur</button>
      <button type="button" data-durum-icin="yayinda" data-kopyala>{I("fa-link")}Bağlantıyı kopyala</button>
      <button type="button" data-roller="super gyy" data-durum-icin="yayinda taslak suresi" data-bildir="Denetim izi bu kayda süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
      <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten geri al</button>
      <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı olarak sil</button>
    </div>
  </section>
</main>
</div>
"""
    s += son()
    return s


def sayfa_ilan():
    iid, b, tur, kur, yay, son_, gor, dur = ILANLAR[0]
    kurumlar = json.dumps(sorted({x[3] for x in ILANLAR}), ensure_ascii=False)
    turler = [(t, t, {"İhale": "Yapım, mal ve hizmet alımı", "Satış": "Taşınmaz ve taşınır satışı", "Kiralama": "Kamu taşınmazı kiralama", "Personel": "Kamu personel alımı"}[t]) for t in IL_TUR]
    s = bas("İlan Düzenle", "ilan", ' data-yeni-baslik="Yeni İlan"')
    s += f"""
<!-- İLAN DÜZENLE (D4; B-26 bekliyor → alanlar varsayım): Detay · SEO (8b: resmî ilan SEO ●, zengin metin ●, zamanlama ●, görsel —).
     Belge kb-dosya data-tur="belge". Kurum havuzdan (yerinde yönetilir, B2). Zorunlular kayıtta: ozel-dikeyler.ilan. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1 data-yeni-metin="Yeni İlan">İlan Düzenle</h1>
      <div class="ph-sub" data-yeni-metin="Taslak · henüz kaydedilmedi">{tur} · Karayolları Genel Müdürlüğü · {yay}'da yayımlandı · {gor} görüntülenme</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ozel-dikeyler.ilanlar" href="ilanlar.html">{I("fa-arrow-left")}İlanlara Dön</a>
      <a class="btn btn-ghost btn-sm" data-yeni-gizle href="{SITE}resmi-ilan-detay.html" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Sitede Görüntüle</a>
    </div>
  </div>

  <div class="form-layout">
  <section class="pnl-card" id="ilForm" data-form data-sekmeli data-zorunlu-kayit="ozel-dikeyler.ilan" aria-label="İlan formu">
{dil_secici("Dil seçici başlık, ilan metni ve SEO alanlarını birlikte değiştirir; kurum, tarihler ve belge bütün dillerde ortaktır.")}
    <div class="sa-form-tabs" role="tablist" aria-label="Düzenleme sekmeleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="pDetay">{I("fa-file-lines")}Detay</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="pSeo">{I("fa-magnifying-glass-chart")}SEO</button>
    </div>

    <div class="sa-form-panel" id="pDetay" role="tabpanel">
      <div class="form-sec"><div class="form-grid">
        <div class="frow"><label for="ilBaslik">Başlık</label>
          <input class="finput kb-buyuk" id="ilBaslik" data-alan-id="baslik" data-alan="baslik" data-sayac="90|110" value="{e(b)}">
          <div class="char-meter"><span>Listede ve ilan sayfasında; SEO başlığı buradan üretilir</span><b>0 / 90</b></div>
          <div class="ferr">{I("fa-circle-exclamation")}Başlık zorunlu.</div></div>
        <div class="frow"><label for="ilOzet">Kısa Açıklama</label>
          <textarea class="ftext" id="ilOzet" data-sayac="160|200" rows="2">Kuzey Marmara Otoyolu bağlantı yollarında bakım ve onarım işi açık ihale usulüyle verilecek; teklifler 9 Aralık'a kadar alınacak.</textarea>
          <div class="char-meter"><span>İlan sayfasında başlığın altında; paylaşımda açıklama</span><b>0 / 160</b></div></div>
      </div></div>
      <div class="kb-ai-adim" data-ai-adim data-ai-kaynak="#ilBaslik" data-yeni-goster hidden>
        <div class="kaa-bas"><span class="kaa-ikon">{I("fa-wand-magic-sparkles")}</span><div><b>Gerisini AI ile üret</b><span data-ai-durum>Başlığı yazın ve ilan metnini yapıştırın; işaretli bölümler bunlardan üretilir. AI ilan metnini değiştirmez.</span></div></div>
        <div class="kaa-secim" role="group" aria-label="Üretilecek bölümler"><label class="kb-secenek"><input type="checkbox" value="ilozet" checked>Kısa Açıklama</label><label class="kb-secenek"><input type="checkbox" value="seo" checked>SEO</label></div>
        <div class="kaa-alt"><button type="button" class="btn btn-acc btn-sm" data-ai-uret disabled>{I("fa-wand-magic-sparkles")}Gerisini Üret</button><span class="fhint" data-ai-neden>Önce başlık</span></div>
      </div>
      <div class="form-sec">
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><span class="flabel">İlan Türü</span>
            {secim("ilTur", turler, deger=tur, bos="Tür seçin", ek=' data-alan-id="tur" data-zorunlu-metin="İlan türünü seçin"')}
            <span class="fhint">Sitedeki sekmeler: İhale, Satış, Kiralama, Personel.</span>
            <div class="ferr">{I("fa-circle-exclamation")}İlan türünü seçin.</div></div>
          <div class="frow"><span class="flabel">Kurum</span>
            <div class="kb-cip-girdi" data-alan-id="kurum" data-zorunlu-metin="İlanı veren kurumu seçin" data-havuz-yonet data-kullanim-birim="ilanda" data-havuz='{e(kurumlar)}'><span class="kb-cip" data-deger="{e(kur)}"><span>{e(kur)}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><input type="text" placeholder="Kurum ara; yoksa yazıp ekleyin" aria-label="Kurum"><div class="pnl-menu kb-cip-oneri"></div></div>
            <div class="ferr">{I("fa-circle-exclamation")}İlanı veren kurumu seçin.</div></div>
          <div class="frow"><label for="ilNo">İlan ya da İhale Kayıt Numarası</label><input class="finput" id="ilNo" value="İKN 2026/1849302"><span class="fhint">İhalede EKAP kayıt numarası; isteğe bağlı.</span></div>
          <div class="frow"><span class="flabel">Son Başvuru</span>
            <div class="kb-tarih-sec" id="ilBitis" data-alan-id="bitis" data-deger="2026-12-09 10.00" data-enaz="bugun" data-zorunlu-metin="Son başvuru tarihini seçin">
              <button type="button" class="kb-tarih-btn" data-acilir="ilBitisMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
              <div class="pnl-menu kb-tarih-menu" id="ilBitisMenu" role="dialog" aria-label="Tarih ve saat seç"></div></div>
            <span class="fhint">Sitede kartta “Son gün”; geçince ilan “Süresi doldu”ya geçer.</span>
            <div class="ferr">{I("fa-circle-exclamation")}Son başvuru tarihini seçin.</div></div>
        </div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-align-left")}İlan Metni<span class="fs-ek">Kurumun yayımladığı metin; değiştirmeden aktarın</span></div>
        <div class="kb-editor" data-editor-ad="İlan Metni">
          <div class="kz-alan ke-alan" data-alan-id="metin" data-zorunlu-metin="İlan metnini yazın ya da yapıştırın"><h2>İşin adı, niteliği ve miktarı</h2><p>Kuzey Marmara Otoyolu bağlantı yollarında (Kurtköy–Akyazı kesimi) üstyapı bakım ve onarım işi. Ayrıntılı bilgi ihale dokümanında yer almaktadır.</p><h2>İhale usulü ve yeri</h2><p>4734 sayılı Kamu İhale Kanunu'nun 19. maddesine göre açık ihale usulüyle, Karayolları 1. Bölge Müdürlüğü ihale salonunda yapılacaktır.</p><h2>Son teklif verme tarihi</h2><p>9 Aralık 2026 saat 10.00. Teklifler elektronik ortamda EKAP üzerinden verilecektir.</p></div>
          <div class="kz-alt"><span data-kz-say></span><span>Sitede ilan sayfasında</span></div>
        </div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-file-pdf")}Belgeler<span class="fs-ek">İsteğe bağlı · şartname, ilan metninin aslı</span></div>
        <div class="kb-dosya" data-tur="belge" data-coklu data-ad="İlan belgeleri"><div class="kb-dosya-oge" data-ad="kmo-bakim-onarim-ilan-metni.pdf" data-boyut="412880"></div></div>
      </div>
    </div>

{seo_bolum("pSeo", "Kuzey Marmara Otoyolu bakım ve onarım ihalesi | Dada Haber", "Kuzey Marmara Otoyolu bağlantı yollarında bakım ve onarım işi ihale edilecek. Son teklif 9 Aralık 2026.", "dadahaber.com/resmi-ilanlar/", "kuzey-marmara-otoyolu-bakim-onarim-ihalesi", ["kuzey marmara otoyolu ihale", "kgm ihale", "bakım onarım ihalesi"])}
  </section>

  <aside class="side-card" aria-label="Yayın">
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-paper-plane")}Yayın</h2><span class="status-dot" data-state="yayinda" data-yeni-durum="taslak" title="Yayında"></span></div>
      <div class="pc-body sc-stack">
        <div class="sc-field"><span class="flabel">Durum</span>
          {secim("ilDurum", [("yayinda", "Yayında", ""), ("taslak", "Taslak", "yayından kalkar"), ("zamanli", "Zamanlanmış", "")], deger="yayinda", bos="Taslak", ek=' data-yeni-deger="taslak"')}</div>
        <div class="sc-field"><span class="flabel">Yayın Zamanı</span>
          <div class="kb-tarih-sec" id="ilYayin" data-deger="2026-11-23 09.00" data-yeni-bos data-bos="Yayımlanınca o anın saati" data-temizlenir="1">
            <button type="button" class="kb-tarih-btn" data-acilir="ilYayinMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
            <div class="pnl-menu kb-tarih-menu" id="ilYayinMenu" role="dialog" aria-label="Tarih ve saat seç"></div></div></div>
        <div class="toggle-row"><span>Son Başvurudan Sonra Listede Tut<small>“Süresi doldu” etiketiyle 30 gün daha görünür</small></span><label class="toggle"><input type="checkbox" checked aria-label="Süresi dolunca listede tut"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      </div>
    </section>
{seo_skor(88)}  </aside>
  </div>

  <div class="kb-kaydet" data-form-icin="ilForm">
    <div class="kk-durum">{I("fa-circle-check")}<span data-yeni-metin="Henüz kaydedilmedi">Kaydedildi · 23.11.2026 09.00 · Ayşe Yıldız</span></div>
    <div class="kk-sag">
      <button type="button" class="btn btn-ghost btn-sm" data-kaydet data-kaydet-tur="taslak" data-kaydet-metin="Taslak olarak kaydedildi" data-bildir="Taslak kaydedildi; yayındaki hal değişmedi">{I("fa-floppy-disk")}Taslak Kaydet</button>
      <button type="button" class="btn btn-acc btn-sm" data-kaydet data-kaydet-metin="Güncellendi" data-bildir="İlan güncellendi; sitede yayında, önceki hal denetim izinde" data-yeni-bildir="İlan yayımlandı; sitede Resmî İlanlar sayfasında görünür">{I("fa-check")}<span data-yeni-metin="Yayımla">Güncelle</span></button>
    </div>
  </div>
</main>
</div>
"""
    s += son(editor=True)
    return s



if __name__ == "__main__":
    yaz = {"spor.html": sayfa_spor, "kulup.html": sayfa_kulup, "takvimler.html": sayfa_takvimler, "veri.html": sayfa_veri,
           "burclar.html": sayfa_burclar, "burc.html": sayfa_burc,
           "ilanlar.html": sayfa_ilanlar, "ilan.html": sayfa_ilan}
    import sys
    secili = [a for a in sys.argv[1:] if a in yaz]  # ör. _uret.py spor.html → yalnız o sayfa
    for ad, fn in yaz.items():
        if secili and ad not in secili:
            continue
        (BURA / ad).write_text(fn(), encoding="utf-8")
        print("yazıldı:", ad)
