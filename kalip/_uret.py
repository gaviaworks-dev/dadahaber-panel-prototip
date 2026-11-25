#!/usr/bin/env python3
"""Sosyal medya kalıp alternatifleri · ayrı sunum sayfası (kalip/index.html) üreticisi — DADAHABER-13.

Panel kabuğu yok; tek başına sunum sayfası. Karar değil; Yasin Bey seçecek.
Kullanım:  python3 -I kalip/_uret.py      Ölçüm:  python3 -I kalip/_olc.py

Sayfa düzeni: solda içerik (küçük resim şeridi → içerik sekmeleri), sağda yapışkan dikey araç çubuğu
(Görünüm: kategori rengi, mecra, güvenli alan · Süsleme: logo, etiket, vurgu öğesi, başlık vurgusu, görsel işlemi, köşe).
İki seçim katmanı:
  1) İSKELET — on dört alternatif (A–N): on yerleşim ailesi (A–J), dikey öğeli iki iskelet (K, L · t-kalip4) ve iki özgün birleşim (M, N).
  2) SÜSLEME — her alternatif kendi varsayılanından başlar; seçimler kalip.js'teki tek durum nesnesinde tutulur.
Tekli görünümde içerik sekmeleri BİR KEZ üretilir; alternatif değişince kalip.js tuvallerin iskelet sınıfını (kp-a … kp-l)
ve metin/logo zeminini (data-yz, data-lz) değiştirir. Durumlar ve Kişi Haberleri bölümleri (t-kalip2: _durum.py, _kisi.py)
iskelete göre farklı çizildiği için her iskeletin sürümü gömülür.
Çizim kalip.css'te (yalnız tema ve çekirdek değişkenleri; kategori rengi temadaki --kat-*).
Görseller veri/gorsel havuzundan (serbest lisanslılar LISANSLAR.md ve veri/panel.json → medya_havuzu.dis_kaynakli);
başlıklar public ornek_veri.json'dan (birebir kontrol); alıntı kartlarındaki kişiler ve sözler KURGUDUR.
"""
import hashlib, html, json, re, sys
from pathlib import Path

BURA = Path(__file__).resolve().parent
KOK = BURA.parent
PUB = KOK.parent / "dadahaber-prototip"
sys.path.insert(0, str(BURA))
e = lambda s: html.escape(str(s), quote=True)
ikon = lambda c: f'<i class="fa-solid {c}" aria-hidden="true"></i>'
soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
HABER = {h["baslik"]: h for h in soz["haberler"]}
AY = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def tarih(b):
    y, a, g = HABER[b]["tarih"].split("-")
    return f"{int(g)} {AY[int(a) - 1]} {y}"


def saat(b):
    return HABER[b].get("saat") or ""


# ------------------------------------------------------------------ içerik: kategori × çeşit (her kartta ayrı görsel)
def H(g, b, v, r, o="50% 50%"):
    return dict(g=g, b=b, v=v, r=r, o=o)


