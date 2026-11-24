#!/usr/bin/env python3
"""Özel Widgetlar modülü · sayfa üretici (yalnızca moduller/ozel-dikeyler/ altına yazar).

Kullanım:  python3 -I moduller/ozel-dikeyler/_uret.py && python3 -I araclar/menu_yaz.py --yalniz moduller/ozel-dikeyler

Kaynaklar (yalnızca okunur): public sözlük (ornek_veri.json: puan_tablosu, piyasa, hava, haberler), public sayfa metinleri
(fikstür, canlı skor, takvimler, resmî ilanlar), moduller.json, moduller/haberler/duzenle.html (kategori listesi).
Sayfalar: spor, kulup, takvimler, veri, ilanlar, ilan. Anket, Sözlük, Firma Rehberi kapalı (K1), üretilmez.
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
HB = (KOK / "moduller" / "haberler" / "duzenle.html").read_text(encoding="utf-8")
I = lambda c, ek="": f'<i class="fa-solid {c}"{ek} aria-hidden="true"></i>'


def isaret(ad):
    return re.search(r"<!--P:%s-->(.*?)<!--/P:%s-->" % (ad, ad), HB, re.S).group(1)


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


def secim(id_, secenekler, deger="", bos="Seçin", etk="", ara=None, ek="", suz=None):
    """kb-secim: secenekler [(deger, ad, alt)]"""
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
            f'<div class="pnl-menu kb-secim-menu" id="{id_}">{arak}<div class="kb-secim-liste" role="listbox">{ops}</div>{bosk}</div></div>')


def row_acts(gor, duz, sil, gor_ad="Görüntüle", duz_ad="Düzenle", sil_ad="Çöpe taşı", diger=True):
    """gor/duz: ('href', url) | ('tanim', id) | ('kilit', neden); sil: 'sil' | ('tasi', attrs) | ('kilit', neden)"""
    def b(x, ikon, ad):
        if x[0] == "href":
            hed = f' data-hedef="{x[2]}"' if len(x) > 2 else ""
            tgt = ' target="_blank" rel="noopener"' if x[1].startswith("http") else ""
            return f'<a class="ia-btn" href="{e(x[1])}"{hed}{tgt} aria-label="{e(ad)}" title="{e(ad)}">{I(ikon)}</a>'
        if x[0] == "tanim":
            return f'<button type="button" class="ia-btn" data-tanim="{x[1]}" aria-label="{e(ad)}" title="{e(ad)}">{I(ikon)}</button>'
        return f'<button type="button" class="ia-btn kb-kilit" disabled aria-label="{e(ad)}: kilitli" title="{e(x[1])}">{I("fa-lock")}</button>'
    s = b(gor, "fa-eye", gor_ad) + b(duz, "fa-pen", duz_ad)
    if sil == "sil":
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
            <button type="button" class="pe-tag" data-suz-temizle>{I("fa-filter-circle-xmark")}Süzgeçleri temizle</button>
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
            <a class="pe-tag" href="{yeniden}">{I("fa-rotate-right")}Yeniden dene</a>
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
PT = soz["puan_tablosu"]
SEHIR = {"GS": "İstanbul", "FB": "İstanbul", "BJK": "İstanbul", "TS": "Trabzon", "BAŞ": "İstanbul", "SAM": "Samsun", "GÖZ": "İzmir", "KAS": "İstanbul",
         "EYP": "İstanbul", "ANT": "Antalya", "KON": "Konya", "ALN": "Antalya", "RİZ": "Rize", "GFK": "Gaziantep", "KOC": "Kocaeli", "AMD": "Diyarbakır",
         "KAY": "Kayseri", "GB": "Ankara"}
ALT = {"Galatasaray": "Galatasaray", "Fenerbahçe": "Fenerbahçe", "Beşiktaş": "Beşiktaş", "Trabzonspor": "Trabzonspor"}
SLUG = {"Galatasaray": "galatasaray.html", "Fenerbahçe": "fenerbahce.html", "Beşiktaş": "besiktas.html", "Trabzonspor": "trabzonspor.html"}
AVRUPA = [("Atlético Madrid", "ATM", "#CB3524", "Madrid", "UEFA Şampiyonlar Ligi"), ("Liverpool", "LIV", "#C8102E", "Liverpool", "Premier Lig"),
          ("Chelsea", "CHE", "#034694", "Londra", "Premier Lig")]
BRANS = [("Fenerbahçe Beko", "FBB", "#0B1F4B", "İstanbul", "Basketbol Süper Ligi"), ("Anadolu Efes", "AEF", "#002F6C", "İstanbul", "Basketbol Süper Ligi"),
         ("Türk Telekom", "TTK", "#00A3E0", "Ankara", "Basketbol Süper Ligi"), ("Fenerbahçe Medicana", "FEN", "#0B1F4B", "İstanbul", "Sultanlar Ligi"),
         ("VakıfBank", "VKF", "#B8860B", "İstanbul", "Sultanlar Ligi"), ("Eczacıbaşı Dynavit", "ECZ", "#E30613", "İstanbul", "Sultanlar Ligi")]
TR_SLUG = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower().translate(str.maketrans("çğıöşüâî", "cgiosuai"))).strip("-")


def haber_say(ad):
    return sum(1 for h in soz["haberler"] if ad in h["baslik"])


def tablo():
    ts = []
    for t in PT["takimlar"]:
        o = t["G"] + t["B"] + t["M"]
        ts.append(dict(t, O=o, AV=t["A"] - t["Y"], P=3 * t["G"] + t["B"]))
    ts.sort(key=lambda x: (-x["P"], -x["AV"], -x["A"]))
    return ts


def kulup_satir(ad, kod, renk, sehir, lig, grup, i):
    kid = TR_SLUG(ad)
    hs = haber_say(ad)
    alt = f'Spor › {ALT[ad]}' if ad in ALT else ("Spor › Süper Lig" if grup == "superlig" else "Spor › Avrupa Ligleri" if grup == "avrupa" else "Spor › " + ("Basketbol" if "Basketbol" in lig else "Voleybol"))
    etiket = (f'<span class="kb-kat"><b>Spor</b>{I("fa-chevron-right")}{e(alt[7:])}</span>')
    durum = ("info", "Elle düzeltildi") if kod == "GFK" else ("wait", "Etiket genel") if alt in ("Spor › Süper Lig",) else ("ok", "API eşleşti")
    kul = f"{alt} konusuyla eşleşik; {hs} haberde geçiyor. Kulüp silinince haberler etkilenmez, puan tablosunda API adı görünür" if hs else ""
    return (f'<tr data-satir="kl-{kid}" data-durum="{grup}" data-lig="{e(lig)}" data-ara="{e(ad + " " + kod + " " + sehir + " " + lig)}" data-baslik="{e(ad)}" data-href="kulup.html?id={kid}"{f" data-kullanim=\"{e(kul)}\"" if kul else ""}>'
            f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(ad)}"></td>'
            f'<td class="kb-ana"><div class="rcp-cell"><span class="kb-ava">{e(kod)}</span><div class="rcp-id"><div class="rcp-name">{e(ad)}</div><div class="rcp-by">{e(lig)} · {e(sehir)}</div></div></div></td>'
            f'<td class="kb-gizle-m"><span class="kb-renk is-ozel" title="Kurumsal renk {renk}"><span style="--kat:{renk}"></span><span class="sr-only">Kurumsal renk {renk}</span></span></td>'
            f'<td class="kb-gizle-t">{etiket}</td>'
            f'<td class="say kb-gizle-t">{sayi(hs)}</td>'
            f'<td><span class="pstat {durum[0]}">{durum[1]}</span></td>'
            f'<td>{row_acts(("href", SITE + SLUG.get(ad, "takimlar.html")), ("href", f"kulup.html?id={kid}", "ozel-dikeyler.kulup"), "sil", gor_ad="Sitede görüntüle")}</td></tr>')


def duzelt_tablo_sablon(t, sira):
    k = t["kod"]
    alan = lambda ad_, v, id_: f'<div class="frow"><label for="{id_}">{ad_}</label><input class="finput" id="{id_}" inputmode="numeric" value="{v}"></div>'
    return f"""<template id="spDz-{TR_SLUG(k)}" data-baslik="{e(t['ad'])} · puan tablosunu düzelt" data-alt="{e(PT['lig'])} · {PT['oynanan_hafta']}. hafta sonu · API verisinin üstüne yazılır, gerekçe zorunlu" data-zorunlu-kayit="ozel-dikeyler.duzeltme">
  <div class="kb-fs">
    <div class="kb-bant bilgi">{I("fa-circle-info")}<span><b>API'deki değer:</b> {sira}. sıra · {t['O']} maç · {t['G']}G {t['B']}B {t['M']}M · {t['A']}-{t['Y']} · {t['P']} puan. Düzeltme denetim izine önceki ve sonraki haliyle yazılır.</span></div>
    <div class="form-grid kb-iki-sutun">{alan("Galibiyet", t['G'], "spG-" + k)}{alan("Beraberlik", t['B'], "spB-" + k)}{alan("Mağlubiyet", t['M'], "spM-" + k)}{alan("Puan düzeltmesi (ceza, hükmen)", 0, "spP-" + k)}{alan("Attığı gol", t['A'], "spA-" + k)}{alan("Yediği gol", t['Y'], "spY-" + k)}</div>
    <div class="frow"><label for="spGer-{k}">Gerekçe</label>
      <textarea class="ftext" id="spGer-{k}" rows="3" data-alan-id="gerekce" data-sayac="200|280" data-zorunlu-metin="Düzeltmenin gerekçesini yazın" placeholder="ör. 12. hafta maçında API golü yanlış işledi; TFF resmî maç raporu esas alındı"></textarea>
      <div class="char-meter"><span>Denetim izinde ve düzeltme geçmişinde görünür</span><b>0 / 200</b></div>
      <div class="ferr">{I("fa-circle-exclamation")}Düzeltmenin gerekçesini yazın.</div></div>
    <div class="toggle-row"><span>API güncellemesi bu düzeltmenin üstüne yazmasın<small>Kapalıysa sonraki API güncellemesi elle düzeltmeyi siler</small></span><label class="toggle"><input type="checkbox" checked aria-label="Düzeltmeyi koru"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-onay-baslik="Puan tablosu düzeltmesi yayımlansın mı?" data-onay-metin="Değişiklik sitede puan durumunda, takım sayfasında ve skor bandında hemen görünür; önceki ve sonraki hal denetim izine yazılır." data-onay-evet="Düzeltmeyi yayımla" data-onay-ikon="fa-pen-to-square" data-sonra-durum="elle" data-sonra-durum-ad="Elle düzeltildi" data-sonra-durum-sinif="info" data-sonra-kapat data-bildir-sonra="Puan tablosu düzeltildi; sitede güncellendi">{I("fa-check")}Düzeltmeyi kaydet</button></div>
