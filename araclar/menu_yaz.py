#!/usr/bin/env python3
"""Kabuk parçalarını modül kaydından sayfalara yazar (K13: karma yöntem).

Kullanım:  python3 -I araclar/menu_yaz.py [--kontrol] [--uyari] [--yalniz cekirdek/kullanicilar]

Ne yapar:
  1. moduller.json ve veri/panel.json'u okur.
  2. İşaretli sayfalarda <!--P:menu-->…<!--/P:menu--> ve <!--P:ust-->…<!--/P:ust-->
     arasını yeniden yazar (yan menü + üst bar). Bağlantılar sayfanın klasörüne göre göreli.
  3. data-hedef="modul.sayfa" taşıyan öğelere href yazar; modül kapalıysa öğeyi gizler
     (hidden). data-modul="modul" taşıyan kutuları modül kapalıysa gizler. Böylece bir
     modül kayıttan kapatılınca hiçbir yerde kırık bağlantı kalmaz.
  4. cekirdek/js/kayit.js dosyasını üretir (JS'nin rol, izin ve sayfa bilgisi; file://
     altında fetch çalışmadığı için kayıt JS dosyasına gömülür).
  5. Yerel CSS ve JS bağlantılarına içerik özetinden sürüm eki koyar (?v=…).
  6. Denetler: kırık yerel bağlantı, kapalı modüle bağlantı, hazır sayılan ama dosyası
     olmayan sayfa. Sorun varsa çıkış kodu 1.
--kontrol: yalnızca denetler, dosya yazmaz.
"""
import hashlib, html, json, os, re, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KONTROL = "--kontrol" in sys.argv
# --yalniz <klasör|dosya>[,…]: yalnız bunları yazar, kayit.js'e dokunmaz (yayılımda teammate'ler aynı anda çalışır); lead --kayit-js ekleyince kayit.js de yazılır
YALNIZ = sys.argv[sys.argv.index("--yalniz") + 1] if "--yalniz" in sys.argv else None
ATLANAN = {"docs", "tasks", "assets", "secenekler", ".git", "araclar", "veri"}

kayit = json.loads((KOK / "moduller.json").read_text(encoding="utf-8"))
veri = json.loads((KOK / "veri" / "panel.json").read_text(encoding="utf-8"))
moduller = {m["id"]: m for m in kayit["moduller"]}
KATALOG = {b["id"]: b for b in json.loads((KOK / "cekirdek" / "bilesenler.json").read_text(encoding="utf-8"))["bilesenler"]}
acik = {k for k, m in moduller.items() if m.get("acik")}
YAKINDA = kayit["yakinda_sayfasi"]

def esc(s): return html.escape(str(s), quote=True)

def sayfa_haritasi():
    harita = {}
    for m in kayit["moduller"]:
        for s in m.get("sayfalar", []):
            harita[f'{m["id"]}.{s["id"]}'] = {
                "baslik": s["baslik"], "ikon": s.get("ikon", "fa-circle"), "modul": m["id"],
                "modul_ad": m["ad"], "grup": m["grup"], "hazir": bool(s.get("hazir")),
                "dosya": s["dosya"], "roller": s.get("roller", m.get("roller", [])),
                "acik": m["id"] in acik,
            }
    return harita
SAYFALAR = sayfa_haritasi()

def goreli(hedef, sayfa_yolu):
    return os.path.relpath(KOK / hedef, (KOK / sayfa_yolu).parent).replace(os.sep, "/")

def hedef_href(anahtar, sayfa_yolu):
    s = SAYFALAR.get(anahtar)
    if not s:
        raise SystemExit(f"Kayıtta olmayan hedef: {anahtar} ({sayfa_yolu})")
    if s["hazir"]:
        return goreli(s["dosya"], sayfa_yolu)
    return goreli(YAKINDA, sayfa_yolu) + "?s=" + anahtar

OTURUM_HEDEF = {"oturum.profil": "kimlik-yetki.profil", "oturum.oturumlar": "kimlik-yetki.oturumlar", "oturum.cikis": "kimlik-yetki.giris", "oturum.bildirimler": "kimlik-yetki.bildirimler"}
def oturum_href(anahtar, sayfa_yolu):
    """Hesap menüsü ve çıkış: Kimlik ve Yetki sayfaları hazırsa oraya, değilse yapım aşamasına."""
    k = OTURUM_HEDEF.get(anahtar)
    if k and k in SAYFALAR and SAYFALAR[k]["hazir"]:
        return goreli(SAYFALAR[k]["dosya"], sayfa_yolu)
    return goreli(YAKINDA, sayfa_yolu) + "?s=" + anahtar

