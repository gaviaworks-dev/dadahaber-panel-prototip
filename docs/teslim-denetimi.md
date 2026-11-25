# Modül teslim denetimi

> Yayılımda her modül teslim edilmeden önce bu listeyle denetlenir (CLAUDE.md "Tutarlılık" → Denetim). Sapma varsa modül değil sözleşme tartışılır, o da Beyar'la. Lead doldurur; her madde ✓ ya da gerekçeli ✗.
> Kaynak: `CLAUDE.md` (Tutarlılık, Arayüz kuralları, Form standartları), `docs/tasarim-kararlari.md`, UI kitteki etkileşim sözleşmesi.

Modül: ________ · Teammate: ________ · Tarih: ________

## 0 · Otomatik denetim (her teslimden önce, zorunlu)
- [ ] **Yayın kapısı (Beyar, 25.11.2026):** her commit + push'tan önce `python3 -I araclar/yayin_kapisi.py`. Denetimden geçmeyen sayfa kayıtta `hazir: false` olur ve menüden çıkar; kayıtta olmayan sayfa kalırsa yayın durur. Ölçüme eklenenler: liste görünümü değiştiricisinin (Kart · Liste) iki görünümü de ölçülür; tablo içi de kesik/binme ölçümüne girer; "…" ile kısaltılan kutuda rozet ya da düğme kesilirse kesik sayılır; `kart-duzen`: aynı listenin kartları farklı yükseklikteyse kaldı; onay penceresinde sağ üstte kapat düğmesi aranır.
- [ ] **25.11.2026 genişletme (Beyar):** `araclar/denetim.py` artık **beş genişlikte** (1440 · 1280 · 1024 · 768 · 390), her sekmede, açılan her çekmece/pencerede ve `?yeni=1` formunda gerçek tarayıcıda ölçer: **blok boşluğu ve binme** (bosluk-olc.js), **çekmece/pencere** başlığı, kapat ve alt çubuk görünürlüğü, yatay taşma (pencere-olc.js), **hiza** (satır, yan yana alan, kart/sayfa sol çizgisi), **kesilen içerik**, **seçenek grubu** (yalnız kalan kutu, iki satır sınırı), **sayfalama** (var mı, çalışıyor mu), **yapışkan sütun**, **yazım** ve **tarayıcı kutusu** (yerlesim-olc.js). `araclar/duyarli.py` ayrıca **bütün açılan kutuları** (menü, tarih, Filtreler, ⋯, renk) açıp ekranda mı, üst bar/kaydet çubuğuna biniyor mu, içerik kesiliyor mu ölçer. Yazım bulguları `python3 -I araclar/yazim.py --uygula` ile kaynakta düzeltilir. Ölçümden kalan çıkarsa sayfaya yama yazılmaz; ortak stilde düzeltilir.
- [ ] `python3 -I araclar/denetim.py <modül klasörü>` → **KALDI 0** (kural başına sonuç; ayrıntı `docs/screenshots/denetim-son.json`). "KARAR" satırları (pano, uzun sayfa önerisi) lead'e iletilir. Betiğin denetledikleri: JS hatası, yatay taşma (1440/390), **liste araç satırı** (tek satır, taşmasız, listede bir tane), **çift blok**, **uzun sayfa**, **kilitli düğme**, satır eylemleri sırası, Çöp sekmesi (yoksa nedeni bantta), **boşluk** (yapışık ipucu/kutu), bildirimin düğmeyi kapatması, zorunlu alan (?yeni=1), elle zorunlu/yıldız, tarayıcı tarih alanı, `<style>`, satır içi renk ve boşluk. Açık istisna yalnız `body[data-denetim-istisna]` + `data-denetim-neden` ile (lead onayı).
- [ ] `python3 -I araclar/duyarli.py <modül klasörü>` (yerelde) ve dalga sonunda `--taban https://gaviaworks-dev.github.io/dadahaber-panel-prototip` (canlıda) → 5 genişlikte sorun 0.

