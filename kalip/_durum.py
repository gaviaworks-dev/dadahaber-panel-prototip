#!/usr/bin/env python3
"""Kalıp alternatifleri · DURUMLAR bölümü (t-kalip5). Sayfa sahibi kalip/_uret.py bu modülü içe aktarır:

    from _durum import durumlar_html, DURUM_CSS
    durumlar_html("a")   # iskelet kodu A…L (küçük harf) → bölümün HTML'i (öneri tablosu + gruplar hâlinde durum kartları)
    DURUM_CSS            # "durum.css" (kalip/ altında; kalip.css'ten SONRA yüklenir)

Kartlar kalıbın tuval yapısını aynen kullanır (.kp-tuval .kp-{iskelet} .kp-sabit, data-tip/bicim/yz/lz, aynı katmanlar ve sınıflar);
iskeletin logo yeri, etiket biçimi, başlık yerleşimi ve renk uygulaması kalip.css'ten gelir. Duruma özgü iç parçalar
(skor, tablo, seçenek, ses dalgası…) .kd-* sınıflarıyla durum.css'te çizilir; yalnız tuvalin zemin değişkenlerini kullanır.
Süsleme (data-o-*) dıştaki .kp-orn kabından gelir; bu modül kendi .kp-orn'unu yazmaz.

Her kart ayrı görsel taşır (veri/gorsel/p600–p699; kaynak ve lisans kalip/_kaynak_t5.json). Başlıkların çoğu public
ornek_veri.json'dan birebir (KAYNAK=True olanlar denetlenir); kişi adları (köşe yazarı hariç sözlükteki kurgu yazarlar),
sözler, kulüp dışı ayrıntılar ve sayılar örnek ve kurgudur. Gerçek kişi ya da kuruma söz atfedilmez.
"""
import html, json, sys
from pathlib import Path

DURUM_CSS = "durum.css"
BURA = Path(__file__).resolve().parent
KOK = BURA.parent
PUB = KOK.parent / "dadahaber-prototip"
e = lambda s: html.escape(str(s), quote=True)
ik = lambda c: f'<i class="fa-solid {c}" aria-hidden="true"></i>'

# ------------------------------------------------------------------ kalıp sayfasından ortak parçalar (tek kaynak: _uret.py)
LOGO_YEDEK = ('<span class="kp-logo"><span class="kb-logo kp-l-sari"></span><span class="kb-logo kb-logo-acik kp-l-koyu"></span>'
              '<span class="kp-l-maske"></span></span>')
YZ_YEDEK = dict(a=("koyu", "koyu"), b=("kat", "kat"), c=("kat", "kat"), d=("acik", "acik"), e=("acik", "koyu"), f=("koyu", "koyu"),
                g=("koyu", "kat"), h=("acik", "acik"), i=("kat", "koyu"), j=("kat", "koyu"), k=("koyu", "kat"), l=("koyu", "koyu"),
                m=("acik", "kat"), n=("acik", "acik"))


def _uret():
    """_uret.py çalışırken (__main__) ya da içe aktarılabiliyorsa onun ALT/zemin/LOGO tanımlarını kullan"""
    m = sys.modules.get("__main__")
    if m is not None and hasattr(m, "ALTD") and hasattr(m, "zemin"):
        return m
    try:
        if str(BURA) not in sys.path:
            sys.path.insert(0, str(BURA))
        import _uret as m2
        return m2
    except Exception:
        return None


def zemin(alt, tip, bicim):
    m = _uret()
    if m is not None and alt in getattr(m, "ALTD", {}):
        try:
            return m.zemin(alt, tip, bicim)
        except Exception:
            pass
    yz, lz = YZ_YEDEK.get(alt, ("koyu", "koyu"))
    if alt == "b" and bicim == "uzun":
        lz = "koyu"
    return yz, lz


def logo():
    m = _uret()
    return getattr(m, "LOGO", LOGO_YEDEK) if m is not None else LOGO_YEDEK


def kl(d):
    """K ve L iskeletlerinin (t-kalip4, _iskelet_kl.kl_parca) her tuvale yazdığı parça; L'de dev dikey kelime"""
    m = _uret()
    f = getattr(m, "kl_parca", None) if m is not None else None
    if f is None:
        try:
            from _iskelet_kl import kl_parca as f
        except Exception:
            return ""
    try:
        return f(d["tip"], lambda fn: fn(dict(ad=d["katad"], r=d["bolge"], b=d.get("b", ""))), lambda b: d.get("saat", ""))
    except Exception:
        return ""


# ------------------------------------------------------------------ içerik
# Her durum: id, ad, grup, ne (tek cümle: ne zaman + standart kalıptan farkı), kat, bolge, g (görsel), o (odak),
# tip (kalıbın içerik çeşidi: durum | sd | veri | ic | reels | hikaye), bicim (kare 4:5 | uzun 9:16), ek=True → ekledik
GRUP = [("acil", "Aciliyet", "fa-bolt"), ("duz", "Düzeltme ve Güncelleme", "fa-pen-to-square"), ("tur", "Haber Türleri", "fa-newspaper"),
        ("gun", "Vefat, Anma, Özel Gün ve Duyuru", "fa-calendar-day"), ("spor", "Spor", "fa-futbol"), ("finans", "Finans", "fa-chart-line"),
        ("hava", "Hava, Afet ve Deprem", "fa-cloud-showers-heavy"), ("derle", "Derleme", "fa-list-ol"), ("ses", "Video ve Ses", "fa-circle-play"),
        ("gorsel", "Galeri ve İnfografik", "fa-images"), ("etk", "Anket ve Soru", "fa-square-poll-horizontal"), ("ek", "Eklediğimiz Durumlar", "fa-plus")]

