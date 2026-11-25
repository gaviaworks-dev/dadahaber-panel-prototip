#!/usr/bin/env python3
"""Sosyal Medya modülü · Hesaplar sayfası üretici (yalnızca moduller/sosyal-medya/hesaplar.html'e yazar).

Kullanım:  python3 -I moduller/sosyal-medya/_uret.py && python3 -I araclar/menu_yaz.py --yalniz moduller/sosyal-medya/hesaplar.html

Sayfanın başı (head, menü, üst bar) ve sonu (çekirdek betikleri) dosyada olduğu gibi kalır; arada kalan <main> ve
şablonlar buradaki veriden yeniden yazılır. Kurallar:
  - Platform başına bir grup (entegrasyon kartı dili): başlıkta platform, hesap sayısı, en kötü durum, "Hesap ekle".
  - Her hesabın dili vardır; aynı platformda birden çok dil hesabı durabilir. Panelde yalnız Türkçe yayın açık;
    başka dildeki hesap bağlanır, ondan yayın "sonraki aşama".
  - Tek veri görünümü: Kart · Liste değiştirici aynı alanda; Çöp, toplu seçim ve satır eylemleri liste dilinde.
"""
import html, json, re, sys
from pathlib import Path

BURA = Path(__file__).resolve().parent
sys.path.insert(0, str(BURA))
SAYFA = BURA / "hesaplar.html"
e = lambda s: html.escape(str(s), quote=True)
I = lambda c: f'<i class="{c}" aria-hidden="true"></i>'

# Platformlar, sıraları ve açık/kapalı durumu tek kaynaktan: moduller.json → sosyal-medya.ayarlar.platformlar (yalnız okunur).
# Burada yalnız bağlantı biçiminin panel metni durur; kayıtta ikon yoksa yedek ikon buradan.
BAGLANTI = {
    "x":               ("fa-brands fa-x-twitter", "OAuth 2.0",                    "OAuth · hesap ya da marka"),
    "facebook":        ("fa-brands fa-facebook",  "OAuth 2.0 · sayfa erişimi",    "OAuth · yönettiğiniz sayfa"),
    "linkedin":        ("fa-brands fa-linkedin",  "OAuth 2.0",                    "OAuth · şirket sayfası"),
    "instagram":       ("fa-brands fa-instagram", "OAuth (Meta) · işletme",       "OAuth (Meta) · işletme hesabı"),
    "telegram":        ("fa-brands fa-telegram",  "Bot token",                    "Bot token · kanal"),
    "threads":         ("fa-brands fa-threads",   "OAuth (Meta) · Threads API",   "OAuth (Meta) · profil"),
    "bluesky":         ("fa-brands fa-bluesky",   "OAuth · AT Protocol",          "OAuth · AT Protocol hesabı"),
    "youtube-shorts":  ("fa-brands fa-youtube",   "OAuth (Google) · YouTube Data API", "OAuth (Google) · kanal"),
    "instagram-reels": ("fa-brands fa-instagram", "Instagram hesabıyla",          "Instagram hesabıyla paylaşılır"),
    "tiktok":          ("fa-brands fa-tiktok",    "OAuth · Content Posting API",  "OAuth · işletme hesabı"),
}
KOK = BURA.parents[1]
_KAYIT = [m for m in json.loads((KOK / "moduller.json").read_text(encoding="utf-8"))["moduller"] if m["id"] == "sosyal-medya"][0]["ayarlar"]["platformlar"]
PLATFORM = {}
for _k in _KAYIT:
    if not _k.get("acik", True): continue
    _b = BAGLANTI.get(_k["id"], ("fa-solid fa-share-nodes", "OAuth", "OAuth"))
    PLATFORM[_k["id"]] = {"ad": _k["ad"], "ikon": _k.get("ikon") or _b[0], "baglanti": _b[1], "yeni": _b[2],
                          "tur": _k.get("tur", "yazi"), "onay": _k.get("onay_gerekir"), "yol": _k.get("resmi_yol")}
ORTAK = {"instagram-reels": "instagram"}  # ayrı bağlantısı olmayan mecra → hesabını kullandığı platform
DIL = {"Türkçe": ("TR", True), "English": ("EN", False), "العربية": ("AR", False), "Deutsch": ("DE", False)}
KULLANIM = [("Bütün Haberler", "içeriğin dilindeki gönderilere önerilir"), ("Spor Haberleri", "Spor kategorisinde önceden seçili"),
            ("Son Dakika", "son dakika gönderilerinde"), ("Yalnız Elle Seçilince", "kendiliğinden seçilmez")]
IZIN = "Gönderi yayımlama, medya yükleme, istatistik okuma"