## 1 · Sök-tak
- [ ] Modül yalnızca kendi klasöründe; sayfaları `moduller.json`'da kayıtlı, `hazir` doğru.
- [ ] Kapatılınca menüden çıkıyor, `python3 -I araclar/menu_yaz.py --kontrol` sorun bildirmiyor (kırık bağlantı 0, kapalı modüle bağlantı 0).
- [ ] Başka modüle doğrudan bağ yok; bağımlılık kayıtta (`bagimli`), isteğe bağlı parçalar `data-modul` ile işaretli.
- [ ] Yeni görsel dil yok: yalnızca UI kitteki bileşenler; sayfada sabit renk ve modüle gömülü stil yok (satır içi stil yalnızca veri: görsel adresi, odak, yüzde).

## 2 · Yetenekler (aynı yerde, aynı görünümde)
- [ ] Kullandığı bütün bileşenler `cekirdek/bilesenler.json`'da "hazır"; `moduller.json` → `bilesenler` güncel (`menu_yaz.py --uyari` temiz).
- [ ] Sitede adresi olan içerikte SEO sekmesi.
- [ ] Uzun metin alanlarında aynı zengin metin editörü.
- [ ] Yayın zamanı olan içerikte aynı tarih-saat seçici (tarayıcının tarih alanı yok).
- [ ] Görseli olan içerikte aynı görsel alanı (web + mobil) ve kırpma penceresi; ölçüler kayıtta.
- [ ] Bildirimi ve paylaşımı anlamlı içerikte Bildirim ve Sosyal Medya sekmeleri.
- [ ] Metin alanı olan içerikte "Gerisini AI ile üret" adımı, başlık ve spotun altında; AI bölümleri onaylanana kadar işaretli.
- [ ] Dile bağlı alanı olan her formda en üstte tek dil seçici.

## 3 · Liste
- [ ] Satır eylemleri: görüntüle, düzenle, sil (bu sırada, bu ikonlarla); ek eylemler yalnızca ⋯ menüsünde, satırın durumuna göre.
- [ ] Satırın tamamı tıklanır; sonuç etkileşim sözleşmesindeki gibi.
- [ ] Durum sekmeleri + sağ uçta Çöp sekmesi; arama ve aranabilir süzgeçler; seçimde toplu işlem çubuğu.
- [ ] Boş, yükleniyor ve hata durumları.
- [ ] Yığılma ve satıra kırılma yok; dar ekranda sütun azalır ya da tablo yatay kayar.
- [ ] **Tek veri görünümü (Beyar, yasak):** aynı kayıt kümesi sayfada iki görünümde (takvim + liste, kart + liste, pano + liste) alt alta yok; ikinci görünüm aynı alanda görünüm değiştiriciyle (Ay · Hafta · Liste / Izgara · Liste). Sekme, arama ve süzgeç tek ve açık görünüme uygulanıyor; Çöp, toplu seçim ve satır eylemleri liste görünümünde. Farklı veri gösteren özet kutuları (sayaçlar) istisna.
- [ ] **Uzun sayfa yok:** sayfa birden çok büyük bloğu alt alta dizip birkaç ekran boyu uzamıyor; bloklar tek kartta sekmelere bölünmüş (sekmede sorun rozeti); sayfa başı düğmelerini tekrarlayan kutu yok.

