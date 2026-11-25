#!/usr/bin/env python3
"""Sosyal medya kalıp alternatifleri · ayrı sunum sayfası (kalip/index.html) üreticisi — DADAHABER-13.

Panel kabuğu (yan menü, üst çubuk) yok; tam genişlik, tek başına sunum sayfası. Karar değil; Yasin Bey seçecek.
Kullanım:  python3 -I kalip/_uret.py      Ölçüm:  python3 -I kalip/_olc.py

İki seçim katmanı:
  1) İSKELET — on alternatif (A–J), her biri ayrı bir yerleşim ailesinde (bölünmüş, tipografik, paspartu, kart, çift ton,
     yan sütun, dergi kapağı, kesik geometri, zemin vurgulu başlık, tam görsel).
  2) SÜSLEME — logo, etiket, vurgu öğesi, başlık vurgusu, görsel işlemi, köşe; her alternatif kendi varsayılanından başlar.
Seçimler: kategori, mecra, düğme alanı çekirdeğin data-mo bağıyla #kpSahne'ye; süsleme ve "Bunu Seç" özeti kalip.js ile.
Çizim kalip.css'te (yalnız tema ve çekirdek değişkenleri; kategori rengi temadaki --kat-*).
Görseller panelin veri/gorsel havuzundan (serbest lisanslı yeniler LISANSLAR.md'de); başlıklar public ornek_veri.json'dan
(birebir kontrol); alıntı kartındaki kişiler ve sözler KURGUDUR.
"""
import hashlib, html, json, re
from pathlib import Path

BURA = Path(__file__).resolve().parent
KOK = BURA.parent
PUB = KOK.parent / "dadahaber-prototip"
e = lambda s: html.escape(str(s), quote=True)
ikon = lambda c: f'<i class="fa-solid {c}" aria-hidden="true"></i>'
soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
HABER = {h["baslik"]: h for h in soz["haberler"]}
AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
LISANS = {g["dosya"]: g for g in json.loads((KOK / "veri" / "panel.json").read_text(encoding="utf-8"))["medya_havuzu"].get("dis_kaynakli", {}).get("gorseller", [])}


def tarih(b):
    y, a, g = HABER[b]["tarih"].split("-")
    return f"{int(g)} {AY[int(a) - 1]} {y}"


def saat(b):
    return HABER[b].get("saat") or ""


