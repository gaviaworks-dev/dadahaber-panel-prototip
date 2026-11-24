# Dada Haber Yönetim Paneli · Modül Envanteri (keşif, onay bekliyor)

Tarih: 24.11.2026 · Durum: **keşif onaylandı (Beyar, 24.11.2026); K1–K19 kararları işlendi** (metinleri `docs/tasarim-kararlari.md` §1). Kararla kapanan yerler "(K#)" ile işaretli. Hâlâ öneri olan yerler (rol dağılımının ayrıntısı, `moduller.json` alan adları, Sayfalar modülünün menüdeki yeri) açıkça "öneri" yazar.
K1, K3, K7 ve K16 Yasin Bey'e de soruldu; cevabı farklı gelirse yalnızca kayıttaki bir ayar değişecek şekilde kurulur (§11 "Yasin Bey'e bağlı ayarlar").

## 0 · Okunan kaynaklar

| Kaynak | Yer | Ne aldım |
|---|---|---|
| Çekirdek spesifikasyon (PDF, 3 sayfa) | `docs/kaynak/Yönetim Paneli … Spesifikasyonu.pdf` | 8 zorunlu modül, güvenlik standartları (maskeleme, ikinci onay, soft delete, before/after audit, rol yükseltme sınırı, rate limit) |
| Dada Haber mimarisi (PDF, 5 sayfa) | `docs/kaynak/Dada Haber — Kapsamlı … Mimarisi.pdf` | 8 katman ve alt modüller; 2.1 bölümü yok, 2.2 iki kez yazılmış |
| Akışlar, mimari, kararlar | `docs/kaynak/DADAHABER-02/03/05` | E1–E5 editör ve yönetici akışları, K1–K4 kaynak kademeleri, kavramsal veri modeli, V-01…V-24 ve B-01…B-28 |
| Milli Müdafaa ekranları (15) | `docs/referans/referans-01…15.png` | İşlev referansı: Otomatik Haberler listesi, haber düzenleme (4 sekme), Kaynaklar, Frekans, Cron Sağlık, Sosyal Hesaplar, kırpma penceresi. referans-09 yanlış dosya, yok sayılır (K17) |
| Referans kabuk | `~/Developer/Projects/dadamutfak/v7-6cu356/sa-shell.html` (= `By4r/dadamutfak-view` deposu; `~/Revenge/dump/dadamutfak-view` yalnızca tek dosya içeriyor) | Kabuk iskeleti, menü üretimi, bileşen sınıfları, belirteçler. Rail'siz kardeş kabuk: `panel-shell.html` |
| Dada Gastro paneli | `~/Developer/Backend Projects/dadagastro/` (Laravel 12, Blade) · kanon ekran `resources/views/admin/puf-noktalari/{index,form}.blade.php` | Liste ve form standardı. Ayrı bir standart dokümanı yok; standart kanon ekranların kodunda |
| Public site | `~/Developer/Projects/dadahaber-prototip/` (yalnızca okundu) | `docs/sayfa-envanteri.md` (274 sayfa), `docs/tasarim-kararlari.md`, `araclar/ornek_veri.json` (2062 haber, 36 yazar, 9 bölüm, 235 alt konu), `assets/css/degiskenler.css`, `CLAUDE.md`, `tasks/durum.md`, `araclar/`, `tasks/araclar/` |

## 1 · Kaynaklardan çıkan temel gözlemler

**Referans kabuk (DadaMutfak V7 `sa-shell`)**
- İskelet: `.sa-app` > `aside.sa-rail` (76px) > `nav.sa-menu` (264px, JS doldurur) > `.sa-divider` (daraltma tutamağı) > `header.pnl-top` (64px) > `main.pnl-main`. Hepsi `position:fixed`.
- Menü `sa-shell.js` içindeki `SECTIONS` nesnesinden üretilir: bölüm `{eyebrow, title, menu:[]}`, kalem `{ic, lbl, href, screen, cnt, soon}`, grup başlığı `{seclbl}`. Etkin kalem `body[data-screen]` ile bulunur. Menü tek seviyelidir.
- **Rail'i kaldırmanın etkisi:** referansta menü yalnızca o anki bölümü gösterir; bölümler arası geçiş ve logo rail'dedir. Rail'siz panelde menü **bütün grupları birlikte** taşımalı, logo menü başına gelmeli, `--sa-side-w` (340px sabit) yeniden hesaplanmalı, daraltma "ikon modu"na dönmeli. `panel-shell.html` bu yapının rail'siz örneğidir.
- Rol: `?role=` → `localStorage` → `super`. Rol yalnızca menüyü değiştiriyor, sayfa içeriği görünmeye devam ediyor (bizde ekran, kutu ve alan düzeyinde gizlenmeli).
- Bileşen sınıfları: `.pnl-page-head/.ph-sub/.ph-actions`, `.pnl-card/.pc-*`, `.kpi-*`, `.pstat.ok|wait|off|warm`, `.pnl-empty`, `.btn(-acc|-ghost|-sm|-danger)`, `saConfirm()`, `saToast()`, `.ptable/.row-acts/.ia-btn`, `.filter-bar/.chips/.chip.is-on/.ch-cnt`, `.pager`, `.form-layout/.form-sec/.frow/.finput/.fselect/.ftext`, `.side-card`, `.ms-field` (çoklu seçim).
- Eksikler: toplu işlem, sütun sıralama, yükleniyor/iskelet, hata durumu, alan doğrulama, gerçek giriş ekranı (giriş sayfası yalnızca rol seçici), özel tarih seçici (yerel `type=date`). Tablo/filtre CSS'i 35 sayfaya kopyalanmış ve kopyalar birbirinden farklı; birkaç sabit renk var; kırılım 980/640.

**Dada Gastro form ve liste standardı (emsal)**
- Liste: başlık + sağ üstte "Yeni …" · tek kart içinde arama + durum çipleri (sayaçlı) · tablo (ilk sütun küçük görsel + ad + alt bilgi, sonda sağa yaslı ikon düğmeler) · sayfalama "N sonuçtan a–b" · boş durum "Filtreyi Temizle".
- Form: iki sütun (içerik + 280–360px yapışkan yan panel: Durum, Yayın tarihi, SEO skoru) · `.form-sec` grupları · tek `lang-tabs` bütün sekmeleri sarar (bizim "tek dil seçici" kuralına yakın) · sekme hata noktası `.has-error` · TinyMCE 7.9.3 · Cropper.js 1.6.2 ile alan sözleşmeli kırpma (`config/admin_images.php`).
- **CLAUDE.md kurallarıyla çelişen yerler** (bizde kural geçerli): satır tıklama yok · yerel tarih, telefon ve e-posta alanı · aranabilir açılır liste yok · zorunlu alan işareti yok · kaydet çubuğu yapışkan değil, kaydedilmemiş değişiklik uyarısı yok · toplu işlem standart değil.

**Milli Müdafaa ekranları (neyin olması gerektiği)**
- Otomatik Haberler: üstte aylık maliyet kutusu; sekmeler Bekleyenler / Taslak / Reddedilen / Yayınlanan (sayaçlı); Bölüm süzgeci; Toplu Onayla / Toplu Reddet; satırda ID, görsel, başlık + kaynak + tier, AI kategori önerisi + yazar, güven skoru, çekilme tarihi, durum (Görsel Eksik, Editör Onayı Bekliyor).
- Düzenleme: üst bilgi şeridi (Durum, Güven Skoru, Çekilme, Kaynak, Kaynak URL, AI Modeli); sekmeler Detay · SEO Bilgileri · Bildirim Ayarları · Sosyal Medya; alt çubukta Manşet, Bildirim Gönder anahtarları + Reddet / Taslağa Kaydet / Onayla ve Yayınla. **Dil sekmeleri her bölümde ayrı ayrı tekrarlanıyor**; bizde formun üstünde tek dil seçici olacak.
- Bildirim: başlık 60, içerik 150 karakter sayacı ("Firebase önerilen max"), bildirim görseli anahtarı, isteğe bağlı gönderim tarihi.
- Sosyal Medya sekmesi: platform sekmeleri, platform metni, karakter çubuğu + URL ve emoji sayacı, oran düğmeleri (X 16:9 1200×675 · 1:1 1080×1080 · Serbest; FB 1.91:1 1200×630; IG 1:1, 4:5 1080×1350), yakınlaştırma çubuğu ve sıfırla, hesap kutusu, Hemen Yayınla / Zamanlı Paylaş, canlı önizleme, Hemen Üret / Yeniden Üret, Hazır/Onaylı/Yayında sayaçları.
- Kaynaklar: Tier, Tip, Aktif, Görsel süzgeçleri + canlı arama; toplu Aktif Yap / Pasif Yap / Sil; sütunlar ID, Tier, Başlık + slug, Tip (RSS/Scraper), URL, Görsel izni, Aktif, Son fetch, Başarı/Hata.
- Frekans: tier başına sıklık (sayı + saat/gün), kaynak sayısı, aylık tahmin (fetch, haber, $), aktif anahtarı; üstte aylık maliyet projeksiyonu.
- Cron Sağlık: Crontab, Lock, Aktif kaynak kullanımı, Genel sağlık kutuları; `image_allowed=0` uyarı bandı; Tier durumu tablosu (frekans, aktif, beklenen/gün, gerçek/24s, kullanılan); Manuel Tetikle, Yenile.
- Sosyal Hesaplar: platform sekmeleri (X, Facebook, LinkedIn, Instagram, Telegram), dil bazlı hesap (X TR, X EN), bağlantı durumu, aktif anahtarı, Hesabı Bağla, Yeni Hesap Ekle, "Teknik detaylar".
- Kırpma (İsmail Turgut Öksüz paneli): tek oran, sürüklenebilir çerçeve, Vazgeç / Kırpmadan Kullan / Kırp ve Kullan. Başlangıç noktası; bizde web + mobil, odak noktası ve çoklu önizleme eklenecek.