D = [
    # ---- aciliyet
    dict(id="sd", ad="Son Dakika", grup="acil", tip="sd", kat="gundem", katad="Gündem", bolge="İstanbul", g="p600.jpg", o="50% 50%",
         b="Havalimanlarında kar nedeniyle 46 iç hat seferi iptal edildi", v="46 iç hat seferi", saat="15.20", kaynak=True,
         ne="Haber ilk duyulduğu anda. Kategori rengi yerine kırmızı kullanılır, fotoğraf siyah-beyaz olur, saat işaretin yanında yazar."),
    dict(id="flas", ad="Flaş", grup="acil", tip="sd", kat="finans", katad="Finans", bolge="Türkiye", g="p601.jpg", o="50% 50%",
         b="Merkez Bankası faizi sabit bıraktı: yüzde 42,5", v="yüzde 42,5", saat="14.00",
         ne="Son Dakika'dan da büyük, nadir gelişmede. Başlık kısa ve daha iri olur, fotoğraf kırmızı tona döner, ayrıntı satırı yoktur."),
    dict(id="gelisiyor", ad="Gelişiyor", grup="acil", tip="durum", kat="gundem", katad="Gündem", bolge="Marmara", g="p602.jpg", o="50% 50%",
         b="Kuzey Marmara Otoyolu'nda ağır tonajlı araç geçişine kısıtlama", v="ağır tonajlı", kaynak=True,
         akis=[("15.50", "Kısıtlama Odayeri'ne kadar uzatıldı"), ("14.40", "İlk duyuru")],
         ne="Olay sürerken ve bilgi değişirken. Kategori renginde \"Gelişiyor\" işareti eklenir, son iki güncelleme saatiyle altta durur."),
    dict(id="canli", ad="Canlı", grup="acil", tip="durum", acil=True, kat="gundem", katad="Gündem", bolge="Ankara", g="p603.jpg", o="50% 50%",
         b="TBMM Genel Kurulu'nda 2027 bütçesinin görüşmeleri sürüyor", v="2027 bütçesinin", meta="13.00'ten beri canlı · dadahaber.com",
         ne="Canlı yayın ya da dakika dakika anlatım sürerken. Kırmızı \"Canlı\" işareti eklenir, fotoğraf doğal renkte kalır, yayının başladığı saat yazar."),
    # ---- düzeltme ve güncelleme
    dict(id="duzeltme", ad="Düzeltme", grup="duz", tip="durum", kat="gundem", katad="Gündem", bolge="Türkiye", g="p604.jpg", o="50% 50%",
         b="Emekli bayram ikramiyesi ödemeleri 4 Aralık'ta başlıyor", v="4 Aralık'ta",
         onceki=dict(ne="24.11 · 18.40 paylaşımımız", yanlis="2 Aralık", dogru="4 Aralık"),
         ne="Önceki paylaşımda hata çıktığında. Nötr \"Düzeltme\" işareti eklenir; önceki paylaşımın küçük resmi, saati, yanlış ve doğru bilgi yan yana durur."),
    dict(id="guncelleme", ad="Güncelleme", grup="duz", tip="durum", kat="gundem", katad="Gündem", bolge="Hatay", g="p605.jpg", o="50% 50%",
         b="Deprem sonrası hasar tespit çalışmaları tamamlandı", v="hasar tespit", kaynak=True,
         ilk="09.15", son="15.00", eklenen="Ağır hasarlı bina sayısı 1.240 olarak açıklandı",
         ne="Paylaşılmış habere yeni bilgi eklendiğinde. Kategori renginde \"Güncelleme\" işareti, ilk paylaşım ve güncelleme saati, eklenen bilgi tek satırda yazar."),
    # ---- haber türleri
    dict(id="ozel", ad="Özel Haber", grup="tur", tip="durum", kat="gundem", katad="Gündem", bolge="Kahramanmaraş", g="p606.jpg", o="50% 50%",
         b="Konteyner kentten kalıcı konuta: üç ailenin hikâyesi", v="üç ailenin",
         ust="Özel Haber", meta="Sibel Arslan · dada'ya özel",
         ne="Yalnız dada'nın ulaştığı haberde. Başlığın üstüne \"Özel Haber\" ibaresi, altına muhabirin adı gelir; gerisi standart kalıptır."),
    dict(id="analiz", ad="Analiz", grup="tur", tip="durum", kat="finans", katad="Finans", bolge="Türkiye", g="p607.jpg", o="50% 50%",
         b="Dezenflasyon sürecinde hizmet fiyatları neden yavaş düşüyor", v="hizmet fiyatları", kaynak=True,
         ust="Analiz", meta="Elif Aras · 8 dk okuma",
         ne="Yorum ve arka plan içeren yazıda. \"Analiz\" ibaresi eklenir; yazar adı ve okuma süresi künyede yazar."),
    dict(id="roportaj", ad="Röportaj", grup="tur", tip="durum", kat="kesfet", katad="Keşfet", bolge="İstanbul", g="p608.jpg", o="50% 50%",
         soz="Salonu dolduran şey bilet fiyatı değil, merak", v="merak", ust="Röportaj", kim="Selin Ateş", unvan="Tiyatro yönetmeni",
         ne="Söyleşi paylaşılırken. Konuğun sözü tırnak içinde başlık olur, \"Röportaj\" ibaresi üstte, konuğun adı ve unvanı altta yazar (kişi ve söz kurgu)."),
    dict(id="kose", ad="Köşe Yazısı", grup="tur", tip="durum", kat="kose", katad="Köşe", bolge="Türkiye", g="p609.jpg", o="50% 50%",
         b="Faiz sabit kaldı ama kredi faizleri neden düşmüyor", v="neden düşmüyor", kaynak=True,
         yazar=dict(ad="Aylin Sezer", unvan="Köşe Yazarı", g="p610.jpg", o="55% 45%"),
         ne="Köşe yazısı paylaşılırken. Yazarın yuvarlak fotoğrafı ve adı başlığın üstünde durur, renk Köşe kategorisinden gelir (yazar sözlükteki kurgu ad; örnekte yüz yerine yazı masası görseli)."),
    # ---- vefat, anma, özel gün, duyuru
    dict(id="vefat", ad="Vefat ve Taziye", grup="gun", tip="durum", notr=True, kat="kesfet", katad="Keşfet", bolge="İstanbul", g="p611.jpg", o="50% 50%",
         b="Usta tiyatro oyuncusu Nermin Aksoy hayatını kaybetti", v="", yil="1938 – 2026", meta="Ailesine ve sevenlerine başsağlığı diliyoruz.",
         ne="Vefat ve taziyede. Kategori rengi, kelime vurgusu ve sarı logo kalkar; fotoğraf siyah-beyaz olur, yıllar ve başsağlığı satırı eklenir (kişi kurgu)."),
    dict(id="anma", ad="Anma Günü", grup="gun", tip="durum", notr=True, kat="gundem", katad="Gündem", bolge="Ankara", g="p612.jpg", o="50% 50%",
         b="Gazi Mustafa Kemal Atatürk'ü saygı ve özlemle anıyoruz", v="", ust="10 Kasım", meta="Ölümünün 88. yılında",
         ne="Anma günlerinde. Vefat kartı gibi sade ve renksizdir, tarih üstte yazar; kutlama dili ve kelime vurgusu kullanılmaz."),
    dict(id="bayram", ad="Bayram ve Özel Gün", grup="gun", tip="durum", kat="gundem", katad="Gündem", bolge="Türkiye", g="p613.jpg", o="50% 50%",
         b="Cumhuriyet Bayramımız kutlu olsun", v="kutlu olsun", ust="29 Ekim", meta="Cumhuriyet'in 103. yılı",
         ne="Bayram ve kutlama günlerinde. Haber başlığı yerine kutlama cümlesi gelir, tarih üstte yazar; fotoğraf doğal renkte kalır."),
    dict(id="duyuru", ad="Duyuru", grup="gun", tip="durum", kat="gundem", katad="Gündem", bolge="Türkiye", g="p614.jpg", o="50% 50%",
         b="dada uygulaması yenilendi: bildirimleri kategoriye göre seçin", v="kategoriye göre", rozet="Duyuru", rozet_ikon="fa-bullhorn",
         cagri="Uygulamayı güncelleyin",
         ne="dada'nın kendi duyurusunda (uygulama, yayın akışı, yeni seri). Kategori renginde \"Duyuru\" işareti ve tek çağrı satırı eklenir."),
    # ---- spor
    dict(id="mac", ad="Maç Sonucu", grup="spor", tip="durum", kat="spor", katad="Spor", bolge="İstanbul", g="p615.jpg", o="50% 50%",
         ev="Galatasaray", dep="Fenerbahçe", s1="2", s2="1", lig="Süper Lig · 14. hafta", gol="23' 67' · 81'",
         ne="Maç bittiğinde. Başlığın yerine skor tabelası gelir (iki takım, büyük rakam, kazanan önde); lig, hafta ve gol dakikaları altta yazar."),
    dict(id="maconu", ad="Maç Önü", grup="spor", tip="durum", kat="spor", katad="Spor", bolge="İstanbul", g="p616.jpg", o="50% 50%",
         ev="Beşiktaş", dep="Trabzonspor", ust="Süper Lig · 15. hafta", zaman="Pazar 19.00 · Tüpraş Stadyumu",
         ne="Maç gününden önce. İki takım adı alt alta, aralarında \"–\" ile başlık olur; gün, saat ve stat tek satırda yazar."),
    dict(id="transfer", ad="Transfer", grup="spor", tip="durum", kat="spor", katad="Spor", bolge="Türkiye", g="p617.jpg", o="50% 50%",
         b="Galatasaray sol bek transferini KAP'a bildirdi", v="sol bek", kaynak=True, damga="Resmî",
         bilgi=[("Sözleşme", "3,5 yıl"), ("Bonservis", "6,5 milyon €")],
         ne="Transfer resmîleştiğinde. \"Resmî\" damgası eklenir; sözleşme süresi ve bonservis iki küçük kutuda yazar (oyuncu adı kullanılmadı)."),
    dict(id="puan", ad="Puan Durumu", grup="spor", tip="ic", kat="spor", katad="Spor", bolge="Türkiye", g="p618.jpg", o="50% 50%",
         bas="Süper Lig · 13 hafta sonunda", tablo="puan",
         ne="Hafta tamamlandığında. Fotoğraf üstte şerit olur; ilk beş sıra oynanan maç, averaj ve puanla tablo halinde yazar."),
    # ---- finans
    dict(id="piyasa", ad="Piyasa Özeti", grup="finans", tip="ic", kat="finans", katad="Finans", bolge="Türkiye", g="p619.jpg", o="50% 50%",
         bas="Piyasalar · 15.50", tablo="piyasa",
         ne="Gün içinde ve kapanışta. Fotoğraf üstte şerit olur; dolar, euro, gram altın ve BIST 100 yön oklarıyla tabloda, güncelleme saati başlıkta yazar."),
    dict(id="veri", ad="Tek Veri", grup="finans", tip="veri", kat="finans", katad="Finans", bolge="Türkiye", g="p620.jpg", o="50% 50%",
         sayi="2.968 ₺", acik="Gram altın satış fiyatı · günde %0,64 yükseliş", yon="y", meta="23 Kasım 2026 · 15.50",
         ne="Tek bir rakam haberi taşıdığında. Dev rakam önde durur; yön oku, değişim yüzdesi ve saat altında yazar."),
    # ---- hava, afet
    dict(id="hava", ad="Hava Durumu", grup="hava", tip="ic", kat="gundem", katad="Gündem", bolge="İstanbul", g="p621.jpg", o="50% 50%",
         bas="İstanbul'da kar hafta ortasına kadar sürecek", hava=True,
         ne="Hava haberinde. Fotoğraf üstte şerit olur; şimdiki sıcaklık büyük, önümüzdeki beş gün simge ve sıcaklıkla tek satırda yazar."),
    dict(id="afet", ad="Afet Uyarısı", grup="hava", tip="durum", acil=True, kat="gundem", katad="Gündem", bolge="Doğu Karadeniz", g="p622.jpg", o="22% 60%",
         b="Karadeniz'de kuvvetli sağanak için turuncu kod uyarısı yapıldı", v="turuncu kod", kaynak=True,
         rozet="Uyarı", rozet_ikon="fa-triangle-exclamation", bilgi=[("Geçerli", "24 Kasım 06.00–21.00")],
         ne="Resmî uyarı yayımlandığında. Kırmızı \"Uyarı\" işareti eklenir; uyarı seviyesi başlıkta, bölge etikette, geçerlilik saati küçük kutuda yazar."),
    dict(id="deprem", ad="Deprem Bilgi Kartı", grup="hava", ek=True, tip="veri", acil=True, kat="gundem", katad="Gündem", bolge="Ege", g="p623.jpg", o="50% 50%",
         sayi="4,2", acik="büyüklüğünde · Seferihisar açıkları, 9,4 km derinlik",
         neden="Türkiye'de en sık paylaşılan acil bilgi; büyüklük, derinlik, saat ve merkez her seferinde aynı sırada ve hızla verilmeli.",
         ne="Deprem olduğunda. Kırmızı \"Deprem\" işareti ve saat; büyüklük dev rakamla, yer ve derinlik tek satırda yazar."),
    # ---- derleme
    dict(id="gun5", ad="Günün 5'i", grup="derle", tip="ic", kat="gundem", katad="Gündem", bolge="Türkiye", g="p624.jpg", o="50% 50%",
         bas="Günün 5'i · 23 Kasım", liste=["İstanbul'da okullar 24 Kasım'da da tatil", "Merkez Bankası faizi yüzde 42,5'te tuttu",
                                              "Kar nedeniyle 46 iç hat seferi iptal", "Asgari ücret masası 4 Aralık'ta kuruluyor",
                                              "Millî takımın aday kadrosu açıklandı"],
         ne="Akşam derlemesinde. Fotoğraf üstte şerit olur; günün beş haberi numaralı kısa liste halinde yazar."),
    dict(id="hafta", ad="Haftanın Özeti", grup="derle", tip="ic", kat="dunya", katad="Dünya", bolge="Dünya", g="p625.jpg", o="50% 50%",
         bas="Haftanın Özeti · 17–23 Kasım", gunler=[("Pzt", "AB genişleme gündemini ele aldı"), ("Çar", "NATO bakanları Brüksel'de buluştu"),
                                                       ("Cum", "BM insani yardım fonuna ek bütçe"), ("Paz", "İklim konferansında sonuç metni kabul edildi")],
         ne="Hafta sonunda. Numara yerine gün adı yazar; tarih aralığı başlıktadır, dört gelişme kısa satırlarla dizilir."),
    # ---- video ve ses
    dict(id="reels", ad="Video ve Reels Kapağı", grup="ses", tip="reels", bicim="uzun", kat="savunma", katad="Savunma", bolge="Türkiye", g="p626.jpg", o="50% 50%",
         b="KAAN'ın ikinci prototipinin test uçuşundan görüntüler", v="test uçuşundan", kaynak=True, sure="1.12",
         ne="Video paylaşılırken (9:16). Oynat işareti ve süre üstte durur; başlık ve logo uygulama düğmelerinin kapatmadığı alanda kalır."),
    dict(id="podcast", ad="Podcast Bölüm Kapağı", grup="ses", tip="durum", kat="finans", katad="Finans", bolge="Türkiye", g="p627.jpg", o="50% 50%",
         b="Asgari ücret görüşmelerinde hangi veriler masada", v="hangi veriler", program="Sabah Masası", bolum="Bölüm 42", sure="24 dk",
         ne="Podcast bölümü paylaşılırken. Program adı ve bölüm numarası üstte, ses dalgası ve süre altta yer alır (program adı kurgu)."),
    dict(id="dinle", ad="Haber Dinle", grup="ses", tip="durum", kat="kadin", katad="Kadın", bolge="Türkiye", g="p628.jpg", o="50% 50%",
         b="Zaman kullanım anketinin yeni sonuçları ücretsiz emeğin payını gösterdi", v="ücretsiz emeğin", kaynak=True, sure="3 dk",
         ne="Haberin sesli sürümü paylaşılırken. Kulaklık simgeli \"Haber Dinle\" işareti eklenir; ses dalgası ve dinleme süresi altta yazar."),
    # ---- galeri ve infografik
    dict(id="galeri", ad="Galeri ve Foto Haber", grup="gorsel", tip="durum", kat="kesfet", katad="Keşfet", bolge="Hatay", g="p629.jpg", o="50% 50%",
         b="Depremin ikinci yılında Hatay: sokak sokak", v="sokak sokak", kaynak=True, adet="18 fotoğraf",
         ne="Foto galeri paylaşılırken. Fotoğraf sayısı ve \"Kaydır\" işareti eklenir, fotoğraf tam alanda kalır, başlık kısa tutulur."),
    dict(id="infografik", ad="İnfografik Kapağı", grup="gorsel", tip="ic", kat="kampus", katad="Kampüs", bolge="Türkiye", g="p630.jpg", o="50% 50%",
         bas="Gençler haberi nereden alıyor?", grafik=[("Sosyal medya", 58), ("Haber siteleri", 19), ("Televizyon", 16), ("Gazete", 3)],
         ne="Veri görseli paylaşılırken. Kapakta küçük bir çubuk grafik ve \"Kaydır, rakamları gör\" daveti yer alır (oranlar örnek)."),
    # ---- anket ve soru
    dict(id="anket", ad="Anket", grup="etk", tip="ic", kat="kampus", katad="Kampüs", bolge="Türkiye", g="p631.jpg", o="50% 50%",
         bas="Ortak sınav haftasında okullar yarım gün olmalı mı?", secenek=[("Evet", 64), ("Hayır", 29), ("Fikrim yok", 7)], oy="3.412 oy · 24 saat",
         ne="Okur anketi sonuçlanırken. Soru başlık olur; seçenekler yüzdeleriyle çubuk halinde, toplam oy ve süre altta yazar (oranlar örnek)."),
    dict(id="soru", ad="Soru Kartı", grup="etk", tip="hikaye", bicim="uzun", kat="kadin", katad="Kadın", bolge="Türkiye", g="p632.jpg", o="50% 50%",
         b="Çalışan ebeveynler için en büyük eksik ne?", v="en büyük eksik",
         ne="Hikâyede okura soru sorulurken (9:16). Soru başlık olur; altında uygulamanın soru kutusu için yer bırakılır."),
    # ---- eklediğimiz
    dict(id="teyit", ad="Teyit (Doğru mu?)", grup="ek", ek=True, tip="durum", kat="kesfet", katad="Keşfet", bolge="Türkiye", g="p633.jpg", o="50% 50%",
         iddia="Asgari ücrete ocakta yüzde 60 zam yapılacak", damga="Yanıltıcı", meta="Görüşmeler 4 Aralık'ta başlıyor; oran henüz belli değil.",
         neden="Sosyal medyada yayılan iddialar çoğaldıkça teyit paylaşımı ayrı ve tanınır bir biçim ister; AI havuzundaki teyit verisiyle de uyumlu.",
         ne="Yayılan bir iddia çürütüldüğünde. İddia tırnak içinde başlık olur, üstüne \"Yanıltıcı\" damgası gelir, doğru bilgi tek satırda yazar."),
    dict(id="yasak", ad="Yayın Yasağı Bildirimi", grup="ek", ek=True, tip="durum", notr=True, kat="gundem", katad="Gündem", bolge="Türkiye", g="p634.jpg", o="50% 50%",
         b="Soruşturma kapsamında olaya ilişkin yayın yasağı getirildi", v="", rozet="Yayın Yasağı", rozet_ikon="fa-scale-balanced",
         meta="Haberlerimiz yasak kalkana kadar güncellenmeyecek.",
         neden="Türkiye'de sık karşılaşılan durum; okura haberin neden güncellenmediğini sade ve tarafsız biçimde söylemek gerekir.",
         ne="Bir olaya yayın yasağı getirildiğinde. Renk ve vurgu kalkar, nötr işaret eklenir; haberin neden güncellenmeyeceği tek satırda yazar."),
]
DD = {d["id"]: d for d in D}

