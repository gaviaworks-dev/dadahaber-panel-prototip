"""AI Haber Havuzu · örnek veri (yalnız bu modülün sayfaları için; _uret.py okur).

Gruplar moduller.json → ai-havuz.ayarlar.kaynak_gruplari'ndan gelir (T1–T4, kanallar).
Yayınlanan haberler public sözlükten (ai_kaynakli kayıtları veri/panel.json'da); taslak ve reddedilenler panel verisi.
"""

# ---- kaynak grupları: sıklık, örnek açıklaması (ad ve kanallar kayıttan) ----
# yeni_oran: çekim başına tekrar elendikten sonra kalan yeni içerik (kaynak arttıkça aynı olay çok kaynaktan gelir, oran düşer)
GRUP_EK = {
    "T1": {"ornek": "örn. Resmî Gazete, bakanlıklar, valilikler", "siklik": 2, "birim": "saat", "yeni_oran": 0.10},
    "T2": {"ornek": "örn. Anadolu Ajansı, DHA, İHA, KAP", "siklik": 30, "birim": "dakika", "yeni_oran": 0.06},
    "T3": {"ornek": "örn. Reuters, AP, AFP, BBC Türkçe", "siklik": 1, "birim": "saat", "yeni_oran": 0.05},
    "T4": {"ornek": "örn. sosyal medya hesapları, küçük haber siteleri", "siklik": 1, "birim": "gün", "yeni_oran": 0.30},
}
HABER_BASI_USD = 0.0195   # içerik başı AI işleme maliyeti (örnek)
KUR = 39.49               # ₺ / $ (Kontrol Paneli: $50,47 ≈ ₺1.993)