# ------------------------------------------------------------------ içerik: kategori × slot (her kartta ayrı görsel)
# slot: (görsel, başlık, vurgulanacak kelime, bölge, odak noktası)
KAT = [
    dict(k="gundem", ad="Gündem", s=dict(
        haber_koyu=("p301.jpg", "İstanbul'da raylı sistemde gece seferleri hafta içine yayılıyor", "gece seferleri", "İstanbul", "50% 62%"),
        haber_acik=("p302.jpg", "Marmara'da kar yağışı: İstanbul sabah saatlerinde", "kar yağışı", "İstanbul", "50% 55%"),
        sd=("p303.jpg", "TBMM'de 2027 bütçesi görüşmeleri: gelişmeler dakika dakika", "2027 bütçesi", "Türkiye", "50% 55%"),
        kapak=("p304.jpg", "81 ilde toplu taşıma ücretlerinin karşılaştırması", "toplu taşıma", "Türkiye", "40% 50%"),
        hikaye=("p305.jpg", "Kış hazırlığı: 24 ilde karla mücadele ekipleri göreve hazır", "24 ilde", "Türkiye", "50% 55%"),
        reels=("p306.jpg", "İstanbul'da Kirazlı–Halkalı metrosu açılıyor", "Kirazlı–Halkalı", "İstanbul", "45% 50%")),
         ic=["Narlıdere metrosunda yolcu sayısı 10 milyonu geçti", "Ankara'da yeni metro hattı için ihale süreci başladı", "Tramvay hattının yeni durağı hizmete girdi"],
         soz=("Gece seferleri, vardiyayla çalışanlar için şehri yeniden ulaşılabilir kılıyor.", "Doç. Dr. Selim Kaya", "Ulaşım planlamacısı"),
         veri=("İstanbul barajlarında doluluk oranı yüzde 38'e geriledi", "%38", "İstanbul barajlarında doluluk oranı"),
         sdm="İstanbul Valiliği: okullar 24 Kasım'da da tatil"),
    dict(k="spor", ad="Spor", s=dict(
        haber_koyu=("p311.jpg", "Süper Lig'de 14. hafta: derbi öncesi son durum", "derbi öncesi", "Türkiye", "50% 55%"),
        haber_acik=("p312.jpg", "Cumhurbaşkanlığı Türkiye Bisiklet Turu'nun 2027 rotası açıklandı", "2027 rotası", "Türkiye", "55% 40%"),
        sd=("p313.jpg", "Derbide 67. dakika: Galatasaray 2, Fenerbahçe 1", "Galatasaray 2", "İstanbul", "50% 50%"),
        kapak=("p314.jpg", "Stadyumda zemin yenileme çalışması tamamlandı", "zemin yenileme", "Türkiye", "50% 60%"),
        hikaye=("p315.jpg", "Basketbol Süper Ligi'nde 9. hafta Efes–Fenerbahçe maçıyla kapanıyor", "Efes–Fenerbahçe", "İstanbul", "45% 45%"),
        reels=("p316.jpg", "Süper Lig'de derbi heyecanı: Galatasaray 2-1 önde", "2-1 önde", "İstanbul", "50% 50%")),
         ic=["Kulüpten stadyum ulaşımına ilişkin duyuru", "Derbi için stadyum çevresinde trafik düzenlemesi", "Beşiktaş'ta yeni stadyum yönetimi göreve başladı"],
         soz=("Bu sezon gençlere güveniyoruz; sonuç tabloya yansımaya başladı.", "Murat Erdem", "Teknik direktör"),
         veri=("Antalya Yarı Maratonu'na 9 bin koşucu katıldı", "9 bin", "Antalya Yarı Maratonu'na katılan koşucu"),
         sdm="Derbide 67. dakika: Galatasaray 2, Fenerbahçe 1"),
    dict(k="kadin", ad="Kadın", s=dict(
        haber_koyu=("p180.jpg", "Kadın girişimcilere yönelik faizsiz kredi başvuruları başladı", "faizsiz kredi", "Türkiye", "38% 50%"),
        haber_acik=("p321.jpg", "Mühendislik fakültelerinde kadın öğrenci oranı yüzde 29'a çıktı", "yüzde 29", "Türkiye", "35% 50%"),
        sd=("p323.jpg", "Bilim alanında kız öğrencilere yönelik mentorluk programı genişliyor", "mentorluk programı", "Türkiye", "50% 50%"),
        kapak=("p324.jpg", "El dokumasını yaşatan atölyeler yeni koleksiyon hazırladı", "El dokumasını", "Türkiye", "45% 50%"),
        hikaye=("p192.jpg", "Hizmet sektöründe uzaktan çalışan kadınların payı artıyor", "uzaktan çalışan", "Türkiye", "55% 50%"),
        reels=("p322.jpg", "Kırsalda kadın çiftçilere yönelik eğitim programı 20 ile yayıldı", "20 ile", "Türkiye", "50% 60%")),
         ic=["Kız çocuklarının okullaşma oranında bölgesel farklar raporlandı", "Genç mühendis, geliştirdiği sulama sensörüyle tarım ödülü aldı", "Trabzon'da kadın balıkçıların kurduğu kooperatif ilk sezonunu tamamladı"],
         soz=("Kooperatife katılan her kadın, köyde bir işyeri daha açmış oluyor.", "Ayşe Demirtaş", "Kooperatif başkanı"),
         veri=("TÜİK verilerine göre kadınların işgücüne katılım oranı yüzde 36'ya yükseldi", "%36", "Kadınların işgücüne katılım oranı (TÜİK)"),
         sdm="Teknoloji şirketlerinde kadın yönetici oranı yüzde 24 oldu"),
    dict(k="finans", ad="Finans", s=dict(
        haber_koyu=("p331.jpg", "Dış ticaret verisi öncesi ihracatçıların beklentisi", "ihracatçıların", "Türkiye", "50% 50%"),
        haber_acik=("p133.jpg", "Otomobil satışları ocak-ekim döneminde yüzde 6 arttı", "yüzde 6", "Türkiye", "62% 60%"),
        sd=("p332.jpg", "Borsa İstanbul öğle saatlerinde yüzde 0,4 ekside", "yüzde 0,4", "İstanbul", "60% 50%"),
        kapak=("p333.jpg", "Kredi kartı borcunu yapılandırmadan önce bilinmesi gerekenler", "bilinmesi gerekenler", "Türkiye", "35% 50%"),
        hikaye=("p334.jpg", "Küresel konteyner taşıma ücretleri kasımda yatay seyretti", "yatay seyretti", "Dünya", "50% 55%"),
        reels=("p182.jpg", "Rüzgâr kurulu gücü 14 bin megavatı aştı", "14 bin megavatı", "Türkiye", "40% 50%")),
         ic=["BDDK kredi kartı taksit sınırlarında yeni düzenleme yaptı", "Kredi kartı azami faiz oranları aralıkta güncellenecek", "Konut kredisi faizlerinde bankalar arası fark açıldı"],
         soz=("Faiz indirimi için ilk adım, hizmet enflasyonundaki katılığın kırılması.", "Doç. Dr. Elif Arslan", "Ekonomist"),
         veri=("Merkez Bankası politika faizini yüzde 42,5'te sabit tuttu", "%42,5", "Merkez Bankası politika faizi, sabit"),
         sdm="Borsa İstanbul öğle saatlerinde yüzde 0,4 ekside"),
    dict(k="savunma", ad="Savunma", s=dict(
        haber_koyu=("p343.jpg", "Amfibi hücum gemisinde insansız hava aracı kullanımı için hazırlık sürüyor", "insansız hava aracı", "Türkiye", "50% 50%"),
        haber_acik=("p342.jpg", "Ege'de çok uluslu deniz tatbikatı başladı", "deniz tatbikatı", "Ege", "50% 50%"),
        sd=("p341.jpg", "Savaş uçağı filosunda yapısal ömür uzatma çalışması sürüyor", "yapısal ömür", "Türkiye", "55% 50%"),
        kapak=("p344.jpg", "Lojistik destek gemisi Deniz Kuvvetleri'ne teslim edildi", "Lojistik destek gemisi", "Türkiye", "50% 55%"),
        hikaye=("p345.jpg", "Altay tankının ilk teslimat partisi için kabul testleri sürüyor", "kabul testleri", "Türkiye", "50% 55%"),
        reels=("p346.jpg", "NATO tatbikatına Türk Deniz Kuvvetleri de katılıyor", "NATO tatbikatına", "Türkiye", "60% 50%")),
         ic=["Millî fırkateyn projesinin üçüncü gemisi denize indirildi", "Sahil güvenlik botlarının ikinci partisi teslim edildi", "Ege'de sahil güvenlik devriyelerinin sayısı artırıldı"],
         soz=("İnsansız sistemlerde asıl fark, sahadaki doktrinin ne kadar hızlı güncellendiği.", "Prof. Dr. Kerem Aydın", "Güvenlik uzmanı"),
         veri=("SSB verilerine göre savunma ve havacılık ihracatı ekimde yüzde 18 arttı", "%18", "Savunma ve havacılık ihracatı artışı, ekim (SSB)"),
         sdm="Amfibi hücum gemisinde insansız hava aracı kullanımı için hazırlık sürüyor"),
]
KATD = {c["k"]: c for c in KAT}
for _c in KAT:
    for _s, (_g, _b, _v, _r, _o) in _c["s"].items():
        assert _b in HABER and _v in _b, (_c["k"], _s, _b)
        assert (KOK / "veri" / "gorsel" / _g).exists(), f"görsel yok: {_g}"
    for _b in _c["ic"] + [_c["veri"][0], _c["sdm"]]:
        assert _b in HABER, _b
    _goruldu = [x[0] for x in _c["s"].values()]
    assert len(set(_goruldu)) == len(_goruldu), f"{_c['k']}: aynı görsel birden fazla kartta"

