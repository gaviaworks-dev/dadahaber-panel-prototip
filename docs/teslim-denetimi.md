# Modül teslim denetimi

> Yayılımda her modül teslim edilmeden önce bu listeyle denetlenir (CLAUDE.md "Tutarlılık" → Denetim). Sapma varsa modül değil sözleşme tartışılır, o da Beyar'la. Lead doldurur; her madde ✓ ya da gerekçeli ✗.
> Kaynak: `CLAUDE.md` (Tutarlılık, Arayüz kuralları, Form standartları), `docs/tasarim-kararlari.md`, UI kitteki etkileşim sözleşmesi.

Modül: ________ · Teammate: ________ · Tarih: ________

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

## 4 · Eklenen düzenlenir ve silinir
- [ ] "Ekle" ya da "yeni" ile oluşan her şey (kayıt, formdan eklenen etiket, havuza yerinde eklenen değer, sekme içindeki satır, ayardaki öğe) **aynı ekrandan düzenlenebiliyor ve silinebiliyor**.
- [ ] Silme: ikinci onay → çöp → geri alınabilir.
- [ ] Başka kayıtlarca kullanılan öğe silinirken kaç yerde kullanıldığı gösteriliyor.
- [ ] İçinde kayıt olan öğe (kategori gibi) doğrudan silinmiyor; kayıtların taşınacağı yer seçiliyor, sonra çöpe gidiyor (B1).
- [ ] Formun içindeki küçük öğeler (çip, satır) onaysız kalkıyor ve "Geri al" var (B8).
- [ ] Havuzlu alanlarda havuz yerinde yönetiliyor: öneride ⋯ ile adını düzelt, sil, kullanım sayısı (B2). SEO anahtar kelimeleri havuzsuz.
- [ ] ⋯ menüsünde "ekle" eylemlerinin karşılığı "çıkar" olarak görünüyor (B6); kalıcı silme e-posta kodu istiyor (B5).
- [ ] Silinemeyen tek öğeler istisnalar (denetim izi, sistem logları, yasal metinlerin eski sürümleri, onay kayıtları) ve ekranda nedeni yazıyor.

## 5 · Form
- [ ] Telefon ülke kodlu ve maskeli, e-posta yazılırken doğrulanıyor.
- [ ] Havuzdan gelen değer (şehir, kategori, yazar, etiket, kaynak…) aranabilir listeden seçiliyor; yoksa aynı yerden ekleniyor.
- [ ] Zorunlu alan doğrulaması, hatalı sekme işareti, kaydet çubuğu ve "kaydedildi" durumu.
- [ ] Gizli değerler maskeli; yalnızca oluşturma anında açık.
- [ ] Hassas işlemler e-posta koduyla (K15).

## 5b · Medya, AI ve yayın kuralları
- [ ] Görsel yüklemede etiketleme adımı (kategori, kişi/kurum, etiket); dış kaynaklı görsel havuza girmiyor (M1–M3); ardından kırpma.
- [ ] Medya seçici etiketle ve kısaltmayla arıyor, kategori ve kişiyle geziliyor (M4); kırpmada yalnız alanın oranları açıkta (M5).
- [ ] AI kaynaklı içerik: "AI · %güven" etiketi, görsel durumu (temiz / kırpıldı / görsel eksik), yayın kanalları gruptan (Y1, YS1–YS4).
- [ ] Onay gereken içerikte okuma onayı bileşeni, rol ayarına göre (Y2, Y3, YS5–YS7).
- [ ] Sosyal metin platformun kendi editör yetenekleriyle; @ ve # önerileri.

## 6 · Yerleşim ve erişim
- [ ] Sayfa başlığı, sağ üst eylemler, süzgeç çubuğu, sekmeler, yan panel ve kaydet çubuğu yerinde.
- [ ] Tek kapat (×); yıkıcı işlem üstüne gelince kırmızı; ikincil kontroller çan gibi tepki veriyor.
- [ ] Rol değiştiricide her rol yalnızca yetkili menüyü, işlemi ve kutuyu görüyor (alan ve kutu düzeyinde).
- [ ] 360, 768, 1024, 1440 genişlikte taşma yok; dokunma alanı en az 44 px.
- [ ] Tek `<h1>`, seviye atlanmıyor; sayılar eşit genişlikli; tarih biçimi `24.11.2026 14.30`.
- [ ] Örnek içerik veri sözlüğünden; lorem ipsum, gerçek anahtar ve kişisel veri yok.
- [ ] Sayfa içi JS hatası yok.