</template>
"""


MACLAR = [
    # id, branş, lig, ev(ad,kod), dep(ad,kod), skor, zaman, durum, not
    ("gs-fb", "Futbol", "Süper Lig · 14. hafta", ("Galatasaray", "GS"), ("Fenerbahçe", "FB"), "2-1", "23.11.2026 14.30", "canli", "67'"),
    ("aef-fbb", "Basketbol", "Basketbol Süper Ligi", ("Anadolu Efes", "AEF"), ("Fenerbahçe Beko", "FBB"), "78-71", "23.11.2026 14.00", "canli", "4. çeyrek 6.12"),
    ("fen-thy", "Voleybol", "Sultanlar Ligi", ("Fenerbahçe Medicana", "FEN"), ("Türk Hava Yolları", "THY"), "2-0", "23.11.2026 15.00", "canli", "3. set"),
    ("ts-bas", "Futbol", "Süper Lig · 14. hafta", ("Trabzonspor", "TS"), ("Başakşehir", "BAŞ"), "1-1", "23.11.2026 11.30", "bitti", "MS"),
    ("sam-goz", "Futbol", "Süper Lig · 14. hafta", ("Samsunspor", "SAM"), ("Göztepe", "GÖZ"), "2-0", "23.11.2026 11.30", "bitti", "MS"),
    ("bjk-ttk", "Basketbol", "Basketbol Süper Ligi", ("Beşiktaş", "BJK"), ("Türk Telekom", "TTK"), "84-80", "23.11.2026 12.00", "elle", "MS · skor elle düzeltildi"),
    ("vkf-ecz", "Voleybol", "Sultanlar Ligi", ("VakıfBank", "VKF"), ("Eczacıbaşı Dynavit", "ECZ"), "–", "23.11.2026 20.00", "bekliyor", "Başlamadı"),
    ("liv-che", "Futbol", "Premier Lig", ("Liverpool", "LIV"), ("Chelsea", "CHE"), "–", "23.11.2026 23.00", "bekliyor", "Başlamadı"),
    ("gs-atm", "Futbol", "UEFA Şampiyonlar Ligi · 5. hafta", ("Galatasaray", "GS"), ("Atlético Madrid", "ATM"), "–", "24.11.2026 20.45", "bekliyor", "Başlamadı"),
    ("kay-goz", "Futbol", "Süper Lig · 15. hafta", ("Kayserispor", "KAY"), ("Göztepe", "GÖZ"), "–", "27.11.2026 20.00", "bekliyor", "Başlamadı"),
    ("fb-ts", "Futbol", "Süper Lig · 15. hafta", ("Fenerbahçe", "FB"), ("Trabzonspor", "TS"), "–", "28.11.2026 20.00", "bekliyor", "Başlamadı"),
]
MAC_DURUM = {"canli": ("warm", "Canlı"), "bitti": ("off", "Bitti"), "bekliyor": ("wait", "Başlamadı"), "elle": ("info", "Elle düzeltildi")}


def mac_satir(m):
    mid, br, lig, ev, dep, skor, zaman, dur, not_ = m
    sinif, dad = MAC_DURUM[dur]
    bas_ = f'{ev[0]} – {dep[0]}'
    return (f'<tr data-satir="mc-{mid}" data-durum="{dur}" data-brans="{br}" data-ara="{e(bas_ + " " + lig + " " + br)}" data-baslik="{e(bas_)}">'
            f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name">{e(bas_)}</div><div class="rcp-by">{e(br)} · {e(lig)}</div></div></td>'
            f'<td class="say"><b>{e(skor)}</b></td><td class="kb-gizle-m">{e(not_)}</td>'
            f'<td class="kb-gizle-t"><span class="kb-tarih">{e(tarih_kisa(zaman))}</span></td>'
            f'<td><span class="pstat {sinif}">{dad}</span></td>'
            f'<td>{row_acts(("tanim", "mcGor-" + mid), ("tanim", "mcDz-" + mid), ("kilit", "Maçlar spor veri API'sinden gelir; silinmez, skor elle düzeltilir"), duz_ad="Skoru düzelt")}</td></tr>')


def mac_sablonlar(m):
    mid, br, lig, ev, dep, skor, zaman, dur, not_ = m
    sinif, dad = MAC_DURUM[dur]
    s1, s2 = (skor.split("-") + ["", ""])[:2] if "-" in skor else ("", "")
    durumlar = [("bekliyor", "Başlamadı", ""), ("canli", "Canlı", ""), ("devre", "Devre arası", ""), ("bitti", "Bitti", ""), ("ertelendi", "Ertelendi", ""), ("iptal", "İptal", "")]
    return f"""<template id="mcGor-{mid}" data-baslik="{e(ev[0])} – {e(dep[0])}" data-alt="{e(br)} · {e(lig)}">
  <div class="kb-fs"><div class="kb-fs-tt">Maç</div><div class="sa-durum">
    <div><span>Durum</span><b><span class="pstat {sinif}">{dad}</span></b></div>
    <div><span>Skor</span><b>{e(skor)}</b></div>
    <div><span>Dakika / periyot</span><b>{e(not_)}</b></div>
    <div><span>Başlama</span><b>{e(zaman)}</b></div>
    <div><span>Veri</span><b>Spor veri API · son güncelleme 15.57</b></div>
  </div></div>
  <div class="kb-fs"><div class="kb-fs-tt">Bağlantılar</div><p class="fhint">Sitede maç merkezi ve skor bandında görünür. Canlı anlatım ve maç haberleri Haberler modülünden bağlanır.</p>
    <a class="kb-bag" href="{SITE}mac-detay.html" target="_blank" rel="noopener">Maç detayını sitede aç</a></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="mcDz-{mid}">{I("fa-pen-to-square")}Skoru düzelt</button></div>
</template>
<template id="mcDz-{mid}" data-baslik="{e(ev[0])} – {e(dep[0])} · skoru düzelt" data-alt="API verisinin üstüne yazılır · gerekçe zorunlu, denetim izine yazılır" data-zorunlu-kayit="ozel-dikeyler.duzeltme">
  <div class="kb-fs">
    <div class="form-grid kb-iki-sutun">
      <div class="frow"><label for="mcS1-{mid}">{e(ev[0])}</label><input class="finput" id="mcS1-{mid}" inputmode="numeric" value="{e(s1)}" placeholder="–"></div>
      <div class="frow"><label for="mcS2-{mid}">{e(dep[0])}</label><input class="finput" id="mcS2-{mid}" inputmode="numeric" value="{e(s2)}" placeholder="–"></div>
      <div class="frow"><span class="flabel">Durum</span>{secim("mcDur-" + mid, durumlar, deger="bitti" if dur == "elle" else dur, bos="Durum seçin")}</div>
      <div class="frow"><label for="mcDk-{mid}">Dakika ya da periyot</label><input class="finput" id="mcDk-{mid}" value="{e(not_)}"></div>
    </div>
    <div class="frow"><label for="mcGer-{mid}">Gerekçe</label>
      <textarea class="ftext" id="mcGer-{mid}" rows="3" data-alan-id="gerekce" data-sayac="200|280" data-zorunlu-metin="Düzeltmenin gerekçesini yazın" placeholder="ör. API 76. dakikadaki golü işlemedi; maç yayını esas alındı">{"API son 3 dakikada skoru güncellemedi; maç sonu skoru resmî kaynaktan işlendi." if dur == "elle" else ""}</textarea>
      <div class="char-meter"><span>Denetim izinde ve düzeltme geçmişinde görünür</span><b>0 / 200</b></div>
      <div class="ferr">{I("fa-circle-exclamation")}Düzeltmenin gerekçesini yazın.</div></div>
    <div class="toggle-row"><span>API güncellemesi bu düzeltmenin üstüne yazmasın<small>Maç bitene kadar açık kalması önerilmez; canlı skor durur</small></span><label class="toggle"><input type="checkbox"{" checked" if dur in ("bitti", "elle") else ""} aria-label="Düzeltmeyi koru"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-onay-baslik="Skor düzeltmesi yayımlansın mı?" data-onay-metin="Skor sitede maç merkezinde, skor bandında ve canlı anlatımda hemen değişir; önceki ve sonraki hal denetim izine yazılır." data-onay-evet="Düzeltmeyi yayımla" data-onay-ikon="fa-pen-to-square" data-sonra-durum="elle" data-sonra-durum-ad="Elle düzeltildi" data-sonra-durum-sinif="info" data-sonra-kapat data-bildir-sonra="Skor düzeltildi; sitede güncellendi">{I("fa-check")}Düzeltmeyi kaydet</button></div>