# öneri (karar Yasin Bey'in): ilk aşamada şart / sonraya bırakılabilir — kısa gerekçe
ONERI_ILK = [("sd", "her gün, birden çok kez"), ("gelisiyor", "Son Dakika'nın devamı; bilgi değiştikçe"), ("canli", "meclis, maç, açıklama yayınları"),
             ("duzeltme", "hata olursa aynı gün şart; güvenilirlik"), ("guncelleme", "paylaşılmış habere yeni bilgi"), ("vefat", "renkli kalıp bu anda kullanılamaz"),
             ("anma", "takvimde sabit; renksiz kalıp şart"), ("afet", "can güvenliği; hız önemli"), ("deprem", "Türkiye'de sık; hep aynı bilgiler"),
             ("mac", "spor akışının en çok paylaşılanı"), ("piyasa", "Finans'ın günlük temel paylaşımı"), ("reels", "video zaten üretiliyor; kapak şart"),
             ("kose", "köşe yazıları her gün yayımlanıyor"), ("analiz", "sitede 48 analiz var; ibare yeterli")]
ONERI_SONRA = [("flas", "Son Dakika ilk aşamada yeter"), ("ozel", "ibare eklemek kolay; sıklık düşük"), ("roportaj", "Alıntı kartı geçici olarak karşılar"),
               ("bayram", "yılda birkaç kez; elle hazırlanabilir"), ("duyuru", "seyrek; elle hazırlanabilir"), ("maconu", "maç sonucundan sonra gelir"),
               ("transfer", "ara transfer 5 Ocak'ta açılıyor"), ("puan", "haftalık; sitede tablo zaten var"), ("veri", "Alıntı ve Veri sekmesindeki veri kartı karşılar"),
               ("hava", "sitede hava sayfası var; sosyalde seyrek"), ("gun5", "derleme düzeni oturunca"), ("hafta", "derleme düzeni oturunca"),
               ("podcast", "podcast yayını başlayınca"), ("dinle", "sesli sürüm yaygınlaşınca"), ("galeri", "kaydırmalı kalıp geçici olarak karşılar"),
               ("infografik", "veri ekibi kurulunca"), ("anket", "anket modülü açılınca"), ("soru", "hikâye takvimi oturunca"),
               ("teyit", "teyit masası kurulunca"), ("yasak", "seyrek; gerekirse nötr kalıpla")]