# akış (3×3): örneklerdeki kategorilerle çakışmayan görseller (Dünya, Kampüs) + görselsiz kartlar
AKIS_HABER = {
    "dunya1": dict(kat="dunya", ad="Dünya", g="p351.jpg", b="Avrupa Parlamentosu yapay zekâ denetim takvimini netleştirdi", v="yapay zekâ", r="Avrupa", o="50% 55%"),
    "kampus": dict(kat="kampus", ad="Kampüs", g="p193.jpg", b="Üniversitelerde yabancı öğrenci sayısı 330 bini geçti", v="330 bini", r="Türkiye", o="50% 60%"),
    "dunya2": dict(kat="dunya", ad="Dünya", g="p352.jpg", b="BM Genel Kurulu insani yardım fonu için ek bütçeyi onayladı", v="ek bütçeyi", r="Dünya", o="50% 50%"),
}
for _a in AKIS_HABER.values():
    assert _a["b"] in HABER and _a["v"] in _a["b"] and (KOK / "veri" / "gorsel" / _a["g"]).exists(), _a
AKIS = [("haber", "dunya1"), ("alinti", "spor"), ("haber", "kampus"),
        ("veri", "finans"), ("sdm", "gundem"), ("haber", "dunya2"),
        ("alinti", "savunma"), ("veri", "kadin"), ("sdm", "spor")]