## 4 · Eklenen düzenlenir ve silinir
- [ ] "Ekle" ya da "yeni" ile oluşan her şey (kayıt, formdan eklenen etiket, havuza yerinde eklenen değer, sekme içindeki satır, ayardaki öğe) **aynı ekrandan düzenlenebiliyor ve silinebiliyor**.
- [ ] Silme: ikinci onay → çöp → geri alınabilir.
- [ ] Başka kayıtlarca kullanılan öğe silinirken kaç yerde kullanıldığı gösteriliyor.
- [ ] İçinde kayıt olan öğe (kategori gibi) doğrudan silinmiyor; kayıtların taşınacağı yer seçiliyor, sonra çöpe gidiyor (B1).
- [ ] Formun içindeki küçük öğeler (çip, satır) onaysız kalkıyor ve "Geri al" var (B8).
- [ ] Havuzlu alanlarda havuz yerinde yönetiliyor: öneride ⋯ ile adını düzelt, sil, kullanım sayısı (B2). SEO anahtar kelimeleri havuzsuz.
- [ ] ⋯ menüsünde "ekle" eylemlerinin karşılığı "çıkar" olarak görünüyor (B6); kalıcı silme e-posta kodu istiyor (B5).
- [ ] Silinemeyen tek öğeler istisnalar (denetim izi, sistem logları, yasal metinlerin eski sürümleri, onay kayıtları) ve ekranda nedeni yazıyor.
- [ ] **Yapılamayan eylemin düğmesi yok:** tamamen kilitli listede satırda kilitli/pasif düğme çizilmiyor (görüntüle + ⋯; neden bantta); kilit yalnız çoğu düzenlenebilir listede tek/az satır için (hiza).
- [ ] **Liste araç satırı tek satır:** sekmeler + arama + en çok 2 süzgeç + Çöp aynı satırda (çekirdek toplar; sayfa ayrı satır kurmaz, süzgeç satırını tablodan sonra koymaz); 1440/1280/1024/768/390'da bölünmüyor.
- [ ] **Boşluk:** ipucu/açıklama ait olduğu öğeye yakın, sonraki gruba uzak; sayfada elle boşluk (satır içi margin/padding, ipucunda `kb-ust-bosluk`) yok.

## 5 · Form
- [ ] Telefon ülke kodlu ve maskeli, e-posta yazılırken doğrulanıyor.
- [ ] Havuzdan gelen değer (şehir, kategori, yazar, etiket, kaynak…) aranabilir listeden seçiliyor; yoksa aynı yerden ekleniyor.
- [ ] **Zorunlu alan ilkesi (CLAUDE.md Tutarlılık):** zorunlu yalnız o olmadan sitede bozuk görünecek ya da yayımlanamayacak alan; taslak için yalnız başlık/ad; sistemin doldurduğu (yazar, adres, yayın zamanı, SEO) ve AI'ın ürettiği alanlar zorunlu değil; editörün dolduracağı zorunlu ≤ 6 (fazlası Beyar'a gerekçeyle); zorunlular ilk sekmede ve formun üst kısmında.
- [ ] Zorunlu liste **modül kaydında** (`moduller.json` → `ayarlar.zorunlu.<form>` = `{taslak, yayin, sistem}`); sayfada form kabında `data-zorunlu-kayit="modul.form"`, alanlarda `data-alan-id`; sayfada elle `data-zorunlu` ya da yıldız yok.
- [ ] Zorunlu alan eksikken ana düğme pasif görünür ama tıklanabilir; tıklanınca eksik alan kırmızı çerçeve + neden + kaydırma; taslak düğmesi `data-kaydet-tur="taslak"` yalnız taslak listesini arar. Bildirim düğmelerin üstüne binmez.
- [ ] Gizli değerler maskeli; yalnızca oluşturma anında açık.
- [ ] Hassas işlemler e-posta koduyla (K15).

## 5b · Medya, AI ve yayın kuralları
- [ ] Görsel yüklemede etiketleme adımı (kategori, kişi/kurum, etiket); dış kaynaklı görsel havuza girmiyor (M1–M3); ardından kırpma.
- [ ] Medya seçici etiketle ve kısaltmayla arıyor, kategori ve kişiyle geziliyor (M4); kırpmada yalnız alanın oranları açıkta (M5).
- [ ] AI kaynaklı içerik: "AI · %güven" etiketi, görsel durumu (temiz / kırpıldı / görsel eksik), yayın kanalları gruptan (Y1, YS1–YS4).
- [ ] Onay gereken içerikte okuma onayı bileşeni, rol ayarına göre (Y2, Y3, YS5–YS7).
- [ ] Sosyal metin platformun kendi editör yetenekleriyle; @ ve # önerileri.

## 5c · Dalga 1'den eklenen kontroller
- [ ] Listelerde `data-liste-ad="…"` (tekil, küçük harf); metinlerde "haber" sabiti kalmadı.
- [ ] Onay ve e-posta kodu gereken işlemler pencerede (`data-onay-baslik` zinciri); onay sonrası satır durumu `data-sonra-durum`.
- [ ] Silinemez satırda `ia-btn kb-kilit disabled` + nedeni bantta; sayfası olmayan kayıtta satır tıklama "görüntüle" eylemini yapar.
- [ ] Sayfa `body[data-sayfa]` kayıttaki anahtarla; yetkisiz rol "yetki yok" kapısını görür.
- [ ] Teammate yalnız `menu_yaz.py --yalniz <klasör>` çalıştırdı; ortak dosyaya yazmadı; eksik bileşeni lead'e bildirdi.