KAT = [
    dict(k="gundem", ad="Gündem", s=dict(
        haber_koyu=H("p301.jpg", "İstanbul'da raylı sistemde gece seferleri hafta içine yayılıyor", "gece seferleri", "İstanbul", "50% 62%"),
        haber_acik=H("p302.jpg", "Marmara'da kar yağışı: İstanbul sabah saatlerinde", "kar yağışı", "İstanbul", "50% 55%"),
        sd=H("p303.jpg", "TBMM'de 2027 bütçesi görüşmeleri: gelişmeler dakika dakika", "2027 bütçesi", "Türkiye", "50% 55%"),
        kapak=H("p304.jpg", "81 ilde toplu taşıma ücretlerinin karşılaştırması", "toplu taşıma", "Türkiye", "40% 50%"),
        hikaye=H("p305.jpg", "Kış hazırlığı: 24 ilde karla mücadele ekipleri göreve hazır", "24 ilde", "Türkiye", "50% 55%"),
        reels=H("p306.jpg", "İstanbul'da Kirazlı–Halkalı metrosu açılıyor", "Kirazlı–Halkalı", "İstanbul", "45% 50%"),
        ic=dict(g="p361.jpg", o="45% 55%", liste=["Narlıdere metrosunda yolcu sayısı 10 milyonu geçti", "Ankara'da yeni metro hattı için ihale süreci başladı", "Tramvay hattının yeni durağı hizmete girdi"]),
        alinti=dict(g="p362.jpg", o="50% 55%", soz="Gece seferleri, vardiyayla çalışanlar için şehri yeniden ulaşılabilir kılıyor.", v="yeniden ulaşılabilir", kim="Doç. Dr. Selim Kaya", unvan="Ulaşım planlamacısı"),
        veri=dict(g="p363.jpg", o="60% 45%", b="İstanbul barajlarında doluluk oranı yüzde 38'e geriledi", sayi="%38", acik="İstanbul barajlarında doluluk oranı"))),
    dict(k="spor", ad="Spor", s=dict(
        haber_koyu=H("p311.jpg", "Süper Lig'de 14. hafta: derbi öncesi son durum", "derbi öncesi", "Türkiye", "50% 55%"),
        haber_acik=H("p312.jpg", "Cumhurbaşkanlığı Türkiye Bisiklet Turu'nun 2027 rotası açıklandı", "2027 rotası", "Türkiye", "55% 40%"),
        sd=H("p313.jpg", "Derbide 67. dakika: Galatasaray 2, Fenerbahçe 1", "Galatasaray 2", "İstanbul", "50% 50%"),
        kapak=H("p314.jpg", "Stadyumda zemin yenileme çalışması tamamlandı", "zemin yenileme", "Türkiye", "50% 60%"),
        hikaye=H("p315.jpg", "Basketbol Süper Ligi'nde 9. hafta Efes–Fenerbahçe maçıyla kapanıyor", "Efes–Fenerbahçe", "İstanbul", "45% 45%"),
        reels=H("p316.jpg", "Süper Lig'de derbi heyecanı: Galatasaray 2-1 önde", "2-1 önde", "İstanbul", "50% 50%"),
        ic=dict(g="p387.jpg", o="50% 60%", liste=["Kulüpten stadyum ulaşımına ilişkin duyuru", "Derbi için stadyum çevresinde trafik düzenlemesi", "Beşiktaş'ta yeni stadyum yönetimi göreve başladı"]),
        alinti=dict(g="p376.jpg", o="50% 50%", soz="Bu sezon gençlere güveniyoruz; sonuç tabloya yansımaya başladı.", v="gençlere güveniyoruz", kim="Murat Erdem", unvan="Teknik direktör"),
        veri=dict(g="p366.jpg", o="55% 65%", b="Antalya Yarı Maratonu'na 9 bin koşucu katıldı", sayi="9 bin", acik="Antalya Yarı Maratonu'na katılan koşucu"))),
    dict(k="kadin", ad="Kadın", s=dict(
        haber_koyu=H("p180.jpg", "Kadın girişimcilere yönelik faizsiz kredi başvuruları başladı", "faizsiz kredi", "Türkiye", "38% 50%"),
        haber_acik=H("p321.jpg", "Mühendislik fakültelerinde kadın öğrenci oranı yüzde 29'a çıktı", "yüzde 29", "Türkiye", "35% 50%"),
        sd=H("p323.jpg", "Bilim alanında kız öğrencilere yönelik mentorluk programı genişliyor", "mentorluk programı", "Türkiye", "50% 50%"),
        kapak=H("p324.jpg", "El dokumasını yaşatan atölyeler yeni koleksiyon hazırladı", "El dokumasını", "Türkiye", "45% 50%"),
        hikaye=H("p192.jpg", "Hizmet sektöründe uzaktan çalışan kadınların payı artıyor", "uzaktan çalışan", "Türkiye", "55% 50%"),
        reels=H("p322.jpg", "Kırsalda kadın çiftçilere yönelik eğitim programı 20 ile yayıldı", "20 ile", "Türkiye", "50% 60%"),
        ic=dict(g="p379.jpg", o="60% 50%", liste=["Kız çocuklarının okullaşma oranında bölgesel farklar raporlandı", "Genç mühendis, geliştirdiği sulama sensörüyle tarım ödülü aldı", "Trabzon'da kadın balıkçıların kurduğu kooperatif ilk sezonunu tamamladı"]),
        alinti=dict(g="p500.jpg", o="50% 55%", soz="Kooperatife katılan her kadın, köyde bir işyeri daha açmış oluyor.", v="bir işyeri daha", kim="Ayşe Demirtaş", unvan="Kooperatif başkanı"),
        veri=dict(g="p501.jpg", o="50% 55%", b="TÜİK verilerine göre kadınların işgücüne katılım oranı yüzde 36'ya yükseldi", sayi="%36", acik="Kadınların işgücüne katılım oranı (TÜİK)"))),
    dict(k="finans", ad="Finans", s=dict(
        haber_koyu=H("p331.jpg", "Dış ticaret verisi öncesi ihracatçıların beklentisi", "ihracatçıların", "Türkiye", "50% 50%"),
        haber_acik=H("p133.jpg", "Otomobil satışları ocak-ekim döneminde yüzde 6 arttı", "yüzde 6", "Türkiye", "62% 60%"),
        sd=H("p332.jpg", "Borsa İstanbul öğle saatlerinde yüzde 0,4 ekside", "yüzde 0,4", "İstanbul", "60% 50%"),
        kapak=H("p333.jpg", "Kredi kartı borcunu yapılandırmadan önce bilinmesi gerekenler", "bilinmesi gerekenler", "Türkiye", "35% 50%"),
        hikaye=H("p334.jpg", "Küresel konteyner taşıma ücretleri kasımda yatay seyretti", "yatay seyretti", "Dünya", "50% 55%"),
        reels=H("p182.jpg", "Rüzgâr kurulu gücü 14 bin megavatı aştı", "14 bin megavatı", "Türkiye", "40% 50%"),
        ic=dict(g="p370.jpg", o="50% 50%", liste=["BDDK kredi kartı taksit sınırlarında yeni düzenleme yaptı", "Kredi kartı azami faiz oranları aralıkta güncellenecek", "Konut kredisi faizlerinde bankalar arası fark açıldı"]),
        alinti=dict(g="p388.jpg", o="45% 55%", soz="Faiz indirimi için ilk adım, hizmet enflasyonundaki katılığın kırılması.", v="hizmet enflasyonundaki", kim="Doç. Dr. Elif Arslan", unvan="Ekonomist"),
        veri=dict(g="p503.jpg", o="45% 50%", b="Merkez Bankası politika faizini yüzde 42,5'te sabit tuttu", sayi="%42,5", acik="Merkez Bankası politika faizi, sabit"))),
    dict(k="savunma", ad="Savunma", s=dict(
        haber_koyu=H("p343.jpg", "Amfibi hücum gemisinde insansız hava aracı kullanımı için hazırlık sürüyor", "insansız hava aracı", "Türkiye", "50% 50%"),
        haber_acik=H("p342.jpg", "Ege'de çok uluslu deniz tatbikatı başladı", "deniz tatbikatı", "Ege", "50% 50%"),
        sd=H("p341.jpg", "Savaş uçağı filosunda yapısal ömür uzatma çalışması sürüyor", "yapısal ömür", "Türkiye", "55% 50%"),
        kapak=H("p344.jpg", "Lojistik destek gemisi Deniz Kuvvetleri'ne teslim edildi", "Lojistik destek gemisi", "Türkiye", "50% 55%"),
        hikaye=H("p345.jpg", "Altay tankının ilk teslimat partisi için kabul testleri sürüyor", "kabul testleri", "Türkiye", "50% 55%"),
        reels=H("p346.jpg", "NATO tatbikatına Türk Deniz Kuvvetleri de katılıyor", "NATO tatbikatına", "Türkiye", "60% 50%"),
        ic=dict(g="p373.jpg", o="55% 55%", liste=["Millî fırkateyn projesinin üçüncü gemisi denize indirildi", "Sahil güvenlik botlarının ikinci partisi teslim edildi", "Ege'de sahil güvenlik devriyelerinin sayısı artırıldı"]),
        alinti=dict(g="p374.jpg", o="40% 55%", soz="İnsansız sistemlerde asıl fark, sahadaki doktrinin ne kadar hızlı güncellendiği.", v="ne kadar hızlı", kim="Prof. Dr. Kerem Aydın", unvan="Güvenlik uzmanı"),
        veri=dict(g="p375.jpg", o="60% 45%", b="SSB verilerine göre savunma ve havacılık ihracatı ekimde yüzde 18 arttı", sayi="%18", acik="Savunma ve havacılık ihracatı artışı, ekim (SSB)"))),
]
KATD = {c["k"]: c for c in KAT}
GORSELLI = ("haber_koyu", "haber_acik", "sd", "kapak", "hikaye", "reels")