</template>
"""


def sayfa_spor():
    ts = tablo()
    kl = [kulup_satir(t["ad"], t["kod"], t["renk"], SEHIR.get(t["kod"], ""), "Süper Lig", "superlig", i) for i, t in enumerate(PT["takimlar"])]
    kl += [kulup_satir(a, k, r, s, l, "avrupa", 0) for a, k, r, s, l in AVRUPA]
    kl += [kulup_satir(a, k, r, s, l, "brans", 0) for a, k, r, s, l in BRANS]
    kl.append(kulup_satir("Pendikspor", "PEN", "#8B1E3F", "İstanbul", "1. Lig", "cop", 0).replace('data-durum="cop"', 'data-durum="cop" data-onceki="superlig"'))
    pt_rows, pt_sab = [], []
    for n, t in enumerate(ts, 1):
        elle = t["kod"] == "GFK"
        kid = TR_SLUG(t["ad"])
        pt_rows.append(f'<tr data-satir="pt-{t["kod"]}" data-durum="{"elle" if elle else "api"}" data-ara="{e(t["ad"] + " " + t["kod"])}" data-baslik="{e(t["ad"])}" data-href="kulup.html?id={kid}">'
                       f'<td class="say">{n}</td><td class="kb-ana"><div class="rcp-cell"><span class="kb-ava k-sm">{e(t["kod"])}</span><div class="rcp-id"><div class="rcp-name">{e(t["ad"])}</div></div></div></td>'
                       f'<td class="say">{t["O"]}</td><td class="say kb-gizle-m">{t["G"]}</td><td class="say kb-gizle-m">{t["B"]}</td><td class="say kb-gizle-m">{t["M"]}</td>'
                       f'<td class="say kb-gizle-t">{t["A"]}:{t["Y"]}</td><td class="say kb-gizle-m">{"+" if t["AV"] > 0 else ""}{t["AV"]}</td><td class="say"><b>{t["P"]}</b></td>'
                       f'<td><span class="pstat {"info" if elle else "ok"}" title="{"22.11.2026 18.40 · Burak Tan · 12. hafta golü API'de yanlış işlendi" if elle else "Spor veri API · 15.57"}">{"Elle düzeltildi" if elle else "API"}</span></td>'
                       f'<td>{row_acts(("href", f"kulup.html?id={kid}", "ozel-dikeyler.kulup"), ("tanim", "spDz-" + TR_SLUG(t["kod"])), ("kilit", "Puan tablosu API verisidir; silinmez, elle düzeltilir"), gor_ad="Kulübü aç", duz_ad="Düzelt", diger=False)}</td></tr>')
        pt_sab.append(duzelt_tablo_sablon(t, n))
    maclar = "".join(mac_satir(m) for m in MACLAR)
    mac_sab = "".join(mac_sablonlar(m) for m in MACLAR)
    ligler = [("superlig", "Süper Lig", "18 takım"), ("tff1", "1. Lig", "20 takım"), ("bsl", "Basketbol Süper Ligi", "16 takım"), ("sultanlar", "Sultanlar Ligi", "14 takım")]
    haftalar = [(str(h), f"{h}. hafta", "") for h in range(PT["oynanan_hafta"], 0, -1)]
    branslar = [("", "Bütün branşlar", ""), ("Futbol", "Futbol", ""), ("Basketbol", "Basketbol", ""), ("Voleybol", "Voleybol", "")]
    kl_ligler = [("", "Bütün ligler", "")] + [(l, l, "") for l in ["Süper Lig", "UEFA Şampiyonlar Ligi", "Premier Lig", "Basketbol Süper Ligi", "Sultanlar Ligi"]]
    s = bas("Spor", "spor")
    s += f"""