## 6 · Yerleşim ve erişim
- [ ] Sayfa başlığı, sağ üst eylemler, süzgeç çubuğu, sekmeler, yan panel ve kaydet çubuğu yerinde.
- [ ] Tek kapat (×); yıkıcı işlem üstüne gelince kırmızı; ikincil kontroller çan gibi tepki veriyor.
- [ ] Rol değiştiricide her rol yalnızca yetkili menüyü, işlemi ve kutuyu görüyor (alan ve kutu düzeyinde).
- [ ] 360, 768, 1024, 1440 genişlikte taşma yok; dokunma alanı en az 44 px.
- [ ] Tek `<h1>`, seviye atlanmıyor; sayılar eşit genişlikli; tarih biçimi `24.11.2026 14.30`.
- [ ] Örnek içerik veri sözlüğünden; lorem ipsum, gerçek anahtar ve kişisel veri yok.
- [ ] Sayfa içi JS hatası yok.


---

## Dalga 1 denetim sonucu (24.11.2026)

| Modül | Teammate | Sayfa | Sök-tak / kayıt | JS | Taşma (4 genişlik) | Zorunlu alan ilkesi | Bileşen kaydı |
|---|---|---|---|---|---|---|---|
| Kimlik ve Yetki | d1-kimlik | 17 | ✓ | ✓ | ✓ 4 genişlik | ✓ 7 form (`kimlik-yetki.rol`, `.izin-grubu`, `.profil`, `.giris`, `.sifremi-unuttum`, `.yeni-sifre`, `.davet-kabul`) | ✓ |
| Kullanıcılar | d1-kimlik | 5 | ✓ | ✓ | ✓ 4 genişlik | ✓ 5 form (`kullanicilar.davet`, `.uye`, `.uye-durum`, `.okur`, `.okur-durum`) | ✓ |
| Denetim İzi | d1-denetim | 4 | ✓ | ✓ | ✓ | ✓ (form yok) | ✓ |
| Raporlar | d1-denetim | 2 | ✓ | ✓ | ✓ | ✓ `raporlar.disa-aktarim` | ✓ |
| Yasal Metinler | d1-yasal | 4 | ✓ | ✓ | ✓ 44/44 | ✓ `yasal-metinler.metin` (2 alan) | ✓ |
| Sayfalar | d1-yasal | 2 | ✓ | ✓ | ✓ | ✓ `sayfalar.sayfa` (2 alan) | ✓ |
| Entegrasyonlar | d1-entegrasyon | 3 | ✓ | ✓ | ✓ 20/20 | ✓ `entegrasyonlar.ayar`, `.anahtar` (2+2) | ✓ |
| Sistem Sağlığı | d1-entegrasyon | 2 | ✓ | ✓ | ✓ | ✓ (form yok) | ✓ |

- Lead denetimi: `menu_yaz.py --kontrol` 0 sorun (kırık bağlantı yok); 44 sayfada JS hatası 0; kayıtta 20 formun zorunlu listesi, hiçbirinde 5'ten fazla zorunlu yok; sayfalarda elle `data-zorunlu`/yıldız 0.
- Bilinçli istisnalar (ekranda nedeni yazıyor): denetim izi ve loglar silinemez (Çöp yok); cron görevleri kodda tanımlı (silinmez); API anahtarı çöpe değil "İptal edildi"ye geçer; yasal metnin eski sürümleri ve onay kayıtları silinemez.


---

## Dalga 2 denetim sonucu (24.11.2026)