# ---- kaynaklar: id, ad, tip, adres, grup, durum (aktif | pasif | hata | cop), son çekim, başarı %, 30 günde haber, not ----
KAYNAKLAR = [
    ("resmi-gazete", "Resmî Gazete", "scraper", "resmigazete.gov.tr", "T1", "aktif", "16.00", 100, 212, ""),
    ("iletisim", "İletişim Başkanlığı", "rss", "iletisim.gov.tr/rss", "T1", "aktif", "16.00", 100, 96, ""),
    ("meb", "Millî Eğitim Bakanlığı", "haber-sitesi", "meb.gov.tr/haberler", "T1", "aktif", "16.00", 98, 64, ""),
    ("ist-valilik", "İstanbul Valiliği", "sosyal-hesap", "x.com/istanbulvalilik", "T1", "aktif", "16.00", 100, 41, ""),
    ("ssb", "Savunma Sanayii Başkanlığı", "rss", "ssb.gov.tr/rss", "T1", "aktif", "16.00", 100, 38, ""),
    ("ticaret", "T.C. Ticaret Bakanlığı", "scraper", "ticaret.gov.tr/haberler", "T1", "aktif", "16.00", 96, 52, ""),
    ("mgm", "Meteoroloji Genel Müdürlüğü", "rss", "mgm.gov.tr/rss", "T1", "aktif", "16.00", 100, 57, ""),
    ("afad", "AFAD", "sosyal-hesap", "x.com/AFADBaskanlik", "T1", "pasif", "18.11 09.00", 0, 0, "18.11.2026'da pasifleştirildi · Selin Aydemir"),
    ("aa", "Anadolu Ajansı", "rss", "aa.com.tr/tr/rss/default?cat=guncel", "T2", "aktif", "16.00", 99, 1840, ""),
    ("dha", "Demirören Haber Ajansı (DHA)", "rss", "dha.com.tr/rss", "T2", "aktif", "16.00", 100, 1215, ""),
    ("iha", "İhlas Haber Ajansı (İHA)", "rss", "iha.com.tr/rss", "T2", "aktif", "16.00", 97, 1102, ""),
    ("aselsan", "ASELSAN Basın Odası", "haber-sitesi", "aselsan.com/tr/haberler", "T2", "aktif", "15.30", 100, 22, ""),
    ("kap", "Kamuyu Aydınlatma Platformu (KAP)", "scraper", "kap.org.tr/tr/bildirim-sorgu", "T2", "aktif", "16.00", 94, 436, ""),
    ("reuters", "Reuters", "rss", "reuters.com/world", "T3", "aktif", "16.00", 100, 388, ""),
    ("ap", "Associated Press", "rss", "apnews.com/hub/world-news", "T3", "aktif", "16.00", 100, 341, ""),
    ("afp", "AFP", "rss", "afp.com/en/news-hub", "T3", "aktif", "16.00", 99, 276, ""),
    ("bbc", "BBC Türkçe", "rss", "bbc.com/turkce", "T3", "pasif", "02.11 10.00", 0, 0, "02.11.2026'da pasifleştirildi · Selin Aydemir"),
    ("defense-news", "Defense News", "rss", "defensenews.com/arc/outboundfeeds/rss", "T3", "hata", "14.20", 26, 48, "403 Forbidden · 14.20'den beri 11 deneme"),
    ("ekonomi-gundem", "@ekonomi_gundem (X)", "sosyal-hesap", "x.com/ekonomi_gundem", "T4", "aktif", "09.00", 100, 30, ""),
    ("tekno-gundem", "Teknoloji Gündemi", "haber-sitesi", "teknolojigundemi.ornek/feed", "T4", "aktif", "09.00", 92, 27, ""),
    ("marmara-yerel", "Marmara Yerel Haber", "haber-sitesi", "marmarayerel.ornek", "T4", "pasif", "12.11 09.00", 0, 0, "12.11.2026'da pasifleştirildi · Selin Aydemir"),
    ("kampus-postasi", "Kampüs Postası", "rss", "kampuspostasi.ornek/rss", "T4", "pasif", "05.11 09.00", 0, 0, "05.11.2026'da pasifleştirildi · Selin Aydemir"),
    ("ekonomi-bulteni", "Ekonomi Bülteni (Telegram)", "sosyal-hesap", "t.me/ekonomibulteni_ornek", "T4", "cop", "01.11 09.00", 0, 0, "20.11.2026'da çöpe taşındı · Selin Aydemir"),
]
# sayfalama için genişletilmiş kaynak listesi (Beyar: listede en az 70 kayıt); gruplar içinde yukarıdakilerin ardından gelir
KAYNAKLAR_EK = [
    # T1 · Resmî (2 saatte bir; son tur 16.00)
    ("saglik-bak", "Sağlık Bakanlığı", "haber-sitesi", "saglik.gov.tr/haberler", "T1", "aktif", "16.00", 100, 48, ""),
    ("disisleri", "Dışişleri Bakanlığı", "scraper", "mfa.gov.tr/aciklamalar", "T1", "aktif", "16.00", 99, 73, ""),
    ("hmb", "Hazine ve Maliye Bakanlığı", "rss", "hmb.gov.tr/duyurular/rss", "T1", "aktif", "16.00", 100, 35, ""),
    ("tcmb", "Türkiye Cumhuriyet Merkez Bankası", "rss", "tcmb.gov.tr/duyurular/rss", "T1", "aktif", "16.00", 100, 44, ""),
    ("tuik", "Türkiye İstatistik Kurumu (TÜİK)", "scraper", "data.tuik.gov.tr/bultenler", "T1", "aktif", "16.00", 95, 31, ""),
    ("msb", "Millî Savunma Bakanlığı", "sosyal-hesap", "x.com/tcsavunma", "T1", "aktif", "16.00", 100, 62, ""),
    ("icisleri", "İçişleri Bakanlığı", "haber-sitesi", "icisleri.gov.tr/haberler", "T1", "aktif", "16.00", 100, 58, ""),
    ("ankara-valilik", "Ankara Valiliği", "sosyal-hesap", "x.com/ankaravalilik", "T1", "aktif", "16.00", 100, 29, ""),
    ("izmir-valilik", "İzmir Valiliği", "haber-sitesi", "izmir.gov.tr/haberler", "T1", "aktif", "16.00", 97, 21, ""),
    ("spk", "Sermaye Piyasası Kurulu (SPK)", "scraper", "spk.gov.tr/duyurular", "T1", "hata", "12.00", 83, 26, "Sayfa yapısı değişti · 14.00 ve 16.00 çekimlerinde haber bulunamadı"),
    ("bddk", "BDDK", "rss", "bddk.org.tr/duyurular/rss", "T1", "aktif", "16.00", 100, 14, ""),
    ("epdk", "Enerji Piyasası Düzenleme Kurumu (EPDK)", "scraper", "epdk.gov.tr/duyurular", "T1", "aktif", "16.00", 98, 19, ""),
    ("kgm", "Karayolları Genel Müdürlüğü", "sosyal-hesap", "x.com/kgmgovtr", "T1", "aktif", "16.00", 100, 33, ""),
    ("yok", "Yükseköğretim Kurulu (YÖK)", "haber-sitesi", "yok.gov.tr/haberler", "T1", "aktif", "16.00", 100, 17, ""),
    ("osym", "ÖSYM", "rss", "osym.gov.tr/duyurular/rss", "T1", "pasif", "14.11 10.00", 0, 0, "14.11.2026'da pasifleştirildi · Selin Aydemir · sınav takvimi elle giriliyor"),
    ("afad-deprem", "AFAD Deprem Kataloğu", "scraper", "deprem.afad.gov.tr/son-depremler", "T1", "aktif", "16.00", 100, 86, ""),
    # T2 · Kurumsal Basın (30 dakikada bir; kurum basın odaları yavaş yanıt verdiği için 15.30 turunda)
    ("anka", "ANKA Haber Ajansı", "rss", "ankahaber.net/rss", "T2", "aktif", "16.00", 98, 642, ""),
    ("trt-haber", "TRT Haber", "rss", "trthaber.com/rss/sondakika.rss", "T2", "aktif", "16.00", 100, 1288, ""),
    ("ntv", "NTV", "rss", "ntv.com.tr/gundem.rss", "T2", "aktif", "16.00", 99, 904, ""),
    ("bloomberght", "Bloomberg HT", "rss", "bloomberght.com/rss", "T2", "aktif", "16.00", 100, 517, ""),
    ("haberturk", "Habertürk", "rss", "haberturk.com/rss", "T2", "pasif", "10.11 11.30", 0, 0, "10.11.2026'da pasifleştirildi · Selin Aydemir · içerik kullanım izni yenileniyor"),
    ("tusas", "TUSAŞ Basın Odası", "haber-sitesi", "tusas.com/medya/haberler", "T2", "aktif", "15.30", 100, 18, ""),
    ("baykar", "Baykar Haberler", "haber-sitesi", "baykartech.com/tr/haberler", "T2", "aktif", "15.30", 100, 15, ""),
    ("roketsan", "Roketsan Basın Odası", "haber-sitesi", "roketsan.com.tr/tr/haberler", "T2", "aktif", "15.30", 100, 11, ""),
    ("thy", "Türk Hava Yolları Basın Bültenleri", "haber-sitesi", "turkishairlines.com/tr-tr/basin-odasi", "T2", "aktif", "15.30", 96, 24, ""),
    ("borsa-ist", "Borsa İstanbul Duyuruları", "scraper", "borsaistanbul.com/tr/duyurular", "T2", "aktif", "16.00", 100, 138, ""),
    ("tobb", "TOBB Haberler", "rss", "tobb.org.tr/haberler/rss", "T2", "aktif", "16.00", 100, 27, ""),
    ("tff", "TFF Duyurular", "haber-sitesi", "tff.org/duyurular", "T2", "aktif", "16.00", 100, 96, ""),
    ("tbf", "Türkiye Basketbol Federasyonu", "haber-sitesi", "tbf.org.tr/haberler", "T2", "pasif", "08.11 16.00", 0, 0, "08.11.2026'da pasifleştirildi · Selin Aydemir · maç sonuçları canlı skordan geliyor"),
    # T3 · Uluslararası Medya (saatte bir)
    ("bloomberg", "Bloomberg", "rss", "bloomberg.com/europe", "T3", "aktif", "16.00", 100, 302, ""),
    ("ft", "Financial Times", "scraper", "ft.com/world", "T3", "pasif", "04.11 12.00", 0, 0, "04.11.2026'da pasifleştirildi · Selin Aydemir · ücretli içerik, tam metin alınamıyor"),
    ("aljazeera", "Al Jazeera", "rss", "aljazeera.com/xml/rss/all.xml", "T3", "aktif", "16.00", 100, 264, ""),
    ("dw", "DW Türkçe", "rss", "dw.com/tr", "T3", "aktif", "16.00", 99, 187, ""),
    ("euronews", "Euronews Türkçe", "rss", "tr.euronews.com/rss", "T3", "aktif", "16.00", 100, 215, ""),
    ("guardian", "The Guardian", "rss", "theguardian.com/world/rss", "T3", "aktif", "16.00", 100, 233, ""),
    ("cnn", "CNN International", "rss", "edition.cnn.com/world", "T3", "aktif", "16.00", 98, 198, ""),
    ("lemonde", "Le Monde", "rss", "lemonde.fr/international/rss_full.xml", "T3", "aktif", "16.00", 100, 121, ""),
    ("al-monitor", "Al-Monitor", "rss", "al-monitor.com/rss", "T3", "aktif", "16.00", 100, 9, ""),
    ("kyiv-ind", "The Kyiv Independent", "rss", "kyivindependent.com/feed", "T3", "aktif", "16.00", 100, 88, ""),
    ("janes", "Janes", "scraper", "janes.com/defence-news", "T3", "aktif", "16.00", 94, 41, ""),
    ("breaking-def", "Breaking Defense", "rss", "breakingdefense.com/feed", "T3", "aktif", "16.00", 100, 57, ""),
    # T4 · Düşük Öncelik (günde bir; 09.00)
    ("ege-yerel", "Ege Yerel Haber", "haber-sitesi", "egeyerel.ornek/haberler", "T4", "aktif", "09.00", 100, 24, ""),
    ("karadeniz-gundem", "Karadeniz Gündem", "haber-sitesi", "karadenizgundem.ornek", "T4", "aktif", "09.00", 96, 19, ""),
    ("spor-bulteni", "Anadolu Spor Bülteni", "rss", "anadolusporbulteni.ornek/feed", "T4", "aktif", "09.00", 100, 31, ""),
    ("oyun-tekno", "Oyun ve Teknoloji", "rss", "oyunteknoloji.ornek/rss", "T4", "hata", "22.11 09.00", 0, 12, "XML ayrıştırılamadı · 23.11 09.00 çekimi başarısız"),
    ("borsa-notlari", "Borsa Notları (Telegram)", "sosyal-hesap", "t.me/borsanotlari_ornek", "T4", "aktif", "09.00", 100, 22, ""),
    ("trafik-bilgi", "@trafik_bilgi (X)", "sosyal-hesap", "x.com/trafik_bilgi_ornek", "T4", "aktif", "09.00", 100, 28, ""),
    ("hava-uyari", "@hava_uyarisi (X)", "sosyal-hesap", "x.com/hava_uyarisi_ornek", "T4", "aktif", "09.00", 100, 17, ""),
    ("oto-dunyasi", "Otomobil Dünyası", "haber-sitesi", "otomobildunyasi.ornek/feed", "T4", "aktif", "09.00", 100, 14, ""),
    ("savunma-analiz", "Savunma Analiz", "rss", "savunmaanaliz.ornek/rss", "T4", "aktif", "09.00", 100, 20, ""),
    ("cukurova", "Çukurova Haber", "haber-sitesi", "cukurovahaber.ornek", "T4", "pasif", "16.11 09.00", 0, 0, "16.11.2026'da pasifleştirildi · Selin Aydemir · tekrar oranı yüksek"),
    ("kripto-sinyal", "Kripto Sinyal (Telegram)", "sosyal-hesap", "t.me/kriptosinyal_ornek", "T4", "cop", "19.11 09.00", 0, 0, "21.11.2026'da çöpe taşındı · Selin Aydemir"),
]
_GRUP_SIRA = ["T1", "T2", "T3", "T4"]
KAYNAKLAR = sorted(KAYNAKLAR + KAYNAKLAR_EK, key=lambda k: _GRUP_SIRA.index(k[4]))  # sıralama kararlı: grup içinde eskiler önce