# ------------------------------------------------------------------ alternatifler (iskelet)
# id, harf, ad, aile, tek cümle fikir, fikirlerin kaynağı, varsayılan süsleme, metnin oturduğu zemin (koyu | acik | kat)
ALT = [
    ("a", "A", "Vitrin", "Tam görsel + alttan geçiş",
     "Fotoğraf bütün kareyi kaplar; alttan yumuşak geçişin üstünde büyük başlık, logo sol üstte.",
     "Başlığın görselin üstünde güçlü durması GDH Dijital'den; sade “logo + renk + başlık” Fokus+ Afrika'dan.",
     dict(logo="plaka", etiket="nokta", oge="kalin", bvurgu="renkli", islem="gecis", kose="keskin"), "koyu"),
    ("b", "B", "Blok", "Bölünmüş",
     "Kare ikiye bölünür: üstte fotoğraf, altta kategori renginde düz blok ve başlık.",
     "Tek kalıp, tek renk düşüncesi BPT Sinema ve BPT Finans'tan; başlığın görselden ayrılması temiz okunurluk için.",
     dict(logo="duz", etiket="duz", oge="ince", bvurgu="yok", islem="dogal", kose="keskin"), "kat"),
    ("c", "C", "Manşet", "Tipografik",
     "Kategori renginde düz zemin ve dev başlık; fotoğraf yalnız zeminde silik bir doku.",
     "Başlığın her şeyden önce gelmesi GDH Dijital'den; renk disiplini BPT'nin tek renk kalıbından.",
     dict(logo="duz", etiket="cerceve", oge="nokta", bvurgu="zeminli", islem="ton", kose="keskin"), "kat"),
    ("d", "D", "Paspartu", "Çerçeve / paspartu",
     "Fotoğraf beyaz paspartunun içinde küçülür; başlık altta beyaz alanda, etiket fotoğrafın kenarına oturur.",
     "Temiz yerleşim ve boşluk Fokus+ Afrika'dan; etiketin fotoğrafa bağlanması BPT Haber'in etiket fikrinden.",
     dict(logo="duz", etiket="dolu", oge="yok", bvurgu="renkli", islem="dogal", kose="yuvarlak"), "acik"),
    ("e", "E", "Kart", "Kart içinde kart",
     "Fotoğrafın üstünde yüzen beyaz kart; başlık ve künye kartın içinde, kartın üstünde renk çizgisi.",
     "Başlığın her görselde okunması için beyaz kart fikri; kategori etiketi BPT Haber'den.",
     dict(logo="plaka", etiket="dolu", oge="kalin", bvurgu="renkli", islem="dogal", kose="yuvarlak"), "acik"),
    ("f", "F", "Ton", "Çift ton",
     "Fotoğrafın tamamı kategori renginde tek tona döner; her şey ortada, simetrik.",
     "Renk tonlu görsel Fokus+ Afrika'dan; tek renk kimlik BPT Sinema ve BPT Finans'tan.",
     dict(logo="rozet", etiket="cerceve", oge="nokta", bvurgu="alti", islem="ton", kose="keskin"), "koyu"),
    ("g", "G", "Sütun", "Yan sütun",
     "Solda kategori renginde dikey sütun; etiket sütunda dik yazılır, logo sütunun dibinde.",
     "BPT Haber'in dikey etiket şeridi bütün yüksekliğe ve kategori rengine taşındı; başlık ağırlığı GDH Dijital'den.",
     dict(logo="duz", etiket="dikey", oge="ince", bvurgu="renkli", islem="gecis", kose="keskin"), "koyu"),
    ("h", "H", "Künye", "Dergi kapağı",
     "Üstte büyük marka satırı ve tarih, ortada fotoğraf, altta başlık ve künye: dergi kapağı gibi.",
     "Basılı dergi kapağı düzeni; sadelik Fokus+ Afrika'dan, kategori · bölge künyesi BPT Haber'den.",
     dict(logo="duz", etiket="duz", oge="ince", bvurgu="yok", islem="dogal", kose="keskin"), "acik"),
    ("i", "I", "Kesik", "Kesik geometri",
     "Fotoğrafın altını çapraz kesen kategori rengi; başlık kesiğin içinde, köşede ince işaret.",
     "GDH Dijital'in başlık üstü renk çizgisi çapraz bir yüzeye büyütüldü; renk disiplini BPT'den.",
     dict(logo="duz", etiket="duz", oge="kose", bvurgu="zeminli", islem="dogal", kose="keskin"), "kat"),
    ("j", "J", "Şerit", "Zemin vurgulu başlık",
     "Başlığın her satırı ayrı renkli kutuda; fotoğraf siyah-beyaz, renk yalnız başlıkta.",
     "GDH Dijital'in zeminli başlık vurgusu bütün satırlara yayıldı; siyah-beyaz fotoğraf + renk Fokus+ Afrika'nın renk disiplininden.",
     dict(logo="plaka", etiket="nokta", oge="yok", bvurgu="yok", islem="sb", kose="keskin"), "koyu"),
]
SUSLEME = [
    ("logo", "Logo", [("duz", "Düz"), ("plaka", "Plaka"), ("rozet", "Rozet"), ("renk", "Renkli")]),
    ("etiket", "Etiket", [("duz", "Düz Yazı"), ("dolu", "Dolu Kutu"), ("cerceve", "Çerçeveli Kutu"), ("nokta", "Nokta ve Yazı"), ("dikey", "Dikey Yazı")]),
    ("oge", "Vurgu Öğesi", [("ince", "İnce Çizgi"), ("kalin", "Kalın Kısa Çizgi"), ("kose", "Köşe İşareti"), ("nokta", "Nokta Dizisi"), ("yok", "Yok")]),
    ("bvurgu", "Başlık Vurgusu", [("yok", "Yok"), ("renkli", "Kelime Renkli"), ("zeminli", "Kelime Zeminli"), ("alti", "Altı Çizgili")]),
    ("islem", "Görsel İşlemi", [("dogal", "Doğal"), ("gecis", "Alttan Geçiş"), ("ton", "Kategori Tonu"), ("sb", "Siyah-Beyaz")]),
    ("kose", "Köşe", [("keskin", "Keskin"), ("yuvarlak", "Yuvarlak")]),
]


# ------------------------------------------------------------------ parçalar
def vurgulu(b, v):
    i = b.find(v)
    return f'{e(b[:i])}<em class="kp-vurgu">{e(v)}</em>{e(b[i + len(v):])}'


def uzunluk(b):
    return " kp-uzun" if len(b) > 70 else " kp-orta" if len(b) > 56 else ""


def K(fn, kat=None):
    """kategori metni: kat verilirse tek; verilmezse beşi birden, seçili olmayanı kalip.css gizler"""
    if kat:
        return fn(KATD[kat])
    return "".join(f'<span data-k="{c["k"]}">{fn(c)}</span>' for c in KAT)


LOGO = ('<span class="kp-logo"><span class="kb-logo kp-l-sari"></span><span class="kb-logo kb-logo-acik kp-l-koyu"></span>'
        '<span class="kp-l-maske"></span></span>')
GORSELLI = ("haber", "sd", "kapak", "hikaye", "reels")
SLOT = {"haber": None, "sd": "sd", "kapak": "kapak", "hikaye": "hikaye", "reels": "reels"}