# akış (3×3): tekli görünümden FARKLI görseller; kategoriler ve çeşitler karışık
AKIS = [
    dict(tip="haber", kat="dunya", ad="Dünya", g="p351.jpg", o="50% 55%", b="Avrupa Parlamentosu yapay zekâ denetim takvimini netleştirdi", v="yapay zekâ", r="Avrupa"),
    dict(tip="alinti", kat="spor", ad="Spor", g="p392.jpg", o="50% 55%", soz=KATD["spor"]["s"]["alinti"]["soz"], v=KATD["spor"]["s"]["alinti"]["v"], kim="Murat Erdem", unvan="Teknik direktör", r="Türkiye"),
    dict(tip="haber", kat="kampus", ad="Kampüs", g="p193.jpg", o="50% 60%", b="Üniversitelerde yabancı öğrenci sayısı 330 bini geçti", v="330 bini", r="Türkiye"),
    dict(tip="veri", kat="finans", ad="Finans", g="p372.jpg", o="50% 50%", b="Merkez Bankası politika faizini yüzde 42,5'te sabit tuttu", sayi="%42,5", acik="Merkez Bankası politika faizi, sabit", r="Türkiye"),
    dict(tip="sd", kat="gundem", ad="Gündem", g="p390.jpg", o="50% 50%", b="İstanbul Valiliği: okullar 24 Kasım'da da tatil", v="24 Kasım'da", r="İstanbul"),
    dict(tip="haber", kat="dunya", ad="Dünya", g="p352.jpg", o="50% 50%", b="BM Genel Kurulu insani yardım fonu için ek bütçeyi onayladı", v="ek bütçeyi", r="Dünya"),
    dict(tip="alinti", kat="savunma", ad="Savunma", g="p377.jpg", o="50% 70%", soz=KATD["savunma"]["s"]["alinti"]["soz"], v=KATD["savunma"]["s"]["alinti"]["v"], kim="Prof. Dr. Kerem Aydın", unvan="Güvenlik uzmanı", r="Türkiye"),
    dict(tip="veri", kat="kadin", ad="Kadın", g="p502.jpg", o="50% 40%", b="Borsa şirketlerinin yönetim kurullarında kadın üye oranı yüzde 19 oldu", sayi="%19", acik="Borsa şirketlerinde kadın yönetim kurulu üyesi oranı", r="Türkiye"),
    dict(tip="sd", kat="spor", ad="Spor", g="p381.jpg", o="50% 45%", b="Süper Lig'de 14. hafta: derbide Galatasaray 2-1 önde", v="2-1 önde", r="İstanbul"),
]

# denetimler: başlıklar sözlükte birebir, görseller diskte, aynı görsel iki kartta yok
_kullanilan = []
for _c in KAT:
    for _s, _d in _c["s"].items():
        assert (KOK / "veri" / "gorsel" / _d["g"]).exists(), f"görsel yok: {_d['g']}"
        _kullanilan.append(_d["g"])
        if "b" in _d:
            assert _d["b"] in HABER, (_c["k"], _s, _d["b"])
        if "v" in _d:
            assert _d["v"] in (_d.get("b") or _d.get("soz")), (_c["k"], _s)
        for _b in _d.get("liste", []):
            assert _b in HABER, _b
for _a in AKIS:
    assert (KOK / "veri" / "gorsel" / _a["g"]).exists(), _a["g"]
    _kullanilan.append(_a["g"])
    if "b" in _a:
        assert _a["b"] in HABER, _a["b"]
assert len(set(_kullanilan)) == len(_kullanilan), "aynı görsel birden fazla kartta: " + str([g for g in _kullanilan if _kullanilan.count(g) > 1])