| Modül | Teammate | Sayfa | Sök-tak / kayıt | JS | Taşma (4 genişlik) | Zorunlu alan ilkesi | Bileşen kaydı |
|---|---|---|---|---|---|---|---|
| Haberler kalanları | d2-haberler | 11 | ✓ | ✓ | ✓ 19 adres | ✓ 8 form (`son-dakika`, `canli`, `canli-giris`, `dosya`, `gunun-5`, `inceleme` 6 alan sınırda, `yazar`, `surum-notu`) | ✓ |
| AI Haber Havuzu | d2-ai | 6 | ✓ | ✓ | ✓ | ✓ 3 form (`kaynak`, `grup`, `reddet`) + düzenlemede `haberler.haber` | ✓ |
| Multimedya ve Medya Havuzu | d2-medya | 14 | ✓ | ✓ | ✓ | ✓ 9 form (`video`, `akis`, `canli`, `seri`, `bolum`, `sesli`, `galeri`, `infografik`, `varlik`) | ✓ |
| Sosyal Medya Merkezi | d2-sosyal | 4 | ✓ | ✓ | ✓ | ✓ 3 form (`gonderi`, `hizli`, `hesap`) | ✓ |

- Lead denetimi: statik kurallar (`<style>` yok, sabit renk yok, elle yıldız/`data-zorunlu` yok, tarayıcı tarih alanı yok, tek `<h1>`, `data-sayfa` kayıtta, zorunlu alan kimlikleri sayfada) + tarayıcıda 360/768/1024/1440 taşma ve JS hatası; `menu_yaz.py --kontrol` 0 sorun. Ekran görüntüsüyle görünüm kontrolü (vitrin, AI havuzu, kaynak motoru, gönderi, takvim, medya havuzu, galeri).
- Denetimde düzeltilenler: vitrin ve Günün 5'i havuzdan sıralı listeye geçti; reddet nedeni pencereye taşındı; ⋯ "Onayla ve yayınla" görseli eksik satırda gizli; yazar fotoğrafı oran sınıfı; sosyal oranlar kayıtla eşitlendi; kategori formundaki elle yıldız kaldırıldı.
- Bilinçli istisnalar: haber sürümleri silinmez (varsayım); cron görevleri silinmez; Sosyal gönderide AI adımı yok (varsayım).
- Çekirdeğe Dalga 2'de eklenenler kararlar dosyasında ("Dalga 2 öncesi …" ve "Dalga 2 sırasında …").


---

## Dalga 3 denetim sonucu (24.11.2026)

| Modül | Teammate | Sayfa | Sök-tak / kayıt | JS | Taşma (4 genişlik) | Zorunlu alan ilkesi | Bileşen kaydı |
|---|---|---|---|---|---|---|---|
| Etkileşim | d2-sosyal (d3-etkilesim) | 8 | ✓ (kapatılınca sorun 0) | ✓ | ✓ | ✓ 6 form (`yanit`, `bulten`, `bulten-turu`, `test`, `push`, `reklam` — editör zorunlusu en çok 5) | ✓ |
| Özel Widgetlar | d2-ai (d3-dikey) | 6 | ✓ (kapatılınca sorun 0) | ✓ | ✓ | ✓ 4 form (`kulup`, `takvim`, `ilan`, `duzeltme`) | ✓ |

- Satır içi renkler yalnız veri (kulüp kurumsal rengi); kural gereği izinli.
- Rol kapısı: Editör yalnız Yorumlar, Geri bildirimler ve Takvimler'i görüyor; diğerlerinde "yetki yok".
- Bilinçli istisnalar: KVKK başvuruları, API verisi (puan tablosu, maçlar), bildirim kayıtları silinmez; nedeni ekranda.

## Son tam denetim (24.11.2026)

- **Kayıt:** `menu_yaz.py --kontrol --uyari` 0 sorun; açık 16 modülün bütün sayfaları `hazir:true`; "yapım aşamasında" sayfasına giden bağlantı yalnız bildirim merkezi tamamlanana kadar.
- **Taşma ve JS:** 94 sayfa × 360 / 768 / 1440 → taşma 0, JS hatası 0, her sayfada tek `<h1>`, tarayıcı tarih alanı 0.
- **Sök-tak:** `araclar/sok_tak.py` (Sosyal Medya kapatılır, sayılır, bağımlılık reddi denenir, geri açılır); her yaprak modül ayrıca kapatılarak denetlendi.