# ---------------------------------------------------------------- menü
def menu_html(sayfa_yolu):
    kontrol = hedef_href("kontrol-paneli.ana", sayfa_yolu)
    parca = [f'<nav class="sa-menu" id="saMenu" aria-label="Ana menü">',
             f'<div class="sa-menu-head"><a class="kb-logo-bag" href="{esc(kontrol)}" aria-label="{esc(kayit["proje_adi"])} Yönetim Paneli"><span class="kb-logo"></span><span class="kb-logo-isaret"></span></a></div>',
             '<div class="sa-mnav">']
    for g in sorted(kayit["gruplar"], key=lambda g: g["sira"]):
        mods = sorted([m for m in kayit["moduller"] if m["grup"] == g["id"] and m["id"] in acik], key=lambda m: m["sira"])
        linkler = []
        for m in mods:
            for s in m.get("sayfalar", []):
                if not s.get("menude") or not s.get("hazir"):  # yarım sayfa (hazir: false) menüde görünmez (Beyar, 25.11.2026)
                    continue
                anahtar = f'{m["id"]}.{s["id"]}'
                roller = " ".join(s.get("roller", m.get("roller", [])))
                rozet = ""
                if s.get("rozet"):
                    n = veri["rozetler"].get(s["rozet"])
                    if n:
                        rozet = f'<span class="pl-cnt">{esc(n)}</span>'
                linkler.append(
                    f'<a class="sa-mlink" href="{esc(hedef_href(anahtar, sayfa_yolu))}" data-sayfa="{anahtar}" data-roller="{roller}" data-tip="{esc(s["baslik"])}">'
                    f'<i class="fa-solid {esc(s.get("ikon", "fa-circle"))}" aria-hidden="true"></i><span class="ml-ad">{esc(s["baslik"])}</span>{rozet}</a>')
        if not linkler:
            continue
        if g["ad"] is None:
            parca.extend(linkler)
        else:
            parca.append(f'<div class="sa-mgrp" data-grup="{g["id"]}">'
                         f'<button class="sa-msec" type="button" aria-expanded="true">{esc(g["ad"])}<i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button>'
                         f'<div class="sa-mgrp-list"><div>{"".join(linkler)}</div></div></div>')
    parca.append('</div>')
    cikis = oturum_href("oturum.cikis", sayfa_yolu)
    parca.append('<div class="sa-menu-foot">'
                 f'<a class="sa-mlink" href="{esc(cikis)}" data-cikis data-tip="Çıkış"><i class="fa-solid fa-right-from-bracket" aria-hidden="true"></i><span class="ml-ad">Çıkış</span></a>'
                 f'<a class="sa-sig" href="https://gaviaworks.com" target="_blank" rel="noopener" aria-label="Gaviaworks" data-tip="Gaviaworks"><img src="{esc(goreli("assets/gavia-isaret.png", sayfa_yolu))}" alt=""></a>'
                 '</div></nav>'
                 '<button class="sa-divider" id="saDivider" type="button" aria-controls="saMenu" aria-label="Menüyü daralt"><span class="sa-grip" aria-hidden="true"></span></button>')
    return "".join(parca)