# durum: ok | hata | pasif | cop · son: son paylaşım · hata: son hata (yoksa None)
HESAPLAR = [
    dict(id="h1", pl="x", ad="Dada Haber", tut="@dadahaber", alt="286 B takipçi", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="ok",
         token="12.02.2027'ye kadar", son="23.11.2026 16.06", hata=None, ay=412, baglayan="Selin Aydemir · 12.08.2026", bekleyen=4),
    dict(id="h2", pl="x", ad="Dada Haber Spor", tut="@dadahaberspor", alt="94 B takipçi", dil="Türkçe", kul="Spor Haberleri", durum="ok",
         token="12.02.2027'ye kadar", son="23.11.2026 15.47", hata=None, ay=236, baglayan="Selin Aydemir · 12.08.2026", bekleyen=1),
    dict(id="h9", pl="x", ad="Dada News", tut="@dadanews_en", alt="3,2 B takipçi", dil="English", kul="Yalnız Elle Seçilince", durum="ok",
         token="12.02.2027'ye kadar", son="—", hata=None, ay=0, baglayan="Selin Aydemir · 18.11.2026", bekleyen=0),
    dict(id="h3", pl="facebook", ad="Dada Haber", tut="Facebook sayfası", alt="184 B takipçi", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="ok",
         token="18.01.2027'ye kadar", son="23.11.2026 14.06", hata="23.11.2026 15.46 · zaman aşımı, yeniden denendi", ay=298, baglayan="Ece Demirel · 19.09.2026", bekleyen=2),
    dict(id="h4", pl="facebook", ad="Dada Haber Spor", tut="Facebook sayfası", alt="41 B takipçi", dil="Türkçe", kul="Yalnız Elle Seçilince", durum="pasif",
         token="18.01.2027'ye kadar", son="02.11.2026 21.10", hata=None, ay=0, baglayan="Ece Demirel · 19.09.2026", bekleyen=0),
    dict(id="h5", pl="linkedin", ad="Dada Haber", tut="Şirket sayfası", alt="12.400 takipçi", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="ok",
         token="04.01.2027'ye kadar · 42 gün kaldı", son="23.11.2026 14.10", hata=None, ay=64, baglayan="Selin Aydemir · 06.10.2026", bekleyen=3),
    dict(id="h6", pl="instagram", ad="dadahaber", tut="İşletme hesabı", alt="132 B takipçi", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="hata",
         token="23.11.2026 15.30'da doldu", son="22.11.2026 21.40", hata="23.11.2026 15.30 · bağlantının süresi doldu", ay=141, baglayan="Ece Demirel · 24.08.2026", bekleyen=2),
    dict(id="h7", pl="telegram", ad="Dada Haber", tut="kanal · @dadahaber", alt="48.200 abone", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="ok",
         token="süresiz · yenilenene kadar", son="23.11.2026 16.06", hata=None, ay=520, baglayan="Selin Aydemir · 12.08.2026", bekleyen=3),
    dict(id="h8", pl="telegram", ad="Dada Son Dakika", tut="kanal · @dadasondakika", alt="21.700 abone", dil="Türkçe", kul="Son Dakika", durum="ok",
         token="süresiz · yenilenene kadar", son="23.11.2026 15.58", hata=None, ay=188, baglayan="Selin Aydemir · 12.08.2026", bekleyen=0),
    dict(id="h12", pl="threads", ad="Dada Haber", tut="@dadahaber", alt="38 B takipçi", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="ok",
         token="21.01.2027'ye kadar", son="23.11.2026 16.08", hata=None, ay=96, baglayan="Selin Aydemir · 25.11.2026", bekleyen=1),
    dict(id="h13", pl="bluesky", ad="Dada Haber", tut="@dadahaber.bsky.social", alt="11 B takipçi", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="ok",
         token="yenileme token'ı · süresiz", son="23.11.2026 15.20", hata=None, ay=58, baglayan="Selin Aydemir · 25.11.2026", bekleyen=1),
    dict(id="h14", pl="youtube-shorts", ad="Dada Haber", tut="YouTube kanalı · @dadahaber", alt="64 B abone", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="ok",
         token="yenileme token'ı · süresiz", son="22.11.2026 18.00", hata=None, ay=22, baglayan="Ece Demirel · 25.11.2026", bekleyen=1),
    dict(id="h6r", pl="instagram-reels", ref="h6", ad="dadahaber", tut="Instagram işletme hesabı", alt="132 B takipçi", dil="Türkçe", kul="Bütün Haberler", durum="hata",
         token="Instagram hesabıyla · 23.11.2026 15.30'da doldu", son="21.11.2026 20.00", hata="23.11.2026 15.30 · Instagram bağlantısının süresi doldu", ay=14, baglayan="Ece Demirel · 24.08.2026", bekleyen=1),
    dict(id="h15", pl="tiktok", ad="Dada Haber", tut="@dadahaber", alt="27 B takipçi", dil="Türkçe", kul="Bütün Haberler", vars=True, durum="onay",
         token="23.02.2027'ye kadar", son="Henüz herkese açık gönderim yok", hata=None, ay=0, baglayan="Selin Aydemir · 25.11.2026", bekleyen=1),
    dict(id="h11", pl="telegram", ad="Dada Ekonomi", tut="kanal · @dadaekonomi", alt="2.100 abone", dil="Türkçe", kul="Yalnız Elle Seçilince", durum="cop",
         token="bağlantı askıda", son="14.10.2026 09.30", hata=None, ay=0, baglayan="Ece Demirel · 02.09.2026", bekleyen=0),
]
DURUM = {"ok": ("ok", "Bağlı"), "hata": ("warm", "Süresi Doldu"), "onay": ("wait", "Uygulama Onayı Bekliyor"), "pasif": ("off", "Pasif"), "cop": ("warm", "Çöpte")}
ONAY_NOT = "Uygulama onayı bekleniyor · gönderiler yalnız özel görünür"


def yayin_acik(h): return DIL[h["dil"]][1]


def dil_etk(h):
    kod, acik = DIL[h["dil"]]
    if acik: return f'<span class="etk" title="{e(h["dil"])} hesap">{kod}</span>'
    return f'<span class="etk wait" title="{e(h["dil"])} hesap · bu dilde yayın sonraki aşamada açılır">{kod}</span>'


def dil_secim(sid, deger):
    ops = ['<div class="ks-grup">Panelde açık</div>']
    for d, (kod, acik) in DIL.items():
        if d == "English": ops.append('<div class="ks-grup">Sonraki aşama · hesap bağlanır, yayın kapalı</div>')
        ops.append(f'<button type="button" data-deger="{e(d)}" data-ad="{e(d)}"{" class=\"is-sec\"" if d == deger else ""}>{e(d)}<span class="ks-alt">{kod}{" · yayın açık" if acik else ""}</span></button>')
    return (f'<div class="frow"><span class="flabel">Dil</span><div class="kb-secim is-dolu" data-alan-id="dil" data-deger="{e(deger)}" data-bos="Dil seçin">'
            f'<button type="button" class="kb-secim-btn" data-acilir="{sid}" aria-expanded="false" aria-haspopup="listbox"><span class="ks-deger">{e(deger)}</span>{I("fa-solid fa-chevron-down")}</button>'
            f'<div class="pnl-menu kb-secim-menu" id="{sid}"><div class="kb-secim-ara">{I("fa-solid fa-magnifying-glass")}<input type="search" placeholder="Dil ara" aria-label="Dil ara"></div>'
            f'<div class="kb-secim-liste" role="listbox">{"".join(ops)}</div><div class="kb-secim-bos" hidden>Bu adla dil yok. Diller Site Ayarları › Diller\'den eklenir.</div></div></div>'
            '<span class="fhint">Aynı platformda her dil için ayrı hesap bağlanır. Panelde şimdilik yalnız Türkçe yayın açık; başka dildeki hesaptan yayın sonraki aşamada açılır.</span></div>')


