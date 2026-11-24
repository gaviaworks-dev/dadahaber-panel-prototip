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
 "medya": {
  "_not": "Stok örnek görseller (picsum.photos, Unsplash lisanslı); haber içeriğiyle ilgisizdir. Klasör ve adlar örnek.",
  "kok": "veri/gorsel/",
  "kucuk": "veri/gorsel/kucuk/",
  "gorseller": [
   {
    "dosya": "p117.jpg",
    "ad": "Kentsel ulaşım",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p122.jpg",
    "ad": "Kıyı ve rüzgâr",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p133.jpg",
    "ad": "Gece şehir",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p155.jpg",
    "ad": "Raylı sistem",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p158.jpg",
    "ad": "Kalabalık cadde",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p163.jpg",
    "ad": "Ofis ve masa",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p164.jpg",
    "ad": "Kitaplar",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p178.jpg",
    "ad": "Sisli sokak",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p180.jpg",
    "ad": "Kırsal yol",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p182.jpg",
    "ad": "Kar ve araç",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p183.jpg",
    "ad": "Kış trafiği",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p188.jpg",
    "ad": "Kent silueti",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p192.jpg",
    "ad": "Pencere ve ışık",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p193.jpg",
    "ad": "Pazar yeri",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p195.jpg",
    "ad": "Kara ve deniz",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   },
   {
    "dosya": "p203.jpg",
    "ad": "Sahil ve bisiklet",
    "klasor": "Stok havuzu",
    "kaynak": "Unsplash lisanslı",
    "olcu": "1200×800"
   }
  ]
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
 },
 "gorsel_alanlari": {
  "haberler": {
   "kapak": {
    "_kaynak": "sitenin görünen genişliği (kap 1280px; masaüstü 4 kart; telefon 390 - 2×16)",
    "web": {
     "kart": {
      "oran": "16:10",
      "px": [
       308,
       193
      ]
     },
     "detay": {
      "oran": "2.4:1",
      "px": [
       1280,
       533
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "16:10",
      "px": [
       358,
       224
      ]
     }
    },
    "mobil_webden_kirpilir": true,
    "bildirim": {
     "oran": "2:1"
    }
   }
  }
 },
 "sosyal_platformlar": [
  {
   "id": "x",
   "ad": "X",
   "acik": true,
   "oranlar": [
    "16:9",
    "1:1",
    "serbest"
   ],
   "editor": {
    "sinir": 280,
    "link_uzunluk": 23,
    "araclar": [
     "b-u",
     "i-u",
     "emoji",
     "etiket",
     "kisi",
     "link"
    ],
    "not": "X biçimlendirme desteklemez: kalın ve italik Unicode harfle · bağlantı 23 karakter sayılır"
   }
  },
  {
   "id": "facebook",
   "ad": "Facebook",
   "acik": true,
   "oranlar": [
    "1.91:1",
    "1:1",
    "serbest"
   ],
   "editor": {
    "sinir": 2000,
    "araclar": [
     "b-u",
     "i-u",
     "emoji",
     "etiket",
     "kisi",
     "link",
     "konum"
    ],
    "not": "Sayfa gönderisinde kalın yok (Unicode harf) · bağlantı önizleme kartı açar · @ ile sayfa ve kişi etiketlenir"
   }
  },
  {
   "id": "linkedin",
   "ad": "LinkedIn",
   "acik": true,
   "oranlar": [
    "1.91:1",
    "1:1",
    "serbest"
   ],
   "editor": {
    "sinir": 3000,
    "kesim": 210,
    "araclar": [
     "b-u",
     "i-u",
     "emoji",
     "etiket",
     "kisi",
     "link"
    ],
    "not": "Kalın ve italik Unicode harfle · ilk ~210 karakter 'daha fazla'dan önce görünür"
   }
  },
  {
   "id": "instagram",
   "ad": "Instagram",
   "acik": true,
   "oranlar": [
    "1:1",
    "4:5",
    "serbest"
   ],
   "editor": {
    "sinir": 2200,
    "kesim": 125,
    "etiket_siniri": 30,
    "araclar": [
     "b-u",
     "i-u",
     "emoji",
     "etiket",
     "kisi",
     "konum",
     "gorselde-etiket"
    ],
    "link_yok": true,
    "not": "Açıklamadaki bağlantı tıklanmaz (profildeki bağlantı kullanılır) · ilk 125 karakter 'daha fazla'dan önce · en fazla 30 etiket"
   }
  },
  {
   "id": "telegram",
   "ad": "Telegram",
   "acik": true,
   "oranlar": [
    "16:9",
    "1:1",
    "serbest"
   ],
   "editor": {
    "sinir": 1024,
    "araclar": [
     "b",
     "i",
     "u",
     "s",
     "kod",
     "spoiler",
     "alinti",
     "link-metin",
     "emoji",
     "etiket"
    ],
    "not": "Gerçek biçim (MarkdownV2): kalın, italik, altı çizili, üstü çizili, kod, gizli metin · görselli gönderide 1024, görselsiz 4096 karakter"
   }
  }
 ],
 "sosyal_oranlar": [
  {
   "oran": "16:9",
   "ad": "Sosyal 16:9",
   "px": [
    1200,
    675
   ]
  },
  {
   "oran": "1:1",
   "ad": "Sosyal 1:1",
   "px": [
    1080,
    1080
   ]
  },
  {
   "oran": "4:5",
   "ad": "Sosyal 4:5",
   "px": [
    1080,
    1350
   ]
  },
  {
   "oran": "1.91:1",
   "ad": "Sosyal 1.91:1",
   "px": [
    1200,
    628
   ]
  }
 ],
 "sosyal_oneriler": {
  "_not": "Örnek. Yazarlar public sözlükten; tutamaçlar örnektir, gerçek hesap değildir. Canlıda öneriler bağlı hesabın platform API'sinden aranır.",
  "hesaplar": [
   {
    "ad": "Dada Haber",
    "tutamac": "dadahaber",
    "tur": "Kurum hesabı",
    "onayli": true
   },
   {
    "ad": "Dada Gastro",
    "tutamac": "dadagastro",
    "tur": "Dada Ailesi",
    "onayli": true
   },
   {
    "ad": "Dada Spiker",
    "tutamac": "dadaspiker",
    "tur": "Dada Ailesi",
    "onayli": false
   },
   {
    "ad": "Dada Fit",
    "tutamac": "dadafit",
    "tur": "Dada Ailesi",
    "onayli": false
   },
   {
    "ad": "Mehmet Koçak",
    "tutamac": "mehmetkocak_dh",
    "tur": "Gündem Editörü",
    "onayli": false
   },
   {
    "ad": "Ayşe Yıldız",
    "tutamac": "ayseyildiz_dh",
    "tur": "Haber Müdürü",
    "onayli": false
   },
   {
    "ad": "Sibel Arslan",
    "tutamac": "sibelarslan_dh",
    "tur": "Saha Muhabiri",
    "onayli": false
   },
   {
    "ad": "Hakan Uysal",
    "tutamac": "hakanuysal_dh",
    "tur": "Çalışma Hayatı Muhabiri",
    "onayli": false
   },
   {
    "ad": "Elif Aras",
    "tutamac": "elifaras_dh",
    "tur": "Finans Editörü",
    "onayli": false
   },
   {
    "ad": "Can Demir",
    "tutamac": "candemir_dh",
    "tur": "Piyasa Muhabiri",
    "onayli": false
   },
   {
    "ad": "Nazlı Öztürk",
    "tutamac": "nazliozturk_dh",
    "tur": "Kişisel Finans Muhabiri",
    "onayli": false
   },
   {
    "ad": "Tolga Bayram",
    "tutamac": "tolgabayram_dh",
    "tur": "Enerji Muhabiri",
    "onayli": false
   },
   {
    "ad": "Burak Tan",
    "tutamac": "buraktan_dh",
    "tur": "Spor Editörü",
    "onayli": false
   },
   {
    "ad": "Murat Tekin",
    "tutamac": "murattekin_dh",
    "tur": "Futbol Yorumcusu",
    "onayli": false
   }
  ],
  "etiketler": [
   "AsgariÜcret",
   "Bütçe2027",
   "Ekonomi",
   "Gündem",
   "Emekli",
   "Memur",
   "Enflasyon",
   "SonDakika",
   "Türkiye",
   "Çalışma"
  ],
  "konumlar": [
   "İstanbul",
   "Ankara",
   "İzmir",
   "Türkiye",
   "Çalışma ve Sosyal Güvenlik Bakanlığı, Ankara"
  ]
 }
};
