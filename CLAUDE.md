# Dada Haber — Yönetim Paneli Prototipi

Bu depo yalnızca **yönetim paneli (back-office) arayüz prototipidir**: statik HTML, CSS ve JS; build adımı yok, göreli yollar. Backend, veritabanı, API ve gerçek giriş burada yoktur.

## Rolün

Yönetim panelinin arayüz tasarımcısı ve frontend mimarısın. İşin tek bir panel çizmek değil, **sök-tak bir panel sistemi** kurmak: her projede aynen kullanılacak bir çekirdek ve projeye göre takılıp çıkarılan modüller. Bu panel ileride türü ne olursa olsun başka projelere miras verilecek; her proje çekirdeği aynen alır ve yalnızca kendi ihtiyacı olan modülleri takar. Haberler, buradaki modüllerden yalnızca biridir; sistem herhangi bir modül türünü taşıyacak şekilde kurulur.

- **Kullanıcı:** editör, yayın yönetmeni, sosyal medya uzmanı, analist, sistem yöneticisi. Gün boyu panelde çalışan insanlar. Güzellik, kullanışlılık ve arayüz tasarımı önemlidir: panel hızlı ve net olduğu kadar özenli ve göze hoş da olmalı; "nasılsa iç araç" diye tasarımdan ödün verilmez.
- **Karar sahibi Beyar'dır; karar verici Yasin Bey'dir.** Sen önerir ve seçtirirsin; verilmemiş kararı verilmiş sayma.

## Bu deponun yeri

1. Public site prototipi ayrı depodadır: `/Users/gaviaworks/Developer/Projects/dadahaber-prototip`. O depoyu **yalnızca okursun**, asla değiştirmezsin.
2. Bu panel, o sitedeki her içerik türünün yönetim ekranını karşılar. Panelde olmayan bir içerik türü sitede yayımlanamaz; sitede olmayan bir alan panelde sorulmaz.
3. Oturan panel sonra full-stack depoya **birebir aktarılır**; yalnızca statik içerik dinamik değişkenle değişir. Yapı, sınıf adları ve bileşen sınırları temiz ve kararlı olmalı.

## Kaynaklar

`docs/kaynak/` altında:

1. `Yönetim Paneli (Back-Office) Teknik Modül Spesifikasyonu.pdf` — **her projede zorunlu** 8 çekirdek modül ve güvenlik standartları.
2. `Dada Haber — Kapsamlı Yönetim Paneli (Back-Office) Teknik Modül Mimarisi.pdf` — Dada Haber'e özgü 8 katman ve alt modüller.
3. `DADAHABER-02-kullanici-akislari.md` (E1–E5 editör ve yönetici akışları), `DADAHABER-03-mimari.md`, `DADAHABER-05-kararlar.md`.

Public depodan okunacaklar (kopyalama, yerinden oku):
- `docs/sayfa-envanteri.md` ve `docs/tasarim-kararlari.md`: sitede hangi içerik türleri ve alanlar var.
- `araclar/ornek_veri.json`: örnek veri sözlüğü. Paneldeki örnek haberler, yazarlar, kategoriler ve sayılar **buradan** gelir; panel ile site aynı içeriği gösterir.
- `assets/css/degiskenler.css`: marka değişkenleri (renk, font, köşe).

İki PDF çelişirse Dada Haber'e özgü olan geçerlidir; ikisinin de susması halinde Beyar'a sor.

## Mimari: çekirdek ve modüller

**Çekirdek (her projede aynen bulunur)**
- Kabuk: yan menü, üst bar, arama, bildirim, hesap menüsü, rol değiştirici.
- Ortak bileşenler: veri tablosu (arama, filtre, sıralama, sayfalama, toplu işlem), form alanları, sekmeli düzenleme sayfası, medya seçici, görsel kırpma, zengin metin alanı, onay diyaloğu, bildirim, boş, yükleniyor ve hata durumları, durum rozetleri, tarih ve saat seçici.
- 8 zorunlu modül: Kimlik ve Yetki (roller, izin matrisi, 2FA, oturumlar) · Kullanıcılar · Site Ayarları ve Özellik Anahtarları · Denetim İzi ve Sistem Logları · Raporlama ve Dışa Aktarım · Yasal Metin Sürümleri · Sistem Sağlığı ve Bakım · Entegrasyonlar ve API Anahtarları.