def kul_secim(sid, deger):
    ops = "".join(f'<button type="button" data-deger="{e(k)}" data-ad="{e(k)}"{" class=\"is-sec\"" if k == deger else ""}>{e(k)}<span class="ks-alt">{e(a)}</span></button>' for k, a in KULLANIM)
    return (f'<div class="frow"><span class="flabel">Kullanım</span><div class="kb-secim is-dolu" data-alan-id="kullanim" data-deger="{e(deger)}" data-bos="Kullanım">'
            f'<button type="button" class="kb-secim-btn" data-acilir="{sid}" aria-expanded="false" aria-haspopup="listbox"><span class="ks-deger">{e(deger)}</span>{I("fa-solid fa-chevron-down")}</button>'
            f'<div class="pnl-menu kb-secim-menu" id="{sid}"><div class="kb-secim-liste" role="listbox">{ops}</div></div></div>'
            '<span class="fhint">Gönderi oluşturucuda, içeriğin dilindeki hesaplar arasında önceden seçilip seçilmeyeceği.</span></div>')


def ad_alani(fid, deger=None):
    v = f' value="{e(deger)}"' if deger else ' placeholder="ör. Dada Haber Ekonomi"'
    return (f'<div class="frow"><label for="{fid}">Görünen Ad</label><input class="finput" id="{fid}" data-alan-id="ad" data-zorunlu-metin="Hesaba panelde görünecek bir ad verin" data-sayac="32|40"{v}>'
            '<div class="char-meter"><span>Gönderi oluşturucuda ve Yayın takviminde görünür</span><b>0 / 32</b></div></div>')


def anahtar(h, etiket=None):
    adt = f'{h["ad"]} · {PLATFORM[h["pl"]]["ad"]}'
    ch = " checked" if h["durum"] in ("ok", "hata", "onay") else ""
    return (f'<label class="toggle"><input type="checkbox" data-anahtar="{e(adt)} hesabı" data-anahtar-etki="bu hesaba gidecek otomatik ve zamanlanmış gönderiler"{ch} aria-label="{e(etiket or adt + " etkin")}">'
            '<span class="toggle-track"></span><span class="toggle-thumb"></span></label>')


def onay_test(adt, hata):
    sonuc = f"{adt} · Test başarısız: bağlantının süresi dolmuş, yeniden bağlayın" if hata else f"{adt} · Test başarılı: bağlantı çalışıyor, örnek istek 240 ms"
    return (f'data-onay-baslik="{e(adt)} bağlantısı test edilsin mi?" data-onay-metin="Platforma yalnız okuma isteği gönderilir; hesapta paylaşım yapılmaz. Sonuç son hatalarda ve denetim izinde görünür." '
            f'data-onay-evet="Test et" data-onay-ikon="fa-plug-circle-check" data-bildir-sonra="{e(sonuc)}"')


def onay_baglan(h):
    adt = f'{h["ad"]} · {PLATFORM[h["pl"]]["ad"]}'
    if h["pl"] == "telegram":
        return (f'data-onay-baslik="{e(adt)} bot token\'ı yenilensin mi?" data-onay-metin="Yeni token BotFather\'dan alınır ve eskisinin yerine geçer; eski token hemen geçersiz olur. Hassas işlem: e-posta koduyla doğrulanır ve denetim izine maskeli yazılır." '
                f'data-onay-evet="Token\'ı yenile" data-onay-ikon="fa-key" data-kod data-kod-baslik="Token yenilemeyi doğrulayın" data-bildir-sonra="{e(adt)} token\'ı yenilendi"')
    return (f'data-onay-baslik="{e(adt)} yeniden bağlansın mı?" data-onay-metin="{PLATFORM[h["pl"]]["ad"]} izin sayfası açılır; hesapla giriş yapıp izinleri onaylarsınız. Yeni token eskisinin yerine geçer. Hassas işlem: e-posta koduyla doğrulanır ve denetim izine yazılır." '
            f'data-onay-evet="Yeniden bağla" data-onay-ikon="fa-link" data-kod data-kod-baslik="Bağlantıyı doğrulayın" data-bildir-sonra="{e(adt)} yeniden bağlandı; bekleyen gönderimler sıraya alındı"')


# ---------------- liste satırı ----------------
def varsayilan(h):
    """Platform başına tek varsayılan hesap (çekirdek kb-isaret, grup = platform tbody'si; zorunlu: kaldırılırsa ilk hesap otomatik)."""
    if h["durum"] in ("pasif", "cop") or not yayin_acik(h) or h.get("ref"): return ""  # yapılamayan işaretin düğmesi çizilmez
    p = PLATFORM[h["pl"]]["ad"]; on = "true" if h.get("vars") else "false"
    return (f'<button type="button" class="kb-isaret" data-isaret="varsayilan" data-isaret-on="Varsayılan" data-isaret-off="Varsayılan Yap" data-isaret-ikon="fa-star" '
            f'data-isaret-zorunlu data-isaret-oto="Varsayılan (Otomatik)" data-isaret-bildir-on="{e(h["ad"])} artık {p} için varsayılan hesap; gönderilerde önceden seçili gelir" '
            f'data-isaret-bildir-off="{p} için varsayılan kaldırıldı; ilk hesap otomatik varsayılan oldu" aria-pressed="{on}"></button>')


SUTUN = 8


