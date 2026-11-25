"""AI Haber Havuzu · örnek veri (yalnız bu modülün sayfaları için; _uret.py okur).

Gruplar moduller.json → ai-havuz.ayarlar.kaynak_gruplari'ndan gelir (T1–T12: ad, sıklık, kanallar; DADAHABER-11).
Kaynaklar DADAHABER-12 kataloğundan grup başına 4–6 gerçek kurum (ad, alan adı, akış, içerik detayı, hedef kategori aynen).
Yayınlanan haberler public sözlükten (ai_kaynakli kayıtları veri/panel.json'da); taslak ve reddedilenler panel verisi.
"""

# ---- kaynak grupları: örnek açıklaması, varsayılan çekim tipi (katalog grup profili), yeni içerik oranı ----
# ad, sıklık ve kanallar kayıttan gelir. yeni_oran: çekim başına tekrar elendikten sonra kalan yeni içerik
# (günlük gruplarda bir çekim günün seçkisini getirir, oran yüksek). Aylık tahmin ≈ Kontrol Paneli AI maliyeti.
GRUP_EK = {
    "T1": {"ornek": 'örn. Resmî Gazete, bakanlıklar, TBMM, AFAD, ÖSYM, YÖK', "tip": "scraper", "yeni_oran": 0.08},
    "T2": {"ornek": 'örn. TCMB, BDDK, SPK, KAP, TÜİK, EPDK, Rekabet Kurumu', "tip": "scraper", "yeni_oran": 0.06},
    "T3": {"ornek": 'örn. AA, DHA, İHA, ANKA', "tip": "rss", "yeni_oran": 0.25},
    "T4": {"ornek": 'örn. Reuters, AP, AFP, Bloomberg, dpa', "tip": "rss", "yeni_oran": 3.0},
    "T5": {"ornek": 'örn. TRT Haber, NTV, CNN Türk, Cumhuriyet, BBC Türkçe', "tip": "rss", "yeni_oran": 0.1},
    "T6": {"ornek": 'örn. BBC News, The Guardian, Al Jazeera, Politico, DW', "tip": "rss", "yeni_oran": 2.5},
    "T7": {"ornek": 'örn. Bloomberg HT, Ekonomim, Dünya Gazetesi, Forbes', "tip": "rss", "yeni_oran": 0.1},
    "T8": {"ornek": 'örn. SSB, ASELSAN, TUSAŞ, ROKETSAN, Baykar, MKE', "tip": "scraper", "yeni_oran": 0.05},
    "T9": {"ornek": 'örn. TFF, UEFA, FIFA, TRT Spor, Fanatik, kulüpler', "tip": "rss", "yeni_oran": 0.15},
    "T10": {"ornek": 'örn. TÜBİTAK, Webrazzi, TechCrunch, NASA, İKSV', "tip": "rss", "yeni_oran": 0.1},
    "T11": {"ornek": 'örn. büyükşehir belediyeleri ve yerel basın', "tip": "scraper", "yeni_oran": 0.08},
    "T12": {"ornek": 'örn. küçük haber siteleri, niş hesaplar, Telegram', "tip": "sosyal-hesap", "yeni_oran": 2.0},
}
HABER_BASI_USD = 0.0195   # içerik başı AI işleme maliyeti (örnek)
KUR = 39.49               # ₺ / $ (Kontrol Paneli: $50,47 ≈ ₺1.993)

