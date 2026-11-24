#!/usr/bin/env python3
"""AI Haber Havuzu modülü · sayfa üretici (yalnızca moduller/ai-havuz/ altına yazar).

Kullanım:  python3 -I moduller/ai-havuz/_uret.py && python3 -I araclar/menu_yaz.py --yalniz moduller/ai-havuz

Kaynaklar (yalnızca okunur): public sözlük (ornek_veri.json), veri/panel.json (ai_kaynakli), moduller.json (kaynak grupları,
okuma zorunluluğu, otomatik yayın), moduller/haberler/duzenle.html (kategori, yazar, tür, alt konu listeleri), _veri.py.
Sayfalar: index (havuz), duzenle, kaynaklar, motor, cron, ayarlar. Bileşenler yalnız UI kitten; sayfada stil yok.
"""
import html, json, re, sys
from pathlib import Path

BURA = Path(__file__).resolve().parent
KOK = BURA.parents[1]
PUB = KOK.parent / "dadahaber-prototip"
SITE = "https://gaviaworks-dev.github.io/dadahaber-prototip/"
sys.path.insert(0, str(BURA))
from _veri import *  # noqa

e = lambda s: html.escape(str(s), quote=True)
soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
pv = json.loads((KOK / "veri" / "panel.json").read_text(encoding="utf-8"))
kayit = json.loads((KOK / "moduller.json").read_text(encoding="utf-8"))
MOD = [m for m in kayit["moduller"] if m["id"] == "ai-havuz"][0]
AY = MOD["ayarlar"]
GRUPLAR = AY["kaynak_gruplari"]
KANAL = {k["id"]: k for k in AY["yayin_kanallari"]}
OKUMA = AY["okuma_zorunlulugu"]
ESIK = AY["otomatik_yayin"]["esik"]
ROL_AD = {r["id"]: r["ad"] for r in kayit["roller"]}
HB = (KOK / "moduller" / "haberler" / "duzenle.html").read_text(encoding="utf-8")
HBL = (KOK / "moduller" / "haberler" / "index.html").read_text(encoding="utf-8")
HABER = {h["id"]: h for h in soz["haberler"]}
KY = {k[0]: k for k in KAYNAKLAR}
GA = {g["id"]: g for g in GRUPLAR}


def isaret(ad):
    m = re.search(r"<!--P:%s-->(.*?)<!--/P:%s-->" % (ad, ad), HB, re.S)
    return m.group(1)


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
<body data-sayfa="ai-havuz.{sayfa}"{ek}>
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


def kanal_ikon(kanallar):
    t = " · ".join(KANAL[k]["ad"] for k in kanallar) or "Kanal yok"
    ic = "".join(f'<i class="fa-solid {KANAL[k]["ikon"]}{" is-on" if k in kanallar else ""}" aria-hidden="true"></i>' for k in KANAL)
    return f'<span class="kb-kanal-ikon" title="{e(t)}" aria-label="Yayın kanalları: {e(t)}">{ic}</span>'


def kanallar_html(kanallar, salt=False, ad="Yayın kanalları"):
    d = " disabled" if salt else ""
    ic = "".join(f'<label class="kb-kanal"><input type="checkbox" value="{k}"{" checked" if k in kanallar else ""}{d}><span>{I(v["ikon"])}{v["ad"]}</span></label>' for k, v in KANAL.items())
    return f'<div class="kb-kanallar{" is-salt" if salt else ""}" role="group" aria-label="{e(ad)}">{ic}</div>'


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


def pager(n_toplam_metin=True, sayfalar=True):
    if not sayfalar:
        return '    <div class="pager"><div class="pager-info">—</div></div>\n'
    return f"""    <div class="pager">
      <div class="pager-info">—</div>
      <div class="pager-btns">
        <button type="button" class="pg-btn" disabled aria-label="Önceki sayfa">{I("fa-chevron-left")}</button>
        <button type="button" class="pg-btn is-on" aria-current="page">1</button>
        <button type="button" class="pg-btn pg-sayi" data-bildir-pg>2</button>
        <span class="pg-dots pg-sayi">…</span>
        <button type="button" class="pg-btn pg-sayi" data-bildir-pg>58</button>
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


def kaynak_kanallari(kids):
    return GA[KY[kids[0]][4]]["kanallar"]


def reddet_sablonu():
    ops = "".join(f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="redNeden" value="{k}"><span><b>{a}</b><small>{al}</small></span></label>' for k, a, al in RED_NEDEN)
    return f"""<template id="aiReddet" data-baslik="Haberi reddet" data-alt="Neden seçin · reddedilen haber Reddedilen sekmesine geçer, oradan taslağa geri alınabilir" data-zorunlu-kayit="ai-havuz.reddet">
  <div class="kb-fs">
    <div class="frow"><span class="flabel">Neden</span>
      <div class="kb-kart-sec" data-alan-id="neden" data-zorunlu-metin="Reddetme nedenini seçin">{ops}</div>
      <div class="ferr">{I("fa-circle-exclamation")}Reddetme nedenini seçin.</div></div>
    <div class="frow"><label for="redNot">Açıklama</label>
      <textarea class="ftext" id="redNot" rows="3" data-sayac="200|280" placeholder="İsteğe bağlı · ör. aynı olay 15.42'de Sibel Arslan imzasıyla yayımlandı"></textarea>
      <div class="char-meter"><span>Reddedilen sekmesinde ve denetim izinde görünür</span><b>0 / 200</b></div></div>
    <div class="toggle-row"><span>Bu kaynaktan benzerlerini daha düşük öncelikle getir<small>Neden “Tekrar” ya da “Kapsam dışı” ise AI aynı türdeki içeriğe daha düşük güven verir</small></span><label class="toggle"><input type="checkbox" aria-label="Benzerlerini daha düşük öncelikle getir"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-danger btn-sm" data-dogrula=".kb-pencere .kb-kap-govde" data-sonra-kapat data-onay-baslik="Haber reddedilsin mi?" data-onay-metin="Haber yayımlanmaz ve Reddedilen sekmesine geçer; oradan taslağa geri alınabilir. Neden ve işlem denetim izine yazılır." data-onay-evet="Reddet" data-onay-tehlike data-onay-ikon="fa-ban" data-sonra-durum="reddedilen" data-sonra-durum-ad="Reddedildi" data-sonra-durum-sinif="off" data-bildir-sonra="Haber reddedildi; Reddedilen sekmesinde">{I("fa-ban")}Reddet</button></div>
</template>
"""


# ================================================================== HAVUZ (index.html)
GORSEL_AD = {"temiz": "Temiz", "kirpildi": "AI kırparak temizledi", "eksik": "Görsel eksik"}
GORSEL_IKON = {"temiz": "fa-image", "kirpildi": "fa-crop-simple", "eksik": "fa-image"}


def havuz_satir(r):
    """r: dict(id, baslik, kat, alt, kaynaklar, guven, gdurum, gorsel, cekilme, durum, durum_ad, durum_sinif, yayin, href, gor, onaylayan, neden, yayin_zaman)"""
    k1 = KY[r["kaynaklar"][0]]
    grup = k1[4]
    kanal = GA[grup]["kanallar"]
    ek = len(r["kaynaklar"]) - 1
    thumb = (f'<span class="rcp-thumb" style="background-image:url(../../veri/gorsel/kucuk/{r["gorsel"]}.jpg)"></span>' if r["gdurum"] != "eksik"
             else f'<span class="rcp-thumb kb-yok" title="Görsel eksik">{I("fa-image")}</span>')
    alt_satir = []
    if r["durum"] == "yayinlanan":
        alt_satir.append(("Otomatik yayımlandı · " if r["yayin"] == "otomatik" else f'{e(r["onaylayan"])} onayladı · ') + e(tarih_kisa(r["yayin_zaman"])))
    elif r["durum"] in ("reddedilen", "cop"):
        alt_satir.append(f'Reddedildi: {e(r["neden"])} · {e(r["onaylayan"])}')
    else:
        alt_satir.append(f'{e(tarih_kisa(r["cekilme"]))} · Öneri: {e(r["kat"])} › {e(r["alt"])}')
    by = " · ".join(alt_satir)
    gd = r["gdurum"]
    ara = " ".join([r["baslik"], k1[1], r["kat"], r["alt"], grup, GA[grup]["ad"]])
    kaynak_by = f'{grup} · ' + (f'+{ek} kaynak' if ek else "tek kaynak")
    tum = " · ".join(f'{n + 1}. {KY[k][1]} ({KY[k][4]})' for n, k in enumerate(r["kaynaklar"]))
    eye = r["gor"]
    duz = ("href", r["href"])
    ozet = (f' data-href="{e(r["href"])}" data-baslik="{e(r["baslik"])}"')
    return (f'<tr data-satir="{r["id"]}" data-durum="{r["durum"]}" data-grup="{grup}" data-kategori="{e(r["kat"])}" data-gorsel="{gd}" data-yayin="{r["yayin"]}" data-ara="{e(ara)}"{ozet}'
            f'{" data-onceki=\"reddedilen\"" if r["durum"] == "cop" else ""}>'
            f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(r["baslik"])}"></td>'
            f'<td class="kb-ana"><div class="rcp-cell">{thumb}<div class="rcp-id"><div class="rcp-name" title="{e(r["baslik"])}">{e(r["baslik"])}</div><div class="rcp-by">{by}</div></div></div></td>'
            f'<td><span class="kb-guven" data-guven="{r["guven"]}" data-esik="{ESIK}"></span></td>'
            f'<td class="kb-gizle-m"><div class="rcp-id" title="{e(tum)}"><div class="rcp-name">{e(KISA.get(k1[0], k1[1]))}</div><div class="rcp-by">{kaynak_by}</div></div></td>'
            f'<td class="kb-gizle-t">{kanal_ikon(kanal)}</td>'
            f'<td><span class="pstat {r["durum_sinif"]}">{e(r["durum_ad"])}</span></td>'
            f'<td>{row_acts(eye, duz, "sil", gor_ad=r.get("gor_ad", "Önizle"))}</td></tr>')


def havuz_satirlari():
    rows = []
    for (i, b, kat, alt, ks, g, gd, gor, cek, _) in TASLAK:
        href = f"duzenle.html?id={gd}"
        rows.append(dict(id=i, baslik=b, kat=kat, alt=alt, kaynaklar=ks, guven=g, gdurum=gd, gorsel=gor, cekilme=cek, durum="taslak",
                         durum_ad="Görsel eksik" if gd == "eksik" else "Onay bekliyor", durum_sinif="warm" if gd == "eksik" else "wait",
                         yayin="", href=href, gor=("href", href, "ai-havuz.duzenle"), onaylayan="", neden="", yayin_zaman=""))
    yay = []
    for hid, ks, g, gd in OTOMATIK:
        h = HABER[hid]
        yay.append((hid, ks, g, gd, "otomatik", "", h))
    for hid, v in pv["ai_kaynakli"]["kayitlar"].items():
        h = HABER[hid]
        yay.append((hid, [KAYNAK_AD_ID[v["kaynak"]]] + IKINCI.get(hid, []), v["skor"], "temiz", "editor", v["onay"], h))
    yay.sort(key=lambda x: (x[6]["tarih"], x[6]["saat"]), reverse=True)
    for hid, ks, g, gd, yol, onay, h in yay:
        m = re.search(r'data-satir="%s"[^>]*data-gorsel="\.\./\.\./veri/gorsel/(p\d+)\.jpg"' % re.escape(hid), HBL)
        gor = m.group(1) if m else ("p203" if "altin" in hid else "p178" if "urdun" in hid else "p158")
        t = f'{h["tarih"][8:10]}.{h["tarih"][5:7]}.{h["tarih"][:4]} {h["saat"]}'
        cek_dk = int(h["saat"][3:]) - 6
        cek = f'{t[:11]}{h["saat"][:3]}{cek_dk:02d}' if cek_dk >= 0 else t
        rows.append(dict(id=hid, baslik=h["baslik"], kat=h["bolum"], alt=h.get("alt_konu") or h["bolum"], kaynaklar=ks, guven=g, gdurum=gd, gorsel=gor,
                         cekilme=cek, durum="yayinlanan", durum_ad="Otomatik yayımlandı" if yol == "otomatik" else "Yayında",
                         durum_sinif="info" if yol == "otomatik" else "ok", yayin=yol, href=f"duzenle.html?id={gd}",
                         gor=("href", SITE + h.get("detay", "haber-detay.html")), gor_ad="Sitede görüntüle", onaylayan=onay, neden="", yayin_zaman=t))
    for (i, b, kat, alt, ks, g, gor, gd, cek, neden, kim, dur) in REDDEDILEN:
        rows.append(dict(id=i, baslik=b, kat=kat, alt=alt, kaynaklar=ks, guven=g, gdurum=gd, gorsel=gor, cekilme=cek, durum=dur,
                         durum_ad="Reddedildi", durum_sinif="off", yayin="", href=f"duzenle.html?id={gd}",
                         gor=("href", f"duzenle.html?id={gd}", "ai-havuz.duzenle"), onaylayan=kim, neden=neden, yayin_zaman=""))
    return rows


def sayfa_havuz():
    rows = havuz_satirlari()
    satir = "".join(havuz_satir(r) for r in rows)
    n_taslak = sum(1 for r in rows if r["durum"] == "taslak")
    n_eksik = sum(1 for r in rows if r["durum"] == "taslak" and r["gdurum"] == "eksik")
    gruplar = [("", "Bütün gruplar", "")] + [(g["id"], f'{g["id"]} · {g["ad"]}', "") for g in GRUPLAR]
    kats = sorted({r["kat"] for r in rows})
    katlar = [("", "Bütün kategoriler", "")] + [(k, k, "") for k in kats]
    gorsel = [("", "Bütün görseller", ""), ("temiz", "Temiz", ""), ("kirpildi", "AI kırparak temizledi", ""), ("eksik", "Görsel eksik", "")]
    yayin = [("", "Bütün yayınlar", ""), ("editor", "Editör onayıyla", ""), ("otomatik", "Otomatik yayımlandı", "")]
    okuma_roller = " ".join(OKUMA["roller"])
    muaf = " ".join(r for r in ROL_AD if r not in OKUMA["roller"] and r not in ("sosyal", "analist"))
    s = bas("AI Haber Havuzu", "havuz")
    s += f"""
<!-- AI HABER HAVUZU (K6, K8, Y1–Y3, YS1–YS7): üç sekme + Çöp; "Görsel eksik" ve "otomatik yayımlandı" satırda etiket ve süzgeç.
     Okuma zorunluluğu açık rolde (kayıt: okuma_zorunlulugu.roller) listeden onay ve Toplu Onayla görünmez. Maliyet kutuları yalnız ai-maliyet izniyle. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>AI Haber Havuzu</h1>
      <div class="ph-sub">{n_taslak} taslak onay bekliyor · {n_eksik}'ü görsel eksik · son çekim 16.00 · otomatik yayın kapalı</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.cron" data-izin="cron-saglik" href="cron.html">{I("fa-heart-pulse")}Hat sağlığı</a>
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.kaynaklar" data-roller="super gyy" href="kaynaklar.html">{I("fa-rss")}Kaynaklar</a>
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.ayarlar" data-roller="super gyy" href="ayarlar.html">{I("fa-sliders")}Otomatik yayın ve onay</a>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card warm">
      <div class="kpi-ico">{I("fa-robot")}</div>
      <div><div class="kpi-num">{n_taslak}</div><div class="kpi-lbl">Taslak onay bekliyor</div>
      <div class="kpi-delta down">{I("fa-image")}{n_eksik}'ü görsel eksik</div></div>
    </div>
    <div class="kpi-card ok">
      <div class="kpi-ico">{I("fa-circle-check")}</div>
      <div><div class="kpi-num">9</div><div class="kpi-lbl">Bugün onaylanıp yayımlandı</div>
      <div class="kpi-delta flat">{I("fa-stopwatch")}ortalama onay süresi 7 dk</div></div>
    </div>
    <div class="kpi-card info" data-izin="ai-maliyet">
      <div class="kpi-ico">{I("fa-microchip")}</div>
      <div><div class="kpi-num">1.560</div><div class="kpi-lbl">Bu ay işlenen içerik</div>
      <div class="kpi-delta flat">{I("fa-filter")}194'ü taslak oldu</div></div>
    </div>
    <div class="kpi-card" data-izin="ai-maliyet">
      <div class="kpi-ico">{I("fa-coins")}</div>
      <div><div class="kpi-num">₺1.993</div><div class="kpi-lbl">AI maliyeti · Kasım</div>
      <div class="kpi-delta flat">{I("fa-dollar-sign")}$50,47 · haber başı $0,26</div></div>
    </div>
    <div class="kpi-card" data-izin-yok="ai-maliyet">
      <div class="kpi-ico">{I("fa-ban")}</div>
      <div><div class="kpi-num">5</div><div class="kpi-lbl">Bugün reddedilen</div>
      <div class="kpi-delta flat">{I("fa-clone")}en sık neden: tekrar</div></div>
    </div>
    <div class="kpi-card" data-izin-yok="ai-maliyet">
      <div class="kpi-ico">{I("fa-gauge-high")}</div>
      <div><div class="kpi-num">%84</div><div class="kpi-lbl">Bugünkü ortalama güven</div>
      <div class="kpi-delta flat">{I("fa-circle-info")}otomatik yayın eşiği %{ESIK}</div></div>
    </div>
  </div>

  <div class="kb-bant bilgi dash-row" data-roller="{okuma_roller}">{I("fa-book-open-reader")}<span><b>Okumadan onay yok.</b> AI haberini onaylamak için haberi açın; Detay sekmesini sonuna kadar okuyunca “Onayla ve Yayınla” açılır. Listeden ve toplu onay bu rolde kapalıdır.</span></div>
  <div class="kb-bant bilgi dash-row" data-roller="super gyy">{I("fa-toggle-off")}<span><b>Otomatik yayın kapalı</b> (22.11.2026 23.30'dan beri). Bütün AI haberleri editör onayı bekler; “Otomatik yayımlandı” etiketli haberler açık olduğu dönemden.</span><a class="btn btn-ghost btn-sm kb-bant-eylem" data-hedef="ai-havuz.ayarlar" href="ayarlar.html">{I("fa-sliders")}Ayarlar</a></div>

  <section class="pnl-card" data-liste data-liste-ad="haber" data-sekme-ilk="taslak" data-ozet-sablon="aiOzet" data-sayfa-boy="25" data-liste-cop-not="Haber havuzdan kalkar ve Çöp sekmesine taşınır" aria-labelledby="aiListeBas">
    <h2 class="sr-only" id="aiListeBas">AI haber listesi</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Duruma göre">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="taslak" data-taban="0">Taslak<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="yayinlanan" data-taban="1414">Yayınlanan<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="reddedilen" data-taban="313">Reddedilen<span class="ch-cnt">0</span></button>
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop" data-taban="0">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>

    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}
        <label class="sr-only" for="aiAra">AI haberlerinde ara</label>
        <input id="aiAra" type="search" data-liste-ara placeholder="Başlık, kaynak ya da kategori ara" autocomplete="off">
      </div>
      {secim("aiSuzGrup", gruplar, etk="Grup:", bos="Tümü", suz="grup")}
      {secim("aiSuzKat", katlar, etk="Kategori:", bos="Tümü", ara="Kategori ara", suz="kategori")}
      {secim("aiSuzGorsel", gorsel, etk="Görsel:", bos="Tümü", suz="gorsel")}
      {secim("aiSuzYayin", yayin, etk="Yayın:", bos="Tümü", suz="yayin")}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>

    <div class="kb-toplu" hidden>
      <b data-secili-say>0 haber seçildi</b>
      <span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-acc btn-sm" data-roller="{muaf}" data-onay-baslik="Seçilen haberler onaylanıp yayımlansın mı?" data-onay-metin="Seçilen taslaklar kaynak gruplarının kanallarında hemen yayımlanır. Görseli eksik olanlar atlanır ve taslakta kalır (YS1). İşlem denetim izine önceki ve sonraki haliyle yazılır." data-onay-evet="Onayla ve yayınla" data-onay-ikon="fa-check-double" data-bildir-sonra="Seçilen haberler yayımlandı; görseli eksik olanlar taslakta kaldı">{I("fa-check-double")}<span>Toplu onayla</span></button>
      <button type="button" class="btn btn-ghost btn-sm" data-pencere="aiReddet">{I("fa-ban")}<span>Toplu reddet</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button>
    </div>

    <div class="ptable-wrap">
      <table class="ptable">
        <thead>
          <tr>
            <th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün haberleri seç"></th>
            <th class="kb-ana">Haber</th>
            <th>Güven</th>
            <th class="kb-gizle-m">Kaynak</th>
            <th class="kb-gizle-t">Kanallar</th>
            <th>Durum</th>
            <th><span class="sr-only">İşlemler</span></th>
          </tr>
        </thead>
        <tbody data-satirlar>{satir}</tbody>
{durum_govdeleri(7, "fa-robot", "Havuz boş", "Kaynaklardan yeni içerik geldiğinde AI taslakları burada listelenir. Sonraki tarama 16.10'da.", "AI haberleri yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin; sorun sürerse sistem yöneticisine haber verin.", iskelet='<td></td><td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td><td><span></span></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>')}      </table>
    </div>

