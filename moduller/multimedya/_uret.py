#!/usr/bin/env python3
"""Multimedya ve Medya Havuzu modülü · sayfa üretici (yalnız moduller/multimedya/ altına yazar).

Kullanım:  python3 -I moduller/multimedya/_uret.py && python3 -I araclar/menu_yaz.py --yalniz moduller/multimedya

Kaynaklar (yalnızca okunur):
  - public sözlük: ../dadahaber-prototip/araclar/ornek_veri.json (video, podcast, Haber Dinle, Foto Fokus, infografik)
  - public sayfalar: podcast.html (seriler), foto-fokus.html (fotoğraf sayısı), akis.html, canli-yayin.html, haber-dinle.html
  - ek sözlük: veri/panel.json → medya_havuzu (görseller ve etiket havuzu, M2), personalar
Ortak bileşenlerin işaretlemesi ui-kit.html ve moduller/haberler/duzenle.html ile aynıdır; sayfaya stil ya da betik konmaz.
"""
import glob, hashlib, html, json, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
PUB = KOK.parent / "dadahaber-prototip"
KLASOR = KOK / "moduller" / "multimedya"
SITE = "https://gaviaworks-dev.github.io/dadahaber-prototip/"

soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
pv = json.loads((KOK / "veri" / "panel.json").read_text(encoding="utf-8"))
MH = pv["medya_havuzu"]
EH = MH["etiket_havuzu"]
GORSELLER = [g["dosya"] for g in MH["gorseller"]]
KATEGORILER = ["Gündem", "Spor", "Finans", "Kadın", "Savunma", "Dünya", "Kampüs", "Keşfet"]
YAZARLAR = [y["ad"] if isinstance(y, dict) else y for y in soz["yazarlar"]]


def e(s):
    return html.escape(str(s), quote=True)


def h(s, n):
    """Kararlı küçük sayı (örnek veri için)."""
    return int(hashlib.md5(s.encode("utf-8")).hexdigest()[:8], 16) % n


def gorsel_sec(anahtar):
    return GORSELLER[h(anahtar, len(GORSELLER))]


def tarih(t, s=None):
    y, a, g = t.split("-")
    return f"{g}.{a}.{y}" + (f" {s}" if s else "")


def sure_yaz(sn):
    sa, dk, s = sn // 3600, sn % 3600 // 60, sn % 60
    if sa:
        return f"{sa} sa {dk} dk"
    return (f"{dk} dk " if dk else "") + f"{s} sn"


# public sayfalarda başlık → görsel
basliklar = {x["baslik"] for x in soz["haberler"]}
GORSEL = {}
for f in sorted(glob.glob(str(PUB / "*.html"))):
    t = open(f, encoding="utf-8").read()
    for m in re.finditer(r"url\(assets/gorsel/(p\d+\.jpg)\)", t):
        hh = re.search(r"<h[23][^>]*>(?:<a[^>]*>)?([^<]+)<", t[m.end():m.end() + 1500])
        if hh:
            b = html.unescape(hh.group(1).strip())
            if b in basliklar and b not in GORSEL and m.group(1) in GORSELLER:
                GORSEL[b] = m.group(1)


def g_of(baslik):
    return GORSEL.get(baslik) or gorsel_sec(baslik)


def tur_listesi(detay):
    return sorted([x for x in soz["haberler"] if x["detay"] == detay], key=lambda x: (x["tarih"], x["saat"]), reverse=True)


# =====================================================================
# ortak parçalar (ui-kit işaretlemesi)
# =====================================================================
def bas(title, sayfa, yeni_baslik=None):
    yb = f' data-yeni-baslik="{e(yeni_baslik)}"' if yeni_baslik else ""
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(title)} · Dada Haber Yönetim Paneli</title>
<link rel="stylesheet" href="../../assets/vendor/fontawesome-6.5.2/css/all.min.css">
<link rel="stylesheet" href="../../tema/dadahaber.css" data-tema>
<link rel="stylesheet" href="../../cekirdek/css/kabuk.css">
<link rel="stylesheet" href="../../cekirdek/css/bilesen.css">
<!--P:bas--><!--/P:bas-->
</head>
<body data-sayfa="{sayfa}"{yb}>
<div class="sa-app">
<!--P:menu--><!--/P:menu-->
<div class="pnl-overlay" id="pnlOverlay"></div>
<!--P:ust--><!--/P:ust-->

<main class="pnl-main" id="icerik">
"""


def son(sablonlar="", editor=False):
    ed = ('\n<script src="../../assets/vendor/tiptap-2.27.3/tiptap.min.js"></script>'
          '\n<script src="../../cekirdek/js/editor.js"></script>') if editor else ""
    return f"""</main>
</div>
{sablonlar}
<script src="../../cekirdek/js/kabuk.js"></script>
<script src="../../cekirdek/js/bilesen.js"></script>
<script src="../../cekirdek/js/form.js"></script>
<script src="../../cekirdek/js/alan.js"></script>
<script src="../../cekirdek/js/kirp.js"></script>{ed}
</body>
</html>
"""


def bb(metin):
    """Yazım kuralı (Beyar): etiket, düğme, sekme ve başlıkta her kelimenin baş harfi büyük; bağlaç ve edatlar küçük; Türkçe büyük harf."""
    def k(w, ilk):
        m = re.match(r"^([(“\"']*)(.)(.*)$", w)
        if not m or (not ilk and w in ("ve", "ya", "da", "de", "ile", "için", "veya", "ki")):
            return w
        o, c, r_ = m.groups()
        if not re.match(r"[a-zçğıöşü]", c) or re.search(r"[A-ZÇĞİÖŞÜ]", r_):
            return w
        return o + {"i": "İ", "ı": "I"}.get(c, c.upper()) + r_
    return " ".join(k(w, i == 0) for i, w in enumerate(metin.split(" ")))


def ikon(ad, cls="fa-solid"):
    return f'<i class="{cls} {ad}" aria-hidden="true"></i>'


def sayfa_bas(h1, alt, eylemler):
    return f"""  <div class="pnl-page-head">
    <div>
      {h1}
      {alt}
    </div>
    <div class="ph-actions">
      {eylemler}
    </div>
  </div>
"""


def btn_link(hedef, metin, ik, acc=False, ek="", roller=None, href=None):
    cls = "btn btn-acc btn-sm" if acc else "btn btn-ghost btn-sm"
    r = f' data-roller="{roller}"' if roller else ""
    hek = f' data-hedef-ek="{e(ek)}"' if ek else ""
    if href:  # aynı klasördeki dosyaya doğrudan bağlantı (modül içi)
        return f'<a class="{cls}" href="{e(href)}"{r}>{ikon(ik)}{metin}</a>'
    return f'<a class="{cls}" data-hedef="{hedef}"{hek}{r} href="#icerik">{ikon(ik)}{metin}</a>'


def secim(sid, deger, secenekler, alan_id=None, bos="Seçin", ara=None, etk=None, suz=None, ek="", ad_goster=None,
          zorunlu_metin=None, alan=None, bos_metin="Bu adla seçenek yok."):
    """Aranabilir açılır liste (kb-secim). secenekler: [(deger, ad, alt)] ya da ('grup', ad)."""
    dolu = deger not in (None, "")
    nit = ""
    if alan_id:
        nit += f' data-alan-id="{alan_id}"'
    if zorunlu_metin:
        nit += f' data-zorunlu-metin="{e(zorunlu_metin)}"'
    if suz:
        nit += f' data-suz="{suz}"'
    if alan:
        nit += f' data-alan="{alan}"'
    if dolu:
        nit += f' data-deger="{e(deger)}"'
    gost = ad_goster if ad_goster is not None else next((s[1] for s in secenekler if s[0] == deger and s[0] != "grup"), deger)
    if not dolu:
        gost = "Tümü" if suz else bos
    ops = ""
    for s in secenekler:
        if s[0] == "grup":
            ops += f'<div class="ks-grup">{e(s[1])}</div>'
            continue
        d, a = s[0], s[1]
        alt = f'<span class="ks-alt">{e(s[2])}</span>' if len(s) > 2 and s[2] else ""
        sec = ' class="is-sec"' if dolu and d == deger else ""
        ops += f'<button type="button" data-deger="{e(d)}" data-ad="{e(a)}"{sec}>{e(a)}{alt}</button>'
    arama = (f'<div class="kb-secim-ara"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>'
             f'<input type="search" placeholder="{e(ara)}" aria-label="{e(ara)}"></div>') if ara else ""
    bosk = f'<div class="kb-secim-bos" hidden>{e(bos_metin)}</div>' if ara else ""
    etiket = f'<span class="ks-etk">{e(etk)}</span>' if etk else ""
    return (f'<div class="kb-secim{" is-dolu" if dolu else ""}"{nit} data-bos="{e("Tümü" if suz else bos)}"{ek}>'
            f'<button type="button" class="kb-secim-btn" data-acilir="{sid}" aria-expanded="false" aria-haspopup="listbox">{etiket}<span class="ks-deger">{e(gost)}</span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button>'
            f'<div class="pnl-menu kb-secim-menu" id="{sid}">{arama}<div class="kb-secim-liste" role="listbox">{ops}</div>{bosk}</div></div>')


def kat_secim(sid, deger, alan_id="kategori"):
    ops = [(k, k) for k in KATEGORILER]
    return secim(sid, deger, ops, alan_id=alan_id, bos="Kategori seçin", ara="Kategori ara", zorunlu_metin="Ana kategori seçin",
                 bos_metin="Bu adla kategori yok.")


def tarih_sec(tid, deger, ek=""):
    return (f'<div class="kb-tarih-sec" id="{tid}" data-deger="{e(deger)}"{ek}>'
            f'<button type="button" class="kb-tarih-btn" data-acilir="{tid}Menu" aria-expanded="false" aria-haspopup="dialog">{ikon("fa-calendar-days")}<span class="kt-deger"></span></button>'
            f'<div class="pnl-menu kb-tarih-menu" id="{tid}Menu" role="dialog" aria-label="Tarih ve saat seç"></div></div>')


def toggle(baslik, alt, acik=True, ek=""):
    return (f'<div class="toggle-row"{ek}><span>{baslik}<small>{alt}</small></span><label class="toggle"><input type="checkbox"{" checked" if acik else ""} aria-label="{e(re.sub("<[^>]+>", "", baslik))}">'
            f'<span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>')


def girdi(fid, etiket, deger="", alan_id=None, alan=None, sayac=None, not_=None, hata=None, buyuk=False, ph="", ek=""):
    nit = (f' data-alan-id="{alan_id}"' if alan_id else "") + (f' data-alan="{alan}"' if alan else "") + (f' data-sayac="{sayac}"' if sayac else "")
    if hata:
        nit += f' data-zorunlu-metin="{e(hata)}"'
    cls = "finput kb-buyuk" if buyuk else "finput"
    p = f' placeholder="{e(ph)}"' if ph else ""
    sayacm = f'<div class="char-meter"><span>{not_ or ""}</span><b>0 / {sayac.split("|")[0]}</b></div>' if sayac else (f'<span class="fhint">{not_}</span>' if not_ else "")
    return f'<div class="frow"{ek}><label for="{fid}">{etiket}</label><input class="{cls}" id="{fid}"{nit}{p} value="{e(deger)}">{sayacm}</div>'


def metin_alani(fid, etiket, deger="", alan_id=None, alan=None, sayac=None, not_=None, hata=None, satir=3, ph=""):
    nit = (f' data-alan-id="{alan_id}"' if alan_id else "") + (f' data-alan="{alan}"' if alan else "") + (f' data-sayac="{sayac}"' if sayac else "")
    if hata:
        nit += f' data-zorunlu-metin="{e(hata)}"'
    p = f' placeholder="{e(ph)}"' if ph else ""
    sayacm = f'<div class="char-meter"><span>{not_ or ""}</span><b>0 / {sayac.split("|")[0]}</b></div>' if sayac else (f'<span class="fhint">{not_}</span>' if not_ else "")
    return f'<div class="frow"><label for="{fid}">{etiket}</label><textarea class="ftext" id="{fid}"{nit} rows="{satir}"{p}>{e(deger)}</textarea>{sayacm}</div>'


def editor(ad, govde, alt_not, alan_id=None, hata=None, medya=False, ai_grup=None, baslik=None, ikon_ad="fa-align-left", fs_ek=""):
    nit = (f' data-alan-id="{alan_id}"' if alan_id else "") + (f' data-zorunlu-metin="{e(hata)}"' if hata else "")
    ag = f' data-ai-grup="{ai_grup}"' if ai_grup else ""
    md = " data-editor-medya" if medya else ""
    ek = f'<span class="fs-ek">{fs_ek}</span>' if fs_ek else ""
    return (f'<div class="form-sec"{ag}><div class="form-sec-tt">{ikon(ikon_ad)}{baslik or ad}{ek}</div>'
            f'<div class="kb-editor" data-editor-ad="{e(ad)}"{md}><div class="kz-alan ke-alan"{nit}>{govde}</div>'
            f'<div class="kz-alt"><span data-kz-say></span><span>{alt_not}</span></div></div></div>')


def dil_bas(not_):
    return ('<div class="kb-form-bas"><div class="kb-dil" role="group" aria-label="İçerik dili">'
            '<button type="button" class="is-on" aria-pressed="true">TR · Türkçe</button>'
            + "".join(f'<button type="button" disabled title="Çeviri ekranları sonraki aşamada">{d}<span class="kd-etk">Sonraki aşama</span></button>' for d in ("EN", "AR", "DE"))
            + f'</div><span class="kfb-not">{ikon("fa-language")}{not_}</span></div>')


def kap_dil():
    """Çekmece ve penceredeki formun en üstündeki dil seçici (Kategori formu kalıbı)."""
    return ('<div class="kb-form-bas kb-kap-dil"><div class="kb-dil" role="group" aria-label="İçerik dili"><button type="button" class="is-on" aria-pressed="true">TR · Türkçe</button>'
            + "".join(f'<button type="button" disabled title="Çeviri ekranları sonraki aşamada">{d}<span class="kd-etk">Sonraki aşama</span></button>' for d in ("EN", "AR", "DE")) + "</div></div>")


def form_sekmeler(liste):
    out = '<div class="sa-form-tabs" role="tablist" aria-label="Düzenleme sekmeleri">'
    for i, (pid, ik, ad, modul) in enumerate(liste):
        m = f' data-modul="{modul}"' if modul else ""
        on = " is-on" if i == 0 else ""
        out += f'<button type="button" class="sa-form-tab{on}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-panel="{pid}"{m}>{ikon(ik)}{ad}</button>'
    return out + "</div>"


def ai_adim(kaynak, secenekler, durum):
    sec = "".join(
        f'<label class="kb-secenek"{f" data-modul=\"{m}\"" if m else ""}><input type="checkbox" value="{v}"{" checked" if c else ""}>{a}</label>'
        for v, a, c, m in secenekler)
    return (f'<div class="kb-ai-adim" data-ai-adim data-ai-kaynak="{kaynak}" data-yeni-goster hidden>'
            f'<div class="kaa-bas"><span class="kaa-ikon">{ikon("fa-wand-magic-sparkles")}</span><div><b>Gerisini AI ile üret</b><span data-ai-durum>{durum}</span></div></div>'
            f'<div class="kaa-secim" role="group" aria-label="Üretilecek bölümler">{sec}</div>'
            f'<div class="kaa-alt"><button type="button" class="btn btn-acc btn-sm" data-ai-uret disabled>{ikon("fa-wand-magic-sparkles")}Gerisini Üret</button><span class="fhint" data-ai-neden>Önce başlık ve spot</span></div></div>')


ORAN_SINIF = {"16:9": "r-16x9", "4:3": "r-4x3", "3:4": "r-3x4", "1:1": "r-1x1", "9:16": "r-9x16", "2:1": "r-2x1", "16:10": "r-kart", "2.4:1": "r-detay"}


def kutu(hedef, kirp, etk, oran, img, odak=(50, 40), odak_isareti=False, genislik=None):
    """Görsel kutusu: oran sınıfı kayıttaki orandan (.kg-resim.r-16x9 …); satır içi stil yalnız görsel ve odak (veri)."""
    bg = f"background-image:url(../../veri/gorsel/{img});background-position:{odak[0]}% {odak[1]}%"
    od = f'<span class="kg-odak" style="left:{odak[0]}%;top:{odak[1]}%"></span>' if odak_isareti else ""
    return f'<div class="kg-resim {ORAN_SINIF[oran]}" data-gorsel-hedef="{hedef}" data-kirp-oran="{kirp}" style="{bg}">{od}<span class="kg-etk">{etk}</span></div>'


def gorsel_alan(sid, alan, ad, img, web, mobil, olcu_web, olcu_mobil, en_az, kaynak="", alan_id="kapak", hata="Kapak görseli yükleyin ya da havuzdan seçin",
                odak=(50, 40), ek_alt="", baslik=None, sec_ek="", alt_yazi=None, yeni=True, kayit=None):
    """Görsel alanı (web + mobil). web: [(kirp, etk, oran, genislik)], mobil: (kirp, etk, oran, genislik)."""
    aid = f' data-alan-id="{alan_id}" data-zorunlu-metin="{e(hata)}"' if alan_id else ""
    ki = f' data-kayit-icin="{kayit}"' if kayit else ""
    ws = "".join(kutu("web", k, et, o, img, odak, i == 0, g) for i, (k, et, o, g) in enumerate(web))
    web_html = f'<div class="kg-ikili">{ws}</div>' if len(web) > 1 else ws
    mk, met, mo, mg = mobil
    yeni_g = ' data-yeni-goster' if yeni else ""
    yeni_h = ' data-yeni-gizle' if yeni else ""
    bos_hidden = " hidden" if yeni else " hidden"
    alt = ""
    if alt_yazi:
        alt = (f'<div class="frow kb-ust-bosluk"><label for="{sid}Alt">Görsel Altyazısı ve Kaynağı</label>'
               f'<input class="finput" id="{sid}Alt" data-sayac="120|160" value="{e(alt_yazi)}">'
               f'<div class="char-meter"><span>Görselin altında ve erişilebilirlik metninde</span><b>0 / 120</b></div></div>')
    ks = f'<span class="fs-ek"{yeni_h}>{kaynak}</span>' if kaynak else ""
    return f"""      <div class="form-sec" id="{sid}"{aid}{ki} data-gorsel-alan="{alan}" data-gorsel-ad="{e(ad)}" data-kirp-sonra{sec_ek}>
        <div class="form-sec-tt">{ikon("fa-image")}{baslik or ad}{ks}</div>
        <div class="kb-yukle"{yeni_g} data-gorsel-bos{bos_hidden}>{ikon("fa-cloud-arrow-up")}<b>{e(ad)} görselini sürükleyin ya da seçin</b><span>Web görseli yüklenince mobil görsel ondan otomatik kırpılır · önerilen en az {en_az}</span><span class="kg-acts"><button type="button" class="btn btn-acc btn-sm" data-gorsel-yukle>{ikon("fa-upload")}Bilgisayardan Yükle</button><button type="button" class="btn btn-ghost btn-sm" data-medya-sec>{ikon("fa-photo-film")}Havuzdan Seç</button></span></div>
        <div class="kb-gorsel"{yeni_h} data-gorsel-dolu>
          <div class="kg-bolum">
            <div class="kg-bas">{ikon("fa-desktop")}Web</div>
            {web_html}
            <div class="kg-olcu">Önerilen: {olcu_web} (sitenin görünen genişliği). <span data-gorsel-bilgi>Yüklenen: 1200×800 JPG, 214 KB.</span></div>
            <div class="kg-acts">
              <button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{ikon("fa-crop-simple")}Kırp ve Odak</button>
              <button type="button" class="btn btn-ghost btn-sm" data-medya-sec>{ikon("fa-photo-film")}Havuzdan Seç</button>
              <button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle>{ikon("fa-upload")}Yükle</button>
              <button type="button" class="btn btn-ghost btn-sm danger" data-gorsel-kaldir>{ikon("fa-trash")}Kaldır</button>
            </div>
          </div>
          <div class="kg-bolum">
            <div class="kg-bas">{ikon("fa-mobile-screen")}Mobil<span class="kg-oto">{ikon("fa-wand-magic-sparkles")} Webden kırpıldı</span></div>
            {kutu("mobil", mk, met, mo, img, odak, True, mg)}
            <div class="kg-olcu">Önerilen: {olcu_mobil} (sitenin telefon görünümü). Aynı odak noktası kullanılır.{ek_alt}</div>
            <div class="kg-acts">
              <button type="button" class="btn btn-ghost btn-sm" data-kirp-ac="{mk}">{ikon("fa-crop-simple")}Kırp</button>
              <button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle data-gorsel-kapsam="mobil">{ikon("fa-upload")}Ayrı Görsel Yükle</button>
              <button type="button" class="btn btn-ghost btn-sm" data-gorsel-webe-don hidden>{ikon("fa-rotate-left")}Webden Kırpılana Dön</button>
            </div>
          </div>
        </div>{alt}
      </div>