def satir(h):
    p = PLATFORM[h["pl"]]; adt = f'{h["ad"]} · {p["ad"]}'
    sinif, dad = DURUM[h["durum"]]
    pas = " is-pasif" if h["durum"] in ("pasif", "cop") else ""
    kul = f' data-kullanim="{h["bekleyen"]} bekleyen gönderim bu hesaba gidecek; silinince bu gönderimler bekletilir"' if h["bekleyen"] else ""
    ara = f'{h["ad"]} {h["tut"]} {p["ad"]} {h["dil"]} {h["kul"]}'
    # aynı bilgi iki görünümde: sütun başlığındaki data-kart, ızgarada hücrenin kart içindeki yerini verir (çekirdek). Boş değer çizgiyle değil yer tutucu metinle
    if h["hata"]:
        hata = f'<td class="kb-gizle-t kb-kisalt" title="{e(h["hata"])}">{I("fa-solid fa-triangle-exclamation")} <b>{e(h["hata"])}</b></td>'
    elif h["durum"] == "onay":
        hata = f'<td class="kb-gizle-t kb-kisalt" title="{ONAY_NOT}">{I("fa-solid fa-hourglass-half")} {ONAY_NOT}</td>'
    else:
        hata = f'<td class="kb-gizle-t" title="Son hata">{I("fa-solid fa-circle-check")} <span class="muted">Hata yok</span></td>'
    son = f'<span class="kb-tarih">{e(h["son"])}</span>' if re.match(r"\d", h["son"]) else f'<span class="muted">{e("Henüz gönderim yok" if h["son"] == "—" else h["son"])}</span>'
    sonraki = '' if yayin_acik(h) else ' <span class="etk wait" title="Bu dilde yayın sonraki aşamada açılır">Sonraki Aşama</span>'
    etkin = anahtar(h) if h["durum"] != "cop" else '<span class="muted">Çöpte</span>'
    hid = h.get("ref") or h["id"]  # ortak satır (Reels): bağlı hesabın kaydını açar; ayrı silinmez, seçilmez
    sec = '' if h.get("ref") else f'<input type="checkbox" class="kb-onay-kutu" aria-label="Seç: {e(adt)}">'
    sil = '' if h.get("ref") else f'<button type="button" class="ia-btn danger" data-sil aria-label="Çöpe Taşı" title="Çöpe Taşı">{I("fa-solid fa-trash")}</button>'
    return (f'<tr data-satir="{h["id"]}" data-durum="{h["durum"]}" data-platform="{h["pl"]}" data-dil="{e(h["dil"])}" data-ara="{e(ara)}" data-baslik="{e(adt)}"{kul}>'
            f'<td class="kb-sec-hucre">{sec}</td>'
            f'<td class="kb-ana"><div class="rcp-cell"><span class="kb-ava{pas}">{I(p["ikon"])}</span><div class="rcp-id">'
            f'<div class="rcp-name" title="{e(adt)}">{e(h["ad"])} <span class="muted">{e(h["tut"])}</span></div>'
            f'<div class="rcp-by">{dil_etk(h)}{sonraki} {e(h["kul"])}</div></div></div></td>'
            f'<td><span class="pstat {sinif}">{dad}</span></td>'
            f'{hata}'
            f'<td class="kb-gizle-m" title="Son gönderim">{I("fa-solid fa-paper-plane")} {son}</td>'
            f'<td class="kb-gizle-m">{varsayilan(h)}</td>'
            f'<td class="kb-gizle-m">{etkin}</td>'
            '<td><div class="row-acts">'
            f'<button type="button" class="ia-btn" data-tanim="hsGor-{hid}" aria-label="Görüntüle" title="Görüntüle">{I("fa-solid fa-eye")}</button>'
            f'<button type="button" class="ia-btn" data-tanim="hsDuz-{hid}" aria-label="Düzenle" title="Düzenle">{I("fa-solid fa-pen")}</button>'
            f'{sil}'
            f'<button type="button" class="ia-btn" data-diger aria-haspopup="true" aria-expanded="false" aria-label="Diğer işlemler" title="Diğer">{I("fa-solid fa-ellipsis")}</button>'
            '</div></td></tr>')


def grup(pl):
    p = PLATFORM[pl]; hs = [h for h in HESAPLAR if h["pl"] == pl]
    canli = [h for h in hs if h["durum"] != "cop"]
    if any(h["durum"] == "hata" for h in canli): ps = '<span class="pstat warm">Bağlantı hatası</span>'
    elif any(h["durum"] == "onay" for h in canli): ps = '<span class="pstat wait">Uygulama onayı bekliyor</span>'
    elif any(h["durum"] == "ok" for h in canli): ps = '<span class="pstat ok">Bağlı</span>'
    else: ps = '<span class="pstat off">Pasif</span>'
    diller = sorted({DIL[h["dil"]][0] for h in canli}, key=lambda k: (k != "TR", k))
    ek = f'{len(canli)} hesap · {" ve ".join(diller)} · {p["baglanti"]}'
    if pl in ORTAK: ek = f'{PLATFORM[ORTAK[pl]]["ad"]} hesabıyla paylaşılır · ayrı bağlantı yok · {"video" if p["tur"] == "video" else "yazı ve görsel"}'
    elif p["tur"] == "video": ek += " · yalnız video"
    if p["onay"]: ek += f' · {p["onay"].lower()}'
    if pl == "linkedin": ek += " · token 04.01.2027'de yenilenmeli"
    ekle = '' if pl in ORTAK else f'<button type="button" class="btn btn-ghost btn-sm" data-tanim="hsYeni-{pl}">{I("fa-solid fa-plus")}Hesap ekle</button>'
    bas = (f'<tr class="kb-grup-bas"><td colspan="{SUTUN + 1}"><div class="kb-entegre-bas"><span class="kb-entegre-ikon">{I(p["ikon"])}</span>'
           f'<div><b>{p["ad"]}</b><small>{e(ek)}</small></div>{ps}'
           f'{ekle}</div></td></tr>')
    return f'<tbody data-satirlar data-grup="{pl}" data-isaret-grup>{bas}{"".join(satir(h) for h in hs)}</tbody>'