def bildirim_html(sayfa_yolu):
    satirlar, okunmadi = [], 0
    for b in veri.get("bildirimler", []):
        s = SAYFALAR[b["hedef"]]
        if not s["acik"]:
            continue
        okunmadi += 1 if b.get("okunmadi") else 0
        satirlar.append(
            f'<a class="kb-bld{" is-yeni" if b.get("okunmadi") else ""}" href="{esc(hedef_href(b["hedef"], sayfa_yolu))}" data-roller="{" ".join(s["roller"])}">'
            f'<span class="kb-bld-ico {esc(b["tur"])}"><i class="fa-solid {esc(b["ikon"])}" aria-hidden="true"></i></span>'
            f'<span class="kb-bld-yazi"><b>{esc(b["baslik"])}</b><span>{esc(b["metin"])}</span></span>'
            f'<span class="kb-bld-saat">{esc(b["saat"])}</span></a>')
    yakinda = goreli(YAKINDA, sayfa_yolu)
    return ('<div class="kb-bld-kap">'
            '<button class="pnl-bell" type="button" data-acilir="bildirimMenu" aria-expanded="false" aria-haspopup="true" data-tip="Bildirimler" aria-label="Bildirimler">'
            '<i class="fa-solid fa-bell" aria-hidden="true"></i><span class="pb-dot"></span></button>'
            '<div class="pnl-menu kb-bildirim" id="bildirimMenu" role="menu">'
            f'<div class="kb-bld-bas"><b>Bildirimler</b><span class="kb-bld-say">{okunmadi} okunmamış</span>'
            '<button type="button" class="kb-bld-oku" data-bld-oku>Tümünü okundu say</button></div>'
            f'<div class="kb-bld-liste">{"".join(satirlar)}</div>'
            f'<a class="kb-bld-alt" href="{esc(oturum_href("oturum.bildirimler", sayfa_yolu))}">Bütün bildirimler<i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>'
            '</div></div>')

# ---------------------------------------------------------------- üst bar
def ust_html(sayfa_yolu):
    yakinda = goreli(YAKINDA, sayfa_yolu)
    roller = {r["id"]: r for r in kayit["roller"]}
    rol_dugmeleri = "".join(
        f'<button type="button" data-rol-sec="{rid}"><i class="fa-solid fa-user-tag" aria-hidden="true"></i>{esc(roller[rid]["ad"])}</button>'
        for rid in kayit["rol_degistirici"])
    return (
        '<header class="pnl-top">'
        '<button class="pnl-burger" id="pnlBurger" type="button" aria-label="Menüyü aç"><i class="fa-solid fa-bars" aria-hidden="true"></i></button>'
        '<div class="pnl-search" role="search"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i>'
        '<label class="sr-only" for="pnlAra">Panelde ara</label>'
        '<input id="pnlAra" type="search" placeholder="Haber, kişi, kaynak ya da ekran ara…" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="araSonuc"><kbd>⌘K</kbd>'
        '<div class="pnl-menu kb-ara-sonuc" id="araSonuc" role="listbox" aria-label="Arama sonuçları"></div></div>'
        '<div class="pnl-top-tools">'
        '<div class="kb-rol"><button class="kb-rol-btn" type="button" data-acilir="rolMenu" aria-expanded="false" aria-haspopup="true">'
        '<i class="fa-solid fa-masks-theater" aria-hidden="true"></i><span class="kr-etk">Rol</span><span class="kr-ad" id="krAd">Süper Admin</span></button>'
        '<div class="pnl-menu" id="rolMenu" role="menu"><div class="pmenu-head"><b>Prototip rol değiştirici</b><span>Seçilen rolün gördüğü menü ve kutular</span></div>'
        f'{rol_dugmeleri}</div></div>'
        f'<a class="pnl-bell kb-site" href="{esc(kayit["site_adresi"])}" target="_blank" rel="noopener" data-tip="Siteyi görüntüle" aria-label="Siteyi görüntüle"><i class="fa-solid fa-globe" aria-hidden="true"></i></a>'
        f'{bildirim_html(sayfa_yolu)}'
        '<div class="kb-hesap"><button class="pnl-me" type="button" data-acilir="hesapMenu" aria-expanded="false" aria-haspopup="true">'
        '<span class="pm-ava" id="pmAva">SA</span><span class="pm-id"><span class="pm-name" id="pmName">Selin Aydemir</span><span class="pm-role" id="pmRole">Süper Admin</span></span>'
        '<i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button>'
        '<div class="pnl-menu" id="hesapMenu" role="menu"><div class="pmenu-head"><b id="pmMenuAd">Selin Aydemir</b><span id="pmMenuEposta">selin.aydemir@dadahaber.ornek</span></div>'
        f'<a href="{esc(oturum_href("oturum.profil", sayfa_yolu))}"><i class="fa-solid fa-user" aria-hidden="true"></i>Profilim</a>'
        f'<a href="{esc(oturum_href("oturum.oturumlar", sayfa_yolu))}"><i class="fa-solid fa-laptop" aria-hidden="true"></i>Aktif oturumlar</a>'
        f'<a class="kb-yalniz-tel" href="{esc(kayit["site_adresi"])}" target="_blank" rel="noopener"><i class="fa-solid fa-globe" aria-hidden="true"></i>Siteyi görüntüle</a>'
        '<div class="pmenu-div"></div>'
        f'<a class="danger" href="{esc(oturum_href("oturum.cikis", sayfa_yolu))}" data-cikis><i class="fa-solid fa-right-from-bracket" aria-hidden="true"></i>Çıkış</a>'
        '</div></div>'
        '</div></header>'
    )