def tuval(alt, yz, tip, zemin="koyu", kat=None, akis=None):
    """Bir sosyal görsel. alt: iskelet · tip: haber sd kapak ic hikaye reels alinti veri sdm · zemin: haber için koyu/açık
    kat: akışta sabit kategori (metin kartları) · akis: akışta sabit haber (AKIS_HABER anahtarı)"""
    slot = (f"haber_{zemin}" if tip == "haber" else SLOT.get(tip)) if tip in GORSELLI else None
    stil, sinif = "", ""
    if akis:  # akışta sabit haber (kendi kategorisi ve görseli)
        a = AKIS_HABER[akis]
        stil = f' style="--kat:var(--kat-{a["kat"]});--g:url(../veri/gorsel/{a["g"]});--o:{a["o"]}"'
        sinif = " kp-sabit"
        etk = f'<b>{e(a["ad"])}</b><span class="kp-bolge">{e(a["r"])}</span>'
        bas = f'<span class="kp-baslik{uzunluk(a["b"])}"><span class="kp-bi">{vurgulu(a["b"], a["v"])}</span></span>'
        meta = e(tarih(a["b"]))
    else:
        if kat:
            stil, sinif = f' style="--kat:var(--kat-{kat})"', " kp-sabit"
        elif slot:  # beş kategorinin görseli ve odak noktası; seçili olanı kalip.css uygular
            stil = ' style="' + ";".join(f'--g-{c["k"]}:url(../veri/gorsel/{c["s"][slot][0]});--o-{c["k"]}:{c["s"][slot][4]}' for c in KAT) + '"'
        if slot:
            etk = K(lambda c: f'<b>{e(c["ad"])}</b><span class="kp-bolge">{e(c["s"][slot][3])}</span>', kat)
            bas = K(lambda c: f'<span class="kp-baslik{uzunluk(c["s"][slot][1])}"><span class="kp-bi">{vurgulu(c["s"][slot][1], c["s"][slot][2])}</span></span>', kat)
            meta = K(lambda c: e(tarih(c["s"][slot][1])), kat)
        else:
            etk = K(lambda c: f'<b>{e(c["ad"])}</b><span class="kp-bolge">{"Türkiye"}</span>', kat)
    etiket = f'<span class="kp-etiket"><span class="kp-nokta"></span>{etk}</span>'
    glif, govde = "", ""
    if tip in GORSELLI:
        govde = f'{etiket}{bas}<span class="kp-meta">{meta}</span>'
        if tip == "sd":
            govde = f'<span class="kp-sdbas"><i></i>Son Dakika<span class="kp-saat">{K(lambda c: e(saat(c["s"]["sd"][1])), kat)}</span></span>' + govde
        if tip == "kapak":
            govde = '<span class="kp-ust-not">Kaydırmalı dosya</span>' + govde
        if tip == "reels":
            govde = f'<span class="kp-oynat">{ikon("fa-play")}<span>0.48</span></span>' + govde
        if tip == "hikaye":
            govde += f'<span class="kp-baglanti">{ikon("fa-link")}Haberi oku</span>'
    elif tip == "ic":
        liste = K(lambda c: "".join(f'<li><span class="kp-no">0{i + 1}</span><span>{e(x)}</span></li>' for i, x in enumerate(c["ic"])), kat)
        govde = f'{etiket}<span class="kp-ic-bas">Öne çıkanlar</span><ol class="kp-liste">{liste}</ol>'
        glif = '<span class="kp-glif kp-glif-sira">2/4</span>'
    elif tip == "alinti":
        govde = (f'{etiket}<span class="kp-baslik kp-soz"><span class="kp-bi">{K(lambda c: "“" + e(c["soz"][0]) + "”", kat)}</span></span>'
                 f'<span class="kp-kim">{K(lambda c: "<b>" + e(c["soz"][1]) + "</b><span>" + e(c["soz"][2]) + "</span>", kat)}</span>')
        glif = f'<span class="kp-glif kp-glif-tirnak">{ikon("fa-quote-left")}</span>'
    elif tip == "veri":
        govde = (f'{etiket}<span class="kp-aciklama">{K(lambda c: e(c["veri"][2]), kat)}</span>'
                 f'<span class="kp-meta">{K(lambda c: e(tarih(c["veri"][0])), kat)}</span>')
        glif = f'<span class="kp-glif kp-glif-sayi">{K(lambda c: e(c["veri"][1]), kat)}</span>'
    else:  # sdm: görselsiz Son Dakika
        govde = (f'<span class="kp-sdbas"><i></i>Son Dakika<span class="kp-saat">{K(lambda c: e(saat(c["sdm"])), kat)}</span></span>{etiket}'
                 f'<span class="kp-baslik{K(lambda c: uzunluk(c["sdm"]), kat) if kat else ""}"><span class="kp-bi">{K(lambda c: e(c["sdm"]), kat)}</span></span>'
                 f'<span class="kp-meta">{K(lambda c: e(tarih(c["sdm"])), kat)}</span>')
    metin = tip not in GORSELLI
    kaydir = f'<span class="kp-kaydir">{"1" if tip == "kapak" else "2"}/4 · Kaydır{ikon("fa-arrow-right")}</span>' if tip in ("kapak", "ic") else ""
    nokta = '<span class="kp-sayfa-nokta"><i></i><i></i><i></i><i></i></span>' if tip in ("kapak", "ic") else ""
    ust = f'<span class="kp-masthead">{K(lambda c: e(tarih(c["s"][slot][1])) if slot else "25 Kasım 2026", kat) if not akis else e(tarih(AKIS_HABER[akis]["b"]))}<b>Sayı 327</b></span>' if alt == "h" else ""
    guvenli = '<span class="kp-guvenli"></span>' if tip in ("hikaye", "reels") else ""
    return (f'<div class="kp-tuval kp-{alt}{" kp-metin" if metin else ""}{sinif}" data-tip="{tip}" data-zemin="{zemin}" data-yz="{yz}"{stil} role="img" aria-label="{e(alt.upper())} · {tip}">'
            f'<span class="kp-gorsel">{glif}</span><span class="kp-karart"></span><span class="kp-sekil"></span><span class="kp-kose"></span>{ust}{LOGO}{kaydir}{nokta}'
            f'<span class="kp-etiket-dikey">{etk}</span>'
            f'<span class="kp-blok"><span class="kp-oge"><i></i><i></i><i></i></span>{govde}{glif.replace("kp-glif ", "kp-glif kp-glif-b ")}</span>{guvenli}</div>')