# ---- kaynaklar: id, ad, tip, alan adı, grup, durum (aktif | pasif | hata | cop), son çekim, başarı %, 30 günde içerik, not ----
# tip ve sıklık gruptan gelir; kaynakta değiştirilebilir (DETAY.siklik, tuple tipi). Ad ve alan adı katalogdan aynen.
KAYNAKLAR = [
    ('resmi-gazete', 'Resmî Gazete', 'scraper', 'resmigazete.gov.tr', 'T1', 'aktif', '16.00', 100, 212, ''),
    ('disisleri', 'T.C. Dışişleri Bakanlığı', 'scraper', 'mfa.gov.tr', 'T1', 'aktif', '16.00', 99, 73, ''),
    ('meb', 'T.C. Millî Eğitim Bakanlığı (MEB)', 'scraper', 'meb.gov.tr', 'T1', 'aktif', '16.00', 98, 64, ''),
    ('ticaret', 'T.C. Ticaret Bakanlığı', 'scraper', 'ticaret.gov.tr', 'T1', 'aktif', '16.00', 96, 52, ''),
    ('afad', 'AFAD (Afet ve Acil Durum Yönetimi Başkanlığı)', 'scraper', 'afad.gov.tr', 'T1', 'aktif', '16.00', 100, 118, ''),
    ('osym', 'ÖSYM (Ölçme, Seçme ve Yerleştirme Merkezi)', 'scraper', 'osym.gov.tr', 'T1', 'pasif', '14.11 10.00', 0, 0, "14.11.2026'da pasifleştirildi · Selin Aydemir · sınav takvimi elle giriliyor"),
    ('kap', 'Kamuyu Aydınlatma Platformu (KAP)', 'scraper', 'kap.org.tr', 'T2', 'aktif', '16.00', 94, 436, ''),
    ('tuik', 'Türkiye İstatistik Kurumu (TÜİK)', 'veri-akisi', 'tuik.gov.tr', 'T2', 'aktif', '16.00', 100, 31, ''),
    ('bddk', 'Bankacılık Düzenleme ve Denetleme Kurumu (BDDK)', 'scraper', 'bddk.org.tr', 'T2', 'aktif', '16.00', 100, 14, ''),
    ('epdk', 'Enerji Piyasası Düzenleme Kurumu (EPDK)', 'scraper', 'epdk.gov.tr', 'T2', 'aktif', '16.00', 98, 19, ''),
    ('rekabet', 'Rekabet Kurumu', 'scraper', 'rekabet.gov.tr', 'T2', 'hata', '13.00', 88, 17, "Sayfa yapısı değişti · 14.00'ten beri haber bulunamadı"),
    ('aa', 'Anadolu Ajansı (AA) — Gündem', 'rss', 'aa.com.tr', 'T3', 'aktif', '16.00', 99, 1840, ''),
    ('aa-ekonomi', 'Anadolu Ajansı (AA) — Ekonomi', 'rss', 'aa.com.tr', 'T3', 'aktif', '16.00', 99, 612, ''),
    ('dha', 'Demirören Haber Ajansı (DHA) — Gündem', 'rss', 'dha.com.tr', 'T3', 'aktif', '16.00', 100, 1215, ''),
    ('iha', 'İhlas Haber Ajansı (İHA) — Gündem', 'rss', 'iha.com.tr', 'T3', 'aktif', '16.00', 97, 1102, ''),
    ('anka', 'ANKA Haber Ajansı — Politika', 'rss', 'ankahaber.net', 'T3', 'aktif', '16.00', 98, 342, ''),
    ('reuters', 'Reuters', 'rss', 'reuters.com', 'T4', 'aktif', '06.00', 100, 94, ''),
    ('ap', 'Associated Press (AP News)', 'rss', 'apnews.com', 'T4', 'aktif', '06.00', 100, 81, ''),
    ('afp', 'Agence France-Presse (AFP)', 'rss', 'afp.com', 'T4', 'aktif', '06.00', 100, 76, ''),
    ('dpa', 'dpa (Deutsche Presse-Agentur)', 'rss', 'dpa.com', 'T4', 'aktif', '06.00', 100, 42, ''),
    ('azertac', 'AZERTAC', 'rss', 'azertag.az', 'T4', 'pasif', '09.11 06.00', 0, 0, "09.11.2026'da pasifleştirildi · Selin Aydemir · tekrar oranı yüksek"),
    ('cnnturk', 'CNN Türk', 'rss', 'cnnturk.com', 'T5', 'aktif', '16.00', 100, 388, ''),
    ('milliyet', 'Milliyet', 'rss', 'milliyet.com.tr', 'T5', 'aktif', '16.00', 99, 341, ''),
    ('cumhuriyet', 'Cumhuriyet', 'rss', 'cumhuriyet.com.tr', 'T5', 'aktif', '16.00', 100, 203, ''),
    ('t24', 'T24', 'rss', 't24.com.tr', 'T5', 'aktif', '16.00', 97, 96, ''),
    ('euronews', 'Euronews Türkçe', 'rss', 'tr.euronews.com', 'T5', 'aktif', '16.00', 100, 215, ''),
    ('bbc-news', 'BBC News', 'rss', 'bbc.com', 'T6', 'aktif', '06.00', 100, 58, ''),
    ('aljazeera', 'Al Jazeera English', 'rss', 'aljazeera.com', 'T6', 'aktif', '06.00', 100, 49, ''),
    ('politico-eu', 'Politico Europe', 'rss', 'politico.eu', 'T6', 'aktif', '06.00', 98, 31, ''),
    ('nytimes', 'The New York Times (NYT)', 'rss', 'nytimes.com', 'T6', 'aktif', '06.00', 100, 44, ''),
    ('ft', 'Financial Times (FT)', 'rss', 'ft.com', 'T6', 'pasif', '04.11 06.00', 0, 0, "04.11.2026'da pasifleştirildi · Selin Aydemir · ücretli içerik, tam metin alınamıyor"),
    ('forbes', 'Forbes Türkiye', 'rss', 'forbes.com.tr', 'T7', 'aktif', '16.00', 100, 64, ''),
    ('patronlar', 'Patronlar Dünyası', 'rss', 'patronlardunyasi.com', 'T7', 'aktif', '16.00', 99, 118, ''),
    ('enerji-gunlugu', 'Enerji Günlüğü', 'rss', 'enerjigunlugu.net', 'T7', 'aktif', '16.00', 100, 57, ''),
    ('emlak-kulisi', 'Emlak Kulisi', 'rss', 'emlakkulisi.com', 'T7', 'aktif', '16.00', 96, 141, ''),
    ('odmd', 'Otomotiv Distribütörleri ve Mobilite Derneği (ODMD)', 'rss', 'odmd.org.tr', 'T7', 'aktif', '16.00', 100, 12, ''),
    ('ssb', 'Savunma Sanayii Başkanlığı (SSB)', 'scraper', 'ssb.gov.tr', 'T8', 'aktif', '16.00', 100, 38, ''),
    ('aselsan', 'ASELSAN', 'scraper', 'aselsan.com', 'T8', 'aktif', '16.00', 100, 22, ''),
    ('baykar', 'Baykar Teknoloji', 'scraper', 'baykartech.com', 'T8', 'aktif', '16.00', 100, 15, ''),
    ('mke', 'MKE (Makine ve Kimya Endüstrisi)', 'scraper', 'mke.gov.tr', 'T8', 'aktif', '16.00', 98, 9, ''),
    ('defense-news', 'Defense News', 'rss', 'defensenews.com', 'T8', 'hata', '12.00', 83, 48, "403 Forbidden · 12.00'den beri 2 deneme"),
    ('tff', 'Türkiye Futbol Federasyonu (TFF)', 'rss', 'tff.org', 'T9', 'aktif', '15.00', 100, 96, ''),
    ('tbf', 'Türkiye Basketbol Federasyonu (TBF)', 'rss', 'tbf.org.tr', 'T9', 'aktif', '15.00', 100, 41, ''),
    ('tvf', 'Türkiye Voleybol Federasyonu (TVF)', 'rss', 'tvf.org.tr', 'T9', 'aktif', '15.00', 100, 33, ''),
    ('fanatik', 'Fanatik', 'rss', 'fanatik.com.tr', 'T9', 'aktif', '15.00', 97, 284, ''),
    ('motorsport', 'Motorsport.com Türkiye', 'rss', 'tr.motorsport.com', 'T9', 'aktif', '15.00', 100, 52, ''),
    ('tua', 'Türkiye Uzay Ajansı (TUA)', 'rss', 'tua.gov.tr', 'T10', 'aktif', '15.00', 100, 11, ''),
    ('webtekno', 'Webtekno', 'rss', 'webtekno.com', 'T10', 'aktif', '15.00', 98, 187, ''),
    ('evrim-agaci', 'Evrim Ağacı', 'rss', 'evrimagaci.org', 'T10', 'aktif', '15.00', 100, 46, ''),
    ('techcrunch', 'TechCrunch', 'rss', 'techcrunch.com', 'T10', 'aktif', '15.00', 100, 73, ''),
    ('ytb', 'YTB (Yurtdışı Türkler ve Akraba Topluluklar Bşk.)', 'rss', 'ytb.gov.tr', 'T10', 'aktif', '15.00', 100, 8, ''),
    ('ibb', 'İstanbul Büyükşehir Belediyesi (İBB)', 'scraper', 'ibb.istanbul', 'T11', 'aktif', '16.00', 100, 96, ''),
    ('ist-valilik', 'T.C. İstanbul Valiliği', 'scraper', 'istanbul.gov.tr', 'T11', 'aktif', '16.00', 100, 41, ''),
    ('ankara-bb', 'Ankara Büyükşehir Belediyesi (ABB)', 'scraper', 'ankara.bel.tr', 'T11', 'aktif', '16.00', 97, 58, ''),
    ('izmir-bb', 'İzmir Büyükşehir Belediyesi', 'scraper', 'izmir.bel.tr', 'T11', 'aktif', '16.00', 100, 62, ''),
    ('bursa-hakimiyet', 'Bursa Hakimiyet', 'scraper', 'bursahakimiyet.com.tr', 'T11', 'aktif', '16.00', 95, 37, ''),
    ('kocaeli-gazetesi', 'Kocaeli Gazetesi', 'scraper', 'kocaeligazetesi.com.tr', 'T11', 'cop', '19.11 12.00', 0, 0, "21.11.2026'da çöpe taşındı · Selin Aydemir"),
    ('x-ekonomi', 'X (Twitter) — Ekonomi & Piyasa Uzmanları', 'sosyal-hesap', 'x.com', 'T12', 'aktif', '09.00', 100, 30, ''),
    ('telegram-kurumsal', 'Telegram — Kurumsal Duyuru Kanalları', 'sosyal-hesap', 't.me', 'T12', 'pasif', '12.11 09.00', 0, 0, "12.11.2026'da pasifleştirildi · Selin Aydemir · kanal listesi gözden geçiriliyor"),
    ('ensonhaber', 'Ensonhaber', 'rss', 'ensonhaber.com', 'T12', 'hata', '22.11 09.00', 0, 12, 'XML ayrıştırılamadı · 23.11 09.00 çekimi başarısız'),
    ('haberler-com', 'Haberler.com', 'rss', 'haberler.com', 'T12', 'aktif', '09.00', 100, 27, ''),
    ('onedio', 'Onedio', 'rss', 'onedio.com', 'T12', 'cop', '18.11 09.00', 0, 0, "20.11.2026'da çöpe taşındı · Selin Aydemir"),
]
# katalog sütunları: Birim/Açıklama, Akış Yolu, İçerik Detayı, Hedef Kategori (üst › alt; public kategori.json ağacından),
# siklik: kaynağa özel sıklık (None → grubun sıklığı). Katalogda çift kategorili (ör. "Dünya / Finans") kaynakta hedef boş: AI her haberde önerir.
DETAY = {
    'resmi-gazete': dict(birim='Cumhurbaşkanlığı Mevzuat Yayın', akis='Günlük Sayı & Mükerrer Akışı', icerik='Kanunlar, Cumhurbaşkanlığı kararnameleri, yönetmelikler, tebliğler, atama kararları ve Yargı/ İlan bölümü.', hedef='Gündem › Hukuk', siklik=None),
    'disisleri': dict(birim='Enformasyon Genel Müdürlüğü', akis='Basın Açıklamaları & Duyurular', icerik='Dış politika bildirimleri, ikili zirveler, konsolosluk seyahat uyarıları ve uluslararası kriz açıklamaları.', hedef='Dünya › Diplomasi', siklik=None),
    'meb': dict(birim='Örgün Eğitim, LGS & Öğretmen Atamaları', akis='Haberler & Duyurular', icerik='Eğitim-öğretim takvimi, ara tatil/karne tarihleri, LGS kılavuzu, müfredat değişiklikleri ve öğretmen atamaları.', hedef='Kampüs › Eğitim ve Sınavlar', siklik=None),
    'ticaret': dict(birim='Dış Ticaret, Gümrük & Piyasa Denetimi', akis='Haberler & Basın Açıklamaları', icerik='Aylık dış ticaret verileri, ikinci el otomotiv/emlak ilan denetimleri, fahiş fiyat cezaları ve gümrük kararları.', hedef='Finans › Türkiye Ekonomisi', siklik=None),
    'afad': dict(birim='Deprem Dairesi & Acil Durum Duyuruları', akis='Son Depremler & Basın Duyuruları', icerik='Resmî deprem verileri, meteorolojik sarı/turuncu uyarılar, afet konutu teslimleri ve insani yardım sevkiyatları.', hedef='Gündem › Çevre ve Afet', siklik='1 saat'),
    'osym': dict(birim='Sınav Takvimi & Sonuç Duyuruları', akis='Duyurular & Sınav Takvimi', icerik='YKS, KPSS, ALES, YDS, DGS ve MSÜ başvuru başlangıç/bitiş tarihleri, sınav giriş belgeleri ve yerleştirme sonuçları.', hedef='Kampüs › Eğitim ve Sınavlar', siklik=None),
    'kap': dict(birim='Şirket Özel Durum & Bilanço Bildirimleri', akis='Bildirim Sorgu & Öne Çıkanlar', icerik='Halka açık şirketlerin yeni iş ilişkileri, sermaye artırımları, temettü kararları ve finansal tabloları.', hedef='Finans › Şirketler', siklik=None),
    'tuik': dict(birim='Resmî İstatistik Haber Bültenleri', akis='Haber Bültenleri Takvimi', icerik='Aylık TÜFE/ÜFE enflasyon oranları, çeyreklik GSYH büyüme rakamları, işgücü, sanayi üretimi ve konut satışları.', hedef='Finans › Enflasyon', siklik=None),
    'bddk': dict(birim='Kurul Kararları & Sektör Verileri', akis='Duyurular & Kurul Kararları', icerik='Kredi kartı taksit sınırları, konut/taşıt kredisi oranları, dijital banka izinleri ve haftalık sektör bülteni.', hedef='Finans › Bankacılık', siklik=None),
    'epdk': dict(birim='Tarife & Enerji Piyasası Kararları', akis='Duyurular & Kurul Kararları', icerik='Mesken ve sanayi elektrik/doğalgaz tarife güncellemeleri, akaryakıt tavan fiyat ve şarj ağı lisans kararları.', hedef='Finans › Enerji', siklik=None),
    'rekabet': dict(birim='Soruşturma & Birleşme/Devralma Kararları', akis='Haberler & Nihai Kararlar', icerik='Büyük şirket birleşme izinleri, dijital platform/perakende soruşturmaları ve rekabet ihlali cezaları.', hedef='Finans › İş Dünyası', siklik=None),
    'aa': dict(birim='Ulusal Birincil Tel Akışı', akis='/tr/gundem', icerik='Türkiye geneli resmi açıklamalar, yargı, güvenlik, eğitim ve toplumsal olaylara dair birincil ajans haberleri.', hedef='Gündem', siklik=None),
    'aa-ekonomi': dict(birim='Finans Terminali & Piyasa Akışı', akis='/tr/ekonomi', icerik='AA Finans beklenti anketleri, makroekonomik veriler, enerji, tarım ve şirket yatırımları.', hedef='Finans', siklik=None),
    'dha': dict(birim='Ulusal Sıcak Haber Akışı', akis='/gundem', icerik='İstanbul, Ankara, İzmir ve yurt genelinden anlık olay, asayiş, ulaşım ve kamu haberleri.', hedef='Gündem', siklik=None),
    'iha': dict(birim='81 İl Muhabir Ağı Akışı', akis='/gundem', icerik='Türkiye genelindeki il ve ilçe muhabirlerinden gelen sıcak gelişmeler, belediye ve valilik etkinlikleri.', hedef='Gündem', siklik=None),
    'anka': dict(birim='TBMM & Siyasi Parti Akışı', akis='/kategori/politika', icerik='Siyasi parti grup toplantıları, Meclis kulisleri, belediye başkanları ve seçim gündemi.', hedef='Gündem › Siyaset', siklik=None),
    'reuters': dict(birim='Birleşik Krallık / Küresel Tel Ağı', akis='/world & /markets', icerik='Küresel merkez bankaları, emtia/petrol fiyatları, diplomasi ve uluslararası sıcak gelişmeler.', hedef='', siklik=None),
    'ap': dict(birim='ABD Uluslararası Haber Ajansı', akis='/world-news', icerik='ABD dış politikası, küresel güvenlik, iklim zirveleri ve uluslararası teyitli haberler.', hedef='Dünya', siklik=None),
    'afp': dict(birim='Fransa Küresel Haber Ajansı', akis='News & Fact-Check Akışı', icerik='Avrupa Birliği, Orta Doğu, Afrika gelişmeleri ve uluslararası doğrulama bültenleri.', hedef='Dünya', siklik=None),
    'dpa': dict(birim='Almanya Ulusal Haber Ajansı', akis='International News Akışı', icerik='Almanya hükümeti kararları, Avrupa sanayisi, göç politikaları ve AB gündemi.', hedef='Dünya › Avrupa', siklik=None),
    'azertac': dict(birim='Azerbaycan Devlet Haber Ajansı', akis='/en & /tr', icerik='Türkiye-Azerbaycan ilişkileri, Karabağ imar projeleri, Zengezur koridoru ve Türk Dünyası.', hedef='Dünya › Türk Dünyası', siklik=None),
    'cnnturk': dict(birim='Haber & Yayın Gündemi', akis='Türkiye, Dünya & Ekonomi', icerik='Canlı yayın konuk açıklamaları, sıcak siyaset ve dış politika analizleri.', hedef='Gündem', siklik=None),
    'milliyet': dict(birim='Ulusal Gazete & Dijital Portal', akis='Gündem, Siyaset & Eğitim', icerik='Ankara kulisleri, çalışma hayatı ve toplumsal gündem haberleri.', hedef='Gündem', siklik=None),
    'cumhuriyet': dict(birim='Ulusal Gazete & Dijital Portal', akis='Siyaset, Hukuk & Kültür', icerik='Yargı süreçleri, yükseköğretim, bilim ve kültür-sanat haberleri.', hedef='Gündem › Hukuk', siklik=None),
    't24': dict(birim='Bağımsız İnternet Gazetesi', akis='Haberler, Dosyalar & Söyleşiler', icerik='Özel araştırmalar, hukuk/insan hakları, kültür ve derinlemesine söyleşiler.', hedef='Gündem › Özel Haber', siklik=None),
    'euronews': dict(birim='Avrupa Haber Ağı Türkçe Servisi', akis='Avrupa, Dünya & Yeşil', icerik='AB politikaları, iklim/enerji dönüşümü, seyahat ve kültür haberleri.', hedef='Dünya › Avrupa', siklik=None),
    'bbc-news': dict(birim='Birleşik Krallık Kamu Yayıncısı', akis='/news/world', icerik='Avrupa, Orta Doğu, ABD seçimleri ve küresel bilim/iklim dosyaları.', hedef='Dünya', siklik=None),
    'aljazeera': dict(birim='Orta Doğu & Küresel Güney Ağı', akis='/news & /middle-east', icerik='Orta Doğu diplomasi trafiği, Gazze/Suriye/Körfez ve Afrika gelişmeleri.', hedef='Dünya › Orta Doğu', siklik=None),
    'politico-eu': dict(birim='AB & Brüksel Politika Yayını', akis='EU Policy & Defense', icerik='Avrupa Komisyonu kararları, AB genişleme süreci, vize ve ticaret kuralları.', hedef='Dünya › Avrupa', siklik=None),
    'nytimes': dict(birim='ABD Uluslararası Gazetesi', akis='/section/world', icerik='ABD dış politikası, araştırmacı gazetecilik ve yapay zekâ/bilim dosyaları.', hedef='Dünya › Amerika', siklik=None),
    'ft': dict(birim='Küresel Ekonomi & Finans Gazetesi', akis='/world & /markets', icerik='Küresel sermaye akışları, ticaret politikaları, bankacılık ve jeoekonomi.', hedef='Finans › Dünya Ekonomisi', siklik=None),
    'forbes': dict(birim='İş Dünyası, Girişim & Finans Yayını', akis='Liderlik, Para & İnovasyon', icerik='Girişim ekosistemleri, finansal analizler ve kurumsal dönüşüm hikayeleri.', hedef='Finans › Girişimcilik', siklik=None),
    'patronlar': dict(birim='İş Dünyası & Şirket Haberleri', akis='Şirketler & İş Dünyası', icerik='Holding yatırımları, şirket satın almaları, üst düzey yönetici değişiklikleri.', hedef='Finans › Şirketler', siklik=None),
    'enerji-gunlugu': dict(birim='Enerji Piyasası & Sektör Portalı', akis='Elektrik, Petrol & Yenilenebilir', icerik='Güneş/rüzgâr santrali yatırımları, elektrik piyasası fiyatları ve enerji diplomasisi.', hedef='Finans › Enerji', siklik=None),
    'emlak-kulisi': dict(birim='Gayrimenkul & İnşaat Sektörü Portalı', akis='Konut, Kentsel Dönüşüm & Projeler', icerik='Konut kira/satış verileri, kentsel dönüşüm projeleri ve inşaat maliyet endeksleri.', hedef='Finans › Gayrimenkul', siklik=None),
    'odmd': dict(birim='Otomotiv Pazar Verileri & Raporlar', akis='Basın Bültenleri & Pazar Verileri', icerik='Aylık otomobil, hafif ticari ve elektrikli araç satış rakamları (Otomotiv dikeyi).', hedef='Finans › Otomotiv', siklik=None),
    'ssb': dict(birim='Cumhurbaşkanlığı Savunma Kurumu', akis='Haberler & Duyurular', icerik='Millî proje sözleşmeleri, envantere giriş törenleri ve savunma ihracat verileri.', hedef='Savunma › Millî Projeler', siklik=None),
    'aselsan': dict(birim='Savunma Elektroniği & Hava Savunma', akis='Medya & Haberler', icerik='Çelik Kubbe bileşenleri, AESA radarlar, elektro-optik sistemler ve ihracat anlaşmaları.', hedef='Savunma › Savunma Teknolojileri', siklik=None),
    'baykar': dict(birim='İnsansız Hava Araçları & Muharip İHA', akis='Haberler & Duyurular', icerik='Bayraktar TB2, TB3, AKINCI, KIZILELMA ve KEMANKEŞ uçuş testleri ve ihracat sözleşmeleri.', hedef='Savunma › İHA ve SİHA', siklik=None),
    'mke': dict(birim='Silah Sistemleri, Topçu & Mühimmat', akis='Haberler & Duyurular', icerik='Fırtına obüsü, BORAN, deniz topu, piyade tüfekleri ve mühimmat üretim tesisleri.', hedef='Savunma › Kara Sistemleri', siklik=None),
    'defense-news': dict(birim='ABD / Küresel Savunma Sanayii Yayını', akis='/global & /pentagon', icerik='NATO savunma bütçeleri, ABD savunma ihaleleri, F-16/F-35 ve füze savunma programları.', hedef='Savunma › NATO', siklik=None),
    'tff': dict(birim='Resmî Futbol Federasyonu', akis='Haberler & Kurul Kararları', icerik='Süper Lig ve 1. Lig fikstürü, hakem atamaları, PFDK/Tahkim kararları ve A Millî Takım duyuruları.', hedef='Spor › Futbol', siklik=None),
    'tbf': dict(birim='Resmî Basketbol Federasyonu', akis='Haberler & Ligler', icerik='Türkiye Sigorta Basketbol Süper Ligi, 12 Dev Adam ve Potanın Perileri maç/kadro duyuruları.', hedef='Spor › Basketbol', siklik=None),
    'tvf': dict(birim='Resmî Voleybol Federasyonu', akis='Haberler & Duyurular', icerik='Vodafone Sultanlar Ligi, Efeler Ligi, VNL ve Avrupa/Dünya Şampiyonası millî takım haberleri.', hedef='Spor › Voleybol', siklik=None),
    'fanatik': dict(birim='Ulusal Spor Gazetesi & Portal', akis='Futbol, Transfer & Branşlar', icerik='Süper Lig kulüpleri transfer gelişmeleri, maç analizleri ve çoklu branş haberleri.', hedef='Spor › Transfer', siklik=None),
    'motorsport': dict(birim='Motor Sporları Haber Portalı', akis='Formula 1, MotoGP & WRC', icerik='Formula 1 yarış takvimi, sıralama turları, MotoGP, WRC ve Türk pilotların yarış sonuçları.', hedef='Spor › Motor Sporları', siklik=None),
    'tua': dict(birim='Ulusal Uzay Programı Kurumu', akis='Haberler & Duyurular', icerik='Türk astronot bilim misyonları, Ay Araştırma Programı, yerli uydu ve uzay teknolojisi haberleri.', hedef='Keşfet › Uzay', siklik=None),
    'webtekno': dict(birim='Dijital Kültür & Popüler Teknoloji', akis='Haberler, Bilim & Oyun', icerik='Sosyal medya platform değişiklikleri, oyun çıkış tarihleri ve gençlik dijital kültürü.', hedef='Keşfet › Teknoloji', siklik=None),
    'evrim-agaci': dict(birim='Popüler Bilim & Araştırma Platformu', akis='Bilim Haberleri & Makaleler', icerik='Evrimsel biyoloji, fizik, astronomi, tıp ve bilimsel okuryazarlık içerikleri.', hedef='Keşfet › Bilim', siklik=None),
    'techcrunch': dict(birim='Küresel Startup & Yapay Zekâ Yayını', akis='/category/artificial-intelligence', icerik='OpenAI, Google, Anthropic, Meta yapay zekâ lansmanları ve Silikon Vadisi yatırımları.', hedef='Keşfet › Yapay Zekâ', siklik=None),
    'ytb': dict(birim='Türkiye Bursları & Uluslararası Öğrenci', akis='Duyurular & Haberler', icerik='Türkiye Bursları başvuru takvimi, staj/akademi programları ve diaspora etkinlikleri.', hedef='Kampüs › Burslar', siklik=None),
    'ibb': dict(birim='İstanbul Yerel Yönetim Duyuruları', akis='Haberler & Duyurular', icerik='Metro/metrobüs hat açılışları, toplu ulaşım tarifeleri, İSKİ/altyapı ve kültür etkinlikleri.', hedef='Gündem › İstanbul', siklik=None),
    'ist-valilik': dict(birim='İstanbul Mülki İdare Duyuruları', akis='Basın Açıklamaları & Duyurular', icerik='Olumsuz hava/kar tatili kararları, trafik kapatma duyuruları ve il güvenliği açıklamaları.', hedef='Gündem › İstanbul', siklik=None),
    'ankara-bb': dict(birim='Başkent Yerel Yönetim Duyuruları', akis='Haberler & Duyurular', icerik='EGO ulaşım duyuruları, ASKİ altyapı çalışmaları, öğrenci/sosyal destek projeleri.', hedef='Gündem › Ankara', siklik=None),
    'izmir-bb': dict(birim='İzmir Yerel Yönetim Duyuruları', akis='Haberler & Duyurular', icerik='İZBAN/ESHOT ulaşım düzenlemeleri, Körfez çevre projeleri ve İzmir fuar/kültür duyuruları.', hedef='Gündem › İzmir', siklik=None),
    'bursa-hakimiyet': dict(birim='Bursa Bölgesel Gazete & Portal', akis='Bursa & Ekonomi Haberleri', icerik='Bursa otomotiv/tekstil sanayii, şehir gündemi ve yerel yönetim haberleri.', hedef='Gündem › Şehirler', siklik=None),
    'kocaeli-gazetesi': dict(birim='Kocaeli Bölgesel Gazete', akis='Kocaeli & Ekonomi', icerik='Kocaeli limanları, otomotiv/kimya sanayii ve yerel gündem haberleri.', hedef='Gündem › Şehirler', siklik=None),
    'x-ekonomi': dict(birim='Finans Yorumcu & Analist Listesi', akis='Ekonomi Analist Listesi', icerik='Piyasa kapanış değerlendirmeleri, veri grafikleri ve kısa finans notları.', hedef='', siklik=None),
    'telegram-kurumsal': dict(birim='Resmî ve Sektörel Telegram Akışı', akis='Onaylı Duyuru Kanalları', icerik='Kısa bülten özetleri, acil durum uyarıları ve medya duyuru kanalları.', hedef='', siklik=None),
    'ensonhaber': dict(birim='Hızlı Portal & Sosyal Akış', akis='Gündem & Aktüel Akışı', icerik='Sosyal medya etkileşimi yüksek kısa başlıklar ve aktüel gündem maddeleri.', hedef='', siklik=None),
    'haberler-com': dict(birim='Derleme Portal Akışı', akis='Son Dakika & Güncel', icerik='Genel derleme akışı (T1–T5 ile çakışanlar elenerek yalnızca eksik kalan başlıklar alınır).', hedef='', siklik=None),
    'onedio': dict(birim='Popüler Kültür & Gençlik Platformu', akis='Gündem & Popüler Kültür', icerik='Sosyal medya trendleri, dizi/sinema popüler kültür başlıkları ve gençlik gündemi.', hedef='', siklik=None),
}