def bas_html(sayfa_yolu):
    return (f'<script src="{esc(goreli("cekirdek/js/kayit.js", sayfa_yolu))}"></script>'
            f'<script src="{esc(goreli("cekirdek/js/erken.js", sayfa_yolu))}"></script>')

# ---------------------------------------------------------------- kayit.js
OTURUM_SAYFALARI = {
    "oturum.cikis": "Çıkış ve giriş ekranı", "oturum.profil": "Profilim",
    "oturum.oturumlar": "Aktif oturumlar", "oturum.bildirimler": "Bildirimler",
}
def kayit_js():
    js = {
        "proje_adi": kayit["proje_adi"],
        "menu": kayit["menu"],
        "roller": {r["id"]: {"ad": r["ad"], "izin_gruplari": r["izin_gruplari"]} for r in kayit["roller"]},
        "rol_degistirici": kayit["rol_degistirici"],
        "etkilesim": {k: v for k, v in kayit.get("etkilesim", {}).items() if not k.startswith("_")},
        "personalar": veri["personalar"],
        "medya": veri.get("medya_havuzu", {}),
        "sayfalar": {k: {x: v[x] for x in ("baslik", "ikon", "modul_ad", "hazir", "acik", "roller")} for k, v in SAYFALAR.items()},
        "oturum_sayfalari": OTURUM_SAYFALARI,
        # görsel alanları ve sosyal platformlar: kırpma penceresi ve sosyal sekme ölçüleri kayıttan okur
        "gorsel_alanlari": {k: (m.get("ayarlar", {}).get("gorsel_alanlari") or m.get("gorsel_alanlari")) for k, m in moduller.items() if (m.get("ayarlar", {}).get("gorsel_alanlari") or m.get("gorsel_alanlari"))},
        "sosyal_platformlar": [x for x in moduller.get("sosyal-medya", {}).get("ayarlar", {}).get("platformlar", []) if x.get("acik")] if "sosyal-medya" in acik else [],
        "sosyal_oranlar": [{"oran": o, "ad": "Sosyal " + o, "px": px} for o, px in moduller.get("sosyal-medya", {}).get("ayarlar", {}).get("oran_olculeri", {}).items()] if "sosyal-medya" in acik else [],
        "sosyal_oneriler": veri.get("sosyal_hesap_onerileri", {}),
        # zorunlu alanlar tek yerden (modül kaydı → ayarlar.zorunlu); anahtar "modul.form"
        "zorunlu": {f"{k}.{f}": v for k, m in moduller.items() for f, v in (m.get("ayarlar", {}) or {}).get("zorunlu", {}).items()},
    }
    return ("/* ÜRETİLMİŞ DOSYA — elle değiştirme. Kaynak: moduller.json + veri/panel.json · araclar/menu_yaz.py */\n"
            "window.PANEL = " + json.dumps(js, ensure_ascii=False, indent=1) + ";\n")

# ---------------------------------------------------------------- yardımcılar
def surum(t, sayfa_yolu):
    def degis(m):
        on, yol, son = m.group(1), m.group(2), m.group(4)
        if yol.startswith(("http", "//")):
            return m.group(0)
        dosya = ((KOK / sayfa_yolu).parent / yol).resolve()
        if not dosya.exists():
            return m.group(0)
        v = hashlib.md5(dosya.read_bytes()).hexdigest()[:8]
        return f'{on}{yol}?v={v}{son}'
    return re.sub(r'((?:href|src)=")([^"?]+\.(?:css|js))(\?v=[0-9a-f]+)?(")', degis, t)