# ------------------------------------------------------------------ alternatifler (iskelet)
# yz: metnin oturduğu zemin (koyu: fotoğraf + karartma · acik: beyaz · kat: kategori rengi düz)
# lz: logonun oturduğu zemin; mecraya (kare 4:5 · uzun 9:16 · yatay) ya da iç sayfaya (ic) göre değişebilir
# guc: özdeğerlendirme (guclu | orta)
ALT = [
    dict(id="a", harf="A", ad="Vitrin", aile="Tam görsel + alttan geçiş",
         fikir="Fotoğraf bütün kareyi kaplar; alttan yumuşak geçişin üstünde büyük başlık, logo hep sol üstte.",
         kaynak="Fotoğrafın başrolde olması Reuters'tan (görüldü); görselin üstünde güçlü başlık GDH Dijital'den; sade “logo + renk + başlık” Fokus+ Afrika'dan (toplantı ekranı).",
         oz="En tanıdık ve en güvenli kalıp; akışta en az ayırt edici olan da bu. Fotoğraf zayıfsa kalıp da zayıflar.", guc="guclu",
         orn=dict(logo="plaka", etiket="nokta", oge="kalin", bvurgu="renkli", islem="gecis", kose="keskin"),
         yz=dict(_="koyu"), lz=dict(_="koyu")),
    dict(id="b", harf="B", ad="Blok", aile="Bölünmüş",
         fikir="Kare ikiye bölünür: üstte fotoğraf, altta kategori renginde düz blok ve başlık.",
         kaynak="Aynı iskelette kategoriye göre renk Sky Sports'tan (kısmen); tek kalıp, tek renk BPT Finans ve BPT Sinema'dan (toplantı ekranı).",
         oz="Her fotoğrafta okunur; akışta renk bloklarıyla güçlü ve düzenli bir ızgara kurar. Fotoğraf alanı yarıya iner.", guc="guclu",
         orn=dict(logo="duz", etiket="duz", oge="ince", bvurgu="renkli", islem="dogal", kose="keskin"),
         yz=dict(_="kat"), lz=dict(_="kat", uzun="koyu")),
    dict(id="c", harf="C", ad="Manşet", aile="Tipografik",
         fikir="Kategori renginde zemin ve dev başlık üstte; fotoğraf altta renge karışarak söner.",
         kaynak="Başlığın her şeyden önce gelmesi GDH Dijital'den; kalın yazılı kart Bleacher Report'tan (görüldü); tek vurgu, sade zemin The New York Times'tan (görüldü).",
         oz="Sözü güçlü haberde çok etkili; fotoğrafı güçlü haberde fotoğrafı geri plana iter.", guc="guclu",
         orn=dict(logo="duz", etiket="cerceve", oge="nokta", bvurgu="zeminli", islem="dogal", kose="keskin"),
         yz=dict(_="kat"), lz=dict(_="kat")),
    dict(id="d", harf="D", ad="Paspartu", aile="Çerçeve / paspartu",
         fikir="Fotoğraf beyaz paspartunun içinde durur; başlık altta beyaz alanda, logo sağ altta.",
         kaynak="Fotoğrafı kırpmadan çerçeveye sığdırma Reuters'tan (görüldü); temiz boşluk ve sadelik Fokus+ Afrika'dan (toplantı ekranı).",
         oz="Ciddi ve dergi gibi; akışta beyaz kareler fazla açık kalabilir, dikeyde fotoğraf küçülür.", guc="orta",
         orn=dict(logo="duz", etiket="dolu", oge="yok", bvurgu="renkli", islem="dogal", kose="yuvarlak"),
         yz=dict(_="acik"), lz=dict(_="acik")),
    dict(id="e", harf="E", ad="Kart", aile="Kart içinde kart",
         fikir="Fotoğrafın üstünde yüzen beyaz kart; başlık kartın içinde, kartın üstünde renk çizgisi.",
         kaynak="Sosyale özel, net okunan kart Financial Times'tan (görüldü); kategori etiketi BPT Haber'den (toplantı ekranı).",
         oz="Her fotoğrafta okunur ve sakin; kart fotoğrafın alt yarısını kapatır.", guc="guclu",
         orn=dict(logo="plaka", etiket="dolu", oge="kalin", bvurgu="renkli", islem="dogal", kose="yuvarlak"),
         yz=dict(_="acik"), lz=dict(_="koyu")),
    dict(id="f", harf="F", ad="Ton", aile="Çift ton",
         fikir="Fotoğrafın tamamı kategori renginde tek tona döner; logo, etiket ve başlık ortada, simetrik.",
         kaynak="Renk tonlu görsel Fokus+ Afrika'dan (toplantı ekranı); bütün grafiklerin tek şablonda, tema renginde olması The Economist'ten (kısmen; kırmızısı alınmadı).",
         oz="Akışta kategori rengini en güçlü taşıyan kalıp; yüzlü ya da renkli fotoğrafı tanınmaz hale getirebilir.", guc="guclu",
         orn=dict(logo="rozet", etiket="cerceve", oge="nokta", bvurgu="alti", islem="ton", kose="keskin"),
         yz=dict(_="koyu"), lz=dict(_="koyu")),
    dict(id="g", harf="G", ad="Sütun", aile="Yan sütun",
         fikir="Solda kategori renginde dikey sütun; etiket sütunda dik yazılır, logo sütunun dibinde.",
         kaynak="BPT Haber'in dikey etiket şeridi tam boya ve kategori rengine taşındı (toplantı ekranı); logo tek ve sabit yerde NowThis'ten (kısmen).",
         oz="Akışta çok tanınır, sütun her karede aynı yerde; fotoğraf genişliği beşte dörde iner.", guc="guclu",
         orn=dict(logo="duz", etiket="dikey", oge="ince", bvurgu="renkli", islem="gecis", kose="keskin"),
         yz=dict(_="koyu"), lz=dict(_="kat")),
    dict(id="h", harf="H", ad="Künye", aile="Dergi kapağı",
         fikir="Üstte büyük marka satırı ve sayı/tarih, ortada fotoğraf, altta başlık: dergi kapağı gibi.",
         kaynak="Başlık, alt metin ve tarihin kademeli dizilişi The New York Times'tan (görüldü); sabit adlı seri kapağı The Guardian'dan (kısmen).",
         oz="Dosya ve analizde çok güçlü; günlük haber akışında ağır kalabilir.", guc="orta",
         orn=dict(logo="duz", etiket="duz", oge="ince", bvurgu="yok", islem="dogal", kose="keskin"),
         yz=dict(_="acik"), lz=dict(_="acik")),
    dict(id="i", harf="I", ad="Kesik", aile="Kesik geometri",
         fikir="Fotoğrafın altını eğik bir kategori rengi keser; başlık kesiğin içinde, köşede ince işaret.",
         kaynak="Spor dilindeki hareket duygusu ESPN'den (kısmen; eğim açısı ve hız çizgisi alınmadı, eğim bizim); geometrik şekil seti DW'den (kısmen).",
         oz="Dinamik; spor ve son dakikada iyi. Eğik yüzey uzun başlıkta sıkışır, başlık küçülür.", guc="guclu",
         orn=dict(logo="plaka", etiket="duz", oge="kose", bvurgu="zeminli", islem="dogal", kose="keskin"),
         yz=dict(_="kat"), lz=dict(_="koyu", yatay="kat")),
    dict(id="j", harf="J", ad="Şerit", aile="Zemin vurgulu başlık",
         fikir="Fotoğraf siyah-beyaz; başlığın her satırı ayrı renkli kutuda, renk yalnız başlıkta.",
         kaynak="Görüntüye bindirilmiş kısa ekran yazısı BBC News ve AJ+'tan (görüldü); tek vurgu fikri AJ+'tan (sarısı alınmadı, renk kategoriden).",
         oz="Her fotoğrafta okunur ve hızlı; renk kutuları akışta kalabalık görünebilir.", guc="guclu",
         orn=dict(logo="plaka", etiket="nokta", oge="yok", bvurgu="yok", islem="sb", kose="keskin"),
         yz=dict(_="kat", ic="koyu"), lz=dict(_="koyu")),
    dict(id="m", harf="M", ad="Çerçeve", aile="Özgün birleşim: paspartu + zemin vurgulu başlık",
         fikir="Fotoğraf kategori renginde kalın çerçevede; başlık fotoğrafın sol altına oturan beyaz kutuda.",
         kaynak="Sabit çerçeve fikri NowThis'ten (kısmen); fotoğrafa saygı Reuters'tan (görüldü); tek renkli etiket The New York Times'tan (görüldü).",
         oz="Renk ve okunurluk bir arada; akışta çerçeveler düzenli bir ızgara kurar. Çerçeve fotoğrafı biraz küçültür.", guc="guclu",
         orn=dict(logo="duz", etiket="dolu", oge="kalin", bvurgu="renkli", islem="dogal", kose="keskin"),
         yz=dict(_="acik"), lz=dict(_="kat")),
    dict(id="n", harf="N", ad="Mercek", aile="Özgün birleşim: kesik geometri + tipografik",
         fikir="Beyaz zeminde fotoğraf büyük bir dairenin içinden köşeye taşar; başlık altta büyük.",
         kaynak="Geometrik şekil seti DW'den (kısmen); tek kalın vurgu Sky Sports'tan (kısmen); başlığın önde olması GDH Dijital'den (toplantı ekranı).",
         oz="Akışta en farklı duran kalıp; fotoğrafın daireye uygun bir odak noktası olmasını ister.", guc="guclu",
         orn=dict(logo="duz", etiket="nokta", oge="kalin", bvurgu="renkli", islem="dogal", kose="yuvarlak"),
         yz=dict(_="acik"), lz=dict(_="acik")),
]
# K ve L: dikey öğeli iki iskelet (t-kalip4: kalip/_iskelet_kl.py → ISKELETLER_KL, çizim kl.css); varsa J'den sonra girer
try:
    from _iskelet_kl import ISKELETLER_KL
except Exception as _ex:
    ISKELETLER_KL = []
    print(f"uyarı: _iskelet_kl yok ({_ex.__class__.__name__})")
try:
    from _iskelet_kl import kl_parca
except Exception:
    kl_parca = None
ALT = ALT[:10] + list(ISKELETLER_KL) + ALT[10:]
ALTD = {a["id"]: a for a in ALT}
SUSLEME = [
    ("logo", "Logo", [("duz", "Düz"), ("plaka", "Plaka"), ("rozet", "Rozet"), ("renk", "Renkli")]),
    ("etiket", "Etiket", [("duz", "Düz Yazı"), ("dolu", "Dolu Kutu"), ("cerceve", "Çerçeveli"), ("nokta", "Nokta"), ("dikey", "Dikey")]),
    ("oge", "Vurgu Öğesi", [("ince", "İnce Çizgi"), ("kalin", "Kalın Çizgi"), ("kose", "Köşe İşareti"), ("nokta", "Nokta Dizisi"), ("yok", "Yok")]),
    ("bvurgu", "Başlık Vurgusu", [("yok", "Yok"), ("renkli", "Renkli"), ("zeminli", "Zeminli"), ("alti", "Altı Çizgili")]),
    ("islem", "Görsel İşlemi", [("dogal", "Doğal"), ("gecis", "Alttan Geçiş"), ("ton", "Kategori Tonu"), ("sb", "Siyah-Beyaz")]),
    ("kose", "Köşe", [("keskin", "Keskin"), ("yuvarlak", "Yuvarlak")]),
]
MECRA = [("ig", "Instagram 4:5", "kare"), ("dikey", "Dikey 9:16", "uzun"), ("linkedin", "LinkedIn", "yatay"), ("facebook", "Facebook", "yatay"), ("x", "X", "yatay")]
KATSEC = [(c["k"], c["ad"]) for c in KAT]