# ---------------- şablonlar ----------------
def yeni_sablon(pl=None):
    sid = f"hsYeni-{pl}" if pl else "hsYeni"; ek = pl or "g"
    kartlar = "".join(
        f'<label class="kb-secenek kb-secenek-kart"><input type="radio" name="hsYeniPl-{ek}" value="{k}"{" data-ac=\"hsYeniTg-" + ek + "\"" if k == "telegram" else ""}{" checked" if k == pl else ""}>'
        f'<span><b>{I(v["ikon"])} {v["ad"]}</b><small>{v["yeni"]}{" · " + v["onay"].lower() if v["onay"] else ""}</small></span></label>' for k, v in PLATFORM.items() if k not in ORTAK)
    ortak = "".join(f'<p class="fhint">{v["ad"]} ayrı bağlanmaz; {PLATFORM[ORTAK[k]]["ad"]} hesabıyla paylaşılır.</p>' for k, v in PLATFORM.items() if k in ORTAK)
    alt = f'{PLATFORM[pl]["ad"]} · {PLATFORM[pl]["baglanti"]}' if pl else "OAuth ya da bot token"
    tg_gizli = "" if pl == "telegram" else " hidden"
    return f'''<template id="{sid}" data-baslik="Hesap bağla" data-alt="{e(alt)}" data-zorunlu-kayit="sosyal-medya.hesap">
  <div class="kb-fs"><div class="kb-fs-tt">Platform</div>
    <div class="kb-kart-sec" data-alan-id="platform" data-zorunlu-metin="Bağlanacak platformu seçin" role="radiogroup" aria-label="Platform">{kartlar}</div>
    {ortak}
  </div>
  <div class="kb-fs"><div class="kb-fs-tt">Hesap</div>
    {ad_alani("hsYeniAd-" + ek)}
    <div class="frow two">
      {dil_secim("hsYeniDil-" + ek, "Türkçe")}
      {kul_secim("hsYeniKul-" + ek, "Yalnız Elle Seçilince")}
    </div>
  </div>
  <div class="kb-fs"><div class="kb-fs-tt">Bağlantı</div>
    <div class="kb-bant bilgi">{I("fa-solid fa-circle-info")}<span><b>Panel şifre sormaz.</b> “Bağla”ya basınca platformun onay sayfası açılır; hesapla giriş yapıp yayımlama iznini onaylarsınız. Token panelde maskeli saklanır.</span></div>
    <div id="hsYeniTg-{ek}"{tg_gizli}>
      <div class="frow"><span class="flabel">Bot token</span><div class="kb-maske" data-maske-yeni data-ad="Telegram bot token"><div class="km-ust">{I("fa-solid fa-lock km-kilit")}<span class="km-deger">Henüz girilmedi</span><button type="button" class="btn btn-ghost btn-sm" data-maske-yenile>{I("fa-solid fa-key")}Token'ı gir</button></div><span class="km-meta">BotFather'dan alınan token; kaydetmek e-posta koduyla doğrulanır, yalnız bir kez açık görünür.</span><div class="km-acik" hidden><p>{I("fa-solid fa-triangle-exclamation")}Bu değer yalnızca şimdi görünür; kapatınca bir daha gösterilmez.</p><code></code><div class="km-acik-btn"><button type="button" class="btn btn-acc btn-sm" data-maske-kopyala>{I("fa-solid fa-copy")}Kopyala</button><button type="button" class="btn btn-ghost btn-sm" data-maske-gizle>Kapat</button></div></div></div></div>
      <div class="frow"><label for="hsYeniKanal-{ek}">Kanal</label><input class="finput" id="hsYeniKanal-{ek}" placeholder="ör. @dadaekonomi"><span class="fhint">Botu önce kanala yönetici olarak ekleyin.</span></div>
    </div>
  </div>
  <div class="kb-kap-alt-cubuk">
    <button type="button" class="btn btn-acc btn-sm" data-onay-baslik="Hesap bağlansın mı?" data-onay-metin="Telegram dışındaki mecralarda platformun onay sayfası açılır; Telegram'da bot token kanala test mesajı göndermeden doğrulanır. Hesap bağlamak hassas işlemdir: e-posta koduyla doğrulanır ve denetim izine yazılır." data-onay-evet="Bağla" data-onay-ikon="fa-link" data-kod data-kod-baslik="Hesap bağlamayı doğrulayın" data-bildir-sonra="Hesap bağlandı; platform kartında ve gönderi oluşturucuda görünür">{I("fa-solid fa-link")}Bağla</button>
  </div>
</template>'''


def gor_sablon(h):
    p = PLATFORM[h["pl"]]; adt = f'{h["ad"]} · {p["ad"]}'; sinif, dad = DURUM[h["durum"]]
    bant = ""
    if not yayin_acik(h):
        bant = (f'<div class="kb-bant uyari">{I("fa-solid fa-language")}<span><b>{e(h["dil"])} hesap · yayın sonraki aşama.</b> Hesap bağlı ve token geçerli; '
                'panelde bu dil açılınca gönderi oluşturucuda bu dildeki içeriklere önerilir. Şimdilik bu hesaba gönderim yapılmaz.</span></div>\n  ')
    elif h["durum"] == "onay":
        bant = (f'<div class="kb-bant uyari">{I("fa-solid fa-hourglass-half")}<span><b>Uygulama onayı bekleniyor.</b> {p["yol"]} incelemesi bitene kadar bu hesaba giden gönderiler '
                'yalnız özel (hesabın kendisine) görünür; onay gelince herkese açık paylaşılır. Bağlantı ve token geçerli.</span></div>\n  ')
    elif h["durum"] == "hata":
        bant = f'<div class="kb-bant tehlike">{I("fa-solid fa-triangle-exclamation")}<span><b>Bağlantının süresi doldu.</b> {h["bekleyen"]} gönderim bekletiliyor; yeniden bağlanınca sıradaki zamanda kendiliğinden gider.</span></div>\n  '
    test = f'<button type="button" class="btn btn-ghost btn-sm" {onay_test(adt, h["durum"] == "hata")}>{I("fa-solid fa-plug-circle-check")}Bağlantıyı test et</button>' if h["durum"] != "cop" else ""
    duz = f'<button type="button" class="btn btn-acc btn-sm" data-sablon-ac="hsDuz-{h["id"]}">{I("fa-solid fa-pen")}Düzenle</button>'
    return f'''<template id="hsGor-{h["id"]}" data-baslik="{e(adt)}" data-alt="{e(h["tut"])} · {e(h["alt"])}">
  {bant}<div class="kb-hesap-kutu"><span class="kb-ava k-lg">{I(p["ikon"])}</span><div><b>{e(h["ad"])}</b><span>{e(h["tut"])} · {e(h["dil"])}</span></div><span class="pstat {sinif}">{dad}</span></div>
  <dl class="kb-ozet-dl">
    <dt>Dil</dt><dd>{e(h["dil"])}{"" if yayin_acik(h) else " · yayın sonraki aşama"}</dd>
    <dt>Kullanım</dt><dd>{e(h["kul"])}</dd>
    <dt>Varsayılan</dt><dd>{"Evet · " + PLATFORM[h["pl"]]["ad"] + " gönderilerinde önceden seçili" if h.get("vars") else "Hayır"}</dd>
    <dt>Bağlantı</dt><dd>{e(p["baglanti"])}</dd>
    <dt>Token</dt><dd>{e(h["token"])}</dd>
    <dt>İzinler</dt><dd title="{IZIN}">{IZIN}</dd>
    <dt>Son paylaşım</dt><dd>{e(h["son"])}</dd>
    <dt>Son hata</dt><dd>{e(h["hata"] or "—")}</dd>
    <dt>Bu Ay</dt><dd>{h["ay"]} gönderi</dd>
    <dt>Bağlayan</dt><dd>{e(h["baglayan"])}</dd>
  </dl>
  <div class="kb-kap-alt-cubuk">
    {test}
    {duz}
  </div>
</template>'''