# hatalı kaynakların çekim günlüğü (görüntüle çekmecesi; yoksa 403 kalıbı)
HATA_LOG = {
    "defense-news": [("hata", "16.00.20", "403 Forbidden · 2. deneme · sonraki deneme 18.00"), ("hata", "14.00.18", "403 Forbidden"), ("bilgi", "12.00.11", "4 yeni içerik, 2 tekrar elendi")],
    "rekabet": [("hata", "16.00.41", "Haber listesi bulunamadı: seçici eşleşmedi (sayfa yapısı değişmiş olabilir)"), ("hata", "15.00.39", "Haber listesi bulunamadı: seçici eşleşmedi"), ("hata", "14.00.40", "Haber listesi bulunamadı: seçici eşleşmedi"), ("bilgi", "13.00.37", "2 yeni içerik")],
    "ensonhaber": [("hata", "09.00.06", "XML ayrıştırılamadı: 214. satırda kapanmamış öğe"), ("bilgi", "22.11 · 09.00.05", "3 yeni içerik, 1 tekrar elendi")],
}
# çekim tipleri: kayıttaki kaynak_tipleri sırasıyla (ad, ikon, kısa açıklama)
TIP = {
    "rss": ("RSS", "fa-rss", "Akış adresi"),
    "scraper": ("Kazıyıcı", "fa-spider", "Sayfa düzenli taranır"),
    "veri-akisi": ("Veri Akışı", "fa-chart-line", "Bülten ya da veri takvimi"),
    "sosyal-hesap": ("Sosyal Hesap", "fa-hashtag", "X, Telegram ya da benzeri hesap"),
}