ORNEK = [("haber", "koyu", "Haber gönderisi · koyu görsel (seçili mecra ölçüsünde)"),
         ("haber", "acik", "Haber gönderisi · açık görsel (seçili mecra ölçüsünde)"),
         ("sd", "koyu", "Son Dakika"),
         ("kapak", "koyu", "Kaydırmalı gönderi · kapak"),
         ("ic", "koyu", "Kaydırmalı gönderi · iç sayfa"),
         ("alinti", "koyu", "Alıntı kartı · kişi ve söz kurgudur"),
         ("veri", "koyu", "Veri kartı"),
         ("hikaye", "koyu", "Hikâye · dikey"),
         ("reels", "koyu", "Reels ve Shorts kapağı · dikey")]


def sekil(alt, yz, tip, zemin, yazi):
    return f'<figure class="frow">{tuval(alt, yz, tip, zemin)}<figcaption class="fhint">{yazi}</figcaption></figure>'


def orn_nit(o):
    return " ".join(f'data-o-{k}="{v}" data-v-{k}="{v}"' for k, v in o.items())


def alternatif_paneli(i, a):
    alt, harf, ad, aile, fikir, kaynak, orn, yz = a
    ornek = "".join(sekil(alt, yz, t, z, y) for t, z, y in ORNEK)
    akis = "".join(tuval(alt, yz, t, "koyu", kat=(None if t == "haber" else k), akis=(k if t == "haber" else None)) for t, k in AKIS)
    return f"""    <div class="sa-form-panel kp-orn" id="kpP{harf}" role="tabpanel" data-alt="{alt}" data-ad="{harf} · {ad}" {orn_nit(orn)}{"" if i == 0 else " hidden"}>
      <div class="form-sec"><div class="form-sec-tt">{harf} · {ad}<span class="fs-ek">{aile}</span></div><div class="form-grid">
        <div class="frow"><span class="fhint"><b>Fikir:</b> {fikir}</span><span class="fhint"><b>Fikirlerin kaynağı:</b> {kaynak}</span></div>
        <div class="kb-saglik-izgara">{ornek}</div>
      </div></div>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-table-cells")}Akışta Nasıl Durur</div><div class="form-grid">
        <span class="fhint">Bu kalıpla yapılmış dokuz gönderi profil ızgarasında: Dünya, Kampüs, Spor, Finans, Gündem, Savunma, Kadın; haber, Son Dakika, alıntı ve veri karışık</span>
        <div class="kp-akis" aria-label="{harf} alternatifi profil akışı">{akis}</div>
      </div></div>
      <div class="form-sec"><div class="form-sec-tt">{ikon("fa-pen")}Görüşünüz</div><div class="form-grid kb-iki-sutun">
        <div class="toggle-row"><span>Bunu Seç<small>Seçilenler sayfanın üstündeki özette süslemeleriyle birlikte görünür; birden fazla seçilebilir</small></span><label class="toggle"><input type="checkbox" class="kp-sec" data-alt="{alt}" aria-label="{harf} alternatifini seç"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
        <div class="frow"><label for="kpNot{harf}">Notunuz</label><textarea class="ftext" id="kpNot{harf}" rows="3" placeholder="ör. sütun iyi, başlık biraz daha büyük olsun"></textarea><span class="fhint">Beğendiğiniz ya da değişmesini istediğiniz parça; bu sayfada kalır, kaydedilmez</span></div>
      </div></div>
    </div>
"""


def hepsi_paneli():
    kart = "".join(f"""      <article class="kb-entegre kp-orn" data-alt="{alt}" {orn_nit(orn)}>
        <div class="kb-entegre-bas"><span class="kb-entegre-ikon">{harf}</span><div><b>{harf} · {ad}</b><small>{aile}</small></div></div>
        <div class="pc-body"><div class="form-grid">{sekil(alt, yz, "haber", "koyu", "Haber gönderisi · koyu görsel")}{sekil(alt, yz, "haber", "acik", "Haber gönderisi · açık görsel")}</div></div>
      </article>
""" for alt, harf, ad, aile, fikir, kaynak, orn, yz in ALT)
    return f"""    <div class="sa-form-panel" id="kpPHepsi" role="tabpanel" hidden>
      <div class="pc-body"><div class="kb-entegre-izgara">
{kart}      </div></div>
    </div>
"""