# hatalı kaynakların çekim günlüğü (görüntüle çekmecesi; yoksa 403 kalıbı)
HATA_LOG = {
    "defense-news": [("hata", "16.00.20", "403 Forbidden · 11. deneme · sonraki deneme 17.00"), ("hata", "15.00.18", "403 Forbidden"), ("bilgi", "14.20.11", "4 yeni içerik, 2 tekrar elendi")],
    "spk": [("hata", "16.00.41", "Haber listesi bulunamadı: seçici eşleşmedi (sayfa yapısı değişmiş olabilir)"), ("hata", "14.00.39", "Haber listesi bulunamadı: seçici eşleşmedi"), ("bilgi", "12.00.37", "2 yeni içerik")],
    "oyun-tekno": [("hata", "09.00.06", "XML ayrıştırılamadı: 214. satırda kapanmamış öğe"), ("bilgi", "22.11 · 09.00.05", "3 yeni içerik, 1 tekrar elendi")],
}
TIP = {
    "rss": ("RSS", "fa-rss"),
    "scraper": ("Kazıyıcı (scraper)", "fa-spider"),
    "haber-sitesi": ("Haber sitesi", "fa-globe"),
    "sosyal-hesap": ("Sosyal medya hesabı", "fa-hashtag"),
}

# ---- havuz satırları ----
# (id, başlık, öneri kategori, alt konu, 1./2./3. kaynak id, güven, görsel durumu, görsel, çekilme, düzenleme kaydı)
TASLAK = [
    ("ai-mgm-kar", "Meteoroloji'den Marmara için turuncu kod kar uyarısı", "Gündem", "İstanbul", ["mgm", "aa", "dha"], 91, "kirpildi", "p183", "23.11.2026 15.58", "kirpildi"),
    ("ai-ab-uyelik", "AB genişleme toplantısında Türkiye'nin üyelik süreci de konuşuldu", "Dünya", "Avrupa", ["reuters", "ap", "aa"], 78, "eksik", "", "23.11.2026 15.52", "eksik"),
    ("ai-benzin", "Benzinde indirim beklentisi: pompaya yansıması hafta sonunu bulabilir", "Finans", "Enerji", ["ekonomi-gundem"], 62, "temiz", "p192", "23.11.2026 09.04", "temiz"),
    ("ai-atama", "Resmî Gazete'de bugün: 14 atama kararı yayımlandı", "Gündem", "Siyaset", ["resmi-gazete"], 95, "eksik", "", "23.11.2026 15.40", "eksik"),
    ("ai-ida", "Savunma Sanayii Başkanlığı yeni insansız deniz aracı projesini duyurdu", "Savunma", "Deniz Platformları", ["ssb", "aselsan"], 89, "temiz", "p195", "23.11.2026 15.31", "kirpildi"),
    ("ai-kap-birlesme", "KAP: iki enerji şirketinden birleşme görüşmesi açıklaması", "Finans", "Şirketler", ["kap", "aa"], 86, "eksik", "", "23.11.2026 15.24", "eksik"),
    ("ai-fed-dolar", "Fed tutanakları sonrası küresel piyasalarda dolar geriledi", "Finans", "Dünya Ekonomisi", ["reuters", "afp"], 83, "kirpildi", "p188", "23.11.2026 15.20", "kirpildi"),
    ("ai-meb-ara-tatil", "Millî Eğitim Bakanlığı: ara tatil takvimi değişmedi", "Gündem", "Eğitim", ["meb", "iha"], 93, "temiz", "p163", "23.11.2026 15.12", "kirpildi"),
    ("ai-kar-koy", "Doğu Anadolu'da kar: 214 köy yolu ulaşıma kapandı", "Gündem", "Türkiye", ["aa", "dha", "iha"], 90, "kirpildi", "p178", "23.11.2026 15.05", "kirpildi"),
    ("ai-g20-tarim", "G20 tarım bakanları gıda güvenliği bildirisi yayımladı", "Dünya", "Uluslararası Kuruluşlar", ["ap"], 71, "temiz", "p180", "23.11.2026 14.48", "kirpildi"),
    ("ai-fahis-fiyat", "Ticaret Bakanlığı fahiş fiyat denetiminde 1.240 işletmeye ceza kesti", "Finans", "Türkiye Ekonomisi", ["ticaret", "aa"], 88, "temiz", "p158", "23.11.2026 14.40", "kirpildi"),
    ("ai-sarj-agi", "Yerli elektrikli otomobil için yeni şarj ağı anlaşması imzalandı", "Keşfet", "Otomobil", ["tekno-gundem"], 58, "temiz", "p193", "23.11.2026 09.02", "temiz"),
]
# yayınlanan: public sözlükteki id + panel.json ai_kaynakli; otomatik yayımlananlar 22.11 (otomatik yayın açıkken)
OTOMATIK = [
    # (public id, kaynak id'leri, güven, görsel durumu)
    ("gram-altin-haftayi-yatay-seyirle-tamamladi", ["aa", "dha"], 92, "temiz"),
    ("urdun-de-yeni-hukumet-guvenoyu-aldi", ["reuters", "ap", "afp"], 87, "kirpildi"),
    ("kisisel-verileri-koruma-kurulu-uc-sirkete-idari-para-cezasi-verdi", ["resmi-gazete", "aa"], 95, "temiz"),
]
KAYNAK_AD_ID = {  # panel.json ai_kaynakli "kaynak" adı → kaynak id
    "İstanbul Valiliği": "ist-valilik", "Savunma Sanayii Başkanlığı": "ssb", "Associated Press": "ap", "Anadolu Ajansı": "aa",
    "Reuters": "reuters", "Millî Eğitim Bakanlığı": "meb", "Resmî Gazete": "resmi-gazete",
}
IKINCI = {  # yayınlananların teyit kaynakları (2. ve 3.)
    "istanbul-valiligi-okullar-24-kasim-da-da-tatil": ["aa", "dha"],
    "savunma-sanayiinde-2027-yatirim-programi-aciklandi": ["aa"],
    "ab-disisleri-bakanlari-bruksel-de-genisleme-gundemini-ele-aldi": ["reuters", "afp"],
    "turkiye-ile-japonya-arasinda-ekonomik-ortaklik-gorusmeleri-suruyor": ["iha"],
    "g7-ulkeleri-kritik-mineraller-icin-ortak-tedarik-plani-hazirladi": ["ap", "afp"],
    "hindistan-da-eyalet-secimlerinin-sonuclari-aciklandi": ["ap"],
    "lgs-icin-ornek-soru-kitapcigi-yayimlandi": ["aa", "iha"],
    "besiktas-turk-telekom-u-84-80-gecti": ["dha"],
    "kamu-kurumlari-icin-toplu-kirtasiye-alimi-ihalesi": [],
}
REDDEDILEN = [
    # (id, başlık, kategori, alt, kaynaklar, güven, görsel, görsel durumu, çekilme, neden, reddeden, durum)
    ("ai-red-butce", "Bütçe görüşmelerinde grupların ilk konuşmaları tamamlandı", "Gündem", "Siyaset", ["aa", "iha"], 84, "p164", "temiz", "23.11.2026 15.30", "Tekrar: aynı olay 15.42'de yayımlandı", "Sibel Arslan", "reddedilen"),
    ("ai-red-kripto", "Kripto parada büyük çöküş iddiası", "Finans", "Kişisel Finans", ["ekonomi-gundem"], 41, "", "eksik", "23.11.2026 09.04", "Teyitsiz: tek kaynak, T4", "Elif Aras", "reddedilen"),
    ("ai-red-saat", "Akıllı saatlerde yüzde 40 indirim kampanyası başladı", "Keşfet", "Teknoloji", ["tekno-gundem"], 52, "p117", "temiz", "23.11.2026 09.02", "Reklam içerikli", "Kerem Aksoy", "reddedilen"),
    ("ai-red-ankara", "Kar nedeniyle Ankara'da bütün okullar tatil edildi", "Gündem", "Ankara", ["dha"], 74, "p122", "kirpildi", "23.11.2026 13.10", "Hatalı bilgi: tatil yalnız 3 ilçede", "Mehmet Koçak", "reddedilen"),
    ("ai-red-nato", "NATO'nun Baltık tatbikatı başladı", "Dünya", "Avrupa", ["defense-news", "reuters"], 66, "p133", "kirpildi", "22.11.2026 18.40", "Güncelliğini yitirdi", "Merve Çınar", "reddedilen"),
    ("ai-red-hakem", "Süper Lig'de 14. hafta hakem atamaları açıklandı", "Spor", "Süper Lig", ["iha"], 80, "p155", "temiz", "23.11.2026 11.20", "Kapsam dışı: spor masası kendi giriyor", "Burak Tan", "cop"),
]
RED_NEDEN = [
    ("tekrar", "Tekrar", "Aynı olay daha önce yayımlandı ya da havuzda var"),
    ("teyitsiz", "Teyitsiz", "Bağımsız ikinci kaynak yok ya da kaynaklar çelişiyor"),
    ("hatali", "Hatalı bilgi", "Kaynakta olmayan ya da yanlış aktarılmış bilgi"),
    ("guncel-degil", "Güncelliğini yitirdi", "Olay eski ya da gelişme geride kaldı"),
    ("kapsam", "Kapsam dışı", "Yayın politikasına uymuyor (reklam, magazin vb.)"),
    ("diger", "Diğer", "Açıklamaya yazın"),
]

KISA = {"mgm": "Meteoroloji GM", "kap": "KAP", "ssb": "SSB", "meb": "MEB", "ticaret": "Ticaret Bakanlığı", "dha": "DHA", "iha": "İHA",
        "aa": "AA", "iletisim": "İletişim Bşk.", "resmi-gazete": "Resmî Gazete", "ist-valilik": "İstanbul Valiliği", "aselsan": "ASELSAN",
        "ap": "AP", "ekonomi-gundem": "@ekonomi_gundem", "tekno-gundem": "Teknoloji Gündemi", "defense-news": "Defense News"}
