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
  "_not": "Stok örnek görseller (picsum.photos, Unsplash lisanslı); haber içeriğiyle ilgisizdir. Etiketler örnektir, görseller temsilîdir (M2).",
  "kok": "veri/gorsel/",
  "kucuk": "veri/gorsel/kucuk/",
  "gorseller": [
   {
    "dosya": "p117.jpg",
    "ad": "Kentsel ulaşım",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Gündem",
     "kisiler": [
      "İstanbul Büyükşehir Belediyesi"
     ],
     "etiketler": [
      "ulaşım",
      "şehir"
     ]
    }
   },
   {
    "dosya": "p122.jpg",
    "ad": "Kıyı ve rüzgâr",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Keşfet",
     "kisiler": [],
     "etiketler": [
      "rüzgâr",
      "hava durumu",
      "sahil"
     ]
    }
   },
   {
    "dosya": "p133.jpg",
    "ad": "Gece şehir",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Gündem",
     "kisiler": [
      "İstanbul Büyükşehir Belediyesi"
     ],
     "etiketler": [
      "gece",
      "şehir",
      "İstanbul"
     ]
    }
   },
   {
    "dosya": "p155.jpg",
    "ad": "Raylı sistem",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Gündem",
     "kisiler": [
      "İstanbul Büyükşehir Belediyesi"
     ],
     "etiketler": [
      "ulaşım",
      "raylı sistem"
     ]
    }
   },
   {
    "dosya": "p158.jpg",
    "ad": "Kalabalık cadde",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Gündem",
     "kisiler": [
      "Recep Tayyip Erdoğan"
     ],
     "etiketler": [
      "miting",
      "şehir"
     ]
    }
   },
   {
    "dosya": "p163.jpg",
    "ad": "Ofis ve masa",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Finans",
     "kisiler": [
      "Çalışma ve Sosyal Güvenlik Bakanlığı"
     ],
     "etiketler": [
      "çalışma hayatı",
      "ekonomi"
     ]
    }
   },
   {
    "dosya": "p164.jpg",
    "ad": "Kitaplar",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Kampüs",
     "kisiler": [
      "Yükseköğretim Kurulu"
     ],
     "etiketler": [
      "eğitim",
      "kütüphane"
     ]
    }
   },
   {
    "dosya": "p178.jpg",
    "ad": "Sisli sokak",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Keşfet",
     "kisiler": [],
     "etiketler": [
      "sis",
      "hava durumu"
     ]
    }
   },
   {
    "dosya": "p180.jpg",
    "ad": "Kırsal yol",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Keşfet",
     "kisiler": [],
     "etiketler": [
      "tarım",
      "yaşam"
     ]
    }
   },
   {
    "dosya": "p182.jpg",
    "ad": "Kar ve araç",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Gündem",
     "kisiler": [
      "Afet ve Acil Durum Yönetimi Başkanlığı"
     ],
     "etiketler": [
      "kar",
      "trafik"
     ]
    }
   },
   {
    "dosya": "p183.jpg",
    "ad": "Kış trafiği",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Gündem",
     "kisiler": [
      "Afet ve Acil Durum Yönetimi Başkanlığı",
      "İstanbul Büyükşehir Belediyesi"
     ],
     "etiketler": [
      "kar",
      "trafik",
      "İstanbul"
     ]
    }
   },
   {
    "dosya": "p188.jpg",
    "ad": "Kent silueti",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Finans",
     "kisiler": [
      "Türkiye Cumhuriyet Merkez Bankası"
     ],
     "etiketler": [
      "ekonomi",
      "İstanbul"
     ]
    }
   },
   {
    "dosya": "p192.jpg",
    "ad": "Pencere ve ışık",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Kadın",
     "kisiler": [],
     "etiketler": [
      "yaşam"
     ]
    }
   },
   {
    "dosya": "p193.jpg",
    "ad": "Pazar yeri",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Finans",
     "kisiler": [
      "Türkiye İstatistik Kurumu"
     ],
     "etiketler": [
      "enflasyon",
      "pazar"
     ]
    }
   },
   {
    "dosya": "p195.jpg",
    "ad": "Kara ve deniz",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Savunma",
     "kisiler": [
      "Milli Güvenlik Kurulu",
      "Recep Tayyip Erdoğan",
      "Türk Silahlı Kuvvetleri"
     ],
     "etiketler": [
      "deniz",
      "güvenlik"
     ]
    }
   },
   {
    "dosya": "p203.jpg",
    "ad": "Sahil ve bisiklet",
    "klasor": "Dada Haber",
    "kaynak": "Dada Haber · telif bizde (örnek)",
    "olcu": "1200×800",
    "etiket": {
     "kategori": "Keşfet",
     "kisiler": [],
     "etiketler": [
      "sahil",
      "yaşam"
     ]
    }
   }
  ],
  "etiket_havuzu": {
   "_m2": "Medya havuzunun kendi etiketleri; haber etiketlerinden ayrıdır (Beyar ve Yasin Bey, 24.11.2026).",
   "kategoriler": [
    "Gündem",
    "Spor",
    "Finans",
    "Kadın",
    "Savunma",
    "Dünya",
    "Kampüs",
    "Keşfet"
   ],
   "kisiler": [
    {
     "ad": "Recep Tayyip Erdoğan",
     "kisaltma": "RTE",
     "tur": "Kişi"
    },
    {
     "ad": "Milli Güvenlik Kurulu",
     "kisaltma": "MGK",
     "tur": "Kurum"
    },
    {
     "ad": "Türkiye Büyük Millet Meclisi",
     "kisaltma": "TBMM",
     "tur": "Kurum"
    },
    {
     "ad": "Türkiye Cumhuriyet Merkez Bankası",
     "kisaltma": "TCMB",
     "tur": "Kurum"
    },
    {
     "ad": "Türkiye İstatistik Kurumu",
     "kisaltma": "TÜİK",
     "tur": "Kurum"
    },
    {
     "ad": "Çalışma ve Sosyal Güvenlik Bakanlığı",
     "kisaltma": "ÇSGB",
     "tur": "Kurum"
    },
    {
     "ad": "İstanbul Büyükşehir Belediyesi",
     "kisaltma": "İBB",
     "tur": "Kurum"
    },
    {
     "ad": "Afet ve Acil Durum Yönetimi Başkanlığı",
     "kisaltma": "AFAD",
     "tur": "Kurum"
    },
    {
     "ad": "Yükseköğretim Kurulu",
     "kisaltma": "YÖK",
     "tur": "Kurum"
    },
    {
     "ad": "Türk Silahlı Kuvvetleri",
     "kisaltma": "TSK",
     "tur": "Kurum"
    }
   ],
   "etiketler": [
    "ulaşım",
    "raylı sistem",
    "gece",
    "şehir",
    "miting",
    "ekonomi",
    "çalışma hayatı",
    "eğitim",
    "kütüphane",
    "hava durumu",
    "sis",
    "rüzgâr",
    "kar",
    "trafik",
    "enflasyon",
    "pazar",
    "deniz",
    "güvenlik",
    "yaşam",
    "sahil",
    "İstanbul",
    "tarım"
   ]
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.kose": {
   "baslik": "Köşe Yazıları",
   "ikon": "fa-feather-pointed",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.kose-duzenle": {
   "baslik": "Köşe Yazısı Düzenle",
   "ikon": "fa-feather-pointed",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.son-dakika": {
   "baslik": "Son Dakika",
   "ikon": "fa-bolt",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.canli-masa": {
   "baslik": "Canlı Anlatım Masası",
   "ikon": "fa-tower-broadcast",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "haberler.dosya": {
   "baslik": "Olay Dosyası Düzenle",
   "ikon": "fa-folder-open",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.gunun-5": {
   "baslik": "Günün 5'i",
   "ikon": "fa-list-ol",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.inceleme": {
   "baslik": "Doğrulama İncelemesi Düzenle",
   "ikon": "fa-scale-balanced",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.yazar": {
   "baslik": "Yazar Düzenle",
   "ikon": "fa-pen-nib",
   "modul_ad": "Haberler ve Vitrin",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "haberler.surumler": {
   "baslik": "Sürüm Geçmişi",
   "ikon": "fa-clock-rotate-left",
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
  "ai-havuz.havuz": {
   "baslik": "Haber Havuzu",
   "ikon": "fa-robot",
   "modul_ad": "AI Haber Havuzu",
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "ai-havuz.duzenle": {
   "baslik": "AI Haber Düzenle",
   "ikon": "fa-robot",
   "modul_ad": "AI Haber Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "analist"
   ]
  },
  "ai-havuz.cron": {
   "baslik": "Cron ve Hat Sağlığı",
   "ikon": "fa-heart-pulse",
   "modul_ad": "AI Haber Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "ai-havuz.ayarlar": {
   "baslik": "Otomatik Yayın ve Onay Ayarları",
   "ikon": "fa-sliders",
   "modul_ad": "AI Haber Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "multimedya.video": {
   "baslik": "Video ve Akış",
   "ikon": "fa-video",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed",
    "sosyal"
   ]
  },
  "multimedya.video-duzenle": {
   "baslik": "Video Düzenle",
   "ikon": "fa-video",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "multimedya.akis-duzenle": {
   "baslik": "Akış Videosu Düzenle",
   "ikon": "fa-mobile-screen",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "multimedya.canli-duzenle": {
   "baslik": "Canlı Yayın Düzenle",
   "ikon": "fa-tower-broadcast",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "multimedya.seri": {
   "baslik": "Podcast Serisi Düzenle",
   "ikon": "fa-podcast",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "multimedya.bolum": {
   "baslik": "Podcast Bölümü Düzenle",
   "ikon": "fa-microphone-lines",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "multimedya.sesli-duzenle": {
   "baslik": "Sesli Bülten Düzenle",
   "ikon": "fa-headphones",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "multimedya.galeri-duzenle": {
   "baslik": "Galeri Düzenle",
   "ikon": "fa-images",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "multimedya.infografik": {
   "baslik": "İnfografik Düzenle",
   "ikon": "fa-chart-pie",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor",
    "kat-ed"
   ]
  },
  "multimedya.sablon": {
   "baslik": "Marka Şablonu",
   "ikon": "fa-stamp",
   "modul_ad": "Multimedya ve Medya Havuzu",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "ozel-dikeyler.spor": {
   "baslik": "Spor",
   "ikon": "fa-futbol",
   "modul_ad": "Özel Widgetlar",
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "ozel-dikeyler.kulup": {
   "baslik": "Kulüp Düzenle",
   "ikon": "fa-shield-halved",
   "modul_ad": "Özel Widgetlar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "kat-ed"
   ]
  },
  "ozel-dikeyler.ilan": {
   "baslik": "İlan Düzenle",
   "ikon": "fa-bullhorn",
   "modul_ad": "Özel Widgetlar",
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal"
   ]
  },
  "sosyal-medya.kuyruk": {
   "baslik": "Yayın Takvimi",
   "ikon": "fa-calendar-check",
   "modul_ad": "Sosyal Medya Merkezi",
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "editor"
   ]
  },
  "etkilesim.bulten-duzenle": {
   "baslik": "Bülten Düzenle",
   "ikon": "fa-envelope-open-text",
   "modul_ad": "Etkileşim",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal"
   ]
  },
  "etkilesim.push-duzenle": {
   "baslik": "Push Bildirimi Düzenle",
   "ikon": "fa-bell",
   "modul_ad": "Etkileşim",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "sosyal"
   ]
  },
  "etkilesim.reklam-duzenle": {
   "baslik": "Reklam Alanı Düzenle",
   "ikon": "fa-rectangle-ad",
   "modul_ad": "Etkileşim",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kullanicilar.liste": {
   "baslik": "Kullanıcılar",
   "ikon": "fa-users",
   "modul_ad": "Kullanıcılar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kullanicilar.uye": {
   "baslik": "Ekip Üyesi",
   "ikon": "fa-user",
   "modul_ad": "Kullanıcılar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kullanicilar.davet": {
   "baslik": "Ekip Üyesi Davet Et",
   "ikon": "fa-user-plus",
   "modul_ad": "Kullanıcılar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kullanicilar.okurlar": {
   "baslik": "Okurlar",
   "ikon": "fa-user-group",
   "modul_ad": "Kullanıcılar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kullanicilar.okur": {
   "baslik": "Okur Detayı",
   "ikon": "fa-user",
   "modul_ad": "Kullanıcılar",
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kimlik-yetki.rol": {
   "baslik": "Rol Düzenle",
   "ikon": "fa-user-shield",
   "modul_ad": "Kimlik ve Yetki",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kimlik-yetki.izin-gruplari": {
   "baslik": "İzin Grupları",
   "ikon": "fa-layer-group",
   "modul_ad": "Kimlik ve Yetki",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kimlik-yetki.izin-grubu": {
   "baslik": "İzin Grubu Düzenle",
   "ikon": "fa-layer-group",
   "modul_ad": "Kimlik ve Yetki",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kimlik-yetki.oturumlar": {
   "baslik": "Aktif Oturumlar",
   "ikon": "fa-laptop",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.bildirimler": {
   "baslik": "Bildirimler",
   "ikon": "fa-bell",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.guvenlik": {
   "baslik": "Güvenlik Politikası",
   "ikon": "fa-shield-halved",
   "modul_ad": "Kimlik ve Yetki",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kimlik-yetki.profil": {
   "baslik": "Profilim",
   "ikon": "fa-user",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.giris": {
   "baslik": "Giriş",
   "ikon": "fa-right-to-bracket",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.dogrulama": {
   "baslik": "İki Adımlı Doğrulama",
   "ikon": "fa-shield",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.sifremi-unuttum": {
   "baslik": "Şifremi Unuttum",
   "ikon": "fa-key",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.yeni-sifre": {
   "baslik": "Yeni Şifre",
   "ikon": "fa-key",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.davet-kabul": {
   "baslik": "Davet ve E-posta Onayı",
   "ikon": "fa-envelope-circle-check",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.dogrulama-kurulum": {
   "baslik": "2FA Kurulumu",
   "ikon": "fa-shield",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.davet-eposta": {
   "baslik": "Davet E-postası Önizlemesi",
   "ikon": "fa-envelope",
   "modul_ad": "Kimlik ve Yetki",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "kimlik-yetki.baglanti-gecersiz": {
   "baslik": "Bağlantı Geçersiz",
   "ikon": "fa-link-slash",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.yetki-yok": {
   "baslik": "Yetki Yok (403)",
   "ikon": "fa-ban",
   "modul_ad": "Kimlik ve Yetki",
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
  "kimlik-yetki.bulunamadi": {
   "baslik": "Sayfa Bulunamadı (404)",
   "ikon": "fa-circle-question",
   "modul_ad": "Kimlik ve Yetki",
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
  "site-ayarlari.ayarlar": {
   "baslik": "Site Ayarları",
   "ikon": "fa-sliders",
   "modul_ad": "Site Ayarları",
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "entegrasyonlar.ayar": {
   "baslik": "Entegrasyon Ayarı",
   "ikon": "fa-gear",
   "modul_ad": "Entegrasyonlar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "entegrasyonlar.api": {
   "baslik": "API Anahtarları",
   "ikon": "fa-key",
   "modul_ad": "Entegrasyonlar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "yasal-metinler.liste": {
   "baslik": "Yasal Metinler",
   "ikon": "fa-file-contract",
   "modul_ad": "Yasal Metinler",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "yasal-metinler.duzenle": {
   "baslik": "Yasal Metin Düzenle",
   "ikon": "fa-file-pen",
   "modul_ad": "Yasal Metinler",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "yasal-metinler.surumler": {
   "baslik": "Sürüm Geçmişi",
   "ikon": "fa-clock-rotate-left",
   "modul_ad": "Yasal Metinler",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "yasal-metinler.onaylar": {
   "baslik": "Onay Kayıtları",
   "ikon": "fa-list-check",
   "modul_ad": "Yasal Metinler",
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "sayfalar.duzenle": {
   "baslik": "Sayfa Düzenle",
   "ikon": "fa-file-pen",
   "modul_ad": "Sayfalar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy"
   ]
  },
  "raporlar.liste": {
   "baslik": "Sistem Raporu",
   "ikon": "fa-chart-pie",
   "modul_ad": "Raporlar",
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
  "raporlar.site": {
   "baslik": "Site İstatistikleri",
   "ikon": "fa-chart-line",
   "modul_ad": "Raporlar",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "analist"
   ]
  },
  "raporlar.disa-aktarim": {
   "baslik": "Dışa Aktarımlar",
   "ikon": "fa-file-export",
   "modul_ad": "Raporlar",
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
  "denetim-izi.liste": {
   "baslik": "Denetim İzi",
   "ikon": "fa-clipboard-list",
   "modul_ad": "Denetim İzi",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "analist"
   ]
  },
  "denetim-izi.loglar": {
   "baslik": "Sistem Logları",
   "ikon": "fa-terminal",
   "modul_ad": "Denetim İzi",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "analist"
   ]
  },
  "denetim-izi.kayit": {
   "baslik": "Denetim Kaydı",
   "ikon": "fa-file-lines",
   "modul_ad": "Denetim İzi",
   "hazir": true,
   "acik": true,
   "roller": [
    "super",
    "gyy",
    "analist"
   ]
  },
  "denetim-izi.log": {
   "baslik": "Log Kaydı",
   "ikon": "fa-terminal",
   "modul_ad": "Denetim İzi",
   "hazir": true,
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
   "hazir": true,
   "acik": true,
   "roller": [
    "super"
   ]
  },
  "sistem-sagligi.onbellek": {
   "baslik": "Önbellek ve Rutin Temizlik",
   "ikon": "fa-broom",
   "modul_ad": "Sistem Sağlığı",
   "hazir": true,
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
   },
   "yazar": {
    "_kaynak": "public CSS (d2-haberler): yazarlar.html .yz1-av 88, yazar.html .pf-av 96, telefonda 72; daire",
    "web": {
     "kart": {
      "oran": "1:1",
      "px": [
       88,
       88
      ]
     },
     "detay": {
      "oran": "1:1",
      "px": [
       96,
       96
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "1:1",
      "px": [
       72,
       72
      ]
     }
    },
    "mobil_webden_kirpilir": true
   },
   "manset": {
    "_kaynak": "public CSS (d2-haberler): .manset .sol 9fr × 490px, yan kart 2:1; telefon önerisi",
    "web": {
     "detay": {
      "oran": "1.93:1",
      "px": [
       948,
       490
      ]
     },
     "kart": {
      "oran": "2:1",
      "px": [
       316,
       155
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "6:7",
      "px": [
       358,
       420
      ]
     }
    },
    "mobil_webden_kirpilir": true
   },
   "canli_giris": {
    "_kaynak": "d2-haberler: canlı anlatım girişinin görseli",
    "web": {
     "kart": {
      "oran": "16:9",
      "px": [
       800,
       450
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "16:9",
      "px": [
       358,
       201
      ]
     }
    },
    "mobil_webden_kirpilir": true
   }
  },
  "multimedya": {
   "video": {
    "_kaynak": "public CSS (d2-medya): video.html .gk .gm 4:3, .oy-video 16:9",
    "web": {
     "kart": {
      "oran": "4:3",
      "px": [
       308,
       231
      ]
     },
     "detay": {
      "oran": "16:9",
      "px": [
       1280,
       720
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "4:3",
      "px": [
       358,
       268
      ]
     }
    },
    "mobil_webden_kirpilir": true,
    "bildirim": {
     "oran": "2:1"
    }
   },
   "akis": {
    "_kaynak": "public CSS (d2-medya): .reel 188px, .ak-oy 420px, telefonda tam ekran",
    "web": {
     "kart": {
      "oran": "9:16",
      "px": [
       188,
       334
      ]
     },
     "detay": {
      "oran": "9:16",
      "px": [
       420,
       747
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "9:16",
      "px": [
       358,
       636
      ]
     }
    },
    "mobil_webden_kirpilir": true
   },
   "podcast": {
    "_kaynak": "public CSS (d2-medya): .pc 168px; telefonda .pc-kap 16:9",
    "web": {
     "kart": {
      "oran": "1:1",
      "px": [
       168,
       168
      ]
     },
     "detay": {
      "oran": "1:1",
      "px": [
       600,
       600
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "16:9",
      "px": [
       358,
       201
      ]
     }
    },
    "mobil_webden_kirpilir": true
   },
   "galeri": {
    "_kaynak": "public CSS (d2-medya): .kolaj 4:3; detay 16:10 varsayım",
    "web": {
     "kart": {
      "oran": "4:3",
      "px": [
       308,
       231
      ]
     },
     "detay": {
      "oran": "16:10",
      "px": [
       1280,
       800
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "4:3",
      "px": [
       358,
       268
      ]
     }
    },
    "mobil_webden_kirpilir": true
   },
   "infografik": {
    "_kaynak": "public CSS (d2-medya): .t-sira 4 sütun",
    "web": {
     "kart": {
      "oran": "3:4",
      "px": [
       305,
       407
      ]
     },
     "detay": {
      "oran": "3:4",
      "px": [
       900,
       1200
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "3:4",
      "px": [
       358,
       477
      ]
     }
    },
    "mobil_webden_kirpilir": true
   }
  },
  "ozel-dikeyler": {
   "arma": {
    "_kaynak": "varsayım (lead): kulüp arması (puan durumu satırı, takım sayfası)",
    "web": {
     "kart": {
      "oran": "1:1",
      "px": [
       48,
       48
      ]
     },
     "detay": {
      "oran": "1:1",
      "px": [
       160,
       160
      ]
     }
    },
    "mobil": {
     "kart": {
      "oran": "1:1",
      "px": [
       40,
       40
      ]
     }
    },
    "mobil_webden_kirpilir": true
   }
  },
  "sosyal-medya": {
   "gonderi": {
    "_kaynak": "yalnız sosyal oranlar (oran_olculeri); web ve mobil kırpım yok"
   }
  },
  "kimlik-yetki": {
   "profil": {
    "web": {
     "kart": {
      "oran": "1:1",
      "px": [
       256,
       256
      ]
     }
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
 },
 "sosyal_baglantilar": [
  {
   "id": "x",
   "ad": "X",
   "ikon": "fa-brands fa-x-twitter",
   "onek": "x.com/",
   "acik": true
  },
  {
   "id": "facebook",
   "ad": "Facebook",
   "ikon": "fa-brands fa-facebook",
   "onek": "facebook.com/",
   "acik": true
  },
  {
   "id": "instagram",
   "ad": "Instagram",
   "ikon": "fa-brands fa-instagram",
   "onek": "instagram.com/",
   "acik": true
  },
  {
   "id": "linkedin",
   "ad": "LinkedIn",
   "ikon": "fa-brands fa-linkedin",
   "onek": "linkedin.com/",
   "acik": true
  },
  {
   "id": "youtube",
   "ad": "YouTube",
   "ikon": "fa-brands fa-youtube",
   "onek": "youtube.com/@",
   "acik": true
  },
  {
   "id": "tiktok",
   "ad": "TikTok",
   "ikon": "fa-brands fa-tiktok",
   "onek": "tiktok.com/@",
   "acik": true
  },
  {
   "id": "telegram",
   "ad": "Telegram",
   "ikon": "fa-brands fa-telegram",
   "onek": "t.me/",
   "acik": true
  },
  {
   "id": "whatsapp",
   "ad": "WhatsApp Kanalı",
   "ikon": "fa-brands fa-whatsapp",
   "onek": "whatsapp.com/channel/",
   "acik": true
  },
  {
   "id": "threads",
   "ad": "Threads",
   "ikon": "fa-brands fa-threads",
   "onek": "threads.net/@",
   "acik": true
  },
  {
   "id": "bluesky",
   "ad": "Bluesky",
   "ikon": "fa-brands fa-bluesky",
   "onek": "bsky.app/profile/",
   "acik": true
  },
  {
   "id": "web",
   "ad": "Kişisel Web Sitesi",
   "ikon": "fa-solid fa-globe",
   "onek": "https://",
   "acik": true
  }
 ],
 "zorunlu": {
  "haberler.kose": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "spot",
    "metin",
    "yazar"
   ],
   "sistem": [
    "kategori",
    "kapak"
   ]
  },
  "haberler.son-dakika": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "kategori"
   ],
   "sistem": [
    "saat"
   ]
  },
  "haberler.canli": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "spot",
    "kategori",
    "kapak"
   ],
   "sistem": [
    "yazar",
    "baslangic"
   ]
  },
  "haberler.canli-giris": {
   "taslak": [
    "metin"
   ],
   "yayin": [
    "metin"
   ],
   "sistem": [
    "saat",
    "yazar"
   ]
  },
  "haberler.dosya": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "spot",
    "kategori",
    "kapak",
    "ozet"
   ],
   "sistem": [
    "yazar"
   ]
  },
  "haberler.gunun-5": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "haberler"
   ],
   "sistem": [
    "kapak",
    "yayin"
   ]
  },
  "haberler.inceleme": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "spot",
    "iddia",
    "karar",
    "bulgular",
    "kapak"
   ],
   "sistem": [
    "yazar"
   ]
  },
  "haberler.yazar": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "unvan"
   ],
   "sistem": []
  },
  "haberler.surum-notu": {
   "taslak": [
    "metin"
   ],
   "yayin": [
    "metin"
   ],
   "sistem": [
    "zaman",
    "yazar"
   ]
  },
  "haberler.haber": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "spot",
    "metin",
    "kategori",
    "kapak"
   ],
   "sistem": [
    "yazar"
   ]
  },
  "haberler.kategori": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "ust"
   ]
  },
  "ai-havuz.kaynak": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "adres",
    "grup"
   ],
   "sistem": [
    "tip"
   ]
  },
  "ai-havuz.grup": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "siklik"
   ],
   "sistem": [
    "kanallar"
   ]
  },
  "ai-havuz.reddet": {
   "taslak": [],
   "yayin": [
    "neden"
   ],
   "sistem": []
  },
  "multimedya.havuz-kisi": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "tur"
   ]
  },
  "multimedya.havuz-etiket": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad"
   ]
  },
  "multimedya.video": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "video",
    "kategori",
    "kapak"
   ],
   "sistem": [
    "yazar",
    "sure"
   ]
  },
  "multimedya.akis": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "video",
    "kategori",
    "kapak"
   ],
   "sistem": [
    "sure",
    "sira"
   ]
  },
  "multimedya.canli": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "video",
    "baslangic",
    "kategori",
    "kapak"
   ],
   "sistem": [
    "yazar"
   ]
  },
  "multimedya.seri": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "kategori",
    "kapak"
   ]
  },
  "multimedya.bolum": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "seri",
    "ses"
   ],
   "sistem": [
    "bolum-no",
    "sure",
    "kapak"
   ]
  },
  "multimedya.sesli": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "haberler",
    "ses"
   ],
   "sistem": [
    "okuma-metni",
    "sure"
   ]
  },
  "multimedya.galeri": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "kategori",
    "slaytlar"
   ],
   "sistem": [
    "kapak"
   ]
  },
  "multimedya.infografik": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "kategori",
    "gorsel"
   ]
  },
  "multimedya.varlik": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "kategori"
   ]
  },
  "ozel-dikeyler.brans": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad"
   ],
   "sistem": []
  },
  "ozel-dikeyler.kulup": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "kod",
    "lig"
   ],
   "sistem": [
    "renk",
    "slug",
    "seo"
   ]
  },
  "ozel-dikeyler.takvim": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "tur",
    "tarih",
    "kategori"
   ],
   "sistem": []
  },
  "ozel-dikeyler.ilan": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "tur",
    "kurum",
    "bitis",
    "metin"
   ],
   "sistem": [
    "yayin",
    "slug",
    "seo"
   ]
  },
  "ozel-dikeyler.duzeltme": {
   "taslak": [],
   "yayin": [
    "gerekce"
   ],
   "sistem": [
    "zaman",
    "yazar"
   ]
  },
  "sosyal-medya.gonderi": {
   "taslak": [
    "metin"
   ],
   "yayin": [
    "metin"
   ],
   "sistem": [
    "gorsel",
    "zaman",
    "hesap"
   ]
  },
  "sosyal-medya.hizli": {
   "taslak": [],
   "yayin": [
    "haber",
    "metin",
    "platform",
    "zaman"
   ],
   "sistem": [
    "zaman"
   ]
  },
  "sosyal-medya.hesap": {
   "taslak": [],
   "yayin": [
    "platform",
    "ad"
   ],
   "sistem": []
  },
  "etkilesim.yanit": {
   "taslak": [],
   "yayin": [
    "yanit"
   ],
   "sistem": []
  },
  "etkilesim.bulten": {
   "taslak": [
    "konu"
   ],
   "yayin": [
    "tur",
    "konu",
    "haberler"
   ],
   "sistem": [
    "zaman"
   ]
  },
  "etkilesim.bulten-turu": {
   "taslak": [],
   "yayin": [
    "ad",
    "gun",
    "saat"
   ],
   "sistem": []
  },
  "etkilesim.test": {
   "taslak": [],
   "yayin": [
    "eposta"
   ],
   "sistem": []
  },
  "etkilesim.push": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "metin",
    "kanal"
   ],
   "sistem": [
    "zaman",
    "gorsel",
    "haber"
   ]
  },
  "etkilesim.reklam": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "alan",
    "kod",
    "gorsel",
    "baslangic",
    "cihaz"
   ],
   "sistem": []
  },
  "kullanicilar.okur-durum": {
   "taslak": [],
   "yayin": [
    "gerekce"
   ],
   "sistem": []
  },
  "kullanicilar.okur": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad"
   ],
   "sistem": []
  },
  "kullanicilar.uye-durum": {
   "taslak": [],
   "yayin": [
    "gerekce"
   ],
   "sistem": []
  },
  "kullanicilar.uye": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "eposta"
   ],
   "sistem": []
  },
  "kullanicilar.davet": {
   "taslak": [],
   "yayin": [
    "ad",
    "eposta",
    "rol"
   ],
   "sistem": []
  },
  "kimlik-yetki.davet-kabul": {
   "taslak": [],
   "yayin": [
    "sifre",
    "sifre-tekrar",
    "kurallar"
   ],
   "sistem": []
  },
  "kimlik-yetki.yeni-sifre": {
   "taslak": [],
   "yayin": [
    "sifre",
    "sifre-tekrar"
   ],
   "sistem": []
  },
  "kimlik-yetki.sifremi-unuttum": {
   "taslak": [],
   "yayin": [
    "eposta"
   ],
   "sistem": []
  },
  "kimlik-yetki.giris": {
   "taslak": [],
   "yayin": [
    "eposta",
    "sifre"
   ],
   "sistem": []
  },
  "kimlik-yetki.profil": {
   "taslak": [],
   "yayin": [
    "ad",
    "eposta"
   ],
   "sistem": []
  },
  "kimlik-yetki.izin-grubu": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad"
   ],
   "sistem": [
    "kod"
   ]
  },
  "kimlik-yetki.rol": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "seviye"
   ],
   "sistem": []
  },
  "site-ayarlari.site": {
   "taslak": [],
   "yayin": [
    "site-adi",
    "eposta"
   ]
  },
  "entegrasyonlar.anahtar": {
   "taslak": [],
   "yayin": [
    "ad",
    "kapsam"
   ],
   "sistem": [
    "gecerlilik",
    "deger"
   ]
  },
  "entegrasyonlar.ayar": {
   "taslak": [],
   "yayin": [
    "ad",
    "adres"
   ],
   "sistem": [
    "api-anahtari",
    "imza-sirri",
    "siklik",
    "zaman-asimi",
    "deneme",
    "onbellek"
   ]
  },
  "yasal-metinler.metin": {
   "taslak": [
    "ad"
   ],
   "yayin": [
    "ad",
    "metin"
   ],
   "sistem": [
    "surum",
    "yururluk",
    "adres",
    "seo-baslik",
    "seo-aciklama"
   ]
  },
  "sayfalar.sayfa": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "metin"
   ],
   "sistem": [
    "adres",
    "seo-baslik",
    "seo-aciklama"
   ]
  },
  "raporlar.disa-aktarim": {
   "taslak": [],
   "yayin": [
    "alanlar"
   ],
   "sistem": [
    "rapor",
    "bicim",
    "aralik"
   ]
  }
 }
};