# ---- havuz satırları ----
# (id, başlık, öneri kategori, alt konu, 1./2./3. kaynak id, güven, görsel durumu, görsel, çekilme, düzenleme kaydı)
TASLAK = [
    ("ai-mgm-kar", "Meteoroloji'den Marmara için turuncu kod kar uyarısı", "Gündem", "İstanbul", ["afad", "aa", "dha"], 91, "kirpildi", "p183", "23.11.2026 15.58", "kirpildi"),
    ("ai-ab-uyelik", "AB genişleme toplantısında Türkiye'nin üyelik süreci de konuşuldu", "Dünya", "Avrupa", ["reuters", "ap", "aa"], 78, "eksik", "", "23.11.2026 15.52", "eksik"),
    ("ai-benzin", "Benzinde indirim beklentisi: pompaya yansıması hafta sonunu bulabilir", "Finans", "Enerji", ["x-ekonomi"], 62, "temiz", "p192", "23.11.2026 09.04", "temiz"),
    ("ai-atama", "Resmî Gazete'de bugün: 14 atama kararı yayımlandı", "Gündem", "Siyaset", ["resmi-gazete"], 95, "eksik", "", "23.11.2026 15.40", "eksik"),
    ("ai-ida", "Savunma Sanayii Başkanlığı yeni insansız deniz aracı projesini duyurdu", "Savunma", "Deniz Platformları", ["ssb", "aselsan"], 89, "temiz", "p195", "23.11.2026 15.31", "kirpildi"),
    ("ai-kap-birlesme", "KAP: iki enerji şirketinden birleşme görüşmesi açıklaması", "Finans", "Şirketler", ["kap", "aa"], 86, "eksik", "", "23.11.2026 15.24", "eksik"),
    ("ai-fed-dolar", "Fed tutanakları sonrası küresel piyasalarda dolar geriledi", "Finans", "Dünya Ekonomisi", ["reuters", "afp"], 83, "kirpildi", "p188", "23.11.2026 15.20", "kirpildi"),
    ("ai-meb-ara-tatil", "Millî Eğitim Bakanlığı: ara tatil takvimi değişmedi", "Kampüs", "Eğitim ve Sınavlar", ["meb", "iha"], 93, "temiz", "p163", "23.11.2026 15.12", "kirpildi"),
    ("ai-kar-koy", "Doğu Anadolu'da kar: 214 köy yolu ulaşıma kapandı", "Gündem", "Çevre ve Afet", ["aa", "dha", "iha"], 90, "kirpildi", "p178", "23.11.2026 15.05", "kirpildi"),
    ("ai-g20-tarim", "G20 tarım bakanları gıda güvenliği bildirisi yayımladı", "Dünya", "Uluslararası Kuruluşlar", ["ap"], 71, "temiz", "p180", "23.11.2026 14.48", "kirpildi"),
    ("ai-fahis-fiyat", "Ticaret Bakanlığı fahiş fiyat denetiminde 1.240 işletmeye ceza kesti", "Finans", "Türkiye Ekonomisi", ["ticaret", "aa"], 88, "temiz", "p158", "23.11.2026 14.40", "kirpildi"),
    ("ai-sarj-agi", "Yerli elektrikli otomobil için yeni şarj ağı anlaşması imzalandı", "Finans", "Otomotiv", ["webtekno"], 58, "temiz", "p193", "23.11.2026 09.02", "temiz"),
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
    ("ai-red-kripto", "Kripto parada büyük çöküş iddiası", "Finans", "Kişisel Finans", ["x-ekonomi"], 41, "", "eksik", "23.11.2026 09.04", "Teyitsiz: tek kaynak, T12", "Elif Aras", "reddedilen"),
    ("ai-red-saat", "Akıllı saatlerde yüzde 40 indirim kampanyası başladı", "Keşfet", "Teknoloji", ["haberler-com"], 52, "p117", "temiz", "23.11.2026 09.02", "Reklam içerikli", "Kerem Aksoy", "reddedilen"),
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

KISA = {"afad": "AFAD", "kap": "KAP", "ssb": "SSB", "meb": "MEB", "ticaret": "Ticaret Bakanlığı", "dha": "DHA", "iha": "İHA",
        "aa": "AA", "aa-ekonomi": "AA Ekonomi", "resmi-gazete": "Resmî Gazete", "ist-valilik": "İstanbul Valiliği", "aselsan": "ASELSAN",
        "ap": "AP", "afp": "AFP", "x-ekonomi": "X · Ekonomi Uzmanları", "webtekno": "Webtekno", "haberler-com": "Haberler.com",
        "defense-news": "Defense News", "tuik": "TÜİK", "anka": "ANKA"}
