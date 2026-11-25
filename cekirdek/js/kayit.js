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
  },
  "dis_kaynakli": {
   "_not": "Serbest lisanslı dış kaynak görseller (Wikimedia Commons), 25.11.2026. M1 gereği medya havuzunun telifli görsel listesine (gorseller) GİRMEZ; yalnız sosyal medya kalıp alternatiflerinde (kalip/) örnek olarak kullanılır. CC BY ve CC BY-SA görsellerde atıf zorunlu. Tam liste: veri/gorsel/LISANSLAR.md.",
   "gorseller": [
    {
     "dosya": "p301.jpg",
     "ad": "İstanbul'da gece nostaljik tramvay",
     "konu": "İstanbul'da gece nostaljik tramvay",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Istanbul_Oct_2019_12_29_13_059000.jpeg",
     "yazar": "Robot8A",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Robot8A · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p302.jpg",
     "ad": "İstanbul'da karlı cadde",
     "konu": "İstanbul'da karlı cadde",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Istanbul_photos_by_J.Lubbock_2015_467.jpg",
     "yazar": "Jwslubbock",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Jwslubbock · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p303.jpg",
     "ad": "TBMM binası",
     "konu": "TBMM binası",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Building_of_the_Grand_National_Assembly_of_Turkey.jpg",
     "yazar": "Clemens Holzmeister (1893-1983) Makril",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Clemens Holzmeister (1893-1983) Makril · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p304.jpg",
     "ad": "İstanbul metrosunda Haliç istasyonu",
     "konu": "İstanbul metrosunda Haliç istasyonu",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Hali%C3%A7_(Istanbul_Metro).JPG",
     "yazar": "My another account (talk)",
     "lisans": "CC0",
     "lisans_adresi": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
     "atif": ""
    },
    {
     "dosya": "p305.jpg",
     "ad": "İstanbul'da karlı yol",
     "konu": "İstanbul'da karlı yol",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Istanbul_photos_by_J.Lubbock_2015_457.jpg",
     "yazar": "Jwslubbock",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Jwslubbock · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p306.jpg",
     "ad": "İstanbul metrosunda tren",
     "konu": "İstanbul metrosunda tren",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Istanbul_metro_vehicle_20220410.jpg",
     "yazar": "Jelican9",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Jelican9 · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p311.jpg",
     "ad": "Gece ışıklandırmalı stadyum ve tribün",
     "konu": "Gece ışıklandırmalı stadyum ve tribün",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Mecz_pi%C5%82karski_Wis%C5%82a_Krak%C3%B3w_-_Zag%C5%82%C4%99bie_Sosnwoiec,_28_pa%C5%BAdziernika_2022,_Po%C5%BCegnanie_Stadionu_Ludowego,_KP.jpg",
     "yazar": "Krzysztof Popławski",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "Krzysztof Popławski · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p312.jpg",
     "ad": "Cumhurbaşkanlığı Türkiye Bisiklet Turu kürsüsü",
     "konu": "Cumhurbaşkanlığı Türkiye Bisiklet Turu kürsüsü",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:TourOfTurkey2019_(47).jpg",
     "yazar": "CeeGee",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "CeeGee · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p313.jpg",
     "ad": "Bayraklı taraftar tribünü (gece)",
     "konu": "Bayraklı taraftar tribünü (gece)",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Galatasaray-hamburg_2009-4.jpg",
     "yazar": "Qwl",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Qwl · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p314.jpg",
     "ad": "Maç öncesi stadyum ve taraftarlar",
     "konu": "Maç öncesi stadyum ve taraftarlar",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Galatasaray_Nef_Stadium_before_match_2022.jpg",
     "yazar": "Antoloji",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Antoloji · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p315.jpg",
     "ad": "Basketbol maçı (EuroLeague)",
     "konu": "Basketbol maçı (EuroLeague)",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Anadolu_Efes_Euroleague_20260929_(2).JPG",
     "yazar": "User:Zafer",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "User:Zafer · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p316.jpg",
     "ad": "Meşaleli taraftar tribünü (gece)",
     "konu": "Meşaleli taraftar tribünü (gece)",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Galatasaray-hamburg_2009-2.jpg",
     "yazar": "Qwl",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Qwl · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p321.jpg",
     "ad": "Uçak hangarında kadın teknisyenler",
     "konu": "Uçak hangarında kadın teknisyenler",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Female_Aircraft_Engineers,_Kwara_State,_Nigeria.jpg",
     "yazar": "Eyibeauty Oyelowo",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Eyibeauty Oyelowo · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p322.jpg",
     "ad": "Tarlada hasat yapan kadın",
     "konu": "Tarlada hasat yapan kadın",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Woman_harvesting_peanuts.jpg",
     "yazar": "Cecil Dzwowa",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Cecil Dzwowa · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p323.jpg",
     "ad": "Okulda mühendislik projesi yapan kız öğrenciler",
     "konu": "Okulda mühendislik projesi yapan kız öğrenciler",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Female_engineers_in_school.jpg",
     "yazar": "Find a Future",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Find a Future · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p324.jpg",
     "ad": "Halı tezgâhında dokuma yapan kadın",
     "konu": "Halı tezgâhında dokuma yapan kadın",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Woman_Weaves_Carpets_-_Goreme_-_Cappadocia_-_Turkey_(5760994299).jpg",
     "yazar": "Adam Jones from Kelowna, BC, Canada",
     "lisans": "CC BY-SA 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/2.0",
     "atif": "Adam Jones from Kelowna, BC, Canada · CC BY-SA 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p331.jpg",
     "ad": "Gün batımında konteyner limanı",
     "konu": "Gün batımında konteyner limanı",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Port_Jersey_container_ship_sunset_2018.jpg",
     "yazar": "Eric Kilby",
     "lisans": "CC BY-SA 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/2.0",
     "atif": "Eric Kilby · CC BY-SA 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p332.jpg",
     "ad": "Levent finans bölgesi gökdelenleri",
     "konu": "Levent finans bölgesi gökdelenleri",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:4._Levent_g%C3%B6kdelenler.jpg",
     "yazar": "Antoloji",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Antoloji · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p333.jpg",
     "ad": "50 Türk lirası banknot",
     "konu": "50 Türk lirası banknot",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:50_T%C3%BCrk_Liras%C4%B1_front.jpg",
     "yazar": "Central Bank of the Republic of Turkey",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": ""
    },
    {
     "dosya": "p334.jpg",
     "ad": "Limanda konteyner gemisi",
     "konu": "Limanda konteyner gemisi",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Container_ship_NYK_Themis_at_the_Port_of_Los_Angeles.jpg",
     "yazar": "Downtowngal",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Downtowngal · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p341.jpg",
     "ad": "Türk Hava Kuvvetleri F-16 savaş uçağı",
     "konu": "Türk Hava Kuvvetleri F-16 savaş uçağı",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkish_Air_Force_F-16_Fighting_Falcon_2461626.jpg",
     "yazar": "Airman 1st Class Kevin Tanenbaum",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": ""
    },
    {
     "dosya": "p342.jpg",
     "ad": "TCG Turgutreis fırkateyni (F-241)",
     "konu": "TCG Turgutreis fırkateyni (F-241)",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:TCG_Turgutreis_(F-241).jpg",
     "yazar": "MC2 Amanda S. Kitchner",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": ""
    },
    {
     "dosya": "p343.jpg",
     "ad": "TCG Anadolu amfibi hücum gemisi",
     "konu": "TCG Anadolu amfibi hücum gemisi",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkish_Navy_amphibious_assault_ship_TCG_Anadolu_(L400)_(starboard).jpg",
     "yazar": "Mass Communication Specialist 2nd Class Jackson Adkins",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": ""
    },
    {
     "dosya": "p344.jpg",
     "ad": "TCG Yüzbaşı Güngör Durmuş lojistik destek gemisi (A-574)",
     "konu": "TCG Yüzbaşı Güngör Durmuş lojistik destek gemisi (A-574)",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkish_Navy_auxiliary_ship_%E2%80%9CTCG_Y%C3%BCzba%C5%9F%C4%B1_G%C3%BCng%C3%B6r_Durmu%C5%9F%E2%80%9D_(A574)_(54232820113).jpg",
     "yazar": "Alan Wilson from Peterborough, Cambs, UK",
     "lisans": "CC BY-SA 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/2.0",
     "atif": "Alan Wilson from Peterborough, Cambs, UK · CC BY-SA 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p345.jpg",
     "ad": "Altay tankı",
     "konu": "Altay tankı",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Altay_Tank.jpg",
     "yazar": "Emir GEÇİR",
     "lisans": "CC0",
     "lisans_adresi": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
     "atif": ""
    },
    {
     "dosya": "p346.jpg",
     "ad": "TCG Fatih fırkateyni (F-242)",
     "konu": "TCG Fatih fırkateyni (F-242)",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkish_Navy_frigate_TCG_Fatih_(F-242),_Augusta_Bay,_June_2,_2014.jpg",
     "yazar": "U.S. Department of Defense Current Photos",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": ""
    },
    {
     "dosya": "p351.jpg",
     "ad": "Avrupa Parlamentosu genel kurul salonu (Strazburg)",
     "konu": "Avrupa Parlamentosu genel kurul salonu (Strazburg)",
     "kategori": "Dünya",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:European_Parliament_hemicycle_Strasbourg_(cropped).jpg",
     "yazar": "Gzen92",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Gzen92 · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p352.jpg",
     "ad": "BM Genel Kurul salonu (New York)",
     "konu": "BM Genel Kurul salonu (New York)",
     "kategori": "Dünya",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:United_Nations_General_Assembly_Hall_(3).jpg",
     "yazar": "Basil D Soufi",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Basil D Soufi · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p361.jpg",
     "ad": "Ankara'da Kızılay metro istasyonuna giren M1 treni",
     "konu": "Ankara'da Kızılay metro istasyonuna giren M1 treni",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:15_Temmuz_K%C4%B1z%C4%B1lay_Mill%C3%AE_%C4%B0rade_%C4%B0stasyonu-Ankara_Metrosu,_M1_Hatt%C4%B1-Ankara_Rayl%C4%B1_Sistemi.jpg",
     "yazar": "Modern primat",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Modern primat · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p362.jpg",
     "ad": "İstanbul M3 hattında boş Özgürlük Meydanı metro peronu",
     "konu": "İstanbul M3 hattında boş Özgürlük Meydanı metro peronu",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Istanbul_M3_%C3%96zg%C3%BCrl%C3%BCk_Meydan%C4%B1_Metro_Station_Train_Platform.jpg",
     "yazar": "MacBookator",
     "lisans": "CC0",
     "lisans_adresi": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
     "atif": "MacBookator · CC0 · Wikimedia Commons"
    },
    {
     "dosya": "p363.jpg",
     "ad": "İstanbul'da suyu çekilmiş kıyılarıyla Ömerli Barajı",
     "konu": "İstanbul'da suyu çekilmiş kıyılarıyla Ömerli Barajı",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:%C3%96merli_Baraji.jpg",
     "yazar": "aachim3",
     "lisans": "CC BY 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/3.0",
     "atif": "aachim3 · CC BY 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p365.jpg",
     "ad": "Antrenman sahasında çizgi üzerinde futbol topu",
     "konu": "Antrenman sahasında çizgi üzerinde futbol topu",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Soccer_Ball_(27181880724).jpg",
     "yazar": "USARJ NCO CORPS",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "USARJ NCO CORPS · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p366.jpg",
     "ad": "İstanbul Maratonu'nda köprü yolunda koşan kalabalık",
     "konu": "İstanbul Maratonu'nda köprü yolunda koşan kalabalık",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:38th_Istanbul_Vodafone_Marathon_(8).jpg",
     "yazar": "Sakhalinio",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Sakhalinio · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p367.jpg",
     "ad": "Sinop limanında bağlı balıkçı tekneleri",
     "konu": "Sinop limanında bağlı balıkçı tekneleri",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Sinop-Marina_port_area.jpg",
     "yazar": "Ertly",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Ertly · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p368.jpg",
     "ad": "Tezgâhta dokuma yapan eller",
     "konu": "Tezgâhta dokuma yapan eller",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:WEAVING_WITH_A_LOOPED_PILE_WEFT_ON_THE_WARP-WEIGHTED_LOOM.jpg",
     "yazar": "SEN Heritage Looms - Sophia Tsourinaki",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "SEN Heritage Looms - Sophia Tsourinaki · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p369.jpg",
     "ad": "İpek fabrikasında dikiş makinelerinde çalışan kadınlar",
     "konu": "İpek fabrikasında dikiş makinelerinde çalışan kadınlar",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Women_working_in_a_silk_factory_in_China.jpg",
     "yazar": "Lindsay Maizland",
     "lisans": "CC BY-SA 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/2.0",
     "atif": "Lindsay Maizland · CC BY-SA 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p370.jpg",
     "ad": "Kredi kartı takılı ödeme (POS) cihazı",
     "konu": "Kredi kartı takılı ödeme (POS) cihazı",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Credit_card_terminal_in_Laos.jpg",
     "yazar": "Basile Morin",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Basile Morin · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p372.jpg",
     "ad": "1 Türk lirası madeni para yakın plan",
     "konu": "1 Türk lirası madeni para yakın plan",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkish_Lira_(13593185824).jpg",
     "yazar": "Mark Morgan from Trinidad",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Mark Morgan from Trinidad · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p373.jpg",
     "ad": "İstanbul Boğazı'nda seyreden Sahil Güvenlik botu",
     "konu": "İstanbul Boğazı'nda seyreden Sahil Güvenlik botu",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkish_Coast_Guard_Kaan_33_class_patrol_boat_312.jpg",
     "yazar": "Eusebius",
     "lisans": "CC BY 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/3.0",
     "atif": "Eusebius · CC BY 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p374.jpg",
     "ad": "Pistte bekleyen Bayraktar TB2 insansız hava aracı",
     "konu": "Pistte bekleyen Bayraktar TB2 insansız hava aracı",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Bayraktar_TB2_Ground.jpg",
     "yazar": "Bayhaluk",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Bayhaluk · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p375.jpg",
     "ad": "TEKNOFEST'te sergilenen HÜRJET jet eğitim uçağı",
     "konu": "TEKNOFEST'te sergilenen HÜRJET jet eğitim uçağı",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:TAI_H%C3%BCrjet_Teknofest2019_(1).jpg",
     "yazar": "CeeGee",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "CeeGee · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p376.jpg",
     "ad": "Münih Olimpiyat Stadı'nda boş yeşil tribün koltukları",
     "konu": "Münih Olimpiyat Stadı'nda boş yeşil tribün koltukları",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Green_seats_Olympiastadion_Munich.jpg",
     "yazar": "Spielvogel",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Spielvogel · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p377.jpg",
     "ad": "Gün batımında denizde seyreden savaş gemisi silueti",
     "konu": "Gün batımında denizde seyreden savaş gemisi silueti",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:USS_Belknap_(CG-26)_silhouetted_against_the_setting_sun_on_3_August_1989_(6454577).jpg",
     "yazar": "PH2 Mark Kettenhofen, U.S. Navy",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": "PH2 Mark Kettenhofen, U.S. Navy · Public domain · Wikimedia Commons"
    },
    {
     "dosya": "p379.jpg",
     "ad": "Laboratuvarda pipetle çalışan kadın araştırmacı",
     "konu": "Laboratuvarda pipetle çalışan kadın araştırmacı",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Analyse_g%C3%A9n%C3%A9tique_de_coraux_d%27eau_froide_durant_la_campagen_REDECOR_2026_en_mer_d%27Irlande_(Ifremer_01088-120004_-_518531).jpg",
     "yazar": "Kim Dornic (IFREMER, Pôle média &amp; web, Centre Bretagne - ZI de la Pointe du Diable - CS 10070 - 29280 Plouzané)\n\nKim Dornic (IFREMER, Pôle média &amp; web, Centre Bretagne - ZI de la Pointe du Diable - CS 10070 - 29280 Plouzané)",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "Kim Dornic (IFREMER, Pôle média &amp; web, Centre Bretagne - ZI de la Pointe du Diable - CS 10070 - 29280 Plouzané)\n\nKim Dornic (IFREMER, Pôle média &amp; web, Centre Bretagne - ZI de la Pointe du Diable - CS 10070 - 29280 Plouzané) · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p381.jpg",
     "ad": "Işıklar altında gece oynanan futbol maçı, geniş açı",
     "konu": "Işıklar altında gece oynanan futbol maçı, geniş açı",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Chicago_Fire_v._Club_Am%C3%A9rica_2013_25.jpg",
     "yazar": "Michael Barera",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Michael Barera · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p382.jpg",
     "ad": "Karlı havada uçağın buzlanmaya karşı ilaçlanması",
     "konu": "Karlı havada uçağın buzlanmaya karşı ilaçlanması",
     "kategori": "Savunma",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:De-icing_a_KC-135_Stratotanker_with_a_de-icing_truck_at_McConnell_Air_Force_Base,_Kansas.jpg",
     "yazar": "Senior Airman Zachary Willis",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": "Senior Airman Zachary Willis · Public domain · Wikimedia Commons"
    },
    {
     "dosya": "p385.jpg",
     "ad": "Gece maçında meşalelerle tribün şovu yapan taraftarlar",
     "konu": "Gece maçında meşalelerle tribün şovu yapan taraftarlar",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:AEK_fans_during_the_first_match_played_in_Agia_Sophia_Stadium.jpg",
     "yazar": "Demian vi",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Demian vi · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p387.jpg",
     "ad": "Maç sırasında dolu bir basketbol salonu, geniş açı",
     "konu": "Maç sırasında dolu bir basketbol salonu, geniş açı",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Mall_of_Asia_Arena_Basketball_FIBA_Asia_2013.jpg",
     "yazar": "WayKurat",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "WayKurat · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p388.jpg",
     "ad": "Üst üste yığılmış külçe altınlar",
     "konu": "Üst üste yığılmış külçe altınlar",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Gold_bullion_bars.jpg",
     "yazar": "Stevebidmead",
     "lisans": "CC0",
     "lisans_adresi": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
     "atif": "Stevebidmead · CC0 · Wikimedia Commons"
    },
    {
     "dosya": "p390.jpg",
     "ad": "İstanbul'da sık yapılaşmış apartmanlar ve çatılar",
     "konu": "İstanbul'da sık yapılaşmış apartmanlar ve çatılar",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Istanbul_rooftops_(2100044136).jpg",
     "yazar": "Francisco Anzola",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Francisco Anzola · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p391.jpg",
     "ad": "Karanlıkta yanan tek mum",
     "konu": "Karanlıkta yanan tek mum",
     "kategori": "Gündem",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Like_a_candle_flame_(233107630).jpg",
     "yazar": "Andy / Andrew Fogg from near Cambridge, UK",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Andy / Andrew Fogg from near Cambridge, UK · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p392.jpg",
     "ad": "Maç öncesi gündüz boş saha ve tribünler",
     "konu": "Maç öncesi gündüz boş saha ve tribünler",
     "kategori": "Spor",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:A_Somewhat_Empty_Wembley_-_geograph.org.uk_-_8222730.jpg",
     "yazar": "Alex Kinney",
     "lisans": "CC BY-SA 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/2.0",
     "atif": "Alex Kinney · CC BY-SA 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p397.jpg",
     "ad": "Fırtına sonrası kara bulutlar altında İstanbul Boğazı ve köprü",
     "konu": "Fırtına sonrası kara bulutlar altında İstanbul Boğazı ve köprü",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Bosphorus,_A_game_of_colors_after_the_storm.jpg",
     "yazar": "Istanbul welove",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Istanbul welove · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p398.jpg",
     "ad": "Kâğıt tambura deprem dalgalarını çizen sismograf",
     "konu": "Kâğıt tambura deprem dalgalarını çizen sismograf",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Seismogram_at_Weston_Observatory.JPG",
     "yazar": "Z22",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Z22 · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p399.jpg",
     "ad": "Gün doğumunda İstanbul Boğazı'nda tekne ve bulutlar",
     "konu": "Gün doğumunda İstanbul Boğazı'nda tekne ve bulutlar",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Sail_at_dawn.jpg",
     "yazar": "Hosna K",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Hosna K · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p400.jpg",
     "ad": "Üst üste yığılmış eski gazeteler",
     "konu": "Üst üste yığılmış eski gazeteler",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:ASC_Leiden_-_Library_-_South_African_newspaper_stack_of_Die_Burger_-_2012.jpg",
     "yazar": "African Studies Centre Leiden",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "African Studies Centre Leiden · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p401.jpg",
     "ad": "Gösteri uçuşunda Türk Hava Kuvvetleri SoloTürk F-16",
     "konu": "Gösteri uçuşunda Türk Hava Kuvvetleri SoloTürk F-16",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:F-16_SoloT%C3%BCrk_Turkish_Air_Force_(52546791439).jpg",
     "yazar": "slezo",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "slezo · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p402.jpg",
     "ad": "Stüdyo mikrofonu ve kulaklık, yakın plan",
     "konu": "Stüdyo mikrofonu ve kulaklık, yakın plan",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Headphone_Microphone_Madrid_(Unsplash).jpg",
     "yazar": "WillSpirit SBLN willspirit",
     "lisans": "CC0",
     "lisans_adresi": "http://creativecommons.org/publicdomain/zero/1.0/deed.en",
     "atif": "WillSpirit SBLN willspirit · CC0 · Wikimedia Commons"
    },
    {
     "dosya": "p404.jpg",
     "ad": "Erzurum İspir'de dağ yamacındaki köy",
     "konu": "Erzurum İspir'de dağ yamacındaki köy",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:%C4%B0spir.jpg",
     "yazar": "Ahmet Talha Yılmaz",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Ahmet Talha Yılmaz · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p407.jpg",
     "ad": "Elde tutulan, ekranı boş akıllı telefon",
     "konu": "Elde tutulan, ekranı boş akıllı telefon",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Hand_holding_smartphone_with_blank_white_screen.jpg",
     "yazar": "Santeri Viinamäki",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Santeri Viinamäki · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p408.jpg",
     "ad": "Kara tahtalı ve sıralı boş eski bir sınıf",
     "konu": "Kara tahtalı ve sıralı boş eski bir sınıf",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Karmsund_folkemuseum_Haugesund_Norway_Interior_Skolestue_klasserom_Class_room_ca_1910_Skolepulter_skrivepulter_benker_school_room_benches_writing_desks_Kateter_Tavle_Blackboard_Skolekart_Vaskefat_Kuleramme_Plansje_etc_2020-06-10_DSC00.jpg",
     "yazar": "Wolfmann",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Wolfmann · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p409.jpg",
     "ad": "Kapalı havada 15 Temmuz Şehitler Köprüsü",
     "konu": "Kapalı havada 15 Temmuz Şehitler Köprüsü",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Bosphorus_Bridge(15_July_Martyrs_Bridge),_Istanbul,_Turkey_(Ank_Kumar)_09.jpg",
     "yazar": "Ank Kumar",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Ank Kumar · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p410.jpg",
     "ad": "Duvarlarında fotoğraflar asılı sergi salonu",
     "konu": "Duvarlarında fotoğraflar asılı sergi salonu",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Liljevalchs_-_Anders_Petersen_photography_exhibition_9609.jpg",
     "yazar": "Avery Jensen",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Avery Jensen · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p411.jpg",
     "ad": "Oy pusulası zarflarıyla dolu şeffaf seçim sandığı",
     "konu": "Oy pusulası zarflarıyla dolu şeffaf seçim sandığı",
     "kategori": "",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkey_2018_elections,_ballot_box.jpg",
     "yazar": "Hedda Gabler",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Hedda Gabler · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p500.jpg",
     "ad": "İzmir Güzelbahçe'de Yalı balıkçı barınağı, havadan",
     "konu": "İzmir Güzelbahçe'de Yalı balıkçı barınağı, havadan",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Yal%C4%B1_Bal%C4%B1k%C3%A7%C4%B1_Bar%C4%B1na%C4%9F%C4%B1_10.jpg",
     "yazar": "BSRF",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "BSRF · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p501.jpg",
     "ad": "Hazır giyim atölyesinde çalışan kadınlar",
     "konu": "Hazır giyim atölyesinde çalışan kadınlar",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Garment_factory_in_Bangladesh_Women_working.jpg",
     "yazar": "Tareq Salahuddin from Dhaka, Bangladesh",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Tareq Salahuddin from Dhaka, Bangladesh · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p502.jpg",
     "ad": "Ataşehir'de İstanbul Finans Merkezi gökdelenleri",
     "konu": "Ataşehir'de İstanbul Finans Merkezi gökdelenleri",
     "kategori": "Kadın",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Finans_Merkezi.jpg",
     "yazar": "Ail Subway",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Ail Subway · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p503.jpg",
     "ad": "Türkiye Cumhuriyet Merkez Bankası Denizli Şubesi cephesi",
     "konu": "Türkiye Cumhuriyet Merkez Bankası Denizli Şubesi cephesi",
     "kategori": "Finans",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:T%C3%BCrkiye_Cumhuriyet_Merkez_Bankas%C4%B1_Denizli_%C5%9Eubesi_01.jpg",
     "yazar": "Biologg",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Biologg · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p600.jpg",
     "ad": "Deicing of an aircraft propeller in Växjö",
     "konu": "Deicing of an aircraft propeller in Växjö",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Deicing_of_an_aircraft_propeller_in_V%C3%A4xj%C3%B6.jpg",
     "yazar": "Sendelbach (talk)",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Sendelbach (talk) · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p601.jpg",
     "ad": "Iskenderun Central Bank building 6639",
     "konu": "Iskenderun Central Bank building 6639",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Iskenderun_Central_Bank_building_6639.jpg",
     "yazar": "Dosseman",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Dosseman · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p602.jpg",
     "ad": "2014-11-13 07 55 15 Elko city snow plow along Lamoille Highway (Nevada State Route 227) in Elko, Nevada",
     "konu": "2014-11-13 07 55 15 Elko city snow plow along Lamoille Highway (Nevada State Route 227) in Elko, Nevada",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:2014-11-13_07_55_15_Elko_city_snow_plow_along_Lamoille_Highway_(Nevada_State_Route_227)_in_Elko,_Nevada.JPG",
     "yazar": "Famartin",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Famartin · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p603.jpg",
     "ad": "Television Outside Broadcast Unit (8724322710)",
     "konu": "Television Outside Broadcast Unit (8724322710)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Television_Outside_Broadcast_Unit_(8724322710).jpg",
     "yazar": "John K  Thorne from Dor",
     "lisans": "CC0",
     "lisans_adresi": "https://creativecommons.org/publicdomain/zero/1.0",
     "atif": "John K  Thorne from Dor · CC0 · Wikimedia Commons"
    },
    {
     "dosya": "p604.jpg",
     "ad": "100 Turkish lira and 50 kuruş",
     "konu": "100 Turkish lira and 50 kuruş",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:100_Turkish_lira_and_50_kuru%C5%9F.jpg",
     "yazar": "Aykhan Zayedzadeh",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "Aykhan Zayedzadeh · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p605.jpg",
     "ad": "Reconstruction with a crane in front of mountains, Hatay, Turkey, 2024",
     "konu": "Reconstruction with a crane in front of mountains, Hatay, Turkey, 2024",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Reconstruction_with_a_crane_in_front_of_mountains,_Hatay,_Turkey,_2024.jpg",
     "yazar": "Middle East Minorities",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "Middle East Minorities · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p606.jpg",
     "ad": "Adana Yüreğir Kışla TOKİ Konutları 04",
     "konu": "Adana Yüreğir Kışla TOKİ Konutları 04",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Adana_Y%C3%BCre%C4%9Fir_K%C4%B1%C5%9Fla_TOK%C4%B0_Konutlar%C4%B1_04.jpg",
     "yazar": "Zeynel Cebeci",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Zeynel Cebeci · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p607.jpg",
     "ad": "Istanbul Grand Bazaar (52556647351)",
     "konu": "Istanbul Grand Bazaar (52556647351)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Istanbul_Grand_Bazaar_(52556647351).jpg",
     "yazar": "Nan Palmero from San Antonio, TX, USA",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Nan Palmero from San Antonio, TX, USA · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p608.jpg",
     "ad": "Theater Show",
     "konu": "Theater Show",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Theater_Show.jpg",
     "yazar": "Kurt Kaiser",
     "lisans": "CC0",
     "lisans_adresi": "https://creativecommons.org/publicdomain/zero/1.0",
     "atif": "Kurt Kaiser · CC0 · Wikimedia Commons"
    },
    {
     "dosya": "p609.jpg",
     "ad": "Hancock Whitney Bank, Carrollton Branch, New Orleans March 2026 - 4",
     "konu": "Hancock Whitney Bank, Carrollton Branch, New Orleans March 2026 - 4",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Hancock_Whitney_Bank,_Carrollton_Branch,_New_Orleans_March_2026_-_4.jpg",
     "yazar": "Infrogmation",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Infrogmation · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p610.jpg",
     "ad": "Hands typing on a vintage typewriter in a cozy workspace",
     "konu": "Hands typing on a vintage typewriter in a cozy workspace",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Hands_typing_on_a_vintage_typewriter_in_a_cozy_workspace.jpg",
     "yazar": "Shixart1985",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Shixart1985 · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p611.jpg",
     "ad": "Flames in the dark",
     "konu": "Flames in the dark",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Flames_in_the_dark.jpg",
     "yazar": "Upcomingphotographerscorner",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Upcomingphotographerscorner · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p612.jpg",
     "ad": "Anıtkabir in November 2025",
     "konu": "Anıtkabir in November 2025",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:An%C4%B1tkabir_in_November_2025.jpg",
     "yazar": "Mehman",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Mehman · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p613.jpg",
     "ad": "Turkish flag 3705",
     "konu": "Turkish flag 3705",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Turkish_flag_3705.jpg",
     "yazar": "User:Darwinek",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "User:Darwinek · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p614.jpg",
     "ad": "2023-01-14 Newsroom ARD-aktuell (tagesschau)",
     "konu": "2023-01-14 Newsroom ARD-aktuell (tagesschau)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:2023-01-14_Newsroom_ARD-aktuell_(tagesschau).jpg",
     "yazar": "User:Wikiuka (Wikimedia)",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "User:Wikiuka (Wikimedia) · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p615.jpg",
     "ad": "Şükrü Saracoğlu Stadium 22012017",
     "konu": "Şükrü Saracoğlu Stadium 22012017",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:%C5%9E%C3%BCkr%C3%BC_Saraco%C4%9Flu_Stadium_22012017.jpg",
     "yazar": "Sakhalinio",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Sakhalinio · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p616.jpg",
     "ad": "Tüpraş Stadyumu 20231011 1",
     "konu": "Tüpraş Stadyumu 20231011 1",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:T%C3%BCpra%C5%9F_Stadyumu_20231011_1.jpg",
     "yazar": "Beşiktaş JK",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Beşiktaş JK · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p617.jpg",
     "ad": "Gola Speedster soccer shoes 20200501 001",
     "konu": "Gola Speedster soccer shoes 20200501 001",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Gola_Speedster_soccer_shoes_20200501_001.jpg",
     "yazar": "Methem (Mikko J. Putkonen)",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "Methem (Mikko J. Putkonen) · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p618.jpg",
     "ad": "Tüpraş Stadyumu 20231011 3",
     "konu": "Tüpraş Stadyumu 20231011 3",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:T%C3%BCpra%C5%9F_Stadyumu_20231011_3.jpg",
     "yazar": "Beşiktaş JK",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Beşiktaş JK · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p619.jpg",
     "ad": "Levent At Night (159321869)",
     "konu": "Levent At Night (159321869)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Levent_At_Night_(159321869).jpeg",
     "yazar": "Giuseppe Pinto",
     "lisans": "CC BY-SA 3.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/3.0",
     "atif": "Giuseppe Pinto · CC BY-SA 3.0 · Wikimedia Commons"
    },
    {
     "dosya": "p620.jpg",
     "ad": "Gold ingot and bar of Banque de France",
     "konu": "Gold ingot and bar of Banque de France",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Gold_ingot_and_bar_of_Banque_de_France.jpg",
     "yazar": "Ibex73",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "Ibex73 · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p621.jpg",
     "ad": "Galata tower with snow",
     "konu": "Galata tower with snow",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Galata_tower_with_snow.jpg",
     "yazar": "Melih1969",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Melih1969 · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p622.jpg",
     "ad": "Sea Storm (41283179412)",
     "konu": "Sea Storm (41283179412)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Sea_Storm_(41283179412).jpg",
     "yazar": "João Dias from Lisboa, Portugal",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "João Dias from Lisboa, Portugal · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p623.jpg",
     "ad": "Aegean Sea (MODIS 2017-07-04)",
     "konu": "Aegean Sea (MODIS 2017-07-04)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Aegean_Sea_(MODIS_2017-07-04).jpg",
     "yazar": "Jeff Schmaltz, MODIS Land Rapid Response Team, NASA GSFC",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": "Jeff Schmaltz, MODIS Land Rapid Response Team, NASA GSFC · Public domain · Wikimedia Commons"
    },
    {
     "dosya": "p624.jpg",
     "ad": "ŞH-Fatih approaching Eminönü Ferry Terminal, March 2024 05",
     "konu": "ŞH-Fatih approaching Eminönü Ferry Terminal, March 2024 05",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:%C5%9EH-Fatih_approaching_Emin%C3%B6n%C3%BC_Ferry_Terminal,_March_2024_05.jpg",
     "yazar": "Calistemon",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Calistemon · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p625.jpg",
     "ad": "Behind the clouds, the lights of Ankara city",
     "konu": "Behind the clouds, the lights of Ankara city",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Behind_the_clouds,_the_lights_of_Ankara_city.jpg",
     "yazar": "DilaverPhoto",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "DilaverPhoto · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p626.jpg",
     "ad": "IMG-TAI-TFX",
     "konu": "IMG-TAI-TFX",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:IMG-TAI-TFX.jpg",
     "yazar": "Dimir",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Dimir · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p627.jpg",
     "ad": "Microphones in SPNN Podcast studio-01",
     "konu": "Microphones in SPNN Podcast studio-01",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Microphones_in_SPNN_Podcast_studio-01.jpg",
     "yazar": "Myotus",
     "lisans": "CC BY 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/4.0",
     "atif": "Myotus · CC BY 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p628.jpg",
     "ad": "Headphones on wood in black and white (Unsplash)",
     "konu": "Headphones on wood in black and white (Unsplash)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Headphones_on_wood_in_black_and_white_(Unsplash).jpg",
     "yazar": "Corey Blaz blazphoto",
     "lisans": "CC0",
     "lisans_adresi": "https://creativecommons.org/publicdomain/zero/1.0",
     "atif": "Corey Blaz blazphoto · CC0 · Wikimedia Commons"
    },
    {
     "dosya": "p629.jpg",
     "ad": "Antakya Decorated buildings in 2008 16",
     "konu": "Antakya Decorated buildings in 2008 16",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Antakya_Decorated_buildings_in_2008_16.jpg",
     "yazar": "Dosseman",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "Dosseman · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p630.jpg",
     "ad": "Colored pen and smartphone on a table (Unsplash 36nRvt6EP2I)",
     "konu": "Colored pen and smartphone on a table (Unsplash 36nRvt6EP2I)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Colored_pen_and_smartphone_on_a_table_(Unsplash_36nRvt6EP2I).jpg",
     "yazar": "Gabriel Santiago gabrielssantiago",
     "lisans": "CC0",
     "lisans_adresi": "https://creativecommons.org/publicdomain/zero/1.0",
     "atif": "Gabriel Santiago gabrielssantiago · CC0 · Wikimedia Commons"
    },
    {
     "dosya": "p631.jpg",
     "ad": "Blackboards – UNM Astrophysics",
     "konu": "Blackboards – UNM Astrophysics",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Blackboards_%E2%80%93_UNM_Astrophysics.JPG",
     "yazar": "Anthony J. Bentley",
     "lisans": "Public domain",
     "lisans_adresi": "",
     "atif": "Anthony J. Bentley · Public domain · Wikimedia Commons"
    },
    {
     "dosya": "p632.jpg",
     "ad": "Playing with colorful building blocks and toys on the floor in a cozy indoor setting",
     "konu": "Playing with colorful building blocks and toys on the floor in a cozy indoor setting",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Playing_with_colorful_building_blocks_and_toys_on_the_floor_in_a_cozy_indoor_setting.jpg",
     "yazar": "Shixart1985",
     "lisans": "CC BY 2.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by/2.0",
     "atif": "Shixart1985 · CC BY 2.0 · Wikimedia Commons"
    },
    {
     "dosya": "p633.jpg",
     "ad": "Convex lens (magnifying glass) and upside-down image",
     "konu": "Convex lens (magnifying glass) and upside-down image",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:Convex_lens_(magnifying_glass)_and_upside-down_image.jpg",
     "yazar": "AntanO",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "AntanO · CC BY-SA 4.0 · Wikimedia Commons"
    },
    {
     "dosya": "p634.jpg",
     "ad": "PalaceOfJusticeIstanbul (1)",
     "konu": "PalaceOfJusticeIstanbul (1)",
     "kategori": "Durumlar",
     "kaynak": "Wikimedia Commons",
     "sayfa": "https://commons.wikimedia.org/wiki/File:PalaceOfJusticeIstanbul_(1).jpg",
     "yazar": "CeeGee",
     "lisans": "CC BY-SA 4.0",
     "lisans_adresi": "https://creativecommons.org/licenses/by-sa/4.0",
     "atif": "CeeGee · CC BY-SA 4.0 · Wikimedia Commons"
    }
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
   "acik": false,
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
   "acik": false,
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
   "ikon": "fa-brands fa-x-twitter",
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
   "ikon": "fa-brands fa-facebook",
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
   "ikon": "fa-brands fa-linkedin",
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
   "ikon": "fa-brands fa-instagram",
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
   "ikon": "fa-brands fa-telegram",
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
  },
  {
   "id": "threads",
   "ad": "Threads",
   "ikon": "fa-brands fa-threads",
   "acik": true,
   "tur": "yazi",
   "resmi_yol": "Threads API (Meta)",
   "oranlar": [
    "1:1",
    "4:5",
    "serbest"
   ],
   "editor": {
    "sinir": 500,
    "araclar": [
     "emoji",
     "etiket",
     "kisi",
     "link"
    ],
    "not": "Bağlantı önizleme kartı açar · gönderi başına bir konu etiketi",
    "dogrulanacak": [
     "konu etiketi sayısı (gönderi başına 1)",
     "görsel oranları"
    ]
   }
  },
  {
   "id": "bluesky",
   "ad": "Bluesky",
   "ikon": "fa-brands fa-bluesky",
   "acik": true,
   "tur": "yazi",
   "resmi_yol": "AT Protocol API",
   "oranlar": [
    "16:9",
    "1:1",
    "serbest"
   ],
   "editor": {
    "sinir": 300,
    "araclar": [
     "emoji",
     "etiket",
     "kisi",
     "link"
    ],
    "not": "300 karakter · bağlantı kartı açar · en fazla 4 görsel",
    "dogrulanacak": [
     "görsel sayısı (4)",
     "bağlantının karakter sayımı"
    ]
   }
  },
  {
   "id": "youtube-shorts",
   "ad": "YouTube Shorts",
   "ikon": "fa-brands fa-youtube",
   "acik": true,
   "tur": "video",
   "resmi_yol": "YouTube Data API",
   "oranlar": [
    "9:16"
   ],
   "editor": {
    "baslik_sinir": 100,
    "sinir": 5000,
    "araclar": [
     "emoji",
     "etiket",
     "link"
    ],
    "etiket_alani": true,
    "kapak_karesi": true,
    "not": "Dikey video · başlık 100, açıklama 5000 karakter",
    "dogrulanacak": [
     "en uzun süre (3 dk)",
     "etiket alanının toplam sınırı",
     "kapak karesinin API ile seçilebilmesi"
    ]
   }
  },
  {
   "id": "instagram-reels",
   "ad": "Instagram Reels",
   "ikon": "fa-brands fa-instagram",
   "acik": true,
   "tur": "video",
   "resmi_yol": "Instagram Graph API",
   "oranlar": [
    "9:16"
   ],
   "editor": {
    "sinir": 2200,
    "kesim": 125,
    "etiket_siniri": 30,
    "araclar": [
     "emoji",
     "etiket",
     "kisi"
    ],
    "link_yok": true,
    "kapak_karesi": true,
    "not": "Dikey video · açıklama 2200 karakter, ilk 125 karakter görünür · en fazla 30 etiket · açıklamadaki bağlantı tıklanmaz",
    "dogrulanacak": [
     "API ile en uzun süre",
     "kapak karesi (zaman konumu) desteği"
    ]
   }
  },
  {
   "id": "tiktok",
   "ad": "TikTok",
   "ikon": "fa-brands fa-tiktok",
   "acik": true,
   "tur": "video",
   "resmi_yol": "TikTok Content Posting API",
   "onay_gerekir": "Uygulama onayı gerekir",
   "oranlar": [
    "9:16"
   ],
   "editor": {
    "sinir": 2200,
    "araclar": [
     "emoji",
     "etiket",
     "kisi"
    ],
    "link_yok": true,
    "kapak_karesi": true,
    "not": "Dikey video · açıklama 2200 karakter · bağlantı tıklanmaz · uygulama onaylanana kadar gönderiler yalnız özel görünür",
    "dogrulanacak": [
     "açıklama sınırı (2200)",
     "en uzun süre",
     "onaysız uygulamada görünürlük kuralı"
    ]
   }
  }
 ],
 "sosyal_oranlar": [
  {
   "oran": "9:16",
   "ad": "Sosyal 9:16",
   "px": [
    1080,
    1920
   ]
  },
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
    "ust",
    "sutun"
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
    "periyot",
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
    "kapak",
    "periyot"
   ]
  },
  "multimedya.sesli": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "kusak",
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
    "tema",
    "slaytlar"
   ],
   "sistem": [
    "kapak",
    "kare-sayisi"
   ]
  },
  "multimedya.infografik": {
   "taslak": [
    "baslik"
   ],
   "yayin": [
    "baslik",
    "kategori",
    "veri-konusu",
    "gorsel",
    "veri-kaynagi",
    "donem"
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