**Proje modülleri (Dada Haber)**
- Kontrol Paneli · Haberler ve Vitrin (manşet, son dakika, köşe yazısı, röportaj, kategori ve etiket yönetimi, yazarlar) · Multimedya ve Medya Havuzu (video, kısa video, infografik, galeri, podcast, stok havuzu, marka şablonu) · Özel Dikeyler (spor, etkinlik takvimi, anket, sözlük, firma rehberi, piyasa ve hava) · AI Haber Havuzu ve Kaynak Motoru · Sosyal Medya Merkezi · Etkileşim (yorum, e-bülten, push, reklam alanları).

**Modül sözleşmesi (sök-tak kuralı)**
- Her modül kendi klasöründe durur; sayfaları, örnek verisi ve modüle özgü parçaları oradadır.
- Tek bir modül kaydı dosyası vardır (`moduller.json`): modülün adı, grubu, ikonu, sırası, sayfaları, kullandığı ortak bileşenler, bağımlı olduğu modüller, açık ya da kapalı olduğu, hangi rollerin gördüğü.
- Yan menü bu dosyadan üretilir; elle yazılmaz. Bir modül kapatılınca menüden çıkar ve hiçbir yerde kırık bağlantı kalmaz.
- Modüller birbirine doğrudan bağlanmaz; bağımlılık kayıt dosyasında yazılıdır. Çekirdek hiçbir proje modülüne bağımlı değildir.
- Modül yeni görsel dil üretmez; yalnızca ortak bileşenleri kullanır. Eksik bileşen çekirdeğe eklenir, modülün içine gömülmez.
- **Tema tek dosyadır:** logo ve marka değişkenleri değişince panel başka bir projenin paneli olur. Sayfalarda sabit renk yazılmaz.

Bu sözleşmenin çalıştığını prototipte kanıtla: bir modülü kayıttan kapatıp menünün ve bağlantıların bozulmadığını göster.

## Referans kabuk

- Kabuk, DadaMutfak V7 süper admin panelinin aynısıdır: `by4r.github.io/dadamutfak-view/v7-6cu356/sa-shell.html?role=super` (yerelde `dadamutfak-view` deposunu ara). Yasin Bey bu paneli beğendi; yapı, yoğunluk, kart ve tablo dili oradan **birebir** alınır.
- Farklar: **solda ikon rayı (rail) yok**, yalnızca yan menü var; renk ve logo Dada Haber'in; menü gruplamaları Dada Haber dokümanındaki 8 katmandan gelir.
- **Projeden projeye yalnızca renk ve logo değişir.** Yazı tipi, köşe yuvarlaklığı, boşluk ölçeği ve bileşen dili panelin kendisine aittir; referans kabuktan ve Dada Gastro yönetim panelinden alınır. Public sitenin yazı tipi (Gilroy) ve köşe değerleri panele taşınmaz. Tema dosyası bu yüzden yalnızca renk ve logo taşır.
- Form ve liste ekranlarında Dada Gastro yönetim panelindeki form ve liste standardına da bak; emsal odur.
- Bu kendi işimizdir, kopyalamak serbesttir. Başka şirketlerin panel tasarımı kopyalanmaz.

## Yasin Bey'in dokümanlarından gelen kurallar