**Public site**
- 8 ana başlık (Gündem, Spor, Finans, Kadın, Savunma, Dünya, Kampüs, Keşfet) + Köşe; 235 alt konu; 36 yazar (bölüm başına 4).
- Site arayüzünde "Teyitli" etiketi ve kaynak sayısı **gösterilmiyor** (Beyar kararı); teyit veride tutuluyor. Panel bu bilgiyi göstermeli (kaynak teyitleri paneli).
- Görsel oranları (site CSS'inden): kart 16:10, detay kapağı 2.4:1, video 16:9, Akış 9:16, infografik 3:4, Foto Fokus kolajı 4:3, podcast kapağı 1:1, yazar fotoğrafı 1:1 (daire), bir yerde 21:9 ve 4:5.
- Marka: kehribar `#FCB623` (açık zeminde metin `#7A5F01`), FA 6.5.2 solid, kırılım 640/1024. **Panele yalnızca renk ve logo taşınır**; sitenin yazı tipi (Gilroy dosyaları, 300/500/800) ve köşe değerleri taşınmaz, panelinkiler referans kabuk ve Gastro panelinden gelir (CLAUDE.md "Referans kabuk"). Değişkenler Türkçe adlı (`--marka`, `--gri-*`, `--k-kontrol` …). Logo yalnızca PNG; SVG sürümü sitede de açık kalem.

## 2 · Gösterim kuralları

- **Ekran türü:** L liste · D düzenleme/form · A ayar · R rapor/pano · P açılır pencere ya da çekmece · S tek başına sayfa (giriş akışı, hata).
- **Rol kısaltmaları:** SA Süper Admin · GYY Genel Yayın Yönetmeni · ED Editör · KE Spor/Kategori Editörü · SM Sosyal Medya Uzmanı · AN Analist. ● tam · ◐ kısıtlı (salt okunur ya da kendi kapsamı) · — görmez. **Rol dağılımı öneridir**; kesinleşen: yorumları editörler yönetir, rol değiştiricide şimdilik SA ve ED (K4).
- **Sayım:** her ekran bir kez sayılır; aynı ekranın masaüstü, tablet ve telefon hali ayrıca sayılmaz (her ekran üç genişlikte üretilecek). Sekmeler ayrı ekran sayılmaz.
- Paylaşılan pencereler (onay diyaloğu, e-posta kodu doğrulaması, medya seçici, kırpma) bileşendir; modüllerde tekrar sayılmaz.
- **"P (çekmece)", "P" ve "D" etiketleri şimdilik yalnızca sayım içindir.** Hangi işin sayfada, hangisinin çekmecede, hangisinin pencerede yapılacağı pilot modülde (Haberler) bir kez seçtirilir, UI kitteki etkileşim sözleşmesine yazılır ve bütün modüllere aynı biçimde uygulanır (CLAUDE.md "Tutarlılık").
- **Liste satırı eylemleri her listede aynıdır:** görüntüle, düzenle, sil; aynı sırada, aynı ikonla. Aşağıdaki tablolarda "satırda …" diye geçen modüle özgü eylemler (onayla, yeniden gönder, yeniden dene, bağla vb.) satıra dağınık düğme olarak değil, aynı "diğer" menüsünün içinde durur.

---

## 3 · Çekirdek modüller (her projede aynen)

### K0 · Kabuk ve Oturum (Kimlik ve Yetki modülünün giriş tarafı)

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Kabuk: yan menü + üst bar | parça | Menü `moduller.json`'dan üretilir; logo menü başında; daraltınca ikon modu; ≤1024 çekmece |
| 2 | Genel arama | P | Haber, kullanıcı, kaynak, ayar ve ekranlarda arama; klavye kısayolu |
| 3 | Bildirim paneli | P | Sistem uyarıları (cron, entegrasyon hatası), AI kuyruk, okur bildirimleri; okunmuş/okunmamış |
| 4 | Hesap menüsü | P | Profil, aktif oturumlar, dil, çıkış |
| 5 | Rol değiştirici (prototip) | P | Şimdilik Süper Admin ve Editör (K4); altı rol kayıtta tanımlı. Seçilen role göre menü, kutu ve alanlar gizlenir |
| 6 | Giriş | S | Örnek bilgilerle dolu, "Beni hatırla" işaretli; tek tık "Giriş Yap" |
| 7 | 2FA doğrulama | S | E-posta koduyla (K15). Şimdilik Süper Admin dışındaki kullanıcılara girişte sorulur; "Bu cihazı hatırla" |
| 8 | Şifremi unuttum | S | E-posta alanı (yazarken doğrulama) |
| 9 | Bağlantı gönderildi | S | |
| 10 | Yeni şifre belirle | S | Şifre kuralı göstergesi |
| 11 | Bağlantı geçersiz / süresi doldu | S | Davet ve şifre bağlantıları için ortak |
| 12 | Davet ve e-posta onayı | S | Onay bağlantısından gelen karşılama |
| 13 | İlk şifre belirleme | S | Davetli kullanıcı |
| 14 | 2FA kurulumu | S | İlk girişte e-posta adresine kod gider ve doğrulanır (K15) |
| 15 | Davet e-postası önizlemesi | S | Gönderilen e-postanın görünümü |
| 16 | Hassas işlem doğrulaması | P | E-posta kodu: rol değişikliği, API anahtarı, toplu silme (CLAUDE.md) + bakım modunu açma, otomatik yayın ayarını değiştirme (K15) |
| 17 | Profilim | D | Ad, fotoğraf (kırpma), e-posta, telefon (maske), şifre, 2FA, arayüz dili |
| 18 | Yetki yok (403) | S | |
| 19 | Sayfa bulunamadı (404) | S | Kapatılmış modülün eski adresi buraya düşer |
| 20 | Oturum düştü | P | Bilgiler dolu, tek tık yeniden giriş |

- **Roller:** hepsi (giriş akışı herkes için aynı).
- **Sitedeki karşılığı:** yok (panel içi). Site üyelik akışı (`giris.html`, `sifremi-unuttum.html`, `eposta-dogrula.html`) okur içindir; panel ekipten ayrıdır.

### K1 · Kimlik ve Yetki

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Roller | L | Rol adı, seviye, kullanıcı sayısı, son değişiklik |
| 2 | Rol düzenle | D | Rol izin gruplarından oluşur (K5): grup seçimi, seviye, kapsam (Spor/Kategori Editörü için kategori sınırı); açılan izinlerin özeti |
| 3 | İzin grupları | L | Grup adı, içerdiği izin sayısı, kullanan roller |
| 4 | İzin grubu düzenle | D | Sekmeler: İşlem izinleri (`kaynak:aksiyon`, ör. `haberler:yayinla`, `kaynaklar:yonet`) · Alan ve kutu görünürlüğü (ör. maliyet ve token, cron ve sistem sağlığı). İkisi aynı yerden yönetilir (K5) |
| 5 | Aktif oturumlar ve hatırlanan cihazlar | L | Kendi oturumları; SA herkesinkini görür; tek tek ya da toplu kapat |
| 6 | Güvenlik politikası | A | 2FA zorunlu (kapatılamaz), hatırlanan cihaz süresi, hassas işlem listesi, oturum zaman aşımı, şifre kuralı |
| 7 | Rol atama onayı | P | Önce/sonra, "kendi seviyenin üstünde rol atanamaz" engeli, 2FA |

- **Bileşenler:** veri tablosu, izin matrisi, anahtar, aranabilir açılır liste, onay diyaloğu, 2FA doğrulama.
- **Roller:** SA ● · GYY ◐ (salt okunur) · diğerleri — (kendi oturumları Profilim üzerinden).
- **Sitede:** yok.

### K2 · Kullanıcılar

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Ekip | L | Ad, rol, durum (aktif/askıda/yasaklı), **doğrulama (bekliyor / onaylandı / süresi doldu)**, 2FA, son giriş; satırda "Onay e-postasını yeniden gönder" |
| 2 | Ekip üyesi davet et | D | Ad, e-posta, telefon, rol (kendi seviyesine kadar), kapsam |
| 3 | Ekip üyesi detayı | D | Rol, durum, doğrulama, oturumlar, 2FA sıfırla, şifre sıfırlama tetikle, iç notlar, denetim izinden son işlemleri |
| 4 | Üyeler (okurlar) | L | Sunucu taraflı sayfalı; ID, e-posta, telefon, durum, kayıt tarihi, giriş yöntemi, etiket |
| 5 | Üye detayı | D | Durum, manuel e-posta/telefon doğrulama, şifre sıfırlama, tercihler, takip ettikleri, bülten abonelikleri, yorumları, yasal onay kayıtları, iç not |
| 6 | Durum değiştir | P | Gerekçe zorunlu; denetim izine önce/sonra |

- **Bileşenler:** veri tablosu, toplu işlem, telefon ve e-posta alanı, durum rozetleri, sekmeli düzenleme, onay diyaloğu.
- **Roller:** SA ● · GYY ◐ (üyeler) · diğerleri —.
- **Sitede:** `uye-ol.html`, `giris.html`, Hesabım (15 sayfa: takip, kaydedilenler, bildirim, bülten, güvenlik, gizlilik, hesap silme).

### K3 · Site Ayarları ve Özellik Anahtarları (çalışma sırası 4 · ikinci kalıp)

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Site ayarları | A | Sekmeler: Kimlik ve logo · İletişim ve sosyal bağlantılar (8 hesap: Instagram, YouTube, X, Facebook, LinkedIn, TikTok, WhatsApp kanalı, RSS) · SEO varsayılanları · Diller (TR açık; EN, AR, DE "sonraki aşama") · Sistem limitleri · Aile siteleri ve footer · **Bakım modu** (K11) |
| 2 | Özellik anahtarları | A | Modül ve özellik anahtarları (ör. Dada'ya Sor, Spiker, Haber Dinle, yorumlar, Günün Serisi), açıklama, son değiştiren; kayıtta "önbellek yenilendi" |
| 3 | Anahtar değişikliği onayı | P | Önce/sonra, etkilenen sayfalar |
| 4 | Bakım modunu aç | P | Okur mesajı, izinli IP'ler, önce/sonra; e-posta kodu (K15) |

- **Bileşenler:** sekmeli ayar sayfası, anahtar, form alanları, logo yükleme, kaydet çubuğu, onay diyaloğu, toast.
- **Roller:** SA ● · GYY ◐ (SEO ve iletişim) · diğerleri —.
- **Sitede:** footer, sosyal ikonlar, aile siteleri bandı, dil seçici, çerez bandı, `bakim.html` (503).
- Bakım modu Site Ayarları'ndadır (K11; Dada PDF'i ile aynı).

### K4 · Denetim İzi ve Sistem Logları

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Denetim izi | L | Zaman, kişi, işlem, varlık, IP, request_id; süzgeç; "otomatik yayımlandı" işareti; silinemez (yalnızca okunur) |
| 2 | Denetim kaydı | P | Önce/sonra fark görünümü |
| 3 | Sistem logları | L | Seviye (bilgi/uyarı/hata), kaynak (kuyruk, cron, API, AI, sosyal), tarih |
| 4 | Log kaydı | P | Mesaj, yığın izi, yeniden dene (varsa) |

- **Bileşenler:** veri tablosu, tarih aralığı seçici, fark görünümü, log görüntüleyici, durum rozetleri.
- **Roller:** SA ● · GYY ◐ (denetim izi) · AN ◐ (denetim izi, kişisel veri maskeli) · diğerleri —.
- **Sitede:** yok (yalnızca `duzeltme-politikasi.html` düzeltme kayıtları denetim izinden beslenebilir).

### K5 · Raporlama ve Dışa Aktarım

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Raporlar | R | Sekmeler: İçerik · Kategori · Yazar · Kaynak · Sosyal medya · Bildirim; tarih aralığı, kırılımlar, özet metrik + detay tablosu |
| 2 | Dışa aktarımlar | L | Hazırlanıyor / hazır / süresi doldu; indir |
| 3 | Dışa aktarım başlat | P | CSV/XLSX, alanlar, tarih aralığı; rate limit uyarısı |

- **Bileşenler:** KPI kartı, grafik, veri tablosu, tarih aralığı, ilerleme.
- **Roller:** SA ● · GYY ● · AN ● · ED ◐ (kendi içerikleri) · KE ◐ (kendi kategorisi) · SM ◐ (sosyal sekmesi). Maliyet sütunları izin grubuyla gizli.
- **Sitede:** görüntülenme sayıları (kartlarda "6,9 B").

### K6 · Yasal Metin Sürümleri

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Yasal metinler | L | Künye, Yayın İlkeleri, Düzeltme Politikası, Kullanım Koşulları, Gizlilik ve KVKK, Aydınlatma Metni, Çerez Politikası, Açık Rıza, Telif Hakları, Topluluk Kuralları, Erişilebilirlik; yayındaki sürüm |
| 2 | Metin düzenle / yeni sürüm | D | Sürüm numarası, zengin metin, yürürlük tarihi |
| 3 | Sürüm geçmişi | D | Salt okunur arşiv, iki sürüm karşılaştırma |
| 4 | Onay kayıtları | L | Kim, hangi metin, hangi sürüm, ne zaman, IP/kanal |
| 5 | Yayına alma onayı | P | Önceki sürüm arşive geçer; 2FA |

- **Bileşenler:** zengin metin, fark görünümü, veri tablosu, onay diyaloğu.
- **Roller:** SA ● · GYY ● · diğerleri —.
- **Sitede:** yasal 11 sayfa. Kurumsal metinler (Hakkımızda, İletişim, Yardım Merkezi, Reklam, İnsan Kaynakları) burada değil, K9 Sayfalar'da (K2).

### K7 · Sistem Sağlığı ve Önbellek

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Sistem sağlığı | R | Veritabanı, Redis, kuyruk/worker, dış bağlantılar, cron özeti; durum noktası, son kontrol |
| 2 | Önbellek ve rutin temizlik | A | Önbellek temizleme (genel, sayfa, görsel), rutin temizlik görevleri, son çalışma |
| 3 | Önbellek temizleme onayı | P | 2FA, rate limit |

- Bakım modu Site Ayarları'nda. Merkezî çöp ekranı yok; çöp her listede aynı yerde bir sekme (K11).
- **Bileşenler:** sağlık kutusu, durum noktası, uyarı bandı, onay diyaloğu.
- **Roller:** SA ● · diğerleri —.
- **Sitede:** dolaylı.

### K8 · Entegrasyonlar ve API Anahtarları

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Entegrasyonlar | L | Kart ızgarası: Search Console, Analytics/Tag Manager, AI sağlayıcıları, spor veri API, piyasa ve hava API, push servisi, e-posta servisi; her kartta durum, son kullanım, son hata |
| 2 | Entegrasyon ayarı | D | Yapılandırma alanları, maskeli secret, "Bağlantıyı test et" |
| 3 | API anahtarları | L | Ad, kapsam, son kullanım, oluşturan, durum; rotasyon, iptal |
| 4 | API anahtarı oluştur | P | Kapsam seçimi; anahtar **yalnızca bir kez** açık gösterilir, kopyala; 2FA |
| 5 | İptal / rotasyon onayı | P | |

- **Bileşenler:** entegrasyon kartı, maskeli gizli alan, durum rozeti, onay diyaloğu, 2FA.
- **Roller:** SA ● · diğerleri —.
- **Sitede:** dolaylı (piyasa, hava, namaz, spor verisi, analitik).

### K9 · Sayfalar (kurumsal metinler, K2)

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Sayfalar | L | Hakkımızda, İletişim, Yardım Merkezi, Reklam, İnsan Kaynakları; durum, son güncelleme; sonda Çöp sekmesi |
| 2 | Sayfa düzenle | D | Başlık, zengin metin gövde, sayfaya özgü bloklar (Yardım'da SSS, İK'da pozisyon tablosu, Reklam'da ölçü tablosu), SEO, dil seçici |

- Öneri: kurumsal sayfa her projede bulunduğu için çekirdek sayıldı; menüde Sistem grubunda Yasal Metinler'in yanında. Yeri yayılımda teyit edilecek.
- **Bileşenler:** veri tablosu, sekmeli düzenleme, zengin metin, dil seçici, SEO alanları.
- **Roller:** SA ● · GYY ●.
- **Sitede:** `hakkimizda.html`, `iletisim.html`, `yardim-merkezi.html`, `reklam.html`, `insan-kaynaklari.html`.

**Çekirdek toplamı: 59 ekran** (K0 20 · K1 7 · K2 6 · K3 4 · K4 4 · K5 3 · K6 5 · K7 3 · K8 5 · K9 2).

---

## 4 · Dada Haber modülleri

### D1 · Kontrol Paneli (çalışma sırası 2 · kabukla birlikte)

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Kontrol paneli | R | Anlık okur trafiği · en çok okunanlar · kategori ve dil dağılımı · AI taslak kuyruğu (bekleyen, görseli eksik, otomatik yayımlanan) · son dakika durumu · zamanlanmış içerik · sosyal kuyruk hataları · cron ve sistem sağlığı özeti · aylık AI maliyeti |

- Kutular izin grubuyla gizlenir: maliyet, cron ve sistem kutuları editörde görünmez. Her rol kendi kutu setini görür.
- **Bileşenler:** KPI kartı, grafik, kısa liste kartı, sağlık kutusu, durum rozeti.
- **Roller:** hepsi (kutu düzeyinde farklı).
- **Sitede:** görüntülenme sayıları, Son Dakika şeridi.

### D2 · Haberler ve Vitrin (çalışma sırası 3 · pilot modül, baştan sona)

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | **Haberler** | L | Durum sekmeleri (Tümü, Yayında, Taslak, Zamanlanmış; sonda Çöp, K11) + sayaç; süzgeç: kategori, alt konu, yazar, tür, dil, tarih; toplu işlem (kategori değiştir, yayından kaldır, çöpe at); satırda görsel, başlık + tür, kategori, yazar, durum, yayın zamanı, görüntülenme, "AI · otomatik yayımlandı" işareti. Sağ üstte: **Kategoriler**, **Etiketler**, **Yeni haber** |
| 2 | **Haber düzenle** | D | Formun üstünde tek dil seçici. Sekmeler: **Detay** (görsel web + mobil, başlık, spot, Dada Özet 15 sn / 1 dk + 3 madde, Neden önemli / Bana etkisi / Bundan sonra, gövde zengin metin, tür, ana kategori + alt konu (zorunlu; adres ve SEO buna göre) + isteğe bağlı ek kategori ve alt konular (K10), etiketler, kişi/kurum/takım, yazar, kaynaklar, ilgili haberler, Haberi dinle, yorumlar açık/kapalı) · **SEO** (otomatik başlık, açıklama, anahtar kelime, adres; sayaçlar; arama sonucu önizlemesi) · **Bildirim** (başlık ve içerik sayacı, görsel, gönderim zamanı, telefon önizlemesi; telefon ve web) · **Sosyal Medya** (platform sekmeleri, metin, sayaçlar, oran ve kırpma, hesap durumu, hemen/zamanlı, canlı kart). Yan panel: durum, yayın zamanı, manşet ve son dakika işareti, sürüm. Yapışkan kaydet çubuğu |
| 3 | Sürüm geçmişi ve düzeltmeler | P | Zaman damgalı sürümler, fark, "neyin, neden değiştiği" notu (sitede düzeltme notu ve "güncellendi" kronolojisi) |
| 4 | Kategoriler | P (çekmece) | 8 ana başlık + alt konu ağacı (235 alt konu), sıra, ikon, renk değeri, kategori sayfası SEO'su |
| 5 | Kategori düzenle | P | |
| 6 | Etiketler ve varlıklar | P (çekmece) | Konu etiketleri, kişi, kurum, takım, şehir, savunma platformu; birleştir |
| 7 | Etiket / varlık düzenle | P | |
| 8 | Yazarlar | L | 36 yazar; bölüm, unvan, yazı sayısı, durum |
| 9 | Yazar düzenle | D | Fotoğraf (1:1, kırpma), ad, unvan, bölüm, kısa biyografi, sosyal bağlantılar, köşe yazarı mı |
| 10 | Vitrin: manşet | D | Yalnızca manşet (K16): manşet haberleri (5 slayt) + yanındaki 3 kart, sürükle-bırak, canlı önizleme. Ana sayfanın geri kalanı sabit düzende kendiliğinden dolar |
| 11 | Son Dakika | L | Şerit ve sayfa tek liste; saat, kategori, başlık, durum; sırala, bitir |
| 12 | Son dakika ekle | P | Hızlı giriş: başlık, kategori, bağlı haber, bildirim gönder |
| 13 | Canlı anlatımlar | L | Dakika Dakika anlatımları: canlı / sona erdi |
| 14 | Canlı anlatım masası | D | Satır ekle (saat, metin, medya), kilit an işaretle, sabitle, anlatımı kapat |
| 15 | Olay dosyaları (Dada Bağlam) | L | Gelişen olay ve dosyalar |
| 16 | Dosya düzenle | D | Özet, kronoloji, taraflar, dosya sözlüğü, bağlı haberler |
| 17 | Günün 5'i | D | Günlük beş haber seçimi (sabah/akşam), sıralama, önizleme |
| 18 | Dada Doğrula incelemeleri | L | |
| 19 | İnceleme düzenle | D | İddia, karar etiketi, kanıtlar, kaynaklar |

- Köşe yazısı, röportaj, özel haber, araştırma, analiz, Farklı Bakışlar: ayrı ekran değil, Haber düzenle formunda **tür** seçimiyle açılan alanlar (K2).
- **Bileşenler:** veri tablosu, toplu işlem, sekmeli düzenleme, dil seçici, zengin metin, görsel alanı (web + mobil), kırpma, aranabilir açılır liste, etiket girişi, tarih-saat seçici, sayaçlı alan, SERP önizlemesi, telefon bildirim önizlemesi, sosyal kart önizlemesi, ağaç, sürükle-bırak liste, zaman çizelgesi, fark görünümü, çekmece.
- **Roller:** SA ● · GYY ● · ED ● · KE ◐ (yalnızca kendi kategorisi) · SM ◐ (okur; Sosyal Medya sekmesini düzenler) · AN ◐ (salt okunur). Vitrin ve Son Dakika: SA, GYY, ED (öneri).
- **Sitede:** bölüm ve alt konu sayfaları (123), haber detayları, `kose-yazisi.html`, `yazarlar.html`, `yazar.html`, `etiket.html`, `kisi.html`, `son-dakika.html`, `dakika-dakika*.html`, `canli*.html`, `dada-baglam*.html`, `gunun-5-i.html`, `dada-dogrula*.html`, `farkli-bakislar.html`, `dada-ozet.html`, `bugun-ne-oldu.html` ve `guncellenen-haberler.html` (otomatik), `duzeltme-politikasi.html`, ana sayfa manşeti.

### D3 · Multimedya ve Medya Havuzu

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Videolar | L | Sekmeler: Video · Akış (9:16) · Canlı yayın; süre, kategori, durum |
| 2 | Video düzenle | D | YouTube/embed ya da dosya, kapak (16:9 / 9:16), süre, kategori, açıklama (zengin metin), altyazı |
| 3 | Podcast serileri | L | |
| 4 | Seri düzenle | D | Kapak 1:1, ad, açıklama, kategori |
| 5 | Bölüm düzenle | D | Ses dosyası, bölüm no, süre, deşifre, kapak |
| 6 | Sesli haber ve Spiker bültenleri | L | Haber Dinle (sesli haber) ve Spiker bültenleri ("16.00 Bülteni") |
| 7 | Sesli bülten düzenle | D | Bülten haberleri, sıra, okuma metni, video/ses |
| 8 | Foto galeriler (Foto Fokus) | L | |
| 9 | Galeri düzenle | D | Çoklu slayt, sürükle-bırak sıra, altyazı ve kaynak, kapak kolajı (4:3), SEO |
| 10 | İnfografikler | L | |
| 11 | İnfografik düzenle | D | 3:4 görsel, kaynakça, indirme ve paylaşım izni |
| 12 | Medya havuzu | L | Klasör ağacı (ör. Savunma → İHA/SİHA → Kızılelma), ızgara/liste, süzgeç (telif, kaynak, çözünürlük), yükle |
| 13 | Medya varlığı | P (çekmece) | Telif ve kaynak, çözünürlük, etiketler, oran sürümleri, kullanım geçmişi |
| 14 | Marka şablonu | A | Logo konumu, kategori şeridi, oranlar (16:9, 1:1, 1.91:1), önizleme |

- **Bileşenler:** veri tablosu, medya seçici, görsel alanı, kırpma, dosya yükleme (ses, video), küçük oynatıcı, galeri sıralayıcı, ağaç, marka şablonu önizlemesi.
- **Roller:** SA ● · GYY ● · ED ● · KE ◐ · SM ◐ (havuzdan seçer, yükler) · AN —.
- **Sitede:** `video*.html`, `akis.html`, `canli-yayin.html`, `podcast*.html`, `haber-dinle*.html` (9), Spiker paneli (her sayfada), `foto-fokus*.html`, `infografik*.html`.

### D4 · Özel Dikeyler

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Kulüpler | L | Süper Lig 18 takım (örnek veriden), Avrupa, branşlar |
| 2 | Kulüp düzenle | D | Arma, kurumsal renk, kısa kod, stadyum, teknik direktör, etiket eşleştirme |
| 3 | Ligler ve puan durumu | L | Lig, hafta, puan tablosu; API verisi + elle düzeltme |
| 4 | Maç merkezi | L | Fikstür, canlı skor, maç detayı |
| 5 | Veri düzeltme (override) | P | Skor ya da tablo düzeltmesi, gerekçe, denetim izi |
| 6 | Takvimler | L | Gündem, ekonomik, sınav ve etkinlik takvimi tek ekranda, tür süzgeçli |
| 7 | Takvim kaydı | P | Tarih-saat, tür, kategori, bağlantı |
| 8 | Anketler | L | Kayıtta, **kapalı**; ekran şimdi üretilmez (K1) |
| 9 | Anket düzenle | D | Kapalı (K1). Açılınca: soru, seçenekler, süre, rate limit, sonuçlar |
| 10 | Sözlük | L | Kayıtta, **kapalı**; ekran şimdi üretilmez (K1). Dada Bağlam dosya sözlüğü D2'de kalır |
| 11 | Terim düzenle | P | Kapalı (K1) |
| 12 | Firma rehberi | L | Kayıtta, **kapalı**; ekran şimdi üretilmez (K1) |
| 13 | Firma düzenle | D | Kapalı (K1) |
| 14 | Veri bantları | A | Piyasa (döviz, altın, borsa, kripto, faiz, akaryakıt), hava, namaz vakitleri, deprem: API önceliği, güncelleme periyodu, önbellek süresi |
| 15 | Resmî ilanlar | L | (B-26 bekliyor) |
| 16 | İlan düzenle | D | |

- **Bileşenler:** veri tablosu, renk seçici, görsel alanı (arma 1:1), takvim görünümü, tarih-saat seçici, aranabilir açılır liste, form, onay diyaloğu.
- **Roller:** SA ● · GYY ● · KE ● (spor) · ED ◐ (takvim, anket) · SM — · AN ◐.
- **Sitede:** `spor.html` ve 9 branş, 4 takım, 2 lig, `canli-skor.html`, `puan-durumu.html`, `fikstur.html`, `takimlar.html`, `transfer.html`, `mac-detay.html`, `gundem-takvimi.html`, `ekonomik-takvim.html`, `sinav-takvimi.html`, piyasa sayfaları (8), `hava-durumu.html`, `namaz-vakitleri.html`, `afet-acil-durum.html`, `resmi-ilanlar.html`. Anket, sözlük, firma rehberi: yok (kayıtta kapalı, K1).

### D5 · AI Haber Havuzu ve Kaynak Motoru

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | AI haber havuzu | L | Üç sekme: Taslak · Yayınlanan · Reddedilen (K6; sonda Çöp, K11). "Görsel eksik", "otomatik yayımlandı" gibi durumlar sekme değil, satırda etiket ve süzgeç; güven skoru, 1./2./3. kaynak + grup, çekilme zamanı, kategori önerisi; Toplu Onayla / Toplu Reddet; üstte aylık işlem ve maliyet kutusu (izinli) |
| 2 | AI haber düzenle | D | Haber düzenle formunun aynısı + üst bilgi şeridi (durum, güven skoru, çekilme, kaynak, URL, AI modeli) + **Kaynak teyitleri** paneli: 1., 2., 3. kaynak (ad, grup, bağlantı, zaman) hem teyidi hem aynı haberin iki kez çekilmediğini gösterir (K8); alternatif kaynaklar + görsel eksikse havuzdan otomatik görsel önerisi |
| 3 | Reddet | P | Neden (tekil ve toplu) |
| 4 | Kaynaklar | L | Grup T1–T4 (K7), tip (RSS, scraper, haber sitesi, sosyal medya hesabı; her tür kaynak eklenebilir), URL, **medya izni**, aktif, son çekim, başarı/hata; toplu aktif/pasif/çöpe at; sonda Çöp |
| 5 | Kaynak ekle / düzenle | P | Medya izni: başkasının logosu ya da damgası olan görsel ve video kullanılmaz; izin kapalıysa haber "Görsel eksik" gelir (K7) |
| 6 | Frekans ve maliyet | A | Katman başına sıklık, aylık tahmini çekim, haber ve token maliyeti |
| 7 | Cron ve hat sağlığı | R | Crontab, kilit, aktif kaynak kullanımı, medya izni kapalı kaynak uyarısı, katman tablosu (beklenen/gerçekleşen), Manuel tetikle |
| 8 | Otomatik yayın ayarları | A | "Otomatik yayınla" anahtarı, güven eşiği ve sayısı ayarlanabilir güvenlik koşulları (K8): koşul eklenir, çıkarılır, açılıp kapanır (örnek koşullar: kaynak grubu, hariç kategori, görseli eksik haber, günlük üst sınır, en az kaynak sayısı). Değişiklik e-posta koduyla (K15) |

- **Bileşenler:** veri tablosu, toplu işlem, güven skoru göstergesi, kaynak teyidi paneli, sağlık kutusu, anahtar, eşik kaydırıcı, uyarı bandı, onay diyaloğu.
- **Roller:** Havuz ve düzenleme: SA ● · GYY ● · ED ● · KE ◐ (kendi kategorisi) · SM — · AN ◐. Kaynaklar: SA ● · GYY ◐. Frekans, maliyet, cron: yalnızca SA (izin grubuyla açılabilir). Otomatik yayın ayarı: SA, GYY + 2FA.
- **Sitede:** dolaylı; yayımlanan AI haberleri normal haber olarak görünür (teyit rozeti yok).

### D6 · Sosyal Medya Merkezi

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Sosyal hesaplar | L | Platform sekmeleri; dil/marka bazlı hesap; bağlantı ve token sağlığı, son paylaşım, son hata, aktif anahtarı |
| 2 | Hesap bağla / düzenle | P | OAuth ya da bot token (maskeli) |
| 3 | Gönderi oluşturucu | D | Bağımsız gönderi: haber seç ya da serbest; platform sekmeleri, AI metin (Hemen Üret / Yeniden Üret), sayaçlar, oran ve kırpma, canlı kart önizlemesi, hemen ya da zamanlı |
| 4 | Yayın takvimi | R | Zamanlanmış gönderiler, ay/hafta görünümü |
| 5 | Gönderim kuyruğu | L | Durum (bekliyor, gönderildi, hata), tek tıkla yeniden dene |

- **Bileşenler:** platform sekmesi, sosyal kart önizlemesi, kırpma, sayaçlı metin alanı, takvim görünümü, maskeli gizli alan, durum rozetleri.
- **Roller:** SA ● · GYY ● · SM ● · ED ◐ (haber formundaki sekme) · KE — · AN ◐ (rapor).
- **Platformlar (K9):** X, Facebook, LinkedIn, Instagram, Telegram açık; diğerleri (WhatsApp kanalı, YouTube, TikTok) kayıtta kapalı.
- **Sitede:** footer sosyal ikonları, paylaş satırı.

### D7 · Etkileşim

| # | Ekran | Tür | İçerik |
|---|---|---|---|
| 1 | Yorumlar | L | Bekleyen / yayında / gizli / spam; okur bildirimleri; toplu onay ve gizleme |
| 2 | Yorum detayı | P (çekmece) | Haber bağlamı, okur, editör yanıtı yaz |
| 3 | Bülten aboneleri | L | Bülten türü (Sabah, Akşam, Hafta sonu), kategori tercihi, durum |
| 4 | Bültenler | L | Gönderilen ve zamanlanmış bültenler, açılma/tıklanma |
| 5 | Bülten düzenle | D | Şablon, haber seçimi ("seçtiğin kategorilerden 5 haber"), e-posta önizlemesi, zaman |
| 6 | Push bildirimleri | L | Gönderilen, zamanlanmış; tıklanma raporu |
| 7 | Yeni push | D | Başlık ve içerik sayacı, görsel, hedef (konu/takım takipçileri, ❓ B-14), telefon önizlemesi, zaman |
| 8 | Reklam alanları | L | Header, manşet altı, haber içi, sidebar, mobil banner; durum, tarih |
| 9 | Reklam alanı düzenle | D | AdSense/Ad Manager kodu ya da sponsorlu görsel; tarih ve cihaz hedefi |
| 10 | Okur geri bildirimleri | L | Görüş bildir, düzeltme bildirimi, iletişim formu, KVKK başvurusu tek gelen kutusunda (K2) |
| 11 | Geri bildirim detayı | P (çekmece) | Yanıtla, ilgili habere git, kapat |

- **Bileşenler:** veri tablosu, toplu işlem, çekmece, zengin metin, e-posta önizlemesi, telefon bildirim önizlemesi, görsel alanı, tarih-saat seçici, grafik.
- **Roller:** Yorumlar: SA ● · GYY ● · ED ● (yorumları editörler yönetir, K4). Bülten ve push: SA ● · GYY ● · SM ●. Reklam: SA ● · GYY ◐. Geri bildirim: SA, GYY, ED.
- **Sitede:** haber detayında Yorumlar, `bulten.html`, `bulten-arsivi.html`, Hesabım bülten ve bildirim ayarları, bildirim izni kartı, `reklam.html` (reklam yer tutucuları Beyar kararıyla kaldırıldı, C25), Görüş bildir pencereleri, `iletisim.html`, `kvkk-basvuru.html`.

**Dada Haber toplamı: kayıtta 74 ekran, şimdi üretilecek 68** (D1 1 · D2 19 · D3 14 · D4 16, bunun 6'sı kapalı · D5 8 · D6 5 · D7 11).

---

## 5 · Site içerik türü → panel karşılığı

| Sitedeki tür | Panel karşılığı | Durum |
|---|---|---|
| Standart haber, bölüm haber detayları | D2 Haber düzenle | var |
| Köşe yazısı, özel haber, araştırma, analiz, uzman görüşü | D2 Haber düzenle · tür | kabul (K2) |
| Son Dakika şeridi ve sayfası | D2 Son Dakika | var |
| Canlı, Canlı Gündem, Dakika Dakika | D2 Canlı anlatım masası | kabul (K2) |
| Dada Özet, Neden önemli / Bana etkisi / Bundan sonra | D2 Haber düzenle · Detay alanları | kabul (K2) |
| Dada Bağlam, gelişen olay sayfası | D2 Olay dosyaları | kabul (K2) |
| Günün 5'i | D2 Günün 5'i | kabul (K2) |
| Dada Doğrula | D2 İncelemeler | kabul (K2) |
| Farklı Bakışlar | D2 Haber düzenle · tür | kabul (K2) |
| Bugün Ne Oldu, Güncellenen Haberler, Arşiv, RSS | otomatik (panel ekranı gerekmez) | — |
| Yazarlar / Sesler | D2 Yazarlar | ad B-05 |
| Etiket, kişi/kurum sayfası | D2 Etiketler ve varlıklar | var |
| Video, Akış, Canlı Yayın | D3 Videolar | Canlı yayın akışı belirsiz |
| Podcast | D3 Podcast | var |
| Haber Dinle, Spiker | D3 Sesli haber ve Spiker | PDF'te "sesli haber" var; Spiker yok |
| Foto Fokus, İnfografik | D3 | var |
| Spor (lig, takım, maç, fikstür, transfer) | D4 Spor | transfer = haber + veri? ❓ |
| Takvimler (gündem, ekonomik, sınav) | D4 Takvimler | var |
| Piyasa, hava, namaz, deprem, akaryakıt | D4 Veri bantları | var |
| Trafik ve Ulaşım, ekonomi araçları | — | B-25 bekliyor |
| Resmî İlanlar | D4 Resmî ilanlar | B-26 bekliyor |
| Hamilelik, Astroloji/burç | — | B-24 bekliyor; içerik statik mi günlük mü belirsiz |
| Dada'ya Sor | K3 Özellik anahtarı (+ kapsam ayarı) | B-16 bekliyor |
| Yorumlar | D7 Yorumlar | var |
| Bülten | D7 Bülten | var |
| Push / bildirim izni | D7 Push | mobil uygulama sonra (V-17) |
| Reklam alanları | D7 Reklam | yerler tanımsız (C25) |
| Görüş bildir, iletişim, KVKK başvuru, İK formu | D7 Okur geri bildirimleri | kabul (K2) |
| Üyelik, Hesabım | K2 Üyeler | var |
| Yasal metinler | K6 | var |
| Kurumsal metinler (Hakkımızda, İletişim, Yardım, Reklam, İK) | K9 Sayfalar | kabul (K2) |
| Çerez bandı ve tercih merkezi | K6 Çerez Politikası + K3 | çerez kategorileri ayarı ❓ |
| Aile siteleri, footer, sosyal bağlantılar | K3 Site ayarları | B-12 bekliyor |
| Bakım (503) | K3 Site Ayarları | var (K11) |
| Hata sayfaları, çevrimdışı, yakında | — | panel ekranı gerekmez |
| Anket, Sözlük, Firma Rehberi, Quiz/Günün Serisi/rozet | D4 (anket, sözlük, firma) · — (quiz) | kayıtta kapalı (K1); quiz ve seri yok |

## 6 · Rol × modül görünürlüğü (öneri)

| Modül | SA | GYY | ED | KE | SM | AN |
|---|---|---|---|---|---|---|
| D1 Kontrol Paneli | ● | ● | ◐ | ◐ | ◐ | ◐ |
| D2 Haberler ve Vitrin | ● | ● | ● | ◐ kendi kategorisi | ◐ sosyal sekmesi | ◐ okur |
| D3 Multimedya | ● | ● | ● | ◐ | ◐ | — |
| D4 Özel Dikeyler | ● | ● | ◐ | ● spor | — | ◐ |
| D5 AI Havuzu | ● | ● | ● havuz | ◐ | — | ◐ |
| D5 Kaynaklar, frekans, maliyet, cron | ● | ◐ kaynaklar | — | — | — | — |
| D6 Sosyal Medya | ● | ● | ◐ | — | ● | ◐ |
| D7 Etkileşim | ● | ● | ● yorum · ◐ diğer | — | ◐ bülten, push | ◐ |
| K1 Kimlik ve Yetki | ● | ◐ | — | — | — | — |
| K2 Kullanıcılar | ● | ◐ | — | — | — | — |
| K3 Site Ayarları | ● | ◐ | — | — | — | — |
| K4 Denetim İzi | ● | ◐ | — | — | — | ◐ |
| K5 Raporlar | ● | ● | ◐ | ◐ | ◐ | ● |
| K6 Yasal Metinler | ● | ● | — | — | — | — |
| K9 Sayfalar | ● | ● | — | — | — | — |
| K7 Sistem Sağlığı | ● | — | — | — | — | — |
| K8 Entegrasyonlar | ● | — | — | — | — | — |

Rol değiştiricide şimdilik yalnızca Süper Admin ve Editör var (K4); diğer dört rol kayıtta tanımlı, satırları öneri. Rol izin gruplarından oluşur (K5).

Alan ve kutu düzeyi gizlenecekler (izin grupları): AI maliyeti ve token, kaynak frekans maliyeti, cron ve sistem sağlığı kutuları, entegrasyon hataları, kişisel veri (e-posta, telefon, IP) maskesi.

## 7 · Toplam ekran sayısı

| Grup | Ekran |
|---|---|
| Çekirdek (K0–K9) | 59 |
| Dada Haber (D1–D7) | 74 |
| **Kayıtta toplam** | **133** |
| Kayıtta kapalı, şimdi üretilmeyen (anket, sözlük, firma rehberi; K1) | 6 |
| **Üretilecek** | **127** |
| Çalışma sırasıyla öncelikli | Kabuk + D1 Kontrol Paneli (adım 2) · D2 Haberler tamamı (adım 3) · K3 Site Ayarları (adım 4) |

Her ekran masaüstü, tablet ve telefonda üretilecek. Üretilecek ekranların 43'ü açılır pencere, çekmece ya da tek başına durum sayfasıdır (giriş akışı dahil); bunların çoğu ortak bileşenden türer.

## 8 · Rail'siz yan menü (kabul, K3)

Menü gruplamaları Dada Haber dokümanındaki 8 katmandan gelir. Alt tanımlar (kategori, etiket, marka şablonu, otomatik yayın ayarı) menüde değil, ekranların sağ üstündeki düğmededir. Süper Admin görünümü:

```
[Dada Haber logosu]                    (daraltınca yalnızca işaret)
─────────────────────────────
  Kontrol Paneli                        (katman 1)

YAYIN MERKEZİ                           (katman 2)
  Haberler                     ⟶ sağ üst: Kategoriler · Etiketler
  Vitrin ve Son Dakika         ⟶ sekme: Manşet · Son Dakika
  Canlı Anlatım
  Dosyalar ve Formatlar        ⟶ sekme: Dada Bağlam · Günün 5'i · Dada Doğrula
  Yazarlar

AI HABER HAVUZU                         (katman 5)
  Haber Havuzu        (12)     ⟶ sağ üst: Otomatik yayın ayarı
  Kaynaklar
  Kaynak Motoru                ⟶ sekme: Frekans ve Maliyet · Cron Sağlık   [editöre kapalı]

MULTİMEDYA                              (katman 3)
  Video ve Akış
  Podcast
  Sesli Haber ve Spiker
  Galeri ve İnfografik
  Medya Havuzu                 ⟶ sağ üst: Marka şablonu

ÖZEL DİKEYLER                           (katman 4)
  Spor                         ⟶ sekme: Kulüpler · Ligler · Maçlar
  Takvimler
  Veri Bantları
  Resmî İlanlar                (B-26 bekliyor)
  [kayıtta kapalı: Anketler · Sözlük · Firma Rehberi — K1]

SOSYAL MEDYA                            (katman 6)
  Gönderi Oluştur
  Yayın Takvimi                ⟶ sekme: Takvim · Gönderim Kuyruğu
  Hesaplar

ETKİLEŞİM                               (katman 7)
  Yorumlar            (5)
  Bülten
  Push Bildirimleri
  Reklam Alanları
  Okur Geri Bildirimleri

SİSTEM                                  (katman 8 · çekirdek)
  Kullanıcılar
  Roller ve Yetki
  Site Ayarları                ⟶ sekme: … · Bakım modu (K11)
  Entegrasyonlar
  Yasal Metinler
  Sayfalar                     (kurumsal metinler, K2)
  Raporlar
  Denetim İzi
  Sistem Sağlığı               ⟶ sekme: Sağlık · Önbellek
─────────────────────────────
  Siteyi görüntüle · Gavia imzası
```

- Süper Admin'de ~35 kalem; Editör görünümünde ~16.
- **Gruplar katlanabilir (K3):** içinde bulunulan grup her zaman açık; diğer grupların açık/kapalı durumu tarayıcıda hatırlanır. Davranış kayıttaki `menu` ayarından gelir.
- Kapalı modüller ve kapalı sosyal platformlar menüde ve bağlantılarda görünmez.
- Rozet sayaçları: AI havuzunda bekleyen, yorumlarda bekleyen, sosyal kuyruğunda hata.
- Kapatılan modülün kalemi ve ekranlara giden bütün bağlantıları kaybolur; eski adres 404'e düşer.

## 8b · Tutarlılık: içerik türü × standart yetenek

CLAUDE.md "Tutarlılık": aynı yetenek, onu gerektiren her modülde aynı yerde ve aynı görünümde. Aşağıdaki tablo hangi içerik türünün düzenleme ekranında hangi standart sekme ve alanın bulunacağını gösterir (● var · — yok · ◐ öneri, pilot sonrası teyit).

| İçerik türü | SEO sekmesi | Zengin metin | Zamanlama (tarih-saat) | Görsel alanı + kırpma | Bildirim sekmesi | Sosyal Medya sekmesi | Dil seçici |
|---|---|---|---|---|---|---|---|
| Haber (bütün türleri) | ● | ● gövde, spot | ● | ● kapak | ● | ● | ● |
| AI haberi | ● | ● | ● | ● | ● | ● | ● |
| Canlı anlatım | ● | ● satır | ● | ● | ● | ● | ● |
| Olay dosyası (Dada Bağlam) | ● | ● | ● | ● | ◐ | ● | ● |
| Günün 5'i | ◐ | ● | ● | ● | ● | ● | ● |
| Dada Doğrula incelemesi | ● | ● | ● | ● | ◐ | ● | ● |
| Video, Akış | ● | ● açıklama | ● | ● kapak | ● | ● | ● |
| Podcast serisi | ● | ● açıklama | — | ● 1:1 | — | ◐ | ● |
| Podcast bölümü | ● | ● açıklama, deşifre | ● | ● 1:1 | ● | ● | ● |
| Sesli bülten | ● | ● okuma metni | ● | ● | ● | ◐ | ● |
| Foto galeri | ● | ● açıklama | ● | ● slaytlar | ● | ● | ● |
| İnfografik | ● | ● açıklama | ● | ● 3:4 | ◐ | ● | ● |
| Yazar | ● | ● biyografi | — | ● 1:1 | — | — | ● |
| Kategori, alt konu | ● | ● açıklama | — | ◐ banner | — | — | ● |
| Etiket, kişi, kurum | ● | ● açıklama | — | ◐ | — | — | ● |
| Kulüp | ● | ● | — | ● arma | — | — | ● |
| Takvim kaydı | — | ● | ● | ◐ | ◐ | ◐ | ● |
| Resmî ilan | ● | ● | ● | — | — | — | ● |
| Sayfa (kurumsal), yasal metin | ● | ● | ● yürürlük | — | — | — | ● |
| Bülten | — | ● | ● | ● | — | — | ● |
| Push | — | — | ● | ● | (kendisi) | — | ● |
| Sosyal gönderi | — | — | ● | ● | — | (kendisi) | ● |
| Reklam alanı | — | — | ● başlangıç-bitiş | ● | — | — | — |

Ortak yerleşim (her ekranda aynı yer): sayfa başlığı · sağ üst eylemler · süzgeç çubuğu · sekmeler · yan panel · kaydet çubuğu. Yerleri kabuk ve pilot modülde seçtirilir.

## 9 · Ortak bileşen listesi (çekirdek)

**Kabuk:** yan menü (kayıttan üretilen) · üst bar · genel arama · bildirim paneli · hesap menüsü · rol değiştirici · sayfa başlığı (h1 + alt satır + sağ üst eylemler) · çekmece (sağdan) · açılır pencere.

**Veri ve gösterim:** veri tablosu (arama, süzgeç, sıralama, sayfalama, toplu işlem çubuğu, sütun gizleme, yatay kayma, satırın tamamı tıklanır) · süzgeç çubuğu · durum sekmeleri + sayaç + her listede aynı yerde Çöp sekmesi (geri al; silen kişi ikinci onayla kalıcı siler, K11) · kart · KPI kartı · grafik (çizgi, çubuk) · sağlık kutusu + durum noktası · takvim görünümü · zaman çizelgesi · ağaç (kategori, klasör) · sürükle-bırak liste · fark görünümü (önce/sonra) · log görüntüleyici · avatar · ipucu.

**Form:** metin, sayı, metin alanı + karakter sayacı · zengin metin editörü · aranabilir açılır liste (tekli, çoklu, "havuza ekle") · etiket girişi · özel tarih-saat seçici · tarih aralığı · telefon (ülke kodu + maske) · e-posta (yazarken doğrulama) · adres (slug) üretici · anahtar · radyo kart · eşik kaydırıcı · renk seçici · dosya yükleme (ses, video, belge) · maskeli gizli alan (bir kez göster, kopyala) · dil seçici (formun üstünde tek) · sekmeli düzenleme sayfası · form yan paneli (durum, yayın zamanı) · yapışkan kaydet çubuğu + kaydedildi + kaydedilmemiş değişiklik uyarısı · alan doğrulama mesajı + sekme hata noktası · güven skoru göstergesi · SEO skoru.

**Medya:** medya seçici (havuz + yükle) · görsel alanı (web + mobil bölümü, önerilen ölçü) · kırpma penceresi (odak noktası, oran ön ayarları, yakınlaştırma, sıfırla, kırpmadan kullan, canlı önizleme) · marka şablonu önizlemesi · küçük ses/video oynatıcı · galeri sıralayıcı.

**Önizleme:** site kartı · mobil kart · sosyal kartlar (X, Facebook, Instagram, LinkedIn, Telegram) · telefon bildirimi · arama sonucu (SERP) · e-posta.

**Geri bildirim:** onay diyaloğu (ikinci onay, tehlikeli işlem) · e-posta kodu doğrulaması (2FA, K15) · toast (geri al) · boş durum · yükleniyor (iskelet) · hata durumu · durum rozetleri · uyarı bandı (bilgi, uyarı, tehlike) · bakım modu bandı · "otomatik yayımlandı" işareti · ilerleme.

Toplam ~60 bileşen. UI kit adımında (çalışma sırası 6) hepsi `ui-kit.html` sayfasında bütün durumlarıyla gösterilir ve dondurulur. Referans kabuktan doğrudan alınabilenler: kabuk, kart, KPI, rozet, düğme, onay diyaloğu, toast, boş durum, sayfa başlığı, form temel alanları. Sıfırdan kurulacaklar: toplu işlem, sıralama, iskelet, hata durumu, özel tarih seçici, aranabilir açılır liste, telefon/e-posta alanı, kırpma, önizlemeler, izin matrisi, fark görünümü.

## 10 · Görsel alanları (önerilen ölçü taslağı)

Ölçüler public sitenin CSS'inden okunan oranlardır; piksel değerleri sitedeki görünen genişlikten hesaplanacak. Mobil ölçüler sitenin telefon görünümünden türetilir ve modül kaydında durur (K14).

| Alan | Web | Mobil | Not |
|---|---|---|---|
| Haber kapağı | 16:10 (kart) · 2.4:1 (detay) | 16:10 | Tek kaynak görselden iki kırpma; odak noktası ortak |
| Video kapağı | 16:9 | 16:9 | |
| Akış (kısa video) | 9:16 | 9:16 | |
| Podcast kapağı | 1:1 | 1:1 | |
| İnfografik | 3:4 | 3:4 | |
| Galeri kapağı | 4:3 kolaj | 4:3 | |
| Yazar fotoğrafı | 1:1 (daire) | 1:1 | |
| Kulüp arması | 1:1 | 1:1 | şeffaf zemin |
| Bildirim görseli | 2:1 | 2:1 | push servisinin önerisine göre doğrulanacak |
| Sosyal | 16:9 · 1:1 · 4:5 · 1.91:1 · serbest | — | X 1200×675 · IG 1080×1080 / 1080×1350 · FB ve LinkedIn 1200×630 (MM referansı) |
| Reklam alanları | — | — | yerler tanımsız (C25) |

## 11 · `moduller.json` taslağı

Tek kayıt dosyası. Yan menü bundan üretilir: betik menü HTML'ini sayfalara yazar, JS etkin kalemi, rolü ve grup açık/kapalı durumunu işaretler (K13). Modül `acik:false` olunca menüden ve bütün bağlantılardan çıkar. Modüller `moduller/<id>/` klasöründe, çekirdek modüller `cekirdek/<id>/` klasöründe durur. Alan adları öneridir; yapı pilot modülde oturur, UI kitte dondurulur.

**Tema ayrı dosyadır ve yalnızca renk ile logo taşır** (CLAUDE.md "Referans kabuk"). Yazı tipi, köşe, boşluk ölçeği ve bileşen dili çekirdektedir; projeden projeye değişmez.

```json
{
  "surum": 1,
  "proje": "dadahaber",
  "tema": "tema/dadahaber.css",
  "logo": { "tam": "tema/logo.svg", "isaret": "tema/logo-isaret.svg" },

  "menu": { "katlanir": true, "etkin_grup_acik": true, "durumu_hatirla": true },

  "roller": [
    { "id": "super",   "ad": "Süper Admin",           "seviye": 100, "izin_gruplari": ["*"] },
    { "id": "gyy",     "ad": "Genel Yayın Yönetmeni", "seviye": 80,  "izin_gruplari": ["icerik-tam", "yayin", "vitrin", "yorum", "rapor"] },
    { "id": "editor",  "ad": "Editör",                "seviye": 50,  "izin_gruplari": ["icerik-tam", "yayin", "vitrin", "yorum", "ai-havuz"] },
    { "id": "kat-ed",  "ad": "Spor/Kategori Editörü", "seviye": 40,  "izin_gruplari": ["icerik-kapsamli", "spor"], "kapsam": "kategori" },
    { "id": "sosyal",  "ad": "Sosyal Medya Uzmanı",   "seviye": 40,  "izin_gruplari": ["sosyal", "bulten-push"] },
    { "id": "analist", "ad": "Analist",               "seviye": 30,  "izin_gruplari": ["rapor", "okuma"] }
  ],
  "rol_degistirici": ["super", "editor"],

  "izin_gruplari": [
    { "id": "ai-maliyet",  "ad": "Maliyet ve token",       "islemler": [], "alanlar": ["ai.maliyet", "kontrol.maliyet-kutusu"] },
    { "id": "cron-saglik", "ad": "Cron ve sistem sağlığı", "islemler": ["ai-motor:goruntule"], "alanlar": ["kontrol.cron-kutusu"] }
  ],

  "dogrulama": {
    "yontem": "eposta-kodu",
    "giriste": { "sorulmayan_roller": ["super"] },
    "hassas_islemler": ["rol-degistir", "api-anahtari", "toplu-silme", "bakim-modu-ac", "otomatik-yayin-ayari"]
  },

  "gruplar": [
    { "id": "panel",     "ad": null,              "sira": 1 },
    { "id": "yayin",     "ad": "Yayın Merkezi",   "sira": 2 },
    { "id": "ai",        "ad": "AI Haber Havuzu", "sira": 3 },
    { "id": "medya",     "ad": "Multimedya",      "sira": 4 },
    { "id": "dikey",     "ad": "Özel Dikeyler",   "sira": 5 },
    { "id": "sosyal",    "ad": "Sosyal Medya",    "sira": 6 },
    { "id": "etkilesim", "ad": "Etkileşim",       "sira": 7 },
    { "id": "sistem",    "ad": "Sistem",          "sira": 8 }
  ],

  "moduller": [
    {
      "id": "haberler",
      "ad": "Haberler ve Vitrin",
      "cekirdek": false, "acik": true,
      "grup": "yayin", "sira": 1, "ikon": "fa-newspaper",
      "klasor": "moduller/haberler/",
      "roller": ["super", "gyy", "editor", "kat-ed", "sosyal", "analist"],
      "bagimli": ["medya-havuzu", "kullanicilar"],
      "bilesenler": ["veri-tablosu", "satir-eylemleri", "toplu-islem", "cop-sekmesi", "sekmeli-duzenleme", "dil-secici",
                     "zengin-metin", "gorsel-alani", "kirpma", "aranabilir-liste", "tarih-saat",
                     "seo-sekmesi", "bildirim-sekmesi", "sosyal-sekmesi"],
      "ayarlar": {
        "kategori": { "ana_zorunlu": true, "alt_konu_zorunlu": true, "ek_kategori": true },
        "vitrin": { "kapsam": "manset", "manset_slayt": 5, "yan_kart": 3 }
      },
      "sayfalar": [
        { "id": "liste",   "baslik": "Haberler",             "dosya": "haberler.html",      "menude": true,
          "sag_ust": ["kategoriler", "etiketler"] },
        { "id": "duzenle", "baslik": "Haber Düzenle",        "dosya": "haber-duzenle.html", "menude": false },
        { "id": "vitrin",  "baslik": "Vitrin ve Son Dakika", "dosya": "vitrin.html",        "menude": true,
          "roller": ["super", "gyy", "editor"] }
      ],
      "gorsel_alanlari": {
        "kapak": {
          "web":   { "kart": { "oran": "16:10", "px": null }, "detay": { "oran": "2.4:1", "px": null } },
          "mobil": { "kart": { "oran": "16:10", "px": null } },
          "mobil_webden_kirpilir": true
        }
      }
    },
    {
      "id": "ai-havuz",
      "ad": "AI Haber Havuzu",
      "cekirdek": false, "acik": true,
      "grup": "ai", "sira": 1, "ikon": "fa-robot",
      "klasor": "moduller/ai-havuz/",
      "roller": ["super", "gyy", "editor", "kat-ed", "analist"],
      "bagimli": ["haberler", "entegrasyonlar"],
      "ayarlar": {
        "sekmeler": ["taslak", "yayinlanan", "reddedilen"],
        "satir_etiketleri": ["gorsel-eksik", "otomatik-yayimlandi"],
        "kaynak_gruplari": [
          { "id": "T1", "ad": "Resmî" },
          { "id": "T2", "ad": "Kurumsal Basın" },
          { "id": "T3", "ad": "Uluslararası Medya" },
          { "id": "T4", "ad": "Düşük Öncelik" }
        ],
        "kaynak_tipleri": ["rss", "scraper", "haber-sitesi", "sosyal-hesap"],
        "medya_izni_kapaliysa": "gorsel-eksik",
        "gosterilen_kaynak_sayisi": 3,
        "otomatik_yayin": { "acik": false, "esik": 85, "kosullar": [] }
      },
      "sayfalar": [
        { "id": "havuz",     "baslik": "Haber Havuzu",  "dosya": "havuz.html",     "menude": true, "rozet": "taslak-sayisi" },
        { "id": "kaynaklar", "baslik": "Kaynaklar",     "dosya": "kaynaklar.html", "menude": true, "roller": ["super", "gyy"] },
        { "id": "motor",     "baslik": "Kaynak Motoru", "dosya": "motor.html",     "menude": true, "roller": ["super"] }
      ]
    },
    {
      "id": "sosyal-medya",
      "ad": "Sosyal Medya Merkezi",
      "cekirdek": false, "acik": true,
      "grup": "sosyal", "sira": 1, "ikon": "fa-share-nodes",
      "klasor": "moduller/sosyal-medya/",
      "roller": ["super", "gyy", "sosyal", "analist"],
      "bagimli": ["haberler", "medya-havuzu"],
      "ayarlar": {
        "platformlar": [
          { "id": "x",         "acik": true,  "oranlar": ["16:9", "1:1", "serbest"] },
          { "id": "facebook",  "acik": true,  "oranlar": ["1.91:1", "1:1", "serbest"] },
          { "id": "linkedin",  "acik": true,  "oranlar": ["1.91:1", "1:1", "serbest"] },
          { "id": "instagram", "acik": true,  "oranlar": ["1:1", "4:5", "serbest"] },
          { "id": "telegram",  "acik": true,  "oranlar": ["16:9", "1:1", "serbest"] },
          { "id": "whatsapp",  "acik": false },
          { "id": "youtube",   "acik": false },
          { "id": "tiktok",    "acik": false }
        ]
      }
    },
    { "id": "anket",         "ad": "Anketler",       "cekirdek": false, "acik": false, "grup": "dikey", "sira": 8,  "ikon": "fa-square-poll-vertical" },
    { "id": "sozluk",        "ad": "Sözlük",         "cekirdek": false, "acik": false, "grup": "dikey", "sira": 9,  "ikon": "fa-book" },
    { "id": "firma-rehberi", "ad": "Firma Rehberi",  "cekirdek": false, "acik": false, "grup": "dikey", "sira": 10, "ikon": "fa-building" },
    {
      "id": "site-ayarlari",
      "ad": "Site Ayarları",
      "cekirdek": true, "acik": true,
      "grup": "sistem", "sira": 3, "ikon": "fa-sliders",
      "klasor": "cekirdek/site-ayarlari/",
      "roller": ["super", "gyy"],
      "bagimli": [],
      "sayfalar": [
        { "id": "ayarlar",    "baslik": "Site Ayarları",       "dosya": "site-ayarlari.html",       "menude": true },
        { "id": "anahtarlar", "baslik": "Özellik Anahtarları", "dosya": "ozellik-anahtarlari.html", "menude": false }
      ]
    }
  ]
}
```

**Yasin Bey'e bağlı ayarlar** (K1, K3, K7, K16; Yasin Bey farklı derse yalnızca bu değerler değişir):

| Karar | Kayıttaki yer | Bugünkü değer |
|---|---|---|
| K1 Anket, Sözlük, Firma Rehberi | `moduller[anket|sozluk|firma-rehberi].acik` | `false` |
| K3 Menü grupları | `menu.katlanir`, `menu.etkin_grup_acik`, `menu.durumu_hatirla` | `true`, `true`, `true` |
| K7 Kaynak grupları, tipleri, medya izni | `ai-havuz.ayarlar.kaynak_gruplari`, `kaynak_tipleri`, `medya_izni_kapaliysa` | T1–T4; dört tip; `gorsel-eksik` |
| K16 Vitrin kapsamı | `haberler.ayarlar.vitrin.kapsam` | `manset` |

Sözleşme kuralları (taslak):
- `cekirdek:true` modüller hiçbir `cekirdek:false` modüle `bagimli` olamaz.
- Bir modül kapatılınca ona bağımlı modüller uyarı verir; kapatma engellenmez, sonucu gösterilir (öneri).
- Sayfa düzeyindeki `roller`, modül düzeyini daraltır, genişletemez. Rol, izin gruplarından oluşur (K5).
- Modül yalnızca `bilesenler` listesindeki ortak bileşenleri kullanır; eksik bileşen çekirdeğe eklenir.
- Sınıf ön eki: modüle özgü sınıflar `m-<modül>-*` (public depodaki `.yeni` sınıf çakışması dersi).
- Kanıt (UI kit adımı): bir modül kayıttan kapatılır; menü, Kontrol Paneli kutuları ve iç bağlantılarda kırık bağlantı kalmadığı tarayıcıyla gösterilir.

## 12 · Public depodan panele uyarlanması önerilen araç ve kurallar

**Kopyalanmayacak; yalnızca öneridir.** Kaynak: `dadahaber-prototip/CLAUDE.md`, `tasks/durum.md`, `araclar/`, `tasks/araclar/`, `docs/negatif-ornekler.md`.

**Menü üretimi (K13: C · karma kabul edildi)**
- **A · Çalışma anında JS:** `moduller.json` fetch edilir, menü çizilir. Sök-tak en kolay; ama `file://` altında fetch çalışmaz (yerel sunucu gerekir), menü ilk anda boş görünür.
- **B · Üretim anında yerleştirme (`parca.py` modeli):** menü `moduller.json`'dan üretilip `<!--P:menu-->` işaretlerinin arasına yazılır. Statik, hızlı, full-stack aktarımında Blade/şablon parçasına birebir döner; modül değişince betik çalıştırılır.
- **C · Karma (tavsiyem):** menü HTML'i B ile yazılır; JS yalnızca etkin kalemi, rolü ve izin kutularını işaretler. Rol değiştirici zaten JS ister.

| Araç ya da kural | Öneri | Gerekçe |
|---|---|---|
| `araclar/parca.py` (P işaretleri, CSS/JS sürüm eki, `main#icerik`, boş "#" uyarısı, sayısal tablo sütununa `say`) | değiştirerek uyarla | Kabuk parçası ve menü üretiminin temeli; haber sitesine özgü dönüşümler (teyit rozeti silme, paylaş satırı vb.) atılır, `moduller.json`'dan menü üreten adım eklenir |
| `araclar/sablon.html` | değiştirerek uyarla | `P:yan-menu`, `P:ust-bar` işaretleri; `noindex` aynen |
| `araclar/baglanti_kurallari.py` | gerekmez | Haber bağlamına özgü; panelde "boş # = 0" ve "kapalı modüle bağlantı = 0" kontrolü yeter |
| `araclar/veri_uygula.py` + `VERI.md` | fikri aynen, kod yeniden | Tek "şimdi" anı ve tek örnek veri kaynağı panelde de tutarsızlığı önler; idempotent ve `--dogrula` deseni alınır. Panel, public sözlüğünü **okur**, panele özgü alanları kendi ek sözlüğünde tutar (K12) |
| `tasks/araclar/son_kontrol.py` | değiştirerek uyarla | `<style>` yok, tek h1, seviye atlamaz, parçalar ortak, kırık bağlantı yok; erişilebilirlik BFS'i "her açık modül menüden ulaşılır, kapalı modüle hiçbir bağlantı yok" kontrolüne çevrilir (sök-tak kanıtı) |
| `tasks/araclar/tasma_tara.py` (headless Chrome, iframe, 360/390/768/1024) | değiştirerek uyarla | 1280/1440 eklenir; koşum dosyası kök yerine geçici klasöre; Chrome yolu parametre; kaydırma kabı içindekiler hariç (tablolar bilinçli kayar) |
| `tasks/araclar/cakisma_tara.py`, `etkilesim_test.py` | değiştirerek uyarla | Yöntem aynı (tıkla, ölç, GEÇTİ/KALDI); testler panel bileşenlerine göre (toplu işlem, kırpma, tarih seçici, rol değiştirici) yazılır; animasyon beklemesi uzatılır |
| `tasks/araclar/dar_bak.py`, `oge_resim.py`, `bos_satir.py` | aynen uyarla | Genel araçlar; `bos_satir.py` "sağı boş satır yok" kuralını panelde de denetler |
| `kararlara_uydur.py`, `*_uret.py`, `logo_uygula.py`, `sistem_kur.py` | gerekmez | Tek seferlik site üreticileri |
| `araclar/kaliplar.md` | değiştirerek uyarla | Panel kalıp kılavuzu açılır (liste, düzenleme, ayar, rapor, pencere kalıpları); C3–C6 kaynak olur |
| `docs/negatif-ornekler.md` (N1–N24) | aynen uyarla, panel kendi dosyasını açar | N1 tablo hizası, N2/N18 tek açık akordeon, N4 boşluk ölçeği, N9/N15/N16 kaydırma, N10/N22 binme, N11 `min-inline-size:0`, N12 iOS düğme rengi, N13 sınıf davranış sızması, N14/N17 görünen her kontrol çalışır, N20 kontrol köşesi 12px, N23 kapat düğmesi, N24 `dialog` konumu |
| Tek kaynak değişkenler, mantıksal özellikler (`inline-start`), tek bileşen, tek h1, `text-wrap: pretty`, `--ikon-bosluk`, yalnızca `fa-solid` | aynen uyarla | Bağlamdan bağımsız; mantıksal özellikler Arapça (sağdan sola) için şart |
| Göreli `url()` değişken içinde bozuluyor → görsel satır içi `background-image` | aynen uyarla | Kare görsel kuralıyla aynı |
| Headless Chrome 500px altına inmiyor → dar ölçüm iframe ile | aynen uyarla | Telefon ölçümleri için |
| Teslimden önce üç tarama (taşma, çakışma, etkileşim); "görüntüye bakmak test sayılmaz" | aynen uyarla | |
| Düzeltme ortak bileşende yapılır, sayfa yaması yok; revize üç genişlikte birden | aynen uyarla | Sök-tak sistemin özü |
| Sabit öğe ve z-index ölçeği tek yerde | değiştirerek uyarla | Panelde sabit menü, üst bar, kaydet çubuğu, toast ve çekmece aynı ölçekten |
| Tablo: metin başa, sayı sona, eşit genişlikli rakam | aynen uyarla | Panel tablo ağırlıklı |
| Kartın tamamı tıklanır, içinde tek bağlantı | aynen uyarla (satır için) | CLAUDE.md'de zaten var |
| Paragraflar iki yana yaslı, bülten son bölüm, Spiker, footer perdesi | gerekmez | Okur sitesi kuralları |

## 13 · Eksik, çelişkili ya da belirsiz bulunanlar

> **24.11.2026 durumu:** kararla kapananlar: 2 (K1), 3 (K2), 4 (K6), 5 (K7), 8 (K4), 9 (K5), 10 (K9), 11 (K10), 12 ve 13 (K11), 14 (K16), 17 (K14), 19 (K12), 24 (K17), 26 (K15), 28 (K2), 30 (K19). Kısmen: 6 (K8: koşul sayısı ayarlanabilir, hangi koşulların varsayılan geleceği Yasin Bey ile), 16 (K15: 2FA yöntemi e-posta kodu; push hedefi B-14'e bağlı). Açık: 1, 7, 15, 18, 20, 21, 22, 23, 25, 27, 29. Aşağıdaki metin keşif anındaki haliyle duruyor.

1. **Dada PDF'inde 2.1 yok, 2.2 iki kez yazılmış** (biri DAM ve akıllı görsel seçiciyi içeren uzun hali). Haber, kategori ve vitrin ayrıntısı siteden türetildi (D2); Beyar ile gözden geçirilecek.
2. **PDF'in istediği ama sitede olmayanlar:** Anket ("Sen Ne Düşünüyorsun" akış A1'de var, sitede bileşen yok), Terimler Sözlüğü (sitede yalnızca Dada Bağlam dosya sözlüğü), Firma Rehberi, Quiz / Günün Serisi / rozet (akışlarda 2. çeyrek). CLAUDE.md: "sitede olmayan bir alan panelde sorulmaz."
3. **Sitede olup PDF'lerde paneli olmayanlar:** Canlı anlatım (Dakika Dakika), Dada Bağlam, Günün 5'i, Dada Özet ve Neden önemli/Bana etkisi alanları, Dada Doğrula, Farklı Bakışlar, Spiker, Dada'ya Sor, Resmî İlanlar, takvimler, Görüş bildir/iletişim/KVKK başvuru formları, hamilelik ve burç içerikleri. Panelde yerleri öneri olarak yazıldı.
4. **AI havuzu sekmeleri:** PDF Taslak / Yayınlanan / Reddedilen (3); Milli Müdafaa'da ayrıca "Bekleyenler" var ve "Taslak" ile "Editör Onayı Bekliyor" ayrı durumlar.
5. **Kaynak katmanları:** yeni doküman T1 Resmî · T2 Kurumsal Basın · T3 Uluslararası Medya · T4 Düşük Öncelik; eski K1 Resmî · K2 Ajans · K3 Rakip site (yalnızca sinyal) · K4 Sosyal medya (asla tek başına yayın). Anlamları örtüşmüyor (K2 ajanslar T'de nereye düşer, sosyal sinyal T'de var mı); MM'de T2 "Şirket Basın".
6. **Otomatik yayın:** E1 "teyit yoksa otomatik yayın kapalı", kabul ölçütü "teyitsiz X/Facebook sinyali asla otomatik yayımlanmaz", B-17 açık; CLAUDE.md'deki "Otomatik yayınla" yalnızca güven skoru eşiğine dayanıyor. Koşullar Yasin Bey ile netleşecek.
7. **Teyit gösterimi:** sitede "Teyitli" ve kaynak sayısı gizli (Beyar kararı); panelde gösterilecek. Teyit kaydının veri modeli (iki bağımsız kaynak, resmî/ajans teyidi) panelde nasıl puanlanıp görüneceği belirsiz.
8. **Roller:** çekirdek PDF Super Admin / Admin / Moderator / Editor / Analyst; Dada PDF altı rol (Dada geçerli). Moderatör yok → yorum moderasyonu kimde? Mimari dokümanda ayrıca "Ses (muhabir/yaratıcı): kendi içeriği" rolü var; Dada listesinde yok. Spor/Kategori Editörü kapsamı ekran değil **veri düzeyinde** (kendi kategorisi) yetki istiyor.
9. **Rol ile izin grubu ilişkisi:** CLAUDE.md "görünürlük izin gruplarından ayarlanır" diyor; rol = izin grupları toplamı mı, yoksa izin grubu yalnızca alan/kutu görünürlüğü mü, belirsiz.
10. **Sosyal platformlar:** Dada PDF X, Facebook, LinkedIn, Instagram, Telegram; mimari X, Instagram, Facebook, Telegram, "Next Social"; 23 Kasım haritası WhatsApp kanalı, YouTube, TikTok; site footer'ı Instagram, YouTube, X, Facebook, LinkedIn, TikTok, WhatsApp, RSS.
11. **Kategori modeli:** 23 Kasım "her habere tek ana kategori"; MM düzenleme ekranında çoklu kategori; sitede 8 bölüm + 235 alt konu + Köşe; Keşfet konu listeleri (teknoloji, sağlık, kültür) ayrı bir küme.
12. **Bakım modu yeri:** çekirdek PDF'te Sistem Sağlığı, Dada PDF'inde Site Ayarları.
13. **Çöp kutusu:** kural zorunlu kılıyor ama hiçbir modül sahiplenmiyor; tek merkez mi, her listede "Çöp" sekmesi mi.
14. **Vitrin kapsamı:** PDF "sürükle-bırak manşet/vitrin sıralama"; sitede ana sayfa çok bölümlü (zebra bölümler, ayırıcılar, Süper Lig rayı). Yalnızca manşet mi, ana sayfa bölüm sırası da mı?
15. **Reklam alanları:** sitede yer tutucular kaldırıldı (C25), slot listesi ve ölçüleri tanımsız.
16. **Push:** "telefon ve web bildirimi" isteniyor; mobil uygulama web'den sonra (V-17); hedefleme takip (B-14) kararına bağlı; 2FA yöntemi (uygulama, e-posta, SMS) yazılı değil.
17. **Görsel ölçü kaynağı:** "ölçüler public sitenin ve mobil uygulamanın gerçek kullanımından gelir"; mobil uygulama yok. MM'de haber görseli 1400×650 (≈2.15:1) öneriliyor; sitede kart 16:10, detay 2.4:1.
18. **Dil:** Dada PDF Kontrol Paneli'nde "TR/EN dağılımı" istiyor; CLAUDE.md şimdilik yalnızca TR açık; B-07 bekliyor. Dil seçicide EN/AR/DE pasif "sonraki aşama" gösterilecek.
19. **Örnek veri sözlüğü panel alanlarını taşımıyor:** haber kaydında durum, görsel, spot, etiket, kaynak, SEO, AI skoru yok; kullanıcı, oturum, log, kaynak listesi, sosyal hesap yok. Public sözlüğü değiştirilemez; panele özgü örnek verinin yeri belirsiz.
20. **Referans kabuk ile CLAUDE.md farkları:** kabuk kırılımı 980/640 (bizde 1024/640); yerel `type=date`; toplu işlem, sıralama, iskelet, hata durumu yok; tablo CSS'i sayfalara kopyalanmış; rol değişimi yalnızca menüyü değiştiriyor; giriş ekranı yalnızca rol seçici; sabit renkler var; aksan rengi bölüme göre değişiyor (Dada Haber'de tek marka rengi mi, modül başına aksan mı?).
21. **Dada Gastro ile CLAUDE.md farkları:** satır tıklama yok, yerel tarih/telefon/e-posta, aranabilir liste yok, zorunlu işareti yok, kaydet çubuğu yapışkan değil, kaydedilmemiş değişiklik uyarısı yok. "Emsal" ile "istisnasız form standartları" çelişiyor; kural geçerli sayıldı.
22. **Marka:** kehribar `#FCB623` beyaz zeminde düşük kontrastlı (site metinde `#7A5F01` kullanıyor); panelde birincil düğme ve etkin menü rengi ayrıca seçilmeli. Site değişkenleri Türkçe adlı, referans kabuk İngilizce adlı (`--acc`, `--ink`); tema dosyası hangi adlandırmayla kurulacak?
23. **Logo:** CLAUDE.md "SVG ya da FA" diyor; Dada Haber logosu yalnızca PNG (sitede de SVG açık kalem).
24. **referans-09:** panel değil, public site oturumunun terminal görüntüsü; yanlış dosya olabilir.
25. **MM düzenleme ekranında dil sekmeleri her bölümde tekrar ediyor:** Beyar'ın "tek dil seçici" kuralı bunu bilerek aşıyor (çelişki değil, not).
26. **Hassas işlem listesi:** CLAUDE.md rol değişikliği, API anahtarı, toplu silme sayıyor; bakım modu, önbellek temizleme, otomatik yayın ayarı, yasal metin yayını da 2FA istesin mi belirsiz.
27. **Trafik verisinin kaynağı:** Kontrol Paneli'ndeki anlık trafik ve görüntülenme hangi kaynaktan (Analytics mi, kendi sayaç mı) belirsiz; panelde yalnızca örnek gösterilecek.
28. **Kurumsal metinler:** Hakkımızda, İletişim, Yardım Merkezi, Reklam, İnsan Kaynakları yasal metin değil; çekirdek Yasal modülünde mi yoksa ayrı bir "Sayfalar" ekranında mı yönetileceği belirsiz.
29. **Haber Dinle ve Spiker:** sesli içerik TTS ile otomatik mi (sitede tarayıcı sesiyle okunuyor), yoksa kayıtlı ses/video mu; panelde ne kadar yönetim gerektiği belirsiz.
30. **Deponun herkese açık/kapalı olması** (CLAUDE.md açık konu).

## 14 · Kararlar

K1–K19 Beyar tarafından verildi (24.11.2026); metinleri `docs/tasarim-kararlari.md` §1'de, bu dosyada ilgili yerlere işlendi. K1, K3, K7 ve K16 Yasin Bey'e de soruldu.

Bekleyen B kararlarından panel ekranını doğrudan etkileyenler: B-05 (Yazarlar/Sesler adı), B-07 (dil), B-12 (aile siteleri), B-14 (takip, push hedefi), B-16 (Dada'ya Sor), B-17 (editör onayı kapsamı), B-19 (ajans lisansı), B-24 (burç, hamilelik), B-25 (servisler), B-26 (resmî ilan, reklam), B-28 (AI görsel standardı ve etiketi).