# 9:16 güvenli alan: TEK VERİ TABLOSU (docs/tasarim-kararlari.md "9:16 güvenli alan ölçüleri", resmî kaynak, 25.11.2026)
GUVENLI = [
    dict(mecra="Instagram Hikâye", ust="%14 (≈269 px)", alt="%35 (672 px)", sol="%6 (≈65 px)", sag="%6 (≈65 px)", durum="Doğrulandı",
         kaynak="Meta Reklam Kılavuzu · Instagram Hikâye", adres="https://www.facebook.com/business/ads-guide/update/video/instagram-story"),
    dict(mecra="Instagram Reels", ust="%14 (≈269 px)", alt="%35 (672 px)", sol="%6 (≈65 px)", sag="%6 (≈65 px)", durum="Doğrulandı",
         kaynak="Meta Reklam Kılavuzu · Instagram Reels", adres="https://www.facebook.com/business/ads-guide/update/video/instagram-reels"),
    dict(mecra="YouTube Shorts", ust="288 px", alt="672 px", sol="48 px", sag="192 px", durum="Doğrulandı",
         kaynak="Google Ads Yardım · Universal safe zones", adres="https://support.google.com/google-ads/answer/13547298"),
    dict(mecra="TikTok", ust="—", alt="—", sol="—", sag="—", durum="Platform resmî ölçü yayımlamıyor",
         kaynak="TikTok Ads Yardım · In-Feed reklam özellikleri", adres="https://ads.tiktok.com/help/article/tiktok-auction-in-feed-ads"),
]
BIRLESIK = dict(ust=288, alt=672, sol=65, sag=192, en=1080, boy=1920)  # kalıpların uyduğu en kısıtlayıcı birleşik alan
OLCU = [("Instagram gönderi", "4:5 · 1080×1350"), ("Hikâye, Reels, Shorts, TikTok", "9:16 · 1080×1920"),
        ("LinkedIn", "1.91:1 · 1200×627"), ("Facebook", "1.91:1 · 1200×630"), ("X", "16:9 · 1200×675")]


# ------------------------------------------------------------------ parçalar
def vurgulu(b, v):
    i = b.find(v)
    return f'{e(b[:i])}<em class="kp-vurgu">{e(v)}</em>{e(b[i + len(v):])}'


def K(fn, sabit=None):
    """kategori metni: sabit (akış) verilirse tek; verilmezse beşi birden, seçili olmayanı kalip.css gizler"""
    if sabit is not None:
        return fn(sabit)
    return "".join(f'<span data-k="{c["k"]}">{fn(c)}</span>' for c in KAT)


LOGO = ('<span class="kp-logo"><span class="kb-logo kp-l-sari"></span><span class="kb-logo kb-logo-acik kp-l-koyu"></span>'
        '<span class="kp-l-maske"></span></span>')


def zemin(alt, tip, bicim):
    a = ALTD[alt]
    yz = a["yz"].get("ic") if tip == "ic" and "ic" in a["yz"] else a["yz"]["_"]
    lz = a["lz"].get("ic") if tip == "ic" and "ic" in a["lz"] else a["lz"].get(bicim, a["lz"]["_"])
    return yz, lz


def tuval(alt, tip, slot=None, bicim="kare", sabit=None, mecrali=False):
    """Bir sosyal görsel. tip: haber sd kapak ic alinti veri hikaye reels · slot: kategori içeriğindeki anahtar
    sabit: akış kartı (kendi kategorisi, görseli, metni) · mecrali: mecra seçimine göre biçim değiştirir (JS)"""
    if sabit:
        d0 = sabit
        stil = f' style="--kat:var(--kat-{d0["kat"]});--g:url(../veri/gorsel/{d0["g"]});--o:{d0["o"]}"'
        sinif = " kp-sabit"
        al = lambda fn: fn(d0)
        katad = lambda d: d["ad"]
        bolge = lambda d: d["r"]
    else:
        stil = ' style="' + ";".join(f'--g-{c["k"]}:url(../veri/gorsel/{c["s"][slot]["g"]});--o-{c["k"]}:{c["s"][slot]["o"]}' for c in KAT) + '"'
        sinif = ""
        al = lambda fn: "".join(f'<span data-k="{c["k"]}">{fn(dict(c["s"][slot], ad=c["ad"]))}</span>' for c in KAT)
        katad = lambda d: d["ad"]
        bolge = lambda d: d.get("r", "Türkiye")
    etk = al(lambda d: f'<b>{e(katad(d))}</b><span class="kp-bolge">{e(bolge(d))}</span>')
    etiket = f'<span class="kp-etiket"><span class="kp-nokta"></span>{etk}</span>'
    ic_ = ""
    if tip in ("haber", "sd", "kapak", "hikaye", "reels"):
        bas = al(lambda d: vurgulu(d["b"], d["v"]))
        ic_ = f'{etiket}<span class="kp-baslik"><span class="kp-bi">{bas}</span></span><span class="kp-meta">{al(lambda d: e(tarih(d["b"])))}</span>'
        if tip == "sd":
            ic_ = f'<span class="kp-sdbas"><i></i>Son Dakika<span class="kp-saat">{al(lambda d: e(saat(d["b"])))}</span></span>' + ic_
        if tip == "kapak":
            ic_ = '<span class="kp-ust-not">Kaydırmalı dosya · 4 sayfa</span>' + ic_
        if tip == "reels":
            ic_ = f'<span class="kp-oynat">{ikon("fa-play")}<span>0.48</span></span>' + ic_
        if tip == "hikaye":
            ic_ += f'<span class="kp-baglanti">{ikon("fa-link")}Haberi oku</span>'
    elif tip == "ic":
        liste = al(lambda d: "".join(f'<li><span class="kp-no">0{i + 1}</span><span>{e(x)}</span></li>' for i, x in enumerate(d["liste"])))
        ic_ = f'{etiket}<span class="kp-ic-bas">Öne çıkanlar</span><ol class="kp-liste">{liste}</ol>'
    elif tip == "alinti":
        ic_ = (f'{etiket}<span class="kp-glif kp-glif-tirnak">{ikon("fa-quote-left")}</span>'
               f'<span class="kp-baslik kp-soz"><span class="kp-bi">{al(lambda d: "“" + vurgulu(d["soz"], d["v"]) + "”")}</span></span>'
               f'<span class="kp-kim">{al(lambda d: "<b>" + e(d["kim"]) + "</b><span>" + e(d["unvan"]) + "</span>")}</span>')
    elif tip == "veri":
        ic_ = (f'{etiket}<span class="kp-sayi"><em class="kp-vurgu">{al(lambda d: e(d["sayi"]))}</em></span>'
               f'<span class="kp-aciklama">{al(lambda d: e(d["acik"]))}</span><span class="kp-meta">{al(lambda d: e(tarih(d["b"])))}</span>')
    kaydir = f'<span class="kp-kaydir">{"1" if tip == "kapak" else "2"}/4 · Kaydır{ikon("fa-arrow-right")}</span><span class="kp-sayfa-nokta"><i></i><i></i><i></i><i></i></span>' if tip in ("kapak", "ic") else ""
    mast = '<span class="kp-masthead"><span>25 Kasım 2026</span><b>Sayı 327</b></span>'
    yz, lz = zemin(alt, tip, bicim)
    return (f'<div class="kp-tuval kp-{alt}{sinif}" data-tip="{tip}" data-bicim="{bicim}" data-yz="{yz}" data-lz="{lz}"{" data-mecrali" if mecrali else ""}{stil} role="img" aria-label="{e(ALTD[alt]["harf"])} · {e(tip)}">'
            f'<span class="kp-gorsel"></span><span class="kp-karart"></span><span class="kp-sekil"></span><span class="kp-sekil2"></span><span class="kp-kose"></span>'
            f'{mast}{LOGO}{kaydir}<span class="kp-etiket-dikey">{etk}</span>'
            f'{kl_parca(tip, al, saat) if kl_parca else ""}<span class="kp-blok"><span class="kp-oge"><i></i><i></i><i></i></span>{ic_}</span><span class="kp-guvenli"></span></div>')