def hedefleri_yaz(t, sayfa_yolu):
    def bas(m):
        etiket = m.group(0)
        anahtar = re.search(r'data-hedef="([^"]+)"', etiket).group(1)
        s = SAYFALAR.get(anahtar)
        if not s:
            raise SystemExit(f"Kayıtta olmayan hedef: {anahtar} ({sayfa_yolu})")
        etiket = re.sub(r'\s(href|hidden)(="[^"]*")?', "", etiket)
        if not s["acik"]:
            return etiket[:-1] + " hidden>"
        ek = re.search(r'data-hedef-ek="([^"]*)"', etiket)
        href = hedef_href(anahtar, sayfa_yolu)
        if ek and SAYFALAR[anahtar]["hazir"]:
            href += html.unescape(ek.group(1))
        return etiket[:-1] + f' href="{esc(href)}">'
    t = re.sub(r'<a\b[^>]*\sdata-hedef="[^"]+"[^>]*>', bas, t)
    def kutu(m):
        # Kapalı modülün kutusu "hidden data-modul-kapali" alır. Açıkken yalnızca bu betiğin koyduğu gizlilik kaldırılır;
        # öğenin kendi varsayılan gizliliğine (sekme paneli, açılır kutu) dokunulmaz.
        etiket = m.group(0)
        mid = re.search(r'data-modul="([^"]+)"', etiket).group(1)
        # Öğe kapatılmadan önce zaten gizliyse (sekme paneli, açılır kutu) işaret data-modul-kapali="kendi" olur
        # ve açılınca hidden kalır; yalnız bu betiğin eklediği hidden kaldırılır.
        m_k = re.search(r'\sdata-modul-kapali(="([^"]*)")?', etiket)
        if m_k:
            kendi = m_k.group(2) == "kendi"
            etiket = etiket.replace(m_k.group(0), "")
            if not kendi:
                etiket = re.sub(r'\shidden(="[^"]*")?', "", etiket)
        if mid in acik:
            return etiket
        if re.search(r'\shidden(?=[\s>=])', etiket):
            return etiket[:-1] + ' data-modul-kapali="kendi">'
        return etiket[:-1] + " hidden data-modul-kapali>"
    return re.sub(r'<\w+\b[^>]*\sdata-modul="[^"]+"[^>]*>', kutu, t)

def katalog_html():
    """UI kitteki bileşen kataloğu: her bileşen, durumu ve onu kullanan açık modüller."""
    kullanan = {}
    for mid, m in moduller.items():
        for b in m.get("bilesenler") or []:
            kullanan.setdefault(b, []).append(m["ad"] + ("" if m.get("acik") else " (kapalı)"))
    satir = []
    for b in KATALOG.values():
        d = '<span class="pstat ok">Hazır</span>' if b["durum"] == "hazir" else '<span class="pstat wait">Yayılımda</span>'
        bag = f'<a class="kb-bag" href="#kit-{esc(b["ui_kit"])}">bölüm</a>' if b["ui_kit"] else "—"
        satir.append(f'<tr><td><b>{esc(b["ad"])}</b><span class="kit-id">{esc(b["id"])}</span></td><td><code>{esc(b["kanca"])}</code></td>'
                     f'<td class="kb-gizle-m">{esc(b["dosya"])}</td><td>{d}</td><td class="kb-gizle-t">{esc(", ".join(kullanan.get(b["id"], [])) or "—")}</td><td class="kb-gizle-m">{esc(b["not"]) or "—"}</td><td>{bag}</td></tr>')
    hazir = sum(1 for b in KATALOG.values() if b["durum"] == "hazir")
    return (f'<p class="kit-not">{len(KATALOG)} bileşen · {hazir} hazır · {len(KATALOG) - hazir} yayılımda, onu kullanan modülden önce çekirdeğe eklenecek. Kaynak: <code>cekirdek/bilesenler.json</code>; <code>moduller.json</code>\'daki her bileşen adı bu listeye göre denetlenir.</p>'
            '<div class="ptable-wrap"><table class="ptable kit-tablo"><thead><tr><th>Bileşen</th><th>Sınıf / çağrı</th><th class="kb-gizle-m">Dosya</th><th>Durum</th><th class="kb-gizle-t">Kullanan modüller</th><th class="kb-gizle-m">Not</th><th></th></tr></thead><tbody>'
            + "".join(satir) + '</tbody></table></div>')