assert {k for k, _ in ONERI_ILK} | {k for k, _ in ONERI_SONRA} == set(DD), "öneri tablosu bütün durumları kapsamalı"
assert not ({k for k, _ in ONERI_ILK} & {k for k, _ in ONERI_SONRA})

# denetim: görseller diskte, her kartta ayrı görsel, sözlükten gelen başlıklar birebir
_g = []
for _d in D:
    _g.append(_d["g"])
    for _alt in ("yazar",):
        if _alt in _d:
            _g.append(_d[_alt]["g"])
assert len(set(_g)) == len(_g), "aynı görsel iki kartta"
GORSELLER = _g
try:
    _soz = json.loads((PUB / "araclar" / "ornek_veri.json").read_text(encoding="utf-8"))
    _bas = {h["baslik"] for h in _soz["haberler"]}
    for _d in D:
        if _d.get("kaynak"):
            assert _d["b"] in _bas, ("sözlükte yok", _d["id"], _d["b"])
    _puan = _soz["puan_tablosu"]["takimlar"]
    _pyasa = {a["ad"]: a for a in _soz["piyasa"]["araclar"]}
    _hava = _soz["hava"]
except FileNotFoundError:  # public depo yoksa sabit örnekler
    _puan, _pyasa, _hava = None, None, None