def sekil(t, yazi, cls=""):
    return f'<figure class="kp-sekil-kap{cls}">{t}<figcaption class="fhint">{yazi}</figcaption></figure>'


# içerik sekmeleri: (id, ad, ikon)
SEKME = [("akis", "Akışta Nasıl Durur", "fa-table-cells"), ("haber", "Haber Gönderisi", "fa-image"), ("sd", "Son Dakika", "fa-bolt"),
         ("kaydir", "Kaydırmalı", "fa-clone"), ("dikey", "Hikâye ve Reels", "fa-mobile-screen"), ("alinti", "Alıntı ve Veri", "fa-quote-left"),
         ("durum", "Durumlar", "fa-layer-group"), ("kisi", "Kişi Haberleri", "fa-user")]


def tek_icerik(sk, alt="a"):
    """tekli görünümde bir sekmenin tuvalleri (alternatiften bağımsız; iskeleti kalip.js değiştirir)"""
    if sk == "akis":
        return f'<div class="kp-akis" aria-label="Profil akışı">{"".join(tuval(alt, a["tip"], sabit=a) for a in AKIS)}</div>'
    if sk == "haber":
        return ('<div class="kp-sira" data-tur="mecra">' + sekil(tuval(alt, "haber", "haber_koyu", mecrali=True), "Koyu fotoğrafla")
                + sekil(tuval(alt, "haber", "haber_acik", mecrali=True), "Açık fotoğrafla") + '</div>')
    if sk == "sd":
        return ('<div class="kp-sira" data-tur="mecra">' + sekil(tuval(alt, "sd", "sd", mecrali=True), "Son Dakika: kategori rengi yerine kırmızı, fotoğraf siyah-beyaz, saat etikette") + '</div>')
    if sk == "kaydir":
        return ('<div class="kp-sira" data-tur="kare">' + sekil(tuval(alt, "kapak", "kapak"), "1. sayfa · kapak, “Kaydır” işaretli")
                + sekil(tuval(alt, "ic", "ic"), "2. sayfa · metin ağırlıklı iç sayfa, üstte görsel şeridi") + '</div>')
    if sk == "dikey":
        return ('<div class="kp-sira" data-tur="uzun">' + sekil(tuval(alt, "hikaye", "hikaye", bicim="uzun"), "Hikâye · 9:16")
                + sekil(tuval(alt, "reels", "reels", bicim="uzun"), "Reels ve Shorts kapağı · 9:16") + '</div>')
    if sk == "alinti":
        return ('<div class="kp-sira" data-tur="mecra">' + sekil(tuval(alt, "alinti", "alinti", mecrali=True), "Alıntı kartı · kişi ve söz kurgudur; görsel kişisiz")
                + sekil(tuval(alt, "veri", "veri", mecrali=True), "Veri kartı · dev rakam önde, görsel geri planda") + '</div>')
    return ""


# ------------------------------------------------------------------ Durumlar ve Kişi Haberleri (t-kalip2'nin modülleri; yalnız içe aktarılır)
def _dis(modul, islev):
    try:
        m = __import__(modul)
        return getattr(m, islev)
    except Exception as ex:  # modül henüz yoksa sayfa yine üretilir; bölümde "hazırlanıyor" yazar
        print(f"uyarı: {modul}.{islev} yok ({ex.__class__.__name__}: {ex})")
        return None


def dis_hazir(sk):
    """Durumlar / Kişi Haberleri ara sürümde yalnız modül var ve bütün görselleri diskteyse gösterilir"""
    fn = _dis("_durum", "durumlar_html") if sk == "durum" else _dis("_kisi", "kisi_html")
    if not fn:
        return False
    try:
        h = "".join(fn(a["id"]) for a in ALT)
    except Exception as ex:
        print(f"uyarı: {sk} üretilemedi ({ex})"); return False
    eksik = sorted({g for g in re.findall(r"veri/gorsel/([\w-]+\.(?:jpg|png))", h) if not (KOK / "veri" / "gorsel" / g).exists()})
    if eksik:
        print(f"uyarı: {sk} sekmesi gizlendi; diskte olmayan görsel {len(eksik)}: {', '.join(eksik[:6])}…")
        return False
    return True


def dis_bolum(sk):
    fn = _dis("_durum", "durumlar_html") if sk == "durum" else _dis("_kisi", "kisi_html")
    ad = "Durumlar" if sk == "durum" else "Kişi Haberleri"
    if not fn:
        return f'<div class="kb-bant bilgi">{ikon("fa-hourglass-half")}<span><b>{ad} hazırlanıyor.</b> Bölüm seçili iskeletin diliyle çizilecek.</span></div>'
    return "".join(f'<div class="kp-dis" data-alt-icerik="{a["id"]}"{"" if a["id"] == "a" else " hidden"}>{fn(a["id"])}</div>' for a in ALT)


def dis_css():
    return [c for c in ("kl.css", "durum.css", "kisi.css") if (BURA / c).exists()]


