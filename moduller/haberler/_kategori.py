"""Haberler modülü · kategori ağacı (tek kaynak: public site araclar/kategori.json, yalnız okunur).

DADAHABER-10 §2: 8 ana kategori, açılır menüdeki sütunlar, sütunlardaki alt kategoriler. Üreticiler (_uret.py, _uret_d2.py)
ağacı buradan alır; elle yazılmış kopya tutulmaz. "Köşe" ağaçta yok (köşe yazıları kendi bölümünde).

Servis sayfası: ağaçta durur ama haber atanmaz (haber formundaki alt konu seçiminde çıkmaz). Liste tek yerde, modül kaydında:
moduller.json → haberler.ayarlar.servis_sayfalari (sutunlar: bütün öğeleri servis olan sütunlar; ogeler: tek tek servis sayfaları).
Kayıt yalnız okunur; Özel Widgetlar da aynı listeyi kullanır.
"""
import json, re
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KAYNAK = KOK.parent / "dadahaber-prototip" / "araclar" / "kategori.json"
_k = json.loads(KAYNAK.read_text(encoding="utf-8"))

_ss = next(m for m in json.loads((KOK / "moduller.json").read_text(encoding="utf-8"))["moduller"] if m["id"] == "haberler")["ayarlar"]["servis_sayfalari"]
SERVIS_SUTUN = set(_ss["sutunlar"])   # sütun adı (bütün öğeleri servis)
SERVIS_OGE = set(_ss["ogeler"])       # öğe adı ("Takımlar" = Spor › Servisler'deki sayfa; Takımlar SÜTUNUNDAKİ kulüpler normal)
RENK = {"Gündem": "gundem", "Spor": "spor", "Finans": "finans", "Kadın": "kadin", "Savunma": "savunma", "Dünya": "dunya", "Kampüs": "kampus", "Keşfet": "kesfet"}

def _adres(a): return re.sub(r"\.html$", "", a or "")

# AGAC: [{"ad", "slug", "ikon", "sutunlar": [{"ad", "ogeler": [{"ad", "slug", "servis"}]}]}]
AGAC = []
for b in _k["basliklar"]:
    AGAC.append({"ad": b["ad"], "slug": _adres(b["adres"]), "ikon": b.get("ikon", ""), "aciklama": b.get("aciklama", ""),
                 "sutunlar": [{"ad": s["ad"], "ogeler": [{"ad": o["ad"], "slug": _adres(o["adres"]),
                                                         "servis": o["ad"] in SERVIS_OGE or s["ad"] in SERVIS_SUTUN}
                                                        for o in s["ogeler"]]} for s in b["sutunlar"]]})

ANALAR = [b["ad"] for b in AGAC]
# haber atanabilen alt kategoriler (haber formlarının alt konu havuzu)
ALTLAR = {b["ad"]: [o["ad"] for s in b["sutunlar"] for o in s["ogeler"] if not o["servis"]] for b in AGAC}
# bütün alt kategoriler (servis dahil; Kategoriler ağacı)
TUM_ALTLAR = {b["ad"]: [o["ad"] for s in b["sutunlar"] for o in s["ogeler"]] for b in AGAC}
SUTUNLAR = {b["ad"]: [s["ad"] for s in b["sutunlar"]] for b in AGAC}
SERVIS_SAYI = sum(1 for b in AGAC for s in b["sutunlar"] for o in s["ogeler"] if o["servis"])
ALT_SAYI = sum(len(v) for v in TUM_ALTLAR.values())

# biçim (DADAHABER-10 §3): site örnek verisindeki `tur` → panel biçim kimliği; yoksa haber
TURLER = _k.get("turler", {})