OLCU = [
    ("Instagram Gönderi", "4:5 · 1080×1350", "Kalıpta yok (akışta tam görünür)", "wait", "Doğrulanacak", "Panel kaydındaki sosyal oran"),
    ("Instagram ve Facebook Hikâye", "9:16 · 1080×1920", "Üst %14 (250 px), alt %14–20 (250–340 px)", "ok", "Doğrulandı", "Meta Business Help · Stories reklam tasarım özellikleri"),
    ("Instagram ve Facebook Reels", "9:16 · 1080×1920", "Üst %14, alt %35, yanlar %6", "wait", "Doğrulanacak", "Üçüncü taraf aktarımı; Meta indirilebilir şablona yönlendiriyor"),
    ("YouTube Shorts", "9:16 · 1080×1920", "Resmî piksel ölçüsü yok; editör kılavuzu gösteriyor", "wait", "Doğrulanacak", "YouTube Help · Enhance your Shorts"),
    ("TikTok", "9:16 · 1080×1920", "Resmî dosya indirilebilir; sayı sayfada yok", "wait", "Doğrulanacak", "TikTok Ads Help · In-Feed reklam özellikleri"),
    ("Kalıplarda kullanılan ortak alan", "9:16", "Üst %14, alt %35, sol %6, sağ %15", "wait", "Doğrulanacak", "Sağ %15: Shorts ve TikTok düğmeleri için varsayım"),
    ("LinkedIn", "1.91:1 · 1200×627", "Kalıpta yok", "wait", "Doğrulanacak", "Panel kaydındaki sosyal oran"),
    ("Facebook", "1.91:1 · 1200×630", "Kalıpta yok", "wait", "Doğrulanacak", "Panel kaydındaki sosyal oran"),
    ("X", "16:9 · 1200×675", "Kalıpta yok", "wait", "Doğrulanacak", "Panel kaydındaki sosyal oran"),
]
KAYNAK = [("Meta · Design specifications for Stories ads", "https://www.facebook.com/business/help/188477725155524"),
          ("Meta · About text overlays and the Safe Zone for ads in Stories and Reels", "https://www.facebook.com/business/help/980593475366490/"),
          ("YouTube Help · Enhance your Shorts", "https://support.google.com/youtube/answer/16215842"),
          ("TikTok Ads Help · Auction In-Feed Ads", "https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads")]


def kaynaklar_karti():
    olcu = "".join(f'<div class="kb-ozk-satir"><span class="kb-ozk-ikon">{ikon("fa-mobile-screen" if "9:16" in o else "fa-image")}</span>'
                   f'<div class="kb-ozk-yazi"><b>{e(m)}</b><span>{e(o)} · {e(g)}</span><span class="kb-ozk-meta">{e(k)}</span></div>'
                   f'<span class="pstat {s}">{d}</span></div>' for m, o, g, s, d, k in OLCU)
    kay = "".join(f'<a class="kb-bag" href="{u}" target="_blank" rel="noopener">{e(a)}</a>' for a, u in KAYNAK)
    gorsel = "".join(f'<div class="kb-ozk-satir"><span class="kb-ozk-ikon">{ikon("fa-image")}</span><div class="kb-ozk-yazi"><b>{e(d)} · {e(v["konu"])}</b>'
                     f'<span>{e(v["yazar"])} · {e(v["lisans"])}</span><span class="kb-ozk-meta"><a class="kb-bag" href="{e(v["sayfa"])}" target="_blank" rel="noopener">Wikimedia Commons sayfası</a></span></div></div>'
                     for d, v in sorted(LISANS.items()))
    return f"""  <section class="pnl-card dash-row" aria-labelledby="kpOlcuBas">
    <div class="pc-head"><h2 class="pc-title" id="kpOlcuBas">{ikon("fa-ruler-combined")}Ölçüler ve Kaynaklar</h2></div>
    <div class="pc-body"><div class="form-grid kb-iki-sutun">
      <div class="frow"><span class="flabel">Düğmelerin Kapattığı Alan ve Ölçüler</span>
        <div class="kb-bant uyari">{ikon("fa-triangle-exclamation")}<span><b>Resmî sayfalar çoğunlukla sayı vermiyor;</b> indirilebilir şablona yönlendiriyor. “Doğrulanacak” satırlar kalıp seçildikten sonra platformun kendi şablonuyla karşılaştırılır.</span></div>
        <div class="kb-ozk">{olcu}</div><div class="frow">{kay}</div></div>
      <div class="frow"><span class="flabel">Görsel Kaynakları</span><span class="fhint">Yeni görseller serbest lisanslı (Wikimedia Commons); CC BY ve CC BY-SA görsellerde atıf zorunlu. Tam liste: veri/gorsel/LISANSLAR.md. Diğer görseller havuzun mevcut örnekleri.</span>
        <div class="kb-ozk">{gorsel}</div></div>
    </div></div>
  </section>
"""


def v(yol):
    return hashlib.sha1((KOK / yol).read_bytes()).hexdigest()[:8] if (KOK / yol).exists() else "0"