# ------------------------------------------------------------------ bilgi parçaları
def alt_bilgi():
    """Akış sekmesinin yanında: seçili alternatifin adı, ailesi, fikri, kaynakları, özdeğerlendirmesi (kalip.js doldurur)"""
    return (f'<aside class="pnl-card kp-bilgi" aria-label="Seçili alternatif">'
            f'<div class="pc-body"><div class="kp-bilgi-bas"><span class="kp-harf" data-kp-yaz="harf">A</span><div><h2 class="kp-bilgi-ad" data-kp-yaz="ad">Vitrin</h2><span class="fhint" data-kp-yaz="aile">{e(ALT[0]["aile"])}</span></div>'
            f'<span class="pstat ok" data-kp-yaz="guc">Güçlü</span></div>'
            f'<dl class="kp-bilgi-dl"><dt>Fikir</dt><dd data-kp-yaz="fikir">{e(ALT[0]["fikir"])}</dd>'
            f'<dt>Fikirlerin kaynağı</dt><dd data-kp-yaz="kaynak">{e(ALT[0]["kaynak"])}</dd>'
            f'<dt>Özdeğerlendirme</dt><dd data-kp-yaz="oz">{e(ALT[0]["oz"])}</dd></dl>'
            f'<p class="kp-bilgi-not">Dokuz gönderi profil ızgarasında: Dünya, Spor, Kampüs, Finans, Gündem, Savunma, Kadın; haber, Son Dakika, alıntı ve veri karışık. Görseller tekli örneklerden farklıdır.</p>'
            f'</div></aside>')


def guvenli_bolum():
    satir = "".join(f'<tr><td>{e(g["mecra"])}</td><td class="num">{e(g["ust"])}</td><td class="num">{e(g["alt"])}</td><td class="num">{e(g["sol"])}</td><td class="num">{e(g["sag"])}</td>'
                    f'<td><span class="pstat {"ok" if g["durum"] == "Doğrulandı" else "wait"}">{e(g["durum"])}</span></td></tr>' for g in GUVENLI)
    b = BIRLESIK
    satir += (f'<tr class="kp-birlesik"><td><b>Kalıpların uyduğu alan</b></td><td class="num">{b["ust"]} px</td><td class="num">{b["alt"]} px</td><td class="num">{b["sol"]} px</td><td class="num">{b["sag"]} px</td>'
              f'<td><span class="pstat ok">En kısıtlayıcı birleşim</span></td></tr>')
    kart = "".join(f'<a class="pnl-card kp-kaynak-kart" href="{e(g["adres"])}" target="_blank" rel="noopener"><div class="pc-body"><span class="kp-kk-ust">{ikon("fa-arrow-up-right-from-square")}{e(g["mecra"])}</span>'
                   f'<b>{e(g["kaynak"])}</b><span class="fhint">{e(g["adres"].split("//")[1].split("/")[0])}</span></div></a>' for g in GUVENLI)
    olcu = "".join(f'<span class="chip kp-olcu-cip">{e(m)}<b>{e(o)}</b></span>' for m, o in OLCU)
    return (f'<section class="kp-guvenli-bilgi" aria-labelledby="kpGuvBas"><h2 class="kp-alt-bas" id="kpGuvBas">{ikon("fa-mobile-screen")}Uygulama düğmelerinin kapattığı alan</h2>'
            f'<span class="fhint">Dikey 9:16 kalıplarda logo, başlık, etiket, “Kaydır” ve Son Dakika işareti bu alanın içinde kalır; Görünüm › Güvenli Alan ile tuvalde gösterilir. Değerler 1080×1920 içindir.</span>'
            f'<div class="tbl-wrap"><table class="tbl kp-guv-tbl"><thead><tr><th>Mecra</th><th class="num">Üst</th><th class="num">Alt</th><th class="num">Sol</th><th class="num">Sağ</th><th>Durum</th></tr></thead><tbody>{satir}</tbody></table></div>'
            f'<div class="kp-kaynak-serit" role="list" aria-label="Ölçü kaynakları">{kart}</div>'
            f'<div class="chips kp-olcu-cipler" aria-label="Gönderi ölçüleri">{olcu}</div></section>')


# ------------------------------------------------------------------ araç çubuğu (sağda, yapışkan)
def secenekler(ad, ad_g, ops, ozel=""):
    return (f'<div class="kb-secenek-grup kp-cipler" data-secenek-serbest role="radiogroup" aria-label="{e(ad_g)}">'
            + "".join(f'<label class="kb-secenek"><input type="radio" name="{ad}" value="{v}" {ozel}>{e(a)}</label>' for v, a in ops) + '</div>')


def arac():
    sus = "".join(f'<div class="kp-yan-satir"><span class="flabel">{e(ad)}</span>{secenekler("kpO-" + k, ad, ops, f"data-orn={k}")}<span class="fhint kp-pasif-not" data-pasif-not="{k}" hidden></span></div>'
                  for k, ad, ops in SUSLEME)
    return f"""  <aside class="kp-yan" id="kpArac" aria-label="Görünüm ve süsleme">
    <div class="kp-yan-ic pnl-card">
      <div class="kp-yan-bas">
        <button type="button" class="btn btn-ghost btn-sm kp-yan-kapat" data-kp-yan-kapat aria-label="Kapat">{ikon("fa-xmark")}</button>
        <span class="kp-harf kp-harf-b" data-kp-yaz="harf">A</span>
        <div class="kp-yan-ad"><b data-kp-yaz="ad">Vitrin</b><span class="fhint" data-kp-yaz="aile">{e(ALT[0]["aile"])}</span></div>
      </div>
      <div class="toggle-row kp-sec-satir"><span>Bunu Seç<small>Birden fazla seçilebilir; seçilenler aşağıda süslemeleriyle görünür</small></span><label class="toggle"><input type="checkbox" id="kpSec" aria-label="Bu alternatifi seç"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      <details class="kp-katman" open><summary>{ikon("fa-chevron-right")}Görünüm</summary>
        <div class="kp-yan-satir"><span class="flabel">Kategori Rengi</span>{secenekler("kpKat", "Kategori rengi", KATSEC, "data-kp=kat")}<span class="fhint">Renk kategori kaydından; görseller ve başlıklar da değişir</span></div>
        <div class="kp-yan-satir"><span class="flabel">Mecra</span>{secenekler("kpMecra", "Mecra", [(m, a) for m, a, b in MECRA], "data-kp=mecra")}<span class="fhint">Gönderi, Son Dakika, alıntı ve veri bu ölçüde yeniden dizilir; kırpılmaz</span></div>
        <div class="toggle-row"><span>Güvenli Alan<small>Dikeyde uygulama düğmelerinin kapattığı alan</small></span><label class="toggle"><input type="checkbox" data-kp="guvenli" aria-label="Güvenli alanı göster"><span class="toggle-track"></span><span class="toggle-thumb"></span></label></div>
      </details>
      <details class="kp-katman" open><summary>{ikon("fa-chevron-right")}Süsleme<button type="button" class="btn btn-ghost btn-sm kp-varsayilan" data-kp-varsayilan>{ikon("fa-rotate-left")}Varsayılan</button></summary>
        <span class="fhint kp-sus-not" data-kp-sus-not>İskelet aynı kalır; yalnız süsleme değişir. Her alternatif kendi varsayılanından başlar.</span>
        {sus}
      </details>
      <details class="kp-katman"><summary>{ikon("fa-chevron-right")}Notunuz ve Seçilenler</summary>
        <div class="kp-yan-satir"><label class="flabel" for="kpNot">Notunuz</label><textarea class="ftext" id="kpNot" rows="3" placeholder="ör. sütun iyi, başlık biraz daha büyük olsun"></textarea><span class="fhint">Bu sayfada kalır, kaydedilmez</span></div>
        <div class="kb-bant bilgi kp-secilen" id="kpOzet">{ikon("fa-circle-check")}<span><b>Seçilen:</b> <span class="kp-secilen-metin">henüz seçilmedi</span></span></div>
      </details>
    </div>
  </aside>
"""