# ------------------------------------------------------------------ parçalar
def vurgulu(b, v):
    if not v or v not in b:
        return e(b)
    i = b.find(v)
    return f'{e(b[:i])}<em class="kp-vurgu">{e(v)}</em>{e(b[i + len(v):])}'


def kare(g, o, sinif):
    """kare/yuvarlak görsel: div + background-image (cover, odak noktası)"""
    return f'<span class="{sinif}" style="background-image:url(../veri/gorsel/{g});background-position:{o}" aria-hidden="true"></span>'


def rozet(metin, ikon=None, tur="kat", saat=None):
    """durum işareti: acil (kırmızı, nabız) · kat (kategori zemini) · notr (çerçeveli)"""
    on = f'<i class="kd-nabiz"></i>' if tur == "acil" and not ikon else (ik(ikon) if ikon else "")
    s = f'<span class="kp-saat">{e(saat)}</span>' if saat else ""
    return f'<span class="kd-rozet kd-rozet-{tur}">{on}{e(metin)}{s}</span>'


def puan_tablo():
    satir = []
    src = _puan or []
    for i, t in enumerate(src[:5]):
        p = 3 * t["G"] + t["B"]
        satir.append((i + 1, t["ad"], t["G"] + t["B"] + t["M"], t["A"] - t["Y"], p))
    if not satir:
        satir = [(1, "Galatasaray", 13, 23, 32), (2, "Fenerbahçe", 13, 19, 30), (3, "Beşiktaş", 13, 12, 25), (4, "Trabzonspor", 13, 8, 24), (5, "Başakşehir", 13, 5, 22)]
    bas = '<span class="kd-tr kd-tr-bas"><span>#</span><span>Takım</span><span>O</span><span>AV</span><span>P</span></span>'
    gov = "".join(f'<span class="kd-tr"><span class="kd-no">{s}</span><span class="kd-tad">{e(a)}</span><span>{o}</span><span>{"+" if av > 0 else ""}{av}</span><b>{p}</b></span>'
                  for s, a, o, av, p in satir)
    return f'<span class="kd-tablo kd-tablo-puan" role="table" aria-label="Puan durumu, ilk beş">{bas}{gov}</span>'