- **Çok adımlı onay zinciri yok.** Değişiklikler doğrudan yayına yansır. Bu yüzden her kritik işlemde: ikinci onay diyaloğu, kalıcı silme yerine geri alınabilir silme (çöp kutusu), ve işlemin denetim izinde önceki ve sonraki haliyle görünmesi.
- **AI haber havuzu tek adımlıdır:** Taslak, Yayınlanan, Reddedilen sekmeleri; güven skoru, kaynak, kategori önerisi, "Görsel Eksik" uyarısı; toplu onayla ve toplu reddet.
- **Gizli değerler maskelidir:** API anahtarı, token ve secret oluşturma anı dışında açık gösterilmez.
- **Yetki sınırı:** hiçbir yönetici kendi seviyesinin üstünde rol atayamaz; panel girişinde 2FA zorunludur.
- **Dil:** yapı çok dillidir (içerik formunda dil sekmesi, hesaplarda dil ayrımı), ama şimdilik yalnızca Türkçe açıktır. Çeviri ekranları tasarlanır, "sonraki aşama" olarak işaretlenir. Denetimsiz çeviri yayımlanmaz.
- **Roller:** Süper Admin, Genel Yayın Yönetmeni, Editör, Spor/Kategori Editörü, Sosyal Medya Uzmanı, Analist. Prototipte rol değiştirici olur; her rol yalnızca yetkili olduğu menüyü ve işlemi görür.

## Panel gereksinimleri (Beyar)

En önemli ölçüt **kullanım kolaylığıdır.** Aşağıdakiler bütün modüller için geçerlidir.

**İşlev referansları (görünüm referansı değil)**
- Milli Müdafaa yönetim paneli: Otomatik Haberler, Kaynaklar, Frekans Ayarları, Cron Sağlık, Sosyal Medya Hesapları ve haber düzenleme sekmeleri. Ekran görüntüleri `docs/referans/` altındadır. Bunlar **neyin olması gerektiğini** gösterir; aylar önce yapıldı, görünümü aşılacak. Aynısını yapma, daha iyisini yap.
- Görsel kırpma için İsmail Turgut Öksüz panelindeki "Görseli Kırp" penceresi: başlangıç noktasıdır, çok daha gelişmişi kurulacak.

**Görsel ve kırpma sistemi (çekirdek bileşen; çok önemli)**
- Her görsel alanında **web** ve **mobil** için ayrı bölüm vardır. Web görseli yüklenince mobil görsel ondan otomatik kırpılır; istenirse mobil için ayrı görsel yüklenir. Tersi de geçerlidir.
- Her modülün her görsel alanının **önerilen ölçüsü ve oranı** modül kaydında tanımlıdır ve tutarlıdır: haber kapağı, podcast kapağı, banner, yazar fotoğrafı farklı ölçü ister. Ölçüler public sitenin ve mobil uygulamanın gerçek kullanımından gelir.
- Varsayılan kırpma düzgün gelir: odak noktası seçilir, bütün oranlar ona göre otomatik hizalanır; editör yalnızca gerekirse düzeltir.
- Oran ön ayarları, yakınlaştırma, sıfırlama, "kırpmadan kullan" ve **canlı önizleme** vardır: görsel sitedeki kartta, mobil kartta ve sosyal medya kartında nasıl duracak, aynı pencerede görünür.
- Sosyal medya için platform oranları hazırdır (16:9, 1:1, 4:5, 1.91:1, serbest) ve platformun önerdiği piksel ölçüsü yazar.

**İçerik düzenleme ekranı**
- Sekmeler: Detay, SEO, Bildirim (telefon ve web bildirimi), Sosyal Medya.
- **Dil seçimi tek ve doğru yerdedir:** formun üstünde tek bir dil seçici bulunur ve dile bağlı bütün alanları birlikte değiştirir; her bölümde ayrı ayrı tekrarlanmaz. Dile bağlı olmayan alanlar (görsel, yazar, kategori) seçiciden etkilenmez.
- **SEO otomatik üretilir** (başlık, açıklama, anahtar kelimeler, adres); editör düzeltebilir. Karakter sayaçları görünür.
- Bildirim sekmesi: başlık ve içerik için karakter sınırı ve sayaç, bildirim görseli, gönderim zamanı, telefonda nasıl görüneceğinin önizlemesi.
- İçerik ve açıklama alanları **zengin metin editörlüdür**; güncel, kaliteli bir editör kullanılır.
- Sosyal Medya sekmesi: platform sekmeleri, platforma özel metin, karakter ve bağlantı sayacı, oran seçici ve kırpma, hesap durumu, hemen ya da zamanlı yayın, gerçeğe yakın canlı kart önizlemesi. Bu ekranın tasarım kalitesi özellikle önemlidir.