def serit():
    oge = "".join(f'<button type="button" class="kp-serit-oge{" is-on" if i == 0 else ""}" data-alt="{a["id"]}" aria-pressed="{"true" if i == 0 else "false"}" title="{e(a["harf"])} · {e(a["ad"])} · {e(a["aile"])}">'
                  f'<span class="kp-minik kp-orn" data-alt="{a["id"]}" {" ".join(f"data-o-{k}={v}" for k, v in a["orn"].items())}>{tuval(a["id"], "haber", "haber_koyu")}</span>'
                  f'<span class="kp-serit-yazi"><span class="kp-harf">{e(a["harf"])}</span><span class="kp-serit-ad">{e(a["ad"])}<small>{e(a["aile"].replace("Özgün birleşim: ", "Birleşim · "))}</small></span></span></button>'
                  for i, a in enumerate(ALT))
    return (f'<div class="kp-secici">'
            f'<button type="button" class="btn btn-ghost btn-sm kp-serit-ok" data-kp-kaydir="-1" aria-label="Önceki alternatifler">{ikon("fa-chevron-left")}</button>'
            f'<div class="kp-serit" id="kpSerit" role="group" aria-label="Alternatifler">{oge}</div>'
            f'<button type="button" class="btn btn-ghost btn-sm kp-serit-ok" data-kp-kaydir="1" aria-label="Sonraki alternatifler">{ikon("fa-chevron-right")}</button>'
            f'<button type="button" class="btn btn-ghost kp-hepsi-btn" data-kp-hepsi aria-pressed="false">{ikon("fa-table-columns")}<span>Hepsini Yan Yana Gör</span></button></div>')


def v(yol):
    return hashlib.sha1((KOK / yol).read_bytes()).hexdigest()[:8] if (KOK / yol).exists() else "0"


def sayfa():
    sekme_liste = [x for x in SEKME if x[0] not in ("durum", "kisi") or dis_hazir(x[0])]
    sekmeler = "".join(f'<button type="button" class="sa-form-tab{" is-on" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-panel="kpT-{s}" data-sekme="{s}">{ikon(ik)}{e(a)}</button>'
                       for i, (s, a, ik) in enumerate(sekme_liste))
    orn0 = " ".join(f'data-o-{k}="{v_}"' for k, v_ in ALT[0]["orn"].items())
    paneller = ""
    for i, (s, a, ik) in enumerate(sekme_liste):
        if s in ("durum", "kisi"):
            ic_ = f'<div class="kp-tek kp-orn kp-dis-kap" {orn0}>{dis_bolum(s)}</div>'
        elif s == "akis":
            ic_ = f'<div class="kp-tek kp-akis-duzen"><div class="kp-orn kp-akis-kap" {orn0}>{tek_icerik(s)}</div>{alt_bilgi()}</div>'
        elif s == "dikey":
            ic_ = f'<div class="kp-tek kp-orn" {orn0}>{tek_icerik(s)}</div>{guvenli_bolum()}'
        else:
            ic_ = f'<div class="kp-tek kp-orn" {orn0}>{tek_icerik(s)}</div>'
        paneller += (f'    <div class="sa-form-panel" id="kpT-{s}" role="tabpanel" data-sekme="{s}"{"" if i == 0 else " hidden"}>\n      {ic_}\n'
                     f'      <div class="kp-hepsi-izgara" data-sekme="{s}" hidden></div>\n    </div>\n')
    veri = dict(alt=[dict(id=a["id"], harf=a["harf"], ad=a["ad"], aile=a["aile"], fikir=a["fikir"], kaynak=a["kaynak"], oz=a["oz"], guc=a["guc"],
                          orn=a["orn"], yz=a["yz"], lz=a["lz"], pasif=a.get("pasif", {})) for a in ALT],
                mecra={m: b for m, a, b in MECRA}, susleme={k: [o for o, _ in ops] for k, _, ops in SUSLEME},
                ad={k: dict(ops) for k, _, ops in SUSLEME}, grupad={k: ad for k, ad, _ in SUSLEME})
    css = ["../assets/vendor/fontawesome-6.5.2/css/all.min.css", "../tema/dadahaber.css", "../cekirdek/css/kabuk.css", "../cekirdek/css/bilesen.css"]
    js = ["../cekirdek/js/bilesen.js"]
    bag = "\n".join(f'<link rel="stylesheet" href="{c}?v={v(c[3:])}"{" data-tema" if "tema" in c else ""}>' for c in css)
    bag += "".join(f'\n<link rel="stylesheet" href="{c}?v={v("kalip/" + c)}">' for c in ["kalip.css"] + dis_css())
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
<!-- KALIP ALTERNATİFLERİ (DADAHABER-13) · ayrı sunum sayfası, panel kabuğu yok. Üretici kalip/_uret.py; çizim kalip.css; davranış kalip.js.
     Karar değil; Yasin Bey seçecek. Alıntı kartlarındaki kişi ve sözler kurgudur. Görsel lisansları: veri/gorsel/LISANSLAR.md -->
<main class="kp-sayfa" id="kpSahne" data-kat="gundem" data-mecra="ig" data-alt="a" data-sekme="akis">
  <div class="kp-duzen">
    <div class="kp-ana">
      <div class="pnl-page-head kp-bas">
        <div>
          <h1>Kalıp Alternatifleri</h1>
          <div class="ph-sub">Dada Haber sosyal medya · {len(ALT)} iskelet, üstüne süsleme · aynı haberler her kalıpta, her çeşitte ve her mecrada · karar değil, Yasin Bey seçecek · 25.11.2026</div>
        </div>
        <div class="ph-actions"><button type="button" class="btn btn-ghost btn-sm kp-yan-ac" data-kp-yan-ac aria-controls="kpArac" aria-expanded="false">{ikon("fa-sliders")}Görünüm</button></div>
      </div>
      {serit()}
      <section class="pnl-card kp-icerik" data-sekmeli aria-label="İçerik çeşitleri">
        <div class="sa-form-tabs" role="tablist" aria-label="İçerik çeşitleri">{sekmeler}</div>
{paneller}      </section>
    </div>
{arac()}  </div>
  <div class="kp-perde" data-kp-yan-kapat hidden></div>
</main>
<script type="application/json" id="kpVeri">{json.dumps(veri, ensure_ascii=False)}</script>
{bet}
</body>
</html>
"""
    (BURA / "index.html").write_text(s, encoding="utf-8")
    print("yazıldı: kalip/index.html", len(s.encode()) // 1024, "KB")


if __name__ == "__main__":
    sayfa()