def sayfa():
    ozet = (f'<div class="kb-bant bilgi dash-row" id="kpOzet">{ikon("fa-circle-check")}<span><b>Seçilen:</b> '
            f'<span class="kp-ozet-metin">henüz seçilmedi; her alternatifin altındaki “Bunu Seç” ile işaretleyin.</span></span></div>')
    kat_ops = "".join(f'<label class="kb-secenek"><input type="radio" name="kpKat" value="{c["k"]}" data-mo="kat" data-mo-hedef="#kpSahne"{" checked" if c["k"] == "gundem" else ""}>{e(c["ad"])}</label>' for c in KAT)
    mecra_ops = "".join(f'<label class="kb-secenek"><input type="radio" name="kpMecra" value="{v_}" data-mo="mecra" data-mo-hedef="#kpSahne"{" checked" if v_ == "ig" else ""}>{a}</label>'
                        for v_, a in [("ig", "Instagram"), ("linkedin", "LinkedIn"), ("facebook", "Facebook"), ("x", "X")])
    gorunum = f"""  <section class="pnl-card dash-row" aria-labelledby="kpGorunum">
    <div class="pc-head"><h2 class="pc-title" id="kpGorunum">{ikon("fa-sliders")}Görünüm</h2></div>
    <div class="pc-body"><div class="form-grid kb-iki-sutun">
      <div class="frow"><span class="flabel">Kategori Rengi</span><div class="kb-secenek-grup" role="radiogroup" aria-label="Kategori rengi">{kat_ops}</div><span class="fhint">Renk Haberler › Kategoriler'deki kayıttan; görseller ve başlıklar da o kategorinin örneklerine döner</span></div>
      <div class="frow"><span class="flabel">Mecra</span><div class="kb-secenek-grup" role="radiogroup" aria-label="Mecra">{mecra_ops}</div><span class="fhint">Haber gönderisi bu mecranın ölçüsüne göre yeniden dizilir: Instagram 4:5 · LinkedIn ve Facebook 1.91:1 · X 16:9</span></div>
      <div class="toggle-row"><span>Düğmelerin Kapattığı Alanı Göster<small>Hikâye ve Reels'te uygulamanın kendi düğmeleri ekranın üstünü, altını ve sağını kapatır; logo ve başlık bu alanın içinde kalır (ölçüler doğrulanacak)</small></span><label class="toggle"><input type="checkbox" data-mo="guvenli" data-mo-hedef="#kpSahne" aria-label="Düğmelerin kapattığı alanı göster"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
    </div></div>
  </section>
"""
    gruplar = "".join(f'<div class="frow"><span class="flabel">{ad}</span><div class="kb-secenek-grup" role="radiogroup" aria-label="{ad}">'
                      + "".join(f'<label class="kb-secenek"><input type="radio" name="kpO-{k}" value="{v_}" data-orn="{k}">{a}</label>' for v_, a in ops)
                      + '</div></div>' for k, ad, ops in SUSLEME)
    susleme = f"""  <section class="pnl-card dash-row" id="kpSusleme" aria-labelledby="kpSusBas">
    <div class="pc-head"><h2 class="pc-title" id="kpSusBas">{ikon("fa-wand-magic-sparkles")}Süsleme<span class="kp-sus-ad">A · Vitrin</span></h2><button type="button" class="btn btn-ghost btn-sm" data-kp-varsayilan>{ikon("fa-rotate-left")}Varsayılana Dön</button></div>
    <div class="pc-body"><span class="fhint kp-sus-not">Seçili alternatifin iskeleti aynı kalır; logo, etiket, vurgu, görsel işlemi ve köşe değişir. Her alternatif kendi varsayılanından başlar.</span><div class="form-grid kp-sus-izgara">{gruplar}</div></div>
  </section>
"""
    sekmeler = "".join(f'<button type="button" class="sa-form-tab{" is-on" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-panel="kpP{a[1]}">{a[1]} · {a[2]}</button>'
                       for i, a in enumerate(ALT))
    sekmeler += f'<button type="button" class="sa-form-tab" role="tab" aria-selected="false" data-panel="kpPHepsi">{ikon("fa-table-columns")}Hepsini Yan Yana Gör</button>'
    css = ["../assets/vendor/fontawesome-6.5.2/css/all.min.css", "../tema/dadahaber.css", "../cekirdek/css/kabuk.css", "../cekirdek/css/bilesen.css"]
    js = ["../cekirdek/js/bilesen.js", "../cekirdek/js/form.js", "../cekirdek/js/alan.js"]
    bag = "\n".join(f'<link rel="stylesheet" href="{c}?v={v(c[3:])}"{" data-tema" if "tema" in c else ""}>' for c in css)
    bag += f'\n<link rel="stylesheet" href="kalip.css?v={v("kalip/kalip.css")}">'
    bet = "\n".join(f'<script src="{j}?v={v(j[3:])}"></script>' for j in js) + f'\n<script src="kalip.js?v={v("kalip/kalip.js")}"></script>'
    s = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Kalıp Alternatifleri · Dada Haber</title>
{bag}
</head>
<body class="kp-sunum">
<!-- KALIP ALTERNATİFLERİ (DADAHABER-13) · ayrı sunum sayfası, panel kabuğu yok. Üretici kalip/_uret.py; çizim kalip.css; süsleme kalip.js.
     Karar değil; Yasin Bey seçecek. Alıntı kartlarındaki kişi ve sözler kurgudur. -->
<main class="kp-sayfa" id="icerik">
  <div class="kp-kunye">{ikon("fa-newspaper")}<span>Dada Haber · Sosyal Medya Kalıp Alternatifleri · Karar değil; Yasin Bey seçecek · 25.11.2026</span></div>
  <div class="pnl-page-head">
    <div>
      <h1>Kalıp Alternatifleri</h1>
      <div class="ph-sub">On iskelet, her biri ayrı bir yerleşim ailesi; üstüne süsleme seçilir · aynı haberler her kalıpta, her içerik çeşidinde ve her mecrada</div>
    </div>
  </div>
{ozet}
{gorunum}
{susleme}
  <section class="pnl-card dash-row" id="kpSahne" data-sekmeli data-kat="gundem" data-mecra="ig" aria-label="Kalıp alternatifleri">
    <div class="sa-form-tabs" role="tablist" aria-label="Alternatifler">{sekmeler}</div>
{"".join(alternatif_paneli(i, a) for i, a in enumerate(ALT))}{hepsi_paneli()}  </section>
{kaynaklar_karti()}</main>
{bet}
</body>
</html>
"""
    (BURA / "index.html").write_text(s, encoding="utf-8")
    print("yazıldı: kalip/index.html", len(s.encode()) // 1024, "KB")


if __name__ == "__main__":
    sayfa()