{pager()}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup" data-durum-icin="taslak">Onay</div>
      <button type="button" data-durum-icin="taslak" data-kosul-icin="gorsel:temiz kirpildi" data-roller="{muaf}" data-onay-baslik="Haber onaylanıp yayımlansın mı?" data-onay-metin="Haber 1. kaynağın grubundaki kanallarda hemen yayımlanır. İşlem denetim izine yazılır." data-onay-evet="Onayla ve yayınla" data-onay-ikon="fa-check" data-sonra-durum="yayinlanan" data-sonra-durum-ad="Yayında" data-sonra-durum-sinif="ok" data-bildir-sonra="Haber onaylandı ve yayımlandı">{I("fa-check")}Onayla ve yayınla</button>
      <button type="button" data-durum-icin="taslak" data-roller="super gyy editor kat-ed" data-pencere="aiReddet">{I("fa-ban")}Reddet</button>
      <button type="button" data-durum-icin="reddedilen" data-roller="super gyy editor kat-ed" data-onay-baslik="Haber taslağa geri alınsın mı?" data-onay-metin="Haber Taslak sekmesine döner ve yeniden onay bekler. Reddetme kaydı denetim izinde kalır." data-onay-evet="Taslağa al" data-onay-ikon="fa-rotate-left" data-sonra-durum="taslak" data-sonra-durum-ad="Onay bekliyor" data-sonra-durum-sinif="wait" data-bildir-sonra="Haber taslağa geri alındı">{I("fa-rotate-left")}Taslağa geri al</button>
      <button type="button" data-durum-icin="yayinlanan" data-roller="super gyy editor" data-onay-baslik="Haber yayından kaldırılsın mı?" data-onay-metin="Önce: yayında → Sonra: taslak. Haber sitede, uygulamada ve sosyal medya kuyruğunda görünmez olur; adresi 410 döner. Denetim izine yazılır." data-onay-evet="Yayından kaldır" data-onay-tehlike data-onay-ikon="fa-eye-slash" data-sonra-durum="taslak" data-sonra-durum-ad="Onay bekliyor" data-sonra-durum-sinif="wait" data-bildir-sonra="Haber yayından kaldırıldı ve taslağa alındı">{I("fa-eye-slash")}Yayından kaldır</button>
      <div class="pmenu-div" data-durum-icin="taslak yayinlanan reddedilen"></div>
      <div class="kb-dm-grup" data-durum-icin="taslak yayinlanan reddedilen">Kaynak</div>
      <button type="button" data-durum-icin="taslak yayinlanan reddedilen" data-bildir="Kaynak haberi yeni sekmede açılır (prototip)">{I("fa-arrow-up-right-from-square")}Kaynak haberini aç</button>
      <button type="button" data-durum-icin="taslak" data-bildir="Aynı olayı veren diğer kaynaklar düzenleme ekranındaki Kaynak teyidi panelinde (prototip)">{I("fa-layer-group")}Teyit kaynaklarını gör</button>
      <div class="pmenu-div"></div>
      <div class="kb-dm-grup">Kayıt</div>
      <button type="button" data-roller="super gyy" data-bildir="Denetim izi bu kayda süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
      <div class="pmenu-div" data-durum-icin="cop"></div>
      <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten geri al</button>
      <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı olarak sil</button>
    </div>
  </section>
</main>
</div>

<template id="aiOzet" data-baslik="AI haber özeti">
  <div class="kb-ozet-gorsel" data-oz="gorsel"></div>
  <p class="kb-ozet-baslik" data-oz="baslik"></p>
  <div class="kb-kap-alt-cubuk"><a class="btn btn-acc btn-sm" data-oz="href" href="#icerik">{I("fa-pen")}Aç</a></div>
</template>
{reddet_sablonu()}"""
    s += son()
    return s


# ================================================================== ortak: grup hesapları
GUN_CEKIM = {"dakika": lambda n: 24 * 60 / n, "saat": lambda n: 24 / n, "gun": lambda n: 1 / n, "gün": lambda n: 1 / n}


def grup_hesap(gid):
    ek = GRUP_EK.get(gid, {"ornek": "", "siklik": 1, "birim": "gün", "yeni_oran": 1})
    ks = [k for k in KAYNAKLAR if k[4] == gid and k[5] != "cop"]
    etkin = [k for k in ks if k[5] in ("aktif", "hata")]
    cekim = round(len(etkin) * GUN_CEKIM[ek["birim"]](ek["siklik"]) * 30)
    haber = round(cekim * ek["yeni_oran"])
    usd = haber * HABER_BASI_USD
    return dict(ek=ek, ks=ks, etkin=etkin, cekim=cekim, haber=haber, usd=usd)


def siklik_metin(ek):
    return f'{ek["siklik"]} {ek["birim"]}{ {"dakika": "da", "saat": "te", "gün": "de"}[ek["birim"]] } bir'


BIRIMLER = [("dakika", "dakika", ""), ("saat", "saat", ""), ("gün", "gün", "")]


def kaynak_durum(k):
    return {"aktif": ("ok", "Etkin"), "pasif": ("off", "Pasif"), "hata": ("warm", "Hata"), "cop": ("off", "Çöpte")}[k[5]]


# ================================================================== KAYNAKLAR
def kaynak_gor_sablon(k):
    kid, ad, tip, url, gid, dur, son_, basari, haber30, not_ = k
    sinif, dad = kaynak_durum(k)
    g = GA[gid]
    bant = ""
    if dur == "hata":
        bant = f'<div class="kb-bant tehlike">{I("fa-triangle-exclamation")}<span><b>Son çekimler başarısız.</b> {e(not_)}. Kaynak sitesi erişimi engelliyor olabilir; adres değiştiyse düzenleyin. Bu sürede grup teyidi diğer kaynaklarla yapılır.</span></div>'
    elif dur == "pasif":
        bant = f'<div class="kb-bant bilgi">{I("fa-circle-pause")}<span><b>Pasif kaynak.</b> {e(not_)}. Çekilmez; eski haberlerdeki teyit kayıtları durur.</span></div>'
    log = {
        "hata": [("hata", "14.20.04", "403 Forbidden · 3. deneme · sonraki deneme 16.30"), ("hata", "13.20.02", "403 Forbidden"), ("bilgi", "12.20.11", "4 yeni içerik, 2 tekrar elendi")],
        "pasif": [("bilgi", son_.replace(" ", " · ") + ".00", "Kaynak pasifleştirildi; çekim durdu")],
    }.get(dur, [("bilgi", f"{son_}.0{len(ad) % 9}", f"{2 + len(ad) % 5} yeni içerik, {len(ad) % 4} tekrar elendi"),
               ("bilgi", "15.30.0" + str(len(ad) % 7), f"{1 + len(ad) % 3} yeni içerik"),
               ("uyari" if basari < 100 else "bilgi", "15.00.03", "Yavaş yanıt (4,2 sn)" if basari < 100 else "Değişiklik yok")])
    logh = "".join(f'<span class="kl-satir {s}"><span class="kl-zaman">{z}</span><span class="kl-seviye">{"uyarı" if s == "uyari" else s}</span><span class="kl-kaynak">{kid}</span><span>{e(m)}</span></span>' for s, z, m in log)
    tad, tik = TIP[tip]
    return f"""<template id="kyGor-{kid}" data-baslik="{e(ad)}" data-alt="{e(tad)} · {gid} · {e(g['ad'])}">
  {bant}
  <div class="kb-fs"><div class="kb-fs-tt">Durum</div><div class="sa-durum">
    <div><span>Durum</span><b><span class="pstat {sinif}">{dad}</span></b></div>
    <div><span>Grup</span><b>{gid} · {e(g['ad'])}</b></div>
    <div><span>Tip</span><b>{e(tad)}</b></div>
    <div><span>Adres</span><b>{e(url)}</b></div>
    <div><span>Son çekim</span><b>{e(son_)}</b></div>
    <div><span>Başarı · son 24 saat</span><b>%{basari}</b></div>
    <div><span>Havuza düşen · 30 gün</span><b>{sayi(haber30)} içerik</b></div>
    <div><span>Yayın kanalları (gruptan)</span><b>{kanal_ikon(g['kanallar'])}</b></div>
  </div></div>
  <div class="kb-fs"><div class="kb-fs-tt">Görsel</div><p class="fhint">Görsel izni kaynak başına ayarlanmaz (YS1). AI bu kaynaktan gelen her görseli temiz, AI kırparak temizledi ya da görsel eksik diye ayırır; son 30 günde bu kaynakta {3 + len(ad) % 6} görsel temizlenemedi ve haber “Görsel eksik” geldi.</p></div>
  <div class="kb-fs"><div class="kb-fs-tt">Son çekimler</div><pre class="kb-log">{logh}</pre><p class="fhint kb-ust-bosluk">Çekim günlüğü sistem logudur; silinemez ve değiştirilemez.</p></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="kyDz-{kid}">{I("fa-pen")}Düzenle</button></div>
</template>
"""


def kaynak_form(kid, k=None):
    ad, tip, url, gid, dur = (k[1], k[2], k[3], k[4], k[5]) if k else ("", "rss", "", "", "aktif")
    sid = kid
    tipler = "".join(f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="kyTip-{sid}" value="{t}"{" checked" if t == tip else ""}><span><b>{I(TIP[t][1])} {TIP[t][0]}</b><small>{ {"rss": "Akış adresi", "scraper": "Sayfa düzenli taranır", "haber-sitesi": "Sitenin haber listesi", "sosyal-hesap": "X, Telegram ya da benzeri hesap"}[t] }</small></span></label>' for t in TIP)
    grp = [(g["id"], f'{g["id"]} · {g["ad"]}', f'{len(grup_hesap(g["id"])["ks"])} kaynak') for g in GRUPLAR]
    return f"""  <div class="kb-fs">
    <div class="frow"><label for="kyAd-{sid}">Kaynak adı</label>
      <input class="finput" id="kyAd-{sid}" data-alan-id="ad" data-sayac="40|60" value="{e(ad)}" placeholder="ör. Anadolu Ajansı">
      <div class="char-meter"><span>Havuzda ve kaynak teyidinde görünür</span><b>0 / 40</b></div>
      <div class="ferr">{I("fa-circle-exclamation")}Kaynak adı zorunlu.</div></div>
    <div class="frow"><span class="flabel">Tip</span><div class="kb-kart-sec">{tipler}</div></div>
    <div class="frow"><label for="kyUrl-{sid}">Adres</label>
      <input class="finput" id="kyUrl-{sid}" data-alan-id="adres" inputmode="url" value="{e(url)}" placeholder="ör. aa.com.tr/tr/rss/default">
      <span class="fhint">RSS'te akış adresi, sitede haber listesinin adresi, hesapta profil adresi.</span>
      <div class="ferr">{I("fa-circle-exclamation")}Adres zorunlu.</div></div>
    <div class="frow"><span class="flabel">Kaynak grubu</span>
      {secim("kyGrup-" + sid, grp, deger=gid, bos="Grup seçin", ara="Grup ara", ek=' data-alan-id="grup" data-zorunlu-metin="Kaynağın grubunu seçin"')}
      <span class="fhint">Çekim sıklığı ve yayın kanalları gruptan gelir. Yeni grup <a class="kb-bag" data-hedef="ai-havuz.motor" href="motor.html">Kaynak Motoru'nda</a> eklenir.</span>
      <div class="ferr">{I("fa-circle-exclamation")}Kaynağın grubunu seçin.</div></div>
    <div class="toggle-row"><span>Etkin<small>Kapalıyken kaynak çekilmez; kayıtları durur</small></span><label class="toggle"><input type="checkbox"{" checked" if dur != "pasif" else ""} aria-label="Etkin"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
  <div class="kb-fs"><div class="kb-bant bilgi">{I("fa-image")}<span><b>Görsel izni kaynak başına değil (YS1).</b> AI her görseli temiz, AI kırparak temizledi ya da görsel eksik diye ayırır; kaynağın logosu ya da damgası temizlenemezse görsel kullanılmaz ve haber “Görsel eksik” gelir.</span></div></div>
"""


def kaynak_dz_sablon(k):
    kid = k[0]
    return f"""<template id="kyDz-{kid}" data-baslik="{e(k[1])} · düzenle" data-alt="Değişiklik sonraki çekimde geçerli olur; denetim izine önceki ve sonraki haliyle yazılır" data-zorunlu-kayit="ai-havuz.kaynak">
{kaynak_form(kid, k)}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="kyGor-{kid}" data-bildir-sonra="Kaynak kaydedildi; önceki hal denetim izinde">{I("fa-floppy-disk")}Kaydet</button></div>
</template>
"""


def kaynak_satir(k):
    kid, ad, tip, url, gid, dur, son_, basari, haber30, not_ = k
    sinif, dad = kaynak_durum(k)
    tad, tik = TIP[tip]
    g = GA[gid]
    kul = f'{gid} · {g["ad"]} grubunda; son 30 günde {sayi(haber30)} içeriğin kaynağı. Teyit kayıtları silinmez' if haber30 else ""
    durum = "cop" if dur == "cop" else dur
    ara = " ".join([ad, url, gid, g["ad"], tad])
    son_h = f'<span class="kb-tarih{" muted" if dur in ("pasif", "cop") else ""}">{e(son_)}</span>'
    bas_ = f'<td class="say kb-gizle-t">{"%" + str(basari) if dur not in ("pasif", "cop") else "—"}</td>'
    return (f'<tr data-satir="{kid}" data-durum="{durum}" data-grup="{gid}" data-tip="{tip}" data-ara="{e(ara)}" data-baslik="{e(ad)}"'
            f'{f" data-kullanim=\"{e(kul)}\"" if kul else ""}{" data-onceki=\"pasif\"" if dur == "cop" else ""}>'
            f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(ad)}"></td>'
            f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name" title="{e(ad)}">{e(ad)}</div><div class="rcp-by">{I(tik)}{e(tad)} · {e(url)}</div></div></td>'
            f'<td class="kb-gizle-m"><div class="rcp-id"><div class="rcp-name">{gid}</div><div class="rcp-by">{e(g["ad"])}</div></div></td>'
            f'<td class="kb-gizle-t">{son_h}</td>{bas_}'
            f'<td class="say kb-gizle-t">{sayi(haber30) if haber30 else "—"}</td>'
            f'<td><span class="pstat {sinif}" title="{e(not_)}">{dad}</span></td>'
            f'<td>{row_acts(("tanim", "kyGor-" + kid), ("tanim", "kyDz-" + kid), "sil")}</td></tr>')


def sayfa_kaynaklar():
    satir = "".join(kaynak_satir(k) for k in KAYNAKLAR)
    sab = "".join(kaynak_gor_sablon(k) + kaynak_dz_sablon(k) for k in KAYNAKLAR)
    canli = [k for k in KAYNAKLAR if k[5] != "cop"]
    etkin = [k for k in canli if k[5] in ("aktif", "hata")]
    hata = [k for k in canli if k[5] == "hata"]
    pasif = [k for k in canli if k[5] == "pasif"]
    gruplar = [("", "Bütün gruplar", "")] + [(g["id"], f'{g["id"]} · {g["ad"]}', str(len([k for k in canli if k[4] == g["id"]]))) for g in GRUPLAR]
    tipler = [("", "Bütün tipler", "")] + [(t, v[0], str(len([k for k in canli if k[2] == t]))) for t, v in TIP.items()]
    s = bas("Kaynaklar", "kaynaklar")
    s += f"""