def piyasa_tablo():
    ad = [("Dolar", "Dolar", "₺"), ("Euro", "Euro", "₺"), ("Gram Altın", "Gram altın", "₺"), ("BIST 100", "BIST 100", "")]
    yedek = {"Dolar": ("34,5448", "0,12", "y"), "Euro": ("36,2180", "0,21", "y"), "Gram Altın": ("2.968,40", "0,64", "y"), "BIST 100": ("10.248,62", "0,43", "d")}
    sat = []
    for k, gor, br in ad:
        a = (_pyasa or {}).get(k)
        deger, deg, yon = (a["deger"], a["degisim"], a["yon"]) if a else yedek[k]
        ok = "fa-caret-up" if yon == "y" else "fa-caret-down"
        sat.append(f'<span class="kd-tr"><span class="kd-tad">{e(gor)}</span><b>{e(deger)}{(" " + br) if br else ""}</b>'
                   f'<span class="kd-yon kd-yon-{yon}">{ik(ok)}%{e(deg)}</span></span>')
    return f'<span class="kd-tablo kd-tablo-piyasa" role="table" aria-label="Piyasa özeti">{"".join(sat)}</span>'


def hava_satir():
    h = _hava or dict(simdi=dict(sicaklik=1, hissedilen=-4, durum="Yoğun kar", ikon="fa-snowflake"),
                      gunler=[dict(gun="Sal", ikon="fa-snowflake", yuksek=1, dusuk=-3), dict(gun="Çar", ikon="fa-cloud-showers-heavy", yuksek=4, dusuk=0),
                              dict(gun="Per", ikon="fa-cloud", yuksek=6, dusuk=1), dict(gun="Cum", ikon="fa-cloud-sun", yuksek=8, dusuk=3),
                              dict(gun="Cmt", ikon="fa-sun", yuksek=10, dusuk=4)])
    s = h["simdi"]
    ust = (f'<span class="kd-hava-simdi">{ik(s["ikon"])}<b>{s["sicaklik"]}°</b><span>{e(s["durum"])}<small>Hissedilen {s["hissedilen"]}°</small></span></span>')
    gun = "".join(f'<span class="kd-hava-gun"><small>{e(g["gun"])}</small>{ik(g["ikon"])}<b>{g["yuksek"]}°</b><small>{g["dusuk"]}°</small></span>'
                  for g in h["gunler"][:5])
    return f'{ust}<span class="kd-hava-gunler">{gun}</span>'


def dalga(n=26):
    """ses dalgası: sabit, tekrar etmeyen yükseklikler (çubuk)"""
    y = [38, 62, 44, 80, 56, 92, 70, 48, 84, 60, 100, 72, 52, 88, 64, 40, 76, 58, 94, 66, 46, 82, 54, 70, 42, 60]
    return '<span class="kd-dalga" aria-hidden="true">' + "".join(f'<i style="--y:{y[i % len(y)]}%"></i>' for i in range(n)) + '</span>'


def bilgi_kutu(bilgi):
    return '<span class="kd-bilgi">' + "".join(f'<span><small>{e(a)}</small><b>{e(b)}</b></span>' for a, b in bilgi) + '</span>'