"""


def dosya_alan(tur, ad, alan_id, dosya=None, hata=None, sinir=None, kabul=None, coklu=False, yeni=True, ek=""):
    """Dosya yükleme (kb-dosya). Yeni kayıtta boş hali görünür, dolu hali gizlenir (aynı alan id'si; gizli olan aranmaz)."""
    nit = f' data-alan-id="{alan_id}"' if alan_id else ""
    if hata:
        nit += f' data-zorunlu-metin="{e(hata)}"'
    if sinir:
        nit += f' data-sinir="{sinir}"'
    if kabul:
        nit += f' data-kabul="{kabul}"'
    if coklu:
        nit += " data-coklu"
    if dosya:
        o = f'<div class="kb-dosya-oge" data-ad="{e(dosya[0])}" data-boyut="{dosya[1]}"' + (f' data-sure="{dosya[2]}"' if len(dosya) > 2 and dosya[2] else "") + "></div>"
        dolu = f'<div{" data-yeni-gizle" if yeni else ""}{ek}><div class="kb-dosya" data-tur="{tur}" data-ad="{e(ad)}"{nit}>{o}</div></div>'
        bos = f'<div data-yeni-goster hidden{ek}><div class="kb-dosya" data-tur="{tur}" data-ad="{e(ad)}"{nit}></div></div>' if yeni else ""
        return dolu + bos
    return f'<div{ek}><div class="kb-dosya" data-tur="{tur}" data-ad="{e(ad)}"{nit}></div></div>'


def seo_panel(pid, baslik, aciklama, pre, slug, kelimeler, ek_toggle=""):
    cip = "".join(f'<span class="kb-cip" data-deger="{e(k)}"><span>{e(k)}</span><button type="button" aria-label="Kaldır">{ikon("fa-xmark")}</button></span>' for k in kelimeler)
    yol = pre.replace("dadahaber.com/", "").strip("/").replace("/", " › ")
    return f"""    <div class="sa-form-panel" id="{pid}" role="tabpanel" data-ai-grup="seo" hidden>
      <div class="form-sec">
        <div class="form-sec-tt">{ikon("fa-wand-magic-sparkles")}Otomatik Üretildi<span class="fs-ek"><button type="button" class="btn btn-ghost btn-sm" data-seo-uret>{ikon("fa-rotate")}Başlıktan Yeniden Üret</button></span></div>
        <div class="form-grid">
          <div class="frow"><label for="{pid}B">SEO Başlığı</label>
            <input class="finput" id="{pid}B" data-alan="seo-baslik" data-sayac="60|70" value="{e(baslik)}">
            <div class="char-meter"><span>Arama sonucunda görünen başlık · 50–60 karakter önerilir</span><b>0 / 60</b></div></div>
          <div class="frow"><label for="{pid}A">SEO Açıklaması</label>
            <textarea class="ftext" id="{pid}A" data-alan="seo-aciklama" data-sayac="155|170">{e(aciklama)}</textarea>
            <div class="char-meter"><span>Arama sonucunda başlığın altında · 120–155 karakter önerilir</span><b>0 / 155</b></div></div>
          <div class="frow"><label for="{pid}S">Adres</label>
            <div class="slug-wrap"><span class="slug-pre">{pre}</span><input class="finput" id="{pid}S" data-alan="slug" value="{e(slug)}"></div>
            <span class="fhint">Başlıktan kendiliğinden üretilir. Yayımlandıktan sonra değiştirilirse eski adres yeniye yönlendirilir.</span></div>
          <div class="frow"><span class="flabel">Anahtar Kelimeler</span>
            <div class="kb-cip-girdi" data-serbest>{cip}<input type="text" placeholder="Yazın; Enter ya da virgülle ekleyin" aria-label="Anahtar kelime ekle"><div class="pnl-menu kb-cip-oneri"></div></div></div>
          <div class="frow"><span class="flabel">Arama Sonucu Önizlemesi</span>
            <div class="serp"><div class="serp-url"><span class="serp-fav kb-logo-isaret"></span><span>dadahaber.com › {e(yol)} › <span data-alan="slug">{e(slug)}</span></span></div>
              <div class="serp-title" data-alan="seo-baslik">{e(baslik)}</div>
              <div class="serp-desc" data-alan="seo-aciklama">{e(aciklama)}</div></div></div>
          {ek_toggle}
        </div>
      </div>
    </div>
"""


def bildirim_panel(pid, baslik, metin, gorsel_not, saat="2026-11-24 18.30"):
    return f"""    <div class="sa-form-panel" id="{pid}" role="tabpanel" data-ai-grup="bildirim" data-modul="etkilesim" hidden>
      <div class="form-sec">
        <div class="form-grid">
          <div class="frow"><span class="flabel">Kanallar</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="checkbox" checked>Telefon Bildirimi</label><label class="kb-secenek"><input type="checkbox" checked>Web Bildirimi</label></div>
            <span class="fhint">Bildirim bütün abonelere gider. Mobil uygulama gelene kadar telefon bildirimi web üzerinden gider.</span></div>
          <div class="frow"><label for="{pid}B">Bildirim Başlığı</label>
            <input class="finput" id="{pid}B" data-alan="push-baslik" data-sayac="60|65" value="{e(baslik)}">
            <div class="kb-cubuk"><span></span></div>
            <div class="char-meter"><span>Telefonda kalın satır · 60 karaktere kadar tam görünür</span><b>0 / 60</b></div></div>
          <div class="frow"><label for="{pid}M">Bildirim Metni</label>
            <textarea class="ftext" id="{pid}M" data-alan="push-metin" data-sayac="150|178">{e(metin)}</textarea>
            <div class="kb-cubuk"><span></span></div>
            <div class="char-meter"><span>Kilit ekranında 3 satıra kadar · 150 karakter önerilir</span><b>0 / 150</b></div></div>
          {toggle("Bildirim Görseli", gorsel_not)}
          <div class="frow"><span class="flabel">Ne Zaman</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="{pid}Z" checked>Kaydedince Hemen</label><label class="kb-secenek"><input type="radio" name="{pid}Z" data-ac="{pid}ZS">Zamanla</label><label class="kb-secenek"><input type="radio" name="{pid}Z">Bildirim Gönderme</label></div>
            <div id="{pid}ZS" hidden>{tarih_sec(pid + "T", saat, ' data-enaz="bugun"')}</div></div>
        </div>
      </div>
    </div>
"""


def bildirim_onizle(pid, baslik, metin, img):
    return f"""    <div class="kb-yan-onizle" data-panel-icin="{pid}" data-modul="etkilesim" hidden>
      <section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{ikon("fa-mobile-screen")}Bildirim Önizlemesi</h2></div>
      <div class="pc-body"><div class="kb-onizle-kap">
        <div class="kb-onizle-sec" data-segment><button type="button" class="is-on" data-hedef="{pid}Tel" aria-pressed="true">Telefon</button><button type="button" data-hedef="{pid}Web" aria-pressed="false">Web</button></div>
        <div id="{pid}Tel"><div class="kb-telefon"><div class="kb-telefon-ekran"><div class="kt-zaman">16.05</div><div class="kt-tarih">24 Kasım Salı</div>
          <div class="kb-push"><span class="kp-ikon kb-logo-isaret"></span><div class="kp-ic"><div class="kp-ust"><span>DADA HABER</span><span>şimdi</span></div><b data-alan="push-baslik">{e(baslik)}</b><p data-alan="push-metin">{e(metin)}</p></div>{f'<span class="kp-resim" style="background-image:url(../../veri/gorsel/kucuk/{img})"></span>' if img else ""}</div>
        </div></div></div>
        <div id="{pid}Web" hidden><div class="kb-web-push"><span class="kp-ikon kb-logo-isaret"></span><div><b data-alan="push-baslik">{e(baslik)}</b><p data-alan="push-metin">{e(metin)}</p><small>dadahaber.com · Chrome</small></div></div></div>
        <p class="kb-onizle-not">Önizleme yaklaşıktır; telefonun ve tarayıcının görünümüne göre değişir.</p>
      </div></div></section>
    </div>
"""


PLATFORM = {
    "x": ("fa-x-twitter", "X", "Dada Haber", "@dadahaber", 280, "16:9=1200×675,1:1=1080×1080,serbest", "ok", ' data-link-uzunluk="23"'),
    "facebook": ("fa-facebook", "Facebook", "Dada Haber", "Facebook sayfası", 2000, "1.91:1=1200×630,1:1=1080×1080,serbest", "ok", ""),
    "linkedin": ("fa-linkedin", "LinkedIn", "Dada Haber", "Medya · 12.400 takipçi", 3000, "1.91:1=1200×627,1:1=1200×1200,serbest", "ok", ""),
    "instagram": ("fa-instagram", "Instagram", "dadahaber", "İstanbul", 2200, "1:1=1080×1080,4:5=1080×1350,serbest", "hata", ""),
    "telegram": ("fa-telegram", "Telegram", "Dada Haber", "kanal · 48.200 abone", 4096, "16:9=1280×720,1:1=1080×1080,serbest", "ok", ""),
}


def sosyal_panel(pid, metinler, img, kirp_alan, odak=(50, 40), ust_not=""):
    """Sosyal Medya sekmesi (haber düzenle ile aynı). metinler: {platform: metin}."""
    pl = ""
    for i, (k, metin) in enumerate(metinler.items()):
        ik, ad, hesap, tutamac, sinir, oranlar, durum, ek = PLATFORM[k]
        pl += (f'<button type="button" class="kb-platform{" is-on" if i == 0 else ""}" role="tab" data-platform="{k}" data-ad="{e(hesap)}" data-tutamac="{e(tutamac)}" data-sinir="{sinir}"{ek} data-hesap-durum="{durum}" data-oranlar="{oranlar}" data-metin="{e(metin)}">'
               f'{ikon(ik, "fa-brands")}{ad}<span class="kp-durum{" hata" if durum == "hata" else ""}"></span></button>')
    bg = f"background-image:url(../../veri/gorsel/{img})"
    un = f'<div class="kb-bant bilgi">{ikon("fa-circle-info")}<span>{ust_not}</span></div>' if ust_not else ""
    return f"""    <div class="sa-form-panel" id="{pid}" role="tabpanel" data-ai-grup="sosyal" data-modul="sosyal-medya" hidden>
      <div class="form-sec kb-sosyal">{un}
        <div class="kb-platformlar" role="tablist" aria-label="Platformlar">{pl}</div>
        <div class="kb-ust-bosluk"><div class="form-grid">
          <div class="kb-hesap-kutu"><span class="kh-ava kb-logo-isaret"></span><div><b data-sosyal-ad>Dada Haber</b><span data-sosyal-tutamac>@dadahaber</span></div><span class="pstat ok" data-sosyal-hesap>Bağlı</span></div>
          <div class="frow" data-sosyal-uyari hidden><div class="kb-hata-not">{ikon("fa-triangle-exclamation")}Instagram bağlantısının süresi doldu. Gönderi hazırlanabilir ama hesap yeniden bağlanana kadar yayımlanmaz.<a data-hedef="sosyal-medya.hesaplar" href="#icerik">Hesabı Bağla</a></div></div>
          <div class="frow"><label for="{pid}M">Gönderi Metni<button type="button" class="btn btn-ghost btn-sm kb-sag" data-sosyal-uret>{ikon("fa-wand-magic-sparkles")}Yeniden Üret</button></label>
            <div class="kb-sosyal-kutu"><div class="kb-sosyal-arac" role="toolbar" aria-label="Gönderi metni biçimi" data-sosyal-arac></div><textarea class="ftext" id="{pid}M" data-sosyal-metin data-oneri rows="7"></textarea></div>
            <div class="kb-cubuk"><span></span></div>
            <div class="char-meter kb-sosyal-say"><span class="kb-sayaclar"></span><b>0 / 280</b></div>
            <p class="fhint kb-sa-not" data-sosyal-not></p></div>
          <div class="kb-sosyal-ek" data-sosyal-ek hidden>
            <div class="frow" data-sosyal-ek-alan="konum"><label for="{pid}K">Konum</label><input class="finput" id="{pid}K" data-oneri="konum" placeholder="Konum ara: İstanbul, Ankara…" autocomplete="off"><span class="fhint">Platformun kendi konum etiketi; gönderinin üstünde görünür</span></div>
            <div class="frow" data-sosyal-ek-alan="gorselde-etiket"><label for="{pid}E">Görselde Etiketlenecek Hesaplar</label><input class="finput" id="{pid}E" data-oneri placeholder="@ yazın: hesap ara" autocomplete="off"><span class="fhint">Instagram'ın "kişileri etiketle" özelliği; hesap görselin üstünde etiket olarak görünür</span></div>
          </div>
          <div class="frow"><span class="flabel">Görsel Oranı<span class="fhint kb-sag" data-oran-not></span></span>
            <div class="kb-oranlar"></div>
            <div class="kb-kirp-alan"><span class="kk-resim" style="{bg}"></span><span class="kk-cerceve" data-kirp-izle="sosyal.16:9" style="{bg};background-position:{odak[0]}% {odak[1]}%"></span></div>
            <span class="fhint">Kapak görselinin odak noktasına göre otomatik kırpıldı. <button type="button" class="kb-bag" data-kirp-ac="sosyal.16:9" data-kirp-alan="{kirp_alan}">Kırpmayı Düzenle</button></span></div>
          <div class="frow"><span class="flabel">Yayın</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="{pid}Z" checked>Kaydedince Hemen</label><label class="kb-secenek"><input type="radio" name="{pid}Z" data-ac="{pid}ZS">Zamanla</label><label class="kb-secenek"><input type="radio" name="{pid}Z">Bu Platformda Paylaşma</label></div>
            <div id="{pid}ZS" hidden>{tarih_sec(pid + "T", "2026-11-24 17.00", ' data-enaz="bugun"')}</div></div>
        </div></div>
      </div>
    </div>
"""


def sosyal_onizle(pid, img, kart_alt, odak=(50, 40)):
    return f"""    <div class="kb-yan-onizle" data-panel-icin="{pid}" data-modul="sosyal-medya" hidden>
      <section class="pnl-card"><div class="pc-head"><h2 class="pc-title">{ikon("fa-eye")}Canlı Önizleme</h2><span class="kb-kap-alt" data-sosyal-ad-platform></span></div>
      <div class="pc-body"><div class="kb-onizle-kap">
        <div class="kb-sosyal-kart p-x" data-sosyal-onizle><div class="ksk-tg">
          <div class="ksk-bas"><span class="kh-ava kb-logo-isaret"></span><div><b><span data-sosyal-ad>Dada Haber</span>{ikon("fa-circle-check")}</b><span data-sosyal-tutamac>@dadahaber</span> · 1 dk</div>{ikon("fa-ellipsis ksk-noktalar")}</div>
          <div class="ksk-metin"></div>
          <div class="ksk-gorsel" style="background-image:url(../../veri/gorsel/{img});background-position:{odak[0]}% {odak[1]}%"></div>
          <div class="ksk-kart-alt">dadahaber.com · {e(kart_alt)}</div>
          <div class="ksk-eylem">{ikon("fa-comment", "fa-regular")}{ikon("fa-retweet")}{ikon("fa-heart", "fa-regular")}{ikon("fa-chart-simple")}{ikon("fa-bookmark", "fa-regular")}</div>
        </div></div>
        <p class="kb-onizle-not">Platformun gerçek görünümüne yakındır</p>
      </div></div></section>
    </div>
"""


def durum_secim(sid, deger, ops, yeni="taslak"):
    sec = "".join(f'<button type="button" data-deger="{d}" data-ad="{e(a)}"{" class=\"is-sec\"" if d == deger else ""}>{e(a)}{f"<span class=\"ks-alt\">{e(alt)}</span>" if alt else ""}</button>' for d, a, alt in ops)
    gost = next(a for d, a, _ in ops if d == deger)
    return (f'<div class="kb-secim is-dolu" data-deger="{deger}" data-bos="Taslak" data-yeni-deger="{yeni}"><button type="button" class="kb-secim-btn" data-acilir="{sid}" aria-expanded="false" aria-haspopup="listbox" aria-label="Durum"><span class="ks-deger">{e(gost)}</span>{ikon("fa-chevron-down")}</button>'
            f'<div class="pnl-menu kb-secim-menu" id="{sid}"><div class="kb-secim-liste" role="listbox">{sec}</div></div></div>')


YAYIN_DURUM = [("yayinda", "Yayında", ""), ("taslak", "Taslak", "yayından kalkar"), ("zamanli", "Zamanlanmış", "")]


def yayin_kart(durum_html, yayin_zamani, ek="", surum=None, durum_state="yayinda"):
    sur = f'<div class="kb-surum" data-yeni-gizle><span><b>Sürüm {surum[0]}</b> · son değişiklik {surum[1]} · {surum[2]}</span><button type="button" class="kb-bag" data-bildir-surum>Sürüm Geçmişi</button></div>' if surum else ""
    return f"""    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{ikon("fa-paper-plane")}Yayın</h2><span class="status-dot" data-state="{durum_state}" data-yeni-durum="taslak" title="Yayında"></span></div>
      <div class="pc-body sc-stack">
        <div class="sc-field"><span class="flabel">Durum</span>{durum_html}</div>
        <div class="sc-field"><span class="flabel">Yayın Zamanı</span>{tarih_sec("ycTarih", yayin_zamani, ' data-yeni-bos data-bos="Yayımlanınca o anın saati" data-temizlenir="1"')}</div>
        {ek}
        {sur}
      </div>
    </section>
"""


def seo_kart(skor, kontroller):
    ch = "".join(f'<div class="seo-chk {"pass" if ok else "fail"}">{ikon("fa-circle-check") if ok else ikon("fa-circle", "fa-regular")}{e(m)}</div>' for ok, m in kontroller)
    etk = "İyi" if skor >= 80 else "Orta"
    return f"""    <section class="pnl-card" data-one-cik="pSeo">
      <div class="pc-head"><h2 class="pc-title">{ikon("fa-gauge")}SEO Skoru</h2></div>
      <div class="pc-body">
        <p class="fhint" data-yeni-goster hidden>Skor, başlık, açıklama ve görsel girilince hesaplanır.</p>
        <div class="seo-score" data-yeni-gizle><div class="score-ring" style="--p:{skor}"><span class="score-num">{skor}</span></div><div class="score-meta"><b>{etk}</b><span>Eksikler giderilince yükselir</span></div></div>
        <div class="seo-checks" data-yeni-gizle>{ch}</div>
      </div>
    </section>
"""


def kaydet_cubugu(form_id, durum, bildir, yeni_bildir, taslak_bildir="Taslak kaydedildi; yayındaki hal değişmedi", ana="Güncelle", ana_yeni="Yayımla", ek=""):
    return f"""  <div class="kb-kaydet" data-form-icin="{form_id}">
    <div class="kk-durum">{ikon("fa-circle-check")}<span data-yeni-metin="Henüz kaydedilmedi">{durum}</span></div>
    <div class="kk-sag">
      <button type="button" class="btn btn-ghost btn-sm" data-kaydet data-kaydet-tur="taslak" data-kaydet-metin="Taslak olarak kaydedildi" data-bildir="{e(taslak_bildir)}">{ikon("fa-floppy-disk")}Taslak Kaydet</button>
      <button type="button" class="btn btn-acc btn-sm" data-kaydet data-kaydet-metin="Güncellendi" data-bildir="{e(bildir)}" data-yeni-bildir="{e(yeni_bildir)}"{ek}>{ikon("fa-check")}<span data-yeni-metin="{ana_yeni}">{ana}</span></button>
    </div>
  </div>
"""


# =====================================================================
# liste ekranı parçaları (Haberler listesi kalıbı)
# =====================================================================
def eylemler(gor_href=None, gor_site=False, gor_tanim=None, duz_href=None, duz_tanim=None, sil=' data-sil', ad=""):
    a = f": {e(ad)}" if ad else ""
    if gor_tanim:
        g = f'<button type="button" class="ia-btn" data-tanim="{gor_tanim}" aria-label="Görüntüle{a}" title="Görüntüle">{ikon("fa-eye")}</button>'
    elif gor_site:
        g = f'<a class="ia-btn" href="{e(gor_href)}" target="_blank" rel="noopener" aria-label="Sitede Görüntüle{a}" title="Sitede Görüntüle">{ikon("fa-eye")}</a>'
    else:
        g = f'<a class="ia-btn" href="{e(gor_href)}" aria-label="Önizle{a}" title="Önizle">{ikon("fa-eye")}</a>'
    if duz_tanim:
        d = f'<button type="button" class="ia-btn" data-tanim="{duz_tanim}" aria-label="Düzenle{a}" title="Düzenle">{ikon("fa-pen")}</button>'
    else:
        d = f'<a class="ia-btn" href="{e(duz_href)}" aria-label="Düzenle{a}" title="Düzenle">{ikon("fa-pen")}</a>'
    s = f'<button type="button" class="ia-btn danger"{sil} aria-label="Çöpe Taşı{a}" title="Çöpe Taşı">{ikon("fa-trash")}</button>'
    m = f'<button type="button" class="ia-btn" data-diger aria-haspopup="true" aria-expanded="false" aria-label="Diğer işlemler{a}" title="Diğer">{ikon("fa-ellipsis")}</button>'
    return f'<div class="row-acts">{g}{d}{s}{m}</div>'


def satir(nit, hucreler, acts, secim=True):
    n = " ".join(f'data-{k}="{e(v)}"' for k, v in nit.items() if v is not None)
    kutu_ = f'<td class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(nit.get("baslik", ""))}"></td>' if secim else ""
    return f"<tr {n}>{kutu_}{''.join(hucreler)}<td>{acts}</td></tr>"


def ana_hucre(baslik, alt, img=None, yok=False, kare=False):
    if img:
        th = f'<span class="rcp-thumb" style="background-image:url(../../veri/gorsel/kucuk/{img})"></span>'
    elif yok:
        th = f'<span class="rcp-thumb kb-yok" title="Görsel eksik">{ikon("fa-image")}</span>'
    else:
        th = ""
    return f'<td class="kb-ana"><div class="rcp-cell">{th}<div class="rcp-id"><div class="rcp-name" title="{e(baslik)}">{e(baslik)}</div><div class="rcp-by">{alt}</div></div></div></td>'


def kat_hucre(ana, alt=None):
    a = f'{ikon("fa-chevron-right")}{e(alt)}' if alt and alt != ana else ""
    return f'<td class="kb-gizle-m"><span class="kb-kat"><b>{e(ana)}</b>{a}</span></td>'


DURUM = {"yayinda": ("ok", "Yayında"), "taslak": ("off", "Taslak"), "zamanli": ("info", "Zamanlanmış"), "cop": ("warm", "Çöpte"),
         "canli": ("warm", "Canlı"), "planli": ("info", "Planlandı"), "bitti": ("off", "Sona Erdi"), "hazirlaniyor": ("wait", "Seslendiriliyor")}


def durum_hucre(d):
    c, a = DURUM[d]
    return f'<td><span class="pstat {c}">{a}</span></td>'


def liste(lid, ad, aria, sekmeler, ara_ph, suzler, toplu, kolonlar, satirlar, bos, hata_metin, diger, dosya, toplam=None, sayfa_boy=25, cop_not=None, cop=True, secimli=True, ust_ek=""):
    ch = ""
    for i, (s, a, taban) in enumerate(sekmeler):
        t = f' data-taban="{taban}"' if taban else ""
        ch += f'<button type="button" class="chip{" is-on" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-sekme="{s}"{t}>{a}<span class="ch-cnt">0</span></button>'
    copb = f'<button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{ikon("fa-trash")}Çöp<span class="ch-cnt">0</span></button>' if cop else ""
    kol = (f'<th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün kayıtları seç"></th>' if secimli else "")
    kol += "".join(f'<th{f" class=\"{c}\"" if c else ""}>{b}</th>' for b, c in kolonlar) + '<th><span class="sr-only">İşlemler</span></th>'
    n = len(kolonlar) + 1 + (1 if secimli else 0)
    isk_h = "".join("<td></td>" if i in (0, n - 1) else ('<td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td>' if i == (1 if secimli else 0) else "<td><span></span></td>") for i in range(n))
    isk = "".join(f'<tr class="kb-iskelet">{isk_h}</tr>' for _ in range(4))
    cn = f' data-liste-cop-not="{e(cop_not)}"' if cop_not else ""
    pager_btn = ""
    if toplam and toplam > sayfa_boy:
        son_s = -(-toplam // sayfa_boy)
        pager_btn = (f'<div class="pager-btns"><button type="button" class="pg-btn" disabled aria-label="Önceki sayfa">{ikon("fa-chevron-left")}</button>'
                     f'<button type="button" class="pg-btn is-on" aria-current="page">1</button>'
                     + "".join(f'<button type="button" class="pg-btn pg-sayi" data-bildir-pg>{k}</button>' for k in range(2, min(son_s, 3) + 1))
                     + (f'<span class="pg-dots pg-sayi">…</span><button type="button" class="pg-btn pg-sayi" data-bildir-pg>{son_s}</button>' if son_s > 3 else "")
                     + f'<button type="button" class="pg-btn" data-bildir-pg aria-label="Sonraki sayfa">{ikon("fa-chevron-right")}</button></div>')
    else:
        pager_btn = (f'<div class="pager-btns" hidden><button type="button" class="pg-btn" disabled aria-label="Önceki sayfa">{ikon("fa-chevron-left")}</button>'
                     f'<button type="button" class="pg-btn is-on" aria-current="page">1</button><button type="button" class="pg-btn" disabled aria-label="Sonraki sayfa">{ikon("fa-chevron-right")}</button></div>')
    bik, bh2, bp, byeni = bos
    toplu_html = (f'<div class="kb-toplu" hidden><b data-secili-say>0 {ad} seçildi</b><span class="kb-toplu-ayir"></span>{toplu}'
                  f'<button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{ikon("fa-trash")}<span>Çöpe Taşı</span></button>'
                  f'<button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi Temizle</button></div>') if secimli else ""
    return f"""  <section class="pnl-card" data-liste data-liste-ad="{ad}"{cn} data-sayfa-boy="{sayfa_boy}" aria-labelledby="{lid}Bas">
    <h2 class="sr-only" id="{lid}Bas">{aria}</h2>{ust_ek}
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Duruma göre">{ch}</div>
      {copb}
    </div>
    <div class="filter-bar">
      <div class="fb-search">{ikon("fa-magnifying-glass")}<label class="sr-only" for="{lid}Ara">{bb(aria + " içinde ara")}</label><input id="{lid}Ara" type="search" data-liste-ara placeholder="{e(ara_ph)}" autocomplete="off"></div>
      {suzler}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
    </div>
    {toplu_html}
    <div class="ptable-wrap">
      <table class="ptable">
        <thead><tr>{kol}</tr></thead>
        <tbody data-satirlar>{satirlar}</tbody>
        <tbody><tr class="kb-bos-satir" hidden><td colspan="{n}"><div class="pnl-empty"><div class="pe-ico">{ikon("fa-magnifying-glass")}</div><h2>Bu süzgeçlerle {ad} bulunamadı</h2><p>Arama metnini kısaltmayı ya da süzgeçleri kaldırmayı deneyin. Taslak ya da çöpte kayıt yoksa sekme boş görünür.</p><button type="button" class="pe-tag" data-suz-temizle>{ikon("fa-filter-circle-xmark")}Süzgeçleri Temizle</button></div></td></tr></tbody>
        <tbody data-durum-goster="yukleniyor" hidden>{isk}</tbody>
        <tbody data-durum-goster="hata" hidden><tr><td colspan="{n}"><div class="pnl-empty kb-hata"><div class="pe-ico">{ikon("fa-triangle-exclamation")}</div><h2>{hata_metin}</h2><p>Sunucuya ulaşılamadı. Sitedeki içerik etkilenmez; bağlantınızı kontrol edip yeniden deneyin, sorun sürerse sistem yöneticisine haber verin.</p><a class="pe-tag" href="{dosya}">{ikon("fa-rotate-right")}Yeniden Dene</a></div></td></tr></tbody>
        <tbody data-durum-goster="bos" hidden><tr><td colspan="{n}"><div class="pnl-empty"><div class="pe-ico">{ikon(bik)}</div><h2>{bh2}</h2><p>{bp}</p>{byeni}</div></td></tr></tbody>
      </table>
    </div>
    <div class="pager"><div class="pager-info">—</div>{pager_btn}</div>
    <div class="pnl-menu kb-diger-menu" role="menu">{diger}</div>
  </section>
"""


def dm_grup(ad, durumlar=None):
    d = f' data-durum-icin="{durumlar}"' if durumlar else ""
    return f'<div class="kb-dm-grup"{d}>{ad}</div>'


def dm_ayir(durumlar=None):
    d = f' data-durum-icin="{durumlar}"' if durumlar else ""
    return f'<div class="pmenu-div"{d}></div>'


def dm(metin, ik, durumlar=None, bildir=None, modul=None, roller=None, ek="", cls=None, disabled=False, pm_ek=None, hedef=None):
    nit = ""
    if cls:
        nit += f' class="{cls}"'
    if durumlar:
        nit += f' data-durum-icin="{durumlar}"'
    if modul:
        nit += f' data-modul="{modul}"'
    if roller:
        nit += f' data-roller="{roller}"'
    if bildir:
        nit += f' data-bildir="{e(bildir)}"'
    if disabled:
        nit += ' disabled title="Çeviri ekranları sonraki aşamada"'
    pe = f'<span class="pm-ek">{pm_ek}</span>' if pm_ek else ""
    if hedef:
        return f'<a data-hedef="{hedef}"{nit}{ek} href="#icerik">{ikon(ik)}{metin}{pe}</a>'
    return f'<button type="button"{nit}{ek}>{ikon(ik)}{metin}{pe}</button>'


def onay(baslik, metin, evet, ikon_ad, sonra=None, tehlike=False, kod=False, sonra_durum=None):
    s = f' data-onay-baslik="{e(baslik)}" data-onay-metin="{e(metin)}" data-onay-evet="{e(evet)}" data-onay-ikon="{ikon_ad}"'
    if tehlike:
        s += " data-onay-tehlike"
    if kod:
        s += " data-kod"
    if sonra:
        s += f' data-bildir-sonra="{e(sonra)}"'
    if sonra_durum:
        s += f' data-sonra-durum="{sonra_durum[0]}" data-sonra-durum-ad="{e(sonra_durum[1])}" data-sonra-durum-sinif="{sonra_durum[2]}"'
    return s


def dm_cop():
    return (dm_ayir("cop") + dm("Çöpten Geri Al", "fa-rotate-left", "cop", ek=" data-geri-al")
            + dm("Kalıcı Olarak Sil", "fa-trash-can", "cop", cls="danger", ek=" data-kalici-sil"))


def dm_kayit():
    return (dm_grup("Kayıt") + dm("Sürüm Geçmişi", "fa-clock-rotate-left", bildir="Sürüm geçmişi düzenleme ekranında açılır (prototip)")
            + dm("Denetim İzinde Gör", "fa-clipboard-list", roller="super gyy", hedef="denetim-izi.liste"))


def sayfa_sekmeler(liste_):
    """Sayfa düzeyinde tür sekmeleri: her sekmede kendi listesi (durum sekmeleri + Çöp). ?sekme=<id> ile açılır."""
    t = '<div class="sa-form-tabs" role="tablist" aria-label="Türe göre">'
    for i, (pid, ik, ad, sayi) in enumerate(liste_):
        t += (f'<button type="button" class="sa-form-tab{" is-on" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-panel="{pid}">'
              f'{ikon(ik)}{ad}<span class="ch-cnt">{sayi}</span></button>')
    return t + "</div>"


def kumele(s):
    return s.replace(".", "").replace(",", ".")


def sayi_tr(n):
    return f"{n:,}".replace(",", ".")


def yaz(dosya, icerik):
    (KLASOR / dosya).write_text(icerik, encoding="utf-8")
    print("yazıldı:", dosya)




# =====================================================================
# ortak menüler ve süzgeçler
# =====================================================================
def kat_suz(lid, sayilar=None):
    ops = [("", "Bütün Kategoriler")] + [(k, k, sayilar.get(k) if sayilar else None) for k in KATEGORILER if not sayilar or sayilar.get(k)]
    return secim(lid + "SuzKat", "", ops, suz="kategori", etk="Kategori:", ara="Kategori ara", bos_metin="Bu adla kategori yok.")


def yazar_suz(lid, adlar):
    ops = [("", "Bütün Kişiler")] + [(a, a) for a in sorted(set(adlar))]
    return secim(lid + "SuzYaz", "", ops, suz="yazar", etk="Hazırlayan:", ara="Kişi ara", bos_metin="Bu adla kişi yok.")


def dm_yayin(ad_tekil, onay_metin_kaldir):
    return (dm_grup("Yayın", "yayinda taslak zamanli")
            + dm("Şimdi Yayımla", "fa-paper-plane", "taslak zamanli",
                 ek=onay(f"{ad_tekil} yayımlansın mı?", "Sitede ve uygulamada hemen görünür; işlem denetim izine yazılır.", "Yayımla", "fa-paper-plane",
                         sonra="Yayımlandı", sonra_durum=("yayinda", "Yayında", "ok")))
            + dm("Yayın Zamanını Değiştir", "fa-calendar-days", "taslak zamanli yayinda", bildir="Yayın zamanı düzenleme ekranındaki Yayın kartından değişir (prototip)")
            + dm("Yayından Kaldır", "fa-eye-slash", "yayinda",
                 ek=onay(f"{ad_tekil} yayından kaldırılsın mı?", onay_metin_kaldir, "Yayından Kaldır", "fa-eye-slash", tehlike=True,
                         sonra="Yayından kaldırıldı; taslak olarak duruyor", sonra_durum=("taslak", "Taslak", "off"))))


def dm_dagitim(gomme=True):
    return (dm_ayir("yayinda") + dm_grup("Dağıtım", "yayinda")
            + dm("Bildirim Gönder", "fa-bell", "yayinda", modul="etkilesim", bildir="Bildirim sekmesi düzenleme ekranında (prototip)")
            + dm("Sosyal Medyada Paylaş", "fa-share-nodes", "yayinda", modul="sosyal-medya", bildir="Sosyal Medya sekmesi düzenleme ekranında (prototip)")
            + dm("Bağlantıyı Kopyala", "fa-link", "yayinda", ek=" data-kopyala")
            + (dm("Gömme Kodunu Kopyala", "fa-code", "yayinda", bildir="Gömme kodu kopyalandı (iframe, 16:9)") if gomme else ""))


def dm_icerik(ek=""):
    return (dm_ayir("yayinda taslak zamanli") + dm_grup("İçerik", "yayinda taslak zamanli") + ek
            + dm("Kopyasını Oluştur", "fa-copy", "yayinda taslak zamanli", bildir="Kopyası taslak olarak oluşturuldu (prototip)")
            + dm("Çeviri İste", "fa-language", "yayinda", disabled=True, pm_ek="Sonraki aşama")
            + dm_ayir("yayinda taslak zamanli"))


# =====================================================================
# 1 · Video ve Akış (video.html)
# =====================================================================
VIDEOLAR = [dict(x, yazar=x.get("yazar") or "Dada Haber") for x in tur_listesi("video-detay.html")]
VIDEO_EK = [
    {"baslik": "Kar yağışında sürücülere 5 uyarı: zincir, lastik ve takip mesafesi", "bolum": "Gündem", "alt_konu": "Afet", "yazar": "Sibel Arslan", "tarih": "2026-11-24", "saat": "", "durum": "taslak", "sure": 214},
    {"baslik": "Bütçe görüşmeleri 3 dakikada: ilk günün öne çıkanları", "bolum": "Finans", "alt_konu": "Türkiye Ekonomisi", "yazar": "Can Demir", "tarih": "2026-11-24", "saat": "19.30", "durum": "zamanli", "sure": 188},
    {"baslik": "Derbi öncesi son antrenman: kadroda iki değişiklik", "bolum": "Spor", "alt_konu": "Futbol", "yazar": "Burak Tan", "tarih": "2026-11-25", "saat": "12.00", "durum": "zamanli", "sure": 142},
    {"baslik": "KAAN test uçuşu: kokpitten görüntüler", "bolum": "Savunma", "alt_konu": "Hava Platformları", "yazar": "Mert Yalın", "tarih": "2026-11-24", "saat": "", "durum": "taslak", "sure": 96},
    {"baslik": "Eski kapak denemesi: haftanın ekonomi özeti", "bolum": "Finans", "alt_konu": "Ekonomi Analizi", "yazar": "Elif Aras", "tarih": "2026-11-20", "saat": "10.00", "durum": "cop", "sure": 305},
]
AKIS = [
    ("Marmara'da kar yağışı: İstanbul sabah saatlerinde", "Gündem", 48, "31,2 B", "p193.jpg", "yayinda", "16.05"),
    ("Asgari ücret masası: ilk toplantı 4 Aralık'ta", "Finans", 44, "18,4 B", "p163.jpg", "yayinda", "15.40"),
    ("KAAN'ın ikinci prototipi test uçuşunda", "Savunma", 51, "22,7 B", "p195.jpg", "yayinda", "15.10"),
    ("Kredi kartı asgari ödeme oranı: 40 saniyede ne değişmedi?", "Finans", 40, "12,9 B", "p183.jpg", "yayinda", "14.35"),
    ("YKS 2027 tarihleri tek ekranda", "Kampüs", 35, "16,1 B", "p178.jpg", "yayinda", "14.00"),
    ("5G hangi illerde açıldı?", "Keşfet", 52, "9,8 B", "p188.jpg", "yayinda", "13.20"),
    ("İklim konferansının sonuç metni üç maddede", "Dünya", 58, "7,4 B", "p122.jpg", "yayinda", "12.45"),
    ("Ara transfer dönemi ne zaman açılıyor?", "Spor", 33, "21,3 B", "p155.jpg", "yayinda", "12.10"),
    ("Merkez Bankası faizi sabit tuttu: 30 saniyede etkisi", "Finans", 30, "14,6 B", "p188.jpg", "yayinda", "11.30"),
    ("Millî takımın aday kadrosu açıklandı", "Spor", 41, "19,0 B", "p158.jpg", "yayinda", "10.55"),
    ("Kar nedeniyle 46 iç hat seferi iptal edildi", "Gündem", 37, "11,2 B", "p182.jpg", "yayinda", "10.20"),
    ("Kadın girişimcilere yeni hibe programı", "Kadın", 45, "6,3 B", "p192.jpg", "yayinda", "09.40"),
    ("Akşam akışı: bütçenin ilk günü 45 saniyede", "Finans", 45, "—", "p163.jpg", "zamanli", "19.00"),
    ("Hava durumu: hafta sonu kar sürecek mi?", "Gündem", 0, "—", "p178.jpg", "taslak", ""),
]
CANLI = [
    ("2027 bütçesinin görüşmeleri Genel Kurul'da başladı", "TBMM Genel Kurulu · Meclis TV yayını", "Gündem", "canli", "24.11.2026 13.00", "4,8 B izleyici", "p195.jpg", "Ayşe Yıldız"),
    ("Valilik kar koordinasyon toplantısı sonrası açıklama", "İstanbul Valiliği · yaklaşık 20 dk", "Gündem", "planli", "24.11.2026 17.00", "hatırlatma 1.240", "p182.jpg", "Sibel Arslan"),
    ("Akşam bülteni canlı: günün sekiz başlığı", "Dada Haber stüdyosu · 25 dk", "Gündem", "planli", "24.11.2026 19.30", "hatırlatma 860", "p133.jpg", "Hande Polat"),
    ("Ekonomi Masası canlı: bütçenin ilk günü", "Can Demir ve konukları · 40 dk", "Finans", "planli", "24.11.2026 21.00", "hatırlatma 2.115", "p163.jpg", "Can Demir"),
    ("Plan ve Bütçe Komisyonu'nda son gün oturumu", "TBMM · 3 sa 10 dk", "Gündem", "bitti", "22.11.2026 10.00", "38,6 B izlenme", "p188.jpg", "Ayşe Yıldız"),
    ("BM İklim Konferansı kapanış oturumu", "Antalya · 1 sa 52 dk", "Dünya", "bitti", "21.11.2026 15.00", "12,1 B izlenme", "p122.jpg", "Zeynep Ak"),
    ("ÖSYM 2027 sınav takvimi tanıtım toplantısı", "Ankara · 48 dk", "Kampüs", "bitti", "21.11.2026 11.00", "27,4 B izlenme", "p164.jpg", "Selin Koç"),
]


def video_sayfasi():
    sat = ""
    kayitlar = [dict(x, durum="yayinda") for x in VIDEOLAR] 
    kayitlar = [x for x in VIDEO_EK if x["durum"] != "cop"] + kayitlar + [x for x in VIDEO_EK if x["durum"] == "cop"]
    say = {}
    for i, v in enumerate(kayitlar):
        sn = v.get("sure") if isinstance(v.get("sure"), int) else 60 + h(v["baslik"], 420)
        img = g_of(v["baslik"])
        d = v["durum"]
        say[v["bolum"]] = say.get(v["bolum"], 0) + 1
        zaman = tarih(v["tarih"], v["saat"]) if v.get("saat") else "—"
        gor = v.get("goruntulenme", "—") if d == "yayinda" else "—"
        href = "video-duzenle.html?id=video"
        alt = f'{ikon("fa-play")}{sure_yaz(sn)} · {e(v["yazar"])}'
        sil_kul = "Video sayfasında ve bir haberin içinde gömülü; oradan da kalkar" if d == "yayinda" and i % 5 == 0 else None
        nit = {"satir": f"v{i}", "durum": d, "kategori": v["bolum"], "yazar": v["yazar"], "ara": f'{v["baslik"]} {v["yazar"]} {v["bolum"]} {v.get("alt_konu") or ""}',
               "baslik": v["baslik"], "href": href, "kullanim": sil_kul}
        acts = eylemler(gor_href=SITE + "video-detay.html" if d == "yayinda" else href, gor_site=d == "yayinda", duz_href=href, ad=v["baslik"])
        sat += satir(nit, [ana_hucre(v["baslik"], alt, img), kat_hucre(v["bolum"], v.get("alt_konu")), durum_hucre(d),
                           f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if d in ("taslak", "cop") else ""}">{zaman}</span></td>',
                           f'<td class="say kb-gizle-t">{e(gor)}</td>'], acts)
    diger = (dm_yayin("Video", "Video sitede ve haberlerin içindeki gömülü oynatıcıda görünmez olur; taslak olarak kalır, geri alınabilir ve denetim izine yazılır.")
             + dm_dagitim() + dm_icerik()
             + dm_kayit() + dm_cop())
    ko = [("Video", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Yayın", "kb-gizle-m"), ("İzlenme", "say kb-gizle-t")]
    l_video = liste("vd", "video", "Video listesi", [("hepsi", "Tümü", None), ("yayinda", "Yayında", None), ("taslak", "Taslak", None), ("zamanli", "Zamanlanmış", None)],
                    "Başlık, hazırlayan ya da kategori ara", kat_suz("vd", say) + yazar_suz("vd", [x["yazar"] for x in kayitlar]),
                    f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen videolar yayından kaldırılıp taslağa alındı">{ikon("fa-eye-slash")}<span>Yayından Kaldır</span></button>',
                    ko, sat, ("fa-video", "Henüz video yok", "İlk videonuzu yükleyin ya da YouTube bağlantısı ekleyin; yayımladığınız videolar burada listelenir.",
                              f'<a class="pe-tag" href="video-duzenle.html?yeni=1&amp;id=video">{ikon("fa-plus")}Yeni Video</a>'),
                    "Videolar yüklenemedi", diger, "video.html", toplam=len(kayitlar),
                    cop_not="Sitede ve gömülü olduğu haberlerde yayından kalkar ve Çöp sekmesine taşınır")

    # Akış
    sat = ""
    for i, (b, k, sn, gor, img, d, saat) in enumerate(AKIS):
        href = "video-duzenle.html?id=akis"
        alt = f'{ikon("fa-mobile-screen")}{("0:%02d" % sn) if sn else "video yok"} · günün akışı {i + 1}/12' if d == "yayinda" else f'{ikon("fa-mobile-screen")}{("0:%02d" % sn) if sn else "video henüz yüklenmedi"}'
        nit = {"satir": f"a{i}", "durum": d, "kategori": k, "ara": f"{b} {k}", "baslik": b, "href": href}
        acts = eylemler(gor_href=SITE + "akis.html" if d == "yayinda" else href, gor_site=d == "yayinda", duz_href=href, ad=b)
        sat += satir(nit, [ana_hucre(b, alt, img), kat_hucre(k), durum_hucre(d),
                           f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if d == "taslak" else ""}">{"24.11.2026 " + saat if saat else "—"}</span></td>',
                           f'<td class="say kb-gizle-t">{gor}</td>'], acts)
    sat += satir({"satir": "a-cop", "durum": "cop", "kategori": "Spor", "ara": "Derbi biletleri satışta", "baslik": "Derbi biletleri satışta", "href": "video-duzenle.html?id=akis"},
                 [ana_hucre("Derbi biletleri satışta", f'{ikon("fa-mobile-screen")}0:29', "p158.jpg"), kat_hucre("Spor"), durum_hucre("cop"),
                  '<td class="kb-gizle-m"><span class="kb-tarih muted">22.11.2026 18.00</span></td>', '<td class="say kb-gizle-t">—</td>'],
                 eylemler(gor_href="video-duzenle.html?id=akis", duz_href="video-duzenle.html?id=akis", ad="Derbi biletleri satışta"))
    diger_a = (dm_yayin("Akış Videosu", "Video günün akışından çıkar; taslak olarak kalır, geri alınabilir ve denetim izine yazılır.")
               + dm("Akıştaki Sırasını Değiştir", "fa-arrow-down-1-9", "yayinda", bildir="Sıra düzenleme ekranındaki “Akıştaki sıra” alanından değişir (prototip)")
               + dm_dagitim(gomme=False) + dm_icerik() + dm_kayit() + dm_cop())
    ko_a = [("Akış Videosu", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Yayın", "kb-gizle-m"), ("İzlenme", "say kb-gizle-t")]
    l_akis = liste("ak", "akış videosu", "Akış videoları", [("hepsi", "Tümü", None), ("yayinda", "Yayında", None), ("taslak", "Taslak", None), ("zamanli", "Zamanlanmış", None)],
                   "Başlık ya da Kategori Ara", kat_suz("ak"),
                   f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen akış videoları akıştan çıkarıldı">{ikon("fa-eye-slash")}<span>Akıştan Çıkar</span></button>',
                   ko_a, sat, ("fa-mobile-screen", "Henüz akış videosu yok", "Dikey (9:16) kısa videolar günün akışında gösterilir; akışın bir sonu vardır.",
                               f'<a class="pe-tag" href="video-duzenle.html?yeni=1&amp;id=akis">{ikon("fa-plus")}Yeni Akış Videosu</a>'),
                   "Akış videoları yüklenemedi", diger_a, "video.html?sekme=tAkis",
                   cop_not="Günün akışından ve sitede yayından kalkar ve Çöp sekmesine taşınır",
                   ust_ek=f'<div class="kb-bant bilgi">{ikon("fa-circle-info")}<span>Günün akışı 12 videodur; sırası yayın saatine göredir, akışın sonunda okur habere yönlendirilir.</span></div>')

    # Canlı yayın
    sat = ""
    for i, (b, alt, k, d, bas_, izl, img, kim) in enumerate(CANLI):
        href = "video-duzenle.html?id=canli"
        site = SITE + "canli-yayin.html"
        nit = {"satir": f"c{i}", "durum": d, "kategori": k, "ara": f"{b} {alt} {k} {kim}", "baslik": b, "href": href,
               "kullanim": "Ana sayfadaki canlı bandında ve Canlı Yayın sayfasında; oradan da kalkar" if d == "canli" else None}
        acts = eylemler(gor_href=site if d != "planli" else href, gor_site=d != "planli", duz_href=href, ad=b)
        sat += satir(nit, [ana_hucre(b, f'{ikon("fa-tower-broadcast")}{e(alt)}', img), kat_hucre(k), durum_hucre(d),
                           f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if d == "bitti" else ""}">{bas_}</span></td>',
                           f'<td class="say kb-gizle-t">{izl}</td>'], acts)
    diger_c = (dm_grup("Yayın", "canli planli bitti")
               + dm("Yayını Şimdi Başlat", "fa-circle-play", "planli", ek=onay("Canlı yayın başlasın mı?", "Yayın sitede Canlı Yayın sayfasında ve ana sayfanın canlı bandında hemen görünür; hatırlatma isteyenlere bildirim gider. İşlem denetim izine yazılır.", "Yayını Başlat", "fa-circle-play", sonra="Canlı yayın başladı", sonra_durum=("canli", "Canlı", "warm")))
               + dm("Yayını Bitir", "fa-circle-stop", "canli", ek=onay("Canlı yayın bitirilsin mi?", "Önce: yayın canlı, 4,8 B izleyici. Sonra: yayın “Sona erdi” olur, tekrar kaydı arşive girer; izleyicilere “yayın sona erdi” görünür. Denetim izine yazılır.", "Yayını Bitir", "fa-circle-stop", tehlike=True, sonra="Yayın sona erdi; tekrarı arşive eklendi", sonra_durum=("bitti", "Sona Erdi", "off")))
               + dm("Başlangıç Zamanını Değiştir", "fa-calendar-days", "planli", bildir="Başlangıç zamanı düzenleme ekranında değişir (prototip)")
               + dm("Canlı akışı aç (dakika dakika)", "fa-list-ul", "canli", hedef="haberler.canli", modul="haberler")
               + dm_ayir("canli planli bitti") + dm_grup("Dağıtım", "canli planli bitti")
               + dm("Hatırlatma Bildirimi Gönder", "fa-bell", "planli", modul="etkilesim", bildir="Hatırlatma bildirimi zamanlandı (yayın başlarken)")
               + dm("Sosyal Medyada Paylaş", "fa-share-nodes", "canli planli bitti", modul="sosyal-medya", bildir="Sosyal Medya sekmesi düzenleme ekranında (prototip)")
               + dm("Bağlantıyı Kopyala", "fa-link", "canli bitti", ek=" data-kopyala")
               + dm_ayir("canli planli bitti") + dm_kayit() + dm_cop())
    ko_c = [("Canlı Yayın", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Başlangıç", "kb-gizle-m"), ("İzleyici", "say kb-gizle-t")]
    l_canli = liste("cy", "canlı yayın", "Canlı yayınlar", [("hepsi", "Tümü", None), ("canli", "Canlı", None), ("planli", "Planlandı", None), ("bitti", "Sona Erdi", None)],
                    "Yayın adı, yer ya da kişi ara", kat_suz("cy"), "", ko_c, sat,
                    ("fa-tower-broadcast", "Henüz canlı yayın yok", "Planladığınız ve sona eren canlı yayınlar burada listelenir.",
                     f'<a class="pe-tag" href="video-duzenle.html?yeni=1&amp;id=canli">{ikon("fa-plus")}Yeni Canlı Yayın</a>'),
                    "Canlı yayınlar yüklenemedi", diger_c, "video.html?sekme=tCanli",
                    cop_not="Canlı Yayın sayfasından kalkar ve Çöp sekmesine taşınır")

    ust = sayfa_bas("<h1>Video ve Akış</h1>",
                    f'<div class="ph-sub">Yayında {len(VIDEOLAR)} video · bugünün akışında 12 dikey video · 1 canlı yayın sürüyor, 3 yayın planlandı</div>',
                    btn_link("multimedya.sablon", "Marka Şablonu", "fa-stamp", roller="super gyy") + "\n      "
                    + btn_link(None, "Canlı Yayın", "fa-plus", href="video-duzenle.html?yeni=1&id=canli") + "\n      "
                    + btn_link(None, "Akış", "fa-plus", href="video-duzenle.html?yeni=1&id=akis") + "\n      "
                    + btn_link(None, "Yeni Video", "fa-plus", acc=True, href="video-duzenle.html?yeni=1&id=video"))
    govde = (ust + '  <div data-sekmeli>\n  ' + sayfa_sekmeler([("tVideo", "fa-video", "Video", len(VIDEOLAR)), ("tAkis", "fa-mobile-screen", "Akış", 12), ("tCanli", "fa-tower-broadcast", "Canlı Yayın", len(CANLI))])
             + f'\n  <div class="sa-form-panel" id="tVideo">\n{l_video}  </div>\n  <div class="sa-form-panel" id="tAkis" hidden>\n{l_akis}  </div>\n  <div class="sa-form-panel" id="tCanli" hidden>\n{l_canli}  </div>\n  </div>\n')
    yaz("video.html", bas("Video ve Akış", "multimedya.video") + govde + son())


# =====================================================================
# düzenleme ekranı iskeleti (Haber düzenle kalıbı)
# =====================================================================
_hd = (KOK / "moduller" / "haberler" / "duzenle.html").read_text(encoding="utf-8")
_m = re.search(r'data-alt-harita="([^"]+)"', _hd)
ALT_HARITA = json.loads(html.unescape(_m.group(1))) if _m else {k: [] for k in KATEGORILER}


def alt_konu(sid, ana, secili):
    cip = "".join(f'<span class="kb-cip" data-deger="{e(a)}"><span>{e(a)}</span><button type="button" aria-label="Kaldır">{ikon("fa-xmark")}</button></span>' for a in secili)
    return (f'<div class="frow"><span class="flabel">Alt Konular</span>'
            f'<div class="kb-cip-girdi" data-alan-id="alt-konu" data-birincil data-havuz-kapali data-ana-kaynak="#{sid}" data-havuz="{e(json.dumps(ALT_HARITA.get(ana, []), ensure_ascii=False))}" data-alt-harita="{e(json.dumps(ALT_HARITA, ensure_ascii=False))}">'
            f'{cip}<input type="text" placeholder="Alt konu ara" aria-label="Alt konu ara"><div class="pnl-menu kb-cip-oneri"></div></div>'
            f'<span class="fhint">İsteğe bağlı; ilk seçilen ana alt konudur. Yeni alt konu Haberler › Kategoriler\'den eklenir.</span></div>')


def yazar_secim(sid, deger, etiket="Hazırlayan"):
    ops = [(y, y) for y in YAZARLAR]
    return (f'<div class="frow"><span class="flabel">{etiket}</span>'
            + secim(sid, deger, ops, alan_id="yazar", ara="Kişi ara", bos="Kişi seçin", ek=" data-oturum-yazar", bos_metin="Bu adla kişi yok.")
            + '<span class="fhint">Yeni kayıtta oturumdaki kişi gelir.</span></div>')


def siniflandirma(sid, kat, alt, yazar, ek=""):
    return (f'<div class="form-sec" data-ai-grup="sinif"><div class="form-sec-tt">{ikon("fa-sitemap")}Sınıflandırma</div><div class="form-grid">'
            f'<div class="frow two"><div class="frow"><span class="flabel">Ana Kategori</span>{kat_secim(sid, kat)}'
            f'<span class="fhint">Adres ve SEO ana kategoriye göre kurulur. Kategoriler <a class="kb-bag" data-hedef="haberler.liste" href="#icerik">Haberler</a> ekranından yönetilir.</span></div>'
            f'{alt_konu(sid, kat, alt)}</div>'
            f'<div class="frow two">{yazar_secim(sid + "Yaz", yazar)}{ek}</div></div></div>')


def baslik_spot(baslik, spot, b_not="Sitede başlık; SEO başlığı buradan üretilir", s_not="Kartta ve paylaşımda başlığın altında", s_etk="Spot", s_sayac="160|200"):
    return (f'<div class="form-sec"><div class="form-grid">'
            + girdi("fBaslik", "Başlık", baslik, alan_id="baslik", alan="baslik", sayac="70|90", not_=b_not, hata="Başlık zorunlu", buyuk=True)
            + metin_alani("fSpot", s_etk, spot, alan_id="spot", alan="spot", sayac=s_sayac, not_=s_not, satir=2)
            + '</div></div>')


def duzenle_sayfasi(dosya, title, sayfa, yeni_baslik, h1, h1_yeni, alt, alt_yeni, geri, site, form_id, kayit, sekmeler, paneller, yan, kaydet, sablonlar="", ust_bant=""):
    gs = f'<a class="btn btn-ghost btn-sm" data-yeni-gizle href="{e(site)}" target="_blank" rel="noopener">{ikon("fa-arrow-up-right-from-square")}Sitede Görüntüle</a>' if site else ""
    ust = sayfa_bas(f'<h1 data-yeni-metin="{e(h1_yeni)}">{e(h1)}</h1>', f'<div class="ph-sub" data-yeni-metin="{e(alt_yeni)}">{alt}</div>',
                    f'<a class="btn btn-ghost btn-sm" data-hedef="{geri[0]}"{f" data-hedef-ek=\"{e(geri[2])}\"" if len(geri) > 2 else ""} href="#icerik">{ikon("fa-arrow-left")}{geri[1]}</a>\n      {gs}')
    govde = f"""{ust}{ust_bant}
  <div class="form-layout">
  <section class="pnl-card" id="{form_id}" data-form data-sekmeli data-zorunlu-kayit="{kayit}" aria-label="{e(title)} formu">
    {dil_bas("Dil seçici bütün sekmelerdeki metin alanlarını birlikte değiştirir; görsel, dosya, hazırlayan ve kategori bütün dillerde ortaktır.")}
    {form_sekmeler(sekmeler)}
{paneller}
  </section>
  <aside class="side-card" aria-label="Yayın">
{yan}
  </aside>
  </div>
{kaydet}"""
    yaz(dosya, bas(title, sayfa, yeni_baslik) + govde + son(sablonlar, editor=True))


def detay_panel(icerik):
    return f'    <div class="sa-form-panel" id="pDetay" role="tabpanel">\n{icerik}\n    </div>\n'


STD_SEKMELER = [("pDetay", "fa-file-lines", "Detay", None), ("pSeo", "fa-magnifying-glass-chart", "SEO", None),
                ("pBildirim", "fa-bell", "Bildirim", "etkilesim"), ("pSosyal", "fa-share-nodes", "Sosyal Medya", "sosyal-medya")]


def okur_etkilesimi(*satirlar):
    return f'<div class="form-sec"><div class="form-sec-tt">{ikon("fa-comments")}Okur Etkileşimi</div><div class="form-grid">{"".join(satirlar)}</div></div>'


# =====================================================================
# 2 · Video düzenle (video-duzenle.html)
# =====================================================================
def video_duzenle():
    v = next((x for x in VIDEOLAR if "kar" in x["baslik"].lower()), VIDEOLAR[0])
    img = g_of(v["baslik"])
    baslik = v["baslik"]
    spot = "İstanbul'da gece başlayan kar yağışı sabah saatlerinde etkisini artırdı; ekipler ana arterlerde tuzlama yapıyor, toplu taşıma seferleri uzatıldı."
    aciklama = ("<p>Marmara Bölgesi'nde etkili olan kar yağışı İstanbul'da sabah saatlerinde yoğunlaştı. Videoda Beşiktaş, Kadıköy ve Mecidiyeköy'den görüntüler ile "
                "İstanbul Büyükşehir Belediyesi ekiplerinin çalışmaları yer alıyor.</p><h2>Videoda neler var?</h2>"
                "<ul><li>Ana arterlerde tuzlama ve kar küreme çalışmaları</li><li>Metro ve Marmaray seferlerindeki uzatma</li><li>Valiliğin okullar için yaptığı açıklama</li></ul>"
                "<p>Meteoroloji, yağışın akşam saatlerine kadar aralıklarla süreceğini bildiriyor.</p>")
    ai = ai_adim("#fBaslik,#fSpot", [("aciklama", "Açıklama Taslağı", False, None), ("sinif", "Kategori ve Alt Konular", True, None), ("seo", "SEO", True, None),
                                     ("bildirim", "Bildirim Metni", True, "etkilesim"), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya"), ("altyazi", "Altyazı (Videonun Sesinden)", True, None)],
                 "Başlığı ve spotu yazın; işaretli bölümler bunlardan ve videonun sesinden üretilir. Üretilen her bölüm “AI önerisi” etiketiyle gelir.")
    icerik = f"""      <div class="form-sec">
        <div class="form-sec-tt">{ikon("fa-film")}Video<span class="fs-ek">Dosya yükleyin ya da YouTube/gömme bağlantısı ekleyin</span></div>
        <div class="form-grid">
          <div class="frow"><span class="flabel">Kaynak</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="vKaynak" data-ac="vKDosya" checked>Dosya Yükle</label><label class="kb-secenek"><input type="radio" name="vKaynak" data-ac="vKBag">YouTube ya da gömme bağlantısı</label></div></div>
          <div class="frow" id="vKDosya"><span class="flabel">Video Dosyası</span>{dosya_alan("video", "Video", "video", ("marmara-kar-istanbul-sabah.mp4", 148897792, 212), hata="Video dosyası yükleyin ya da bağlantı ekleyin")}
            <span class="fhint">MP4, MOV ya da WEBM · en fazla 500 MB (Site Ayarları › Limitler). Süre ve çözünürlük dosyadan okunur: <b>3 dk 32 sn · 1920×1080</b>.</span></div>
          <div class="frow" id="vKBag" hidden><label for="vBag">Bağlantı</label><input class="finput" id="vBag" data-alan-id="video" data-zorunlu-metin="Video dosyası yükleyin ya da bağlantı ekleyin" placeholder="https://www.youtube.com/watch?v=… ya da gömme kodu" inputmode="url">
            <span class="fhint">YouTube, Vimeo ve Dailymotion bağlantısı ya da &lt;iframe&gt; gömme kodu. Süre ve kapak bağlantıdan okunur.</span></div>
          <div class="frow" data-ai-grup="altyazi"><span class="flabel">Altyazı</span>
            {dosya_alan("belge", "Altyazı dosyası", None, ("marmara-kar-istanbul-sabah.tr.vtt", 6144), kabul=".vtt,.srt", sinir=5)}
            {toggle("Otomatik Türkçe Altyazı", "Dosya yoksa videonun sesinden üretilir; editör düzeltir")}</div>
        </div>
      </div>
{gorsel_alan("vKapak", "multimedya.video", "Kapak Görseli", img, [("web.detay", "Oynatıcı · 16:9", "16:9", None), ("web.kart", "Kart · 4:3", "4:3", None)], ("mobil.kart", "Mobil kart · 4:3", "4:3", None),
             "oynatıcı <b>1280×720</b>, kart <b>308×231</b>", "<b>358×268</b>", "1280×720", kaynak="Dada Haber · telif bizde", odak=(50, 45),
             ek_alt=" Videodan kare seçmek için “Kırp ve odak” penceresinde yüklenen görsel kullanılır.")}
{editor("Açıklama", aciklama, "Sitede videonun altında; okur “devamını oku” ile açar", ai_grup="aciklama", fs_ek="Ara başlık, bağlantı, liste")}
{siniflandirma("vKat", v["bolum"], [v["alt_konu"]] if v.get("alt_konu") and v["alt_konu"] != v["bolum"] else ["Afet"], v["yazar"])}
{okur_etkilesimi(toggle("Yorumlar Açık", "Yorumları editörler yönetir"), toggle("Haberlerin İçine Gömülebilir", "Haber metnine “video ekle” ile eklenir; gömme kodu verilir"), toggle("Otomatik Oynat", "Sessiz başlar; yalnız video sayfasında", False))}"""
    paneller = (detay_panel(baslik_spot(baslik, spot) + ai + "\n" + icerik)
                + seo_panel("pSeo", "İstanbul'da kar yağışı: sabah saatlerinden görüntüler | Dada Haber", "İstanbul'da kar yağışı sabah saatlerinde yoğunlaştı. Tuzlama çalışmaları, uzatılan seferler ve valiliğin açıklaması videoda.",
                            "dadahaber.com/video/", "marmara-da-kar-yagisi-istanbul-sabah", ["istanbul kar", "kar yağışı video", "marmara kar"],
                            toggle("Video Şeması (VideoObject)", "Google video sonuçlarında küçük görsel ve süreyle görünür"))
                + bildirim_panel("pBildirim", "Video: İstanbul'da kar sabah yoğunlaştı", "Ana arterlerde tuzlama sürüyor, seferler uzatıldı. Sabahın görüntüleri 3 dakikada.", "Kapak görselinin bildirim kırpımı (2:1)")
                + sosyal_panel("pSosyal", {"x": f"İstanbul'da kar sabah saatlerinde yoğunlaştı 🎥 Tuzlama sürüyor, seferler uzatıldı.\n\nhttps://dadahaber.com/video/marmara-da-kar-yagisi\n\n#İstanbul #kar",
                                           "facebook": "İstanbul'da gece başlayan kar yağışı sabah saatlerinde etkisini artırdı. Beşiktaş, Kadıköy ve Mecidiyeköy'den görüntüler 3 dakikada.\n\nhttps://dadahaber.com/video/marmara-da-kar-yagisi",
                                           "instagram": "İstanbul'da kar sabah saatlerinde yoğunlaştı ❄️ Sabahın görüntüleri profildeki bağlantıda.\n\n#istanbul #kar #dadahaber",
                                           "telegram": "🎥 İstanbul'da kar sabah yoğunlaştı\n\nTuzlama sürüyor, toplu taşıma seferleri uzatıldı.\n\nhttps://dadahaber.com/video/marmara-da-kar-yagisi"},
                               img, "#vKapak", (50, 45), "Videonun kendisi platforma yüklenir (X, Facebook, Telegram); Instagram'da kapak ve bağlantı paylaşılır."))
    yan = (bildirim_onizle("pBildirim", "Video: İstanbul'da kar sabah yoğunlaştı", "Ana arterlerde tuzlama sürüyor, seferler uzatıldı. Sabahın görüntüleri 3 dakikada.", img)
           + sosyal_onizle("pSosyal", img, baslik, (50, 45))
           + yayin_kart(durum_secim("ycDurum", "yayinda", YAYIN_DURUM), f'{v["tarih"]} {v["saat"]}',
                        toggle("Video Sayfasında Öne Çıkar", "Video sayfasının vitrininde", True) + toggle("Ana Sayfa Video Rayında", "Ana sayfadaki Video bölümünde", True)
                        + '<div class="sa-durum" data-yeni-gizle><div><span>İzlenme</span><b>' + e(v["goruntulenme"]) + '</b></div><div><span>Ortalama izleme</span><b>1 dk 48 sn</b></div><div><span>Tamamlama</span><b>%51</b></div></div>',
                        surum=(3, "23.11.2026 16.20", "Sibel Arslan"))
           + seo_kart(84, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Kapak 1280 px üstü"), (False, "Altyazı dosyası dizinde yok")]))
    duzenle_sayfasi("video-duzenle.html", "Video Düzenle", "multimedya.video", "Yeni Video", "Video Düzenle", "Yeni Video",
                    f'{e(v["bolum"])} › Afet · {e(v["yazar"])} · {tarih(v["tarih"], v["saat"])}\'te yayımlandı · {e(v["goruntulenme"])} izlenme',
                    "Taslak · henüz kaydedilmedi · hazırlayan: oturumdaki kullanıcı", ("multimedya.video", "Videolara Dön"), SITE + "video-detay.html",
                    "vdForm", "multimedya.video", STD_SEKMELER, paneller, yan,
                    kaydet_cubugu("vdForm", "Kaydedildi · 23.11.2026 16.20 · Sibel Arslan", "Video güncellendi; sitede yayında ve önceki hal sürüm geçmişinde", "Video yayımlandı; video sayfasında ve uygulamada görünür"))


# =====================================================================
# 3 · Akış videosu düzenle (akis-duzenle.html)
# =====================================================================
HABER_SEC = [x for x in sorted(soz["haberler"], key=lambda x: (x["tarih"], x["saat"]), reverse=True) if x["detay"].endswith("-detay.html") and x["detay"] not in ("video-detay.html", "podcast-detay.html", "foto-fokus-detay.html", "infografik-detay.html", "haber-dinle-detay.html")][:30]


def haber_secim(sid, deger, alan_id=None, etiket="Bağlı haber", not_="", ek=""):
    ops = [(x["baslik"], x["baslik"], f'{x["bolum"]} · {tarih(x["tarih"], x["saat"])}') for x in HABER_SEC]
    if deger and deger not in [o[0] for o in ops]:
        ops.insert(0, (deger, deger, "Gündem"))
    return (f'<div class="frow" data-modul="haberler"{ek}><span class="flabel">{etiket}</span>'
            + secim(sid, deger, ops, alan_id=alan_id, ara="Haber başlığı ara", bos="Haber seçin", bos_metin="Bu başlıkla haber yok.")
            + (f'<span class="fhint">{not_}</span>' if not_ else "") + "</div>")


def akis_duzenle():
    b, k, sn, gor, img, d, saat = AKIS[0]
    ai = ai_adim("#fBaslik,#fSpot", [("sinif", "Kategori ve Alt Konular", True, None), ("seo", "SEO", True, None), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya"),
                                     ("altyazi", "Ekran Yazıları (Videonun Sesinden)", True, None)],
                 "Başlığı ve kısa metni yazın; işaretli bölümler bunlardan ve videonun sesinden üretilir.")
    icerik = f"""      <div class="form-sec">
        <div class="form-sec-tt">{ikon("fa-mobile-screen")}Dikey Video<span class="fs-ek">9:16 · en fazla 90 saniye</span></div>
        <div class="form-grid">
          <div class="frow"><span class="flabel">Dikey Video</span>{dosya_alan("video", "Dikey Video", "video", ("akis-marmara-kar.mp4", 38273024, 48), hata="Dikey videoyu yükleyin", sinir=200)}
            <span class="fhint">Telefonda tam ekran oynar. Süre dosyadan okunur: <b>48 sn · 1080×1920</b>. Yatay video yüklenirse ortası kırpılır.</span></div>
          <div class="frow" data-ai-grup="altyazi"><span class="flabel">Ekran Yazıları</span>
            {toggle("Otomatik Ekran Yazısı", "Sessiz izleyen okur için videonun sesinden; editör düzeltir")}</div>
          <div class="frow two">
            <div class="frow"><label for="aSira">Akıştaki Sıra</label><div class="kb-birim"><input class="finput" id="aSira" data-alan-id="sira" inputmode="numeric" value="1"><span>/ 12</span></div><span class="fhint">Boşsa yayın saatine göre sıralanır.</span></div>
            {haber_secim("aHaber", "Marmara'da kar yağışı: İstanbul'da okullar yarın da tatil", etiket="“Habere Git” Bağlantısı", not_="Akışın sonunda ve videonun altında okur bu habere gider.")}
          </div>
        </div>
      </div>
{gorsel_alan("aKapak", "multimedya.akis", "Kapak Görseli", img, [("web.detay", "Oynatıcı · 9:16", "9:16", 150), ("web.kart", "Ray kartı · 9:16", "9:16", 110)], ("mobil.kart", "Tam ekran · 9:16", "9:16", 150),
             "oynatıcı <b>420×747</b>, ray kartı <b>188×334</b>", "<b>358×636</b>", "1080×1920", kaynak="Dada Haber · telif bizde", odak=(50, 50))}
{siniflandirma("aKat", k, ["İstanbul"], "Sibel Arslan")}
{okur_etkilesimi(toggle("Yorumlar Açık", "Yorumları editörler yönetir"), toggle("Ana Sayfa Akış Rayında", "Ana sayfadaki dikey video rayında"))}"""
    paneller = (detay_panel(baslik_spot(b, "Gece başlayan kar sabah yoğunlaştı; ekipler tuzlama yapıyor, seferler uzatıldı.", s_etk="Kısa Metin", s_not="Videonun üstünde iki satır", s_sayac="90|120") + ai + "\n" + icerik)
                + seo_panel("pSeo", "Marmara'da kar: İstanbul sabah saatlerinde | Dada Haber Akış", "İstanbul'da kar yağışı sabah saatlerinde: 48 saniyede yollar, seferler ve okullar. Dada Haber Akış.",
                            "dadahaber.com/akis/", "marmara-da-kar-yagisi-istanbul-sabah", ["istanbul kar", "akış"])
                + bildirim_panel("pBildirim", "Akış: İstanbul'da kar 48 saniyede", "Yollar, seferler ve okullar: sabahın özeti dikey videoda.", "Kapak görselinin bildirim kırpımı (2:1)")
                + sosyal_panel("pSosyal", {"instagram": "İstanbul'da kar sabah yoğunlaştı ❄️ 48 saniyede yollar, seferler, okullar.\n\n#istanbul #kar #dadahaber",
                                           "x": "İstanbul'da kar 48 saniyede ❄️\n\nhttps://dadahaber.com/akis/marmara-da-kar-yagisi\n\n#İstanbul",
                                           "facebook": "İstanbul'da kar sabah saatlerinde yoğunlaştı: yollar, seferler ve okullar 48 saniyede."},
                               img, "#aKapak", (50, 50), "Dikey video Instagram Reels, YouTube Shorts ve X'e video olarak yüklenir."))
    yan = (bildirim_onizle("pBildirim", "Akış: İstanbul'da kar 48 saniyede", "Yollar, seferler ve okullar: sabahın özeti dikey videoda.", img)
           + sosyal_onizle("pSosyal", img, b, (50, 50))
           + yayin_kart(durum_secim("ycDurum", "yayinda", YAYIN_DURUM), "2026-11-24 16.05",
                        f'<div class="sa-durum" data-yeni-gizle><div><span>İzlenme</span><b>{gor}</b></div><div><span>Sonuna kadar izleyen</span><b>%62</b></div><div><span>Habere geçen</span><b>%14</b></div></div>',
                        surum=(2, "24.11.2026 16.10", "Sibel Arslan"))
           + seo_kart(78, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Dikey kapak 1080 px üstü"), (False, "Ekran yazısı dizinde yok")]))
    duzenle_sayfasi("akis-duzenle.html", "Akış Videosu Düzenle", "multimedya.video", "Yeni Akış Videosu", "Akış Videosu Düzenle", "Yeni Akış Videosu",
                    f"Gündem · günün akışında 1/12 · 24.11.2026 16.05'te yayımlandı · {gor} izlenme", "Taslak · henüz kaydedilmedi · hazırlayan: oturumdaki kullanıcı",
                    ("multimedya.video", "Akışa Dön", "?sekme=tAkis"), SITE + "akis.html", "akForm", "multimedya.akis", STD_SEKMELER, paneller, yan,
                    kaydet_cubugu("akForm", "Kaydedildi · 24.11.2026 16.10 · Sibel Arslan", "Akış videosu güncellendi; günün akışında yayında", "Akış videosu yayımlandı; günün akışına eklendi"))


# =====================================================================
# 4 · Canlı yayın düzenle (canli-duzenle.html)
# =====================================================================
def canli_duzenle():
    b, alt, k, d, bas_, izl, img, kim = CANLI[0]
    ai = ai_adim("#fBaslik,#fSpot", [("aciklama", "Açıklama Taslağı", False, None), ("seo", "SEO", True, None), ("bildirim", "Hatırlatma Bildirimi", True, "etkilesim"),
                                     ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")],
                 "Başlığı ve spotu yazın; işaretli bölümler bunlardan üretilir.")
    aciklama = ("<p>2027 yılı merkezi yönetim bütçe kanunu teklifi, Plan ve Bütçe Komisyonu'nun ardından Türkiye Büyük Millet Meclisi Genel Kurulu'nda görüşülmeye başlandı. "
                "Oturumu canlı izleyebilir, öne çıkan gelişmeleri canlı akıştan takip edebilirsin.</p>")
    icerik = f"""      <div class="form-sec">
        <div class="form-sec-tt">{ikon("fa-tower-broadcast")}Yayın<span class="fs-ek">Kaynak, zaman ve yayın anahtarı</span></div>
        <div class="form-grid">
          <div class="frow"><span class="flabel">Yayın Kaynağı</span>
            <div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="cKaynak" data-ac="cKBag" checked>Dış Yayın Bağlantısı</label><label class="kb-secenek"><input type="radio" name="cKaynak" data-ac="cKSunucu">Kendi Yayın Sunucumuz (RTMP)</label></div></div>
          <div class="frow" id="cKBag"><label for="cBag">Yayın Bağlantısı</label><input class="finput" id="cBag" data-alan-id="video" data-zorunlu-metin="Yayın bağlantısını ekleyin ya da kendi sunucumuzu seçin" inputmode="url" value="https://www.youtube.com/live/meclistv-genel-kurul">
            <span class="fhint">YouTube canlı, Meclis TV ya da kurumun yayın bağlantısı; sitede gömülü oynatıcıda açılır.</span></div>
          <div id="cKSunucu" hidden><div class="frow"><span class="flabel">Sunucu Adresi</span><input class="finput" value="rtmp://yayin.dadahaber.ornek/canli" readonly aria-label="Sunucu Adresi"><span class="fhint">Yayın yazılımına (OBS vb.) bu adres yazılır.</span></div>
            <div class="frow" data-alan-id="video"><span class="flabel">Yayın Anahtarı</span><div class="kb-maske" data-ad="Yayın Anahtarı" data-on-ek="live_"><div class="km-ust"><i class="fa-solid fa-lock km-kilit" aria-hidden="true"></i><span class="km-deger">••••••••••••••••7q2k</span><button type="button" class="btn btn-ghost btn-sm" data-maske-yenile>{ikon("fa-rotate")}Yenile</button></div><span class="km-meta">Oluşturuldu 01.11.2026 · Selin Aydemir · son kullanım 13.00</span><div class="km-acik" hidden><p>{ikon("fa-triangle-exclamation")}Bu değer yalnızca şimdi görünür; kapatınca bir daha gösterilmez.</p><code></code><div class="km-acik-btn"><button type="button" class="btn btn-acc btn-sm" data-maske-kopyala>{ikon("fa-copy")}Kopyala</button><button type="button" class="btn btn-ghost btn-sm" data-maske-gizle>Kapat</button></div></div></div><span class="fhint">Gizli değerdir; yenilemek e-posta koduyla doğrulanır.</span></div></div>
          <div class="frow two">
            <div class="frow"><span class="flabel">Başlangıç</span>{tarih_sec("cBas", "2026-11-24 13.00", ' data-alan-id="baslangic" data-zorunlu-metin="Yayının başlangıç zamanını seçin" data-yeni-bos')}<span class="fhint">Planlanan yayın sitede “Yakında” olarak görünür; hatırlatma isteyen okura bildirim gider.</span></div>
            <div class="frow"><label for="cSure">Tahmini Süre</label><div class="kb-birim"><input class="finput" id="cSure" inputmode="numeric" value="240"><span>dk</span></div></div>
          </div>
          {girdi("cYer", "Yer ve Yayın Sahibi", alt, not_="Kartta başlığın altında")}
          {toggle("Yayın Bitince Tekrarını Arşive Ekle", "Sona eren yayınlar listesinde “Tekrarını izle” olarak görünür")}
          <div class="frow" data-modul="haberler"><span class="flabel">Canlı Akış (Dakika Dakika)</span><span class="fhint">Yayının altında öne çıkan gelişmeler akışı: <a class="kb-bag" data-hedef="haberler.canli" href="#icerik">Canlı anlatım masasında aç</a></span></div>
        </div>
      </div>
{gorsel_alan("cKapak", "multimedya.video", "Kapak Görseli", img, [("web.detay", "Oynatıcı · 16:9", "16:9", None), ("web.kart", "Kart · 4:3", "4:3", None)], ("mobil.kart", "Mobil kart · 4:3", "4:3", None),
             "oynatıcı <b>1280×720</b>, kart <b>308×231</b>", "<b>358×268</b>", "1280×720", kaynak="TBMM · basın görseli", odak=(50, 45),
             ek_alt=" Yayın başlamadan önce oynatıcıda bu görsel görünür.")}
{editor("Açıklama", aciklama, "Sitede oynatıcının altında", ai_grup="aciklama")}
{siniflandirma("cKat", k, ["Siyaset"], kim)}
{okur_etkilesimi(toggle("Canlı Sohbet", "Yayın sırasında yorumlar akar; editörler yönetir", False), toggle("Ana Sayfa Canlı Bandı", "Yayın sürerken ana sayfanın üstünde"))}"""
    paneller = (detay_panel(baslik_spot(b, "Plan ve Bütçe Komisyonu'nun ardından bütçe teklifi Genel Kurul'da; oturum canlı.") + ai + "\n" + icerik)
                + seo_panel("pSeo", "Canlı: 2027 bütçe görüşmeleri Genel Kurul'da | Dada Haber", "2027 bütçesinin TBMM Genel Kurulu görüşmeleri canlı yayında. Öne çıkan gelişmeler canlı akışta.",
                            "dadahaber.com/canli-yayin/", "2027-butcesinin-gorusmeleri-genel-kurul-da", ["bütçe 2027 canlı", "tbmm genel kurul canlı"],
                            toggle("Canlı Yayın Şeması (BroadcastEvent)", "Google'da “CANLI” etiketiyle görünür"))
                + bildirim_panel("pBildirim", "Canlı: Bütçe görüşmeleri başladı", "TBMM Genel Kurulu'nda 2027 bütçesi görüşülüyor. Oturumu canlı izle.", "Kapak görselinin bildirim kırpımı (2:1)", "2026-11-24 13.00")
                + sosyal_panel("pSosyal", {"x": "🔴 CANLI | 2027 bütçesinin görüşmeleri Genel Kurul'da başladı.\n\nhttps://dadahaber.com/canli-yayin/butce-2027\n\n#Bütçe2027 #TBMM",
                                           "facebook": "🔴 Canlı yayın: 2027 bütçesi TBMM Genel Kurulu'nda. Oturumu ve öne çıkan gelişmeleri buradan takip edin.\n\nhttps://dadahaber.com/canli-yayin/butce-2027",
                                           "telegram": "🔴 CANLI\n\n2027 bütçesinin görüşmeleri Genel Kurul'da başladı.\n\nhttps://dadahaber.com/canli-yayin/butce-2027"},
                               img, "#cKapak", (50, 45)))
    yan = (bildirim_onizle("pBildirim", "Canlı: Bütçe görüşmeleri başladı", "TBMM Genel Kurulu'nda 2027 bütçesi görüşülüyor. Oturumu canlı izle.", img)
           + sosyal_onizle("pSosyal", img, b, (50, 45))
           + yayin_kart(durum_secim("ycDurum", "canli", [("planli", "Planlandı", "yakında olarak görünür"), ("canli", "Canlı", ""), ("bitti", "Sona Erdi", "tekrarı arşive girer"), ("taslak", "Taslak", "sitede görünmez")]),
                        "2026-11-24 12.30",
                        '<div class="sa-durum" data-yeni-gizle><div><span>Şu an izleyen</span><b>4,8 B</b></div><div><span>En yüksek</span><b>6,1 B · 14.20</b></div><div><span>Başladı</span><b>13.00</b></div></div>',
                        surum=(5, "24.11.2026 15.42", "Ayşe Yıldız"), durum_state="yayinda")
           + seo_kart(81, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Kapak 1280 px üstü"), (False, "Canlı akış bağlantısı yok")]))
    duzenle_sayfasi("canli-duzenle.html", "Canlı Yayın Düzenle", "multimedya.video", "Yeni Canlı Yayın", "Canlı Yayın Düzenle", "Yeni Canlı Yayın",
                    f"Gündem › Siyaset · {kim} · 13.00'te başladı · şu an 4,8 B izleyici", "Planlandı · henüz kaydedilmedi · hazırlayan: oturumdaki kullanıcı",
                    ("multimedya.video", "Canlı Yayınlara Dön", "?sekme=tCanli"), SITE + "canli-yayin.html", "cyForm", "multimedya.canli", STD_SEKMELER, paneller, yan,
                    kaydet_cubugu("cyForm", "Kaydedildi · 24.11.2026 15.42 · Ayşe Yıldız", "Canlı yayın güncellendi; değişiklik oynatıcıda hemen görünür", "Canlı yayın planlandı; sitede “Yakında” olarak görünür", ana_yeni="Planla"),
                    ust_bant=f'<div class="kb-bant uyari kb-alt-bosluk" data-yeni-gizle>{ikon("fa-tower-broadcast")}<span><b>Yayın sürüyor.</b> Kaydettiğiniz başlık, açıklama ve kapak izleyicilere hemen yansır; yayın bağlantısını değiştirmek yayını keser.</span></div>')


def act_satir(ik, b, alt, sag, href=None, sira=None):
    ic = f'<span class="act-ico sira">{sira}</span>' if sira else f'<span class="act-ico">{ikon(ik)}</span>'
    ic_ = f'{ic}<span class="act-info"><b>{e(b)}</b><span>{alt}</span></span><span class="act-time">{sag}</span>'
    return f'<a class="act-row" href="{e(href)}">{ic_}</a>' if href else f'<div class="act-row">{ic_}</div>'


# =====================================================================
# 5 · Podcast (podcast.html: Seriler · Bölümler)
# =====================================================================
SERILER = [
    ("ekonomi-masasi", "Ekonomi Masası", "Finans", ["Can Demir", "Kerem Aksoy"], 42, "p163.jpg", "Haftalık · Perşembe", "yayinda", "48,2 B", "Enflasyon, faiz ve bütçe: haftanın ekonomisini masaya yatırıyoruz."),
    ("teknoloji-sohbetleri", "Teknoloji Sohbetleri", "Keşfet", ["Ozan Er"], 41, "p178.jpg", "Haftalık · Salı", "yayinda", "31,6 B", "Yapay zekâdan uzaya, gündelik hayatı değiştiren teknoloji."),
    ("saha", "Saha", "Gündem", ["Sibel Arslan", "Hakan Uysal"], 40, "p182.jpg", "Haftalık · Pazartesi", "yayinda", "27,9 B", "Muhabirlerimiz sahadan anlatıyor: deprem bölgesinden şantiyeye."),
    ("tribun", "Tribün", "Spor", ["Burak Tan", "Murat Tekin"], 39, "p188.jpg", "Haftada iki · Pazartesi, Cuma", "yayinda", "52,4 B", "Süper Lig'den Avrupa'ya haftanın maçları ve hesapları."),
    ("dunya-turu", "Dünya Turu", "Dünya", ["Zeynep Ak"], 27, "p193.jpg", "Haftalık · Çarşamba", "yayinda", "14,8 B", "Brüksel'den Washington'a dünyanın gündemi yarım saatte."),
    ("savunma-notlari", "Savunma Notları", "Savunma", ["Mert Yalın", "Tarık Bulut"], 22, "p122.jpg", "İki haftada bir · Cuma", "yayinda", "19,3 B", "Millî projeler, platformlar ve güvenlik politikası."),
    ("kampus-saati", "Kampüs Saati", "Kampüs", ["Selin Koç"], 18, "p203.jpg", "Haftalık · Cumartesi", "yayinda", "11,2 B", "Sınavlar, tercihler, burslar: gençlerin gündemi."),
    ("ev-ekonomisi", "Ev Ekonomisi", "Finans", ["Nazlı Öztürk"], 15, "p155.jpg", "Haftalık · Pazar", "yayinda", "9,7 B", "Aile bütçesi, faturalar, kira: evin hesabı."),
    ("kadin-gundemi", "Kadın Gündemi Sesli", "Kadın", ["Deniz Kara"], 0, "p192.jpg", "Haftalık · Perşembe", "taslak", "—", "Kadınların gündemi, haklar ve başarı hikâyeleri."),
    ("gece-kutuphanesi", "Gece Kütüphanesi", "Keşfet", ["İrem Su"], 3, "p164.jpg", "Aylık", "cop", "—", "Kitaplar ve yazarlar üzerine sohbetler."),
]
BOLUMLER = [
    ("Enflasyon sepetinde bu ay ne değişti?", "ekonomi-masasi", 42, 2280, "yayinda", "23.11.2026 12.05", "12,4 B"),
    ("Yapay zekâ haber odasına girerse", "teknoloji-sohbetleri", 41, 2640, "yayinda", "23.11.2026 10.50", "8,8 B"),
    ("Deprem bölgesinde üçüncü kış", "saha", 40, 1980, "yayinda", "23.11.2026 08.45", "1,1 B"),
    ("Süper Lig'de devre arası hesapları", "tribun", 39, 3120, "yayinda", "23.11.2026 12.35", "9,8 B"),
    ("Politika faizi sabit kaldı, sırada ne var", "ekonomi-masasi", 41, 2010, "yayinda", "23.11.2026 12.40", "2,2 B"),
    ("Kira artışında TÜFE ortalaması nasıl hesaplanır", "ekonomi-masasi", 40, 1740, "yayinda", "23.11.2026 12.55", "8,4 B"),
    ("Kira artışında yeni dönemin ilk ayı", "ekonomi-masasi", 39, 1860, "yayinda", "23.11.2026 15.35", "7,2 B"),
    ("Asgari ücret pazarlığı nasıl işliyor", "ekonomi-masasi", 38, 2220, "yayinda", "23.11.2026 11.55", "9,6 B"),
    ("Brüksel'deki göç pazarlığının arka planı", "dunya-turu", 27, 1920, "yayinda", "22.11.2026 18.00", "4,1 B"),
    ("Yerli hava savunma sistemlerinde son durum", "savunma-notlari", 22, 2460, "yayinda", "21.11.2026 17.00", "6,3 B"),
    ("Üniversite tercihinde bölüm mü şehir mi", "kampus-saati", 18, 1680, "yayinda", "22.11.2026 10.00", "3,9 B"),
    ("Aile bütçesinde kış faturalarına hazırlık", "ev-ekonomisi", 15, 1560, "yayinda", "23.11.2026 09.00", "5,2 B"),
    ("Bütçe 2027: vergi tarafında ne değişiyor?", "ekonomi-masasi", 43, 0, "zamanli", "27.11.2026 09.00", "—"),
    ("Derbi haftası: kadrolar ve sakatlar", "tribun", 40, 0, "taslak", "—", "—"),
]
SERI_AD = {s[0]: s for s in SERILER}


def podcast_sayfasi():
    sat = ""
    for s in SERILER:
        sid, ad, kat, sun, n, img, siklik, d, dinl, tanit = s
        href = "seri.html?id=" + sid
        nit = {"satir": sid, "durum": d, "kategori": kat, "ara": f"{ad} {kat} {' '.join(sun)}", "baslik": ad, "href": href}
        alt = f'{ikon("fa-microphone-lines")}{e(", ".join(sun))} · {e(siklik)}'
        if n and d != "cop":
            hedefler = "|".join(x[1] for x in SERILER if x[0] != sid and x[7] == "yayinda")
            sil = (f' data-tasi-sil data-sonra-kaldir data-tasi-ad="{e(ad)}" data-tasi-sayi="{n}" data-tasi-birim="bölüm" data-tasi-birim-cogul="bölümler" data-tasi-ikon="fa-microphone-lines"'
                   f' data-tasi-soru="Bölümler hangi seriye taşınsın?" data-tasi-hedefler="{e(hedefler)}"'
                   f' data-tasi-not="Bölümlerin adresi yeni seriye göre değişir, eski adresler yönlendirilir; RSS aboneleri yeni seride dinlemeye devam eder. “{e(ad)}” çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır."')
        else:
            sil = " data-sil"
        acts = eylemler(gor_href=SITE + "podcast-kategori.html" if d == "yayinda" else href, gor_site=d == "yayinda", duz_href=href, sil=sil, ad=ad)
        sat += satir(nit, [ana_hucre(ad, alt, img), kat_hucre(kat), durum_hucre(d), f'<td class="say kb-gizle-m">{n}</td>', f'<td class="say kb-gizle-t">{dinl}</td>'], acts)
    diger = (dm_yayin("Seri", "Seri ve bütün bölümleri sitede ve dinleme platformlarının RSS akışında görünmez olur; taslak olarak kalır, geri alınabilir.")
             + dm("Yeni bölüm ekle", "fa-plus", "yayinda taslak", hedef="multimedya.bolum", ek=' data-hedef-ek="?yeni=1"')
             + dm_ayir("yayinda") + dm_grup("Dağıtım", "yayinda")
             + dm("RSS Adresini Kopyala", "fa-rss", "yayinda", bildir="RSS adresi kopyalandı: dadahaber.com/podcast/…/rss")
             + dm("Bağlantıyı Kopyala", "fa-link", "yayinda", ek=" data-kopyala")
             + dm_icerik() + dm_kayit() + dm_cop())
    ko = [("Seri", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Bölüm", "say kb-gizle-m"), ("Dinlenme · 30 gün", "say kb-gizle-t")]
    l_seri = liste("ps", "seri", "Podcast serileri", [("hepsi", "Tümü", None), ("yayinda", "Yayında", None), ("taslak", "Taslak", None)], "Seri adı, sunucu ya da kategori ara",
                   kat_suz("ps"), f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen seriler yayından kaldırıldı">{ikon("fa-eye-slash")}<span>Yayından Kaldır</span></button>',
                   ko, sat, ("fa-podcast", "Henüz podcast serisi yok", "Önce bir seri oluşturun; bölümler serinin altında yayımlanır.",
                             f'<a class="pe-tag" data-hedef="multimedya.seri" data-hedef-ek="?yeni=1" href="#icerik">{ikon("fa-plus")}Yeni Seri</a>'),
                   "Podcast serileri yüklenemedi", diger, "podcast.html", cop_not="Seri sitede ve RSS akışında yayından kalkar ve Çöp sekmesine taşınır")
    # bölümler
    sat = ""
    for i, (b, sid, no, sn, d, z, dinl) in enumerate(BOLUMLER):
        s = SERI_AD[sid]
        href = "bolum.html?id=" + sid
        nit = {"satir": f"b{i}", "durum": d, "seri": s[1], "kategori": s[2], "ara": f"{b} {s[1]} {' '.join(s[3])}", "baslik": b, "href": href}
        alt = f'{ikon("fa-microphone-lines")}{e(s[1])} · {no}. bölüm · {sure_yaz(sn) if sn else "ses dosyası yok"}'
        acts = eylemler(gor_href=SITE + "podcast-detay.html" if d == "yayinda" else href, gor_site=d == "yayinda", duz_href=href, ad=b)
        sat += satir(nit, [ana_hucre(b, alt, s[5]), f'<td class="kb-gizle-m"><span class="kb-kat"><b>{e(s[1])}</b></span></td>', durum_hucre(d),
                           f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if d == "taslak" else ""}">{z}</span></td>', f'<td class="say kb-gizle-t">{dinl}</td>'], acts)
    seri_suz = secim("pbSuzSeri", "", [("", "Bütün Seriler")] + [(x[1], x[1]) for x in SERILER if x[7] != "cop"], suz="seri", etk="Seri:", ara="Seri ara", bos_metin="Bu adla seri yok.")
    diger_b = (dm_yayin("Bölüm", "Bölüm sitede ve dinleme platformlarında görünmez olur; taslak olarak kalır, geri alınabilir ve denetim izine yazılır.")
               + dm_dagitim(gomme=False) + dm_icerik() + dm_kayit() + dm_cop())
    ko_b = [("Bölüm", "kb-ana"), ("Seri", "kb-gizle-m"), ("Durum", ""), ("Yayın", "kb-gizle-m"), ("Dinlenme", "say kb-gizle-t")]
    l_bolum = liste("pb", "bölüm", "Podcast bölümleri", [("hepsi", "Tümü", None), ("yayinda", "Yayında", None), ("taslak", "Taslak", None), ("zamanli", "Zamanlanmış", None)],
                    "Bölüm başlığı, seri ya da sunucu ara", seri_suz,
                    f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen bölümler yayından kaldırıldı">{ikon("fa-eye-slash")}<span>Yayından Kaldır</span></button>',
                    ko_b, sat, ("fa-microphone-lines", "Henüz bölüm yok", "Bir seri seçip ilk bölümü yükleyin.",
                                f'<a class="pe-tag" data-hedef="multimedya.bolum" data-hedef-ek="?yeni=1" href="#icerik">{ikon("fa-plus")}Yeni Bölüm</a>'),
                    "Bölümler yüklenemedi", diger_b, "podcast.html?sekme=tBolum", cop_not="Bölüm sitede ve RSS akışında yayından kalkar ve Çöp sekmesine taşınır")
    yay = [s for s in SERILER if s[7] == "yayinda"]
    ust = sayfa_bas("<h1>Podcast</h1>", f'<div class="ph-sub">{len(yay)} seri yayında · {sum(s[4] for s in yay)} bölüm · son 30 günde {"229,1 B"} dinlenme</div>',
                    btn_link("multimedya.bolum", "Yeni Bölüm", "fa-plus", ek="?yeni=1") + "\n      " + btn_link("multimedya.seri", "Yeni Seri", "fa-plus", acc=True, ek="?yeni=1"))
    govde = (ust + '  <div data-sekmeli>\n  ' + sayfa_sekmeler([("tSeri", "fa-podcast", "Seriler", len(yay)), ("tBolum", "fa-microphone-lines", "Bölümler", sum(s[4] for s in yay))])
             + f'\n  <div class="sa-form-panel" id="tSeri">\n{l_seri}  </div>\n  <div class="sa-form-panel" id="tBolum" hidden>\n{l_bolum}  </div>\n  </div>\n')
    yaz("podcast.html", bas("Podcast", "multimedya.podcast") + govde + son())


# =====================================================================
# 6 · Podcast serisi düzenle (seri.html)
# =====================================================================
def seri_duzenle():
    sid, ad, kat, sun, n, img, siklik, d, dinl, tanit = SERILER[0]
    ai = ai_adim("#fBaslik,#fSpot", [("aciklama", "Açıklama Taslağı", True, None), ("seo", "SEO", True, None)],
                 "Seri adını ve kısa tanıtımı yazın; açıklama ve SEO bunlardan üretilir.")
    aciklama = ("<p>Ekonomi Masası, haftanın ekonomi gündemini yarım saatte anlatan Dada Haber podcast'idir. Can Demir ve Kerem Aksoy her perşembe enflasyon, faiz, "
                "bütçe ve çalışma hayatındaki gelişmeleri konuklarıyla birlikte ele alır.</p><p>Bölümlerde rakamların arkasındaki hikâyeyi ve <b>bana etkisi</b> sorusunun cevabını arıyoruz.</p>")
    sun_cip = "".join(f'<span class="kb-cip" data-deger="{e(a)}"><span>{e(a)}</span><button type="button" aria-label="Kaldır">{ikon("fa-xmark")}</button></span>' for a in sun)
    sik = secim("srSiklik", "haftalik", [("haftalik", "Haftalık"), ("iki-hafta", "İki Haftada Bir"), ("haftada-iki", "Haftada İki"), ("aylik", "Aylık"), ("duzensiz", "Düzensiz")])
    gun = secim("srGun", "persembe", [(g.lower().replace("ı", "i").replace("ş", "s").replace("ç", "c").replace("ü", "u"), g) for g in ("Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar")])
    icerik = f"""{gorsel_alan("srKapak", "multimedya.podcast", "Seri Kapağı", img, [("web.kart", "Kart · 1:1", "1:1", 200), ("web.detay", "Seri sayfası · 1:1", "1:1", 200)], ("mobil.kart", "Mobil kart · 16:9", "16:9", None),
             "kart <b>168×168</b>, seri sayfası <b>600×600</b>; Spotify ve Apple için en az <b>1400×1400</b>", "<b>358×201</b> (telefonda kart yatay)", "1400×1400",
             kaynak="Dada Haber · telif bizde", odak=(50, 45), ek_alt=" Bölüm kapağı ayrıca yüklenmezse bu kapak kullanılır.")}
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-sitemap")}Seri Bilgileri</div><div class="form-grid">
        <div class="frow two"><div class="frow"><span class="flabel">Ana Kategori</span>{kat_secim("srKat", kat)}<span class="fhint">Seri sayfası ve bölüm adresleri bu kategoriye göre kurulur.</span></div>
          <div class="frow"><span class="flabel">Sunucular</span><div class="kb-cip-girdi" data-havuz-yonet data-kullanim-birim="seride" data-havuz="{e(json.dumps(YAZARLAR, ensure_ascii=False))}">{sun_cip}<input type="text" placeholder="Kişi ara" aria-label="Sunucu ara"><div class="pnl-menu kb-cip-oneri"></div></div><span class="fhint">Havuzda yoksa aynı yerden eklenir; ⋯ ile adını düzeltin ya da silin.</span></div></div>
        <div class="frow two"><div class="frow"><span class="flabel">Yayın Sıklığı</span>{sik}</div><div class="frow"><span class="flabel">Yayın Günü</span>{gun}</div></div>
      </div></div>
{editor("Açıklama", aciklama, "Seri sayfasının başında ve dinleme platformlarında", ai_grup="aciklama")}
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-rss")}Dinleme Platformları<span class="fs-ek">RSS ile otomatik</span></div><div class="form-grid">
        <div class="frow"><span class="flabel">RSS Adresi</span><div class="slug-wrap"><span class="slug-pre">dadahaber.com/</span><input class="finput" value="podcast/ekonomi-masasi/rss" readonly aria-label="RSS Adresi"></div><span class="fhint">Spotify, Apple Podcasts ve YouTube Music bu adresten yeni bölümleri kendiliğinden alır.</span></div>
        {girdi("srSpotify", "Spotify Sayfası", "https://open.spotify.com/show/ekonomi-masasi", ph="https://open.spotify.com/show/…")}
        {girdi("srApple", "Apple Podcasts Sayfası", "https://podcasts.apple.com/tr/podcast/ekonomi-masasi", ph="https://podcasts.apple.com/…")}
        {girdi("srYt", "YouTube Music Sayfası", "", ph="https://music.youtube.com/playlist?list=…")}
        {toggle("Açık İçerik (Explicit) Değil", "Dinleme platformlarında aile filtresinden geçer")}
      </div></div>"""
    paneller = (detay_panel(baslik_spot(ad, tanit, b_not="Sitede seri adı; SEO başlığı buradan üretilir", s_etk="Kısa Tanıtım", s_not="Seri kartında ve platformlarda adın altında", s_sayac="120|160").replace('id="fBaslik" data-alan-id="baslik"', 'id="fBaslik" data-alan-id="ad"').replace("Başlık zorunlu", "Seri adı zorunlu").replace('<label for="fBaslik">Başlık</label>', '<label for="fBaslik">Seri Adı</label>') + ai + "\n" + icerik)
                + seo_panel("pSeo", "Ekonomi Masası podcast'i | Dada Haber", "Haftanın ekonomi gündemi yarım saatte: enflasyon, faiz, bütçe ve çalışma hayatı. Can Demir ve Kerem Aksoy ile her perşembe.",
                            "dadahaber.com/podcast/", "ekonomi-masasi", ["ekonomi podcast", "enflasyon podcast"],
                            toggle("Podcast Şeması (PodcastSeries)", "Google'da bölümleriyle görünür")))
    son_b = "".join(act_satir(None, b, f"{no}. bölüm · {sure_yaz(sn) if sn else 'ses dosyası yok'}", z.split(" ")[0] if z != "—" else "taslak", href="bolum.html?id=ekonomi-masasi", sira=no)
                    for b, s_, no, sn, dd, z, _ in sorted([x for x in BOLUMLER if x[1] == sid], key=lambda x: -x[2])[:5])
    yan = (yayin_kart(durum_secim("ycDurum", "yayinda", [("yayinda", "Yayında", ""), ("taslak", "Taslak", "seri ve bölümleri yayından kalkar")]), "2025-03-06 09.00",
                      toggle("Yeni Bölümde Bildirim", "Seriyi takip eden okura bölüm yayımlanınca", True, ek=' data-modul="etkilesim"')
                      + '<div class="sa-durum" data-yeni-gizle><div><span>Bölüm</span><b>42</b></div><div><span>Takipçi</span><b>6.418</b></div><div><span>Dinlenme · 30 gün</span><b>48,2 B</b></div></div>',
                      surum=(7, "20.11.2026 10.15", "Kerem Aksoy"))
           + f"""    <section class="pnl-card" data-yeni-gizle>
      <div class="pc-head"><h2 class="pc-title">{ikon("fa-microphone-lines")}Son Bölümler</h2><a class="kb-bag" data-hedef="multimedya.podcast" data-hedef-ek="?sekme=tBolum" href="#icerik">Tümü</a></div>
      <div class="act-list">{son_b}</div>
      <div class="kb-kap-alt-cubuk"><a class="btn btn-acc btn-sm" data-hedef="multimedya.bolum" data-hedef-ek="?yeni=1" href="#icerik">{ikon("fa-plus")}Yeni Bölüm</a></div>
    </section>
"""
           + seo_kart(88, [(True, "Seri adı ve tanıtım dolu"), (True, "Kapak 1400 px üstü"), (True, "RSS akışı geçerli"), (False, "YouTube Music bağlantısı yok")]))
    duzenle_sayfasi("seri.html", "Podcast Serisi Düzenle", "multimedya.podcast", "Yeni Podcast Serisi", "Podcast Serisi Düzenle", "Yeni Podcast Serisi",
                    f"Finans · {', '.join(sun)} · haftalık, perşembe · 42 bölüm · 30 günde 48,2 B dinlenme", "Taslak · henüz kaydedilmedi",
                    ("multimedya.podcast", "Podcast'e Dön"), SITE + "podcast-kategori.html", "srForm", "multimedya.seri",
                    [("pDetay", "fa-file-lines", "Detay", None), ("pSeo", "fa-magnifying-glass-chart", "SEO", None)], paneller, yan,
                    kaydet_cubugu("srForm", "Kaydedildi · 20.11.2026 10.15 · Kerem Aksoy", "Seri güncellendi; RSS akışı yenilendi", "Seri oluşturuldu; ilk bölümü ekleyebilirsiniz", ana_yeni="Oluştur"))


# =====================================================================
# 7 · Podcast bölümü düzenle (bolum.html)
# =====================================================================
def bolum_duzenle():
    b, sid, no, sn, d, z, dinl = BOLUMLER[0]
    s = SERI_AD[sid]
    img = s[5]
    ai = ai_adim("#fBaslik,#fSpot", [("aciklama", "Açıklama Taslağı", False, None), ("desifre", "Deşifre (Ses Dosyasından)", True, None), ("bolumler", "Zaman Damgaları", True, None),
                                     ("seo", "SEO", True, None), ("bildirim", "Bildirim Metni", True, "etkilesim"), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")],
                 "Başlığı ve spotu yazın; deşifre ve zaman damgaları ses dosyasından, diğerleri başlık ve spottan üretilir.")
    aciklama = ("<p>Ekim enflasyonu açıklandı; sepette en çok hangi kalemler pahalandı? Can Demir ve Kerem Aksoy, TÜİK verilerini gıda, kira ve ulaşım üzerinden okuyor; "
                "konuğumuz ekonomist Doç. Dr. Elif Aras ile asgari ücret ve kira artışlarına etkisini konuşuyor.</p>")
    desifre = ("<p><b>Can Demir:</b> Ekonomi Masası'na hoş geldiniz. Bu hafta masada ekim enflasyonu var.</p>"
               "<p><b>Kerem Aksoy:</b> Aylık rakam yüzde 2,1; yıllık tarafta yüzde 33,3'e geriledik. Ama sepetin içine bakınca tablo değişiyor.</p>"
               "<p><b>Elif Aras:</b> Gıdada mevsimsellik var, kirada ise yapışkanlık. Hane bütçesini en çok bu iki kalem zorluyor.</p>")
    zd = [("00.00", "Giriş: ekim rakamları"), ("03.40", "Gıda: sebze ve meyvede mevsim etkisi"), ("12.15", "Kira: yapışkan enflasyon"), ("24.30", "Asgari ücrete etkisi"), ("33.10", "Dinleyici soruları")]
    zd_html = "".join(f'<div class="km-satir" data-sira><button type="button" class="kb-tutamac" aria-label="Sırayı değiştir (sürükleyin ya da ok tuşları)">{ikon("fa-grip-vertical")}</button><span class="km-yazi">{e(t)}<small>{e(a)}</small></span><button type="button" class="ia-btn" data-satir-duzenle aria-label="Zaman damgasını düzenle">{ikon("fa-pen")}</button><button type="button" class="ia-btn danger" data-satir-sil aria-label="Zaman damgasını kaldır">{ikon("fa-trash")}</button></div>' for t, a in zd)
    konuk = '<span class="kb-cip" data-deger="Elif Aras"><span>Elif Aras</span><button type="button" aria-label="Kaldır">' + ikon("fa-xmark") + "</button></span>"
    seri_sec = secim("blSeri", s[1], [(x[1], x[1], f"{x[4]} bölüm") for x in SERILER if x[7] != "cop"], alan_id="seri", ara="Seri ara", bos="Seri seçin", zorunlu_metin="Bölümün serisini seçin", bos_metin="Bu adla seri yok.")
    icerik = f"""      <div class="form-sec">
        <div class="form-sec-tt">{ikon("fa-microphone-lines")}Ses<span class="fs-ek">MP3, M4A, WAV ya da OGG</span></div>
        <div class="form-grid">
          <div class="frow two"><div class="frow"><span class="flabel">Seri</span>{seri_sec}<span class="fhint">Yeni Seri <a class="kb-bag" data-hedef="multimedya.podcast" href="#icerik">Podcast</a> ekranından eklenir.</span></div>
            <div class="frow"><label for="blNo">Bölüm No</label><div class="kb-birim"><input class="finput" id="blNo" data-alan-id="bolum-no" inputmode="numeric" value="42"><span>. bölüm</span></div><span class="fhint">Seriden sıradaki numara kendiliğinden gelir.</span></div></div>
          <div class="frow"><span class="flabel">Ses Dosyası</span>{dosya_alan("ses", "Bölüm ses dosyası", "ses", ("ekonomi-masasi-42.mp3", 43253760, 2280), hata="Bölümün ses dosyasını yükleyin")}
            <span class="fhint">Süre dosyadan okunur: <b>38 dk 0 sn · 128 kbps</b>. Site Ayarları › Limitler: en fazla 200 MB.</span></div>
          <div class="frow"><span class="flabel">Konuklar</span><div class="kb-cip-girdi" data-havuz-yonet data-kullanim-birim="bölümde" data-havuz="{e(json.dumps(['Elif Aras', 'Prof. Dr. Hakan Kara', 'Doç. Dr. Selva Demiralp', 'Tolga Bayram'], ensure_ascii=False))}">{konuk}<input type="text" placeholder="Konuk ara ya da ekle" aria-label="Konuk ara"><div class="pnl-menu kb-cip-oneri"></div></div><span class="fhint">Konuk havuzu bu ekrandan yönetilir: ⋯ ile adını düzeltin ya da silin.</span></div>
          {yazar_secim("blYaz", "Kerem Aksoy")}
        </div>
      </div>
      <div class="form-sec" data-ai-grup="bolumler"><div class="form-sec-tt">{ikon("fa-list-ol")}Zaman Damgaları<span class="fs-ek">Oynatıcıda bölüm bölüm atlanır</span></div>
        <div class="kb-madde" data-satir-liste data-siralanir data-satir-ad="Zaman damgası" data-satir-alan1="Zaman (ör. 12.15)" data-satir-alan2="Başlık">{zd_html}<button type="button" class="kb-ekle-btn" data-satir-ekle>{ikon("fa-plus")}Zaman Damgası Ekle</button></div></div>
{gorsel_alan("blKapak", "multimedya.podcast", "Bölüm Kapağı", img, [("web.kart", "Kart · 1:1", "1:1", 200), ("web.detay", "Bölüm sayfası · 1:1", "1:1", 200)], ("mobil.kart", "Mobil kart · 16:9", "16:9", None),
             "kart <b>168×168</b>, bölüm sayfası <b>600×600</b>", "<b>358×201</b>", "1400×1400", kaynak="Seri kapağından", odak=(50, 45), alan_id=None,
             ek_alt=" Ayrı kapak yüklenmezse seri kapağı kullanılır.")}
{editor("Açıklama", aciklama, "Bölüm sayfasında ve dinleme platformlarında", ai_grup="aciklama")}
{editor("Deşifre", desifre, "Sitede “Deşifreyi oku” ile açılır; arama motorları bu metni okur", ai_grup="desifre", ikon_ad="fa-closed-captioning", fs_ek="Ses dosyasından üretilir, editör düzeltir")}
{okur_etkilesimi(toggle("Yorumlar Açık", "Yorumları editörler yönetir"), toggle("İndirilebilir", "Okur bölümü uygulamada çevrimdışı dinler"))}"""
    paneller = (detay_panel(baslik_spot(b, "Ekim enflasyonunda sepetin içine bakıyoruz: gıda, kira ve ulaşım. Konuğumuz ekonomist Elif Aras.") + ai + "\n" + icerik)
                + seo_panel("pSeo", "Enflasyon sepetinde bu ay ne değişti? | Ekonomi Masası", "Ekim enflasyonunda gıda, kira ve ulaşım: Ekonomi Masası'nın 42. bölümünde Can Demir ve Kerem Aksoy, konuk Elif Aras ile.",
                            "dadahaber.com/podcast/ekonomi-masasi/", "enflasyon-sepetinde-bu-ay-ne-degisti", ["enflasyon podcast", "ekim enflasyonu"],
                            toggle("Bölüm Şeması (PodcastEpisode)", "Google'da süre ve dinle düğmesiyle görünür"))
                + bildirim_panel("pBildirim", "Ekonomi Masası: Enflasyon sepetinde ne değişti?", "42. bölüm yayında: gıda, kira ve ulaşımda ekim rakamları. 38 dakika.", "Bölüm kapağının bildirim kırpımı (2:1)")
                + sosyal_panel("pSosyal", {"x": "🎧 Ekonomi Masası 42. bölüm: Enflasyon sepetinde bu ay ne değişti?\n\nhttps://dadahaber.com/podcast/ekonomi-masasi/42\n\n#enflasyon #podcast",
                                           "linkedin": "Ekonomi Masası'nın 42. bölümünde ekim enflasyonunu sepetin içinden okuyoruz: gıda, kira, ulaşım. Konuğumuz ekonomist Elif Aras.\n\nhttps://dadahaber.com/podcast/ekonomi-masasi/42",
                                           "telegram": "🎧 Yeni bölüm: Enflasyon sepetinde bu ay ne değişti?\n\nhttps://dadahaber.com/podcast/ekonomi-masasi/42"},
                               img, "#blKapak", (50, 45)))
    yan = (bildirim_onizle("pBildirim", "Ekonomi Masası: Enflasyon sepetinde ne değişti?", "42. bölüm yayında: gıda, kira ve ulaşımda ekim rakamları. 38 dakika.", img)
           + sosyal_onizle("pSosyal", img, b, (50, 45))
           + yayin_kart(durum_secim("ycDurum", "yayinda", YAYIN_DURUM), "2026-11-23 12.05",
                        '<div class="sa-durum" data-yeni-gizle><div><span>Dinlenme</span><b>12,4 B</b></div><div><span>Ortalama dinleme</span><b>24 dk</b></div><div><span>Spotify · Apple</span><b>RSS ile gönderildi</b></div></div>',
                        surum=(2, "23.11.2026 12.20", "Kerem Aksoy"))
           + seo_kart(90, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Deşifre var"), (True, "Zaman damgaları var")]))
    duzenle_sayfasi("bolum.html", "Podcast Bölümü Düzenle", "multimedya.podcast", "Yeni Podcast Bölümü", "Podcast Bölümü Düzenle", "Yeni Podcast Bölümü",
                    f"Ekonomi Masası · 42. bölüm · Kerem Aksoy · 23.11.2026 12.05'te yayımlandı · 12,4 B dinlenme", "Taslak · henüz kaydedilmedi · hazırlayan: oturumdaki kullanıcı",
                    ("multimedya.podcast", "Bölümlere Dön", "?sekme=tBolum"), SITE + "podcast-detay.html", "blForm", "multimedya.bolum", STD_SEKMELER, paneller, yan,
                    kaydet_cubugu("blForm", "Kaydedildi · 23.11.2026 12.20 · Kerem Aksoy", "Bölüm güncellendi; RSS akışı yenilendi", "Bölüm yayımlandı; sitede ve dinleme platformlarında görünür"))


# =====================================================================
# 8 · Sesli Haber ve Spiker (sesli.html: Haber Dinle · Spiker bültenleri)
# =====================================================================
SESLI = [dict(x, yazar=x.get("yazar") or "Dada Spiker") for x in tur_listesi("haber-dinle-detay.html")]
SES_LISTEDE = 14
BULTENLER = [
    ("aksam", "Akşam bülteni, 24 Kasım: günün 8 haberi", "Akşam Bülteni", "zamanli", "24.11.2026 18.00", 8, 0, "—"),
    ("gece", "Gece özeti, 24 Kasım", "Gece Özeti", "zamanli", "24.11.2026 22.30", 5, 0, "—"),
    ("ogle", "Öğle bülteni, 24 Kasım: sabahtan bu yana 8 haber", "Öğle Bülteni", "yayinda", "24.11.2026 12.30", 8, 548, "3,2 B"),
    ("sabah", "Sabah bülteni: güne başlamadan bilmen gereken 6 haber", "Sabah Bülteni", "yayinda", "24.11.2026 07.00", 6, 372, "5,8 B"),
    ("aksam-23", "Akşam bülteni, 23 Kasım: günün 8 haberi 9 dakikada", "Akşam Bülteni", "yayinda", "23.11.2026 18.00", 8, 544, "7,1 B"),
    ("gece-23", "Gece özeti, 23 Kasım", "Gece Özeti", "yayinda", "23.11.2026 22.30", 5, 301, "2,4 B"),
    ("hafta", "Hafta özeti: haftanın on gelişmesi, kaynaklarıyla", "Hafta Özeti", "yayinda", "22.11.2026 10.00", 10, 905, "9,6 B"),
    ("ozel", "Özel bülten: deprem bölgesinde üçüncü kış", "Özel Bülten", "taslak", "—", 4, 0, "—"),
    ("ogle-22", "Öğle bülteni, 22 Kasım (ses hatalı)", "Öğle Bülteni", "cop", "22.11.2026 12.30", 8, 530, "—"),
]
PROGRAMLAR = [("Sabah Bülteni", "07.00 · 6 dk · güne başlamadan bilinmesi gerekenler"), ("Öğle Bülteni", "12.30 · 9 dk · sabahtan bu yana öne çıkan sekiz haber"),
              ("Akşam Bülteni", "18.00 · 9 dk · günün öne çıkan sekiz haberi"), ("Gece Özeti", "22.30 · 5 dk · günün kısa özeti ve yarının takvimi"),
              ("Hafta Özeti", "Pazar 10.00 · 15 dk · haftanın on gelişmesi, kaynaklarıyla")]


def km_satir(baslik, alt, ad, img=None, tutamac=True, duzenle=True):
    t = f'<button type="button" class="kb-tutamac" aria-label="Sırayı değiştir (sürükleyin ya da ok tuşları)">{ikon("fa-grip-vertical")}</button>' if tutamac else ""
    th = f'<span class="rcp-thumb" style="background-image:url(../../veri/gorsel/kucuk/{img})"></span>' if img else ""
    dz = f'<button type="button" class="ia-btn" data-satir-duzenle aria-label="{ad} düzenle">{ikon("fa-pen")}</button>' if duzenle else ""
    return (f'<div class="km-satir" data-sira>{t}{th}<span class="km-yazi">{e(baslik)}<small>{e(alt)}</small></span>{dz}'
            f'<button type="button" class="ia-btn danger" data-satir-sil aria-label="{ad} kaldır">{ikon("fa-trash")}</button></div>')


def sesli_sayfasi():
    sat, sab = "", ""
    for i, x in enumerate(SESLI[:SES_LISTEDE]):
        d = "hazirlaniyor" if i == 0 else ("taslak" if i == 9 else "yayinda")
        ses = "Stüdyo kaydı · Hande Polat" if i in (3, 7) else ("Dada Spiker · erkek sesi" if i % 4 == 1 else "Dada Spiker · kadın sesi")
        sn = 120 + h(x["baslik"], 160)
        tid = f"shV{i}"
        nit = {"satir": f"s{i}", "durum": d, "kategori": x["bolum"], "ara": f'{x["baslik"]} {x["bolum"]} {x["yazar"]} {ses}', "baslik": x["baslik"]}
        alt = f'{ikon("fa-headphones")}{sure_yaz(sn)} · {e(x["yazar"])}'
        acts = eylemler(gor_tanim=tid, duz_tanim=tid, ad=x["baslik"])
        sat += satir(nit, [ana_hucre(x["baslik"], alt), kat_hucre(x["bolum"], x.get("alt_konu")), f'<td class="kb-gizle-m"><span class="kb-kat">{e(ses)}</span></td>', durum_hucre(d),
                           f'<td class="say kb-gizle-t">{e(x.get("goruntulenme", "—")) if d == "yayinda" else "—"}</td>'], acts)
        dosya = f'haber-dinle-{h(x["baslik"], 9000) + 1000}.mp3'
        studyo = "Stüdyo" in ses
        sab += f"""<template id="{tid}" data-baslik="Sesli Haber" data-alt="{e(x["baslik"])}">
  <div class="kb-fs"><div class="kb-fs-tt">Ses</div>
    <div class="kb-dosya" data-tur="ses" data-ad="Sesli Haber">{'' if d == "hazirlaniyor" else f'<div class="kb-dosya-oge" data-ad="{dosya}" data-boyut="{sn * 16000}" data-sure="{sn}"></div>'}</div>
    {f'<p class="fhint">{ikon("fa-spinner fa-spin")} Dada Spiker seslendiriyor; yaklaşık 1 dakika içinde hazır olur.</p>' if d == "hazirlaniyor" else ""}
    <dl class="kb-ozet-dl"><dt>Haber</dt><dd>{e(x["baslik"])}</dd><dt>Kategori</dt><dd>{e(x["bolum"])}</dd><dt>Yazar</dt><dd>{e(x["yazar"])}</dd><dt>Yayın</dt><dd>{tarih(x["tarih"], x["saat"])}</dd><dt>Dinlenme</dt><dd>{e(x.get("goruntulenme", "—")) if d == "yayinda" else "—"}</dd></dl></div>
  <div class="kb-fs"><div class="kb-fs-tt">Seslendirme · Dada Spiker</div>
    <div class="frow"><div class="kb-secenek-grup">
      <label class="kb-secenek"><input type="radio" name="{tid}S"{"" if studyo else " checked"}>Kadın Sesi</label>
      <label class="kb-secenek"><input type="radio" name="{tid}S">Erkek Sesi</label>
      <label class="kb-secenek"><input type="radio" name="{tid}S" data-ac="{tid}St"{" checked" if studyo else ""}>Stüdyo Kaydı</label></div></div>
    <div class="frow" id="{tid}St"{"" if studyo else " hidden"}><span class="flabel">Stüdyo Kaydı</span><div class="kb-dosya" data-tur="ses" data-ad="Stüdyo Kaydı">{f'<div class="kb-dosya-oge" data-ad="studyo-{dosya}" data-boyut="{sn * 20000}" data-sure="{sn}"></div>' if studyo else ""}</div></div>
    <div class="frow"><span class="flabel">Okuma Hızı</span>{secim(tid + "H", "1", [("0.9", "Yavaş · 0,9×"), ("1", "Normal · 1×"), ("1.1", "Hızlı · 1,1×")])}</div>
    {toggle("Haber Güncellenince Yeniden Seslendir", "Güncelleme ve düzeltme notu da okunur")}
    <p class="fhint">Okuma metni haber metninden gelir; düzeltme <a class="kb-bag" data-hedef="haberler.duzenle" data-modul="haberler" href="#icerik">Haber düzenle</a> ekranında yapılır.</p></div>
  <div class="kb-kap-alt-cubuk">
    <button type="button" class="btn btn-ghost btn-sm"{onay("Yeniden seslendirilsin mi?", "Mevcut ses dosyası sürüm geçmişine alınır; Dada Spiker haber metnini baştan okur (yaklaşık 1 dakika). Bu sürede sitede önceki ses çalar.", "Yeniden Seslendir", "fa-rotate", sonra="Yeniden seslendirme başladı; hazır olunca bildirim gelir")}>{ikon("fa-rotate")}Yeniden Seslendir</button>
    <button type="button" class="btn btn-acc btn-sm" data-kapat data-bildir-hemen="Seslendirme ayarı kaydedildi">{ikon("fa-check")}Kaydet</button>
  </div>
</template>
"""
    diger = (dm_grup("Ses", "yayinda taslak hazirlaniyor")
             + dm("Yeniden Seslendir", "fa-rotate", "yayinda taslak", ek=onay("Yeniden seslendirilsin mi?", "Mevcut ses sürüm geçmişine alınır; Dada Spiker haber metnini baştan okur (yaklaşık 1 dakika).", "Yeniden Seslendir", "fa-rotate",
                                                                            sonra="Yeniden seslendirme başladı", sonra_durum=("hazirlaniyor", "Seslendiriliyor", "wait")))
             + dm("Sitede “Haberi Dinle”yi Kapat", "fa-volume-xmark", "yayinda", ek=onay("“Haberi dinle” kapatılsın mı?", "Haberin sayfasındaki dinle düğmesi ve Haber Dinle listesindeki satırı kalkar; ses dosyası silinmez, geri açılabilir.", "Kapat", "fa-volume-xmark", tehlike=True, sonra="Sesli hali kapatıldı; taslak olarak duruyor", sonra_durum=("taslak", "Taslak", "off")))
             + dm("Sitede “Haberi Dinle”yi Aç", "fa-volume-high", "taslak", ek=onay("“Haberi dinle” açılsın mı?", "Haberin sayfasında dinle düğmesi ve Haber Dinle listesinde satırı görünür.", "Aç", "fa-volume-high", sonra="Sesli hali yayında", sonra_durum=("yayinda", "Yayında", "ok")))
             + dm_ayir("yayinda") + dm("Haberi düzenle", "fa-newspaper", "yayinda taslak", hedef="haberler.duzenle", modul="haberler")
             + dm("Bağlantıyı Kopyala", "fa-link", "yayinda", ek=" data-kopyala")
             + dm_ayir() + dm_kayit() + dm_cop())
    seslendirme_suz = secim("shSuzSes", "", [("", "Bütün Sesler"), ("Dada Spiker · kadın sesi", "Dada Spiker · kadın"), ("Dada Spiker · erkek sesi", "Dada Spiker · erkek"), ("Stüdyo kaydı · Hande Polat", "Stüdyo Kaydı")], suz="ses", etk="Ses:")
    # ses süzgeci satırın data-ses değerini arar
    sat = re.sub(r'data-satir="s(\d+)" ', lambda m: m.group(0), sat)
    for i, x in enumerate(SESLI[:SES_LISTEDE]):
        ses = "Stüdyo kaydı · Hande Polat" if i in (3, 7) else ("Dada Spiker · erkek sesi" if i % 4 == 1 else "Dada Spiker · kadın sesi")
        sat = sat.replace(f'data-satir="s{i}" ', f'data-satir="s{i}" data-ses="{e(ses)}" ', 1)
    ko = [("Sesli Haber", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Seslendirme", "kb-gizle-m"), ("Durum", ""), ("Dinlenme", "say kb-gizle-t")]
    l_haber = liste("sh", "sesli haber", "Sesli haberler", [("hepsi", "Tümü", len(SESLI) - SES_LISTEDE), ("yayinda", "Yayında", len(SESLI) - SES_LISTEDE), ("hazirlaniyor", "Seslendiriliyor", None), ("taslak", "Kapalı", None)],
                    "Haber başlığı, kategori ya da yazar ara", kat_suz("sh") + seslendirme_suz,
                    f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="yeniden" data-bildir="Seçilen haberler yeniden seslendirilmek üzere sıraya alındı">{ikon("fa-rotate")}<span>Yeniden Seslendir</span></button>',
                    ko, sat, ("fa-headphones", "Henüz sesli haber yok", "Haber düzenle ekranında “Haberi dinle” açık olan haberler Dada Spiker ile seslendirilir ve burada listelenir.", ""),
                    "Sesli haberler yüklenemedi", diger, "sesli.html", toplam=len(SESLI),
                    cop_not="Haberin sesli hali kalkar (haber yayında kalır) ve Çöp sekmesine taşınır",
                    ust_ek=f'<div class="kb-bant bilgi">{ikon("fa-circle-info")}<span>Sesli haber, haberin <b>Dada Spiker</b> ile okunmuş halidir; haber yayımlanınca kendiliğinden seslendirilir. Satıra tıklayınca seslendirme ayarı açılır.</span></div>')
    # bültenler
    sat = ""
    for bid, b, prog, d, z, n, sn, dinl in BULTENLER:
        href = "sesli-duzenle.html?id=" + bid
        nit = {"satir": "b-" + bid, "durum": d, "program": prog, "ara": f"{b} {prog}", "baslik": b, "href": href}
        alt = f'{ikon("fa-microphone-lines")}{e(prog)} · {n} haber · {sure_yaz(sn) if sn else "henüz seslendirilmedi"}'
        acts = eylemler(gor_href=SITE + "haber-dinle-detay.html" if d == "yayinda" else href, gor_site=d == "yayinda", duz_href=href, ad=b)
        sat += satir(nit, [ana_hucre(b, alt), durum_hucre(d), f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if d in ("taslak", "cop") else ""}">{z}</span></td>',
                           f'<td class="say kb-gizle-t">{dinl}</td>'], acts)
    prog_suz = secim("sbSuzProg", "", [("", "Bütün Programlar")] + [(p, p) for p, _ in PROGRAMLAR] + [("Özel Bülten", "Özel Bülten")], suz="program", etk="Program:")
    diger_b = (dm_yayin("Bülten", "Bülten Haber Dinle sayfasından ve Spiker panelinden kalkar; taslak olarak kalır, geri alınabilir.")
               + dm_ayir("yayinda") + dm_grup("Dağıtım", "yayinda")
               + dm("Bildirim Gönder", "fa-bell", "yayinda", modul="etkilesim", bildir="Bildirim sekmesi düzenleme ekranında (prototip)")
               + dm("Bağlantıyı Kopyala", "fa-link", "yayinda", ek=" data-kopyala")
               + dm_icerik() + dm_kayit() + dm_cop())
    ko_b = [("Bülten", "kb-ana"), ("Durum", ""), ("Yayın", "kb-gizle-m"), ("Dinlenme", "say kb-gizle-t")]
    l_bulten = liste("sb", "bülten", "Spiker Bültenleri", [("hepsi", "Tümü", None), ("yayinda", "Yayında", None), ("zamanli", "Zamanlanmış", None), ("taslak", "Taslak", None)],
                     "Bülten adı ya da program ara", prog_suz,
                     f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen bültenler yayından kaldırıldı">{ikon("fa-eye-slash")}<span>Yayından Kaldır</span></button>',
                     ko_b, sat, ("fa-microphone-lines", "Henüz bülten yok", "Yayın saatleri tanımlıysa bültenler kendiliğinden hazırlanır; özel bülten de buradan eklenir.",
                                 f'<a class="pe-tag" data-hedef="multimedya.sesli-duzenle" data-hedef-ek="?yeni=1" href="#icerik">{ikon("fa-plus")}Yeni Bülten</a>'),
                     "Bültenler yüklenemedi", diger_b, "sesli.html?sekme=tBulten", cop_not="Bülten Haber Dinle'den ve Spiker panelinden kalkar ve Çöp sekmesine taşınır",
                     ust_ek=f'<div class="kb-bant bilgi">{ikon("fa-circle-info")}<span>Bültenler yayın saatinden 20 dakika önce son haberlerle kendiliğinden hazırlanır ve editör onayına düşer; onaylanmayan bülten yayımlanmaz.</span></div>')
    prog = "".join(km_satir(p, a, "Program") for p, a in PROGRAMLAR)
    sab += f"""<template id="sbProgramlar" data-baslik="Yayın Saatleri" data-alt="Spiker bülteni programları · sitede Haber Dinle › Yayın akışında görünür">
  {kap_dil()}
  <div class="kb-fs"><div class="kb-fs-tt">Programlar</div>
    <div class="kb-madde" data-satir-liste data-siralanir data-satir-ad="Program" data-satir-alan1="Program adı" data-satir-alan2="Saat · süre · içerik">{prog}<button type="button" class="kb-ekle-btn" data-satir-ekle>{ikon("fa-plus")}Program Ekle</button></div>
    <p class="fhint">Program kaldırılınca o saatin bülteni artık hazırlanmaz; yayımlanmış bültenler arşivde kalır.</p></div>
  <div class="kb-fs"><div class="kb-fs-tt">Hazırlama</div>
    <div class="frow"><span class="flabel">Kendiliğinden Hazırla</span>{secim("sbOnce", "20", [("10", "Yayından 10 Dk Önce"), ("20", "Yayından 20 Dk Önce"), ("30", "Yayından 30 Dk Önce")])}</div>
    {toggle("Editör Onayı Olmadan Yayımlama", "Hazırlanan bülten onay bekler; onaylanmazsa yayımlanmaz")}</div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-kapat data-bildir-hemen="Yayın saatleri kaydedildi; Haber Dinle › Yayın akışı güncellendi">{ikon("fa-check")}Kaydet</button></div>
</template>
"""
    ust = sayfa_bas("<h1>Sesli Haber ve Spiker</h1>", f'<div class="ph-sub">{len(SESLI)} sesli haber · bugün 2 bülten yayında, 2 bülten zamanlandı · seslendirme: Dada Spiker</div>',
                    f'<button type="button" class="btn btn-ghost btn-sm" data-tanim="sbProgramlar">{ikon("fa-clock")}Yayın Saatleri</button>\n      '
                    + btn_link("multimedya.sesli-duzenle", "Yeni Bülten", "fa-plus", acc=True, ek="?yeni=1"))
    govde = (ust + '  <div data-sekmeli>\n  ' + sayfa_sekmeler([("tHaber", "fa-headphones", "Haber Dinle", len(SESLI)), ("tBulten", "fa-microphone-lines", "Spiker Bültenleri", 7)])
             + f'\n  <div class="sa-form-panel" id="tHaber">\n{l_haber}  </div>\n  <div class="sa-form-panel" id="tBulten" hidden>\n{l_bulten}  </div>\n  </div>\n')
    yaz("sesli.html", bas("Sesli Haber ve Spiker", "multimedya.sesli") + govde + son(sab))


# =====================================================================
# 9 · Spiker bülteni düzenle (sesli-duzenle.html)
# =====================================================================
def sirali(satirlar_, haberler, dolu):
    sar = " data-yeni-gizle" if dolu else " data-yeni-goster hidden"
    var = [y["baslik"] for y in haberler]
    sec = secim("sdHaberEkle" + ("D" if dolu else "B"), "", [(x["baslik"], x["baslik"], x["bolum"]) for x in HABER_SEC[:20] if x["baslik"] not in var],
                ara="Haber başlığı ara", bos="Haber ekle", bos_metin="Bu başlıkla haber yok.", ek=' data-sirali-kaynak data-yer="Haber ekle"')
    return (f'<div{sar}><div class="kb-sirali" data-sirali-havuz data-sinir="10" data-sirali-ad="Haber" data-alan-id="haberler" data-zorunlu-metin="Bültene en az bir haber ekleyin">'
            f'<div class="kb-madde" data-siralanir>{satirlar_}</div>{sec}</div></div>')


def sesli_duzenle():
    bid, b, prog, d, z, n, sn, dinl = BULTENLER[4]
    haberler = [x for x in SESLI if x["tarih"] == "2026-11-23" and not re.search(r"bülten|özet", x["baslik"], re.I)][:8]
    satirlar_ = "".join(f'<div class="km-satir" data-sira data-deger="{e(x["baslik"])}" data-ad="{e(x["baslik"])}" data-alt="{e(x["bolum"])} · {sure_yaz(50 + h(x["baslik"], 40))} okuma"></div>' for x in haberler)
    okuma = ("<p>İyi akşamlar, Dada Haber akşam bülteninde bugün sekiz başlık var.</p>"
             + "".join(f"<p><b>{e(x['bolum'])}.</b> {e(x['baslik'])}.</p>" for x in haberler[:4])
             + "<p>Bültenin tamamı ve kaynaklar dadahaber.com'da. İyi akşamlar.</p>")
    ai = ai_adim("#fBaslik,#fSpot", [("okuma", "Okuma Metni (Seçilen Haberlerden)", True, None), ("seo", "SEO", True, None), ("bildirim", "Bildirim Metni", True, "etkilesim")],
                 "Başlığı ve spotu yazın; okuma metni seçilen haberlerin spotlarından üretilir. Üretilen bölüm “AI önerisi” etiketiyle gelir.")
    prog_sec = secim("sdProg", prog, [(p, p, a.split(" · ")[0]) for p, a in PROGRAMLAR] + [("Özel Bülten", "Özel Bülten", "saati serbest")], ara="Program ara", bos="Program seçin")
    icerik = f"""      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-list-ol")}Bültendeki Haberler<span class="fs-ek">Okuma sırası; sürükleyerek değiştirin</span></div>
        <div class="form-grid">
          <div class="frow"><span class="flabel">Program</span>{prog_sec}<span class="fhint">Saatler <a class="kb-bag" data-hedef="multimedya.sesli" href="#icerik">Sesli Haber › Yayın saatleri</a>'nden yönetilir.</span></div>
          <div class="frow" data-modul="haberler"><span class="flabel">Haberler</span>
            {sirali(satirlar_, haberler, True)}{sirali("", [], False)}
            <span class="fhint">Bir bültende en çok 10 haber; toplam okuma süresi 9 dakikayı geçmesin. Kaldırılan haber “Geri al” ile döner.</span></div>
        </div></div>
{editor("Okuma Metni", okuma, "Spiker bu metni okur; köşeli parantez içi [duraklama] okunmaz", ai_grup="okuma", alan_id="okuma-metni", ikon_ad="fa-microphone-lines", fs_ek="Haberlerin spotlarından üretilir")}
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-headphones")}Ses ya da Video</div><div class="form-grid">
        <div class="frow"><span class="flabel">Seslendirme</span><div class="kb-secenek-grup">
          <label class="kb-secenek"><input type="radio" name="sdSes" data-ac="sdSpiker" checked>Dada Spiker (Yapay Ses)</label>
          <label class="kb-secenek"><input type="radio" name="sdSes" data-ac="sdStudyo">Stüdyo Kaydı</label>
          <label class="kb-secenek"><input type="radio" name="sdSes" data-ac="sdVideo">Video Bülten</label></div></div>
        <div class="frow" id="sdSpiker"><span class="flabel">Dada Spiker</span>
          <div class="frow two"><div class="frow">{secim("sdSesTur", "kadin", [("kadin", "Kadın Sesi"), ("erkek", "Erkek Sesi")])}</div><div class="frow">{secim("sdHiz", "1", [("0.9", "Yavaş · 0,9×"), ("1", "Normal · 1×"), ("1.1", "Hızlı · 1,1×")])}</div></div>
          <div data-yeni-gizle><div class="kb-dosya" data-tur="ses" data-ad="Oluşturulan ses"><div class="kb-dosya-oge" data-ad="aksam-bulteni-2311.mp3" data-boyut="8704000" data-sure="544"></div></div></div>
          <span class="fhint">Okuma metni değişince “Seslendir” yeniden okur. <button type="button" class="kb-bag"{onay("Bülten seslendirilsin mi?", "Dada Spiker okuma metnini baştan okur (yaklaşık 1 dakika); önceki ses sürüm geçmişine alınır.", "Seslendir", "fa-microphone-lines", sonra="Seslendirme başladı; hazır olunca ses alanına gelir")}>Seslendir</button></span></div>
        <div class="frow" id="sdStudyo" hidden><span class="flabel">Stüdyo Kaydı</span>{dosya_alan("ses", "Stüdyo Kaydı", "ses", hata="Stüdyo kaydını yükleyin")}<span class="fhint">Spiker: <b>Hande Polat</b> · MP3 ya da WAV</span></div>
        <div class="frow" id="sdVideo" hidden><span class="flabel">Video Bülten</span>{dosya_alan("video", "Video Bülten", "ses", hata="Video bülteni yükleyin")}<span class="fhint">Video Spiker panelinde ve Haber Dinle'de oynar; ses ayrıca çıkarılır.</span></div>
      </div></div>"""
    paneller = (detay_panel(baslik_spot(b, "Bütçe görüşmeleri, kar yağışı ve asgari ücret: günün sekiz haberi dokuz dakikada.", s_not="Haber Dinle listesinde ve Spiker panelinde") + ai + "\n" + icerik)
                + seo_panel("pSeo", "Akşam bülteni, 23 Kasım: günün 8 haberi | Dada Haber", "Günün öne çıkan sekiz haberi dokuz dakikada: bütçe görüşmeleri, Marmara'da kar ve asgari ücret. Dada Haber akşam bülteni.",
                            "dadahaber.com/haber-dinle/", "aksam-bulteni-23-kasim", ["akşam bülteni", "sesli haber"])
                + bildirim_panel("pBildirim", "Akşam bülteni hazır: günün 8 haberi", "Bütçe, kar yağışı ve asgari ücret: dokuz dakikada dinle.", "Marka şablonundaki bülten görseli", "2026-11-23 18.00"))
    yan = (bildirim_onizle("pBildirim", "Akşam bülteni hazır: günün 8 haberi", "Bütçe, kar yağışı ve asgari ücret: dokuz dakikada dinle.", None)
           + yayin_kart(durum_secim("ycDurum", "yayinda", YAYIN_DURUM), "2026-11-23 18.00",
                        toggle("Spiker Panelinde Göster", "Her sayfadaki Spiker panelinde en son bülten olarak")
                        + '<div class="sa-durum" data-yeni-gizle><div><span>Süre</span><b>9 dk 4 sn</b></div><div><span>Dinlenme</span><b>7,1 B</b></div><div><span>Onaylayan</span><b>Ayşe Yıldız</b></div></div>',
                        surum=(2, "23.11.2026 17.52", "Ayşe Yıldız"))
           + seo_kart(80, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Okuma metni sayfada"), (False, "Görsel yok (sitede görselsiz satır)")]))
    duzenle_sayfasi("sesli-duzenle.html", "Spiker Bülteni Düzenle", "multimedya.sesli", "Yeni Bülten", "Spiker Bülteni Düzenle", "Yeni Bülten",
                    "Akşam bülteni · 8 haber · 9 dk 4 sn · 23.11.2026 18.00'de yayımlandı · 7,1 B dinlenme", "Taslak · henüz kaydedilmedi",
                    ("multimedya.sesli", "Bültenlere Dön", "?sekme=tBulten"), SITE + "haber-dinle-detay.html", "sdForm", "multimedya.sesli",
                    [("pDetay", "fa-file-lines", "Detay", None), ("pSeo", "fa-magnifying-glass-chart", "SEO", None), ("pBildirim", "fa-bell", "Bildirim", "etkilesim")], paneller, yan,
                    kaydet_cubugu("sdForm", "Kaydedildi · 23.11.2026 17.52 · Ayşe Yıldız", "Bülten güncellendi; Haber Dinle'de yayında", "Bülten yayımlandı; Haber Dinle'de ve Spiker panelinde görünür"))


# =====================================================================
# 10 · Galeri ve İnfografik (galeri.html: Foto Galeri · İnfografik)
# =====================================================================
GALERILER = [dict(x, yazar=x.get("yazar") or "Dada Haber") for x in tur_listesi("foto-fokus-detay.html")]
INFOGRAFIKLER = [dict(x, yazar=x.get("yazar") or "Dada Haber") for x in tur_listesi("infografik-detay.html")]
_ff = (PUB / "foto-fokus.html").read_text(encoding="utf-8")
FOTO_SAY, KOLAJ = {}, {}
for m in re.finditer(r'<(?:a|article) class="gk[^"]*"(.*?)</(?:a|article)>', _ff, flags=re.S):
    tx = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split())
    s = re.search(r"(\d+) fotoğraf (.+)$", tx)
    if s:
        FOTO_SAY[s.group(2).replace("’", "'")] = int(s.group(1))
        KOLAJ[s.group(2).replace("’", "'")] = [x for x in re.findall(r"assets/gorsel/(p\d+\.jpg)", m.group(1)) if x in GORSELLER][:3]


def galeri_sayfasi():
    sat = ""
    kay = [dict(x, durum="yayinda") for x in GALERILER]
    kay = [{"baslik": "Erciyes'te kayak sezonu açılış hazırlıkları", "bolum": "Keşfet", "alt_konu": "Şehir", "yazar": "Ozan Er", "tarih": "2026-11-24", "saat": "", "durum": "taslak"},
           {"baslik": "Derbi gününden kareler", "bolum": "Spor", "alt_konu": "Futbol", "yazar": "Gizem Aktaş", "tarih": "2026-11-25", "saat": "22.30", "durum": "zamanli"}] + kay + \
          [{"baslik": "Deneme albümü (yinelenen kareler)", "bolum": "Keşfet", "alt_konu": "Şehir", "yazar": "İrem Su", "tarih": "2026-11-20", "saat": "10.00", "durum": "cop"}]
    for i, g in enumerate(kay):
        d = g["durum"]
        n = FOTO_SAY.get(g["baslik"], 12 + h(g["baslik"], 20))
        img = (KOLAJ.get(g["baslik"]) or [g_of(g["baslik"])])[0]
        href = "galeri-duzenle.html?id=galeri"
        nit = {"satir": f"g{i}", "durum": d, "kategori": g["bolum"], "yazar": g["yazar"], "ara": f'{g["baslik"]} {g["yazar"]} {g["bolum"]} {g.get("alt_konu") or ""}', "baslik": g["baslik"], "href": href,
               "kullanim": "Foto Fokus vitrininde ve bir haberin içinde gömülü; oradan da kalkar" if i == 2 else None}
        alt = f'{ikon("fa-images")}{n} fotoğraf · {e(g["yazar"])}'
        acts = eylemler(gor_href=SITE + "foto-fokus-detay.html" if d == "yayinda" else href, gor_site=d == "yayinda", duz_href=href, ad=g["baslik"])
        sat += satir(nit, [ana_hucre(g["baslik"], alt, img), kat_hucre(g["bolum"], g.get("alt_konu")), durum_hucre(d),
                           f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if d in ("taslak", "cop") else ""}">{tarih(g["tarih"], g["saat"]) if g.get("saat") else "—"}</span></td>',
                           f'<td class="say kb-gizle-t">{e(g.get("goruntulenme", "—")) if d == "yayinda" else "—"}</td>'], acts)
    diger = (dm_yayin("Galeri", "Galeri Foto Fokus'tan ve gömülü olduğu haberlerden kalkar; taslak olarak kalır, geri alınabilir ve denetim izine yazılır.")
             + dm_dagitim() + dm_icerik()
             + dm_kayit() + dm_cop())
    ko = [("Galeri", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Yayın", "kb-gizle-m"), ("Görüntülenme", "say kb-gizle-t")]
    l_gal = liste("fg", "galeri", "Foto galeriler", [("hepsi", "Tümü", None), ("yayinda", "Yayında", None), ("taslak", "Taslak", None), ("zamanli", "Zamanlanmış", None)],
                  "Galeri adı, fotoğrafçı ya da kategori ara", kat_suz("fg") + yazar_suz("fg", [x["yazar"] for x in kay]),
                  f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen galeriler yayından kaldırıldı">{ikon("fa-eye-slash")}<span>Yayından Kaldır</span></button>',
                  ko, sat, ("fa-images", "Henüz galeri yok", "Fotoğrafları medya havuzundan seçin ya da yükleyin; galeri Foto Fokus'ta yayımlanır.",
                            f'<a class="pe-tag" data-hedef="multimedya.galeri-duzenle" data-hedef-ek="?yeni=1" href="#icerik">{ikon("fa-plus")}Yeni Galeri</a>'),
                  "Galeriler yüklenemedi", diger, "galeri.html", cop_not="Foto Fokus'tan ve gömülü olduğu haberlerden kalkar ve Çöp sekmesine taşınır")
    # infografik
    sat = ""
    kay = [dict(x, durum="yayinda") for x in INFOGRAFIKLER] + [
        {"baslik": "Bölgelere göre konut fiyat artışı", "bolum": "Finans", "alt_konu": "Gayrimenkul", "yazar": "Nazlı Öztürk", "tarih": "2026-11-24", "saat": "", "durum": "taslak"},
        {"baslik": "Eski taslak: yıllık turist sayısı", "bolum": "Keşfet", "alt_konu": "Seyahat", "yazar": "Ozan Er", "tarih": "2026-11-18", "saat": "11.00", "durum": "cop"}]
    for i, g in enumerate(kay):
        d = g["durum"]
        img = g_of(g["baslik"])
        href = "infografik.html?id=infografik"
        nit = {"satir": f"i{i}", "durum": d, "kategori": g["bolum"], "yazar": g["yazar"], "ara": f'{g["baslik"]} {g["yazar"]} {g["bolum"]} {g.get("alt_konu") or ""}', "baslik": g["baslik"], "href": href}
        alt = f'{ikon("fa-chart-pie")}{e(g.get("alt_konu") or g["bolum"])} · {e(g["yazar"])}'
        acts = eylemler(gor_href=SITE + "infografik-detay.html" if d == "yayinda" else href, gor_site=d == "yayinda", duz_href=href, ad=g["baslik"])
        sat += satir(nit, [ana_hucre(g["baslik"], alt, img), kat_hucre(g["bolum"], g.get("alt_konu")), durum_hucre(d),
                           f'<td class="kb-gizle-m"><span class="kb-tarih{" muted" if d in ("taslak", "cop") else ""}">{tarih(g["tarih"], g["saat"]) if g.get("saat") else "—"}</span></td>',
                           f'<td class="say kb-gizle-t">{e(g.get("goruntulenme", "—")) if d == "yayinda" else "—"}</td>'], acts)
    diger_i = (dm_yayin("İnfografik", "İnfografik sitede ve gömülü olduğu haberlerde görünmez olur; taslak olarak kalır, geri alınabilir.")
               + dm_dagitim() + dm("Yüksek Çözünürlüklü Dosyayı İndir", "fa-download", "yayinda taslak", bildir="PDF indiriliyor (prototip)")
               + dm_icerik() + dm_kayit() + dm_cop())
    ko_i = [("İnfografik", "kb-ana"), ("Kategori", "kb-gizle-m"), ("Durum", ""), ("Yayın", "kb-gizle-m"), ("Görüntülenme", "say kb-gizle-t")]
    l_inf = liste("in", "infografik", "İnfografikler", [("hepsi", "Tümü", None), ("yayinda", "Yayında", None), ("taslak", "Taslak", None), ("zamanli", "Zamanlanmış", None)],
                  "Başlık, hazırlayan ya da kategori ara", kat_suz("in"),
                  f'<button type="button" class="btn btn-ghost btn-sm" data-toplu="taslak" data-bildir="Seçilen infografikler yayından kaldırıldı">{ikon("fa-eye-slash")}<span>Yayından Kaldır</span></button>',
                  ko_i, sat, ("fa-chart-pie", "Henüz infografik yok", "3:4 infografik görselini yükleyin, veri kaynaklarını yazın; İnfografik sayfasında yayımlanır.",
                              f'<a class="pe-tag" data-hedef="multimedya.infografik" data-hedef-ek="?yeni=1" href="#icerik">{ikon("fa-plus")}Yeni İnfografik</a>'),
                  "İnfografikler yüklenemedi", diger_i, "galeri.html?sekme=tInfo", cop_not="İnfografik sayfasından ve gömülü olduğu haberlerden kalkar ve Çöp sekmesine taşınır")
    ust = sayfa_bas("<h1>Galeri ve İnfografik</h1>", f'<div class="ph-sub">Foto Fokus\'ta {len(GALERILER)} galeri · {len(INFOGRAFIKLER)} infografik yayında · görseller medya havuzundan</div>',
                    btn_link("multimedya.infografik", "İnfografik", "fa-plus", ek="?yeni=1") + "\n      " + btn_link("multimedya.galeri-duzenle", "Yeni Galeri", "fa-plus", acc=True, ek="?yeni=1"))
    govde = (ust + '  <div data-sekmeli>\n  ' + sayfa_sekmeler([("tGaleri", "fa-images", "Foto Galeri", len(GALERILER)), ("tInfo", "fa-chart-pie", "İnfografik", len(INFOGRAFIKLER))])
             + f'\n  <div class="sa-form-panel" id="tGaleri">\n{l_gal}  </div>\n  <div class="sa-form-panel" id="tInfo" hidden>\n{l_inf}  </div>\n  </div>\n')
    yaz("galeri.html", bas("Galeri ve İnfografik", "multimedya.galeri") + govde + son())


# =====================================================================
# 11 · Galeri düzenle (galeri-duzenle.html)
# =====================================================================
def slaytlar(icerik, dolu):
    sar = " data-yeni-gizle" if dolu else " data-yeni-goster hidden"
    return (f'<div{sar}><div class="kb-slaytlar" data-slaytlar data-gorsel-alan="multimedya.galeri" data-gorsel-ad="Galeri slaytı" data-alan-id="slaytlar" data-zorunlu-metin="Galeriye en az bir görsel ekleyin">'
            f'<div class="kb-slayt-liste" data-siralanir>{icerik}</div>'
            f'<div class="kb-slayt-ekle"><button type="button" class="btn btn-ghost btn-sm" data-medya-sec data-gorsel-kapsam="yeni" data-slayt-ekle>{ikon("fa-photo-film")}Havuzdan Ekle</button>'
            f'<button type="button" class="btn btn-ghost btn-sm" data-gorsel-yukle data-gorsel-kapsam="yeni" data-slayt-ekle>{ikon("fa-upload")}Yükle</button><span hidden data-gorsel-hedef="yeni"></span><span data-slayt-say></span></div></div></div>')


def galeri_duzenle():
    g = next(x for x in GALERILER if x["baslik"].startswith("Ankara'da ilk kar"))
    kolaj = KOLAJ.get(g["baslik"]) or ["p117.jpg", "p163.jpg", "p188.jpg"]
    slayt = [("p117.jpg", "Kızılay'da sabah saatlerinde kar küreme çalışması", "Dada Haber · Nilay Ersoy"), ("p163.jpg", "Ulus'ta kar altında tarihî çarşı", "Dada Haber · Nilay Ersoy"),
             ("p188.jpg", "Atakule'den beyaz bir şehir", "Dada Haber · Nilay Ersoy"), ("p133.jpg", "Akşam saatlerinde Tunalı Hilmi Caddesi", "Dada Haber · Nilay Ersoy"),
             ("p182.jpg", "Eskişehir yolunda kar nedeniyle yavaşlayan trafik", "AA"), ("p178.jpg", "Seğmenler Parkı'nda sisli bir sabah", "Dada Haber · Nilay Ersoy")]
    sl = "".join(f'<div class="kb-slayt" data-sira data-gorsel="../../veri/gorsel/kucuk/{im}" data-altyazi="{e(a)}" data-kaynak="{e(k)}"{" data-kapak" if j == 0 else ""}></div>' for j, (im, a, k) in enumerate(slayt))
    ai = ai_adim("#fBaslik,#fSpot", [("aciklama", "Açıklama Taslağı", False, None), ("sinif", "Kategori ve Alt Konular", True, None), ("seo", "SEO", True, None),
                                     ("bildirim", "Bildirim Metni", True, "etkilesim"), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")],
                 "Başlığı ve spotu yazın; işaretli bölümler bunlardan üretilir. Slayt altyazıları sizde.")
    aciklama = "<p>Ankara'da gece başlayan kar yağışı sabah şehri beyaza bürüdü. Foto muhabirimiz Nilay Ersoy, Kızılay'dan Ulus'a başkentin ilk kar gününü yirmi dört karede anlattı.</p>"
    icerik = f"""      <div class="form-sec">
        <div class="form-sec-tt">{ikon("fa-images")}Slaytlar<span class="fs-ek">Sürükleyerek sıralayın · ilk üç slayt kart kolajında</span></div>
        {slaytlar(sl, True)}{slaytlar("", False)}
        <span class="fhint">Yüklenen görsel önce etiketlenir (Dada Haber'e ait görsel medya havuzuna girer, dış kaynaklı yalnız bu galeride kalır). Kapak işaretli slayt sosyal medya ve bildirim görselidir.</span>
      </div>
{gorsel_alan("glKapak", "multimedya.galeri", "Kapak Görseli", kolaj[0], [("web.detay", "Görüntüleyici · 16:10", "16:10", None), ("web.kart", "Kart kolajı · 4:3", "4:3", None)], ("mobil.kart", "Mobil kart · 4:3", "4:3", None),
             "görüntüleyici <b>1280×800</b>, kart <b>308×231</b> (ilk üç slayttan kolaj)", "<b>358×268</b>", "1280×800", kaynak="Kapak slaytından", odak=(50, 45), alan_id=None,
             baslik="Kapak Kırpımı", ek_alt=" Kapak slaytı değişince bu kırpım da yenilenir.")}
{editor("Açıklama", aciklama, "Görüntüleyicinin başında", ai_grup="aciklama")}
{siniflandirma("glKat", g["bolum"], ["Foto Fokus"] if "Foto Fokus" in ALT_HARITA.get(g["bolum"], []) else [], g["yazar"])}
{okur_etkilesimi(toggle("Yorumlar Açık", "Yorumları editörler yönetir"), toggle("Haberlerin İçine Gömülebilir", "Haber metnine “galeri ekle” ile eklenir"), toggle("Tam Ekran Görüntüleyici", "Okur kaydırarak ve yakınlaştırarak gezer"))}"""
    paneller = (detay_panel(baslik_spot(g["baslik"], "Başkentte gece başlayan kar sabah şehri beyaza bürüdü; Kızılay'dan Ulus'a ilk kar günü.") + ai + "\n" + icerik)
                + seo_panel("pSeo", "Ankara'da ilk kar: şehirden 24 kare | Foto Fokus", "Başkentte gece başlayan kar yağışı sabah şehri beyaza bürüdü. Kızılay'dan Ulus'a Ankara'nın ilk kar günü 24 karede.",
                            "dadahaber.com/foto-fokus/", "ankara-da-ilk-kar-sehirden-yirmi-dort-kare", ["ankara kar", "ilk kar fotoğraf"],
                            toggle("Görsel Şeması (ImageGallery)", "Google Görseller'de galeri olarak görünür"))
                + bildirim_panel("pBildirim", "Foto Fokus: Ankara'da ilk kar", "Başkentin ilk kar günü 24 karede. Kızılay'dan Ulus'a beyaz bir şehir.", "Kapak slaytının bildirim kırpımı (2:1)")
                + sosyal_panel("pSosyal", {"instagram": "Ankara'da ilk kar ❄️ Kızılay'dan Ulus'a başkentin beyaz günü. Galerinin tamamı profildeki bağlantıda.\n\n#ankara #kar #fotofokus",
                                           "x": "Ankara'da ilk kar: şehirden yirmi dört kare 📷\n\nhttps://dadahaber.com/foto-fokus/ankara-da-ilk-kar\n\n#Ankara",
                                           "facebook": "Başkentte gece başlayan kar sabah şehri beyaza bürüdü. Foto muhabirimiz Nilay Ersoy'un objektifinden Ankara'nın ilk kar günü.\n\nhttps://dadahaber.com/foto-fokus/ankara-da-ilk-kar"},
                               kolaj[0], "#glKapak", (50, 45), "Instagram'da ilk 10 slayt kaydırmalı gönderi (carousel) olur; diğer platformlarda kapak ve bağlantı paylaşılır."))
    yan = (bildirim_onizle("pBildirim", "Foto Fokus: Ankara'da ilk kar", "Başkentin ilk kar günü 24 karede. Kızılay'dan Ulus'a beyaz bir şehir.", kolaj[0])
           + sosyal_onizle("pSosyal", kolaj[0], g["baslik"], (50, 45))
           + yayin_kart(durum_secim("ycDurum", "yayinda", YAYIN_DURUM), "2026-11-22 12.30",
                        toggle("Foto Fokus Vitrininde", "Foto Fokus sayfasının başında", True)
                        + f'<div class="sa-durum" data-yeni-gizle><div><span>Slayt</span><b>6</b></div><div><span>Görüntülenme</span><b>{e(g["goruntulenme"])}</b></div><div><span>Ortalama gezilen</span><b>5 slayt</b></div></div>',
                        surum=(4, "22.11.2026 13.05", "Nilay Ersoy"))
           + seo_kart(87, [(True, "Başlık 50–60 karakter"), (True, "Açıklama 120–155 karakter"), (True, "Her slaytta altyazı"), (False, "2 slaytta kaynak eksik")]))
    duzenle_sayfasi("galeri-duzenle.html", "Galeri Düzenle", "multimedya.galeri", "Yeni Galeri", "Galeri Düzenle", "Yeni Galeri",
                    f'Keşfet › Foto Fokus · {e(g["yazar"])} · 6 slayt · {tarih(g["tarih"], g["saat"])}\'te yayımlandı · {e(g["goruntulenme"])} görüntülenme',
                    "Taslak · henüz kaydedilmedi · hazırlayan: oturumdaki kullanıcı", ("multimedya.galeri", "Galerilere Dön"), SITE + "foto-fokus-detay.html",
                    "glForm", "multimedya.galeri", STD_SEKMELER, paneller, yan,
                    kaydet_cubugu("glForm", "Kaydedildi · 22.11.2026 13.05 · Nilay Ersoy", "Galeri güncellendi; Foto Fokus'ta yayında", "Galeri yayımlandı; Foto Fokus'ta görünür"))


# =====================================================================
# 12 · İnfografik düzenle (infografik.html)
# =====================================================================
def infografik_duzenle():
    g = next(x for x in INFOGRAFIKLER if "Asgari" in x["baslik"])
    img = "p163.jpg"
    ai = ai_adim("#fBaslik,#fSpot", [("aciklama", "Açıklama Taslağı", False, None), ("alt", "Erişilebilirlik Metni (Görselden)", True, None), ("sinif", "Kategori ve Alt Konular", True, None),
                                     ("seo", "SEO", True, None), ("sosyal", "Sosyal Medya Metinleri", True, "sosyal-medya")],
                 "Başlığı ve spotu yazın; erişilebilirlik metni görseldeki rakamlardan, diğerleri başlık ve spottan üretilir.")
    kay = [("Türkiye İstatistik Kurumu", "Asgari ücret ve TÜFE serileri, 2016–2026"), ("Çalışma ve Sosyal Güvenlik Bakanlığı", "Asgari Ücret Tespit Komisyonu kararları")]
    kay_html = "".join(km_satir(a, b, "Kaynak") for a, b in kay)
    icerik = f"""{gorsel_alan("ifGorsel", "multimedya.infografik", "İnfografik Görseli", img, [("web.detay", "Görüntüleyici · 3:4", "3:4", None), ("web.kart", "Kart · 3:4", "3:4", None)], ("mobil.kart", "Mobil · 3:4", "3:4", None),
             "görüntüleyici <b>900×1200</b>, kart <b>305×407</b>", "<b>358×477</b>", "1800×2400", kaynak="Dada Haber grafik masası", odak=(50, 50), alan_id="gorsel",
             hata="İnfografik görselini yükleyin", ek_alt=" Metin içeren görsel kırpılmaz; “Kırpmadan kullan” önerilir.")}
      <div class="form-sec" data-ai-grup="alt"><div class="form-grid">
        {metin_alani("ifAlt", "Erişilebilirlik Metni", "2016'da 1.300 lira olan net asgari ücret 2026'da 22.104 liraya yükseldi; en büyük artış 2023'te yüzde 100 oldu.", sayac="250|320", not_="Ekran okuyucu bu metni okur; görseldeki rakamları yazın")}
      </div></div>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-link")}Veri Kaynakları<span class="fs-ek">Sitede görselin altında</span></div>
        <div class="kb-madde" data-satir-liste data-siralanir data-satir-ad="Kaynak" data-satir-alan1="Kaynak adı (kurum, belge)" data-satir-alan2="Veri seti, tarih ya da bağlantı">{kay_html}<button type="button" class="kb-ekle-btn" data-satir-ekle>{ikon("fa-plus")}Kaynak Ekle</button></div></div>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-share-from-square")}İndirme ve Paylaşım İzni</div><div class="form-grid">
        {toggle("Okur İndirebilir", "Görüntüleyicide “İndir” düğmesi (PNG)")}
        {toggle("Başka Siteler Gömebilir", "Gömme kodu verilir; Dada Haber'e atıf ve bağlantı zorunlu")}
        <div class="frow"><span class="flabel">Lisans</span>{secim("ifLisans", "atif", [("hakli", "Dada Haber · tüm hakları saklı"), ("atif", "Atıfla Paylaşılabilir (CC BY 4.0)"), ("ticari-degil", "Atıfla, Ticari Olmayan (CC BY-NC 4.0)")])}</div>
        <div class="frow"><span class="flabel">Yüksek Çözünürlüklü Dosya</span>{dosya_alan("belge", "Baskı dosyası", None, ("asgari-ucret-on-yil.pdf", 2516582), kabul=".pdf,.png,.svg", sinir=50)}<span class="fhint">İsteğe bağlı; basın ve kurumlar için indirme bağlantısı.</span></div>
      </div></div>
{editor("Açıklama", "<p>Asgari ücretin son on yıldaki seyri: net tutar, yıllık artış oranı ve aynı dönemde enflasyon. Veriler TÜİK ve Çalışma ve Sosyal Güvenlik Bakanlığı'ndan.</p>", "Görüntüleyicinin altında", ai_grup="aciklama")}
{siniflandirma("ifKat", g["bolum"], [], g["yazar"])}"""
    paneller = (detay_panel(baslik_spot(g["baslik"], "2016'dan 2026'ya net asgari ücret, yıllık artış ve enflasyon tek grafikte.") + ai + "\n" + icerik)
                + seo_panel("pSeo", "Asgari ücretin on yıllık seyri | Dada Haber İnfografik", "2016'dan 2026'ya net asgari ücret, yıllık artış oranları ve enflasyon. Veriler TÜİK ve Çalışma Bakanlığı'ndan.",
                            "dadahaber.com/infografik/", "asgari-ucretin-on-yillik-seyri", ["asgari ücret grafik", "asgari ücret 10 yıl"])
                + sosyal_panel("pSosyal", {"instagram": "Asgari ücretin on yıllık seyri 📊 2016'da 1.300 lira, 2026'da 22.104 lira.\n\n#asgariücret #infografik #dadahaber",
                                           "x": "Asgari ücretin on yıllık seyri 📊\n\nhttps://dadahaber.com/infografik/asgari-ucret-on-yil\n\n#AsgariÜcret",
                                           "linkedin": "2016'dan 2026'ya net asgari ücret, yıllık artış ve enflasyon tek grafikte. Veriler TÜİK ve Çalışma ve Sosyal Güvenlik Bakanlığı'ndan.\n\nhttps://dadahaber.com/infografik/asgari-ucret-on-yil"},
                               img, "#ifGorsel", (50, 50), "Instagram'da 4:5 kırpım; metinli görselde “Kırpmadan kullan” ile kenarlar boş bırakılır."))
    yan = (sosyal_onizle("pSosyal", img, g["baslik"], (50, 50))
           + yayin_kart(durum_secim("ycDurum", "yayinda", YAYIN_DURUM), "2026-11-23 09.30",
                        f'<div class="sa-durum" data-yeni-gizle><div><span>Görüntülenme</span><b>{e(g["goruntulenme"])}</b></div><div><span>İndirilme</span><b>214</b></div><div><span>Gömülü olduğu site</span><b>3</b></div></div>',
                        surum=(2, "23.11.2026 09.40", g["yazar"]))
           + seo_kart(82, [(True, "Başlık 50–60 karakter"), (True, "Erişilebilirlik metni var"), (True, "Veri kaynağı yazılı"), (False, "Görsel 1800 px altında")]))
    duzenle_sayfasi("infografik.html", "İnfografik Düzenle", "multimedya.galeri", "Yeni İnfografik", "İnfografik Düzenle", "Yeni İnfografik",
                    f'Keşfet › Veri ve Harita · {e(g["yazar"])} · {tarih(g["tarih"], g["saat"])}\'te yayımlandı · {e(g["goruntulenme"])} görüntülenme', "Taslak · henüz kaydedilmedi · hazırlayan: oturumdaki kullanıcı",
                    ("multimedya.galeri", "İnfografiklere Dön", "?sekme=tInfo"), SITE + "infografik-detay.html", "ifForm", "multimedya.infografik",
                    [("pDetay", "fa-file-lines", "Detay", None), ("pSeo", "fa-magnifying-glass-chart", "SEO", None), ("pSosyal", "fa-share-nodes", "Sosyal Medya", "sosyal-medya")], paneller, yan,
                    kaydet_cubugu("ifForm", f'Kaydedildi · 23.11.2026 09.40 · {e(g["yazar"])}', "İnfografik güncellendi; sitede yayında", "İnfografik yayımlandı; İnfografik sayfasında görünür"))


# =====================================================================
# 13 · Medya havuzu (havuz.html) — M1–M4
# =====================================================================
KISI = {k["ad"]: k for k in EH["kisiler"]}
KULLANIM = {}
for b, dosya in GORSEL.items():
    KULLANIM.setdefault(dosya, []).append(b)
HAVUZ_ORAN = "web.genis=Geniş · 16:9=16:9=1280×720;web.kart=Kart · 4:3=4:3=1200×900;web.kare=Kare · 1:1=1:1=1080×1080;web.dikey=Dikey · 3:4=3:4=900×1200"
YUKLEYEN = ["Nilay Ersoy", "Ozan Er", "Kerem Aksoy", "İrem Su", "Sibel Arslan", "Mert Yalın"]
# Etiket yönetimi örnekleri (yalnız bu sayfada): birleştirmeyi göstermek için yinelenen kayıtlar, kullanılmayan ve çöpte birer kayıt.
# Yinelenen kayıt bir görselde gerçek kaydın yerine (ya da yanında) geçer; böylece görsel listesi ile etiket listeleri aynı sayıyı verir.
EK_KISI = [{"ad": "Cumhurbaşkanı Erdoğan", "kisaltma": "", "tur": "Kişi"}, {"ad": "Merkez Bankası", "kisaltma": "", "tur": "Kurum"}]
COP_KISI = [{"ad": "Devlet Planlama Teşkilatı", "kisaltma": "DPT", "tur": "Kurum"}]
EK_ETIKET = ["Istanbul", "hava", "seçim"]
COP_ETIKET = ["yağmur"]
YINELEME = [("p158.jpg", "kisiler", "Recep Tayyip Erdoğan", "Cumhurbaşkanı Erdoğan"), ("p163.jpg", "kisiler", None, "Merkez Bankası"),
            ("p133.jpg", "etiketler", "İstanbul", "Istanbul"), ("p178.jpg", "etiketler", "hava durumu", "hava")]
KISILER = EH["kisiler"] + EK_KISI
KISI.update({k["ad"]: k for k in EK_KISI + COP_KISI})
ETIKETLER = EH["etiketler"] + EK_ETIKET


def kisi_etk(ad):
    k = KISI.get(ad, {})
    return k.get("kisaltma") or ad


def havuz_gorselleri():
    gl = [json.loads(json.dumps(g)) for g in MH["gorseller"]] + [dict(json.loads(json.dumps(MH["gorseller"][-1])), ad="Sahil ve bisiklet (yinelenen kopya)", cop=True)]
    for dosya, alan, eski, yeni in YINELEME:
        for g in gl:
            if g["dosya"] == dosya and not g.get("cop"):
                xs = g.setdefault("etiket", {}).setdefault(alan, [])
                if eski in xs:
                    xs[xs.index(eski)] = yeni
                else:
                    xs.append(yeni)
    return gl


def havuz_sayfasi():
    gl = havuz_gorselleri()
    sat, sab = "", ""
    say_kat, say_kisi = {}, {}
    for i, g in enumerate(gl):
        et = g.get("etiket", {})
        kul = [] if g.get("cop") else KULLANIM.get(g["dosya"], [])
        if i in (1, 8, 12):
            kul = []
        kul = kul[:2 + h(g["dosya"], 4)]
        n = len(kul) + (h(g["dosya"] + "s", 3) if kul else 0)
        d = "cop" if g.get("cop") else ("kullanimda" if n else "bos")
        if d != "cop":
            say_kat[et.get("kategori")] = say_kat.get(et.get("kategori"), 0) + 1
            for k in et.get("kisiler", []):
                say_kisi[k] = say_kisi.get(k, 0) + 1
        kis = et.get("kisiler", [])
        alt = " · ".join([et.get("kategori", "")] + [kisi_etk(k) for k in kis])
        kb = 160 + h(g["dosya"], 240)
        yk = YUKLEYEN[h(g["dosya"], len(YUKLEYEN))]
        tar = f"{10 + h(g['dosya'], 14):02d}.11.2026"
        vid, did = f"mhV{i}", f"mhD{i}"
        kul_metin = f"{n} içerikte kullanılıyor ({', '.join(kul[:2])}{'…' if n > 2 else ''}); o içeriklerde görünmeye devam eder, yalnız havuzdan ve aramadan kalkar" if n else None
        nit = {"satir": f"m{i}", "durum": d, "kategori": et.get("kategori"), "kisi": "|".join(kis), "etiket": "|".join(et.get("etiketler", [])),
               "ara": f'{g["ad"]} {et.get("kategori", "")} {" ".join(kis)} {" ".join(KISI.get(k, {}).get("kisaltma", "") for k in kis)} {" ".join(et.get("etiketler", []))}',
               "baslik": g["ad"], "kullanim": kul_metin}
        etiketler = "".join(f'<span class="etk">{e(x)}</span> ' for x in et.get("etiketler", [])[:2]) + (f'<span class="etk">+{len(et["etiketler"]) - 2}</span>' if len(et.get("etiketler", [])) > 2 else "")
        acts = eylemler(gor_tanim=vid, duz_tanim=did, ad=g["ad"])
        sat += satir(nit, [ana_hucre(g["ad"], e(alt), g["dosya"]),
                           f'<td class="kb-gizle-m kb-izgara-gizle">{etiketler}</td>',
                           f'<td class="kb-gizle-t kb-izgara-gizle"><span class="kb-kat">{ikon("fa-copyright")}Dada Haber</span></td>',
                           f'<td class="say kb-gizle-t kb-izgara-gizle">{e(g.get("olcu", "1200×800"))}</td>',
                           durum_hucre_m(d, n)], acts)
        kul_html = "".join(act_satir("fa-newspaper", b, "Haber · kapak görseli", f"{20 + h(b, 4)}.11", href=SITE + "haber-detay.html") for b in kul[:4]) or \
            '<div class="pnl-empty"><div class="pe-ico">' + ikon("fa-image") + '</div><h2>Henüz kullanılmadı</h2><p>Bir içerikte seçildiğinde burada listelenir.</p></div>'
        cip = lambda xs, kisa=False: "".join(f'<span class="kb-cip" data-deger="{e(x)}"><span>{e(x)}</span>{f"<small>{e(KISI.get(x, {}).get(chr(107) + chr(105) + chr(115) + chr(97) + chr(108) + chr(116) + chr(109) + chr(97), chr(32)))}</small>" if kisa else ""}<button type="button" aria-label="Kaldır">{ikon("fa-xmark")}</button></span>' for x in xs)
        sil = onay("Görsel çöpe taşınsın mı?", (f"“{g['ad']}” {kul_metin}. " if n else f"“{g['ad']}” hiçbir içerikte kullanılmıyor. ") + "Çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır.",
                   "Çöpe Taşı", "fa-trash", tehlike=True, sonra="Görsel çöpe taşındı", sonra_durum=("cop", "Çöpte", "warm"))
        sab += f"""<template id="{vid}" data-baslik="Görsel Bilgileri" data-alt="{e(g['ad'])} · {e(g.get('olcu', '1200×800'))} · {kb} KB">
  <div class="kb-ozet-gorsel" style="background-image:url(../../veri/gorsel/{g['dosya']})"></div>
  <dl class="kb-ozet-dl"><dt>Dosya</dt><dd>{e(g['dosya'])}</dd><dt>Çözünürlük</dt><dd>{e(g.get('olcu', '1200×800'))} · {kb} KB · JPG</dd><dt>Telif</dt><dd>Dada Haber'e ait · {e(g.get('kaynak', ''))}</dd><dt>Yükleyen</dt><dd>{e(yk)} · {tar}</dd>
    <dt>Kategori</dt><dd>{e(et.get('kategori', '—'))}</dd><dt>Kişi ve Kurum</dt><dd>{e(', '.join(f"{k} ({KISI.get(k, {}).get('kisaltma', '')})" if KISI.get(k, {}).get('kisaltma') else k for k in kis) or '—')}</dd><dt>Etiketler</dt><dd>{e(', '.join(et.get('etiketler', [])) or '—')}</dd></dl>
  <div class="kb-fs" data-gorsel-alan="multimedya.havuz" data-gorsel-ad="{e(g['ad'])}" data-kirp-oranlar="{HAVUZ_ORAN}"><div class="kb-fs-tt">Oran Sürümleri<span class="fs-ek"><button type="button" class="btn btn-ghost btn-sm" data-kirp-ac>{ikon("fa-crop-simple")}Odak ve Kırp</button></span></div>
    <div class="kg-ikili">{kutu("web", "web.genis", "16:9", "16:9", g['dosya'], (50, 45), True)}{kutu("web", "web.kart", "4:3", "4:3", g['dosya'], (50, 45))}</div>
    <div class="kg-ikili">{kutu("web", "web.kare", "1:1", "1:1", g['dosya'], (50, 45))}{kutu("web", "web.dikey", "3:4", "3:4", g['dosya'], (50, 45))}</div>
    <p class="fhint">Bir içerikte kullanılırken o alanın oranı bu odak noktasından kendiliğinden kırpılır; içerikte ayrıca düzeltilebilir.</p></div>
  <div class="kb-fs"><div class="kb-fs-tt">Kullanım Geçmişi<span class="fs-ek">{n} içerik</span></div><div class="act-list">{kul_html}</div></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm danger kb-sol"{sil}>{ikon("fa-trash")}Çöpe Taşı</button><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="{did}">{ikon("fa-pen")}Düzenle</button></div>
</template>
<template id="{did}" data-baslik="Görseli Düzenle" data-alt="{e(g['ad'])}" data-zorunlu-kayit="multimedya.varlik">
  {kap_dil()}
  <div class="kb-gorsel-kucuk"><div class="kg-resim r-4x3" style="background-image:url(../../veri/gorsel/kucuk/{g['dosya']})"></div><div><b>{e(g.get('olcu', '1200×800'))} · {kb} KB</b><span>Telif: Dada Haber'e ait · havuzda yalnız telifi bize ait görseller durur (M1)</span></div></div>
  <div class="kb-fs"><div class="kb-fs-tt">Bilgiler</div>
    <div class="frow"><label for="{did}Ad">Görsel Adı</label><input class="finput" id="{did}Ad" data-alan-id="ad" data-zorunlu-metin="Görsel adı zorunlu" data-sayac="60|80" value="{e(g['ad'])}"><div class="char-meter"><span>Havuzda ve aramada görünür</span><b>0 / 60</b></div></div>
    <div class="frow"><span class="flabel">Kategori</span>{secim(did + "Kat", et.get('kategori', ''), [(k, k) for k in EH['kategoriler']], alan_id="kategori", ara="Kategori ara", bos="Kategori seçin", zorunlu_metin="Kategori seçin", bos_metin="Bu adla kategori yok.")}</div>
    <div class="frow"><span class="flabel">Kişi ve Kurum</span><div class="kb-cip-girdi" data-havuz-yonet data-kullanim-birim="görselde" data-havuz="{e(json.dumps([k['ad'] for k in KISILER], ensure_ascii=False))}">{cip(kis)}<input type="text" placeholder="Ad ya da kısaltma: RTE, MGK…" aria-label="Kişi ya da kurum ara"><div class="pnl-menu kb-cip-oneri"></div></div><span class="fhint">Havuzda yoksa aynı yerden eklenir; ⋯ ile adını düzeltin, silin, kaç görselde kullanıldığını görün.</span></div>
    <div class="frow"><span class="flabel">Etiketler</span><div class="kb-cip-girdi" data-havuz-yonet data-kullanim-birim="görselde" data-havuz="{e(json.dumps(ETIKETLER, ensure_ascii=False))}">{cip(et.get('etiketler', []))}<input type="text" placeholder="Etiket ara ya da yaz" aria-label="Etiket ara"><div class="pnl-menu kb-cip-oneri"></div></div></div>
    <div class="frow"><label for="{did}Fo">Fotoğrafçı ya da Kaynak</label><input class="finput" id="{did}Fo" value="{e(yk)} · Dada Haber"></div>
    <div class="frow"><label for="{did}Alt">Varsayılan Altyazı</label><textarea class="ftext" id="{did}Alt" rows="2" data-sayac="120|160">{e(g['ad'])} · Fotoğraf: {e(yk)}</textarea><div class="char-meter"><span>İçerikte seçilince altyazı alanına gelir</span><b>0 / 120</b></div></div></div>
  <div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-kapat data-bildir-hemen="Görsel bilgileri kaydedildi; arama ve Gez hemen güncellendi">{ikon("fa-floppy-disk")}Kaydet</button></div>
</template>
"""
    gez = (f'<nav class="kb-medya-gez kb-gez-sayfa" aria-label="Havuzu gez"><button type="button" data-gez-suz="kategori" data-v="">Bütün Görseller<span>{len(gl) - 1}</span></button><div class="kmg-tt">Kategori</div>'
           + "".join(f'<button type="button" data-gez-suz="kategori" data-v="{e(k)}" aria-pressed="false">{e(k)}<span>{say_kat[k]}</span></button>' for k in EH["kategoriler"] if say_kat.get(k))
           + '<div class="kmg-tt">Kişi ve Kurum</div>'
           + "".join(f'<button type="button" data-gez-suz="kisi" data-v="{e(k["ad"])}" aria-pressed="false" title="{e(k["ad"])}">{e(k["kisaltma"] or k["ad"])}<small>{e(k["ad"] if k["kisaltma"] else "")}</small><span>{say_kisi[k["ad"]]}</span></button>' for k in KISILER if say_kisi.get(k["ad"]))
           + "</nav>")
    suz = (secim("mhSuzKat", "", [("", "Bütün Kategoriler")] + [(k, k, say_kat.get(k)) for k in EH["kategoriler"] if say_kat.get(k)], suz="kategori", etk="Kategori:", ara="Kategori ara")
           + secim("mhSuzKisi", "", [("", "Bütün Kişi ve Kurumlar")] + [(k["ad"], k["ad"], k["kisaltma"]) for k in KISILER if say_kisi.get(k["ad"])], suz="kisi", etk="Kişi ve Kurum:", ara="Ad ya da kısaltma ara", ek=" data-suz-coklu", bos_metin="Bu adla kişi ya da kurum yok.")
           + secim("mhSuzEt", "", [("", "Bütün Etiketler")] + [(x, x) for x in sorted(set(t for g in gl for t in g.get("etiket", {}).get("etiketler", [])))], suz="etiket", etk="Etiket:", ara="Etiket ara", ek=" data-suz-coklu")
           + f'<div class="kb-gorunum-sec" data-gorunum-sec role="group" aria-label="Görünüm"><button type="button" class="chip" data-gorunum="izgara" aria-pressed="false">{ikon("fa-grip")}Izgara</button><button type="button" class="chip" data-gorunum="liste" aria-pressed="false">{ikon("fa-list")}Liste</button></div>')
    n_kol = 7
    isk = "".join('<tr class="kb-iskelet"><td></td><td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td><td class="kb-gizle-m"><span></span></td><td class="kb-gizle-t"><span></span></td><td class="kb-gizle-t"><span></span></td><td><span></span></td><td></td></tr>' for _ in range(4))
    diger = (dm_grup("Görsel", "kullanimda bos")
             + dm("Odak ve Kırp", "fa-crop-simple", "kullanimda bos", bildir="Görüntüle penceresinde “Odak ve kırp” ile açılır (prototip)")
             + dm("Etiketleri Düzenle", "fa-tags", "kullanimda bos", bildir="Satırdaki düzenle düğmesiyle açılır: kategori, kişi ve kurum, etiketler (prototip)")
             + dm("Bağlantıyı Kopyala", "fa-link", "kullanimda bos", ek=" data-kopyala")
             + dm("Aslını İndir", "fa-download", "kullanimda bos", bildir="Görselin aslı indiriliyor (1200×800 JPG)")
             + dm_ayir("kullanimda bos") + dm_grup("Kayıt") + dm("Denetim İzinde Gör", "fa-clipboard-list", roller="super gyy", hedef="denetim-izi.liste") + dm_cop())
    kalici_not = "Kalıcı silinen görsel kullanıldığı içeriklerde “Görsel eksik” olur; e-posta koduyla doğrulanır"
    liste_html = f"""  <div class="sa-form-panel" id="mhPGorsel" role="tabpanel">
  <div data-liste data-liste-ad="görsel" data-liste-cop-not="Havuzdan ve aramadan kalkar (kullanıldığı içeriklerde görünmeye devam eder) ve Çöp sekmesine taşınır" data-sayfa-boy="24" data-gorunum="izgara" id="mhListe" aria-labelledby="mhBas">
    <h2 class="sr-only" id="mhBas">Görseller</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Kullanıma göre"><button type="button" class="chip is-on" role="tab" aria-selected="true" data-sekme="hepsi">Tümü<span class="ch-cnt">0</span></button><button type="button" class="chip" role="tab" aria-selected="false" data-sekme="kullanimda">Kullanımda<span class="ch-cnt">0</span></button><button type="button" class="chip" role="tab" aria-selected="false" data-sekme="bos">Kullanılmayan<span class="ch-cnt">0</span></button></div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{ikon("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{ikon("fa-magnifying-glass")}<label class="sr-only" for="mhAra">Medya Havuzunda Ara</label><input id="mhAra" type="search" data-liste-ara placeholder="Kişi, kurum, kısaltma (RTE) ya da etiket ara" autocomplete="off"></div>
      {suz}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
    </div>
    <div class="kb-toplu" hidden><b data-secili-say>0 görsel seçildi</b><span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="etiket" data-bildir="Seçilen görsellere etiket ekleme penceresi (prototip)">{ikon("fa-tags")}<span>Etiket Ekle</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{ikon("fa-trash")}<span>Çöpe Taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi Temizle</button></div>
    <div class="kb-medya-gov">
      {gez}
      <div>
        <div class="ptable-wrap">
          <table class="ptable">
            <thead><tr><th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün görselleri seç"></th><th class="kb-ana">Görsel</th><th class="kb-gizle-m">Etiketler</th><th class="kb-gizle-t">Telif</th><th class="say kb-gizle-t">Çözünürlük</th><th>Kullanım</th><th><span class="sr-only">İşlemler</span></th></tr></thead>
            <tbody data-satirlar>{sat}</tbody>
            <tbody><tr class="kb-bos-satir" hidden><td colspan="{n_kol}"><div class="pnl-empty"><div class="pe-ico">{ikon("fa-magnifying-glass")}</div><h2>Bu aramayla görsel yok</h2><p>Kişi, kurum, kısaltma (RTE, MGK) ya da etiketle arayın; süzgeçleri kaldırmayı deneyin.</p><button type="button" class="pe-tag" data-suz-temizle>{ikon("fa-filter-circle-xmark")}Süzgeçleri Temizle</button></div></td></tr></tbody>
            <tbody data-durum-goster="yukleniyor" hidden>{isk}</tbody>
            <tbody data-durum-goster="hata" hidden><tr><td colspan="{n_kol}"><div class="pnl-empty kb-hata"><div class="pe-ico">{ikon("fa-triangle-exclamation")}</div><h2>Medya havuzu yüklenemedi</h2><p>Sunucuya ulaşılamadı. İçeriklerdeki görseller etkilenmez; bağlantınızı kontrol edip yeniden deneyin.</p><a class="pe-tag" href="havuz.html">{ikon("fa-rotate-right")}Yeniden Dene</a></div></td></tr></tbody>
            <tbody data-durum-goster="bos" hidden><tr><td colspan="{n_kol}"><div class="pnl-empty"><div class="pe-ico">{ikon("fa-photo-film")}</div><h2>Medya havuzu boş</h2><p>Dada Haber'e ait görselleri yükleyip etiketleyin; içeriklerde “Havuzdan seç” ile bulunur.</p></div></td></tr></tbody>
          </table>
        </div>
      </div>
    </div>
    <div class="pnl-menu kb-diger-menu" role="menu">{diger}</div>
  </div>
  </div>
"""
    yukle = (f'<span data-panel-icin="mhPGorsel" data-gorsel-alan="multimedya.havuz" data-gorsel-ad="Havuz görseli" data-kirp-sonra data-kirp-oranlar="{HAVUZ_ORAN}">'
             f'<button type="button" class="btn btn-acc btn-sm" data-gorsel-yukle>{ikon("fa-upload")}Görsel Yükle</button>'
             f'<span hidden data-gorsel-hedef="web" data-kirp-oran="web.genis"></span><button type="button" hidden data-kirp-ac aria-hidden="true" tabindex="-1">Kırp</button></span>')
    p_kisi, s_kisi, n_kisi = hv_kisi_panel(gl)
    p_et, s_et, n_et = hv_etiket_panel(gl)
    yonet = (f'<button type="button" class="btn btn-ghost btn-sm" data-sekme-git="mhPKisi" data-panel-icin="mhPGorsel">{ikon("fa-tags")}Etiketleri Yönet</button>'
             f'<button type="button" class="btn btn-acc btn-sm" data-tanim="mhKYeni" data-panel-icin="mhPKisi">{ikon("fa-plus")}Yeni Kişi ya da Kurum</button>'
             f'<button type="button" class="btn btn-acc btn-sm" data-tanim="mhEYeni" data-panel-icin="mhPEtiket">{ikon("fa-plus")}Yeni Etiket</button>')
    ust = sayfa_bas("<h1>Medya Havuzu</h1>", f'<div class="ph-sub">{len(gl) - 1} görsel · {n_kisi} kişi ve kurum · {n_et} etiket · yalnız Dada Haber\'e ait görseller (M1)</div>', yonet + yukle)
    bant = f'<div class="kb-bant bilgi kb-alt-bosluk">{ikon("fa-circle-info")}<span>Yüklenen görsel önce <b>etiketlenir</b>, sonra <b>kırpılır</b>; dış kaynaklı görsel havuza girmez. Kişi, kurum ve etiketler yalnız medya havuzuna aittir, haber etiketlerinden ayrıdır (M2).</span></div>'
    sekmeler = ('<div class="sa-form-tabs" role="tablist" aria-label="Medya havuzu bölümleri">'
                f'<button type="button" class="sa-form-tab is-on" role="tab" aria-selected="true" data-panel="mhPGorsel">{ikon("fa-images")}Görseller</button>'
                f'<button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="mhPKisi">{ikon("fa-address-card")}Kişi ve Kurumlar</button>'
                f'<button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="mhPEtiket">{ikon("fa-tags")}Etiketler</button></div>')
    kart = f'  <section class="pnl-card" id="mhKart" data-sekmeli aria-label="Medya havuzu">\n    {sekmeler}\n{liste_html}{p_kisi}{p_et}  </section>\n'
    yaz("havuz.html", bas("Medya Havuzu", "multimedya.havuz") + ust + bant + kart + son(sab + s_kisi + s_et))


# ---- Medya havuzu › Kişi ve kurumlar · Etiketler (aynı kartta sekme; tek liste, tek araç satırı) ----
def hv_kullanim(gl, alan):
    m = {}
    for g in gl:
        if not g.get("cop"):
            for x in g.get("etiket", {}).get(alan, []):
                m.setdefault(x, []).append(g)
    return m


def hv_on(gs):
    """Satırın alt satırı: kullanıldığı ilk görseller."""
    if not gs:
        return "Henüz bir görselde yok"
    return e(", ".join(g["ad"] for g in gs[:2])) + (f" ve {len(gs) - 2} görsel daha" if len(gs) > 2 else "")


def hv_kul_hucre(d, n):
    if d == "cop":
        return '<td><span class="pstat warm">Çöpte</span></td>'
    return f'<td><span class="pstat ok">{n} görsel</span></td>' if n else '<td><span class="pstat off">Kullanılmıyor</span></td>'


def hv_gorsel_satirlari(gs):
    if not gs:
        return f'<div class="pnl-empty"><div class="pe-ico">{ikon("fa-image")}</div><h2>Henüz bir görselde yok</h2><p>Görsel etiketlenirken seçildiğinde burada listelenir.</p></div>'
    return "".join(act_satir("fa-image", g["ad"], e(" · ".join([g.get("etiket", {}).get("kategori", "")] + [kisi_etk(k) for k in g.get("etiket", {}).get("kisiler", [])])),
                             g.get("olcu", "1200×800")) for g in gs)


def hv_liste(pid, lid, ad, aria, ara_ph, suzler, kolonlar, satirlar, bos, diger, cop_not):
    kol = ('<th class="kb-sec-hucre"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün kayıtları seç"></th>'
           + "".join(f'<th{f" class=\"{c}\"" if c else ""}>{b}</th>' for b, c in kolonlar) + '<th><span class="sr-only">İşlemler</span></th>')
    n = len(kolonlar) + 2
    isk_h = "".join("<td></td>" if i in (0, n - 1) else ('<td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td>' if i == 1 else "<td><span></span></td>") for i in range(n))
    isk = "".join(f'<tr class="kb-iskelet">{isk_h}</tr>' for _ in range(4))
    bik, bh2, bp, byeni = bos
    sek = "".join(f'<button type="button" class="chip{" is-on" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-sekme="{s}">{a}<span class="ch-cnt">0</span></button>'
                  for i, (s, a) in enumerate([("hepsi", "Tümü"), ("kullanimda", "Kullanımda"), ("bos", "Kullanılmayan")]))
    return f"""  <div class="sa-form-panel" id="{pid}" role="tabpanel" hidden>
  <div data-liste data-liste-ad="{ad}" data-liste-cop-not="{e(cop_not)}" data-sayfa-boy="25" id="{lid}" aria-labelledby="{lid}Bas">
    <h2 class="sr-only" id="{lid}Bas">{aria}</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Kullanıma göre">{sek}</div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop">{ikon("fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{ikon("fa-magnifying-glass")}<label class="sr-only" for="{lid}Ara">{bb(aria + " içinde ara")}</label><input id="{lid}Ara" type="search" data-liste-ara placeholder="{e(ara_ph)}" autocomplete="off"></div>
      {suzler}
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri Temizle</button>
    </div>
    <div class="kb-toplu" hidden><b data-secili-say>0 {ad} seçildi</b><span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{ikon("fa-trash")}<span>Çöpe Taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi Temizle</button></div>
    <div class="ptable-wrap">
      <table class="ptable">
        <thead><tr>{kol}</tr></thead>
        <tbody data-satirlar>{satirlar}</tbody>
        <tbody><tr class="kb-bos-satir" hidden><td colspan="{n}"><div class="pnl-empty"><div class="pe-ico">{ikon("fa-magnifying-glass")}</div><h2>Bu aramayla {ad} yok</h2><p>Adın bir kısmıyla ya da kısaltmayla arayın; süzgeçleri kaldırmayı deneyin.</p><button type="button" class="pe-tag" data-suz-temizle>{ikon("fa-filter-circle-xmark")}Süzgeçleri Temizle</button></div></td></tr></tbody>
        <tbody data-durum-goster="yukleniyor" hidden>{isk}</tbody>
        <tbody data-durum-goster="hata" hidden><tr><td colspan="{n}"><div class="pnl-empty kb-hata"><div class="pe-ico">{ikon("fa-triangle-exclamation")}</div><h2>{aria} yüklenemedi</h2><p>Sunucuya ulaşılamadı. Görsellerin etiketleri etkilenmez; bağlantınızı kontrol edip yeniden deneyin.</p><a class="pe-tag" href="havuz.html?sekme={pid}">{ikon("fa-rotate-right")}Yeniden Dene</a></div></td></tr></tbody>
        <tbody data-durum-goster="bos" hidden><tr><td colspan="{n}"><div class="pnl-empty"><div class="pe-ico">{ikon(bik)}</div><h2>{bh2}</h2><p>{bp}</p>{byeni}</div></td></tr></tbody>
      </table>
    </div>
    <div class="pnl-menu kb-diger-menu" role="menu">{diger}</div>
  </div>
  </div>
"""


def hv_diger(grup):
    return (dm_grup(grup, "kullanimda bos")
            + dm("Başka Kayıtla Birleştir", "fa-code-merge", "kullanimda bos", ek=' data-birlestir data-birlestir-birim="görsel"')
            + dm_ayir("kullanimda bos") + dm_grup("Kayıt") + dm("Denetim İzinde Gör", "fa-clipboard-list", roller="super gyy", hedef="denetim-izi.liste") + dm_cop())


def hv_kaydet(metin):
    return f'<div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-acc btn-sm" data-kapat data-bildir-hemen="{e(metin)}">{ikon("fa-floppy-disk")}Kaydet</button></div>'


def hv_gor_alt(sil, did, d):
    if d == "cop":
        return ""
    return f'<div class="kb-kap-alt-cubuk"><button type="button" class="btn btn-ghost btn-sm danger kb-sol"{sil}>{ikon("fa-trash")}Çöpe Taşı</button><button type="button" class="btn btn-acc btn-sm" data-sablon-ac="{did}">{ikon("fa-pen")}Düzenle</button></div>'


def hv_sil_metin(ad, gs):
    if not gs:
        return f"“{ad}” hiçbir görselde kullanılmıyor. Çöpe gider, oradan geri alınabilir; işlem denetim izine yazılır."
    return (f"“{ad}” {len(gs)} görselden kalkar: {', '.join(g['ad'] for g in gs)}. Görseller havuzda kalır. "
            "Çöpe gider, oradan geri alınabilir (geri alınca görsellere döner); işlem denetim izine yazılır.")


def hv_kisi_form(fid, k=None):
    k = k or {}
    tur = k.get("tur")
    tr_ = "".join(f'<label class="kb-secenek"><input type="radio" name="{fid}Tur" value="{v}"{" checked" if tur == a else ""}>{a}</label>' for v, a in (("kisi", "Kişi"), ("kurum", "Kurum")))
    return f"""  {kap_dil()}
  <div class="kb-fs"><div class="kb-fs-tt">Bilgiler</div>
    <div class="frow"><label for="{fid}Ad">Ad</label><input class="finput" id="{fid}Ad" data-alan-id="ad" data-zorunlu-metin="Kişinin ya da kurumun adını yazın" value="{e(k.get('ad', ''))}" placeholder="ör. Milli Güvenlik Kurulu"><span class="fhint">Tam ad; görsel etiketlenirken ve aramada görünür.</span></div>
    <div class="frow"><label for="{fid}Ks">Kısaltma</label><input class="finput" id="{fid}Ks" maxlength="12" value="{e(k.get('kisaltma', ''))}" placeholder="ör. MGK, RTE"><span class="fhint">İsteğe bağlı. Görsel kısaltmayla da bulunur; Gez listesinde kısaltma görünür.</span></div>
    <div class="frow"><span class="flabel">Tür</span><div class="kb-secenek-grup" role="radiogroup" aria-label="Tür" data-alan-id="tur" data-zorunlu-metin="Kişi mi kurum mu, seçin">{tr_}</div></div>
  </div>
"""


def hv_kisi_panel(gl):
    kul = hv_kullanim(gl, "kisiler")
    kayitlar = [(k, "") for k in KISILER] + [(k, "cop") for k in COP_KISI]
    sat, sab = "", ""
    for i, (k, cop) in enumerate(kayitlar):
        ad, ks, tur = k["ad"], k.get("kisaltma", ""), k.get("tur", "Kurum")
        gs = [] if cop else kul.get(ad, [])
        n = len(gs)
        d = "cop" if cop else ("kullanimda" if n else "bos")
        vid, did = f"mhKV{i}", f"mhKD{i}"
        hedefler = "|".join(x["ad"] for x, c in kayitlar if not c and x["ad"] != ad)
        nit = {"satir": f"k{i}", "durum": d, "tur": "kisi" if tur == "Kişi" else "kurum", "ara": f"{ad} {ks} {tur}", "baslik": ad,
               "kullanim": (f"{n} görselden kalkar: {', '.join(g['ad'] for g in gs)}; görseller havuzda kalır" if n else None),
               "birlestir-sayi": n, "birlestir-hedefler": hedefler}
        ana = (f'<td class="kb-ana"><div class="rcp-cell"><span class="act-ico">{ikon("fa-user" if tur == "Kişi" else "fa-building-columns")}</span>'
               f'<div class="rcp-id"><div class="rcp-name" title="{e(ad)}">{e(ad)}</div><div class="rcp-by">{f"<b>{e(ks)}</b> · " if ks else ""}{e(tur)}</div></div></div></td>')
        goh = f'<td class="kb-gizle-m"><span class="kb-kat">{hv_on(gs)}</span></td>' if gs else '<td class="kb-gizle-m"><span class="muted">—</span></td>'
        sat += satir(nit, [ana, goh, hv_kul_hucre(d, n)],
                     eylemler(gor_tanim=vid, duz_tanim=did, ad=ad))
        sil = onay("Kişi ya da kurum çöpe taşınsın mı?", hv_sil_metin(ad, gs), "Çöpe Taşı", "fa-trash", tehlike=True, sonra=f"“{ad}” çöpe taşındı",
                   sonra_durum=("cop", "Çöpte", "warm"))
        yk = YUKLEYEN[h(ad, len(YUKLEYEN))]
        sab += f"""<template id="{vid}" data-baslik="{'Kişi' if tur == 'Kişi' else 'Kurum'} Bilgileri" data-alt="{e(ad)}{f' · {e(ks)}' if ks else ''}">
  <dl class="kb-ozet-dl"><dt>Ad</dt><dd>{e(ad)}</dd><dt>Kısaltma</dt><dd>{e(ks) or '—'}</dd><dt>Tür</dt><dd>{e(tur)}</dd><dt>Kullanım</dt><dd>{f'{n} görsel' if n else 'Henüz bir görselde yok'}</dd><dt>Ekleyen</dt><dd>{e(yk)} · {10 + h(ad, 14):02d}.11.2026</dd></dl>
  <div class="kb-fs"><div class="kb-fs-tt">Kullanıldığı Görseller<span class="fs-ek">{n} görsel</span></div><div class="act-list">{hv_gorsel_satirlari(gs)}</div></div>
  {hv_gor_alt(sil, did, d)}
</template>
<template id="{did}" data-baslik="Kişi ya da Kurumu Düzenle" data-alt="{e(ad)}" data-zorunlu-kayit="multimedya.havuz-kisi">
{hv_kisi_form(did, k)}  {hv_kaydet(f"“{ad}” kaydedildi; {n} görselde ve aramada güncellendi" if n else f"“{ad}” kaydedildi")}
</template>
"""
    sab += f"""<template id="mhKYeni" data-baslik="Yeni Kişi ya da Kurum" data-alt="Medya havuzu" data-zorunlu-kayit="multimedya.havuz-kisi">
{hv_kisi_form("mhKYeni")}  {hv_kaydet("Kişi ya da kurum havuza eklendi; görsel etiketlenirken seçilebilir")}
</template>
"""
    say = {"kisi": sum(1 for k, c in kayitlar if not c and k.get("tur") == "Kişi"), "kurum": sum(1 for k, c in kayitlar if not c and k.get("tur") != "Kişi")}
    suz = secim("mhKSuzTur", "", [("", "Bütün Türler"), ("kisi", "Kişi", say["kisi"]), ("kurum", "Kurum", say["kurum"])], suz="tur", etk="Tür:")
    panel = hv_liste("mhPKisi", "mhKListe", "kişi ya da kurum", "Kişi ve kurumlar", "Ad ya da kısaltma ara (RTE, MGK)", suz,
                     [("Ad", "kb-ana"), ("Görseller", "kb-gizle-m"), ("Kullanım", "")], sat,
                     ("fa-address-card", "Henüz kişi ya da kurum yok", "Görsel etiketlenirken eklenir ya da buradan eklenir; kısaltmayla (RTE, MGK) aranır.",
                      f'<button type="button" class="pe-tag" data-tanim="mhKYeni">{ikon("fa-plus")}Yeni Kişi ya da Kurum</button>'),
                     hv_diger("Kişi ve Kurum"), "Görsel etiketlemede ve aramada görünmez olur ve Çöp sekmesine taşınır")
    return panel, sab, sum(1 for _, c in kayitlar if not c)


def hv_etiket_form(fid, ad=""):
    return f"""  {kap_dil()}
  <div class="kb-fs"><div class="kb-fs-tt">Bilgiler</div>
    <div class="frow"><label for="{fid}Ad">Etiket</label><input class="finput" id="{fid}Ad" data-alan-id="ad" data-zorunlu-metin="Etiket adını yazın" value="{e(ad)}" placeholder="ör. raylı sistem"><span class="fhint">Küçük harfle yazılır; özel adlar büyük harfle (İstanbul).</span></div>
  </div>
"""


def hv_etiket_panel(gl):
    kul = hv_kullanim(gl, "etiketler")
    kayitlar = [(x, "") for x in ETIKETLER] + [(x, "cop") for x in COP_ETIKET]
    sat, sab = "", ""
    katlar = set()
    for i, (ad, cop) in enumerate(kayitlar):
        gs = [] if cop else kul.get(ad, [])
        n = len(gs)
        d = "cop" if cop else ("kullanimda" if n else "bos")
        kat = sorted({g.get("etiket", {}).get("kategori", "") for g in gs} - {""}, key=lambda k: EH["kategoriler"].index(k) if k in EH["kategoriler"] else 99)
        katlar.update(kat)
        vid, did = f"mhEV{i}", f"mhED{i}"
        nit = {"satir": f"e{i}", "durum": d, "kategori": "|".join(kat), "ara": ad, "baslik": ad,
               "kullanim": (f"{n} görselden kalkar: {', '.join(g['ad'] for g in gs)}; görseller havuzda kalır" if n else None),
               "birlestir-sayi": n, "birlestir-hedefler": "|".join(x for x, c in kayitlar if not c and x != ad)}
        ana = (f'<td class="kb-ana"><div class="rcp-cell"><span class="act-ico">{ikon("fa-tag")}</span>'
               f'<div class="rcp-id"><div class="rcp-name" title="{e(ad)}">{e(ad)}</div><div class="rcp-by">{hv_on(gs)}</div></div></div></td>')
        kh = f'<td class="kb-gizle-m"><span class="kb-kat">{e(", ".join(kat))}</span></td>' if kat else '<td class="kb-gizle-m"><span class="muted">—</span></td>'
        sat += satir(nit, [ana, kh, hv_kul_hucre(d, n)], eylemler(gor_tanim=vid, duz_tanim=did, ad=ad))
        sil = onay("Etiket çöpe taşınsın mı?", hv_sil_metin(ad, gs), "Çöpe Taşı", "fa-trash", tehlike=True, sonra=f"“{ad}” çöpe taşındı",
                   sonra_durum=("cop", "Çöpte", "warm"))
        yk = YUKLEYEN[h(ad, len(YUKLEYEN))]
        sab += f"""<template id="{vid}" data-baslik="Etiket Bilgileri" data-alt="{e(ad)} · {n} görsel">
  <dl class="kb-ozet-dl"><dt>Etiket</dt><dd>{e(ad)}</dd><dt>Kategoriler</dt><dd>{e(", ".join(kat)) or '—'}</dd><dt>Kullanım</dt><dd>{f'{n} görsel' if n else 'Henüz bir görselde yok'}</dd><dt>Ekleyen</dt><dd>{e(yk)} · {10 + h(ad, 14):02d}.11.2026</dd></dl>
  <div class="kb-fs"><div class="kb-fs-tt">Kullanıldığı Görseller<span class="fs-ek">{n} görsel</span></div><div class="act-list">{hv_gorsel_satirlari(gs)}</div></div>
  {hv_gor_alt(sil, did, d)}
</template>
<template id="{did}" data-baslik="Etiketi Düzenle" data-alt="{e(ad)}" data-zorunlu-kayit="multimedya.havuz-etiket">
{hv_etiket_form(did, ad)}  {hv_kaydet(f"“{ad}” kaydedildi; {n} görselde ve aramada güncellendi" if n else f"“{ad}” kaydedildi")}
</template>
"""
    sab += f"""<template id="mhEYeni" data-baslik="Yeni Etiket" data-alt="Medya havuzu" data-zorunlu-kayit="multimedya.havuz-etiket">
{hv_etiket_form("mhEYeni")}  {hv_kaydet("Etiket havuza eklendi; görsel etiketlenirken seçilebilir")}
</template>
"""
    suz = secim("mhESuzKat", "", [("", "Bütün Kategoriler")] + [(k, k) for k in EH["kategoriler"] if k in katlar], suz="kategori", etk="Kategori:", ara="Kategori ara", ek=" data-suz-coklu")
    panel = hv_liste("mhPEtiket", "mhEListe", "etiket", "Etiketler", "Etiket ara", suz,
                     [("Etiket", "kb-ana"), ("Kategoriler", "kb-gizle-m"), ("Kullanım", "")], sat,
                     ("fa-tags", "Henüz etiket yok", "Görsel etiketlenirken eklenir ya da buradan eklenir.",
                      f'<button type="button" class="pe-tag" data-tanim="mhEYeni">{ikon("fa-plus")}Yeni Etiket</button>'),
                     hv_diger("Etiket"), "Görsel etiketlemede ve aramada görünmez olur ve Çöp sekmesine taşınır")
    return panel, sab, sum(1 for _, c in kayitlar if not c)


def durum_hucre_m(d, n):
    if d == "cop":
        return '<td><span class="pstat warm">Çöpte</span></td>'
    if not n:
        return '<td><span class="pstat off">Kullanılmıyor</span></td>'
    return f'<td><span class="pstat ok">{n} içerik</span></td>'


# =====================================================================
# 14 · Marka şablonu (sablon.html) — ayar ekranı kalıbı
# =====================================================================
def sablon_sayfasi():
    img = "p195.jpg"
    oranlar = "".join(f'<label class="kb-secenek kb-secenek-kart"><input type="checkbox"{" checked" if c else ""}><span><b>{o} · {px}</b><small>{p}</small></span></label>'
                      for o, px, p, c in [("16:9", "1200×675", "X, Telegram, YouTube kapağı", True), ("1:1", "1080×1080", "Instagram, Facebook gönderisi", True), ("4:5", "1080×1350", "Instagram dikey gönderi", True),
                                          ("1.91:1", "1200×630", "Facebook ve LinkedIn bağlantı kartı", True), ("9:16", "1080×1920", "Hikâye ve Reels", False)])
    p1 = f"""    <div class="sa-form-panel" id="pGorsel" role="tabpanel">
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-stamp")}Logo<span class="fs-ek">Temadan gelir</span></div><div class="form-grid">
        <div class="kb-gorsel-kucuk"><span class="kb-logo kb-logo-acik" role="img" aria-label="Dada Haber logosu"></span><div><b>dada.svg · sarı</b><span>Logo ve renk tema dosyasından gelir; tema değişince bütün şablonlar kendiliğinden güncellenir.</span></div></div>
        <div class="frow"><span class="flabel">Logo Konumu</span><div class="kb-konum" data-konum data-ad="msLogo" data-deger="sag-alt" data-etiket="Logo Konumu" data-mo="logo"></div>
          <span class="fhint">9 konumdan biri; önerilen sağ alt (yüzleri ve başlığı kapatmaz). Önizlemede canlı görünür.</span></div>
        <div class="frow two"><div class="frow"><label for="msBoy">Logo Boyutu</label><div class="kb-birim"><input class="finput" id="msBoy" inputmode="numeric" value="14" data-mo="logo-boyut"><span>% genişlik</span></div></div>
          <div class="frow"><label for="msKenar">Kenar Boşluğu</label><div class="kb-birim"><input class="finput" id="msKenar" inputmode="numeric" value="4"><span>%</span></div></div></div>
      </div></div>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-grip-lines")}Kategori Şeridi</div><div class="form-grid">
        <div class="frow"><span class="flabel">Şerit Konumu</span><div class="kb-secenek-grup"><label class="kb-secenek"><input type="radio" name="msSerit" value="ust" data-mo="serit" checked>Üstte</label><label class="kb-secenek"><input type="radio" name="msSerit" value="alt" data-mo="serit">Altta</label><label class="kb-secenek"><input type="radio" name="msSerit" value="yok" data-mo="serit">Şerit Yok</label></div>
          <span class="fhint">Görselin kenarında kategori adı, kategorinin renginde (Haberler › Kategoriler).</span></div>
      </div></div>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-heading")}Başlık Bandı</div><div class="form-grid">
        <div class="toggle-row"><span>Görselin Üstüne Başlık Yaz<small>Instagram ve Telegram'da; X ve Facebook'ta başlık kartın altında zaten görünür</small></span><label class="toggle"><input type="checkbox" data-mo="baslik-bandi" aria-label="Görselin Üstüne Başlık Yaz"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        <div class="toggle-row"><span>Alt Karartma<small>Başlığın okunması için görselin alt yarısı koyulaşır</small></span><label class="toggle"><input type="checkbox" data-mo="karart" checked aria-label="Alt Karartma"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        <div class="frow two"><div class="frow"><label for="msKarartma">Karartma Oranı</label><div class="kb-birim"><input class="finput" id="msKarartma" inputmode="numeric" value="40"><span>%</span></div></div>
          <div class="frow"><span class="flabel">Son Dakika Görseli</span>{secim("msSonDakika", "kirmizi", [("kirmizi", "Kırmızı “SON DAKİKA” Bandı"), ("marka", "Marka Renginde Bant"), ("yok", "Bant Yok")])}</div></div>
      </div></div>
    </div>
"""
    p2 = f"""    <div class="sa-form-panel" id="pOran" role="tabpanel" hidden>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-crop-simple")}Paylaşım Oranları<span class="fs-ek">Kırpma penceresinde “Diğer oranlar” altında</span></div><div class="form-grid">
        <div class="kb-kart-sec">{oranlar}</div>
        <p class="fhint">Platformun önerdiği piksel ölçüleri sosyal medya kaydındaki oran ölçüleriyle aynıdır; oran kapatılınca o platformda bağlantı kartı kullanılır. Odak noktası her görselde ortaktır, oranlar ona göre kendiliğinden hizalanır.</p>
      </div></div>
    </div>
"""
    p3 = f"""    <div class="sa-form-panel" id="pVideo" role="tabpanel" hidden>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-film")}Açılış ve Kapanış</div><div class="form-grid">
        <div class="frow"><span class="flabel">Açılış (Intro)</span>{dosya_alan("video", "Açılış videosu", None, ("dada-intro-2026.mp4", 4194304, 3), sinir=50, yeni=False)}<span class="fhint">Yatay videoların başında, 3 saniyeyi geçmesin.</span></div>
        <div class="frow"><span class="flabel">Kapanış (Outro)</span>{dosya_alan("video", "Kapanış videosu", None, ("dada-outro-2026.mp4", 6291456, 5), sinir=50, yeni=False)}</div>
        {toggle("Akış Videolarında Açılış Yok", "Dikey kısa videolar doğrudan başlar")}
      </div></div>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-closed-captioning")}Alt Yazı Bandı ve Filigran</div><div class="form-grid">
        {toggle("Konuşan Kişinin Adı ve Unvanı (Alt Bant)", "Videoda kişi ilk kez konuşurken 4 saniye görünür")}
        <div class="frow"><span class="flabel">Filigran Logo</span><div class="kb-konum" data-konum data-ad="msFil" data-deger="sag-ust" data-yok="Logo Yok" data-etiket="Filigran Logo Konumu"></div></div>
      </div></div>
    </div>
"""
    yan = f"""    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{ikon("fa-eye")}Önizleme</h2><span class="kb-kap-alt">Ayarlar canlı yansır</span></div>
      <div class="pc-body"><div class="kb-onizle-kap">
        <div id="msOniz" data-marka-oniz data-gorsel="../../veri/gorsel/{img}" data-kategori="Savunma" data-renk="var(--kat-savunma)" data-baslik="KAAN'ın ikinci prototipi test uçuşunda" data-logo="sag-alt" data-serit="ust" data-oran="1:1" data-logo-boyut="14" data-karart></div>
        <p class="kb-onizle-not">Örnek görsel ve başlık; oran düğmeleriyle platform ölçüsünü değiştirin.</p>
      </div></div>
    </section>
    <section class="pnl-card">
      <div class="pc-head"><h2 class="pc-title">{ikon("fa-clock-rotate-left")}Son Değişiklikler</h2></div>
      <div class="act-list">{act_satir("fa-stamp", "Logo konumu: sol üst → sağ alt", "Ayşe Yıldız", "20.11")}{act_satir("fa-crop-simple", "9:16 oranı kapatıldı", "Selin Aydemir", "12.11")}{act_satir("fa-film", "Açılış videosu yenilendi", "Ayşe Yıldız", "01.11")}</div>
    </section>
"""
    ust = sayfa_bas("<h1>Marka Şablonu</h1>", '<div class="ph-sub">Sosyal medya görsellerine ve videolara otomatik eklenen logo, kategori şeridi ve oranlar · son değişiklik 20.11.2026 · Ayşe Yıldız</div>',
                    f'<a class="btn btn-ghost btn-sm" data-hedef="multimedya.video" href="#icerik">{ikon("fa-arrow-left")}Video ve Akış\'a Dön</a>')
    govde = f"""{ust}
  <div class="form-layout">
  <section class="pnl-card" id="msForm" data-form data-sekmeli aria-label="Marka şablonu formu">
    {form_sekmeler([("pGorsel", "fa-image", "Görsel Şablonu", None), ("pOran", "fa-crop-simple", "Oranlar", None), ("pVideo", "fa-film", "Video", None)])}
{p1}{p2}{p3}
  </section>
  <aside class="side-card" aria-label="Önizleme">
{yan}
  </aside>
  </div>
  <div class="kb-kaydet" data-form-icin="msForm">
    <div class="kk-durum">{ikon("fa-circle-check")}<span>Kaydedildi · 20.11.2026 11.40 · Ayşe Yıldız</span></div>
    <div class="kk-sag"><button type="button" class="btn btn-acc btn-sm" data-kaydet data-kaydet-metin="Kaydedildi" data-bildir="Marka şablonu kaydedildi; yeni paylaşımlarda geçerli, önceki hal denetim izinde">{ikon("fa-check")}Kaydet</button></div>
  </div>
"""
    yaz("sablon.html", bas("Marka Şablonu", "multimedya.sablon") + govde + son())


if __name__ == "__main__":
    video_sayfasi(); video_duzenle(); akis_duzenle(); canli_duzenle()
    podcast_sayfasi(); seri_duzenle(); bolum_duzenle()
    sesli_sayfasi(); sesli_duzenle()
    galeri_sayfasi(); galeri_duzenle(); infografik_duzenle()
    havuz_sayfasi(); sablon_sayfasi()
