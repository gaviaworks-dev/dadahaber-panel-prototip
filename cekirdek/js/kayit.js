/* ÜRETİLMİŞ DOSYA — elle değiştirme. Kaynak: moduller.json + veri/panel.json · araclar/menu_yaz.py */
window.PANEL = {
 "proje_adi": "Dada Haber",
 "menu": {
  "katlanir": true,
  "etkin_grup_acik": true,
  "durumu_hatirla": true,
  "daraltma": "ikon"
 },
 "roller": {
  "super": {
   "ad": "Süper Admin",
   "izin_gruplari": [
    "*"
   ]
  },
  "gyy": {
   "ad": "Genel Yayın Yönetmeni",
   "izin_gruplari": [
    "icerik",
    "vitrin",
    "yorum",
    "rapor",
    "sosyal",
    "bulten-push"
   ]
  },
  "editor": {
   "ad": "Editör",
   "izin_gruplari": [
    "icerik",
    "vitrin",
    "yorum",
    "ai-havuz"
   ]
  },
  "kat-ed": {
   "ad": "Spor/Kategori Editörü",
   "izin_gruplari": [
    "icerik",
    "spor"
   ]
  },
  "sosyal": {
   "ad": "Sosyal Medya Uzmanı",
   "izin_gruplari": [
    "sosyal",
    "bulten-push"
   ]
  },
  "analist": {
   "ad": "Analist",
   "izin_gruplari": [
    "rapor"
   ]
  }
 },
 "rol_degistirici": [
  "super",
  "editor"
 ],
 "etkilesim": {
  "satir": "sayfa",
  "kucuk_tanim": "cekmece",
  "onay": "pencere"
 },
 "personalar": {
  "super": {
   "ad": "Selin Aydemir",
   "bas_harf": "SA",
   "unvan": "Süper Admin",
   "eposta": "selin.aydemir@dadahaber.ornek"
  },
  "gyy": {
   "ad": "Ayşe Yıldız",
   "bas_harf": "AY",
   "unvan": "Haber Müdürü",
   "eposta": "ayse.yildiz@dadahaber.ornek"
  },
  "editor": {
   "ad": "Mehmet Koçak",
   "bas_harf": "MK",
   "unvan": "Gündem Editörü",
   "eposta": "mehmet.kocak@dadahaber.ornek"
  },
  "kat-ed": {
   "ad": "Burak Tan",
   "bas_harf": "BT",
   "unvan": "Spor Editörü",
   "eposta": "burak.tan@dadahaber.ornek"
  },
  "sosyal": {
   "ad": "Ece Demirel",
   "bas_harf": "ED",
   "unvan": "Sosyal Medya Uzmanı",
   "eposta": "ece.demirel@dadahaber.ornek"
  },
  "analist": {
   "ad": "Kerem Aksoy",
   "bas_harf": "KA",
   "unvan": "Analist",
   "eposta": "kerem.aksoy@dadahaber.ornek"
  }
 },
 "sayfalar": {
  "kontrol-paneli.ana": {
   "baslik": "Kontrol Paneli",
   "ikon": "fa-gauge-high",
   "modul_ad": "Kontrol Paneli",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "sosyal",
    "analist"
   ]
  },
  "haberler.liste": {
   "baslik": "Haberler",
   "ikon": "fa-newspaper",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "sosyal",
    "analist"
   ]
  },
  "haberler.duzenle": {
   "baslik": "Haber Düzenle",
   "ikon": "fa-pen",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "sosyal",
    "analist"
   ]
  },
  "haberler.vitrin": {
   "baslik": "Vitrin ve Son Dakika",
   "ikon": "fa-star",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.canli": {
   "baslik": "Canlı Anlatım",
   "ikon": "fa-tower-broadcast",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "haberler.dosyalar": {
   "baslik": "Dosyalar ve Formatlar",
   "ikon": "fa-folder-open",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.yazarlar": {
   "baslik": "Yazarlar",
   "ikon": "fa-pen-nib",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "ai-havuz.havuz": {
   "baslik": "Haber Havuzu",
   "ikon": "fa-robot",
   "modul_ad": "AI Haber Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "analist"
   ]
  },
  "ai-havuz.kaynaklar": {
   "baslik": "Kaynaklar",
   "ikon": "fa-rss",
   "modul_ad": "AI Haber Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "ai-havuz.motor": {
   "baslik": "Kaynak Motoru",
   "ikon": "fa-gears",
   "modul_ad": "AI Haber Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "multimedya.video": {
   "baslik": "Video ve Akış",
   "ikon": "fa-video",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "multimedya.podcast": {
   "baslik": "Podcast",
   "ikon": "fa-podcast",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "multimedya.sesli": {
   "baslik": "Sesli Haber ve Spiker",
   "ikon": "fa-headphones",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "multimedya.galeri": {
   "baslik": "Galeri ve İnfografik",
   "ikon": "fa-images",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "multimedya.havuz": {
   "baslik": "Medya Havuzu",
   "ikon": "fa-photo-film",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "sosyal"
   ]
  },
  "ozel-dikeyler.spor": {
   "baslik": "Spor",
   "ikon": "fa-futbol",
   "modul_ad": "Özel Widgetlar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "kat-ed"
   ]
  },
  "ozel-dikeyler.takvimler": {
   "baslik": "Takvimler",
   "ikon": "fa-calendar-days",
   "modul_ad": "Özel Widgetlar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "ozel-dikeyler.veri": {
   "baslik": "Veri Bantları",
   "ikon": "fa-chart-line",
   "modul_ad": "Özel Widgetlar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "ozel-dikeyler.ilanlar": {
   "baslik": "Resmî İlanlar",
   "ikon": "fa-bullhorn",
   "modul_ad": "Özel Widgetlar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "anket.liste": {
   "baslik": "Anketler",
   "ikon": "fa-square-poll-vertical",
   "modul_ad": "Anketler",
   "hazir": false,
   "acik": false,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "sozluk.liste": {
   "baslik": "Sözlük",
   "ikon": "fa-book",
   "modul_ad": "Sözlük",
   "hazir": false,
   "acik": false,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "firma-rehberi.liste": {
   "baslik": "Firma Rehberi",
   "ikon": "fa-building",
   "modul_ad": "Firma Rehberi",
   "hazir": false,
   "acik": false,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "sosyal-medya.gonderi": {
   "baslik": "Gönderi Oluştur",
   "ikon": "fa-pen-to-square",
   "modul_ad": "Sosyal Medya Merkezi",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal"
   ]
  },
  "sosyal-medya.takvim": {
   "baslik": "Yayın Takvimi",
   "ikon": "fa-calendar-check",
   "modul_ad": "Sosyal Medya Merkezi",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal",
    "analist"
   ]
  },
  "sosyal-medya.hesaplar": {
   "baslik": "Hesaplar",
   "ikon": "fa-share-nodes",
   "modul_ad": "Sosyal Medya Merkezi",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal"
   ]
  },
  "etkilesim.yorumlar": {
   "baslik": "Yorumlar",
   "ikon": "fa-comments",
   "modul_ad": "Etkileşim",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "etkilesim.bulten": {
   "baslik": "Bülten",
   "ikon": "fa-envelope-open-text",
   "modul_ad": "Etkileşim",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal"
   ]
  },
  "etkilesim.push": {
   "baslik": "Push Bildirimleri",
   "ikon": "fa-bell",
   "modul_ad": "Etkileşim",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal"
   ]
  },
  "etkilesim.reklam": {
   "baslik": "Reklam Alanları",
   "ikon": "fa-rectangle-ad",
   "modul_ad": "Etkileşim",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "etkilesim.geri": {
   "baslik": "Okur Geri Bildirimleri",
   "ikon": "fa-inbox",
   "modul_ad": "Etkileşim",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "kullanicilar.liste": {
   "baslik": "Kullanıcılar",
   "ikon": "fa-users",
   "modul_ad": "Kullanıcılar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kimlik-yetki.roller": {
   "baslik": "Roller ve Yetki",
   "ikon": "fa-user-shield",
   "modul_ad": "Kimlik ve Yetki",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "site-ayarlari.ayarlar": {
   "baslik": "Site Ayarları",
   "ikon": "fa-sliders",
   "modul_ad": "Site Ayarları",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "entegrasyonlar.liste": {
   "baslik": "Entegrasyonlar",
   "ikon": "fa-plug",
   "modul_ad": "Entegrasyonlar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "yasal-metinler.liste": {
   "baslik": "Yasal Metinler",
   "ikon": "fa-file-contract",
   "modul_ad": "Yasal Metinler",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "sayfalar.liste": {
   "baslik": "Sayfalar",
   "ikon": "fa-file-lines",
   "modul_ad": "Sayfalar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "raporlar.liste": {
   "baslik": "Raporlar",
   "ikon": "fa-chart-pie",
   "modul_ad": "Raporlar",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "sosyal",
    "analist"
   ]
  },
  "denetim-izi.liste": {
   "baslik": "Denetim İzi",
   "ikon": "fa-clipboard-list",
   "modul_ad": "Denetim İzi",
   "hazir": false,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "analist"
   ]
  },
  "sistem-sagligi.ana": {
   "baslik": "Sistem Sağlığı",
   "ikon": "fa-heart-pulse",
   "modul_ad": "Sistem Sağlığı",
   "hazir": false,
   "acik": true,
   "roller": [
    "super"
   ]
  }
 },
 "oturum_sayfalari": {
  "oturum.cikis": "Çıkış ve giriş ekranı",
  "oturum.profil": "Profilim",
  "oturum.oturumlar": "Aktif oturumlar",
  "oturum.bildirimler": "Bildirimler"
 }
};