**Form standartları (istisnasız)**
- Tarih ve saat için her yerde özel tarih seçici kullanılır; tarayıcının varsayılan tarih alanı **asla** kullanılmaz.
- Telefon ve e-posta alanları biçimlidir: telefon ülke koduyla ve maskeyle girilir, e-posta yazılırken doğrulanır.
- Şehir, kategori, yazar, etiket, kaynak gibi bir havuzdan gelen hiçbir değer düz metin olarak girilmez; aranabilir açılır listeden seçilir. Havuzda yoksa aynı yerden eklenir.

**Gezinme**
- Yan menü sade kalır. Bir modülün alt tanımları yan menüde ayrı kalem olmaz: örneğin haber kategorileri, Haberler liste ekranının sağ üstündeki düğmeden açılır ve orada yönetilir.

**AI haber havuzu**
- Düzenleme ekranında **kaynak teyitleri ve alternatif kaynaklar** görünür: haberin geldiği kaynak, katmanı, aynı olayı veren diğer kaynaklar ve bağlantıları.
- Ayarlarda **"Otomatik yayınla"** anahtarı bulunur: açıkken güven skoru belirlenen eşiğin üstündeki AI haberleri editör onayı beklemeden yayımlanır; altındakiler kuyrukta kalır. Eşik aynı ekranda ayarlanır. Otomatik yayımlanan her haber listede ve denetim izinde "otomatik yayımlandı" olarak işaretlenir. Bu ayarın koşulları (hangi kaynak katmanları, hangi kategoriler, görseli eksik haber) için bkz. "Açık konular".

**İzinler**
- Maliyet, token ve fiyat bilgileri, cron ve sistem sağlığı gibi teknik ve mali alanlar editörlere görünmez. Görünürlük ekran düzeyinde değil **alan ve kutu düzeyinde** izinle yönetilir ve izin gruplarından ayarlanır.

**Sistem**
- Bakım modu kesinlikle vardır. Entegrasyon ekranları özenli ve anlaşılır olur: her bağlantının durumu, son kullanım zamanı ve hatası tek bakışta görünür.

## Giriş ve oturum kuralları (Beyar)

- **"Beni hatırla" kesinlikle çalışır.** Panel kullanıcısı her girişte kullanıcı adı ve şifre yazmak zorunda kalmaz: kutu işaretliyse oturum açık kalır; oturum düşmüşse giriş ekranında bilgiler dolu gelir ve tek tıkla "Giriş Yap" denir.
- **2FA ile birlikte:** iki adımlı doğrulama zorunludur, ama hatırlanan cihazda her girişte yeniden sorulmaz; yeni cihazda ve hassas işlemlerde (rol değişikliği, API anahtarı, toplu silme) sorulur. Kullanıcı "Aktif oturumlar" ekranından hatırlanan cihazları görür ve tek tek kapatabilir.
- **E-posta doğrulama:** ilk kurulumdaki Süper Admin hesabı doğrulanmış sayılır. Sonradan eklenen her ekip üyesi (editör ve diğer roller) için e-postasına onay bağlantısı gider; e-postasını onaylamadan panele giremez. Akış: yönetici kullanıcıyı ekler → davet ve onay e-postası gider → kullanıcı onaylar ve şifresini belirler → ilk girişte 2FA kurar.
- Kullanıcılar ekranında doğrulama durumu görünür (bekliyor, onaylandı, süresi doldu) ve "onay e-postasını yeniden gönder" işlemi vardır.
- Prototipte: giriş ekranı örnek bilgilerle dolu ve "Beni hatırla" işaretli gelir; Beyar yalnızca "Giriş Yap"a basar. Davet, onay e-postası, şifre belirleme ve 2FA kurulum ekranları da ayrı ayrı gösterilir.

## Çalışma sırası