<!-- KAYNAKLAR (Y1, YS1): liste + çekmecede görüntüle/düzenle (kaynağın kendi sayfası yok; satır tıklama = görüntüle). Görsel izni kaynak başına yok. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Kaynaklar</h1>
      <div class="ph-sub">{len(canli)} kaynak · {len(etkin)} etkin ({len(hata)}'i hatalı) · {len(pasif)} pasif · her 10 dakikada taranır</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.havuz" href="index.html">{I("fa-arrow-left")}Haber havuzu</a>
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.motor" data-roller="super" href="motor.html">{I("fa-gears")}Gruplar ve sıklık</a>
      <button type="button" class="btn btn-acc btn-sm" data-tanim="kyYeni">{I("fa-plus")}Yeni kaynak</button>
    </div>
  </div>

  <div class="kb-bant tehlike dash-row">{I("fa-triangle-exclamation")}<span><b>1 kaynak hata veriyor.</b> Defense News 14.20'den beri 403 döndürüyor; T3 grubunda teyit diğer kaynaklarla yapılıyor.</span><button type="button" class="btn btn-ghost btn-sm kb-bant-eylem" data-tanim="kyGor-defense-news">{I("fa-eye")}İncele</button></div>

  <section class="pnl-card" data-liste data-liste-ad="kaynak" data-sayfa-boy="25" data-liste-cop-not="Kaynak çekilmez ve Çöp sekmesine taşınır" aria-labelledby="kyListeBas">
    <h2 class="sr-only" id="kyListeBas">Kaynak listesi</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Duruma göre">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="aktif">Etkin<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="hata">Hatalı<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="pasif">Pasif<span class="ch-cnt">0</span></button>
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}
        <label class="sr-only" for="kyAra">Kaynaklarda ara</label>
        <input id="kyAra" type="search" data-liste-ara placeholder="Kaynak adı ya da adres ara" autocomplete="off">
      </div>
      {secim("kySuzGrup", gruplar, etk="Grup:", bos="Tümü", suz="grup")}
      {secim("kySuzTip", tipler, etk="Tip:", bos="Tümü", suz="tip")}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>
    <div class="kb-toplu" hidden>
      <b data-secili-say>0 kaynak seçildi</b>
      <span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="aktif" data-bildir="Seçilen kaynaklar etkinleştirildi; sonraki taramada çekilir">{I("fa-circle-play")}<span>Etkinleştir</span></button>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="pasif" data-bildir="Seçilen kaynaklar pasifleştirildi; denetim izine yazıldı">{I("fa-circle-pause")}<span>Pasifleştir</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-trash")}<span>Çöpe taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button>
    </div>
    <div class="ptable-wrap">
      <table class="ptable">
        <thead><tr>
          <th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün kaynakları seç"></th>
          <th class="kb-ana">Kaynak</th><th class="kb-gizle-m">Grup</th><th class="kb-gizle-t">Son çekim</th><th class="say kb-gizle-t">Başarı · 24 sa</th><th class="say kb-gizle-t">İçerik · 30 gün</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th>
        </tr></thead>
        <tbody data-satirlar>{satir}</tbody>
{durum_govdeleri(8, "fa-rss", "Henüz kaynak yok", "İlk kaynağı ekleyin; AI haber havuzu kaynaklardan beslenir.", "Kaynaklar yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", bos_eylem=chr(10) + '            <button type="button" class="pe-tag" data-tanim="kyYeni">' + I("fa-plus") + 'Yeni kaynak</button>', iskelet='<td></td><td><div class="rcp-id"><span></span></div></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td class="kb-gizle-t"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="kaynaklar.html")}      </table>
    </div>
{pager(sayfalar=False)}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup" data-durum-icin="aktif hata pasif">Çekim</div>
      <button type="button" data-durum-icin="aktif hata" data-onay-baslik="Kaynak şimdi çekilsin mi?" data-onay-metin="Grubun sıklığını beklemeden bu kaynak hemen taranır; yeni içerik varsa AI taslağı olarak havuza düşer." data-onay-evet="Şimdi çek" data-onay-ikon="fa-rotate" data-bildir-sonra="Kaynak kuyruğa alındı; birkaç saniye içinde çekilir">{I("fa-rotate")}Şimdi çek</button>
      <button type="button" data-durum-icin="aktif hata" data-onay-baslik="Kaynak pasifleştirilsin mi?" data-onay-metin="Önce: etkin → Sonra: pasif. Kaynak çekilmez; havuzdaki ve yayındaki haberlerin teyit kayıtları durur. Denetim izine yazılır." data-onay-evet="Pasifleştir" data-onay-tehlike data-onay-ikon="fa-circle-pause" data-sonra-durum="pasif" data-sonra-durum-ad="Pasif" data-sonra-durum-sinif="off" data-bildir-sonra="Kaynak pasifleştirildi">{I("fa-circle-pause")}Pasifleştir</button>
      <button type="button" data-durum-icin="pasif" data-onay-baslik="Kaynak etkinleştirilsin mi?" data-onay-metin="Önce: pasif → Sonra: etkin. Grubun sonraki taramasında çekilir. Denetim izine yazılır." data-onay-evet="Etkinleştir" data-onay-ikon="fa-circle-play" data-sonra-durum="aktif" data-sonra-durum-ad="Etkin" data-sonra-durum-sinif="ok" data-bildir-sonra="Kaynak etkinleştirildi">{I("fa-circle-play")}Etkinleştir</button>
      <div class="pmenu-div" data-durum-icin="aktif hata pasif"></div>
      <div class="kb-dm-grup" data-durum-icin="aktif hata pasif">Kayıt</div>
      <button type="button" data-durum-icin="aktif hata pasif" data-bildir="Kaynak adresi yeni sekmede açılır (prototip)">{I("fa-arrow-up-right-from-square")}Kaynak adresini aç</button>
      <button type="button" data-durum-icin="aktif hata pasif" data-bildir="Havuz bu kaynağa süzülerek açılır (prototip)">{I("fa-robot")}Bu kaynağın haberleri</button>
      <button type="button" data-durum-icin="aktif hata pasif" data-bildir="Denetim izi bu kayda süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
      <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten geri al</button>
      <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı olarak sil</button>
    </div>
  </section>
</main>
</div>

<template id="kyYeni" data-baslik="Yeni kaynak" data-alt="Kaynak ajans, haber sitesi ya da sosyal medya hesabı olabilir · ilk çekim kaydedince sıradaki taramada" data-zorunlu-kayit="ai-havuz.kaynak">
{kaynak_form("yeni")}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="kyEklendi" data-bildir-sonra="Kaynak eklendi; denetim izine yazıldı">{I("fa-plus")}Kaynağı ekle</button></div>
</template>
<template id="kyEklendi" data-baslik="Kaynak eklendi" data-alt="Sıradaki taramada (16.10) ilk kez çekilir">
  <div class="pnl-empty"><div class="pe-ico">{I("fa-circle-check")}</div><h2>Kaynak eklendi</h2><p>İlk çekim 16.10'daki taramada yapılır. Yeni içerik AI taslağı olarak havuza düşer; ilk 24 saatin başarısı listede görünür.</p></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm" data-kapat>{I("fa-check")}Tamam</button></div>
</template>
{sab}"""
    s += son()
    return s


# ================================================================== KAYNAK MOTORU (gruplar ve sıklık)
def grup_gor_sablon(g):
    gid = g["id"]
    h = grup_hesap(gid)
    satir = "".join(f'<div class="km-satir"><span class="km-yazi">{e(k[1])}<small>{TIP[k[2]][0]} · {e(k[3])}</small></span><span class="pstat {kaynak_durum(k)[0]}">{kaynak_durum(k)[1]}</span><button type="button" class="ia-btn" data-sablon-ac="kyGorM-{k[0]}" aria-label="{e(k[1])} ayrıntısı" title="Ayrıntı">{I("fa-eye")}</button></div>' for k in h["ks"])
    return f"""<template id="mtGor-{gid}" data-baslik="{gid} · {e(g['ad'])}" data-alt="{e(h['ek']['ornek'])}">
  <div class="kb-fs"><div class="kb-fs-tt">Grup</div><div class="sa-durum">
    <div><span>Çekim sıklığı</span><b>{siklik_metin(h['ek'])}</b></div>
    <div><span>Yayın kanalları</span><b>{kanal_ikon(g['kanallar'])}</b></div>
    <div><span>Etkin kaynak</span><b>{len(h['etkin'])} / {len(h['ks'])}</b></div>
    <div><span>Aylık tahmin</span><b>{sayi(h['cekim'])} çekim · {sayi(h['haber'])} içerik<span data-izin="ai-maliyet"> · ${para(h['usd'])}</span></b></div>
  </div></div>
  <div class="kb-fs"><div class="kb-fs-tt">Kaynaklar · {len(h['ks'])}</div><div class="kb-madde">{satir}</div>
    <p class="fhint">Kaynak eklemek ve düzenlemek için <a class="kb-bag" data-hedef="ai-havuz.kaynaklar" href="kaynaklar.html">Kaynaklar</a>; gruba bağlamak için “Düzenle”.</p></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="mtDz-{gid}">{I("fa-pen")}Düzenle</button></div>
</template>
""" + "".join(kaynak_gor_sablon(k).replace(f'id="kyGor-{k[0]}"', f'id="kyGorM-{k[0]}"').replace(f'data-sablon-ac="kyDz-{k[0]}">{I("fa-pen")}Düzenle', f'data-sablon-ac="mtGor-{gid}">{I("fa-arrow-left")}Gruba dön') for k in h["ks"])


def grup_form(gid, g=None):
    h = grup_hesap(gid) if g else None
    ad = g["ad"] if g else ""
    ek = h["ek"] if g else {"ornek": "", "siklik": "", "birim": "saat"}
    kanallar = g["kanallar"] if g else ["web", "uygulama", "sosyal"]
    havuz = json.dumps([k[1] for k in KAYNAKLAR if k[5] != "cop"], ensure_ascii=False)
    cip = "".join(f'<span class="kb-cip" data-deger="{e(k[1])}"><span>{e(k[1])}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for k in (h["ks"] if h else []))
    return f"""  <div class="kb-fs">
    <div class="frow"><label for="mtAd-{gid}">Grup adı</label>
      <input class="finput" id="mtAd-{gid}" data-alan-id="ad" data-sayac="30|40" value="{e(ad)}" placeholder="ör. Ajans, Düşük öncelikli dijital mecralar">
      <div class="char-meter"><span>Havuzda ve kaynak teyidinde görünür</span><b>0 / 30</b></div>
      <div class="ferr">{I("fa-circle-exclamation")}Grup adı zorunlu.</div></div>
    <div class="frow"><label for="mtOrnek-{gid}">Örnek açıklaması</label>
      <input class="finput" id="mtOrnek-{gid}" data-sayac="60|80" value="{e(ek['ornek'])}" placeholder="ör. örn. Anadolu Ajansı, DHA, İHA">
      <div class="char-meter"><span>Listede adın altında</span><b>0 / 60</b></div></div>
    <div class="frow"><span class="flabel">Çekim sıklığı</span>
      <div class="frow two">
        <input class="finput" id="mtSik-{gid}" data-alan-id="siklik" inputmode="numeric" value="{ek['siklik']}" aria-label="Çekim sıklığı sayısı" placeholder="ör. 2" data-zorunlu-metin="Çekim sıklığını yazın">
        {secim("mtBirim-" + gid, BIRIMLER, deger=ek['birim'], bos="Birim")}
      </div>
      <span class="fhint">Tarama her 10 dakikada çalışır; grubun son çekiminden bu yana süre dolmuşsa gruptaki kaynaklar çekilir.</span>
      <div class="ferr">{I("fa-circle-exclamation")}Çekim sıklığını yazın.</div></div>
    <div class="frow"><span class="flabel">Yayın kanalları</span>
      {kanallar_html(kanallar)}
      <p class="fhint" data-kanal-uyari hidden>Hiçbir kanal seçili değil: bu gruptan gelen haberler yayımlanmaz.</p>
      <span class="fhint">Bu gruptan gelen haber yalnız işaretli kanallarda yayımlanır; yalnız Sosyal Medya'ya giden gönderi bağlantısızdır (YS2). Kaynakları farklı gruplardan olan haberin kanallarını 1. kaynağın grubu belirler (YS4).</span></div>
    <div class="frow"><span class="flabel">Kaynaklar</span>
      <div class="kb-cip-girdi" data-havuz-kapali data-havuz='{e(havuz)}'>{cip}<input type="text" placeholder="Kaynak ara" aria-label="Kaynak ara"><div class="pnl-menu kb-cip-oneri"></div></div>
      <span class="fhint">Çıkarılan kaynak grupsuz kalır ve çekilmez. Listede olmayan kaynak <a class="kb-bag" data-hedef="ai-havuz.kaynaklar" href="kaynaklar.html">Kaynaklar</a> ekranında eklenir.</span></div>
    <div class="toggle-row"><span>Etkin<small>Kapalıyken gruptaki kaynakların hiçbiri çekilmez</small></span><label class="toggle"><input type="checkbox" checked aria-label="Grup etkin"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
  </div>
"""


def tasi_attr(gid, ad, n, satir=True):
    hed = "|".join(f'{x["id"]} · {x["ad"]}' for x in GRUPLAR if x["id"] != gid)
    return (f'data-tasi-sil data-tasi-ad="{gid} · {e(ad)}" data-tasi-sayi="{n}" data-tasi-birim="kaynak" data-tasi-birim-cogul="kaynaklar" data-tasi-ikon="fa-rss" '
            f'data-tasi-soru="Kaynaklar hangi gruba taşınsın?" data-tasi-hedefler="{e(hed)}" '
            f'data-tasi-not="Taşınan kaynaklar yeni grubun sıklığı ve kanallarıyla çekilir. “{gid} · {e(ad)}” çöpe gider ve oradan geri alınabilir; işlem denetim izine yazılır."'
            + (" data-sonra-kaldir" if satir else ""))


def grup_dz_sablon(g):
    gid = g["id"]
    h = grup_hesap(gid)
    return f"""<template id="mtDz-{gid}" data-baslik="{gid} · {e(g['ad'])} · düzenle" data-alt="Değişiklik sonraki taramada geçerli olur; denetim izine önceki ve sonraki haliyle yazılır" data-zorunlu-kayit="ai-havuz.grup">
{grup_form(gid, g)}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm danger kb-sol" {tasi_attr(gid, g['ad'], len(h['ks']), satir=False)}>{I("fa-trash")}Grubu sil</button><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="mtGor-{gid}" data-bildir-sonra="Grup kaydedildi; önceki hal denetim izinde">{I("fa-floppy-disk")}Kaydet</button></div>
</template>
"""


def grup_satir(g, cop=False):
    gid = g["id"]
    if cop:
        return (f'<tr data-satir="grp-{gid}" data-durum="cop" data-onceki="aktif" data-ara="{e(g["ad"])}" data-baslik="{gid} · {e(g["ad"])}">'
                f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name">{e(g["ad"])}</div><div class="rcp-by">{e(g["ornek"])}</div></div></td>'
                f'<td><span class="kb-tarih muted">{siklik_metin(g)}</span></td>'
                f'<td class="say kb-gizle-m">0 / 0</td><td class="kb-gizle-m">{kanal_ikon(g["kanallar"])}</td><td class="kb-gizle-t">—</td>'
                f'<td><span class="pstat off">Çöpte</span></td>'
                f'<td>{row_acts(("kilit", "Çöpteki grup görüntülenmez; önce geri alın"), ("kilit", "Çöpteki grup düzenlenmez; önce geri alın"), "sil")}</td></tr>')
    h = grup_hesap(gid)
    ek = h["ek"]
    ara = " ".join([gid, g["ad"], ek["ornek"]] + [k[1] for k in h["ks"]])
    return (f'<tr data-satir="grp-{gid}" data-durum="aktif" data-ara="{e(ara)}" data-baslik="{gid} · {e(g["ad"])}">'
            f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name">{gid} · {e(g["ad"])}</div><div class="rcp-by">{e(ek["ornek"])}</div></div></td>'
            f'<td><span class="kb-tarih">{siklik_metin(ek)}</span></td>'
            f'<td class="say kb-gizle-m"><button type="button" class="kb-bag" data-tanim="mtGor-{gid}">{len(h["etkin"])} / {len(h["ks"])} kaynak göster</button></td>'
            f'<td class="kb-gizle-m">{kanal_ikon(g["kanallar"])}</td>'
            f'<td class="kb-gizle-t"><div class="rcp-id"><div class="rcp-name">{sayi(h["cekim"])} çekim</div><div class="rcp-by">{sayi(h["haber"])} içerik<span data-izin="ai-maliyet"> · ${para(h["usd"])}</span></div></div></td>'
            f'<td><div class="toggle-row"><label class="toggle"><input type="checkbox" checked data-anahtar="{gid} · {e(g["ad"])} grubu" data-anahtar-etki="{len(h["etkin"])} kaynak çekilmez, yeni AI taslağı gelmez" aria-label="{gid} grubu etkin"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div></td>'
            f'<td>{row_acts(("tanim", "mtGor-" + gid), ("tanim", "mtDz-" + gid), ("tasi", tasi_attr(gid, g["ad"], len(h["ks"]))), sil_ad="Grubu sil")}</td></tr>')


def sayfa_motor():
    hs = {g["id"]: grup_hesap(g["id"]) for g in GRUPLAR}
    cekim = sum(h["cekim"] for h in hs.values())
    haber = sum(h["haber"] for h in hs.values())
    usd = sum(h["usd"] for h in hs.values())
    etkin = sum(len(h["etkin"]) for h in hs.values())
    toplam = sum(len(h["ks"]) for h in hs.values())
    cop_grup = {"id": "AJ", "ad": "Ajans (deneme)", "ornek": "örn. AA, DHA, İHA birlikte", "siklik": 15, "birim": "dakika", "kanallar": ["web", "uygulama", "sosyal"]}
    satir = "".join(grup_satir(g) for g in GRUPLAR) + grup_satir(cop_grup, cop=True)
    sab = "".join(grup_gor_sablon(g) + grup_dz_sablon(g) for g in GRUPLAR)
    s = bas("Kaynak Motoru", "motor")
    s += f"""
<!-- KAYNAK MOTORU (Y1): Milli Müdafaa "Frekans" ekranı yapısında (referans-06). Her satır bir kaynak grubu: ad, örnek, sıklık, kaynaklar,
     yayın kanalları, aylık tahmin (maliyet yalnız ai-maliyet izniyle), etkin anahtarı. İçinde kaynak olan grup taşınarak silinir (B1). -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Kaynak Motoru</h1>
      <div class="ph-sub">Kaynak grupları ve çekim sıklığı · tarama her 10 dakikada çalışır; grubun süresi dolmuşsa kaynakları çekilir · sıklık ve kanallar “Düzenle”den</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.cron" href="cron.html">{I("fa-heart-pulse")}Hat sağlığı</a>
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.kaynaklar" href="kaynaklar.html">{I("fa-rss")}Kaynaklar</a>
      <button type="button" class="btn btn-acc btn-sm" data-tanim="mtYeni">{I("fa-plus")}Yeni grup</button>
    </div>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card" data-izin="ai-maliyet">
      <div class="kpi-ico">{I("fa-coins")}</div>
      <div><div class="kpi-num">${para(usd)}</div><div class="kpi-lbl">Aylık tahmini maliyet</div>
      <div class="kpi-delta flat">{I("fa-turkish-lira-sign")}~₺{sayi(round(usd * KUR))} · içerik başı ${para(HABER_BASI_USD, 4)}</div></div>
    </div>
    <div class="kpi-card info">
      <div class="kpi-ico">{I("fa-arrows-rotate")}</div>
      <div><div class="kpi-num">{sayi(cekim)}</div><div class="kpi-lbl">Aylık çekim</div>
      <div class="kpi-delta flat">{I("fa-layer-group")}{len(GRUPLAR)} etkin grup</div></div>
    </div>
    <div class="kpi-card ok">
      <div class="kpi-ico">{I("fa-microchip")}</div>
      <div><div class="kpi-num">{sayi(haber)}</div><div class="kpi-lbl">Aylık işlenecek içerik</div>
      <div class="kpi-delta flat">{I("fa-filter")}tekrarlar elendikten sonra</div></div>
    </div>
    <div class="kpi-card warm">
      <div class="kpi-ico">{I("fa-rss")}</div>
      <div><div class="kpi-num">{etkin} / {toplam}</div><div class="kpi-lbl">Etkin kaynak</div>
      <div class="kpi-delta down">{I("fa-triangle-exclamation")}1'i hata veriyor</div></div>
    </div>
  </div>

  <section class="pnl-card" id="mtListe" data-liste data-liste-ad="grup" data-sayfa-boy="25" data-liste-cop-not="Grup çekilmez ve Çöp sekmesine taşınır" aria-labelledby="mtListeBas">
    <h2 class="sr-only" id="mtListeBas">Kaynak grupları</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Duruma göre">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="aktif">Etkin<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="kapali">Kapalı<span class="ch-cnt">0</span></button>
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{I("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}
        <label class="sr-only" for="mtAra">Gruplarda ara</label>
        <input id="mtAra" type="search" data-liste-ara placeholder="Grup ya da kaynak adı ara" autocomplete="off">
      </div>
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>
    <div class="ptable-wrap">
      <table class="ptable">
        <thead><tr>
          <th class="kb-ana">Grup</th><th>Sıklık</th><th class="say kb-gizle-m">Kaynak</th><th class="kb-gizle-m">Kanallar</th><th class="kb-gizle-t">Aylık tahmin</th><th>Etkin</th><th><span class="sr-only">İşlemler</span></th>
        </tr></thead>
        <tbody data-satirlar>{satir}</tbody>
{durum_govdeleri(7, "fa-layer-group", "Henüz kaynak grubu yok", "İlk grubu ekleyin; kaynaklar gruplara bağlanır, sıklık ve yayın kanalları gruptan gelir.", "Gruplar yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin.", bos_eylem=chr(10) + '            <button type="button" class="pe-tag" data-tanim="mtYeni">' + I("fa-plus") + 'Yeni grup</button>', iskelet='<td><div class="rcp-id"><span></span></div></td><td><span></span></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td>', yeniden="motor.html")}      </table>
    </div>
{pager(sayfalar=False)}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup" data-durum-icin="aktif kapali">Çekim</div>
      <button type="button" data-durum-icin="aktif" data-onay-baslik="Grup şimdi taransın mı?" data-onay-metin="Sıklığı beklemeden gruptaki etkin kaynaklar hemen çekilir; yeni içerik AI taslağı olarak havuza düşer ve AI maliyeti oluşur. Denetim izine yazılır." data-onay-evet="Şimdi tara" data-onay-ikon="fa-rotate" data-bildir-sonra="Grup kuyruğa alındı; birkaç saniye içinde çekilir">{I("fa-rotate")}Şimdi tara</button>
      <button type="button" data-durum-icin="aktif kapali" data-bildir="Havuz bu gruba süzülerek açılır (prototip)">{I("fa-robot")}Bu grubun haberleri</button>
      <button type="button" data-durum-icin="aktif kapali" data-bildir="Denetim izi bu gruba süzülerek açılır (prototip)">{I("fa-clipboard-list")}Denetim izinde gör</button>
      <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-rotate-left")}Çöpten geri al</button>
      <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-trash-can")}Kalıcı olarak sil</button>
    </div>
  </section>

</main>
</div>

<template id="mtYeni" data-baslik="Yeni kaynak grubu" data-alt="Ad, sıklık ve yayın kanalları · kaynakları şimdi ya da sonra ekleyin" data-zorunlu-kayit="ai-havuz.grup">
{grup_form("yeni")}  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="mtEklendi" data-bildir-sonra="Grup eklendi; denetim izine yazıldı">{I("fa-plus")}Grubu ekle</button></div>
</template>
<template id="mtEklendi" data-baslik="Grup eklendi" data-alt="Listede en alta eklendi">
  <div class="pnl-empty"><div class="pe-ico">{I("fa-circle-check")}</div><h2>Grup eklendi</h2><p>Kaynakları gruba bağlayın; grup ancak içinde etkin kaynak varsa çekilir. Sıklık ve kanallar bu gruptan gelen her haberde geçerli olur.</p></div>
  <div class="kb-kap-alt-cubuk"><a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.kaynaklar" href="kaynaklar.html">{I("fa-rss")}Kaynaklara git</a><button type="button" class="btn btn-acc btn-sm" data-kapat>{I("fa-check")}Tamam</button></div>
</template>
{sab}"""
    s += son()
    return s

# ================================================================== CRON VE HAT SAĞLIĞI
HAT_LOG = [("bilgi", "16.04.08", "Görsel temizleme: 14 görsel, 1 temizlenemedi → “KAP: iki enerji şirketinden…” Görsel eksik"), ("bilgi", "16.03.13", "12 taslak havuza düştü; 3'ü görsel eksik"), ("uyari", "16.02.40", "“Benzinde indirim beklentisi…” tek kaynaklı (T4); güven %62"), ("uyari", "16.02.22", "Çelişki: “AB genişleme toplantısında…” 3. kaynakta tarih farklı"), ("bilgi", "16.01.01", "AI üretimi başladı: 42 içerik, 17 olay grubu"), ("hata", "16.00.20", "Defense News: 403 Forbidden (11. deneme)"), ("bilgi", "16.00.00", "Kaynak taraması başladı: T1–T4, 18 etkin kaynak")] + [("bilgi", "15.50.48", "Kaynak taraması bitti: 18 kaynak, 37 yeni içerik"), ("uyari", "15.31.02", "Teknoloji Gündemi yavaş yanıt verdi (5,8 sn)"), ("bilgi", "15.20.11", "11 taslak havuza düştü"), ("hata", "15.20.04", "Defense News: 403 Forbidden (10. deneme)")]
CRONLAR = [
    # id, ad, komut, sıklık, son, süre, sonraki, durum, log
    ("tara", "Kaynak taraması", "kaynak:tara", "Her 10 dakikada", "16.00", "48 sn", "16.10", "ok",
     [("bilgi", "16.00.48", "Tarama bitti: 18 kaynak, 42 yeni içerik, 9 tekrar elendi"), ("hata", "16.00.20", "Defense News: 403 Forbidden (11. deneme)"), ("bilgi", "16.00.00", "Tarama başladı: T1–T4, 18 etkin kaynak")]),
    ("uret", "AI taslak üretimi", "ai-havuz:uret", "Her 10 dakikada", "16.01", "2 dk 12 sn", "16.11", "ok",
     [("bilgi", "16.03.13", "12 taslak havuza düştü; 3'ü görsel eksik"), ("uyari", "16.02.40", "1 içerik tek kaynaklı; güven %62"), ("bilgi", "16.01.01", "Üretim başladı: 42 içerik, 17 olay grubu")]),
    ("gorsel", "Görsel temizleme (logo ve damga)", "ai-havuz:gorsel", "Her 10 dakikada", "16.03", "1 dk 05 sn", "16.13", "ok",
     [("bilgi", "16.04.08", "14 görsel: 9 temiz, 4 AI kırparak temizledi, 1 temizlenemedi → Görsel eksik"), ("bilgi", "16.03.00", "Görsel işleme başladı")]),
    ("teyit", "Teyit ve tekrar eleme", "ai-havuz:teyit", "Her 10 dakikada", "16.02", "22 sn", "16.12", "ok",
     [("bilgi", "16.02.22", "17 olay grubu: 11'i en az 2 kaynakla teyitli, 1 çelişki işaretlendi"), ("bilgi", "16.02.00", "Teyit turu başladı")]),
    ("saglik", "Kaynak erişim denetimi", "kaynak:saglik", "Her saat", "16.00", "31 sn", "17.00", "hata",
     [("hata", "16.00.31", "Defense News 403 döndürüyor; kaynak sahibine erişim engeli olabilir"), ("bilgi", "16.00.02", "22 kaynak denetlendi: 17 sağlıklı, 1 hatalı, 4 pasif")]),
    ("otomatik", "Otomatik yayın", "ai-havuz:otomatik-yayin", "Her dakika", "22.11 23.29", "1 sn", "—", "durdu",
     [("bilgi", "22.11 23.30", "Otomatik yayın ayarı kapatıldı (Selin Aydemir); görev duraklatıldı"), ("bilgi", "22.11 22.25", "Eşik üstü 1 haber otomatik yayımlandı (%92)")]),
    ("maliyet", "Maliyet ve kullanım özeti", "ai-havuz:maliyet", "Her gün 00.05", "00.05", "6 sn", "00.05", "ok",
     [("bilgi", "00.05.06", "22.11 özeti: 64 içerik işlendi, $2,14"), ("bilgi", "00.05.00", "Özet başladı")]),
]
CRON_DURUM = {"ok": ("ok", "Çalışıyor"), "hata": ("warm", "Hata"), "gecikme": ("wait", "Gecikmeli"), "durdu": ("off", "Duraklatıldı")}


def log_html(satirlar, kaynak):
    return "".join(f'<span class="kl-satir {s}"><span class="kl-zaman">{z}</span><span class="kl-seviye">{"uyarı" if s == "uyari" else s}</span><span class="kl-kaynak">{kaynak}</span><span>{e(m)}</span></span>' for s, z, m in satirlar)


def sayfa_cron():
    rows, sab = [], []
    for cid, ad, kom, sik, son_, sure, sonraki, dur, log in CRONLAR:
        sinif, dad = CRON_DURUM[dur]
        rows.append(f'<tr data-satir="cr-{cid}" data-durum="{dur}" data-ara="{e(ad + " " + kom)}" data-baslik="{e(ad)}">'
                    f'<td class="kb-ana"><div class="rcp-id"><div class="rcp-name" title="{e(ad)}">{e(ad)}</div><div class="rcp-by">{I("fa-terminal")}{e(kom)}</div></div></td>'
                    f'<td class="kb-gizle-m">{e(sik)}</td><td class="kb-gizle-m"><span class="kb-tarih">{e(son_)}</span></td><td class="say kb-gizle-t">{e(sure)}</td>'
                    f'<td class="kb-gizle-m"><span class="kb-tarih muted">{e(sonraki)}</span></td><td><span class="pstat {sinif}">{dad}</span></td>'
                    f'<td>{row_acts(("tanim", "crLog-" + cid), None, None, gor_ad="Günlüğü görüntüle")}</td></tr>')
        sab.append(f"""<template id="crLog-{cid}" data-baslik="{e(ad)}" data-alt="{e(sik)} · {e(kom)}">
  <div class="kb-fs"><div class="kb-fs-tt">Durum</div><div class="sa-durum"><div><span>Durum</span><b><span class="pstat {sinif}">{dad}</span></b></div><div><span>Son çalışma</span><b>{e(son_)}</b></div><div><span>Süre</span><b>{e(sure)}</b></div><div><span>Sonraki</span><b>{e(sonraki)}</b></div><div><span>Kilit</span><b>{"Serbest" if dur != "durdu" else "—"}</b></div></div></div>
  <div class="kb-fs"><div class="kb-fs-tt">Son çalışmalar</div><pre class="kb-log">{log_html(log, cid)}</pre><p class="fhint kb-ust-bosluk">Sistem logları silinemez ve değiştirilemez; 90 günden eskisi arşive taşınır.</p></div>
  <div class="kb-kap-alt-cubuk"><a class="btn btn-ghost btn-sm" data-hedef="denetim-izi.loglar" href="../../cekirdek/denetim-izi/loglar.html">{I("fa-list")}Bütün loglar</a></div>
</template>
""")
    katman = []
    gercek = {"T1": (84, 41), "T2": (238, 312), "T3": (78, 58), "T4": (2, 3)}
    for g in GRUPLAR:
        h = grup_hesap(g["id"])
        bek = round(len(h["etkin"]) * GUN_CEKIM[h["ek"]["birim"]](h["ek"]["siklik"]))
        ger, yeni = gercek.get(g["id"], (bek, 0))
        oran = round(ger / bek * 100) if bek else 100
        sinif, dad = ("ok", "Normal") if oran >= 95 else ("wait", "Eksik") if oran >= 80 else ("warm", "Düşük")
        katman.append(f'<tr><td class="kb-ana"><div class="rcp-id"><div class="rcp-name">{g["id"]} · {e(g["ad"])}</div><div class="rcp-by">{siklik_metin(h["ek"])} · {len(h["etkin"])} etkin kaynak</div></div></td>'
                      f'<td class="say">{bek}</td><td class="say">{ger}</td><td class="say kb-gizle-m">%{oran}</td><td class="say kb-gizle-t">{yeni}</td><td><span class="pstat {sinif}">{dad}</span></td></tr>')
    s = bas("Cron ve hat sağlığı", "cron")
    s += f"""
<!-- CRON VE HAT SAĞLIĞI (yalnız Süper Admin; cron-saglik izni): sağlık kutuları, katman tablosu (beklenen/gerçekleşen), cron listesi (silinmez), manuel tetikle, hat günlüğü. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Cron ve hat sağlığı</h1>
      <div class="ph-sub">AI haber hattı · son tur 16.04 · her dakika kendiliğinden yenilenir</div>
    </div>
    <div class="ph-actions" data-izin="cron-saglik">
      <a class="btn btn-ghost btn-sm" data-hedef="sistem-sagligi.ana" href="../../cekirdek/sistem-sagligi/index.html">{I("fa-server")}Sistem sağlığı</a>
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.motor" href="motor.html">{I("fa-gears")}Kaynak Motoru</a>
      <button type="button" class="btn btn-acc btn-sm" data-onay-baslik="Kaynak taraması şimdi çalıştırılsın mı?" data-onay-metin="Grupların sıklığı beklenmeden 18 etkin kaynağın hepsi çekilir; yeni içerik AI taslağı olarak havuza düşer ve AI maliyeti oluşur. Çalışan bir tur varsa kilit çözülene kadar bekler. İşlem denetim izine yazılır." data-onay-evet="Şimdi çalıştır" data-onay-ikon="fa-play" data-bildir-sonra="Tarama kuyruğa alındı; kilit serbest, birkaç saniye içinde başlar">{I("fa-play")}Manuel tetikle</button>
    </div>
  </div>

  <section class="pnl-card" data-izin="cron-saglik" data-sekmeli aria-label="Cron ve hat sağlığı">
    <div class="sa-form-tabs" role="tablist" aria-label="Hat sağlığı bölümleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="crGenel">{I("fa-gauge-high")}Genel bakış</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="crGrup">{I("fa-layer-group")}Kaynak grupları<span class="ch-cnt" title="1 grupta çekim eksik">1</span></button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="crGorev">{I("fa-clock")}Zamanlanmış görevler<span class="ch-cnt" title="1 görev hata veriyor">1</span></button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="crLog">{I("fa-wave-square")}Hat günlüğü<span class="ch-cnt" title="1 hata, 2 uyarı · son 1 saat">3</span></button>
    </div>

    <!-- ===== GENEL BAKIŞ ===== -->
    <div class="sa-form-panel pc-body" id="crGenel" role="tabpanel">
      <div class="kb-bant tehlike">{I("fa-triangle-exclamation")}<span><b>1 hata.</b> Defense News 14.20'den beri 403 döndürüyor; T3 grubunda beklenen çekimin %81'i gerçekleşti. AI kuyruğu yoğun (96 iş), taslaklar 6 dk gecikmeli düşüyor.</span><a class="btn btn-ghost btn-sm kb-bant-eylem" data-hedef="ai-havuz.kaynaklar" href="kaynaklar.html">{I("fa-rss")}Kaynaklar</a></div>
      <div class="kb-saglik-izgara kb-ust-bosluk">
      <a class="kb-saglik" href="cron.html?sekme=crGorev"><span class="kb-saglik-bas"><span class="status-nokta"></span>Kaynak taraması</span><span class="kb-saglik-deger">16.00</span><span class="kb-saglik-meta">48 sn · 42 yeni içerik · sonraki 16.10</span></a>
      <a class="kb-saglik" href="cron.html?sekme=crGorev"><span class="kb-saglik-bas"><span class="status-nokta"></span>AI taslak üretimi</span><span class="kb-saglik-deger">2 dk 12 sn</span><span class="kb-saglik-meta">16.01 · 12 taslak havuza düştü</span></a>
      <div class="kb-saglik"><span class="kb-saglik-bas"><span class="status-nokta"></span>Kilit</span><span class="kb-saglik-deger">Serbest</span><span class="kb-saglik-meta">Son alınma 16.01 · 2 dk 12 sn tuttu · çakışma yok</span></div>
      <a class="kb-saglik uyari" data-hedef="sistem-sagligi.ana" href="../../cekirdek/sistem-sagligi/index.html"><span class="kb-saglik-bas"><span class="status-nokta"></span>AI kuyruğu</span><span class="kb-saglik-deger">96 iş</span><span class="kb-saglik-meta">Normalin 3 katı · en eski 6 dk</span></a>
      <a class="kb-saglik hata" data-hedef="ai-havuz.kaynaklar" href="kaynaklar.html"><span class="kb-saglik-bas"><span class="status-nokta"></span>Etkin kaynak</span><span class="kb-saglik-deger">17 / 18</span><span class="kb-saglik-meta">Defense News 14.20'den beri hata</span></a>
      <div class="kb-saglik"><span class="kb-saglik-bas"><span class="status-nokta"></span>Görsel temizleme · 24 sa</span><span class="kb-saglik-deger">%89</span><span class="kb-saglik-meta">41 temiz · 9 kırpıldı · 6 görsel eksik</span></div>
      <div class="kb-saglik"><span class="kb-saglik-bas"><span class="status-nokta"></span>Tekrar eleme · 24 sa</span><span class="kb-saglik-deger">128</span><span class="kb-saglik-meta">Aynı olay ikinci kez taslak olmadı</span></div>
      <a class="kb-saglik" data-hedef="ai-havuz.ayarlar" href="ayarlar.html"><span class="kb-saglik-bas"><span class="status-nokta"></span>Otomatik yayın</span><span class="kb-saglik-deger">Kapalı</span><span class="kb-saglik-meta">22.11.2026 23.30'dan beri · eşik %{ESIK}</span></a>
      <div class="kb-saglik"><span class="kb-saglik-bas"><span class="status-nokta"></span>AI servisi</span><span class="kb-saglik-deger">1,8 sn</span><span class="kb-saglik-meta">Ortalama yanıt · hata %0,4 · Claude Haiku 4.5</span></div>
      <div class="kb-saglik" data-izin="ai-maliyet"><span class="kb-saglik-bas"><span class="status-nokta"></span>Maliyet · bugün</span><span class="kb-saglik-deger">$2,31</span><span class="kb-saglik-meta">~₺91 · ay toplamı $50,47</span></div>
    </div>
      <div class="kb-fs kb-ust-bosluk"><div class="kb-fs-tt">Son olaylar</div><pre class="kb-log">{log_html(HAT_LOG[:5], "ai-hat")}</pre>
        <a class="kb-bag" href="cron.html?sekme=crLog">Bütün hat günlüğü</a></div>
    </div>

    <!-- ===== KAYNAK GRUPLARI · SON 24 SAAT ===== -->
    <div class="sa-form-panel" id="crGrup" role="tabpanel" hidden>
      <div class="pc-body"><p class="fhint">Son 24 saatte grup başına beklenen ve gerçekleşen çekim. Sıklık ve kanallar <a class="kb-bag" data-hedef="ai-havuz.motor" href="motor.html">Kaynak Motoru'nda</a>.</p></div>
    <div class="ptable-wrap"><table class="ptable">
      <thead><tr><th class="kb-ana">Grup</th><th class="say">Beklenen</th><th class="say">Gerçekleşen</th><th class="say kb-gizle-m">Oran</th><th class="say kb-gizle-t">Yeni içerik</th><th>Durum</th></tr></thead>
      <tbody>{"".join(katman)}</tbody>
    </table></div>
    </div>

    <!-- ===== ZAMANLANMIŞ GÖREVLER ===== -->
    <div class="sa-form-panel" id="crGorev" role="tabpanel" data-liste data-liste-ad="görev" data-sayfa-boy="25" hidden>
    <div class="pc-body"><div class="kb-bant bilgi">{I("fa-lock")}<span><b>Sistem görevleri kodda tanımlıdır; düzenlenmez ve silinmez.</b> Gerekirse ⋯ menüsünden duraklatılır. Sıklıklar Kaynak Motoru'ndan, otomatik yayın görevi otomatik yayın ayarından yönetilir. Görev günlükleri sistem logudur, değiştirilemez.</span></div></div>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Duruma göre">
        <button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="hata">Hata<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="ok">Çalışıyor<span class="ch-cnt">0</span></button>
        <button type="button" class="chip" role="tab" aria-selected="false" data-sekme="durdu">Duraklatıldı<span class="ch-cnt">0</span></button>
      </div>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-magnifying-glass")}
        <label class="sr-only" for="crAra">Görevlerde ara</label>
        <input id="crAra" type="search" data-liste-ara placeholder="Görev adı ya da komut ara" autocomplete="off">
      </div>
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
    </div>
    <div class="ptable-wrap">
      <table class="ptable">
        <thead><tr><th class="kb-ana">Görev</th><th class="kb-gizle-m">Sıklık</th><th class="kb-gizle-m">Son çalışma</th><th class="say kb-gizle-t">Süre</th><th class="kb-gizle-m">Sonraki</th><th>Durum</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
        <tbody data-satirlar>{"".join(rows)}</tbody>
{durum_govdeleri(7, "fa-clock", "Zamanlanmış görev yok", "Bu kurulumda AI hattı için tanımlı görev bulunmuyor. Görevler kodda tanımlanır; geliştiriciye başvurun.", "Görev durumu okunamadı", "Zamanlayıcıya ulaşılamadı. Sayfayı yenileyin; sorun sürerse sunucuda zamanlayıcı servisinin çalıştığını kontrol edin.", iskelet='<td><div class="rcp-id"><span></span></div></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td class="kb-gizle-m"><span></span></td><td><span></span></td><td></td>', yeniden="cron.html")}      </table>
    </div>
{pager(sayfalar=False)}
    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup">Görev</div>
      <button type="button" data-durum-icin="ok hata" data-onay-baslik="Görev şimdi çalıştırılsın mı?" data-onay-metin="Görev sıradaki turu beklemeden kuyruğa alınır; kilit doluysa serbest kalınca başlar. AI maliyeti oluşabilir. İşlem denetim izine yazılır." data-onay-evet="Çalıştır" data-onay-ikon="fa-play" data-bildir-sonra="Görev kuyruğa alındı; birkaç saniye içinde çalışır">{I("fa-play")}Şimdi çalıştır</button>
      <button type="button" data-durum-icin="ok hata" data-onay-baslik="Görev duraklatılsın mı?" data-onay-metin="Önce: çalışıyor → Sonra: duraklatıldı. Sürdürülene kadar hiçbir turda çalışmaz; havuza yeni taslak gelmeyebilir. Denetim izine yazılır." data-onay-evet="Duraklat" data-onay-tehlike data-onay-ikon="fa-pause" data-sonra-durum="durdu" data-sonra-durum-ad="Duraklatıldı" data-sonra-durum-sinif="off" data-bildir-sonra="Görev duraklatıldı; denetim izine yazıldı">{I("fa-pause")}Duraklat</button>
      <button type="button" data-durum-icin="durdu" data-onay-baslik="Görev sürdürülsün mü?" data-onay-metin="Önce: duraklatıldı → Sonra: çalışıyor. Otomatik yayın görevi, otomatik yayın ayarı kapalıyken çalışsa da haber yayımlamaz. Denetim izine yazılır." data-onay-evet="Sürdür" data-onay-ikon="fa-play" data-sonra-durum="ok" data-sonra-durum-ad="Çalışıyor" data-sonra-durum-sinif="ok" data-bildir-sonra="Görev sürdürüldü; sonraki turda çalışır">{I("fa-play")}Sürdür</button>
      <div class="pmenu-div"></div>
      <div class="kb-dm-grup">Kayıt</div>
      <button type="button" data-bildir="Son 7 günün görev günlüğü indiriliyor (CSV, prototip)">{I("fa-file-arrow-down")}Günlüğü indir</button>
      <button type="button" data-bildir="Bu görevin uyarıları e-postanıza da gelecek (prototip)">{I("fa-bell")}Hata olunca bana haber ver</button>
    </div>
    </div>

    <!-- ===== HAT GÜNLÜĞÜ ===== -->
    <div class="sa-form-panel pc-body" id="crLog" role="tabpanel" hidden>
      <pre class="kb-log">{log_html(HAT_LOG, "ai-hat")}</pre>
      <p class="fhint kb-ust-bosluk">Sistem logları silinemez ve değiştirilemez; 90 günden eskisi arşive taşınır. <a class="kb-bag" data-hedef="denetim-izi.loglar" href="../../cekirdek/denetim-izi/loglar.html">Bütün sistem logları</a></p>
    </div>
  </section>

  <div class="kb-bant tehlike" data-izin-yok="cron-saglik">{I("fa-lock")}<span><b>Bu ekran yalnız Süper Admin'e açık.</b> Cron ve hat sağlığı “Cron ve sistem sağlığı” izin grubundadır.</span></div>
</main>
</div>
{"".join(sab)}"""
    s += son()
    return s


# ================================================================== OTOMATİK YAYIN VE ONAY AYARLARI
def kosul(baslik, aciklama, kontrol, acik=True, kilit=None, sil=True):
    t = f'<label class="toggle"><input type="checkbox"{" checked" if acik else ""}{" disabled" if kilit else ""} aria-label="{e(baslik)}"><span class="toggle-track"></span><span class="toggle-thumb"></span></label>'
    s_ = (f'<button type="button" class="ia-btn kb-kilit" disabled aria-label="Kaldırılamaz" title="{e(kilit)}">{I("fa-lock")}</button>' if kilit
          else f'<button type="button" class="ia-btn danger" data-satir-sil aria-label="Koşulu kaldır: {e(baslik)}" title="Kaldır">{I("fa-trash")}</button>')
    return f'<div class="km-satir"><div class="km-yazi">{e(baslik)}<small>{e(aciklama)}</small>{kontrol}</div>{t}{s_}</div>'


def sayfa_ayarlar():
    rol_kutu = "".join(f'<label class="kb-secenek"><input type="checkbox" value="{r}"{" checked" if r in OKUMA["roller"] else ""}>{e(ROL_AD[r])}{" · muaf" if r in OKUMA.get("muaf", []) else ""}</label>' for r in ROL_AD if r not in ("sosyal", "analist"))
    kanal_rol = "".join(f'<label class="kb-secenek"><input type="checkbox" value="{r}"{" checked" if r in AY["kanal_degistirebilen_roller"] else ""}>{e(ROL_AD[r])}</label>' for r in ROL_AD if r not in ("sosyal", "analist"))
    grp_cip = "".join(f'<span class="kb-cip" data-deger="{g["id"]} · {e(g["ad"])}"><span>{g["id"]} · {e(g["ad"])}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for g in GRUPLAR[:2])
    grp_havuz = json.dumps([f'{g["id"]} · {g["ad"]}' for g in GRUPLAR], ensure_ascii=False)
    kat_cip = "".join(f'<span class="kb-cip" data-deger="{k}"><span>{k}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for k in ["Gündem › Siyaset", "Dünya › Savaş ve Çatışmalar"])
    alt = json.loads(html.unescape(re.search(r'data-alt-harita="([^"]*)"', isaret("hb-df-alt")).group(1)))
    kat_havuz = json.dumps([f"{a} › {b}" for a, bs in alt.items() for b in bs], ensure_ascii=False)
    kosullar = "".join([
        kosul("Görseli eksik haber otomatik yayımlanmaz", "Logo ya da damga temizlenemediyse haber her zaman editör onayına düşer (YS1)", "", kilit="YS1 gereği kapatılamaz ve kaldırılamaz"),
        kosul("Yalnız bu kaynak gruplarından", "1. kaynağın grubu listede değilse haber kuyrukta kalır", f'<div class="kb-cip-girdi kb-ust-bosluk" data-havuz-kapali data-havuz=\'{e(grp_havuz)}\'>{grp_cip}<input type="text" placeholder="Grup ekle" aria-label="Kaynak grubu ekle"><div class="pnl-menu kb-cip-oneri"></div></div>'),
        kosul("Hariç tutulan kategoriler", "Bu kategorilerdeki haber eşiği geçse de onay bekler", f'<div class="kb-cip-girdi kb-ust-bosluk" data-havuz-kapali data-havuz=\'{e(kat_havuz)}\'>{kat_cip}<input type="text" placeholder="Kategori ekle" aria-label="Hariç kategori ekle"><div class="pnl-menu kb-cip-oneri"></div></div>'),
        kosul("En az bağımsız kaynak sayısı", "Önceki dokümandaki “iki bağımsız kaynak olmadan otomatik yayın yok” kuralı; açık konu", f'<div class="kb-birim kb-ust-bosluk"><input class="finput" inputmode="numeric" value="2" aria-label="En az kaynak sayısı"><span>kaynak</span></div>'),
        kosul("Günlük üst sınır", "Sınıra ulaşınca o gün eşik üstündeki haberler de onay bekler", f'<div class="kb-birim kb-ust-bosluk"><input class="finput" inputmode="numeric" value="40" aria-label="Günlük üst sınır"><span>haber / gün</span></div>'),
        kosul("Çelişki işaretli haber otomatik yayımlanmaz", "Kaynak teyidinde rakam, tarih ya da ad farkı bulunursa", ""),
    ])
    s = bas("Otomatik yayın ve onay ayarları", "ayarlar")
    s += f"""
<!-- OTOMATİK YAYIN VE ONAY AYARLARI (Y3, YS1, YS4, YS6, YS7, K8, K15). Ayar ekranı kalıbı: sekmeler + sağ sütun + kaydet çubuğu.
     Kaydetmek e-posta koduyla (otomatik yayın ayarı hassas işlem). Dile bağlı alan yok, dil seçici yok. -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Otomatik yayın ve onay ayarları</h1>
      <div class="ph-sub">AI haber havuzu · son değişiklik 22.11.2026 23.30 · Selin Aydemir</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.havuz" href="index.html">{I("fa-arrow-left")}Haber havuzu</a>
      <a class="btn btn-ghost btn-sm" data-hedef="denetim-izi.liste" href="../../cekirdek/denetim-izi/index.html">{I("fa-clipboard-list")}Denetim izi</a>
    </div>
  </div>

  <div class="form-layout">
  <section class="pnl-card" id="ayForm" data-form data-sekmeli aria-label="Otomatik yayın ve onay ayarları formu">
    <div class="sa-form-tabs" role="tablist" aria-label="Ayar sekmeleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="ayOkuma">{I("fa-book-open-reader")}Onay ve okuma</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="ayOto">{I("fa-robot")}Otomatik yayın</button>
      <button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="ayGorsel">{I("fa-image")}Görsel ve kanallar</button>
    </div>

    <!-- ===== ONAY VE OKUMA (Y2, Y3, YS5, YS6) ===== -->
    <div class="sa-form-panel" id="ayOkuma" role="tabpanel">
      <div class="form-sec">
        <div class="toggle-row"><span>Onaydan önce içeriği okuma zorunluluğu<small>Açık olan rollerde “Onayla ve Yayınla” Detay sekmesi sonuna kadar okununca açılır; listeden hızlı onay ve Toplu Onayla görünmez (Y2)</small></span><label class="toggle"><input type="checkbox" checked data-ac="ayOkumaRol" aria-label="Okuma zorunluluğu"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      </div>
      <div class="form-sec" id="ayOkumaRol">
        <div class="frow"><span class="flabel">Geçerli olduğu roller</span>
          <div class="kb-secenek-grup" role="group" aria-label="Okuma zorunluluğunun geçerli olduğu roller">{rol_kutu}</div>
          <span class="fhint">Başlangıç: Editör ve Kategori Editörü açık; Süper Admin ve Genel Yayın Yönetmeni muaf (YS6).</span></div>
        <div class="form-grid kb-iki-sutun kb-ust-bosluk">
          <div class="frow"><span class="flabel">Okunması gereken</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="ayOkunacak" checked>Detay sekmesi</label><label class="kb-secenek"><input type="radio" name="ayOkunacak">Bütün sekmeler</label></div>
            <span class="fhint">YS5: Detay sekmesi sonuna kadar kaydırılınca açılır; diğer sekmelere girmek zorunlu değil.</span></div>
          <div class="frow"><label for="aySure">İçerik ekrana sığıyorsa bekleme</label>
            <div class="kb-birim"><input class="finput" id="aySure" inputmode="numeric" value="{OKUMA['sigan_icerik_saniye']}"><span>saniye</span></div>
            <span class="fhint">Kaydırılacak bir şey yoksa düğme bu süre sonunda açılır.</span></div>
        </div>
        <div class="kb-bant bilgi kb-ust-bosluk">{I("fa-robot")}<span><b>Otomatik yayın bu kuralın bilinçli istisnasıdır (YS7).</b> Eşiğin üstündeki haber okunmadan çıkar; okuma kuralı yalnız editörün önüne düşen haberlerde geçerlidir. Otomatik çıkan her haber listede ve denetim izinde “Otomatik yayımlandı” olarak işaretlenir.</span></div>
      </div>
    </div>

    <!-- ===== OTOMATİK YAYIN (K8, YS1, YS7, açık konular) ===== -->
    <div class="sa-form-panel" id="ayOto" role="tabpanel" hidden>
      <div class="form-sec">
        <div class="toggle-row"><span>Otomatik yayınla<small>Açıkken güven skoru eşiğin üstündeki ve aşağıdaki koşulları sağlayan AI haberleri editör onayı beklemeden yayımlanır; altındakiler kuyrukta kalır</small></span><label class="toggle"><input type="checkbox" aria-label="Otomatik yayınla"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        <p class="fhint">Kapalı · 22.11.2026 23.30'da Selin Aydemir kapattı. Açmak ve koşulları değiştirmek e-posta koduyla doğrulanır (K15).</p>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-gauge-high")}Güven eşiği<span class="fs-ek">Güven seviyeleri: %85 ve üstü yüksek, %60–84 orta, altı düşük</span></div>
        <div class="kb-esik" data-dagilim="9,14,21,30,38,52,71,96,118,104" data-donem="Son 7 gün"><div class="kb-esik-ust"><label for="ayEsik">Otomatik yayın eşiği</label><output for="ayEsik"></output></div><input type="range" id="ayEsik" min="50" max="100" step="1" value="{ESIK}"></div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-shield-halved")}Güvenlik koşulları<span class="fs-ek">Hepsi birlikte aranır; biri sağlanmazsa haber onay bekler</span></div>
        <div class="kb-madde" data-satir-liste data-satir-ad="Koşul" data-satir-alan1="Koşul adı" data-satir-alan2="Açıklama">
          {kosullar}
          <button type="button" class="kb-ekle-btn" data-satir-ekle>{I("fa-plus")}Özel koşul ekle</button>
        </div>
        <div class="kb-bant uyari kb-ust-bosluk">{I("fa-circle-question")}<span><b>Açık konu.</b> Koşulların son hali (hangi kaynak grupları, hangi kategoriler, en az kaynak sayısı, günlük üst sınır) Beyar ve Yasin Bey ile netleşecek. Ekrandaki değerler öneridir.</span></div>
      </div>
    </div>

    <!-- ===== GÖRSEL VE KANALLAR (YS1–YS4) ===== -->
    <div class="sa-form-panel" id="ayGorsel" role="tabpanel" hidden>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-image")}Görsel durumu<span class="fs-ek">AI her görseli üçe ayırır; kaynak başına izin yok (YS1)</span></div>
        <div class="kb-ozk">
          <div class="kb-ozk-satir"><span class="kb-ozk-ikon">{I("fa-image")}</span><div class="kb-ozk-yazi"><b>Temiz</b><span>Logo ya da damga yok; görsel aynen kullanılır. Otomatik yayına girebilir.</span></div><div class="kb-ozk-kapsam"><span>Otomatik yayın</span></div><span class="pstat ok">Kullanılır</span></div>
          <div class="kb-ozk-satir"><span class="kb-ozk-ikon">{I("fa-crop-simple")}</span><div class="kb-ozk-yazi"><b>AI kırparak temizledi</b><span>Logo ya da damga kırpılarak çıkarıldı; düzenleme ekranında aslı ve kırpılmış hali görünür. Otomatik yayına girebilir.</span></div><div class="kb-ozk-kapsam"><span>Otomatik yayın</span></div><span class="pstat ok">Kullanılır</span></div>
          <div class="kb-ozk-satir"><span class="kb-ozk-ikon">{I("fa-image")}</span><div class="kb-ozk-yazi"><b>Görsel eksik</b><span>Kaynağın logosu ya da damgası temizlenemedi; görsel kullanılmaz, haber görselsiz onaya gider ve havuzdan görsel önerilir. Hiçbir zaman otomatik yayımlanmaz.</span></div><div class="kb-ozk-kapsam"><span>Yalnız editör</span></div><span class="pstat warm">Kullanılmaz</span></div>
        </div>
      </div>
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-share-nodes")}Yayın kanalları<span class="fs-ek">Grupların kanalları <a class="kb-bag" data-hedef="ai-havuz.motor" href="motor.html">Kaynak Motoru'nda</a></span></div>
        <div class="kb-ozk">
          <div class="kb-ozk-satir"><span class="kb-ozk-ikon">{I("fa-layer-group")}</span><div class="kb-ozk-yazi"><b>Kanalları 1. kaynağın grubu belirler</b><span>Kaynakları farklı gruplardan olan haberde ilk kaynağın grubundaki kanallar geçerlidir (YS4).</span></div><div class="kb-ozk-kapsam"><span>Kural</span></div>{I("fa-lock")}</div>
          <div class="kb-ozk-satir"><span class="kb-ozk-ikon">{I("fa-link-slash")}</span><div class="kb-ozk-yazi"><b>Yalnız Sosyal Medya'ya giden gönderi bağlantısızdır</b><span>Metin ve görsel kendi başına durur, haber gönderinin içinde özetlenir, sitede sayfa açılmaz (YS2).</span></div><div class="kb-ozk-kapsam"><span>Kural</span></div>{I("fa-lock")}</div>
        </div>
        <div class="frow kb-ust-bosluk"><span class="flabel">Tek haberde kanalı değiştirebilen roller</span>
          <div class="kb-secenek-grup" role="group" aria-label="Kanalı değiştirebilen roller">{kanal_rol}</div>
          <span class="fhint">Diğer roller kanalları görür ama değiştiremez (YS3). Her değişiklik denetim izine yazılır.</span></div>
      </div>
    </div>
  </section>

  <aside class="side-card" aria-label="Durum">
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-signal")}Şu an</h2><span class="pstat off">Otomatik yayın kapalı</span></div>
      <div class="pc-body sa-durum">
        <div><span>Eşik</span><b>%{ESIK}</b></div>
        <div><span>Bu eşikle son 7 gün</span><b>318 / 553 haber</b></div>
        <div><span>Etkin koşul</span><b>6</b></div>
        <div><span>Okuma zorunluluğu</span><b>Editör, Kategori Editörü</b></div>
        <div><span>Bekleme (sığan içerik)</span><b>{OKUMA['sigan_icerik_saniye']} sn</b></div>
      </div>
    </section>
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-clock-rotate-left")}Son değişiklikler</h2></div>
      <div class="pc-body sa-gecmis">
        <div><b>Otomatik yayın kapatıldı</b><span>Selin Aydemir · 22.11.2026 23.30</span></div>
        <div><b>Eşik %80 → %85</b><span>Selin Aydemir · 21.11.2026 10.30</span></div>
        <div><b>Günlük üst sınır 40 eklendi</b><span>Ayşe Yıldız · 21.11.2026 10.24</span></div>
        <div><b>Okuma zorunluluğu açıldı</b><span>Selin Aydemir · 20.11.2026 09.00</span></div>
        <a class="kb-bag" data-hedef="denetim-izi.liste" href="../../cekirdek/denetim-izi/index.html">Denetim izinde bütün kayıtlar</a>
      </div>
    </section>
  </aside>
  </div>

  <div class="kb-kaydet" data-form-icin="ayForm">
    <div class="kk-durum">{I("fa-circle-check")}<span>Kaydedildi · 22.11.2026 23.30 · Selin Aydemir</span></div>
    <div class="kk-sag">
      <button type="button" class="btn btn-acc btn-sm" data-kaydet data-kod data-kod-baslik="Otomatik yayın ayarını e-posta koduyla doğrulayın" data-kaydet-metin="Kaydedildi" data-bildir="Ayarlar kaydedildi; hemen geçerli, önceki hal denetim izinde">{I("fa-floppy-disk")}Kaydet</button>
    </div>
  </div>
</main>
</div>
"""
    s += son()
    return s

# ================================================================== AI HABER DÜZENLE
PROFILLER = [("ogrenci", "Öğrenci", "fa-graduation-cap"), ("calisan", "Çalışan", "fa-briefcase"), ("emekli", "Emekli", "fa-person-cane"),
             ("ev-sahibi", "Ev sahibi", "fa-house"), ("kiraci", "Kiracı", "fa-key"), ("esnaf", "Esnaf", "fa-store")]

KAYIT = {
    "kirpildi": dict(
        baslik="Meteoroloji'den Marmara için turuncu kod kar uyarısı",
        spot="Meteoroloji Genel Müdürlüğü, Marmara Bölgesi için 24 Kasım sabahından itibaren kuvvetli kar yağışı uyarısı yaptı. İstanbul'un kuzey ilçelerinde kar kalınlığının yer yer 15 santimetreyi bulması bekleniyor.",
        kat="Gündem", alt=["İstanbul", "Afet"], kaynaklar=["mgm", "aa", "dha"], guven=91, gdurum="kirpildi", gorsel="p183", odak=(50, 40),
        cekilme="23.11.2026 15.58", url="https://www.mgm.gov.tr", model="Claude Haiku 4.5",
        metin=["<p>Meteoroloji Genel Müdürlüğü, Marmara Bölgesi için 24 Kasım Salı sabahından itibaren geçerli turuncu kodlu kar yağışı uyarısı yayımladı. Uyarıya göre İstanbul'un kuzey ilçeleri ile Kırklareli, Tekirdağ ve Kocaeli'nin yüksek kesimlerinde kar kalınlığı yer yer 15 santimetreyi bulabilir.</p>",
               "<p>Yağışın gece saatlerinde kuzeydoğudan gelen soğuk hava ile birlikte etkisini artırması bekleniyor. Meteoroloji, rüzgârın yer yer saatte 60 kilometreye ulaşabileceğini ve görüş mesafesinin düşebileceğini belirtti.</p>",
               "<h2>Ulaşım ve okullar</h2>",
               "<p>İstanbul Valiliği, ulaşımda aksama yaşanabileceğini, sürücülerin zorunlu olmadıkça özel araçla yola çıkmamasını istedi. Toplu taşıma seferleri gece yarısına kadar uzatıldı; okulların durumuna ilişkin kararın akşam saatlerinde açıklanması bekleniyor.</p>",
               "<p>AFAD, olası afet durumlarına karşı ekiplerin hazır beklediğini açıkladı. Uyarı 25 Kasım akşamına kadar geçerli; uzmanlar yağışın hafta sonuna doğru yerini soğuk ve kuru havaya bırakmasını bekliyor.</p>"],
        ozet=["Marmara için 24 Kasım sabahından itibaren turuncu kod kar uyarısı var.", "İstanbul'un kuzeyinde kar kalınlığı 15 santimetreyi bulabilir.", "Toplu taşıma seferleri gece yarısına kadar uzatıldı."],
        neden="Turuncu kod, günlük yaşamı ve ulaşımı aksatabilecek tehlikeli hava anlamına geliyor.",
        sonra="Valiliğin okullar için kararı akşam saatlerinde açıklanacak; uyarı 25 Kasım akşamına kadar geçerli.",
        etki_genel="İstanbul'un kuzeyinde yaşıyor ya da oraya gidiyorsan salı sabahı ulaşıma ek süre ayır; toplu taşıma gece yarısına kadar çalışıyor.",
        etki={"ogrenci": "Okulların durumu akşam açıklanacak; valiliğin duyurusunu bekle, servis saatleri değişebilir.",
              "calisan": "Salı sabahı işe gidişte ek süre ayır; toplu taşıma seferleri gece yarısına kadar uzatıldı.",
              "esnaf": "Kar nedeniyle salı sabahı müşteri ve tedarik trafiği yavaşlayabilir; teslimat saatlerini buna göre planla."},
        site=[("Meteoroloji Genel Müdürlüğü", "Turuncu kod uyarısı · 23 Kasım 2026 15.40"), ("İstanbul Valiliği", "Ulaşım ve toplu taşıma duyurusu · 23 Kasım 2026"), ("AFAD", "Hazırlık açıklaması · 23 Kasım 2026")],
        teyit=[("mgm", "15.40", "ok", "Ana kaynak", ""), ("aa", "15.46", "ok", "Teyit", ""), ("dha", "15.51", "ok", "Teyit", "")],
        teyit_ozet=("fa-circle-check", "3 kaynak · 2 bağımsız teyit", "Aynı olay iki kez çekilmedi; kanallar 1. kaynağın grubundan (YS4)"),
        alternatif=[("İHA · aynı olay", "15.55"), ("İstanbul Valiliği (X) · ulaşım duyurusu", "15.57")],
        seo=("Marmara'ya turuncu kod: İstanbul'da kar uyarısı | Dada Haber", "Meteoroloji, Marmara için 24 Kasım sabahından itibaren turuncu kod kar uyarısı yaptı. İstanbul'un kuzeyinde kar 15 santimetreyi bulabilir.", "meteorolojiden-marmara-icin-turuncu-kod-kar-uyarisi", ["marmara kar uyarısı", "turuncu kod", "istanbul kar"]),
        push=("Marmara'ya turuncu kod kar uyarısı", "İstanbul'un kuzeyinde kar 15 santimetreyi bulabilir; toplu taşıma gece yarısına kadar uzatıldı."),
    ),
    "eksik": dict(
        baslik="AB genişleme toplantısında Türkiye'nin üyelik süreci de konuşuldu",
        spot="AB dışişleri bakanları Brüksel'de genişleme gündemini ele aldı. Toplantıda Türkiye ile katılım müzakerelerinin durumu ve gümrük birliğinin güncellenmesi de değerlendirildi.",
        kat="Dünya", alt=["Avrupa", "Diplomasi"], kaynaklar=["reuters", "ap", "aa"], guven=78, gdurum="eksik", gorsel="", odak=(50, 50),
        cekilme="23.11.2026 15.52", url="https://www.reuters.com/world", model="Claude Haiku 4.5",
        metin=["<p>Avrupa Birliği dışişleri bakanları, Brüksel'de yapılan toplantıda birliğin genişleme gündemini ele aldı. Toplantıda Batı Balkan ülkeleri, Ukrayna ve Moldova'nın yanı sıra Türkiye ile katılım müzakerelerinin durumu da değerlendirildi.</p>",
               "<p>Reuters'ın aktardığına göre bakanlar, Türkiye ile ilişkilerde gümrük birliğinin güncellenmesi ve vize kolaylığı başlıklarında somut adım atılması gerektiği görüşünde birleşti. Katılım müzakerelerinde yeni fasıl açılmasına ilişkin bir karar alınmadı.</p>",
               "<h2>Sonraki adım</h2>",
               "<p>Genişleme raporunun aralık ayındaki zirvede liderlerin önüne gelmesi bekleniyor. Türkiye Dışişleri Bakanlığı toplantıya ilişkin henüz açıklama yapmadı.</p>"],
        ozet=["AB bakanları Brüksel'de genişleme gündemini ele aldı.", "Türkiye ile gümrük birliği ve vize kolaylığı konuşuldu.", "Yeni fasıl açılmasına ilişkin karar alınmadı."],
        neden="Gümrük birliğinin güncellenmesi Türkiye'nin AB ile ticaretini doğrudan etkiliyor.",
        sonra="Genişleme raporu aralıktaki liderler zirvesinde ele alınacak.",
        site=[("Reuters", "AB dışişleri bakanları toplantısı · 23 Kasım 2026"), ("Associated Press", "Genişleme gündemi · 23 Kasım 2026")],
        teyit=[("reuters", "15.30", "ok", "Ana kaynak", ""), ("ap", "15.38", "ok", "Teyit", ""), ("aa", "15.44", "warm", "Çelişki", "toplantı günü farklı")],
        teyit_ozet=("fa-triangle-exclamation", "3 kaynak · 1 bağımsız teyit · 1 çelişki", "3. kaynakta toplantı günü farklı; yayımlamadan önce kontrol edin"),
        alternatif=[("AFP · aynı olay", "15.49"), ("AB Konseyi basın bülteni", "15.20")],
        seo=("AB genişleme toplantısında Türkiye de konuşuldu | Dada Haber", "AB dışişleri bakanları Brüksel'de genişlemeyi ele aldı; Türkiye ile gümrük birliği ve vize kolaylığı da gündemdeydi.", "ab-genisleme-toplantisinda-turkiyenin-uyelik-sureci-de-konusuldu", ["ab genişleme", "türkiye ab üyelik", "gümrük birliği"]),
        push=("AB genişleme toplantısında Türkiye de konuşuldu", "Gümrük birliği ve vize kolaylığı gündemdeydi; yeni fasıl açılmasına karar çıkmadı."),
    ),
    "temiz": dict(
        baslik="Benzinde indirim beklentisi: pompaya yansıması hafta sonunu bulabilir",
        spot="Brent petroldeki düşüşün ardından benzinde litre başına indirim bekleniyor. Sektör kaynaklarına dayanan paylaşıma göre indirimin pompaya yansıması hafta sonunu bulabilir.",
        kat="Finans", alt=["Enerji"], kaynaklar=["ekonomi-gundem"], guven=62, gdurum="temiz", gorsel="p192", odak=(50, 50),
        cekilme="23.11.2026 09.04", url="https://x.com/ekonomi_gundem", model="Claude Haiku 4.5",
        metin=["<p>Brent petrol fiyatlarındaki son düşüşün ardından benzinde indirim beklentisi oluştu. @ekonomi_gundem hesabının sektör kaynaklarına dayandırdığı paylaşıma göre indirimin litre başına 1 lira civarında olması ve pompaya hafta sonu yansıması bekleniyor.</p>",
               "<p>İndirime ilişkin dağıtım şirketlerinden ya da EPDK'dan resmî bir açıklama yapılmadı. Akaryakıt fiyatları, ürün fiyatları ve döviz kurundaki değişime göre belirleniyor.</p>"],
        ozet=["Benzinde litre başına 1 lira civarında indirim bekleniyor.", "İndirimin hafta sonu pompaya yansıması bekleniyor.", "Resmî açıklama henüz yok."],
        neden="Akaryakıt fiyatı ulaşım ve gıda fiyatlarını dolaylı olarak etkiliyor.",
        sonra="Dağıtım şirketlerinin fiyat listesi hafta sonundan önce netleşecek.",
        site=[("@ekonomi_gundem (X)", "Paylaşım · 23 Kasım 2026 09.00")],
        teyit=[("ekonomi-gundem", "09.00", "wait", "Ana kaynak", "")],
        teyit_ozet=("fa-circle-exclamation", "1 kaynak · teyit yok", "Aynı olayı veren başka kaynak bulunamadı; tek kaynaklı haber otomatik yayına girmez"),
        alternatif=[],
        seo=None, push=None,
    ),
}


def gorsel_bolum(rid, r):
    gd, gor, (ox, oy) = r["gdurum"], r["gorsel"], r["odak"]
    k1 = KY[r["kaynaklar"][0]][1]
    url = f"../../veri/gorsel/{gor}.jpg" if gor else ""
    bp = f"background-position:{ox}% {oy}%"
    if gd == "eksik":
        ust = f'<div class="kb-bant tehlike">{I("fa-image")}<span><b>Görsel eksik.</b> Kaynağın görselinde {e(k1)} logosu var ve AI temizleyemedi; görsel kullanılmadı. Havuzdan seçin ya da yükleyin. Görseli eksik haber hiçbir zaman otomatik yayımlanmaz (YS1).</span></div>'
        bos_gizli, dolu_gizli, stil = "", " hidden", ""
        ek_et = "Görsel eksik"
    else:
        if gd == "kirpildi":
            ust = (f'<div class="kb-bant bilgi">{I("fa-wand-magic-sparkles")}<span><b>AI kırparak temizledi.</b> Kaynak görselin sağ alt köşesindeki ajans damgası kırpılarak çıkarıldı; kırpılmış hali kullanılıyor. Otomatik yayına girebilir (YS1).</span></div>'
                   f'<div class="form-grid kb-iki-sutun kb-alt-bosluk"><div class="kb-gorsel-kucuk"><span class="kg-resim r-kart" style="background-image:url({url})"></span><div><b>Aslı · kaynaktan</b><span>1600×1067 · sağ altta damga</span></div></div>'
                   f'<div class="kb-gorsel-kucuk"><span class="kg-resim r-kart" style="background-image:url({url});{bp}"></span><div><b>Kırpılmış hali</b><span>1440×960 · damga dışarıda kaldı</span></div></div></div>')
            ek_et = "AI kırparak temizledi"
        else:
            ust = f'<div class="kb-bant tamam">{I("fa-circle-check")}<span><b>Temiz görsel.</b> Logo ya da damga bulunmadı; görsel aynen kullanılıyor (YS1).</span></div>'
            ek_et = "Temiz"
        bos_gizli, dolu_gizli, stil = " hidden", "", f"background-image:url({url});{bp}"
    odak = f'<span class="kg-odak" style="left:{ox}%;top:{oy}%"></span>' if gor else ""
    oneri = ""
    if gd == "eksik":
        oneri = f'<p class="fhint">AI önerisi: havuzda “AB”, “Brüksel” ve “Dışişleri” etiketli 6 görsel var. <button type="button" class="kb-bag" data-medya-sec data-medya-ara="AB Brüksel">Önerileri havuzda aç</button></p>'
    return f"""      <div class="form-sec" id="aiKapak-{rid}" data-alan-id="kapak" data-zorunlu-metin="Kapak görseli yükleyin ya da havuzdan seçin" data-gorsel-alan="haberler.kapak" data-gorsel-ad="Kapak görseli" data-kirp-sonra>
        <div class="form-sec-tt">{I("fa-image")}Kapak görseli<span class="fs-ek">Kaynak: {e(k1)} · {ek_et}</span></div>
        {ust}
        <div class="kb-yukle" data-gorsel-bos{bos_gizli}>{I("fa-cloud-arrow-up")}<b>Kapak görselini sürükleyin ya da seçin</b><span>Web görseli yüklenince mobil görsel ondan otomatik kırpılır · önerilen en az 1280×533</span><span class="kg-acts"><button type="button" class="btn btn-acc btn-sm" data-medya-sec data-medya-ara="AB Brüksel">{I("fa-photo-film")}Havuzdan seç</button><button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{I("fa-upload")}Bilgisayardan yükle</button></span></div>
        {oneri}
        <div class="kb-gorsel" data-gorsel-dolu{dolu_gizli}>
          <div class="kg-bolum">
            <div class="kg-bas">{I("fa-desktop")}Web</div>
            <div class="kg-ikili">
              <div class="kg-resim r-detay" data-gorsel-hedef="web" data-kirp-oran="web.detay" style="{stil}">{odak}<span class="kg-etk">Detay · 2.4:1</span></div>
              <div class="kg-resim r-kart" data-gorsel-hedef="web" data-kirp-oran="web.kart" style="{stil}"><span class="kg-etk">Kart · 16:10</span></div>
            </div>
            <div class="kg-olcu">Önerilen: detay <b>1280×533</b>, kart <b>308×193</b> (sitenin görünen genişliği). <span data-gorsel-bilgi>{"Kırpılmış: 1440×960 JPG" if gd == "kirpildi" else "Kaynaktan: 1280×853 JPG" if gor else ""}</span></div>
            <div class="kg-acts">
              <button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{I("fa-crop-simple")}Kırp ve odak</button>
              <button type="button" class="btn btn-ghost btn-sm" data-medya-sec>{I("fa-photo-film")}Havuzdan seç</button>
              <button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{I("fa-upload")}Yükle</button>
              <button type="button" class="btn btn-ghost btn-sm danger" data-gorsel-kaldir>{I("fa-trash")}Kaldır</button>
            </div>
          </div>
          <div class="kg-bolum">
            <div class="kg-bas">{I("fa-mobile-screen")}Mobil<span class="kg-oto">{I("fa-wand-magic-sparkles")} Webden kırpıldı</span></div>
            <div class="kg-resim r-kart" data-gorsel-hedef="mobil" data-kirp-oran="mobil.kart" style="{stil}">{odak}<span class="kg-etk">Mobil kart · 16:10</span></div>
            <div class="kg-olcu">Önerilen: <b>358×224</b> (sitenin telefon görünümü). Aynı odak noktası kullanılır.</div>
            <div class="kg-acts">
              <button type="button" class="btn btn-ghost btn-sm" data-kirp-ac="mobil.kart">{I("fa-crop-simple")}Kırp</button>
              <button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle data-gorsel-kapsam="mobil">{I("fa-upload")}Ayrı görsel yükle</button>
              <button type="button" class="btn btn-ghost btn-sm" data-gorsel-webe-don hidden>{I("fa-rotate-left")}Webden kırpılana dön</button>
            </div>
          </div>
        </div>
        <div class="frow kb-ust-bosluk"><label for="aiAlt-{rid}">Görsel altyazısı ve kaynağı</label>
          <input class="finput" id="aiAlt-{rid}" data-sayac="120|160" value="{e("Marmara'da kar yağışı, arşiv · Fotoğraf: " + k1) if gor else ""}">
          <div class="char-meter"><span>Görselin altında ve erişilebilirlik metninde</span><b>0 / 120</b></div></div>
      </div>
"""


def profil_blok(r):
    kartlar, cipler = [], []
    for pid, ad, ik in PROFILLER:
        v = r["etki"].get(pid, "")
        on = bool(v)
        cipler.append(f'<button type="button" class="kb-pm-cip{" is-on" if on else ""}" data-pm-cip="{pid}" aria-pressed="{"true" if on else "false"}">{I(ik)}{ad}<i class="fa-solid {"fa-check" if on else "fa-plus"} kb-pm-durum" aria-hidden="true"></i></button>')
        kartlar.append(f'<div class="kb-pm-kart" data-pm-kart="{pid}" data-oneri="{e(v or "Bu profil için öneri üretilmedi; kendi metninizi yazın.")}"{"" if on else " hidden"}><div class="kb-pm-bas">{I(ik)}<b>{ad}</b><button type="button" class="ia-btn danger" data-pm-kaldir aria-label="{ad} metnini kaldır" title="Kaldır">{I("fa-xmark")}</button></div><div class="frow"><textarea class="ftext" rows="2" data-sayac="180|240" aria-label="{ad} için Bana etkisi" placeholder="{ad} bu haberden nasıl etkilenir?">{e(v)}</textarea><div class="char-meter"><span></span><b>0 / 180</b></div></div><input class="finput kb-pm-kaynak kb-ust-bosluk" value="" placeholder="Kaynak (isteğe bağlı) · ör. TÜİK · 3 Kasım" aria-label="{ad} kaynağı"></div>')
    return f"""          <div class="kb-profil-metin" data-profil-metin>
            <div class="kb-pm-ust"><span class="flabel">Bana etkisi</span><span class="kb-pm-say" data-pm-say></span>
              <button type="button" class="btn btn-ghost btn-sm kb-sag" data-pm-oner>{I("fa-wand-magic-sparkles")}Profillere göre öner</button></div>
            <div class="frow"><label for="aiEtki" class="kb-pm-alt">Genel <small>profil seçmemiş okura görünür</small></label>
              <textarea class="ftext" id="aiEtki" rows="2" data-sayac="180|240">{e(r["etki_genel"])}</textarea>
              <div class="char-meter"><span></span><b>0 / 180</b></div></div>
            <div class="kb-pm-cipler" role="group" aria-label="Okur profilleri">{"".join(cipler)}</div>
            <div class="kb-pm-kartlar">{"".join(kartlar)}</div>
            <p class="fhint">Okur Hesabım'da profil seçtiyse sitede kendi profilinin metni öne çıkar. Profil listesi sitenin Hesabım > Tercihler listesiyle aynıdır.</p>
          </div>
"""


def teyit_blok(r):
    ik, bas_, not_ = r["teyit_ozet"]
    lis = []
    for n, (kid, saat, sinif, etk, fark) in enumerate(r["teyit"]):
        k = KY[kid]
        g = GA[k[4]]
        cls = " is-ana" if n == 0 else " is-celiski" if sinif == "warm" else ""
        lis.append(f'<li class="kb-teyit-kaynak{cls}"><span class="kb-teyit-no">{n + 1}</span><div class="kb-teyit-ad"><b>{e(k[1])}</b><span>{k[4]} · {e(g["ad"])} · 23.11.2026 {saat}{" · " + e(fark) if fark else ""}</span></div><span class="pstat {sinif}">{etk}</span><a class="ia-btn" href="https://{e(k[3])}" target="_blank" rel="noopener" aria-label="Kaynağı aç: {e(k[1])}" title="Kaynağı aç">{I("fa-arrow-up-right-from-square")}</a></li>')
    ALT_URL = {"İHA": "https://www.iha.com.tr", "İstanbul": "https://x.com/istanbulvalilik", "AFP": "https://www.afp.com", "AB": "https://www.consilium.europa.eu"}
    alt = "".join(f'<li>{I("fa-link")}<a class="kb-bag" href="{ALT_URL.get(a.split()[0], "https://www.aa.com.tr")}" target="_blank" rel="noopener">{e(a)}</a><span>{s}</span></li>' for a, s in r["alternatif"]) or f'<li>{I("fa-circle-info")}<span>Aynı olayı veren başka kaynak bulunamadı.</span><span>—</span></li>'
    return f"""      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-list-check")}Kaynak teyidi<span class="fs-ek">1., 2., 3. kaynak · aynı haberin iki kez çekilmediğini de gösterir (K8)</span></div>
        <div class="kb-teyit">
          <div class="kb-teyit-ozet"><span class="kb-teyit-durum">{I(ik)}{bas_}</span><span class="kb-teyit-not">{e(not_)}</span></div>
          <ol class="kb-teyit-liste">{"".join(lis)}</ol>
          <div class="kb-teyit-alt"><h3>Alternatif kaynaklar</h3><ul>{alt}</ul></div>
        </div>
      </div>
"""


def kategori_blok(rid, r):
    kat_list = isaret("hb-df-kat").replace(' class="is-sec"', "").replace(f'data-deger="{r["kat"]}" data-ad="{r["kat"]}"', f'data-deger="{r["kat"]}" data-ad="{r["kat"]}" class="is-sec"')
    alt = isaret("hb-df-alt")
    alt = re.sub(r'<span class="kb-cip".*?</button></span>', "", alt, flags=re.S)
    cip = "".join(f'<span class="kb-cip" data-deger="{a}"><span>{a}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for a in r["alt"])
    alt = alt.replace('<input type="text" placeholder="Alt konu ara"', cip + '<input type="text" placeholder="Alt konu ara"').replace('data-ana-kaynak="#dfKatSecim"', f'data-ana-kaynak="#aiKat-{rid}"')
    harita = json.loads(html.unescape(re.search(r'data-alt-harita="([^"]*)"', alt).group(1)))
    alt = re.sub(r'data-havuz="[^"]*"', f'data-havuz="{e(json.dumps(harita[r["kat"]], ensure_ascii=False))}"', alt, count=1)
    yazar = isaret("hb-df-yazar").replace(' class="is-sec"', "")
    tur = isaret("hb-df-tur")
    return f"""      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-sitemap")}Sınıflandırma<span class="fs-ek">AI önerisi · gözden geçirin</span></div>
        <div class="form-grid">
          <div class="frow two">
            <div class="frow"><span class="flabel">Ana kategori</span>
              <div class="kb-secim is-dolu" id="aiKat-{rid}" data-alan-id="kategori" data-deger="{r['kat']}" data-bos="Kategori seçin">
                <button type="button" class="kb-secim-btn" data-acilir="aiKatM-{rid}" aria-expanded="false" aria-haspopup="listbox"><span class="ks-deger">{r['kat']}</span>{I("fa-chevron-down")}</button>
                <div class="pnl-menu kb-secim-menu" id="aiKatM-{rid}"><div class="kb-secim-ara">{I("fa-magnifying-glass")}<input type="search" placeholder="Kategori ara" aria-label="Kategori ara"></div>
                  <div class="kb-secim-liste" role="listbox">{kat_list}</div><div class="kb-secim-bos" hidden>Bu adla kategori yok.</div></div>
              </div>
              <span class="fhint">Adres ve SEO ana kategoriye göre kurulur.</span>
              <div class="ferr">{I("fa-circle-exclamation")}Ana kategori zorunlu.</div></div>
            <div class="frow"><span class="flabel">Alt konular</span>
              {alt}
              <span class="fhint">Birden fazla seçilebilir; <b>ilk seçilen ana alt konudur</b>.</span></div>
          </div>
          <div class="frow two">
            <div class="frow"><span class="flabel">Yazar</span>
              <div class="kb-secim is-dolu" data-alan-id="yazar" data-deger="Dada Haber" data-bos="Yazar seçin">
                <button type="button" class="kb-secim-btn" data-acilir="aiYazar-{rid}" aria-expanded="false" aria-haspopup="listbox"><span class="ks-deger">Dada Haber</span>{I("fa-chevron-down")}</button>
                <div class="pnl-menu kb-secim-menu" id="aiYazar-{rid}"><div class="kb-secim-ara">{I("fa-magnifying-glass")}<input type="search" placeholder="Yazar ara" aria-label="Yazar ara"></div>
                  <div class="kb-secim-liste" role="listbox"><button type="button" data-deger="Dada Haber" data-ad="Dada Haber" class="is-sec">Dada Haber<span class="ks-alt">AI haberlerinde varsayılan imza</span></button>{yazar}</div><div class="kb-secim-bos" hidden>Bu adla yazar yok.</div></div>
              </div><span class="fhint">Onaylayan editör denetim izinde ve sürüm geçmişinde görünür.</span></div>
            <div class="frow"><span class="flabel">Tür</span>
              <div class="kb-secim is-dolu" data-deger="Haber" data-bos="Haber">
                <button type="button" class="kb-secim-btn" data-acilir="aiTur-{rid}" aria-expanded="false" aria-haspopup="listbox"><span class="ks-deger">Haber</span>{I("fa-chevron-down")}</button>
                <div class="pnl-menu kb-secim-menu" id="aiTur-{rid}"><div class="kb-secim-liste" role="listbox">{tur}</div></div>
              </div></div>
          </div>
        </div>
      </div>
"""



def ai_adim():
    """Haber düzenle'deki "Gerisini AI ile üret" adımı (yeni kayıtta görünür; AI haberinde gizli kalır, AI önerisi etiketlerinin onayını kurar)."""
    i = HB.index('<div class="kb-ai-adim"')
    j = HB.index('<div class="form-sec" data-ai-grup="sinif">', i)
    return "      " + HB[i:j].strip().replace('data-ai-kaynak="#fBaslik,#fSpot"', 'data-ai-kaynak="#aiBaslik-kirpildi,#aiSpot-kirpildi"') + "\n"


def detay_kayit(rid, r):
    madde = "".join(f'<div class="km-satir"><span class="km-no">{n + 1}</span><input value="{e(m)}" aria-label="Özet maddesi {n + 1}"></div>' for n, m in enumerate(r["ozet"]))
    site = "".join(f'<div class="km-satir" data-sira><button type="button" class="kb-tutamac" aria-label="Sırayı değiştir (sürükleyin ya da ok tuşları)">{I("fa-grip-vertical")}</button><span class="km-yazi">{e(a)}<small>{e(b)}</small></span><button type="button" class="ia-btn" data-satir-duzenle aria-label="Kaynağı düzenle">{I("fa-pen")}</button><button type="button" class="ia-btn danger" data-satir-sil aria-label="Kaynağı kaldır">{I("fa-trash")}</button></div>' for a, b in r["site"])
    return f"""     <div data-kayit-icin="{rid}"{' data-kayit-varsayilan="kirpildi"' if rid == "kirpildi" else ""}>
      <div class="form-sec">
        <div class="form-grid">
          <div class="frow"><label for="aiBaslik-{rid}">Başlık</label>
            <input class="finput kb-buyuk" id="aiBaslik-{rid}" data-alan-id="baslik" data-sayac="70|90" value="{e(r['baslik'])}">
            <div class="char-meter"><span>Sitede başlık; SEO başlığı buradan üretilir</span><b>0 / 70</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Başlık zorunlu.</div></div>
          <div class="frow"><label for="aiSpot-{rid}">Spot</label>
            <textarea class="ftext" id="aiSpot-{rid}" data-alan-id="spot" data-sayac="220|280">{e(r['spot'])}</textarea>
            <div class="char-meter"><span>Başlığın altındaki giriş cümlesi</span><b>0 / 220</b></div>
            <div class="ferr">{I("fa-circle-exclamation")}Spot zorunlu.</div></div>
        </div>
      </div>
{ai_adim() if rid == "kirpildi" else ""}{kategori_blok(rid, r)}{gorsel_bolum(rid, r)}
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-align-left")}Haber metni<span class="fs-ek">AI kaynaklardan yazdı · okuyup düzeltin</span></div>
        <div class="kb-editor" data-editor-ad="Haber metni" data-editor-medya>
          <div class="kz-alan ke-alan" data-alan-id="metin" data-zorunlu-metin="Haber metnini yazın">{"".join(r['metin'])}</div>
          <div class="kz-alt"><span data-kz-say></span><span>Sitede “Haberi dinle” bu metinden okunur</span></div>
        </div>
      </div>

      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-bolt")}Dada Özet<span class="fs-ek">Sitede 15 sn · 1 dk · tam metin katmanları</span></div>
        <div class="form-grid">
          <div class="frow"><span class="flabel">Üç maddede özet</span><div class="kb-madde">{madde}</div></div>
          <div class="frow"><label for="aiNeden-{rid}">Neden önemli?</label>
            <textarea class="ftext" id="aiNeden-{rid}" data-sayac="180|240">{e(r['neden'])}</textarea>
            <div class="char-meter"><span>Sitede açılır kutuda</span><b>0 / 180</b></div></div>
          <div class="frow"><label for="aiSonra-{rid}">Bundan sonra ne olacak?</label>
            <textarea class="ftext" id="aiSonra-{rid}" data-sayac="180|240">{e(r['sonra'])}</textarea>
            <div class="char-meter"><span>Sitede açılır kutuda</span><b>0 / 180</b></div></div>
{profil_blok(r) if r.get("etki") else ""}        </div>
      </div>

      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-link")}Kaynaklar<span class="fs-ek">Sitede haberin sonunda; teyit sayısı gösterilmez</span></div>
        <div class="kb-madde" data-satir-liste data-siralanir data-satir-ad="Kaynak" data-satir-alan1="Kaynak adı (kurum, belge)" data-satir-alan2="Açıklama, tarih ya da bağlantı">
          {site}
          <button type="button" class="kb-ekle-btn" data-satir-ekle>{I("fa-plus")}Kaynak ekle</button>
        </div>
      </div>
{teyit_blok(r)}     </div>
"""


def bilgi_seridi(rid, r):
    k1 = KY[r["kaynaklar"][0]]
    g = GA[k1[4]]
    kan = g["kanallar"]
    sosyal_yalniz = kan == ["sosyal"]
    durum = '<span class="pstat warm">Görsel eksik</span>' if r["gdurum"] == "eksik" else '<span class="pstat wait">Onay bekliyor</span>'
    gor = {"temiz": '<span class="pstat ok">Temiz</span>', "kirpildi": '<span class="pstat info">AI kırparak temizledi</span>', "eksik": '<span class="pstat warm">Görsel eksik</span>'}[r["gdurum"]]
    kk = f'1. kaynağın grubundan: {k1[4]} · {g["ad"]}' + (" · gönderi bağlantısız (YS2)" if sosyal_yalniz else "")
    return f"""  <section class="pnl-card dash-row" data-kayit-icin="{rid}" aria-label="AI kaynağı">
    <div class="pc-head"><h2 class="pc-title">{I("fa-robot")}AI kaynağı</h2><span class="kb-guven k-lg" data-guven="{r['guven']}" data-esik="{ESIK}"></span></div>
    <div class="pc-body">
      <div class="form-grid kb-iki-sutun">
        <div class="sa-durum">
          <div><span>Durum</span><b>{durum}</b></div>
          <div><span>Çekilme</span><b>{e(r['cekilme'])}</b></div>
          <div><span>1. kaynak</span><b>{e(k1[1])} · {k1[4]}</b></div>
          <div><span>Kaynak adresi</span><b><a class="kb-bag" href="{e(r['url'])}" target="_blank" rel="noopener">{e(k1[3])}</a></b></div>
        </div>
        <div class="sa-durum">
          <div><span>AI modeli</span><b>{e(r['model'])}</b></div>
          <div><span>Görsel</span><b>{gor}</b></div>
          <div><span>Kaynak sayısı</span><b>{len(r['kaynaklar'])}{" · tek kaynak" if len(r['kaynaklar']) == 1 else ""}</b></div>
          <div data-izin="ai-maliyet"><span>İşleme maliyeti</span><b>$0,021 · 2.140 token</b></div>
        </div>
      </div>
      <div class="frow kb-ust-bosluk"><span class="flabel">Yayın kanalları</span>
        <div data-roller="super gyy">{kanallar_html(kan)}</div>
        <div data-roller="editor kat-ed analist sosyal">{kanallar_html(kan, salt=True)}</div>
        <span class="kb-kanal-kaynak">{I("fa-lock")}{e(kk)}<span data-roller="editor kat-ed analist sosyal"> · Editör kanalları değiştiremez (YS3)</span><span data-roller="super gyy"> · bu haberde değiştirirseniz denetim izine yazılır (YS3)</span></span></div>
    </div>
  </section>
"""


def seo_kayit(rid, r):
    if not r["seo"]:
        return f'      <div class="form-sec" data-kayit-icin="{rid}"><div class="kb-bant bilgi">{I("fa-link-slash")}<span><b>Yalnız Sosyal Medya kanalı.</b> Bu haber 1. kaynağın grubu ({KY[r["kaynaklar"][0]][4]}) gereği yalnız sosyal medyada yayımlanır; sitede sayfa açılmaz, SEO uygulanmaz (YS2). Kanalı Süper Admin ya da Genel Yayın Yönetmeni değiştirirse SEO otomatik üretilir.</span></div></div>\n'
    b, a, slug, kw = r["seo"]
    pre = f'dadahaber.com/{"gundem" if r["kat"] == "Gündem" else "dunya" if r["kat"] == "Dünya" else "finans"}/'
    cip = "".join(f'<span class="kb-cip" data-deger="{e(k)}"><span>{e(k)}</span><button type="button" aria-label="Kaldır">{I("fa-xmark")}</button></span>' for k in kw)
    return f"""      <div class="form-sec" data-kayit-icin="{rid}">
        <div class="form-sec-tt">{I("fa-wand-magic-sparkles")}Otomatik üretildi<span class="kb-ai-oneri">{I("fa-wand-magic-sparkles")}AI önerisi · onay bekliyor<button type="button" data-ai-onayla>Onayla</button></span><span class="fs-ek"><button type="button" class="btn btn-ghost btn-sm" data-seo-uret>{I("fa-rotate")}Başlıktan yeniden üret</button></span></div>
        <div class="form-grid">
          <div class="frow"><label for="sBaslik-{rid}">SEO başlığı</label>
            <input class="finput" id="sBaslik-{rid}" data-alan="seo-baslik-{rid}" data-sayac="60|70" value="{e(b)}">
            <div class="char-meter"><span>Arama sonucunda görünen başlık · 50–60 karakter önerilir</span><b>0 / 60</b></div></div>
          <div class="frow"><label for="sAciklama-{rid}">SEO açıklaması</label>
            <textarea class="ftext" id="sAciklama-{rid}" data-alan="seo-aciklama-{rid}" data-sayac="155|170">{e(a)}</textarea>
            <div class="char-meter"><span>Arama sonucunda başlığın altında · 120–155 karakter önerilir</span><b>0 / 155</b></div></div>
          <div class="frow"><label for="sSlug-{rid}">Adres</label>
            <div class="slug-wrap"><span class="slug-pre">{pre}</span><input class="finput" id="sSlug-{rid}" data-alan="slug-{rid}" value="{slug}"></div>
            <span class="fhint">Yayımlandıktan sonra değiştirilirse eski adres yeniye yönlendirilir.</span></div>
          <div class="frow"><span class="flabel">Anahtar kelimeler</span>
            <div class="kb-cip-girdi" data-serbest>{cip}<input type="text" placeholder="Yazın; Enter ya da virgülle ekleyin" aria-label="Anahtar kelime ekle"><div class="pnl-menu kb-cip-oneri"></div></div></div>
          <div class="frow"><span class="flabel">Arama sonucu önizlemesi</span>
            <div class="serp"><div class="serp-url"><span class="serp-fav kb-logo-isaret"></span><span>{pre.replace("/", " › ").rstrip(" › ")} › <span data-alan="slug-{rid}">{slug}</span></span></div>
              <div class="serp-title" data-alan="seo-baslik-{rid}">{e(b)}</div>
              <div class="serp-desc" data-alan="seo-aciklama-{rid}">{e(a)}</div></div></div>
          <div class="toggle-row"><span>Google Haberler ve Discover'a uygun<small>NewsArticle şeması ve büyük görsel önizlemesi açık</small></span><label class="toggle"><input type="checkbox" checked aria-label="Google Haberler uygunluğu"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        </div>
      </div>
"""


def bildirim_kayit(rid, r):
    if not r["push"]:
        return f'      <div class="form-sec" data-kayit-icin="{rid}"><div class="kb-bant bilgi">{I("fa-bell-slash")}<span><b>Bildirim gönderilmez.</b> Yalnız Sosyal Medya kanalına giden haberde telefon ve web bildirimi yoktur (YS2).</span></div></div>\n'
    b, m = r["push"]
    return f"""      <div class="form-sec" data-kayit-icin="{rid}">
        <div class="form-sec-tt">{I("fa-bell")}Bildirim<span class="kb-ai-oneri">{I("fa-wand-magic-sparkles")}AI önerisi · onay bekliyor<button type="button" data-ai-onayla>Onayla</button></span></div>
        <div class="form-grid">
          <div class="frow"><span class="flabel">Kanallar</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="checkbox">Telefon bildirimi</label><label class="kb-secenek"><input type="checkbox">Web bildirimi</label></div>
            <span class="fhint">AI haberlerinde bildirim varsayılan olarak kapalıdır; editör isterse işaretler.</span></div>
          <div class="frow"><label for="bBaslik-{rid}">Bildirim başlığı</label>
            <input class="finput" id="bBaslik-{rid}" data-alan="push-baslik-{rid}" data-sayac="60|65" value="{e(b)}">
            <div class="kb-cubuk"><span></span></div>
            <div class="char-meter"><span>Telefonda kalın satır · 60 karaktere kadar tam görünür</span><b>0 / 60</b></div></div>
          <div class="frow"><label for="bIcerik-{rid}">Bildirim metni</label>
            <textarea class="ftext" id="bIcerik-{rid}" data-alan="push-metin-{rid}" data-sayac="150|178">{e(m)}</textarea>
            <div class="kb-cubuk"><span></span></div>
            <div class="char-meter"><span>Kilit ekranında 3 satıra kadar · 150 karakter önerilir</span><b>0 / 150</b></div></div>
          <div class="toggle-row"><span>Bildirim görseli<small>Kapak görselinin mobil kırpımı kullanılır (2:1)</small></span><label class="toggle"><input type="checkbox"{"" if r["gdurum"] == "eksik" else " checked"} aria-label="Bildirim görseli"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
          <div class="frow"><span class="flabel">Ne zaman</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="bZaman-{rid}" checked>Onaylanınca hemen</label><label class="kb-secenek"><input type="radio" name="bZaman-{rid}" data-ac="bZamanSec-{rid}">Zamanla</label></div>
            <div id="bZamanSec-{rid}" hidden>
              <div class="kb-tarih-sec" id="bTarih-{rid}" data-deger="2026-11-23 18.30" data-enaz="bugun">
                <button type="button" class="kb-tarih-btn" data-acilir="bTarihMenu-{rid}" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
                <div class="pnl-menu kb-tarih-menu" id="bTarihMenu-{rid}" role="dialog" aria-label="Tarih ve saat seç"></div>
              </div>
            </div></div>
        </div>
      </div>
"""


def bildirim_onizleme(rid, r):
    if not r["push"]:
        return ""
    b, m = r["push"]
    gor = f'<span class="kp-resim" style="background-image:url(../../veri/gorsel/kucuk/{r["gorsel"]}.jpg)"></span>' if r["gorsel"] else ""
    return f"""      <section class="pnl-card" data-kayit-icin="{rid}"><div class="pc-head"><h2 class="pc-title">{I("fa-mobile-screen")}Bildirim önizlemesi</h2></div>
      <div class="pc-body"><div class="kb-onizle-kap">
        <div class="kb-onizle-sec" data-segment><button type="button" class="is-on" data-hedef="onzTel-{rid}" aria-pressed="true">Telefon</button><button type="button" data-hedef="onzWeb-{rid}" aria-pressed="false">Web</button></div>
        <div id="onzTel-{rid}"><div class="kb-telefon"><div class="kb-telefon-ekran">
          <div class="kt-zaman">16.05</div><div class="kt-tarih">23 Kasım Pazartesi</div>
          <div class="kb-push"><span class="kp-ikon kb-logo-isaret"></span><div class="kp-ic"><div class="kp-ust"><span>DADA HABER</span><span>şimdi</span></div><b data-alan="push-baslik-{rid}">{e(b)}</b><p data-alan="push-metin-{rid}">{e(m)}</p></div>{gor}</div>
        </div></div></div>
        <div id="onzWeb-{rid}" hidden><div class="kb-web-push"><span class="kp-ikon kb-logo-isaret"></span><div><b data-alan="push-baslik-{rid}">{e(b)}</b><p data-alan="push-metin-{rid}">{e(m)}</p><small>dadahaber.com · Chrome</small></div></div></div>
        <p class="kb-onizle-not">Önizleme yaklaşıktır; telefonun ve tarayıcının görünümüne göre değişir.</p>
      </div></div></section>
"""


SOSYAL_METIN = {
    "x": "Meteoroloji'den Marmara için turuncu kod: İstanbul'un kuzeyinde kar 15 santimetreyi bulabilir. Toplu taşıma gece yarısına kadar uzatıldı.\n\nhttps://dadahaber.com/gundem/meteorolojiden-marmara-icin-turuncu-kod-kar-uyarisi\n\n#kar #İstanbul",
    "facebook": "Meteoroloji Genel Müdürlüğü, Marmara Bölgesi için 24 Kasım sabahından itibaren turuncu kodlu kar uyarısı yaptı. İstanbul'un kuzey ilçelerinde kar kalınlığı yer yer 15 santimetreyi bulabilir.\n\nSalı sabahı ulaşıma ek süre ayırın; toplu taşıma seferleri gece yarısına kadar uzatıldı.\n\nhttps://dadahaber.com/gundem/meteorolojiden-marmara-icin-turuncu-kod-kar-uyarisi",
    "linkedin": "Marmara için turuncu kod: kar yağışının salı sabahı ulaşımı etkilemesi bekleniyor.\n\nİşverenler için not: İstanbul Valiliği zorunlu olmadıkça özel araçla yola çıkılmamasını istiyor; esnek çalışma planı yapmak için iyi bir gün.\n\nhttps://dadahaber.com/gundem/meteorolojiden-marmara-icin-turuncu-kod-kar-uyarisi\n\n#kar #istanbul",
    "instagram": "Marmara'ya turuncu kod ❄️ İstanbul'un kuzeyinde kar 15 santimetreyi bulabilir; toplu taşıma gece yarısına kadar uzatıldı.\n\nAyrıntılar profildeki bağlantıda.\n\n#kar #istanbul #marmara #dadahaber",
    "telegram": "❄️ Marmara için turuncu kod kar uyarısı\n\nİstanbul'un kuzeyinde kar 15 santimetreyi bulabilir; toplu taşıma gece yarısına kadar uzatıldı.\n\nhttps://dadahaber.com/gundem/meteorolojiden-marmara-icin-turuncu-kod-kar-uyarisi",
}


def sosyal_panel():
    i = HB.index('<div class="form-sec kb-sosyal">')
    j = HB.rindex("</div>", i, HB.rindex("</div>", i, HB.index("</section>", i)))  # kb-sosyal kabı + panel kapanışı dışarıda
    h = HB[i:j + 6]
    # platform metinleri bu haberinkiyle
    for p, t in SOSYAL_METIN.items():
        h = re.sub(r'(data-platform="%s"[^>]*?data-metin=")[^"]*(")' % p, lambda m: m.group(1) + e(t) + m.group(2), h, flags=re.S)
    h = h.replace("p203.jpg", "p183.jpg").replace('data-kirp-alan="#hbKapak"', 'data-kirp-alan="#aiKapak-kirpildi"')
    h = h.replace('<div class="form-sec kb-sosyal">', '<div class="form-sec kb-sosyal" data-kayit-icin="kirpildi">', 1)
    return h


def sosyal_onizleme():
    m = re.search(r'(<div class="kb-yan-onizle" data-panel-icin="pSosyal" hidden>.*?</div></section>\s*</div>)', HB, re.S)
    h = m.group(1).replace("p203.jpg", "p183.jpg").replace("dadahaber.com · Asgari ücret görüşmelerinde ilk toplantı 4 Aralık'ta", "dadahaber.com · Meteoroloji'den Marmara için turuncu kod kar uyarısı")
    h = h.replace('<section class="pnl-card">', '<section class="pnl-card" data-kayit-icin="kirpildi">', 1)
    return h


def sayfa_duzenle():
    okuma_roller = " ".join(OKUMA["roller"])
    sub = {rid: f'{r["kat"]} › {r["alt"][0]} · {KY[r["kaynaklar"][0]][1]} ({KY[r["kaynaklar"][0]][4]}) · {r["cekilme"]}\'de çekildi · onay bekliyor' for rid, r in KAYIT.items()}
    s = bas("AI haber düzenle", "duzenle")
    s += f"""
<!-- AI HABER DÜZENLE: Haber düzenle formunun aynısı (zorunlu kayıt haberler.haber) + AI kaynağı şeridi (güven, çekilme, kaynak, model,
     kanallar: Editör görür, değiştiremez YS3) + kaynak teyidi (K8) + görsel durumu (YS1) + "Onayla ve Yayınla" okuma onayıyla (Y2, YS5).
     Üç örnek kayıt ?id= ile: kirpildi (varsayılan), eksik, temiz (yalnız sosyal kanal, YS2). -->
<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>AI haber düzenle</h1>
      {"".join(f'<div class="ph-sub" data-kayit-icin="{rid}">{e(t)}</div>' for rid, t in sub.items())}
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="ai-havuz.havuz" href="index.html">{I("fa-arrow-left")}Haber havuzuna dön</a>
      {"".join(f'<a class="btn btn-ghost btn-sm" data-kayit-icin="{rid}" href="{e(r["url"])}" target="_blank" rel="noopener">{I("fa-arrow-up-right-from-square")}Kaynak haberini aç</a>' for rid, r in KAYIT.items())}
    </div>
  </div>

  <div class="kb-bant bilgi dash-row" data-roller="{okuma_roller}">{I("fa-book-open-reader")}<span><b>Okumadan onay yok.</b> “Onayla ve Yayınla” Detay sekmesini sonuna kadar okuyunca açılır; kaydet çubuğundaki düğmede ilerleme görünür. Diğer sekmelere girmek zorunlu değil (Y2, YS5).</span></div>
{"".join(bilgi_seridi(rid, r) for rid, r in KAYIT.items())}
  <div class="form-layout">
  <section class="pnl-card" id="aiForm" data-form data-sekmeli data-zorunlu-kayit="haberler.haber" aria-label="AI haber formu">
{dil_secici("Dil seçici bütün sekmelerdeki metin alanlarını birlikte değiştirir; görsel, yazar ve kategori bütün dillerde ortaktır. AI çevirisi denetimsiz yayımlanmaz.")}
    <div class="sa-form-tabs" role="tablist" aria-label="Düzenleme sekmeleri">
      <button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="pDetay">{I("fa-file-lines")}Detay</button>
      <button type="button" class="sa-form-tab has-ai" role="tab" aria-selected="false" data-panel="pSeo">{I("fa-magnifying-glass-chart")}SEO</button>
      <button type="button" class="sa-form-tab has-ai" role="tab" aria-selected="false" data-panel="pBildirim" data-modul="etkilesim">{I("fa-bell")}Bildirim</button>
      <button type="button" class="sa-form-tab has-ai" role="tab" aria-selected="false" data-panel="pSosyal" data-modul="sosyal-medya">{I("fa-share-nodes")}Sosyal Medya</button>
    </div>

    <!-- ================= DETAY (okunacak sekme, YS5) ================= -->
    <div class="sa-form-panel" id="pDetay" role="tabpanel">
{"".join(detay_kayit(rid, r) for rid, r in KAYIT.items())}
      <div class="form-sec">
        <div class="form-sec-tt">{I("fa-comments")}Okur etkileşimi</div>
        <div class="form-grid">
          <div class="toggle-row"><span>Yorumlar açık<small>Yorumları editörler yönetir</small></span><label class="toggle"><input type="checkbox" checked aria-label="Yorumlar açık"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
          <div class="toggle-row"><span>Haberi dinle<small>Metin tarayıcının sesiyle okunur</small></span><label class="toggle"><input type="checkbox" checked aria-label="Haberi dinle"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        </div>
      </div>
    </div>

    <!-- ================= SEO ================= -->
    <div class="sa-form-panel is-ai" id="pSeo" role="tabpanel" data-ai-grup="seo" hidden>
{"".join(seo_kayit(rid, r) for rid, r in KAYIT.items())}    </div>

    <!-- ================= BİLDİRİM ================= -->
    <div class="sa-form-panel is-ai" id="pBildirim" role="tabpanel" data-ai-grup="bildirim" hidden>
{"".join(bildirim_kayit(rid, r) for rid, r in KAYIT.items())}    </div>

    <!-- ================= SOSYAL MEDYA ================= -->
    <div class="sa-form-panel is-ai" id="pSosyal" role="tabpanel" data-ai-grup="sosyal" hidden>
      <div class="form-sec" data-kayit-icin="eksik"><div class="kb-bant uyari">{I("fa-image")}<span><b>Görsel seçilince sosyal kartlar üretilir.</b> Bu haberin görseli eksik (YS1); Detay sekmesinde havuzdan seçtiğiniz görselle platform metinleri ve kırpımlar burada hazırlanır.</span></div></div>
      <div class="form-sec" data-kayit-icin="temiz"><div class="kb-bant bilgi">{I("fa-link-slash")}<span><b>Bağlantısız gönderi (YS2).</b> Bu haber yalnız Sosyal Medya kanalına gider: metin ve görsel kendi başına durur, haber gönderinin içinde özetlenir, sitede sayfa açılmaz. Gönderi onaydan sonra <a class="kb-bag" data-modul="sosyal-medya" data-hedef="sosyal-medya.gonderi" href="../../cekirdek/yakinda.html?s=sosyal-medya.gonderi">Gönderi Oluştur</a> ekranında bu haberle açılır.</span></div></div>
      {sosyal_panel()}
    </div>
  </section>

  <aside class="side-card" aria-label="Yayın">
    <div class="kb-yan-onizle" data-panel-icin="pBildirim" hidden>
{"".join(bildirim_onizleme(rid, r) for rid, r in KAYIT.items())}    </div>
    {sosyal_onizleme()}
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{I("fa-paper-plane")}Yayın</h2><span class="status-dot" data-state="taslak" title="Taslak"></span></div>
      <div class="pc-body sc-stack">
        <div class="sc-field"><span class="flabel">Durum</span><b>Taslak · onay bekliyor</b></div>
        <div class="sc-field"><span class="flabel">Yayın zamanı</span>
          <div class="kb-tarih-sec" id="aiTarih" data-deger="" data-bos="Onaylanınca o anın saati" data-temizlenir="1">
            <button type="button" class="kb-tarih-btn" data-acilir="aiTarihMenu" aria-expanded="false" aria-haspopup="dialog">{I("fa-calendar-days")}<span class="kt-deger"></span></button>
            <div class="pnl-menu kb-tarih-menu" id="aiTarihMenu" role="dialog" aria-label="Tarih ve saat seç"></div>
          </div></div>
        <div class="toggle-row"><span>Manşette<small>Vitrinden sıralanır</small></span><label class="toggle"><input type="checkbox" aria-label="Manşette"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        <div class="toggle-row"><span>Son dakika<small>Şeritte ve sayfada görünür</small></span><label class="toggle"><input type="checkbox" aria-label="Son dakika"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        <div class="kb-surum"><span><b>AI taslağı</b> · ilk sürüm · henüz insan düzenlemesi yok</span></div>
      </div>
    </section>
  </aside>
  </div>

  <div class="kb-kaydet" data-form-icin="aiForm">
    <div class="kk-durum">{I("fa-circle-dot")}<span>AI taslağı · henüz onaylanmadı</span></div>
    <div class="kk-sag">
      <button type="button" class="btn btn-ghost btn-sm danger" data-pencere="aiReddet">{I("fa-ban")}Reddet</button>
      <button type="button" class="btn btn-ghost btn-sm" data-kaydet data-kaydet-tur="taslak" data-kaydet-metin="Taslak olarak kaydedildi" data-bildir="Taslak kaydedildi; havuzda onay bekliyor">{I("fa-floppy-disk")}Taslak kaydet</button>
      <div class="kb-okuma-onay" data-okuma-hedef="#pDetay" data-okuma-roller="{okuma_roller}" data-okuma-sure="{OKUMA['sigan_icerik_saniye']}"><button type="button" class="btn btn-acc btn-sm" data-okuma-btn data-kaydet data-kaydet-metin="Onaylandı ve yayımlandı" data-bildir="Haber onaylandı ve yayımlandı; 1. kaynağın grubundaki kanallarda görünür">{I("fa-check")}Onayla ve Yayınla</button><span class="ko-neden"></span></div>
    </div>
  </div>
</main>
</div>
{reddet_sablonu()}"""
    s += son(editor=True)
    return s

# @@SAYFALAR@@

if __name__ == "__main__":
    yaz = {"index.html": sayfa_havuz, "kaynaklar.html": sayfa_kaynaklar, "motor.html": sayfa_motor, "cron.html": sayfa_cron,
           "ayarlar.html": sayfa_ayarlar, "duzenle.html": sayfa_duzenle}
    for ad, fn in yaz.items():
        (BURA / ad).write_text(fn(), encoding="utf-8")
        print("yazıldı:", ad)
