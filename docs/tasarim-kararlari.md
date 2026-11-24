# Dada Haber Yönetim Paneli — Tasarım Kararları

> Beyar'ın verdiği her karar buraya yazılır. Sonraki işlerde esas bu dosyadır: burada yazan yeniden sorulmaz, burada olmayan verilmiş sayılmaz.
> Kurallar ve çalışma sırası `CLAUDE.md`'de, ekran listesi `docs/modul-envanteri.md`'de, anlık durum `tasks/durum.md`'dedir.
> Tarih ve saat biçimi: `24.11.2026 14.30`.

## 1 · Keşif kararları (K1–K19)

Keşif onaylandı (Beyar, 24.11.2026). **K1, K3, K7 ve K16 Yasin Bey'e de soruldu**; aşağıdakiler Beyar'ın kararıdır ve geçerlidir. Yasin Bey farklı cevap verirse güncellenir; bu dört karar `moduller.json`'da tek bir ayar değiştirilerek geri alınabilecek şekilde kurulur (envanter §11 "Yasin Bey'e bağlı ayarlar").

| Kod | Karar | Yasin Bey'e soruldu | Tarih |
|---|---|---|---|
| K1 | Anket, Terimler Sözlüğü ve Firma Rehberi modül kaydında durur ama **kapalı** gelir; ekranı şimdi üretilmez. | evet | 24.11.2026 |
| K2 | Envanterde önerilen yerler kabul (Canlı anlatım, Dada Bağlam, Günün 5'i, Dada Doğrula Haberler modülünde; köşe yazısı, röportaj, Farklı Bakışlar haber formunda "tür"; okur formları tek gelen kutusunda). **Tek fark:** kurumsal metinler (Hakkımızda, İletişim, Yardım, Reklam, İnsan Kaynakları) Yasal modülünde değil, ayrı bir **"Sayfalar"** ekranında. | | 24.11.2026 |
| K3 | Yan menü taslağı kabul. Grup başlıkları **katlanabilir**; içinde bulunulan grup hep açık kalır; açık ve kapalı durumu hatırlanır. | evet | 24.11.2026 |
| K4 | Yorumları **editörler** yönetir. Altı rol kayıtta tanımlı kalır; prototipte rol değiştiricide şimdilik **Süper Admin ve Editör** gösterilir. "Ses (muhabir)" rolü yok. | | 24.11.2026 |
| K5 | Rol, **izin gruplarından** oluşur; alan ve kutu görünürlüğü de aynı yerden yönetilir. | | 24.11.2026 |
| K6 | AI havuzunda **üç sekme**: Taslak, Yayınlanan, Reddedilen. "Görsel eksik" gibi durumlar sekme değil, satırda etiket ve süzgeç. | | 24.11.2026 |
| K7 | Kaynak grupları **T1–T4** (yeni doküman). Haber siteleri ve sosyal medya hesapları dahil her tür kaynak eklenebilir. Üzerinde başkasının logosu ya da damgası olan görsel ve video kullanılmaz; bunu **kaynak başına medya izni** ayarı yönetir; izin kapalıysa haber "Görsel eksik" olarak gelir. | evet | 24.11.2026 |
| K8 | Otomatik yayın ayarında **güven eşiği** ve **sayısı ayarlanabilir güvenlik koşulları** bulunur. Her AI haberinde **1., 2., 3. kaynak** görünür: hem teyit için hem aynı haberin iki kez çekilmediğini göstermek için. | | 24.11.2026 |
| K9 | Sosyal platformlar: **X, Facebook, LinkedIn, Instagram, Telegram**. Diğerleri kayıtta kapalı. | | 24.11.2026 |
| K10 | Her haberin bir **ana kategorisi ve alt konusu zorunlu** (adres ve SEO ona göre); isteğe bağlı olarak ek kategori ve alt konulara da bağlanabilir. | | 24.11.2026 |
| K11 | Çöp **her listede aynı yerde bir sekmedir**; merkezî çöp ekranı yok. Silen kişi çöpten kalıcı olarak da silebilir, ikinci onayla. **Bakım modu Site Ayarları'nda.** | | 24.11.2026 |
| K12 | Panel, public sözlüğü (`dadahaber-prototip/araclar/ornek_veri.json`) yalnızca okur; panele özgü alanlar bu depoda **ek sözlükte** durur. | | 24.11.2026 |
| K13 | Menü üretimi **karma**: betik menü HTML'ini yazar, JS etkin kalemi ve rolü işaretler. | | 24.11.2026 |
| K14 | Mobil görsel ölçüleri **sitenin telefon görünümünden** türetilir; ölçüler modül kaydında. | | 24.11.2026 |
| K15 | Doğrulama (2FA) **e-posta koduyla**. Şimdilik girişte Süper Admin dışındaki kullanıcılara sorulur; ayrıca **bakım modunu açarken** ve **otomatik yayın ayarını değiştirirken**. | | 24.11.2026 |
| K16 | Vitrin yönetimi **yalnızca manşeti** kapsar (manşet haberleri ve yanındaki kartlar, sürükle-bırak). Ana sayfanın geri kalanı sabit düzende, kendiliğinden dolar. | evet | 24.11.2026 |
| K17 | `docs/referans/referans-09.png` yanlış dosya, yok sayılır. | | 24.11.2026 |
| K18 | Panel teması kabuk aşamasında önizlemeyle seçtirilir. | | 24.11.2026 |
| K19 | Depo **herkese açık** olacak; git kurulumu ve her commit, push yine Beyar'ın onayıyla. | | 24.11.2026 |

**Uygulama notları (yorum değil, kararların bu depodaki karşılığı):**
- K15 + CLAUDE.md: e-posta kodu istenen işlemler = CLAUDE.md'deki hassas işlemler (rol değişikliği, API anahtarı, toplu silme) + K15'teki iki işlem.
- K2: "Sayfalar" ekranı envanterde K9 modülü olarak yazıldı; menüdeki yeri (Sistem grubu) öneridir, yayılımda teyit edilecek.

## 2 · Genel kurallar (CLAUDE.md, Beyar · 24.11.2026)

Bu kurallar `CLAUDE.md`'dedir; burada yalnızca karar defterinde iz bıraksın diye anılır:
- **Tema:** projeden projeye yalnızca renk ve logo değişir. Yazı tipi, köşe yuvarlaklığı, boşluk ölçeği ve bileşen dili panelin kendisine aittir (referans kabuk + Dada Gastro paneli). Public sitenin yazı tipi ve köşe değerleri panele taşınmaz. Tema dosyası yalnızca renk ve logo taşır.
- **Çalışma sırası:** keşif → kabuk (yan menü, üst bar, rol değiştirici, Kontrol Paneli) → pilot modül Haberler → Site Ayarları → dondurma ve UI kit → yayılım.
- **Tutarlılık:** aynı iş her modülde aynı yerde ve aynı görünümde; liste satırında görüntüle, düzenle, sil + "diğer" menüsü; sayfa/çekmece/pencere kuralı pilot modülde bir kez seçilir.

## 3 · Kabuk kararları

| Parça | Seçilen | Kaynak / önizleme | Tarih |
|---|---|---|---|
| Menü grubu adı (katman 4) | **Özel Widgetlar** (eski adı "Özel Dikeyler"). Beyar kabuk onayında yeniden soracak; değişebilir. Yalnızca `moduller.json`'daki grup ve modül adı değişir | `moduller.json` | 24.11.2026 |
| Kabuk onayı | **Kabuk kilitlendi** (yan menü, üst bar, rol değiştirici, bildirim paneli, genel arama, Kontrol Paneli; masaüstü, tablet, telefon). Beyar: "genel hataları gider, kilitleyelim" → "sen bildiğin gibi yap, modüllere geç". Bundan sonra kabuğa yalnızca Beyar onayıyla dokunulur; açık kalan tek kalem menü grubu adı ("Özel Widgetlar", yeniden sorulacak) | `moduller/kontrol-paneli/index.html` | 24.11.2026 |
| S2 · Menünün daraltılmış hali | **A · İkon şeridi** (76px): menü kenarındaki sekmeyle daralır; logo yerine işaret, kalem adları üstüne gelince ipucu olarak, rozetler ikonun köşesinde, grup başlıkları ince çizgi. Dar/açık hal hatırlanır, sayfa geçişlerinde menü sıçramaz, kaydırma yeri korunur (Beyar düzeltmesi) | `secenekler/kabuk-daraltma.html` · `moduller.json` → `menu.daraltma: ikon` | 24.11.2026 |
| KURAL · üstüne gelme (ikincil kontroller) | **Bütün ikincil kontroller üstüne gelince üst bardaki çan gibi tepki verir:** kehribar çerçeve, koyu kehribar yazı ve ikon; zemin ve konum değişmez. Kapsam: çerçeveli düğme ("Rapor indir" gibi), ikon düğmesi, rol düğmesi; ileride eklenen her ikincil kontrol. Hiçbir düğme üstüne gelince yerinden oynamaz (ana ve tehlike düğmesinde yalnızca zemin koyulaşır) | Beyar ("Rapor indir" siyah çerçeveyle kötü duruyordu) | 24.11.2026 |
| S1 · Tema | **A · Koyu menü, kehribar dolu ana düğme (koyu yazı); etkin menü kalemi kehribar zemin, koyu yazı ve ikon.** Yasin Bey seçti (Beyar önce B demişti). Düzeltme (Beyar): üstüne gelinen kalemin yazısı silikleşmez, ikonla aynı netlikte; etkin kalemin ikonu kehribar zeminde görünür (koyu) | `secenekler/kabuk-tema.html` · `tema/dadahaber.css` | 24.11.2026 |

## 4 · CC'nin verdiği küçük seçimler (Beyar gözden geçirecek)

| Konu | Seçim | Neden |
|---|---|---|
| Yazı tipi dosyaları | Referans kabuğun Gilroy dosyaları (`dadamutfak/v7-6cu356/assets/fonts`: Light, Medium, ExtraBold) panelin `assets/font/` klasörüne alınır | CLAUDE.md: yazı tipi referans kabuktan gelir. Referans kabuk yalnızca Medium yüklüyor ve kalın yazıyı tarayıcıya yapay çizdiriyor; ExtraBold dosyası da yüklenerek bu düzeltildi |
| Logo | İşaret (konuşma balonu "dada!") resmî SVG'den: `dadahaber-app/module/gen/assets/icons/ic_logo_dada_haber.svg`. Tam logo (işaret + "dadahaber" yazısı) için SVG bulunamadı; şimdilik public sitenin PNG'si kullanılır | CLAUDE.md "logo SVG ya da FA" diyor; tam logo SVG'si açık kalem (`tasks/durum.md`) |
| Sınıf adları | Referans kabuğun sınıf adları korunur (`sa-menu`, `sa-mlink`, `pnl-top`, `pnl-card`, `kpi-*`, `pstat` …); yeni parçalar `kb-*` ön ekiyle | Referans "birebir"; Dada Gastro'nun Laravel paneli de aynı adları kullanıyor, full-stack aktarımı kolaylaşır |
| Değişken adları | Referans kabuğun anlamsal adları korunur (`--acc`, `--ink`, `--line`, `--paper`, `--bg`, `--muted`); renge göre adlandırılmış olanlar anlama çevrildi (`--tomato` → `--danger`, `--green` → `--ok`) | Tema her projede değişeceği için renk adı yerine anlam |
| Dosya düzeni | `tema/` (yalnızca renk ve logo) · `cekirdek/css`, `cekirdek/js` (kabuk) · `moduller/<id>/` (modül sayfaları) · `moduller.json` (kayıt) · `veri/panel.json` (ek sözlük, K12) · `araclar/menu_yaz.py` (menü ve üst bar üretici) | Modül sözleşmesi |
| Henüz üretilmemiş ekranlar | Menü ve bağlantılar tek bir "yapım aşamasında" sayfasına (`cekirdek/yakinda.html?s=modul.sayfa`) gider | Kırık bağlantı olmaz; sayfa üretilince kayıtta `hazir:true` yapılır, bağlantılar kendiliğinden gerçek sayfaya döner |
| Kırılımlar | 1024 (çekmece menü) ve 640 (telefon); referanstaki 980 yerine | CLAUDE.md |