1. **Keşif ve modül envanteri:** iki PDF'i, referans kabuğu ve public deponun envanterini incele. Her modül için ekran listesini çıkar (liste, düzenleme, ayar, rapor, açılır pencere). **DUR, onay bekle.**
2. **Kabuk:** yan menü, üst bar, rol değiştirici, Kontrol Paneli. Parça parça, seçtirerek.
3. **Pilot modül: Haberler, baştan sona.** Liste, düzenleme (Detay, SEO, Bildirim, Sosyal Medya sekmeleri), kırpma sistemi, kategoriler, tarih seçici, havuzdan seçim. Ortak parçaların hepsi gerçek bir modülün içinde, seçtirerek oturtulur.
4. **İkinci kalıp: Site Ayarları** ve özellik anahtarları (ayar ekranı kalıbı, bakım modu, maskeli alanlar).
5. **Seçtirerek ilerleme** (2-4. adımlar boyunca): kabuk hazır geldiği için yalnızca belirsiz parçalar sorulur. Her soruda 2-3 seçenek, kaynağı, artısı ve eksisi, tek tavsiye; **her mesajda tek soru.** Sözle anlaşılmayan parça `secenekler/` altında yan yana önizlemeyle seçtirilir. Her seçim `docs/tasarim-kararlari.md` dosyasına yazılır.
6. **Dondurma ve UI kit:** ortak bileşenler adlandırılır ve tek yere çıkarılır; **`ui-kit.html`** sayfası üretilir: renkler, yazı ölçeği, düğmeler, form alanları, tablo, sekmeler, pencereler, önizlemeler ve her bileşenin bütün durumları tek sayfada. Aynı sayfada **etkileşim sözleşmesi** yazılı durur (bkz. "Tutarlılık"). Modül sözleşmesi çalışır hale gelir; bir modül kapatılarak sök-tak kanıtlanır. Beyar UI kiti onaylar. **Bu noktadan sonra ortak bileşene ya da etkileşim sözleşmesine dokunmak Beyar'ın onayına bağlıdır.**
7. **Yayılım:** önce çekirdek modüller, sonra Dada Haber modülleri. Modüller yalnızca UI kitteki bileşenlerle kurulur; her modülde yalnızca o modüle özgü olan sorulur, ortak kararlar yeniden açılmaz. Onay gelmeden yayılıma geçme.

## Tutarlılık (Beyar; çok önemli)

Aynı iş her modülde aynı biçimde yapılır. Bir modülde olan bir yetenek, onu gerektiren her modülde aynı yerde ve aynı görünümde bulunur.