def isaret_yaz(t, ad, icerik):
    desen = re.compile(rf"(<!--P:{ad}-->).*?(<!--/P:{ad}-->)", re.S)
    if not desen.search(t):
        return t, False
    return desen.sub(lambda m: m.group(1) + icerik + m.group(2), t), True

# ---------------------------------------------------------------- çalıştır
def sayfalar():
    for p in sorted(KOK.rglob("*.html")):
        rel = p.relative_to(KOK)
        if rel.parts[0] in ATLANAN:
            continue
        if YALNIZ and not any(rel.as_posix() == y or rel.as_posix().startswith(y.rstrip("/") + "/") for y in YALNIZ.split(",")):
            continue
        yield p, rel.as_posix()

kjs = KOK / "cekirdek" / "js" / "kayit.js"
icerik = kayit_js()
if not KONTROL and (not YALNIZ or "--kayit-js" in sys.argv) and (not kjs.exists() or kjs.read_text(encoding="utf-8") != icerik):
    kjs.write_text(icerik, encoding="utf-8")

sorunlar, yazilan = [], 0
for p, rel in sayfalar():
    t = p.read_text(encoding="utf-8")
    yeni, m1 = isaret_yaz(t, "menu", menu_html(rel))
    yeni, m2 = isaret_yaz(yeni, "ust", ust_html(rel))
    yeni, m3 = isaret_yaz(yeni, "bas", bas_html(rel))
    yeni, _ = isaret_yaz(yeni, "katalog", katalog_html())
    if not (m1 or m2 or m3):   # kabuksuz sayfalar (giriş akışı) yalnız P:bas taşır
        continue
    yeni = hedefleri_yaz(yeni, rel)
    yeni = surum(yeni, rel)
    # denetim: yerel bağlantılar
    for h in re.findall(r'(?:href|src)="([^"#:]+?)(?:[?#][^"]*)?"', yeni):
        if h.startswith(("http", "//", "mailto")) or not h:
            continue
        if not ((KOK / rel).parent / h).resolve().exists():
            sorunlar.append(f"{rel}: kırık bağlantı → {h}")
    # kapalı modülün kendi sayfaları denetlenmez (modül kapalıyken o sayfalara hiçbir yerden ulaşılmaz);
    # aranan: açık modüllerin ve çekirdeğin sayfalarında kapalı modüle bağlantı. Düz metin (<pre>, kod) sayılmaz.
    kapali_sayfa = any(rel.startswith(m["klasor"]) for m in moduller.values() if not m.get("acik") and m.get("klasor"))
    bag = " ".join(re.findall(r'(?:href|src)="([^"]+)"', yeni))
    for anahtar, s in SAYFALAR.items():
        if not kapali_sayfa and not s["acik"] and goreli(s["dosya"], rel) in bag:
            sorunlar.append(f"{rel}: kapalı modüle bağlantı → {anahtar}")
    if '"#"' in yeni:
        sorunlar.append(f'{rel}: boş bağlantı href="#"')
    if yeni != t and not KONTROL:
        p.write_text(yeni, encoding="utf-8")
        yazilan += 1

uyarilar = []
for mid, m in moduller.items():
    for b in m.get("bilesenler") or []:
        if b not in KATALOG:
            sorunlar.append(f"kayıt: {mid} katalogda olmayan bileşeni kullanıyor → {b}")
        elif KATALOG[b]["durum"] != "hazir" and m.get("acik"):
            uyarilar.append(f"{mid}: '{b}' bileşeni henüz yok ({KATALOG[b]['not']})")
for mid in sorted(acik):
    for b in moduller[mid].get("bagimli", []):
        if b not in acik:
            sorunlar.append(f"kayıt: açık modül kapalı modüle bağımlı → {mid} → {b}")
for anahtar, s in SAYFALAR.items():
    if s["hazir"] and not (KOK / s["dosya"]).exists():
        sorunlar.append(f"kayıt: hazır sayılan sayfanın dosyası yok → {anahtar} ({s['dosya']})")

print(f"{'Denetim' if KONTROL else 'Yazıldı'}: {yazilan} sayfa · açık modül {len(acik)}/{len(moduller)}")
if "--uyari" in sys.argv:
    for u in uyarilar:
        print("YAYILIMDAN ÖNCE:", u)
for s in sorunlar:
    print("SORUN:", s)
sys.exit(1 if sorunlar else 0)