def duz_sablon(h):
    p = PLATFORM[h["pl"]]; adt = f'{h["ad"]} · {p["ad"]}'; sinif, dad = DURUM[h["durum"]]
    if yayin_acik(h):
        durum = f'<div class="toggle-row"><span>Hesap etkin<small>Kapalıyken bu hesaba gönderim yapılmaz; bağlantı korunur</small></span>{anahtar(h, "Hesap etkin")}</div>'
    else:
        durum = f'<p class="fhint">{e(h["dil"])} hesaptan yayın sonraki aşamada açılır; o zamana kadar bu hesaba gönderim yapılmaz.</p>'
    return f'''<template id="hsDuz-{h["id"]}" data-baslik="Hesabı düzenle" data-alt="{e(adt)} · değişiklik denetim izine yazılır" data-zorunlu-kayit="sosyal-medya.hesap">
  <div class="kb-fs"><div class="kb-fs-tt">Hesap</div>
    <div class="frow"><span class="flabel">Platform</span><div class="kb-kart-sec" data-alan-id="platform"><label class="kb-secenek kb-secenek-kart"><input type="radio" name="hsPl-{h["id"]}" value="{h["pl"]}" checked disabled><span><b>{I(p["ikon"])} {p["ad"]}</b><small>Platform değişmez; başka platform için yeni hesap bağlayın</small></span></label></div></div>
    {ad_alani("hsAd-" + h["id"], h["ad"])}
    <div class="frow two">
      {dil_secim("hsDil-" + h["id"], h["dil"])}
      {kul_secim("hsKul-" + h["id"], h["kul"])}
    </div>
  </div>
  <div class="kb-fs"><div class="kb-fs-tt">Bağlantı</div><div class="kb-hesap-kutu"><span class="kb-ava">{I(p["ikon"])}</span><div><b>{e(p["baglanti"])}</b><span>Token {e(h["token"])}</span></div><span class="pstat {sinif}">{dad}</span></div><div class="frow"><span class="flabel">İzinler</span><span class="fhint">{IZIN}. İzinler platformun onay sayfasında verilir; panel şifre saklamaz.</span></div><div class="kg-acts"><button type="button" class="btn btn-ghost btn-sm" {onay_baglan(h)}>{I("fa-solid fa-key" if h["pl"] == "telegram" else "fa-solid fa-link")}{"Token'ı yenile" if h["pl"] == "telegram" else "Yeniden bağla"}</button></div></div>
  <div class="kb-fs"><div class="kb-fs-tt">Durum</div>
    {durum}
  </div>
  <div class="kb-kap-alt-cubuk">
    <button type="button" class="btn btn-ghost btn-sm kb-sol" data-sablon-ac="hsGor-{h["id"]}">{I("fa-solid fa-arrow-left")}Hesaba dön</button>
    <button type="button" class="btn btn-acc btn-sm" data-sablon-ac="hsGor-{h["id"]}" data-bildir-sonra="Hesap güncellendi; önceki hal denetim izinde">{I("fa-solid fa-floppy-disk")}Kaydet</button>
  </div>
</template>'''