<!-- SPOR (D4): Kulüpler · Ligler ve puan durumu · Maç merkezi. Puan tablosu ve maçlar spor veri API'sinden gelir; silinmez,
     elle düzeltilir (çekmece, gerekçe zorunlu, denetim izi). Kulüp düzenle ayrı sayfa (kulup.html). -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Spor</h1>
      <div class="ph-sub">{len(PT['takimlar'])} Süper Lig kulübü · {PT['oynanan_hafta']}. hafta oynandı, 14. hafta sürüyor · 3 canlı maç</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="entegrasyonlar.ayar" data-hedef-ek="?id=spor" data-roller="super" href="../../cekirdek/entegrasyonlar/ayar.html?id=spor">{I("fa-plug")}Spor veri API</a>
      <a class="btn btn-acc btn-sm" data-hedef="ozel-dikeyler.kulup" data-hedef-ek="?yeni=1" href="kulup.html?yeni=1">{I("fa-plus")}Yeni kulüp</a>
    </div>
  </div>

  <div class="kb-bant tehlike dash-row">{I("fa-triangle-exclamation")}<span><b>Spor veri API 15.58'den beri yanıt vermiyor.</b> Sitedeki skor bandı ve maç merkezi son veriyi (15.57) gösteriyor. Canlı maçlarda skoru gerekirse elle düzeltin; API dönünce düzeltilmemiş veriler kendiliğinden güncellenir.</span><a class="btn btn-ghost btn-sm kb-bant-eylem" data-hedef="entegrasyonlar.ayar" data-hedef-ek="?id=spor" data-roller="super" href="../../cekirdek/entegrasyonlar/ayar.html?id=spor">{I("fa-plug")}Bağlantı</a></div>

  <section class="pnl-card" data-sekmeli aria-label="Spor verisi">
    <div class="sa-form-tabs" role="tablist" aria-label="Spor sekmeleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="spKulup">{I("fa-shield-halved")}Kulüpler</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="spLig">{I("fa-list-ol")}Ligler ve puan durumu</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="spMac">{I("fa-futbol")}Maç merkezi</button>
    </div>

    <!-- ===== KULÜPLER ===== -->
    <div class="sa-form-panel" id="spKulup" role="tabpanel">
      <div data-liste data-liste-ad="kulüp" data-sayfa-boy="50" data-liste-cop-not="Kulüp listelerden kalkar ve Çöp sekmesine taşınır">
        <div class="kb-liste-ust">
          <div class="chips" role="tablist" aria-label="Kulüp grubu">
            <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="superlig">Süper Lig<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="avrupa">Avrupa<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="brans">Branşlar<span class="ch-cnt">0</span></button>
          </div>
          <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
        </div>
        <div class="filter-bar">
          <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="klAra">Kulüplerde ara</label><input id="klAra" type="search" data-liste-ara placeholder="Kulüp adı, kısa kod ya da şehir ara" autocomplete="off"></div>
          {secim("klSuzLig", kl_ligler, etk="Lig:", bos="Tümü", suz="lig")}
          <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
        </div>
        <div class="kb-toplu" hidden>
          <b data-secili-say>0 kulüp seçildi</b><span class="kb-toplu-ayir"></span>
          <button type="button" class="btn btn-ghost btn-sm" data-toplu="api" data-bildir="Seçilen kulüplerin verisi API'den yeniden çekilecek (prototip)">{I("fa-rotate")}<span>API'den yenile</span></button>
          <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe taşı</span></button>
          <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button>
        </div>
        <div class="ptable-wrap"><table class="ptable">
          <thead><tr><th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün kulüpleri seç"></th><th class="kb-ana">Kulüp</th><th class="kb-gizle-m">Renk</th><th class="kb-gizle-t">Etiket eşleşmesi</th><th class="say kb-gizle-t">Haber</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
          <tbody data-satirlar>{"".join(kl)}</tbody>
{durum_govdeleri(7, "fa-shield-halved", "Henüz kulüp yok", "Kulüpler spor veri API'sinden gelir; listede olmayanı “Yeni kulüp” ile ekleyin.", "Kulüpler yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", iskelet='<td></td><td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="spor.html")}        </table></div>
{pager(sayfalar=False)}
        <div class="pnl-menu kb-diger-menu" role="menu">
          <div class="kb-dm-grup" data-durum-icin="superlig avrupa brans">Veri</div>
          <button type="button" data-durum-icin="superlig avrupa brans" data-onay-baslik="Kulüp verisi API'den yenilensin mi?" data-onay-metin="Ad, kadro ve istatistikler API'den yeniden çekilir; elle girilen renk, kısa kod ve etiket eşleşmesi korunur." data-onay-evet="Yenile" data-onay-ikon="fa-rotate" data-bildir-sonra="Kulüp verisi kuyruğa alındı">{I("fa-rotate")}API'den yenile</button>
          <button type="button" data-durum-icin="superlig avrupa brans" data-bildir="Haberler bu kulübün etiketine süzülerek açılır (prototip)">{I("fa-newspaper")}Kulübün haberleri</button>
          <button type="button" data-durum-icin="superlig avrupa brans" data-roller="super gyy" data-bildir="Denetim izi bu kayda süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
          <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten geri al</button>
          <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı olarak sil</button>
        </div>
      </div>
    </div>

    <!-- ===== LİGLER VE PUAN DURUMU ===== -->
    <div class="sa-form-panel" id="spLig" role="tabpanel" hidden>
      <div class="filter-bar">
        {secim("spLigSec", ligler, deger="superlig", bos="Lig seçin", etk="Lig:")}
        {secim("spHafta", haftalar, deger=str(PT['oynanan_hafta']), bos="Hafta", etk="Hafta:")}
      </div>
      <div class="pc-body"><div class="kb-bant bilgi">{I("fa-lock")}<span><b>Puan tablosu API verisidir; silinmez.</b> Yanlış değer “Düzelt” ile elle düzeltilir; gerekçe zorunludur ve düzeltme denetim izine önceki ve sonraki haliyle yazılır. Son güncelleme 15.57.</span></div></div>
      <div data-liste data-liste-ad="takım" data-sayfa-boy="25">
        <div class="ptable-wrap"><table class="ptable">
          <thead><tr><th class="say">#</th><th class="kb-ana">Takım</th><th class="say">O</th><th class="say kb-gizle-m">G</th><th class="say kb-gizle-m">B</th><th class="say kb-gizle-m">M</th><th class="say kb-gizle-t">A:Y</th><th class="say kb-gizle-m">AV</th><th class="say">P</th><th>Kaynak</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
          <tbody data-satirlar>{"".join(pt_rows)}</tbody>
{durum_govdeleri(11, "fa-list-ol", "Bu lig için puan tablosu yok", "Sezon başlamadıysa ya da API bu ligi vermiyorsa tablo boş görünür.", "Puan tablosu yüklenemedi", "Spor veri API yanıt vermiyor. Entegrasyonlar ekranından bağlantıyı kontrol edin.", yeniden="spor.html")}        </table></div>
{pager(sayfalar=False)}
      </div>
    </div>

    <!-- ===== MAÇ MERKEZİ ===== -->
    <div class="sa-form-panel" id="spMac" role="tabpanel" hidden>
      <div data-liste data-liste-ad="maç" data-sayfa-boy="25">
        <div class="kb-liste-ust">
          <div class="chips" role="tablist" aria-label="Maç durumu">
            <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="canli">Canlı<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="bekliyor">Fikstür<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="bitti">Bitti<span class="ch-cnt">0</span></button>
            <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="elle">Elle düzeltilen<span class="ch-cnt">0</span></button>
          </div>
        </div>
        <div class="filter-bar">
          <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="mcAra">Maçlarda ara</label><input id="mcAra" type="search" data-liste-ara placeholder="Takım ya da lig ara" autocomplete="off"></div>
          {secim("mcSuzBrans", branslar, etk="Branş:", bos="Tümü", suz="brans")}
          <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
        </div>
        <div class="pc-body"><div class="kb-bant bilgi">{I("fa-lock")}<span><b>Maçlar spor veri API'sinden gelir; silinmez.</b> Skor ve durum “Skoru düzelt” ile elle düzeltilir (gerekçe zorunlu, denetim izine yazılır).</span></div></div>
        <div class="ptable-wrap"><table class="ptable">
          <thead><tr><th class="kb-ana">Maç</th><th class="say">Skor</th><th class="kb-gizle-m">Dakika</th><th class="kb-gizle-t">Başlama</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
          <tbody data-satirlar>{maclar}</tbody>
{durum_govdeleri(6, "fa-futbol", "Bu süzgeçle maç yok", "Fikstür API'den gelir; sezon arasında liste boş olabilir.", "Maçlar yüklenemedi", "Spor veri API yanıt vermiyor. Entegrasyonlar ekranından bağlantıyı kontrol edin.", yeniden="spor.html")}        </table></div>
{pager(sayfalar=False)}
        <div class="pnl-menu kb-diger-menu" role="menu">
          <div class="kb-dm-grup">Maç</div>
          <button type="button" data-modul="haberler" data-bildir="Canlı anlatım Haberler › Canlı anlatım ekranında bu maçla açılır (prototip)">{I("fa-tower-broadcast")}Canlı anlatım aç</button>
          <button type="button" data-bildir="Maç haberleri süzülerek açılır (prototip)">{I("fa-newspaper")}Maç haberleri</button>
          <button type="button" data-durum-icin="elle" data-onay-baslik="Elle düzeltme kaldırılsın mı?" data-onay-metin="Skor yeniden API'den gelir; düzeltme kaydı denetim izinde kalır." data-onay-evet="API'ye dön" data-onay-ikon="fa-rotate-left" data-sonra-durum="bitti" data-sonra-durum-ad="Bitti" data-sonra-durum-sinif="off" data-bildir-sonra="Skor yeniden API'den geliyor">{I("fa-rotate-left")}API değerine dön</button>
          <button type="button" data-roller="super gyy" data-bildir="Denetim izi bu maça süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
        </div>
      </div>
    </div>
  </section>
</main>
</div>
{"".join(pt_sab)}{mac_sab}"""
    s += son()
    return s


# ================================================================== KULÜP DÜZENLE
def seo_bolum(pid, baslik, aciklama, onek, slug, kw, uret=True):
    cip = "".join(f'<span class="kb-cip" data-deger="{e(k)}"><span>{e(k)}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for k in kw)
    return f"""    <div class="sa-form-panel" id="{pid}" role="tabpanel" data-ai-grup="seo" hidden>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-wand-magic-sparkles")}Otomatik üretildi<span class="fs-ek"><button type="button" class="btn btn-ghost btn-sm" data-seo-uret>{I("fa-rotate")}Başlıktan yeniden üret</button></span></div>
        <div class="form-grid">
          <div class="frow"><label for="{pid}B">SEO başlığı</label>
            <input class="finput" id="{pid}B" data-alan="seo-baslik" data-sayac="60|70" value="{e(baslik)}">
            <div class="char-meter"><span>Arama sonucunda görünen başlık · 50–60 karakter önerilir</span><b>0 / 60</b></div></div>
          <div class="frow"><label for="{pid}A">SEO açıklaması</label>
            <textarea class="ftext" id="{pid}A" data-alan="seo-aciklama" data-sayac="155|170">{e(aciklama)}</textarea>
            <div class="char-meter"><span>Arama sonucunda başlığın altında · 120–155 karakter önerilir</span><b>0 / 155</b></div></div>
          <div class="frow"><label for="{pid}S">Adres</label>
            <div class="slug-wrap"><span class="slug-pre">{e(onek)}</span><input class="finput" id="{pid}S" data-alan="slug" value="{e(slug)}"></div>
            <span class="fhint">Yayımlandıktan sonra değiştirilirse eski adres yeniye yönlendirilir.</span></div>
          <div class="frow"><span class="flabel">Anahtar kelimeler</span>
            <div class="kb-cip-girdi" data-serbest>{cip}<input type="text" placeholder="Yazın; Enter ya da virgülle ekleyin" aria-label="Anahtar kelime ekle"><div class="pnl-menu kb-cip-oneri"></div></div></div>
          <div class="frow"><span class="flabel">Arama sonucu önizlemesi</span>
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
      <div class="pc-head"><h2 class="pc-title">{I("fa-gauge")}SEO skoru</h2></div>
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
    alt = json.loads(html.unescape(re.search(r'data-alt-harita="([^"]*)"', isaret("hb-df-alt")).group(1)))
    spor_alt = [(a, f"Spor › {a}", "") for a in alt["Spor"]]
    sehirler = json.dumps(["İstanbul", "Ankara", "İzmir", "Trabzon", "Samsun", "Antalya", "Konya", "Rize", "Gaziantep", "Kocaeli", "Diyarbakır", "Kayseri"], ensure_ascii=False)
    renkler = "".join(f'<label class="kb-renk kat-{k}" title="{a}"><input type="radio" name="klRenk" value="{k}"><span></span><span class="sr-only">{a}</span></label>' for k, a in [("gundem", "Gündem"), ("spor", "Spor"), ("finans", "Finans"), ("savunma", "Savunma"), ("dunya", "Dünya"), ("kose", "Köşe")])
    renkler += f'<label class="kb-renk is-ozel" title="Özel renk {t["renk"]}"><input type="radio" name="klRenk" value="{t["renk"]}" checked><span style="--kat:{t["renk"]}"></span><span class="sr-only">Özel renk {t["renk"]}</span></label>'
    s = bas("Kulüp düzenle", "kulup", ' data-yeni-baslik="Yeni kulüp"')
    s += f"""
<!-- KULÜP DÜZENLE (D4): Detay · SEO (kulüp sayfası sitede var, 8b). Arma 1:1 (ozel-dikeyler.arma; kişisel/kurumsal işaret,
     medya havuzuna girmez, data-etiketsiz). Kurumsal renk hazır + özel (kb-renkler[data-renk-ozel]). Sitede arma yoksa renkli kısa kod rozeti görünür. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1 data-yeni-metin="Yeni kulüp">Kulüp düzenle</h1>
      <div class="ph-sub" data-yeni-metin="Henüz kaydedilmedi · spor veri API'sinde eşleşme aranır">Galatasaray · Süper Lig · {sira}. sıra, {t['P']} puan · API ile eşleşik</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ozel-dikeyler.spor" href="spor.html">{I("fa-arrow-left")}Spora dön</a>
      <a class="btn btn-ghost btn-sm" data-yeni-gizle href="{SITE}galatasaray.html" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Sitede görüntüle</a>
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
          <div class="frow"><label for="klAd">Kulüp adı</label>
            <input class="finput kb-buyuk" id="klAd" data-alan-id="ad" data-sayac="30|40" value="Galatasaray">
            <div class="char-meter"><span>Puan durumunda, skor bandında ve takım sayfasında</span><b>0 / 30</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Kulüp adı zorunlu.</div></div>
          <div class="frow"><label for="klKod">Kısa kod</label>
            <input class="finput" id="klKod" data-alan-id="kod" data-sayac="3|4" value="GS">
            <div class="char-meter"><span>Skor bandında ve arma yoksa rozette</span><b>0 / 3</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Kısa kod zorunlu.</div></div>
          <div class="frow"><span class="flabel">Lig</span>
            {secim("klLig", ligler, deger="Süper Lig", bos="Lig seçin", ara="Lig ara", ek=' data-alan-id="lig" data-zorunlu-metin="Kulübün ligini seçin"')}
            <div class="ferr">{I("fa-circle-exclamation")}Kulübün ligini seçin.</div></div>
          <div class="frow"><span class="flabel">Şehir</span>
            <div class="kb-cip-girdi" data-havuz-yonet data-kullanim-birim="kulüpte" data-havuz='{e(sehirler)}'><span class="kb-cip" data-deger="İstanbul"><span>İstanbul</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><input type="text" placeholder="Şehir ara" aria-label="Şehir"><div class="pnl-menu kb-cip-oneri"></div></div></div>
          <div class="frow"><label for="klStat">Stadyum ya da salon</label><input class="finput" id="klStat" value="Ali Sami Yen Spor Kompleksi"></div>
          <div class="frow"><label for="klTd">Teknik direktör</label><input class="finput" id="klTd" value="" placeholder="Spor veri API'sinden gelir"><span class="fhint">Boş bırakılırsa API'deki ad gösterilir.</span></div>
        </div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-palette")}Kurumsal renk<span class="fs-ek">Puan durumunda rozet, skor bandında çizgi</span></div>
        <div class="kb-renkler" role="radiogroup" aria-label="Kurumsal renk" data-renk-ozel>{renkler}</div>
        <span class="fhint">Hazır renkler temadan; damlalık ile kulübün kendi rengi seçilir (okunurluk denetlenir).</span>
      </div>
      <div class="form-sec" data-gorsel-alan="ozel-dikeyler.arma" data-gorsel-ad="Arma" data-kirp-sonra data-etiketsiz>
        <div class="form-sec-tt">{I("fa-shield-halved")}Arma<span class="fs-ek">İsteğe bağlı · yoksa renkli kısa kod rozeti görünür</span></div>
        <div class="kb-yukle" data-gorsel-bos><span class="kb-ava k-lg">GS</span><b>Armayı sürükleyin ya da seçin</b><span>1:1 · puan durumu 48×48, takım sayfası 160×160, mobil 40×40 · şeffaf PNG ya da SVG önerilir; medya havuzuna girmez</span><span class="kg-acts"><button type="button" class="btn btn-acc btn-sm" data-gorsel-yukle>{I("fa-upload")}Bilgisayardan yükle</button></span></div>
        <div class="kb-gorsel" data-gorsel-dolu hidden><div class="kg-bolum"><div class="kg-bas">{I("fa-desktop")}Web</div><div class="kg-ikili"><div class="kg-resim" data-gorsel-hedef="web" data-kirp-oran="web.detay" style="aspect-ratio:1/1"><span class="kg-etk">Takım sayfası · 1:1</span></div><div class="kg-resim" data-gorsel-hedef="web" data-kirp-oran="web.kart" style="aspect-ratio:1/1"><span class="kg-etk">Puan durumu · 1:1</span></div></div><div class="kg-olcu">Önerilen: takım sayfası <b>160×160</b>, puan durumu <b>48×48</b>.</div><div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{I("fa-crop-simple")}Kırp</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{I("fa-upload")}Yükle</button><button type="button" class="btn btn-ghost btn-sm danger" data-gorsel-kaldir>{I("fa-trash")}Kaldır</button></div></div>
          <div class="kg-bolum"><div class="kg-bas">{I("fa-mobile-screen")}Mobil<span class="kg-oto">{I("fa-wand-magic-sparkles")} Webden kırpıldı</span></div><div class="kg-resim" data-gorsel-hedef="mobil" data-kirp-oran="mobil.kart" style="aspect-ratio:1/1"><span class="kg-etk">Mobil · 1:1</span></div><div class="kg-olcu">Önerilen: <b>40×40</b>.</div><div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac="mobil.kart">{I("fa-crop-simple")}Kırp</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle data-gorsel-kapsam="mobil">{I("fa-upload")}Ayrı görsel yükle</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-webe-don hidden>{I("fa-rotate-left")}Webden kırpılana dön</button></div></div></div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-tags")}Etiket eşleştirme<span class="fs-ek">Haberler, skor ve kulüp sayfası bu eşleşmeyle bağlanır</span></div>
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><span class="flabel">Spor alt konusu</span>{secim("klAlt", spor_alt, deger="Galatasaray", bos="Alt konu seçin", ara="Alt konu ara")}<span class="fhint">Yeni alt konu Haberler › Kategoriler'den eklenir.</span></div>
          <div class="frow"><label for="klApi">Spor veri API kimliği</label><input class="finput" id="klApi" value="takim/645" readonly><span class="fhint">API eşleşmesi kendiliğinden yapılır; değişmez.</span></div>
        </div>
        <div class="frow kb-ust-bosluk"><span class="flabel">Haberlerde geçen diğer adlar</span>
          <div class="kb-cip-girdi" data-serbest><span class="kb-cip" data-deger="GS"><span>GS</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><span class="kb-cip" data-deger="Cimbom"><span>Cimbom</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><span class="kb-cip" data-deger="Sarı-Kırmızılılar"><span>Sarı-Kırmızılılar</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><input type="text" placeholder="Yazın; Enter ya da virgülle ekleyin" aria-label="Diğer ad ekle"></div>
          <span class="fhint">AI havuzu ve arama bu adlarla da kulübü tanır.</span></div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-align-left")}Kulüp hakkında<span class="fs-ek">Takım sayfasının başında</span></div>
        <div class="kb-editor" data-editor-ad="Kulüp hakkında" data-editor-kisa><div class="kz-alan ke-alan"><p>1905'te kurulan Galatasaray, Süper Lig'in en çok şampiyonluk kazanan kulübü. Maçlarını İstanbul'da Ali Sami Yen Spor Kompleksi'nde oynuyor.</p></div></div>
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
TK_KAT = ["Siyaset", "Ekonomi", "Eğitim", "Dünya", "Spor", "Toplum", "Sağlık", "Ulaşım", "Kültür"]
ONEM = {"yuksek": ("warm", "Yüksek"), "orta": ("wait", "Orta"), "dusuk": ("off", "Düşük")}
TAKVIM = [
    # id, tür, başlık, tarih, kategori, kurum, not, önem, durum, ekonomik (önceki, beklenti, açıklanan), sınav aşaması
    ("tk-tuketici", "ekonomik", "Tüketici Güven Endeksi · Kasım", "23.11.2026 10.00", "Ekonomi", "TÜİK", "Önceki 84,1 · Beklenti 85,0", "yuksek", "yayinda", ("84,1", "85,0", "85,4"), ""),
    ("tk-ppk", "ekonomik", "TCMB Para Politikası Kurulu · Faiz kararı", "23.11.2026 14.00", "Ekonomi", "TCMB", "Açıklandı %42,50 · Beklenti %42,50", "yuksek", "yayinda", ("%42,50", "%42,50", "%42,50"), ""),
    ("tk-butce", "gundem", "Genel Kurul'da bütçe görüşmeleri", "23.11.2026 14.00", "Siyaset", "TBMM", "Bakanlık bütçeleri", "yuksek", "yayinda", None, ""),
    ("tk-abd-issizlik", "ekonomik", "ABD haftalık işsizlik başvuruları", "23.11.2026 15.30", "Ekonomi", "ABD Çalışma Bakanlığı", "Önceki 231 bin · Beklenti 228 bin", "orta", "yayinda", ("231 bin", "228 bin", ""), ""),
    ("tk-eyds-basvuru", "sinav", "2026-e-YDS/12 İngilizce başvuruları son gün", "23.11.2026 23.59", "Eğitim", "ÖSYM", "Sınav 6 Aralık", "yuksek", "yayinda", None, "basvuru"),
    ("tk-kko", "ekonomik", "Kapasite Kullanım Oranı · Kasım", "24.11.2026 10.00", "Ekonomi", "TCMB", "Önceki %74,2 · Beklenti %74,5", "orta", "yayinda", ("%74,2", "%74,5", ""), ""),
    ("tk-gs-atm", "etkinlik", "Şampiyonlar Ligi: Galatasaray – Atlético Madrid", "24.11.2026 20.45", "Spor", "UEFA", "5. hafta", "orta", "yayinda", None, ""),
    ("tk-siddet", "gundem", "Kadına Yönelik Şiddete Karşı Uluslararası Mücadele Günü", "25.11.2026 10.00", "Toplum", "", "Etkinlikler 81 ilde", "yuksek", "yayinda", None, ""),
    ("tk-ab-konsey", "gundem", "AB Dışişleri Konseyi toplantısı", "26.11.2026 10.00", "Dünya", "AB Konseyi", "Brüksel", "orta", "yayinda", None, ""),
    ("tk-pce", "ekonomik", "ABD Çekirdek PCE fiyat endeksi · Ekim", "26.11.2026 16.30", "Ekonomi", "ABD Ticaret Bakanlığı", "Önceki %2,7 · Beklenti %2,8", "yuksek", "yayinda", ("%2,7", "%2,8", ""), ""),
    ("tk-basket", "etkinlik", "Basketbol: Türkiye – Macaristan", "26.11.2026 20.00", "Spor", "FIBA", "Dünya Kupası elemeleri", "orta", "yayinda", None, ""),
    ("tk-pmi", "ekonomik", "Euro Bölgesi Öncü İmalat PMI", "27.11.2026 12.00", "Ekonomi", "S&P Global", "Önceki 49,8 · Beklenti 50,1", "orta", "yayinda", ("49,8", "50,1", ""), ""),
    ("tk-dis-ticaret", "ekonomik", "Dış ticaret dengesi · Ekim", "28.11.2026 10.00", "Ekonomi", "TÜİK", "Önceki -6,9 milyar $ · Beklenti -6,4 milyar $", "orta", "yayinda", ("-6,9 milyar $", "-6,4 milyar $", ""), ""),
    ("tk-kis-lastigi", "gundem", "Kış lastiği uygulaması başlıyor", "01.12.2026 00.00", "Ulaşım", "Emniyet Genel Müdürlüğü", "Ticari araçlar için 1 Nisan'a kadar", "yuksek", "yayinda", None, ""),
    ("tk-gsyh", "ekonomik", "GSYH · 3. çeyrek (yıllık)", "01.12.2026 10.00", "Ekonomi", "TÜİK", "Önceki %4,8 · Beklenti %3,9", "yuksek", "yayinda", ("%4,8", "%3,9", ""), ""),
    ("tk-kpss-tercih", "sinav", "KPSS-2026/7 tercih dönemi", "01.12.2026 10.00", "Eğitim", "ÖSYM", "Tercih 1–8 Aralık · Sonuç 18 Aralık", "orta", "yayinda", None, "tercih"),
    ("tk-aids", "gundem", "Dünya AIDS Günü", "01.12.2026 09.00", "Sağlık", "Sağlık Bakanlığı", "Ücretsiz test noktaları açılıyor", "dusuk", "yayinda", None, ""),
    ("tk-kulup-haftasi", "etkinlik", "Kış dönemi kulüp tanıtım haftası", "01.12.2026 10.00", "Kültür", "Üniversiteler", "Kampüslerde bir hafta", "dusuk", "taslak", None, ""),
    ("tk-tufe", "ekonomik", "TÜFE · Kasım (yıllık)", "03.12.2026 10.00", "Ekonomi", "TÜİK", "Önceki %32,9 · Beklenti %31,8", "yuksek", "yayinda", ("%32,9", "%31,8", ""), ""),
    ("tk-eyds-sinav", "sinav", "2026-e-YDS/12 İngilizce sınavı", "06.12.2026 10.15", "Eğitim", "ÖSYM", "Sonuç 10 Aralık", "orta", "yayinda", None, "sinav"),
    ("tk-yokdil", "sinav", "2026-YÖKDİL/2 sonuçları", "18.12.2026 14.00", "Eğitim", "ÖSYM", "Sonuçlar aday işlemleri sisteminde", "orta", "yayinda", None, "sonuc"),
    ("tk-eski", "gundem", "Bütçe görüşmeleri Plan ve Bütçe Komisyonu'nda", "02.11.2026 10.00", "Siyaset", "TBMM", "Komisyon görüşmeleri", "orta", "cop", None, ""),
]
ASAMA = [("basvuru", "Başvuru", ""), ("sinav", "Sınav", ""), ("sonuc", "Sonuç", ""), ("tercih", "Tercih", "")]


def tk_tarih_iso(t):
    return f"{t[6:10]}-{t[3:5]}-{t[0:2]} {t[11:]}"


def tk_form(sid, r=None):
    tid, tur, bas_, tarih, kat, kurum, not_, onem, dur, eko, asama = r if r else ("", "", "", "", "", "", "", "orta", "taslak", None, "")
    turler = "".join(f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="tkTur-{sid}" value="{k}"{" checked" if k == tur else ""}{f" data-ac=\"tkEko-{sid}\"" if k == "ekonomik" else f" data-ac=\"tkSnv-{sid}\"" if k == "sinav" else ""}><span><b>{I(v[2])} {v[0]}</b><small>{ {"gundem": "Gündem Takvimi", "ekonomik": "Ekonomik Takvim", "sinav": "Sınav Takvimi", "etkinlik": "Gündem Takvimi · etkinlik"}[k] }</small></span></label>' for k, v in TK_TUR.items())
    katlar = [(k, k, "") for k in TK_KAT]
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
      <div class="frow"><span class="flabel">Tarih ve saat</span>
        <div class="kb-tarih-sec" id="tkT-{sid}" data-alan-id="tarih" data-deger="{tk_tarih_iso(tarih) if tarih else ""}" data-zorunlu-metin="Tarih ve saati seçin">
          <button type="button" class="kb-tarih-btn" data-acilir="tkTM-{sid}" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
          <div class="pnl-menu kb-tarih-menu" id="tkTM-{sid}" role="dialog" aria-label="Tarih ve saat seç"></div></div>
        <div class="ferr">{I("fa-circle-exclamation")}Tarih ve saati seçin.</div></div>
      <div class="frow"><span class="flabel">Kategori</span>
        {secim("tkK-" + sid, katlar, deger=kat, bos="Kategori seçin", ara="Kategori ara", ek=' data-alan-id="kategori" data-zorunlu-metin="Kategoriyi seçin"')}
        <div class="ferr">{I("fa-circle-exclamation")}Kategoriyi seçin.</div></div>
      <div class="frow"><label for="tkKu-{sid}">Kurum</label><input class="finput" id="tkKu-{sid}" value="{e(kurum)}" placeholder="ör. TÜİK, ÖSYM, TBMM"></div>
      <div class="frow"><label for="tkN-{sid}">Kısa not</label><input class="finput" id="tkN-{sid}" data-sayac="60|80" value="{e(not_)}" placeholder="ör. Etkinlikler 81 ilde"><div class="char-meter"><span>Başlığın altında</span><b>0 / 60</b></div></div>
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
<template id="tkDz-{tid}" data-baslik="{e(bas_)} · düzenle" data-alt="Değişiklik sitede takvim sayfalarında hemen görünür" data-zorunlu-kayit="ozel-dikeyler.takvim">
{tk_form(tid, r)}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm" data-kaydet-tur="taslak" data-sablon-ac="tkGor-{tid}" data-bildir-sonra="Taslak olarak kaydedildi; sitede görünmez">{I("fa-floppy-disk")}Taslak kaydet</button><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="tkGor-{tid}" data-bildir-sonra="Takvim kaydı güncellendi; önceki hal denetim izinde">{I("fa-check")}Kaydet ve yayımla</button></div>
</template>
"""


def sayfa_takvimler():
    canli = [r for r in TAKVIM if r[8] != "cop"]
    def olaylar(tur=None):
        return "".join(f'<a data-tanim="tkGor-{r[0]}" data-tarih="{r[3]}" data-ton="{TK_TUR[r[1]][1]}" data-ikon="fa-solid {TK_TUR[r[1]][2]}" data-not="{e(TK_TUR[r[1]][0] + " · " + r[4] + (" · " + r[5] if r[5] else ""))}" href="takvimler.html">{e(r[2])}</a>' for r in canli if tur is None or r[1] == tur)
    takvimler = "".join(f'<div class="kb-takvim" id="tkV-{k}" data-baslangic="23.11.2026" data-gorunum="ay" data-gun-ac="tkYeni"{"" if k == "hepsi" else " hidden"}><div class="kb-takvim-veri" hidden>{olaylar(None if k == "hepsi" else k)}</div></div>' for k in ["hepsi"] + list(TK_TUR))
    seg = f'<button type="button" class="chip is-on" aria-pressed="true" data-hedef="tkV-hepsi">Tümü<span class="ch-cnt">{len(canli)}</span></button>' + "".join(f'<button type="button" class="chip" aria-pressed="false" data-hedef="tkV-{k}">{I(v[2])}{v[0]}<span class="ch-cnt">{sum(1 for r in canli if r[1] == k)}</span></button>' for k, v in TK_TUR.items())
    rows = []
    for r in TAKVIM:
        tid, tur, bas_, tarih, kat, kurum, not_, onem, dur, eko, asama = r
        ad, ton, ik = TK_TUR[tur]
        durum = "cop" if dur == "cop" else tur
        rows.append(f'<tr data-satir="{tid}" data-durum="{durum}" data-kategori="{e(kat)}" data-onem="{onem}" data-yayin="{dur}" data-ara="{e(bas_ + " " + kat + " " + kurum + " " + ad)}" data-baslik="{e(bas_)}"{" data-onceki=\"gundem\"" if dur == "cop" else ""}>'
                    f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(bas_)}"></td>'
                    f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name" title="{e(bas_)}">{e(bas_)}</div><div class="rcp-by">{I(ik)}{ad} · {e(kat)}{" · " + e(kurum) if kurum else ""}</div></div></td>'
                    f'<td><span class="kb-tarih">{e(tarih)}</span></td>'
                    f'<td class="kb-gizle-m">{e(not_)}</td>'
                    f'<td class="kb-gizle-t"><span class="pstat {ONEM[onem][0]}">{ONEM[onem][1]}</span></td>'
                    f'<td><span class="pstat {"ok" if dur == "yayinda" else "off"}">{"Yayında" if dur == "yayinda" else "Taslak" if dur == "taslak" else "Çöpte"}</span></td>'
                    f'<td>{row_acts(("tanim", "tkGor-" + tid), ("tanim", "tkDz-" + tid), "sil")}</td></tr>')
    sab = "".join(tk_sablonlar(r) for r in TAKVIM)
    katlar = [("", "Bütün kategoriler", "")] + [(k, k, str(sum(1 for r in canli if r[4] == k))) for k in TK_KAT if any(r[4] == k for r in canli)]
    onemler = [("", "Bütün önemler", "")] + [(k, v[1], "") for k, v in ONEM.items()]
    yuksek = sum(1 for r in canli if r[7] == "yuksek")
    s = bas("Takvimler", "takvimler")
    s += f"""
<!-- TAKVİMLER (D4): gündem, ekonomik, sınav ve etkinlik takvimi tek ekranda. Üstte kb-takvim (tür süzgeci: her tür ayrı takvim, data-segment),
     altta liste (sekme = tür, sağ uçta Çöp). Kayıt çekmecede (görüntüle → düzenle); boş güne tıklayınca yeni kayıt (data-gun-ac). -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Takvimler</h1>
      <div class="ph-sub">{len(canli)} kayıt · {yuksek} yüksek önemli · takvimde boş bir güne tıklayarak o güne kayıt ekleyin</div>
    </div>
    <div class="ph-actions">
      <button type="button" class="btn btn-acc btn-sm" data-tanim="tkYeni">{I("fa-plus")}Yeni kayıt</button>
    </div>
  </div>

  <section class="pnl-card dash-row" data-durum-gizle="hata yukleniyor bos" aria-labelledby="tkTakvimBas">
    <div class="pc-head"><h2 class="pc-title" id="tkTakvimBas">{I("fa-calendar-days")}Takvim</h2></div>
    <div class="kb-liste-ust"><div class="chips" data-segment role="group" aria-label="Takvim türü">{seg}</div></div>
    <div class="pc-body">{takvimler}</div>
  </section>

  <section class="pnl-card" data-liste data-liste-ad="kayıt" data-sayfa-boy="25" data-liste-cop-not="Kayıt takvimlerden kalkar ve Çöp sekmesine taşınır" aria-labelledby="tkListeBas">
    <div class="pc-head"><h2 class="pc-title" id="tkListeBas">{I("fa-list")}Kayıtlar</h2></div>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Takvim türü">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
        {"".join(f'<button type="button" class="chip" role="tab" aria-selected="false" data-sekme="{k}">{v[0]}<span class="ch-cnt">0</span></button>' for k, v in TK_TUR.items())}
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="tkAra">Kayıtlarda ara</label><input id="tkAra" type="search" data-liste-ara placeholder="Başlık, kurum ya da kategori ara" autocomplete="off"></div>
      {secim("tkSuzKat", katlar, etk="Kategori:", bos="Tümü", ara="Kategori ara", suz="kategori")}
      {secim("tkSuzOnem", onemler, etk="Önem:", bos="Tümü", suz="onem")}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>
    <div class="kb-toplu" hidden>
      <b data-secili-say>0 kayıt seçildi</b><span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="yayin" data-bildir="Seçilen kayıtlar yayımlandı">{I("fa-paper-plane")}<span>Yayımla</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button>
    </div>
    <div class="ptable-wrap"><table class="ptable">
      <thead><tr><th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün kayıtları seç"></th><th class="kb-ana">Kayıt</th><th>Tarih</th><th class="kb-gizle-m">Not</th><th class="kb-gizle-t">Önem</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
      <tbody data-satirlar>{"".join(rows)}</tbody>
{durum_govdeleri(7, "fa-calendar-days", "Henüz takvim kaydı yok", "İlk kaydı ekleyin ya da takvimde boş bir güne tıklayın.", "Takvim kayıtları yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", bos_eylem=chr(10) + '            <button type="button" class="pe-tag" data-tanim="tkYeni">' + I("fa-plus") + 'Yeni kayıt</button>', iskelet='<td></td><td><div class="rcp-id"><span></span></div></td><td><span></span></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="takvimler.html")}    </table></div>
{pager(sayfalar=False)}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup" data-durum-icin="gundem ekonomik sinav etkinlik">Kayıt</div>
      <button type="button" data-durum-icin="gundem ekonomik sinav etkinlik" data-bildir="Kopyası taslak olarak oluşturuldu (prototip)">{I("fa-copy")}Kopyasını oluştur</button>
      <button type="button" data-durum-icin="gundem ekonomik sinav etkinlik" data-bildir="Kayıt sitede ilgili takvim sayfasında açılır (prototip)">{I("fa-arrow-up-right-from-square")}Sitede görüntüle</button>
      <button type="button" data-durum-icin="gundem ekonomik sinav etkinlik" data-roller="super gyy" data-bildir="Denetim izi bu kayda süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
      <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten geri al</button>
      <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı olarak sil</button>
    </div>
  </section>
</main>
</div>

<template id="tkYeni" data-baslik="Yeni takvim kaydı" data-alt="Kayıt seçtiğiniz türün takvim sayfasında görünür" data-zorunlu-kayit="ozel-dikeyler.takvim">
{tk_form("yeni")}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm" data-kaydet-tur="taslak" data-sablon-ac="tkEklendi" data-bildir-sonra="Taslak olarak kaydedildi; sitede görünmez">{I("fa-floppy-disk")}Taslak kaydet</button><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="tkEklendi" data-bildir-sonra="Takvim kaydı eklendi; denetim izine yazıldı">{I("fa-plus")}Ekle ve yayımla</button></div>
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
    return f"""        <div class="frow"><span class="flabel">Kaynak önceliği<span class="fhint kb-sag">Sürükleyerek sıralayın; birincil düşerse sıradaki devreye girer</span></span>
          <div class="kb-madde" data-siralanir aria-label="Kaynak önceliği">{sat}</div>
          <span class="fhint">Kaynak ekleme ve API anahtarı Entegrasyonlar ekranındadır; burada yalnız öncelik ve kullanım ayarlanır.</span></div>
"""


def periyot(sid, gun, gb, onb, ob, gecikme=None):
    birim = [("saniye", "saniye", ""), ("dakika", "dakika", ""), ("saat", "saat", ""), ("gün", "gün", "")]
    return f"""        <div class="form-grid kb-iki-sutun">
          <div class="frow"><label for="{sid}Per">Güncelleme periyodu</label><div class="frow two"><input class="finput" id="{sid}Per" inputmode="numeric" value="{gun}">{secim(sid + "PerB", birim, deger=gb, bos="Birim")}</div><span class="fhint">Kaynaktan bu sıklıkla yeni veri çekilir.</span></div>
          <div class="frow"><label for="{sid}Onb">Önbellek süresi</label><div class="frow two"><input class="finput" id="{sid}Onb" inputmode="numeric" value="{onb}">{secim(sid + "OnbB", birim, deger=ob, bos="Birim")}</div><span class="fhint">Okur bu süre boyunca aynı veriyi görür; kaynak yükü azalır.</span></div>
        </div>
""" + (f'        <div class="frow kb-ust-bosluk"><span class="flabel">Gecikme</span><div class="kb-birim"><input class="finput" inputmode="numeric" value="{gecikme}" aria-label="Gecikme süresi"><span>dakika</span></div><span class="fhint">Sitede değerlerin yanında “{gecikme} dk gecikmeli” yazar (lisans koşulu).</span></div>\n' if gecikme else "")


def hata_davranis(sid, sec="son"):
    return f"""        <div class="frow kb-ust-bosluk"><span class="flabel">Kaynak yanıt vermezse</span>
          <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="{sid}Hata"{" checked" if sec == "son" else ""}>Son veriyi saatiyle göster</label><label class="kb-secenek"><input type="radio" name="{sid}Hata"{" checked" if sec == "gizle" else ""}>Bandı gizle</label></div></div>
"""


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
     önbellek süresi, hata davranışı; durumlar kb-saglik dilinde. Bağlantı ve API anahtarı Entegrasyonlar'da (gizli değer burada yok). -->
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
    <div class="pc-head"><h2 class="pc-title" id="vbDurum">{I("fa-signal")}Bant durumu</h2><span class="kb-kap-alt">Son kontrol 16.04</span></div>
    <div class="pc-body"><div class="kb-saglik-izgara">
      <a class="kb-saglik" href="veri.html?sekme=vbPiyasa"><span class="kb-saglik-bas"><span class="status-nokta"></span>Piyasa</span><span class="kb-saglik-deger">{soz["piyasa"]["guncelleme"]}</span><span class="kb-saglik-meta">{len(pyasa)} araç · 15 dk gecikmeli · Dolar {next(a["deger"] for a in pyasa if a["ad"] == "Dolar")}</span></a>
      <a class="kb-saglik uyari" href="veri.html?sekme=vbHava"><span class="kb-saglik-bas"><span class="status-nokta"></span>Hava</span><span class="kb-saglik-deger">16.00</span><span class="kb-saglik-meta">81 il · İstanbul {h["sicaklik"]}°, {h["durum"].lower()} · turuncu kod uyarısı şeritte</span></a>
      <a class="kb-saglik" href="veri.html?sekme=vbNamaz"><span class="kb-saglik-bas"><span class="status-nokta"></span>Namaz vakitleri</span><span class="kb-saglik-deger">00.10</span><span class="kb-saglik-meta">81 il ve 40 yurt dışı şehri · günde bir</span></a>
      <a class="kb-saglik" href="veri.html?sekme=vbDeprem"><span class="kb-saglik-bas"><span class="status-nokta"></span>Deprem</span><span class="kb-saglik-deger">13.58</span><span class="kb-saglik-meta">Son: Sındırgı (Balıkesir) 2,8 · en büyük 4,1 · AFAD</span></a>
    </div></div>
  </section>

  <div class="form-layout">
  <section class="pnl-card" id="vbForm" data-form data-sekmeli aria-label="Veri bantları ayarları">
    <div class="sa-form-tabs" role="tablist" aria-label="Bantlar">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="vbPiyasa">{I("fa-chart-line")}Piyasa</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="vbHava">{I("fa-cloud-sun")}Hava</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="vbNamaz">{I("fa-mosque")}Namaz vakitleri</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="vbDeprem">{I("fa-house-crack")}Deprem</button>
    </div>

    <div class="sa-form-panel" id="vbPiyasa" role="tabpanel">
      <div class="form-sec">
{saglayicilar("vbP", [("Piyasa veri API", "Döviz, altın, borsa, emtia · 15 dk gecikmeli lisans", "ok", "Bağlı", "piyasa"), ("TCMB EVDS", "Gösterge kurlar ve politika faizi · yedek", "ok", "Hazır", ""), ("Borsa İstanbul gecikmeli veri", "Endeksler · yedek", "ok", "Hazır", ""), ("EPDK akaryakıt fiyatları", "Akaryakıt · günde bir", "ok", "Bağlı", "")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbP", 1, "dakika", 60, "saniye", gecikme=15)}        <div class="toggle-row kb-ust-bosluk"><span>Piyasa kapalıyken çekme<small>Hafta sonu ve resmî tatilde son kapanış gösterilir; kaynak kotası harcanmaz</small></span><label class="toggle"><input type="checkbox" checked aria-label="Piyasa kapalıyken çekme"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-arrow-right-arrow-left")}Şeritte görünenler<span class="fs-ek">Sitenin üst şeridi · sırası buradaki sıra</span></div>
        <div class="kb-cip-girdi" data-havuz-kapali data-havuz='{e(havuz)}'>{cip}<input type="text" placeholder="Araç ekle" aria-label="Şeride araç ekle"><div class="pnl-menu kb-cip-oneri"></div></div>
        <span class="fhint">Kur ve altında satış fiyatı gösterilir ve “satış” etiketi taşır. Araç listesi kaynaktan gelir.</span>
{hata_davranis("vbP")}      </div>
    </div>

    <div class="sa-form-panel" id="vbHava" role="tabpanel" hidden>
      <div class="form-sec">
{saglayicilar("vbH", [("Hava durumu API", "81 il · 6 günlük ve saatlik tahmin", "ok", "Bağlı", "hava"), ("Meteoroloji Genel Müdürlüğü", "Resmî uyarılar (sarı, turuncu, kırmızı kod)", "ok", "Hazır", "")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbH", 30, "dakika", 15, "dakika")}        <div class="frow kb-ust-bosluk"><span class="flabel">Varsayılan şehir</span>{secim("vbHSehir", sehirler, deger="İstanbul", bos="Şehir seçin", ara="Şehir ara")}<span class="fhint">Konum izni vermeyen ya da şehir seçmemiş okura gösterilir.</span></div>
        <div class="toggle-row kb-ust-bosluk"><span>Turuncu ve kırmızı kod uyarısını şeritte göster<small>Meteoroloji uyarısı süresince sitenin üstünde uyarı şeridi çıkar</small></span><label class="toggle"><input type="checkbox" checked aria-label="Hava uyarısını şeritte göster"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
{hata_davranis("vbH")}      </div>
    </div>

    <div class="sa-form-panel" id="vbNamaz" role="tabpanel" hidden>
      <div class="form-sec">
{saglayicilar("vbN", [("Diyanet İşleri Başkanlığı", "81 il ve yurt dışı şehirleri · resmî vakitler", "ok", "Bağlı", "namaz")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbN", 1, "gün", 24, "saat")}        <div class="frow kb-ust-bosluk"><span class="flabel">Varsayılan şehir</span>{secim("vbNSehir", sehirler, deger="İstanbul", bos="Şehir seçin", ara="Şehir ara")}</div>
        <div class="toggle-row kb-ust-bosluk"><span>Yurt dışı şehirleri<small>Namaz vakitleri sayfasında 40 yurt dışı şehri listelenir</small></span><label class="toggle"><input type="checkbox" checked aria-label="Yurt dışı şehirleri"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
{hata_davranis("vbN")}      </div>
    </div>

    <div class="sa-form-panel" id="vbDeprem" role="tabpanel" hidden>
      <div class="form-sec">
{saglayicilar("vbD", [("AFAD", "Son depremler · resmî kaynak", "ok", "Hazır", ""), ("Kandilli Rasathanesi", "Son depremler · yedek", "ok", "Hazır", "")])}      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-clock")}Güncelleme</div>
{periyot("vbD", 1, "dakika", 30, "saniye")}        <div class="form-grid kb-iki-sutun kb-ust-bosluk">
          <div class="frow"><label for="vbDMin">Listede en küçük büyüklük</label><div class="kb-birim"><input class="finput" id="vbDMin" inputmode="decimal" value="2,0"><span>büyüklük</span></div><span class="fhint">Afet ve Acil Durum sayfasındaki “Son depremler” listesi.</span></div>
          <div class="frow"><label for="vbDSerit">Şeritte gösterme eşiği</label><div class="kb-birim"><input class="finput" id="vbDSerit" inputmode="decimal" value="4,0"><span>ve üstü</span></div><span class="fhint">Bu büyüklük ve üstündeki deprem 6 saat şeritte kalır.</span></div>
        </div>
        <div class="toggle-row kb-ust-bosluk"><span>5,0 ve üstünde editörlere haber ver<small>Panelde bildirim; son dakika ve push kararı editörde kalır</small></span><label class="toggle"><input type="checkbox" checked aria-label="Büyük depremde editörlere haber ver"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
{hata_davranis("vbD", "gizle")}      </div>
    </div>
  </section>

  <aside class="side-card" aria-label="Son değişiklikler">
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-clock-rotate-left")}Son değişiklikler</h2></div>
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
"""
    s += son()
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
IL_DURUM = {"yayinda": ("ok", "Yayında"), "taslak": ("off", "Taslak"), "suresi": ("wait", "Süresi doldu"), "cop": ("off", "Çöpte")}


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
                    f'<td>{row_acts(("href", SITE + "resmi-ilan-detay.html") if dur == "yayinda" else ("href", f"ilan.html?id={iid}", "ozel-dikeyler.ilan"), ("href", f"ilan.html?id={iid}", "ozel-dikeyler.ilan"), "sil", gor_ad="Sitede görüntüle" if dur == "yayinda" else "Önizle")}</td></tr>')
    turler = [("", "Bütün türler", "")] + [(t, t, str(sum(1 for x in ILANLAR if x[2] == t and x[7] != "cop"))) for t in IL_TUR]
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
      <a class="btn btn-acc btn-sm" data-hedef="ozel-dikeyler.ilan" data-hedef-ek="?yeni=1" href="ilan.html?yeni=1">{I("fa-plus")}Yeni ilan</a>
    </div>
  </div>

  <section class="pnl-card" data-liste data-liste-ad="ilan" data-sayfa-boy="25" data-liste-cop-not="İlan yayından kalkar ve Çöp sekmesine taşınır" aria-labelledby="ilListeBas">
    <h2 class="sr-only" id="ilListeBas">İlan listesi</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Duruma göre">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi" data-taban="1305">Tümü<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="yayinda" data-taban="1272">Yayında<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="taslak" data-taban="0">Taslak<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="suresi" data-taban="33">Süresi doldu<span class="ch-cnt">0</span></button>
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop" data-taban="0">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}<label class="sr-only" for="ilAra">İlanlarda ara</label><input id="ilAra" type="search" data-liste-ara placeholder="Başlık, kurum ya da tür ara" autocomplete="off"></div>
      {secim("ilSuzTur", turler, etk="Tür:", bos="Tümü", suz="tur")}
      {secim("ilSuzKurum", kurumlar, etk="Kurum:", bos="Tümü", ara="Kurum ara", suz="kurum")}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>
    <div class="kb-toplu" hidden>
      <b data-secili-say>0 ilan seçildi</b><span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen ilanlar yayından kaldırılıp taslağa alındı">{I("fa-eye-slash")}<span>Yayından kaldır</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe taşı</span></button>
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
    s = bas("İlan düzenle", "ilan", ' data-yeni-baslik="Yeni ilan"')
    s += f"""
<!-- İLAN DÜZENLE (D4; B-26 bekliyor → alanlar varsayım): Detay · SEO (8b: resmî ilan SEO ●, zengin metin ●, zamanlama ●, görsel —).
     Belge kb-dosya data-tur="belge". Kurum havuzdan (yerinde yönetilir, B2). Zorunlular kayıtta: ozel-dikeyler.ilan. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1 data-yeni-metin="Yeni ilan">İlan düzenle</h1>
      <div class="ph-sub" data-yeni-metin="Taslak · henüz kaydedilmedi">{tur} · Karayolları Genel Müdürlüğü · {yay}'da yayımlandı · {gor} görüntülenme</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ozel-dikeyler.ilanlar" href="ilanlar.html">{I("fa-arrow-left")}İlanlara dön</a>
      <a class="btn btn-ghost btn-sm" data-yeni-gizle href="{SITE}resmi-ilan-detay.html" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Sitede görüntüle</a>
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
        <div class="frow"><label for="ilOzet">Kısa açıklama</label>
          <textarea class="ftext" id="ilOzet" data-sayac="160|200" rows="2">Kuzey Marmara Otoyolu bağlantı yollarında bakım ve onarım işi açık ihale usulüyle verilecek; teklifler 9 Aralık'a kadar alınacak.</textarea>
          <div class="char-meter"><span>İlan sayfasında başlığın altında; paylaşımda açıklama</span><b>0 / 160</b></div></div>
      </div></div>
      <div class="kb-ai-adim" data-ai-adim data-ai-kaynak="#ilBaslik" data-yeni-goster hidden>
        <div class="kaa-bas"><span class="kaa-ikon">{I("fa-wand-magic-sparkles")}</span><div><b>Gerisini AI ile üret</b><span data-ai-durum>Başlığı yazın ve ilan metnini yapıştırın; işaretli bölümler bunlardan üretilir. AI ilan metnini değiştirmez.</span></div></div>
        <div class="kaa-secim" role="group" aria-label="Üretilecek bölümler"><label class="kb-secenek"><input type="checkbox" value="ilozet" checked>Kısa açıklama</label><label class="kb-secenek"><input type="checkbox" value="seo" checked>SEO</label></div>
        <div class="kaa-alt"><button type="button" class="btn btn-acc btn-sm" data-ai-uret disabled>{I("fa-wand-magic-sparkles")}Gerisini üret</button><span class="fhint" data-ai-neden>Önce başlık</span></div>
      </div>
      <div class="form-sec">
        <div class="form-grid kb-iki-sutun">
          <div class="frow"><span class="flabel">İlan türü</span>
            {secim("ilTur", turler, deger=tur, bos="Tür seçin", ek=' data-alan-id="tur" data-zorunlu-metin="İlan türünü seçin"')}
            <span class="fhint">Sitedeki sekmeler: İhale, Satış, Kiralama, Personel.</span>
            <div class="ferr">{I("fa-circle-exclamation")}İlan türünü seçin.</div></div>
          <div class="frow"><span class="flabel">Kurum</span>
            <div class="kb-cip-girdi" data-alan-id="kurum" data-zorunlu-metin="İlanı veren kurumu seçin" data-havuz-yonet data-kullanim-birim="ilanda" data-havuz='{e(kurumlar)}'><span class="kb-cip" data-deger="{e(kur)}"><span>{e(kur)}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span><input type="text" placeholder="Kurum ara; yoksa yazıp ekleyin" aria-label="Kurum"><div class="pnl-menu kb-cip-oneri"></div></div>
            <div class="ferr">{I("fa-circle-exclamation")}İlanı veren kurumu seçin.</div></div>
          <div class="frow"><label for="ilNo">İlan ya da ihale kayıt numarası</label><input class="finput" id="ilNo" value="İKN 2026/1849302"><span class="fhint">İhalede EKAP kayıt numarası; isteğe bağlı.</span></div>
          <div class="frow"><span class="flabel">Son başvuru</span>
            <div class="kb-tarih-sec" id="ilBitis" data-alan-id="bitis" data-deger="2026-12-09 10.00" data-enaz="bugun" data-zorunlu-metin="Son başvuru tarihini seçin">
              <button type="button" class="kb-tarih-btn" data-acilir="ilBitisMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
              <div class="pnl-menu kb-tarih-menu" id="ilBitisMenu" role="dialog" aria-label="Tarih ve saat seç"></div></div>
            <span class="fhint">Sitede kartta “Son gün”; geçince ilan “Süresi doldu”ya geçer.</span>
            <div class="ferr">{I("fa-circle-exclamation")}Son başvuru tarihini seçin.</div></div>
        </div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-align-left")}İlan metni<span class="fs-ek">Kurumun yayımladığı metin; değiştirmeden aktarın</span></div>
        <div class="kb-editor" data-editor-ad="İlan metni">
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
        <div class="sc-field"><span class="flabel">Yayın zamanı</span>
          <div class="kb-tarih-sec" id="ilYayin" data-deger="2026-11-23 09.00" data-yeni-bos data-bos="Yayımlanınca o anın saati" data-temizlenir="1">
            <button type="button" class="kb-tarih-btn" data-acilir="ilYayinMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
            <div class="pnl-menu kb-tarih-menu" id="ilYayinMenu" role="dialog" aria-label="Tarih ve saat seç"></div></div></div>
        <div class="toggle-row"><span>Son başvurudan sonra listede tut<small>“Süresi doldu” etiketiyle 30 gün daha görünür</small></span><label class="toggle"><input type="checkbox" checked aria-label="Süresi dolunca listede tut"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      </div>
    </section>
{seo_skor(88)}  </aside>
  </div>

  <div class="kb-kaydet" data-form-icin="ilForm">
    <div class="kk-durum">{I("fa-circle-check")}<span data-yeni-metin="Henüz kaydedilmedi">Kaydedildi · 23.11.2026 09.00 · Ayşe Yıldız</span></div>
    <div class="kk-sag">
      <button type="button" class="btn btn-ghost btn-sm" data-kaydet data-kaydet-tur="taslak" data-kaydet-metin="Taslak olarak kaydedildi" data-bildir="Taslak kaydedildi; yayındaki hal değişmedi">{I("fa-floppy-disk")}Taslak kaydet</button>
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
           "ilanlar.html": sayfa_ilanlar, "ilan.html": sayfa_ilan}
    for ad, fn in yaz.items():
        (BURA / ad).write_text(fn(), encoding="utf-8")
        print("yazıldı:", ad)
