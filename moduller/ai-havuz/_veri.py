"""AI Haber Havuzu · örnek veri (yalnız bu modülün sayfaları için; _uret.py okur).

Gruplar moduller.json → ai-havuz.ayarlar.kaynak_gruplari'ndan gelir (T1–T4, kanallar).
Yayınlanan haberler public sözlükten (ai_kaynakli kayıtları veri/panel.json'da); taslak ve reddedilenler panel verisi.
"""

# ---- kaynak grupları: sıklık, örnek açıklaması (ad ve kanallar kayıttan) ----
GRUP_EK = {
    "T1": {"ornek": "örn. Resmî Gazete, bakanlıklar, valilikler", "siklik": 2, "birim": "saat", "yeni_oran": 0.30},
    "T2": {"ornek": "örn. Anadolu Ajansı, DHA, İHA, KAP", "siklik": 30, "birim": "dakika", "yeni_oran": 0.20},
    "T3": {"ornek": "örn. Reuters, AP, AFP, BBC Türkçe", "siklik": 1, "birim": "saat", "yeni_oran": 0.20},
    "T4": {"ornek": "örn. sosyal medya hesapları, küçük haber siteleri", "siklik": 1, "birim": "gün", "yeni_oran": 1.50},
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