# ---------------- sayfa gövdesi ----------------
def ana():
    canli = [h for h in HESAPLAR if h["durum"] != "cop" and not h.get("ref")]
    tr_n = sum(1 for h in canli if yayin_acik(h)); diger = len(canli) - tr_n
    hata_n = sum(1 for h in canli if h["durum"] == "hata")
    alt = f'{len(PLATFORM)} platform · {len(canli)} hesap ({tr_n} Türkçe, {diger} English) · {hata_n} bağlantı hatası · son kontrol 23.11.2026 16.04'
    sekme = lambda s, ad, on=False: f'<button type="button" class="chip{" is-on" if on else ""}" role="tab" aria-selected="{"true" if on else "false"}" data-sekme="{s}" data-taban="0">{ad}<span class="ch-cnt">0</span></button>'
    dil_ops = "".join(f'<button type="button" data-deger="{e(d)}" data-ad="{e(d)}">{e(d)}</button>' for d in ("Türkçe", "English"))
    bos = lambda ikon, bas, metin, eylem: f'<tr><td colspan="{SUTUN + 1}"><div class="pnl-empty{" kb-hata" if "yüklenemedi" in bas else ""}"><div class="pe-ico">{I(ikon)}</div><h2>{bas}</h2><p>{metin}</p>{eylem}</div></td></tr>'
    iskelet = "".join(f'<tr class="kb-iskelet"><td></td><td><div class="rcp-cell"><span class="ks-gorsel"></span><div class="rcp-id"><span></span></div></div></td>{"<td><span></span></td>" * (SUTUN - 2)}<td></td></tr>' for _ in range(4))
    return f'''<main class="pnl-main" id="icerik">
  <div class="pnl-page-head">
    <div>
      <h1>Sosyal medya hesapları</h1>
      <div class="ph-sub">{alt}</div>
    </div>
    <div class="ph-actions">
      <a class="btn btn-ghost btn-sm" data-hedef="sosyal-medya.kuyruk" href="kuyruk.html">{I("fa-solid fa-calendar-check")}Yayın takvimi</a>
      <button type="button" class="btn btn-acc btn-sm" data-tanim="hsYeni">{I("fa-solid fa-plus")}Hesap bağla</button>
    </div>
  </div>

  <div class="kb-bant tehlike dash-row">{I("fa-solid fa-triangle-exclamation")}<span><b>Instagram bağlantısının süresi 15.30'da doldu.</b> 2 gönderim bekletiliyor (16.30 ve 17.00); hesap yeniden bağlanınca sıradaki zamanda kendiliğinden gider.</span><button type="button" class="btn btn-ghost btn-sm kb-bant-eylem" data-onay-baslik="Instagram yeniden bağlansın mı?" data-onay-metin="Meta izin sayfası açılır; dadahaber hesabıyla giriş yapıp izinleri onaylarsınız. Bağlanınca bekletilen 2 gönderim sıradaki zamanda gider. E-posta koduyla doğrulanır ve denetim izine yazılır." data-onay-evet="Yeniden bağla" data-onay-ikon="fa-link" data-kod data-kod-baslik="Bağlantıyı doğrulayın" data-bildir-sonra="Instagram yeniden bağlandı; bekletilen 2 gönderim sıraya alındı">{I("fa-solid fa-link")}Yeniden bağla</button></div>

  <section class="pnl-card" data-liste data-grupla data-liste-ad="hesap" data-gorunum="izgara" id="hsListe" data-liste-cop-not="Bağlantı askıya alınır ve Çöp sekmesine taşınır; bu hesaba gönderim yapılmaz" data-sayfa-boy="50" aria-labelledby="hsBas">
    <h2 class="sr-only" id="hsBas">Platformlar ve hesaplar</h2>
    <div class="kb-liste-ust">
      <div class="chips" role="tablist" aria-label="Bağlantı durumuna göre">
        {sekme("hepsi", "Tümü", True)}{sekme("ok", "Bağlı")}{sekme("hata", "Sorunlu")}{sekme("onay", "Onay Bekliyor")}{sekme("pasif", "Pasif")}
      </div>
      <button type="button" class="chip kb-cop" role="tab" aria-selected="false" data-sekme="cop" data-taban="0">{I("fa-solid fa-trash")}Çöp<span class="ch-cnt">0</span></button>
    </div>
    <div class="filter-bar">
      <div class="fb-search">{I("fa-solid fa-magnifying-glass")}
        <label class="sr-only" for="hsAra">Hesaplarda Ara</label>
        <input id="hsAra" type="search" data-liste-ara placeholder="Hesap adı, tutamaç ya da platform ara" autocomplete="off">
      </div>
      <div class="kb-secim" data-suz="dil" data-bos="Tümü"><button type="button" class="kb-secim-btn" data-acilir="hsSuzDil" aria-expanded="false" aria-haspopup="listbox"><span class="ks-etk">Dil:</span><span class="ks-deger">Tümü</span>{I("fa-solid fa-chevron-down")}</button><div class="pnl-menu kb-secim-menu" id="hsSuzDil"><div class="kb-secim-liste" role="listbox"><button type="button" data-deger="" data-ad="Bütün diller">Bütün diller</button>{dil_ops}</div></div></div>
      <button type="button" class="kb-suz-temizle" data-suz-temizle hidden>Süzgeçleri temizle</button>
      <div class="kb-gorunum-sec" data-gorunum-sec role="group" aria-label="Görünüm"><button type="button" class="chip" data-gorunum="izgara" aria-pressed="false">{I("fa-solid fa-grip")}Kart</button><button type="button" class="chip" data-gorunum="liste" aria-pressed="false">{I("fa-solid fa-list")}Liste</button></div>
    </div>
    <div class="kb-toplu" hidden>
      <b data-secili-say>0 hesap seçildi</b>
      <span class="kb-toplu-ayir"></span>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="test" data-bildir="Seçilen hesapların bağlantısı test edildi; sonuçlar son hatalarda">{I("fa-solid fa-plug-circle-check")}<span>Bağlantıyı Test Et</span></button>
      <button type="button" class="btn btn-ghost btn-sm" data-toplu="pasif" data-toplu-durum="pasif" data-toplu-durum-ad="Pasif" data-toplu-durum-sinif="off" data-bildir="Seçilen hesaplar pasif yapıldı; bu hesaplara gönderim yapılmaz">{I("fa-solid fa-circle-pause")}<span>Pasif yap</span></button>
      <button type="button" class="btn btn-ghost btn-sm danger" data-toplu="cop">{I("fa-solid fa-trash")}<span>Çöpe Taşı</span></button>
      <button type="button" class="kb-suz-temizle" data-secim-temizle>Seçimi temizle</button>
    </div>
    <div class="ptable-wrap">
      <table class="ptable">
        <thead>
          <tr>
            <th class="kb-sec-hucre" data-kart="sec"><input type="checkbox" class="kb-onay-kutu" data-hepsini-sec aria-label="Görünen bütün hesapları seç"></th>
            <th class="kb-ana" data-kart="ad">Hesap</th>
            <th data-kart="durum">Durum</th>
            <th class="kb-gizle-t" data-kart="neden">Son Hata</th>
            <th class="kb-gizle-m" data-kart="zaman">Son Gönderim</th>
            <th class="kb-gizle-m" data-kart="isaret">Varsayılan</th>
            <th class="kb-gizle-m" data-kart="etkin">Etkin</th>
            <th data-kart="eylem"><span class="sr-only">İşlemler</span></th>
          </tr>
        </thead>
        {"".join(grup(pl) for pl in PLATFORM)}
        <tbody>
          <tr class="kb-bos-satir" hidden><td colspan="{SUTUN + 1}"><div class="pnl-empty">
            <div class="pe-ico">{I("fa-solid fa-magnifying-glass")}</div>
            <h2>Bu süzgeçlerle hesap bulunamadı</h2>
            <p>Arama metnini kısaltmayı ya da süzgeçleri kaldırmayı deneyin.</p>
            <button type="button" class="pe-tag" data-suz-temizle>{I("fa-solid fa-filter-circle-xmark")}Süzgeçleri temizle</button>
          </div></td></tr>
        </tbody>
        <tbody data-durum-goster="yukleniyor" hidden>{iskelet}</tbody>
        <tbody data-durum-goster="hata" hidden>{bos("fa-solid fa-triangle-exclamation", "Hesaplar yüklenemedi", "Sunucuya ulaşılamadı. Bağlantınızı kontrol edip yeniden deneyin; sorun sürerse sistem yöneticisine haber verin.", '<a class="pe-tag" href="hesaplar.html">' + I("fa-solid fa-rotate-right") + 'Yeniden dene</a>')}</tbody>
        <tbody data-durum-goster="bos" hidden>{bos("fa-solid fa-share-nodes", "Henüz bağlı hesap yok", "Bir sosyal medya hesabı bağlayın; gönderi oluşturucu ve haberlerin Sosyal Medya sekmesi bağlı hesaplara, içeriğin diline göre paylaşır.", '<button type="button" class="pe-tag" data-tanim="hsYeni">' + I("fa-solid fa-plus") + 'Hesap bağla</button>')}</tbody>
      </table>
    </div>

    <div class="pnl-menu kb-diger-menu" role="menu">
      <div class="kb-dm-grup" data-durum-icin="ok hata onay pasif">Bağlantı</div>
      <button type="button" data-durum-icin="ok hata onay pasif" data-onay-baslik="Hesabın bağlantısı test edilsin mi?" data-onay-metin="Platforma yalnız okuma isteği gönderilir; hesapta paylaşım yapılmaz. Sonuç son hatalarda ve denetim izinde görünür." data-onay-evet="Test et" data-onay-ikon="fa-plug-circle-check" data-bildir-sonra="Test tamamlandı; sonuç son hatalarda ve denetim izinde">{I("fa-solid fa-plug-circle-check")}Bağlantıyı test et</button>
      <button type="button" data-durum-icin="ok hata onay pasif" data-kosul-icin="platform:{' '.join(k for k in PLATFORM if k not in ORTAK and k != 'telegram')}" data-onay-baslik="Hesap yeniden bağlansın mı?" data-onay-metin="Platformun izin sayfası açılır; hesapla giriş yapıp izinleri onaylarsınız. Yeni token eskisinin yerine geçer. E-posta koduyla doğrulanır ve denetim izine yazılır." data-onay-evet="Yeniden bağla" data-onay-ikon="fa-link" data-kod data-kod-baslik="Bağlantıyı doğrulayın" data-sonra-durum="ok" data-sonra-durum-ad="Bağlı" data-sonra-durum-sinif="ok" data-bildir-sonra="Hesap yeniden bağlandı; bekleyen gönderimler sıraya alındı">{I("fa-solid fa-link")}Yeniden bağla</button>
      <button type="button" data-durum-icin="ok hata onay pasif" data-kosul-icin="platform:telegram" data-onay-baslik="Bot token'ı yenilensin mi?" data-onay-metin="Yeni token BotFather'dan alınır ve eskisinin yerine geçer; eski token hemen geçersiz olur. E-posta koduyla doğrulanır ve denetim izine maskeli yazılır." data-onay-evet="Token'ı yenile" data-onay-ikon="fa-key" data-kod data-kod-baslik="Token yenilemeyi doğrulayın" data-bildir-sonra="Bot token'ı yenilendi">{I("fa-solid fa-key")}Token'ı yenile</button>
      <a data-durum-icin="ok hata onay pasif" data-hedef="sosyal-medya.kuyruk" href="kuyruk.html">{I("fa-solid fa-calendar-check")}Yayın takviminde gör</a>
      <a data-durum-icin="ok hata onay pasif" data-roller="super gyy" data-hedef="denetim-izi.liste" href="../../cekirdek/denetim-izi/index.html">{I("fa-solid fa-clipboard-list")}Denetim izinde gör</a>
      <div class="pmenu-div" data-durum-icin="cop"></div>
      <button type="button" data-durum-icin="cop" data-geri-al>{I("fa-solid fa-rotate-left")}Çöpten geri al</button>
      <button type="button" class="danger" data-durum-icin="cop" data-kalici-sil>{I("fa-solid fa-trash-can")}Kalıcı olarak sil</button>
    </div>
  </section>
  <p class="fhint kb-ust-bosluk">Panel platform şifresi saklamaz: Telegram bot token ile, diğer mecralar platformun onay sayfasıyla (OAuth) bağlanır; Instagram Reels Instagram hesabını kullanır. Değişiklikler e-posta koduyla doğrulanır ve denetim izine maskeli yazılır. Mecraların sırası ve açık/kapalı durumu Site Ayarları › Sosyal Mecralar'dan yönetilir.</p>
</main>
</div>
'''


def uret():
    t = SAYFA.read_text(encoding="utf-8")
    bas = t[:t.index('<main class="pnl-main" id="icerik">')]
    son = t[t.index('<script src="../../cekirdek/js/kabuk.js'):]
    sablonlar = [yeni_sablon()] + [yeni_sablon(pl) for pl in PLATFORM]
    for h in HESAPLAR:
        if not h.get("ref"): sablonlar += [gor_sablon(h), duz_sablon(h)]
    from _yazim import duzelt  # yazım kuralı: etiket, başlık, düğme ve seçenek adlarında kelime başları büyük
    SAYFA.write_text(duzelt(bas + ana() + "\n".join(sablonlar) + "\n" + son), encoding="utf-8")
    print(f"hesaplar.html · {len(HESAPLAR)} hesap, {len(PLATFORM)} platform, {len(sablonlar)} şablon")


if __name__ == "__main__":
    uret()