def icerik(d):
    """kp-blok içi: sıra kalıbınki (etiket → vurgu öğesi → başlık → künye); durum parçaları order ile yerleşir"""
    x = d["id"]
    p = []
    if d["tip"] == "sd":
        p.append(f'<span class="kp-sdbas"><i></i>{"Flaş" if x == "flas" else "Son Dakika"}<span class="kp-saat">{e(d["saat"])}</span></span>')
    if x == "gelisiyor":
        p.append(rozet("Gelişiyor", "fa-arrows-rotate"))
    if x == "canli":
        p.append(rozet("Canlı", tur="acil"))
    if x == "duzeltme":
        p.append(rozet("Düzeltme", "fa-pen", tur="notr"))
    if x == "guncelleme":
        p.append(rozet("Güncelleme", "fa-clock-rotate-left", saat=d["son"]))
    if x in ("afet",):
        p.append(rozet(d["rozet"], d["rozet_ikon"], tur="acil"))
    if x == "deprem":
        p.append(rozet("Deprem", "fa-house-crack", tur="acil", saat="08.30"))
    if x in ("duyuru",):
        p.append(rozet(d["rozet"], d["rozet_ikon"]))
    if x == "yasak":
        p.append(rozet(d["rozet"], d["rozet_ikon"], tur="notr"))
    if x == "dinle":
        p.append(rozet("Haber Dinle", "fa-headphones", saat=d["sure"]))
    if x == "podcast":
        p.append(f'<span class="kd-program">{ik("fa-microphone-lines")}<b>{e(d["program"])}</b><span>{e(d["bolum"])}</span></span>')
    if x == "galeri":
        p.append(rozet(d["adet"], "fa-images"))
    if d.get("ust"):
        p.append(f'<span class="kp-ust-not kd-ust">{e(d["ust"])}</span>')
    if x == "kose":
        y = d["yazar"]
        p.append(f'<span class="kd-yazar">{kare(y["g"], y["o"], "kd-yazar-foto")}<span><b>{e(y["ad"])}</b><small>{e(y["unvan"])}</small></span></span>')
    # etiket (Kategori · Bölge)
    p.append(f'<span class="kp-etiket"><span class="kp-nokta"></span><b>{e(d["katad"])}</b><span class="kp-bolge">{e(d["bolge"])}</span></span>')
    # başlık ya da durumun yerine geçen ana öğe
    if x == "roportaj":
        p.append(f'<span class="kp-glif kp-glif-tirnak kd-tirnak">{ik("fa-quote-left")}</span>')
        p.append(f'<span class="kp-baslik kp-soz"><span class="kp-bi">“{vurgulu(d["soz"], d["v"])}”</span></span>')
        p.append(f'<span class="kp-kim kd-kim"><b>{e(d["kim"])}</b><span>{e(d["unvan"])}</span></span>')
    elif x == "teyit":
        p.append(f'<span class="kd-damga kd-damga-yanlis">{ik("fa-xmark")}{e(d["damga"])}</span>')
        p.append(f'<span class="kp-baslik kd-iddia"><span class="kp-bi">“{e(d["iddia"])}”</span></span>')
    elif x in ("mac",):
        k1, k2 = ("", " kd-kaybeden") if int(d["s1"]) >= int(d["s2"]) else (" kd-kaybeden", "")
        p.append(f'<span class="kd-ust kp-ust-not">Maç Sonucu · {e(d["lig"].split(" · ")[-1])}</span>')
        p.append(f'<span class="kd-skor" aria-label="{e(d["ev"])} {d["s1"]}, {e(d["dep"])} {d["s2"]}">'
                 f'<span class="kd-skor-satir{k1}"><span>{e(d["ev"])}</span><b>{d["s1"]}</b></span>'
                 f'<span class="kd-skor-satir{k2}"><span>{e(d["dep"])}</span><b>{d["s2"]}</b></span></span>')
    elif x == "maconu":
        p.append(f'<span class="kp-baslik kd-karsi"><span class="kp-bi">{e(d["ev"])}<em class="kp-vurgu kd-vs">–</em>{e(d["dep"])}</span></span>')
    elif d["tip"] == "veri":
        p.append(f'<span class="kp-sayi"><em class="kp-vurgu">{e(d["sayi"])}</em></span>')
        p.append(f'<span class="kp-aciklama">{e(d["acik"])}</span>')
    elif d["tip"] == "ic":
        p.append(f'<span class="kp-ic-bas">{e(d["bas"])}</span>')
    else:
        p.append(f'<span class="kp-baslik"><span class="kp-bi">{vurgulu(d["b"], d.get("v"))}</span></span>')
    # durumun alt parçaları
    if x == "gelisiyor":
        p.append('<span class="kd-akis">' + "".join(f'<span><b>{e(s)}</b>{e(t)}</span>' for s, t in d["akis"]) + '</span>')
    if x == "duzeltme":
        o = d["onceki"]
        p.append(f'<span class="kd-onceki">{kare(d["g"], d["o"], "kd-onceki-foto")}<span><small>{e(o["ne"])}</small>'
                 f'<span class="kd-fark"><s>{e(o["yanlis"])}</s>{ik("fa-arrow-right")}<b>{e(o["dogru"])}</b></span></span></span>')
    if x == "guncelleme":
        p.append(f'<span class="kd-eklenen">{ik("fa-plus")}<span>{e(d["eklenen"])}</span></span>')
        p.append(f'<span class="kp-meta">İlk paylaşım {e(d["ilk"])} · Güncellendi {e(d["son"])}</span>')
    if x in ("transfer",):
        p.insert(0, f'<span class="kd-damga kd-damga-ok">{ik("fa-check")}{e(d["damga"])}</span>')
        p.append(bilgi_kutu(d["bilgi"]))
    if x == "afet":
        p.append(bilgi_kutu(d["bilgi"]))
    if x == "maconu":
        p.append(f'<span class="kd-zaman">{ik("fa-calendar-day")}{e(d["zaman"])}</span>')
    if x == "mac":
        p.append(f'<span class="kp-meta">{e(d["lig"].split(" · ")[0])} · Goller {e(d["gol"])}</span>')
    if x == "veri":
        p.append(f'<span class="kp-meta">{e(d["meta"])}</span>')
    if x == "vefat":
        p.append(f'<span class="kd-yil">{e(d["yil"])}</span>')
    if x in ("anma", "bayram", "canli", "ozel", "analiz") and d.get("meta"):
        p.append(f'<span class="kp-meta">{e(d["meta"])}</span>')
    if x in ("vefat", "teyit", "yasak"):
        p.append(f'<span class="kd-not">{e(d["meta"])}</span>')
    if x == "duyuru":
        p.append(f'<span class="kd-cagri">{e(d["cagri"])}{ik("fa-arrow-right")}</span>')
    if x in ("podcast", "dinle"):
        p.append(f'<span class="kd-ses">{ik("fa-play")}{dalga()}<b>{e(d["sure"])}</b></span>')
    if x == "puan":
        p.append(puan_tablo())
    if x == "piyasa":
        p.append(piyasa_tablo())
    if x == "hava":
        p.append(hava_satir())
    if x == "gun5":
        p.append('<ol class="kp-liste kd-liste">' + "".join(f'<li><span class="kp-no">{i + 1}</span><span>{e(t)}</span></li>' for i, t in enumerate(d["liste"])) + '</ol>')
    if x == "hafta":
        p.append('<ol class="kp-liste kd-liste kd-liste-gun">' + "".join(f'<li><span class="kp-no">{e(g)}</span><span>{e(t)}</span></li>' for g, t in d["gunler"]) + '</ol>')
    if x == "infografik":
        p.append('<span class="kd-grafik" role="img" aria-label="Çubuk grafik">' + "".join(
            f'<span class="kd-cubuk" style="--y:{v}%"><span>{e(a)}</span><i></i><b>%{v}</b></span>' for a, v in d["grafik"]) + '</span>')
        p.append(f'<span class="kd-cagri">Kaydır, rakamları gör{ik("fa-arrow-right")}</span>')
    if x == "anket":
        p.append('<span class="kd-secenekler">' + "".join(
            f'<span class="kd-secenek{" kd-secenek-on" if i == 0 else ""}" style="--y:{v}%"><span>{e(a)}</span><b>%{v}</b></span>' for i, (a, v) in enumerate(d["secenek"])) + '</span>')
        p.append(f'<span class="kp-meta">{e(d["oy"])}</span>')
    if x == "soru":
        p.append(f'<span class="kd-soru-kutu">{ik("fa-keyboard")}Yanıtını yaz…</span>')
    if x == "reels":
        p.insert(0, f'<span class="kp-oynat">{ik("fa-play")}<span>{e(d["sure"])}</span></span>')
    return "".join(p)