- **Yetenekler:** yayımlanan ve sitede adresi olan her içerik türünde SEO sekmesi vardır (haber, video, podcast, galeri, yazar, kategori, dosya). Uzun metin alanı olan her yerde aynı zengin metin editörü kullanılır (haber gövdesi de, podcast açıklaması da). Yayın zamanı olan her içerikte aynı zamanlama (özel tarih-saat seçici) vardır. Görseli olan her içerikte aynı görsel alanı ve kırpma penceresi vardır. Bildirim ve Sosyal Medya sekmeleri, bildirimi ve paylaşımı anlamlı olan her içerik türünde aynı biçimde bulunur.
- **Liste satırı eylemleri:** her listede aynı eylem seti, aynı sırada ve aynı ikonla durur: görüntüle, düzenle, sil. Modüle özgü ek eylem gerekiyorsa aynı "diğer" menüsüne girer; satıra dağınık düğme eklenmez.
- **Eklenebilen her şey düzenlenebilir ve silinebilir.** Panelde "ekle" ya da "yeni" ile oluşturulabilen her kayıt (listedeki kayıt, formun içinden eklenen etiket, havuza yerinde eklenen değer, sekme içindeki satır, ayarlardaki öğe) aynı ekrandan düzenlenebilir ve silinebilir olur. Silme her yerde aynı işler: ikinci onay, çöpe gider, geri alınabilir. Başka kayıtlarca kullanılan bir şey silinirken kaç yerde kullanıldığı gösterilir. İstisnalar yalnızca şunlardır ve ekranda neden silinemediği yazar: denetim izi, sistem logları, yasal metinlerin eski sürümleri ve onay kayıtları.
- **Zorunlu alan ilkesi.** Bir alan ancak o olmadan içerik sitede bozuk görünecekse ya da yayımlanamayacaksa zorunludur; "olsa iyi olur" alanı zorunlu yapılmaz. Taslak kaydetmek için yalnızca başlık ya da ad gerekir; zorunlu alanlar yayımlarken aranır. Sistemin doldurabildiği alan (yazar, adres, yayın zamanı, SEO) boş gelmez ve eksik olarak gösterilmez. AI'ın ürettiği alanlar (özet maddeleri, SEO, bildirim ve sosyal medya metinleri) zorunlu değildir. Bir formda yayımlamak için editörün dolduracağı zorunlu alan sayısı 6'yı geçmez; geçmesi gerekiyorsa gerekçesiyle Beyar'a sorulur. Zorunlu alanlar ilk sekmede ve formun üst kısmında durur. Hangi alanın zorunlu olduğu sayfada değil modül kaydında tanımlanır. İçerik türlerinin ortak zorunluları: ad ya da başlık, ana kategori (kategorisi olan türlerde), kapak görseli (sitede kartı olan türlerde) ve türün asıl içeriği (haberde metin, videoda video, podcast bölümünde ses dosyası, galeride en az bir görsel). Haberde: başlık, spot, haber metni, ana kategori, kapak görseli.
- **Zorunlu alan eksikken düğme davranışı.** Ana düğme pasif görünür ama tıklanabilir kalır; tıklanınca eksik alan kırmızı çerçeveyle işaretlenir, altına ne eksik olduğu yazar, ekran o alana kayar. Bildirim hiçbir ekranda düğmelerin üstüne binmez.
- **Etkileşim:** aynı tür tıklama her modülde aynı sonucu verir. Bir listede satıra tıklamak sayfa açıyorsa bütün listelerde sayfa açar; birinde yandan çekmece, diğerinde pencere, bir başkasında yeni sayfa olmaz. Hangi iş sayfada, hangisi çekmecede, hangisi pencerede yapılır kuralı pilot modülde bir kez seçtirilir, UI kitteki etkileşim sözleşmesine yazılır ve her modül ona uyar.
- **Yerleşim:** sayfa başlığı, sağ üst eylemler, süzgeç çubuğu, sekmeler, yan panel ve kaydet çubuğu her ekranda aynı yerdedir.
- **Denetim:** yayılımda her modül teslim edilmeden önce bu sözleşmeye göre denetlenir; sapma varsa modül değil sözleşme tartışılır, o da Beyar'la.

## Arayüz kuralları

- **Yığılma ve satıra kırılma yok** (Yasin Bey). Tabloda aynı türden bilgi tek satırda kalır; sığmayan sütun kısaltılır, gizlenir ya da tablo yatay kayar. Sağı boş kalan, satırı ziyan eden düzen olmaz; gereksiz satır açılmaz.
- **Panel kesinlikle responsive'dir:** masaüstü, tablet ve telefon; kaliteli ve tutarlı bir standartla. Kırılımlar public siteyle aynı: 640px ve 1024px. Sıra: kök ekranlar önce masaüstünde oturur, hemen ardından aynı ekranların tablet ve telefon hali çıkar; yayılımda her ekran üç genişlikte birlikte üretilir. Dar ekranda tablo yığılmaz: sütunlar azalır ya da tablo yatay kayar; dokunma alanları en az 44px.
- Tek font ailesi; sayılar için eşit genişlikli rakam. Sayfada tek `<h1>`, seviye atlanmaz.
- Kare görsel: `div` + `background-image` + `cover` + `center`. Görsel boyutu CSS'te görünen genişliğe göre; 2x retina çarpanı yok.
- Logo ve ikonlar SVG ya da Font Awesome 6.5.2 Free (depoda barındırılır).
- Her liste ekranının boş, yükleniyor ve hata durumu; her formun doğrulama mesajı ve kaydedildi durumu vardır.
- Kartın ve tablo satırının tamamı tıklanır; satır içindeki düğmeler kendi işini yapar.
- Örnek içerik gerçekçidir ve veri sözlüğünden gelir; lorem ipsum yok. Gerçek anahtar, token ya da kişisel veri yazılmaz.
- Tarih ve saat biçimi nokta ile: `14.30`.

## Takım çalışması

- Kabuk, ortak bileşenler, modül sözleşmesi ve dört kök ekran **tek elden** çıkar; teammate açma.
- Yayılımda lead + 3-5 teammate: her modül tek teammate. Lead sayfa yazmaz; ortak dosyalar (kabuk, bileşenler, tema, modül kaydı) yalnızca lead'dedir.
- Teammate ortak dosyaya dokunmaz, eksik bileşeni uydurmaz; lead'e bildirir.
- Dalga planı Beyar'a sunulur; onay gelmeden başlatılmaz. Dalga sonunda kısa yazılı rapor.

## Compact'e dayanıklı çalışma

- İki dosya her an günceldir: `docs/tasarim-kararlari.md` (verilmiş bütün seçimler) ve `tasks/durum.md` (hangi adımdayız, sıradaki soru, açık kalemler, Beyar'ın son talimatları).
- Her karardan hemen sonra iki dosya güncellenir; sıradaki soru ondan sonra sorulur.
- Compact sonrası ya da emin olmadığın her an: CLAUDE.md, kararlar ve durum dosyalarını baştan oku. Dosyada yazan esastır.
- Kayıtlı kararı yeniden sorma; kayıtta olmayanı verilmiş sayma.

## Çalışma düzeni

- Büyük iş: keşif → plan → DUR → onay → uygulama. Küçük iş: doğrudan yap.
- Beklenmedik bir şey görürsen (kaynak okunmuyor, dokümanlar çelişiyor, bir şeyi silmen gerekiyor) dur ve raporla.
- Git hesabı `gaviaworks-dev`. `git add -A` ve force push yok; dosyalar adıyla eklenir. Ayrı konu ayrı commit; mesajlar İngilizce, Conventional Commits. Commit ve push için ayrı ayrı Beyar'ın açık onayı gerekir. Deponun herkese açık mı kapalı mı olacağını git kurulumunda Beyar'a sor; panel iç işleyişi gösterir.
- Ekran görüntüleri yalnızca kendi kontrolün için, `docs/screenshots/` altında (git'e girmez). `tasks/` git'e girmez.
- Prototip ritmi: yap, tek hızlı kontrol, raporla. Uzun ölçüm ya da test turundan önce büyük harfle yaz: `ÖLÇÜM: <ne>, tahmini X dk`; 10 dakikayı aşacaksa önce sor.
- Raporlar Türkçe, kısa, sonuç önce, madde madde.

## Açık konular (Beyar ve Yasin Bey ile netleşecek)

- Dada Haber dokümanında 2.1 "Editoryal Haber ve Vitrin Yönetimi" ayrıntı bölümü yok (2.2 iki kez yazılmış). Haber, kategori ve vitrin yönetiminin ayrıntısı public siteden türetilecek ve Beyar ile birlikte gözden geçirilecek.
- Teyit: önceki kaynak dokümanda "iki bağımsız kaynak olmadan otomatik yayın yok" kuralı vardı; yeni dokümanda yalnızca AI güven skoru ve editör onayı geçiyor. Panelde teyit bilgisinin nasıl görüneceği.
- Kaynak katmanları yeni dokümanda T1–T4 (Resmî, Kurumsal Basın, Uluslararası Medya, Düşük Öncelik); önceki dokümandaki K1–K4 tanımlarıyla farklı.
- "Otomatik yayınla" ayarının koşulları: önceki kaynak dokümandaki "teyitsiz otomatik yayın yok" kuralıyla birlikte nasıl çalışacağı. Öneri olarak ekranda şu koşullar da gösterilsin ve Beyar ile Yasin Bey karar versin: yalnızca belirli kaynak katmanlarından gelenler, hariç tutulan kategoriler, görseli eksik haberin otomatik yayımlanmaması, günlük üst sınır.
- Deponun herkese açık ya da kapalı olması.