def tuval(alt, d):
    tip, bicim = d["tip"], d.get("bicim", "kare")
    yz, lz = zemin(alt, tip, bicim)
    kat = "var(--ink)" if d.get("notr") else f'var(--kat-{d["kat"]})'
    stil = f'--kat:{kat};--g:url(../veri/gorsel/{d["g"]});--o:{d["o"]}'
    bayrak = (" data-acil" if d.get("acil") else "") + (" data-notr" if d.get("notr") else "")
    kaydir = (f'<span class="kp-kaydir kd-kaydir">1/18 · Kaydır{ik("fa-arrow-right")}</span>' if d["id"] == "galeri" else "")
    return (f'<div class="kp-tuval kp-{alt} kp-sabit kd-tuval" data-tip="{tip}" data-bicim="{bicim}" data-yz="{yz}" data-lz="{lz}" data-durum="{d["id"]}"{bayrak}'
            f' style="{stil}" role="img" aria-label="{e(d["ad"])} · {alt.upper()}">'
            f'<span class="kp-gorsel"></span><span class="kp-karart"></span><span class="kp-sekil"></span><span class="kp-sekil2"></span><span class="kp-kose"></span>'
            f'<span class="kp-masthead"><span>25 Kasım 2026</span><b>Sayı 327</b></span>{logo()}{kaydir}'
            f'<span class="kp-etiket-dikey"><b>{e(d["katad"])}</b><span class="kp-bolge">{e(d["bolge"])}</span></span>'
            f'{kl(d)}<span class="kp-blok"><span class="kp-oge"><i></i><i></i><i></i></span>{icerik(d)}</span><span class="kp-guvenli"></span></div>')


def kart(alt, d):
    ek = '<span class="pstat info kd-ek">Ek</span>' if d.get("ek") else ""
    neden = f'<span class="kd-neden"><b>Neden ekledik:</b> {e(d["neden"])}</span>' if d.get("neden") else ""
    return (f'<figure class="kp-sekil-kap kd-kap" data-durum="{d["id"]}">{tuval(alt, d)}'
            f'<figcaption class="kd-yazi"><b class="kd-ad">{e(d["ad"])}{ek}</b><span class="fhint">{e(d["ne"])}</span>{neden}</figcaption></figure>')


def oneri():
    def liste(o, sinif):
        return f'<ul class="kd-oneri-liste {sinif}">' + "".join(f'<li><b>{e(DD[k]["ad"])}</b><span>{e(n)}</span></li>' for k, n in o) + '</ul>'
    return (f'<div class="kd-oneri" role="group" aria-label="Öneri: ilk aşamada şart ve sonraya bırakılabilir">'
            f'<div class="pnl-card kd-oneri-kol"><div class="pc-body"><span class="kd-oneri-bas">{ik("fa-circle-check")}İlk Aşamada Şart<span class="kd-sayac">{len(ONERI_ILK)}</span></span>{liste(ONERI_ILK, "ilk")}</div></div>'
            f'<div class="pnl-card kd-oneri-kol"><div class="pc-body"><span class="kd-oneri-bas">{ik("fa-clock")}Sonraya Bırakılabilir<span class="kd-sayac">{len(ONERI_SONRA)}</span></span>{liste(ONERI_SONRA, "sonra")}</div></div>'
            f'</div>')


def durumlar_html(iskelet_kodu):
    alt = str(iskelet_kodu).lower()
    gruplar = ""
    for gk, gad, gik in GRUP:
        uye = [d for d in D if d["grup"] == gk]
        if not uye:
            continue
        gruplar += (f'<section class="kd-grup" aria-label="{e(gad)}"><h3 class="kd-grup-bas">{ik(gik)}{e(gad)}<span class="kd-sayac">{len(uye)}</span></h3>'
                    f'<div class="kp-sira kd-sira">{"".join(kart(alt, d) for d in uye)}</div></section>')
    return (f'<div class="kd" data-kd-alt="{alt}">'
            f'<div class="kd-giris"><h2 class="kp-alt-bas">{ik("fa-layer-group")}Durumlar · {len(D)} durum</h2>'
            f'<span class="fhint">Aynı iskelet, habere göre değişen işaretler. Her kart: ne zaman kullanılır ve standart kalıptan farkı. '
            f'Kişi, söz, program adı ve oranlar örnektir; başlıkların çoğu sitedeki örnek haberlerden.</span></div>'
            f'<div class="kb-bant bilgi">{ik("fa-circle-info")}<span><b>Öneri, karar değil.</b> Hangi durumların ilk aşamada yapılacağına Yasin Bey karar verecek.</span></div>'
            f'{oneri()}{gruplar}</div>')


if __name__ == "__main__":
    s = durumlar_html(sys.argv[1] if len(sys.argv) > 1 else "a")
    print(len(D), "durum ·", len(GORSELLER), "görsel ·", len(s) // 1024, "KB / iskelet")
